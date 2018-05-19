import os
import sys
import time
import requests
import json

def main():
    entities = [
        [["China"], ["United_States"], ["Canada"]],
        [["China", "Xi_Jinping"], ["United_States", "Barack_Obama"], ["Canada", "Justin_Trudeau"]],
        [
            ["Dick_Van_Dyke", "Barry_Van_Dyke", "Murder_101_(film_series)"],
            ["Jerry_Stiller", "Ben_Stiller", "The_Independent_(2000_film)"],
            ["Martin_Sheen", "Charlie_Sheen", "No_Code_of_Conduct"]
        ],
        [
            ["United_States", "Joe_Biden", "Jill_Biden", "Hunter_Biden"],
            ["United_States", "Joe_Biden", "Jill_Biden", "Beau_Biden"],
            ["China", "Xi_Jinping", "Peng_Liyuan", "Xi_Mingze"]
        ]
    ]
    for i in range(4, 10):
        tmp = []
        tmp.append(["China" for j in range(i + 1)])
        tmp.append(["United_States" for j in range(i + 1)])
        tmp.append(["Canada" for j in range(i + 1)])
        entities.append(tmp)

    
    times_multi = []
    for i in range(10):
        json_dict = {
            "entities": entities[i],
            "row_number": 3,
            "v_number": i + 1
        }
        print(json.dumps(json_dict))
        start = time.time()
        for t in range(10):
            r = requests.post("http://162.105.146.135:8080/demo/attributes/", data=json.dumps(json_dict))
        end = time.time()
        times_multi.append((end - start) / 10)

    print(times_multi)
    
    times_single = []
    for i in range(10):
        tot_time = 0
        for j in range(i + 1):
            column_entities = [entities[i][k][j] for k in range(3)]
            json_dict = {
                "entities": column_entities
            }
            print(json.dumps(json_dict))
            start = time.time()
            for t in range(10):
                r = requests.post("http://162.105.146.135:8080/demo/types/", data=json.dumps(json_dict))
                r = requests.post("http://162.105.146.135:8080/demo/facts/", data=json.dumps(json_dict))
            end = time.time()
            tot_time += (end - start) / 10;
        times_single.append(tot_time)

    print(times_single)

if __name__ == '__main__':
    main()