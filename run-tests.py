# Copyright 2019 Telharmonium. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import unittest
import dicecalc

class ExpressionsCase(unittest.TestCase):
    """Test various expressions."""

    # These lists contain an expression followed by the expected result.

    basicExpressionsList = [
        ('3', 3),
        ('-3', -3),
        ################################ 
        # Addition
        ('3 + 0', 3),
        ('3 + 2', 5),
        ('-3 + 2', -1),
        ('3 + -2', 1),
        ('-3 + -2', -5),
        ################################ 
        # Subtraction
        ('3 - 0', 3),
        ('3 - 2', 1),
        ('3 - 5', -2),
        ('-3 - 2', -5),
        ('-3 - -2', -1),
        ('3 - -2', 5),
        ################################ 
        # Multiplication
        ('3 * 1', 3),
        ('3 * 0', 0),
        ('3 * 2', 6),
        ('3 * 6', 18),
        ('-3 * 2', -6),
        ('3 * -2', -6),
        ('-3 * -2', 6),
        ################################ 
        # Division
        # ('3 / 0', 'Error!'),
        ('3 / 2', 1.5),
        ('6 / 1', 6),
        ('6 / 6', 1),
        ('6 / 3', 2),
        ('-6 / 3', -2),
        ('-6 / -3', 2),
        ('6 / -3', -2),
        ################################ 
        # Exponentiation
        ('0^2', 0),
        ('0^0', 1),
        ('3^0', 1),
        ('3^1', 3),
        ('3^2', 9),
        # Note: '-3^2' should return -9, or at least it should if we interpret the 
        # expression algebraically. 
        # Essentially, the order of operations requires that exponentiation 
        # comes BEFORE the unary negation.
        # Here are some URLs:
        #   http://macnauchtan.com/pub/precedence.html#_index
        #   http://mathforum.org/library/drmath/view/55713.html
        #   http://mathforum.org/library/drmath/view/53194.html
        #   http://www.purplemath.com/modules/negative4.htm
        # Therefore -3^2 means -(3^2) or -(3 * 3)
        ('-3^2', -9),
        # This next expression is essentially how -3^2 should be interpreted.
        ('-(3^2)', -9),
        # Whereas this one is what we might intuitively expect -3^2 to mean.  
        # This means variables will need to always be wrapped in parentheses.
        ('(-3)^2', 9),
        ('-3^3', -27),
        ################################ 
        # Parentheses
        ('(3)', 3),
        ('(-3)', -3),
        ('-(3)', -3),
        ('2(3)', 6),
        ('-2(3)', -6),
        ('-2(-3)', 6),
        ('2(-3)', -6),
        ('-(-3 * -3)', -9),
        ('(-3 * 3)', -9),
        ('-(-3 * 3)', 9),
        # The missing opening ( looks like an error, but the system doesn't care.
        ('2 + 2)', 4),
        ################################ 
        ################################ 
        # Decimals
        ('.3', .3),
        ('-.3', -.3),
        ('.3 + 0', .3),
        ('.3 + -.2', .1),
        ('.3 + .2', .5),
        ('.3 - -.2', .5),
        ('3 * .1', .3),
        ('-3 * -.1', .3),
        ('3 / 2', 1.5),
        ('3 / .1', 30),
        ('.2^3', .008),
        ('3^-3', 0.037),
        ('(.3)', .3),
        ('(-.3)', -.3),
        ('-(.3)', -.3),
        ('2(.3)', .6),
        ('-2(.3)', -.6),
        ('-2(-.3)', .6),
        ('2(-.3)', -.6),
        ('-(-3 * -.3)', -.9),
        ('(-3 * .3)', -.9),
        ('-(-3 * .3)', .9),
        ################################ 
        # Combinations
        ('2 + 5 + 3 / 1', 10),
        ('3 + 10 * 2 * 4 + 5', 88),
        ('3 + 10 / 2 - 3 * 4 + 15', 11),
        ('5(2 + 4)', 30),
        ('-5(2 + 4)', -30),
        ('3 + (4 / 2) - (3 * 4)', -7),
        ('3 - (2 + 4) * -5', 33),
        ('3 * (2 + 4) - 5', 13),
        ('6 / (2 + 4) - 5', -4),
        ('3 * 4((4 - 2) * 3)', 72), 
        ('3 * 4(((4 - 2) * 3)^2)', 432),
        ('3(4+5)^2', 243),
        ('3 * 4 * ((4 - 2) * 3)^2', 432),
        ('3 * -((3 - 2) - 5)', 12),
        ('3 * -((3 - 2) - 5) * 2', 24),
        ('-3 * -((3 - 2) - 5)^2', 48),
        ('3 * -((3 - 2) - 5)^2', -48),
        ('3 * -((3 - 2) - 5)^3', 192),
        ('45^2 + (3 * 2)', 2031),
        ('45^3 * 3', 273375),
        ('3 * 45^3', 273375),
        ('(45^3)(3)', 273375),
        ('3(45^3)', 273375),
        ('3 * 45^3', 273375),
        ('45^1+2', 47),
        ('45^3*2', 182250),
        ('1 + 3(9 + 1 * 2)', 34),
        ('10 * 3(9 + 1 * 2)', 330),
        ('2 + 3(5+5)', 32),
        ('2 + 3 * (5+5)', 32),
        ('3 * 4((4 - 2) * 3)^2', 432),
        ('4((4 - 2) * 3)^2', 144),
        ('4(2 * 3)^2', 144),
        ('4(6)^2', 144),
        ('4(6)*3', 72),
        ('4(6)^2 + 2', 146),
        ('4(6)^2 * 2', 288),
        ('4(-6)^2 + 2', 146),
        ('4(-6)^3 + 2', -862),
        ('4(6 - 12)^2 * 2', 288),
        ('4(6 - 12)^3 * 2', -1728)
    ]

    errorExpressionsList = [
        ('2 *', 'Unexpected end of expression', False),
        ('(2 *', 'Unexpected end of expression', False),
        ('(2', 'Expected )', 0, 'Missing )'),
        ('(2 * )', 'Unexpected value in expression', 3, 'Unexpected value'),
        ('+ 2', 'Unexpected value in expression', 0, 'Unexpected value'),
        ('()', 'Unexpected value in expression', 1, 'Unexpected value'),
        ('(2 * -', 'Unexpected end of expression', False),
        ('(1 - 3 + (2 *', 'Unexpected end of expression', False),
        ('(1 - 3 + (2 * 4 / 2', 'Expected )', 5, 'Missing )'),
        ('(1 - 3) + (2 * 4 / 2', 'Expected )', 6, 'Missing )'),
        ('(2 * 5 7', 'Unexpected value in expression', 3, 'Unexpected value'),
        ('2 * 5 7', 'Unexpected value in expression', 2, 'Unexpected value'),
        ('2 * pencil', 'Unrecognized characters', 2, 'Unrecognized characters'),
        ('pencil * 2', 'Unrecognized characters', 0, 'Unrecognized characters'),
        ('(pencil)', 'Unrecognized characters', 1, 'Unrecognized characters'),
        ('dice', 'Unrecognized characters', 1, 'Unrecognized characters'),
        # This expression should have two tokens flagged as bad numbers, in positions 2 and 4.
        ('5.2 + .6.3 + 0.4.3', 'Unrecognized number', 2, 'Unrecognized number'),
        # Therefore we'll check it twice.
        ('5.2 + .6.3 + 0.4.3', 'Unrecognized number', 4, 'Unrecognized number')
    ]

    # I don't care enough to build a comprehensive test of dice rolling.  
    # So, we'll just do some basic tests to verify that gross errors 
    # aren't present.

    diceExpressionsList = [
        {
            'expr': 'd20',
            'rolls': [
                {
                    'numRolls': 1,
                    'numSides': 20
                }
            ]
        },
        {
            'expr': '22d20',
            'rolls': [
                {
                    'numRolls': 22,
                    'numSides': 20
                }
            ]
        },
        {
            'expr': '2d4(3d2)',
            'rolls': [
                {
                    'numRolls': 2,
                    'numSides': 4
                },
                {
                    'numRolls': 3,
                    'numSides': 2
                }
            ]
        }
    ]


    def test_basic_expressions(self):
        """Test Basic Expressions."""
        for testExpression in self.basicExpressionsList:
            result = dicecalc.tdop.parse(dicecalc.tokenizer.tokenize(testExpression[0]))
            self.assertFalse(result['error'])
            self.assertEqual(result['result'], testExpression[1])

    def test_error_expressions(self):
        for errorExpression in self.errorExpressionsList:
            result = dicecalc.tdop.parse(dicecalc.tokenizer.tokenize(errorExpression[0]))
            self.assertEqual(result['errorCode'], errorExpression[1])
            # A nicely printed message here might be:
            # print 'Error: %s returned error code "%s", expected error code "%s"' % (errorExpression[0], result['errorCode'], errorExpression[1])
            if errorExpression[2]:
                self.assertEqual(result['tokenized'][errorExpression[2]]['errorMsg'], errorExpression[3])
                # A nicely printed message here might be:
                # print 'Error: %s did not attach correct error message to token %s' % (errorExpression[0], errorExpression[2])

    def test_dice_expressions(self):
        for rollExpression in self.diceExpressionsList:
            result = dicecalc.tdop.parse(dicecalc.tokenizer.tokenize(rollExpression['expr']))
            self.assertFalse(result['error'])
            # print 'Error: Expression %s returned a parse error: "%s" This is very unexpected.' % (rollExpression['expr'], result['errorCode'])
            self.assertEqual(len(result['diceRolls']), len(rollExpression['rolls']))
            # print 'Error: Expression %s did not result in the expected number of overall rolls.' % rollExpression['expr']
            for index in range(len(rollExpression['rolls'])):
                self.assertEqual(rollExpression['rolls'][index]['numRolls'], len(result['diceRolls'][index]['rolls']))
                # A nicely printed message here might be:
                # print 'Error: Expression %s - roll %s did not result in the expected number of rolls.' % (rollExpression['expr'], index)
                self.assertEqual(rollExpression['rolls'][index]['numSides'], result['diceRolls'][index]['sides'])
                # A nicely printed message here might be:
                # print 'Error: Expression %s - roll %s reported an incorrect number of sides.' % (rollExpression['expr'], index)
                for r in result['diceRolls'][index]['rolls']:
                    self.assertTrue(1 <= r and r <= rollExpression['rolls'][index]['numSides'])
                    # A nicely printed message here might be:
                    # print 'Error: Expression %s - roll %s contains a roll result beyond the defined number of sides.' % (rollExpression['expr'], index)


    """These are known problems."""
    # This consumes all available memory.
    # print tdop.parse(tokenizer.tokenize('4000000000000d200000'))

    ################################ 
    # More complex dice rolls for testing:
    # tokenized = tokenizer.tokenize('0d20') # Should = 0.
    # tokenized = tokenizer.tokenize('2d(2d6)')
    # tokenized = tokenizer.tokenize('(2d4)d(3d20)')
    # tokenized = tokenizer.tokenize('(2d4)d(3d20)^2d20')
    # tokenized = tokenizer.tokenize('(2d4)d((3d20)^2d20)')
    # pprint.pprint(tdop.parse(tokenized))

    ################################ 
    # These are currently working correctly:
    # print tdop.parse(tokenizer.tokenize('2 * 2d20'))["diceRolls"]
    # print tdop.parse(tokenizer.tokenize('2(2d20)'))["diceRolls"]
    # print tdop.parse(tokenizer.tokenize('2+4*2d20'))["diceRolls"]
    # print tdop.parse(tokenizer.tokenize('2+4(2d20)'))["diceRolls"]
    # print tdop.parse(tokenizer.tokenize('2d20 * (8 + 2)'))["diceRolls"]
    # print tdop.parse(tokenizer.tokenize('2d20(8 + 2)'))["diceRolls"]
    # print tdop.parse(tokenizer.tokenize('2d20^2'))["diceRolls"]
    # print tdop.parse(tokenizer.tokenize('2*2d20^2'))["diceRolls"]
    # print tdop.parse(tokenizer.tokenize('2(2d20)^2'))["diceRolls"]
    # print tdop.parse(tokenizer.tokenize('(2*2d20)^2'))["diceRolls"]
    # print tdop.parse(tokenizer.tokenize('(d4^d4)(4+6)'))["diceRolls"]
    # print tdop.parse(tokenizer.tokenize('(d4^2d4)(4+6)'))["diceRolls"]
    ################################ 
    # Some possibly deviant behavior:
    # Perhaps we should consider automatically performing multiplication
    # in this case?  Maybe as a reaction to raising an error?  Or perhaps not.
    # print parse('(1 + 9)2')


if __name__ == '__main__':
    unittest.main()