import enum


class Token:
    def __init__(self, tokenText, tokenKind):
        self.text = tokenText
        self.kind = tokenKind


class TokenType(enum.Enum):
    EOF = -1
    NLN = 0
    WSP = 1
    COM = 2
    STR = 3
    TRU = 4
    FLS = 5
    INT = 6
    BIN = 7
    OCT = 8
    HEX = 9
    EQL = 201
    ADD = 202
    SUB = 203
    MUL = 204
    DIV = 205
    LEQ = 206
    LTH = 207
    NEG = 208
    NOT = 209
    LPR = 210
    RPR = 211
    VAR = 212
    LET = 213
    IN = 214
    END = 215
    BACKARROW = 216
    IF = 217
    THEN = 218
    ELSE = 219
    OR = 220
    AND = 221


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.sourcePointer = 0
        self.currChar = self.source[self.sourcePointer] if self.source else None

    def nextChar(self):
        self.sourcePointer += 1
        if self.sourcePointer >= len(self.source):
            self.currChar = None
        else:
            self.currChar = self.source[self.sourcePointer]

    def tokens(self):
        token = self.getToken()
        while token is not None and token.kind != TokenType.EOF:
            if token.kind not in (TokenType.WSP, TokenType.NLN):
                yield token
            token = self.getToken()

    def getToken(self):
        # Skip whitespace
        if self.currChar is None:
            return Token("", TokenType.EOF)

        if self.currChar.isspace():
            if self.currChar == "\n":
                self.nextChar()
                return Token("\\n", TokenType.NLN)
            self.nextChar()
            return Token(" ", TokenType.WSP)

        # Single char operators
        if self.currChar == "+":
            self.nextChar()
            return Token("+", TokenType.ADD)
        if self.currChar == "-":
            self.nextChar()
            # check comment
            if self.currChar == "-":
                text = "--"
                self.nextChar()
                while self.currChar is not None and self.currChar != "\n":
                    text += self.currChar
                    self.nextChar()
                return Token(text, TokenType.COM)
            return Token("-", TokenType.SUB)
        if self.currChar == "*":
            self.nextChar()
            return Token("*", TokenType.MUL)
        if self.currChar == "/":
            self.nextChar()
            return Token("/", TokenType.DIV)
        if self.currChar == "=":
            self.nextChar()
            return Token("=", TokenType.EQL)
        if self.currChar == "~":
            self.nextChar()
            return Token("~", TokenType.NEG)
        if self.currChar == "<":
            self.nextChar()
            if self.currChar == "=":
                self.nextChar()
                return Token("<=", TokenType.LEQ)
            if self.currChar == "-":
                self.nextChar()
                return Token("<-", TokenType.BACKARROW)
            return Token("<", TokenType.LTH)
        if self.currChar == "(":
            self.nextChar()
            return Token("(", TokenType.LPR)
        if self.currChar == ")":
            self.nextChar()
            return Token(")", TokenType.RPR)

        if self.source.startswith("true", self.sourcePointer):
            self.sourcePointer += 4
            self.currChar = self.source[self.sourcePointer] if self.sourcePointer < len(self.source) else None
            return Token("true", TokenType.TRU)
        if self.source.startswith("false", self.sourcePointer):
            self.sourcePointer += 5
            self.currChar = self.source[self.sourcePointer] if self.sourcePointer < len(self.source) else None
            return Token("false", TokenType.FLS)
        if self.source.startswith("not", self.sourcePointer):
            self.sourcePointer += 3
            self.currChar = self.source[self.sourcePointer] if self.sourcePointer < len(self.source) else None
            return Token("not", TokenType.NOT)
        if self.source.startswith("let", self.sourcePointer):
            self.sourcePointer += 3
            self.currChar = self.source[self.sourcePointer] if self.sourcePointer < len(self.source) else None
            return Token("let", TokenType.LET)
        if self.source.startswith("end", self.sourcePointer):
            self.sourcePointer += 3
            self.currChar = self.source[self.sourcePointer] if self.sourcePointer < len(self.source) else None
            return Token("end", TokenType.END)
        if self.source.startswith("in", self.sourcePointer):
            self.sourcePointer += 2
            self.currChar = self.source[self.sourcePointer] if self.sourcePointer < len(self.source) else None
            return Token("in", TokenType.IN)
        if self.source.startswith("if", self.sourcePointer):
            self.sourcePointer += 2
            self.currChar = self.source[self.sourcePointer] if self.sourcePointer < len(self.source) else None
            return Token("if", TokenType.IF)
        if self.source.startswith("then", self.sourcePointer):
            self.sourcePointer += 4
            self.currChar = self.source[self.sourcePointer] if self.sourcePointer < len(self.source) else None
            return Token("then", TokenType.THEN)
        if self.source.startswith("else", self.sourcePointer):
            self.sourcePointer += 4
            self.currChar = self.source[self.sourcePointer] if self.sourcePointer < len(self.source) else None
            return Token("else", TokenType.ELSE)
        if self.source.startswith("and", self.sourcePointer):
            self.sourcePointer += 3
            self.currChar = self.source[self.sourcePointer] if self.sourcePointer < len(self.source) else None
            return Token("and", TokenType.AND)
        if self.source.startswith("or", self.sourcePointer):
            self.sourcePointer += 2
            self.currChar = self.source[self.sourcePointer] if self.sourcePointer < len(self.source) else None
            return Token("or", TokenType.OR)

        if self.currChar.isdigit():
            text = self.currChar
            self.nextChar()
            if text == "0":
                if self.currChar in ("b", "B"):
                    text += self.currChar
                    self.nextChar()
                    while self.currChar is not None and self.currChar in ("0", "1"):
                        text += self.currChar
                        self.nextChar()
                    return Token(text, TokenType.BIN)
                if self.currChar in ("x", "X"):
                    text += self.currChar
                    self.nextChar()
                    while self.currChar is not None and (self.currChar.isdigit() or self.currChar.upper() in "ABCDEF"):
                        text += self.currChar
                        self.nextChar()
                    return Token(text, TokenType.HEX)
                if self.currChar is not None and self.currChar.isdigit():
                    while self.currChar is not None and self.currChar.isdigit():
                        text += self.currChar
                        self.nextChar()
                    return Token(text, TokenType.OCT)
                return Token("0", TokenType.INT)
            else:
                while self.currChar is not None and self.currChar.isdigit():
                    text += self.currChar
                    self.nextChar()
                return Token(text, TokenType.INT)

        if self.currChar.isalpha():
            text = self.currChar
            self.nextChar()
            while self.currChar is not None and (self.currChar.isalpha() or self.currChar.isdigit()):
                text += self.currChar
                self.nextChar()
            return Token(text, TokenType.VAR)


        ch = self.currChar
        self.nextChar()
        return Token(ch, TokenType.STR)
