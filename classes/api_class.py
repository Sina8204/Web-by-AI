from google import genai 
import re

class models :
    def __init__(self):
        self.key = ""
        self.system_instruction = "" #Explain to your model what to do
        self.user_input = "" #Your promt
        #creat model
        self.response_text = ""
    
    def send_requiest_to_model(self):
        self.client = genai.Client(api_key=self.key) #Input your api key
        self.response = self.client.models.generate_content (
        model="gemini-2.5-flash",
        config=genai.types.GenerateContentConfig(system_instruction=self.system_instruction),
        contents=self.user_input
        )
        self.response_text = self.response.text

    def outpute(self):
        try:
            return self.response_text
        except Exception as e:

            return f"Error : {e}"
