# Wisecube SDK - Version - 0.0.1

## **Overview**

The Wisecube SDK provides a Python interface to interact with the Wisecube AI services. This SDK allows developers to seamlessly integrate with Wisecube's APIs for various functionalities.

## Getting Started
### 1. Install the sdk from github

```bash
pip install git+https://github.com/wisecubeai/wisecube-python-sdk
```


### 2. Authentication

Create an instance of the WisecubeClient class with your authentication credentials. This is done in a python console:

```python
from src import WisecubeClient
```

**Replace with your actual credentials** !

```python
auth_user = WisecubeClient('your_username@domain.com', 'your_password')
auth_key = WisecubeClient('api_key')
```

### 3. Use SDK Methods

Run one of the following commands

Quick Answers (QA)  
```python
auth_client.client.qa("Your QA Text")
```
Documents
```python
auth_client.client.documents("Your Search Text")
```
Search Graph
```python
# The second variable (nr) is optional and defaults to 10
auth_client.client.search_graph("Your Graph Text", nr=20)
```
Search Text
```python
auth_client.client.search_text("Your Search Text")
```

### 4. Example
```python
# Replace with your actual credentials
auth_client = WisecubeClient('your_username@domain.com', 'your_password', 'your_api_key')

# Perform operations using the SDK methods
auth_client.client.qa("What is the meaning of life?")
```

***Below is a table with all the methods and their corresponding variables. Optional variables are marked with an asterisk `*`.***


| Query          | Variables                                  | Implementation                                             |
|----------------|------------------------------------------- |------------------------------------------------------------|
| QA             | query                                      | qa("query")                                                |
| Documents      | query                                      | documents("query")                                         |
| Search_Graph   | *maxNeighbours, startNode/startNodeName    | search_graph("link",*nr) **OR** search_graph("keyword",*nr)|
| Search_Text    | query                                      | search_text("query")                                       |


## Explore the capabilities of the Wisecube SDK and leverage the power of Wisecube AI services in your Python applications!
