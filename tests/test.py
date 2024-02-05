from src.wisecube_sdk.clint import WisecubeClient


auth_api_client = WisecubeClient('LUcIwKi1SY2bkQgji8uwA5SAYO20hu0n53Ew4Bdq').client

graphIds = [
    "Q84263196",
    "Q12078"
  ]
vectors = auth_api_client.executeVectorFunction(graphIds)
print(vectors)