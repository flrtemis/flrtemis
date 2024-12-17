import os
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

# Directory where images are stored
IMAGE_DIR = r"C:\Users\bran\Desktop\AI\Emotions"

# Mood-to-image mapping
MOOD_IMAGES = {
    "happy": "happy.png",
    "worried": "worried.png",
    "angry": "angry.png",
    "sad": "sad.png",
}

current_mood = "happy"  # Default mood

@app.route("/change_mood", methods=["POST"])
def change_mood():
    global current_mood
    data = request.json
    mood = data.get("mood", "").lower()
    if mood in MOOD_IMAGES:
        current_mood = mood
        return jsonify({
            "response": f"I am {mood} now.",
            "mood": mood,
            "image_path": f"{IMAGE_DIR}/{MOOD_IMAGES[mood]}"
        })
    else:
        return jsonify({"response": "Mood not recognized.", "error": True})

@app.route("/current_mood", methods=["GET"])
def get_current_mood():
    return jsonify({
        "mood": current_mood,
        "image_path": f"{IMAGE_DIR}/{MOOD_IMAGES[current_mood]}"
    })

@app.route("/get_image/<filename>")
def get_image(filename):
    file_path = os.path.join(IMAGE_DIR, filename)
    if os.path.exists(file_path):
        return send_file(file_path, mimetype="image/png")
    else:
        return jsonify({"response": "Image not found.", "error": True})

if __name__ == "__main__":
    app.run(debug=True)  # Default host is localhost (127.0.0.1)