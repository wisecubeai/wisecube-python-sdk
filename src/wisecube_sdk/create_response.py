from wisecube_sdk.model_formats import OutputFormat
import pandas as pd


def basic(response):
    response = response.json()
    return response


def qa(response, output_format: OutputFormat):
    response = response.json()
    if output_format == OutputFormat.JSON:
        return response, None
    documents = pd.DataFrame(response["data"]["summaryInsights"][0]["data"]["answers"][0]["document"])
    answer = response["data"]["summaryInsights"][0]["data"]["answers"][0]["answer"]
    return answer, documents


def documents(response, output_format: OutputFormat):
    response = response.json()
    if output_format == OutputFormat.JSON:
        return response
    return pd.DataFrame(response["data"]["summaryInsights"][0]["data"]["answers"][0]["document"])


def search_graph(response, output_format: OutputFormat):
    response = response.json()
    if output_format == OutputFormat.JSON:
        return response
    nodes = pd.DataFrame(response["data"]["graphInsights"]["data"]["nodes"])
    nodes = pd.concat((pd.DataFrame([response["data"]["graphInsights"]["data"]["rootNode"]]), nodes))
    edges = pd.DataFrame(response["data"]["graphInsights"]["data"]["edges"])
    return nodes, edges


def search_text(response, output_format: OutputFormat):
    response = response.json()
    if output_format == OutputFormat.JSON:
        return response
    return pd.DataFrame(response["data"]["searchAsYouType"]["data"]["searchLabels"])


def execute_vector_function(response, output_format: OutputFormat):
    response = response.json()
    if output_format == OutputFormat.JSON:
        return response
    return pd.DataFrame(response["data"]["executeVectorFunction"])


def execute_score_function(response, output_format: OutputFormat):
    response = response.json()
    if output_format == OutputFormat.JSON:
        return response
    return pd.DataFrame(response["data"]["executeScoreFunction"], columns=["subject", "predicate", "object", "score"])


def get_predicates(response, output_format: OutputFormat):
    response = response.json()
    if output_format == OutputFormat.JSON:
        return response
    return pd.DataFrame(response["data"]["getPredicates"])


def nl_2_sparql(response):
    response = response.json()
    try:
        return response["data"]["executeNl2Sparql"]["SPARQL"]
    except Exception as e:
        print(e)
    return response


def advanced_search(response, output_format: OutputFormat):
    response = response.json()
    if output_format == OutputFormat.JSON:
        return response
    columns = response["data"]["advancedSearchGraph"]["head"]["vars"]
    rows = [{k: d["value"] for k, d in r.items()} for r in
            response["data"]["advancedSearchGraph"]["results"]["bindings"]]
    return pd.DataFrame(rows)[columns]
