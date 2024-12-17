import numpy as np
from collections import defaultdict

class OfflineIntentPredictor:
    def __init__(self):
        self.intent_keywords = {
            "greeting": ["hello", "hi", "hey"],
            "query_weather": ["weather", "forecast", "temperature"],
            "perform_action": ["turn on", "turn off", "start", "stop"],
            "query_information": ["what is", "how do", "explain", "show me"]
        }
        self.embedding_similarities = defaultdict(list)

    def predict_intent(self, user_input):
        # Check keywords
        for intent, keywords in self.intent_keywords.items():
            if any(keyword in user_input.lower() for keyword in keywords):
                return f"Predicted intent: {intent}"

        # Fallback: Semantic similarity (dummy example for embeddings)
        embedding_similarities = self.simulate_embeddings(user_input)
        most_similar_intent = max(embedding_similarities, key=embedding_similarities.get)
        return f"Predicted intent: {most_similar_intent} (semantic similarity)"

    def simulate_embeddings(self, user_input):
        # Dummy embedding logic for demonstration
        example_intents = ["greeting", "query_weather", "perform_action", "query_information"]
        user_embedding = np.random.rand(50)
        for intent in example_intents:
            intent_embedding = np.random.rand(50)
            similarity = np.dot(user_embedding, intent_embedding) / (
                np.linalg.norm(user_embedding) * np.linalg.norm(intent_embedding)
            )
            self.embedding_similarities[intent].append(similarity)
        return {intent: np.mean(similarities) for intent, similarities in self.embedding_similarities.items()}

# Example usage
predictor = OfflineIntentPredictor()
print(predictor.predict_intent("Can you tell me the weather?"))
