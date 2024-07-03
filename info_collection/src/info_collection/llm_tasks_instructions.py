
from textwrap import dedent

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
                                          
    There should be a paragraph for company culture and values, what the company is looking for in a candidate, and what the candidate can expect from the company. This will help in creating a better resume for the candidate. Keep the keywords and phrases same as in the job description.
    """)

company_value_extraction_system_instruction = dedent("""
company_value_extraction_task:
  description: >
    Extract key information from a provided job description that highlights the company's mission, values, and goals. This information will be used to align the applicant's career objective with the company's culture and expectations.

    **Procedure**:
    - **Introduction**: Mention the company name and job title.
    - **Identify Keywords and Phrases**: Scan the job description for explicit mentions of the company's mission, core values, strategic goals, and cultural elements.
    - **Contextual Relevance**: Ensure that the extracted keywords and phrases are directly related to what the company emphasizes as its priorities and ideals.
    - **Summarization**: Summarize the extracted information into concise phrases that can be seamlessly integrated into the applicant's career objective to demonstrate alignment with the company.

    **Expected Output**:
    - A list of key phrases and sentences extracted from the job description that clearly reflect the company's values and goals. These should be presented in a way that they can be directly used or slightly modified for inclusion in the career objective section of a resume.
                                                     
    This task will help ensure that the applicant's career objectives are not only aligned with the company's current objectives but also resonate with the company's broader vision and cultural ethos.

  expected_output: >
    In JSON format, 
      {
        "Company Values and Goals": [
          "Company Mission: []",
          "Core Values: []",
          "Strategic Goals: []",
          "Cultural Elements: []",
          "Company Vision: []",
          "Company Culture: []",
          ...etc
        ]
      }
    """)