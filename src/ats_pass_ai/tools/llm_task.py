import os
import google.generativeai as genai

from ats_pass_ai.limiter import Limiter

class LLMTask:

	def run(self):

		# if user_info_orgainzed_file_path does not exist then proceed
		if(self._shouldRun()):
			content = self._read_file(self.user_info_file_path)
			response = self.model.generate_content(content, request_options={"timeout": 600})
			self.large_llm_limiter.request_limiter(output=None)
			self.large_llm_limiter.record_token_usage(response.text)
			self._write_to_file(response.text)
	
	def _set_model(self):
		self.generation_config = {
				"temperature": 1.0,
				# "top_p": 0.95,
				# "top_k": 50,
				"max_output_tokens": 8192,
		}

		# Note: Safaty settings is at the initialization of this class, see __init__ method

		self.model = genai.GenerativeModel(
			model_name="gemini-1.5-pro-latest",
			# name="gemini-pro",
			system_instruction=self.system_instruction, # it will not work with gemini-pro, comment it out if gemini-pro is needed
			generation_config=self.generation_config,
			safety_settings=self.safety_settings
		)

	def _shouldRun(self):
		if self.override:
			print(f"Starting {self.task_name} task...")
			return True
		
		try:
			with open(self.user_info_orgainzed_file_path, 'r', encoding='utf-8') as f:
				content = f.read()
			if len(content) < 50:
				print(f"{self.task_name} output file found but it is most likely empty.")
				raise FileNotFoundError
			print(f"{self.task_name} output file already found and will not re-run this task. Please delete the file or it's content if you want to re-run.")
			return False
		except FileNotFoundError as e:
			print(f"Starting {self.task_name} task...")
			return True

			
	def _read_file(self, file_path):
		try:
			print(f'Started reading {file_path}')
			with open(file_path, 'r', encoding='utf-8') as file:
				return file.read()
		except FileNotFoundError:
			print(f"File not found at the specified path: {file_path}")

	def _write_to_file(self, content):
		try:
			with open(self.user_info_orgainzed_file_path, 'w', encoding='utf-8') as file:
				file.write(content)
			print(f"Successfully wrote the {self.task_name} content to: {self.user_info_orgainzed_file_path}")
		except Exception as e:
			print(f"An error occurred while writing the file: {e}")


	def __init__(self, task_name: str, user_info_file_path: str, user_info_orgainzed_file_path: str, system_instruction: str, override: bool):
		self.task_name = task_name
		self.user_info_file_path = user_info_file_path
		self.user_info_orgainzed_file_path = user_info_orgainzed_file_path
		self.system_instruction = system_instruction
		self.override = override
			# Set up the model
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
		self.large_llm_limiter = Limiter(llm_size='LARGE', llm = self.model, langchainMethods=False)
		genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))


	