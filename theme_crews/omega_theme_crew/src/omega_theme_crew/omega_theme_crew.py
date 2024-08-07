# -*- coding: utf-8 -*-
"""
	Author: Saif Mahmud
	Date: 04-23-2024
	Description: This file contains the crew class for the applicant info organizer crew.
"""
import os
import yaml
import agentops

from langchain_google_genai import GoogleGenerativeAI, HarmBlockThreshold, HarmCategory
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from util.limiter import Limiter
from path.output_file_paths import PATHS
from omega_theme_crew.omega_file_paths import OMEGA_PATHS

@CrewBase
class OmegaThemeCrew:
	"""Resume Maker Crew"""
	agents_config = 'config/omega_theme_agents.yaml'
	tasks_config_path = 'config/omega_theme_tasks.yaml'
	tasks_config = tasks_config_path # because tasks_config somehow getting recognized as a dictionary, not a simple string path.

	# agentops.init(tags=["resume-crew"])

	genAI = GoogleGenerativeAI(
		model="gemini-pro",
		temperature=0.7,
		safety_settings = {
			HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
			HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
			HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
			HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
		},
	)

	small_limiter = Limiter(llm_size='SMALL', llm = genAI, langchainMethods=True)
	
	# rpd, rpm limiter, these will be used on agents
	small_llm_limiter = small_limiter.request_limiter

	# token limiter, these will be used on the tasks to limit the token usage.
	small_token_limiter = small_limiter.record_token_usage

	debugFlag = False

	# debugFlag = True

	@crew
	def crew(self) -> Crew:
		"""Creates the applicant info organizer crew"""

		tasks = [
			self.name_section(),
			self.concise_jd_task(),

			# ---- set Column 1 content -----
			self.remove_data(),
			self.data_extraction(),
			self.relevance_assessment(),
			self.final_selection(),


			# --- latex of column 1 ---
			self.education_section(),
			self.coursework_section(),
			self.volunteer_section(),
			self.references_section(), 
			self.skill_section(),

			# Column 2 content
			self.career_objective_section(),

			self.summary_point_selector(),
			self.link_handler(),
			self.link_latex(),
			self.experience_section(),
			self.exp_latex_verified()
		]
		
		# Return the crew
		return Crew(
			agents=self.agents,
			tasks=tasks,
			language="en",
			# cache=True,
			full_output=True,
			process=Process.sequential,
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
	def latex_maker_agent(self) -> Agent:
		# load yaml
		yaml = self.yaml_loader("latex_maker_agent", False)
		return Agent(
			role=yaml[0],
			goal=yaml[1],
			backstory=yaml[2],
			allow_delegation=False,
			# verbose=True,
			llm=self.genAI,
			step_callback=self.small_llm_limiter,
			# llm=self.genAILarge,
			# step_callback=self.large_llm_limiter
		)
	
	@agent
	def basic_agent(self) -> Agent:
		# load yaml
		yaml = self.yaml_loader("basic_agent", False)
		return Agent(
			role=yaml[0],
			goal=yaml[1],
			backstory=yaml[2],
			allow_delegation=False,
			# verbose=True,
			llm=self.genAI,
			step_callback=self.small_llm_limiter,
		)

	@agent
	def profile_data_extractor_agent(self) -> Agent:
		# load yaml
		yaml = self.yaml_loader("profile_data_extractor_agent", False)
		return Agent(
			role=yaml[0],
			goal=yaml[1],
			backstory=yaml[2],
			allow_delegation=False,
			# verbose=True,
			llm=self.genAI,
			step_callback=self.small_llm_limiter,
		)
	
	@agent
	def relevance_and_prioritization_agent(self) -> Agent:
		# load yaml
		yaml = self.yaml_loader("relevance_and_prioritization_agent", False)
		return Agent(
			role=yaml[0],
			goal=yaml[1],
			backstory=yaml[2],
			allow_delegation=False,
			# verbose=True,
			llm=self.genAI,
			step_callback=self.small_llm_limiter,
		)

	@task
	def name_section(self):

		yaml = self.yaml_loader("name_section", True)
		description = yaml[0]
		expected_output = yaml[1]
		
		description = description + "\n\n" + self.load_file(PATHS["personal_information_extraction_task"])

		return Task(
			description=description,
			expected_output=expected_output,
			agent=self.latex_maker_agent(),
			output_file=OMEGA_PATHS["name_section"],
			callback=self.small_token_limiter
		)
	
	@task
	def concise_jd_task(self):
		yaml = self.yaml_loader("concise_jd_task", True)
		description = yaml[0]
		expected_output = yaml[1]
		description = description + "\n\n" + self.load_file(PATHS["jd_file_path"])

		return Task(
			description=description,
			expected_output=expected_output,
			agent=self.basic_agent(),
			output_file=OMEGA_PATHS["concise_jd_task"],
			callback=self.small_token_limiter
		)

	@task
	def remove_data(self):
		yaml = self.yaml_loader("remove_data", True)
		description = yaml[0]
		expected_output = yaml[1]

		description = description + "\n\n" + self.load_file(PATHS["profile_builder_task"])

		return Task(
			description=description,
			expected_output=expected_output,
			agent=self.profile_data_extractor_agent(),
			output_file=OMEGA_PATHS["remove_data"],
			callback=self.small_token_limiter
		)

	@task
	def data_extraction(self):
		yaml = self.yaml_loader("data_extraction", True)
		description = yaml[0]
		expected_output = yaml[1]

		description = description + "\nRelevant Courses:\n" + self.load_file(PATHS["coursework_extraction_task"])

		if self.debugFlag:
			description = description + "\n\n" + self.load_file(OMEGA_PATHS["remove_data"])

		return Task(
			description=description,
			expected_output=expected_output,
			agent=self.profile_data_extractor_agent(),
			context=[self.remove_data()],
			output_file=OMEGA_PATHS["data_extraction"],
			callback=self.small_token_limiter
		)

	@task
	def relevance_assessment(self):
		yaml = self.yaml_loader("relevance_assessment", True)
		description = yaml[0]
		expected_output = yaml[1]

		description = description + "\n\n" + self.load_file(OMEGA_PATHS["concise_jd_task"])

		if self.debugFlag:
			description = description + "\n\n" + self.load_file(OMEGA_PATHS["data_extraction"])

		return Task(
			description=description,
			expected_output=expected_output,
			agent=self.relevance_and_prioritization_agent(),
			context=[self.data_extraction()],
			output_file=OMEGA_PATHS["relevance_assessment"],
			callback=self.small_token_limiter
		)
		
	@task
	def final_selection(self):
		yaml = self.yaml_loader("final_selection", True)
		description = yaml[0]
		expected_output = yaml[1]

		if self.debugFlag:
			description = description + "\n\n" + self.load_file(OMEGA_PATHS["relevance_assessment"])

		return Task(
			description=description,
			expected_output=expected_output,
			agent=self.relevance_and_prioritization_agent(),
			context=[self.relevance_assessment()],
			output_file=OMEGA_PATHS["final_selection"],
			callback=self.small_token_limiter
		)

	# @task
	# def assess_and_prioritize(self):
	# 	yaml = self.yaml_loader("assess_and_prioritize", True)
	# 	description = yaml[0]
	# 	expected_output = yaml[1]

	# 	if(self.debugFlag):
	# 		description = description + "\n\n" + self.load_file(OMEGA_PATHS["concise_jd_task"])
	
	# 	description = description + "\n\n" + self.load_file(PATHS["profile_builder_task"])
	# 	description = description + "\n\n" + self.load_file(PATHS["coursework_extraction_task"])

	# 	return Task(
	# 		description=description,
	# 		expected_output=expected_output,
	# 		agent=self.content_selector_agent(),
	# 		context=[self.concise_jd_task()],
	# 		output_file=OMEGA_PATHS["assess_and_prioritize"],
	# 		callback=self.small_token_limiter
	# 	)



	# @task
	# def split_content_of_select_first_column_content(self):
	# 	yaml = self.yaml_loader("split_content_of_select_first_column_content", True)
		
	# 	description = yaml[0]
	# 	expected_output = yaml[1]
		
	# 	if self.debugFlag:
	# 		description += "\n\n" + self.load_file(PATHS["select_first_column_content"])

	# 	return Task(
	# 		description=description,
	# 		expected_output=expected_output,
	# 		agent=self.basic_agent(),
	# 		context=[self.select_first_column_content()],
	# 		output_file=PATHS["split_content_of_select_first_column_content"],
	# 		callback=self.small_token_limiter
	# 	)

	@task
	def education_section(self):
		yaml = self.yaml_loader("education_section", True)
		description = yaml[0]
		expected_output = yaml[1]
		
		if(self.debugFlag):
			description = description + "\n\n" + self.load_file(OMEGA_PATHS["final_selection"])

		return Task(
			description=description,
			expected_output=expected_output,
			agent=self.latex_maker_agent(),
			context=[self.final_selection()],
			output_file=OMEGA_PATHS["education_section"],
			callback=self.small_token_limiter
		)
	
	@task
	def skill_section(self):
		yaml = self.yaml_loader("skill_section", True)

		description = yaml[0] + "\n\n" + self.load_file(PATHS["correct_categorization_of_skills_task"])

		expected_output = yaml[1]

		return Task(
			description=description,
			expected_output=expected_output,
			agent=self.latex_maker_agent(),
			output_file=OMEGA_PATHS["skill_section"],
			callback=self.small_token_limiter
		)
	
	@task
	def coursework_section(self):
		yaml = self.yaml_loader("coursework_section", True)
		description = yaml[0]
		expected_output = yaml[1]
		
		if(self.debugFlag):
			description = description + "\n\n" + self.load_file(OMEGA_PATHS["final_selection"])

		return Task(
			description=description,
			expected_output=expected_output,
			agent=self.latex_maker_agent(),
			context=[self.final_selection()],
			output_file=OMEGA_PATHS["coursework_section"],
			callback=self.small_token_limiter
		)

	@task
	def volunteer_section(self):
		yaml = self.yaml_loader("volunteer_section", is_task=True)
		description = yaml[0]
		expected_output = yaml[1]

		if(self.debugFlag):
			description = description + "\n\n" + self.load_file(OMEGA_PATHS["final_selection"])

		return Task(
			description=description,
			expected_output=expected_output,
			agent=self.latex_maker_agent(),
			context=[self.final_selection()],
			output_file=OMEGA_PATHS["volunteer_section"],
			callback=self.small_token_limiter
		)
	
	@task
	def references_section(self):
		yaml = self.yaml_loader("references_section", True)
		description = yaml[0]
		expected_output = yaml[1]

		if(self.debugFlag):
			description = description + "\n\n" + self.load_file(OMEGA_PATHS["final_selection"])

		return Task(
			description=description,
			expected_output=expected_output,
			agent=self.latex_maker_agent(),
			context=[self.final_selection()],
			output_file=OMEGA_PATHS["references_section"],
			callback=self.small_token_limiter
		)
	
	@task
	def career_objective_section(self):
		yaml = self.yaml_loader("career_objective_section", True)
		description = yaml[0]
		expected_output = yaml[1]
		description = description + "\n\n" + self.load_file(PATHS["career_objective_task"])

		return Task(
			description=description,
			expected_output=expected_output,
			agent=self.latex_maker_agent(),
			output_file=OMEGA_PATHS["career_objective_section"],
			callback=self.small_token_limiter
		)
	
	# @task
	# def exp_item_count_chooser(self):
	# 	yaml = self.yaml_loader("exp_item_count_chooser", True)
	# 	description = yaml[0]
	# 	expected_output = yaml[1]
	# 	description = description + "\n\n" + self.load_file(PATHS["split_context_of_ats_friendly_keywords_into_experiences"])

	# 	return Task(
	# 		description=description,
	# 		expected_output=expected_output,
	# 		agent=self.expItemSelectorAgent(),
	# 		output_file=OMEGA_PATHS["exp_item_count_chooser"],
	# 		callback=self.small_token_limiter
	# 	)

	# @task
	# def exp_item_chooser(self):
	# 	yaml = self.yaml_loader("exp_item_chooser", True)
	# 	description = yaml[0]
	# 	expected_output = yaml[1]

	# 	if(self.debugFlag):
	# 		description = description + "\n\n" + self.load_file(OMEGA_PATHS["exp_item_count_chooser"])

	# 	return Task(
	# 		description=description,
	# 		expected_output=expected_output,
	# 		agent=self.expItemSelectorAgent(),
	# 		context=[self.exp_item_count_chooser()],
	# 		output_file=OMEGA_PATHS["exp_item_chooser"],
	# 		callback=self.small_token_limiter
	# 	)

	@task
	def summary_point_selector(self):
		yaml = self.yaml_loader("summary_point_selector", True)
		description = yaml[0]
		expected_output = yaml[1]

		description = description + "\n\n" + self.load_file(PATHS["split_context_of_ats_friendly_keywords_into_experiences"])

		return Task(
			description=description,
			expected_output=expected_output,
			agent=self.basic_agent(),
			output_file=OMEGA_PATHS["summary_point_selector"],
			callback=self.small_token_limiter
		)
	
	@task
	def link_handler(self):
		yaml = self.yaml_loader("link_handler", True)
		description = yaml[0]
		expected_output = yaml[1]

		if(self.debugFlag):
			description = description + "\n\n" + self.load_file(OMEGA_PATHS["summary_point_selector"])

		return Task(
			description=description,
			expected_output=expected_output,
			agent=self.basic_agent(),
			context=[self.summary_point_selector()],
			output_file=OMEGA_PATHS["link_handler"],
			callback=self.small_token_limiter
		)
	
	@task
	def link_latex(self):
		yaml = self.yaml_loader("link_latex", True)
		description = yaml[0]
		expected_output = yaml[1]

		if(self.debugFlag):
			description = description + "\n\n" + self.load_file(OMEGA_PATHS["link_handler"])

		return Task(
			description=description,
			expected_output=expected_output,
			agent=self.latex_maker_agent(),
			context=[self.link_handler()],
			output_file=OMEGA_PATHS["link_latex"],
			callback=self.small_token_limiter
		)

	@task
	def experience_section(self):
		yaml = self.yaml_loader("experience_section", True)
		description = yaml[0]
		expected_output = yaml[1]

		if(self.debugFlag):
			description = description + "\n\n" + self.load_file(OMEGA_PATHS["link_latex"])

		return Task(
			description=description,
			expected_output=expected_output,
			agent=self.latex_maker_agent(),
			callback=self.small_token_limiter,
			context=[self.link_latex()],
			output_file=OMEGA_PATHS["experience_section"],
			# agent=self.latex_maker_large_agent(),
			# callback=self.large_token_limiter
		)
	
	@task
	def exp_latex_verified(self):
		yaml = self.yaml_loader("exp_latex_verified", True)
		description = yaml[0]
		expected_output = yaml[1]

		if(self.debugFlag):
			description = description + "\n\n" + self.load_file(OMEGA_PATHS["experience_section"])

		return Task(
			description=description,
			expected_output=expected_output,
			agent=self.latex_maker_agent(),
			context=[self.experience_section()],
			output_file=OMEGA_PATHS["exp_latex_verified"],
			callback=self.small_token_limiter
		)

	def load_file(self, file_path):
		"""Load text file"""
		try:
			with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
				return file.read()
		except IOError as e:
			print(f"Omega Theme: Error opening or reading the file {file_path}: {e}")
			return ""

	def yaml_loader(self, item_name, is_task):
		# load the yaml file
		output = []
		if(is_task):
			path = OMEGA_PATHS['omega_theme_tasks']
		else:
			path = OMEGA_PATHS['omega_theme_agents']
		try:
			cwd = os.getcwd()
			with open (path, 'r') as file:
				yaml_data = yaml.safe_load(file)
				if(is_task):
					output.append(yaml_data[item_name]['description'])
					output.append(yaml_data[item_name]['expected_output'])
				else:
					output.append(yaml_data[item_name]['role'])
					output.append(yaml_data[item_name]['goal'])
					output.append(yaml_data[item_name]['backstory'])
		except IOError as e:
			print(f"YAML LOADER: Error opening or reading the file {path}: {e}")
		
		return output