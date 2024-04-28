from ats_pass_ai.tools.text_reader_tool import TextFileReaderTool
from textwrap import dedent

class OrganizeUserInfo:

    def __init__(self, user_info_file_path: str, user_info_orgainzed_file_path: str):
        self.user_info_file_path = user_info_file_path
        self.user_info_orgainzed_file_path = user_info_orgainzed_file_path

    def run(self):
        tool = TextFileReaderTool()
        action = dedent("""
                        You are responsible for ensuring that the output of the content below is a complete and well-structured and organized extraction of the content. Your output should clearly present the information in an organized, structured, and categorized format, integrating all segments cohesively. You must ensure the inclusion of all essential sections and details:
                        
                        * A detailed introduction of the user. For example, 
                        
                            User's Profile: \n
                            Name: \n
                            Phone Number: \n
                            Email: \n
                            LinkedIn Profile: \n
                            other social media profiles links: \n
                            Personal website link: \n
                            Portfolio Link: \n
                            GitHub Profile: \n
                            Address: \n
                            City: \n
                            State: \n
                            Zip Code: \n
                            Country: \n
                        and more...
                        

                        * Complete and detailed descriptions and dates for all projects, experiences, including links and technologies used. Do not make it concise. Make it detailed.
                        
                        Include all other information provided in the content.
                        Important:
                        * Do not create links yourself. If the content does not have any links, do not create them.
                        * Do not remove any information or links from the document. keep it detailed and organized.  

                        Before giving the output, ensure that If you are unable to find an information, please ignore it, do not mention it and do not say, "Not provided" or "Not available" or "N/A" etc, just simply ignore it.                    
                        """)
        result = tool._run(file_path=self.user_info_file_path, action=action)
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
