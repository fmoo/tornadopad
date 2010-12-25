Goal
====

This project is basically my sandbox for testing out collaborative tricks using
tornado, javascript, and websockets.

It may evolve eventually into an full open source collaborative CMS.  Only time
will tell.

Contents
========

simplechat
----------
Located in simplechat/, this is a really quick example of chat using websockets.

sharearea
---------
Located in sharearea/, this is a collaborative textarea.  It uses a "big blob" 
or substring approach, where all edits are done using bytes offsets and ranges.
This approch is generally flawed if both users are attempting to edit
simultaneously (the edits near the top will drastically change the offsets of
outstanding edits at the bottom, and the letters will get shuffled up)

