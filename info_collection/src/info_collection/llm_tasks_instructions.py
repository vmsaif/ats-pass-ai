"""
    Author: Saif Mahmud
    Date: March 2024
    Project: ATS Pass AI
    Version: 1.0

    Description:

    This script contains the instructions for the three tasks in the ATS Pass AI pipeline:
    
    1. Organize System: Reorganizes unstructured content into a clear, structured format.
    2. Job Description Fetch System: Extracts job description from a web page.
    3. JD Extraction System: Extracts keywords and phrases from a job description for resume optimization.

"""

from textwrap import dedent

organize_system_instruction = dedent("""
    Task: Content Organization and Structuring
    Objective: Reorganize provided unstructured content into a clear, structured format without missing any details. Every detail in the content is important and should be included in the final output.
    
    Instructions:
    1. Comprehension: Read the content to understand the themes and details. Each section should have a description of more than 2-3 lines on what it contains as it will help doing symanctic search on this document later.
                                
    2. Identification:
        - Begin with identifying and documenting key personal identification details such as the applicant's name, contact information, location, phone number, and email address etc.
        - Use the heading '# Personal Details' for this section.
        - Write in a structured format, such as:
            Name: [Applicant's Name]
            Location: [City, State]
            Phone: [Phone Number]... etc.
                                     
    3. Structure Development: 
        - Write a description of each Category of more than 2-3 lines of what it contains. For example, if you have a section called "References", write, "This section contains the personnel who can provide references, testimonials or recommendations for the Aplicant."
                                
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

job_description_fetch_system_instruction = dedent("""
    You are given an extracted texts of a job description from a web page.
                                
    Give me everything as is. 
                                
    Expertec Output:
    - Full context in the exactly provided words without any changes.
    - Start the output with:
        Job Role: 
        Company Name:
        Location: (if available)
        Rest of the content as is.
                                
    - Remove any unnecessary white spaces or blank lines. 
                          
    Here is the extracted texts of the job description web page:
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
                                          
    Keep the keywords and phrases same as in the job description.
    """)

company_value_extraction_system_instruction = dedent("""
You are provided a job description for a position at a company. Your task is to extract the company's values and culture from the job description. This information will be used to create a compelling career objective or summary for the applicant's resume.
                                                     
Instructions:
1. Read the job description carefully to identify any mentions of the company's values, mission, culture, or work environment.
2. Extract keywords and phrases related to the company's values and culture.
3. Summarize the company's values and culture in a concise paragraph.
4. Ensure that the extracted information accurately reflects the company's ethos and culture. Use direct quotes or paraphrasing from the job description where necessary.
                                                     
Outcome:
A well-crafted paragraph that captures the essence of the company's values and culture, based on the information provided in the job description.
                                                     
In JSON format, the output should look like this:
{
    "company_name": "Company Name",
    "Job_title": "Job Title",
    "Information needed to create a compelling career objective or summary": [
      "Paragraph 1",
      "Paragraph 2",
      "Paragraph 3", ...so on
    ],
    "Phases used in the job description that reflect the company's values and culture": [ "Phase 1", "Phase 2", "Phase 3", ...so on ]
}
""")