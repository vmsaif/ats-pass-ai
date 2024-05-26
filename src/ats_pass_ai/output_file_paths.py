# Base directory variables
info_files = 'info_files'
info_extraction = 'info_extraction'
pre_tasks = f'{info_extraction}/pre_tasks'
jd_keyword_extraction = f'{info_extraction}/jd_keyword_extraction'
draft_output = f'{info_extraction}/draft_output'

# Config dictionary with all paths
PATHS = {
    "user_info_organized": f"{info_files}/user_info_organized.txt",
    "info_extraction_folder_path": info_extraction,
    "pre_tasks_folder_path": pre_tasks,
    "jd_keyword_extraction": f"{jd_keyword_extraction}/job_description_extracted_keywords.txt",
    "personal_information_extraction_task": f"{pre_tasks}/personal_information_extraction_task.txt",
    "education_extraction_task": f"{info_extraction}/education_extraction_task.txt",
    "volunteer_work_extraction_task": f"{info_extraction}/volunteer_work_extraction_task.txt",
    "awards_recognitions_extraction_task": f"{info_extraction}/awards_recognitions_extraction_task.txt",
    "references_extraction_task": f"{info_extraction}/references_extraction_task.txt",
    "personal_traits_interests_extraction_task": f"{info_extraction}/personal_traits_interests_extraction_task.txt",
    "profile_builder_task": f"{info_extraction}/profile_builder_task.txt",
    "work_experience_extraction_task": f"{pre_tasks}/work_experience_extraction_task.txt",
    "project_experience_extraction_task": f"{pre_tasks}/project_experience_extraction_task.txt",
    "skills_from_exp_and_project": f"{pre_tasks}/skills_from_exp_and_project.txt",
    "skills_extraction_task": f"{pre_tasks}/skills_extraction_task.txt",
    "coursework_extraction_task": f"{info_extraction}/coursework_extraction_task.txt",
    "ats_friendly_skills_task": f"{pre_tasks}/ats_friendly_skills_task.txt",
    "find_comparable_items_from_missing_skills": f"{pre_tasks}/find_comparable_items_from_missing_skills.txt",
    "reduce_missing_skills_task": f"{pre_tasks}/reduce_missing_skills_task.txt",
    "split_context_of_ats_friendly_skills_task": f"{info_extraction}/split_context_of_ats_friendly_skills_task.txt",
    "experience_choosing_task": f"{pre_tasks}/experience_choosing_task.txt",
    "split_context_of_experience_choosing_task": f"{pre_tasks}/split_context_of_experience_choosing_task.txt",
    "gather_info_of_chosen_experiences": f"{pre_tasks}/gather_info_of_chosen_experiences.txt",
    "ats_friendly_keywords_into_experiences": f"{pre_tasks}/ats_friendly_keywords_into_experiences.txt",
    "split_context_of_ats_friendly_keywords_into_experiences": f"{info_extraction}/split_context_of_ats_friendly_keywords_into_experiences.txt",
    "career_objective_task": f"{info_extraction}/career_objective_task.txt",
    "resume_in_json_task": f"{draft_output}/resume_in_json_task.txt",
    "resume_compilation_task": f"{draft_output}/resume_compilation_task.txt"
}
