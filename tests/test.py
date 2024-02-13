from src.wisecube_sdk.client import WisecubeClient
import wisecube_sdk.model_names
from wisecube_sdk.client import WisecubeClient
from wisecube_sdk.model_names import WisecubeModel as model

auth_api_client = WisecubeClient('API_KEY').client

graphIds = [
    "Q84263196",
    "Q12078"
  ]
vectors = auth_api_client.executeVectorFunction(graphIds)
print(vectors)



client = WisecubeClient("API_KEY").client

predicates = client.getPredicates("encoded")
print("Predicates data ....")

print(predicates)

graphIds =  "Q84263196"


vectors = client.executeVectorFunction(graphIds)

print("Vector data ....")
print(vectors)

triples= [
    [
      "Q14865565",
      "P2293",
      "Q3658562"
    ],
    [
      "Q14865565",
      "P2293",
      "Q282142"
    ],
    [
      "Q14865565",
      "P2293",
      "Q264118"
    ]
  ]
score = client.executeScoreFunction(triples)

print("Score data ....")
print(score)


smiles = [
"O1COc(c12)ccc(c2)NC(=O)C(=O)NCCc(c3)ccc(c34)N(C)CCC4",
"C1COc(c12)cc(Br)c(c2)NC(=O)C(=O)NCc(c3)ccc(c34)N(C)CC(C4)CO",
"c1coc(c12)cc(Br)c(c2)NC(=O)C(=O)NCc(c3)ccc(c34)N(C)CC(C4)CO"
]
predictions = client.getAdmetPrediction(smiles=smiles, model=model.CACO2)
print(predictions)