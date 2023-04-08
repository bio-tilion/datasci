from src.acquisition import get_uniprot
from src.acquisition import get_sublocation
from src.acquisition import get_query
import pandas as pd


# list of sub-cellular compartments
compartments = ["Nucleus", "Cell membrane", "Cytoplasm",
                "Mitochondrion", "Endoplasmic reticulum", "Golgi apparatus"]
sub_locations = dict()

# look for sub-location IDs and store it in a dictionary
for sub_loc in compartments:
    r = get_sublocation(sub_loc)
    for i in r.json()["results"]:
        if i["name"] == sub_loc:
            sub_locations[sub_loc] = i["id"]

# old query in one go
#query = "{search_term} AND ({organism}) AND ({revision}) AND ({location}){fields}{format}".format(
#    # any wildcard
#    search_term="*",
#    # human
#    organism="taxonomy_id:9606",
#    # swissprot reviewed
#    revision="reviewed:true",
#    # selected fields
#    fields="&fields=accession,id,cc_subcellular_location",  # accession,id,cc_subcellular_location
#    # output format
#    format="&format=json",  # &format=tsv
#    # sub-cellular locations, loops all given compartments to generate a string
#    location=" OR ".join(["(cc_scl_term:" + sub_locations[i] + ")" for i in compartments])
#)

# query using the get_query function and looping through sub_locations
query_terms = {
    # human
    "taxonomy_id": "9606",
    # swissprot reviewed
    "reviewed": "true",
    # selected fields
    "fields": ["accession", "id", "sequence", "cc_subcellular_location"],
    # output format
    "format": "tsv",  # &format=tsv
}

for sub_loc in compartments:
    query = get_query("*", **query_terms, **{"cc_scl_term": sub_locations[sub_loc]})
    #print(query)

    # Uniprot search
    r = get_uniprot(query)
    # get results table
    table = [line.split("\t") for line in r.text.splitlines()]

    # create dataframe from table
    # first row as columns header
    df = pd.DataFrame(table[1:], columns=table[0])
    # add column for label encoding
    df["subcellular_location"] = [sub_loc] * len(df.index)

    # save dataframe in data folder
    df.to_parquet(f"data/df_{sub_loc.lower().replace(' ', '_')}.parquet")
