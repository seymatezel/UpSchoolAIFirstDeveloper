# rag/rag_module.py (DÜZELTİLMİŞ HALİ)

import streamlit as st
import os
import tempfile
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document

# <<< DEĞİŞİKLİK BURADA: st.cache_data yerine st.cache_resource kullanıldı.
@st.cache_resource(show_spinner="RAG zinciri oluşturuluyor...")
def create_rag_chain(document_input, api_key: str):
    """
    Yüklenen bir PDF dosyasını VEYA doğrudan metni alır, işler ve 
    bir soru-cevap (RAG) zinciri oluşturur. Bu fonksiyon, serileştirilemeyen
    kaynakları (LLM, retriever vb.) önbelleğe alır.
    """
    # Gerekli girdilerin olup olmadığını kontrol et
    if document_input is None:
        st.error("Lütfen bir belge yükleyin veya metin girin.")
        return None
    if not api_key:
        st.error("Lütfen Google API anahtarınızı girin.")
        return None

    # Girdinin dosya mı yoksa metin mi olduğunu kontrol et
    # hasattr(document_input, 'getvalue') kontrolü bir Streamlit UploadedFile nesnesi için çalışır.
    if hasattr(document_input, 'getvalue'): 
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(document_input.getvalue())
                tmp_file_path = tmp_file.name
            
            loader = PyPDFLoader(file_path=tmp_file_path)
            documents = loader.load_and_split() # Yükleme ve bölmeyi birleştirebiliriz
        finally:
            # Geçici dosyayı her zaman sil
            os.remove(tmp_file_path)
    
    # Girdinin metin olup olmadığını kontrol et
    elif isinstance(document_input, str) and document_input.strip(): 
        documents = [Document(page_content=document_input)]
        
    else:
        # Geçersiz girdi durumu
        return None

    try:
        # Metinleri parçalara ayır
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        text_chunks = text_splitter.split_documents(documents)

        # Eğer hiç metin parçası oluşmadıysa, hata ver
        if not text_chunks:
            st.warning("Belgeden işlenecek metin bulunamadı. Lütfen belgenin içeriğini kontrol edin.")
            return None

        # Gömme (embedding) modelini ve vektör veritabanını oluştur
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
        vector_store = Chroma.from_documents(documents=text_chunks, embedding=embeddings)
        
        # LLM modelini oluştur
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key, temperature=0.7)
        
        # RetrievalQA zincirini oluştur
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
            return_source_documents=True
        )
        return qa_chain

    except Exception as e:
        # API anahtarı hatası veya başka bir LangChain hatası durumunda kullanıcıya bilgi ver
        st.error(f"RAG zinciri oluşturulurken bir hata oluştu: {e}")
        return None