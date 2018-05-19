from django.conf import settings
import os

import requests


from ctypes import cdll, c_int, c_double, c_char_p, Structure, POINTER

TYPES_RANKING = {}

for t in open(settings.TYPE_FILE_PATH, 'r', encoding='utf-8'):
    t = t.strip().split(' ')
    TYPES_RANKING[t[0]] = float(t[1])


ENTITY_2_ID = {}
ENTITY = [] # must be bytes for 'ctypes'
ENTITY_LEN = []
cnt = 0
for entity in open(settings.ENTITY_FILE_PATH, 'r', encoding='utf-8'):
    ENTITY_2_ID[entity.strip()] = cnt
    ENTITY.append(entity.strip().encode('utf-8')) # must be bytes for 'ctypes'
    ENTITY_LEN.append(len(entity.strip()))
    cnt += 1

TOT_ENTITY = cnt
ALL_ENTITY_TYPE = c_char_p * TOT_ENTITY
ALL_ENTITY = ALL_ENTITY_TYPE(*ENTITY)
ALL_ENTITY_LEN_TYPE = c_int * TOT_ENTITY
ALL_ENTITY_LEN = ALL_ENTITY_LEN_TYPE(*ENTITY_LEN)



RELATION_2_ID = {}
RELATION = []
cnt = 0
for relation in open(settings.RELATION_FILE_PATH, 'r', encoding='utf-8'):
    RELATION_2_ID[relation.strip()] = cnt
    RELATION.append(relation.strip())
    cnt += 1

class GraphEdge(Structure):
    _fields_ = [("to", c_int), ("direction", c_int)]

class GraphEdgeSet(Structure):
    _fields_ = [("edges", POINTER(GraphEdge)), ("total", c_int)]


ROW_GRAPH = [[] for i in range(TOT_ENTITY)]

WEIGHT = {}

for edge in open(settings.GRAPH_FILE_PATH, 'r'):
    edge = edge.strip().split(" ")
    WEIGHT[' '.join(edge[: 3])] = float(edge[3])
    ROW_GRAPH[int(edge[0])].append(GraphEdge(to=int(edge[1]), direction=0))
    ROW_GRAPH[int(edge[1])].append(GraphEdge(to=int(edge[0]), direction=1))


GRAPH_TYPE = GraphEdgeSet * TOT_ENTITY

ROW_GRAPH_TMP = []
for i in range(TOT_ENTITY):
    ROW_GRAPH_TMP.append(GraphEdgeSet(edges=(GraphEdge * len(ROW_GRAPH[i]))(*ROW_GRAPH[i]), total=len(ROW_GRAPH[i])))

GRAPH = GRAPH_TYPE(*ROW_GRAPH_TMP)

BASE = "http://yago-knowledge.org/resource/"
PREFIX_RDF = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"

SPARQL_QUERY_URL = "http://162.105.146.140:8001/sparql"

def cmp_type(x):
    if x in TYPES_RANKING:
        return TYPES_RANKING[x]

    return 0.970

def query_final_sparql(sparql):
    # Query
    print(sparql)
    payload = {
        'default-graph-uri': '',
        'query': sparql,
        'format': 'application/sparql-results+json',
        'timeout': 2000,
        'debug': 'on'
    }

    try:
        r = requests.get(SPARQL_QUERY_URL, params=payload)
        result_dict = r.json()

    except Exception as ins:
        print(ins)
        return None


    variable_name = result_dict['head']['vars']
    results = []

    for res in result_dict['results']['bindings']:
        r = {}
        for i in range(len(variable_name)):
            v_name = variable_name[i]
            v_value = res[variable_name[i]]['value']
            r[v_name] = v_value[v_value.rfind('/resource/') + 10 : ]

        results.append(r)


    return results

