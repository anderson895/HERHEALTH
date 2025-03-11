

import json
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
                "image_url": "https://github.com/user-attachments/assets/eb048ca0-6acc-42da-8596-8ece266d3b64",
                "type": "img_url"
            }
        elif "programming languages" in user_input.lower():
            return {
                "response": "Here is a visualization of programming language usage.",
                "image_url": "https://github-readme-stats-salesp07.vercel.app/api/top-langs/?username=anderson895&hide=HTML&langs_count=8&layout=compact&theme=react&border_radius=10&size_weight=0.5&count_weight=0.5&exclude_repo=github-readme-stats",
                "type": "img_url"
            }
        else:
            # Use trained model to generate response
            # Use trained model to generate response
            predicted_response = model.predict([user_input])[0]
            return {"response": predicted_response}




    def record_chat(self, chat_sender_id, user_input, chat_bot_response):
        """I-save ang chat sa database."""
        
        # Determine response type and content
        if isinstance(chat_bot_response, dict):
            chat_response_type = chat_bot_response.get("type", "text")  # Default to "text"
            chat_response_content = (
                chat_bot_response.get("image_url") or  # Use image URL if available
                chat_bot_response.get("response", "")  # Otherwise, use response text
            )
        elif isinstance(chat_bot_response, str):
            chat_response_type = "text"
            chat_response_content = chat_bot_response
        else:
            chat_response_type = "unknown"
            chat_response_content = str(chat_bot_response)

        # Format response as JSON string
        chat_bot_response_formatted = json.dumps({
            "type": chat_response_type,
            "content": chat_response_content
        })

        status = 1  # Default status

        try:
            self.execute_query(
                '''INSERT INTO "chat" (chat_sender_id, chat_content, chat_bot_response, chat_status) 
                VALUES (%s, %s, %s, %s)''', 
                (chat_sender_id, user_input, chat_bot_response_formatted, status)
            )
            print(f"✅ Chat record saved successfully for sender_id {chat_sender_id}")
            return True
        except Exception as e:
            print(f"❌ Error saving chat record (sender_id: {chat_sender_id}, input: {user_input}): {e}")
            return False


    def get_chats(self, chat_sender_id, target_date):
        if not chat_sender_id:
            return {"error": "Missing chat_sender_id"}

        chat_instance = Chat()

        # Convert TIMESTAMPTZ to DATE for comparison
        query = '''SELECT chat_content, chat_bot_response 
                FROM chat 
                WHERE chat_sender_id = %s 
                AND DATE(chat_sent_date) = %s 
                ORDER BY chat_id ASC'''
        
        chat_records = chat_instance.fetch_all(query, (chat_sender_id, target_date))

        chat_instance.close()

        if not chat_records:
            return []

        formatted_chats = []
        for record in chat_records:
            if isinstance(record, dict):
                chat_content = record.get("chat_content", "")
                chat_bot_response = record.get("chat_bot_response", "{}")
            else:
                chat_content, chat_bot_response = record  # Tuple unpacking

            # ✅ Convert string representation of dict into actual JSON
            if isinstance(chat_bot_response, str):
                try:
                    bot_response = json.loads(chat_bot_response.replace("'", '"'))  # Fix single quotes to double quotes
                except json.JSONDecodeError:
                    bot_response = {"type": "text", "content": chat_bot_response}
            else:
                bot_response = chat_bot_response  # Already a dict

            formatted_chats.append({
                "user_message": chat_content,
                "bot_type": bot_response.get("type", "text"),
                "bot_message": bot_response.get("content", ""),
            })

        return formatted_chats










    def close(self):
        """Closes the database connection properly."""
        super().close()




if __name__ == "__main__":
    app.run(debug=True)
