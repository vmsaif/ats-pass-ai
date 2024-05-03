import os
import google.generativeai as genai
from textwrap import dedent

class LLMTask:
	def set_model(self):
		self.generation_config = {
				"temperature": 1,
				"top_p": 0.95,
				# "top_k": 50,
				"max_output_tokens": 8192,
		}

		# Note: Safaty settings is at the initialization of this class, see __init__ method

		self.model = genai.GenerativeModel(
				model_name="gemini-1.5-pro-latest",
				generation_config=self.generation_config,
				system_instruction=self.system_instruction,
				safety_settings=self.safety_settings
		)

	def run(self):

		# if user_info_orgainzed_file_path does not exist then proceed
		if(self.shouldRun()):
			self.set_model()
			content = self.read_file(self.user_info_file_path)
			response = self.model.generate_content(content, request_options={"timeout": 600})
			self.write_to_file(response.text)

	def shouldRun(self):
		if self.override:
			print(f"Starting {self.task_name} task...")
			return True
		
		try:
			with open(self.user_info_orgainzed_file_path, 'r') as f:
				content = f.read()
			if len(content) < 50:
				print(f"{self.task_name} output file found but it is most likely empty.")
				raise FileNotFoundError
			print(f"{self.task_name} output file already found and will not re-run this task. Please delete the file or it's content if you want to re-run.")
			return False
		except FileNotFoundError as e:
			print(f"Starting {self.task_name} task...")
			return True

			
	def read_file(self, file_path):
		try:
			print(f'Started reading {file_path}')
			with open(file_path, 'r', encoding='utf-8') as file:
				return file.read()
		except FileNotFoundError:
			print(f"File not found at the specified path: {file_path}")

	def write_to_file(self, content):
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
				"threshold": "BLOCK_MEDIUM_AND_ABOVE"
			},
			{
				"category": "HARM_CATEGORY_HATE_SPEECH",
				"threshold": "BLOCK_MEDIUM_AND_ABOVE"
			},
			{
				"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
				"threshold": "BLOCK_MEDIUM_AND_ABOVE"
			},
			{
				"category": "HARM_CATEGORY_DANGEROUS_CONTENT",
				"threshold": "BLOCK_MEDIUM_AND_ABOVE"
			},
		]
		genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))


















# convo = model.start_chat(history=[
#   {
#     "role": "user",
#     "parts": ["A unique self-made philosophy has always guided my journey in software development: to\ncreate a \"magic button\" for users. That is, One button should do everything the user wants at this moment."]
#   },
#   {
#     "role": "model",
#     "parts": ["## Personal Narrative\n\nSaif Mahmud is a recent Computer Science graduate from the University of Manitoba, driven by a unique philosophy of creating \"magic button\" solutions for users. His passion lies in simplifying complex processes and crafting intuitive user experiences. \n\n## Skills \n\n### Programming Languages\n\n*   Python\n*   JavaScript\n*   C++\n*   Java\n\n### Databases\n\n*"]
#   },
# ])

# convo.send_message("YOUR_USER_INPUT")
# print(convo.last.text)

