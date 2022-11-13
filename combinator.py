
from functools import wraps
from itertools import combinations
from timeit import default_timer as timer

# range combinators with timer wrapping and generator usage


def timed(f):
    """function timer wrapper"""
    @wraps(f)
    def wrap(*args, **kw):
        t1 = timer()
        result = f(*args, **kw)
        print( f'\n{f.__name__.upper(): <8}: {timer()-t1:.8f}\n\n' )
        return result
        
    return wrap


# list-builder method
@timed
def getCombos1( _rangeSize ):
    # combos = []
    for n, r in enumerate( ( vNums:= range( 1, _rangeSize + 1 )) ):
        # combos += combinations( vNums, r )
        comboGrp = combinations( vNums, r )
        print( f"{len([ c for c in comboGrp ])} combos for range size {n+1}" )
    # return combos


# generator yield method
def getCombinator( _rangeSize ):
    for r in ( vNums:= range( 1, _rangeSize + 1 )):
        yield combinations( vNums, r )

@timed
def getCombos2( rSiz ):
    for n, comboGrp in enumerate(getCombinator( rSiz )): 
        print( f"{len([ c for c in comboGrp ])} combos for range size {n+1}" )


# test both
for rangeSize in range(1, 30):
    print( f"RANGE SIZE: {rangeSize}\n" )
    getCombos1( rangeSize )
    getCombos2( rangeSize )
    print( "\n========================\n" )
