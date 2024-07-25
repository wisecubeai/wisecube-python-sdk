# from langchain.chat_models import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor
from langchain_core.runnables.passthrough import RunnablePassthrough
from langchain.agents.output_parsers.openai_functions import OpenAIFunctionsAgentOutputParser
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain.agents.format_scratchpad.openai_functions import format_to_openai_functions
from langchain_core.prompts.chat import MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_postgres import PostgresChatMessageHistory
import psycopg

from tools import (
    generic_search,
    disease_biology,
    target_differentiation,
    biological_process_target,
    reverse_translational_analyses,
    summarization, disease_biology_ex,biological_process_target_treg,biological_process_target_autoimmune

)

def find_tool_in_text(tools, text):
    for tool in tools:
        if tool in text:
            return tool
    return None

def db_connection(session_id):
    db_params = "host=localhost port=5432 dbname=chat connect_timeout=10 user=user password=test"
    sync_connection = psycopg.connect(db_params)
    table_name = "chat_history"
    PostgresChatMessageHistory.create_tables(sync_connection, table_name)
    chat_history = PostgresChatMessageHistory(
        table_name,
        session_id,
        sync_connection=sync_connection
    )

    return chat_history

def create_agent(chat_history):

    tools = [generic_search,disease_biology,target_differentiation,reverse_translational_analyses,summarization,biological_process_target_treg,biological_process_target_autoimmune]

    functions = [convert_to_openai_function(f) for f in tools]
    model = ChatOpenAI(model_name="gpt-4o").bind(functions=functions)

    prompt = ChatPromptTemplate.from_messages([("system", "You are helpful but sassy assistant"),
                                               MessagesPlaceholder(variable_name="chat_history"), ("user", "{input}"),
                                               MessagesPlaceholder(variable_name="agent_scratchpad")])

    chain = RunnablePassthrough.assign(agent_scratchpad=lambda x: format_to_openai_functions(x["intermediate_steps"])
                                      ) | prompt | model | OpenAIFunctionsAgentOutputParser()

    agent_executor = AgentExecutor(agent=chain, tools=tools, verbose=True)

    agent_with_chat_history = RunnableWithMessageHistory(
        agent_executor,
        lambda session_id: chat_history,
        input_messages_key="input",
        history_messages_key="chat_history",
    )

    return agent_with_chat_history

