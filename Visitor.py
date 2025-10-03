import sys
from abc import ABC, abstractmethod
from Expression import *

class ArrowType():
    def __init__(self, tp_formal, tp_body):

        self.hd = tp_formal
        self.tl = tp_body

    def __eql__(self, other):
        if isinstance(other, ArrowType):
            return self.hd == other.hd and self.tl == other.tl
        else:
            return False

    def __repr__(self):
        if isinstance(self.hd, ArrowType):
            hd_str = f"( {str(self.hd)} )"
        else:
            hd_str = str(self.hd)
        if isinstance(self.tl, ArrowType):
            tl_str = f"( {str(self.tl)} )"
        else:
            tl_str = str(self.tl)
        return f"{hd_str} -> {tl_str}"

class Function():
    def __init__(self, formal, body, env):

        self.formal = formal
        self.body = body
        self.env = env

    def __str__(self):
        return f"Fn({self.formal})"

class RecFunction(Function):

    def __init__(self, name, formal, body, env):
        super().__init__(formal, body, env)
        self.name = name

    def __str__(self):
        return f"Fun {self.name} ({self.formal})"

class Visitor(ABC):
    """
    The visitor pattern consists of two abstract classes: the Expression and the
    Visitor. The Expression class defines on method: 'accept(visitor, args)'.
    This method takes in an implementation of a visitor, and the arguments that
    are passed from expression to expression. The Visitor class defines one
    specific method for each subclass of Expression. Each instance of such a
    subclasse will invoke the right visiting method.
    """
    @abstractmethod
    def visit_var(self, var, env):
        pass
    @abstractmethod
    def visit_bln(self, bln, env):
        pass
    @abstractmethod
    def visit_num(self, num, env):
        pass
    @abstractmethod
    def visit_eql(self, eql, env):
        pass
    @abstractmethod
    def visit_add(self, add, env):
        pass
    @abstractmethod
    def visit_sub(self, sub, env):
        pass
    @abstractmethod
    def visit_mul(self, mul, env):
        pass
    @abstractmethod
    def visit_div(self, div, env):
        pass
    @abstractmethod
    def visit_leq(self, leq, env):
        pass
    @abstractmethod
    def visit_lth(self, lth, env):
        pass
    @abstractmethod
    def visit_neg(self, neg, env):
        pass
    @abstractmethod
    def visit_not(self, not_node, env):
        pass
    @abstractmethod
    def visit_let(self, let, env):
        pass
    @abstractmethod
    def visit_and(self, exp, env):
        pass
    @abstractmethod
    def visit_or(self, exp, env):
        pass
    @abstractmethod
    def visit_ifThenElse(self, exp, env):
        pass
    @abstractmethod
    def visit_function(self, exp, env):
        pass
    @abstractmethod
    def visit_app(self, exp, env):
        pass
    @abstractmethod
    def visit_rec_fun(self, exp, env):
        pass
    @abstractmethod
    def visit_mod(self, exp, env):
        pass

