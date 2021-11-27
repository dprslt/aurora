#!/bin/bash

echo "Syncing"
rsync -avz -r --exclude-from=.rsyncignore .. aurora:aurora-dev > /dev/null 