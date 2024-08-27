from langchain.agents import Tool
from langchain_core.tools import StructuredTool, tool
from tabulate import tabulate
import numpy as np
import pandas as pd
from openai import OpenAI
import os
from wisecube_sdk.client import WisecubeClient
from wisecube_sdk.model_formats import OutputFormat


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
wisecube_api_key = os.getenv("API_KEY")

gpt_client = OpenAI(api_key=OPENAI_API_KEY)
client = WisecubeClient(wisecube_api_key).client
# client.output_format = OutputFormat.JSON


@tool
def generic_search(query):
    """Call this tool for default search."""
    try:
        client.output_format = OutputFormat.PANDAS
        print("\n")
        print("Calling nl_to_sparql for the question")
        response_sparql = client.nl_to_sparql(query)
        print(response_sparql)
        response = client.advance_search(response_sparql)
        print("\n")
        print("Response for advance_search based on sparql query")
        return response
    except Exception as e:
        return None

# def biological_process_target(question):
#     try:
#         print("\n")
#         print("Combine data for given proteins, and collect embeddings and preferred labels from graph")
#         client.output_format = OutputFormat.PANDAS
#
#         treg_data = client.advance_search("""
#     SELECT DISTINCT ?gene ?geneLabel ?target ?targetLabel ?process ?processLabel ?drug ?drugLabel ?cancer ?cancerLabel ?role ?roleLabel
#     WHERE {
#       ?target wdt:P682 ?process .       # target is involved in biological process
#       ?process wdt:P279+ wd:Q14865404 . # biological process is a kind of regulation of T cell activation
#       ?gene wdt:P688 ?target .          # the gene that encodes the target
#       ?drug wdt:P129 ?target .          # the drug that physically interacts with the target
#       ?drug wdt:P2175 ?cancer .         # the drug is used to treat a cancer
#       ?cancer (wdt:P279*)|(wdt:P31/wdt:P279*) wd:Q12078 .
#       OPTIONAL {
#         ?drug p:P129 ?st .
#         ?st ps:P129 ?target .
#         ?st pq:P2868 ?role .
#         ?role rdfs:label ?roleLabel . FILTER(LANG(?roleLabel)="en")
#       }
#       ?target rdfs:label ?targetLabel. FILTER(LANG(?targetLabel)="en")
#       ?process rdfs:label ?processLabel. FILTER(LANG(?processLabel)="en")
#       ?gene rdfs:label ?geneLabel. FILTER(LANG(?geneLabel)="en")
#       ?drug rdfs:label ?drugLabel. FILTER(LANG(?drugLabel)="en")
#       ?cancer rdfs:label ?cancerLabel. FILTER(LANG(?cancerLabel)="en")
#     }
#     """)
#
#         treg_data["qid"] = treg_data["target"].str.split("/").str[-1]
#         treg_data["emb"] = treg_data["qid"].apply(client.execute_vector_function)
#         treg_data["emb"] = treg_data["emb"].apply(lambda emb: emb.values.squeeze())
#
#         treg_data_display = treg_data.copy()
#         treg_data_display["emb"] = treg_data_display["emb"].apply(lambda emb: str(emb)[:20] + '...' if len(str(emb)) > 20 else str(emb))
#         print(tabulate(treg_data_display.head(10), headers='keys', tablefmt='pretty'))
#
#         print("\n")
#         print("Get autoimmune targets from the graph")
#
#         autoimmune_data = client.advance_search("""
#         SELECT DISTINCT ?drug ?drugLabel ?disease ?diseaseLabel ?target ?targetLabel ?gene ?geneLabel ?role ?roleLabel
#         WHERE {
#           ?drug wdt:P2175 ?disease .
#           ?disease (wdt:P31/wdt:P279*)|(wdt:P279*) wd:Q8084905 .
#           ?drug wdt:P129 ?target .
#           OPTIONAL {
#             ?drug p:P129 ?st .
#             ?st ps:P129 ?target .
#             ?st pq:P2868 ?role .
#             ?role rdfs:label ?roleLabel . FILTER(LANG(?roleLabel)="en")
#           }
#           ?target wdt:P702 ?gene .
#           ?drug rdfs:label ?drugLabel . FILTER(LANG(?drugLabel)="en")
#           ?disease rdfs:label ?diseaseLabel . FILTER(LANG(?diseaseLabel)="en")
#           ?target rdfs:label ?targetLabel . FILTER(LANG(?targetLabel)="en")
#           ?gene rdfs:label ?geneLabel . FILTER(LANG(?geneLabel)="en")
#         }
#         ORDER BY (?geneLabel)
#         """)
#
#         print("\n")
#         print("Collect embeddings for the autoimmune targets")
#         autoimmune_data["qid"] = autoimmune_data["target"].str.split("/").str[-1]
#         autoimmune_data["emb"] = autoimmune_data["qid"].apply(client.execute_vector_function)
#         autoimmune_data["emb"] = autoimmune_data["emb"].apply(lambda emb: emb.values.squeeze())
#
#         autoimmune_data_display = autoimmune_data.copy()
#         autoimmune_data_display["emb"] = autoimmune_data["emb"].apply(lambda emb: str(emb)[:20] + '...' if len(str(emb)) > 20 else str(emb))
#         print(tabulate(autoimmune_data_display.head(10), headers='keys', tablefmt='pretty'))
#
#
#
#         print("\n")
#         print("Now that we have both kinds of targets, we can score the Treg targetst by how close they are to autoimmune targets using the embeddings")
#         treg_X = treg_data[["qid", "emb"]].rename({"qid": "treg_qid"}, axis=1).groupby("treg_qid").agg("first")["emb"]
#         ai_X = autoimmune_data[["qid", "emb"]].rename({"qid": "ai_qid"}, axis=1).groupby("ai_qid").agg("first")["emb"]
#
#         cross = pd.DataFrame(index=treg_X.index, columns=ai_X.index)
#         for treg_qid, u in treg_X.items():
#           for ai_qid, v in ai_X.items():
#             cross.at[treg_qid, ai_qid] = np.dot(u, v)/(np.linalg.norm(u)*np.linalg.norm(v))
#         cross = cross.drop_duplicates()
#
#         scoring = pd.DataFrame({
#             "mean": cross.mean(axis=1),
#             "median": cross.quantile(axis=1, numeric_only=False),
#             "max": cross.max(axis=1),
#             "idxmax": cross.apply(lambda r: cross.columns[np.argmax(r)], axis=1),
#         })
#
#         scoring = pd.merge(scoring, treg_data[["qid", "targetLabel"]].set_index("qid").drop_duplicates(), left_index=True, right_index=True)
#         ai_joind_data = autoimmune_data[["targetLabel", "geneLabel", "diseaseLabel", "drugLabel", "roleLabel", "qid"]].rename({"targetLabel": "autoimmuneTargetLabel"}, axis=1)
#         ai_joind_data = ai_joind_data.drop_duplicates().groupby("qid").first()
#         scoring = pd.merge(scoring, ai_joind_data.rename({c: c+"_max" for c in ai_joind_data.columns}, axis=1), left_on="idxmax", right_index=True)
#         scoring = scoring.reset_index(drop=False).sort_values("max", ascending=False)
#         print("\n")
#         print("Now let's aggregate these scores. Let's look at the max cosine similarity score, and the mean cosine similarity score")
#         print("\n")
#         return tabulate(scoring, headers='keys', tablefmt='fancy_grid')
#     except Exception as e:
#         print(f"Error in calculate_similarity: {e}")
#         return None


