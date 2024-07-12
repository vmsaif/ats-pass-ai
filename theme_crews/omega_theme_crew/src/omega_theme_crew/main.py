
from util.timer import Timer, print_task_time

import traceback
from omega_theme_crew.omega_theme_crew import OmegaThemeCrew
from omega_theme_crew.latex_generator import compile_latex
# from path.output_file_paths import PATHS
from omega_theme_crew.omega_file_paths import OMEGA_PATHS 

def run():
    try:
        omega_theme_crew = OmegaThemeCrew().crew()
        omega_theme_crew.kickoff()
    except Exception as e:
        traceback.print_exc()

    compile_latex(tex_path = OMEGA_PATHS["omega_theme_final_output_tex"], sub_tex_files_dir = OMEGA_PATHS['sub_tex_files_dir'], output_dir = OMEGA_PATHS["omega_theme_final_output_pdf"])


