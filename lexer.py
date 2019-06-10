import token_names as tokens
from tokeng import Token


RESERVED_KEYWORDS = {
    'int': Token('int', 'int', None, None),
    'string': Token('string', 'string', None, None),
    'var': Token('var', 'var', None, None),
    'func': Token('func', 'func', None, None),
    'package': Token('package', 'package', None, None),
    'import': Token('import', 'import', None, None),
    'print': Token('print', 'print', None, None),
    'if': Token('if', 'if', None, None),
    'for': Token('for', 'for', None, None),
}

class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.posx = 1
        self.posy = 1
        # текущий символ
        self.current_char = self.text[self.pos]

    def error(self, message):
        raise Exception(message)

    # перемещение по тексту
    def next(self):
        self.pos += 1
        self.posx += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
    #следующий символ
    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            if self.current_char == "\n":
                self.posy += 1
                self.posx = 0
            self.next()

    def skip_comment(self):
        self.next()
        while self.current_char is not None and self.current_char != "\n":
            self.next()
        self.next
    #числа
    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.next()
        tmp = self.current_char
        if tmp is not None and tmp.isalpha():
            self.error('Unknown character ' + str(result) + str(self.current_char))
        return int(result)
    #зарезервированные слова и переменные
    def _id(self):
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.next()
        token = RESERVED_KEYWORDS.get(result, Token(tokens.ID, result, self.posx, self.posy))
        token.x = self.posx - len(token.value)
        token.y = self.posy
        return token

    def get_next_token(self):
        while self.current_char is not None:
            #если буква
            if self.current_char.isalpha():
                return self._id()
            if self.current_char == '"':
                self.next()
                word = ''
                while self.current_char != '"':
                    word += str(self.current_char)
                    self.next()
                self.next()
                return Token(tokens.LITTERAL, word, self.posx - len(word) - 2, self.posy)

            if self.current_char == '=':
                if self.peek() == '=':
                    self.next()
                    self.next()
                    return Token(tokens.EQUAL, '==', self.posx, self.posy)
                self.next()
                return Token(tokens.ASSIGN, '=', self.posx - 1, self.posy)

            if self.current_char == '<':
                if self.peek() == '=':
                    self.next()
                    self.next()
                    return Token(tokens.EQL, '<=', self.posx - 2, self.posy)
                self.next()
                self.next()
                return Token(tokens.LESS, '<', self.posx - 1, self.posy)

            if self.current_char == '>':
                if self.peek() == '=':
                    self.next()
                    self.next()
                    return Token(tokens.EQR, '>=', self.posx - 2, self.posy)
                self.next()
                self.next()
                return Token(tokens.MORE, '>', self.posx - 1, self.posy)

            if self.current_char == ';':
                self.next()
                return Token(tokens.SEMI, ';', self.posx - 1, self.posy)
            if self.current_char == ',':
                self.next()
                return Token(tokens.COMMA, ',', self.posx - 1, self.posy)
            if self.current_char == ':':
                self.next()
                return Token(tokens.COLON, ':', self.posx - 1, self.posy)
            if self.current_char == '!' and self.peek() == '=':
                self.next()
                self.next()
                return Token(tokens.NOTEQUAL, '!=', self.posx - 2, self.posy)

            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char == '#':
                self.skip_comment()
                continue

            if self.current_char.isdigit():
                result = self.integer()
                return Token(tokens.INT, str(result), self.posx - 1, self.posy)
            if self.current_char == '+':
                self.next()
                return Token(tokens.PLUS, '+', self.posx - 1, self.posy)
            if self.current_char == '-':
                self.next()
                return Token(tokens.MINUS, '-', self.posx - 1, self.posy)
            if self.current_char == '*':
                self.next()
                return Token(tokens.MULTIPLY, '*', self.posx - 1, self.posy)
            if self.current_char == '/':
                self.next()
                return Token(tokens.DIVIDE, '/', self.posx - 1, self.posy)
            if self.current_char == '(':
                self.next()
                return Token(tokens.LPAREN, '(', self.posx - 1, self.posy)
            if self.current_char == ')':
                self.next()
                return Token(tokens.RPAREN, ')', self.posx - 1, self.posy)
            if self.current_char == '[':
                self.next()
                return Token(tokens.LBRACKET, '[', self.posx - 1, self.posy)
            if self.current_char == ']':
                self.next()
                return Token(tokens.RBRACKET, ']', self.posx - 1, self.posy)
            if self.current_char == '{':
                self.next()
                return Token(tokens.LBRACE, '{', self.posx - 1, self.posy)
            if self.current_char == '}':
                self.next()
                return Token(tokens.RBRACE, '}', self.posx - 1, self.posy)
            if self.current_char == '.':
                self.next()
                return Token(tokens.POINT, 'POINT', self.posx - 1, self.posy)
            self.error('Unknown character %s found' % self.current_char)
        return Token(tokens.EOF, None, self.posx, self.posy)