from langchain_google_genai import ChatGoogleGenerativeAI
from transformers import GPT2Tokenizer
import getpass
import os

# Check and set the API key
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Provide your Google API Key")


# Initialize the model
llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    top_k=50, 
    top_p=0.95
)

# Load the tokenizer
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

def read_text_file(file_path):
    """Read and return content from a given file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def split_text(text, limit):
    """Split the text into chunks that fit within the given token limit."""
    words = text.split()
    current_chunk = []
    chunks = []
    current_length = 0

    for word in words:
        tokens = tokenizer.tokenize(word)
        num_tokens = len(tokens)  # Get the number of tokens for the current word
        if current_length + num_tokens + 1 > limit:  # +1 for space between words
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_length = num_tokens  # Reset current_length to the number of tokens in the new word
        else:
            current_chunk.append(word)
            current_length += num_tokens + 1  # Add number of tokens + 1 for space

    if current_chunk:  # Don't forget to add the last chunk if it exists
        chunks.append(' '.join(current_chunk))
    print(f"Number of chunks created: {len(chunks)}")
    return chunks

def interact_with_document(text):
    """Interact with the model to generate a summary for the provided text while managing token limits using batch processing."""
    token_limit = 2000  # Define the token limit for the model context window
    summaries = []

    # Split the text into manageable chunks
    text_chunks = split_text(text, token_limit)

    # Prepare the batch of inputs
    payload = []
    for chunk in text_chunks:
        payload.append("Please summarize the following document." + chunk)
    response = llm.batch(payload)

    for res in response:
        summaries.append(res.content)

    return " ".join(summaries)  # Joining summaries if they're separate strings

def main():
    """Main function to process the document summary."""
    file_path = "../../info_files/user_info.txt"  # Update path if necessary
    text = read_text_file(file_path)
    summary = interact_with_document(text)
    print("Summary of the document:")
    print(summary)

if __name__ == "__main__":
    main()
