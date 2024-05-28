import subprocess
import os
def compile_latex(tex_path, output_dir):
    
    sanitized_file(tex_path)
    # get the filename from the tex_path
    filename = os.path.basename(tex_path)
    # print(f"Compiling LaTeX file: {filename}")
    # print(f"Output directory: {output_dir}")
    class_path = os.path.dirname(tex_path)
    # print(f"Class path: {class_path}")
    # get the current working directory from tex_path
    # cwd = os.getcwd()
    # list all in the current working directory 

    try:
        command = [
            'xelatex', 
            '-interaction=nonstopmode', 
            '-output-directory', f"../../../{output_dir}", 
            filename]
        # print cwd
        result = subprocess.run(command, cwd = class_path, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)        
        # Print outputs regardless of success
        # print("Standard Output:")
        # print(result.stdout)
        
        if result.returncode == 0:
            print("PDF generated successfully!")
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

def sanitized_file(tex_path):
    # remove the lines that starts with quotes
    try:
        with open(tex_path, "r") as file:
            lines = file.readlines()
            with open(tex_path, "w") as file:
                for line in lines:
                    if not line.startswith("`"):
                        file.write(line)
    except IOError as e:
        print(e)
    return tex_path

