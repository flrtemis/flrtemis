from collections import defaultdict, Counter

class NGramChatbot(PersonalChatbot):
    def __init__(self, name="Bot"):
        super().__init__(name)
        self.ngram_model = defaultdict(Counter)

    def ingest_knowledge(self, source, text):
        """Processes text to extract n-grams (bigrams, trigrams) and store frequencies."""
        words = text.split()
        for i in range(len(words) - 2):  # Trigram example
            w1, w2, w3 = words[i].lower(), words[i + 1].lower(), words[i + 2].lower()
            self.ngram_model[(w1, w2)][w3] += 1

    def predict_next_word(self, w1, w2):
        """Predicts the most likely next word based on two prior words."""
        candidates = self.ngram_model[(w1.lower(), w2.lower())]
        if candidates:
            next_word = candidates.most_common(1)[0][0]
            return f"The next likely word is: '{next_word}'"
        return "I couldn't predict the next word. Try different input."
