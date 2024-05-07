# -*- coding: utf-8 -*-
"""
	Author: Saif Mahmud
	Date: 04-23-2024
	Description: This file contains the crew class for the user info organizer crew.
"""

from langchain_groq import ChatGroq
from langchain_google_genai import GoogleGenerativeAI
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
	tasks_config = 'config/tasks.yaml'
	
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
	job_description_cross_check_task_file_path = 'info_extraction/job_description_relevance_task.txt'

	# Dictionary to store file paths
	file_paths = {
		"personal_information_extraction_task": personal_information_extraction_task_file_path,
		"education_extraction_task": education_extraction_task_file_path,
		"volunteer_work_extraction_task": volunteer_work_extraction_task_file_path,
  		"resume_building_task": resume_building_task_file_path,
		"awards_recognitions_extraction_task": awards_recognitions_extraction_task_file_path,
		"references_extraction_task": references_extraction_task_file_path,
		"personal_traits_interests_extraction_task": personal_traits_interests_extraction_task_file_path,
		"miscellaneous_extraction_task": miscellaneous_extraction_task_file_path,
		"job_description_cross_check_task": job_description_cross_check_task_file_path,
	}

	# Define the tools
	queryTool = SearchInChromaDB().search # passing the function reference, not calling the function
	jd_reader = CrewAIFileReadTool.create(jd_keyword_extraction_file_path)


	# llm = ChatGroq(
	# 		temperature=0.5,
	# 		model_name="llama3-8b-8192",
	# 		# model_kwargs={
	# 		# 	'top_p': 0.95  # Nucleus sampling: cumulatively retains the top p% probability mass
    # 		# },
	# 		verbose=True
	# )
	
	genAI = GoogleGenerativeAI(
		model="gemini-pro",
		verbose=True,
		temperature=1.0,
		cache=True
	)

	genAILarge = ChatVertexAI(
		model="gemini-1.5-pro-preview-0409",
		verbose=True,
		temperature=0.9,
	)


	# Define the agents
	@agent
	def generalist_agent(self) -> Agent:
		return Agent(
			config=self.agents_config["generalist_agent"],
			verbose=True,
			# max_iter=3,
			# max_rpm=2,
			allow_delegation=False,
			cache=True,
			llm=self.genAI,
		)

	# Define the tasks
	@task
	def education_extraction_task(self):
		return Task(
			config=self.tasks_config["education_extraction_task"],
			agent=self.generalist_agent(),
			output_file=self.education_extraction_task_file_path,
			tools=[self.queryTool],
		)
	
	# @task
	# def personal_information_extraction_task(self):
	# 	return Task(
	# 		config=self.tasks_config["personal_information_extraction_task"],
	# 		agent=self.generalist_agent(),
	# 		output_file=self.personal_information_extraction_task_file_path,
	# 		tools=[self.queryTool],
	# 	)
 
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

	@agent
	def job_description_relevance_agent (self) -> Agent:
		return Agent(
			config=self.agents_config["job_description_cross_check_agent"],
			verbose=True,
			# max_iter=3,
			max_rpm=2,
			allow_delegation=False,
			cache=True,
			tools=[self.jd_reader],
			llm=self.genAI,
		)
	
	@task
	def job_description_cross_check_task(self):
		return Task(
			config=self.tasks_config["job_description_cross_check_task"],
			agent=self.job_description_relevance_agent(),
			context=[self.education_extraction_task()],
			output_file=self.job_description_cross_check_task_file_path,

		)

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

