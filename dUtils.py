import OsOps  # see github.com/romstroller/FileTools

# kaggle acquire
from kaggle.api.kaggle_api_extended import KaggleApi
from zipfile import ZipFile
from pathlib import Path

import pandas as pd
import time
import json
import os

# notebook outputs
from IPython.display import Markdown
from IPython.display import Code
from IPython.display import display
from IPython.core.display import HTML


ops = OsOps.Ops()

# kit = osOps.OsKit()

def getKaggleSet( owner, dSetTitle, keyPath = None ):
    """
    Authenticate with Kaggle, download datasete and load to Pandas
    Authentication looks for your Kaggle key file at the defined path
    """
    
    def download(_keyPath = keyPath):
        if not _keyPath: _keyPath = f"{userDir}\\PYC\\_ADMIN\\kaggle.json"
        with open( _keyPath, 'r' ) as f: keyDict = json.load( f )
        userTitle, keyTitle = keyDict.keys()
        os.environ[ 'KAGGLE_USERNAME' ] = keyDict[ userTitle ]
        os.environ[ 'KAGGLE_KEY' ] = keyDict[ keyTitle ]
        api = KaggleApi()
        api.authenticate()
        api.dataset_download_files( f'{owner}/{dSetTitle}', path="." )
        return True
    
    downloadStarted = False
    currWorkDir = os.getcwd()
    userDir = Path.home()
    dataFname = None
    
    while not dataFname:
        sortedFs = ops.datesortFiles( currWorkDir, dSetTitle )
        if len( sortedFs ) == 0:
            if not downloadStarted: downloadStarted = download()
            else: print( f"- [{osOps.OsKit().dtStamp()}] Await Kaggle API request" )
            time.sleep( 1 )
        else:
            dataFname, dated = list( sortedFs.items() )[ 0 ]
            print( f"- [{(st := osOps.OsKit().dtStamp())}] Got '{dataFname}'\n"
                   f"{' ' * (len( st ) + 5)}{dated=}" )
    
    # extract and identify datafiles
    datDir = f"{currWorkDir}\\data_or"
    if not os.path.exists( datDir ): os.makedirs( datDir )
    if dataFname and Path( dataFname ).suffix == ".zip":
        with ZipFile( dataFname, 'r' ) as zipf: zipf.extractall( datDir )
    dataPaths = [ f"{datDir}\\{pth}" for pth in os.listdir( datDir )
        if Path( pth ).suffix == ".csv" ]
    
    return (pd.read_csv( [ pth for pth in dataPaths ][ 0 ] )
            if len( dataPaths ) > 0 else None)


def getColTypes( _df, pr=False ):
    
    """ if pr, outputs type's .__name__
        else return dct(<colname:string>, <coltype:type>) """
    
    colTypes = { c : 
        [ t for t in set( type(_df.iloc[n][c]) 
            for n in range(0, _df.shape[0] ) ) ] 
            for c in _df.columns }
    
    if not pr: return colTypes
    
    for c, tLi in colTypes.items():
        print( f"{c+':': <{max( [ len(str(t)) for t in colTypes.keys() ] )+2}}"
            f"{[ t.__name__ for t in tLi ]}" )


def wrapBulletValue( _val, room = 79, inset = None, bulletsize = 3 ):
    """ for bulleted item-value printing for bullet lists;
        value is split on space closest to room-limit,
        inset is applied to all lines after first line,
        which is already inset by the bullet-item """
    
    def getLine( _rmndr, _room ):
        # return if entire string fits in line
        if len( _rmndr ) <= room: return _rmndr, [ ]
        vSplit = _rmndr.split( ' ' )
        
        if firstLine: _room = room - inset
        
        # return segment of first split item if it is too big
        if len( (first := vSplit[ 0 ]) ) > _room:
            _rmndr = f"{first[ _room: ]} {' '.join( vSplit[ 1: ] )}"
            return first[ :_room ], _rmndr
        else:  # else add words to line until room reached
            _line = ""
            while bool( vSplit ) & (len( _line + vSplit[ 0 ] ) <= _room):
                _line += f"{vSplit.pop( 0 )} "
            return _line[ :-1 ], ' '.join( vSplit )  # remove traling space
    
    _val = str( _val )
    valueWrapped = ""
    
    firstLine = True
    
    while True:
        line, rmndr = getLine( _val, room )
        firstLine = False
        # add newline if there is remainder to split, else return
        if len( rmndr ) == 0: return valueWrapped + f"{line}"
        else:
            _val = ((inset + bulletsize) * " ") + rmndr if inset else rmndr
            valueWrapped += f"{line}\n"


def write( inp = None, bullets = False, code = False, thinBreak = False,
    header = 0 ):
    """ Parses some htmlbreak for markdown
        Bullets require list of tuples
    """
    if (h := header) > 0: return display( HTML( f"<h{h}> {inp} </h{h}>" ) )
    elif thinBreak: return display(
        HTML( '<hr style="height:2px;background-color:gray">' ) )
    elif bullets:
        code = True
        bullets = ""
        x = 0  # get padding from longest key string
        for k, _ in inp: x = x if x >= (y := len( k )) else y
        for item, value in inp:
            value = wrapBulletValue( value, inset=(x + 4) )
            bullets += f" - {item: <{x + 4}}{value}\n"
        inp = bullets
    
    if code: return display( Code( inp ) )
    return display( Markdown( inp ) )
    
    
def displayDF( _df, mask = None, rng = None, title = None, align = 'left',
    allRows = False ):
    try: _df = _df.loc[ mask ] if mask.any() else _df
    except AttributeError: pass
    
    if title: display( HTML( f"<h4> {title} </h4>" ) )
    if rng: _df = _df[ rng[ 0 ]: rng[ 1 ] ]
    minRows = _df.shape[0] if allRows else None
    
    _df.style.set_properties(
        **{ 'color': 'black !important',
            'border': '1px black solid !important',
            'text-align': align } )
    
    with pd.option_context(
        'display.min_rows', minRows,
        'notebook_repr_html', True,
        'max_colwidth', 200,
        'styler.latex.multicol_align', 'l'
        ): display( _df )


def tPrint( msg ):
    write( [ (f"[{osOps.OsKit().dtStamp()}]", msg) ], bullets=True )

