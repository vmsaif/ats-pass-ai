"""
	Author: Saif Mahmud
	Date: 04-23-2024
	Description: This file contains the main function to run the ATS-PASS-AI
"""
from datetime import timedelta
from textwrap import dedent
from ats_pass_ai.request_limiter import printRemainingRequestsPerDay
from ats_pass_ai.resume_crew import ResumeCrew
from ats_pass_ai.tools.rag_search_tool import RagSearchTool, SearchInChromaDB
from ats_pass_ai.tools.llm_task import LLMTask
from ats_pass_ai.output_file_paths import PATHS
from ats_pass_ai.timer import Timer
from ats_pass_ai.latex_generator import compile_latex
# First, Lets Organize the User Information provided by the user.
user_info_file_path = 'info_files/user_info.txt'
jd_file_path = 'info_files/job_description.txt'

user_info_orgainzed_file_path = PATHS["user_info_organized"]
jd_extracted_keywords_file_path = PATHS["jd_keyword_extraction"]

def run():

    with Timer() as total_time:
        # This will not run if there is already an organized file,
        organize_system_instruction = dedent("""
                    Task: Content Organization and Structuring
                    Objective: Reorganize provided unstructured content into a clear, structured format without missing any details. Every detail in the content is important and should be included in the final output.
                    
                    Instructions:
                    1. Comprehension: Read the content to understand the themes and details. Each section should have a description of more than 2 lines on what it contains as it will help doing symanctic search on this document later.
                                             
                    2. Identification:
                        - Begin with identifying and documenting key personal identification details such as the applicant's name, contact information, location, phone number, and email address etc.
                        - Use the heading '# Personal Details' for this section.
                    3. Structure Development: 
                        - Write a description of each Category of more than 2 lines of what it contains. For example, if you have a section called "References", write, "This section contains the personnel who can provide references, testimonials or recommendations for the Aplicant."
                                             
                        For Coursework, you can write, "This section contains the courses taken by the Applicant during their academic career."
                                             
                        - Main Categories: Identify and label key themes with '#'.
                        - Subcategories: Create necessary subcategories under each main category with '##'.
                    4. Content Handling:
                        - Preservation: Ensure all original information (links, dates, names) is included.
                        - Clarity and Readability: Use clear headings, subheadings, and bullet points to enhance readability.
                    5. Personal Content Handling:
                        - Summarize personal narratives or self-descriptions in third-person, without categorization.
                    6. Final Review: Check the structured content for completeness, accuracy, and coherence. Make any necessary adjustments, ensuring that related information is grouped together. Also ensure that each section has a description of more than 2 lines on what it contains.
                                            
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
                                                  
                    6. Make a list of "partial match" skills. For example, if the job description mentions "Microsoft Office Suite," you can include "Microsoft Word," "Excel," "PowerPoint," etc. as partial matching skills. Later on this will be used to find comparable items from the applicant's skills. You should represent this as a json object with the following format:
                    {
                        "list of skills": {
                        "Essential Skills": [
                            {
                                Name: "Skill 1", 
                                Partial_Match: ["Partial Match 1", "Partial Match 2"]
                            },
                            {
                                Name: "Skill 2", 
                                Partial_Match: ["Partial Match 1", "Partial Match 2"]
                            }
                        ]
                    } 
                                                  
                    7. ATS Optimization Tips: 

                        * **Strategic Keyword Placement:**  Integrate keywords naturally throughout your resume, particularly in the skills section, experience descriptions, and summary/objective statement.
                        * **Keyword Density:** Use keywords thoughtfully and avoid excessive repetition or "keyword stuffing," which can be penalized by ATS algorithms.
                        * **Tailoring and Customization:** Adapt the extracted keywords and your resume content to each specific job application, highlighting the most relevant qualifications for each role.

                    Outcome: A comprehensive list of relevant keywords and actionable tips to optimize your resume for both ATS algorithms and human reviewers, increasing your chances of landing an interview.
                    """)

        with Timer() as t:
            organizer = LLMTask("User Info Organize", 
                            user_info_file_path, 
                            user_info_orgainzed_file_path, 
                            organize_system_instruction, 
                            override=False
                        )
            organizer.run()
        info_organizing_time = t.interval

        
        with Timer() as t:
            # Change the override to True to force the extraction, ie, new job description
            job_description_extractor = LLMTask("Job desc keyword extraction", 
                                                jd_file_path, 
                                                jd_extracted_keywords_file_path, 
                                                jd_extraction_system_instruction, 
                                                override=False
                                        )
            job_description_extractor.run()

        jd_extraction_time = t.interval

        with Timer() as t:
            # Index into DB: this will not run if the file is already indexed
            RagSearchTool.process_and_index(user_info_orgainzed_file_path)
        indexing_time = t.interval

        with Timer() as t:
            # Delete the user profile files but not the folder To start fresh
            # RagSearchTool.delete_user_profile_files(delete_pretasks = False)

            # Run the main crew program
            crew = ResumeCrew().crew()
            crew.kickoff()
            # print(crew.usage_metrics)
        crew_run_time = t.interval
    
        with Timer() as t:
            compile_latex(PATHS["latex_resume_generation_task"], PATHS["final_output_dir"])
        latex_generation_time = t.interval

    program_run_time = total_time.interval
    
    # Print the time taken for each task
    print("---- Time Statistics -----")

    print_task_time("User Info Organizing", info_organizing_time)
    print_task_time("JD Extraction", jd_extraction_time)
    print_task_time("Indexing", indexing_time)
    print_task_time("Crew Run", crew_run_time)
    print_task_time("Latex Generation", latex_generation_time)
    print_task_time("Total", program_run_time)
    printRemainingRequestsPerDay()

def print_task_time(task_name, total_seconds):
        days, hours, minutes, seconds = convert_seconds(total_seconds)
        print(f"-- Time taken for {task_name}: {minutes} minutes, {seconds} seconds")

def convert_seconds(total_seconds):
    # Extract days, seconds from timedelta
    td = timedelta(seconds=total_seconds)
    total_seconds = int(td.total_seconds())
    days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    # Format each component to two decimal places
    formatted_days = f"{days:.2f}"
    formatted_hours = f"{hours:.2f}"
    formatted_minutes = f"{minutes:.2f}"
    formatted_seconds = f"{seconds:.2f}"
    
    return formatted_days, formatted_hours, formatted_minutes, formatted_seconds