def get_treg_data(client):
    try:
        print("Combine data for given proteins, and collect embeddings and preferred labels from graph")

        treg_data = client.advance_search("""
    SELECT DISTINCT ?gene ?geneLabel ?target ?targetLabel ?process ?processLabel ?drug ?drugLabel ?cancer ?cancerLabel ?role ?roleLabel
    WHERE {
      ?target wdt:P682 ?process .       # target is involved in biological process
      ?process wdt:P279+ wd:Q14865404 . # biological process is a kind of regulation of T cell activation
      ?gene wdt:P688 ?target .          # the gene that encodes the target
      ?drug wdt:P129 ?target .          # the drug that physically interacts with the target
      ?drug wdt:P2175 ?cancer .         # the drug is used to treat a cancer
      ?cancer (wdt:P279*)|(wdt:P31/wdt:P279*) wd:Q12078 .
      OPTIONAL {
        ?drug p:P129 ?st .
        ?st ps:P129 ?target .
        ?st pq:P2868 ?role .
        ?role rdfs:label ?roleLabel . FILTER(LANG(?roleLabel)="en")
      }
      ?target rdfs:label ?targetLabel. FILTER(LANG(?targetLabel)="en")
      ?process rdfs:label ?processLabel. FILTER(LANG(?processLabel)="en")
      ?gene rdfs:label ?geneLabel. FILTER(LANG(?geneLabel)="en")
      ?drug rdfs:label ?drugLabel. FILTER(LANG(?drugLabel)="en")
      ?cancer rdfs:label ?cancerLabel. FILTER(LANG(?cancerLabel)="en")
    }
    """)
        print(treg_data)
        treg_data["qid"] = treg_data["target"].str.split("/").str[-1]
        treg_data["emb"] = treg_data["qid"].apply(client.execute_vector_function)
        treg_data["emb"] = treg_data["emb"].apply(lambda emb: emb.values.squeeze())

        treg_data_display = treg_data.copy()
        treg_data_display["emb"] = treg_data_display["emb"].apply(
            lambda emb: str(emb)[:20] + '...' if len(str(emb)) > 20 else str(emb))
        # print(tabulate(treg_data_display.head(10), headers='keys', tablefmt='pretty'))
        # print(treg_data_display)
        return treg_data_display
    except Exception as e:
        print(f"Error in get_treg_data: {e}")
        return None


