"""
	Author: Saif Mahmud
	Date: 04-23-2024
	Description: This file contains the main function to run the ATS-PASS-AI
"""
from datetime import timedelta
from textwrap import dedent
from ats_pass_ai.limiter import printRemainingRequestsPerDay
from ats_pass_ai.resume_crew import ResumeCrew
from ats_pass_ai.themes_crew.omega_theme.omega_theme_crew import OmegaThemeCrew
from ats_pass_ai.tools.rag_search_tool import RagSearchTool
from ats_pass_ai.tools.llm_task import LLMTask
from ats_pass_ai.output_file_paths import PATHS
from ats_pass_ai.timer import Timer
from ats_pass_ai.latex_generator import compile_latex
# First, Lets Organize the applicant Information provided by the applicant.

applicant_info_file_path = PATHS["applicant_info_file_path"]
jd_file_path = PATHS["jd_file_path"]

# After organizing the applicant information, we will extract the keywords from the job description 
applicant_info_orgainzed_file_path = PATHS["applicant_info_organized"]
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

    Objective: Extract relevant keywords and phrases from the provided job description to optimize the resume for Applicant Tracking Systems (ATS) and human reviewers.

    Instructions:

    1. Introduction:
        - Role: [Role Title]
        - Company: [Company Name]
        - Location: [Location]
        - Industry: [Industry/Field]
    
    2. Thorough Analysis: Review the job description to understand required skills, responsibilities, qualifications, and company culture.
    
    3. Keyword Categorization: 
        * **Essential Skills:** Identify hard and soft skills emphasized in the job description.
        * **Industry Terms:** Extract common industry-specific terms.
        * **Company Values & Culture:** Note keywords reflecting the company's mission and values.
        * **Action Verbs:** List action verbs associated with required responsibilities.
    
    4. Prioritization and Relevance:
        * **Frequency and Emphasis:** Note frequently mentioned or emphasized keywords.
        * **Essential vs. Preferred Qualifications:** Distinguish between mandatory and preferred skills.

    5. Keyword List Creation: Compile the extracted keywords into a structured json format, categorized for easy reference.
    
    6. Partial Match Skills:
        * Create a list of "partial match" skills, categorizing skills that correspond to broader skills mentioned in the job description.
        * Format as JSON:
        {
            "list of skills": {
                "Essential Skills": [
                    {
                        "Name": "Skill 1", 
                        "Partial_Match": ["Partial Match 1", "Partial Match 2, upto 5"]
                    },
                    {
                        "Name": "Skill 2", 
                        "Partial_Match": ["Partial Match 1", "Partial Match 2, upto 5"]
                    }
                ]
            }
        }
        
    
    7. ATS Optimization Tips:
        * **Strategic Keyword Placement:** Integrate keywords naturally throughout your resume.
        * **Keyword Density:** Use keywords thoughtfully without "keyword stuffing."
        * **Tailoring and Customization:** Adapt keywords and content for each job application.

    Outcome: A comprehensive list of relevant keywords and actionable tips to optimize resume for ATS algorithms and human reviewers, enhancing interview prospects.
    """)

        with Timer() as t:
            organizer = LLMTask("Applicant Info Organize", 
                            applicant_info_file_path, 
                            applicant_info_orgainzed_file_path, 
                            organize_system_instruction, 
                            override=True
                        )
            # organizer.run()
        info_organizing_time = t.interval

        with Timer() as t:
            # Change the override to True to force the extraction, ie, new job description
            job_description_extractor = LLMTask("Job desc keyword extraction", 
                                                jd_file_path, 
                                                jd_extracted_keywords_file_path, 
                                                jd_extraction_system_instruction, 
                                                override=True
                                        )
            # job_description_extractor.run()
        jd_extraction_time = t.interval

        with Timer() as t:
            # Index into DB: this will not run if the file is already indexed
            RagSearchTool.process_and_index(applicant_info_orgainzed_file_path)
        indexing_time = t.interval

        with Timer() as t:         
            try:
                # Delete the applicant profile files but not the folder To start fresh
                # RagSearchTool.delete_applicant_profile_files(delete_pretasks = True)
                crew = ResumeCrew().crew()
                # crew.kickoff()
            except Exception as e:
                print(f"Error: {e}")
                # exit the program
                # print("Exiting the program due to error in crew kickoff")
                # exit(1)
                # crew.kickoff() # Retry once
        crew_run_time = t.interval
    
        with Timer() as t:
            omega_theme_crew = OmegaThemeCrew().crew()
            omega_theme_crew.kickoff()
            compile_latex(PATHS["omega_theme_final_output_tex"], PATHS["omega_theme_final_output_pdf"])
        latex_generation_time = t.interval

    program_run_time = total_time.interval
    
    # Print the time taken for each task
    print("---- Time Statistics -----")

    print_task_time("applicant Info Organizing", info_organizing_time)
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
