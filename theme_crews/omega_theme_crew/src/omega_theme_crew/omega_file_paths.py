from pathlib import Path

omega_theme_crew_src_dir = f'src/omega_theme_crew'

# Omega theme paths
omega_theme_latex_dir = f"{omega_theme_crew_src_dir}/theme_latex"
sub_tex_files_dir = f"{omega_theme_latex_dir}/sub_tex_files_dir" # if needs to  change this, also change in the actual tex file. 
omega_theme_pre_tasks_dir = f"{omega_theme_latex_dir}/pre_tasks"

current_dir = Path.cwd()


OMEGA_PATHS = {
# Omega theme paths

    "omega_theme_final_output_tex": f"{omega_theme_latex_dir}/omega_theme_final_output.tex",
    
    "omega_theme_final_output_pdf": '../../../../../output/', # to the mother project directory, relative to the class_path of latex class path
    "omega_theme_agents": f"{omega_theme_crew_src_dir}/config/omega_theme_agents.yaml",
    "omega_theme_tasks": f"{omega_theme_crew_src_dir}/config/omega_theme_tasks.yaml",

    "concise_jd_task": f"{omega_theme_pre_tasks_dir}/concise_jd_task.txt",

    "remove_data": f"{omega_theme_pre_tasks_dir}/remove_data.txt",
    "data_extraction": f"{omega_theme_pre_tasks_dir}/data_extraction.txt",
    "relevance_assessment": f"{omega_theme_pre_tasks_dir}/relevance_assessment.txt",
    "prioritization_logic": f"{omega_theme_pre_tasks_dir}/prioritization_logic.txt",
    "final_selection": f"{omega_theme_pre_tasks_dir}/final_selection.txt",


    "sub_tex_files_dir": sub_tex_files_dir,
    "omega_theme_pre_tasks_dir" : omega_theme_pre_tasks_dir,
    
    "name_section": f"{sub_tex_files_dir}/name_section.tex",
    "education_section": f"{sub_tex_files_dir}/education_section.tex",
    "skill_section": f"{sub_tex_files_dir}/skill_section.tex",
    "coursework_section": f"{sub_tex_files_dir}/coursework_section.tex",
    "volunteer_section": f"{sub_tex_files_dir}/volunteer_section.tex",
    "references_section": f"{sub_tex_files_dir}/references_section.tex",
    "career_objective_section": f"{sub_tex_files_dir}/career_objective_section.tex",
    
    "exp_item_count_chooser": f"{omega_theme_pre_tasks_dir}/exp_item_count_chooser.txt",
    "exp_item_chooser": f"{omega_theme_pre_tasks_dir}/exp_item_chooser.txt",
    "summary_point_selector": f"{omega_theme_pre_tasks_dir}/summary_point_selector.txt",
    "link_handler": f"{omega_theme_pre_tasks_dir}/link_handler.txt",
    "link_latex": f"{omega_theme_pre_tasks_dir}/link_latex.txt",

    "experience_content_refinement": f"{omega_theme_pre_tasks_dir}/experience_content_refinement.txt",
    "experience_section": f"{sub_tex_files_dir}/experience_section.tex",
    "exp_latex_verified": f"{sub_tex_files_dir}/exp_latex_verified.tex",
}