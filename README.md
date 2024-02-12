# Wisecube SDK - Version - 0.0.1

## **Overview**

The Wisecube SDK provides a Python interface to interact with the Wisecube AI services. This SDK allows developers to seamlessly integrate with Wisecube's APIs for various functionalities.

## Getting Started
#### 1. Install the sdk from github

```bash
pip install git+https://github.com/wisecubeai/wisecube-python-sdk
```


#### 2. Authentication

Create an instance of the WisecubeClient class with your API key. This is done in a python console:

```python
from src import WisecubeClient
```

**Replace with API key** !

```python
auth_key = WisecubeClient('api_key')
```

## API Usage

```python
# Replace with the API key
auth_client = WisecubeClient('api_key')

# Perform operations using the SDK methods
auth_client.client.qa("What is the meaning of life?")
```
***Below is a table with the APIs and a short descirption. ***


| APIs                   | Description                                                                                           |
|------------------------|-------------------------------------------------------------------------------------------------------|
| [QA](#qa)              | returns the answer and documents related to the question                                             |
| [Documents](#doc)      | return documents for the question                                                                    |
| [Search_Graph](#graph) | returns results containing nodes and edges                                                           |
| [Search_Text](#search) | returns a list of entities related to the search term                                                |
 | [advanced_search](#ad) | returns a dataframe with multiple rows, each representing a different entity with its URI and label  |






### <h2 id="qa">QA</h2>
#### Description
This API provides relevant summary information for the specified question, including the answer and relevant documents associated with them.
```python
auth_client.client.qa(question)
```
#### Parameters
* _question_ (String): the input must be a question you want the answer to



### <h2 id="doc">Documents</h2>
#### Description
This  API query provides insights and relevant documents related to the question.
```python
auth_client.client.documents(question)
```

#### Parameters
* _question_ (String): the input must be a question to get the documents


### <h2 id="graph">Search Graph</h2>
#### Description
This API retrieves insights based on specified parameters and returns the results in the form of a subgraph containing nodes and edges.
```python
auth_client.client.search_graph(graphIds, nr=20)
```
#### Parameters
* -_graphIds_ ([String]): the input must be a list of ids, ID of the starting node in the graph
* -_maxNeighbors_(Int): represented by **_nr_** : optional variable, default is 10,representing the maximum number of neighbor nodes to retrieve


### <h2 id="search">Search Text</h2>
#### Description
The API returns a list of entities related to the search term.
```python
auth_client.client.search_text(searchText)
```
#### Parameters
* _searchText_ (String): the string you want to search

### <h2 id="ad">Advanced Search</h2>
#### Description
This API returns the entities retrieved from the Wikidata database based on the provided query.
```python
auth_client.client.advancedSearch(query)
```
#### Parameters
* _query_ (String): query for advanced search, encoded as a string

