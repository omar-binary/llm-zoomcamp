import json
from elasticsearch import Elasticsearch
import requests
import tiktoken


def download_documents():
    docs_url = 'https://github.com/DataTalksClub/llm-zoomcamp/blob/main/01-intro/documents.json?raw=1'
    docs_response = requests.get(docs_url)
    return docs_response.json()

def setup_elasticsearch():
    es_client = Elasticsearch('http://localhost:9200')
    return es_client

def create_index(es_client, index_name, documents_raw):
    documents = []
    index_settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "properties": {
                "text": {"type": "text"},
                "section": {"type": "text"},
                "question": {"type": "text"},
                "course": {"type": "keyword"}
            }
        }
    }

    # having the index already exist causing inaccuracy in the search results
    if not es_client.indices.exists(index=index_name):
        es_client.indices.create(index=index_name, body=index_settings)
        print(f'Created index {index_name}')
    else:
        print(f'Index {index_name} already exists')
        es_client.indices.delete(index=index_name)
        es_client.indices.create(index=index_name, body=index_settings)

    for course in documents_raw:
        course_name = course['course']
        for doc in course['documents']:
            doc['course'] = course_name
            documents.append(doc)
            es_client.index(index=index_name, document=doc)

def elastic_search(es_client, index_name, query):
    search_query = {
    "size": 3,
    "query": {
        "bool": {
            "must": {
                "multi_match": {
                    "query": query,
                    "fields": ["question^4", "text"],
                    "type": "best_fields"
                }
            },
            "filter": {
                "term": {
                    "course": "machine-learning-zoomcamp"
                }
            }
        }
    }
}

    response = es_client.search(index=index_name, body=search_query)
    # print(response)
    result_docs = []
    for hit in response['hits']['hits']:
        result_docs.append(hit['_source'])
        print(hit['_score'])
        print(hit['_source']['question'])
        print('---')

    return result_docs

def build_prompt(query, search_results):
    context_template = """
Q: {question}
A: {text}
""".strip()

    context = "\n\n".join([context_template.format(question=doc['question'], text=doc['text']) for doc in search_results])

    prompt_template = f"""
You're a course teaching assistant. Answer the QUESTION based on the CONTEXT from the FAQ database.
Use only the facts from the CONTEXT when answering the QUESTION.

QUESTION: {query}

CONTEXT:
{context}
""".strip()

    return prompt_template

def llm(prompt):
    encoding = tiktoken.encoding_for_model("gpt-4o")
    tokens = encoding.encode(prompt)

    # For future use
    # response=client.chat.completions.create(model='gpt-4o', messages=[{'role':'user','content': prompt}])
    # return response.choices[0].message.content
    return len(tokens)


def run():
    question = "How do I execute a command in a running docker container?"
    documents_raw = download_documents()
    es_client = setup_elasticsearch()
    create_index(es_client, index_name = "course-questions", documents_raw=documents_raw)
    search_results = elastic_search(es_client, index_name="course-questions", query=question)
    # print(json.dumps(search_results, indent=2))
    prompt = build_prompt(question, search_results)
    print(len(prompt))
    # print(prompt)
    print(llm(prompt))


if __name__ == "__main__":
    run()