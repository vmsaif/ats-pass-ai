import os
from textwrap import dedent
import traceback
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from util.limiter import Limiter
from path.output_file_paths import PATHS
from dotenv import load_dotenv
# URL of the webpage
class WebScraper:
    load_dotenv()
    system_instruction = dedent("""
    You are given an extracted texts of a job description from a web page.
                                
    Give me everything as is. 
                                
    Expertec Output:
    - Full context in the exactly provided words without any changes.
    - Start the output with:
        Job Role:
        Company Name:
        Location: (if available)
        Rest of the content as is.
                                
    You can remove:
    - any unnecessary white spaces or blank lines. 
    - How to Apply section.
    - Benefits section like "Dental, Vision, Medical, 401k, etc." 
                          
    Here is the extracted texts of the job description web page:
    """)

    def __init__(self, url):
        self.url = url
        self.initLLM()

    def run(self):
        print("Running Web Scraper Task...")
        self.delete_previous_jd_llm_output()
        try:
            response = self.fetch_page()
            soup = self.parse_html(response)
            text = self.extract_text(soup)
            prompt = WebScraper.system_instruction + '\n' + text
            print("Job Description has been fetched")
        except Exception as e:
            print("Error fetching Job Description")
            traceback.print_exc()
            exit(1)
            
        try:
            llm_response = self.model.generate_content(prompt, request_options={"timeout": 600})
            print("LLM Has cleaned-up the Job Description Successfully.")
            self.write_to_file(llm_response.text)
        except Exception as e:
            print("Error cleaning-up Job Description with LLM")
            traceback.print_exc()
            exit(1)
        return llm_response.text

    def delete_previous_jd_llm_output(self):
        try:           
            os.remove(PATHS['jd_keyword_extraction'])
            print("Deleted previous jd_keyword_extraction.")
        except FileNotFoundError:
            print("No previous jd_keyword_extraction to delete.")
        try:
            os.remove(PATHS['company_value_extraction'])
            print("Deleted previous company_value_extraction.")
        except FileNotFoundError:
            print("No previous company_value_extraction to delete.")

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

        # list all environ keys
        genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
        self.model = genai.GenerativeModel(
			model_name="gemini-pro",
			# name="gemini-1.5-pro-latest",
			# system_instruction=self.system_instruction, # it will not work with gemini-pro, comment it out if gemini-pro is needed
			generation_config=self.generation_config,
			safety_settings=self.safety_settings

		)
