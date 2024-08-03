import streamlit as st
from pathlib import Path
from time import sleep
from langchain.memory import ConversationBufferMemory


st.set_page_config(page_title="ChatBot PDF", layout="wide")

FILES_DIR = Path(__name__).parent / 'files'


def cria_chain_conversa():
    st.session_state['chain'] = True
    
    memory = ConversationBufferMemory(return_messages=True)
    memory.chat_memory.add_user_message('Oi')
    memory.chat_memory.add_ai_message('Oi, eu sou uma LLM')
    
    st.session_state['memory'] = memory
    sleep(1)
    pass



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


def chat_window():
    st.header("Welcome to RAG ChatBot", divider=True)
    if not 'chain' in st.session_state:
        st.warning('Faça o upload de PDFs para começar')
        st.stop()
    
    # chain = st.session_state['chain']
    # memory = chain.memory
    
    memory = st.session_state['memory']
    mensagens = memory.load_memory_variables({})['history']
    
    container = st.container()
    for mensagem in mensagens:
        chat = container.chat_message(mensagem.type)
        chat.markdown(mensagem.content)
    
    nova_mensagem = st.chat_input('Converse com os seus documentos...')
    if nova_mensagem:
        chat = container.chat_message('human')
        chat.markdown(nova_mensagem)
        chat = container.chat_message('ai')
        chat.markdown('Gerando resposta')
        sleep(2)
        memory.chat_memory.add_user_message(nova_mensagem)
        memory.chat_memory.add_ai_message('Oi, é a LLM aqui novamente')
        st.rerun()
    

def main():
    with st.sidebar:
        sidebar()
    chat_window()


if __name__ == '__main__':
    main()
