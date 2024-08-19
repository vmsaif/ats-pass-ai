"""

    Author: Saif Mahmud
    Date: June 2024
    Project: ATS Pass AI

    Description:
    This module contains the functions to compile the latex file to generate the PDF. The function compile_latex() compiles the latex file to generate the PDF. The function sanitize_directory() sanitizes all the .tex files in the given directory by removing the lines that start with quotes. The function sanitize_file() sanitizes the .tex file by removing the lines that start with quotes.

"""

import subprocess
import os
def compile_latex(tex_path, sub_tex_files_dir, output_dir):

    """
    Compile the latex file to generate the PDF.

    Args:
        tex_path (str): The path to the main .tex file.
        sub_tex_files_dir (str): The path to the directory containing the .tex files that are included in the main .tex file.
        output_dir (str): The path to the directory where the output PDF will be saved.

    Returns:
        None
    """
    
    sanitize_directory(sub_tex_files_dir)

    print(f"Current working directory: {os.getcwd()}")
    filename = os.path.basename(tex_path)
    print(f"Compiling {filename}...")
    class_dir = os.path.dirname(tex_path)
    print(f"Class path: {class_dir}")

    try:
        command = [
            'xelatex',
            '-interaction=nonstopmode',  
            '-output-directory', f"{output_dir}",
            filename]
                
        # print cwd
        result = subprocess.run(command, cwd = class_dir, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)        
        # Print outputs regardless of success
        
        # print("Standard Output:" + result.stdout)
        
        if result.returncode == 0:
            print("\n\n------PDF generated successfully!-----\n\n")
        else:
            print("PDF generation had issues:")
            print("Error Output:")
            print(result.stderr)
    except subprocess.CalledProcessError as e:
        # Catch any non-zero exit status errors from xelatex
        print("Failed to compile PDF:")
        print("Standard Error:")
        print(e.stderr if e.stderr else "No error message available.")
        print("Standard Output:")
        print(e.output if e.output else "No output available.")

def sanitize_directory(directory):

    """

    Sanitize all the .tex files in the given directory. This function removes the lines that start with quotes.

    Args:

        directory (str): The path to the directory containing the .tex files to sanitize.

    Returns:

        None

    """

    for file in os.listdir(directory):
        if file.endswith(".tex"):
            sanitize_file(os.path.join(directory, file))
        else:
            print(f"Skipping {file} as it is not a .tex file. Not sanitizing it.")

def sanitize_file(tex_path):

    """

    Sanitize the .tex file by removing the lines that start with quotes.

    Args:

        tex_path (str): The path to the .tex file to sanitize.

    Returns:

        str: The path to the sanitized .tex file.

    """
    # remove the lines that starts with quotes
    try:
        with open(tex_path, "r") as file:
            lines = file.readlines()
            with open(tex_path, "w") as file:
                for line in lines:
                    if not line.startswith("`") and not line.startswith("*"):
                        file.write(line)
    except IOError as e:
        print(e)
    return tex_path