def get_autoimmune_data(client):
    try:
        print("Get autoimmune targets from the graph")

        autoimmune_data = client.advance_search("""
        SELECT DISTINCT ?drug ?drugLabel ?disease ?diseaseLabel ?target ?targetLabel ?gene ?geneLabel ?role ?roleLabel
        WHERE {
          ?drug wdt:P2175 ?disease .
          ?disease (wdt:P31/wdt:P279*)|(wdt:P279*) wd:Q8084905 .
          ?drug wdt:P129 ?target .
          OPTIONAL {
            ?drug p:P129 ?st .
            ?st ps:P129 ?target .
            ?st pq:P2868 ?role .
            ?role rdfs:label ?roleLabel . FILTER(LANG(?roleLabel)="en")
          }
          ?target wdt:P702 ?gene .
          ?drug rdfs:label ?drugLabel . FILTER(LANG(?drugLabel)="en")
          ?disease rdfs:label ?diseaseLabel . FILTER(LANG(?diseaseLabel)="en")
          ?target rdfs:label ?targetLabel . FILTER(LANG(?targetLabel)="en")
          ?gene rdfs:label ?geneLabel . FILTER(LANG(?geneLabel)="en")
        }
        ORDER BY (?geneLabel)
        """)

        print("Collect embeddings for the autoimmune targets")
        autoimmune_data["qid"] = autoimmune_data["target"].str.split("/").str[-1]
        autoimmune_data["emb"] = autoimmune_data["qid"].apply(client.execute_vector_function)
        autoimmune_data["emb"] = autoimmune_data["emb"].apply(lambda emb: emb.values.squeeze())

        autoimmune_data_display = autoimmune_data.copy()
        autoimmune_data_display["emb"] = autoimmune_data_display["emb"].apply(
            lambda emb: str(emb)[:20] + '...' if len(str(emb)) > 20 else str(emb))
        # print(tabulate(autoimmune_data_display.head(10), headers='keys', tablefmt='pretty'))

        return autoimmune_data_display
    except Exception as e:
        print(f"Error in get_autoimmune_data: {e}")
        return None


