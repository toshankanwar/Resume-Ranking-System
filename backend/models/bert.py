from transformers import DistilBertTokenizer, DistilBertModel

# Force download fresh copy
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased', force_download=True)
model = DistilBertModel.from_pretrained('distilbert-base-uncased', force_download=True)
