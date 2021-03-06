#!/bin/bash
gcc CUTE/demo/c_lib/libsim.c -o CUTE/demo/c_lib/libsim.so -fPIC -shared -pthread -O3
gcc CUTE/demo/c_lib/libpath.c -o CUTE/demo/c_lib/libpath.so -fPIC -shared -O3

if [ -n "$2" ]
then
    cp -r $2 CUTE/
fi

source venv/bin/activate
python CUTE/manage.py runserver $1
