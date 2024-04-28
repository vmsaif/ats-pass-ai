#!/usr/bin/env python
from ats_pass_ai.user_info_organizer_crew import UserInfoOrganizerCrew
from ats_pass_ai.organize_user_info import OrganizeUserInfo


def run():

    # First, Lets Organize the User Information provided by the user.
    user_info_file_path = 'info_files/user_info.txt'
    user_info_orgainzed_file_path = 'info_files/user_info_organized.txt'

    # Organize the user information

    # try:
    #     organize = OrganizeUserInfo(user_info_file_path, user_info_orgainzed_file_path)
    #     organize.run()
    #     # it should print: User information organized and saved to: user_info_orgainzed_file_path -> info_files/user_info_organized.txt
    # except Exception as e:
    #     print(f"Error while organizing user information: {e}")
    #     # exit the program
    #     return
    
    # Now, lets call the main crew to build the resume
    
    inputs = {
        'user_info_orgainzed_file_path': user_info_orgainzed_file_path
    }
    UserInfoOrganizerCrew().crew().kickoff(inputs=inputs)
