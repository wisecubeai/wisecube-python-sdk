from __future__ import annotations

import base64
from typing import List, Tuple

from wisecube_sdk import api_calls, create_payload, create_response, string_query
from wisecube_sdk.model_formats import WisecubeModel, OutputFormat
from wisecube_sdk.node_types import NodeType
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

    def search_qid(self, text):
        variables = {
            "question": text
        }
        payload = create_payload.create(string_query.search_qids, variables)
        headers = self.get_headers()
        response = api_calls.create_api_call(payload, headers, self.url, "json")
        return create_response.search_qids(response)

    def search_by_type(self, qid, name: str | None = None, include_instances: bool | None = None, include_subclasses: bool | None = None):
        variables = {
            "qid": qid
        }
        if name is not None:
            variables["name"] = name
        if include_instances is None:
            variables["include_instances"] = True  # default value
        else:
            variables["include_instances"] = include_instances
        if include_subclasses is None:
            variables["include_subclasses"] = False  # default value
        else:
            variables["include_subclasses"] = include_subclasses
        payload = create_payload.create(string_query.search_by_type, variables)
        headers = self.get_headers()
        response = api_calls.create_api_call(payload, headers, self.url, "json")
        return create_response.search_by_type(response,self.output_format)

    def search_by_relationship(self, predicate, qid, incoming: bool | None = None, qid_name: str | None = None, neighbor_name: str | None = None, batch_size: int | None = None):
        variables = {
            "predicate": predicate,
            "qid": qid
        }

        if incoming is None:
            variables["incoming"] = False
        else:
            variables["incoming"] = incoming
        if qid_name is not None:
            variables["qid_name"] = qid_name
        if neighbor_name is not None:
            variables["neighbor_name"] = neighbor_name
        if batch_size is None:
            variables["batch_size"] = 100
        else:
            variables["batch_size"] = batch_size

        payload = create_payload.create(string_query.search_by_relationship, variables)
        headers = self.get_headers()
        response = api_calls.create_api_call(payload, headers, self.url, "json")
        return create_response.search_by_relationship(response,self.output_format)

    def search_by_qualifier(self, triples: Tuple[str, str, str] | List[Tuple[str, str, str]],
        qual_pred: str,
        qual_name: str | None = None,
        sub_name: str | None = None,
        pred_name: str | None = None,
        obj_name: str | None = None,
        batch_size: int | None = None):
        variables = {
            "triple": triples,
            "qual_pred": qual_pred
        }
        if qual_name is not None:
            variables["qual_name"] = qual_name
        if sub_name is not None:
            variables["sub_name"] = sub_name
        if pred_name is not None:
            variables["pred_name"] = pred_name
        if obj_name is not None:
            variables["obj_name"] = obj_name
        if batch_size is None:
            variables["batch_size"] = 100
        else:
            variables["batch_size"] = batch_size
        payload = create_payload.create(string_query.search_by_qualifier, variables)
        headers = self.get_headers()
        response = api_calls.create_api_call(payload, headers, self.url, "json")
        return create_response.search_by_qualifier(response,self.output_format)

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
    def __init__(self, api_key):
        super().__init__("https://api.wisecube.ai/orpheus/graphql", "1mbgahp6p36ii1jc851olqfhnm")
        self.api_key = api_key

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key
        }

