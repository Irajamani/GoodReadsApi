#!/bin/bash
export FLASK_APP=$"application.py"
export DATABASE_URL=$"postgresql://postgres:iR@030199@localhost/test"
export FLASK_DEBUG=$"1"
# use source test.sh to make it available to current processes
# rather than sh which forks a child process.