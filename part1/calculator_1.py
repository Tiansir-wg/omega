# EOF token表示到达输入串尾部
token_types = {"INT": "INT", "PLUS": "PLUS", "EOF": "EOF"}


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


class Interpreter(object):
    def __init__(self, text):
        # 输入,比如1+2
        self.text = text
        # 当前待处理字符在text的位置,初始时为0
        self.pos = 0
        # 当前处理字符的Token实例对象
        self.currentToken = None

    def error(self):
        raise Exception("解析文本错误")

    def get_next_token(self):
        """
        读取当前的字符并返回对应的token

        """
        # 读取文本串尾部
        if len(self.text) <= self.pos:
            return Token(token_types["EOF"], None)

        # 当前待读取的字符
        ch = self.text[self.pos]

        # 数字
        if ch.isdigit():
            self.pos += 1
            return Token(token_types["INT"], int(ch))

        # 加号
        if ch == '+':
            self.pos += 1
            return Token(token_types["PLUS"], ch)

        self.error()

    def eat(self, type_):
        """
        检查是否是期望的token类型

        """
        if self.currentToken.type == type_:
            self.currentToken = self.get_next_token()
        else:
            self.error()

    def expr(self):

        self.currentToken = self.get_next_token()
        # 运算符左边的数字
        left = self.currentToken
        # 期望类型是INT
        self.eat(token_types["INT"])

        op = self.currentToken
        # 期望的类型是PLUS
        self.eat(token_types["PLUS"])

        # 运算符右边的数字
        right = self.currentToken
        # 期望的类型是PLUS
        self.eat(token_types["INT"])

        # 能运行到这里而且还没有出现异常则说明输入串是
        # INT PLUS INT形式的
        return left.value + right.value


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
        interceptor = Interpreter(text)
        result = interceptor.expr()
        print(result)


if __name__ == '__main__':
    main()
