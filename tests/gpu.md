### Check if GPU is available

```
oc project nvidia-gpu-operator
oc get pod -owide -lopenshift.driver-toolkit=true
oc exec -it <POD_NAME> -- nvidia-smi
```

### Test GPU

```
cat << EOF | oc create -f -
apiVersion: v1
kind: Pod
metadata:
  name: cuda-vectoradd
spec:
  tolerations:
    - effect: NoSchedule
      key: ssa-team-france.redhat.com/gpu
      operator: Exists
  restartPolicy: OnFailure
  containers:
  - name: cuda-vectoradd
    image: "nvidia/samples:vectoradd-cuda11.2.1"
    resources:
      limits:
        nvidia.com/gpu: 1
EOF
oc logs cuda-vectoradd
```

### Test GPU sharing

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: time-slicing-verification
  labels:
    app: time-slicing-verification
spec:
  replicas: 5
  selector:
    matchLabels:
      app: time-slicing-verification
  template:
    metadata:
      labels:
        app: time-slicing-verification
    spec:
      tolerations:
        - key: ssa-team-france.redhat.com/gpu
          operator: Exists
          effect: NoSchedule
      containers:
        - name: cuda-sample-vector-add
          image: "nvcr.io/nvidia/k8s/cuda-sample:vectoradd-cuda11.7.1-ubuntu20.04"
          command: ["/bin/bash", "-c", "--"]
          args:
            - while true; do /cuda-samples/vectorAdd; done
          resources:
           limits:
             nvidia.com/gpu: 1
```