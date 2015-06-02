#!/bin/sh

USER=$1

rsync -avz --no-group --delete -e "ssh -A ${USER}@portal.lofar.eu ssh" ./ ${USER}@lhn001:genvalobs/
