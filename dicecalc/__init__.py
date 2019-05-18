# Copyright 2019 Telharmonium. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from dicecalc import tdop, tokenizer

# __all__ = ["tdop", "tokenizer"]

"""An example of usage:
	from dicecalc import calc
	rollResult = calc('2d20')
"""

def calc(expression):
	return  tdop.parse(tokenizer.tokenize(expression))