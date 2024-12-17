import tkinter as tk
from tkinter import scrolledtext
import json
from datetime import datetime


class SageChatbot:
    def __init__(self, root):
        self.root = root
        self.root.title("Sage Chatbot")
        self.root.geometry("500x600")
        self.root.configure(bg="#e6f7f9")  # Turquoise-inspired background

        # Chat display area
        self.chat_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state="disabled", bg="#000000", fg="#ffffff", font=("Arial", 12))
        self.chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Input frame
        self.input_frame = tk.Frame(self.root, bg="#e6f7f9")
        self.input_frame.pack(fill=tk.X, padx=10, pady=10)

        # Input field
        self.input_field = tk.Entry(self.input_frame, font=("Arial", 14), width=40)
        self.input_field.pack(side=tk.LEFT, padx=5, pady=5)
        self.input_field.focus()
        self.input_field.bind('<Return>', lambda event: self.send_message())
        self.input_field.config(insertbackground='white')  # Cursor color

        # Send button
        self.send_button = tk.Button(self.input_frame, text="Send", font=("Arial", 12), bg="#00aaff", fg="#ffffff", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # Memory initialization
        self.memory_file = "chat_memory.json"
        self.conversation_history = self.load_memory()

    def load_memory(self):
        """Load conversation memory from a file."""
        try:
            with open(self.memory_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_memory(self):
        """Save conversation history to a file."""
        with open(self.memory_file, "w") as file:
            json.dump(self.conversation_history, file, indent=4)

    def send_message(self):
        """Handles sending messages to Sage."""
        user_input = self.input_field.get().strip()
        if user_input:
            self.display_message("You", user_input)
            self.input_field.delete(0, tk.END)

            # Generate Sage's response
            sage_response = self.generate_response(user_input)
            self.typewriter_display("Sage", sage_response)

            # Log conversation
            self.log_conversation(user_input, sage_response)

    def generate_response(self, user_input):
        """Generate a basic response (expandable)."""
        if "hello" in user_input.lower():
            return "Hello! How can I assist you today?"
        if "remember" in user_input.lower():
            return "I always try to remember things for you!"
        return f"I'm still learning, but I appreciate your input: '{user_input}'"

    def display_message(self, sender, message):
        """Display messages in the chat window."""
        self.chat_display.config(state="normal")
        self.chat_display.insert(tk.END, f"{sender}: {message}\n")
        self.chat_display.config(state="disabled")
        self.chat_display.see(tk.END)

    def typewriter_display(self, sender, message, delay=80):
        """Display Sage's response with a typewriter effect."""
        def display_char(index=0):
            if index == 0:
                self.chat_display.config(state="normal")
                self.chat_display.insert(tk.END, f"{sender}: ")  # Add sender label
            if index < len(message):
                self.chat_display.insert(tk.END, message[index])
                self.chat_display.see(tk.END)
                self.chat_display.after(delay, display_char, index + 1)
            else:
                self.chat_display.insert(tk.END, "\n")
                self.chat_display.config(state="disabled")  # Lock the chat display again

        display_char()  # Start displaying characters

    def log_conversation(self, user_input, bot_response):
        """Log conversation to memory."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.conversation_history.append({"timestamp": timestamp, "user": user_input, "bot": bot_response})
        self.save_memory()


# Run the tkinter app
if __name__ == "__main__":
    root = tk.Tk()
    app = SageChatbot(root)
    root.mainloop()
