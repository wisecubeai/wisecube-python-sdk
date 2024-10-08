qa = """
query($query: String!) {
  summaryInsights(engineID: "23343", searchInput: {query: $query, type: [QA]}) {
    data {
      __typename
      ... on QAInsight {
        question
        answers {
          answer
          document {
            id
            title
            abs
            source
            index_name
            __typename
          }
          took
          context
          statistics
          probability
          __typename
        }
        __typename
      }
    }
    __typename
  }
}
"""

documents = """
query($query: String!){
  summaryInsights(engineID: "23343", searchInput: {query: $query, type: [DOCUMENTS]}) {
    data {
      __typename
      ... on QAInsight {
        question
        answers {
          document {
            id
            title
            abs
            source
            index_name
            __typename
          }
          took
          context
          statistics
          probability
          __typename
        }
        __typename
      }
    }
    __typename
  }
}
"""

search_graph = """
query graphInsights($startNode: ID, $startNodeName: String, $nodeTypes: [NodeType], $maxNeighbors: Int) {
  graphInsights(
    engineID: "23343"
    graphInput: {startNode: $startNode, startNodeName: $startNodeName, nodeTypes: $nodeTypes, maxNeighbors: $maxNeighbors}
  ) {
    description
    data {
      __typename
      ... on SubGraph {
        description
        rootNode{
            id
            name
        }
        nodes {
          id
          name
          type
          properties {
            name
            values
            __typename
          }
          __typename
        }
        edges {
          id
          start {
            id
            __typename
          }
          end {
            id
            __typename
          }
          __typename
        }
        __typename
      }
    }
    __typename
  }
}
"""

search_text = """
query($query: String!){
  searchAsYouType(
    searchInput: { searchText: $query, type: SEARCH_LABEL }
  ) {
    description
    type
    data {
      __typename
      ... on SearchLabels {
        searchLabels {
          qid
          text
          nodeTypes
        }
      }
    }
  }
}
"""

execute_score_function = """
query($triples: [[String!]]) { executeScoreFunction(triples: $triples
  )
}
"""

execute_vector_function = """
query($graphIds: [String!]) { executeVectorFunction(graphIds: $graphIds)  
}
"""

execute_nl2sparql = """
query executeNl2Sparql($question: String!) {
  executeNl2Sparql(question: $question) 
}
"""

get_predicates = """
query($label: String!){getPredicates(label: $label)}
"""

get_admet_prediction = """
query ($smiles: [String!], $modelName: String){ admetPredict(smiles: $smiles, modelName: $modelName)
}

"""

advanced_search_query = """
query advancedSearchQuery($query: String) {
  advancedSearchGraph(query: $query) {
    head
    results
    __typename
  }
}
"""


ask_pythia = """
query askPythia($reference: [String!], $response: String!, $question: String, $includeDefaultValidators: Boolean) {
  askPythia(reference: $reference, response: $response, question: $question, includeDefaultValidators: $includeDefaultValidators) 
}
"""


search_qids = """
query getQids($question: String!) { getQids(question: $question) }
"""

search_entities ="""
query searchEntities($name: String!, $ignoreCase: Boolean, $matchingStrategy: String,$limit:Int) {
  searchEntities(name: $name, ignoreCase: $ignoreCase, matchingStrategy: $matchingStrategy, limit: $limit)}
"""

search_predicate="""
query searchPredicates($name: String!, $ignoreCase: Boolean, $matchingStrategy: String,$limit:Int) {
  searchPredicates(name: $name, ignoreCase: $ignoreCase, matchingStrategy: $matchingStrategy,limit: $limit)}
"""


