import azure.functions as func
import logging
import json
from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F

class TextEmbedder():
    def __init__(self):
        model_path = 'text-embedding-3-small'
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModel.from_pretrained(model_path)

    def _mean_pooling(self, model_output, attention_mask):
        token_embeddings = model_output[0]
        input_mask_expanded = (attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float())
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

    def generate_embeddings(self, sentences):
        encoded_input = self.tokenizer(sentences, padding=True, truncation=True, return_tensors='pt')

        with torch.no_grad():
            model_output = self.model(**encoded_input)

        sentence_embeddings = self._mean_pooling(model_output, encoded_input['attention_mask'])

        sentence_embeddings = F.normalize(sentence_embeddings, p=2, dim=1)
        return sentence_embeddings

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)
EMBEDDING_HELPER = TextEmbedder()

@app.function_name(name="TextEmbedder")
@app.route(route="custom_embeddings")
def custom_embeddings(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    request = req.get_json()

    texts = []
    for value in request["values"]:
        texts.append(value["data"]["text"])

    embeddings = EMBEDDING_HELPER.generate_embeddings(texts)

    values = []
    for index, value in enumerate(request['values']):
        recordId = value['recordId']
        embedding = embeddings[index]
        values.append({
            "recordId": recordId,
            "data": {"vector": embedding.tolist()},
            "errors": None,
            "warnings": None
        })

    response_body = { "values": values }

    response = func.HttpResponse(json.dumps(response_body, default=lambda obj: obj.__dict__))
    response.headers['Content-Type'] = 'application/json'    
    return response