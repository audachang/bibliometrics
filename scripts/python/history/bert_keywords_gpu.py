import torch
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
from tqdm import tqdm

def get_bert_embeddings(text, model, tokenizer, device):
    """ Generate BERT embeddings from input text using a specified model and tokenizer on a specified device (CPU/GPU). """
    encoded_input = tokenizer(text, padding=True, truncation=True, max_length=512, return_tensors='pt')
    encoded_input = {key: val.to(device) for key, val in encoded_input.items()}  # Move input to GPU
    with torch.no_grad():
        output = model(**encoded_input)
    return output.last_hidden_state.mean(dim=1).squeeze().cpu().numpy()  # Move embeddings back to CPU

def extract_keywords_bert(abstracts, model, tokenizer, device, top_n=5):
    """ Extracts top N keywords from a list of abstracts using BERT embeddings for similarity comparison on a specified device. """
    results = []
    progress_bar = tqdm(abstracts, desc="Processing Abstracts", unit="abstract")
    for abstract in progress_bar:
        if abstract:
            words = list(set(abstract.lower().replace("(", "").replace(")", "").replace(".", "").replace(",", "").split()))
            document_embedding = get_bert_embeddings(abstract, model, tokenizer, device)
            word_embeddings = np.array([get_bert_embeddings(word, model, tokenizer, device) for word in words])
            
            similarities = cosine_similarity([document_embedding], word_embeddings).flatten()
            top_indices = np.argsort(similarities)[::-1][:top_n]
            keywords = [(words[index], round(similarities[index], 3)) for index in top_indices]
        else:
            keywords = [("No abstract available", 0)]
        
        results.append({f"Keyword {i+1}": keywords[i][0] + " (Importance: " + str(keywords[i][1]) + ")" for i in range(len(keywords))})
    return results

droot = '../../data/scopus/'

# Setting up the device for GPU usage
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

print("Loading the BERT model and tokenizer...")
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased').to(device)  # Move model to GPU

print("Reading dataset...")
data = pd.read_csv(droot+'scopus_results_brain-psychology.csv')
data['Abstract'] = data['Abstract'].fillna('')  # Handle missing abstracts

print("Extracting keywords from abstracts...")
data['Keywords'] = extract_keywords_bert(data['Abstract'], model, tokenizer, device)

print("Saving the results to a new CSV file...")
data.to_csv(droot+'scopus_results_with_keywords.csv', index=False)
print("Keywords extraction completed and results saved.")
