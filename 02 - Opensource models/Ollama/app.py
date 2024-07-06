import streamlit as st
import time
from elasticsearch import Elasticsearch
from tqdm.auto import tqdm
import json

from openai import OpenAI


with open("documents.json","r") as docs:
    documents_raw = json.load(docs)

documents = []

for course in documents_raw:
    course_name = course['course']

    for doc in course['documents']:
        doc['course'] = course_name
        documents.append(doc)

es_client = Elasticsearch('http://localhost:9200')

def elastic_query(query):
    search_query = {
        "size":10,
        "query":{
            "bool":{
                "must":{
                    "multi_match":{
                        "query":query,
                        "fields":["question^3","text","section"],
                        "type":"best_fields"
                    }
                },
                "filter":{
                    "term":{
                        "course":"data-engineering-zoomcamp"
                    }
                }
            }
        }
    }
    response = es_client.search(index="course-questions",body=search_query)
    
    results = []

    for doc in response['hits']['hits']:
        results.append(doc['_source']) 

    return results


client = OpenAI(
    base_url='http://localhost:11434/v1/',
    # required but ignored
    api_key='ollama',
)

def build_prompt(query, search_results):
    prompt_template = """
You're a course teaching assistant. Answer the QUESTION based on the CONTEXT from the FAQ database.
Use only the facts from the CONTEXT when answering the QUESTION. If fact not present, return NONE

QUESTION: {question}

CONTEXT: 
{context}
""".strip()

    context = ""
    
    for doc in search_results:
        context = context + f"section: {doc['section']}\nquestion: {doc['question']}\nanswer: {doc['text']}\n\n"
    
    prompt = prompt_template.format(question=query, context=context).strip()
    return prompt

# Function to generate response from OpenAI API
def generate_response(prompt):
    try:
        response = client.chat.completions.create(model='phi3',
        messages=[{"role": "user", "content": prompt}]
        )
    
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def rag(query):
    search_results = elastic_query(query)
    prompt = build_prompt(query, search_results)
    print(prompt[0])
    answer = generate_response(prompt)
    return answer

# Main interface function
def main():
    # Set page config
    st.set_page_config(page_title="RAG", page_icon="🌟", layout="centered")
    
    # Custom CSS for styling
    st.markdown("""
        <style>
            .container {
                max-width: 750px;
                margin: auto;
                padding: 2rem;
                background-color: #1c1e21;
                border-radius: 10px;
                box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
                color: white;
            }
            .header {
                text-align: center;
                font-size: 2rem;
                font-weight: bold;
                margin-bottom: 2rem;
            }
            .input-box {
                width: 100%;
                padding: 1rem;
                border-radius: 10px;
                border: none;
                margin-bottom: 1rem;
                font-size: 1rem;
            }
            .example-buttons {
                display: flex;
                justify-content: space-around;
                margin-top: 1rem;
            }
            .example-buttons button {
                padding: 0.5rem 1rem;
                font-size: 1rem;
                border-radius: 5px;
                border: none;
                cursor: pointer;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # HTML container for the interface
    # st.markdown('<div class="container">', unsafe_allow_html=True)
    
    # Header
    st.markdown('<div class="header">Hello there</div>', unsafe_allow_html=True)
    
    # User input
    user_input = st.text_area("How can I help you today?", key="user_input", height=100)
    
    # Generate Response button
    if st.button("Send"):
        if user_input:
            with st.spinner('Generating response...'):
                response = rag(user_input)
                time.sleep(2)  # Simulating response time
                start_time = time.time()
                progress_bar = st.progress(0)
                status_text = st.empty()

                for i in range(10):
                    elapsed_time = time.time() - start_time
                    progress_bar.progress((i + 1) / 10)
                    status_text.text(f"Time elapsed: {int(elapsed_time)} seconds")
                    time.sleep(0.5)
                
                elapsed_time = time.time() - start_time
                st.markdown(f"**Dani 1.0 Sonnet:**\n{response}")
                status_text.text(f"Total time elapsed: {int(elapsed_time)} seconds")
        else:
            st.warning("Please enter a query to get a response.")

if __name__ == "__main__":
    main()
