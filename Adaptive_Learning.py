    def adapt_knowledge(self, user_input):
        """Learns new patterns dynamically during conversations."""
        words = user_input.split()
        for i in range(len(words) - 2):
            w1, w2, w3 = words[i].lower(), words[i + 1].lower(), words[i + 2].lower()
            self.ngram_model[(w1, w2)][w3] += 1
        print(f"{self.name} has learned from this conversation!")

    def chat(self):
        """Chat mode with adaptive learning."""
        print(f"{self.name}: Hi! I can predict words and learn dynamically. Type 'exit' to quit.")
        while True:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                print(f"{self.name}: Goodbye!")
                break
            self.adapt_knowledge(user_input)
            words = user_input.split()
            if len(words) >= 2:
                response = self.predict_next_word(words[-2], words[-1])
                print(f"{self.name}: {response}")
