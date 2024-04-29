from ats_pass_ai.tools.data_extractor_tool import DataExtractorTool
from textwrap import dedent

class OrganizeUserInfo:

    def __init__(self, user_info_file_path: str, user_info_orgainzed_file_path: str):
        self.user_info_file_path = user_info_file_path
        self.user_info_orgainzed_file_path = user_info_orgainzed_file_path

    def run(self):
        print("Starting to organize user information...")
        tool = DataExtractorTool()
        action = dedent("""
                        You are responsible for ensuring that the output of the content below is a complete and well-structured and organized extraction of the content. Your output should clearly present the information in an organized, structured, and categorized format, integrating all segments cohesively. You must ensure the inclusion of all essential sections and details.
                        
                        * A detailed introduction of the user (if not available, check again, if still not available, ignore it): 
                        
                            User's Profile:
                            Name:
                            Phone Number:
                            Email:
                            LinkedIn Profile:
                            other social media profiles links:
                            Personal website link:
                            Portfolio Link:
                            GitHub Profile:
                            Address:
                            City:
                            State:
                            Zip Code:
                            Country:
                            and more...
                        

                        * Complete and detailed descriptions and dates for all projects, experiences, including links and technologies used. Do not make it concise. Make it detailed.
                        
                        Include all other information provided in the content.
                        Important:
                        * Do not create links yourself. If the content does not have any links, do not create them.
                        * Do not remove any information or links from the document. keep it detailed and organized.                    
                        """)
        result = tool._run(file_path=self.user_info_file_path, action=action, temperature=0.8, top_k=20, top_p=0.9)

        self.write_to_file(result)
        # export the result to a file
        
    def write_to_file(self, content):
        try:
            open(self.user_info_orgainzed_file_path, 'w').close()
            with open(self.user_info_orgainzed_file_path, 'w') as f:
                f.write(content)
            print(f"User information organized and saved to: {self.user_info_orgainzed_file_path}")
        except Exception as e:
            print(f"Error while creating the file: {e}")