def run_conversation(agent, session_id):
    print("How can I help you?")
    state = "WAITING_FOR_QUESTION"
    last_question = ""
    suggested_tool = None
    tool_functions = {
                    "generic_search": generic_search,
                    "biological_process_target": biological_process_target,
                    "disease_biology": disease_biology,
                    "target_differentiation": target_differentiation,
                    "reverse_translational_analyses": reverse_translational_analyses,
                    "summarization": summarization,
                    "biological_process_target_treg": biological_process_target_treg,
                    "biological_process_target_autoimmune": biological_process_target_autoimmune
                }
    chat_history = db_connection(session_id)
    while True:
        user_input = input("User: ").strip().lower()
        chat_history.add_user_message(user_input)
        if state == "WAITING_FOR_QUESTION":
            last_question = user_input
            # context_response = agent.invoke({
            #                                     "input": f"Extract keywords and reformulate the following question: '{user_input}' to identify the appropriate tool based on tool keywords. Analyze the following reformulated question and suggest the appropriate tool key to use in quotation marks."},
            #                                 config={"configurable": {"session_id": session_id}})

            # print(context_response)
            reformulation_response = agent.invoke({
                "input": f"Extract keywords from input and reformulate the following question: '{last_question}' to identify the appropriate tool based on tool keywords."},
                config={"configurable": {"session_id": session_id}})
            reformulated_question = reformulation_response['output']
            chat_history.add_ai_message(reformulated_question)
            # print(f"Reformulated question: '{reformulated_question}'")
            confirmation = input("Is this what you asked? (yes/no): ").strip().lower()
            chat_history.add_user_message(confirmation)
            if confirmation == "yes":
                # context_response = agent.invoke({
                #     "input": f"Analyze the following reformulated question: '{reformulated_question}' and suggest the appropriate tool key to use in quotation marks."},
                #     config = {"configurable": {"session_id": session_id}})
                tools_list = [
                    "generic_search",
                    "biological_process_target",
                    "disease_biology",
                    "target_differentiation",
                    "reverse_translational_analyses",
                    "summarization"
                ]
                suggested_tool = find_tool_in_text(tools_list, reformulated_question)
                print(suggested_tool)
                if not suggested_tool:
                    print("Please ask a more specific question so I can find the tool.")
                    continue
                print(f"Do you want to run the suggested tool: '{suggested_tool}'? (yes/no)")
                state = "WAITING_FOR_TOOL_ACTION"
            elif confirmation == "no":
                print("Please rephrase your question.")
                continue
            else:
                print("Please answer with 'yes' or 'no'.")
            # match = re.search(r'"([a-zA-Z0-9_]+)"', context_response['output'])
            # if match:
            #     suggested_tool = match.group(1)
            # if not suggested_tool or suggested_tool not in tool_functions:
            #     print("Please ask a more specific question so I can find the tool.")
            #     continue

            # print(f"Do you want to run the suggested tool: '{suggested_tool}' ? (yes/no)")
            # state = "WAITING_FOR_TOOL_ACTION"

        elif state == "WAITING_FOR_TOOL_ACTION":
            if "yes" in user_input.lower():
                if suggested_tool == "disease_biology":
                    print(
                        "Which branches would you like to run for 'disease_biology'? Options are: etiology, pathology, genetics. Type 'all' for all branches.")
                    branch_choice = input("Your choice: ").strip().lower()
                    chat_history.add_user_message(branch_choice)

                    if branch_choice == 'all':
                        response = disease_biology_ex(last_question, query_type='all')
                        print("Response:", response)
                        chat_history.add_ai_message(response)
                    elif branch_choice in ['etiology', 'pathology', 'genetics']:
                        response = disease_biology_ex(last_question, query_type=branch_choice)
                        print("Response:", response)
                        chat_history.add_ai_message(response)
                    elif ',' in branch_choice:
                        response = disease_biology_ex(last_question, query_type=branch_choice)
                        print("Response:", response)
                        chat_history.add_ai_message(response)
                    else:
                        print("Invalid choice. Please choose from the specified branches or 'all'.")
                        continue
                elif suggested_tool == "biological_process_target":
                    print(
                        "Which steps would you like to run for 'biological_process_target'? Options are: treg, autoimmune, score. Type 'all' for all steps.")
                    step_choice = input("Your choice: ").strip().lower()
                    chat_history.add_user_message(step_choice)
                    if step_choice == 'all':
                        step_choice = "treg,autoimmune,score"

                    response = biological_process_target(step_choice)
                    print("Response:", response)
                    chat_history.add_ai_message(response)

                else:
                    response = tool_functions.get(suggested_tool, lambda x: "Invalid tool")(last_question)
                    print("Response:", response)
                    chat_history.add_ai_message(response)
                print("Would you like to run another tool for the same question? (yes/no)")
                state = "WAITING_FOR_ANOTHER_TOOL_ACTION"
            elif "no" in user_input.lower():
                print("Please specify which tool you would like to use: " + ', '.join(list(tool_functions.keys())))
                state = "WAITING_FOR_TOOL_SELECTION"
            else:
                print("Please answer with 'yes' or 'no'.")

        elif state == "WAITING_FOR_TOOL_SELECTION":
            if user_input.lower() in tool_functions:
                if user_input.lower() == "disease_biology":
                    print(
                        "Which branches would you like to run for 'disease_biology'? Options are: etiology, pathology, genetics. Type 'all' for all branches.")
                    branch_choice = input("Your choice: ").strip().lower()
                    chat_history.add_user_message(branch_choice)

                    if branch_choice == 'all':
                        response = disease_biology_ex(last_question, query_type='all')
                        print("Response:", response)
                        chat_history.add_ai_message(response)
                    elif branch_choice in ['etiology', 'pathology', 'genetics']:
                        response = disease_biology_ex(last_question, query_type=branch_choice)
                        print("Response:", response)
                        chat_history.add_ai_message(response)
                    elif ',' in branch_choice:
                        response = disease_biology_ex(last_question, query_type=branch_choice)
                        print("Response:", response)
                        chat_history.add_ai_message(response)

                    else:
                        print("Invalid choice. Please choose from the specified branches or 'all'.")
                        continue

                elif user_input.lower() == "biological_process_target":
                    print(
                        "Which steps would you like to run for 'biological_process_target'? Options are: treg, autoimmune, score. Type 'all' for all steps.")
                    step_choice = input("Your choice: ").strip().lower()
                    chat_history.add_user_message(step_choice)
                    if step_choice == 'all':
                        step_choice = "treg,autoimmune,score"

                    response = biological_process_target(step_choice)
                    print("Response:", response)
                    chat_history.add_ai_message(response)
                else:
                    response = tool_functions[user_input.lower()](last_question)
                    print("Response:", response)
                    chat_history.add_ai_message(response)
            else:
                print("Invalid tool specified. Please specify a valid tool.")
                continue
            state = "WAITING_FOR_ANOTHER_TOOL_ACTION"
            print("Would you like to run another tool for the same question? (yes/no)")

        elif state == "WAITING_FOR_ANOTHER_TOOL_ACTION":
            if "yes" in user_input.lower():
                print("Please specify which tool you would like to use: " + ', '.join(list(tool_functions.keys())))
                state = "WAITING_FOR_TOOL_SELECTION"
            elif "no" in user_input.lower():
                print("Is the conversation complete? (yes/no)")
                state = "WAITING_FOR_CONVERSATION_END_CONFIRMATION"
            else:
                print("Please answer with 'yes' or 'no'.")

        elif state == "WAITING_FOR_CONVERSATION_END_CONFIRMATION":
            if "yes" in user_input.lower():
                print("Thank you.Have a great day!")
                break
            elif "no" in user_input.lower():
                state = "WAITING_FOR_QUESTION"
                print("How else can I assist you?")
            else:
                print("Please answer with 'yes' or 'no'.")


# def run_conversation2(agent, session_id):
#     print("How can I help you?")
#     user_input = input("User: ").strip().lower()
#     agent.invoke({
#         "input": f"Extract keywords from input and reformulate the following question: '{user_input}' to identify the appropriate tool."
#                  f"Think very carefully about how you will help the user accomplish their goal. Explain what steps should be used."},
#         config={"configurable": {"session_id": session_id}})
#

# specific_uuid_str = "123e4567-e89b-12d3-a456-426614174000"
# session_id = "d5c5e67f-f1b2-44b1-8b69-ec5c62cf60e5"
# session_id = "f47ac10b-58cc-4372-a567-0e02b2c3d79a"
session_id ="8f0d5e8a-1d57-4c6a-9b20-dc2d6f3e8d3a"
# session_id = "b9a4e3e9-92d1-4d9e-bdf2-c6f684b4e8e2"
# session_id = "123e4567-e89b-12d3-a456-426614174000"
# session_id = "550e8400-e29b-41d4-a716-446655440000"

chat_history = db_connection(session_id)
# print(chat_history.messages)
agent_with_chat_history = create_agent(chat_history)
run_conversation(agent_with_chat_history, session_id)

