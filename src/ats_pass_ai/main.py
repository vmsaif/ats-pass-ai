#!/usr/bin/env python
from ats_pass_ai.user_info_organizer_crew import UserInfoOrganizerCrew


def run():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    # inputs = {
    #     'topic': 'AI LLMs'
    # }
    # AtsPassAiCrew().crew().kickoff(inputs=inputs)
    UserInfoOrganizerCrew().crew().kickoff()