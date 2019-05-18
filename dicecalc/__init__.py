from dicecalc import tdop, tokenizer

# __all__ = ["tdop", "tokenizer"]

"""An example of usage:
	from dicecalc import calc
	rollResult = calc('2d20')
"""

def calc(expression):
	return  tdop.parse(tokenizer.tokenize(expression))