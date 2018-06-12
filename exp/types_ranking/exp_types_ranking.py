import os
import sys


count_d = {}
count_f = {}
count_o = {}

def cmp_f(x):
    if x in count_f:
        return count_f[x]
    return 288.74

def cmp_o(x):
    if x in count_o:
        return count_o[x]
    return 0.964

def cmp_d(x):
    if x in count_d:
        return count_d[x]
    return 4.283

def frequency():
    for line in open("typeCount.txt"):
        line = line.strip().split(" ")
        count_f[line[0]] = float(line[1])

    candidates = [one_type.strip() for one_type in open("types.txt")]

    candidates.sort(key=cmp_f)
    print("frequency:", candidates)


def du():
    for line in open("/Users/wzc/Downloads/taxonomy.txt"):
        line = line.strip().split(" ")
        x = line[0].strip("<>")
        y = line[2].strip("<>")
        if x not in count_d:
            count_d[x] = 0
        if y not in count_d:
            count_d[y] = 0
        count_d[x] += 1
        count_d[y] += 1


    candidates = [one_type.strip() for one_type in open("types.txt")]

    candidates.sort(key=cmp_d)
    print("du:", candidates)

def ours():
    for line in open("/Users/wzc/CUTE/CUTE/data/types_ranking.txt"):
        line = line.strip().split(" ")
        count_o[line[0]] = float(line[1])

    candidates = [one_type.strip() for one_type in open("types.txt")]

    candidates.sort(key=cmp_o, reverse=True)
    print("ours:", candidates)

def main():

    frequency()
    du()
    ours()

    tot = 0
    for t in count_f.keys():
        tot += count_f[t]
    print(tot / len(count_f))


if __name__ == '__main__':
    main()