#!/usr/bin/env python
from ats_pass_ai.user_info_organizer_crew import UserInfoOrganizerCrew


def run():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    inputs = {
        'user_info_file_path': 'info_files/user_info.txt'
    }
    UserInfoOrganizerCrew().crew().kickoff(inputs=inputs)
