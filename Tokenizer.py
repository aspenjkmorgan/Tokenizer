import sys

class Tokenizer:

    def __init__(t, f):
        t.f = f
        t.keywords = ['boolean', 'char', 'class', 'constructor', 'do', 'else', 'false', 'field',
            'function', 'if', 'int', 'let', 'method', 'null', 'return', 'static', 'this',
            'true', 'var', 'void', 'while']
        t.symbols = '{}()[].,;+-*/&|<>=~'
        t.numberChars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        t.identStart = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 
                        'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 
                        'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                        'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
                        'W', 'X', 'Y', 'Z', '_']
        t.identChars = t.identStart.extend(t.numberChars)
        t.special = {'<': '&lt;', '>': '&gt;', '"': '&quot;', '&': '&amp;'}
        t.x = 0 # counter
        t.allTokens = []
        t.getAllTokens(f)
    
    def getAllTokens(t, f):
        result =[]
        isComment = False
        for line in f:
            if isComment and "*/" in line:   # remove comments
                isComment = False
                if line.split('*/')[1] != '':
                    result.extend(t.splitIntoParts(line.split('*/')[1]))
            elif "/**" in line:
                isComment = True
                if line.split('/**')[0] != '':
                    result.extend(t.splitIntoParts(line.split('/**')[0]))
            elif "//" in line and line.split('//')[0] != '':
                result.extend(t.splitIntoParts(line.split('//')[0]))
            elif isComment == False:
                result.extend(t.splitIntoParts(line))

        t.allTokens.extend(result)

    def splitIntoParts(t, l):  # input: String line; output: String of tokens
        tokens = []
        num = ''
        word = ''

        conNumber = False   # create bools and word string
        stringCon = False
        inString = False

        for char in l:
            # ----------------- CONSTANT NUMBERS -----------------------
            # last char was in a number but this char is not
            if conNumber and char not in t.numberChars:
                conNumber = False
                tokens.append(num)

            # first number character (not in a string)
            elif char in t.numberChars and not conNumber and not inString:
                conNumber = True
                num = char

            # char is part of multichar constant
            elif conNumber and char in t.numberChars:
                num += char

            # ------------------ NORMAL STRINGS -------------------------
            # end of normal string
            if inString and char not in t.identChars:
                tokens.append(word)
                inString = False

            # first letter in a string
            elif char in t.identStart and not inString and not stringCon:
                inString = True
                word = char

            # char is apart of a string but its not first letter
            elif inString and char in t.identChars:
                word += char

            # ----------------- STRING CONSTANTS -----------------------
            # end of a string constant
            if char == '"' and stringCon:
                tokens.append(word)
                stringCon = False

            # first letter in a string constant
            elif char == '"' and not stringCon:
                stringCon = True
                word = char

            # char is apart of a string but its not first letter
            elif stringCon and char in t.identStart or char == ' ':
                word += char

            # ----------------- SYMBOLS -------------------------------
            if char in t.symbols:
                tokens.append(char)

        return tokens

    def advance(t):  # advances to the next token
        t.x += 1
        
    def hasMoreTokens(t):  # returns a boolean
        has_more = True
        if (t.x + 1 > len(t.allTokens)):
            has_more = False
        return has_more

    def tokenType(t):    # returns the type of the current token
        token = t.allTokens[t.x]
        type = ''
        
        if token in t.numberChars:
            type = 'intConst'
        elif token in t.keywords:
            type = 'keyword'
        elif token[1] in t.symbols:
            type = 'symbol'
        elif token[0] == '"':
            type = 'stringConst'
        else:
            type = 'identifier'
        
        return type

    def giveToken(t):    # returns the current token
        token = t.allTokens[t.x]
        
        if token[0] == '"':
            token.strip('"')[1]
        elif token[0] in t.special:
            token = t.special[token]
        return token

def main():
    input = sys.argv[1]
    file = open(input, "r")
    sys.stdout = open(input.split('.')[0] + 'T.xml', 'wt')  # write to .xml file
    
    test = Tokenizer(file)  # create instance of Tokenizer class using input file
    type = ""
    token = ""
    
    # use Tokenizer functions to print out xml line by line
    while test.hasMoreTokens():
        type = test.tokenType()
        token = test.giveToken()
        print('<' + type + '> ')
        print(token)
        print(' </' + type + '>')
        print('\n')
        test.advance()
    


if __name__ == "__main__":
    main()
