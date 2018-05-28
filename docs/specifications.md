## main UI
* All web UI will be displayed at [`the index page`](http://162.105.146.135:8080/demo/) based on `Django` framework.
* We plan to adopt `AJAX` to show results of every step.
* The final UI is similar to the picture written by `HTML`.
* Next, we will introduce the events and actions of every step.



## Entity Recommendation
1. The user will see a table with default number of columns (3) and rows(2) in the middle of the index page.
2. The UI provides users with 4 buttons for adding (deleting) a row (column).
3. When the user is typing a string, the system would offer 'real-time' entity recommendation by a pull-down list.
4. Blank is not allowed and the user must select one of the recommendation from the pull-down list.
5. Finally, the user can `submit` the tabular examples to the system.
* entity-recommendation API
    * request: `http://162.105.146.135:8080/demo/entity-recommendation/`
    * method: `POST`
    * data: `JSON e.g. {"input_name": "xxx", "top_k": 10} (Default k is 10)` 
    * response: `JSON e.g. {"mapped_entities": ["entity_1", "entity_2", ... ,"entity_10"]`


## Common Attributes and relations
### Common Types and Facts (Only for test)
* The system will display common types and facts of entities in one column.
* common types API
    * request: `http://162.105.146.135:8080/demo/types/`
    * method: `POST`
    * data: `JSON e.g. {"entities" : ["entity_1", "entity_2", ...]}`
    * response: `JSON e.g. {"types": ["types_1", "types_2", ...]`

* common facts API
    * URL: `http://162.105.146.135:8080/demo/facts/`
    * method: `POST`
    * data: `JSON e.g. {"entities" : ["entity_1", "entity_2", ...]}`
    * response: `JSON`
```
e.g.

response:
{
    "facts_po": [{"p": "xxx", "o": "xxx"}, {"p": "xxx", "o": "xxx"}, ...],
    "facts_sp": [{"s": "xxx", "p": "xxx"}, {"s": "xxx", "p": "xxx"}, ...]
}
```

### Common Attributes
* common attributes API
    * request: `http://162.105.146.135:8080/demo/attributes/`
    * method: `POST`
    * data: `JSON`
    * response: `JSON`
```
e.g.

data:
1. {
    "row_number": 2,
    "v_number": 3,
    "entities": [
        ["Xi_Jinping", "China", "Peng_Liyuan"],
        ["Barack_Obama", "United_States", "Michelle_Obama"]
    ]
}

2. {
    "row_number": 2,
    "v_number": 3,
    "entities": [
        ["Dick_Van_Dyke", "Barry_Van_Dyke", "Murder_101_(film_series)"],
        ["Jerry_Stiller", "Ben_Stiller", "The_Independent_(2000_film)"]
    ]
}

response:
{
    "types": {
        "v0": [],
        "v1": [],
        "v2": [],
        ...
    },
    "facts": {
        "v0": {
            "facts_po": [{"p": "xxx"}, {"o": "xxx"}, ...],
            "facts_sp": [{"s": "xxx"}, {"p": "xxx"}, ...]
        },
        "v1": {
            "facts_po": [],
            "facts_sp": []
        },
        "v2": {
            "facts_po": [],
            "facts_sp": []
        },
        ...
    }
}
```

### Common relations
* The system will find relations of entities in one row.
* common relations API
    * URL: `http://162.105.146.135:8080/demo/pattern/`
    * method: `POST`
    * data: `JSON`
    * response: `JSON`
```
e.g.

data:
1. {
    "row_number": 2,
    "v_number": 3,
    "entities": [
        ["Xi_Jinping", "China", "Peng_Liyuan"],
        ["Barack_Obama", "United_States", "Michelle_Obama"]
    ]
}

2. {
    "row_number": 2,
    "v_number": 3,
    "entities": [
        ["Dick_Van_Dyke", "Barry_Van_Dyke", "Murder_101_(film_series)"],
        ["Jerry_Stiller", "Ben_Stiller", "The_Independent_(2000_film)"]
    ]
}

response:
1. {
    "pattern": {
        "r_0_1": [{"p": "isLeaderOf", "o": "?v1", "s": "?v0"}],
        "r_0_2": [{"p": "isMarriedTo", "o": "?v2", "s": "?v0"}],
        "r_1_2": [{"s": "?v2", "o": "?t_1_2_0", "p": "graduatedFrom"}, {"p": "isLocatedIn", "o": "?v1", "s": "?t_1_2_0"}]}
}

2. {
    "pattern": {
        "r_0_1": [{"p": "hasChild", "o": "?v1", "s": "?v0"}],
        "r_0_2": [{"p": "actedIn", "o": "?v2", "s": "?v0"}],
        "r_0_3": [{"p": "actedIn", "o": "?v2", "s": "?v1"}]
    }
}
similar to one relation
tot: n * (n - 1) / 2 pairs.
```

### Query by positive examples (deprecated)
* URL: `http://162.105.146.135:8080/demo/query-positive/`
* method: `POST`
* data: `JSON`
* response: `JSON`
```
e.g.

data:
{
    "v_number": 3,
    "types": {
        "v0": [],
        "v1": [],
        "v2": []
    },
    "facts": {
        "v0": {
            "facts_po": [{"p": "xxx"}, {"o": "xxx"}, ...],
            "facts_sp": [{"s": "xxx"}, {"p": "xxx"}, ...]
        },
        "v1": {
            "facts_po": [],
            "facts_sp": []
        },
        "v2": {
            "facts_po": [],
            "facts_sp": []
        }
    },
    "pattern": {
        "r_0_1": [{"p": "hasChild", "o": "?v1", "s": "?v0"}],
        "r_0_2": [{"p": "actedIn", "o": "?v2", "s": "?v0"}],
        "r_1_2": [{"p": "actedIn", "o": "?v2", "s": "?v1"}]
    },
    "limit": 50
    "offset": 0
}
limit: the max number of results displayed in one page
offset: from where the results displayed

response:
{
    "sparql": "xxx",
    "results": [
        {"v0": "xxx", "v1": "xxx", "v2": "xxx"},
        {"v0": "xxx", "v1": "xxx", "v2": "xxx"},
        ...
    ]
}
```

### query by both positive and negative examples
* URL: `http://162.105.146.135:8080/demo/query/`
* method: `POST`
* data: `JSON`
* response: `JSON`
```
e.g.

data:
{
    "v_number": 3,
    "pos_types": {
        "v0": [],
        "v1": [],
        "v2": []
    },
    "pos_facts": {
        "v0": {
            "facts_po": [{"p": "xxx"}, {"o": "xxx"}, ...],
            "facts_sp": [{"s": "xxx"}, {"p": "xxx"}, ...]
        },
        "v1": {
            "facts_po": [],
            "facts_sp": []
        },
        "v2": {
            "facts_po": [],
            "facts_sp": []
        }
    },
    "neg_types": {
        "v0": [],
        "v1": [],
        "v2": []
    },
    "neg_facts": {
        "v0": {
            "facts_po": [{"p": "xxx"}, {"o": "xxx"}, ...],
            "facts_sp": [{"s": "xxx"}, {"p": "xxx"}, ...]
        },
        "v1": {
            "facts_po": [],
            "facts_sp": []
        },
        "v2": {
            "facts_po": [],
            "facts_sp": []
        }
    },
    "pattern": {
        "r_0_1": [{"p": "hasChild", "o": "?v1", "s": "?v0"}],
        "r_0_2": [{"p": "actedIn", "o": "?v2", "s": "?v0"}],
        "r_1_2": [{"p": "actedIn", "o": "?v2", "s": "?v1"}]
    },
    "limit": 50
    "offset": 0
}

# limit: the max number of results displayed in one page
# offset: from where the results displayed

response:
{
    "sparql": "xxx",
    "results": [
        {"v0": "xxx", "v1": "xxx", "v2": "xxx"},
        {"v0": "xxx", "v1": "xxx", "v2": "xxx"},
        ...
    ]
}
```


## Answer refinement
### Common Strings (deprecated)
* Display all strings of every column from negative results
* strings API:
    * URL: `http://162.105.146.135:8080/demo/strings/`
    * method: `POST`
    * data: `JSON`
    * response: `JSON`
```
e.g.

data:
{
    "row_number": 3,
    "v_number": 3,
    "entities": [
        ["e0_0", "e1_1", "e2_2"],
        ["e0_0", "e1_2", "e2_3"],
        ["e0_1", "e1_1", "e2_4"],
        ...
    ]
}

response:
{
    "strings": {
        "v0": ["e0_0", "e0_1"],
        "v1": ["e1_1", "e1_2"],
        "v2": ["e2_2", "e2_3", "e2_4"],
        ...
    }
}
```

### Interaction (similar to before) (deprecated)
* Users can choose results that they are not interested in.
* Query these negative results via `common strings` and `common attributes` api.
* sending negative common attributes API:
    * URL: `http://162.105.146.135:8080/demo/query-negative/`
    * method: `POST`
    * data: `JSON`      
    * response: `JSON`
```
e.g.

data:
{
    "v_number": 3,
    "types": {
        "v0": [],
        "v1": [],
        "v2": []
    },
    "facts": {
        "v0": {
            "facts_po": [{"p": "xxx"}, {"o": "xxx"}, ...],
            "facts_sp": [{"s": "xxx"}, {"p": "xxx"}, ...]
        },
        "v1": {
            "facts_po": [],
            "facts_sp": []
        },
        "v2": {
            "facts_po": [],
            "facts_sp": []
        }
    },
    "old_sparql": "xxx",
    "limit": 50
    "offset": 0
}

response:
{
    "sparql": "xxx",
    "results": [
        {"v0": "xxx", "v1": "xxx", "v2": "xxx"},
        {"v0": "xxx", "v1": "xxx", "v2": "xxx"},
        ...
    ]
}
```

## Get More Results
* The user probably wants to get more results from one SPARQL query.
* API:
    * URL: `http://162.105.146.135:8080/demo/get-more-results/`
    * method: `POST`
    * data: `JSON e.g. {"sparql": "xxx", "limit": xx, "offset": xx}`
    * response: `JSON`
```
e.g.

response:
{
    "sparql": "xxx",
    "results": [
        {"v0": "xxx", "v1": "xxx", "v2": "xxx"},
        {"v0": "xxx", "v1": "xxx", "v2": "xxx"},
        ...
    ]
}
```
