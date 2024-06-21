# Base directory variables
info_files_dir = 'info_files'
info_extraction_dir = 'info_extraction'
pre_tasks_dir = f'{info_extraction_dir}/pre_tasks'
jd_keyword_extraction = f'{info_extraction_dir}/jd_keyword_extraction'
draft_output_dir = f'{info_extraction_dir}/draft_output'
llm_task_output_dir = f'{info_files_dir}/llm_task_output'
src_root = 'src/ats_pass_ai'
themes_crew_dir = f'{src_root}/themes_crew'
limiter_db_dir = 'custom_db'
rag_db_perist_dir = "./chroma_db"

# Omega theme paths
omega_theme_dir = f"{themes_crew_dir}/omega_theme"
omega_theme_latex_dir = f"{themes_crew_dir}/omega_theme/theme_latex"
sub_tex_files_dir = f"{omega_theme_latex_dir}/sub_tex_files_dir" # if needs to change this, also change in the actual tex file. 

# Config dictionary with all paths

PATHS = {
    "applicant_info_file_path": f"{info_files_dir}/applicant_info.txt",
    "applicant_info_organized": f"{llm_task_output_dir}/applicant_info_organized.txt",
    "jd_file_path": f"{info_files_dir}/job_description.txt",
    "jd_keyword_extraction": f"{llm_task_output_dir}/job_description_extracted_keywords.txt",

    "limiter_db_dir": limiter_db_dir,
    "limiter_db_file": f"{limiter_db_dir}/request_limiter.db",
    
    "src_root": src_root,
    "info_files_dir": info_files_dir,
    "info_extraction_dir": info_extraction_dir,
    "pre_tasks_dir": pre_tasks_dir,
    "draft_output_dir": draft_output_dir,
    "llm_task_output_dir": llm_task_output_dir,

    "rag_db_perist_dir": rag_db_perist_dir,
    "hash_file_path": f"{rag_db_perist_dir}/hash_store.txt",
    
    "info_extraction_folder_path": info_extraction_dir,
    "pre_tasks_folder_path": pre_tasks_dir,
    
    "personal_information_extraction_task": f"{pre_tasks_dir}/personal_information_extraction_task.txt",
    "education_extraction_task": f"{info_extraction_dir}/education_extraction_task.txt",
    "volunteer_work_extraction_task": f"{info_extraction_dir}/volunteer_work_extraction_task.txt",
    "awards_recognitions_extraction_task": f"{info_extraction_dir}/awards_recognitions_extraction_task.txt",
    "references_extraction_task": f"{info_extraction_dir}/references_extraction_task.txt",
    "personal_traits_interests_extraction_task": f"{info_extraction_dir}/personal_traits_interests_extraction_task.txt",
    "profile_builder_task": f"{info_extraction_dir}/profile_builder_task.txt",
    "work_experience_extraction_task": f"{pre_tasks_dir}/work_experience_extraction_task.txt",
    "project_experience_extraction_task": f"{pre_tasks_dir}/project_experience_extraction_task.txt",
    "skills_from_exp_and_project": f"{pre_tasks_dir}/skills_from_exp_and_project.txt",
    "skills_extraction_task": f"{pre_tasks_dir}/skills_extraction_task.txt",
    "coursework_extraction_task": f"{info_extraction_dir}/coursework_extraction_task.txt",
    "ats_friendly_skills_task": f"{pre_tasks_dir}/ats_friendly_skills_task.txt",
    "find_comparable_items_from_missing_skills": f"{pre_tasks_dir}/find_comparable_items_from_missing_skills.txt",
    "reduce_missing_skills_task": f"{pre_tasks_dir}/reduce_missing_skills_task.txt",
    "split_context_of_ats_friendly_skills_task": f"{info_extraction_dir}/split_context_of_ats_friendly_skills_task.txt",
    "experience_choosing_task": f"{pre_tasks_dir}/experience_choosing_task.txt",
    "split_context_of_experience_choosing_task": f"{pre_tasks_dir}/split_context_of_experience_choosing_task.txt",
    "gather_info_of_chosen_experiences": f"{pre_tasks_dir}/gather_info_of_chosen_experiences.txt",
    "ats_friendly_keywords_into_experiences": f"{pre_tasks_dir}/ats_friendly_keywords_into_experiences.txt",
    "split_context_of_ats_friendly_keywords_into_experiences": f"{info_extraction_dir}/split_context_of_ats_friendly_keywords_into_experiences.txt",
    "career_objective_task": f"{info_extraction_dir}/career_objective_task.txt",
    "resume_in_json_task": f"{draft_output_dir}/resume_in_json_task.txt",
    "resume_compilation_task": f"{draft_output_dir}/resume_compilation_task.txt",
    "latex_resume_generation_task": f"{src_root}/latex_class/resume_generation_task.tex", 
    "cover_letter_generation_task": f"{draft_output_dir}/cover_letter_generation_task.txt",

    # Omega theme paths

    "omega_theme_final_output_tex": f"{omega_theme_latex_dir}/omega_theme_final_output.tex",
    
    "omega_theme_final_output_pdf": f"../../../../../{omega_theme_latex_dir}", # need to go back to project root from class path
    "omega_theme_agents": f"{themes_crew_dir}/omega_theme/config/omega_theme_agents.yaml",
    "omega_theme_tasks": f"{themes_crew_dir}/omega_theme/config/omega_theme_tasks.yaml",
    "concise_jd_task": f"{omega_theme_latex_dir}/text_outputs/concise_jd_task.txt",
    "sub_tex_files_dir": sub_tex_files_dir,
    "namesection": f"{sub_tex_files_dir}/namesection.tex",
    "educationsection": f"{sub_tex_files_dir}/educationsection.tex",
    "skillsection": f"{sub_tex_files_dir}/skillsection.tex",
    "courseworksection": f"{sub_tex_files_dir}/courseworksection.tex",
    "volunteersection": f"{sub_tex_files_dir}/volunteersection.tex",
    "referencessection": f"{sub_tex_files_dir}/referencessection.tex",
    "careerobjectivesection": f"{sub_tex_files_dir}/careerobjectivesection.tex",
    "experiencesection": f"{sub_tex_files_dir}/experiencesection.tex",
    "select_first_column_content": f"{omega_theme_latex_dir}/text_outputs/select_first_column_content.txt",
    "split_content_of_select_first_column_content": f"{omega_theme_latex_dir}/text_outputs/split_content_of_select_first_column_content.txt",
    
}
