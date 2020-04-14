# EOF token表示到达输入串尾部
token_types = {
    "INT": "INT",
    "PLUS": "PLUS",
    "EOF": "EOF",
    "MINUS": "MINUS"
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


class Interceptor(object):
    def __init__(self, text):
        # 输入,比如1+2
        self.text = text
        # 当前待处理字符在text的位置,初始时为0
        self.pos = 0
        # 当前的Token实例对象
        self.currentToken = None
        # 当前待处理字符
        self.currentChar = self.text[self.pos]

    def error(self):
        raise Exception("解析文本错误")

    def advance(self):
        """
        向前移动pos指针并且将currentChar设置为该位置字符
        :return:
        """
        self.pos += 1
        if self.pos >= len(self.text):
            self.currentChar = None
        else:
            self.currentChar = self.text[self.pos]

    # 跳过空格
    def skip_whitespace(self):
        while self.currentChar is not None and self.currentChar.isspace():
            self.advance()

    def get_int(self):
        """
        将连续的几个数字字符转化为为一个多位整数
        """
        result = ''
        while self.currentChar is not None and self.currentChar.isdigit():
            result += self.currentChar
            self.advance()
        return int(result)

    def get_next_token(self):
        """
        读取当前的字符并返回对应的token

        """

        while self.currentChar is not None:
            # 空格
            if self.currentChar.isspace():
                self.skip_whitespace()
                continue

            # 数字
            if self.currentChar.isdigit():
                return Token(token_types["INT"], self.get_int())

            # 加号
            if self.currentChar == '+':
                self.advance()
                return Token(token_types["PLUS"], '+')

            # 减号
            if self.currentChar == '-':
                self.advance()
                return Token(token_types["MINUS"], '-')

            self.error()

        return Token(token_types["EOF"], None)

    def eat(self, type_):
        """
        检查是否是期望的token类型

        """
        if self.currentToken.type == type_:
            self.currentToken = self.get_next_token()
        else:
            self.error()

    def term(self):
        """Return an INTEGER token value."""
        token = self.currentToken
        self.eat(token_types["INT"])
        return token.value

    def expr(self):
        self.currentToken = self.get_next_token()

        result = self.term()

        while self.currentToken.type in (token_types["PLUS"], token_types["MINUS"]):
            token = self.currentToken
            if token.type == token_types["PLUS"]:
                self.eat(token_types["PLUS"])
                result = result + self.term()
            elif token.type == token_types["MINUS"]:
                self.eat(token_types["MINUS"])
                result = result - self.term()

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
        interceptor = Interceptor(text)
        result = interceptor.expr()
        print(result)


if __name__ == '__main__':
    main()
