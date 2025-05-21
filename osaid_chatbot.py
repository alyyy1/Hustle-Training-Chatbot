import pandas as pd
import google.generativeai as genai

class ChatBot:
    def __init__(self):
        self.gemini_api_key = "AIzaSyDJj7oSPFomRy9WjOBWOH-N3mt05uQzzNo"


    def gemini_code(self,prompt):
        try:
            genai.configure(api_key=self.gemini_api_key)

            # Create the model
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
            safety_settings = safety_settings
            # See https://ai.google.dev/gemini-api/docs/safety-settings
            )

            chat_session = model.start_chat(
            history=[]
            )

            response = chat_session.send_message(prompt)

            print(response.text)
            return response.text
        except Exception as ex:
            print(f'status: error, msg: Exception occurs at gemini_code function, data: {ex}')
            return {'status': 'error', 'msg': 'Exception occurs at gemini_code function', 'data': str(ex)}
        
    
    def main(self):
        excel_data = pd.read_excel(r"C:\Users\iqra com\Downloads\ht360.xlsx")
        data_dict = excel_data.to_dict(orient='records') 
        print(data_dict)

        while True:
            user_input = input("Ask me anything...")

            # prompt = f""" You are a chatbot for a fitness class center, and your task is to answer users' questions based on the fitness class information provided below.

            #     Here is the class information:

            #     {data_dict}

            #     User: {user_input}

            #     Please respond based on the information provided above. If the question isn’t covered in the list, respond with “I’m sorry, I don’t have information on that.
            # """

            prompt = f""" You are a chatbot asssitant and you are tasked to fetch and return desired link from the data provided for user based on user input.

                Here is the class information:

                {data_dict}

                User: {user_input}

                Please respond based on the information provided above. If the question isn’t covered in the list, respond with “I’m sorry, I don’t have information on that.
            """

            self.gemini_code(prompt)


if __name__ == "__main__":
    c1 = ChatBot()
    c1.main()