def calculate_similarity(treg_data, autoimmune_data):
    try:
        print(
            "Now that we have both kinds of targets, we can score the Treg targetst by how close they are to autoimmune targets using the embeddings")
        treg_X = treg_data[["qid", "emb"]].rename({"qid": "treg_qid"}, axis=1).groupby("treg_qid").agg("first")["emb"]
        ai_X = autoimmune_data[["qid", "emb"]].rename({"qid": "ai_qid"}, axis=1).groupby("ai_qid").agg("first")["emb"]

        cross = pd.DataFrame(index=treg_X.index, columns=ai_X.index)
        for treg_qid, u in treg_X.items():
            for ai_qid, v in ai_X.items():
                cross.at[treg_qid, ai_qid] = np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))
        cross = cross.drop_duplicates()

        scoring = pd.DataFrame({
            "mean": cross.mean(axis=1),
            "median": cross.quantile(axis=1, numeric_only=False),
            "max": cross.max(axis=1),
            "idxmax": cross.apply(lambda r: cross.columns[np.argmax(r)], axis=1),
        })

        scoring = pd.merge(scoring, treg_data[["qid", "targetLabel"]].set_index("qid").drop_duplicates(),
                           left_index=True, right_index=True)
        ai_joind_data = autoimmune_data[
            ["targetLabel", "geneLabel", "diseaseLabel", "drugLabel", "roleLabel", "qid"]].rename(
            {"targetLabel": "autoimmuneTargetLabel"}, axis=1)
        ai_joind_data = ai_joind_data.drop_duplicates().groupby("qid").first()
        scoring = pd.merge(scoring, ai_joind_data.rename({c: c + "_max" for c in ai_joind_data.columns}, axis=1),
                           left_on="idxmax", right_index=True)
        scoring = scoring.reset_index(drop=False).sort_values("max", ascending=False)

        print(
            "Now let's aggregate these scores. Let's look at the max cosine similarity score, and the mean cosine similarity score")
        return scoring
    except Exception as e:
        print(f"Error in calculate_similarity: {e}")
        return None


@tool
def biological_process_target(steps="treg,autoimmune,score"):
    """Call this tool for biological process search, it does have a semantic relation to any of these concepts: TNFR2, autoimmune, cancer, T cell activation, target."""
    try:
        steps = [step.strip() for step in steps.split(",")]
        client.output_format = OutputFormat.JSON
        treg_data = None
        autoimmune_data = None
        results = []

        if "treg" in steps:
            treg_data = get_treg_data(client)
            df = pd.json_normalize(treg_data)
            # print(tabulate(treg_data.head(10), headers='keys', tablefmt='pretty'))
            results.append(tabulate(df.head(10), headers='keys', tablefmt='pretty'))

        if "autoimmune" in steps:
            autoimmune_data = get_autoimmune_data(client)
            df2 = pd.json_normalize(autoimmune_data)
            results.append(tabulate(df2.head(10), headers='keys', tablefmt='pretty'))

        if "score" in steps:
            if treg_data is None:
                treg_data = get_treg_data(client)
            if autoimmune_data is None:
                autoimmune_data = get_autoimmune_data(client)
            scoring = calculate_similarity(treg_data, autoimmune_data)
            print(tabulate(scoring.head(10), headers='keys', tablefmt='fancy_grid'))
            results.append(scoring)

        return results

    except Exception as e:
        print(f"Error in biological_process_target: {e}")
        return None

