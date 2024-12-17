# chatbot.py
import json
import os
from datetime import datetime

class Chatbot:
    def __init__(self, memory_file="chat_memory.json"):
        self.memory_file = memory_file
        self.conversation = []
        self.knowledge_base = {}
        self.load_memory()
    
    def load_memory(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, "r") as f:
                self.conversation = json.load(f)
                self.build_knowledge_base()
        else:
            self.conversation = []
    
    def save_memory(self):
        with open(self.memory_file, "w") as f:
            json.dump(self.conversation, f, indent=4)
    
    def log_conversation(self, user_input, bot_response):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.conversation.append({
            "timestamp": timestamp,
            "user": user_input,
            "bot": bot_response
        })
        self.save_memory()
    
    def build_knowledge_base(self):
        for entry in self.conversation:
            user_input = entry["user"].lower()
            bot_response = entry["bot"]
            if "your name is" in user_input:
                name = user_input.split("your name is")[-1].strip().capitalize()
                self.knowledge_base["bot_name"] = name
            if "my name is" in user_input:
                name = user_input.split("my name is")[-1].strip().capitalize()
                self.knowledge_base["user_name"] = name
    
    def get_response(self, user_input):
        user_input = user_input.lower()
        
        # Knowledge-based responses
        if "your name" in user_input:
            return f"My name is {self.knowledge_base.get('bot_name', 'Aria')}."
        if "my name is" in user_input:
            name = user_input.split("my name is")[-1].strip().capitalize()
            self.knowledge_base["user_name"] = name
            return f"Nice to meet you, {name}!"
        if "what's my name" in user_input:
            return f"Your name is {self.knowledge_base.get('user_name', 'I don\'t know yet. Can you tell me?')}"
        
        # Default responses
        if "hello" in user_input:
            return "Hello! How can I help you today?"
        elif "bye" in user_input:
            return "Goodbye! See you next time."
        else:
            return "I'm not sure how to respond to that. Can you tell me what you mean?"
    
    def chat(self):
        print("Hi! I'm your offline chatbot. Type 'exit' to quit.")
        while True:
            user_input = input()
            if user_input.lower() == "exit":
                print("Goodbye!")
                break
            bot_response = self.get_response(user_input)
            print(bot_response)
            self.log_conversation(user_input, bot_response)
    
    def search_conversation(self, keyword):
        print(f"Searching conversations for: '{keyword}'")
        for entry in self.conversation:
            if keyword.lower() in entry["user"].lower() or keyword.lower() in entry["bot"].lower():
                print(f"[{entry['timestamp']}] {entry['user']} | {entry['bot']}")

if __name__ == "__main__":
    bot = Chatbot()
    bot.chat()
