from sys import warnoptions
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
        >>> parser = Parser([Token('123', TokenType.NUM)])
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
        >>> tk1 = Token('123', TokenType.NUM)
        >>> parser = Parser([tk0, tk1])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        -123

        >>> tk0 = Token('3', TokenType.NUM)
        >>> tk1 = Token('*', TokenType.MUL)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        12

        >>> tk0 = Token('3', TokenType.NUM)
        >>> tk1 = Token('*', TokenType.MUL)
        >>> tk2 = Token('~', TokenType.NEG)
        >>> tk3 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2, tk3])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        -12

        >>> tk0 = Token('30', TokenType.NUM)
        >>> tk1 = Token('/', TokenType.DIV)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        7

        >>> tk0 = Token('3', TokenType.NUM)
        >>> tk1 = Token('+', TokenType.ADD)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        7

        >>> tk0 = Token('30', TokenType.NUM)
        >>> tk1 = Token('-', TokenType.SUB)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        26

        >>> tk0 = Token('2', TokenType.NUM)
        >>> tk1 = Token('*', TokenType.MUL)
        >>> tk2 = Token('(', TokenType.LPR)
        >>> tk3 = Token('3', TokenType.NUM)
        >>> tk4 = Token('+', TokenType.ADD)
        >>> tk5 = Token('4', TokenType.NUM)
        >>> tk6 = Token(')', TokenType.RPR)
        >>> parser = Parser([tk0, tk1, tk2, tk3, tk4, tk5, tk6])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        14

        >>> tk0 = Token('4', TokenType.NUM)
        >>> tk1 = Token('==', TokenType.EQL)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        True

        >>> tk0 = Token('4', TokenType.NUM)
        >>> tk1 = Token('<=', TokenType.LEQ)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        True

        >>> tk0 = Token('4', TokenType.NUM)
        >>> tk1 = Token('<', TokenType.LTH)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        False

        >>> tk0 = Token('not', TokenType.NOT)
        >>> tk1 = Token('(', TokenType.LPR)
        >>> tk2 = Token('4', TokenType.NUM)
        >>> tk3 = Token('<', TokenType.LTH)
        >>> tk4 = Token('4', TokenType.NUM)
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
        >>> tk3 = Token('42', TokenType.NUM)
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
        >>> tk3 = Token('21', TokenType.NUM)
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
        >>> tk1 = Token('2', TokenType.NUM)
        >>> tk2 = Token('<', TokenType.LTH)
        >>> tk3 = Token('3', TokenType.NUM)
        >>> tk4 = Token('then', TokenType.THEN)
        >>> tk5 = Token('1', TokenType.NUM)
        >>> tk6 = Token('else', TokenType.ELSE)
        >>> tk7 = Token('2', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2, tk3, tk4, tk5, tk6, tk7])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        1

        >>> tk0 = Token('if', TokenType.IF)
        >>> tk1 = Token('false', TokenType.FLS)
        >>> tk2 = Token('then', TokenType.THEN)
        >>> tk3 = Token('1', TokenType.NUM)
        >>> tk4 = Token('else', TokenType.ELSE)
        >>> tk5 = Token('2', TokenType.NUM)
        >>> parser = Parser([tk0, tk1, tk2, tk3, tk4, tk5])
        >>> exp = parser.parse()
        >>> ev = EvalVisitor()
        >>> exp.accept(ev, None)
        2
        """

        if not self.tokens:
            raise ValueError("Cannot parse empty stream of tokens")
        expr = self.parse_fn_exp()

        tok = self.curr_token()
        if tok is not None:
            sys.exit("Parse error")
        return expr
    
    def parse_fn_exp(self):
        
        tok = self.curr_token()

        if tok is not None and tok.kind == TokenType.FNX:
           self.advance() 
           tok = self.curr_token()

           if tok is not None and tok.kind != TokenType.VAR:
                sys.exit("Expected VAR token")
           arg = Var(str(tok.text))

           self.advance()
           tok = self.curr_token()

           if tok is not None and tok.kind != TokenType.ARW:
              raise ValueError("Expected ARW token")

           self.advance()
           body = self.parse_fn_exp()
           tok = self.curr_token()
           
           return Fn(arg, body)

        else:
            return self.parse_if_exp()


    def parse_if_exp(self):

        tok = self.curr_token()

        if tok is not None and tok.kind == TokenType.IF:
            self.advance()
            cond = self.parse_if_exp()
            tok = self.curr_token()

            if tok is not None and tok.kind != TokenType.THEN:
                raise ValueError("Expected THEN token")
            self.advance()

            e0 = self.parse_fn_exp()
            tok = self.curr_token()

            if tok is not None and tok.kind != TokenType.ELSE:
                raise ValueError("Expected ELSE token")
            self.advance()

            e1 = self.parse_fn_exp()
            tok = self.curr_token()

            return IfThenElse(cond, e0, e1)
        else:
            return self.parse_or_exp()

    def parse_or_exp(self):

        tok = self.curr_token()
        node = self.parse_and_exp()
        tok = self.curr_token()
        while tok is not None and tok.kind == TokenType.OR:
            self.advance()
            node = Or(node, self.parse_and_exp()) 
            tok = self.curr_token()
        return node



    def parse_and_exp(self):

        tok = self.curr_token()
        node = self.parse_eq_exp()
        tok = self.curr_token()
        while tok is not None and tok.kind == TokenType.AND:
            self.advance()
            node = And(node, self.parse_eq_exp()) 
            tok = self.curr_token()
        return node



    def parse_eq_exp(self):

        tok = self.curr_token()
        node = self.parse_cmp_exp()
        tok = self.curr_token()
        while tok is not None and tok.kind == TokenType.EQL:
            self.advance()
            node = Eql(node, self.parse_cmp_exp())
            tok = self.curr_token()
        return node



    def parse_cmp_exp(self):

        tok = self.curr_token()
        node = self.parse_add_exp()
        tok = self.curr_token()
        while tok is not None and tok.kind in (TokenType.LTH, TokenType.LEQ):
            if tok.kind == TokenType.LTH:

                self.advance()
                node = Lth(node, self.parse_add_exp())

            elif tok.kind == TokenType.LEQ:

                self.advance()
                node = Leq(node, self.parse_add_exp())

            tok = self.curr_token()
        return node



    def parse_add_exp(self):

        tok = self.curr_token()
        node = self.parse_mul_exp()
        tok = self.curr_token()
        while tok is not None and tok.kind in (TokenType.ADD, TokenType.SUB):
            if tok.kind == TokenType.ADD:

                self.advance()
                node = Add(node, self.parse_mul_exp())

            elif tok.kind == TokenType.SUB:

                self.advance()
                node = Sub(node, self.parse_mul_exp())

            tok = self.curr_token()
        return node



    def parse_mul_exp(self):

        tok = self.curr_token()
        node = self.parse_unary_exp()
        tok = self.curr_token()

        while tok is not None and tok.kind in (TokenType.MUL, TokenType.DIV, TokenType.MOD):
            if tok.kind == TokenType.MUL:

                self.advance()
                node = Mul(node, self.parse_unary_exp())

            elif tok.kind == TokenType.DIV:

                self.advance()
                node = Div(node, self.parse_unary_exp())

            elif tok.kind == TokenType.MOD:

                self.advance()
                node = Mod(node, self.parse_unary_exp())

            tok = self.curr_token()
        return node


    def parse_unary_exp(self):

        tok = self.curr_token()
        if tok is not None and tok.kind in (TokenType.NEG, TokenType.NOT):

            if tok.kind == TokenType.NEG:

                self.advance()
                tok = self.curr_token()
                return Neg(self.parse_unary_exp())

            elif tok.kind == TokenType.NOT:

                self.advance()
                tok = self.curr_token()
                return Not(self.parse_unary_exp())
        else:
            return self.parse_let_exp()


    def parse_let_exp(self):

        tok = self.curr_token() 
        if tok is not None and tok.kind == TokenType.LET:
            
            self.advance()
            tok = self.curr_token()
            identifier, exp_def = self.parse_decl() 
            tok = self.curr_token()
            if tok is not None and tok.kind != TokenType.IN:
                sys.exit("Parse error")

            else:
                self.advance()
                tok = self.curr_token()
            exp_body = self.parse_fn_exp()
            tok = self.curr_token()
            if tok is not None and tok.kind != TokenType.END:
                sys.exit("Parse error")

            else:
                self.advance()
            return Let(identifier, exp_def, exp_body)

        else:
            return self.parse_val_exp()
    
    def parse_val_exp(self):

        tok = self.curr_token()
        node = self.parse_val_tk() 
        tok = self.curr_token()
        while tok is not None and tok.kind in (TokenType.VAR, TokenType.LPR, TokenType.NUM, TokenType.OCT, TokenType.BIN, TokenType.HEX, TokenType.FLS, TokenType.TRU):
            node = App(node, self.parse_val_tk())
            tok = self.curr_token()
        return node

    def parse_val_tk(self):

        tok = self.curr_token()
        if tok is not None and tok.kind in (TokenType.HEX, TokenType.BIN, TokenType.NUM, TokenType.OCT):
            self.advance()
            return Num(int(tok.text, 0))

        elif tok is not None and tok.kind in (TokenType.FLS, TokenType.TRU):
            self.advance()
            return Bln(tok.kind == TokenType.TRU) 

        elif tok is not None and tok.kind == TokenType.LPR:
            self.advance()
            exp = self.parse_fn_exp()
            tok = self.curr_token()
            if tok is not None and tok.kind != TokenType.RPR:
                sys.exit("Parse error")
            self.advance()
            return exp
        elif tok is not None and tok.kind == TokenType.VAR:
            self.advance()
            return Var(tok.text) 

    def parse_decl(self):
       
        tok = self.curr_token()
        if tok is not None and tok.kind == TokenType.VAL:
            self.advance()
            tok = self.curr_token()
            if tok is not None and tok.kind != TokenType.VAR:
                sys.exit("Expected VAR token")
            var = Var(str(tok.text))
            self.advance()
            tok = self.curr_token()
            if tok is not None and tok.kind != TokenType.EQL:
                sys.exit("Expected EQL token")
            self.advance()
            value = self.parse_fn_exp()
            return (var, value)

        elif tok is not None and tok.kind == TokenType.FUN:
            self.advance()
            tok = self.curr_token()
            if tok is not None and tok.kind != TokenType.VAR:
                sys.exit("Expected VAR token(name of rec function)")
            name = Var(str(tok.text))
            self.advance()
            tok = self.curr_token()
            if tok is not None and tok.kind != TokenType.VAR:
                sys.exit("Expected VAR token(parameter of rec function)")
            formal = Var(str(tok.text))
            self.advance()
            tok = self.curr_token()
            if tok is not None and tok.kind != TokenType.EQL:
                sys.exit("Expected EQL token in recursive function declaration")
            self.advance()
            tok = self.curr_token()
            body = self.parse_fn_exp()
            return (name, Fun(name, formal, body))

