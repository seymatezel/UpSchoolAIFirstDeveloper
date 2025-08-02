# rag/rag_module.py dosyasının GÜNCELLENMİŞ içeriği

import os
import tempfile
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document

def create_rag_chain(document_input, api_key: str):
    """
    Yüklenen bir PDF dosyasını VEYA doğrudan metni alır, işler ve 
    bir soru-cevap (RAG) zinciri oluşturur.
    """
    if document_input is None or api_key is None:
        return None

    # Girdinin dosya mı yoksa metin mi olduğunu kontrol et
    if hasattr(document_input, 'getvalue'): # Bu bir Streamlit UploadedFile nesnesi
        # Dosyayı geçici olarak diske yaz
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(document_input.getvalue())
            tmp_file_path = tmp_file.name
        
        loader = PyPDFLoader(file_path=tmp_file_path)
        documents = loader.load()
        os.remove(tmp_file_path) # Geçici dosyayı sil
    
    elif isinstance(document_input, str): # Bu bir metin (string)
        # Metni LangChain'in anlayacağı Document formatına çevir
        documents = [Document(page_content=document_input)]
        
    else:
        return None # Desteklenmeyen format

    try:
        # 2. Belgeyi Parçalara Ayır (Chunking)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        text_chunks = text_splitter.split_documents(documents)

        # 3. Embedding Modelini Oluştur (Google)
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)

        # 4. Vector Database Oluştur ve Doldur (ChromaDB)
        vector_store = Chroma.from_documents(documents=text_chunks, embedding=embeddings)

        # 5. LLM'i ve Soru-Cevap Zincirini Oluştur
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key, temperature=0.7)
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
            return_source_documents=True
        )
        return qa_chain

    except Exception as e:
        print(f"Hata oluştu: {e}")
        return None