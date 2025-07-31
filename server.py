from flask import Flask, request, send_from_directory
import os
import subprocess

app = Flask(__name__)

# Serve the HTML file
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

# Handle answer submission
@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    answer = data.get("answer", "").strip().lower()

    if answer == "yes":
        with open("ans.txt", "w") as f:
            f.write("yes\n")

        # Git operations
        try:
            subprocess.run(["git", "add", "ans.txt"], check=True)
            subprocess.run(["git", "commit", "-m", "💍 Proposal answer recorded: yes"], check=True)
            subprocess.run(["git", "push"], check=True)
        except subprocess.CalledProcessError as e:
            return {"status": "error", "message": f"Git error: {e}"}, 500

    return {"status": "saved", "answer": answer}

if __name__ == '__main__':
    app.run(debug=True)
