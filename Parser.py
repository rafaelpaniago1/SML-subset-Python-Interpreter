from Expression import *
from Lexer import Token, TokenType
from typing import Optional

class Parser:
    
    def __init__(self, tokens):

        self.tokens = list(tokens)
        self.curr_pointer = 0

    def curr_token(self):
        
        if len(self.tokens) <= self.curr_pointer:
            return None
        return self.tokens[self.curr_pointer]

    def advance(self):
        self.curr_pointer += 1

    def parse(self):

        """
        Returns the expression associated with the stream of tokens.

        Examples:
        >>> parser = Parser([Token('123', TokenType.INT)])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        123

        >>> parser = Parser([Token('True', TokenType.TRU)])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        True

        >>> parser = Parser([Token('False', TokenType.FLS)])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        False

        >>> tk0 = Token('~', TokenType.NEG)
        >>> tk1 = Token('123', TokenType.INT)
        >>> parser = Parser([tk0, tk1])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        -123

        >>> tk0 = Token('3', TokenType.INT)
        >>> tk1 = Token('*', TokenType.MUL)
        >>> tk2 = Token('4', TokenType.INT)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        12

        >>> tk0 = Token('3', TokenType.INT)
        >>> tk1 = Token('*', TokenType.MUL)
        >>> tk2 = Token('~', TokenType.NEG)
        >>> tk3 = Token('4', TokenType.INT)
        >>> parser = Parser([tk0, tk1, tk2, tk3])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        -12

        >>> tk0 = Token('30', TokenType.INT)
        >>> tk1 = Token('/', TokenType.DIV)
        >>> tk2 = Token('4', TokenType.INT)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        7

        >>> tk0 = Token('3', TokenType.INT)
        >>> tk1 = Token('+', TokenType.ADD)
        >>> tk2 = Token('4', TokenType.INT)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        7

        >>> tk0 = Token('30', TokenType.INT)
        >>> tk1 = Token('-', TokenType.SUB)
        >>> tk2 = Token('4', TokenType.INT)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        26

        >>> tk0 = Token('2', TokenType.INT)
        >>> tk1 = Token('*', TokenType.MUL)
        >>> tk2 = Token('(', TokenType.LPR)
        >>> tk3 = Token('3', TokenType.INT)
        >>> tk4 = Token('+', TokenType.ADD)
        >>> tk5 = Token('4', TokenType.INT)
        >>> tk6 = Token(')', TokenType.RPR)
        >>> parser = Parser([tk0, tk1, tk2, tk3, tk4, tk5, tk6])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        14

        >>> tk0 = Token('4', TokenType.INT)
        >>> tk1 = Token('==', TokenType.EQL)
        >>> tk2 = Token('4', TokenType.INT)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        True

        >>> tk0 = Token('4', TokenType.INT)
        >>> tk1 = Token('<=', TokenType.LEQ)
        >>> tk2 = Token('4', TokenType.INT)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        True

        >>> tk0 = Token('4', TokenType.INT)
        >>> tk1 = Token('<', TokenType.LTH)
        >>> tk2 = Token('4', TokenType.INT)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        False

        >>> tk0 = Token('not', TokenType.NOT)
        >>> tk1 = Token('(', TokenType.LPR)
        >>> tk2 = Token('4', TokenType.INT)
        >>> tk3 = Token('<', TokenType.LTH)
        >>> tk4 = Token('4', TokenType.INT)
        >>> tk5 = Token(')', TokenType.RPR)
        >>> parser = Parser([tk0, tk1, tk2, tk3, tk4, tk5])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        True

        >>> tk0 = Token('true', TokenType.TRU)
        >>> tk1 = Token('or', TokenType.OR)
        >>> tk2 = Token('false', TokenType.FLS)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        True

        >>> tk0 = Token('true', TokenType.TRU)
        >>> tk1 = Token('and', TokenType.AND)
        >>> tk2 = Token('false', TokenType.FLS)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        False

        >>> tk0 = Token('let', TokenType.LET)
        >>> tk1 = Token('v', TokenType.VAR)
        >>> tk2 = Token('<-', TokenType.BACKARROW)
        >>> tk3 = Token('42', TokenType.INT)
        >>> tk4 = Token('in', TokenType.IN)
        >>> tk5 = Token('v', TokenType.VAR)
        >>> tk6 = Token('end', TokenType.END)
        >>> parser = Parser([tk0, tk1, tk2, tk3, tk4, tk5, tk6])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, {})
        42

        >>> tk0 = Token('let', TokenType.LET)
        >>> tk1 = Token('v', TokenType.VAR)
        >>> tk2 = Token('<-', TokenType.BACKARROW)
        >>> tk3 = Token('21', TokenType.INT)
        >>> tk4 = Token('in', TokenType.IN)
        >>> tk5 = Token('v', TokenType.VAR)
        >>> tk6 = Token('+', TokenType.ADD)
        >>> tk7 = Token('v', TokenType.VAR)
        >>> tk8 = Token('end', TokenType.END)
        >>> parser = Parser([tk0, tk1, tk2, tk3, tk4, tk5, tk6, tk7, tk8])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, {})
        42

        >>> tk0 = Token('if', TokenType.IF)
        >>> tk1 = Token('2', TokenType.INT)
        >>> tk2 = Token('<', TokenType.LTH)
        >>> tk3 = Token('3', TokenType.INT)
        >>> tk4 = Token('then', TokenType.THEN)
        >>> tk5 = Token('1', TokenType.INT)
        >>> tk6 = Token('else', TokenType.ELSE)
        >>> tk7 = Token('2', TokenType.INT)
        >>> parser = Parser([tk0, tk1, tk2, tk3, tk4, tk5, tk6, tk7])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        1

        >>> tk0 = Token('if', TokenType.IF)
        >>> tk1 = Token('false', TokenType.FLS)
        >>> tk2 = Token('then', TokenType.THEN)
        >>> tk3 = Token('1', TokenType.INT)
        >>> tk4 = Token('else', TokenType.ELSE)
        >>> tk5 = Token('2', TokenType.INT)
        >>> parser = Parser([tk0, tk1, tk2, tk3, tk4, tk5])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        2
        """

        if not self.tokens:
            raise ValueError("Cannot parse empty stream of tokens")
        expr = self.parse_8()

        tok = self.curr_token()
        if tok is not None:
            raise SyntaxError("Extra tokens at the end of expression")
        return expr

    def parse_8(self):

        tok = self.curr_token()

        if tok is not None and tok.kind == TokenType.IF:
            self.advance()
            cond = self.parse_8()
            tok = self.curr_token()

            if tok is not None and tok.kind != TokenType.THEN:
                raise ValueError("Expected THEN token")
            self.advance()

            e0 = self.parse_8()
            tok = self.curr_token()

            if tok is not None and tok.kind != TokenType.ELSE:
                raise ValueError("Expected ELSE token")
            self.advance()

            e1 = self.parse_8()
            tok = self.curr_token()

            return IfThenElse(cond, e0, e1)
        else:
            return self.parse_7()

    def parse_7(self):

        tok = self.curr_token()
        node = self.parse_6()
        tok = self.curr_token()
        while tok is not None and tok.kind == TokenType.OR:
            self.advance()
            node = Or(node, self.parse_6()) 
            tok = self.curr_token()
        return node



    def parse_6(self):

        tok = self.curr_token()
        node = self.parse_5()
        tok = self.curr_token()
        while tok is not None and tok.kind == TokenType.AND:
            self.advance()
            node = And(node, self.parse_5()) 
            tok = self.curr_token()
        return node



    def parse_5(self):

        tok = self.curr_token()
        node = self.parse_4()
        tok = self.curr_token()
        while tok is not None and tok.kind == TokenType.EQL:
            self.advance()
            node = Eql(node, self.parse_4())
            tok = self.curr_token()
        return node



    def parse_4(self):

        tok = self.curr_token()
        node = self.parse_3()
        tok = self.curr_token()
        while tok is not None and tok.kind in (TokenType.LTH, TokenType.LEQ):
            if tok.kind == TokenType.LTH:

                self.advance()
                node = Lth(node, self.parse_3())

            if tok.kind == TokenType.LEQ:

                self.advance()
                node = Leq(node, self.parse_3())

            tok = self.curr_token()
        return node



    def parse_3(self):

        tok = self.curr_token()
        node = self.parse_2()
        tok = self.curr_token()
        while tok is not None and tok.kind in (TokenType.ADD, TokenType.SUB):
            if tok.kind == TokenType.ADD:

                self.advance()
                node = Add(node, self.parse_2())

            if tok.kind == TokenType.SUB:

                self.advance()
                node = Sub(node, self.parse_2())

            tok = self.curr_token()
        return node



    def parse_2(self):

        tok = self.curr_token()
        node = self.parse_1()
        tok = self.curr_token()

        while tok is not None and tok.kind in (TokenType.MUL, TokenType.DIV):
            if tok.kind == TokenType.MUL:

                self.advance()
                node = Mul(node, self.parse_1())

            if tok.kind == TokenType.DIV:

                self.advance()
                node = Div(node, self.parse_1())

            tok = self.curr_token()
        return node



    def parse_1(self):

        tok = self.curr_token()
        if tok is not None and tok.kind in (TokenType.HEX, TokenType.BIN, TokenType.INT, TokenType.OCT):
            self.advance()
            return Num(int(tok.text, 0))

        elif tok is not None and tok.kind == TokenType.LET:
            
            identifier = ""
            self.advance()
            tok = self.curr_token()
            if tok is not None and tok.kind != TokenType.NOME:
                raise SyntaxError("Expected identifier")

            identifier = tok.text if tok is not None else ""
            self.advance()
            tok = self.curr_token()
            if tok is not None and tok.kind != TokenType.BACKARROW:
                raise SyntaxError("Expected back arrow")
            else:
                self.advance()
                tok = self.curr_token()
            exp_def = self.parse_8()
            tok = self.curr_token()
            if tok is not None and tok.kind != TokenType.IN:
                raise SyntaxError("Expected IN token")
            else:
                self.advance()
                tok = self.curr_token()
            exp_body = self.parse_8()
            tok = self.curr_token()
            if tok is not None and tok.kind != TokenType.END:
                raise SyntaxError("Expected END token")
            else:
                self.advance()
            return Let(identifier, exp_def, exp_body)

        elif tok is not None and tok.kind in (TokenType.FLS, TokenType.TRU):
            self.advance()
            return Bln(tok.kind == TokenType.TRU) 
        elif tok is not None and tok.kind == TokenType.LPR:
            self.advance()
            exp = self.parse_8()
            tok = self.curr_token()
            if tok is not None and tok.kind != TokenType.RPR:
                raise SyntaxError("No closing parenthesis") 
            self.advance()
            return exp
        elif tok is not None and tok.kind == TokenType.NOME:
            self.advance()
            return Var(tok.text) 

        #Think about how to parse this
        elif tok is not None and tok.kind == TokenType.NEG:
            self.advance()
            return Neg(self.parse_1())
        elif tok is not None and tok.kind == TokenType.NOT:
            self.advance()
            return Not(self.parse_1())
        else:
            raise SyntaxError("Unexpected token")


