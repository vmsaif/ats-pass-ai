# -*- coding: utf-8 -*-
"""
	Author: Saif Mahmud
	Date: 04-23-2024
	Description: This file contains the crew class for the user info organizer crew.
"""

import datetime
import os
import yaml
from langchain_google_genai import GoogleGenerativeAI, HarmBlockThreshold, HarmCategory
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import agentops
from langchain_community.tools import DuckDuckGoSearchRun
from ats_pass_ai.request_limiter import RequestLimiter
from ats_pass_ai.tools.rag_search_tool import SearchInChromaDB
from ats_pass_ai.output_file_paths import PATHS

@CrewBase
class ResumeCrew:
	"""Resume Maker Crew"""
	agents_config = 'config/agents.yaml'
	tasks_config_path = 'config/tasks.yaml'
	tasks_config = tasks_config_path # because tasks_config somehow getting recognized as a dictionary, not a simple string path.

	agentops.init(tags=["resume-crew"])

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

	small_llm_limiter = RequestLimiter(llm_size='SMALL').run
	large_llm_limiter = RequestLimiter(llm_size='LARGE').run

	@crew
	def crew(self) -> Crew:
		"""Creates the user info organizer crew"""

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

		# # Either way, these tasks will be executed.
		
		my_tasks.append(self.ats_friendly_skills_task())
		my_tasks.append(self.split_context_of_ats_friendly_skills_task())

		my_tasks.append(self.experience_choosing_task())
		my_tasks.append(self.split_context_of_experience_choosing_task())
		my_tasks.append(self.gather_info_of_chosen_experiences())
		my_tasks.append(self.ats_friendly_keywords_into_experiences_task())
		my_tasks.append(self.split_context_of_ats_friendly_keywords_into_experiences())

		my_tasks.append(self.coursework_extraction_task())
		my_tasks.append(self.career_objective_task())

		# my_tasks.append(self.resume_in_json_task())
		# my_tasks.append(self.resume_compilation_task())
		

		
		# Return the crew
		return Crew(
			# max_rpm=10,
			agents=[self.generalist_agent()],
			tasks=my_tasks,
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
			step_callback=self.large_llm_limiter,
			function_calling_llm=self.genAI,
			llm=self.genAILarge,
			verbose=True,
		)
	
	@agent
	def resume_compilation_agent(self) -> Agent:
		return Agent(
			config=self.agents_config["resume_compilation_agent"],
			# max_rpm=2,
			step_callback=self.large_llm_limiter,
			allow_delegation=False,
			verbose=True,
			# cache=True,
			llm=self.genAILarge,
			function_calling_llm=self.genAI,
		)

	# ---------------------- Define the tasks ----------------------

	@task
	def personal_information_extraction_task(self):
		return Task(
			config=self.tasks_config["personal_information_extraction_task"],
			agent=self.generalist_agent(),
			output_file=PATHS["personal_information_extraction_task"],
			tools=[self.queryTool],
		)
	
	@task
	def education_extraction_task(self):
		return Task(
			config=self.tasks_config["education_extraction_task"],
			agent=self.generalist_agent(),
			output_file=PATHS["education_extraction_task"],
			tools=[self.queryTool],
		)
 
	@task
	def volunteer_work_extraction_task(self):
		return Task(
			config=self.tasks_config["volunteer_work_extraction_task"],
			agent=self.generalist_agent(),
			output_file=PATHS["volunteer_work_extraction_task"],
			tools=[self.queryTool],
		)

	@task
	def awards_recognitions_extraction_task (self):
		return Task(
			config=self.tasks_config["awards_recognitions_extraction_task"],
			agent=self.generalist_agent(),
			output_file=PATHS["awards_recognitions_extraction_task"],
			tools=[self.queryTool],
		)
 
	@task
	def references_extraction_task(self):
		return Task(
			config=self.tasks_config["references_extraction_task"],
			agent=self.generalist_agent(),
			output_file=PATHS["references_extraction_task"],
			tools=[self.queryTool],
		)
	
	@task
	def personal_traits_interests_extraction_task(self):
		return Task(
			config=self.tasks_config["personal_traits_interests_extraction_task"],
			agent=self.generalist_agent(),
			output_file=PATHS["personal_traits_interests_extraction_task"],
			tools=[self.queryTool],
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
		)

	@task
	def coursework_extraction_task(self):
		return Task(
			config=self.tasks_config["coursework_extraction_task"],
			agent=self.generalist_agent(),
			output_file=PATHS["coursework_extraction_task"],
			tools=[self.queryTool],
		)

	@task
	def work_experience_extraction_task(self):
		
		yaml = self.yaml_loader('work_experience_extraction_task')
		user_info_organized_data = self.load_txt_file(PATHS["user_info_organized"])

		task_description = yaml[0].format(user_info_organized_data = user_info_organized_data)
		expected_output = yaml[1]

		return Task(
			description = task_description,
			expected_output = expected_output,
			agent=self.generalist_agent(),
			output_file=PATHS["work_experience_extraction_task"],
		)

	@task
	def project_experience_extraction_task(self):

		# Load YAML file
		yaml = self.yaml_loader('project_experience_extraction_task')
		user_info_organized_data = self.load_txt_file(PATHS["user_info_organized"])

		task_description = yaml[0].format(user_info_organized_data = user_info_organized_data)
		expected_output = yaml[1]

		return Task(
			description=task_description,
			expected_output=expected_output,
			agent=self.generalist_agent(),
			output_file=PATHS["project_experience_extraction_task"],
		)
	
	@task
	def skills_from_exp_and_project_task(self):
		return Task(
			config=self.tasks_config["skills_from_exp_and_project_task"],
			agent=self.technical_details_agent(),
			context=[self.work_experience_extraction_task(), self.project_experience_extraction_task()],
			
			output_file=PATHS["skills_from_exp_and_project"],
		)

	@task
	def skills_extraction_task(self):

		yaml = self.yaml_loader('skills_extraction_task')
		description = yaml[0]
		expected_output = yaml[1]

		# description = description + "\n" + self.load_txt_file(PATHS["skills_from_exp_and_project"])

		return Task(
			description=description,
			expected_output=expected_output,
   			agent=self.technical_details_agent(),
			context=[self.skills_from_exp_and_project_task()],
			output_file=PATHS["skills_extraction_task"],
			tools=[self.queryTool, self.webSearchTool],
		)

	# # ----------------- Skills Match Identification -----------------
	
	@task
	def ats_friendly_skills_task(self):
		# Load YAML file
		yaml = self.yaml_loader('ats_friendly_skills_task')
		
		src_1 = self.load_txt_file(PATHS["jd_keyword_extraction"])
		task_description = yaml[0].format(src_1 = src_1)
		expected_output = yaml[1]
		
		# task_description = task_description + "\n" + self.load_txt_file(PATHS["skills_extraction_task"])
		return Task(
			description=task_description,
			expected_output=expected_output,
			agent=self.cross_match_evaluator_with_job_description_agent(),
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

		# task_description = task_description + "\n" + self.load_txt_file(PATHS["reduce_missing_skills_task"])

		return Task(
			description=task_description,
			expected_output=expected_output,
			agent=self.generalist_agent(),
			context=[self.ats_friendly_skills_task()],
			output_file=PATHS["split_context_of_ats_friendly_skills_task"],
		)
	
	# ----------------- End of Skills Match Identification -----------------

	# ----------------- Choose Work/Project Experience -----------------
	@task
	def experience_choosing_task(self):
		# Load YAML file
		yaml = self.yaml_loader('experience_choosing_task')
		
		jd_keyword = self.load_txt_file(PATHS["jd_keyword_extraction"])
		today_date = datetime.date.today().strftime("%B %d, %Y")
		
		task_description = yaml[0].format(jd_keyword = jd_keyword, today_date = today_date)

		# # add the project and work experience data
		# task_description = task_description + "\n" + self.load_txt_file(PATHS["work_experience_extraction_task"]) + "\n" + self.load_txt_file(PATHS["project_experience_extraction_task"])

		expected_output = yaml[1]

		return Task(
			description=task_description,
			expected_output=expected_output,
			agent=self.cross_match_evaluator_with_job_description_agent(),
			context=[self.work_experience_extraction_task(), self.project_experience_extraction_task()],
			output_file=PATHS["experience_choosing_task"],
		)
	
	@task
	def split_context_of_experience_choosing_task(self):

		# TODO: Instead making agent doing this split, use a tool to split the context.
		yaml = self.yaml_loader('split_context_of_experience_choosing_task')
		task_description = yaml[0]
		expected_output = yaml[1]

		# task_description = task_description + "\n" + self.load_txt_file(PATHS["experience_choosing_task"])
		
		return Task(
			description=task_description,
			expected_output=expected_output,
			agent=self.generalist_agent(),
			context=[self.experience_choosing_task()],
			output_file=PATHS["split_context_of_experience_choosing_task"],
		)

	# ----------------- End of Choose Work/Project Experience -----------------

	# ----------------- Include ATS Keywords into Experiences -----------------

	# @task
	def gather_info_of_chosen_experiences(self):
		# Load YAML file
		yaml = self.yaml_loader('gather_info_of_chosen_experiences')

		# Load the user info organized data
		user_info_organized_data = self.load_txt_file(PATHS["user_info_organized"])
		task_description = yaml[0].format(user_info_organized_data = user_info_organized_data)
		expected_output = yaml[1]

		task_description = task_description + "\nChosen Experiences for the resume:\n" + self.load_txt_file(PATHS["split_context_of_experience_choosing_task"])

		return Task(
			description=task_description,
			expected_output=expected_output,
			agent=self.generalist_agent(),
			# context=[self.split_context_of_experience_choosing_task()],
			output_file=PATHS["gather_info_of_chosen_experiences"],
		)

	@task
	def ats_friendly_keywords_into_experiences_task(self):
		# Load YAML file
		yaml = self.yaml_loader('ats_friendly_keywords_into_experiences')
		jd_keywords = self.load_txt_file(PATHS["jd_keyword_extraction"])
		task_description = yaml[0].format(jd_keywords = jd_keywords)
		expected_output = yaml[1]

		# add gathered info of chosen experiences
		task_description = task_description + "\nChosen Experiences for the resume:\n" + self.load_txt_file(PATHS["gather_info_of_chosen_experiences"])
		return Task(
			description=task_description,
			expected_output=expected_output,
			agent=self.ats_keyword_integration_agent(),
			# context=[self.gather_info_of_chosen_experiences()],
			output_file=PATHS["ats_friendly_keywords_into_experiences"],
		)

	@task
	def split_context_of_ats_friendly_keywords_into_experiences(self):
		# TODO: Instead making agent doing this split, use a tool to split the context.

		yaml = self.yaml_loader('split_context_of_ats_friendly_keywords_into_experiences')
		task_description = yaml[0]
		expected_output = yaml[1]

		task_description = task_description + "\n" + self.load_txt_file(PATHS["ats_friendly_keywords_into_experiences"])
		return Task(
			description=task_description,
			expected_output=expected_output,
			agent=self.generalist_agent(),
			# context=[self.ats_friendly_keywords_into_experiences_task()],
			output_file=PATHS["split_context_of_ats_friendly_keywords_into_experiences"],
		)
	
	@task
	def career_objective_task(self):
		# Load YAML file
		yaml = self.yaml_loader('career_objective_task')

		job_description = self.load_txt_file(PATHS["jd_keyword_extraction"])
		task_description = yaml[0].format(job_description = job_description)
		expected_output = yaml[1]

		return Task(
			description=task_description,
			expected_output=expected_output,
			agent=self.career_objective_agent(),
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
			data = self.load_all_txt_files(PATHS["info_extraction_folder_path"])
			description = description + "\n" + data
			print("---------------Profile loaded successfully. Input Provided:--------------")
			# print(description)
		else :	
			# need to build profile from scratch
			# insert the profile_builder_task at the beginning of the context
			print("Profile not found. Will wait for the profile to be built.")
			context.insert(0, self.profile_builder_task()) 

		return Task(
			description = description,
			expected_output = expected_output,
			agent = self.resume_in_json_agent(),
			context = context,
			output_file = PATHS["resume_in_json_task"],
		)
	
	@task
	def resume_compilation_task(self):
		# load the yaml file
		yaml = self.yaml_loader('resume_compilation_task')

		# resume_json_data = self.load_txt_files(self.resume_in_json_file_path)
		# description = yaml[0] + '\n' + resume_json_data
		# print("Description: ", description)

		description = yaml[0]
		expected_output = yaml[1]

		return Task(
			description=description,
			expected_output=expected_output,
			agent=self.resume_compilation_agent(),
			context=[self.resume_in_json_task()],
			output_file=PATHS["resume_compilation_task"],
		)
	
	def load_txt_file(self, file_path):
		"""Load text file"""
		with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
			return file.read()

	def load_all_txt_files(self, folder_path) -> str:
		# Initialize the text
		all_text = ""
		for filename in os.listdir(folder_path):
			if filename.endswith('.txt'):
				# Construct full file path
				file_path = os.path.join(folder_path, filename)
				# Open the file and read its contents
				with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
					all_text += file.read() + "\n"  # Append text with a newline to separate files
		return all_text

	def yaml_loader(self, task_name):
		# load the yaml file
		output = []
		with open(f'src/ats_pass_ai/{self.tasks_config_path}', 'r') as file:
			yaml_data = yaml.safe_load(file)
			output.append(yaml_data[task_name]['description'])
			output.append(yaml_data[task_name]['expected_output'])
		return output
	
	def profile_already_created(self) -> bool:
		"""
		Inside the rag_search_tool.py file, there is a function called file_indexed_before. It checks if the user info has been changed or not by looking at hash value. If changed, then all the files inside the info_extraction folder will be deleted.

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
	