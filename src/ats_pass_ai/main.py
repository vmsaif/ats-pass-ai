"""
	Author: Saif Mahmud
	Date: 04-23-2024
	Description: This file contains the main function to run the ATS-PASS-AI
"""
from textwrap import dedent
from ats_pass_ai.resume_crew import ResumeCrew
from ats_pass_ai.tools.rag_search_tool import RagSearchTool
from ats_pass_ai.tools.llm_task import LLMTask


# First, Lets Organize the User Information provided by the user.
user_info_file_path = 'info_files/user_info.txt'
user_info_orgainzed_file_path = 'info_files/user_info_organized.txt'
jd_file_path = 'info_files/job_description.txt'
jd_extracted_keywords_file_path = ResumeCrew.jd_keyword_and_phrases_extraction_task_file_path


def run():

    # This will not run if there is already an organized file,
    organize_system_instruction = dedent("""
                Task: Content Organization and Structuring
                Objective: Reorganize provided unstructured content into a clear, structured format without missing any details. Every detail in the content is important and should be included in the final output.
                Instructions:
                1. Comprehension: Read the content to understand the themes and details.
                2. Identification:
                    - Begin with identifying and documenting key personal identification details such as the user's name.
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

    organizer = LLMTask("User Info Organize", user_info_file_path, user_info_orgainzed_file_path, organize_system_instruction, override=False)
    organizer.run()

    # Now, lets extract the keywords from the job description
    jd_extraction_system_instruction = dedent("""
                Task: Job Description Keyword and Phrase Extraction for Resume Optimization

                Objective: Extract relevant keywords and phrases from the provided job description to optimize your resume for Applicant Tracking Systems (ATS) and human reviewers.

                Instructions:

                1. Thorough Analysis: Carefully read the job description to understand the required skills, responsibilities, qualifications, company culture, and overall job context.

                2. Keyword Categorization: 

                    * **Essential Skills:** Identify the core skills and qualifications emphasized in the job description, including both hard skills (e.g., specific software, tools, technical abilities) and soft skills (e.g., communication, teamwork, problem-solving).
                    * **Industry/Field Specific Terms:**  Extract keywords and phrases commonly used within the specific industry or field of the job. 
                    * **Company Values & Culture:** Identify keywords that reflect the company's mission, values, and work environment (e.g., innovation, collaboration, customer-focus). 
                    * **Action Verbs:** Extract action verbs associated with skills and responsibilities (e.g., manage, develop, implement, lead) to showcase your abilities effectively.

                3. Prioritization and Relevance:

                    * **Frequency and Emphasis:** Pay close attention to keywords mentioned multiple times or with particular emphasis in the job description.
                    * **Required vs. Preferred Qualifications:** Differentiate between essential requirements and preferred or "nice-to-have" skills.
                    * **Alignment with Your Background:** Focus on extracting keywords that align with your skills and experience, ensuring you can genuinely demonstrate those qualities.

                4. Keyword List Creation: Create a structured list or table with the extracted keywords organized by category for easy reference.

                5. ATS Optimization Tips: 

                    * **Strategic Keyword Placement:**  Integrate keywords naturally throughout your resume, particularly in the skills section, experience descriptions, and summary/objective statement.
                    * **Keyword Density:** Use keywords thoughtfully and avoid excessive repetition or "keyword stuffing," which can be penalized by ATS algorithms.
                    * **Tailoring and Customization:** Adapt the extracted keywords and your resume content to each specific job application, highlighting the most relevant qualifications for each role.

                Outcome: A comprehensive list of relevant keywords and actionable tips to optimize your resume for both ATS algorithms and human reviewers, increasing your chances of landing an interview.
                """)

    # job_description_extractor = LLMTask("Job desc keyword extraction", jd_file_path, jd_extracted_keywords_file_path, jd_extraction_system_instruction, override=True)
    # job_description_extractor.run()

    # this will not run if the file is already indexed
    RagSearchTool.process_and_index(user_info_orgainzed_file_path)

    # Now, lets call the main crew to build the resume
    ResumeCrew().crew().kickoff()
    
    # inputs = {
    #     'user_info_orgainzed_file_path': user_info_orgainzed_file_path
    # }
    # UserInfoOrganizerCrew().crew().kickoff(inputs=inputs)


    
