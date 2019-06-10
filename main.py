from lexer import Lexer
from parsert import Parser
from semantic_analyzer import SemanticAnalyzer


import sys

def file(name):
    file = open(name, 'r')
    text = file.read()
    file.close()
    return text



if __name__ == "__main__":
    if len(sys.argv) > 2:
        if sys.argv[2] == '-l':
            print("Lexing...")
            code = file(sys.argv[1])
            lexer = Lexer(code)
            token = lexer.get_next_token()
            while token.type is not "EOF":
                print("<" + str(token.y) + ">" + "<" + str(token.x) + ">" + "=" + token.type + "," + token.value)
                token = lexer.get_next_token()
            print("Lexer[OK]")

        if sys.argv[2] == '-p':
            print("Lexing...")
            code = file(sys.argv[1])
            lexer = Lexer(code)
            print("Lexer[OK]")
            parser = Parser(lexer)
            tree = parser.parse()
            print(tree.toJSON())
        if sys.argv[2] == '-s':
            print("Lexing...")
            code = file(sys.argv[1])
            lexer = Lexer(code)
            print("Lexer[OK]")
            print("Parsing...")
            parser = Parser(lexer)
            tree = parser.parse()
            print("Parser[OK]")
            print("Semantic Analyzer...")
            semantic_analyzer = SemanticAnalyzer()
            semantic_analyzer.visit(tree)
            print("Semantic[OK]")
    else:
        print("шо по аргументам?")