class QUERY_TYPES:
    def __init__(self, input_entities):
        self.result_types = None
        self.entities = input_entities

    def make_sparql(self):
        sparql = ''
        sparql += 'BASE <%s>\r\n' % BASE
        sparql += 'PREFIX rdf: <%s>\r\n' % PREFIX_RDF
        sparql += 'SELECT DISTINCT ?t\r\n'
        sparql += 'WHERE {\r\n'
        for entity in self.entities:
            sparql += '    <%s>  rdf:type ?t .\r\n' % entity

        sparql += 'FILTER ( isURI(?t) )\r\n'
        sparql += '}\r\n'

        print(sparql)
        return sparql
    
    def run(self, *args, **kwargs):

        sparql = self.make_sparql()

        payload = {
            'default-graph-uri': '',
            'query': sparql,
            'format': 'application/sparql-results+json',
            'timeout': 2000,
            'debug': 'on'
        }

        try:
            r = requests.get(SPARQL_QUERY_URL, params=payload)
            result_dict = r.json()

        except Exception as ins:
            print(ins)
            return

        variable_name = result_dict['head']['vars'][0]

        self.result_types = []
        for res in result_dict['results']['bindings']:
            if res[variable_name]['value'] != "http://www.w3.org/2002/07/owl#Thing":
                t = res[variable_name]['value']
                self.result_types.append(t[t.rfind('/resource/') + 10 : ])

        self.result_types.sort(key=cmp_type, reverse=True)

    def get_result(self):
        return self.result_types



class QUERY_FACTS:
    def __init__(self, input_entities, flag):
        self.result_facts = None
        self.entities = input_entities
        self.flag = flag

    def make_sparql(self):
        sparql = ''
        sparql += 'BASE <%s>\r\n' % BASE

        if self.flag == 'po':
            sparql += 'SELECT DISTINCT ?p ?o\r\n'
            sparql += 'WHERE {\r\n'
            for entity in self.entities:
                sparql += '    <%s> ?p ?o .\r\n' % entity

            sparql += 'FILTER (\r\n'
            sparql += '    isURI(?o) &&\r\n'

        elif self.flag == 'sp':
            sparql += 'SELECT DISTINCT ?s ?p\r\n'
            sparql += 'WHERE {\r\n'
            for entity in self.entities:
                sparql += '    ?s ?p <%s> .\r\n' % entity

            sparql += 'FILTER (\r\n'
            sparql += '    isURI(?s) &&\r\n'

        else:
            return None

        sparql += '    regex(?p, "('
        for i in range(len(RELATION)):
            if i != 0:
                sparql += '|'
            sparql += RELATION[i]
        sparql += ')$", "i")\r\n'

        sparql += ')\r\n'
        sparql += '}\r\n'
        sparql += 'LIMIT 50\r\n'
        print(sparql)
        return sparql

    
    def run(self, *args, **kwargs):

        sparql = self.make_sparql()

        payload = {
            'default-graph-uri': '',
            'query': sparql,
            'format': 'application/sparql-results+json',
            'timeout': 2000,
            'debug': 'on'
        }

        try:
            r = requests.get(SPARQL_QUERY_URL, params=payload)
            result_dict = r.json()

        except Exception as ins:
            print(ins)
            return

        variable_name = result_dict['head']['vars']
        result_facts = []

        if self.flag == 'po':
            for res in result_dict['results']['bindings']:
                p = res[variable_name[0]]['value']
                o = res[variable_name[1]]['value']
                p = p[p.rfind('/resource/') + 10 : ]
                o = o[o.rfind('/resource/') + 10 : ]
                weight = 0.0;
                for s in self.entities:
                    if s not in ENTITY_2_ID or o not in ENTITY_2_ID:
                        pass
                    else:
                        ws = ' '.join([str(ENTITY_2_ID[s]), str(ENTITY_2_ID[o]), str(RELATION_2_ID[p])]);
                        if ws not in WEIGHT:
                            print("%s not found!" % ws)
                        else:
                            weight += WEIGHT[ws]

                result_facts.append({
                        "p": p,
                        "o": o,
                        "weight": weight
                })
            result_facts.sort(key=lambda facts: facts["weight"], reverse=True)
            self.result_facts = [{"p": res["p"], "o": res["o"]} for res in result_facts]


        elif self.flag == 'sp':
            for res in result_dict['results']['bindings']:
                s = res[variable_name[0]]['value']
                p = res[variable_name[1]]['value']
                s = s[s.rfind('/resource/') + 10 : ]
                p = p[p.rfind('/resource/') + 10 : ]
                weight = 0.0;
                for o in self.entities:
                    if s not in ENTITY_2_ID or o not in ENTITY_2_ID:
                        pass
                    else:
                        ws = ' '.join([str(ENTITY_2_ID[s]), str(ENTITY_2_ID[o]), str(RELATION_2_ID[p])]);
                        if ws not in WEIGHT:
                            print("%s not found!" % ws)
                        else:
                            weight += WEIGHT[ws]

                result_facts.append({
                        "s": s,
                        "p": p,
                        "weight": weight
                })
            result_facts.sort(key=lambda facts: facts["weight"], reverse=True)
            self.result_facts = [{"s": res["s"], "p": res["p"]} for res in result_facts]

        else:
            self.result_facts = None
    
    def get_result(self):
        return self.result_facts


