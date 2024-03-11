#!/usr/local/casperscript/bin/cs
# muted post horn from Crying of Lot 49
/inch {72 mul} bind def
pagesize /pagewidth exch def /pageheight exch def
/segment 3 inch def  # see README.md
/radius segment 2 div def
1 inch 4 inch moveto
segment 0 rlineto  # mouthpiece to start of loop
currentpoint radius sub radius 90 450 arc  # the loop
segment 0 rlineto  # loop to start of bell
stroke
showpage
