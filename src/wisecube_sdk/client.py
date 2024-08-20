import base64
from typing import List

from wisecube_sdk import api_calls, create_payload, create_response, string_query
from wisecube_sdk.model_formats import WisecubeModel, OutputFormat
from wisecube_sdk.node_types import NodeType
import json
from openai import OpenAI


class WisecubeClient:
    def __init__(self, *args, openai_api_key=None):
        if len(args) == 0:
            open_url = "http://127.0.0.1:5000/api/endpoint"
            self.client = OpenClient(open_url)
        elif len(args) == 1:
            self.client = ApiClient(*args, openai_api_key)
        elif len(args) == 3:
            self.client = AuthClient(*args)
        else:
            raise Exception("Invalid args")

class QueryMethods:
    def __init__(self, url, client_id, openai_api_key):
        self.url = url
        self.client_id = client_id
        self.gpt_client = OpenAI(api_key=openai_api_key) if openai_api_key else None


    @property
    def output_format(self):
        return getattr(self, '_output_format', OutputFormat.JSON)

    @output_format.setter
    def output_format(self, value):
        if not isinstance(value, OutputFormat):
            raise ValueError("output_format must be a OutputFormat.")
        self._output_format = value

    def get_headers(self):
        raise NotImplementedError("Subclasses must implement get_headers")


    def chat_gpt(self, question):
        prompt = f"""
        Given the following scientific question, extract only the biological process or disease terms depending on question!

        Question:
        "{question}"
        The response will be returned as text separated by |:
        """
        response = self.gpt_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()

    def search_qids(self, question):
        # self.output_format = OutputFormat.JSON
        list_of_words = self.chat_gpt(question).split("|")
        # print(list_of_words)
        qids = []
        for word in list_of_words:
            search_text = self.search_text(word)
            try:
                qid = search_text["data"]["searchAsYouType"]["data"]["searchLabels"][0]["qid"]
                qids.append(qid)
            except (KeyError, IndexError) as e:
                print(f"Error retrieving QID for word '{word}': {e}")

        return qids


    def qa(self, text):
        variables = {
            "query": text
        }
        payload = create_payload.create(string_query.qa, variables)
        headers = self.get_headers()
        response = api_calls.create_api_call(payload, headers, self.url, "json")
        return create_response.qa(response, self.output_format)

    def documents(self, text):
        variables = {
            "query": text
        }
        payload = create_payload.create(string_query.documents, variables)
        headers = self.get_headers()
        response = api_calls.create_api_call(payload, headers, self.url, "json")
        return create_response.documents(response, self.output_format)

    def search_graph(self, text, nr=10, node_types: List[NodeType] = None):
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

        if node_types is not None:
            node_type_names = [node_type.name for node_type in node_types]
            variables["nodeTypes"] = node_type_names

        payload = create_payload.create(string_query.search_graph, variables)
        headers = self.get_headers()
        response = api_calls.create_api_call(payload, headers, self.url, "json")
        return create_response.search_graph(response, self.output_format)

    def search_text(self, text):
        variables = {
            "query": text
        }
        payload = create_payload.create(string_query.search_text, variables)
        headers = self.get_headers()
        response = api_calls.create_api_call(payload, headers, self.url, "json")
        return create_response.search_text(response, self.output_format)

    def execute_vector_function(self, graphIds: [str]):
        variables = {
            "graphIds": graphIds
        }
        payload = create_payload.create(string_query.execute_vector_function, variables)
        headers = self.get_headers()
        response = api_calls.create_api_call(payload, headers, self.url, "json")
        if response is not None:
            return create_response.execute_vector_function(response, self.output_format)

    def execute_score_function(self, graphIds: [[str]]):
        variables = {
            "triples": graphIds
        }
        payload = create_payload.create(string_query.execute_score_function, variables)
        headers = self.get_headers()
        response = api_calls.create_api_call(payload, headers, self.url, "json")
        return create_response.execute_score_function(response, self.output_format)

    def nl_to_sparql(self, question: str):
        variables = {
            "question": question
        }
        payload = create_payload.create(string_query.execute_nl2sparql, variables)
        headers = self.get_headers()
        response = api_calls.create_api_call(payload, headers, self.url, "json")
        return create_response.nl_2_sparql(response)

    def get_predicates(self, label: str):
        variables = {
            "label": label
        }
        payload = create_payload.create(string_query.get_predicates, variables)
        headers = self.get_headers()
        response = api_calls.create_api_call(payload, headers, self.url, "json")
        return create_response.get_predicates(response, self.output_format)

    def advance_search(self, query: str):
        variables = {
            "query": query
        }
        payload = create_payload.create(string_query.advanced_search_query, variables)
        headers = self.get_headers()
        response = api_calls.create_api_call(payload, headers, self.url, "json")
        return create_response.advanced_search(response, self.output_format)

    def get_admet_predictions(self, smiles: [str], model: WisecubeModel):
        variables = {
            "smiles": smiles,
            "modelName": model.value
        }
        payload = create_payload.create(string_query.get_admet_prediction, variables)
        headers = self.get_headers()
        response = api_calls.create_api_call(payload, headers, self.url, "json")
        return create_response.basic(response)

    def ask_pythia(self, references: [str], response: str, question: str, include_default_validators=False):

        variables = {
            "reference": references,
            "response": response
        }
        if question is not None:
            variables["question"] = question
        if include_default_validators is None:
            variables["includeDefaultValidators"] = False
        else:
            variables["includeDefaultValidators"] = include_default_validators


        payload = create_payload.create(string_query.ask_pythia, variables)
        headers = self.get_headers()
        response = api_calls.create_api_call(payload, headers, self.url, "json")
        return create_response.basic(response)


class OpenClient:
    def __init__(self, url):
        self.url = url


class AuthClient(QueryMethods):
    def __init__(self, username, password, ):
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
    def __init__(self, api_key,openai_api_key):
        super().__init__("https://api.wisecube.ai/orpheus/graphql", "1mbgahp6p36ii1jc851olqfhnm",openai_api_key=openai_api_key)
        self.api_key = api_key

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key
        }

