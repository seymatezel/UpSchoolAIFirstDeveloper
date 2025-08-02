# ----------------------------------------------------
# AI KARİYER KOÇU - V4 (Gelişmiş Arayüz ve Prompt'lar)
# ----------------------------------------------------
import streamlit as st
import os
from dotenv import load_dotenv
import time 
import PyPDF2 as pdf
from docx import Document

# ... import satırlarından sonra ...

st.set_page_config(page_title="AI Kariyer Koçu", page_icon="🚀", layout="wide")

# --- ÖZEL CSS İLE GÖRSELLEŞTİRME ---
st.markdown("""
<style>
    /* Ana arkaplan ve metin renkleri */
    .stApp {
        background-color: #f0f2f6;
    }
    /* Kart (container) stili */
    .st-emotion-cache-1r4qj8v {
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 20px;
        background-color: white;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    .st-emotion-cache-1r4qj8v:hover {
        transform: scale(1.02);
    }
    /* Buton stili */
    .stButton>button {
        border-radius: 20px;
        border: 1px solid #4CAF50;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45a049;
        border-color: #45a049;
    }
</style>
""", unsafe_allow_html=True)

# ... (kodun geri kalanı) ...

# Agent'larımızı projemize dahil ediyoruz
from agents.swot_agent import get_swot_analysis
from agents.career_agent import get_career_paths
from agents.plan_agent import get_learning_plan

# ----------------------------------------------------
# TEMEL AYARLAR VE FONKSİYONLAR
# ----------------------------------------------------
st.set_page_config(page_title="AI Kariyer Koçu", page_icon="🚀", layout="wide")

# .env dosyasındaki API anahtarını yükle
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# --- Hafıza (Session State) ---
# Analiz sonuçlarını sekmeler arasında geçiş yaparken kaybetmemek için hafıza kullanıyoruz.
if 'swot' not in st.session_state:
    st.session_state.swot = None
if 'career' not in st.session_state:
    st.session_state.career = None
if 'plan' not in st.session_state:
    st.session_state.plan = None
if 'cv_text' not in st.session_state:
    st.session_state.cv_text = ""

# --- Dosya Okuma Fonksiyonları ---
def get_pdf_text(uploaded_file):
    try:
        pdf_reader = pdf.PdfReader(uploaded_file)
        text = "".join(page.extract_text() for page in pdf_reader.pages)
        return text
    except Exception:
        st.error("PDF okunurken bir hata oluştu. Lütfen dosyanın bozuk olmadığını kontrol edin.")
        return None

def get_docx_text(uploaded_file):
    try:
        document = Document(uploaded_file)
        return "\n".join([para.text for para in document.paragraphs])
    except Exception:
        st.error("Word dosyası okunurken bir hata oluştu.")
        return None

# ----------------------------------------------------
# ARAYÜZ (UI) - KENAR ÇUBUĞU (SIDEBAR)
# ----------------------------------------------------
with st.sidebar:
    st.image("https://www.gstatic.com/a/ads/images/logo_gemini_2023_1x_dark_e72a0f5a7e64a135bd1850757e796839.png", width=150)
    st.header("🚀 Kariyerinizi Başlatın")
    st.write("Analizi başlatmak için CV'nizi girin.")

    # Sekmeli yapı ile CV girişi
    tab1, tab2 = st.tabs(["📄 Dosya Yükle", "✍️ Metin Yapıştır"])

    with tab1:
        uploaded_file = st.file_uploader("PDF veya DOCX formatında yükleyin", type=["pdf", "docx"], label_visibility="collapsed")
        if uploaded_file:
            if uploaded_file.type == "application/pdf":
                st.session_state.cv_text = get_pdf_text(uploaded_file)
            else:
                st.session_state.cv_text = get_docx_text(uploaded_file)
            
            # Dosya yüklendiğinde otomatik olarak yeniden çalıştırarak ana ekranı güncelle
            st.rerun()
            
    with tab2:
        text_input = st.text_area("CV metninizi buraya yapıştırın", height=250, label_visibility="collapsed")
        # YENİ BUTON: Kullanıcı metni girdikten sonra bu butona basacak
        if st.button("Bu Metni Analiz Et", use_container_width=True):
            if text_input:
                st.session_state.cv_text = text_input
                # Butona basıldığında ana ekranı güncellemek için yeniden çalıştır
                st.rerun()
            else:
                st.warning("Lütfen önce metin alanını doldurun.")
    
    if st.session_state.cv_text:
        st.success("CV'niz analiz için hazır!")
        if st.button("Yeni CV Analiz Et", use_container_width=True):
            # Hafızayı temizle ve yeniden başlat
            for key in st.session_state.keys():
                st.session_state[key] = None
            st.rerun()

# ----------------------------------------------------
# ARAYÜZ (UI) - ANA EKRAN
# ----------------------------------------------------
st.title("AI Destekli Kariyer Analiz Panosu")

# CV girilmediyse, kullanıcıyı yönlendir
if not st.session_state.cv_text:
    st.info("⬅️ Lütfen analizi başlatmak için sol menüden CV'nizi girin.")
    st.stop()

