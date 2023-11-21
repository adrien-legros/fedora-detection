Test locally
```
podman pod create --name inference -p 8080:8080 -p 9000:900 -p 8000:8000

podman run -d --pod=inference --rm -v ../models:/model:Z openvino/model_server:latest --model_name fedora_detection --model_path /model --port 9000 --rest_port 8000

podman run --pod inference localhost/webrowser-fedora-detection
```
Get layers information
```
curl localhost:8000/v2/models/fedora_detection/
```