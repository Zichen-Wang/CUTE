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

# Virtuoso目录
/home/wangzichen/virtuoso/

## 启动脚本位置：
/home/wangzichen/virtuoso/

## Data load
refer: http://vos.openlinksw.com/owiki/wiki/VOS/VirtBulkRDFLoader
注意：isql 所在目录位置：/home/yxshao/virtuoso/sempre/virtuoso-opensource/install/bin
isql启动命令为：isql <port> 这里的port与启动命令的port不一致，需要前面加 1。前面的8001是web页面的端口。
比如 isql 18001 
