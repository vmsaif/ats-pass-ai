src_root = 'src/ats_pass_ai'
themes_crew_dir = f'{src_root}/themes_crew'

# Omega theme paths
omega_theme_dir = f"{themes_crew_dir}/omega_theme"
omega_theme_latex_dir = f"{themes_crew_dir}/omega_theme/theme_latex"
sub_tex_files_dir = f"{omega_theme_latex_dir}/sub_tex_files_dir" # if needs to  change this, also change in the actual tex file. 
omega_theme_pre_tasks_dir = f"{omega_theme_latex_dir}/text_outputs"

OMEGA_PATHS = {
# Omega theme paths

    "omega_theme_final_output_tex": f"{omega_theme_latex_dir}/omega_theme_final_output.tex",
    
    "omega_theme_final_output_pdf": f"../../../../../{omega_theme_latex_dir}", # need to go back to project root from class path
    "omega_theme_agents": f"{themes_crew_dir}/omega_theme/config/omega_theme_agents.yaml",
    "omega_theme_tasks": f"{themes_crew_dir}/omega_theme/config/omega_theme_tasks.yaml",

    "concise_jd_task": f"{omega_theme_pre_tasks_dir}/concise_jd_task.txt",
    "assess_and_prioritize": f"{omega_theme_pre_tasks_dir}/assess_and_prioritize.txt",
    "select_first_column_content": f"{omega_theme_pre_tasks_dir}/select_first_column_content.txt",


    "sub_tex_files_dir": sub_tex_files_dir,
    
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
    "experience_section": f"{omega_theme_pre_tasks_dir}/experience_section.txt",
    "exp_latex_verified": f"{sub_tex_files_dir}/exp_latex_verified.tex",
}