# CUTE
Querying Knowledge Graphs by Tabular Examples

## Deploy Instructions

1. Build and activate a `python3 virtualenv` named `venv` in the same directory with `setup.sh`.
2. `pip install` some python packages indicated by `requirements.txt` to `venv`.
3. Run `setup.sh [port] [data_path_dir](optional if existing data)`. `e.g. ./setup.sh 0:8080 (/home/wangzc/yago_data_for_CUTE/data/)`. 
4. Visit `http://localhost:<port_number>/demo/`.


# Internal SPARQL Service
* url: http://162.105.146.140:8001/sparql
* dataset: yagoFacts (cleaned); yagoTransitiveTypes

# Virtuoso Directory
/home/wangzichen/virtuoso/

## Start Command
/home/wangzichen/virtuoso/start_daemon.sh

## Data Load
refer: http://vos.openlinksw.com/owiki/wiki/VOS/VirtBulkRDFLoader
Note: isql directory：/home/yxshao/virtuoso/sempre/virtuoso-opensource/install/bin
isql start command：isql <port> this port is different from the port of start command. We need add 1 before. 8001 is the port for web.
For example: isql 18001 
