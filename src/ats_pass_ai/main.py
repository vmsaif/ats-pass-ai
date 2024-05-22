"""
	Author: Saif Mahmud
	Date: 04-23-2024
	Description: This file contains the main function to run the ATS-PASS-AI
"""
from datetime import timedelta
import os
import sqlite3
from textwrap import dedent
from ats_pass_ai.request_limiter import RequestLimiter
from ats_pass_ai.resume_crew import ResumeCrew
from ats_pass_ai.tools.rag_search_tool import RagSearchTool
from ats_pass_ai.tools.llm_task import LLMTask
import time
from ats_pass_ai.output_file_paths import PATHS

# First, Lets Organize the User Information provided by the user.
user_info_file_path = 'info_files/user_info.txt'
jd_file_path = 'info_files/job_description.txt'

user_info_orgainzed_file_path = PATHS["user_info_organized"]
jd_extracted_keywords_file_path = PATHS["jd_keyword_extraction"]


def run():

    start_main_time = time.perf_counter()

    # This will not run if there is already an organized file,
    organize_system_instruction = dedent("""
                Task: Content Organization and Structuring
                Objective: Reorganize provided unstructured content into a clear, structured format without missing any details. Every detail in the content is important and should be included in the final output.
                
                Instructions:
                1. Comprehension: Read the content to understand the themes and details.
                2. Identification:
                    - Begin with identifying and documenting key personal identification details such as the user's name, contact information, location, phone number, and email address etc.
                    - Use the heading '### Personal Details' for this section.
                3. Structure Development:
                    - Main Categories: Identify and label key themes with '#'. 
                    - Subcategories: Create necessary subcategories under each main category with '##'.
                4. Content Handling:
                    - Preservation: Ensure all original information (links, dates, names) is included.
                    - Clarity and Readability: Use clear headings, subheadings, and bullet points to enhance readability.
                5. Personal Content Handling:
                    - Summarize personal narratives or self-descriptions in third-person, without categorization.
                6. Final Review: Check the structured content for completeness, accuracy, and coherence. Make any necessary adjustments, ensuring that related information is grouped together.
                                         
                Outcome: Deliver a well-organized document that maintains all original details in an accessible format.
                """)

    # Now, lets extract the keywords from the job description
    jd_extraction_system_instruction = dedent("""
                Task: Job Description Keyword and Phrase Extraction for Resume Optimization

                Objective: Extract relevant keywords and phrases from the provided job description to optimize your resume for Applicant Tracking Systems (ATS) and human reviewers.

                Instructions:

                1. Make a short introduction of the role and the company.
                    Role: [Role Title]
                    Company: [Company Name]
                    Location: [Location]
                    Industry: [Industry/Field]
                  
                2. Thorough Analysis: Carefully read the job description to understand the required skills, responsibilities, qualifications, company culture, and overall job context. 

                3. Keyword Categorization: 

                    * **Essential Skills:** Identify the core skills and qualifications emphasized in the job description, including both hard skills (e.g., specific software, tools, technical abilities) and soft skills (e.g., communication, teamwork, problem-solving).
                    * **Industry/Field Specific Terms:**  Extract keywords and phrases commonly used within the specific industry or field of the job. 
                    * **Company Values & Culture:** Identify keywords that reflect the company's mission, values, and work environment (e.g., innovation, collaboration, customer-focus). 
                    * **Action Verbs:** Extract action verbs associated with skills and responsibilities (e.g., manage, develop, implement, lead) to showcase your abilities effectively.

                4. Prioritization and Relevance:

                    * **Frequency and Emphasis:** Pay close attention to keywords mentioned multiple times or with particular emphasis in the job description.
                    * **Required vs. Preferred Qualifications:** Differentiate between essential requirements and preferred or "nice-to-have" skills.
                    * **Alignment with Your Background:** Focus on extracting keywords that align with your skills and experience, ensuring you can genuinely demonstrate those qualities.

                5. Keyword List Creation: Create a structured list or table with the extracted keywords organized by category for easy reference.

                6. ATS Optimization Tips: 

                    * **Strategic Keyword Placement:**  Integrate keywords naturally throughout your resume, particularly in the skills section, experience descriptions, and summary/objective statement.
                    * **Keyword Density:** Use keywords thoughtfully and avoid excessive repetition or "keyword stuffing," which can be penalized by ATS algorithms.
                    * **Tailoring and Customization:** Adapt the extracted keywords and your resume content to each specific job application, highlighting the most relevant qualifications for each role.

                                              
                
                Outcome: A comprehensive list of relevant keywords and actionable tips to optimize your resume for both ATS algorithms and human reviewers, increasing your chances of landing an interview.
                """)

    start_time = time.perf_counter()
    organizer = LLMTask("User Info Organize", 
                        user_info_file_path, 
                        user_info_orgainzed_file_path, 
                        organize_system_instruction, 
                        override=True
                    ).run()
    
    end_time = time.perf_counter()
    info_organizing_time = (end_time - start_time) / 60

    start_time = time.perf_counter()
    # Change the override to True to force the extraction, ie, new job description
    job_description_extractor = LLMTask("Job desc keyword extraction", 
                                        jd_file_path, 
                                        jd_extracted_keywords_file_path, 
                                        jd_extraction_system_instruction, 
                                        override=True
                                ).run()

    end_time = time.perf_counter()
    jd_extraction_time = (end_time - start_time) / 60

    # Index into DB: this will not run if the file is already indexed
    start_time = time.perf_counter()
	
    RagSearchTool.process_and_index(user_info_orgainzed_file_path)
	
    end_time = time.perf_counter()
    indexing_time = (end_time - start_time) / 60

    # Now, call the main crew to build the resume
    start_time = time.perf_counter()

    # Delete the user profile files but not the folder To start fresh
    RagSearchTool.delete_user_profile_files(delete_pretasks = True)
	
    # Run the main crew program
    ResumeCrew().crew().kickoff()

    end_time = time.perf_counter()
    crew_run_time = (end_time - start_time) / 60
    end_main_time = time.perf_counter()
    program_run_time = (end_main_time - start_main_time) / 60
    
    # Print the time taken for each task
    print("---- Time Statistics -----")
    print(f"-- Time taken for User Info Organizing: {info_organizing_time:.2f} minutes")
    print(f"-- Time taken for JD Extraction: {jd_extraction_time:.2f} minutes")
    print(f"-- Time taken for Indexing: {indexing_time:.2f} minutes")
    print(f"-- Time taken for Crew Run: {crew_run_time:.2f} minutes")
    print(f"-- Total Time taken: {program_run_time:.2f} minutes")
    printDailyLimitRemaining()
	
