#!/bin/sh

INTERNAL_PORT=7999
OUTPUT_PORT=3000

# start flask server
FLASK_APP=python/main.py FLASK_ENV=develpment python3 -m flask run --port $INTERNAL_PORT
# start react server
cd frontend
PORT=$INTERNAL_PORT parcel src/index.html -p $OUTPUT_PORT

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # ...
        xdg-open http://localhost:$OUTPUT_PORT
elif [[ "$OSTYPE" == "darwin"* ]]; then
        # Mac OSX
        open http://localhost:$OUTPUT_PORT
elif [[ "$OSTYPE" == "cygwin" ]]; then
        # POSIX compatibility layer and Linux environment emulation for Windows
        xdg-open http://localhost:$OUTPUT_PORT
elif [[ "$OSTYPE" == "msys" ]]; then
        # Lightweight shell and GNU utilities compiled for Windows (part of MinGW)
        start http://localhost:$OUTPUT_PORT
elif [[ "$OSTYPE" == "win32" ]]; then
        # I'm not sure this can happen.
        start http://localhost:$OUTPUT_PORT
elif [[ "$OSTYPE" == "freebsd"* ]]; then
        # ...
        xdg-open http://localhost:$OUTPUT_PORT
else
        # Unknown.
        echo "unknown OS type"
fi