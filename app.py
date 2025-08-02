# YENİ VE TAM app.py KODU

import streamlit as st
import os
from dotenv import load_dotenv
import time 
import PyPDF2 as pdf
from docx import Document

# Agent'larımızı ve RAG modülümüzü projemize dahil ediyoruz
from agents.swot_agent import get_swot_analysis
from agents.career_agent import get_career_paths
from agents.plan_agent import get_learning_plan
from rag.rag_module import create_rag_chain

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(
    page_title="AI Kariyer Koçu",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ÖZEL CSS İLE GÖRSELLEŞTİRME (KOYU TEMA ODAKLI) ---
st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: #FAFAFA; }
    [data-testid="stSidebar"] { background-color: #1a1c24; border-right: 1px solid #2c2f3b; }
    .st-emotion-cache-1r4qj8v, .st-emotion-cache-1jicfl2 { border: 1px solid #2c2f3b; border-radius: 10px; padding: 25px !important; background-color: #161a21; box-shadow: 0 4px 12px rgba(0,0,0,0.3); transition: transform 0.2s ease-in-out; }
    .st-emotion-cache-1r4qj8v:hover { transform: translateY(-5px); border-color: #4CAF50; }
    .stButton>button { border-radius: 8px; border: 1px solid #4CAF50; background-color: transparent; color: #4CAF50; font-weight: bold; transition: all 0.2s ease-in-out; }
    .stButton>button:hover { background-color: #4CAF50; color: white; transform: scale(1.05); }
    .stButton>button:focus { outline: none !important; box-shadow: 0 0 0 2px #0E1117, 0 0 0 4px #4CAF50 !important; }
    h1, h2, h3 { color: #FFFFFF; }
    .st-emotion-cache-1vbkxwb p { font-size: 1.1rem; }
</style>
""", unsafe_allow_html=True)

# .env dosyasındaki API anahtarını yükle
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# --- HAFIZA (SESSION STATE) ---
# Mevcut durum ve analiz sonuçlarını saklamak için
if 'swot' not in st.session_state: st.session_state.swot = None
if 'career' not in st.session_state: st.session_state.career = None
if 'plan' not in st.session_state: st.session_state.plan = None
if 'cv_text' not in st.session_state: st.session_state.cv_text = ""
if 'qa_chain' not in st.session_state: st.session_state.qa_chain = None
if 'interview_history' not in st.session_state: st.session_state.interview_history = []
if 'interview_started' not in st.session_state: st.session_state.interview_started = False
if 'processed_file_id' not in st.session_state: st.session_state.processed_file_id = None
if 'processed_text' not in st.session_state: st.session_state.processed_text = None

# --- DOSYA OKUMA FONKSİYONLARI ---
def get_pdf_text(uploaded_file):
    try:
        pdf_reader = pdf.PdfReader(uploaded_file)
        return "".join(page.extract_text() for page in pdf_reader.pages)
    except Exception as e:
        st.error(f"PDF okunurken hata: {e}")
        return None

def get_docx_text(uploaded_file):
    try:
        document = Document(uploaded_file)
        return "\n".join([para.text for para in document.paragraphs])
    except Exception as e:
        st.error(f"Word dosyası okunurken hata: {e}")
        return None

# --- KENAR ÇUBUĞU (SIDEBAR) ---
with st.sidebar:
    st.image("https://www.gstatic.com/a/ads/images/logo_gemini_2023_1x_dark_e72a0f5a7e64a135bd1850757e796839.png", width=150)
    st.title("AI Kariyer Koçu")
    st.markdown("---")
    st.subheader("1. CV'nizi Girin")
    st.info("Tüm analizler, burada girdiğiniz CV'ye göre kişiselleştirilecektir.")

    cv_tab1, cv_tab2 = st.tabs(["📄 Yükle", "✍️ Yapıştır"])

    with cv_tab1:
        uploaded_file = st.file_uploader("PDF veya DOCX formatında yükleyin", type=["pdf", "docx"], label_visibility="collapsed", key="cv_uploader")
        if uploaded_file:
            if uploaded_file.type == "application/pdf": st.session_state.cv_text = get_pdf_text(uploaded_file)
            else: st.session_state.cv_text = get_docx_text(uploaded_file)
            st.rerun()
            
    with cv_tab2:
        text_input = st.text_area("CV metninizi buraya yapıştırın", height=250, label_visibility="collapsed")
        if st.button("Bu Metni Kullan", use_container_width=True, key="cv_text_submit"):
            if text_input:
                st.session_state.cv_text = text_input
                st.rerun()
            else:
                st.warning("Lütfen metin girin.")
    
    if st.session_state.cv_text:
        st.markdown("---")
        st.success("✅ CV Analize Hazır!")
        with st.expander("CV Metnini Görüntüle"):
            st.text(st.session_state.cv_text[:500] + "...")
        
        if st.button("Yeni Analiz Başlat (Sıfırla)", use_container_width=True):
            for key in list(st.session_state.keys()): del st.session_state[key]
            st.rerun()

# --- ANA EKRAN ---
st.title("AI Destekli Kariyer Analiz Panosu")

if not st.session_state.cv_text:
    st.info("⬅️ Lütfen analizi başlatmak için sol menüden CV'nizi girin.")
    st.stop()

tab_pano, tab_swot, tab_career, tab_plan, tab_rag = st.tabs(["📊 Pano", "SWOT Analizi", "Kariyer Yolları", "Öğrenme Planı", "🚀 Mülakat Simülatörü"])

with tab_pano:
    st.header("📊 Kontrol Panosu")
    st.write("Hoş geldin! CV'niz analiz için hazır. Aşağıdaki modülleri kullanarak kariyer yolculuğunuza başlayabilirsiniz.")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        with st.container():
            st.subheader("🎯 SWOT Analizi")
            st.write("Güçlü ve gelişime açık yönlerinizi, fırsatları ve tehditleri keşfedin.")
            if st.button("SWOT Analizi Yap", use_container_width=True, key="swot_btn"):
                with st.spinner("Kişilik ve yetenekleriniz analiz ediliyor..."):
                    st.session_state.swot = get_swot_analysis(st.session_state.cv_text, GOOGLE_API_KEY)
                st.success("SWOT analizi tamamlandı!")
                st.balloons()
    
    with col2:
        with st.container():
            st.subheader("🧭 Kariyer Yolları")
            st.write("CV'nize en uygun potansiyel kariyer yollarını ve unvanları öğrenin.")
            if st.button("Kariyer Yolları Öner", use_container_width=True, key="career_btn"):
                with st.spinner("Potansiyelinizle eşleşen kariyerler bulunuyor..."):
                    st.session_state.career = get_career_paths(st.session_state.cv_text, GOOGLE_API_KEY)
                st.success("Kariyer önerileri hazır!")

    with col3:
        with st.container():
            st.subheader("🗺️ Öğrenme Planı")
            st.write("Belirlediğiniz bir kariyer hedefi için size özel bir yol haritası oluşturun.")
            chosen_career = st.text_input("Hedeflediğiniz kariyeri yazın:", key="career_input")
            if st.button("Öğrenme Planı Oluştur", use_container_width=True, key="plan_btn"):
                if chosen_career:
                    with st.spinner(f"'{chosen_career}' için kişisel yol haritanız çiziliyor..."):
                        st.session_state.plan = get_learning_plan(st.session_state.cv_text, chosen_career, GOOGLE_API_KEY)
                    st.success("Öğrenme planınız hazır!")
                else:
                    st.warning("Lütfen bir kariyer alanı girin.")

with tab_swot:
    st.header("🎯 SWOT Analiziniz")
    if st.session_state.swot: st.markdown(st.session_state.swot)
    else: st.info("SWOT analizi sonucunu görmek için 'Pano' sekmesindeki ilgili butona tıklayın.")

with tab_career:
    st.header("🧭 Size Özel Kariyer Yolları")
    if st.session_state.career: st.markdown(st.session_state.career)
    else: st.info("Kariyer yolu önerilerini görmek için 'Pano' sekmesindeki ilgili butona tıklayın.")

with tab_plan:
    st.header("🗺️ Kişisel Öğrenme Planınız")
    if st.session_state.plan: st.markdown(st.session_state.plan)
    else: st.info("Öğrenme planını görmek için 'Pano' sekmesinde bir kariyer seçip ilgili butona tıklayın.")

with tab_rag:
    st.header("🚀 Etkileşimli Mülakat Simülatörü")
    st.write("Başvurmak istediğiniz pozisyonun iş ilanını yükleyin veya yapıştırın ve o ilana özel bir mülakat deneyimi yaşayın.")
    st.markdown("---")
    
    should_create_chain = False
    input_data = None
    
    input_tab1, input_tab2 = st.tabs(["📄 PDF Yükle", "✍️ Metin Yapıştır"])

    with input_tab1:
        rag_uploaded_file = st.file_uploader("İş ilanı PDF'ini buraya yükleyin", type="pdf", key="interview_pdf_uploader")
        if rag_uploaded_file and st.session_state.processed_file_id != rag_uploaded_file.file_id:
            should_create_chain = True
            input_data = rag_uploaded_file
            st.session_state.processed_file_id = rag_uploaded_file.file_id

    with input_tab2:
        job_ad_text = st.text_area("İş ilanı metnini buraya yapıştırın", height=250, key="job_ad_text")
        if st.button("Bu Metni Analiz Et", use_container_width=True, key="job_text_submit"):
            if job_ad_text and st.session_state.processed_text != job_ad_text:
                should_create_chain = True
                input_data = job_ad_text
                st.session_state.processed_text = job_ad_text

    if should_create_chain:
        with st.spinner("İş ilanı analiz ediliyor ve mülakat hazırlanıyor..."):
            st.session_state.qa_chain = create_rag_chain(input_data, GOOGLE_API_KEY)
            st.session_state.interview_started = False
            st.session_state.interview_history = []
        if st.session_state.qa_chain: st.success("İlan analiz edildi! Simülasyonu başlatmaya hazırsın.")
        else: st.error("İlan işlenirken bir sorun oluştu.")
        st.rerun()
    
    if st.session_state.get('qa_chain') is not None:
        if not st.session_state.interview_started:
            if st.button("Mülakat Simülasyonunu Başlat", use_container_width=True):
                st.session_state.interview_started = True
                st.session_state.interview_history = []
                st.rerun()

        if st.session_state.interview_started:
            if not st.session_state.interview_history:
                with st.spinner("İlk mülakat sorusu hazırlanıyor..."):
                    initial_prompt = "Sen deneyimli bir işe alım yöneticisisin. Sana verdiğim iş ilanı metnini kullanarak bir mülakat simülasyonu başlat. İlk görevin, ilandaki en önemli teknik veya sosyal yetkinliğe odaklanan, adayın yeteneklerini ölçmeye yönelik yaratıcı ve açık uçlu bir soru sormak. Sadece soruyu sor, başka bir şey söyleme."
                    response = st.session_state.qa_chain({"query": initial_prompt})
                    if response: st.session_state.interview_history.append({"role": "assistant", "content": response['result']})
                    st.rerun()
            
            for message in st.session_state.interview_history:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            if user_answer := st.chat_input("Cevabınızı buraya yazın..."):
                st.session_state.interview_history.append({"role": "user", "content": user_answer})
                with st.spinner("Cevabınız değerlendiriliyor ve yeni soru hazırlanıyor..."):
                    follow_up_prompt = f"Sen deneyimli bir işe alım yöneticisisin ve bir mülakat simülasyonu yapıyorsun. Sana verdiğim iş ilanı metnini ve adayın son cevabını dikkate alarak şu iki adımı uygula: 1. Geri Bildirim Ver: Adayın '{user_answer}' cevabını kısaca değerlendir. (Örn: 'Harika bir örnek. Bu projenin sonuçlarını rakamlarla ifade etseydiniz daha da etkili olurdu.') 2. Yeni Soru Sor: İlandaki FARKLI bir yetkinliği ölçmek için yeni bir soruya geç. Tüm bu cevabını tek bir paragraf olarak sun. İşte tüm konuşma geçmişi ve en altta adayın son cevabı: {st.session_state.interview_history}"
                    response = st.session_state.qa_chain({"query": follow_up_prompt})
                    if response: st.session_state.interview_history.append({"role": "assistant", "content": response['result']})
                st.rerun()
    else:
        st.info("Lütfen başlamak için bir iş ilanı yükleyin veya metnini yapıştırın.")