# -*- coding: utf-8 -*-
"""Welcome to Zesty 2.0
"""

# Commented out IPython magic to ensure Python compatibility.
# %%capture --no-stderr
# %pip install --upgrade --quiet langchain langgraph langchain-community beautifulsoup4 langchain_openai

import getpass
import os

os.environ["OPENAI_API_KEY"] = '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'

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo")

LANGCHAIN_TRACING_V2= True
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_API_KEY="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"
LANGCHAIN_PROJECT="pr-charming-piracy-31"

from typing import Sequence

import bs4
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages
from typing_extensions import Annotated, TypedDict
from flask import Flask, request, jsonify

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


### Construct retriever ###
loader = WebBaseLoader(
    web_paths=("https://www.zestfulblends.com/",),
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(
            class_=("post-content", "post-title", "post-header")
        )
    ),
)


docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)
vectorstore = InMemoryVectorStore.from_documents(
    documents=splits, embedding=OpenAIEmbeddings()
)
retriever = vectorstore.as_retriever()


### Contextualize question ###
contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
)
contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)
history_aware_retriever = create_history_aware_retriever(
    llm, retriever, contextualize_q_prompt
)


### Answer question ###
system_prompt = (
    """You are a helpful and friendly customer service chatbot for a juice selling website and your name is Zesty.

    Your primary goal is to assist customers with their inquiries related to:

    * Our juice products (ingredients, flavors, nutritional information)
    * Ordering and delivery
    * Promotions and discounts
    * Returns and refunds
    * General questions about our company

    Always be polite and professional in your responses.

    Use the following guidelines when interacting with customers:

    * Greet the customer and introduce yourself as the juice company's chatbot assistant.
    * Ask clarifying questions to understand the customer's needs.
    * Provide accurate and concise information.
    * Offer relevant links to our website for more details.
    * If you are unable to answer a question, apologize and offer to connect the customer with a human representative.

    End the conversation by thanking the customer for their time.."""
    "\n\n"
    "{context}"
)
qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)
question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

#streaming the output 
for chunck in rag_chain.stream()

### Statefully manage chat history ###
class State(TypedDict):
    input: str
    chat_history: Annotated[Sequence[BaseMessage], add_messages]
    context: str
    answer: str


def call_model(state: State):
    response = rag_chain.invoke(state)
    return {
        "chat_history": [
            HumanMessage(state["input"]),
            AIMessage(response["answer"]),
        ],
        "context": response["context"],
        "answer": response["answer"],
    }


workflow = StateGraph(state_schema=State)
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "abc123"}}


# def handle_conversation():
#     context = ''
#     print("Type 'exit' to quit.")
#     # # print('')
#     # name= input('whats your name?   ')
#     # print(f"Hello, {name}! How can I assist you today?")
#     # background= input(f" {name}: ")

#     while True:
#       user_input = input("You:  ")

#       if user_input.lower()== "exit":
#         break

#       config = {"configurable": {"thread_id": "abc234"}}

#       # for chunk, result in app.invoke({"messages": user_input, "language": 'English'},
#       #                                   config, stream_mode="messages"):
#       #     if isinstance(chunk, AIMessage):  # Filter to just model responses
#       #         print(chunk.content, end="")

#       result = app.invoke({"input": user_input},
#                           config=config,
#                           stream_mode="values")

#       print("Zesty: ", result["answer"])

#       context += f"\nUser: {user_input}\nAI: {result}"

# if __name__ == "__main__":
#   handle_conversation()




app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('message')
    if not user_input:
        return jsonify({'error': 'Message is required'}), 400

    result = app.invoke({"input": user_input}, config=config, stream_mode="values" )
    
    return jsonify({'response': result['answer']})

if __name__ == '__main__':
    app.run(debug=True)