class EvalVisitor(Visitor):
    """
    The EvalVisitor class evaluates logical and arithmetic expressions. The
    result of evaluating an expression is the value of that expression. The
    inherited attribute propagated throughout visits is the environment that
    associates the names of variables with values.

    Examples:
    >>> e0 = Let('v', Add(Num(40), Num(2)), Mul(Var('v'), Var('v')))
    >>> e1 = Not(Eql(e0, Num(1764)))
    >>> ev = EvalVisitor()
    >>> e1.accept(ev, {})
    False

    >>> e0 = Let('v', Add(Num(40), Num(2)), Sub(Var('v'), Num(2)))
    >>> e1 = Lth(e0, Var('x'))
    >>> ev = EvalVisitor()
    >>> e1.accept(ev, {'x': 41})
    True
    """
    def visit_var(self, var, env):
        if var.identifier in env:
            return env[var.identifier]
        else:
            raise sys.exit("Def error") 

    def visit_bln(self, bln, env):
        return bln.bln

    def visit_num(self, num, env):
        return num.num

    def visit_eql(self, eql, env):
        left = eql.left.accept(self, env)
        right = eql.right.accept(self, env)
        if type(left) == type(right):
            return left == right
        else:
            sys.exit("Type error")


    def visit_add(self, add, env):
        left = add.left.accept(self, env)
        right = add.right.accept(self, env)
        if type(left) == type(1) and type(right) == type(1):
            return left + right
        else:
            sys.exit("Type error")


    def visit_sub(self, sub, env):
        left = sub.left.accept(self, env)
        right = sub.right.accept(self, env)
        if type(left) == type(1) and type(right == type(1)):
            return left - right
        else:
            sys.exit("Type error")


    def visit_mul(self, mul, env):
        left = mul.left.accept(self, env)
        right = mul.right.accept(self, env)
        if type(left) == type(1) and type(right == type(1)):
            return left * right
        else:
            sys.exit("Type error")


    def visit_div(self, div, env):
        left = div.left.accept(self, env)
        right = div.right.accept(self, env)
        if type(left) == type(1) and type(right == type(1)):
            return left // right
        else:
            sys.exit("Type error")


    def visit_leq(self, leq, env):
        left = leq.left.accept(self, env)
        right = leq.right.accept(self, env)
        if type(left) == type(1) and type(right == type(1)):
            return left <= right
        else:
            sys.exit("Type error")


    def visit_lth(self, lth, env):
        left = lth.left.accept(self, env)
        right = lth.right.accept(self, env)
        if type(left) == type(1) and type(right == type(1)):
            return left < right
        else:
            sys.exit("Type error")


    def visit_neg(self, neg, env):
        exp = neg.exp.accept(self, env)
        if type(exp) == type(1):
            return -1 * exp
        else:
            sys.exit("Type error")

    def visit_not(self, not_node, env):
        exp = not_node.exp.accept(self, env)
        if type(exp) == type(True):
            return not exp  
        else:
            sys.exit("Type error")

    def visit_let(self, let, env):
        definition_value = let.exp_def.accept(self, env)
        new_env = env.copy()
        new_env[let.identifier] = definition_value
        return let.exp_body.accept(self, new_env) 
    
    def visit_and(self, exp, env):
        e0 = exp.left.accept(self, env)
        if type(e0) != type(True):
            sys.exit("Type error")
        if e0:
            e1 = exp.right.accept(self, env)
            if type(e1) != type(True):
                sys.exit("Type error")
            else:
                return e1
        else:
            return False

    def visit_or(self, exp, env):
        e0 = exp.left.accept(self, env)
        if type(e0) != type(True):
            sys.exit("Type error")
        if not e0:
            e1 = exp.right.accept(self, env)
            if type(e1) != type(True):
                sys.exit("Type error")
            else:
                return e1
        else:
            return True 

    def visit_ifThenElse(self, exp, env):
        cond = exp.cond.accept(self, env)
        if type(cond) != type(True):
            sys.exit("Type error")
        if cond:
            return exp.e0.accept(self, env)
        else:
            return exp.e1.accept(self, env)

    #Recebe o env de fora
    def visit_function(self, exp, env):
        return Function(exp.formal, exp.body, env)

    def visit_rec_fun(self, exp, env):
        return RecFunction(exp.name, exp.formal, exp.body, env)
    
    def visit_app(self, exp, env):

        function_value = exp.function.accept(self, env)
        if not isinstance(function_value, Function):
            sys.exit("Type Error") 

        parameter_value = exp.actual.accept(self, env)

        new_env = function_value.env.copy()
        new_env[function_value.formal] = parameter_value 

        if isinstance(function_value, RecFunction):
            new_env[function_value.name] = function_value

        return function_value.body.accept(self, new_env)

    def visit_mod(self, exp, env):
        left = exp.left.accept(self, env)
        right = exp.right.accept(self, env)
        if type(left) == type(1) and type(right == type(1)):
            return left % right
        else:
            sys.exit("Type error")

