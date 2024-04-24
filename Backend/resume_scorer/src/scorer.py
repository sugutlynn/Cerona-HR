from typing import List
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()


class ResumeScorer:
    def __init__(self, resumes: List[str], jd: str):
        """
        Initializes the ResumeScorer instance.

        Parameters:
        - resumes (List[str]): List of resumes submitted for the job.
        - jd (str): Job description details.
        """
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.model_name = 'text-embedding-ada-002'
        self.resumes = resumes
        self.jd = jd
        self.client = OpenAI(api_key=self.openai_api_key)

    def generate_analysis(self) -> str:
        """
        Generates an analysis of the compatibility between resumes and the job description.

        Returns:
        - str: The numerical score out of 100 indicating how well the resume matches the job description.
        """
        # Generate a text completion using OpenAI GPT-3.5-turbo
        text_gen = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {
                    "role": "system",
                    "content": """
                            Your task is to score each resume to determine how well the resume matches the job description and give a score out of 100.
                            Follow these steps:

                            1. **Content Relevance**: Assess how closely the content of the resume aligns with the job description, focusing on key skills, experiences, and qualifications required for the role.

                            2. **Language and Tone**: Evaluate the language and tone of the resume to see if they match the job description in terms of professionalism and alignment with the company's culture.

                            3. **Format and Presentation**: Examine the format and presentation of the resume to ensure it is clear, concise, and easy to read.

                            4. **Keywords Matching**: Check the presence of relevant keywords in the resume that match the job description.

                            5. **Experience and Achievements**: Assess whether the candidate's experience and achievements are relevant to the job requirements.

                            6. **Overall Compatibility**: Consider the overall compatibility of the resume with the job description.

                            Strictly respond with just the numerical score.
                            Do not include newlines. Do not return any markdown formatting, just a numerical value.
                            """
                },
                {
                    "role": "user",
                    "content": f"These are the individual's information: \
                            \n- resume: {self.resumes} \
                            \n- job description: {self.jd} "
                }
            ]
        )

        choice = text_gen.choices[0]
        message = choice.message
        content = message.content
        
        return content
