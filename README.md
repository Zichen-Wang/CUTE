# CUTE
Querying Knowledge Graphs by Tabular Examples

## Deploy Instructions

1. Build and activate a `python3 virtualenv` named `venv` in the same directory with `setup.sh`.
2. `pip install` some python packages indicated by `requirements.txt` to `venv`.
3. Run `setup.sh [port] [data_path_dir]`. `e.g. ./setup.sh 0:8080 /home/wangzc/yago_data_for_CUTE/data/`.
4. Visit `http://localhost:<port_number>/demo/`.
