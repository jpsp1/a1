#!/bin/bash
d=`date`
git commit -m "updates a $d" -a
git push -u origin main
