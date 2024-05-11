# -*- coding: utf-8 -*-
"""
	Author: Saif Mahmud
	Date: 04-23-2024
	Description: This file contains the crew class for the user info organizer crew.
"""
import os
import agentops
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
	resume_building_task_file_path = 'info_extraction/resume_building_task.txt'
	
	work_experience_extraction_task_file_path = 'info_extraction/work_experience_extraction_task.txt'
	project_experience_extraction_task_file_path = 'info_extraction/project_experience_extraction_task.txt'
	skills_from_exp_and_project_file_path = 'info_extraction/skills_from_exp_and_project.txt'
	all_togather_skills_extraction_task_file_path = 'info_extraction/all_togather_skills_extraction_task.txt'

	# Cross Checked with JD keywords
	skills_cross_check_task_file_path = 'info_extraction/relevent_to_jd/skills_cross_check_task.txt'

	# Dictionary to store file paths
	file_paths = {
		# "personal_information_extraction_task": personal_information_extraction_task_file_path,
		# "education_extraction_task": education_extraction_task_file_path,
		# "volunteer_work_extraction_task": volunteer_work_extraction_task_file_path,
  		# "resume_building_task": resume_building_task_file_path,
		# "awards_recognitions_extraction_task": awards_recognitions_extraction_task_file_path,
		# "references_extraction_task": references_extraction_task_file_path,
		# "personal_traits_interests_extraction_task": personal_traits_interests_extraction_task_file_path,
		# "miscellaneous_extraction_task": miscellaneous_extraction_task_file_path,

		# "all_togather_skills_extraction_task": all_togather_skills_extraction_task_file_path,
		# "work_experience_extraction_task": work_experience_extraction_task_file_path,
		# "project_experience_extraction_task": project_experience_extraction_task_file_path,
		# "skills_from_exp_and_project": skills_from_exp_and_project_file_path,
		"job_description_cross_check_task": skills_cross_check_task_file_path,
	}

	# Define the tools
	queryTool = SearchInChromaDB().search # passing the function reference, not calling the function
	jd_extr_keywords_reader = CrewAIFileReadTool.create(jd_keyword_extraction_file_path)
	user_info_organized_reader = CrewAIFileReadTool.create('info_files/user_info_organized.txt')

	tempTool = CrewAIFileReadTool.create(all_togather_skills_extraction_task_file_path)


	# llama = ChatGroq(
	# 		temperature=0.5,
	# 		model_name="llama3-8b-8192",
	# 		# model_kwargs={
	# 		# 	'top_p': 0.95  # Nucleus sampling: cumulatively retains the top p% probability mass
    # 		# },
	# 		verbose=True
	# )
	# agentops.init()
 
	# itirative_AI = ChatGoogleGenerativeAI(
	# 	model="gemini-pro",
	# 	verbose=True,
	# 	temperature=0.9,
	# 	cache=True
	# )

	genAI = GoogleGenerativeAI(
		model="gemini-pro",
		verbose=True,
		max_output_tokens=4096,
		temperature=0.9,
		# cache=True
	)



	# Define the agents


	# Define the tasks
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
		# )

	
	# @agent
	# def resume_builder_agent(self) -> Agent:
	# 	return Agent(
	# 		config=self.agents_config["resume_builder_agent"],
	# 		verbose=True,
	# 		# max_iter=3,
	# 		max_rpm=2,
	# 		allow_delegation=False,
	# 		cache=True,
	# 		llm=self.genAI,
	# 	)

	# @task
	# def resume_build_task(self):
	# 	return Task(
	# 		config=self.tasks_config["resume_build_task"],
	# 		agent=self.resume_builder_agent(),
	# 		output_file=self.resume_building_task_file_path,
	# 		context=[
	# 			self.personal_information_extraction_task(),
	# 			self.education_extraction_task(),
	# 			self.volunteer_work_extraction_task(),
	# 			self.awards_recognitions_extraction_task(),
	# 			self.references_extraction_task(),
	# 			self.personal_traits_interests_extraction_task(),
	# 			self.miscellaneous_extraction_task(),
	# 		],
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
	# 		# max_iter=3,
	# 		max_rpm=2,
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


	genAILarge = ChatVertexAI(
		model="gemini-1.5-pro-preview-0409",
		verbose=True,
		temperature=1.0,
	)
	@agent
	def technical_details_agent (self) -> Agent:
		return Agent(
			config=self.agents_config["technical_details_agent"],
			verbose=True,
			allow_delegation=False,
			# cache=True,
			llm=self.genAILarge,
		)
	
	@task
	def skills_cross_check_task(self):
		# Load YAML file
		with open(f'src/ats_pass_ai/{self.tasks_config_path}', 'r') as file:
			yaml_data = yaml.safe_load(file)
			description = yaml_data['skills_cross_check_task']['description']
			expected_output = yaml_data['skills_cross_check_task']['expected_output']

		src_2 = self.load_txt_files(self.all_togather_skills_extraction_task_file_path)
		src_1 = self.load_txt_files(self.jd_keyword_extraction_file_path)

		description = description.format(src_1=src_1, src_2=src_2)
		return Task(
			description=description,
			expected_output=expected_output,
			agent=self.technical_details_agent(),
			output_file=self.skills_cross_check_task_file_path,
		)

	# ----------------- End of Skills Match Identification -----------------

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
			verbose=2,
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
				open(file_path, 'w').close()
			except Exception as e:
				print(f"Error while creating the file: {e}")
	
	def load_txt_files(self, file_path):
		"""Load text file"""
		with open(file_path, 'r', encoding='utf-8') as file:
			return file.read()


