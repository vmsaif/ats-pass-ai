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
from langchain_google_genai import GoogleGenerativeAI
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
	jd_keyword_extraction_file_path = 'info_extraction/job_description_extracted_keywords.txt' # do not use it inside file_path dictionary below.

	# Info extraction task file paths
	personal_information_extraction_task_file_path = 'info_extraction/personal_information_extraction_task.txt'
	education_extraction_task_file_path = 'info_extraction/education_extraction_task.txt'
	volunteer_work_extraction_task_file_path = 'info_extraction/volunteer_work_extraction_task.txt'
	awards_recognitions_extraction_task_file_path = 'info_extraction/awards_recognitions_extraction_task.txt'
	references_extraction_task_file_path = 'info_extraction/references_extraction_task.txt'
	personal_traits_interests_extraction_task_file_path = 'info_extraction/personal_traits_interests_extraction_task.txt'
	miscellaneous_extraction_task_file_path = 'info_extraction/miscellaneous_extraction_task.txt'

	work_experience_extraction_task_file_path = 'info_extraction/work_experience_extraction_task.txt'
	project_experience_extraction_task_file_path = 'info_extraction/project_experience_extraction_task.txt'
	skills_from_exp_and_project_file_path = 'info_extraction/skills_from_exp_and_project.txt'
	all_togather_skills_extraction_task_file_path = 'info_extraction/all_togather_skills_extraction_task.txt'


	# Cross Checked with JD keywords
	skills_cross_check_task_file_path = 'info_extraction/relevent_to_jd/skills_cross_check_task.txt'
	experience_choosing_task_file_path = 'info_extraction/relevent_to_jd/experience_choosing_task.txt'
	gather_info_of_choosen_experiences_file_path = 'info_extraction/relevent_to_jd/gather_info_of_choosen_experiences.txt'
	include_ats_keywords_into_experiences_file_path = 'info_extraction/relevent_to_jd/include_ats_keywords_into_experiences.txt'

	# Dictionary to store file paths
	file_paths = {
		# "personal_information_extraction_task": personal_information_extraction_task_file_path,
		# "education_extraction_task": education_extraction_task_file_path,
		# "volunteer_work_extraction_task": volunteer_work_extraction_task_file_path,
		# "awards_recognitions_extraction_task": awards_recognitions_extraction_task_file_path,
		# "references_extraction_task": references_extraction_task_file_path,
		# "personal_traits_interests_extraction_task": personal_traits_interests_extraction_task_file_path,
		# "miscellaneous_extraction_task": miscellaneous_extraction_task_file_path,

		# "all_togather_skills_extraction_task": all_togather_skills_extraction_task_file_path,

		# "skills_from_exp_and_project": skills_from_exp_and_project_file_path,
		# "skills_cross_check_task": skills_cross_check_task_file_path,
		# "work_experience_extraction_task": work_experience_extraction_task_file_path,
		# "project_experience_extraction_task": project_experience_extraction_task_file_path,
		# "experience_choosing_task": experience_choosing_task_file_path,
		# "gather_info_of_choosen_experiences": gather_info_of_choosen_experiences_file_path,
		"include_ats_keywords_into_experiences": include_ats_keywords_into_experiences_file_path,
	}

	# Define the tools
	queryTool = SearchInChromaDB().search # passing the function reference, not calling the function
	jd_extr_keywords_reader = CrewAIFileReadTool.create(jd_keyword_extraction_file_path)
	user_info_organized_reader = CrewAIFileReadTool.create('info_files/user_info_organized.txt')

	genAILarge = ChatVertexAI(
		model="gemini-1.5-pro-preview-0409",
		verbose=True,
		temperature=1.0,
	)

	genAI = GoogleGenerativeAI(
		model="gemini-pro",
		verbose=True,
		max_output_tokens=6000,
		temperature=1.0,
		# cache=True
	)

	# @task
	# def education_extraction_task(self):
	# 	return Task(
	# 		config=self.tasks_config["education_extraction_task"],
	# 		agent=self.generalist_agent(),
	# 		output_file=self.education_extraction_task_file_path,
	# 		tools=[self.queryTool],
	# 	)
	
	# @task
	# def personal_information_extraction_task(self):
	# 	return Task(
	# 		config=self.tasks_config["personal_information_extraction_task"],
	# 		agent=self.generalist_agent(),
	# 		output_file=self.personal_information_extraction_task_file_path,
	# 		tools=[self.queryTool],
	# 	)
 
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

	# @agent
	# def generalist_agent(self) -> Agent:
	# 	return Agent(
	# 		config=self.agents_config["generalist_agent"],
	# 		verbose=True,
	# 		allow_delegation=False,
	# 		cache=True,
	# 		llm=self.genAI,
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



	# genAILarge = ChatVertexAI(
	# 	model="gemini-1.5-pro-preview-0409",
	# 	verbose=True,
	# 	temperature=1.0,
	# )

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
	
	# @task
	# def skills_cross_check_task(self):
	# 	# Load YAML file
	# 	with open(f'src/ats_pass_ai/{self.tasks_config_path}', 'r') as file:
	# 		yaml_data = yaml.safe_load(file)
	# 		description_value = yaml_data['skills_cross_check_task']['description']
	# 		expected_output = yaml_data['skills_cross_check_task']['expected_output']

	# 	src_1 = self.load_txt_files(self.jd_keyword_extraction_file_path)
	# 	task_description = description_value.format(src_1 = src_1)

	# 	return Task(
	# 		description=task_description,
	# 		expected_output=expected_output,
	# 		agent=self.cross_match_evaluator_with_job_description_agent(),
	# 		context=[self.skills_extraction_task()],
	# 		output_file=self.skills_cross_check_task_file_path,
	# 	)

	# ----------------- End of Skills Match Identification -----------------

	# ----------------- Choose Work/Project Experience -----------------
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
	# def gather_info_of_choosen_experiences(self):
	# 	# Load YAML file
	# 	with open(f'src/ats_pass_ai/{self.tasks_config_path}', 'r') as file:
	# 		yaml_data = yaml.safe_load(file)
	# 		description_value = yaml_data['gather_info_of_choosen_experiences']['description']
	# 		expected_output = yaml_data['gather_info_of_choosen_experiences']['expected_output']

	# 	experience_choosen = self.load_txt_files(self.experience_choosing_task_file_path)
	# 	user_info_organized_data = self.load_txt_files('info_files/user_info_organized.txt')
	# 	task_description = description_value.format(experience_choosen = experience_choosen, user_info_organized_data = user_info_organized_data)

	# 	return Task(
	# 		description=task_description,
	# 		expected_output=expected_output,
	# 		agent=self.generalist_agent(),
	# 		# context=[self.experience_choosing_task()],
	# 		output_file=self.gather_info_of_choosen_experiences_file_path,
	# 	)
	

	# ----------------- End of Choose Work/Project Experience -----------------

	# ----------------- Include ATS Keywords into Experiences -----------------

	llama3_70b = ChatGroq(
		model_name="llama3-70b-8192",
		# verbose=True,
		temperature=1.5,
	)

	@agent
	def ats_keyword_integration_agent(self) -> Agent:
		return Agent(
			config=self.agents_config["ats_keyword_integration_agent"],
			# verbose=True,
			allow_delegation=False,
			cache=True,
			llm=self.genAILarge
			# llm=self.llama3_70b,
			# system_template="""
			# <|begin_of_text|>
			# <|start_header_id|>system<|end_header_id|>

			# {{ .System }}<|eot_id|>""",
			# prompt_template="""<|start_header_id|>user<|end_header_id|>

			# {{ .Prompt }}<|eot_id|>""",
			# response_template="""<|start_header_id|>assistant<|end_header_id|>

			# {{ .Response }}<|eot_id|>
			# """,
		)
		


	@task
	def include_ats_keywords_into_experiences(self):
		# Load YAML file
		with open(f'src/ats_pass_ai/{self.tasks_config_path}', 'r') as file:
			yaml_data = yaml.safe_load(file)
			description_value = yaml_data['ats_friendly_experience_enhancement_task']['description']
			expected_output = yaml_data['ats_friendly_experience_enhancement_task']['expected_output']

		chosen_experiences = self.load_txt_files(self.gather_info_of_choosen_experiences_file_path)
		jd_keywords = self.load_txt_files(self.jd_keyword_extraction_file_path)
		task_description = description_value.format(chosen_experiences = chosen_experiences, jd_keywords = jd_keywords)

		return Task(
			description=task_description,
			expected_output=expected_output,
			agent=self.ats_keyword_integration_agent(),
			# context=[self.experience_choosing_task()],
			output_file=self.include_ats_keywords_into_experiences_file_path,
		)

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
			cache=True,
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
			}
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


