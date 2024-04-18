from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd


droot = "../../data/scopus/"
data = pd.read_csv(droot+"scopus_results_brain-psychology.csv")

# Assuming 'data' is already loaded as in the previous TF-IDF example
data['Abstract'] = data['Abstract'].fillna('')

# Initialize Count Vectorizer
vectorizer = CountVectorizer(stop_words='english')
x_counts = vectorizer.fit_transform(data['Abstract'])

# Initialize LDA Model: Let's assume we are looking for 5 topics
lda = LatentDirichletAllocation(n_components=5, random_state=0)
x_topics = lda.fit_transform(x_counts)

# Get words that contribute to each topic
words = vectorizer.get_feature_names_out()
topic_summaries = []
for topic_idx, topic in enumerate(lda.components_):
    message = "Topic #%d: " % topic_idx
    message += " ".join([words[i] for i in topic.argsort()[:-10 - 1:-1]])
    topic_summaries.append(message)

# Print the topics found by the LDA model
print("\n".join(topic_summaries))
