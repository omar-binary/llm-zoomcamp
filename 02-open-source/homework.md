# Homework: Open-Source LLMs

## Q1. Running Ollama with Docker

```bash
docker run -it \
    --rm \
    -v ollama:/root/.ollama \
    -p 11434:11434 \
    --name ollama \
    ollama/ollama
```

```bash
ollama -v
```

## Q2. Downloading an LLM

```bash
ollama pull gemma:2b

cat /root/.ollama/models/manifests/registry.ollama.ai/library/gemma/2b
```

## Q3. Running the LLM

```bash
ollama run gemma:2b
>>> 10 * 10
```

## Q4. Downloading the weights

```bash
mkdir ollama_files

docker run -it \
    --rm \
    -v ./ollama_files:/root/.ollama \
    -p 11434:11434 \
    --name ollama \
    ollama/ollama

# Now pull the model:
docker exec -it ollama ollama pull gemma:2b

du -h ollama_files/
```

## Q5. Adding the weights

```docker
COPY ./ollama_files/ /root/.ollama/
```

## Q6. Serving it

```bash
# Let's build it:
docker build -t ollama-gemma2b .

# And run it:
docker run -it --rm -p 11434:11434  --name ollama ollama-gemma2b

# We can connect to it using the OpenAI client
# Let's test it with the following prompt:
# prompt = "What's the formula for energy?"
# Also, to make results reproducible, set the temperature parameter to 0:

response = client.chat.completions.create(model='gemma:2b',
    messages=[{'role': 'user', 'content': "What's the formula for energy?"}],
    temperature=0.0
    )
```
