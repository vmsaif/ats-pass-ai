# from util.limiter import printRemainingRequestsPerDay
import subprocess
import os
from shared.src.path.output_file_paths import PATHS
from theme_crews.omega_theme_crew.src.omega_theme_crew.omega_file_paths import OMEGA_PATHS

def main():
    # Define the paths to the projects relative to this script

    job_description_link = "\"https://boards.greenhouse.io/robinhood/jobs/6022269?gh_src=NaN&gh_jid=6022269\""

    info_collection = "info_collection"
    resume_crew = "resume_crew"
    omega_theme_crew = "omega_theme_crew"

    current_directory = os.path.dirname(os.path.abspath(__file__))
    project_a_path = os.path.join(current_directory, info_collection)
    project_b_path = os.path.join(current_directory, resume_crew)
    project_c_path = os.path.join(current_directory, 'theme_crews', omega_theme_crew)

    startFresh(
        run = True,
        delete_latex_files = True, 
        deleteDB = False, 
        # delete_llm_task_output_dir = True, 
        delete_info_files = False
    )
    
    # Define the command to run in each project
    # run_poetry_project(project_a_path, info_collection, job_description_link)
    run_poetry_project(project_b_path, resume_crew)
    run_poetry_project(project_c_path, omega_theme_crew)

    # Run commands in both projects
    # printRemainingRequestsPerDay()



def delete_files_recursively_from_directory(directory_path):
    """Delete all files in the given directory recursively."""
    if not os.path.exists(directory_path):
        print(f"Directory does not exist: {directory_path}")
        return

    for root, dirs, files in os.walk(directory_path, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
            except OSError as e:
                print(f"Error deleting file {file_path}: {e}")

def run_poetry_project(project_path, command, *args):
    # Change the directory to the project's directory
    os.chdir(project_path)
    
    # Run the poetry command (e.g., `poetry run script_name`)

    full_command = f"poetry run {command} {' '.join(args)}" if args else f"poetry run {command}"
    print (f"Running command in {project_path}")
    
    process = subprocess.run(full_command, shell=True)
    
    # Check if the command was executed successfully
    if process.returncode == 0:
        print(f"Successfully ran command in {project_path}")
    else:
        print(f"Failed to run command in {project_path} with return code {process.returncode}")

def startFresh(
        run: bool = False,
        delete_latex_files: bool = False, 
        deleteDB: bool = False, 
        delete_llm_task_output_dir: bool = False, 
        delete_info_files: bool = False):
    
    if(run):
        # delete all files recursively from a given directory
        """Delete the applicant profile files but not the folder, optionally delete pre-task files."""

        to_be_deleted = []
        to_be_deleted.append(PATHS["info_extraction_folder_path"])
        
        if delete_latex_files:
            to_be_deleted.append(OMEGA_PATHS["sub_tex_files_dir"])
            to_be_deleted.append(OMEGA_PATHS["omega_theme_pre_tasks_dir"])
            to_be_deleted.append(OMEGA_PATHS["omega_theme_final_output_pdf"])

        if deleteDB:
            to_be_deleted.append('resume_crew/chroma_db')

        if delete_info_files:
            to_be_deleted.append(PATHS["info_files_dir"])

        if delete_llm_task_output_dir:
            to_be_deleted.append(PATHS["llm_task_output_dir"])
        
        for directory_path in to_be_deleted:
            delete_files_recursively_from_directory(directory_path)

if __name__ == "__main__":
    main()
    