# 

from ats_pass_ai.tools.langchain_tool_template_data_extractor_tool_old import DataExtractorTool
from textwrap import dedent

class OrganizeUserInfo:

    def __init__(self, user_info_file_path: str, user_info_orgainzed_file_path: str):
        self.user_info_file_path = user_info_file_path
        self.user_info_orgainzed_file_path = user_info_orgainzed_file_path

    def run(self):

        # if user_info_orgainzed_file_path does not exist then proceed
        try:
            with open(self.user_info_orgainzed_file_path, 'r') as f:
                content = f.read()
            if len(content) < 50:
                print(f"User information file found but it is most likely empty.")
                raise FileNotFoundError
            print(f"User information organized file found. \nAssuming it is already organized in the {self.user_info_orgainzed_file_path}")
            return
        except FileNotFoundError as e:
            print("Starting to organize user information...")
            tool = DataExtractorTool()
            action = dedent("""
                            Task: Content Organization and Structuring
                            Objective: Reorganize provided unstructured content into a clear, structured format
                            Instructions:
                            1. Comprehension: Read the content to understand the themes and details.
                            2. Structure Development:
                               - Main Categories: Identify and label key themes with '#'.
                               - Subcategories: Create necessary subcategories under each main category with '##'.
                            3. Content Handling:
                               - Preservation: Ensure all original information (links, dates, names) is included.
                               - Clarity and Readability: Use clear headings, subheadings, and bullet points to enhance readability.
                            4. Personal Content Handling:
                               - Summarize personal narratives or self-descriptions in third-person, without categorization.
                            5. Final Review: Check the structured content for completeness, accuracy, and coherence.
                            Outcome: Deliver a well-organized document that maintains all original details in an accessible format.
                            """)

            result = tool._run(file_path=self.user_info_file_path, action=action, temperature=0.7, top_k=50, top_p=0.95)

            self.write_to_file(result)
            # export the result to a file
            return

    def write_to_file(self, content):
        try:
            open(self.user_info_orgainzed_file_path, 'w').close()
            with open(self.user_info_orgainzed_file_path, 'w') as f:
                f.write(content)
            print(f"User information organized and saved to: {self.user_info_orgainzed_file_path}")
        except Exception as e:
            print(f"Error while creating the file: {e}")
