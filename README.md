# ollama-on-k8s

## Docker
Run in docker container
```
docker run -it -p 11434:11434 --name ollama ollama/ollama:latest
docker exec -it ollama ollama run mistral
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
  "name": "mistral"
}'
```

Generate query
```
curl http://localhost:11434/api/generate -d '{
  "model": "mistral",
  "prompt": "What is the color of the sky"
}'
```

Generate query (no streaming)
```
curl http://localhost:11434/api/generate -d '{
  "model": "mistral",
  "prompt": "In exactly 10 words or less, explain why is the sky blue.",
  "stream": false
}'
```

# Deploy with GPU

## Get GPU operator helm chart
```
helm repo add nvidia https://helm.ngc.nvidia.com/nvidia \
    && helm repo update
```

## Install GPU operator helm chart
Installs several components (Device Plugin, GPU Driver, nvidia container toolkit, etc)
```
helm upgrade --install gpu-operator nvidia/gpu-operator \
    --namespace gpu-operator --create-namespace \
    --values gpu-setup/gpu-values.yaml
```

## Deploy Ollama with GPUs
```
kubectl apply -f gpu-manifests/
```

## Deploy time slicing config-map
```
kubectl delete deploy/ollama -n ollama --force

kubectl apply -f gpu-setup/time-slicing-config-map.yaml

kubectl patch clusterpolicies.nvidia.com/cluster-policy \
    -n gpu-operator --type merge \
    -p '{"spec": {"devicePlugin": {"config": {"name": "time-slicing-config", "default": "any"}}}}'

kubectl rollout restart deploy/gpu-operator -n gpu-operator
```

# ollama-UI
## Docker
Run in docker container
```
docker pull ghcr.io/dimitrisbro/ollama-ui:latest
docker run -it -e OLLAMA_URL="http://localhost" -e OLLAMA_PORT="11434" -p 8501:8501 ghcr.io/dimitrisbro/ollama-ui:latest
```

## K8s
```
kubectl apply -f user-interface/manifests
```
