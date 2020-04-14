# EOF token表示到达输入串尾部
token_types = {
    "INT": "INT",
    "MUL": "MUL",
    "EOF": "EOF",
    "DIV": "DIV"
}


class Token(object):
    def __init__(self, type_, value_):
        # token的类型,如INT,PLUS,EOF
        self.type = type_
        # token的值,如1,2,+和None
        self.value = value_

    def __str__(self):
        """返回token的字符串形式

        比如:
        Token(INTEGER, 3)
        """
        return 'Token({type}, {value})'.format(
            self.type,
            self.__repr__(self.value))

    def __repr__(self):
        return self.__str__()


class Lexser(object):
    def __init__(self, text):
        # 输入,比如1+2
        self.text = text
        # 当前待处理字符在text的位置,初始时为0
        self.pos = 0
        # 当前待处理字符
        self.currentChar = self.text[self.pos]

    def error(self):
        raise Exception("不合法的字符")

    def advance(self):
        self.pos += 1
        if self.pos >= len(self.text):
            self.currentChar = None
        else:
            self.currentChar = self.text[self.pos]

    def skip_whitespace(self):
        while self.currentChar is not None and self.currentChar.isspace():
            self.advance()

    def get_int(self):
        result = ''
        while self.currentChar is not None and self.currentChar.isdigit():
            result += self.currentChar
            self.advance()
        return int(result)

    def get_next_token(self):
        while self.currentChar is not None:
            # 空格
            if self.currentChar.isspace():
                self.skip_whitespace()
                continue

            # 数字
            if self.currentChar.isdigit():
                return Token(token_types["INT"], self.get_int())

            # 乘号
            if self.currentChar == '*':
                self.advance()
                return Token(token_types["MUL"], '*')

            # 除号
            if self.currentChar == '/':
                self.advance()
                return Token(token_types["DIV"], '/')

            self.error()

        return Token(token_types["EOF"], None)


class Interpreter(object):
    def __init__(self, lexser):
        self.lexser = lexser
        self.current_token = self.lexser.get_next_token()

    def error(self):
        raise Exception("不合法的标识")

    def eat(self, type_):
        if self.current_token.type == type_:
            self.current_token = self.lexser.get_next_token()
        else:
            self.error()

    def factor(self):
        token = self.current_token
        self.eat(token_types["INT"])
        return token.value

    def expr(self):
        """
        expr   : factor ((MUL | DIV) factor)*
        factor : INTEGER
        """
        result = self.factor()

        while self.current_token.type in (token_types["MUL"], token_types["DIV"]):
            token = self.current_token
            if token.type == token_types["MUL"]:
                self.eat(token_types["MUL"])
                result = result * self.factor()
            elif token.type == token_types["DIV"]:
                self.eat(token_types["DIV"])
                result = result / self.factor()

        return result


def main():
    while True:
        try:
            text = input("calc> ")
            if text == 'exit':
                break
        except IOError:
            break
        # 输入为空的情况
        if not text:
            continue
        lexser = Lexser(text)
        interceptor = Interpreter(lexser)
        result = interceptor.expr()
        print(result)


if __name__ == '__main__':
    main()
