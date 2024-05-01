# 

from ats_pass_ai.tools.data_extractor_tool import DataExtractorTool
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
                            Objective: You are being provided with content that is currently unorganized. Your task is to analyze, understand, and reorganize this content into a structured, human-readable format.
                            Instructions:
                            1. Comprehension: Carefully read and interpret the content to grasp the themes, details, and nuances.
                            2. Structure Development:
                            - Main Categories: Identify key themes and create main categories. Use #
                            - Subcategories: Within each main category, establish subcategories as necessary to further organize the details. Use ##
                            3. Content Handling:
                            - Preservation: Ensure that no details or pieces of information are omitted from the original content like links, dates, names, etc.
                            - Clarity and Readability: Enhance the readability of the content by using clear headings, subheadings, and bullet points.
                            4. Personal Content Handling:
                            - If any part of the content includes personal narratives or self-descriptions, do not categorize this information. Instead, summarize this portion to capture the essence of the individual’s message or story. Provide a third-person perspective.
                            5. Final Review: After organizing, review the structured content to ensure completeness, accuracy, and coherence.
                            Outcome: The end product should be a well-organized document that maintains all original details in a clear and accessible manner.
                            """)

            result = tool._run(file_path=self.user_info_file_path, action=action, temperature=0.7, top_k=80, top_p=0.95)

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
