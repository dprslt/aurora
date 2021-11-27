#!/bin/bash

fswatch -o -r ../ |  xargs -n 1 ./upload.sh