def printDailyLimitRemaining():
    now = time.time()

    for llm_size, daily_limit in [
        ('large', RequestLimiter.LLM_LARGE_DAILY_REQUEST_LIMIT),
        ('small', RequestLimiter.LLM_SMALL_DAILY_REQUEST_LIMIT)
    ]:
        db_file = getattr(RequestLimiter, f"DB_FILE_{llm_size.upper()}_LLM")
        db_path = os.path.join(RequestLimiter.DB_DIR, db_file)
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT count, first_request_time FROM Requests')
                row = cursor.fetchone()

                if row:
                    first_request_time = row[1]
                    time_since_first_request = now - first_request_time
                    remaining_requests = daily_limit - row[0]
                    time_remaining_until_reset = RequestLimiter.DAY_IN_SECONDS - time_since_first_request
                else:
                    # If no data found, assume no requests have been made yet
                    remaining_requests = daily_limit
                    time_remaining_until_reset = RequestLimiter.DAY_IN_SECONDS

                days, hours, minutes, seconds = convert_seconds(time_remaining_until_reset)
                print(f"{llm_size.capitalize()} LLM: requests remaining: {remaining_requests} with time until reset: {days} days, {hours} hours, {minutes} minutes, {seconds} seconds")

        except Exception as e:
            print(f"Error connecting to {llm_size.capitalize()} LLM database: {e}")


def convert_seconds(seconds):
    # Create a timedelta object from the number of seconds
    td = timedelta(seconds=seconds)
    
    # Extract days, hours, minutes, and seconds from the timedelta object
    days = td.days
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    return days, hours, minutes, seconds    
