# ollama-on-k8s

## Docker
Run in docker container
```
docker run -it -p 11434:11434 --name ollama ollama/ollama:latest
docker exec -it ollama ollama run llama3.2
```

## K8s
```
kubectl apply -f manifests
```

## API
Show models
```
curl http://localhost:11434/api/tags
```

Download a model
```
curl http://localhost:11434/api/pull -d '{
  "name": "llama3.2"
}'
```

Generate query
```
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2",
  "prompt": "In exactly 10 words or less, explain why is the sky blue."
}'
```

Generate query (no streaming)
```
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2",
  "prompt": "In exactly 10 words or less, explain why is the sky blue.",
  "stream": false
}'

```