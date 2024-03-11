#!/usr/local/casperscript/bin/cs
% muted post horn from Crying of Lot 49
/inch {72 mul} bind def
/unit {0.25 inch mul} bind def
pagesize /pagewidth exch def /pageheight exch def
/segment 3 unit def  % see README.md
/radius segment 2 div def
/secant {cos 1.0 exch div} bind def  % hypotenuse over near
/bell 30 secant segment mul def 
1 inch 4 inch moveto
/posthorn {
  segment 0 rlineto  % mouthpiece to start of loop
  currentpoint radius sub radius 90 450 arc  % the loop
  segment 0 rlineto  % loop to start of bell
  30 rotate  bell 0 rlineto
  -120 rotate bell 0 rlineto
  -120 rotate bell 0 rlineto
  -150 rotate  % reorient left to right
} bind def
gsave posthorn stroke grestore
-1 unit 0 rmoveto posthorn stroke
showpage
