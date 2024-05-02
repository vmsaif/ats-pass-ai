
from crewai_tools import DirectorySearchTool
# Create a new instance of the TXTSearchTool

class CrewAIDirectorySearchTool:
    @classmethod
    def create(cls, directory: str):
        return DirectorySearchTool(
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
            directory=directory
        )
            
