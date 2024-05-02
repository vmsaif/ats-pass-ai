"""
	Author: Saif Mahmud
	Date: 04-23-2024
	Description: This file contains the main function to run the ATS-PASS-AI
"""
from textwrap import dedent
from ats_pass_ai.user_info_organizer_crew import UserInfoOrganizerCrew
from ats_pass_ai.tools.rag_search_tool import RagSearchTool
from ats_pass_ai.tools.llm_task import LLMTask


def run():

    # First, Lets Organize the User Information provided by the user.
    user_info_file_path = 'info_files/user_info.txt'
    user_info_orgainzed_file_path = 'info_files/user_info_organized.txt'
    job_description_file_path = 'info_files/job_description.txt'
    job_description_extracted_keywords_file_path = 'info_extraction/job_description_extracted_keywords.txt'

    # This will not run if there is already an organized file,
    organize_system_instruction = dedent("""
				Task: Content Organization and Structuring
				Objective: Reorganize provided unstructured content into a clear, structured format without missing any details. Every detail in the content is important and should be included in the final output.
				Instructions:
				1. Comprehension: Read the content to understand the themes and details.
				2. Structure Development:
					- Main Categories: Identify and label key themes with '#'.
					- Subcategories: Create necessary subcategories under each main category with '##'.
				3. Content Handling:
					- Preservation: Ensure all original information (links, dates, names) is included.
					- Clarity and Readability: Use clear headings, subheadings, and bullet points to enhance readability.
				4. Personal Content Handling:
					- Summarize personal narratives or self-descriptions in third-person, without categorization.
				5. Final Review: Check the structured content for completeness, accuracy, and coherence.Outcome: Deliver a well-organized document that maintains all original details in an accessible format.
				""")
    organizer = LLMTask("User Info Organize", user_info_file_path, user_info_orgainzed_file_path, organize_system_instruction, override=False)
    organizer.run()

    # Now, lets extract the keywords from the job description
    jd_extraction_system_instruction = dedent("""
                Task: Job Description Keyword and Phrases Extraction
                Objective: Extract relevant keywords and phrases from the provided job description.
                Instructions:
                1. Read the Job Description: Read the job description to understand the requirements and responsibilities.
                2. About the company: Understand the company's background and culture. Extract phrases that can be used to tailor the resume or a cover letter.
                3. Keyword Identification: Identify important keywords and phrases related to the job description.
                4. Keyword Extraction: Extract the relevant keywords and phrases from the job description.
                5. Keyword List: Create a list of extracted keywords and phrases.
                6. Review: Review the extracted keywords and phrases for relevance and accuracy.
                Outcome: Deliver a list of relevant keywords and phrases extracted from the job description.
                
                Purpose of this task: These keywords will be used to make a resume that is ATS friendly.
    """)

    job_description_extractor = LLMTask("Job desc keyword extraction",job_description_file_path, job_description_extracted_keywords_file_path, jd_extraction_system_instruction, override=True)
    job_description_extractor.run()

    # this will not run if the file is already indexed
    # RagSearchTool.process_and_index(user_info_orgainzed_file_path)

    
    # Now, lets call the main crew to build the resume
    # UserInfoOrganizerCrew().crew().kickoff()
    
    # inputs = {
    #     'user_info_orgainzed_file_path': user_info_orgainzed_file_path
    # }
    # UserInfoOrganizerCrew().crew().kickoff(inputs=inputs)
    
