"""
Author: 	Saif Mahmud
Date: 		August 2024
Project: 	ATS Pass AI

Description: 

This is the main script that runs the three projects in the ATS Pass AI pipeline.

1. Info Collection: Collects all the information of the applicant and then organizes it. properly in a file.

2. Resume Crew: Creates a database of the applicant's info from the collected information. Then it creates generates all the necessary information for the resume.

3. Omega Theme Crew: Generates the resume in a beautiful format.
"""


import subprocess
import os
import sys
from textwrap import dedent
import time
from shared.src.path.output_file_paths import PATHS
from theme_crews.omega_theme_crew.src.omega_theme_crew.omega_file_paths import OMEGA_PATHS

def main():

    """ 
    Run the three projects in the ATS Pass AI pipeline.

    Args:
    
    Returns:
        None    
    """   

    # Define the paths to the projects relative to this script

    job_description = os.path.abspath(PATHS["jd_text_file"])
    # job_description = "\"https://www.linkedin.com/jobs/view/3960243613/?refId=f8d73875-df88-4bf4-a047-dec407effa15&trackingId=dcGZfgYwQ1K1WkiSvtvZqA%3D%3D\""

    info_collection = "info_collection"
    resume_crew = "resume_crew"
    omega_theme_crew = "omega_theme_crew"

    current_directory = os.path.dirname(os.path.abspath(__file__))
    project_a_path = os.path.join(current_directory, info_collection)
    project_a_path = os.path.normpath(project_a_path)

    project_b_path = os.path.join(current_directory, resume_crew)
    project_b_path = os.path.normpath(project_b_path)

    project_c_path = os.path.join(current_directory, 'theme_crews', omega_theme_crew)
    project_c_path = os.path.normpath(project_c_path)
        
    startFresh (
        new_applicant = check_args(), # Delete the previous applicant profile files for new applicants
        delete_resume_profiles = False, # Delete the previous applicant profile files for new applicants
        delete_latex_files = False, # Delete the pre-task files for the Omega Theme Crew
        deleteDB = False, # Delete the database files 
        delete_llm_task_output_dir = False, # Delete the Applicant Info Organized files. (True for new applicants)
        delete_info_files = False
    )
    
    # Define the command to run in each project

    try:
        run_poetry_project(project_a_path, info_collection, job_description)
        time.sleep(10)
        run_poetry_project(project_b_path, resume_crew)
        time.sleep(10)
        run_poetry_project(project_c_path, omega_theme_crew)
    except Exception as e:
        print(f"Error running projects: {e}")
        
        exit(1)

def check_args() -> bool:
    """
    Check if the user has passed the "new" argument to the script.

    Args:
        None

    Returns:
        bool: True if the user has passed the "new" argument, False otherwise.
    """
    output = False
    # argsv length
    if len(sys.argv) > 1:
        if sys.argv[1] == "new":
            output = True
    return output

def delete_files_recursively_from_directory(directory_path):
    """
    Delete all files in the given directory recursively.
    
    Args:
        directory_path (str): The path to the directory to delete files from.

    Returns:
        None
    """
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

def delete_file_from_path(file_path):
    """
    Delete the file at the given path.

    Args:
        file_path (str): The path to the file to delete.

    Returns:
        None
    
    """

    if not os.path.exists(file_path):
        print(f"File does not exist: {file_path}")
        return

    try:
        os.remove(file_path)
        print(f"Deleted file: {file_path}")
    except OSError as e:
        print(f"Error deleting file {file_path}: {e}")

def run_poetry_project(project_path, command, *args):
    
    """
    Run a command in a poetry project. 

    Args:
        project_path (str): The path to the poetry project. Will chdir to this directory before running the command.
        command (str): The command to run.
        *args: Additional arguments to pass to the command.

    Returns:
        None

    """
    
    os.chdir(project_path)
    
    # Run the poetry command (e.g., `poetry run script_name`)

    full_command = f"poetry run {command} {' '.join(args)}" if args else f"poetry run {command}"
    print (f"Running command in {project_path}")
    print(full_command)
    
    process = subprocess.run(full_command, shell=True)
    
    # Check if the command was executed successfully
    if process.returncode == 0:
        print(f"Successfully ran command in {project_path}")
    else:
        print(f"Failed to run command in {project_path} with return code {process.returncode}")

def startFresh(
        new_applicant: bool = False,
        delete_resume_profiles: bool = False,
        delete_latex_files: bool = False, 
        deleteDB: bool = False, 
        delete_llm_task_output_dir: bool = False, 
        delete_info_files: bool = False):
    
        """
        Delete the applicant profile files but not the folder, optionally delete pre-task files.
        
        Args:
            delete_resume_profiles (bool): Delete the applicant profile files.
            delete_latex_files (bool): Delete the pre-task files for the Omega Theme Crew.
            deleteDB (bool): Delete the database files.
            delete_llm_task_output_dir (bool): Delete the LLM task output directory.
            delete_info_files (bool): Delete the info files directory. Usually this will never be used.

        Returns:
            None

        """

        to_be_deleted = []

        if(new_applicant):
            delete_resume_profiles = True
            delete_latex_files = True
            deleteDB = True
            delete_llm_task_output_dir = True
            

        if(delete_resume_profiles):
            to_be_deleted.append(PATHS["info_extraction_folder_path"])
        
        if delete_latex_files:
            to_be_deleted.append(f'theme_crews\omega_theme_crew\{OMEGA_PATHS["sub_tex_files_dir"]}')
            to_be_deleted.append(f'theme_crews\omega_theme_crew\{OMEGA_PATHS["omega_theme_pre_tasks_dir"]}')

        if deleteDB:
            to_be_deleted.append('resume_crew/chroma_db')

        if delete_info_files:
            to_be_deleted.append(PATHS["info_files_dir"])

        if delete_llm_task_output_dir:
            print("Deleting LLM task output directory")
            delete_file_from_path(PATHS["jd_file_path"])
            to_be_deleted.append(PATHS["llm_task_output_dir"])
        
        if len(to_be_deleted) > 0:
            for directory_path in to_be_deleted:
                delete_files_recursively_from_directory(directory_path)

def sum()
    

if __name__ == "__main__":  
    main()
    