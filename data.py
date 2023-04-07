from src.acquisition import get_uniprot
from src.acquisition import get_sublocation


compartments = ["Nucleus", "Cell membrane", "Cytoplasm",
                "Mitochondrion", "Endoplasmic reticulum", "Golgi apparatus"]

for sub_loc in compartments:
    r = get_sublocation(sub_loc)
    for i in r.json()["results"]:
        if i["name"] == sub_loc:
            print(i["name"], i["id"])
