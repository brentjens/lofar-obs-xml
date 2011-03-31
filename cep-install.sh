#!/bin/sh

comm="rsync -avz --delete brentjens@dop95.astron.nl:`basename $1` `basename $1`"
echo $comm
rsync -avz $1 brentjens@dop95.astron.nl: && lfc lfe001 "$comm"
