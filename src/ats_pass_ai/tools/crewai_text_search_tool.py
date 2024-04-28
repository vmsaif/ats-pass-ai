
from crewai_tools import TXTSearchTool
# Create a new instance of the TXTSearchTool

class CrewAITextSearchTool:
    @classmethod
    def create(cls):
        return TXTSearchTool(
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
        )
            
