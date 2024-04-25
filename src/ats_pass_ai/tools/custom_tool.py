# Creating a tool to perform rag search on a txt file
from langchain.tools.retriever import create_retriever_tool
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter

from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings


    # name: str = "Text Search Tool"
    # description: str = "This tool searches for a specific text in a txt file."

def run(self, argument: str) -> str:
    loader = TextLoader('info_files/user_info.txt')
    documents=loader.load()

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=500)
    texts = text_splitter.split_documents(documents)

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    db = FAISS.from_documents(texts, embeddings)

    retriever = db.as_retriever()

    
    return 

# test it

# tool = MyCustomTool()

# print(tool.run("What is the user's name?"))




    

