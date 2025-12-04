import os
import google.generativeai as genai
from dotenv import load_dotenv
from src.neural_core.prompts import SYSTEM_PROMPT, RULE_GENERATION_PROMPT


load_dotenv()

class NeuralBrain:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def analyze_log_and_generate_rule(self, log_entry):
        # gui log len gemini va nhan ve Falco rule YAML


        prompt = RULE_GENERATION_PROMPT.format(log_json = log_entry)

        try:
            response = self.model.generate_content(prompt)
            return self.clean_response(response.text)
        except Exception as e:
            print(f"Error generating rule: {e}")
            return None
        
    def clean_response(self, text):
        """
        Làm sạch response để chỉ lấy nội dung YAML.
        Loại bỏ markdown ```yaml ... ``` nếu có.
        """
        text = text.strip()
        if text.startswith("```yaml"):
            text = text.replace("```yaml", "", 1)
        if text.startswith("```"):
            text = text.replace("```", "", 1)
        if text.endswith("```"):
            text = text[:-3]
        return text.strip()