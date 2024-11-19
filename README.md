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

# Deploy with GPU

## Create EKS cluster with GPU
This step will take 15-20 minutes.
```
eksctl create cluster -f gpu-setup/cluster-config.yaml
```

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
