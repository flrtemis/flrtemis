import os

class PersonalChatbot:
    def __init__(self, name="Bot"):
        self.name = name
        self.knowledge_base = {}

    def read_files(self, folder_path):
        """Reads all text files from the specified folder and builds a knowledge base."""
        if not os.path.exists(folder_path):
            print(f"Error: Folder {folder_path} does not exist.")
            return

        for filename in os.listdir(folder_path):
            if filename.endswith(".txt"):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    self.ingest_knowledge(filename, content)
        print(f"{self.name} has read all text files in {folder_path}.")

    def ingest_knowledge(self, source, text):
        """Splits text into sections and stores it in the knowledge base."""
        paragraphs = text.split("\n\n")
        for i, paragraph in enumerate(paragraphs):
            key = f"{source} - Section {i + 1}"
            self.knowledge_base[key] = paragraph.strip()

    def search_knowledge(self, query):
        """Searches the knowledge base for content matching the query."""
        results = []
        for key, content in self.knowledge_base.items():
            if query.lower() in content.lower():
                results.append(content)
        return results if results else ["I couldn't find anything related to that."]

    def chat(self):
        """Engages in conversation, using the knowledge base for responses."""
        print(f"{self.name}: Hi! I can answer questions based on the files I've read. Type 'exit' to quit.")
        while True:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                print(f"{self.name}: Goodbye!")
                break
            responses = self.search_knowledge(user_input)
            for response in responses:
                print(f"{self.name}: {response}")

# Example Usage
if __name__ == "__main__":
    bot = PersonalChatbot(name="PersonalBot")
    bot.read_files("C:/Users/bran/Desktop/AI/AI_Reader/")  # Replace with the folder containing your text files
    bot.chat()