class QUERY_RELATION_DIRECTIONS:
    def __init__(self, input_entities):
        self.result_relation_directions = None
        self.entities = input_entities
        self.tot_entity = len(self.entities)

    def run(self, *args, **kwargs):

        class Path(Structure):
            _fields_ = [("directions", POINTER(c_int)), ("length", c_int)]


        ENTITY_TYPE = c_int * len(self.entities)
        try:
            entities = [ENTITY_2_ID[e] for e in self.entities]
        except KeyError as ins:
            print(ins)
            return


        librel = cdll.LoadLibrary(os.path.join(settings.BASE_DIR, 'demo/c_lib/libpath.so'))
        librel.find.argtypes = [ENTITY_TYPE, c_int, GRAPH_TYPE]
        librel.find.restype = POINTER(Path)
        relations = librel.find(ENTITY_TYPE(*entities), self.tot_entity, GRAPH)
        
        tot_pairs = int(self.tot_entity * (self.tot_entity - 1) / 2)
        
        self.result_relation_directions = [
                [ relations[i].directions[j] for j in range(relations[i].length) ] for i in range(tot_pairs)
            ]


    def get_result(self):
        return self.result_relation_directions
 

class QUERY_RELATION_NAMES:
    def __init__(self, input_entities, S, T, dirs):
        self.result_relation_names = None
        self.entities = input_entities
        self.S = S
        self.T = T
        self.dirs = dirs

    def make_sparql(self):
        entities = self.entities
        S = self.S
        T = self.T

        row_number = len(entities)
        if row_number == 0:
            return None
        v_number = len(entities[0])

        sparql = ''
        sparql += 'BASE <%s>\r\n' % BASE
        sparql += 'SELECT DISTINCT'

        for i in range(len(self.dirs)):
            sparql += ' ?p%d' % i

        for r in range(row_number):
            for k in range(len(self.dirs) - 1):
                sparql += ' ?t%d_%d' % (r, k)

        sparql += '\r\nWHERE {\r\n'

        
        if len(self.dirs) == 1:
            for r in range(row_number):
                if self.dirs[0] == 0:
                    sparql += '    <%s> ?p0 <%s> .\r\n' % (entities[r][S], entities[r][T])
                else:
                    sparql += '    <%s> ?p0 <%s> .\r\n' % (entities[r][T], entities[r][S])
                sparql += '\r\n'

        else:
            for r in range(row_number):
                for k in range(len(self.dirs)):
                    if self.dirs[k] == 0:
                        if k == 0:
                            sparql += '    <%s> ?p%d ?t%d_%d .\r\n' % (entities[r][S], k, r, k)
                        elif k == len(self.dirs) - 1:
                            sparql += '    ?t%d_%d ?p%d <%s> .\r\n' % (r, k - 1, k, entities[r][T])
                        else:
                            sparql += '    ?t%d_%d ?p%d ?t%d_%d .\r\n' % (r, k - 1, k, r, k)
                    else:
                        if k == 0:
                            sparql += '    ?t%d_%d ?p%d <%s> .\r\n' % (r, k, k, entities[r][S])
                        elif k == len(self.dirs) - 1:
                            sparql += '    <%s> ?p%d ?t%d_%d .\r\n' % (entities[r][T], k, r, k - 1)
                        else:
                            sparql += '    ?t%d_%d ?p%d ?t%d_%d .\r\n' % (r, k, k, r, k - 1)
                sparql += '\r\n'

            for r in range(row_number):
                sparql += 'FILTER ('
                for k in range(len(self.dirs) - 1):
                    if k != 0:
                        sparql += '&&'
                    sparql += ' isURI(?t%d_%d) ' % (r, k)
                sparql += ')\r\n'

                for k in range(len(self.dirs) - 1):
                    sparql += 'FILTER ('
                    for i in range(v_number):
                        if i != 0:
                            sparql += '&&'
                        sparql += ' ?t%d_%d != <%s> ' % (r, k, entities[r][i])
                    sparql += ')\r\n'


        sparql += 'FILTER ('
        for i in range(len(self.dirs)):
            if i != 0:
                sparql += "&&"

            sparql += ' regex(?p%d, "(' % i
            for j in range(len(RELATION)):
                if j != 0:
                    sparql += '|'
                sparql += RELATION[j]
            sparql += ')$", "i") '

        sparql += ')\r\n'
        sparql += '}\r\n'
        sparql += 'LIMIT 50\r\n'

        print(sparql)
        return sparql


    def run(self, *args, **kwargs):
        if len(self.dirs) == 0:
            self.result_relation_names = []
            return

        sparql = self.make_sparql()
        if sparql == None:
            return

        payload = {
            'default-graph-uri': '',
            'query': sparql,
            'format': 'application/sparql-results+json',
            'timeout': 2000,
            'debug': 'on'
        }
        

        try:
            r = requests.get(SPARQL_QUERY_URL, params=payload)
            result_dict = r.json()

        except Exception as ins:
            print(ins)
            return

        all_result_relation_names_id = []
        entities = self.entities
        row_number = len(entities)
        v_number = len(entities[0])
        S = self.S
        T = self.T

        variable_name = result_dict['head']['vars']
        for res in result_dict['results']['bindings']:
            result_relation_names_id = []
            for k in variable_name:
                if k[0] == 'p':
                    name = res[k]["value"]
                    result_relation_names_id.append(RELATION_2_ID[name[name.rfind('/resource/') + 10 : ]])

            # calc weight
            result_relation_names_id_weight = 0.0
            for r in range(row_number):
                # First, find all entities in that path
                result_entity_names_id = [ENTITY_2_ID[entities[r][S]]]
                for k in variable_name:
                    if k[0] == 't' and k[1] == str(r):
                        name = res[k]["value"]
                        result_entity_names_id.append(ENTITY_2_ID[name[name.rfind('/resource/') + 10 : ]])

                result_entity_names_id.append(ENTITY_2_ID[entities[r][T]])

                # Second, calc every triple of that path for all rows
                for c in range(len(result_relation_names_id)):
                    if self.dirs[c] == 0:
                        triple = ' '.join([str(result_entity_names_id[c]), str(result_entity_names_id[c + 1]), str(result_relation_names_id[c])])
                    else:
                        triple = ' '.join([str(result_entity_names_id[c + 1]), str(result_entity_names_id[c]), str(result_relation_names_id[c])])

                    triple_weight = 0.0
                    try:
                        triple_weight = WEIGHT[triple]
                    except KeyError as ins:
                        print(ins)
                    
                    result_relation_names_id_weight += triple_weight

            all_result_relation_names_id.append({"names": result_relation_names_id, "weight": result_relation_names_id_weight})

        if len(all_result_relation_names_id) == 0:
            self.result_relation_names = []
            return

        # ranking relation names
        all_result_relation_names_id.sort(key=lambda relation_names: relation_names["weight"], reverse=True)
        # return top 1
        self.result_relation_names = []
        print(all_result_relation_names_id[0]["weight"])
        for relation_id in all_result_relation_names_id[0]["names"]:
            self.result_relation_names.append(RELATION[relation_id])


    def get_result(self):
        return self.result_relation_names




