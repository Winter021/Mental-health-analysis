import streamlit as st
from util import context_retrieval, rag_process
import pandas as pd
import os 

st.markdown("<h1 style='text-align: center; color: #0066ff;'>SereneScreen</h1>", unsafe_allow_html=True)

# Upload file
uploaded_file = st.file_uploader("Upload a file", type=['csv'])

if uploaded_file is not None:
    try:
        # Save the uploaded file locally
        save_path = os.path.join("files", uploaded_file.name)  # Specify the save path
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getvalue())

        # Retrieve context based on the saved file and query
        print("save path is: ", save_path)
        retrieved_docs = context_retrieval(save_path, "Which of these is most indicative of the user's mental health state?")

        # Proceed button
        if st.button("Proceed"):
            # Perform RAG process and get prediction
            question = "From the information provided, what do you make of the mental state of the user? You can answer with possible mental health conditions or conclude that the user seems normal."
            prediction = rag_process("mistral", retrieved_docs, question)

            # Display prediction in a nice box
            st.success("Mental Health Prediction:")
            st.info(prediction)
            # Add an exit button to start afresh
            if st.button("Exit"):
                st.experimental_rerun()
    except Exception as e:
        st.error(f"Error loading CSV file: {e}")
