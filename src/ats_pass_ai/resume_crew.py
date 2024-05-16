# -*- coding: utf-8 -*-
"""
	Author: Saif Mahmud
	Date: 04-23-2024
	Description: This file contains the crew class for the user info organizer crew.
"""
import datetime
import os

import yaml
from langchain_groq import ChatGroq
from langchain_google_genai import GoogleGenerativeAI, HarmBlockThreshold, HarmCategory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_vertexai import ChatVertexAI
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
# from langchain_openai import ChatOpenAI
# from langchain_google_vertexai import VertexAI # to use codey - code-bison model to generate latex
from ats_pass_ai.tools.crewai_directory_search_tool import CrewAIFileReadTool

from ats_pass_ai.tools.rag_search_tool import SearchInChromaDB

@CrewBase
class ResumeCrew:
	"""Resume Maker Crew"""
	agents_config = 'config/agents.yaml'
	tasks_config_path = 'config/tasks.yaml'
	tasks_config = tasks_config_path # because tasks_config somehow getting recognized as a dictionary, not a simple string path.
	
	# Job Keywords extraction task file path
	jd_keyword_extraction_file_path = 'info_extraction/jd_keyword_extraction/job_description_extracted_keywords.txt' # do not use it inside file_path dictionary below.

	# Info extraction task file paths
	personal_information_extraction_task_file_path = 'info_extraction/personal_information_extraction_task.txt'
	education_extraction_task_file_path = 'info_extraction/education_extraction_task.txt'
	volunteer_work_extraction_task_file_path = 'info_extraction/volunteer_work_extraction_task.txt'
	awards_recognitions_extraction_task_file_path = 'info_extraction/awards_recognitions_extraction_task.txt'
	references_extraction_task_file_path = 'info_extraction/references_extraction_task.txt'
	personal_traits_interests_extraction_task_file_path = 'info_extraction/personal_traits_interests_extraction_task.txt'
	miscellaneous_extraction_task_file_path = 'info_extraction/miscellaneous_extraction_task.txt'

	work_experience_extraction_task_file_path = 'info_extraction/pre_tasks/work_experience_extraction_task.txt'
	project_experience_extraction_task_file_path = 'info_extraction/pre_tasks/project_experience_extraction_task.txt'
	skills_from_exp_and_project_file_path = 'info_extraction/pre_tasks/skills_from_exp_and_project.txt'
	all_togather_skills_extraction_task_file_path = 'info_extraction/pre_tasks/all_togather_skills_extraction_task.txt'
	
	# Cross Checked with JD keywords
	ats_friendly_skills_pre_task_file_path = 'info_extraction/pre_tasks/ats_friendly_skills_task.txt'
	split_context_of_ats_friendly_skills_task_file_path = 'info_extraction/pre_tasks/split_context_of_ats_friendly_skills_task.txt' 
	experience_choosing_task_file_path = 'info_extraction/pre_tasks/experience_choosing_task.txt'
	split_context_of_experience_choosing_task_file_path = 'info_extraction/pre_tasks/split_context_of_experience_choosing_task.txt'
	gather_info_of_choosen_experiences_file_path = 'info_extraction/pre_tasks/gather_info_of_choosen_experiences.txt'
	ats_friendly_keywords_into_experiences_file_path = 'info_extraction/pre_tasks/ats_friendly_keywords_into_experiences.txt'
	split_context_of_ats_friendly_keywords_into_experiences_file_path = 'info_extraction/split_context_of_ats_friendly_keywords_into_experiences.txt'
	career_objective_task_file_path = 'info_extraction/career_objective_task.txt'


	# finalized_resume
	resume_json_file_path = 'info_extraction/draft_output/resume_json.txt'
	resume_compilation_task_file_path = 'info_extraction/draft_output/resume_compilation.txt'

	# Dictionary to store file paths
	file_paths = {

		# "volunteer_work_extraction_task": volunteer_work_extraction_task_file_path,
		# "awards_recognitions_extraction_task": awards_recognitions_extraction_task_file_path,
		# "references_extraction_task": references_extraction_task_file_path,
		# "personal_traits_interests_extraction_task": personal_traits_interests_extraction_task_file_path,
		# "miscellaneous_extraction_task": miscellaneous_extraction_task_file_path,

		# "personal_information_extraction_task": personal_information_extraction_task_file_path,
		# "education_extraction_task": education_extraction_task_file_path,
		
		
		# "work_experience_extraction_task": work_experience_extraction_task_file_path,
		# "project_experience_extraction_task": project_experience_extraction_task_file_path,
		# "skills_from_exp_and_project": skills_from_exp_and_project_file_path,
		# "all_togather_skills_extraction_task": all_togather_skills_extraction_task_file_path,
		
		# "ats_friendly_skills_task": ats_friendly_skills_task_file_path,
		# "experience_choosing_task": experience_choosing_task_file_path,

		# "split_context_of_experience_choosing_task": split_context_of_experience_choosing_task_file_path,

		# "gather_info_of_choosen_experiences": gather_info_of_choosen_experiences_file_path,
		# "include_ats_keywords_into_experiences": ats_friendly_keywords_into_experiences_file_path,
		# "split_context_of_ats_friendly_keywords_into_experiences": split_context_of_ats_friendly_keywords_into_experiences_file_path,
		# "career_objective_task": career_objective_task_file_path,
		# "resume_json_task": resume_json_file_path,
		"resume_compilation_task": resume_compilation_task_file_path,
	}

	# Define the tools
	queryTool = SearchInChromaDB().search # passing the function reference, not calling the function
	jd_extr_keywords_reader = CrewAIFileReadTool.create(jd_keyword_extraction_file_path)
	user_info_organized_reader = CrewAIFileReadTool.create('info_files/user_info_organized.txt')


	safety_settings = {
		HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
		HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
		HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
		HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
	}
	
	genAI = GoogleGenerativeAI(
		model="gemini-pro",
		verbose=True,
		max_output_tokens=6000,
		temperature=1.0,
		safety_settings=safety_settings,
		# cache=True
	)

	genAILarge = ChatVertexAI(
		model="gemini-1.5-pro-preview-0409",
		verbose=True,
		temperature=1.0,
	)

	llama3_70b = ChatGroq(
		model_name="llama3-70b-8192",
		# verbose=True,
		temperature=1.5,
	)

	@agent
	def generalist_agent(self) -> Agent:
		return Agent(
			config=self.agents_config["generalist_agent"],
			verbose=True,
			allow_delegation=False,
			cache=True,
			llm=self.genAI,
		)

	# @task
	# def education_extraction_task(self):
	# 	return Task(
	# 		config=self.tasks_config["education_extraction_task"],
	# 		agent=self.generalist_agent(),
	# 		output_file=self.education_extraction_task_file_path,
	# 		tools=[self.queryTool],
	# 	)
	
	@task
	def personal_information_extraction_task(self):
		return Task(
			config=self.tasks_config["personal_information_extraction_task"],
			agent=self.generalist_agent(),
			output_file=self.personal_information_extraction_task_file_path,
			tools=[self.queryTool],

		)
 
	# @task
	# def volunteer_work_extraction_task(self):
	# 	return Task(
	# 		config=self.tasks_config["volunteer_work_extraction_task"],
	# 		agent=self.generalist_agent(),
	# 		output_file=self.volunteer_work_extraction_task_file_path,
	# 		tools=[self.queryTool],
	# 	)

	# @task
	# def awards_recognitions_extraction_task (self):
	# 	return Task(
	# 		config=self.tasks_config["awards_recognitions_extraction_task"],
	# 		agent=self.generalist_agent(),
	# 		output_file=self.awards_recognitions_extraction_task_file_path,
	# 		tools=[self.queryTool],
	# 	)
 
	# @task
	# def references_extraction_task(self):
	# 	return Task(
	# 		config=self.tasks_config["references_extraction_task"],
	# 		agent=self.generalist_agent(),
	# 		output_file=self.references_extraction_task_file_path,
	# 		tools=[self.queryTool],
	# 	)
	
	# @task
	# def personal_traits_interests_extraction_task(self):
	# 	return Task(
	# 		config=self.tasks_config["personal_traits_interests_extraction_task"],
	# 		agent=self.generalist_agent(),
	# 		output_file=self.personal_traits_interests_extraction_task_file_path,
	# 		tools=[self.queryTool],
	# 	)
	
	# @task
	# def miscellaneous_extraction_task(self):
	# 	return Task(
	# 		config=self.tasks_config["miscellaneous_extraction_task"],
	# 		agent=self.generalist_agent(),
	# 		output_file=self.miscellaneous_extraction_task_file_path,
	# 		tools=[self.queryTool],
	# 	)


	
	# @task
	# def work_experience_extraction_task(self):
	# 	return Task(
	# 		config=self.tasks_config["work_experience_extraction_task"],
	# 		agent=self.generalist_agent(),
	# 		output_file=self.work_experience_extraction_task_file_path,
	# 		tools=[self.user_info_organized_reader],
	# 	)

	# @task
	# def project_experience_extraction_task(self):
	# 	return Task(
	# 		config=self.tasks_config["project_experience_extraction_task"],
	# 		agent=self.generalist_agent(),
	# 		tools=[self.user_info_organized_reader],
	# 		output_file=self.project_experience_extraction_task_file_path,
	# 	)
	
	# @agent
	# def technical_details_agent(self) -> Agent:
	# 	return Agent(
	# 		config=self.agents_config["technical_details_agent"],
	# 		verbose=True,
	# 		allow_delegation=False,
	# 		cache=True,
	# 		llm=self.genAI,
	# 	)
	
	# @task
	# def skills_from_exp_and_project_task(self):
	# 	return Task(
	# 		config=self.tasks_config["skills_from_exp_and_project_task"],
	# 		agent=self.technical_details_agent(),
	# 		context=[self.work_experience_extraction_task(), self.project_experience_extraction_task()],
	# 		output_file=self.skills_from_exp_and_project_file_path,
	# 	)

	# @task
	# def skills_extraction_task(self):
	# 	return Task(
	# 		config=self.tasks_config["skills_extraction_task"],
   	# 		agent=self.technical_details_agent(),
	# 		context=[self.skills_from_exp_and_project_task()],
	# 		output_file=self.all_togather_skills_extraction_task_file_path,
	# 		tools=[self.queryTool],
	# 	)

	# ----------------- Skills Match Identification -----------------





	# @agent
	# def cross_match_evaluator_with_job_description_agent (self) -> Agent:
	# 	return Agent(
	# 		config=self.agents_config["cross_match_evaluator_with_job_description_agent"],
	# 		max_rpm=2,
	# 		verbose=True,
	# 		allow_delegation=False,
	# 		# cache=True,
	# 		llm=self.genAILarge,
	# 	)
	
	@task
	def ats_friendly_skills_task(self):
		# Load YAML file
		with open(f'src/ats_pass_ai/{self.tasks_config_path}', 'r') as file:
			yaml_data = yaml.safe_load(file)
			description_value = yaml_data['ats_friendly_skills_task']['description']
			expected_output = yaml_data['ats_friendly_skills_task']['expected_output']

		src_1 = self.load_txt_files(self.jd_keyword_extraction_file_path)
		task_description = description_value.format(src_1 = src_1)

		return Task(
			description=task_description,
			expected_output=expected_output,
			agent=self.cross_match_evaluator_with_job_description_agent(),
			# context=[self.skills_extraction_task()],
			output_file=self.ats_friendly_skills_pre_task_file_path,
		)
	
	@task
	def split_context_of_ats_friendly_skills_task(self):
		# Load YAML file
		with open(f'src/ats_pass_ai/{self.tasks_config_path}', 'r') as file:
			yaml_data = yaml.safe_load(file)
			description_value = yaml_data['split_context_of_ats_friendly_skills_task']['description']
			expected_output = yaml_data['split_context_of_ats_friendly_skills_task']['expected_output']

		ats_friendly_skills = self.load_txt_files(self.ats_friendly_skills_pre_task_file_path)
		task_description = description_value.format(ats_friendly_skills = ats_friendly_skills)

		return Task(
			description=task_description,
			expected_output=expected_output,
			agent=self.generalist_agent(),
			output_file=self.split_context_of_ats_friendly_skills_task_file_path,
		)


	# ----------------- End of Skills Match Identification -----------------

	# # ----------------- Choose Work/Project Experience -----------------
	# @task
	# def experience_choosing_task(self):
	# 	# Load YAML file
	# 	with open(f'src/ats_pass_ai/{self.tasks_config_path}', 'r') as file:
	# 		yaml_data = yaml.safe_load(file)
	# 		description_value = yaml_data['experience_choosing_task']['description']
	# 		expected_output = yaml_data['experience_choosing_task']['expected_output']

	# 	jd_keyword = self.load_txt_files(self.jd_keyword_extraction_file_path)
	# 	work_experience = self.load_txt_files(self.work_experience_extraction_task_file_path)
	# 	project_experience = self.load_txt_files(self.project_experience_extraction_task_file_path)
	# 	# get date
	# 	today_date = datetime.date.today().strftime("%B %d, %Y")
	# 	task_description = description_value.format(jd_keyword = jd_keyword, work_experience = work_experience, project_experience = project_experience, today_date = today_date)

	# 	return Task(
	# 		description=task_description,
	# 		expected_output=expected_output,
	# 		agent=self.cross_match_evaluator_with_job_description_agent(),
	# 		# context=[self.work_experience_extraction_task(), self.project_experience_extraction_task()],
	# 		output_file=self.experience_choosing_task_file_path,
	# 	)
	
	# @task
	# def split_context_of_experience_choosing_task (self):

	# TODO: Instead making agent doing this split, use a tool to split the context.

	# 	# Load YAML file
	# 	with open(f'src/ats_pass_ai/{self.tasks_config_path}', 'r') as file:
	# 		yaml_data = yaml.safe_load(file)
	# 		description_value = yaml_data['split_context_of_experience_choosing_task']['description']
	# 		expected_output = yaml_data['split_context_of_experience_choosing_task']['expected_output']

	# 	experience_choosen = self.load_txt_files(self.experience_choosing_task_file_path)
	# 	task_description = description_value.format(experience_choosen = experience_choosen)

	# 	return Task(
	# 		description=task_description,
	# 		expected_output=expected_output,
	# 		agent=self.generalist_agent(),
	# 		output_file=self.split_context_of_experience_choosing_task_file_path,
	# 	)

	
	# @task
	# def gather_info_of_choosen_experiences(self):
	# 	# Load YAML file
	# 	with open(f'src/ats_pass_ai/{self.tasks_config_path}', 'r') as file:
	# 		yaml_data = yaml.safe_load(file)
	# 		description_value = yaml_data['gather_info_of_choosen_experiences']['description']
	# 		expected_output = yaml_data['gather_info_of_choosen_experiences']['expected_output']

	# 	split_context_experience_choosen = self.load_txt_files(self.split_context_of_experience_choosing_task_file_path)
	# 	user_info_organized_data = self.load_txt_files('info_files/user_info_organized.txt')
	# 	task_description = description_value.format(split_context_experience_choosen = split_context_experience_choosen, user_info_organized_data = user_info_organized_data)

	# 	return Task(
	# 		description=task_description,
	# 		expected_output=expected_output,
	# 		agent=self.generalist_agent(),
	# 		# context=[self.experience_choosing_task()],
	# 		output_file=self.gather_info_of_choosen_experiences_file_path,
	# 	)
	# # ----------------- End of Choose Work/Project Experience -----------------

	# ----------------- Include ATS Keywords into Experiences -----------------



	# @agent
	# def ats_keyword_integration_agent(self) -> Agent:
	# 	return Agent(
	# 		config=self.agents_config["ats_keyword_integration_agent"],
	# 		# verbose=True,
	# 		allow_delegation=False,
	# 		cache=True,
	# 		llm=self.genAILarge
	# 		# llm=self.llama3_70b,
	# 		# system_template="""
	# 		# <|begin_of_text|>
	# 		# <|start_header_id|>system<|end_header_id|>

	# 		# {{ .System }}<|eot_id|>""",
	# 		# prompt_template="""<|start_header_id|>user<|end_header_id|>

	# 		# {{ .Prompt }}<|eot_id|>""",
	# 		# response_template="""<|start_header_id|>assistant<|end_header_id|>

	# 		# {{ .Response }}<|eot_id|>
	# 		# """,
	# 	)
		


	# @task
	# def ats_friendly_keywords_into_experiences_task(self):
	# 	# Load YAML file
	# 	with open(f'src/ats_pass_ai/{self.tasks_config_path}', 'r') as file:
	# 		yaml_data = yaml.safe_load(file)
	# 		description_value = yaml_data['ats_friendly_keywords_into_experiences']['description']
	# 		expected_output = yaml_data['ats_friendly_keywords_into_experiences']['expected_output']

	# 	chosen_experiences = self.load_txt_files(self.gather_info_of_choosen_experiences_file_path)
	# 	jd_keywords = self.load_txt_files(self.jd_keyword_extraction_file_path)
	# 	task_description = description_value.format(chosen_experiences = chosen_experiences, jd_keywords = jd_keywords)
		

	# 	return Task(
	# 		description=task_description,
	# 		expected_output=expected_output,
	# 		agent=self.ats_keyword_integration_agent(),
	# 		# context=[self.experience_choosing_task()],
	# 		output_file=self.ats_friendly_keywords_into_experiences_file_path,
	# 	)

	# @task
	# def split_context_of_ats_friendly_keywords_into_experiences(self):
	# 	# Load YAML file

	# 	# TODO: Instead making agent doing this split, use a tool to split the context.

	# 	with open(f'src/ats_pass_ai/{self.tasks_config_path}', 'r') as file:
	# 		yaml_data = yaml.safe_load(file)
	# 		description_value = yaml_data['split_context_of_ats_friendly_keywords_into_experiences']['description']
	# 		expected_output = yaml_data['split_context_of_ats_friendly_keywords_into_experiences']['expected_output']

	# 	ats_friendly_experiences = self.load_txt_files(self.ats_friendly_keywords_into_experiences_file_path)
	# 	task_description = description_value.format(ats_friendly_experiences = ats_friendly_experiences)

	# 	return Task(
	# 		description=task_description,
	# 		expected_output=expected_output,
	# 		agent=self.generalist_agent(),
	# 		output_file=self.split_context_of_ats_friendly_keywords_into_experiences_file_path,
	# 	)
	
	

	# @agent
	# def resume_in_json_agent(self) -> Agent:
	# 	return Agent(
	# 		config=self.agents_config["resume_in_json_agent"],
	# 		verbose=True,
	# 		allow_delegation=False,
	# 		cache=True,
	# 		# llm=self.genAILarge,
	# 		llm=self.llama3_70b,
	# 		system_template="""
	# 		<|begin_of_text|>
	# 		<|start_header_id|>system<|end_header_id|>

	# 		{{ .System }}<|eot_id|>""",
	# 		prompt_template="""<|start_header_id|>user<|end_header_id|>

	# 		{{ .Prompt }}<|eot_id|>""",
	# 		response_template="""<|start_header_id|>assistant<|end_header_id|>

	# 		{{ .Response }}<|eot_id|>
	# 		""",
	# 	)


	# @task
	# def resume_in_json_task(self):
	# 	# Load YAML file
	# 	with open(f'src/ats_pass_ai/{self.tasks_config_path}', 'r') as file:
	# 		yaml_data = yaml.safe_load(file)
	# 		description_value = yaml_data['resume_in_json_task']['description']
	# 		expected_output = yaml_data['resume_in_json_task']['expected_output']

	# 	resume_data = self.load_all_txt_files('info_extraction')
	# 	task_description = description_value.format(resume_data = resume_data)

	# 	return Task(
	# 		description=task_description,
	# 		expected_output=expected_output,
	# 		agent=self.resume_in_json_agent(),
	# 		output_file=self.resume_json_file_path,
	# 	)

		
	@agent
	def resume_compilation_agent(self) -> Agent:
		return Agent(
			config=self.agents_config["resume_compilation_agent"],
			verbose=True,
			allow_delegation=False,
			cache=True,
			llm=self.genAILarge,
		)
	
	# @task
	# def resume_compilation_task(self):
	# 	# Load YAML file
	# 	with open(f'src/ats_pass_ai/{self.tasks_config_path}', 'r') as file:
	# 		yaml_data = yaml.safe_load(file)
	# 		description_value = yaml_data['resume_compilation_task']['description']
	# 		expected_output = yaml_data['resume_compilation_task']['expected_output']

	# 	resume_data_in_json = self.load_txt_files(self.resume_json_file_path)
	# 	task_description = description_value.format(resume_data_in_json = resume_data_in_json)
		
	# 	return Task(
	# 		description=task_description,
	# 		expected_output=expected_output,
	# 		agent=self.resume_compilation_agent(),
	# 		output_file=self.resume_compilation_task_file_path,
	# 	)

	@agent
	def career_objective_agent(self) -> Agent:
		return Agent(
			config=self.agents_config["career_objective_agent"],
			verbose=True,
			allow_delegation=False,
			cache=True,
			llm=self.genAILarge,
			tools=[self.queryTool],
		)
	
	# @task
	# def career_objective_task(self):
	# 	# Load YAML file
	# 	with open(f'src/ats_pass_ai/{self.tasks_config_path}', 'r') as file:
	# 		yaml_data = yaml.safe_load(file)
	# 		description_value = yaml_data['career_objective_task']['description']
	# 		expected_output = yaml_data['career_objective_task']['expected_output']

	# 	skills = self.load_txt_files(self.split_context_of_ats_friendly_skills_task_file_path)
	# 	job_description = self.load_txt_files(self.jd_keyword_extraction_file_path)

	# 	task_description = description_value.format(skills = skills, job_description = job_description)

	# 	return Task(
	# 		description=task_description,
	# 		expected_output=expected_output,
	# 		agent=self.career_objective_agent(),
	# 		output_file=self.career_objective_task_file_path,
	# 	)

	@crew
	def crew(self) -> Crew:
		"""Creates the user info organizer crew"""

		# Create necessary files
		self.create_files()

		# Return the crew
		return Crew(
			max_rpm=11,
			agents=self.agents,
			tasks=self.tasks,
			# cache=True,
			full_output=True,
			process=Process.sequential,
			# process=Process.hierarchical,
			# manager_llm=self.composerLLM,
			verbose=1,
			memory=True,
			embedder={
				"provider": "google",
				"config":{
					"model": 'models/embedding-001',
					"task_type": "retrieval_document",
					"title": "Embeddings for Embedchain"
				}
			},
			output_log_file='output_log.txt',
		)
	
	def create_files(self):
		"""Creates the necessary files for the crew"""
		for file_path in self.file_paths.values():
			try:
				open(file_path, 'w', encoding='utf-8').close()
			except Exception as e:
				print(f"Error while creating the file: {e}")
	
	def load_txt_files(self, file_path):
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
				with open(file_path, 'r', encoding='utf-8') as file:
					all_text += file.read() + "\n"  # Append text with a newline to separate files

		return all_text

