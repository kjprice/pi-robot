#!/bin/bash
cd "$(dirname "$0")"
cd ..

nodemon -e py,sh -x "python -m python.tests"
