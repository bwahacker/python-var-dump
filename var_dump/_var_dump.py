from __future__ import print_function
from types import NoneType

__author__ = "Shamim Hasnath"
__copyright__ = "Copyright 2013, Shamim Hasnath"
__license__ = "BSD License"
__version__ = "1.0.1"


TAB_SIZE = 4



def display(o, space, num, key, typ):
    st = ""
    l = []
    if key:
        if typ is dict:
            st += " " * space + "['%s'] => "
        else:
            st += " " * space + "%s => "
        l.append(key)
    elif space > 0:
        st += " " * space + "[%d] => "
        l.append(num)
    else:  # at the very start
        st += "#%d "
        l.append(num)

    if type(o) in (tuple, list, dict, int, str, float, long, bool, NoneType, unicode):
        st += "%s(%s) "
        l.append(type(o).__name__)

        if type(o) in (int, float, long, bool, NoneType):
            l.append(o)
        else:
            l.append(len(o))

        if type(o) in (str, unicode):
            st += '"%s"'
            l.append(o)

    elif type(o).__name__ == 'datetime':
        st += "%s(%s)"
        l.append(type(o).__name__)
        l.append(o.__str__())

    elif isinstance(o, object):
        st += "object(%s) (%d)"
        l.append(o.__class__.__name__)
        l.append(len(getattr(o, '__dict__', {})))

    print(st % tuple(l))

#
# Dumb little state addition to deal with dumping huge python data structures.
#
class _State:
    def __init__(self, md):
        if md is None:
            md = -1

        self._max_depth = md 
        self._depth = 0
        self.last_printed_more_msg = False
        self.visited = []

    def inc_depth(self):
        self._depth += 1

    def dec_depth(self):
        self._depth -= 1
    
    def traverse_current(self):
        return (self._max_depth > 0) and (self._depth < self._max_depth)

    def reset_print_marker(self):
        self.last_printed_more_msg = False

    def add_visited_object(self, o):
        self.visited.append(o)

    def has_visited_object(self, o):
        return o in self.visited

def dump(state, o, space, num, key, typ):
    if not state.traverse_current():
        if not state.last_printed_more_msg:
            print("%s [and possibly more here]" % (" " * (space + TAB_SIZE)))
        state.last_printed_more_msg = True
        return

    if state.has_visited_object(o):
        print("%s [skipping object found in a cycle?]" % (" " * (space + TAB_SIZE)))
        return

    state.add_visited_object(o)
    state.reset_print_marker()

    if type(o) in (str, int, float, long, bool, NoneType, unicode):
        display(o, space, num, key, typ)

    elif isinstance(o, object):
        display(o, space, num, key, typ)
        num = 0
        if type(o) in (tuple, list, dict):
            typ = type(o)  # type of the container of str, int, long, float etc
        elif isinstance(o, object):
            o = getattr(o, '__dict__', {})
            typ = object
        for i in o:
            space += TAB_SIZE
            state.inc_depth()
            if type(o) is dict:
                dump(state, o[i], space, num, i, typ)
            else:
                dump(state, i, space, num, '', typ)
            num += 1
            space -= TAB_SIZE
            state.dec_depth()

def var_dump(*obs, **kwargs):
    """
      shows structured information of a object, list, tuple etc

      pass max_depth=<number> to prevent super deep recursive traversal.

      TODO:  Need to keep a stack and not let circular references cause infinite loops
    """
    max_depth = kwargs.get('max_depth')
    state = _State(max_depth)
    i = 0
    for x in obs:
        print("greetings")
        dump(state, x, 0, i, '', object)
        i += 1
