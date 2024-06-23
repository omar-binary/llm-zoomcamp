# Homework: Introduction

## Q1. Running Elastic

```bash
docker run -it \
    --rm \
    --name elasticsearch \
    -p 9200:9200 \
    -p 9300:9300 \
    -e "discovery.type=single-node" \
    -e "xpack.security.enabled=false" \
    docker.elastic.co/elasticsearch/elasticsearch:8.4.3
```

```bash
curl localhost:9200
```

## Q2. Indexing the data

```bash
es_client.index(index=index_name, document=doc)
```

## Q3. Searching

```python
search_query = {
        "size": 1,
        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": query,
                        "fields": ["question^4", "text"],
                        "type": "best_fields"
                    }
                },
            }
        }
    }
```

## Q4. Filtering

```python
search_query = {
        "size": 5,
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
```

## Q5. Building a prompt

```python
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
# len: 1462
```

## Q6. Tokens

```python
def llm(prompt):
    encoding = tiktoken.encoding_for_model("gpt-4o")
    tokens = encoding.encode(prompt)
    return len(tokens)
# 322
```
