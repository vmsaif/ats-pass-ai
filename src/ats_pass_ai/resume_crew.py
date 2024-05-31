# -*- coding: utf-8 -*-
"""
	Author: Saif Mahmud
	Date: 04-23-2024
	Description: This file contains the crew class for the applicant info organizer crew.
"""

import datetime
import os
import yaml
import agentops
from langchain_google_genai import GoogleGenerativeAI, HarmBlockThreshold, HarmCategory
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from langchain_community.tools import DuckDuckGoSearchRun
from ats_pass_ai.limiter import Limiter
from ats_pass_ai.tools.rag_search_tool import SearchInChromaDB
from ats_pass_ai.output_file_paths import PATHS

@CrewBase
class ResumeCrew:
	"""Resume Maker Crew"""
	agents_config = 'config/agents.yaml'
	tasks_config_path = 'config/tasks.yaml'
	tasks_config = tasks_config_path # because tasks_config somehow getting recognized as a dictionary, not a simple string path.

	# agentops.init(tags=["resume-crew"])

	debugFlag = False

	# Define the tools
	queryTool = SearchInChromaDB().search # passing the function reference, not calling the function

	webSearchTool = DuckDuckGoSearchRun()
	
	safety_settings = {
		HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
		HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
		HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
		HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
	}
	
	genAI = GoogleGenerativeAI(
		model="gemini-pro",
		# max_output_tokens=8192,
		temperature=1.0,
		safety_settings=safety_settings,
	)

	genAILarge = GoogleGenerativeAI(
		model="gemini-1.5-pro-latest",
		# max_output_tokens=8192,
		temperature=1.0,
		safety_settings=safety_settings,
	)

	small_limiter = Limiter(llm_size='SMALL', llm = genAI, langchainMethods=True)
	large_limiter = Limiter(llm_size='LARGE', llm = genAILarge, langchainMethods=True)

	# rpd, rpm limiter, these will be used on agents
	small_llm_limiter = small_limiter.request_limiter
	large_llm_limiter = large_limiter.request_limiter

	# token limiter, these will be used on the tasks to limit the token usage.
	small_token_limiter = small_limiter.record_token_usage
	large_token_limiter = large_limiter.record_token_usage

	debugFlag = False
	# debugFlag = True

	@crew
	def crew(self) -> Crew:
		"""Creates the applicant info organizer crew"""

		my_tasks = []
	
		# if needs to change here, remember to change in the resume_in_json_task as well.
		if(not self.profile_already_created()):
			my_tasks.append(self.personal_information_extraction_task())
			my_tasks.append(self.education_extraction_task())
			my_tasks.append(self.volunteer_work_extraction_task())
			my_tasks.append(self.awards_recognitions_extraction_task())
			my_tasks.append(self.references_extraction_task())
			my_tasks.append(self.personal_traits_interests_extraction_task())
			my_tasks.append(self.work_experience_extraction_task())
			my_tasks.append(self.project_experience_extraction_task())
			my_tasks.append(self.skills_from_exp_and_project_task())
			my_tasks.append(self.skills_extraction_task())

			my_tasks.append(self.profile_builder_task())

		# Either way, these tasks will be executed.
		my_tasks.append(self.ats_friendly_skills_task())
		my_tasks.append(self.split_context_of_ats_friendly_skills_task())

		my_tasks.append(self.experience_choosing_task())
		my_tasks.append(self.split_context_of_experience_choosing_task())
		my_tasks.append(self.gather_info_of_chosen_experiences())
		my_tasks.append(self.ats_friendly_keywords_into_experiences_task())
		my_tasks.append(self.split_context_of_ats_friendly_keywords_into_experiences())

		my_tasks.append(self.coursework_extraction_task())
		my_tasks.append(self.career_objective_task())

		my_tasks.append(self.resume_in_json_task())
		my_tasks.append(self.resume_compilation_task())
		my_tasks.append(self.latex_resume_generation_task())
		my_tasks.append(self.cover_letter_generation_task())
				
		# Return the crew
		return Crew(
			# max_rpm=10,
			agents=self.agents,
			tasks=my_tasks,
			language="en",
			# cache=True,
			full_output=True,
			process=Process.sequential,
			# process=Process.hierarchical,
			# manager_llm=self.composerLLM,
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
			output_log_file='output_log.txt',
		)

	@agent
	def skills_compatibility_analyst_agent(self) -> Agent:
		return Agent(
			config=self.agents_config["skills_compatibility_analyst_agent"],
			allow_delegation=False,
			verbose=True,
			# cache=True,
			llm=self.genAI,
			# function_calling_llm = self.genAI,
			# step_callback=self.large_llm_limiter
			step_callback=self.small_llm_limiter
		)

	@agent
	def generalist_agent(self) -> Agent:
		return Agent(
			config=self.agents_config["generalist_agent"],
			allow_delegation=False,
			# cache=True,
			verbose=True,
			llm=self.genAI,
			step_callback=self.small_llm_limiter
		)
	
	@agent
	def technical_details_agent(self) -> Agent:
		return Agent(
			config=self.agents_config["technical_details_agent"],
			allow_delegation=False,
			verbose=True,
			# cache=True,
			llm=self.genAI,
			step_callback=self.small_llm_limiter
		)

	@agent
	def career_objective_agent(self) -> Agent:
		return Agent(
			config=self.agents_config["career_objective_agent"],
			# max_rpm=1,
			allow_delegation=False,
			verbose=True,
			# cache=True,
			llm=self.genAILarge,
			function_calling_llm=self.genAI,
			step_callback=self.large_llm_limiter,
			tools=[self.queryTool],
		)

	@agent
	def cross_match_evaluator_with_job_description_agent (self) -> Agent:
		return Agent(
			config=self.agents_config["cross_match_evaluator_with_job_description_agent"],
			step_callback=self.large_llm_limiter,
			allow_delegation=False,
			verbose=True,
			function_calling_llm=self.genAI,
			# cache=True,
			llm=self.genAILarge,
		)
	
	@agent
	def ats_keyword_integration_agent(self) -> Agent:
		return Agent(
			config=self.agents_config["ats_keyword_integration_agent"],
			verbose=True,
			# max_rpm=1,
			step_callback=self.large_llm_limiter,
			function_calling_llm=self.genAI,
			allow_delegation=False,
			# cache=True,
			llm=self.genAILarge
		)
	
	@agent
	def resume_in_json_agent(self) -> Agent:
		return Agent(
			config=self.agents_config["resume_in_json_agent"],
			allow_delegation=False,
			# max_rpm=1,
			# step_callback=self.large_llm_limiter,
			llm=self.genAILarge,
			step_callback = self.small_llm_limiter,
			function_calling_llm=self.genAI,
			verbose=True,
		)
	
	@agent
	def resume_compilation_agent(self) -> Agent:
		return Agent(
			config=self.agents_config["resume_compilation_agent"],
			llm=self.genAI,
			# step_callback=self.large_llm_limiter,
			step_callback=self.small_llm_limiter,
			function_calling_llm=self.genAI,
			allow_delegation=False,
			verbose=True,
			# cache=True,
		)
	
	@agent
	def latex_resume_agent(self) -> Agent:
		return Agent(
			config=self.agents_config["latex_resume_agent"],
			allow_delegation=False,
			verbose=True,
			# cache=True,
			llm=self.genAILarge,
			step_callback=self.large_llm_limiter
			# step_callback=self.small_llm_limiter,
			# llm=self.genAI
		)
	
	@agent
	def cover_letter_generation_agent(self) -> Agent:
		return Agent(
			config=self.agents_config["cover_letter_generation_agent"],
			allow_delegation=False,
			verbose=True,
			function_calling_llm=self.genAI,
			# cache=True,
			llm=self.genAILarge,
			step_callback=self.large_llm_limiter
			# step_callback=self.small_llm_limiter,
			# llm=self.genAI
		)

	# ---------------------- Define the tasks ----------------------

	@task
	def cover_letter_generation_task(self):
		# Load YAML file
		yaml = self.yaml_loader('cover_letter_generation_task')
		description = yaml[0]
		expected_output = yaml[1]

		today_date = datetime.date.today().strftime("%B %d, %Y")

		
		# add the job description extracted keywords
		description = description + f'\n Today\'s Date:{today_date}\n' + self.load_file(PATHS["job_description"]) 

		context = []

		# Either way these context is needed to complete the task.

		context.append(self.split_context_of_ats_friendly_skills_task())
		context.append(self.coursework_extraction_task())
		context.append(self.split_context_of_ats_friendly_keywords_into_experiences())
		context.append(self.career_objective_task())

		if(self.profile_already_created()):

			print("Profile already found. Simply loading the output txt files in the context for the cover letter generation.")
			# load the output txt files and append to the yaml[0] in new paragraph, No need to build profile from scratch.
			description = description + "\n" + self.load_file(PATHS["profile_builder_task"])
			
		else :	
			# insert the profile_builder_task at the beginning of the context
			print("Profile not found. Will wait for the profile to be built.")
			context.insert(0, self.profile_builder_task()) 

		if(self.debugFlag):
			paths = [
				"split_context_of_ats_friendly_skills_task",
				"coursework_extraction_task",
				"split_context_of_ats_friendly_keywords_into_experiences",
				"career_objective_task",
				"profile_builder_task"
			]
			description = description + "\n" + self.load_paths(paths)

		print
		return Task(
			description=description,
			expected_output=expected_output,
			context=context,
			agent=self.cover_letter_generation_agent(),
			output_file=PATHS["cover_letter_generation_task"],
			callback = self.large_token_limiter
		)

	@task
	def latex_resume_generation_task(self):

		# Note the the output of this task gets sanitized by latex_generator.py file.
		# Load YAML file
		yaml = self.yaml_loader('latex_resume_generation_task')
		description = yaml[0]
		expected_output = yaml[1]

		if(self.debugFlag):
			description = description + "\n" + self.load_file(PATHS["resume_in_json_task"])
			
		return Task(
			description=description,
			expected_output=expected_output,
			agent=self.latex_resume_agent(),
			output_file=PATHS["latex_resume_generation_task"],
			callback = self.large_token_limiter
		)

	@task
	def personal_information_extraction_task(self):
		return Task(
			config=self.tasks_config["personal_information_extraction_task"],
			agent=self.generalist_agent(),
			output_file=PATHS["personal_information_extraction_task"],
			tools=[self.queryTool],
			callback=self.small_token_limiter	
		)

	@task
	def education_extraction_task(self):
		return Task(
			config=self.tasks_config["education_extraction_task"],
			agent=self.generalist_agent(),
			output_file=PATHS["education_extraction_task"],
			tools=[self.queryTool],
			callback=self.small_token_limiter
		)
 
	@task
	def volunteer_work_extraction_task(self):
		return Task(
			config=self.tasks_config["volunteer_work_extraction_task"],
			agent=self.generalist_agent(),
			output_file=PATHS["volunteer_work_extraction_task"],
			tools=[self.queryTool],
			callback=self.small_token_limiter
		)

	@task
	def awards_recognitions_extraction_task (self):
		return Task(
			config=self.tasks_config["awards_recognitions_extraction_task"],
			agent=self.generalist_agent(),
			output_file=PATHS["awards_recognitions_extraction_task"],
			tools=[self.queryTool],
			callback=self.small_token_limiter
		)
 
	@task
	def references_extraction_task(self):
		return Task(
			config=self.tasks_config["references_extraction_task"],
			agent=self.generalist_agent(),
			output_file=PATHS["references_extraction_task"],
			tools=[self.queryTool],
			callback=self.small_token_limiter
		)
	
	@task
	def personal_traits_interests_extraction_task(self):
		return Task(
			config=self.tasks_config["personal_traits_interests_extraction_task"],
			agent=self.generalist_agent(),
			output_file=PATHS["personal_traits_interests_extraction_task"],
			tools=[self.queryTool],
			callback=self.small_token_limiter
		)
	
	@task
	def profile_builder_task(self):
		
		context = []
		
		context.append(self.personal_information_extraction_task())
		context.append(self.education_extraction_task())
		context.append(self.volunteer_work_extraction_task())
		context.append(self.awards_recognitions_extraction_task())
		context.append(self.references_extraction_task())
		context.append(self.personal_traits_interests_extraction_task())
		
		return Task(
			config=self.tasks_config["profile_builder_task"],
			agent=self.generalist_agent(),
			context=context,
			output_file=PATHS["profile_builder_task"],
			callback=self.small_token_limiter
		)

	@task
	def coursework_extraction_task(self):
		return Task(
			config=self.tasks_config["coursework_extraction_task"],
			agent=self.generalist_agent(),
			output_file=PATHS["coursework_extraction_task"],
			tools=[self.queryTool],
			callback=self.small_token_limiter
		)

	@task
	def work_experience_extraction_task(self):
		
		yaml = self.yaml_loader('work_experience_extraction_task')
		applicant_info_organized_data = self.load_file(PATHS["applicant_info_organized"])

		task_description = yaml[0].format(applicant_info_organized_data = applicant_info_organized_data)
		expected_output = yaml[1]

		return Task(
			description = task_description,
			expected_output = expected_output,
			agent=self.generalist_agent(),
			output_file=PATHS["work_experience_extraction_task"],
			callback=self.small_token_limiter
		)

	@task
	def project_experience_extraction_task(self):

		# Load YAML file
		yaml = self.yaml_loader('project_experience_extraction_task')
		applicant_info_organized_data = self.load_file(PATHS["applicant_info_organized"])

		task_description = yaml[0].format(applicant_info_organized_data = applicant_info_organized_data)
		expected_output = yaml[1]

		return Task(
			description=task_description,
			expected_output=expected_output,
			agent=self.generalist_agent(),
			output_file=PATHS["project_experience_extraction_task"],
			callback=self.small_token_limiter
		)
	
	@task
	def skills_from_exp_and_project_task(self):
		return Task(
			config=self.tasks_config["skills_from_exp_and_project_task"],
			agent=self.technical_details_agent(),
			context=[self.work_experience_extraction_task(), self.project_experience_extraction_task()],
			output_file=PATHS["skills_from_exp_and_project"],
			callback=self.small_token_limiter
		)

	@task
	def skills_extraction_task(self):

		yaml = self.yaml_loader('skills_extraction_task')
		description = yaml[0]
		expected_output = yaml[1]

		if(self.debugFlag):
			description = description + "\n" + self.load_file(PATHS["skills_from_exp_and_project"])
			
		return Task(
			description=description,
			expected_output=expected_output,
   			agent=self.technical_details_agent(),
			context=[self.skills_from_exp_and_project_task()],
			output_file=PATHS["skills_extraction_task"],
			tools=[self.queryTool],
			callback=self.small_token_limiter
		)

	# # ----------------- Skills Match Identification -----------------
	
	@task
	def ats_friendly_skills_task(self):
		# Load YAML file
		yaml = self.yaml_loader('ats_friendly_skills_task')
		
		src_1 = self.load_file(PATHS["jd_keyword_extraction"])
		task_description = yaml[0].format(src_1 = src_1)
		expected_output = yaml[1]
		
		if(self.debugFlag):
			task_description = task_description + "\n" + self.load_file(PATHS["skills_extraction_task"])
		return Task(
			description=task_description,
			expected_output=expected_output,
			agent=self.cross_match_evaluator_with_job_description_agent(),
			callback=self.large_token_limiter,
			context=[self.skills_extraction_task()],
			tools=[self.webSearchTool],
			output_file=PATHS["ats_friendly_skills_task"],
		)
	
	@task
	def split_context_of_ats_friendly_skills_task(self):
		# Load YAML file
		yaml = self.yaml_loader('split_context_of_ats_friendly_skills_task')
		task_description = yaml[0]
		expected_output = yaml[1]

		if(self.debugFlag):
			task_description = task_description + "\n" + self.load_file(PATHS["ats_friendly_skills_task"])

		return Task(
			description=task_description,
			expected_output=expected_output,
			agent=self.generalist_agent(),
			context=[self.ats_friendly_skills_task()],
			output_file=PATHS["split_context_of_ats_friendly_skills_task"],
			callback=self.small_token_limiter			
		)
	
	# ----------------- End of Skills Match Identification -----------------

	# ----------------- Choose Work/Project Experience -----------------
	@task
	def experience_choosing_task(self):
		# Load YAML file
		yaml = self.yaml_loader('experience_choosing_task')
		
		jd_keyword = self.load_file(PATHS["jd_keyword_extraction"])
		today_date = datetime.date.today().strftime("%B %d, %Y")
		
		task_description = yaml[0].format(jd_keyword = jd_keyword, today_date = today_date)

		# # add the project and work experience data
		if(self.debugFlag):
			task_description = task_description + "\n" + self.load_file(PATHS["work_experience_extraction_task"]) + "\n" + self.load_file(PATHS["project_experience_extraction_task"])

		expected_output = yaml[1]

		return Task(
			description=task_description,
			expected_output=expected_output,
			agent=self.cross_match_evaluator_with_job_description_agent(),
			callback=self.large_token_limiter,
			context=[self.work_experience_extraction_task(), self.project_experience_extraction_task()],
			output_file=PATHS["experience_choosing_task"],
		)
	
	@task
	def split_context_of_experience_choosing_task(self):

		# TODO: Instead making agent doing this split, use a tool to split the context.
		yaml = self.yaml_loader('split_context_of_experience_choosing_task')
		task_description = yaml[0]
		expected_output = yaml[1]

		if(self.debugFlag):
			task_description = task_description + "\n" + self.load_file(PATHS["experience_choosing_task"])
		
		return Task(
			description=task_description,
			expected_output=expected_output,
			agent=self.generalist_agent(),
			context=[self.experience_choosing_task()],
			output_file=PATHS["split_context_of_experience_choosing_task"],
			callback=self.small_token_limiter
		)

	# ----------------- End of Choose Work/Project Experience -----------------

	# ----------------- Include ATS Keywords into Experiences -----------------

	@task
	def gather_info_of_chosen_experiences(self):
		# Load YAML file
		yaml = self.yaml_loader('gather_info_of_chosen_experiences')

		# Load the applicant info organized data
		applicant_info_organized_data = self.load_file(PATHS["applicant_info_organized"])
		
		task_description = yaml[0].format(applicant_info_organized_data = applicant_info_organized_data)
		expected_output = yaml[1]

		if(self.debugFlag):
			task_description = task_description + "\nChosen Experiences for the resume:\n" + self.load_file(PATHS["split_context_of_experience_choosing_task"])

		return Task(
			description=task_description,
			expected_output=expected_output,
			agent=self.generalist_agent(),
			context=[self.split_context_of_experience_choosing_task()],
			output_file=PATHS["gather_info_of_chosen_experiences"],
			callback=self.small_token_limiter	
		)

	@task
	def ats_friendly_keywords_into_experiences_task(self):
		# Load YAML file
		yaml = self.yaml_loader('ats_friendly_keywords_into_experiences')
		jd_keywords = self.load_file(PATHS["jd_keyword_extraction"])

		today_date = datetime.date.today().strftime("%B %d, %Y")
		task_description = yaml[0].format(jd_keywords = jd_keywords, today_date = today_date)
		expected_output = yaml[1]

		# add gathered info of chosen experiences
		if(self.debugFlag):
			task_description = task_description + "\nChosen Experiences for the resume:\n" + self.load_file(PATHS["gather_info_of_chosen_experiences"])

		return Task(
			description=task_description,
			expected_output=expected_output,
			agent=self.ats_keyword_integration_agent(),
			callback=self.large_token_limiter,
			context=[self.gather_info_of_chosen_experiences()],
			output_file=PATHS["ats_friendly_keywords_into_experiences"],
		)

	@task
	def split_context_of_ats_friendly_keywords_into_experiences(self):
		# TODO: Instead making agent doing this split, use a tool to split the context.

		yaml = self.yaml_loader('split_context_of_ats_friendly_keywords_into_experiences')
		task_description = yaml[0]
		expected_output = yaml[1]

		# task_description = task_description + "\n" + self.load_file(PATHS["ats_friendly_keywords_into_experiences"])
		return Task(
			description=task_description,
			expected_output=expected_output,
			agent=self.generalist_agent(),
			context=[self.ats_friendly_keywords_into_experiences_task()],
			output_file=PATHS["split_context_of_ats_friendly_keywords_into_experiences"],
			callback=self.small_token_limiter
		)
	
	@task
	def career_objective_task(self):
		# Load YAML file
		yaml = self.yaml_loader('career_objective_task')

		job_description = self.load_file(PATHS["jd_keyword_extraction"])
		task_description = yaml[0].format(job_description = job_description)
		expected_output = yaml[1]

		return Task(
			description=task_description,
			expected_output=expected_output,
			agent=self.career_objective_agent(),
			callback=self.large_token_limiter,
			context=[self.split_context_of_ats_friendly_skills_task(), self.split_context_of_ats_friendly_keywords_into_experiences()],
			output_file=PATHS["career_objective_task"],
		)

	@task
	def resume_in_json_task(self):

		context = []

		# Either way these context is needed to complete the task.

		context.append(self.split_context_of_ats_friendly_skills_task())
		context.append(self.coursework_extraction_task())
		context.append(self.split_context_of_ats_friendly_keywords_into_experiences())
		context.append(self.career_objective_task())

		# Load YAML file
		yaml = self.yaml_loader('resume_in_json_task')
		
		# append data to the yaml[0] in new paragraph
		description = yaml[0]
		description = description.format(today_date = datetime.date.today().strftime("%B %d, %Y"))
		expected_output = yaml[1]

		if(self.profile_already_created()):

			print("Profile already found. Simply loading the output txt files in the context.")
			# load the output txt files and append to the yaml[0] in new paragraph, No need to build profile from scratch.
			description = description + "\n" + self.load_file(PATHS["profile_builder_task"])
		else :	
			# need to build profile from scratch
			# insert the profile_builder_task at the beginning of the context
			print("Profile not found. Will wait for the profile to be built.")
			context.insert(0, self.profile_builder_task()) 

		return Task(
			description = description,
			expected_output = expected_output,
			agent = self.resume_in_json_agent(),
			callback=self.large_token_limiter,
			context = context,
			output_file = PATHS["resume_in_json_task"],
		)
	
	@task
	def resume_compilation_task(self):
		# load the yaml file
		yaml = self.yaml_loader('resume_compilation_task')
		description = yaml[0]
		expected_output = yaml[1]

		if(self.debugFlag):
			description = yaml[0] + '\n' + self.load_file(PATHS["resume_in_json_task"])

		return Task(
			description=description,
			expected_output=expected_output,
			agent=self.resume_compilation_agent(),
			callback=self.small_token_limiter,
			# agent=self.generalist_agent(),
			context=[self.resume_in_json_task()],
			output_file=PATHS["resume_compilation_task"],

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

	def yaml_loader(self, task_name):
		# load the yaml file
		output = []
		with open(f'{PATHS["src_root"]}/{self.tasks_config_path}', 'r') as file:
			yaml_data = yaml.safe_load(file)
			output.append(yaml_data[task_name]['description'])
			output.append(yaml_data[task_name]['expected_output'])
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
			file_content = self.load_file(PATHS[path])
			if isinstance(file_content, str):  # Ensure the content is a string	
				all_text += file_content + "\n"
			else:
				print(f"Expected a string from {path}, but got a {type(file_content)}")
		return all_text