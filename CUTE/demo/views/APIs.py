from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.conf import settings

from ctypes import cdll, c_int, c_double, c_char_p, Structure, POINTER

import os

import requests
import threading
import json
from ..utils import *

def entity_recommendation(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("<h1>Please request via POST</h1>")

    class Node(Structure):
        _fields_ = [("str", c_char_p), ("sim", c_double)]

    json_dict = json.loads(request.body.decode('utf-8'))
    input_name = json_dict["input_name"]
    top_k = int(json_dict["top_k"])

    libsim = cdll.LoadLibrary(os.path.join(settings.BASE_DIR, 'demo/c_lib/libsim.so'))
    libsim.find.argtypes = [c_char_p, c_int, ALL_ENTITY_TYPE, ALL_ENTITY_LEN_TYPE, c_int]
    libsim.find.restype = POINTER(Node)
    candidates = libsim.find(input_name.encode('utf-8'), TOT_ENTITY, ALL_ENTITY, ALL_ENTITY_LEN, top_k)

    mapped_entities = []

    for i in range(top_k):
        mapped_entities.append(candidates[i].str.decode('utf-8'))

    return JsonResponse({
        "mapped_entities": mapped_entities
    })
def find_types(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("<h1>Please request via POST</h1>")

    entities = json.loads(request.body.decode('utf-8'))["entities"]

    if len(entities) == 0:
        return HttpResponseBadRequest("<h1>Too few entity</h1>")

    r = QUERY_TYPES(input_entities=entities)
    thr = threading.Thread(target=r.run)
    thr.start()
    thr.join()

    if r.get_result() == None:
        return HttpResponseBadRequest("<h1>Bad SPARQL query</h1>")

    return JsonResponse({
        "types" : r.get_result()
    })


def find_facts(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("<h1>Please request via POST</h1>")

    entities = json.loads(request.body.decode('utf-8'))["entities"]

    if len(entities) == 0:
        return HttpResponseBadRequest("<h1>Too few entity</h1>")

    r_po = QUERY_FACTS(input_entities=entities, flag="po")
    thr_po = threading.Thread(target=r_po.run)
    thr_po.start()


    r_sp = QUERY_FACTS(input_entities=entities, flag="sp")
    thr_sp = threading.Thread(target=r_sp.run)
    thr_sp.start()


    thr_po.join()
    thr_sp.join()


    if r_po.get_result() == None or r_sp.get_result() == None:
        return HttpResponseBadRequest("<h1>Bad SPARQL query</h1>")


    return JsonResponse({
        "facts-po": r_po.get_result(),
        "facts-sp": r_sp.get_result()
    })


def find_attributes(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("<h1>Please request via POST</h1>")

    json_dict = json.loads(request.body.decode('utf-8'))
    entities = json_dict["entities"]

    row_number = int(json_dict["row_number"])
    v_number = int(json_dict["v_number"])

    r_types = []
    r_facts_po = []
    r_facts_sp = []

    thr_types = []
    thr_facts_po = []
    thr_facts_sp = []

    for i in range(v_number):
        column_entities = []
        for j in range(row_number):
            column_entities.append(entities[j][i])

        r_type = QUERY_TYPES(input_entities=column_entities)
        thr_type = threading.Thread(target=r_type.run)
        thr_type.start()

        r_fact_po = QUERY_FACTS(input_entities=column_entities, flag="po")
        thr_fact_po = threading.Thread(target=r_fact_po.run)
        thr_fact_po.start()

        r_fact_sp = QUERY_FACTS(input_entities=column_entities, flag="sp")
        thr_fact_sp = threading.Thread(target=r_fact_sp.run)
        thr_fact_sp.start()

        r_types.append(r_type)
        r_facts_po.append(r_fact_po)
        r_facts_sp.append(r_fact_sp)

        thr_types.append(thr_type)
        thr_facts_po.append(thr_fact_po)
        thr_facts_sp.append(thr_fact_sp)


    for i in range(v_number):
        thr_types[i].join()
        thr_facts_po[i].join()
        thr_facts_sp[i].join()


    types = {}
    facts = {}
    for i in range(v_number):
        if r_types[i].get_result() == None or r_facts_po[i].get_result() == None or r_facts_sp[i].get_result() == None:
            return HttpResponseBadRequest("<h1>Bad SPARQL query</h1>")

        types["v" + str(i)] = r_types[i].get_result()
        facts["v" + str(i)] = {
            "facts_po": r_facts_po[i].get_result(),
            "facts_sp": r_facts_sp[i].get_result()
        }


    return JsonResponse({
        "types": types,
        "facts": facts
    })


def find_one_row_direction(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("<h1>Please request via POST</h1>")

    # A list of entity
    json_dict = json.loads(request.body.decode('utf-8'))
    row_entities = json_dict["entities"]

    v_number = int(json_dict["v_number"])
    if v_number < 1:
        return HttpResponseBadRequest("<h1>The number of columns is invalid</h1>")

    r = QUERY_RELATION_DIRECTIONS(input_entities=row_entities)
    thr = threading.Thread(target=r.run)
    thr.start()
    thr.join()
    if r.get_result() == None:
        return HttpResponseBadRequest("<h1>Bad relation directions query</h1>")

    return HttpResponse("Done.")


def find_pattern(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("<h1>Please request via POST</h1>")

    # A list of lists of entity
    json_dict = json.loads(request.body.decode('utf-8'))
    entities = json_dict["entities"]

    row_number = int(json_dict["row_number"])
    v_number = int(json_dict["v_number"])
    if "exp" not in json_dict:
        exp = False
    else:
        exp = json_dict["exp"]

    if row_number < 1 or v_number < 1:
        return HttpResponseBadRequest("<h1>The number of rows or columns is invalid</h1>")

    # All_result_relations_directions querying for every row
    rs = []
    thrs = []

    for row_entities in entities:
        r = QUERY_RELATION_DIRECTIONS(input_entities=row_entities)
        thr = threading.Thread(target=r.run)
        thr.start()

        rs.append(r)
        thrs.append(thr)

    all_result_relation_directions = []
    for i in range(row_number):
        thrs[i].join()
        if rs[i].get_result() == None:
            return HttpResponseBadRequest("<h1>Bad relation directions query</h1>")

        all_result_relation_directions.append(rs[i].get_result())

    if exp:
        return HttpResponse("Done.")

    # Common relation directions finding
    common_relation_directions = []
    counter = 0
    for i in range(v_number):
        for j in range(i + 1, v_number):
            first_relation_directions = all_result_relation_directions[0][counter]
            checked_flag = True

            for r in range(1, row_number):
                if first_relation_directions != all_result_relation_directions[0][counter]:
                    checked_flag = False
                    break

            if checked_flag:
                common_relation_directions.append(first_relation_directions)
            else:
                common_relation_directions.append([])

            counter += 1

    # Common relation names finding by SPARQL query
    rs = []
    thrs = []

    counter = 0
    for i in range(v_number):
        for j in range(i + 1, v_number):
            r = QUERY_RELATION_NAMES(input_entities=entities, S=i, T=j, dirs=common_relation_directions[counter])
            thr = threading.Thread(target=r.run)
            thr.start()

            rs.append(r)
            thrs.append(thr)
            counter += 1

    common_relation_names = []
    counter = 0
    for i in range(v_number):
        for j in range(i + 1, v_number):
            thrs[counter].join()
            if rs[counter].get_result() == None:
                return HttpResponseBadRequest("<h1>Bad relation names query</h1>")

            common_relation_names.append(rs[counter].get_result())
            counter += 1

    # Construct common relations
    common_relations = {}
    counter = 0
    for i in range(v_number):
        for j in range(i + 1, v_number):

            if len(common_relation_names[counter]) == 0:
                common_relations["r_%d_%d" % (i, j)] = []

            elif len(common_relation_names[counter]) == 1:
                if common_relation_directions[counter][0] == 0:
                    common_relations["r_%d_%d" % (i, j)] = [
                        {
                            "s": "?v%d" % i,
                            "p": common_relation_names[counter][0],
                            "o": "?v%d" % j
                        }
                    ]
                else:
                    common_relations["r_%d_%d" % (i, j)] = [
                        {
                            "s": "?v%d" % j,
                            "p": common_relation_names[counter][0],
                            "o": "?v%d" % i
                        }
                    ]
            else:
                relations = []
                for k in range(len(common_relation_names[counter])):
                    if common_relation_directions[counter][k] == 0:
                        if k == 0:
                            relations.append({
                                "s": "?v%d" % i,
                                "p": common_relation_names[counter][k],
                                "o": "?t%d_%d" % (counter, k)
                            })
                        elif k == len(common_relation_directions[counter]) - 1:
                            relations.append({
                                "s": "?t%d_%d" % (counter, k - 1),
                                "p": common_relation_names[counter][k],
                                "o": "?v%d" % j
                            })
                        else:
                            relations.append({
                                "s": "?t%d_%d" % (counter, k - 1),
                                "p": common_relation_names[counter][k],
                                "o": "?t%d_%d" % (counter, k)
                            })
                    else:
                        if k == 0:
                            relations.append({
                                "s": "?t%d_%d" % (counter, k),
                                "p": common_relation_names[counter][k],
                                "o": "?v%d" % i,
                                
                            })
                        elif k == len(common_relation_directions[counter]) - 1:
                            relations.append({
                                "s": "?v%d" % j,
                                "p": common_relation_names[counter][k],
                                "o": "?t%d_%d" % (counter, k - 1)
                            })
                        else:
                            relations.append({
                                "s": "?t%d_%d" % (counter, k),
                                "p": common_relation_names[counter][k],
                                "o": "?t%d_%d" % (counter, k - 1)
                            })
                common_relations["r_%d_%d" % (i, j)] = relations

            counter += 1

    return JsonResponse({
        "pattern": common_relations
    })

def query_positive(request): #deprecated
    if request.method != 'POST':
        return HttpResponseBadRequest("<h1>Please request via POST</h1>")

    json_dict = json.loads(request.body.decode('utf-8'))
    v_number = json_dict["v_number"]

    sparql = ''
    sparql += 'BASE <%s>\r\n' % BASE
    sparql += 'PREFIX rdf: <%s>\r\n' % PREFIX_RDF
    sparql += 'SELECT DISTINCT'

    for i in range(v_number):
        sparql += ' ?v%d' % i

    sparql += '\r\n'
    sparql += 'WHERE {\r\n'

    # Add pattern
    for i in range(v_number):
        for j in range(i + 1, v_number):
            relations = json_dict["pattern"]["r_%d_%d" % (i, j)]
            for edge in relations:
                sparql += '    %s <%s> %s .\r\n' % (edge["s"], edge["p"], edge["o"])
    sparql += '\r\n'

    # Add types
    for i in range(v_number):
        for t in json_dict["types"]["v%d" % i]:
            sparql += '    ?v%d rdf:type <%s> .\r\n' % (i, t)

    # Add facts
    sparql += '\r\n'
    for i in range(v_number):
        for po in json_dict["facts"]["v%d" % i]["facts_po"]:
            sparql += '    ?v%d <%s> <%s> .\r\n' % (i, po["p"], po["o"])

        for sp in json_dict["facts"]["v%d" % i]["facts_sp"]:
            sparql += '    <%s> <%s> ?v%d .\r\n' % (sp["s"], sp["p"], i)


    # Add general striction
    sparql += 'FILTER ('
    for i in range(v_number):
        if i != 0:
            sparql += ' &&'
        sparql += ' isURI(?v%d)' % i

    sparql += ' )\r\n'
    sparql += '\r\n'

    sparql += '###\r\n'
    sparql += '}\r\n'

    # Add limit and offset
    sparql += 'LIMIT %d\r\n' % json_dict["limit"]
    sparql += 'OFFSET %d\r\n' % json_dict["offset"]

    results = query_final_sparql(sparql)
    if results == None:
        return HttpResponseBadRequest("<h1>Bad SPARQL query</h1>")

    return JsonResponse({
        "sparql": sparql,
        "results": results
    })

def find_strings(request): # deprecated
    if request.method != 'POST':
        return HttpResponseBadRequest("<h1>Please request via POST</h1>")

    json_dict = json.loads(request.body.decode('utf-8'))
    entities = json_dict["entities"]
    row_number = json_dict["row_number"]
    v_number = json_dict["v_number"]

    strings = {}
    for i in range(v_number):
        column_entities = []
        for j in range(row_number):
            column_entities.append(entities[j][i])

        strings["v%d" % i] = list(set(column_entities))

    return JsonResponse({
        "strings": strings
    })

def query_negative(request): # deprecated
    if request.method != 'POST':
        return HttpResponseBadRequest("<h1>Please request via POST</h1>")

    json_dict = json.loads(request.body.decode('utf-8'))
    v_number = json_dict["v_number"]

    sparql = json_dict["old_sparql"].split('###')[0]

    '''
    # Add negative common strings
    for i in range(v_number):
        first_flag = True
        for s in json_dict["strings"]["v%d" % i]:
            if first_flag == True:
                sparql += 'FILTER ('
                first_flag = False
            else:
                sparql += '&&'
            sparql += ' ?v%d != <%s> ' % (i, s)

        if first_flag == False:
            sparql += ')\r\n'
    '''

    # Add negative common types

    for i in range(v_number):
        if len(json_dict["types"]["v%d" % i]) > 0:
            sparql += 'FILTER NOT EXISTS {\r\n'
            break

    for i in range(v_number):
        if len(json_dict["types"]["v%d" % i]) > 0:
            sparql += '    ?v%d rdf:type ?t%d .\r\n' % (i, i)

    for i in range(v_number):
        first_flag = True
        for t in json_dict["types"]["v%d" % i]:
            if first_flag == True:
                sparql += '    FILTER ( regex(?t%d, "(' % i
                first_flag = False
            else:
                sparql += '|'
            sparql += t

        if first_flag == False:
            sparql += ')$", "-i") )\r\n'

    for i in range(v_number):
        if len(json_dict["types"]["v%d" % i]) > 0:
            sparql += '}\r\n'
            break

    # Add negative common facts
    for i in range(v_number):
        if len(json_dict["facts"]["v%d" % i]["facts_po"]) or len(json_dict["facts"]["v%d" % i]["facts_sp"]) > 0:
            sparql += 'FILTER NOT EXISTS {\r\n'
            break

    for i in range(v_number):
        for fact_po in json_dict["facts"]["v%d" % i]["facts_po"]:
            sparql += '    ?v%d <%s> <%s> .\r\n' % (i, fact_po["p"], fact_po["o"])

        for fact_sp in json_dict["facts"]["v%d" % i]["facts_sp"]:
            sparql += '    <%s> <%s> ?v%d .\r\n' % (fact_sp["s"], fact_sp["p"], i)

    for i in range(v_number):
        if len(json_dict["facts"]["v%d" % i]["facts_po"]) or len(json_dict["facts"]["v%d" % i]["facts_sp"]) > 0:
            sparql += '}\r\n'
            break

    sparql += '###\r\n'
    sparql += '}\r\n'

    # Add limit and offset
    sparql += 'LIMIT %d\r\n' % json_dict["limit"]
    sparql += 'OFFSET %d\r\n' % json_dict["offset"]

    results = query_final_sparql(sparql)
    if results == None:
        return HttpResponseBadRequest("<h1>Bad SPARQL query</h1>")
    
    return JsonResponse({
        "sparql": sparql,
        "results": results
    })

def query(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("<h1>Please request via POST</h1>")

    json_dict = json.loads(request.body.decode('utf-8'))
    v_number = json_dict["v_number"]

    sparql = ''
    sparql += 'BASE <%s>\r\n' % BASE
    sparql += 'PREFIX rdf: <%s>\r\n' % PREFIX_RDF
    sparql += 'SELECT DISTINCT'

    for i in range(v_number):
        sparql += ' ?v%d' % i

    sparql += '\r\n'
    sparql += 'WHERE {\r\n'

    # Add pattern
    for i in range(v_number):
        for j in range(i + 1, v_number):
            relations = json_dict["pattern"]["r_%d_%d" % (i, j)]
            for edge in relations:
                sparql += '    %s <%s> %s .\r\n' % (edge["s"], edge["p"], edge["o"])
    sparql += '\r\n'

    # Add positive types
    for i in range(v_number):
        for t in json_dict["pos_types"]["v%d" % i]:
            sparql += '    ?v%d rdf:type <%s> .\r\n' % (i, t)

    # Add positive facts
    sparql += '\r\n'
    for i in range(v_number):
        for po in json_dict["pos_facts"]["v%d" % i]["facts_po"]:
            sparql += '    ?v%d <%s> <%s> .\r\n' % (i, po["p"], po["o"])

        for sp in json_dict["pos_facts"]["v%d" % i]["facts_sp"]:
            sparql += '    <%s> <%s> ?v%d .\r\n' % (sp["s"], sp["p"], i)


    # Add general restriction
    sparql += 'FILTER ('
    for i in range(v_number):
        if i != 0:
            sparql += ' &&'
        sparql += ' isURI(?v%d)' % i

    sparql += ' )\r\n'

    # Add negative types

    for i in range(v_number):
        if len(json_dict["neg_types"]["v%d" % i]) > 0:
            sparql += 'FILTER NOT EXISTS {\r\n'
            break

    for i in range(v_number):
        if len(json_dict["neg_types"]["v%d" % i]) > 0:
            sparql += '    ?v%d rdf:type ?t%d .\r\n' % (i, i)

    for i in range(v_number):
        first_flag = True
        for t in json_dict["neg_types"]["v%d" % i]:
            if first_flag == True:
                sparql += '    FILTER ( regex(?t%d, "(' % i
                first_flag = False
            else:
                sparql += '|'
            sparql += t

        if first_flag == False:
            sparql += ')$", "-i") )\r\n'

    for i in range(v_number):
        if len(json_dict["neg_types"]["v%d" % i]) > 0:
            sparql += '}\r\n'
            break

    # Add negative facts
    for i in range(v_number):
        if len(json_dict["neg_facts"]["v%d" % i]["facts_po"]) or len(json_dict["neg_facts"]["v%d" % i]["facts_sp"]) > 0:
            sparql += 'FILTER NOT EXISTS {\r\n'
            break

    for i in range(v_number):
        for fact_po in json_dict["neg_facts"]["v%d" % i]["facts_po"]:
            sparql += '    ?v%d <%s> <%s> .\r\n' % (i, fact_po["p"], fact_po["o"])

        for fact_sp in json_dict["neg_facts"]["v%d" % i]["facts_sp"]:
            sparql += '    <%s> <%s> ?v%d .\r\n' % (fact_sp["s"], fact_sp["p"], i)

    for i in range(v_number):
        if len(json_dict["neg_facts"]["v%d" % i]["facts_po"]) or len(json_dict["neg_facts"]["v%d" % i]["facts_sp"]) > 0:
            sparql += '}\r\n'
            break


    sparql += '}\r\n'

    # Add limit and offset
    sparql += 'LIMIT %d\r\n' % json_dict["limit"]
    sparql += 'OFFSET %d\r\n' % json_dict["offset"]

    results = query_final_sparql(sparql)
    if results == None:
        return HttpResponseBadRequest("<h1>Bad SPARQL query</h1>")

    return JsonResponse({
        "sparql": sparql,
        "results": results
    })


def get_more_results(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("<h1>Please request via POST</h1>")

    json_dict = json.loads(request.body.decode('utf-8'))
    sparql = json_dict["sparql"].split('LIMIT')[0]

    # Add limit and offset
    sparql += 'LIMIT %d\r\n' % json_dict["limit"]
    sparql += 'OFFSET %d\r\n' % json_dict["offset"]
    
    results = query_final_sparql(sparql)
    if results == None:
        return HttpResponseBadRequest("<h1>Bad SPARQL query</h1>")
    
    return JsonResponse({
        "sparql": sparql,
        "results": results
    })
