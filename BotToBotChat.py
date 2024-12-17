import json
from datetime import datetime
import random

class Chatbot:
    def __init__(self, name="Aria", memory_file="chat_memory.json"):
        self.name = name
        self.memory_file = memory_file
        self.conversation = []
        self.knowledge_base = {"bot_name": self.name, "user_name": None}
        self.load_memory()
    
    def load_memory(self):
        try:
            with open(self.memory_file, "r") as f:
                self.conversation = json.load(f)
                self.build_knowledge_base()
        except FileNotFoundError:
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
                self.knowledge_base["bot_name"] = user_input.split("your name is")[-1].strip().capitalize()
            if "my name is" in user_input:
                self.knowledge_base["user_name"] = user_input.split("my name is")[-1].strip().capitalize()
    
    def get_response(self, user_input):
        user_input = user_input.lower()
        if "your name" in user_input:
            return f"My name is {self.knowledge_base.get('bot_name', self.name)}."
        if "my name is" in user_input:
            name = user_input.split("my name is")[-1].strip().capitalize()
            self.knowledge_base["user_name"] = name
            return f"Nice to meet you, {name}!"
        if "what's my name" in user_input:
            return f"Your name is {self.knowledge_base.get('user_name', 'I don\'t know yet. Can you tell me?')}"
        if "hello" in user_input:
            return f"Hello! How can I help you today?"
        if "bye" in user_input:
            return "Goodbye! See you next time."
        return random.choice([
            "I'm not sure how to respond to that. Can you elaborate?",
            "Interesting! Tell me more.",
            "I'm here to listen. Go on!"
        ])
    
    def chat(self):
        print(f"{self.name}: Hi! I'm your offline chatbot. Type 'exit' to quit.")
        while True:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                print(f"{self.name}: Goodbye!")
                break
            bot_response = self.get_response(user_input)
            print(f"{self.name}: {bot_response}")
            self.log_conversation(user_input, bot_response)
    
    def auto_chat(self, other_bot, turns=10):
        print(f"{self.name} and {other_bot.name} are having a conversation!")
        for _ in range(turns):
            user_input = random.choice(["hello", "how are you?", "what's your name?", "bye"])
            bot_response = self.get_response(user_input)
            print(f"{self.name}: {bot_response}")
            self.log_conversation(user_input, bot_response)
            
            if user_input.lower() == "bye":
                break
            
            user_input_other = bot_response  # Pass response to the other bot
            other_bot_response = other_bot.get_response(user_input_other)
            print(f"{other_bot.name}: {other_bot_response}")
            other_bot.log_conversation(user_input_other, other_bot_response)

if __name__ == "__main__":
    bot1 = Chatbot(name="Aria")
    bot2 = Chatbot(name="Bran")
    
    # Uncomment one of the modes below to try different functionalities:
    
    # Human-Bot Chat
     bot1.chat()
    
    # Bot-to-Bot Conversation
     bot1.auto_chat(bot2, turns=5)
