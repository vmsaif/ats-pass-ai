# TODO: Implement the RAG tool that will be used to search inside a txt file
# Intended to maintain crewAI framework format

from langchain.tools import tool
from crewai_tools import TXTSearchTool


class RagTool:

    # @tool('search inside a txt file')
    # def txtRagTool(query):

        
    # Create a new instance of the TXTSearchTool

    # class MyTXTSearchTool:
    #     @classmethod 
    #     def create(cls, txt_path):
    #         return TXTSearchTool(
    #             config=dict(
    #                 llm=dict(
    #                     provider="google", 
    #                     config=dict(
    #                         model="gemini-pro"
    #                     ),
    #                 ),
    #                 embedder=dict(
    #                     provider="google",
    #                     config=dict(
    #                         model="models/embedding-001",
    #                         task_type="retrieval_document"
    #                     ),
    #                 ),
    #             ),
    #             txt=txt_path
    #         )
    
    pass