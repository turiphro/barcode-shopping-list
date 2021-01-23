#!/bin/sh

gunicorn run:api -w 1 --threads 2 -b 0.0.0.0:$PORT