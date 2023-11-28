import base64
import logging
import traceback
import streamlit as st
import os
from libs.decompile import decompile_qvm
from libs.convert import convert_qvm

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
        try:
            if isinstance(data, bytes):
                # Data is binary, no need to encode it as utf-8
                b64_data = base64.b64encode(data).decode()
            else:
                # Data is text, encode it as utf-8 before base64 encoding
                b64_data = base64.b64encode(data.encode('utf-8')).decode()
        except Exception:
            logging.error(f"Error in encoding data: {traceback.format_exc()}")
        
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


import streamlit as st
import os
import base64
import logging
import traceback
from libs.decompile import decompile_qvm
from libs.convert import convert_qvm

# Other functions like 'initialize_session_state', 'clear_resources', 'generate_download_link' go here

def main():
    st.title("QVM File Handler")
    initialize_session_state()
    clear_resources('input')

    uploaded_file = st.file_uploader("Choose a file", type=['qvm'])
    if uploaded_file is not None:
        with open(os.path.join('input', uploaded_file.name), 'wb') as file:
            file.write(uploaded_file.getvalue())
        st.session_state.file = uploaded_file.name

    with st.form(key='conversion_form'):
        col1, col2,_,col3, col4 = st.columns([2, 2, 1, 2, 2],gap='small')
        
        with col1:
            convert_clicked = st.form_submit_button('Convert')
        
        with col2:
            # Use a placeholder to center the number input
            with st.container():
                st.session_state.version = st.number_input('Version', min_value=5, max_value=7, step=2,label_visibility='collapsed')
        
        with col3:
            decompile_clicked = st.form_submit_button('Decompile')
        
        with col4:
            download_clicked = st.form_submit_button('Download')

    # ... rest of the code ...


    # Conversion process
    if convert_clicked and st.session_state.file is not None:
        try:
            st.session_state.output_file = convert_qvm(st.session_state.version)
            with open(st.session_state.output_file, 'rb') as file:
                convert_data = file.read()
            st.session_state.download_link = generate_download_link(
                convert_data, filename=st.session_state.output_file, auto_click=True
            )
        except Exception as e:
            st.error(f"An error occurred during conversion: {e}")
            logging.error(f"Conversion error: {traceback.format_exc()}")

    # Decompile process
    if decompile_clicked and st.session_state.file is not None:
        try:
            st.session_state.output_file = decompile_qvm()
            with open(st.session_state.output_file, 'r') as file:
                st.session_state.code = file.read()
                
        except Exception as e:
            st.error(f"An error occurred during decompiling: {e}")
            logging.error(f"Decompilation error: {traceback.format_exc()}")

    # Download process
    if download_clicked and st.session_state.code is not None:
        try:
            st.session_state.download_link = generate_download_link(
                st.session_state.code, filename=st.session_state.output_file, auto_click=True
            )
        except Exception as e:
            st.error(f"An error occurred during download: {e}")
            logging.error(f"Download error: {traceback.format_exc()}")

    # Display the output code or conversion success message
    if st.session_state.code is not None:
        st.code(st.session_state.code, language='cpp')
        
    elif "qvm" in st.session_state.output_file and st.session_state.download_link is not None:
        st.success("File converted successfully.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f'An error occurred: {e}')
        logging.error(f"Main function error: {traceback.format_exc()}")