class UseDefVisitor(Visitor):
    """
    The UseDefVisitor class reports the use of undefined variables. It takes
    as input an environment of defined variables, and produces, as output,
    the set of all the variables that are used without being defined.

    Examples:
    >>> e0 = Let('v', Add(Num(40), Num(2)), Mul(Var('v'), Var('v')))
    >>> e1 = Not(Eql(e0, Num(1764)))
    >>> ev = UseDefVisitor()
    >>> len(e1.accept(ev, set()))
    0

    >>> e0 = Let('v', Add(Num(40), Num(2)), Sub(Var('v'), Num(2)))
    >>> e1 = Lth(e0, Var('x'))
    >>> ev = UseDefVisitor()
    >>> len(e1.accept(ev, set()))
    1

    >>> e = Let('v', Add(Num(40), Var('v')), Sub(Var('v'), Num(2)))
    >>> ev = UseDefVisitor()
    >>> len(e.accept(ev, set()))
    1

    >>> e1 = Let('v', Add(Num(40), Var('v')), Sub(Var('v'), Num(2)))
    >>> e0 = Let('v', Num(3), e1)
    >>> ev = UseDefVisitor()
    >>> len(e0.accept(ev, set()))
    0
    """
    # TODO: Implement all the 13 methods of the visitor.
    def visit_var(self, var, env):
        if var.identifier in env: 
            return set() 
        else:
            return {var.identifier} 

    def visit_bln(self, bln, env):
        return set()

    def visit_num(self, num, env):
        return set()

    def visit_eql(self, eql, env):
        return eql.left.accept(self, env) | eql.right.accept(self, env)
         
    def visit_add(self, add, env):
        return add.left.accept(self, env) | add.right.accept(self, env)

    def visit_sub(self, sub, env):
        return sub.left.accept(self, env) | sub.right.accept(self, env)

    def visit_mul(self, mul, env):
        return mul.left.accept(self, env) | mul.right.accept(self, env)

    def visit_div(self, div, env):
        return div.left.accept(self, env) | div.right.accept(self, env)

    def visit_leq(self, leq, env):
        return leq.left.accept(self, env) | leq.right.accept(self, env)

    def visit_lth(self, lth, env):
        return lth.left.accept(self, env) | lth.right.accept(self, env)

    def visit_neg(self, neg, env):
        return neg.exp.accept(self, env)

    def visit_not(self, not_node, env):
        return not_node.exp.accept(self, env)

    def visit_let(self, let, env):
        undef_in_def = let.exp_def.accept(self, env)
        env_for_body = env | {let.identifier} 
        undef_in_body = let.exp_body.accept(self, env_for_body) 
        return undef_in_body |  undef_in_def 

    def visit_and(self, exp, env):
        return exp.left.accept(self, env) | exp.right.accept(self, env)

    def visit_or(self, exp, env):
        return exp.left.accept(self, env) | exp.right.accept(self, env)

    def visit_ifThenElse(self, exp, env):
        return exp.cond.accept(self, env) | exp.e0.accept(self, env) | exp.e1.accept(self, env)
    
    def visit_app(self, exp, env):
        #IMPLEMENTAR DEPOIS
        pass 

    def visit_function(self, exp, env):
        #IMPLEMENTAR DEPOIS
        pass

    def visit_rec_fun(self, exp, env):
        pass

    def visit_mod(self, exp, env):
        pass

def safe_eval(exp):
    """
    This method applies one simple semantic analysis onto an expression, before
    evaluating it: it checks if the expression contains free variables, there
    is, variables used without being defined.

    Example:
    >>> e0 = Let('v', Add(Num(40), Num(2)), Mul(Var('v'), Var('v')))
    >>> e1 = Not(Eql(e0, Num(1764)))
    >>> safe_eval(e1)
    Value is False

    >>> e0 = Let('v', Add(Num(40), Num(2)), Sub(Var('v'), Num(2)))
    >>> e1 = Lth(e0, Var('x'))
    >>> safe_eval(e1)
    Error: expression contains undefined variables.
    """
    ev1 = UseDefVisitor()
    if len(exp.accept(ev1, set())) > 0:
        print("Error: expression contains undefined variables.")
    else:
        ev2 = EvalVisitor()
        value = exp.accept(ev2, {})
        print(f"Value is {value}")


