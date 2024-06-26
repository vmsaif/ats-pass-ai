# ATS Pass AI

[![Hits](https://hits.sh/github.com/vmsaif/ats-pass-ai.svg?label=Visits&color=100b75)](https://hits.sh/github.com/vmsaif/ats-pass-ai/)

## Project Description

The idea is to craft a unique resume for each job application. With this approach, every resume is designed anew, ensuring it's **highly** tailored to the specific job description and optimized to pass the Applicant Tracking System (ATS). 

This program is your ultimate tool for creating highly personalized resumes efficiently, saving you time and increasing your chances of catching an employer's eye.

ATS Pass AI is an innovative tool designed to automate the creation of personalized resumes. It utilizes several AI agents, each specializing in different aspects of the resume creation process. They collaborate to make the best possible resume for the user. The system is designed to help job seekers create resumes that are highly tailored to specific job descriptions, increasing their chances of passing through Applicant Tracking Systems (ATS) and landing interviews.

The system aims to achieve at least an 85% keyword match with job descriptions, ensuring that the resumes are tailored and ATS-friendly.

## Current Development Status 🚀

The project is currently in the **active development stage**. The following features have been implemented:

1. **User Information Collection** 📋
   - The system can extract and organize user data provided by the user in an unorganized way. *(Completed)* ✅

2. **Job Description Analysis** 🤝
   - The system can analyze job descriptions to identify key keywords and requirements. *(Completed)* ✅

3. **Resume Creation** 🧑‍💼
   - The system can integrate user information with job description analysis to draft resumes. *(Completed)* ✅

4. **LaTeX Resume Generation** 🛠️
   - The system can convert finalized resumes into professionally formatted LaTeX documents. *(In Progress)* ⏳

## An Overview of the System
The user begins by providing their information however they see fit, also can upload their resume. Then the system will extract and organize the user data and understand the user's skills and experiences. The user can then upload job descriptions which will be analyzed to identify key phases, keywords and requirements. 

The system will then compare the user data with the job description to generate a resume that is tailored to the job. The user can then download the resume in LaTeX format or plain text format. More features will be added in the future to make the system more user-friendly and efficient.

### Key Features
- **User Information Collection**: Extracts and organizes user data from provided text files.
- **Job Description Analysis**: Analyzes job descriptions to identify key keywords and requirements.
- **Resume Creation**: Integrates user information with job description analysis to draft resumes.
- **LaTeX Resume Generation**: Converts finalized resumes into professionally formatted LaTeX documents.

## Installation and Usage

### Prerequisites
- Ensure Python 3.8 or higher is installed on your machine. [Download Python](https://www.python.org/downloads/) and include it in your system's PATH during installation.


### 1: Clone the repository and install the required Python libraries:
```bash
git clone https://github.com/vmsaif/ats-pass-ai
```

### 2: Install poetry

```bash
pip install poetry
```

### 3: Set the virtual environment to be in the project directory (This is optional but recommended):
This will make it easier to set IDE's Python interpreter to the virtual environment. Run the following command in the project directory:

```bash
poetry config virtualenvs.in-project true
```

Also, install the required libraries:

```bash
poetry install

```

### 4: Configure API Key
- Obtain a GOOGLE_API_KEY by following the instructions at [Google Cloud Console](https://console.cloud.google.com/apis/credentials). Ensure the API key has appropriate permissions enabled.

- Obtain a GROQ_API_KEY by following the instructions at [GROQ](https://console.groq.com/keys). 

- `Create` a .env file in the root directory and add:

```plaintext
GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY_HERE
GROQ_API_KEY=YOUR_GROQ_API_KEY_HERE
```

Note: Replace `YOUR_GOOGLE_API_KEY_HERE ` and `YOUR_GROQ_API_KEY ` with your actual API keys. No need to include quotes.

### 5: Prepare Your Data

- Add your information or resume to `user_info.txt`.
- Add job descriptions to `job_description.txt`.

### 6: Run the Application
   
From the root directory, run the following command:

```bash
poetry run ats_pass_ai

```

### 7. Retrieve Your Resumes
- Find the generated resumes in the output directory, available in both LaTeX and plain text formats. (Coming soon)

