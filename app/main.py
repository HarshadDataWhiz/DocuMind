from pdfLoader import load_pages
from vectorStore import vectorStore
from chain import Chain
import os

def get_response(question: str, filepath: str):

    document_pages = load_pages(filepath)

    print(document_pages[0])

    # splitting
    document_pages_split = vectorStore.split_text(document_pages)
    
    # creating the vector store
    vectorStore.create_vector_store(document_pages_split)

    # search question in vector store
    pages_data = vectorStore.search(question = question)

    # getting the answer
    chain = Chain()
    answer = chain.get_answer(question = question, docs_data = pages_data)
    return answer

if __name__ == '__main__':
    file_path = os.path.join(os.curdir, 'data', 'Documents', 'Report_Harshad_Kumar.pdf')
    
    ans = get_response("Who is the supervisor of the thesis?", file_path)

    print(ans)

