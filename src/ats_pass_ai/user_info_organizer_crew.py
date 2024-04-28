# -*- coding: utf-8 -*-
"""
	Author: Saif Mahmud
	Date: 04-23-2024
	Description: This file contains the crew class for the user info organizer crew.
"""

from langchain_groq import ChatGroq
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
# from langchain_google_vertexai import VertexAI # to use codey - code-bison model to generate latex

from ats_pass_ai.tools.text_reader_tool import TextFileReaderTool

@CrewBase
class UserInfoOrganizerCrew:
	"""UserInfoOrganizerCrew crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/profile_building_task.yaml'
	
	# Define the file paths
	personal_information_task_file_path = 'user_info_extraction/personal_information_task.txt'
	# initialize the tools
	queryTool = TextFileReaderTool()

	# Define the model
	llm = ChatGroq(
			temperature=0.7, 
			model_name="llama3-8b-8192", 
			verbose=True
		)

	# Define the agents
	@agent
	def generalist_agent(self) -> Agent:
		return Agent(
			config=self.agents_config["generalist_agent"],
			verbose=True,
			allow_delegation=True,
			llm=self.llm
		)

	# Define the tasks
	@task
	def personal_information_task(self):
		return Task(
			config=self.tasks_config["personal_information_task"],
			agent=self.generalist_agent(),
			output_file=self.personal_information_task_file_path,
			tools=[self.queryTool],
		)
	
	# @task
	# def education_task(self):
	# 	return Task(
	# 		config=self.tasks_config["education_task"],
	# 		agent=self.generalist_agent(),
	# 		output_file=self.personal_information_task_file_path,
	# 		tools=[self.file_reader_tool],
	# 	)

	@crew
	def crew(self) -> Crew:
		"""Creates the user info organizer crew"""

		# Create necessary files
		try:
			open(self.personal_information_task_file_path, 'w').close()
		except Exception as e:
			print(f"Error while creating the file: {e}")
   
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			cache=True,
			process=Process.sequential,
			verbose=2,
			memory=True,
			embedder={
				"provider": "google",
				"config":{
					"model": 'models/embedding-001',
					"task_type": "retrieval_document",
					"title": "Embeddings for Embedchain"
				}
			},
		)
