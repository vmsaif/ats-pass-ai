import os
import google.generativeai as genai
from textwrap import dedent

class UserInfoOrganizer:
	def set_model(self, system_instruction):
		self.generation_config = {
				"temperature": 1,
				"top_p": 0.95,
				"top_k": 50,
				"max_output_tokens": 8192,
		}

		# Note: Safaty settings is at the initialization of this class, see __init__ method

		self.model = genai.GenerativeModel(
				model_name="gemini-1.5-pro-latest",
				generation_config=self.generation_config,
				system_instruction=system_instruction,
				safety_settings=self.safety_settings
		)

	def run(self):

		# if user_info_orgainzed_file_path does not exist then proceed
		if(self.shouldRun()):
			system_instruction = dedent("""
				Task: Content Organization and Structuring
				Objective: Reorganize provided unstructured content into a clear, structured format without missing any details. Every detail in the content is important and should be included in the final output.
				Instructions:
				1. Comprehension: Read the content to understand the themes and details.
				2. Structure Development:
					- Main Categories: Identify and label key themes with '#'.
					- Subcategories: Create necessary subcategories under each main category with '##'.
				3. Content Handling:
					- Preservation: Ensure all original information (links, dates, names) is included.
					- Clarity and Readability: Use clear headings, subheadings, and bullet points to enhance readability.
				4. Personal Content Handling:
					- Summarize personal narratives or self-descriptions in third-person, without categorization.
				5. Final Review: Check the structured content for completeness, accuracy, and coherence.Outcome: Deliver a well-organized document that maintains all original details in an accessible format.
				""")
			self.set_model(system_instruction)
			content = self.read_file(self.user_info_file_path)
			response = self.model.generate_content(content, request_options={"timeout": 600})
			self.write_to_file(response.text)

	def shouldRun(self):
		try:
			with open(self.user_info_orgainzed_file_path, 'r') as f:
				content = f.read()
			if len(content) < 50:
				print(f"User information organized file found but it is most likely empty.")
				raise FileNotFoundError
			print(f"User information organized file found. \nAssuming it is already organized in the {self.user_info_orgainzed_file_path}")
			return False
		except FileNotFoundError as e:
			print("Starting to organize user information...")
			return True

			
	def read_file(self, file_path):
		try:
			print('Started reading the file...')
			with open(file_path, 'r', encoding='utf-8') as file:
				return file.read()
		except FileNotFoundError:
			print(f"File not found at the specified path: {file_path}")

	def write_to_file(self, content):
		try:
			with open(self.user_info_orgainzed_file_path, 'w', encoding='utf-8') as file:
				file.write(content)
			print(f"Successfully wrote the organized content to: {self.user_info_orgainzed_file_path}")
		except Exception as e:
			print(f"An error occurred while writing the file: {e}")


	def __init__(self, user_info_file_path: str, user_info_orgainzed_file_path: str):
		self.user_info_file_path = user_info_file_path
		self.user_info_orgainzed_file_path = user_info_orgainzed_file_path
			
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

