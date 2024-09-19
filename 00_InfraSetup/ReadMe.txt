:: Open terminal from MacOS
Validate if v0.221.1 is available databricks --version

:: Connect to a workspace
databricks configure --token
## This will prompt to insert a host, e.g. https://e2-demo-field-eng.cloud.databricks.com/
## and a personal access token

:: Create new cluster via CLI
databricks clusters create --json @"/Users/gabriele.albini/Downloads/cluster_config.json"