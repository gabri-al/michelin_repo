:: Open terminal from MacOS
Validate if v0.221.1 is available databricks --version

:: Connect to a workspace
databricks configure --token
## This will prompt to insert a host, e.g. https://e2-demo-field-eng.cloud.databricks.com/
## and a personal access token

:: Create new cluster via CLI
databricks clusters create --json @"/Users/gabriele.albini/Downloads/cluster_config.json"

:: Create a new secret scope
databricks secrets create-scope michelin_scope
## to delete the scope: databricks secrets delete-scope michelin_scope
:: Store the PAT as a new secret
databricks secrets put-secret --json '{
  "scope": "michelin_scope",
  "key": "pat_ga",
  "string_value": ""
}'
## to delete the secret: databricks secrets delete-secret michelin_scope pat_ga

:: From a Notebook, we can verify if above exists
# Check scope
existing_scopes = [scope.name for scope in dbutils.secrets.listScopes()]
if scope_name_ in existing_scopes:
    print("Secret scope exists!")
else:
    print("Secret scope doesn't exist, create it via CLI!")

# Check secret
existing_secrets = [secret.key for secret in dbutils.secrets.list(scope_name_)]
if secret_name_ in existing_secrets:
    print("Secret exists!")
else:
    print("Secret doesn't exist, create it via CLI!")