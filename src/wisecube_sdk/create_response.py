def qa(response):
    response = response.json()
    return pd.DataFrame(response["data"]["summaryInsights"][0]["data"]["answers"][0]["document"])


def documents(response):
    response = response.json()
    return pd.DataFrame(response["data"]["summaryInsights"][0]["data"]["answers"][0]["document"])


def search_graph(response):
    response = response.json()
    nodes = pd.DataFrame(response["data"]["graphInsights"]["data"]["nodes"])
    nodes = pd.concat((pd.DataFrame([response["data"]["graphInsights"]["data"]["rootNode"]]), nodes))
    edges = pd.DataFrame(response["data"]["graphInsights"]["data"]["edges"])
    return nodes, edges


def search_text(response):
    response = response.json()
    return pd.DataFrame(response["data"]["searchAsYouType"]["data"]["searchLabels"])


def advanced_search(response):
    response = response.json()
    columns = response["data"]["advancedSearchGraph"]["head"]["vars"]
    rows = [{k: d["value"] for k, d in r.items()} for r in response["data"]["advancedSearchGraph"]["results"]["bindings"]]
    pd.DataFrame(rows)[columns]
    return response.json()
