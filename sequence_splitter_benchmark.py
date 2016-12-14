import timeit
import keyword
import re

def isidentifier(candidate):
    "Is the candidate string an identifier in Python 2.x"
    is_not_keyword = candidate not in keyword.kwlist
    pattern = re.compile(r'^[a-z_][a-z0-9_]*$', re.I)
    matches_pattern = bool(pattern.match(candidate))
    return is_not_keyword and matches_pattern

kabie=("isplit_kabie",
"""
import itertools
def isplit_kabie(iterable,splitters):
    return [list(g) for k,g in itertools.groupby(iterable,lambda x:x in splitters) if not k]
""" )

ssplit=("ssplit",
"""
def ssplit(seq,splitters):
    seq=list(seq)
    if splitters and seq:
        result=[]
        begin=0
        for end in range(len(seq)):
            if seq[end] in splitters:
                if end > begin:
                    result.append(seq[begin:end])
                begin=end+1
        if begin<len(seq):
            result.append(seq[begin:])
        return result
    return [seq]
""" )

ssplit2=("ssplit2",
"""
def ssplit2(seq,splitters):
    seq=list(seq)
    if splitters and seq:
        splitters=set(splitters).intersection(seq)
        if splitters:
            result=[]
            begin=0
            for end in range(len(seq)):
                if seq[end] in splitters:
                    if end > begin:
                        result.append(seq[begin:end])
                    begin=end+1
            if begin<len(seq):
                result.append(seq[begin:])
            return result
    return [seq]
""" )

emile=("magicsplit",
"""
def _itersplit(l, *splitters):
    current = []
    for item in l:
        if item in splitters:
            yield current
            current = []
        else:
            current.append(item)
    yield current

def magicsplit(l, splitters):
    return [subl for subl in _itersplit(l, *splitters) if subl]
""" )

emile_improved=("magicsplit2",
"""
def _itersplit(l, *splitters):
    current = []
    for item in l:
        if item in splitters:
            if current:
                yield current
                current = []
        else:
            current.append(item)
    if current:
        yield current

def magicsplit2(l, splitters):
    if splitters and l:
        return [i for i in _itersplit(l, *splitters)]
    return [list(l)]
""" )

karl=("ssplit_karl",
"""
def ssplit_karl(original,splitters):
    indices = [i for (i, x) in enumerate(original) if x in splitters]
    ends = indices + [len(original)]
    begins = [0] + [x + 1 for x in indices]
    return [original[begin:end] for (begin, end) in zip(begins, ends)]
""" )

ryan=("split_on",
"""
from functools import reduce
def split_on (seq, delims, remove_empty=True):
    '''Split seq into lists using delims as a delimiting elements.

    For example, split_on(delims=2, list=xrange(0,5)) yields [ [0,1], [3,4] ].

    delims can be either a single delimiting element or a list or
    tuple of multiple delimiting elements. If you wish to use a list
    or tuple as a delimiter, you must enclose it in another list or
    tuple.

    If remove_empty is False, then consecutive delimiter elements or delimiter elements at the beginning or end of the longlist'''
    delims=set(delims)
    def reduce_fun(lists, elem):
        if elem in delims:
            if remove_empty and lists[-1] == []:
                # Avoid adding multiple empty lists
                pass
            else:
                lists.append([])
        else:
            lists[-1].append(elem)
        return lists
    result_list = reduce(reduce_fun, seq, [ [], ])
    # Maybe remove trailing empty list
    if remove_empty and result_list[-1] == []:
        result_list.pop()
    return result_list
""" )

cases=(kabie, emile, emile_improved, ssplit ,ssplit2 ,ryan)

data=(
    ([1, 4, None, 6, 9, None, 3, 9, 4 ],(None,)),
    ([1, 4, None, 6, 9, None, 3, 9, 4 ]*5,{None,9,7}),
    ((),()),
    (range(1000),()),
    ("Split me",('','')),
    ("split me "*100,' '),
    ("split me,"*100,' ,'*20),
    ("split me, please!"*100,' ,!'),
    (range(100),range(100)),
    (range(100),range(101,1000)),
    (range(100),range(50,150)),
    (list(range(100))*30,(99,)),
    )

params="seq,splitters"

def benchmark(func,code,data,params='',times=10000,rounds=3,debug=''):
    #assert(func.isidentifier())
    assert(isidentifier(func))
    tester = timeit.Timer(stmt='{func}({params})'.format(
                                func=func,params=params),
                          setup="{code}\n".format(code=code)+
            (params and "{params}={data}\n".format(params=params,data=data)) +
            (debug and """ret=repr({func}({params}))
print({func}.__name__.rjust(16),":",ret[:30]+"..."+ret[-15:] if len(ret)>50 else ret)
                       """.format(func=func,params=params)))
    results = [tester.timeit(times) for i in range(rounds)]
    if not debug:
        print("{:>16s} takes:{:6.4f},avg:{:.2e},best:{:.4f},worst:{:.4f}".format(
            func,sum(results),sum(results)/times/rounds,min(results),max(results)))

def testAll(cases,data,params='',times=10000,rounds=3,debug=''):
    if debug:
        times,rounds = 1,1
    for dat in data:
        sdat = tuple(map(repr,dat))
        print("{}x{} times:".format(times,rounds),
              ','.join("{}".format(d[:8]+"..."+d[-5:] if len(d)>16 else d)for d in map(repr,dat)))
        for func,code in cases:
            benchmark(func,code,dat,params,times,rounds,debug)

if __name__=='__main__':
    testAll(cases,data,params,500,10)#,debug=True)
