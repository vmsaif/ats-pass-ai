import os
import re
import textwrap
import numpy as np
import pandas as pd
from crewai_tools import BaseTool
import google.generativeai as genai

class DocumentSearchTool(BaseTool):
    name: str = "DocumentSearchTool"
    description: str = "Tool to search documents and generate answers using embeddings and text generation from Google's Gemini API."

    def generate_embedding(self, text, task_type='RETRIEVAL_DOCUMENT', title=None):
        return genai.embed_content(model='models/embedding-001', content=text, task_type=task_type, title=title)['embedding']

    def build_embeddings_db(self, text_chunks):
        valid_chunks = [chunk for chunk in text_chunks if not chunk.startswith('%')]
        embeddings = [self.generate_embedding(chunk, title=f"Section {i+1}") 
                      for i, chunk in enumerate(valid_chunks)]
        return pd.DataFrame({
            'Title': [f"Section {i+1}" for i in range(len(valid_chunks))],
            'Text': valid_chunks,
            'Embeddings': embeddings
        })

    def find_best_passage(self, query, df):
        query_embedding = self.generate_embedding(query, task_type='RETRIEVAL_QUERY')
        similarities = np.dot(np.stack(df['Embeddings']), query_embedding)
        max_index = np.argmax(similarities)
        return df.iloc[max_index]['Text']

    def make_prompt(self, query, relevant_passage):
        escaped = relevant_passage.replace("'", "").replace('"', "").replace("\n", " ")
        prompt = textwrap.dedent(f"""
            As an intelligent assistant, your task is to provide a comprehensive overview based on the passage provided. Summarize the key information in a clear, concise manner suitable for someone unfamiliar with the details. Focus on delivering a thorough explanation and overview.
            
            QUERY: '{query}'
            PASSAGE: '{escaped}'

            OVERVIEW:
        """)
        return prompt

    def generate_answer(self, prompt):
        model = genai.GenerativeModel('models/gemini-pro')
        response = model.generate_content(prompt)
        return response.text

    def _run(self, filepath, query):
        # Read the file and potentially split into sections
        with open(filepath, 'r') as file:
            text = file.read()
            print(f"Document length: {len(text)} characters")  # Check if the document is read correctly
        text_chunks = self.split_text_into_sections(text)
        print(f"Number of sections created: {len(text_chunks)}")  # Verify the number of sections

        df = self.build_embeddings_db(text_chunks)
        passage = self.find_best_passage(query, df)
        print(f"Selected passage for response: {passage[:500]}")  # Print a snippet of the selected passage
        prompt = self.make_prompt(query, passage)
        answer = self.generate_answer(prompt)
        return answer

    def split_text_into_sections(self, text, max_length=9900):  # slightly below 10KB for safety
      sections = []
      while text:
          # Find the last whitespace character before the max_length
          split_index = text.rfind(' ', 0, max_length)
          if split_index == -1:  # No whitespace found, force split
              split_index = max_length
          sections.append(text[:split_index].strip())
          text = text[split_index:].strip()
      return sections


# Usage example
tool = DocumentSearchTool()
file_path = "../../info_files/user_info.txt"
query = "Tell me everything about the document."
result = tool._run(file_path, query)
print(result)

# models/gemini-1.0-pro
# models/gemini-1.0-pro-001
# models/gemini-1.0-pro-latest
# models/gemini-1.0-pro-vision-latest
# models/gemini-1.5-pro-latest
# models/gemini-pro
# models/gemini-pro-vision