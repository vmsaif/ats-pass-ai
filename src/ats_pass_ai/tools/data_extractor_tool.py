from langchain.tools import BaseTool
from langchain.pydantic_v1 import BaseModel, Field
from transformers import GPT2Tokenizer
from typing import Type, Optional
from textwrap import dedent
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)

from langchain.callbacks.manager import (
    # AsyncCallbackManagerForToolRun, # need to turn on if want to use async, also change run method to async and the parameter
    CallbackManagerForToolRun,
)

class DocumentInput(BaseModel):
    action: str = Field(description="The action needs to be done")
    file_path: str = Field(description="The path to the local file containing the document.")
    temperature: float = Field(description="The temperature for the model.")
    top_k: int = Field(description="The top_k for the model.")
    top_p: float = Field(description="The top_p for the model.")

class DataExtractorTool(BaseTool):
    name = "DataExtractorTool"
    description = dedent(
        """The tool takes 2 arguments: 
        action: str = Field(description="The action needs to be done")
        file_path: str = Field(description="The path to the local file containing the document.")
        temperature: float = Field(description="The temperature for the model.")
        top_k: int = Field(description="The top_k for the model.")
        top_p: float = Field(description="The top_p for the model.")

        Note, the tool internally breaks down the document into chunks and query each chunks. So it is normal to see some repeated information or some missing information.
        Ensure completeness and accuracy. Note that the user may not have all the information.
        """)
    args_schema: Type[BaseModel] = DocumentInput

    def _run(self, file_path: str, action: str, temperature: float, top_k: int, top_p: float, run_manager: Optional[CallbackManagerForToolRun] = None):
        """This method breaks the document into multiple chunks then sends each chunk to the model with the action asked."""

        llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            safety_settings={
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            }
        )

        tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
        token_limit = 2000
        chunk_overlap_tokens = 100

        document = self._read_text_file(file_path)
        text_chunks = self._split_text(document, action, token_limit, tokenizer, chunk_overlap_tokens)
        payload = []
        summaries = []

        # Prepare the batch of inputs
        
        for chunk in text_chunks:
            payload.append(action +'\n'+ chunk)
        print('Sending the payload to the model...')
        response = llm.batch(payload)

        for res in response:
            summaries.append(res.content)
        print('Received response from the model...')
        return "\n".join(summaries)  # Joining summaries if they're separate strings


    def _read_text_file(self, file_path: str):
        """Read and return content from a file specified by its path."""
        try:
            print('\n\nStarted reading the file...')
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            print(f"File not found at the specified path: {file_path}")
        

    def _split_text(self, text: str, action: str, limit: int, tokenizer: GPT2Tokenizer, chunk_overlap_tokens: int):
        """
        Splits the text into chunks at the nearest double newline character before exceeding the limit,
        or based on token count if no suitable newline is found. It includes an overlap between consecutive chunks.

        Parameters:
            text (str): The text to be split.
            limit (int): The maximum token count for each chunk.
            tokenizer (GPT2Tokenizer): The tokenizer to use for tokenizing text.
            chunk_overlap_tokens (int): The number of tokens to overlap between consecutive chunks.
        """
        words = text.split()
        current_chunk = []
        chunks = []
        current_length = 0
        overlap_buffer = []
        reconstructed_text = ' '.join(words)
        last_newline_pos = 0  # Position of last encountered newline in reconstructed text

        action_tokens = tokenizer.tokenize(action)
        num_action_tokens = len(action_tokens)

        start_index = 0  # Start index of the current chunk in reconstructed text

        for i, word in enumerate(words):
            tokens = tokenizer.tokenize(word)
            num_tokens = len(tokens)

            if current_length + num_tokens + num_action_tokens > limit:
                # Look for last double newline before the current position in the reconstructed text
                last_newline_pos = reconstructed_text.rfind('\n\n', start_index, start_index + current_length)
                
                # If a newline is found and is a reasonable place to split
                if last_newline_pos != -1:
                    # Create the chunk up to the last newline
                    chunks.append(reconstructed_text[start_index:last_newline_pos].strip())
                    start_index = last_newline_pos + 2  # Start after the newline
                    current_chunk = reconstructed_text[start_index:start_index + current_length].split()
                    current_length = sum(len(tokenizer.tokenize(w)) for w in current_chunk)
                    overlap_buffer = current_chunk[-chunk_overlap_tokens:] if len(current_chunk) > chunk_overlap_tokens else current_chunk
                else:
                    # No newline found, split at current position
                    chunks.append(' '.join(current_chunk))
                    current_chunk = overlap_buffer + [word]
                    current_length = sum(len(tokenizer.tokenize(w)) for w in current_chunk)

            else:
                current_chunk.append(word)
                current_length += num_tokens

        # Add the last chunk if it exists
        if current_chunk:
            chunks.append(' '.join(current_chunk))

        return chunks

