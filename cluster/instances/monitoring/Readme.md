Generate a service account token
```
echo token="Bearer $(oc create token grafana-a-sa)" > ./cluster/instances/monitoring/grafana-token.env
```
Manually add the dashboad (cause datasource default issue): https://raw.githubusercontent.com/kserve/modelmesh-performance/main/docs/monitoring/modelmesh_grafana_dashboard_1634165844916.json