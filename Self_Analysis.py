# chatbot.py
import json
import os
import re
from datetime import datetime

class Chatbot:
    def __init__(self, memory_file="chat_memory.json", feedback_file="feedback.json"):
        self.memory_file = memory_file
        self.feedback_file = feedback_file
        self.conversation = []
        self.feedback = []
        self.knowledge_base = {}
        self.context = {}
        self.load_memory()
        self.load_feedback()

    def load_memory(self):
        """Loads conversation memory from a file with error handling."""
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, "r") as f:
                    self.conversation = json.load(f)
                    self.build_knowledge_base()
            else:
                self.conversation = []
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error loading memory. Starting with an empty conversation log.")
            self.conversation = []

    def save_memory(self):
        """Saves the conversation memory to a file."""
        try:
            with open(self.memory_file, "w") as f:
                json.dump(self.conversation, f, indent=4)
        except IOError as e:
            print(f"Error saving memory: {e}")

    def load_feedback(self):
        """Loads feedback data from a file."""
        try:
            if os.path.exists(self.feedback_file):
                with open(self.feedback_file, "r") as f:
                    self.feedback = json.load(f)
            else:
                self.feedback = []
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error loading feedback data. Starting with an empty feedback log.")
            self.feedback = []

    def save_feedback(self):
        """Saves feedback data to a file."""
        try:
            with open(self.feedback_file, "w") as f:
                json.dump(self.feedback, f, indent=4)
        except IOError as e:
            print(f"Error saving feedback: {e}")

    def log_conversation(self, user_input, bot_response):
        """Logs each interaction with a timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.conversation.append({
            "timestamp": timestamp,
            "user": user_input,
            "bot": bot_response
        })
        self.save_memory()

    def build_knowledge_base(self):
        """Extracts key knowledge from the conversation history."""
        for entry in self.conversation:
            user_input = entry["user"].lower()
            bot_response = entry["bot"]
            if "your name is" in user_input:
                name = user_input.split("your name is")[-1].strip().capitalize()
                self.knowledge_base["bot_name"] = name
            if "my name is" in user_input:
                name = user_input.split("my name is")[-1].strip().capitalize()
                self.knowledge_base["user_name"] = name

    def update_context(self, user_input):
        """Tracks context for ongoing conversation."""
        if "my name is" in user_input:
            name_match = re.search(r"my name is (\w+)", user_input.lower())
            if name_match:
                self.context["user_name"] = name_match.group(1).capitalize()

    def get_response(self, user_input):
        """Generates a response based on user input."""
        user_input = user_input.lower()
        self.update_context(user_input)

        # Knowledge-based responses
        if re.search(r"\byour name\b", user_input):
            return f"My name is {self.knowledge_base.get('bot_name', 'Aria')}."
        if re.search(r"\bmy name is\b", user_input):
            name_match = re.search(r"my name is (\w+)", user_input)
            if name_match:
                name = name_match.group(1).capitalize()
                self.knowledge_base["user_name"] = name
                return f"Nice to meet you, {name}!"
        if re.search(r"\bwhat's my name\b", user_input):
            return f"Your name is {self.knowledge_base.get('user_name', 'I don\'t know yet. Can you tell me?')}"
        
        # Context-aware responses
        if "how are you" in user_input and "user_name" in self.context:
            return f"I'm fine, {self.context['user_name']}! How about you?"
        
        # Default responses
        if "hello" in user_input:
            return "Hello! How can I help you today?"
        if "bye" in user_input:
            return "Goodbye! See you next time."
        return "I'm not sure how to respond to that. Can you tell me more?"

    def collect_feedback(self, user_input, bot_response):
        """Asks for user feedback on the bot's response."""
        print(f"How would you rate my response to: '{user_input}'?\nResponse: '{bot_response}'")
        print("Rate from 1 (poor) to 5 (excellent): ", end="")
        try:
            rating = int(input())
            if 1 <= rating <= 5:
                self.feedback.append({
                    "user_input": user_input,
                    "bot_response": bot_response,
                    "rating": rating
                })
                self.save_feedback()
                print("Thank you for your feedback!")
            else:
                print("Invalid rating. Feedback not recorded.")
        except ValueError:
            print("Invalid input. Feedback not recorded.")

    def chat(self):
        """Runs an interactive chat session with feedback collection."""
        print("Hi! I'm your offline chatbot. Type 'exit' to quit.")
        while True:
            user_input = input()
            if user_input.lower() == "exit":
                print("Goodbye!")
                break
            bot_response = self.get_response(user_input)
            print(bot_response)
            self.log_conversation(user_input, bot_response)
            self.collect_feedback(user_input, bot_response)

if __name__ == "__main__":
    bot = Chatbot()
    bot.chat()