# CV girildiyse, analiz sekmelerini göster
tab_pano, tab_swot, tab_career, tab_plan = st.tabs(["📊 Pano", "SWOT Analizi", "Kariyer Yolları", "Öğrenme Planı"])

with tab_pano:
    st.header("Kontrol Merkeziniz")
    st.write("Aşağıdaki butonları kullanarak analizleri başlatabilir ve sonuçları ilgili sekmelerde görüntüleyebilirsiniz.")

    # --- MANUEL AGENT ÇAĞIRMA ---
    st.subheader("Adım Adım Analiz")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("SWOT Analizi Yap", use_container_width=True):
            with st.spinner("Kişilik ve yetenekleriniz analiz ediliyor..."):
                st.session_state.swot = get_swot_analysis(st.session_state.cv_text, GOOGLE_API_KEY)
            st.success("SWOT analizi tamamlandı! Sonucu 'SWOT Analizi' sekmesinde görebilirsiniz.")
    with col2:
        if st.button("Kariyer Yolları Öner", use_container_width=True):
            with st.spinner("Potansiyelinizle eşleşen kariyerler bulunuyor..."):
                st.session_state.career = get_career_paths(st.session_state.cv_text, GOOGLE_API_KEY)
            st.success("Kariyer önerileri hazır! 'Kariyer Yolları' sekmesine göz atın.")

    # --- ÖĞRENME PLANI ---
    st.subheader("Öğrenme Planı Oluşturma")
    chosen_career = st.text_input("Gelişim yol haritası istediğiniz kariyeri yazın:")
    if st.button("Bu Kariyer İçin Öğrenme Planı Oluştur", use_container_width=True):
        if chosen_career:
            with st.spinner(f"'{chosen_career}' için kişisel yol haritanız çiziliyor..."):
                st.session_state.plan = get_learning_plan(st.session_state.cv_text, chosen_career, GOOGLE_API_KEY)
            st.success(f"Öğrenme planınız hazır! 'Öğrenme Planı' sekmesinde bulabilirsiniz.")
        else:
            st.warning("Lütfen bir kariyer alanı girin.")

with tab_swot:
    st.header("🎯 SWOT Analiziniz")
    if st.session_state.swot:
        # SWOT analizini 4 ayrı sütunda, kartlar içinde gösterelim
        # Önce metni başlıklara göre ayırmamız gerekiyor (basit bir varsayım yapıyoruz)
        try:
            parts = st.session_state.swot.split("###")
            strengths = parts[1]
            weaknesses = parts[2]
            opportunities = parts[3]
            threats = parts[4]

            col1, col2 = st.columns(2)
            with col1:
                with st.container():
                    st.subheader("👍 Güçlü Yönler")
                    st.markdown(strengths.split(")", 1)[1]) # Başlığı atmak için
            with col2:
                with st.container():
                    st.subheader("💪 Gelişim Fırsatları")
                    st.markdown(weaknesses.split(")", 1)[1])
            
            col3, col4 = st.columns(2)
            with col3:
                with st.container():
                    st.subheader("✨ Fırsatlar")
                    st.markdown(opportunities.split(")", 1)[1])
            with col4:
                with st.container():
                    st.subheader("🤔 Dikkate Alınması Gerekenler")
                    st.markdown(threats.split(")", 1)[1])

        except Exception:
            # Eğer ayırma başarısız olursa, metni olduğu gibi göster
            st.markdown(st.session_state.swot)
    else:
        st.info("SWOT analizi sonucunu görmek için 'Pano' sekmesindeki ilgili butona tıklayın.")

# Mevcut tab_career bloğunu silip bunu yapıştırın:
with tab_career:
    st.header("🧭 Size Özel Kariyer Yolları")
    if st.session_state.career:
        # Her bir kariyer yolunu ayrı bir kart içinde göster
        try:
            paths = st.session_state.career.split("---")
            for path in paths:
                if "Kariyer Yolu Önerisi" in path:
                    with st.container():
                        st.markdown(path)
        except Exception:
            st.markdown(st.session_state.career)
    else:
        st.info("Kariyer yolu önerilerini görmek için 'Pano' sekmesindeki ilgili butona tıklayın.")

# Mevcut tab_plan bloğunu silip bunu yapıştırın:
with tab_plan:
    st.header("🗺️ Kişisel Öğrenme Planınız")
    if st.session_state.plan:
        # Öğrenme planını açılır/kapanır bölümlerde göster
        try:
            # Metni '####' başlıklarına göre böl
            sections = st.session_state.plan.split("####")
            st.markdown(sections[0]) # Giriş metnini yazdır
            
            for section in sections[1:]:
                # Her bir seviye başlığını expander'ın başlığı yap
                title = section.split("\n")[0]
                content = "\n".join(section.split("\n")[1:])
                with st.expander(f"**{title}**"):
                    st.markdown(content)
        except Exception:
            st.markdown(st.session_state.plan)
    else:
        st.info("Öğrenme planını görmek için 'Pano' sekmesinde bir kariyer seçip ilgili butona tıklayın.")