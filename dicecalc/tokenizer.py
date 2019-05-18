# Copyright 2019 Telharmonium. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

def getChar(expr, i):
	try:
		return (expr[i], i)
	except IndexError: # We've reached the end of the string.
		return (False, i)

def buildToken(tokType, value):
	return {
		'tokType': tokType,
		'value': value
	}

def tokenize(exprString):
	opList = ['+', '-', '*', '/', '^', '(', ')', 'd', 'D']
	collectedString = ""
	result = []
	hasError = False # Error canary.

	if not len(exprString) > 0: # No input, no parsing.
		return {
			'tokenList': [],
			'origString': exprString,
			'hasError': True
		}

	i = 0 # Current location in string.
	c = exprString[i] # Currently selected character.
	while c:
		 # The begins variable would track the start of each token in the 
		 # original expression string.  Including begins and i in the 
		 # returned buildToken object would let the caller know this location, 
		 # like this: result.append(buildToken('operator', c, begins, i)) 
		# begins = i
		if c <= ' ': # This is whitespace; ignore it.
			c, i = getChar(exprString, i+1) # Get next character.

		# Check for numbers and decimals.
		elif c == '.' or (c >= '0' and c <= '9'):
			collectedString = c # Clear any previous value, then store current character.
			i += 1
			# Look for additional numbers.
			while True: 
				c = getChar(exprString, i)[0]
				if c < '0' or c > '9':
					break
				i += 1
				collectedString += c
			# Look for a decimal, and numbers after the decimal.
			if c == '.':
				collectedString += c
				i += 1
				# Look for additional numbers.
				while True: 
					c = getChar(exprString, i)[0]
					if c != '.' and (c < '0' or c > '9'):
					# This would work also, but would serve to split 0.4.3 into 
					# 0.4 and .3, which isn't necessarily correct.
					# 	if c < '0' or c > '9':
						break
					i += 1
					collectedString += c
			# Validate that this is a number.
			try: # Is it an integer?
				validNum = int(collectedString)
			except ValueError:
				try: # Or perhaps a decimal?
					validNum = float(collectedString)
				except ValueError: # This is not a number.
					validNum = None
			if not validNum is None:
				#Add this number to the result array.
				result.append(buildToken('number', validNum))
			else:
				hasError = True
				# Add an error object instead.
				thisToken = buildToken('number', collectedString)
				thisToken['errorType'] = 'badNum'
				thisToken['errorMsg'] = 'Unrecognized number'
				result.append(thisToken)

		# Check for operators.
		elif c in opList:
			i += 1
			# Add this operator to the result array.
			result.append(buildToken('operator', c))
			c, i = getChar(exprString, i)

		# Currently unrecognized characters.
		else:
			hasError = True
			collectedString = c
			i += 1
			# Look for additional unrecognized characters.
			while True:
				c = getChar(exprString, i)[0]
				# This will need to be kept up to date.
				if not c or (c in opList or (c == '.' or (c >= '0' and c <= '9'))):
					break
				i += 1
				collectedString += c
			thisToken = buildToken('number', collectedString)
			thisToken['errorType'] = 'badChars'
			thisToken['errorMsg'] = 'Unrecognized characters'
			result.append(thisToken)

	# Return the array of collected tokens, the original expression and 
	# the error canary.  The error canary isn't currently being used.
	return {
		'tokenList': result,
		'origString': exprString,
		'hasError': hasError
	}