@tool
def query_retrieval_tool():
    """
    Tool for biological process search, it does have a semantic relation to any of these concepts: TNFR2, autoimmune, cancer, T cell activation, target.
    :return: table with data for given proteins, collect embeddings and preferred labels from graph
    """

    def get_treg_data(question: str) -> str:
        print("Combine data for given proteins, and collect embeddings and preferred labels from graph")
        treg_data = client.advance_search("""
            SELECT DISTINCT ?gene ?geneLabel ?target ?targetLabel ?process ?processLabel ?drug ?drugLabel ?cancer ?cancerLabel ?role ?roleLabel
            WHERE {
              ?target wdt:P682 ?process .       # target is involved in biological process
              ?process wdt:P279+ wd:Q14865404 . # biological process is a kind of regulation of T cell activation
              ?gene wdt:P688 ?target .          # the gene that encodes the target
              ?drug wdt:P129 ?target .          # the drug that physically interacts with the target
              ?drug wdt:P2175 ?cancer .         # the drug is used to treat a cancer
              ?cancer (wdt:P279*)|(wdt:P31/wdt:P279*) wd:Q12078 .
              OPTIONAL {
                ?drug p:P129 ?st .
                ?st ps:P129 ?target .
                ?st pq:P2868 ?role .
                ?role rdfs:label ?roleLabel . FILTER(LANG(?roleLabel)="en")
              }
              ?target rdfs:label ?targetLabel. FILTER(LANG(?targetLabel)="en")
              ?process rdfs:label ?processLabel. FILTER(LANG(?processLabel)="en")
              ?gene rdfs:label ?geneLabel. FILTER(LANG(?geneLabel)="en")
              ?drug rdfs:label ?drugLabel. FILTER(LANG(?drugLabel)="en")
              ?cancer rdfs:label ?cancerLabel. FILTER(LANG(?cancerLabel)="en")
            }
            """)

        treg_data["qid"] = treg_data["target"].str.split("/").str[-1]
        treg_data["emb"] = treg_data["qid"].apply(client.execute_vector_function)
        treg_data["emb"] = treg_data["emb"].apply(lambda emb: emb.values.squeeze())

        treg_data_display = treg_data.copy()
        treg_data_display["emb"] = treg_data_display["emb"].apply(
            lambda emb: str(emb)[:20] + '...' if len(str(emb)) > 20 else str(emb))
        # print(tabulate(treg_data_display.head(10), headers='keys', tablefmt='pretty'))
        # print(treg_data_display)
        return treg_data_display

    def get_autoimmune_data(question: str) -> str:
        print("Get autoimmune targets from the graph")

        autoimmune_data = client.advance_search("""
        SELECT DISTINCT ?drug ?drugLabel ?disease ?diseaseLabel ?target ?targetLabel ?gene ?geneLabel ?role ?roleLabel
        WHERE {
          ?drug wdt:P2175 ?disease .
          ?disease (wdt:P31/wdt:P279*)|(wdt:P279*) wd:Q8084905 .
          ?drug wdt:P129 ?target .
          OPTIONAL {
            ?drug p:P129 ?st .
            ?st ps:P129 ?target .
            ?st pq:P2868 ?role .
            ?role rdfs:label ?roleLabel . FILTER(LANG(?roleLabel)="en")
          }
          ?target wdt:P702 ?gene .
          ?drug rdfs:label ?drugLabel . FILTER(LANG(?drugLabel)="en")
          ?disease rdfs:label ?diseaseLabel . FILTER(LANG(?diseaseLabel)="en")
          ?target rdfs:label ?targetLabel . FILTER(LANG(?targetLabel)="en")
          ?gene rdfs:label ?geneLabel . FILTER(LANG(?geneLabel)="en")
        }
        ORDER BY (?geneLabel)
        """)

        print("Collect embeddings for the autoimmune targets")
        autoimmune_data["qid"] = autoimmune_data["target"].str.split("/").str[-1]
        autoimmune_data["emb"] = autoimmune_data["qid"].apply(client.execute_vector_function)
        autoimmune_data["emb"] = autoimmune_data["emb"].apply(lambda emb: emb.values.squeeze())

        autoimmune_data_display = autoimmune_data.copy()
        autoimmune_data_display["emb"] = autoimmune_data_display["emb"].apply(
            lambda emb: str(emb)[:20] + '...' if len(str(emb)) > 20 else str(emb))
        # print(tabulate(autoimmune_data_display.head(10), headers='keys', tablefmt='pretty'))

        return autoimmune_data_display

    treg_tool = StructuredTool.from_function(func=get_treg_data,
                                             name='treg_data',
                                             description='This function focuses specifically on T cell regulation processes. It is ideal when you need detailed information on how targets influence T cell activation, which is crucial in contexts like cancer therapy and immune regulation.')
    autoimmune_tool = StructuredTool.from_function(func=get_autoimmune_data,
                                             name='autoimmune_data',
                                             description='This function is dedicated to autoimmune diseases, providing data on how targets and drugs are involved in autoimmune conditions. It’s suitable for questions about how different treatments and targets interact with autoimmune diseases.')

    return treg_tool,autoimmune_tool

