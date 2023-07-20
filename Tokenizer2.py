import sys

class Tokenizer:

    def __init__(self, file):
        self. keywords = ['boolean', 'char', 'class', 'constructor', 'do', 'else', 'false', 'field',
                'function', 'if', 'int', 'let', 'method', 'null', 'return', 'static', 'this',
                'true', 'var', 'void', 'while']
        self.symbols = '{}()[].,;+-*/&|<>=~'
        self.other = ':? '
        self.numberChars = '0123456789'
        self.identStart = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'
        self.identChars = self.identStart + self.numberChars
        self.special = {'<': '&lt;', '>': '&gt;', '"': '&quot;', '&': '&amp;'}
        self.tokens = self.getTokens(file)
        self.x = 0

        # input: String line; output: String of tokens
    def splitIntoParts(self, l):

        tokens = []
        num = ''
        word = ''

        conNumber = False   # create bools and word string
        stringCon = False
        inString = False

        for char in l:
            # ----------------- CONSTANT NUMBERS -----------------------
            # last char was in a number but this char is not
            if conNumber and char not in self.numberChars:
                conNumber = False
                tokens.append(num)

            # first number character (not in a string)
            elif char in self.numberChars and not conNumber and not inString:
                conNumber = True
                num = char

            # char is part of multichar constant
            elif conNumber and char in self.numberChars:
                num += char

            # ------------------ NORMAL STRINGS -------------------------
            # end of normal string
            if inString and char not in self.identChars:
                tokens.append(word)
                inString = False

            # first letter in a string
            elif char in self.identStart and not inString and not stringCon:
                inString = True
                word = char

            # char is apart of a string but its not first letter
            elif inString and char in self.identChars:
                word += char

            # ----------------- STRING CONSTANTS -----------------------
            # end of a string constant
            if char == '"' and stringCon:
                word += char
                tokens.append(word)
                stringCon = False

            # first letter in a string constant
            elif char == '"' and not stringCon:
                stringCon = True
                word = char

            # char is apart of a string but its not first letter
            elif stringCon and (char in self.identStart or char in self.other or char in self.symbols):
                word += char

            # ----------------- SYMBOLS -------------------------------
            if char in self.symbols and not stringCon:
                tokens.append(char)

        return tokens

    def getTokens(self, file):

        result = []  # create string to store result
        isComment = False    # boolean for multi line comments

        for line in file:
            line.strip()     # get rid of whitespaces

            if "/**" in line:
                isComment = True
                result.extend(self.splitIntoParts(line.split('/**')[0]))
            elif isComment and "*/" in line:   # remove comments
                isComment = False
                result.extend(self.splitIntoParts(line.split('*/')[1]))
            elif "//" in line:
                result.extend(self.splitIntoParts(line.split('//')[0]))
            else:
                result.extend(self.splitIntoParts(line))

        return result
    
    # hasMoreTokens() - returns a boolean
    def hasMoreTokens(self):
        hasMore = True
        if self.x >= len(self.tokens):
            hasMore = False
        return hasMore
    
    # advance() - advances to the next token
    def advance(self):
        self.x += 1
    
    # tokenType() - returns the type of the current token
    def tokenType(self):
        token = self.tokens[self.x]
        type = ''

        for x in token:
            if x in self.numberChars:
                type = 'integerConstant'
            else:
                break
        
        if token in self.keywords:
            type = 'keyword'
        elif token in self.symbols:
            type = 'symbol'
        elif token[0] == '"':
            type = 'stringConstant'
        elif type != 'integerConstant':
            type = 'identifier'
        
        return type

    # token() - returns the current token
    def token(self):
        token = self.tokens[self.x]
        
        if self.tokenType() == 'stringConstant':
            token = token.replace('"', '')
        elif token in self.special:
            token = self.special[token]
        return token
    
    def getNext(self):
        nToken = self.tokens[self.x + 1]
        
        if nToken[0] == '"':
            nToken = nToken.replace('"', '')
        elif nToken in self.special:
            nToken = self.special[nToken]
        return nToken

def main():
    input = sys.argv[1]
    file = open(input, 'r') 

    test = Tokenizer(file)  # create instance of Tokenizer class using input file
    type = ''
    token = ''

    # write to .xml file
    sys.stdout = open(input.split('.')[0] + 'T.xml', 'wt')
    
    # use Tokenizer functions to print out xml line by line
    print('<tokens>')
    while test.hasMoreTokens():
        type = test.tokenType()
        token = test.token()
        print('<' + type + '> ' + token + ' </' + type + '>')
        test.advance()
    print('</tokens>')

if __name__ == "__main__":
    main()
