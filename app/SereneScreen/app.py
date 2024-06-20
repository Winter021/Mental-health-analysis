import streamlit as st
import pandas as pd
import os
import csv
import threading
import datetime
from util import context_retrieval, rag_process
from capture import capture, ScreenshotApp

st.markdown("<h1 style='text-align: center; color: #0066ff;'>SereneScreen</h1>", unsafe_allow_html=True)

# Initialize session state for capture process
if 'capture_running' not in st.session_state:
    st.session_state.capture_running = False
    st.session_state.capture_thread = None
    st.session_state.stop_flag = threading.Event()

# Path to the CSV file
csv_file = "captions.csv"
flag = True
if not os.path.exists(csv_file):
    with open(csv_file, 'w', newline='') as file:
        # file.write("")
        writer = csv.writer(file)
        writer.writerow(["Caption", "Extracted text", "Summary", "Time of the Event", "Anxiety%", "Loneliness%", "Stress%", "Event Time Period"])
        current_time = datetime.datetime.now().time()
        writer.writerow(["Unkown Event", "", "", current_time, "", "", ""])

# Function to toggle capture process
def toggle_capture():
    if st.session_state.capture_running:
        st.session_state.capture_running = False
        if st.session_state.capture_thread and st.session_state.capture_thread.is_alive():
            st.session_state.stop_flag.set()  # Signal the thread to stop
            st.warning("Stopping capture process...")
            st.session_state.capture_thread.join()  # Wait for the thread to finish
            st.success("Capture process stopped.")
    else:
        st.session_state.stop_flag.clear()  # Reset the stop flag
        st.session_state.capture_running = True
        st.session_state.capture_thread = threading.Thread(target=capture, args=(st.session_state.stop_flag, flag,))
        st.session_state.capture_thread.start()
        st.success("Capture process started.")

# Upload file
uploaded_file = st.file_uploader("Upload a file", type=['csv'])

if uploaded_file is not None:
    try:
        # Save the uploaded file locally
        script_dir = os.path.dirname(os.path.abspath(__file__))
        files_dir = os.path.join(script_dir, "files")
        os.makedirs(files_dir, exist_ok=True)
        save_path = os.path.join("files", uploaded_file.name)  # Specify the save path
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        # Retrieve context based on the saved file and query
        retrieved_docs = context_retrieval(save_path, "Which of these is most indicative of the user's mental health state?")

        print("doesn't work")
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

# Button to start/stop the capture process
if st.button("Toggle Capture"):
    toggle_capture()

# Display capture status
if st.session_state.capture_running:
    st.info("Capture process is running...")
else:
    st.info("Capture process is stopped.")





# st.markdown("<h1 style='text-align: center; color: #0066ff;'>SereneScreen</h1>", unsafe_allow_html=True)

# # Initialize session state for capture process
# if 'capture_running' not in st.session_state:
#     st.session_state.capture_running = False

# # Function to toggle capture process
# def toggle_capture():
#     if st.session_state.capture_running:
#         st.session_state.capture_running = False
#     else:
#         st.session_state.capture_running = True

# # Upload file
# uploaded_file = st.file_uploader("Upload a file", type=['csv'])

# if uploaded_file is not None:
#     try:
#         # Save the uploaded file locally
#         save_path = os.path.join("files", uploaded_file.name)
#         with open(save_path, "wb") as f:
#             f.write(uploaded_file.getvalue())

#         # Retrieve context based on the saved file and query
#         retrieved_docs = context_retrieval(save_path, "Which of these is most indicative of the user's mental health state?")

#         # Proceed button
#         if st.button("Proceed"):
#             # Perform RAG process and get prediction
#             question = "From the information provided, what do you make of the mental state of the user? You can answer with possible mental health conditions or conclude that the user seems normal."
#             prediction = rag_process("mistral", retrieved_docs, question)

#             # Display prediction in a nice box
#             st.success("Mental Health Prediction:")
#             st.info(prediction)
            
#             # Add an exit button to start afresh
#             if st.button("Exit"):
#                 st.experimental_rerun()
#     except Exception as e:
#         st.error(f"Error loading CSV file: {e}")

# # Button to start/stop the capture process
# if st.button("Toggle Capture"):
#     toggle_capture()

# # Display capture status
# if st.session_state.capture_running:
#     st.info("Capture process is running...")
# else:
#     st.info("Capture process is stopped.")

# # Run the capture function if the capture process is running
# if st.session_state.capture_running:
#     capture()
