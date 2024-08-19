import os
import subprocess
import argparse

def execute_poetry_command(base_path, command):
    """
    Recursively search for 'pyproject.toml' files starting from the base_path,
    and execute a specified poetry command in directories where 'pyproject.toml' is found.
    """
    poetry_toml_file_name = 'pyproject.toml'

    # Recursively search for 'pyproject.toml' files starting from the base_path up to a depth of 2
    base_depth = base_path.count(os.sep)  # Count the number of separators in the base path
    for root, dirs, files in os.walk(base_path):
        current_depth = root.count(os.sep) - base_depth
        # Stop walking deeper if the depth is greater than 2
        if current_depth > 2:
            del dirs[:]  # Clear the list of directories to prevent walking deeper
            continue

        if poetry_toml_file_name in files:
            print(f"{poetry_toml_file_name} found in: {root}")
            # Change directory to where 'pyproject.toml' is found
            os.chdir(root)
            # Execute the specified poetry command
            print(f"Executing 'poetry {command}' in {root}")
            try:
                process = subprocess.run(f"poetry {command}", shell=True, text=True, check=True)
                print(f"Poetry command '{command}' completed successfully in {root}")
            except subprocess.CalledProcessError as e:
                print(f"Poetry command '{command}' failed in {root} with return code {e.returncode}")
                print(f"Error message: {e.output}")

def main():
    print("Starting the script to execute Poetry commands on projects with a 'pyproject.toml' file...")
    parser = argparse.ArgumentParser(description="Execute arbitrary Poetry commands on projects with a pyproject.toml.")
    parser.add_argument('command', type=str,
                        help='The full Poetry command to execute (e.g., "install", "update --no-dev", "cache clear pypi --all"). Enter the command within quotes to avoid parsing errors.')
    args = parser.parse_args()

    # Use the directory of this script as the base directory
    base_directory = os.path.dirname(os.path.abspath(__file__))
    print(f"Starting to search for 'pyproject.toml' from base directory: {base_directory}")
    execute_poetry_command(base_directory, args.command)

if __name__ == "__main__":
    print("Running the main function...")
    main()