class CtrGenVisitor(Visitor):

    #No caso dessa classe, o env é o TYPE_VAR, ou seja o tipo de exp.
    def __init__(self):
        self.fresh_type_counter = 0 

    def fresh_type_var(self):
        self.fresh_type_counter += 1
        variable = f"TV_{self.fresh_type_counter}"
        return variable

    def visit_var(self, var, env):
       return {(env, var.identifier)}

    def visit_num(self, num, env):
       return {(env, type(1))} 

    def visit_sub(self, sub, env):
 
        K0 = sub.left.accept(self, type(1))
        K1 = sub.right.accept(self, type(1))
        return K0 | K1 | {(env, type(1))}       

    def visit_add(self, add, env):
 
        K0 = add.left.accept(self, type(1))
        K1 = add.right.accept(self, type(1))
        return K0 | K1 | {(env, type(1))}       

    def visit_div(self, div, env):
 
        K0 = div.left.accept(self, type(1))
        K1 = div.right.accept(self, type(1))
        return K0 | K1 | {(env, type(1))}       

    def visit_mul(self, mul, env):

        K0 = mul.left.accept(self, type(1))
        K1 = mul.right.accept(self, type(1))
        return K0 | K1 | {(env, type(1))}
        
    def visit_let(self, let, env):

        K0 = let.exp_def.accept(self, let.identifier)
        TV_2 = self.fresh_type_var()
        K1 = let.exp_body.accept(self, TV_2)
        return K0 | K1 | {(env, TV_2)}

    def visit_ifThenElse(self, exp, env):
        K0 = exp.cond.accept(self, type(True))
        K1 = exp.e0.accept(self, env)
        K2 = exp.e1.accept(self, env)
        return K0 | K1 | K2

    def visit_or(self, exp, env):
        K0 = exp.left.accept(self, type(True)) 
        K1 = exp.right.accept(self, type(True))
        return K0 | K1 | {(env, type(True))}

    def visit_bln(self, bln, env):
        return {(env, type(True))} 

    def visit_neg(self, neg, env):
        K0 = neg.exp.accept(self, type(1))
        return K0 | {(env, type(1))} 

    def visit_not(self, not_node, env):
        K0 = not_node.exp.accept(self, type(True)) 
        return K0 | {(env, type(True))}

    def visit_and(self, exp, env):
        K0 = exp.left.accept(self, type(True))
        K1 = exp.right.accept(self, type(True))
        return K0 | K1 | {(env, type(True))}

    def visit_leq(self, leq, env):
        K0 = leq.left.accept(self, type(1))
        K1 = leq.right.accept(self, type(1))
        return K0 | K1 | {(env, type(True))}

    def visit_lth(self, lth, env):
        K0 = lth.left.accept(self, type(1))
        K1 = lth.right.accept(self, type(1))
        return K0 | K1 | {(env, type(True))}

    def visit_eql(self, eql, env):
        TV_1 = self.fresh_type_var()
        K0 = eql.left.accept(self, TV_1)
        K1 = eql.right.accept(self, TV_1) 
        return K0 | K1 | {(env, type(True))}

    def visit_app(self, exp, env):
        pass
        #IMPLEMENTAR ISSO AQUI DEPOIS

    def visit_function(self, exp, env):
        pass
        #IMPLEMENTAR ISSO AQUI DEPOIS

    def visit_rec_fun(self, exp, env):
        pass

    def visit_mod(self, exp, env):
        pass

