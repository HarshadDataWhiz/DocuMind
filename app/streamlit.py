import streamlit as st
import requests

st.title("📄 PDF Q&A with FastAPI + Streamlit")

# Input fields
filename = st.text_input("Enter PDF filename (e.g., Report_Harshad_Kumar.pdf)")
question = st.text_area("Enter your question")

if st.button("Ask"):
    if filename and question:
        with st.spinner("Fetching answer..."):
            response = requests.get("http://127.0.0.1:8000/ask",
                                    params={"question": question, "filename": filename})
            if response.status_code == 200:
                data = response.json()
                if "error" in data:
                    st.error(data["error"])
                else:
                    st.success(f"Answer: {data['answer']}")
            else:
                st.error("Error contacting backend API")
    else:
        st.warning("Please provide both filename and question")
