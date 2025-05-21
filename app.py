import os
from flask import Flask, render_template, request
import pandas as pd
import google.generativeai as genai

app = Flask(__name__)

class ChatBot:
    def __init__(self):
        self.gemini_api_key = "AIzaSyDJj7oSPFomRy9WjOBWOH-N3mt05uQzzNo"
        self.data_dict = self.load_data()

    def load_data(self):
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(base_dir, "ht360.xlsx")
            excel_data = pd.read_excel(file_path) 
            return excel_data.to_dict(orient='records')
        except Exception as e:
            print(f"Error loading data: {e}")
            return []

    def gemini_code(self, prompt):
        try:
            genai.configure(api_key=self.gemini_api_key)

            generation_config = {
                "temperature": 1,
                "top_p": 0.95,
                "top_k": 64,
                "max_output_tokens": 8192,
                "response_mime_type": "text/plain",
            }

            safety_settings = [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ]

            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config=generation_config,
                safety_settings=safety_settings
            )

            chat_session = model.start_chat(history=[])

            response = chat_session.send_message(prompt)
            return response.text

        except Exception as ex:
            return f"Error occurred: {ex}"

chatbot = ChatBot()

@app.route("/", methods=["GET", "POST"])
def index():
    response = ""
    if request.method == "POST":
        user_input = request.form.get("user_input")

        prompt = f""" You are a chatbot assistant and you are tasked to fetch and return desired link from the data provided for user based on user input.

        Here is the class information:

        {chatbot.data_dict}

        User: {user_input}

        Please respond based on the information provided above. If the question isn’t covered in the list, respond with “I’m sorry, I don’t have information on that."""
        
        response = chatbot.gemini_code(prompt)

    return render_template("index.html", response=response)

if __name__ == "__main__":
    app.run(debug=True)