##########################################################################################
    def parse_not(self):

        tok = self.curr_token()
        if tok is not None and tok.kind == TokenType.NOT:
            self.advance()
            operand = self.parse_not()
            return Not(operand)
        return self.parse_comparing()

    def parse_comparing(self):

        node = self.parse_add_sub()
        tok = self.curr_token()
        while tok is not None and tok.kind in (TokenType.LEQ, TokenType.LTH, TokenType.EQL):
            if tok.kind == TokenType.LEQ:
                self.advance()
                node = Leq(node, self.parse_add_sub())
            elif tok.kind == TokenType.LTH:
                self.advance()
                node = Lth(node, self.parse_add_sub())
            elif tok.kind == TokenType.EQL:
                self.advance()
                node = Eql(node, self.parse_add_sub())
            tok = self.curr_token()
        return node


    def parse_add_sub(self):

        node = self.parse_mul_div()
        tok = self.curr_token()
        while tok is not None and tok.kind in (TokenType.ADD, TokenType.SUB):
            if tok.kind == TokenType.ADD:
                self.advance()
                node = Add(node, self.parse_mul_div())
            elif tok.kind == TokenType.SUB:
                self.advance()
                node = Sub(node, self.parse_mul_div())
            tok = self.curr_token()
        return node

    def parse_mul_div(self):

        node = self.parse_neg()
        tok = self.curr_token()
        while tok is not None and tok.kind in (TokenType.MUL, TokenType.DIV):
            if tok.kind == TokenType.MUL:
                self.advance()
                node = Mul(node, self.parse_neg())
            elif tok.kind == TokenType.DIV:
                self.advance()
                node = Div(node, self.parse_neg())
            tok = self.curr_token()
        return node

    def parse_neg(self):

        tok = self.curr_token()
        if tok is not None and tok.kind == TokenType.NEG:
            self.advance()
            other = self.parse_neg()
            return Neg(other)
        return self.parse_let()

    def parse_let(self):

        tok = self.curr_token()
        if tok is not None and tok.kind in (TokenType.HEX, TokenType.BIN, TokenType.INT, TokenType.OCT):
            self.advance()
            return Num(int(tok.text, 0))
        #Implement parsing for let and var expressions
        elif tok is not None and tok.kind == TokenType.LET:
            
            identifier = ""
            self.advance()
            tok = self.curr_token()
            if tok is not None and tok.kind != TokenType.NOME:
                raise SyntaxError("Expected identifier")

            identifier = tok.text if tok is not None else ""
            self.advance()
            tok = self.curr_token()
            if tok is not None and tok.kind != TokenType.BACKARROW:
                raise SyntaxError("Expected back arrow")
            else:
                self.advance()
                tok = self.curr_token()
            exp_def = self.parse_not()
            tok = self.curr_token()
            if tok is not None and tok.kind != TokenType.IN:
                raise SyntaxError("Expected IN token")
            else:
                self.advance()
                tok = self.curr_token()
            exp_body = self.parse_not()
            tok = self.curr_token()
            if tok is not None and tok.kind != TokenType.END:
                raise SyntaxError("Expected END token")
            else:
                self.advance()
            return Let(identifier, exp_def, exp_body)

        elif tok is not None and tok.kind in (TokenType.FLS, TokenType.TRU):
            self.advance()
            return Bln(tok.kind == TokenType.TRU) 
        elif tok is not None and tok.kind == TokenType.LPR:
            self.advance()
            exp = self.parse_not()
            tok = self.curr_token()
            if tok is not None and tok.kind != TokenType.RPR:
                raise SyntaxError("No closing parenthesis") 
            self.advance()
            return exp
        elif tok is not None and tok.kind == TokenType.NOME:
            self.advance()
            return Var(tok.text) 
        else:
            raise SyntaxError("Unexpected token")

