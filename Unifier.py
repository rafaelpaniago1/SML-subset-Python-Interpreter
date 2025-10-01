from Expression import *
from Visitor import *
import sys

def unify(constraints, sets):
    
    if not constraints:
        return sets
    else:
        t0, t1 = constraints[0]
        rest = constraints[1:]
        if t0 != t1:
            s0 = sets.setdefault(t0, set())
            s1 = sets.setdefault(t1, set())
            new_set = s0 | s1 | {t0, t1}
            for type_name in new_set:
                sets[type_name] = new_set

        return unify(rest, sets)


def name_sets(sets):
    """
    This method replaces type sets with "canonical type names". A canonical
    type name is the name of a type set. For instance, the type set
    {'a', 'b', type(int)} has the canonical name type(int)

    Notice that this method produces two types of error messages:
    * Polymorphic type: if any canonical type set is empty
    * Ambiguous type: if any canonical type set contains more than one element.
    In both cases, if any of these errors happen, the program should stop with
    the following error message: 'Type error'

    Example:
        >>> sets = name_sets({'a': {'a', 'b', type(1)}, 'b': {'a', 'b', type(1)}})
        >>> [sets['a'], sets['b']]
        [<class 'int'>, <class 'int'>]

        >>> sets = name_sets({'a': {'a', type(1)}, 'b': {'b', type(True)}})
        >>> [sets['a'], sets['b']]
        [<class 'int'>, <class 'bool'>]
    """
    canonical_set = dict()
    for key, my_set in sets:

        set_type = None
        for element in my_set:

            if set_type is not None and isinstance(element, type):
                if element != set_type:
                    sys.exit("Type Error") 

            if isinstance(element, type):
                set_type = element

        if set_type is None:
            sys.exit("Type Error") 

        canonical_set[key] = set_type

    return canonical_set

def infer_types(expression):
    """
    This method maps all the program variables to type names. We have
    implemented this method for you. This implementation might help you to
    understand how the other two methods, unify and name_sets are meant to
    work.

    Example:
        >>> e = Let('v', Num(42), Var('v'))
        >>> type_names = infer_types(e)
        >>> type_names['v']
        <class 'int'>

        >>> e = Let('v', Num(1), Let('y', Var('v'), Var('y')))
        >>> type_names = infer_types(e)
        >>> [type_names['v'], type_names['y']]
        [<class 'int'>, <class 'int'>]

        >>> e0 = Let('v', Num(1), Let('y', Var('v'), Var('y')))
        >>> e1 = IfThenElse(Lth(e0, Num(2)), Bln(True), Bln(False))
        >>> e2 = Let('w', e1, And(Var('w'), Var('w')))
        >>> type_names = infer_types(e2)
        >>> [type_names['v'], type_names['w'], type_names['y']]
        [<class 'int'>, <class 'bool'>, <class 'int'>]
    """
    ev = CtrGenVisitor()
    constraints = list(expression.accept(ev, ev.fresh_type_var()))
    type_sets = unify(constraints, {})
    return name_sets(type_sets)
