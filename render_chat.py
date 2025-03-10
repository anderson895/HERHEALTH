from flask import Flask, request, jsonify, render_template
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from database import Database  # Ensure this is correctly implemented

app = Flask(__name__)

# Load dataset and prepare AI model
dataset = pd.read_csv('static/assets/datasets/data.csv')

# Normalize column names
dataset.columns = [col.strip().lower() for col in dataset.columns]

# Ensure expected columns exist
if 'question' not in dataset.columns or 'answer' not in dataset.columns:
    raise ValueError("Dataset must contain 'question' and 'answer' columns")

# Train the model
model = make_pipeline(
    TfidfVectorizer(),
    LogisticRegression(solver='liblinear')
)
model.fit(dataset['question'], dataset['answer'])


class Chat(Database):
    def __init__(self):
        """Initialize the Chat class and establish database connection."""
        super().__init__()

    def chat_response(self, user_input):
        if not user_input:
            return {"error": "No message provided"}  # Return an error message
        
        # Handle specific user queries
        if "ecommerce project" in user_input.lower():
            return {
                "response": "Here is an example of an e-commerce project.",
                "image_url": "https://github.com/user-attachments/assets/eb048ca0-6acc-42da-8596-8ece266d3b64"
            }
        elif "programming languages" in user_input.lower():
            return {
                "response": "Here is a visualization of programming language usage.",
                "image_url": "https://github-readme-stats-salesp07.vercel.app/api/top-langs/?username=anderson895&hide=HTML&langs_count=8&layout=compact&theme=react&border_radius=10&size_weight=0.5&count_weight=0.5&exclude_repo=github-readme-stats"
            }
        else:
            # Use trained model to generate response
            predicted_response = model.predict([user_input])[0]
            return {"response": predicted_response}

    def close(self):
        """Closes the database connection properly."""
        super().close()




if __name__ == "__main__":
    app.run(debug=True)
