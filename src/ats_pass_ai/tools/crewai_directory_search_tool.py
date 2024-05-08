
from crewai_tools import FileReadTool
# from crewai_tools import DirectoryReadTool
# from crewai_tools import TXTSearchTool
# Create a new instance of the TXTSearchTool

class CrewAIFileReadTool:
    @classmethod
    def create(cls, file_path: str):
        return FileReadTool(
            config=dict(
                llm=dict(
                    provider="google", 
                    config=dict(
                        model="gemini-pro",
                    ),
                ),
                embedder=dict(
                    provider="google",
                    config=dict(
                        model="models/embedding-001",
                        task_type="retrieval_document",
                        # title=""
                    ),
                ),
            ),
            file_path=file_path
        )
            
