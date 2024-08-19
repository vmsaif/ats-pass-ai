"""

    Author: Saif Mahmud
    Date: July 2024
    Project: ATS Pass AI
    Version: 1.0

    Description:
    This module is responsible for scraping the job description from the provided URL or file path.
"""

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

    def __init__(self, job_description: str, system_instruction: str):
        self.system_instruction = system_instruction

        """
        Initialize the WebScraper object with the job description URL or file path.

        Args:
            job_description (str): The URL or file path of the job description.
            system_instruction (str): The system instruction for the LLM model.

        Returns:
            None
        """

        if(job_description.startswith("http")):
            self.url = job_description
            self.job_description_file_path = None
        else:
            self.job_description_file_path = job_description
            self.url = None
        
        self.initLLM()

    def run(self):

        """
        Run the Web Scraper task to fetch the job description from the URL or file path.
        """
        print("Running Web Scraper Task...")
        self._delete_previous_jd_llm_output()
        
        # Fetch the job description from the URL or file path
        try:
            if self.url:
                response = self.fetch_page()
                soup = self.parse_html(response)
                text = self.extract_text(soup)
                print("Job Description has been fetched")
                prompt = f'{self.system_instruction} \n {text}'
            elif self.job_description_file_path:
                text = self._read_file(self.job_description_file_path)
                self.write_to_file(text)
                return True
            else:
                print("Error: No Job Description provided")
                exit(1)

        except Exception as e:
            print("Error fetching Job Description")
            traceback.print_exc()
            exit(1)
            
        # Clean-up the job description with LLM
        try:
            llm_response = self.model.generate_content(prompt, request_options={"timeout": 600})
            print("LLM Has cleaned-up the Job Description Successfully.")
            self.write_to_file(llm_response.text)
        except Exception as e:
            print("Error cleaning-up Job Description with LLM")
            traceback.print_exc()
            exit(1)
        return llm_response.text

    def _read_file(self, file_path):
        """
        Read the content of the file at the given path.

        Args:
            file_path (str): The path to the file to read

        Returns:
            str: The content of the file
        """
        try:
            print(f'Started reading {file_path}')
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            print(f"File not found at the specified path: {file_path}")


    def _delete_previous_jd_llm_output(self):

        """
        Delete the previous output files of the JD LLM Task.

        Returns: 
            None
        """
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
        # Fetch the webpage
        response = requests.get(self.url)
        return response

    def parse_html(self, response):
        # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup

    def extract_text(self, soup: BeautifulSoup):
        text = soup.get_text()
        return text

    def write_to_file(self, text):
        """
        Write the Job Description to the file at job_description_file_path.

        Args:
            text (str): The Job Description text to write to the file.

        Returns:
            None

        """

        try:
            with open(PATHS['jd_file_path'], 'w', encoding='utf-8') as file:
                file.write(text)
            print("Job Description has been written to file.")
        except IOError:
            print("Error writing Job Description to file.")
            
    
    def initLLM(self) -> None:

        """
        Initialize the LLM model for cleaning up the job description.

        Returns:
            None
        """
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

        """
            Set up the GenerativeAI model for cleaning up the job description.

            Returns:
                None

        """

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
