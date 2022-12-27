
import os
import re
from osOps import OsKit
from datetime import datetime, timedelta

OsKit().setCWDtoFile( __file__ )

file = (
    f"The.Good.Boss.2021.SPANISH.WEBRip.x264-YTS.MX-YIFY-English_fixed_221115_164206932805_fxd_221115_182149977422_fxd_221115_183357296129.srt" )

pattern = (
    r"^\s*(\d+:\d+:\d+,\d+)[^\S\n]+-->[^\S\n]+(\d+:\d+:\d+,\d+)((?:\n(?!\d+:"
    + r"\d+:\d+,\d+\b|\n+\d+$).*)*)" )

def adjustStamp(_line, by, start="00:00:00,000" ):
    
    tFromStr, tToStr = [ el.strip() for el in _line.split(" --> ") ]
    
    tFrom, tTo = ( datetime.strptime(
        el, '%H:%M:%S,%f') for el in [ tFromStr, tToStr ] )
        
    if tFrom < datetime.strptime( start, '%H:%M:%S,%f' ): return _line
    tFromAdj, tToAdj = [ t + timedelta(seconds=by) for t in [ tFrom, tTo] ]
    
    matches = {
        tFromStr : tFromAdj.strftime('%H:%M:%S,%f')[:-3],
        tToStr : tToAdj.strftime('%H:%M:%S,%f')[:-3], }
    
    lineFixed = _line
    for match, replacement in matches.items():
        lineFixed = lineFixed.replace( match, replacement )
    
    return lineFixed


saveName = f"{os.path.splitext( file )[0]}_fxd_{OsKit().dtStamp()}.srt"

with (
    open( file, 'r', encoding='utf-8' ) as orig,
    open( saveName, "w", encoding='utf-8') as fixed ):
    lines = orig.readlines()
    for lineNum in range(len(lines)):
        if re.match(pattern, lines[lineNum]): fixed.write( 
            adjustStamp( lines[lineNum], 2, start="00:13:30,000" ))
        else: fixed.write( lines[lineNum] )


print( "Adjust completed." )