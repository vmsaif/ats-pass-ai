from crewai_tools import TXTSearchTool

# Create a new instance of the TXTSearchTool

class MyTXTSearchTool:
    @classmethod 
    def create(cls, txt_path):
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
                        model="models/text-embedding-004",
                        task_type="retrieval_document",
                        title=""
                    ),
                ),
            ),
            txt=txt_path
        )
            
