import streamlit as st
import os
import tempfile
import pandas as pd
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Configuración de interfaz en modo oscuro
st.set_page_config(page_title="Mercado Central 24h - Asistente IA", layout="wide", page_icon="🛒")

st.markdown("""
    <style>
    .main { background-color: #0d1117; color: #ffffff; }
    .stApp { background-color: #0f141c; }
    div[data-testid="stSidebar"] { background-color: #161b22; }
    .stChatMessage { border-radius: 12px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# ----------------- BARRA LATERAL -----------------
with st.sidebar:
    st.title("⚙️ Configuración & Archivos")
    
    # Selector de Proveedor de LLM
    proveedor = st.selectbox(
        "Proveedor de IA",
        ["Google Gemini", "Groq", "OpenRouter"]
    )
    
    # Campo dinamico para API Key y Selección de Modelos
    if proveedor == "Google Gemini":
        api_key = st.text_input("Gemini API Key", type="password")
        modelo_seleccionado = st.selectbox("Modelo", ["gemini-2.0-flash", "gemini-1.5-flash"])
    elif proveedor == "Groq":
        api_key = st.text_input("Groq API Key (console.groq.com)", type="password")
        modelo_seleccionado = st.selectbox("Modelo", ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"])
    elif proveedor == "OpenRouter":
        api_key = st.text_input("OpenRouter API Key (openrouter.ai)", type="password")
        modelo_seleccionado = st.selectbox("Modelo", ["meta-llama/llama-3.3-70b-instruct:free", "google/gemini-2.0-flash-exp:free", "deepseek/deepseek-r1:free"])

    st.markdown("---")
    
    st.subheader("📂 Cargar Documentos")
    uploaded_files = st.file_uploader(
        "Sube tus archivos (PDF o Excel)", 
        type=["pdf", "xlsx", "xls"], 
        accept_multiple_files=True
    )
    
    procesar_btn = st.button("🚀 Procesar Documentos")

    st.markdown("---")
    st.subheader("💡 Preguntas Frecuentes")
    st.markdown("""
    * ¿Cuál es el plazo para devoluciones?
    * ¿En qué pasillo está el Arroz Blanco?
    * ¿Cuántos días de vacaciones corresponden?
    * ¿A qué temperatura están las cámaras frías?
    """)

# ----------------- PROCESAMIENTO RAG -----------------
@st.cache_resource(show_spinner=False)
def inicializar_embeddings():
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if procesar_btn and uploaded_files and api_key:
    with st.spinner("Procesando y vectorizando documentos..."):
        docs = []
        for file in uploaded_files:
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.name)[1]) as tmp:
                tmp.write(file.getvalue())
                tmp_path = tmp.name

            # Procesar PDF
            if file.name.endswith(".pdf"):
                loader = PyPDFLoader(tmp_path)
                docs.extend(loader.load())
                
            # Procesar Excel con pandas
            elif file.name.endswith((".xlsx", ".xls")):
                excel_data = pd.read_excel(tmp_path, sheet_name=None)
                for sheet_name, df in excel_data.items():
                    texto_tabla = df.to_string(index=False)
                    doc = Document(
                        page_content=f"Hoja de inventario ({sheet_name}):\n\n{texto_tabla}",
                        metadata={"source": file.name, "sheet": sheet_name}
                    )
                    docs.append(doc)
            
            os.remove(tmp_path)

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
        chunks = text_splitter.split_documents(docs)
        
        embeddings = inicializar_embeddings()
        st.session_state.vectorstore = Chroma.from_documents(chunks, embeddings)
        st.success("¡Base de conocimientos actualizada con éxito!")

# ----------------- INTERFAZ DE CHAT -----------------
st.title("🛒 Mercado Central 24h - Asistente IA")
st.caption("Pregunta tus dudas sobre políticas, inventario, RRHH y seguridad del supermercado.")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "¡Hola! Soy tu asistente virtual de Mercado Central 24h. Carga tus documentos en la barra lateral para empezar a consultar."}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt_input := st.chat_input("Ingresa tu pregunta aquí..."):
    if not api_key:
        st.error("Por favor ingresa la API Key en la barra lateral.")
    elif not st.session_state.vectorstore:
        st.warning("Por favor sube tus documentos y haz clic en 'Procesar Documentos'.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt_input})
        st.chat_message("user").write(prompt_input)

        retriever = st.session_state.vectorstore.as_retriever(search_kwargs={"k": 3})
        
        # Inicialización del modelo según proveedor seleccionado
        if proveedor == "Google Gemini":
            os.environ["GOOGLE_API_KEY"] = api_key
            llm = ChatGoogleGenerativeAI(model=modelo_seleccionado, temperature=0)
            
        elif proveedor == "Groq":
            llm = ChatOpenAI(
                model_name=modelo_seleccionado,
                openai_api_key=api_key,
                openai_api_base="https://api.groq.com/openai/v1",
                temperature=0
            )
            
        elif proveedor == "OpenRouter":
            llm = ChatOpenAI(
                model_name=modelo_seleccionado,
                openai_api_key=api_key,
                openai_api_base="https://openrouter.ai/api/v1",
                temperature=0,
                default_headers={
                    "HTTP-Referer": "https://localhost:8501",
                    "X-Title": "Mercado Central 24h Assistant"
                }
            )

        sys_prompt = (
            "Eres un asistente virtual experto del supermercado Mercado Central 24h.\n"
            "Responde únicamente usando la información del contexto proporcionado.\n"
            "Sé conciso y directo (máximo 2-3 oraciones).\n\n"
            "Contexto:\n{context}\n\n"
            "Pregunta: {question}"
        )
        prompt_template = ChatPromptTemplate.from_template(sys_prompt)

        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt_template
            | llm
            | StrOutputParser()
        )

        with st.chat_message("assistant"):
            with st.spinner("Buscando en la base de conocimientos..."):
                try:
                    respuesta = rag_chain.invoke(prompt_input)
                    st.write(respuesta)
                    st.session_state.messages.append({"role": "assistant", "content": respuesta})
                except Exception as e:
                    if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e) or "rate_limit" in str(e).lower():
                        st.error("⏳ Has alcanzado el límite de consultas por minuto de la API seleccionada. Espera un momento e inténtalo de nuevo o cambia de proveedor.")
                    else:
                        st.error(f"Ocurrió un error con el proveedor: {e}")
