import os
import sys
import math

def extracting():
    valid_set = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_,.()'"
    entity = set()
    relation = set()

    fout = open('facts.txt', 'w')
    fe = open('../CUTE/data/entity.txt', 'w')
    fp = open('../CUTE/data/relation.txt', 'w')
    first = True
    for line in open(sys.argv[1]):
        if first:
            first = False
            continue
        
        line = line.strip().split('\t')
        flag = True
        for c in line[1].strip("<>"):
            if c not in valid_set:
                flag = False
                break
        if flag == False:
            continue

        for c in line[3].strip("<>"):
            if c not in valid_set:
                flag = False
                break
        if flag == False:
            continue
        

        if line[2] == "<hasWebsite>" or line[2] == "<imports>" or line[2] == "<exports>":
            continue
        
        entity.add(line[1].strip("<>"))
        entity.add(line[3].strip("<>"))
        relation.add(line[2].strip("<>"))
        fout.write(line[1].strip("<>") + " " + line[2].strip("<>") + " " + line[3].strip("<>") + "\n")

    fout.close()
    for e in entity:
        fe.write(e + "\n")
    fe.close()
    for r in relation:
        fp.write(r + "\n")
    fp.close()

def fact2id():
    entity = {}
    cnt = 0
    for e in open("../CUTE/data/entity.txt"):
        entity[e.strip()] = cnt
        cnt += 1

    relation = {}
    cnt = 0
    for r in open("../CUTE/data/relation.txt"):
        relation[r.strip()] = cnt
        cnt += 1

    fout = open("fact2id.txt", "w")
    for line in open("facts.txt"):
        line = line.strip().split(" ")
        fout.write(str(entity[line[0]]) + " " + str(entity[line[2]]) + " " + str(relation[line[1]]) + "\n")

    fout.close()

def make_weight():
    edges = []
    dic_entity = {}
    dic_p = {}
    dic_po = {}
    dic_sp = {}
    tot = 0
    for edge in open("fact2id.txt"):
        edge = edge.strip().split(" ")
        edges.append(edge)

        if edge[0] in dic_entity:
            dic_entity[edge[0]] += 1
        else:
            dic_entity[edge[0]] = 1

        if edge[1] in dic_entity:
            dic_entity[edge[1]] += 1
        else:
            dic_entity[edge[1]] = 1

        if edge[2] in dic_p:
            dic_p[edge[2]] += 1
        else:
            dic_p[edge[2]] = 1

        if edge[2] + " " + edge[1] in dic_po:
            dic_po[edge[2] + " " + edge[1]] += 1
        else:
            dic_po[edge[2] + " " + edge[1]] = 1

        if edge[0] + " " + edge[2] in dic_sp:
            dic_sp[edge[0] + " " + edge[2]] += 1
        else:
            dic_sp[edge[0] + " " + edge[2]] = 1

        tot += 1



    fout = open("../CUTE/data/graph.txt", "w")
    for edge in edges:
        w = (dic_po[edge[2] + " " + edge[1]]) * 1.0 / dic_entity[edge[1]] * math.log(float(tot * 1.0 / dic_p[edge[2]]))
        w += (dic_sp[edge[0] + " " + edge[2]]) * 1.0 / dic_entity[edge[0]] * math.log(float(tot * 1.0 / dic_p[edge[2]]))
        w = w * 1.0 / 2
        fout.write("%s %s %s %.2lf\n" % (edge[0], edge[1], edge[2], w))
    fout.close()

def main():
    if len(sys.argv) < 2:
        print('Usage: python3 facts_extractor.py [raw_facts_file]')
        return
    extracting()
    print("extracting done.")
    fact2id()
    print("fact2id done.")
    make_weight()
    os.remove('facts.txt')
    os.remove('fact2id.txt')
   

if __name__ == '__main__':
    main()
