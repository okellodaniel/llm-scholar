# Ollama


**Framework** for running llms locally

([Documentation](https://github.com/ollama/ollama/tree/main))

## Running options
1. Codespaces (Locally on its root)
2. Local Installon my machine
3. Run in a docker image

```
docker run \
-d -v ollama:/root/.ollama \
-p 11434:11434 \
--name ollama ollama/ollama

```


Ollama can be run as a replacement for OpenAI client

[here](https://github.com/ollama/ollama/blob/main/docs/openai.md)

