from wisecube_sdk import api_calls, create_payload, create_response, string_query
import json


class WisecubeClient:
    def __init__(self, *args):
        if len(args) == 0:
            open_url = "http://127.0.0.1:5000/api/endpoint"
            self.client = OpenClient(open_url)
        elif len(args) == 1:
            self.client = ApiClient(*args)
        elif len(args) == 3:
            self.client = AuthClient(*args)
        else:
            raise Exception("Invalid args")


class QueryMethods:
    def __init__(self, url, client_id):
        self.url = url
        self.client_id = client_id

    def get_headers(self):
        raise NotImplementedError("Subclasses must implement get_headers")

    def qa(self, text):
        variables = {
            "query": text
        }
        payload = create_payload.create(string_query.qa, variables)
        headers = self.get_headers()
        response = api_calls.create_api_call(payload, headers, self.url, "json")
        return create_response.qa(response)

    def documents(self, text):
        variables = {
            "query": text
        }
        payload = create_payload.create(string_query.documents, variables)
        headers = self.get_headers()
        response = api_calls.create_api_call(payload, headers, self.url, "json")
        return create_response.documents(response)

    def search_graph(self, text, nr=10):
        if create_payload.is_valid_url(text):
            variables = {
                "maxNeighbours": nr,
                "startNode": text
            }
        else:
            variables = {
                "maxNeighbours": nr,
                "startNodeName": text
            }
        payload = create_payload.create(string_query.search_graph, variables)
        headers = self.get_headers()
        response = api_calls.create_api_call(payload, headers, self.url, "json")
        return create_response.search_graph(response)

    def search_text(self, text):
        variables = {
            "query": text
        }
        payload = create_payload.create(string_query.search_text, variables)
        headers = self.get_headers()
        response = api_calls.create_api_call(payload, headers, self.url, "json")
        return create_response.search_text(response)


class OpenClient:
    def __init__(self, url):
        self.url = url


class AuthClient(QueryMethods):
    def __init__(self, username, password):
        super().__init__("https://api.wisecube.ai/orpheus/graphql", "1mbgahp6p36ii1jc851olqfhnm")
        self.username = username
        self.password = password

    def create_token(self):
        payload = {
            "AuthParameters": {
                "USERNAME": self.username,
                "PASSWORD": self.password
            },
            "AuthFlow": "USER_PASSWORD_AUTH",
            "ClientId": self.client_id
        }
        headers = {"X-Amz-Target": "AWSCognitoIdentityProviderService.InitiateAuth",
                   "Content-Type": "application/x-amz-json-1.1"
                   }
        cognito_url = "https://cognito-idp.us-east-2.amazonaws.com/"

        response = api_calls.create_api_call(payload, headers, cognito_url, "json")

        token = json.loads(response.text)["AuthenticationResult"]["AccessToken"]

        return token

    def get_headers(self):
        return {
            'Authorization': 'Bearer {}'.format(self.create_token()),
            'Content-Type': 'application/json',
        }


class ApiClient(QueryMethods):
    def __init__(self, api_key):
        super().__init__("https://api.wisecube.ai/orpheus/graphql", "1mbgahp6p36ii1jc851olqfhnm")
        self.api_key = api_key

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key
        }
