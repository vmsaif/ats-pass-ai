from textwrap import dedent
import requests
from bs4 import BeautifulSoup
import os
import google.generativeai as genai
from ats_pass_ai.limiter import Limiter
from ats_pass_ai.output_file_paths import PATHS

# URL of the webpage
class WebScraper:

    system_instruction = dedent("""
    You are given an extracted texts of a job description web page.
                                
    Give me everything as is. 
    You can remove:
    - any unnecessary white spaces or blank lines.
    - How to Apply section.
    - Company Benefits section. 
                          
    Here is the extracted texts of the job description web page:
    """)

    def __init__(self, url):
        self.url = url
        self.initLLM()

    def run(self):
        print("Running Web Scraper Task...")

        try:
            response = self.fetch_page()
            soup = self.parse_html(response)
            text = self.extract_text(soup)
            prompt = WebScraper.system_instruction + '\n' + text
            print("Job Description has been fetched")
        except Exception as e:
            print("Error fetching Job Description")
            print(e)
            exit(1)
            
        try:
            llm_response = self.model.generate_content(prompt, request_options={"timeout": 600})
            self.write_to_file(llm_response.text)
        except Exception as e:
            print("Error cleaning-up Job Description with LLM")
            exit(1)
        return llm_response.text

    def fetch_page(self):
        response = requests.get(self.url)
        return response

    def parse_html(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup

    def extract_text(self, soup):
        text = soup.get_text()
        return text

    def write_to_file(self, text):
        try:
            with open(PATHS['jd_file_path'], 'w', encoding='utf-8') as file:
                file.write(text)
            print("Job Description has been written to file.")
        except IOError:
            print("Error writing Job Description to file.")
            
    
    def initLLM(self):
        self.safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE"
            },
        ]
        self._set_model()
        self.small_llm_limiter = Limiter(llm_size='SMALL', llm = self.model, langchainMethods=False)

    def _set_model(self):
        self.generation_config = {
            "temperature": 0.75,
            # "top_p": 0.95,
            # "top_k": 50,
            "max_output_tokens": 8192,
        }
        self.model = genai.GenerativeModel(
			model_name="gemini-pro",
			# name="gemini-pro",
			# system_instruction=self.system_instruction, # it will not work with gemini-pro, comment it out if gemini-pro is needed
			generation_config=self.generation_config,
			safety_settings=self.safety_settings
		)
