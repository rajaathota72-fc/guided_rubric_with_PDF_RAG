# retrieve_embeddings.py
from pymongo import MongoClient
from langchain_openai import OpenAIEmbeddings
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableSequence
from langchain_core.output_parsers import StrOutputParser
from langchain_community.callbacks.manager import get_openai_callback
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load environment variables
openai_api_key = os.environ['OPENAI_API_KEY']
client = MongoClient(os.environ["MONGODB_URI"])
db = client[os.environ["DATABASE_NAME"]]
collection = db[os.environ["COLLECTION_NAME"]]

ATLAS_VECTOR_SEARCH_INDEX_NAME = "vector_index"

# Ensure the vector store is correctly initialized
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key, disallowed_special=())
vector_search = MongoDBAtlasVectorSearch(
    collection=collection,
    index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
    embedding=embeddings
)

retriever = vector_search.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 1}
)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def retrieve_and_generate_response(question, template_text):
    prompt = PromptTemplate.from_template(template=template_text)
    output_parser = StrOutputParser()
    model = ChatOpenAI(api_key=openai_api_key, model_name='gpt-3.5-turbo', temperature=0)

    retrieval_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | model
            | output_parser
    )

    with get_openai_callback() as cb_rag:
        rag_response = retrieval_chain.invoke(question)
        rag_cost = cb_rag.total_cost

    return rag_response, rag_cost

template_text = """You are a helpful tutor that is guiding a university student through a critical appraisal of a scholarly journal article. You want to encourage the students ideas, but you also want those idea to be rooted in evidence from the journal article that you'll fetch via retrieval.Provide helpful feedback for the following question. If the student has not answered the question accurately, then do not provide the correct answer for the student. Instead, use evidence from the article coach them towards the correct answer. If the student has answered the question correctly, then explain why they were correct and use evidence from the article. Give score also based on rubric and explain score for each

Answer: This article investigates the impact of various video production decisions on student engagement in online educational videos, utilizing data from 6.9 million video watching sessions on the edX platform. It identifies factors such as video length, presentation style, and speaking speed that influence engagement, and offers recommendations for creating more effective educational content.

"rubric": "
                1. Length
                    1 point - Response is greater than or equal to 150 characters.
                    0 points - Response is less than 150 characters. 
                2. Key Points
                    2 points - The response mentions both videos AND student engagement rates
                    1 point - The response mentions either videos OR student engagement rates, but not both
                    0 points - The response does not summarize any important points in the article. 
        "
"""

question = """

Question: What is the article about?
    
"""

response, cost = retrieve_and_generate_response(question, template_text)
print(f"Response: {response}\nCost: {cost:.6f} USD")