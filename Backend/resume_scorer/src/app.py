from fastapi import FastAPI, HTTPException, UploadFile, File
import PyPDF2
from docx import Document
import io
from scorer import ResumeScorer
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware


origins = [
        "*",  
]
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/resume_scorer")
async def score_resume(resume_file: UploadFile = File(...), job_description: str = ("The job description")) -> JSONResponse:
    """
    Scores a resume based on a job description.

    Parameters:
    - resume_file (UploadFile): The uploaded resume file to be scored.
    - job_description (str): The job description to compare the resume against.

    Returns:
    - JSONResponse: JSON response containing the compatibility score between the resume and job description.
    """
    try:
        # Read text from the resume file
        if resume_file.filename.endswith('.pdf'):
            pdf_reader = PyPDF2.PdfReader(resume_file.file)
            count = len(pdf_reader.pages)
            text = []
            for i in range(count):
                page = pdf_reader.pages[i]
                text.append(page.extract_text())

        elif resume_file.filename.endswith('.docx'):
            doc = Document(io.BytesIO(await resume_file.read()))
            text = [p.text for p in doc.paragraphs]

        # Join text from the resume
        text = ' '.join(text)

        # Create a ResumeScorer instance and score the resume
        scoring = ResumeScorer(text, job_description)
        score = scoring.generate_analysis()

        # Return the score as a JSON response
        return JSONResponse(content={"score": score})
    except Exception as e:
        # Raise an HTTP exception if an error occurs
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def health_check() -> str:
    """
    Basic health check endpoint to confirm the application is running.

    Returns:
    - str: A simple message indicating that the application is running successfully.
    """
    return "Running Successfully"
