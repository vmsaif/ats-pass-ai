"""
	Author: Saif Mahmud
	Date: 04-23-2024
	Description: This file contains the main function to run the ATS-PASS-AI
"""
from ats_pass_ai.user_info_organizer_crew import UserInfoOrganizerCrew
from ats_pass_ai.tools.rag_search_tool import RagSearchTool
from ats_pass_ai.organize_user_info import OrganizeUserInfo


def run():

    # First, Lets Organize the User Information provided by the user.
    user_info_file_path = 'info_files/user_info.txt'
    user_info_orgainzed_file_path = 'info_files/user_info_organized.txt'

    # This will not run if there is already an organized file
    OrganizeUserInfo(user_info_file_path, user_info_orgainzed_file_path).run()

    # this will not run if the file is already indexed
    RagSearchTool.process_and_index(user_info_orgainzed_file_path)

    
    # Now, lets call the main crew to build the resume
    UserInfoOrganizerCrew().crew().kickoff()
    
    # inputs = {
    #     'user_info_orgainzed_file_path': user_info_orgainzed_file_path
    # }
    # UserInfoOrganizerCrew().crew().kickoff(inputs=inputs)
    
