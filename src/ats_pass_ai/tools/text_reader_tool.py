from langchain.tools import BaseTool
from langchain.pydantic_v1 import BaseModel, Field
from transformers import GPT2Tokenizer
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Type, Optional
from textwrap import dedent


from langchain.callbacks.manager import (
    # AsyncCallbackManagerForToolRun, # need to turn on if want to use async, also change run method to async and the parameter
    CallbackManagerForToolRun,
)

class DocumentInput(BaseModel):
    action: str = Field(description="The action needs to be done")
    file_path: str = Field(description="The path to the local file containing the document.")

class TextFileReaderTool(BaseTool):
    name = "Text File Reader Tool"
    description = dedent(
        """The tool takes 2 arguments: 
        action: str = Field(description="The action needs to be done")
        file_path: str = Field(description="The path to the local file containing the document.")

        Note, the tool internally breaks down the document into chunks and query each chunks. So it is normal to see some repeated information or some missing information.
        Ensure completeness and accuracy. Note that the user may not have all the information.
        """)
    args_schema: Type[BaseModel] = DocumentInput

    def _run(self, file_path: str, action: str, run_manager: Optional[CallbackManagerForToolRun] = None):
        """This method breaks the document into multiple chunks then sends each chunk to the model with the action asked."""

        llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            top_k=50, 
            top_p=0.95
        )

        tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
        token_limit = 2000
        chunk_overlap_tokens = 20

        document = self._read_text_file(file_path)
        text_chunks = self._split_text(document, token_limit, tokenizer, chunk_overlap_tokens)
        payload = []
        summaries = []

        # Prepare the batch of inputs
        for chunk in text_chunks:
            payload.append(action + "\n" + chunk)
        response = llm.batch(payload)

        for res in response:
            summaries.append(res.content)

        return "\n".join(summaries)  # Joining summaries if they're separate strings


    def _read_text_file(self, file_path: str):
        """Read and return content from a file specified by its path."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            print(f"File not found at the specified path: {file_path}")
        

    def _split_text(self, text: str, limit: int, tokenizer: GPT2Tokenizer, chunk_overlap_tokens: int):
        """
        Splits the text into chunks that fit within the given token limit, with an overlap between consecutive chunks.

        Overlap Mechanism: The function includes an overlap parameter that determines how many tokens (approximately, based on word count) are carried over to the next chunk. This helps in maintaining context across chunk boundaries.

        Overlap Buffer: This buffer stores the last few words of the current chunk to prepend them to the next chunk, creating the overlap.
        
        Current Length Recalculation: When a new chunk starts, instead of resetting to zero or the length of the new word, the length is recalculated to include the entire new chunk starting with the overlap.
        
        Parameters:
            text (str): The text to be split.
            limit (int): The maximum token count for each chunk.
            tokenizer (GPT2Tokenizer): The tokenizer to use for tokenizing text.
            overlap (int): The number of tokens to overlap between consecutive chunks.
        """
        words = text.split()
        current_chunk = []
        chunks = []
        current_length = 0
        overlap_buffer = []

        for word in words:
            tokens = tokenizer.tokenize(word)
            num_tokens = len(tokens)
            if current_length + num_tokens > limit:
                # When the current chunk limit is reached
                # Join the current chunk and store it
                chunks.append(' '.join(current_chunk))
                # Start new chunk with the overlap from the previous chunk
                current_chunk = overlap_buffer + [word]
                current_length = sum(len(tokenizer.tokenize(w)) for w in current_chunk)
                # Prepare overlap buffer for the next chunk
                overlap_buffer = current_chunk[-chunk_overlap_tokens:] if len(current_chunk) > chunk_overlap_tokens else current_chunk
            else:
                current_chunk.append(word)
                current_length += num_tokens

        # add the last chunk if it exists
        if current_chunk:
            chunks.append(' '.join(current_chunk))

        return chunks


