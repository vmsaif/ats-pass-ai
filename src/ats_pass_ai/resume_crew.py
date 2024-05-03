# -*- coding: utf-8 -*-
"""
	Author: Saif Mahmud
	Date: 04-23-2024
	Description: This file contains the crew class for the user info organizer crew.
"""

from langchain_groq import ChatGroq
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
# from langchain_openai import ChatOpenAI
# from langchain_google_vertexai import VertexAI # to use codey - code-bison model to generate latex

from ats_pass_ai.tools.rag_search_tool import SearchInChromaDB

@CrewBase
class ResumeCrew:
	"""UserInfoOrganizerCrew crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/profile_building_task.yaml'
	
	# Job Keywords extraction task file path
	jd_keyword_and_phrases_extraction_task_file_path = 'info_extraction/job_description_extracted_keywords.txt'

	# Info extraction task file paths
	personal_information_extraction_task_file_path = 'info_extraction/personal_information_extraction_task.txt'
	education_extraction_task_file_path = 'info_extraction/education_extraction_task.txt'
	volunteer_work_extraction_task_file_path = 'info_extraction/volunteer_work_extraction_task.txt'
	awards_recognitions_extraction_task_file_path = 'info_extraction/awards_recognitions_extraction_task.txt'
	references_extraction_task_file_path = 'info_extraction/references_extraction_task.txt'
	personal_traits_interests_extraction_task_file_path = 'info_extraction/personal_traits_interests_extraction_task.txt'
	miscellaneous_extraction_task_file_path = 'info_extraction/miscellaneous_extraction_task.txt'

	# Dictionary to store file paths
	file_paths = {
		"job_description_keyword_and_phrases_extraction_task": jd_keyword_and_phrases_extraction_task_file_path,
		"personal_information_extraction_task": personal_information_extraction_task_file_path,
		"education_extraction_task": education_extraction_task_file_path,
	}

	# Define the tools
	queryTool = SearchInChromaDB().search # passing the function reference, not calling the function

	llm = ChatGroq(
			temperature=0.95,
			model_name="llama3-8b-8192",
			# model_kwargs={
			# 	'top_p': 0.95  # Nucleus sampling: cumulatively retains the top p% probability mass
    		# },
			verbose=True
		)

	# Define the agents
	@agent
	def data_retrieval_agent(self) -> Agent:
		return Agent(
			config=self.agents_config["chunk_retrieval_agent"],
			verbose=True,
			# max_iter=3,
			# max_rpm=2,
			allow_delegation=False,
			# cache=True,
			llm=self.llm,
			tools=[self.queryTool],
		)

	# Define the tasks
	@task
	def chunk_retrival_personal_information_task(self):
		return Task(
			config=self.tasks_config["chunk_retrival_personal_information_task"],
			agent=self.data_retrieval_agent(),
		)
	
	@agent
	def data_extraction_agent(self) -> Agent:
		return Agent(
			config=self.agents_config["data_extraction_agent"],
			verbose=True,
			# max_iter=10,
			# max_rpm=2,
			allow_delegation=True,
			# cache=True,
			llm=self.llm
		)
	
	@task
	def personal_information_extraction_task(self):
		return Task(
			config=self.tasks_config["personal_information_extraction_task"],
			agent=self.data_extraction_agent(),
			context=[self.chunk_retrival_personal_information_task()],
			output_file=self.personal_information_extraction_task_file_path,
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
	# def volunteer_work_extraction_task(self):
	# 	return Task(
	# 		config=self.tasks_config["volunteer_work_extraction_task"],
	# 		agent=self.generalist_agent(),
	# 		output_file=self.volunteer_work_extraction_task_file_path,
	# 		tools=[self.queryTool],
	# 	)
 
	# @task
	# def awards_recognitions_extraction_task(self):
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
	# def profile_building_task(self):
	# 	return Task(
	# 		config=self.tasks_config["profile_building_task"],
	# 		agent=self.profile_builder_agent(),
	# 		output_file=self.profile_building_task_file_path,
	# 		tools=[],
	# 	)

	def create_files(self):
		"""Creates the necessary files for the crew"""
		for file_path in self.file_paths.values():
			try:
				open(file_path, 'w').close()
			except Exception as e:
				print(f"Error while creating the file: {e}")
	
	@crew
	def crew(self) -> Crew:
		"""Creates the user info organizer crew"""

		# Create necessary files
		self.create_files()

		# Return the crew
		return Crew(
			max_rpm=5,
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			cache=True,
			full_output=True,
			process=Process.sequential,
			# process=Process.hierarchical,
			# manager_llm=self.llm,
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
	

