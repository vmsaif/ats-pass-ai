# ATS Pass AI

## Project Description

The idea is to craft a unique resume for each job application. With this approach, every resume is designed anew, ensuring it's **highly** tailored to the specific job description and optimized to pass the Applicant Tracking System (ATS). 

This program is your ultimate tool for creating highly personalized resumes efficiently, saving you time and increasing your chances of catching an employer's eye.

ATS Pass AI is an innovative tool designed to automate the creation of personalized resumes. It utilizes several AI agents, each specializing in different aspects of the resume creation process. They collaborate to make the best possible resume for the user. The system is designed to help job seekers create resumes that are highly tailored to specific job descriptions, increasing their chances of passing through Applicant Tracking Systems (ATS) and landing interviews.

The system aims to achieve at least an 85% keyword match with job descriptions, ensuring that the resumes are tailored and ATS-friendly.

## Current Development Status 🚀

The project is currently in the **active development stage**. The following features have been implemented:

1. **User Information Collection** ✅
   - The system can extract and organize user data provided by the user in an unorganized way. *(Completed)* ✅

2. **Job Description Analysis** 🔧
   - The system can analyze job descriptions to identify key keywords and requirements. *(In Progress)* ⏳

3. **Resume Creation** 🔧
   - The system can integrate user information with job description analysis to draft resumes. *(Scheduled)* 📅

4. **LaTeX Resume Generation** 🔧
   - The system can convert finalized resumes into professionally formatted LaTeX documents. *(Scheduled)* 📅



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

### 2: Create a Python virtual environment and install the required libraries:

```bash
# create a python virtual environment

# for windows
python -m venv venv
.\.venv\Scripts\activate 
```
    
```bash
# for linux
python3 -m venv venv
source .venv/bin/activate 
```

### 3: Install the required Python libraries:
```bash
cd ats-pass-ai
pip install -r requirements.txt
```

### 4: Configure API Key
- Obtain a GOOGLE_API_KEY by following the instructions at [Google Cloud Console](https://console.cloud.google.com/apis/credentials). Ensure the API key has appropriate permissions enabled.

- Create a .env file in the root directory and add:
```plaintext
GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY_HERE
```



### 5: Prepare Your Data

- Add your information or resume to `user_info.txt`.
- Add job descriptions to `job_description.txt`.

### 6: Run the Application
```bash
#Windows:
python app_gem.py

#Linux:
python3 app_gem.py
```


### 7. Retrieve Your Resumes
- Find the generated resumes in the output directory, available in both LaTeX and plain text formats.

