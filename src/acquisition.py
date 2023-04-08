import requests
import sys

uniprot_API = "https://rest.uniprot.org/"


# function adapted from Uniprot webinar
def get_url(url, **kwargs):
    """
    Function to handle status codes other than 200
    """
    response = requests.get(url, **kwargs)

    if not response.ok:
        print(response.text)
        response.raise_for_status()
        sys.exit()

    return response


def results_page_stream(paginated: bool) -> str:
    """
    Function for choosing the results format:
        paginated or a single stream.
    """
    if paginated:
        # paginated results
        results_format = "search"
    else:
        # results in one unique stream
        results_format = "stream"
    return results_format


def get_uniprot(query: str, pages=False) -> requests.models.Response:
    """
    Function to retrieve results from Uniprot based on a query statement

    Arguments
        query       String, Uniprot formatted query
                    (see https://www.uniprot.org/help/text-search)
        pages       Bool, to get results organised in pages or a single stream
                    (Default False, single stream)

    Return a Response object
    """
    # paginated results or single stream
    search = results_page_stream(pages)

    # full url
    url = f"{uniprot_API}/uniprotkb/{search}?query={query}"

    # get query
    response = get_url(url)

    return response


def get_sublocation(query: str, pages=False) -> requests.models.Response:
    """
    Function to retrieve Subcellular location results from Uniprot based
    on a query statement

    Arguments
        query       String, Uniprot formatted query
                    (see https://www.uniprot.org/help/text-search)
        pages       Bool, to get results organised in pages or a single stream
                    (Default False, single stream)

    Return a Response object
    """
    # paginated results or single stream
    search = results_page_stream(pages)

    # full url
    url = f"{uniprot_API}/locations/{search}?query={query}"

    # get query
    response = get_url(url)

    return response


def get_query(search_term: str, **parameters) -> str:
    """
    Function to produce a query statement for a Uniprot search

    Arguments
        search_term     String, keyword for the Uniprot search
        parameters      Dictionary, optional parameters that can be passed for the search.
                        Each key and value must be a supported Uniprot field (see
                        https://www.uniprot.org/help/query-fields).
                        'format' and 'fields' are dealt separately, and the value for
                        'fields' must be a list of the desired fields.

    Returns a string with the full query
    """
    # get list with all terms for the search
    query = [search_term]

    for k, v in parameters.items():
        if k == "format":
            # get format
            output_format = f"&format={v}"
        elif k == "fields":
            # get fields
            fields = f"&fields={','.join(v)}"
        else:
            # get all other terms
            query.append(f"({k}:{v})")

    # get string concatenated with "AND"
    query = " AND ".join(query)

    # add format and fields
    query = query + fields + output_format
    return query


if __name__ == "__main__":
    help(get_uniprot)
    help(get_sublocation)
    help(get_query)
