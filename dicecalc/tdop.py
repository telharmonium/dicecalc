from __future__ import division
import math
import random

# NOTE:
# In other projects tokenAsPrefix is sometimes called nud for null denotation.
# In other projects tokenAsInfix is sometimes called led for left denotation.

# A custom error class; exists only to allow raising of errors during parsing.
class SyntaxError(Exception):
    pass

def roll(quantity, diceVal):
    """Accepts two values.  First value is an int representing the number 
    of dice being rolled, the second is an int representing the number 
    of sides these dice have. 
    Returns a list containing each roll result as an individual value.
    An empty list indicates an error."""
    rolls = []
    try:
        numRolls = int(quantity)
        numSides = int(diceVal)
        if numRolls <= 0:
            rolls.append(0)
        elif numSides <= 0:
            for die in range(numRolls):
                rolls.append(0)
        else:
            for die in range(numRolls):
                rolls.append(random.randint(1, numSides))
        return rolls
    except:
        return rolls

def expression(rightBindingPower=0):
    # lastToken will contain the right-most token in a given expression block. 
    # In 3d20, lastToken = 20.  In 3d(2d6), lastToken = ), and so forth.
    global token, lastToken
    lastToken = token
    curToken = token
    try: # Catch StopIteration error from next() calls.
        token = next()
        left = curToken.tokenAsPrefix()
        while rightBindingPower < token.leftBindingPower:
            curToken = token
            token = next()
            left = curToken.tokenAsInfix(left)
            lastToken = token
    except AttributeError:
        lastToken.parentToken['errorType'] = 'badOp'
        lastToken.parentToken['errorMsg'] = 'Unexpected value'
        raise SyntaxError("Unexpected value in expression")
    except StopIteration:
        raise SyntaxError("Unexpected end of expression")
    return left

class literal_token(object):
    def __init__(self, value, parentToken):
        self.value = value
        self.parentToken = parentToken
    def tokenAsPrefix(self):
        return self.value

class operator_add_token(object):
    leftBindingPower = 10
    def __init__(self, parentToken):
        self.parentToken = parentToken
    def tokenAsInfix(self, left):
        return left + expression(10)

class operator_mul_token(object):
    leftBindingPower = 20
    def __init__(self, parentToken):
        self.parentToken = parentToken
    def tokenAsInfix(self, left):
        return left * expression(20)

class operator_div_token(object):
    leftBindingPower = 20
    def __init__(self, parentToken):
        self.parentToken = parentToken
    def tokenAsInfix(self, left):
        try:
            return left / expression(20)
        except ZeroDivisionError:
            self.parentToken['errorType'] = 'badOp'
            self.parentToken['errorMsg'] = 'Cannot divide by zero.'
            raise SyntaxError("Cannot divide by zero.")

class operator_pow_token(object):
    leftBindingPower = 30
    def __init__(self, parentToken):
        self.parentToken = parentToken
    def tokenAsInfix(self, left):
        return left ** expression(self.leftBindingPower - 1)

class operator_sub_token(object):
    leftBindingPower = 10
    def __init__(self, parentToken):
        self.parentToken = parentToken
    def tokenAsPrefix(self):
        return -expression(25)
    def tokenAsInfix(self, left):
        return left - expression(10)

class operator_dice_token(object):
    leftBindingPower = 100
    def __init__(self, parentToken, mainRollList):
        self.parentToken = parentToken
        self.mainRollList = mainRollList # To add roll results to the main roll list.
    def tokenAsPrefix(self):
        dieSides = expression(100)
        rollList = roll(1, dieSides)
        thisRoll = {
            "sides": dieSides,
            "rolls": rollList,
            "sum": rollList[0]
        }
        self.parentToken['thisRoll'] = thisRoll
        # Attach the roll dict to the token which ended the dice expression.
        # For example, the ) in 6d(3d4 + 3).
        lastToken.parentToken['rollResult'] = thisRoll
        self.mainRollList.append(thisRoll)
        return rollList[0]
    def tokenAsInfix(self, left):
        dieSides = expression(100)
        rollList = roll(left, dieSides)
        rollTotal = sum(rollList)
        thisRoll = {
            "sides": dieSides,
            "rolls": rollList,
            "sum": rollTotal
        }
        self.parentToken['thisRoll'] = thisRoll
        lastToken.parentToken['rollResult'] = thisRoll
        self.mainRollList.append(thisRoll)
        return rollTotal

