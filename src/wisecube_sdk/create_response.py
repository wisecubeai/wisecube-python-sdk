try:
    import pandas as pd
    use_pandas = True
except ImportError:
    use_pandas = False


def qa(response):
    response = response.json()
    if not use_pandas:
        return response, None
    documents =  pd.DataFrame(response["data"]["summaryInsights"][0]["data"]["answers"][0]["document"])
    answer = response["data"]["summaryInsights"][0]["data"]["answers"][0]["answer"]
    return answer, documents


def documents(response):
    response = response.json()
    if not use_pandas:
        return response
    return pd.DataFrame(response["data"]["summaryInsights"][0]["data"]["answers"][0]["document"])


def search_graph(response):
    response = response.json()
    if not use_pandas:
        return response
    nodes = pd.DataFrame(response["data"]["graphInsights"]["data"]["nodes"])
    nodes = pd.concat((pd.DataFrame([response["data"]["graphInsights"]["data"]["rootNode"]]), nodes))
    edges = pd.DataFrame(response["data"]["graphInsights"]["data"]["edges"])
    return nodes, edges


def search_text(response):
    response = response.json()
    if not use_pandas:
        return response
    return pd.DataFrame(response["data"]["searchAsYouType"]["data"]["searchLabels"])


def executeVectorFunction(response):
    response = response.json()
    if not use_pandas:
        return response
    return pd.DataFrame(response["data"]["executeVectorFunction"])


def executeScoreFunction(response):
    response = response.json()
    if not use_pandas:
        return response
    return pd.DataFrame(response["data"]["executeScoreFunction"], columns=["subject", "predicate", "object", "score"])


def getPredicates(response):
    response = response.json()
    if not use_pandas:
        return response
    return pd.DataFrame(response["data"]["getPredicates"])


def advanced_search(response):
    response = response.json()
    if not use_pandas:
        return response
    columns = response["data"]["advancedSearchGraph"]["head"]["vars"]
    rows = [{k: d["value"] for k, d in r.items()} for r in response["data"]["advancedSearchGraph"]["results"]["bindings"]]
    return pd.DataFrame(rows)[columns]
