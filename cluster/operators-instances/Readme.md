### GPU info

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
cat << EOF | oc create -f -
apiVersion: v1
kind: Pod
metadata:
  name: cuda-vectoradd-1
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
---
apiVersion: v1
kind: Pod
metadata:
  name: cuda-vectoradd-2
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
```