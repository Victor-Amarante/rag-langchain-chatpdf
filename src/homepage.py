import streamlit as st
from pathlib import Path
from time import sleep


FILES_DIR = Path(__name__).parent / 'files'


def cria_chain_conversa():
    st.session_state['chain'] = True
    sleep(1)

def sidebar():
    uploaded_pdfs = st.file_uploader('Selecione os arquivos PDF',
                     type=['.PDF'],
                     accept_multiple_files=True)
    if not uploaded_pdfs is None:
        for file in FILES_DIR.glob('*.pdf'):
            file.unlink() # delete all files
        for pdf in uploaded_pdfs:
            with open(FILES_DIR / pdf.name, 'wb') as f:
                f.write(pdf.read())
                
    button_label = 'Start ChatBot'
    if 'chain' in st.session_state:
        button_label = 'Update ChatBot'
    if st.button(button_label, use_container_width=True):
        if len(list(FILES_DIR.glob('*.pdf'))) == 0:
            st.error('Adicione arquivos .pdf para inicializar o chatbot')
        else:
            st.success('Initializing the ChatBot...')
            cria_chain_conversa()
            st.rerun()


def main():
    with st.sidebar:
        sidebar()


if __name__ == '__main__':
    main()
