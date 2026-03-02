# СТРУКТУРА
# data  → dict
# data["list1"] → list
# data["list1"][0] → dict

import json
import sys

from datetime import date

current_year = date.today().year

try:
    with open("input.txt", "r", encoding="utf-8") as file:
        content = file.read()

        if not content.strip():
            print("Empty file")
        else:        
            data = json.loads(content)

except FileNotFoundError:
    print("error! file not found")

except json.JSONDecodeError:
    print("error! incorrect json")            
    sys.exit()

for movie in data["list1"]:
    if "title" not in movie or "year" not in movie or not movie["title"].strip():
        print("error!incorrect key")
        sys.exit()
    if not isinstance(movie["title"], str) or not isinstance(movie["year"], int):
        print("error!error in type of date")
        sys.exit()
    if movie["year"] > current_year or movie["year"] < 1895 or movie["year"] is None:
        print("error!error in date")
        sys.exit()

for movie in data["list2"]:
    if "title" not in movie or "year" not in movie or not movie["title"].strip():
        print("error!incorrect key")
        sys.exit()
    if not isinstance(movie["title"], str) or not isinstance(movie["year"], int):
        print("error!error in type of date")
        sys.exit()
    if movie["year"] > current_year or movie["year"] < 1895 or movie["year"] is None:
        print("error!error in date")
        sys.exit()


# объединяет 2 списка 
# data["list1"].extend(data["list2"])
# all_movies = data["list1"]
all_movies = data["list1"] + data["list2"]

all_movies.sort(key=lambda movie: movie["year"])

result = {"list0": all_movies}

print(json.dumps(result, ensure_ascii=False, indent=2))

