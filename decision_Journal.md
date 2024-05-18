# Decision Journal

## May-1-2024

Here, I will be documenting the decisions I make during the project. Because of doing test and trials, I will be making a lot of decisions and there will be a lot of dead-ends. I will be documenting them here. 

1. First, I tried to use gemini to organize the whole txt file to organize. It couldnt process the whole file,
    - then i broke in into chunks, then asked it to process. It was able to process the chunks and "Almost" accurate
2. Then I tried to use txt rag from crewai to build an user profile, or experience profile, didnt work with my current model llama3. the txt rag tool was always looking at the wrong place.
3. Then I tried to rag using the organizer tool of step 1. but this time, sending the organized file to extract info. It was working really good, but when i started doing 6-7 tasks togather, the crewai was maxed out groq api token requests per minute. 
    Consideration: need its own vector db so that I can reduce the token count.

4. Working on local vectordb with chroma, i intened to do rag with llama3 on the vectordb.

## May-5-2024

- ended up doing rag using chromadb llama3 to do the rag. It was working okay, but the agents were doing repeatative behavious using llala3-8b-8192 model. 

- Switched to langchain_google_genai -> GoogleGenerativeAI (Not ChatGoogleGenerativeAI) and it was doing the rags in just 1 shot.

- Also the context field of tasks was not working with llama3-8b,70b models. So, I switched to langchain_google_genai, and it is working fine.