import os
import sys
import time

from ctypes import cdll, c_int, c_double, c_char_p, Structure, POINTER

ENTITY_2_ID = {}
ENTITY = [] # must be bytes for 'ctypes'
ENTITY_LEN = []
cnt = 0
for entity in open("../CUTE/data/entity.txt", 'r', encoding='utf-8'):
    ENTITY_2_ID[entity.strip()] = cnt
    ENTITY.append(entity.strip().encode('utf-8')) # must be bytes for 'ctypes'
    ENTITY_LEN.append(len(entity.strip()))
    cnt += 1

TOT_ENTITY = cnt
ALL_ENTITY_TYPE = c_char_p * TOT_ENTITY
ALL_ENTITY = ALL_ENTITY_TYPE(*ENTITY)
ALL_ENTITY_LEN_TYPE = c_int * TOT_ENTITY
ALL_ENTITY_LEN = ALL_ENTITY_LEN_TYPE(*ENTITY_LEN)

class Node(Structure):
    _fields_ = [("str", c_char_p), ("sim", c_double)]

def test(test_entities, top_k, thread_num):

    libsim = cdll.LoadLibrary('so_file/%d.so' % thread_num)
    libsim.find.argtypes = [c_char_p, c_int, ALL_ENTITY_TYPE, ALL_ENTITY_LEN_TYPE, c_int]
    libsim.find.restype = POINTER(Node)

    tot = 0.0
    for input_name in test_entities:
        start = time.time()
        candidates = libsim.find(input_name.encode('utf-8'), TOT_ENTITY, ALL_ENTITY, ALL_ENTITY_LEN, top_k)
        end = time.time()
        tot += end - start

    return tot / 10

def main():
    test_entities = ["china", "xijinping", "pengliyuan", "unitedstates", "barack_obama", "michelle_obama", "ximingze", "Joebiden", "canada", "justintrudeau"]
    top_k = [20, 50, 100]
    for k in top_k:
        results = []
        for i in range(1, 33):
            r = test(test_entities, k, i)
            print("thread: %d, top_k: %d, time: %lf" % (i, k, r))
            results.append(r)
        print(results)



if __name__ == '__main__':
    main()
