from Expression import *
from Visitor import *

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
