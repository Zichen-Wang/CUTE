#!/bin/bash
for i in {1..32}
do
    gcc libsim.c -o so_file/$i.so -D MAX_THREAD=$i -fPIC -pthread -shared -O3
done
