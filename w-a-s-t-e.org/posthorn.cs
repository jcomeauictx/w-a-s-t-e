#!/usr/local/casperscript/bin/cs
% muted post horn from Crying of Lot 49
/inch {72 mul} bind def
/unit {0.25 inch mul} bind def
pagesize /pagewidth exch def /pageheight exch def
/segment 3 unit def  % see README.md
/radius segment 2 div def
/secant {cos 1.0 exch div} bind def  % hypotenuse over near
/bell 30 secant segment mul def
/erase {gsave 1 setgray rectfill grestore} bind def  % whitefill rectangle
/pathrect {  % pathbbox to rectangle
  pathbbox  % returns path as llx lly urx ury
  % we want to convert this into x y width height
  2 index sub exch 3 index sub exch
} bind def
/patherase {  % erase current path
  pathrect erase
} bind def
/posthorn {
  1 unit 5 div setlinewidth
  segment 0 rlineto  % mouthpiece to start of loop
  currentpoint radius sub radius 90 450 arc  % the loop
  segment 0 rlineto  % loop to start of bell
  30 rotate  bell 0 rlineto
  -120 rotate bell 0 rlineto
  -120 rotate bell 0 rlineto
  -150 rotate  % reorient left to right
} bind def
/measure {  % let's measure the muted posthorn so as to render it best
  gsave
  0 0 moveto
  gsave posthorn strokepath pathbbox
} bind def
/muted-posthorn {  % the ultimate form
  gsave
  1 unit 0 rmoveto
  gsave posthorn stroke grestore
  -1 unit 0 rmoveto currentpoint newpath moveto
  gsave posthorn strokepath patherase grestore
  posthorn stroke
  grestore
} bind def
measure
4 2 roll  % move llx and lly to top of stack
exch pop  % get rid of almost-zero llx
sub  % compute total y offset
/hornheight exch def
/hornwidth exch def
newpath  % clear the horn used for measuring so it doesn't show on `stroke`
% let's assume page height greater than width, and that horn will fit width
% if that doesn't work, we need to add more code to compute a better fit
(/hornwidth: ) print hornwidth =
(/hornheight: ) print hornheight =
(/pagewidth: ) print pagewidth =
(/pageheight: ) print pageheight =
1 inch 4 inch moveto muted-posthorn showpage
