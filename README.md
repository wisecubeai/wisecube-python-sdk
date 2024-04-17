# Wisecube SDK - Version - 0.0.1

## **Overview**

The Wisecube SDK provides a Python interface to interact with the Wisecube AI services. This SDK allows developers to seamlessly integrate with Wisecube's APIs for various functionalities.

## Getting Started
#### 1. Install the sdk from github

```bash
pip install wisecube
```


#### 2. Authentication

Create an instance of the WisecubeClient class with your API key. This is done in a python console:

```python
from wisecube_sdk.client import WisecubeClient
from wisecube_sdk.model_formats import OutputFormat
  

client = WisecubeClient("key").client
client.output_format=OutputFormat.PANDAS
```

## API Usage

```python
# Replace with your API key
client = WisecubeClient("key").client
client.output_format=OutputFormat.PANDAS

# Perform operations using the SDK methods
client.qa("Which proteins participate in the formation of the ryanodine receptor quaternary macromolecular complex?")
```
***Below is a table with the APIs and a short descirption. ***


| APIs                           | Description                                                                                         |
|--------------------------------|-----------------------------------------------------------------------------------------------------|
| [qa](#qa)                      | returns the answer and documents related to the question                                            |
| [documents](#doc)              | return documents for the question                                                                   |
| [search_graph](#graph)         | returns results containing nodes and edges                                                          |
| [search_text](#search)         | returns a list of entities related to the search term                                               |
 | [advance_search](#ad)         | returns a dataframe with multiple rows, each representing a different entity with its URI and label |
| [get_predicates](#pred)         | retrieves information about predicates associated with a given label                                |
| [execute_vector_function](#vect) | retrieves embeddings for the given entities                                                         |
| [execute_score_function](#score) | returns the score for each triple                                                                   |
| [get_admet_prediction](#admet)   | returns prediction using ADMET models and sagemaker 
| [nl_to_sparql](#nl)              | returns text converted to sparql                                                                    |
| [ask_pythia](#pythia)            | return claims about the input                                                                       |


### <h2 id="qa">QA</h2>
#### Description
This API provides relevant summary information for the specified question, including the answer and relevant documents associated with them.
```python
client.qa(question)
```
#### Parameters
* _question_ (String): the input must be a question you want the answer to



### <h2 id="doc">Documents</h2>
#### Description
This  API query provides insights and relevant documents related to the question.
```python
client.documents(question)
```

#### Parameters
* _question_ (String): the input must be a question to get the documents


### <h2 id="graph">Search Graph</h2>
#### Description
This API retrieves insights based on specified parameters and returns the results in the form of a subgraph containing nodes and edges.
```python
client.search_graph(graphIds, nr=20)
```
#### Parameters
* -_graphIds_ ([String]): the input must be a list of ids, ID of the starting node in the graph
* -_maxNeighbors_(Int): represented by **_nr_** : optional variable, default is 10,representing the maximum number of neighbor nodes to retrieve


### <h2 id="search">Search Text</h2>
#### Description
The API returns a list of entities related to the search term.
```python
client.search_text(searchText)
```
#### Parameters
* _searchText_ (String): the string you want to search

### <h2 id="ad">Advanced Search</h2>
#### Description
This API returns the entities retrieved from the Wikidata database based on the provided query.
```python
client.advance_search(query)
```
#### Parameters
* _query_ (String): query for advanced search, encoded as a string


### <h2 id="pred">Predicate Graph</h2>
#### Description
The API retrieves information about predicates associated with a given label.

```python
client.get_predicates(labels)
```
#### Parameters
* _labels_(String): represents the label of a predicate


### <h2 id="vect">Execute Vector Function</h2>
#### Description
The API retrieves embeddings for the given entities.

```python
client.execute_vector_function(graphIds)
```

#### Parameters
* _graphIds_[String]: variable used to specify a list of graph IDs


### <h2 id="score">Execute Score Function</h2>
#### Description
This API retrieves the score for each triple.

```python
client.execute_score_function(triples)
```

#### Parameters
* _triples_[[String]]: variable representing a list of lists of strings, containing three elements


### <h2 id="admet">Admet Prediction </h2>
#### Description
This API retrieves prediction using ADMET models and sagemaker.

List of models: [BBB, logS, CYP2CI9i, LogD7, PGPi, PGPs, HIA, F20, F30, PPB, VD, CYPIA2i, CYPIA2s, CYP3A4i, CYP3A4s, CYP2C9i, CYP2C9s, CYP2C19s, CYP2D6i, CYP2D6s,  CL, Ames, DILI, SkinS, Caco2, THALF, hERG, HHT ]

```python
client.get_admet_prediction(smiles=smiles, model=model.BBB)
```

#### Parameters
* _smiles_[String]: specification in the form of a line notation for describing the structure of chemical species
* _model_ (String): represents the model name


### <h2 id="nl">Nl to sparql</h2>
#### Description
This API converts text to sparql.

```python
client.nl_to_sparql(question)
```

#### Parameters

* _question_[String]: the input must be a question 


#### Parameters
* _graphIds_[String]: variable used to specify a list of graph IDs


### <h2 id="pythia">Ask Pythia</h2>
#### Description
This API obtains related claims or information about the input reference, response and question.

```python
client.ask_pythia(reference,response,question)
```

#### Parameters
* _question_(String): the input must be a question
* _reference_([String]): information related to a medical report
* _response_ (String): response related to a medical report

