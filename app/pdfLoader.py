from langchain_community.document_loaders import PyPDFLoader
import os

def load_pages(filepath: str):
    # Ensure absolute path
    abs_path = os.path.abspath(filepath)
    print(f"Loading file from: {abs_path}")

    if not os.path.isfile(abs_path):
        raise FileNotFoundError(f"File does not exist: {abs_path}")

    loader = PyPDFLoader(abs_path)
    pages = loader.load()
    return pages

# if __name__ == '__main__':
#     file_path = os.path.join(os.curdir, 'data', 'Documents', 'Report_Harshad_Kumar.pdf')
#     pages = load_pages(file_path)
#     print(f"Loaded {len(pages)} pages")