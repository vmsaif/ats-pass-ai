from langchain_community.embeddings import OllamaEmbeddings
from langchain.tools import tool
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader

# Set up the embedding function
embedding_function = OllamaEmbeddings(model='nomic-embed-text')

# class Document:
#     """Extended document structure to handle metadata and text data."""
#     def __init__(self, content, metadata):
#         self.page_content = content
#         self.metadata = metadata

class RagSearchTool:
    
    def process_and_index(file_path: str):
        """Reads TXT file and indexes its content in Chroma DB."""
        loader = TextLoader(file_path)
        doc = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(doc)  # Split large document  content
        
        # Now index the content in Chroma DB
        if splits:
            # Create a VectorStore with document embedding
            print("Indexing content in Chroma DB...")
            Chroma.from_documents(splits, embedding=embedding_function, persist_directory="./chroma_db")
            print("Content indexed in Chroma DB")
            return "Content indexed in Chroma DB"
        else:
            return "No content available for processing."

# Tool to search in Chroma DB
class SearchInChromaDB:
    @tool("Search in vector database tool")
    def search(question: str) -> str:
        """Search for relevant content based on a query from a vector database.
        args:
            question (str): The question as a string to search for.
            example:
                question = "Tell me about the user's name",
                'or' 
                question = "What are the skills of the user?"
        returns:
            results (str): a chunk of relavent content based on the question.
        """
        vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embedding_function)
        results = vectorstore.similarity_search(question)
        return results
    
# # Example usage
# if __name__ == "__main__":
#     file_path = "info_files/user_info_organized.txt"
#     # RagSearchTool.process_and_index(file_path)
#     query = "Tell me about the user's name"
#     SearchInChromaDB.search(query)

