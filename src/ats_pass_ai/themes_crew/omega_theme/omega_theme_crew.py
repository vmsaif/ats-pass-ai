# -*- coding: utf-8 -*-
"""
	Author: Saif Mahmud
	Date: 04-23-2024
	Description: This file contains the crew class for the applicant info organizer crew.
"""

import os
import yaml
import agentops

from langchain_google_genai import GoogleGenerativeAI, HarmBlockThreshold, HarmCategory
from crewai import Agent, Crew, Process, Task
from ats_pass_ai.limiter import Limiter
from ats_pass_ai.output_file_paths import PATHS

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter

trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
	SimpleSpanProcessor(ConsoleSpanExporter())
)

os.environ['OTEL_PYTHON_AUTO_INSTRUMENT'] = '0'  # Disable automatic instrumentation
os.environ["OTEL_PYTHON_DISABLED"] = "1"  # Disable OpenTelemetry tracing for the crew

class OmegaThemeCrew:
	"""Resume Maker Crew"""
	agents_config = 'src/ats_pass_ai/themes_crew/omega_theme/config/omega_theme_agents.yaml'
	tasks_config_path = 'src/ats_pass_ai/themes_crew/omega_theme/config/omega_theme_tasks.yaml'
	tasks_config = tasks_config_path # because tasks_config somehow getting recognized as a dictionary, not a simple string path.

	# agentops.init(tags=["resume-crew"])
	debugFlag = False

	genAI = GoogleGenerativeAI(
		model="gemini-pro",
		temperature=0.5,
		safety_settings = {
			HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
			HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
			HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
			HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
		},
	)

	small_limiter = Limiter(llm_size='SMALL', llm = genAI, langchainMethods=True)

	# rpd, rpm limiter, these will be used on agents
	small_llm_limiter = small_limiter.request_limiter

	# token limiter, these will be used on the tasks to limit the token usage.
	small_token_limiter = small_limiter.record_token_usage

	debugFlag = False
	# debugFlag = True

	def latex_maker_agent(self) -> Agent:
		# load yaml
		yaml = self.yaml_loader("latex_maker_agent", False)
		return Agent(
			role=yaml[0],
			goal=yaml[1],
			backstory=yaml[2],
			allow_delegation=False,
			verbose=True,
			llm=self.genAI,
			step_callback=self.small_llm_limiter,
		)

	def namesection(self):

		yaml = self.yaml_loader("namesection", True)
		description = yaml[0]
		expected_output = yaml[1]
		description = description + "\n\n" + self.load_file(PATHS["personal_information_extraction_task"])

		return Task(
			description=description,
			expected_output=expected_output,
			agent=self.latex_maker_agent(),
			output_file=PATHS["namesection"],
			callback=self.small_token_limiter
		)
	
	def educationsection(self):
		yaml = self.yaml_loader("educationsection", True)
		description = yaml[0]
		expected_output = yaml[1]
		description = description + "\n\n" + self.load_file(PATHS["education_extraction_task"])

		return Task(
			description=description,
			expected_output=expected_output,
			agent=self.latex_maker_agent(),
			output_file=PATHS["educationsection"],
			callback=self.small_token_limiter
		)
	
	def courseworksection(self):
		yaml = self.yaml_loader("courseworksection", True)
		description = yaml[0]
		expected_output = yaml[1]
		description = description + "\n\n" + self.load_file(PATHS["coursework_extraction_task"])

		return Task(
			description=description,
			expected_output=expected_output,
			agent=self.latex_maker_agent(),
			output_file=PATHS["courseworksection"],
			callback=self.small_token_limiter
		)

	def volunteerworksection(self):
		yaml = self.yaml_loader("volunteersection", True)
		description = yaml[0]
		expected_output = yaml[1]
		description = description + "\n\n" + self.load_file(PATHS["volunteer_work_extraction_task"])

		return Task(
			description=description,
			expected_output=expected_output,
			agent=self.latex_maker_agent(),
			output_file=PATHS["volunteersection"],
			callback=self.small_token_limiter
		)
	
	def referencessection(self):
		yaml = self.yaml_loader("referencessection", True)
		description = yaml[0]
		expected_output = yaml[1]
		description = description + "\n\n" + self.load_file(PATHS["references_extraction_task"])

		return Task(
			description=description,
			expected_output=expected_output,
			agent=self.latex_maker_agent(),
			output_file=PATHS["referencessection"],
			callback=self.small_token_limiter
		)
	
	def careerobjectivesection(self):
		yaml = self.yaml_loader("careerobjectivesection", True)
		description = yaml[0]
		expected_output = yaml[1]
		description = description + "\n\n" + self.load_file(PATHS["career_objective_task"])

		return Task(
			description=description,
			expected_output=expected_output,
			agent=self.latex_maker_agent(),
			output_file=PATHS["careerobjectivesection"],
			callback=self.small_token_limiter
		)
	
	def experiencesection(self):
		yaml = self.yaml_loader("experiencesection", True)
		description = yaml[0]
		expected_output = yaml[1]
		description = description + "\n\n" + self.load_file(PATHS["work_experience_extraction_task"]) + "\n\n" + self.load_file(PATHS["project_experience_extraction_task"])

		return Task(
			description=description,
			expected_output=expected_output,
			agent=self.latex_maker_agent(),
			output_file=PATHS["experiencesection"],
			callback=self.small_token_limiter
		)
	def crew(self) -> Crew:
		"""Creates the applicant info organizer crew"""

		# Return the crew
		return Crew(
			agents=[self.latex_maker_agent()],
			tasks=[self.namesection(), self.educationsection(), self.courseworksection(), self.volunteerworksection(), self.referencessection(), self.careerobjectivesection(), self.experiencesection()],
			# tasks=[self.courseworksection()],
			language="en",
			# cache=True,
			full_output=True,
			process=Process.sequential,
			verbose=2,
			# memory=True,
			# embedder={
			# 	"provider": "google",
			# 	"config":{
			# 		"model": 'models/embedding-001',
			# 		"task_type": "retrieval_document",
			# 		"title": "Embeddings for Embedchain"
			# 	}
			# },
			output_log_file='src/ats_pass_ai/themes_crew/omega_theme/output_log.txt',
		)
	
	def load_file(self, file_path):
		"""Load text file"""
		try:
			with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
				return file.read()
		except IOError as e:
			print(f"Error opening or reading the file {file_path}: {e}")
			return False


	def load_all_files(self, directory_path) -> str:
		# Initialize the text
		all_text = ""
		entries = os.listdir(directory_path)
		for entry in entries:
			# Construct full file path
			full_path = os.path.join(directory_path, entry)
			# Open the file and read its contents
			if(os.path.isfile(full_path)):
				try:
					with open(full_path, 'r', encoding='utf-8', errors='ignore') as file:
						all_text += file.read() + "\n"  # Append text with a newline to separate files
				except IOError as e:
					print(f"Error opening or reading the file {full_path}: {e}")
		return all_text

	def yaml_loader(self, item_name, is_task):
		# load the yaml file
		output = []
		if(is_task):
			path = self.tasks_config
		else:
			path = self.agents_config
		try:
			with open (path, 'r') as file:
				yaml_data = yaml.safe_load(file)
				if(is_task):
					output.append(yaml_data[item_name]['description'])
					output.append(yaml_data[item_name]['expected_output'])
				else:
					output.append(yaml_data[item_name]['role'])
					output.append(yaml_data[item_name]['goal'])
					output.append(yaml_data[item_name]['backstory'])
		except IOError as e:
			print(f"Error opening or reading the file {path}: {e}")
		
		return output
	
	def profile_already_created(self) -> bool:
		"""
		Inside the rag_search_tool.py file, there is a function called file_indexed_before. It checks if the applicant info has been changed or not by looking at hash value. If changed, then all the files inside the info_extraction folder will be deleted.

		So we can check if profile has been already created by looking for files inside the info_extraction folder. 

		Check if there are any files in the 'info_extraction' folder.
		This function returns True if there are any files, and False otherwise.
		"""
		path = PATHS["info_extraction_folder_path"]
		entries = os.listdir(path)
		
		# Loop through each entry in the directory
		for entry in entries:
			full_path = os.path.join(path, entry)  # Get the full path of the entry
			if os.path.isfile(full_path):  # Check if it is a file
				# if a single file found, then I am assuming that the profile is already created.
				return True
		return False
	
	def load_paths(self, paths) -> str:
		"""Load text from multiple files"""
		all_text = ""
		for path in paths:
			file_content = self.load_file(PATHS[paths])
			if isinstance(file_content, str):  # Ensure the content is a string	
				all_text += file_content + "\n"
			else:
				print(f"Expected a string from {path}, but got a {type(file_content)}")
		return all_text