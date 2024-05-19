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
# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_vertexai import ChatVertexAI
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
# from langchain_google_vertexai import VertexAI # to use codey - code-bison model to generate latex
# from ats_pass_ai.tools.crewai_web_search_tool import CrewAIWebsiteSearchTool
# from crewai_tools import SerperDevTool
from langchain_community.tools import DuckDuckGoSearchRun
from ats_pass_ai.tools.rag_search_tool import SearchInChromaDB

@CrewBase
class ResumeCrew:
	"""Resume Maker Crew"""
	agents_config = 'config/agents.yaml'
	tasks_config_path = 'config/tasks.yaml'
	tasks_config = tasks_config_path # because tasks_config somehow getting recognized as a dictionary, not a simple string path.
	
	# user_info_orgainzed_file_path
	user_info_organized_file_path = 'info_files/user_info_organized.txt'

	# root of extraction folder
	info_extraction_folder_path = 'info_extraction'

	# Job Keywords extraction task file path
	jd_keyword_extraction_file_path = f'{info_extraction_folder_path}/jd_keyword_extraction/job_description_extracted_keywords.txt' # do not use it inside file_path dictionary below.

	# Info extraction task file paths
	personal_information_extraction_task_file_path = f'{info_extraction_folder_path}/personal_information_extraction_task.txt'
	education_extraction_task_file_path = f'{info_extraction_folder_path}/education_extraction_task.txt'
	volunteer_work_extraction_task_file_path = f'{info_extraction_folder_path}/volunteer_work_extraction_task.txt'
	awards_recognitions_extraction_task_file_path = f'{info_extraction_folder_path}/awards_recognitions_extraction_task.txt'
	references_extraction_task_file_path = f'{info_extraction_folder_path}/references_extraction_task.txt'
	personal_traits_interests_extraction_task_file_path = f'{info_extraction_folder_path}/personal_traits_interests_extraction_task.txt'
	miscellaneous_extraction_task_file_path = f'{info_extraction_folder_path}/miscellaneous_extraction_task.txt'
	profile_builder_task_file_path = f'{info_extraction_folder_path}/profile_builder_task.txt'

	work_experience_extraction_task_file_path = f'{info_extraction_folder_path}/pre_tasks/work_experience_extraction_task.txt'
	project_experience_extraction_task_file_path = f'{info_extraction_folder_path}/pre_tasks/project_experience_extraction_task.txt'
	skills_from_exp_and_project_file_path = f'{info_extraction_folder_path}/pre_tasks/skills_from_exp_and_project.txt'
	all_togather_skills_extraction_task_file_path = f'{info_extraction_folder_path}/pre_tasks/all_togather_skills_extraction_task.txt'
	
	# Cross Checked with JD keywords
	ats_friendly_skills_pre_task_file_path = f'{info_extraction_folder_path}/pre_tasks/ats_friendly_skills_task.txt'
	split_context_of_ats_friendly_skills_task_file_path = f'{info_extraction_folder_path}/split_context_of_ats_friendly_skills_task.txt' 
	experience_choosing_task_file_path = f'{info_extraction_folder_path}/pre_tasks/experience_choosing_task.txt'
	split_context_of_experience_choosing_task_file_path = f'{info_extraction_folder_path}/pre_tasks/split_context_of_experience_choosing_task.txt'
	gather_info_of_choosen_experiences_file_path = f'{info_extraction_folder_path}/pre_tasks/gather_info_of_choosen_experiences.txt'
	ats_friendly_keywords_into_experiences_file_path = f'{info_extraction_folder_path}/pre_tasks/ats_friendly_keywords_into_experiences.txt'
	split_context_of_ats_friendly_keywords_into_experiences_file_path = f'{info_extraction_folder_path}/split_context_of_ats_friendly_keywords_into_experiences.txt'
	career_objective_task_file_path = f'{info_extraction_folder_path}/career_objective_task.txt'

	# finalized_resume
	resume_in_json_file_path = f'{info_extraction_folder_path}/draft_output/resume_in_json.txt'
	resume_compilation_task_file_path = f'{info_extraction_folder_path}/draft_output/resume_compilation.txt'

	# Define the tools
	queryTool = SearchInChromaDB().search # passing the function reference, not calling the function
	webSearchTool = DuckDuckGoSearchRun()
	

	safety_settings = {
		HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
		HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
		HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
		HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
	}
	
	genAI = GoogleGenerativeAI(
		model="gemini-pro",
		max_output_tokens=8192,
		temperature=1.0,
		safety_settings=safety_settings,
	)

	genAILarge = ChatVertexAI(
		model="gemini-1.5-pro-preview-0409",
		temperature=1.0,
	)

	llama3_70b = ChatGroq(
		model_name="llama3-70b-8192",
		temperature=1.5,
	)

	@agent
	def generalist_agent(self) -> Agent:
		return Agent(
			config=self.agents_config["generalist_agent"],
			allow_delegation=False,
			# cache=True,
			verbose=True,
			llm=self.genAI,
		)
	
	@agent
	def technical_details_agent(self) -> Agent:
		return Agent(
			config=self.agents_config["technical_details_agent"],
			allow_delegation=False,
			verbose=True,
			# cache=True,
			llm=self.genAI,
		)

	@agent
	def career_objective_agent(self) -> Agent:
		return Agent(
			config=self.agents_config["career_objective_agent"],
			max_rpm=1,
			allow_delegation=False,
			verbose=True,
			# cache=True,
			llm=self.genAILarge,
			tools=[self.queryTool],
		)

	@agent
	def cross_match_evaluator_with_job_description_agent (self) -> Agent:
		return Agent(
			config=self.agents_config["cross_match_evaluator_with_job_description_agent"],
			max_rpm=1,
			allow_delegation=False,
			verbose=True,
			# cache=True,
			tools=[self.webSearchTool],
			llm=self.genAILarge,
		)
	

	
	@agent
	def ats_keyword_integration_agent(self) -> Agent:
		return Agent(
			config=self.agents_config["ats_keyword_integration_agent"],
			verbose=True,
			max_rpm=1,
			allow_delegation=False,
			# cache=True,
			llm=self.genAILarge
		)
	
	@agent
	def resume_in_json_agent(self) -> Agent:
		return Agent(
			config=self.agents_config["resume_in_json_agent"],
			allow_delegation=False,
			max_rpm=1,
			llm=self.genAILarge,
			verbose=True,
			# cache=True,
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
	
	@agent
	def resume_compilation_agent(self) -> Agent:
		return Agent(
			config=self.agents_config["resume_compilation_agent"],
			max_rpm=1,
			allow_delegation=False,
			verbose=True,
			# cache=True,
			llm=self.genAILarge,
		)

	# ---------------------- Define the tasks ----------------------

	@task
	def personal_information_extraction_task(self):
		return Task(
			config=self.tasks_config["personal_information_extraction_task"],
			agent=self.generalist_agent(),
			output_file=self.personal_information_extraction_task_file_path,
			tools=[self.queryTool],
		)
	
	@task
	def education_extraction_task(self):
		return Task(
			config=self.tasks_config["education_extraction_task"],
			agent=self.generalist_agent(),
			output_file=self.education_extraction_task_file_path,
			tools=[self.queryTool],
		)
 
	@task
	def volunteer_work_extraction_task(self):
		return Task(
			config=self.tasks_config["volunteer_work_extraction_task"],
			agent=self.generalist_agent(),
			output_file=self.volunteer_work_extraction_task_file_path,
			tools=[self.queryTool],
		)

	@task
	def awards_recognitions_extraction_task (self):
		return Task(
			config=self.tasks_config["awards_recognitions_extraction_task"],
			agent=self.generalist_agent(),
			output_file=self.awards_recognitions_extraction_task_file_path,
			tools=[self.queryTool],
		)
 
	@task
	def references_extraction_task(self):
		return Task(
			config=self.tasks_config["references_extraction_task"],
			agent=self.generalist_agent(),
			output_file=self.references_extraction_task_file_path,
			tools=[self.queryTool],
		)
	
	@task
	def personal_traits_interests_extraction_task(self):
		return Task(
			config=self.tasks_config["personal_traits_interests_extraction_task"],
			agent=self.generalist_agent(),
			output_file=self.personal_traits_interests_extraction_task_file_path,
			tools=[self.queryTool],
		)
	
	@task
	def miscellaneous_extraction_task(self):
		return Task(
			config=self.tasks_config["miscellaneous_extraction_task"],
			agent=self.generalist_agent(),
			output_file=self.miscellaneous_extraction_task_file_path,
			tools=[self.queryTool],
		)

	@task
	def profile_builder_task(self):
		return Task(
			config=self.tasks_config["profile_builder_task"],
			agent=self.generalist_agent(),
			context=[
					self.personal_information_extraction_task(), 
					self.education_extraction_task(), 
					self.volunteer_work_extraction_task(), 
					self.awards_recognitions_extraction_task(), 
					self.references_extraction_task(), 
					self.personal_traits_interests_extraction_task(), 
					self.miscellaneous_extraction_task(),
				],
			output_file=self.profile_builder_task_file_path,
		)

	@task
	def work_experience_extraction_task(self):
		
		yaml = self.yaml_loader('work_experience_extraction_task')
		user_info_organized_data = self.load_txt_files(self.user_info_organized_file_path)

		task_description = yaml[0].format(user_info_organized_data = user_info_organized_data)
		expected_output = yaml[1]

		return Task(
			description = task_description,
			expected_output = expected_output,
			agent=self.generalist_agent(),
			
			output_file=self.work_experience_extraction_task_file_path,
		)

	@task
	def project_experience_extraction_task(self):

		# Load YAML file
		yaml = self.yaml_loader('project_experience_extraction_task')
		user_info_organized_data = self.load_txt_files(self.user_info_organized_file_path)

		task_description = yaml[0].format(user_info_organized_data = user_info_organized_data)
		expected_output = yaml[1]

		return Task(
			description=task_description,
			expected_output=expected_output,
			agent=self.generalist_agent(),
			output_file=self.project_experience_extraction_task_file_path,
		)
	
	@task
	def skills_from_exp_and_project_task(self):
		return Task(
			config=self.tasks_config["skills_from_exp_and_project_task"],
			agent=self.technical_details_agent(),
			context=[self.work_experience_extraction_task(), self.project_experience_extraction_task()],
			tools=[self.webSearchTool],
			output_file=self.skills_from_exp_and_project_file_path,
		)

	@task
	def skills_extraction_task(self):
		return Task(
			config=self.tasks_config["skills_extraction_task"],
   			agent=self.technical_details_agent(),
			context=[self.skills_from_exp_and_project_task()],
			output_file=self.all_togather_skills_extraction_task_file_path,
			tools=[self.queryTool],
		)

	# # ----------------- Skills Match Identification -----------------
	
	@task
	def ats_friendly_skills_task(self):
		# Load YAML file
		yaml = self.yaml_loader('ats_friendly_skills_task')
		
		src_1 = self.load_txt_files(self.jd_keyword_extraction_file_path)
		task_description = yaml[0].format(src_1 = src_1)
		expected_output = yaml[1]

		return Task(
			description=task_description,
			expected_output=expected_output,
			agent=self.cross_match_evaluator_with_job_description_agent(),
			context=[self.skills_extraction_task()],
			tools=[self.webSearchTool],
			output_file=self.ats_friendly_skills_pre_task_file_path,
		)
	
	@task
	def split_context_of_ats_friendly_skills_task(self):
		return Task(
			config=self.tasks_config["split_context_of_ats_friendly_skills_task"],
			agent=self.generalist_agent(),
			context=[self.ats_friendly_skills_task()],
			output_file=self.split_context_of_ats_friendly_skills_task_file_path,
		)
	# ----------------- End of Skills Match Identification -----------------

	# ----------------- Choose Work/Project Experience -----------------
	@task
	def experience_choosing_task(self):
		# Load YAML file
		yaml = self.yaml_loader('experience_choosing_task')
		
		jd_keyword = self.load_txt_files(self.jd_keyword_extraction_file_path)
		today_date = datetime.date.today().strftime("%B %d, %Y")
		
		task_description = yaml[0].format(jd_keyword = jd_keyword, today_date = today_date)
		expected_output = yaml[1]

		return Task(
			description=task_description,
			expected_output=expected_output,
			agent=self.cross_match_evaluator_with_job_description_agent(),
			context=[self.work_experience_extraction_task(), self.project_experience_extraction_task()],
			output_file=self.experience_choosing_task_file_path,
		)
	
	@task
	def split_context_of_experience_choosing_task(self):

		# TODO: Instead making agent doing this split, use a tool to split the context.
		
		return Task(
			config=self.tasks_config["split_context_of_experience_choosing_task"],
			agent=self.generalist_agent(),
			context=[self.experience_choosing_task()],
			output_file=self.split_context_of_experience_choosing_task_file_path,
		)

	
	@task
	def gather_info_of_choosen_experiences(self):
		# Load YAML file
		yaml = self.yaml_loader('gather_info_of_choosen_experiences')

		# Load the user info organized data
		user_info_organized_data = self.load_txt_files(self.user_info_organized_file_path)
		task_description = yaml[0].format(user_info_organized_data = user_info_organized_data)
		expected_output = yaml[1]

		return Task(
			description=task_description,
			expected_output=expected_output,
			agent=self.generalist_agent(),
			context=[self.split_context_of_experience_choosing_task()],
			output_file=self.gather_info_of_choosen_experiences_file_path,
		)
	# ----------------- End of Choose Work/Project Experience -----------------

	# ----------------- Include ATS Keywords into Experiences -----------------

	@task
	def ats_friendly_keywords_into_experiences_task(self):
		# Load YAML file
		yaml = self.yaml_loader('ats_friendly_keywords_into_experiences')
		jd_keywords = self.load_txt_files(self.jd_keyword_extraction_file_path)		
		task_description = yaml[0].format(jd_keywords = jd_keywords)
		expected_output = yaml[1]

		return Task(
			description=task_description,
			expected_output=expected_output,
			agent=self.ats_keyword_integration_agent(),
			context=[self.gather_info_of_choosen_experiences()],
			output_file=self.ats_friendly_keywords_into_experiences_file_path,
		)

	@task
	def split_context_of_ats_friendly_keywords_into_experiences(self):
		# TODO: Instead making agent doing this split, use a tool to split the context.

		return Task(
			config=self.tasks_config["split_context_of_ats_friendly_keywords_into_experiences"],
			agent=self.generalist_agent(),
			context=[self.ats_friendly_keywords_into_experiences_task()],
			output_file=self.split_context_of_ats_friendly_keywords_into_experiences_file_path,
		)
	
	@task
	def career_objective_task(self):
		# Load YAML file
		yaml = self.yaml_loader('career_objective_task')

		job_description = self.load_txt_files(self.jd_keyword_extraction_file_path)
		task_description = yaml[0].format(job_description = job_description)
		expected_output = yaml[1]

		return Task(
			description=task_description,
			expected_output=expected_output,
			agent=self.career_objective_agent(),
			context=[self.split_context_of_ats_friendly_skills_task(), self.split_context_of_ats_friendly_keywords_into_experiences()],
			output_file=self.career_objective_task_file_path,
		)

	@task
	def resume_in_json_task(self):

		context = []

		# Either way these context is needed to complete the task.

		context.append(self.split_context_of_ats_friendly_skills_task())
		context.append(self.split_context_of_ats_friendly_keywords_into_experiences())
		context.append(self.career_objective_task())

		# Load YAML file
		yaml = self.yaml_loader('resume_in_json_task')
		
		# append data to the yaml[0] in new paragraph
		description = yaml[0]
		expected_output = yaml[1]

		if(self.profile_already_created()):

			print("Profile already found. Simply loading the output txt files in the context.")
			# load the output txt files and append to the yaml[0] in new paragraph, No need to build profile from scratch.
			data = self.load_all_txt_files(self.info_extraction_folder_path)
			description = description + "\n" + data
			print("---------------Profile loaded successfully. Input IS:--------------")
			print(description)
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
				output_file = self.resume_in_json_file_path,
			)
	
	@task
	def resume_compilation_task(self):
		return Task(
			config=self.tasks_config["resume_compilation_task"],
			agent=self.resume_compilation_agent(),
			context=[self.resume_in_json_task()],
			output_file=self.resume_compilation_task_file_path,
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the user info organizer crew"""

		tasks = []
	
		# if needs to change here, remember to change in the resume_in_json_task as well.
		if(not self.profile_already_created()):
			tasks.append(self.personal_information_extraction_task())
			tasks.append(self.education_extraction_task())
			tasks.append(self.volunteer_work_extraction_task())
			tasks.append(self.awards_recognitions_extraction_task())
			tasks.append(self.references_extraction_task())
			tasks.append(self.personal_traits_interests_extraction_task())
			tasks.append(self.miscellaneous_extraction_task())
			tasks.append(self.profile_builder_task())
			tasks.append(self.work_experience_extraction_task())
			tasks.append(self.project_experience_extraction_task())
			tasks.append(self.skills_from_exp_and_project_task())
			tasks.append(self.skills_extraction_task())

		# Either way, these tasks will be executed.
		tasks.append(self.ats_friendly_skills_task())
		tasks.append(self.split_context_of_ats_friendly_skills_task())
		tasks.append(self.experience_choosing_task())
		tasks.append(self.split_context_of_experience_choosing_task())
		tasks.append(self.gather_info_of_choosen_experiences())
		tasks.append(self.ats_friendly_keywords_into_experiences_task())
		tasks.append(self.split_context_of_ats_friendly_keywords_into_experiences())
		tasks.append(self.career_objective_task())
		tasks.append(self.resume_in_json_task())
		tasks.append(self.resume_compilation_task())
		
		
		# Return the crew
		return Crew(
			max_rpm=11,
			agents=self.agents,
			tasks=tasks,
			# cache=True,
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
			},
			output_log_file='output_log.txt',
		)
	
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
		path = self.info_extraction_folder_path  # Get the path of the folder
		entries = os.listdir(path)
		
		# Loop through each entry in the directory
		for entry in entries:
			full_path = os.path.join(path, entry)  # Get the full path of the entry
			if os.path.isfile(full_path):  # Check if it is a file
				# if a single file found, then I am assuming that the profile is already created.
				return True
		return False
	

# To reset all the files

	# def clear_file_content(self):
	# 	"""Creates the necessary files for the crew"""
	# 	for file_path in self.file_paths.values():
	# 		try:
	# 			open(file_path, 'w', encoding='utf-8').close()
	# 		except Exception as e:
	# 			print(f"Error while creating the file: {e}")
	
	# Dictionary to store file paths
	# file_paths = {

	# 	"volunteer_work_extraction_task": volunteer_work_extraction_task_file_path,
	# 	"awards_recognitions_extraction_task": awards_recognitions_extraction_task_file_path,
	# 	"references_extraction_task": references_extraction_task_file_path,
	# 	"personal_traits_interests_extraction_task": personal_traits_interests_extraction_task_file_path,
	# 	"miscellaneous_extraction_task": miscellaneous_extraction_task_file_path,

	# 	"personal_information_extraction_task": personal_information_extraction_task_file_path,
	# 	"education_extraction_task": education_extraction_task_file_path,
		
		
	# 	"work_experience_extraction_task": work_experience_extraction_task_file_path,
	# 	"project_experience_extraction_task": project_experience_extraction_task_file_path,
	# 	"skills_from_exp_and_project": skills_from_exp_and_project_file_path,
	# 	"all_togather_skills_extraction_task": all_togather_skills_extraction_task_file_path,
		
	# 	"ats_friendly_skills_pre_task": ats_friendly_skills_pre_task_file_path,
	# 	"split_context_of_ats_friendly_skills_task": split_context_of_ats_friendly_skills_task_file_path,
	# 	"experience_choosing_task": experience_choosing_task_file_path,

	# 	"split_context_of_experience_choosing_task": split_context_of_experience_choosing_task_file_path,

	# 	"gather_info_of_choosen_experiences": gather_info_of_choosen_experiences_file_path,
	# 	"include_ats_keywords_into_experiences": ats_friendly_keywords_into_experiences_file_path,
	# 	"split_context_of_ats_friendly_keywords_into_experiences": split_context_of_ats_friendly_keywords_into_experiences_file_path,
	# 	"career_objective_task": career_objective_task_file_path,
	# 	"resume_json_task": resume_json_file_path,
	# 	"resume_compilation_task": resume_compilation_task_file_path,

		

	# }