def chat_gpt(question):
    prompt = f"""
        Given the following scientific question, extract only the disease terms!

        Question:
        "{question}"

        The response will be return as text separated by |:
        """
    response = gpt_client.chat.completions.create(model="gpt-4o",
    messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content.strip()

def search_qids(question):
    list_of_words = chat_gpt(question).split("|")

    qids = []
    for word in list_of_words:
        search_text = client.search_text(word)
        try:
            qid = search_text["data"]["searchAsYouType"]["data"]["searchLabels"][0]["qid"]
            qids.append(qid)
        except Exception as e:
            print(e)

    return qids


# def disease_biology(question):
#   client.output_format = OutputFormat.JSON
#   search = search_qids(question)
#   first_qid = search[0].split("/")[-1]
#
#   biological_query = client.advance_search(f"""
#   SELECT ?subject ?subjectLabel ?property WHERE {{
#     wd:{first_qid} ?property ?subject .
#     OPTIONAL {{
#       ?subject rdfs:label ?subjectLabel. FILTER(LANG(?subjectLabel)="en")
#     }}
#   }}
#   """)
#   results = biological_query.get('data', {}).get('advancedSearchGraph', {}).get('results', {}).get('bindings', [])
#   df = pd.json_normalize(results)
#   return tabulate(df.head(10), headers='keys', tablefmt='pretty')
#
# def disease_biology_ex(question, query_type):
#     client.output_format = OutputFormat.JSON
#
#     search = search_qids(question)
#     first_qid = search[0].split("/")[-1]
#
#     queries = {
#         'default': f"""
#             SELECT ?subject ?subjectLabel ?property WHERE {{
#                 wd:{first_qid} ?property ?subject .
#                 OPTIONAL {{
#                     ?subject rdfs:label ?subjectLabel. FILTER(LANG(?subjectLabel)="en")
#                 }}
#             }}
#         """,
#         'extended': f"""
#             SELECT ?subject ?subjectLabel ?property WHERE {{
#                 wd:{first_qid} ?property ?subject .
#                 OPTIONAL {{
#                     ?subject rdfs:label ?subjectLabel. FILTER(LANG(?subjectLabel)="en")
#                 }}
#             }}
#         """
#     }
#
#     if query_type == 'all':
#         results_summary = []
#
#         for key in queries:
#             query = queries[key]
#             biological_query = client.advance_search(query)
#             results = biological_query.get('data', {}).get('advancedSearchGraph', {}).get('results', {}).get('bindings', [])
#             df = pd.json_normalize(results)
#             results_summary.append(
#                     f"Results for '{key}':\n{tabulate(df, headers='keys', tablefmt='pretty')}\n"
#                 )
#         return "\n".join(results_summary)
#     elif query_type in queries:
#         query = queries[query_type]
#         # print(query)
#         biological_query = client.advance_search(query)
#         results = biological_query.get('data', {}).get('advancedSearchGraph', {}).get('results', {}).get('bindings', [])
#         df = pd.json_normalize(results)
#         return tabulate(df.head(10), headers='keys', tablefmt='pretty')
#
#     else:
#         return "Invalid query type specified."


def disease_biology_ex(question, query_type):
    """Tool for analyzing and interpreting the biological mechanisms of diseases. It integrates genomic, proteomic, and clinical data to identify molecular and cellular factors involved in disease pathogenesis. It helps discover new therapeutic targets and understand the biological processes essential for disease development and progression.
        Keywords: etiology, biology, models of IBD, pathology, pathways, cytokines, genetics, comorbidity, differential expression, co-expression, animal models."""
    client.output_format = OutputFormat.JSON

    search = search_qids(question)
    first_qid = search[0].split("/")[-1]

    queries = {
        'etiology': f"""
            SELECT ?subject ?subjectLabel ?property WHERE {{
                wd:{first_qid} ?property ?subject .
                OPTIONAL {{
                    ?subject rdfs:label ?subjectLabel. FILTER(LANG(?subjectLabel)="en")
                }}
            }}
        """,
        'pathology': f"""
            SELECT ?subject ?subjectLabel ?property WHERE {{
                wd:{first_qid} ?property ?subject .
                OPTIONAL {{
                    ?subject rdfs:label ?subjectLabel. FILTER(LANG(?subjectLabel)="en")
                }}
            }}
        """,
        'genetics': f"""
                SELECT ?subject ?subjectLabel ?property WHERE {{
                    wd:{first_qid} ?property ?subject .
                    OPTIONAL {{
                        ?subject rdfs:label ?subjectLabel. FILTER(LANG(?subjectLabel)="en")
                    }}
                }}
            """
    }
    results_summary = []
    query_types_list = [qt.strip() for qt in query_type.split(',')]

    if 'all' in query_types_list:
        for key in queries:
            query = queries[key]
            biological_query = client.advance_search(query)
            results = biological_query.get('data', {}).get('advancedSearchGraph', {}).get('results', {}).get('bindings',
                                                                                                             [])
            df = pd.json_normalize(results)
            results_summary.append(
                f"Results for '{key}':\n{tabulate(df.head(10), headers='keys', tablefmt='pretty')}\n")
    else:
        for query_type in query_types_list:
            if query_type in queries:
                query = queries[query_type]
                biological_query = client.advance_search(query)
                results = biological_query.get('data', {}).get('advancedSearchGraph', {}).get('results', {}).get(
                    'bindings', [])
                df = pd.json_normalize(results)
                results_summary.append(
                    f"Results for '{query_type}':\n{tabulate(df.head(10), headers='keys', tablefmt='pretty')}\n")
            else:
                results_summary.append(f"Invalid query type specified: {query_type}")

    return "\n".join(results_summary)


@tool
def target_differentiation(question):
    """Tool for distinguishing and characterizing potential therapeutic targets. It evaluates molecular targets based on their relevance to specific diseases, mechanisms of action, and potential for selective therapeutic intervention. This agent aids in prioritizing targets for drug development and personalized medicine approaches."""
    return question

@tool
def reverse_translational_analyses(question):
    """Tool for conducting reverse translational analyses, which involves translating clinical observations back into basic research. It identifies clinical insights that can inform experimental studies, aiming to bridge the gap between clinical findings and laboratory research to uncover underlying mechanisms and potential new treatments."""
    return "reverse_translational_analyses method run"

@tool
def summarization(question):
    """Tool for summarizing complex scientific and medical texts. It extracts key information and presents it in a concise, easy-to-understand format. This agent is useful for quickly understanding large volumes of research literature, reports, and data, providing clear and actionable insights."""
    return "summarization method run"



# query_predifined=Tool(
#     name="query",
#     func=query_retrieval_tool,
#     description="Tool for biological process search, it does have a semantic relation to any of these concepts: TNFR2, autoimmune, cancer, T cell activation, target."
# )

disease_biology = Tool(
    name="disease_biology",
    func=disease_biology_ex,
    description="Tool for analyzing and interpreting the biological mechanisms of diseases. It integrates genomic, proteomic, and clinical data to identify molecular and cellular factors involved in disease pathogenesis. It helps discover new therapeutic targets and understand the biological processes essential for disease development and progression."
                "Keywords: etiology, biology, models of IBD, pathology, pathways, cytokines, genetics, comorbidity, differential expression, co-expression, animal models."
)
#
# biological_process_target = Tool(
#     name="biological_process_target",
#     func=biological_process_target,
#     description="Tool for biological process search, it does have a semantic relation to any of these concepts: TNFR2, autoimmune, cancer, T cell activation, target."
# )
#
# biological_process_target_treg = Tool(
#     name="biological_process_target_treg",
#     func=get_treg_data,
#     description="This tool focuses specifically on T cell regulation processes. It is ideal when you need detailed information on how targets influence T cell activation, which is crucial in contexts like cancer therapy and immune regulation."
# )
# biological_process_target_autoimmune = Tool(
#     name="biological_process_target_autoimmune",
#     func=get_autoimmune_data,
#     description="This tool is dedicated to autoimmune diseases, providing data on how targets and drugs are involved in autoimmune conditions. It’s suitable for questions about how different treatments and targets interact with autoimmune diseases."
# )

# target_differentiation = Tool(
#     name="target_differentiation",
#     func=target_differentiation,
#     description="Tool for distinguishing and characterizing potential therapeutic targets. It evaluates molecular targets based on their relevance to specific diseases, mechanisms of action, and potential for selective therapeutic intervention. This agent aids in prioritizing targets for drug development and personalized medicine approaches."
# )
# reverse_translational_analyses = Tool(
#     name="reverse_translational_analyses",
#     func=reverse_translational_analyses,
#     description="Tool for conducting reverse translational analyses, which involves translating clinical observations back into basic research. It identifies clinical insights that can inform experimental studies, aiming to bridge the gap between clinical findings and laboratory research to uncover underlying mechanisms and potential new treatments."
# )
# summarization = Tool(
#     name="summarization",
#     func=summarization,
#     description="Tool for summarizing complex scientific and medical texts. It extracts key information and presents it in a concise, easy-to-understand format. This agent is useful for quickly understanding large volumes of research literature, reports, and data, providing clear and actionable insights."
# )

