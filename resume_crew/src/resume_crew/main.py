
"""
	Author: Saif Mahmud
	Date: 04-23-2024
	Description: This file contains the main function to run the ATS-PASS-AI
"""

import time
import traceback
from resume_crew.resume_crew import ResumeCrew
from util.timer import Timer, print_task_time
from resume_crew.tools.rag_search_tool import RagSearchTool
from path.output_file_paths import PATHS

applicant_info_orgainzed_file_path = PATHS["applicant_info_organized"]

def run():

    # Index Applicant's info DB to make it searchable
    # this will not run if the file is already indexed
    ragSearchTool = RagSearchTool()
    ragSearchTool.process_and_index(applicant_info_orgainzed_file_path)

    # Run the Resume Crew
    try:
        crew = ResumeCrew().crew()
        crew.kickoff()
    except Exception as e:
        traceback.print_exc()
        exit(1)

