import os
import sys
from info_collection.tools.llm_task import LLMTask
from info_collection.llm_tasks_instructions import organize_system_instruction, jd_extraction_system_instruction, company_value_extraction_system_instruction

from info_collection.tools.web_scraper import WebScraper
from util.timer import Timer, print_task_time
from path.output_file_paths import PATHS

applicant_info_orgainzed_file_path = PATHS["applicant_info_organized"]
jd_extracted_keywords_file_path = PATHS["jd_keyword_extraction"]
company_value_extraction_file_path = PATHS["company_value_extraction"]


def run():
    
    if len(sys.argv) != 2:
        print(f"Please provide the job description link as an argument in \"DOUBLE\" quotes.\nExample: python main.py \"https://www.indeed.com/viewjob?jk=1234567890abcde\"")
        exit(1)

    args = sys.argv[1:]
    job_description_link = args[0]

    # Prepare and Organize Applicant's Info
    with Timer() as t:

        organizer = LLMTask("Applicant Info Organize", 
                        PATHS["applicant_info_file_path"], 
                        applicant_info_orgainzed_file_path, 
                        organize_system_instruction, 
                        override=False,
                        islargeLLM=True
                    )
        organizer.run()
    info_organizing_time = t.interval

    # Fetch the job description from the webpage link
    with Timer() as t:
        web_scraper_tool = WebScraper(job_description_link)
        web_scraper_tool.run()

    jd_fetch_time = t.interval

    with Timer() as t:
        jd_keywords_extractor = LLMTask("Job desc keyword extraction", 
            PATHS["jd_file_path"],
            jd_extracted_keywords_file_path, 
            jd_extraction_system_instruction, 
            override=False,
            islargeLLM=True
    )
        jd_keywords_extractor.run()
    jd_extraction_time = t.interval

    with Timer() as t:
        company_value_extraction = LLMTask("Company Value Extraction",
            PATHS["jd_file_path"],
            company_value_extraction_file_path,
            company_value_extraction_system_instruction,
            override=False,
            islargeLLM=False
        )
        company_value_extraction.run()
    company_value_extraction_time = t.interval

# def readFile(file_path):
#     cwd = os.getcwd()
#     print(f"Current Working Directory: {cwd}")
#     print(f"Reading file from path: {file_path}")
#     with open(file_path, 'r', encoding='utf-8') as file:
#         return file.read()

#     # print("---- Time Statistics -----")
#     # print_task_time("applicant Info Organizing", info_organizing_time)
#     # print_task_time("JD Fetch", jd_fetch_time)
#     # print_task_time("JD Extraction", jd_extraction_time)