import os
import sys
from info_collection.tools.llm_task import LLMTask
from info_collection.llm_tasks_instructions import organize_system_instruction, jd_extraction_system_instruction, company_value_extraction_system_instruction, job_description_fetch_system_instruction

from info_collection.tools.web_scraper import WebScraper
from util.timer import Timer, print_task_time
from path.output_file_paths import PATHS

def run():
    
    # Check if the user provided the job description link as an argument
    if len(sys.argv) != 2:
        print(f"len(sys.argv): {len(sys.argv)}")
        print(f"Please provide the job description link as an argument in \"DOUBLE\" quotes.\nExample: python main.py \"https://www.indeed.com/viewjob?jk=1234567890abcde\" or the job description text's file path.\nExample: python main.py \"path/to/job_description.txt\"")
        exit(1)

    args = sys.argv[1:]
    job_description = args[0]

    # Prepare and Organize Applicant's Info
    organizer = LLMTask("Applicant Info Organize", 
                    PATHS["applicant_info_file_path"], 
                    PATHS["applicant_info_organized"], 
                    organize_system_instruction, 
                    override=False,
                    islargeLLM=True
                )
    
    # Fetch the job description from the webpage link
    web_scraper_tool = WebScraper(job_description,
                        job_description_fetch_system_instruction)

    # Extract Keywords from the Job Description with Large LLM
    jd_keywords_extractor = LLMTask("Job desc keyword extraction", 
            PATHS["jd_file_path"],
            PATHS["jd_keyword_extraction"], 
            jd_extraction_system_instruction, 
            override=True,
            islargeLLM=True
    )

    # Extract Company Values from the Job Description with Small LLM
    company_value_extraction = LLMTask("Company Value Extraction",
        PATHS["jd_file_path"],
        PATHS["company_value_extraction"],
        company_value_extraction_system_instruction,
        override=True,
        islargeLLM=False
    )

    # RUN THE TASKS
    organizer.run()   
    web_scraper_tool.run()
    jd_keywords_extractor.run()
    company_value_extraction.run()