class TypeCheckVisitor(Visitor):

    def visit_var(self, var, env):
        return env[var]

    def visit_num(self, num, env):
        return type(1)

    def visit_sub(self, sub, env):

        left = sub.left.accept(self, env)
        right = sub.right.accept(self, env)
        if isinstance(left, type(1)) and isinstance(right, type(1)):
            return type(1)
        else:
            raise TypeError("Erro de tipo")

    def visit_add(self, add, env):
        left = add.left.accept(self, env)
        right = add.right.accept(self, env)
        if isinstance(left, type(1)) and isinstance(right, type(1)):
            return type(1)
        else:
            raise TypeError("Erro de tipo")


    def visit_div(self, div, env):
        left = div.left.accept(self, env)
        right = div.right.accept(self, env)
        if isinstance(left, type(1)) and isinstance(right, type(1)):
            return type(1)
        else:
            raise TypeError("Erro de tipo")


    def visit_mul(self, mul, env):
        left = mul.left.accept(self, env)
        right = mul.right.accept(self, env)
        if isinstance(left, type(1)) and isinstance(right, type(1)):
            return type(1)
        else:
            raise TypeError("Erro de tipo")

       
    def visit_let(self, let, env):

        typeE0 = let.exp_def.accept(self, env)
        if typeE0 != let.tp_var:
            raise TypeError("Erro de tipo")
        new_env = env.copy()
        new_env[let.identifier] = typeE0
        typeE1 = let.exp_body.accept(self, new_env)
        return typeE1


    def visit_ifThenElse(self, exp, env):
        cond = exp.cond.accept(self, env)
        e0 = exp.e0.accept(self, env)
        e1 = exp.e1.accept(self, env)

        if not isinstance(cond, type(True)):
            raise TypeError("Erro de tipo")

        if e0 != e1:
            raise TypeError("Erro de tipo")

        return e0

    def visit_or(self, exp, env):
        left = exp.left.accept(self, env)
        right = exp.right.accept(self, env)
        if isinstance(left, type(True)) and isinstance(right, type(True)):
            return type(True)
        else:
            raise TypeError("Erro de tipo")


    def visit_bln(self, bln, env):
        bln = bln.bln
        if isinstance(bln, type(True)):
            return type(True)
        else:
            raise TypeError("Erro de tipo")

    def visit_not(self,not_node, env):
        value = not_node.exp.accept(self, env)
        if isinstance(value, type(True)):
            return type(True)
        else:
            raise TypeError("Erro de tipo")

    def visit_neg(self, neg, env):
        value = neg.exp.accept(self, env)
        if isinstance(value, type(1)):
            return type(1)
        else:
            raise TypeError("Erro de tipo")

    def visit_and(self, exp, env):
        left = exp.left.accept(self, env)
        right = exp.right.accept(self, env)
        if isinstance(left, type(True)) and isinstance(right, type(True)):
            return type(True)
        else:
            raise TypeError("Erro de tipo")

    def visit_leq(self, leq, env):
        left = leq.left.accept(self, env)
        right = leq.right.accept(self, env)
        if isinstance(left, type(1)) and isinstance(right, type(1)):
            return type(True)
        else:
            raise TypeError("Erro de tipo")


    def visit_lth(self, lth, env):
        left = lth.left.accept(self, env)
        right = lth.right.accept(self, env)
        if isinstance(left, type(1)) and isinstance(right, type(1)):
            return type(True)
        else:
            raise TypeError("Erro de tipo")


    def visit_eql(self, eql, env):
        left = eql.left.accept(self, env)
        right = eql.right.accept(self, env)
        if isinstance(left, type(1)) and isinstance(right, type(1)):
            return type(True)
        else:
            raise TypeError("Erro de tipo")


    def visit_app(self, exp, env):

        function_type = exp.function.accept(self, env)
        actual_type = exp.function.accept(self, env)
        
        if not isinstance(function_type, ArrowType):
            raise TypeError("Erro de tipo")

        if not isinstance(actual_type, function_type.hd):
            raise TypeError("Erro de tipo")
            
        return function_type.tl

    def visit_function(self, exp, env):

        new_env = env.copy()
        new_env[exp.formal] = exp.tp_var

        body_type = exp.body.accept(self, new_env)

        return ArrowType(exp.tp_var, body_type)

    def visit_rec_fun(self, exp, env):
        #NAO IMPLEMENTAR

    def visit_mod(self, exp, env):
        left = exp.left.accept(self, env)
        right = exp.right.accept(self, env)
        if isinstance(left, type(1)) and isinstance(right, type(1)):
            return type(1)
        else:
            raise TypeError("Erro de tipo")

