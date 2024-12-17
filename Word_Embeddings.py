import numpy as np
from gensim.models import KeyedVectors

class EmbeddingChatbot(NGramChatbot):
    def __init__(self, name="Bot", embedding_path="glove.6B.50d.txt"):
        super().__init__(name)
        self.embeddings = self.load_embeddings(embedding_path)

    def load_embeddings(self, path):
        """Loads word embeddings from a file."""
        embeddings = {}
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                values = line.split()
                word = values[0]
                vector = np.array(values[1:], dtype="float32")
                embeddings[word] = vector
        return embeddings

    def predict_with_embeddings(self, word):
        """Finds the most semantically similar words based on embeddings."""
        if word not in self.embeddings:
            return "I couldn't find a prediction based on embeddings."
        word_vec = self.embeddings[word]
        similarities = {
            other_word: np.dot(word_vec, vec) / (np.linalg.norm(word_vec) * np.linalg.norm(vec))
            for other_word, vec in self.embeddings.items()
        }
        similar_word = max(similarities, key=similarities.get)
        return f"The most semantically similar word is: '{similar_word}'"