class operator_lparen_token(object):
    leftBindingPower = 20 # Should match lbp of * & / operators.
    def __init__(self, parentToken):
        self.parentToken = parentToken
    def tokenAsPrefix(self):
        expr = expression() # Collect the enclosed expression up to next ).
        validateClosingTokenAndConsume(operator_rparen_token, ')', self) # Check for ), advance to next token.
        return expr # Return the expression we gathered from between ( and ).
    def tokenAsInfix(self, left):
        expr = expression() # Collect the enclosed expression up to next ).
        # Check for higher-precedent infix operators following ) and get the 
        # results of that expression.
        result = validateClosingTokenAndCreateProxyLiteralToken(operator_rparen_token, ')', self, expr, 20)
        return left * result # Perform multiplication against result.

class operator_rparen_token(object):
    def __init__(self, parentToken):
        self.parentToken = parentToken
    leftBindingPower = 0

class end_token(object):
    leftBindingPower = 0

# expectedClosingToken is the token class we're looking to consume.
# expectedClosingTokenStr is a string representing that token.  
# callingToken is a reference to the token instance which called this 
# function, so we can attach an error to it.
def validateClosingTokenAndConsume(expectedClosingToken=None, expectedClosingTokenStr='', callingToken=None):
    global token
    if expectedClosingToken and expectedClosingToken != type(token):
        if callingToken:
            callingToken.parentToken['errorType'] = 'badOp'
            callingToken.parentToken['errorMsg'] = 'Missing %s' % expectedClosingTokenStr
        raise SyntaxError('Expected %s' % expectedClosingTokenStr)
    token = next()

def validateClosingTokenAndCreateProxyLiteralToken(expectedClosingToken=None, expectedClosingTokenStr='', callingToken=None, proxyTokenValue=0, rightBindingPower=0):
    global token
    if expectedClosingToken and expectedClosingToken != type(token):
        if callingToken:
            callingToken.parentToken['errorType'] = 'badOp'
            callingToken.parentToken['errorMsg'] = 'Missing %s' % expectedClosingTokenStr
        raise SyntaxError('Expected %s' % expectedClosingTokenStr)
    token = literal_token(proxyTokenValue, {"tokType": "number", "value": proxyTokenValue}) # Set passed-in value as value of new global current token.
    return expression(rightBindingPower)

# Map tokens to the objects which define their behavior.
# This creates a generator used to iterator over the tokenList.
def tokenMapper(tokenList, diceRollsMasterList):
    for t in tokenList:
        if 'errorType' in t:
            raise SyntaxError(t['errorMsg']) # Stop execution and report this token's attached error message.
        elif t['tokType'] == "number":
            yield literal_token(t['value'], t)
        elif t['tokType'] == "operator":
            operator = t['value']
            if operator == "+":
                yield operator_add_token(t)
            elif operator == "-":
                yield operator_sub_token(t)
            elif operator == "*":
                yield operator_mul_token(t)
            elif operator == "/":
                yield operator_div_token(t)
            elif operator == "^":
                yield operator_pow_token(t)
            elif operator == '(':
                yield operator_lparen_token(t)
            elif operator == ')':
                yield operator_rparen_token(t)
            elif operator == 'd' or operator == 'D':
                yield operator_dice_token(t, diceRollsMasterList)
        else: # This is unlikely to happen.
            raise SyntaxError('Unknown operator: %s', t['value'])
    yield end_token()

def parse(tokenized):
    global token, next
    diceRolls = [] # Will contain the roll dicts.
    error = False
    errorCode = False
    next = tokenMapper(tokenized['tokenList'], diceRolls).next # A generator
    try:
        token = next() # Get the first token.
        result = expression() # expression() actually starts the parsing.
        # If the fractional part is not 0, round to <= 3 decimal places.
        if not math.modf(result)[0] == 0: 
            result = round(result, 3)
        else: # Otherwise, make sure it doesn't show the '.0'
            result = int(result)
    except SyntaxError, e:
        error = True
        errorCode = str(e)
        result = 0
    except: # Catch unanticipated errors.
        error = True
        errorCode = "Unable to parse expression."
        result = 0
    return {
        "error": error,
        "errorCode": errorCode,
        "result": result,
        "origString": tokenized['origString'],
        "diceRolls": diceRolls,
        "tokenized": tokenized['tokenList']
    }
