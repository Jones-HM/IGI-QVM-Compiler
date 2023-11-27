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

def main():
    st.title("Project IGI Compiler")
    initialize_session_state()

    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        with open(os.path.join('input', uploaded_file.name), 'wb') as f:
            f.write(uploaded_file.getvalue())
        st.session_state.file = uploaded_file.name

    st.session_state.operation = st.selectbox('Choose operation', ['Convert QVM', 'Decompile QVM'])
    st.session_state.version = st.number_input('Enter version', min_value=5, max_value=7, step=1)

    if st.button('Execute'):
        if st.session_state.operation == 'Convert QVM':
            try:
                convert_qvm(st.session_state.version)
                st.success('Conversion completed successfully.')
            except Exception as e:
                st.error(f'Error occurred: {str(e)}')
        elif st.session_state.operation == 'Decompile QVM':
            try:
                decompile_qvm()
                st.success('Decompilation completed successfully.')
            except Exception as e:
                st.error(f'Error occurred: {str(e)}')

        output_file = st.session_state.file.replace('.qvm', '.qsc')
        with open(os.path.join('output', output_file), 'r') as f:
            code = f.read()
        st.code(code, language='cpp')

if __name__ == "__main__":
    main()