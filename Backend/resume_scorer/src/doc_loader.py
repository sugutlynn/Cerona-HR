from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import Docx2txtLoader
from langchain.document_loaders import TextLoader
from pathlib import Path

class DocumentLoader:
    def load_file(self, file_path: str) -> str:
        """
        Loads a document from the given file path and returns its content as a single string.

        Parameters:
        - file_path (str): The path to the file to be loaded.

        Returns:
        - str: The content of the file as a single string.

        Raises:
        - ValueError: If the file format is not supported.
        """
        documents = []

        # Convert file path to Path object if it's a string
        file = Path(file_path) if isinstance(file_path, str) else file_path

        if file is not None:
            file_name = file.name

            # Determine file type and load accordingly
            if file_name.endswith(".pdf"):
                loader = PyPDFLoader(str(file))
                documents.extend(loader.load())
            elif file_name.endswith('.docx') or file_name.endswith('.doc'):
                loader = Docx2txtLoader(str(file))
                documents.extend(loader.load())
            elif file_name.endswith('.txt'):
                loader = TextLoader(str(file))
                documents.extend(loader.load())
            else:
                raise ValueError("Unsupported file format. Supported formats are .pdf, .docx, .doc, and .txt.")

        # Combine all loaded documents into a single string and return
        return ' '.join(str(doc) for doc in documents)
