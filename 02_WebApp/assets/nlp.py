import requests

## Function to call model from Huggingface API
def embed_from_api(sentence_):
    model_name = 'BAAI/bge-base-en-v1.5'
    api_url = f"https://api-inference.huggingface.co/models/{model_name}"

    # Prepare API call info
    hf_token = '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'
    headers = {"Authorization": f"Bearer {hf_token}"}
    payload = {
        "inputs": sentence_
    }

    # Call to API
    response = requests.post(api_url, headers=headers, json=payload)

    # Process response
    if response.status_code == 200:
      embedded_data = response.json()
    else:
      embedded_data = None
      print("Failed! Status code: %s" % (response.status_code))

    return response.status_code, embedded_data