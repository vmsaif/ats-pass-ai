#!/usr/bin/env python
from ats_pass_ai.crew import AtsPassAiCrew


def run():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    inputs = {
        'topic': 'AI LLMs'
    }
    AtsPassAiCrew().crew().kickoff(inputs=inputs)