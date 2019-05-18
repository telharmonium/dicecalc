# A Dice Calculator in Python

A tokenizer and parser for calculating the results of (unnecessarily complex?) dice expressions such as `2d20 + 2` or `2d4(3d2)+9`

## Example Usage
Calculate the result of rolling 2 d20 dice, then adding 2 to that result:
`python roll.py "2d20 + 2"`

Do the same as the above, but output a dictionary describing the results of each individual roll, and how the dice expression was tokenized:
`python roll.py -v "2d20 + 2"`


# Notes on the Operation of this Parser
This is a hopefully a Top Down Operational Precedence Parser, also known as a Pratt-style parser.

## Collected Links on TDOP Parsers:

### General
* Pratt himself participated [in this discussion of his technique on Reddit](http://www.reddit.com/r/programming/comments/g7892/expression_parsing_made_easy_if_recursive_descent/)
* Two really good resources with diagrams showing the operation of a Pratt Parser:
    * [https://github.com/joyjding/spot](https://github.com/joyjding/spot)
    * [http://l-lang.org/blog/TDOP---Pratt-parser-in-pictures/](http://l-lang.org/blog/TDOP---Pratt-parser-in-pictures/)
    (The second link above is especially great.)

### Python Specific
* A relatively simplified [introduction to the subject](http://eli.thegreenplace.net/2010/01/02/top-down-operator-precedence-parsing/d1), in Python.  My implementation started here.
* A [much more complex article](http://effbot.org/zone/simple-top-down-parsing.htm) in Python

### Javascript Specific
* [Crockford's seminal article](http://javascript.crockford.com/tdop/tdop.html) on Top Down Operator Precedence
* This project [implements a trop equation parser in javascript](https://github.com/kevinmehall/EquationExplorer/blob/master/tdop_math.js)
* While [this uses a modified version](https://github.com/kevinmehall/EquationExplorer/blob/master/tokens.js) of Crockford's tokenizer
* An [article on writing a tokenizer](http://ariya.ofilabs.com/2011/08/math-evaluator-in-javascript-part1.html) (lexer) in javascript


## How This Project Works, In General:
The expression should be passed into `tokenizer`, which will attempt to identify meaningful tokens out of it.  These tokens will become dictionaries containing their Type and their Value.
At the moment there are only two Types: 
```
number
operator
```

If the tokenizer doesn't like the looks of part of the expression, it will create a token as usual, but attach these error flags to it:
```
errorType
errorMsg
```

**Note:** I've modified two variable names from the way they're traditionally used in a TDOP parser:
`tokenAsPrefix` is usually called `nud` for null denotation.
`tokenAsInfix` is usually called `led` for left denotation.


Tokenizer will return a dictionary with a list of these token dicts which is intended to be passed straight into `tdop`.

`tdop` creates a generator, `tokenMapper()`, which will, upon each call, yield an instance of appropriate class for that token, be it operator or literal number.
    
The magic all hapens in `expression()`, which calls `tokenAsPrefix()` or `tokenAsInfix()` on the currently active token instance, and determines the order of operations between tokens according to the passed in `rightBindingPower` and the token's innate `leftBindingPower`.

If an error was attached to a token by `tokenizer`, a `SyntaxError` will be raised by `tokenMapper()` when it reaches that token.  If an error occurs during an operation a different `SyntaxError` will be raised, and an error message attached to the token which triggered it, if appropriate.

These errors, if present, are caught, and and a dictionary is constructed for the return value. A successful return value might look like this for the expression `3 * 2d20`:

    {'diceRolls': [{'rolls': [15, 14], 'sides': 20, 'sum': 29}],
     'error': False,
     'errorCode': False,
     'origString': '3 * 2d20',
     'result': 87,
     'tokenized': [{'tokType': 'number', 'value': 3},
                   {'tokType': 'operator', 'value': '*'},
                   {'tokType': 'number', 'value': 2},
                   {'thisRoll': {'rolls': [15, 14], 'sides': 20, 'sum': 29},
                    'tokType': 'operator',
                    'value': 'd'},
                   {'rollResult': {'rolls': [15, 14], 'sides': 20, 'sum': 29},
                    'tokType': 'number',
                    'value': 20}]}


## Order of Operations Chart:

| TOKEN TYPE:             | LBP:        | prefix RBP      | infix RBP |
| ----------------------- | ----------- | --------------- | --------- |
| operator_dice_token     | 100         | 100             | 100 |
| operator_pow_token      | 30          | -               | 29 |
| operator_sub_token      | 10          | 25              | 10 |
| operator_mul_token      | 20          | -               | 20 |
| operator_div_token      | 20          | -               | 20 |
| operator_add_token      | 10          | -               | 10 |
| operator_lparen_token   | 11          | 0               | 20 |
| operator_rparen_token   | 0           | -               | - |
| end_token               | 0           | -               | - |
| literal_token           | -           | -               | - |


## A note on the operation of operator_lparen_token.tokenAsInfix():
As the infix form is performing multiplication, it should respect the order of operations. So, if the expression is of the form: 
    3(4+5)^2

we need to treat it as: 
    3*((4+5)^2)
rather than as:
    (3*(4+5))^2

Therefore, `operator_lparen_token.tokenAsInfix()` will first call `expression()` to collect and compute between ( and ) as it normally would, '(4+5)' in this case, with `expression()` returning when it hits )'s low lbp.

However, any following operators with higher precedence than multiplication, '^2' in this case, need to be sent the results of this computed expression **before** we perform the multiplication and return our result.  Essentially we need to work in this order:
    3(4+5)^2
    3(9)^2
    3*81
    return 243
    
Therefore we call `validateTokenAndCreateProxyLiteralToken()`, which will first ensure we've actually encountered ), and then instantiates a new `literal_token` object with the result of our parenthetical expression, '(4+5)', as its value.  This new token is then made the current value of the global token, and `expression()` is called again, essentially starting evaluation again, but beginning with the value resulting from '(4+5)', with the rbp of multiplication.
    
The result of this `expression()` is returned to `operator_lparen_token.tokenAsInfix()`, where it is multiplied with the left argument and returned up the chain.
