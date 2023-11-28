import base64
import logging
import traceback
import streamlit as st
import os
from decompile import decompile_qvm
from convert import convert_qvm

def initialize_session_state():
    if "file" not in st.session_state:
        st.session_state.file = None
    if "operation" not in st.session_state:
        st.session_state.operation = None
    if "version" not in st.session_state:
        st.session_state.version = None
    if "code" not in st.session_state:
        st.session_state.code = None
    if "output_file" not in st.session_state:
        st.session_state.output_file = None
    if "download_link" not in st.session_state:
        st.session_state.download_link = None
        
def clear_resources(directory):
    for file in os.listdir(directory):
        os.remove(os.path.join(directory, file))

def generate_download_link(data=None, filename="download.txt", file_extension="text/plain", auto_click=False):
    try:
        # Check for empty file name
        if not filename or len(filename) == 0:
            st.toast("Please enter a valid file name.", icon="❌")
            logging.error("Error in code downloading: Please enter a valid file name.")
            return
        
        # Check for empty data
        if data is None:
            st.toast("Data is empty. Cannot download an empty file.", icon="❌")
            logging.error("Error in code downloading: Data is empty.")
            return

        # Get the file extension if not provided
        if not file_extension or len(file_extension) == 0:
            file_extension = filename.split(".")[-1]
        
        logging.info(f"Downloading code to file: {filename} with extension: {file_extension}")

        # Check if data is binary or text
        if isinstance(data, bytes):
            # Data is binary, no need to encode it as utf-8
            b64_data = base64.b64encode(data).decode()
        else:
            # Data is text, encode it as utf-8 before base64 encoding
            b64_data = base64.b64encode(data.encode('utf-8')).decode()

        href = f"data:{file_extension};base64,{b64_data}"  # creating the href for anchor tag
        link = f'<a id="download_link" href="{href}" download="{filename}">Download Code</a>'  # creating the anchor tag

        # JavaScript code to automatically click the link
        auto_click_js = "<script>document.getElementById('download_link').click();</script>"
        
        if auto_click:
            st.components.v1.html(link + auto_click_js, height=0, scrolling=False)
        else:
            return link  # return the anchor tag
        
    except Exception as e:
        st.toast(traceback.format_exc())
        logging.error(f"Error in code downloading: {traceback.format_exc()}")


def main():
    st.title("Project IGI Compiler - HM")
    initialize_session_state()
    clear_resources('input')

    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        with open(os.path.join('input', uploaded_file.name), 'wb') as file:
            file.write(uploaded_file.getvalue())
        st.session_state.file = uploaded_file.name
    
    if st.form(key='conversion_form'):
        col1,col2,col3,col4 = st.columns(4)
        
        with col1:
            if st.button('Convert'):
                try:
                    st.session_state.output_file = convert_qvm(st.session_state.version)
                    
                    convert_data = None
                    with open(st.session_state.output_file, 'rb') as file:
                        convert_data = file.read()
                    
                    st.session_state.download_link = generate_download_link(convert_data, filename=st.session_state.output_file, auto_click=True)
                
                except Exception as exception:
                    raise Exception("An error occurred while converting the file: " + str(exception))
        
        with col2:
            st.session_state.version = st.number_input('QVM version', min_value=5, max_value=7, step=2)
                     
        with col3:
            if st.button('Decompile'):
                try:
                    st.session_state.output_file = decompile_qvm()
                    
                    with open(st.session_state.output_file, 'rb') as file:
                        st.session_state.code = file.read()
                        
                except Exception as exception:
                    raise Exception("An error occurred while decompiling the file: " + str(exception))
        with col4:
            if st.button('Download'):
                st.session_state.download_link = generate_download_link(st.session_state.code, filename=st.session_state.output_file, auto_click=True)
                import time
                time.sleep(3)
                clear_resources('output')
        
        # Check if input file is uploaded
        if st.session_state.file is None:
            st.toast("Please upload a file.", icon="❌")
            st.error("Please upload a file.")
            clear_resources('input')
            clear_resources('output')
        
        # Display the output.
        if st.session_state.code is not None:
                filename = os.path.basename(st.session_state.output_file)
                with open(os.path.join('output', filename), 'r') as file:
                    st.session_state.code = file.read()
                    st.code(st.session_state.code, language='cpp')
        
if __name__ == "__main__":
    try:
        main()
    except Exception as exception:
        st.error(f'An error occurred: {str(exception)}')
