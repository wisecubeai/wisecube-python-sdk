from wisecube_sdk.client import WisecubeClient
from wisecube_sdk.model_names import WisecubeModel as model
from getpass import getpass
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        API_KEY = sys.argv[1]
    else:
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
    results = client.execute_vector_function(graphIds)
    print(results)

    print("="*50, end="\n"*3)

    triples = [
        ['Q183134', 'P2176', 'Q1050019'],
        ['Q183134', 'P2176', 'Q1052672'],
        ['Q183134', 'P2176', 'Q1082945']
    ]
    print("results = client.executeScoreFunction(triples)")
    results = client.execute_score_function(triples)
    print(results)

    print("="*50)

    predicate = "encodes"
    print("results = client.getPredicates(predicate)")
    results = client.get_predicates(predicate)
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



    smiles = [
       "O1COc(c12)ccc(c2)NC(=O)C(=O)NCCc(c3)ccc(c34)N(C)CCC4",
       "C1COc(c12)cc(Br)c(c2)NC(=O)C(=O)NCc(c3)ccc(c34)N(C)CC(C4)CO",
       "c1coc(c12)cc(Br)c(c2)NC(=O)C(=O)NCc(c3)ccc(c34)N(C)CC(C4)CO"
    ]
    predictions = client.getAdmetPrediction(smiles=smiles, model=model.CACO2)
    print(predictions)