length_1_queries = ["""
SELECT DISTINCT
  ?target ("->" AS ?dir)?pred ?predLabel ?idxmax
WHERE {
  BIND(wd:INDEX AS ?target)
  BIND(wd:IDXMAX AS ?idxmax)
  ?target ?pred ?idxmax .
  ?predEntity wikibase:directClaim ?pred .
  ?predEntity rdfs:label ?predLabel .
  FILTER(LANG(?predLabel)="en")
}
""", """
SELECT DISTINCT
  ?target ("<-" AS ?dir) ?pred ?predLabel ?idxmax
WHERE {
  BIND(wd:INDEX AS ?target)
  BIND(wd:IDXMAX AS ?idxmax)
  ?idxmax ?pred ?target.
  ?predEntity wikibase:directClaim ?pred .
  ?predEntity rdfs:label ?predLabel .
  FILTER(LANG(?predLabel)="en")
}
"""]

length_2_queries = ["""
SELECT DISTINCT
  ?target ("->" AS ?dir1) ?pred1 ?pred1Label ?n ?nLabel ("->" AS ?dir2) ?pred2 ?pred2Label ?idxmax
WHERE {
  BIND(wd:INDEX AS ?target)
  BIND(wd:IDXMAX AS ?idxmax)
  ?target ?pred1 ?n .
  ?n ?pred2 ?idxmax .
  ?pred1Entity wikibase:directClaim ?pred1 .
  ?pred1Entity rdfs:label ?pred1Label .
  FILTER(LANG(?pred1Label)="en")
  ?pred2Entity wikibase:directClaim ?pred2 .
  ?pred2Entity rdfs:label ?pred2Label .
  FILTER(LANG(?pred2Label)="en")
  ?n rdfs:label ?nLabel .
  FILTER(LANG(?nLabel)="en")
}
""", """
SELECT DISTINCT
  ?target ("->" AS ?dir1) ?pred1 ?pred1Label ?n ?nLabel ("<-" AS ?dir2) ?pred2 ?pred2Label ?idxmax
WHERE {
  BIND(wd:INDEX AS ?target)
  BIND(wd:IDXMAX AS ?idxmax)
  ?target ?pred1 ?n .
  ?idxmax ?pred2 ?n .
  ?pred1Entity wikibase:directClaim ?pred1 .
  ?pred1Entity rdfs:label ?pred1Label .
  FILTER(LANG(?pred1Label)="en")
  ?pred2Entity wikibase:directClaim ?pred2 .
  ?pred2Entity rdfs:label ?pred2Label .
  FILTER(LANG(?pred2Label)="en")
  ?n rdfs:label ?nLabel .
  FILTER(LANG(?nLabel)="en")
}
""", """
SELECT DISTINCT
  ?target ("<-" AS ?dir1) ?pred1 ?pred1Label ?n ?nLabel ("->" AS ?dir2) ?pred2 ?pred2Label ?idxmax
WHERE {
  BIND(wd:INDEX AS ?target)
  BIND(wd:IDXMAX AS ?idxmax)
  ?n ?pred1 ?target .
  ?n ?pred2 ?idxmax .
  ?pred1Entity wikibase:directClaim ?pred1 .
  ?pred1Entity rdfs:label ?pred1Label .
  FILTER(LANG(?pred1Label)="en")
  ?pred2Entity wikibase:directClaim ?pred2 .
  ?pred2Entity rdfs:label ?pred2Label .
  FILTER(LANG(?pred2Label)="en")
  ?n rdfs:label ?nLabel .
  FILTER(LANG(?nLabel)="en")
}
""", """
SELECT DISTINCT
  ?target ("<-" AS ?dir1) ?pred1 ?pred1Label ?n ?nLabel ("<-" AS ?dir2) ?pred2 ?pred2Label ?idxmax
WHERE {
  BIND(wd:INDEX AS ?target)
  BIND(wd:IDXMAX AS ?idxmax)
  ?n ?pred1 ?target .
  ?idxmax ?pred2 ?n .
  ?pred1Entity wikibase:directClaim ?pred1 .
  ?pred1Entity rdfs:label ?pred1Label .
  FILTER(LANG(?pred1Label)="en")
  ?pred2Entity wikibase:directClaim ?pred2 .
  ?pred2Entity rdfs:label ?pred2Label .
  FILTER(LANG(?pred2Label)="en")
  ?n rdfs:label ?nLabel .
  FILTER(LANG(?nLabel)="en")
}
"""]