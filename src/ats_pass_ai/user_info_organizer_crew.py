# -*- coding: utf-8 -*-
"""
	Author: Saif Mahmud
	Date: 04-23-2024
	Description: This file contains the crew class for the user info organizer crew.
"""

import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# from langchain_google_vertexai import VertexAI # to use codey - code-bison model to generate latex
from langchain_google_genai import ChatGoogleGenerativeAI
from ats_pass_ai.tools.my_txt_search_tool import MyTXTSearchTool

# from ats_pass_ai.tools.custom_tool import MyCustomTool # Import custom tool here


@CrewBase
class UserInfoOrganizerCrew:
	"""UserInfoOrganizerCrew crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/info_organize_tasks.yaml'

	# Define the file paths
	user_info_file_path = 'info_files/user_info.txt'
	personal_information_task_file_path = 'user_info_extraction/personal_information_task.txt'

	# Define the tools
	# basic_info_tool = MyTXTSearchTool.create(user_info_file_path)

	# Initialize Gemini model
	gemini = ChatGoogleGenerativeAI(
		model="gemini-pro",
		google_api_key=os.getenv("GOOGLE_API_KEY"),
		verbose=True,
		temperature=0.2
	)

	# embedder = dict(
#             provider = "google",
#             config = dict(
#                 model = 'models/embedding-001'
#             )
#         )

	# Define the agents
	@agent
	def generalist_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['generalist_agent'],
			tools=[self.basic_info_tool],
			verbose=True,
			allow_delegation=True,
			llm=self.gemini
		)

	# Define the tasks
	@task
	def personal_information_task(self) -> Task:
		return Task(
			config=self.tasks_config['personal_information_task'],
			agent=self.generalist_agent(),
			output_file=self.personal_information_task_file_path
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the user info organizer crew"""

		# # Create necessary files
		# try:
		# 	open(self.personal_information_task_file_path, 'w').close()
		# except Exception as e:
		# 	print(f"Error while creating the file: {e}")
   
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			cache=True,
			process=Process.sequential,
			verbose=2,	
		)
	
	# generate(messages: List[List[BaseMessage]], stop: Optional[List[str]] = None, callbacks: Optional[Union[List[BaseCallbackHandler], BaseCallbackManager]] = None, *, tags: Optional[List[str]] = None, metadata: Optional[Dict[str, Any]] = None, run_name: Optional[str] = None, run_id: Optional[UUID] = None, **kwargs: Any) → LLMResult
	result = gemini.generate(messages=[["What is the user's name?"]])
	print(result)