import os
import sys
import time
import requests
import json

def main():
    entities = [
        ["Dick_Van_Dyke", "Barry_Van_Dyke", "Murder_101_(film_series)"],
        ["John_Huston","Anjelica_Huston", "e_Dead_(1987_film)"],
        ["Martin_Sheen", "Charlie_Sheen", "A_Letter_from_Death_Row_(film)"],
        ["Martin_Sheen", "Charlie_Sheen", "Wall_Street_(1987_film)"],
        ["Martin_Sheen", "Charlie_Sheen", "The_Execution_of_Private_Slovik"],
        ["Martin_Sheen", "Charlie_Sheen", "Free_Money_(film)"],
        ["Martin_Sheen", "Charlie_Sheen", "No_Code_of_Conduct"],
        ["John_Carradine", "David_Carradine Boxcar_Bertha"],
        ["Lloyd_Bridges", "Jeff_Bridges", "Blown_Away_(1994_film)"],
        ["Diane_Ladd", "Laura_Dern", "Rambling_Rose_(film)"],
        ["Diane_Ladd", "Laura_Dern", "Wild_at_Heart_(film)"]
    ]
    
    times_multi = []
    for i in range(10):
        json_dict = {
            "entities": entities[: i + 1],
            "row_number": i + 1,
            "v_number": 3,
            "exp": True
        }
        print(json.dumps(json_dict))
        start = time.time()
        for t in range(10):
            r = requests.post("http://162.105.146.135:8080/demo/pattern/", data=json.dumps(json_dict))
        end = time.time()
        times_multi.append((end - start) / 10)

    print(times_multi)
    
    times_single = []
    for i in range(10):
        tot_time = 0
        for row_entities in entities[: i + 1]:
            json_dict = {
                "entities": row_entities,
                "v_number": 3
            }
            print(json.dumps(json_dict))
            start = time.time()
            for t in range(10):
                r = requests.post("http://162.105.146.135:8080/demo/one-row-direction/", data=json.dumps(json_dict))
            end = time.time()
            tot_time += (end - start) / 10;
        times_single.append(tot_time)

    print(times_single)

if __name__ == '__main__':
    main()