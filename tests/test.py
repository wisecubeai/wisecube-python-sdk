from wisecube_sdk.client import WisecubeClient
from getpass import getpass


if __name__ == "__main__":
    API_KEY = getpass("Wisecube API key")
    client = WisecubeClient(API_KEY).client

    query = "What genes are associated with diabetes?"
    print("results = client.qa(query)")
    results = client.qa(query)
    print(results)

    print("="*50)

    print("results = client.documents(query)")
    results = client.documents(query)
    print(results)

    print("="*50)

    entity = "diabetes"
    print("results = client.search_text(entity)")
    results = client.search_text(entity)
    print(results)

    print("="*50)

    print("results = client.search_graph(entity)")
    results = client.search_graph(entity)
    print(results)

    print("="*50)

    graphIds = [
        "Q84263196",
        "Q12078"
      ]
    print("results = client.executeVectorFunction(graphIds)")
    results = client.executeVectorFunction(graphIds)
    print(results)

    print("="*50, end="\n"*3)

    triples = [
        ['Q183134', 'P2176', 'Q1050019'],
        ['Q183134', 'P2176', 'Q1052672'],
        ['Q183134', 'P2176', 'Q1082945']
    ]
    print("results = client.executeScoreFunction(triples)")
    results = client.executeScoreFunction(triples)
    print(results)

    print("="*50)

    predicate = "encodes"
    print("results = client.getPredicates(predicate)")
    results = client.getPredicates(predicate)
    print(results)

    query = """
    SELECT DISTINCT ?predicate ?predicateLabel ?object ?objectLabel
    WHERE {
      #get all edges going from sepsis to anything else
      wd:Q183134 ?predicate ?object .

      #this is how you get names of predicates
      ?predicateEntity wikibase:directClaim ?predicate .
      ?predicateEntity rdfs:label ?predicateLabel .
      FILTER(LANG(?predicateLabel)="en")

      #this is how you get names for entities
      #this also has the effect limiting the objects to entities and not property values
      ?object rdfs:label ?objectLabel .
      FILTER(LANG(?objectLabel)="en")
    }
    """
    results = client.advancedSearch(query)
    results = client.advancedSearch(query)
    print(results)