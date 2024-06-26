import os
from textwrap import dedent
# from langchain_community.embeddings import OllamaEmbeddings
from langchain.tools import tool
from langchain_community.vectorstores import Chroma

# from chromadb.utils.embedding_functions import GoogleGenerativeAiEmbeddingFunction
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
# from langchain.docstore.document import Document
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
import hashlib
import shutil
from ats_pass_ai.output_file_paths import PATHS

# Set up the embedding function
# embedding_function = OllamaEmbeddings(model='nomic-embed-text')
# embedding_function = OllamaEmbeddings(model='mxbai-embed-large')
# embedding_function = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")

from langchain_core.embeddings import Embeddings
from chromadb.api.types import EmbeddingFunction

# Adapter to use Chroma Embeddings with Langchain Embeddings
class ChromaEmbeddingsAdapter(Embeddings):
    def __init__(self, ef: EmbeddingFunction):
        self.ef = ef

    def embed_documents(self, texts):
        return self.ef(texts)

    def embed_query(self, query):
        return self.ef([query])[0]
    
# embedding_function = ChromaEmbeddingsAdapter(GoogleGenerativeAiEmbeddingFunction(api_key=os.getenv('GOOGLE_API_KEY')))
embedding_function = ChromaEmbeddingsAdapter(SentenceTransformerEmbeddingFunction(model_name='all-MiniLM-L6-v2'))


# Tool to search in Chroma DB
class SearchInChromaDB:
    @tool("Search for the chunk of relevant content")
    def search(question: str) -> str:
        """Search for relevant content based on an question.
            argument:
            question: (str) The question as a string to search for.
            
            return:
            results: (str) a chunk of relavent content based on the question. 
            
            You need to understand the content and extract the information you need within the chunk without any further calling of this tool.
        """
        vectorstore = Chroma(persist_directory=RagSearchTool.persist_directory, embedding_function=embedding_function)
        results = vectorstore.similarity_search(query = question, k = 3)
        
        return results

class RagSearchTool:

    persist_directory = PATHS['rag_db_perist_dir']
    
    def _file_hash(file_path: str) -> str:
        """Generate a hash for a given file."""
        hasher = hashlib.sha256()
        with open(file_path, 'rb') as f:
            buf = f.read()
            hasher.update(buf)
        return hasher.hexdigest()

    # Check if a file has been already indexed in Chroma DB
    def _file_indexed_before(file_path: str, hash_file_path: str) -> bool:
        """Check if a file has been indexed in Chroma DB."""
        current_file_hash = RagSearchTool._file_hash(file_path)
        result = False

        # Check if the file hash is in the hash_store, if not, then then file definitely has not been indexed
        if not os.path.exists(hash_file_path):
            # create the hash_store file, then return False
            with open(hash_file_path, 'w') as file:
                pass 
            result = False
            print("New hash store file created.")
        else:
            # Check if the file hash is in the hash_store
            with open(hash_file_path, 'r') as f:
                hashes = f.readlines()
                for hash in hashes:
                    if current_file_hash in hash:
                        result = True
                        print("File has been indexed before.")
        if(result == False):
            RagSearchTool.delete_applicant_profile_files(delete_pretasks = True)
        return result
    
    def process_and_index(file_path: str):
        """Reads TXT file and indexes its content in Chroma DB."""

        hash_file_path = PATHS['hash_file_path'] # should be in the same directory as the Chroma DB

        run_flag = False

        # check if the persist directory exists, if not, create it
        if not os.path.exists(RagSearchTool.persist_directory):
            run_flag = True
            print("Persist directory does not exist.")
        else:
            # Persist directory already exists. 
            # Check if the file has been processed before
            if not RagSearchTool._file_indexed_before(file_path, hash_file_path):
                run_flag = True
                print("File has not been processed before.")
            else:
                print("File has been indexed before. Skipping Indexing.")

        if(run_flag):
            # Load the content from the file

            # delete the existing Chroma DB if it exists
            RagSearchTool._delete_persist_directory()

            loader = TextLoader(file_path, encoding='utf-8')
            doc = loader.load()
            # print(doc)
            # Split the content into chunks
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=900, chunk_overlap=200)
            splits = text_splitter.split_documents(doc)  # Split large document content
            # print ("Splits: ", splits[0])
            # Now index the content in Chroma DB
            if splits:
                # Create a VectorStore with document embedding
                print("Indexing content in DB...")
                # print(splits)
                # for split in splits:
                #     print(split)
                Chroma.from_documents(documents=splits, embedding=embedding_function, persist_directory=RagSearchTool.persist_directory)
                print("Content indexed in Chroma DB")

                RagSearchTool._updateHashFile(file_path, hash_file_path)
                return "Content indexed in DB"
            else:
                return "No content available for processing."  

    def _delete_persist_directory():
        """Delete the persist directory."""
        if os.path.exists(RagSearchTool.persist_directory):
            shutil.rmtree(RagSearchTool.persist_directory)
            print("Persist directory deleted.")

    def _updateHashFile(file_path: str, hash_file_path: str):
        """Update the hash store file with the hash of the processed file."""
        current_file_hash = RagSearchTool._file_hash(file_path)

        try:
            if not os.path.exists(hash_file_path):
                with open(hash_file_path, 'w') as file:
                    print("New hash store file created.")
            with open(hash_file_path, 'a') as f:
                f.write(current_file_hash + '\n')
            print("Hash store file updated.")
        except Exception as e:
            print(f"Error while updating/creating hash store file: {e}")

    def delete_applicant_profile_files(delete_pretasks: bool = False):
        """Delete the applicant profile files but not the folder, optionally delete pre-task files."""
        
        RagSearchTool._delete_files_in_directory(PATHS["info_extraction_folder_path"])
        print("applicant profile files deletion attempt complete.")

        # Optionally delete files in the pre-tasks folder
        if delete_pretasks:
            RagSearchTool._delete_files_in_directory(PATHS["draft_output_dir"])
            RagSearchTool._delete_files_in_directory(PATHS["pre_tasks_folder_path"])
            print("Pre-task files deletion attempt complete. Deleted Draft output and Pre-tasks files.")

    def _delete_files_in_directory(directory_path):
        """Helper function to delete all files in the specified directory and print the operation results."""
        print(f"Deleting files in directory: {directory_path}")
        entries = os.listdir(directory_path)
        for entry in entries:
            full_path = os.path.join(directory_path, entry)
            if os.path.isfile(full_path):
                try:
                    os.remove(full_path)
                    print(f"Deleted file: {full_path}")
                except PermissionError as e:
                    print(f"Could not delete {full_path}. Permission denied: {e}")
                except Exception as e:
                    print(f"Error while deleting {full_path}: {e}")
            else:
                print(f"Skipped: {full_path} (not a file)")
