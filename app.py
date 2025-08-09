# TAM VE GÜNCEL APP.PY KODU - Performans Optimize Edilmiş Versiyon

import streamlit as st
import os
from dotenv import load_dotenv
import time 
import PyPDF2 as pdf
from docx import Document
import re

# Agent'larımızı ve RAG modülümüzü projemize dahil ediyoruz
from agents.swot_agent import get_swot_analysis
from agents.career_agent import get_career_paths
from agents.plan_agent import get_learning_plan
from rag.rag_module import create_rag_chain

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(
    page_title="AI Kariyer Rehberiniz",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- PERFORMANS İYİLEŞTİRMESİ: CSS'i cache'le ---
@st.cache_data
def get_custom_css():
    return """
<style>
    /* Ana arka plan - bej */
    .stApp { 
        background-color: #F5F5DC; 
        color: #1A1A1A; 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Sidebar - açık bej tonu */
    [data-testid="stSidebar"] { 
        background-color: #FAF0E6; 
        border-right: 2px solid #E6E6FA; 
    }
    
    /* Ana konteynerler - turuncu tonları */
    .st-emotion-cache-1r4qj8v, 
    .st-emotion-cache-1jicfl2,
    div[data-testid="column"] > div {
        border: 2px solid #FFB366; border-radius: 15px; padding: 25px !important;
        background-color: #FDFCFF; box-shadow: 0 6px 20px rgba(255, 179, 102, 0.3);
        transition: all 0.3s ease-in-out; margin: 10px 0;
    }
    
    /* Hover efektleri */
    .st-emotion-cache-1r4qj8v:hover,
    .st-emotion-cache-1jicfl2:hover {
        transform: translateY(-3px); border-color: #FF9B73;
        box-shadow: 0 8px 25px rgba(255, 155, 115, 0.4);
    }
    
    /* Butonlar */
    .stButton > button {
        border-radius: 12px; border: 2px solid #FF9B73; background-color: #FF9B73;
        color: #1A1A1A; font-weight: 700; font-size: 1rem; padding: 12px 24px;
        transition: all 0.3s ease-in-out; box-shadow: 0 4px 12px rgba(255, 155, 115, 0.3);
    }
    
    .stButton > button:hover {
        background-color: #FF7F50; color: #FFFFFF; transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(255, 127, 80, 0.4);
    }
    
    .stButton > button:active, .stButton > button:focus {
        background-color: #FF7F50 !important; color: #FFFFFF !important;
        outline: none !important; box-shadow: 0 0 0 3px #F5F5DC, 0 0 0 6px #FF9B73 !important;
        border: 2px solid #FF9B73 !important;
    }
    
    /* Başlıklar */
    h1, h2, h3, h4 { color: #2C2C2C !important; font-weight: 700; }
    h1 { border-bottom: 3px solid #FF9B73; padding-bottom: 10px; color: #1A1A1A !important; }
    
    /* BİLDİRİM MESAJLARI */
    .stInfo > div { background-color: #E7F3FF !important; color: #00529B !important; border: 2px solid #BDE5F8 !important; border-radius: 10px; font-weight: 600; }
    .stSuccess > div { background-color: #E6F7F0 !important; color: #006400 !important; border: 2px solid #A3D9B1 !important; border-radius: 10px; font-weight: 600; }
    .stWarning > div { background-color: #FFFBEA !important; color: #9F6000 !important; border: 2px solid #FEEFB3 !important; border-radius: 10px; font-weight: 600; }
    .stError > div { background-color: #FEF2F2 !important; color: #DC2626 !important; border: 2px solid #F87171 !important; border-radius: 10px; font-weight: 600; }
    
    /* SWOT EXPANDER STİLLERİ */
    .swot-section-title {
        color: #FF7F50 !important; border-bottom: 2px solid #FFDAB9;
        padding-bottom: 8px; margin-bottom: 1rem; font-size: 1.5rem;
    }
    
    .streamlit-expanderHeader {
        background-color: #FFF4E6 !important; border: 1px solid #FFDAB9 !important;
        border-radius: 10px !important; padding: 12px 15px !important;
        font-weight: 600 !important; color: #4A4A4A !important;
        transition: all 0.2s ease-in-out; margin-bottom: 5px;
    }

    .streamlit-expanderHeader:hover {
        background-color: #FFDAB9 !important; border-color: #FFB366 !important;
    }
    
    [data-testid="stExpanderDetails"] {
        background-color: #FDFDFD !important; border: 1px solid #EAEAEA;
        border-top: none; border-radius: 0 0 10px 10px; padding: 20px !important;
        margin-top: -6px;
    }
    
    .swot-detail-kanit {
        font-size: 0.95rem; font-weight: 600; color: #333 !important;
        margin-bottom: 8px !important; padding: 8px 12px;
        background-color: #F5F5F5; border-radius: 5px;
    }
    .swot-detail-yorum {
        font-size: 0.9rem; font-style: italic; color: #555 !important;
        margin: 0 !important; padding-left: 15px; border-left: 3px solid #FFDAB9;
    }
</style>
"""

# CSS'i yükle
st.markdown(get_custom_css(), unsafe_allow_html=True)

# .env dosyasındaki API anahtarını yükle
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# --- PERFORMANS İYİLEŞTİRMESİ: Session State'i optimize et ---
def initialize_session_state():
    """Session state'i bir kere initialize et"""
    default_values = {
        'swot': None,
        'career': None,
        'plan': None,
        'cv_text': "",
        'qa_chain': None,
        'interview_history': [],
        'interview_started': False,
        'cv_uploaded': False,
        'processed_rag_file_id': None,
        'processed_rag_text': None,
        'analysis_in_progress': False,  # Yeni: Çoklu tıklamayı önle
        'chosen_career_for_plan': None  # Yeni: Seçilen kariyeri sakla
    }
    
    for key, default_value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

# Session state'i initialize et
initialize_session_state()

# --- PERFORMANS İYİLEŞTİRMESİ: Dosya okuma fonksiyonlarını cache'le ---
@st.cache_data
def get_pdf_text_cached(file_content):
    """PDF okuma işlemini cache'le"""
    try:
        import io
        pdf_reader = pdf.PdfReader(io.BytesIO(file_content))
        return "".join(page.extract_text() for page in pdf_reader.pages)
    except Exception as e:
        st.error(f"PDF okunurken bir hata oluştu: {e}")
        return None

@st.cache_data
def get_docx_text_cached(file_content):
    """Word dosyası okuma işlemini cache'le"""
    try:
        import io
        document = Document(io.BytesIO(file_content))
        return "\n".join([para.text for para in document.paragraphs])
    except Exception as e:
        st.error(f"Word dosyası okunurken bir hata oluştu: {e}")
        return None

def get_pdf_text(uploaded_file):
    return get_pdf_text_cached(uploaded_file.getvalue())

def get_docx_text(uploaded_file):
    return get_docx_text_cached(uploaded_file.getvalue())

# --- PERFORMANS İYİLEŞTİRMESİ: Karriyer listesi çıkarımını cache'le ---
@st.cache_data
def extract_career_list(career_text):
    """Kariyer listesini çıkarma işlemini cache'le"""
    try:
        titles = re.findall(r"Kariyer Yolu Önerisi:\s*(.*)", str(career_text))
        return [title.replace('**', '').replace('🚀', '').strip() for title in titles]
    except Exception:
        return []

# --- KENAR ÇUBUĞU (SIDEBAR) ---
with st.sidebar:
    st.title("AI Kariyer Rehberiniz")
    st.markdown("---")
    st.subheader("1. Adım: Kendinizi Tanıtın")
    st.info("Kariyer analizinizi kişiselleştirmek için CV'nizi yükleyebilirsiniz.")

    cv_tab1, cv_tab2 = st.tabs(["Dosya Yükle", "Metin Olarak Yapıştır"])

    def process_cv(text):
        st.session_state.cv_text = text
        st.session_state.cv_uploaded = True
        st.success("Harika! Analize Hazırız.")
        time.sleep(1)
        st.rerun()

    with cv_tab1:
        uploaded_file = st.file_uploader("PDF veya DOCX dosyanızı buraya sürükleyin", type=["pdf", "docx"], label_visibility="collapsed", key="file_uploader_key")
        if uploaded_file and not st.session_state.cv_uploaded:
            if st.button("CV'mi Yükle ve Başla", use_container_width=True, key="analyze_file"):
                with st.spinner("CV'niz işleniyor..."):
                    text = get_pdf_text(uploaded_file) if uploaded_file.type == "application/pdf" else get_docx_text(uploaded_file)
                    if text: 
                        process_cv(text)

    with cv_tab2:
        text_input = st.text_area("CV metninizi buraya yapıştırabilirsiniz", height=250, label_visibility="collapsed")
        if st.button("Bu Metinle Başla", use_container_width=True, key="cv_text_submit"):
            if text_input:
                process_cv(text_input)
            else:
                st.warning("Lütfen metin alanını doldurun.")
    
    if st.session_state.cv_text:
        st.markdown("---")
        with st.expander("Yüklenen CV Metnini Görüntüle"):
            st.text(st.session_state.cv_text[:500] + "...")
        
        if st.button("Yeni Bir Yolculuk Başlat (Sıfırla)", use_container_width=True):
            # Session state'i temizle
            for key in list(st.session_state.keys()):
                if key != 'file_uploader_key':
                    del st.session_state[key]
            initialize_session_state()
            st.rerun()

# --- ANA EKRAN ---
st.title("Kariyer Gelişim Yolculuğunuza Hoş Geldiniz")

if not st.session_state.cv_text:
    st.markdown("### Kariyer potansiyelinizi keşfetmeye hazır mısınız?")
    st.info("Lütfen sol menüden CV'nizi yükleyerek ilk adımı atın.")
    st.stop()

tab_pano, tab_swot, tab_career, tab_plan, tab_rag = st.tabs(["Genel Bakış", "SWOT: Hızlı Bakış", "Kariyer Alanları", "Yol Haritanız", "Mülakat Provası Yap!"])

with tab_pano:
    st.header("Genel Bakış")
    st.markdown("CV'nizi analiz ettik. Şimdi potansiyelinizi keşfetme zamanı! Aşağıdaki adımları takip ederek kariyerinize yön verin.")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("1. Kendinizi Keşfedin")
        st.write("Kariyer yolculuğunuzda size avantaj sağlayacak güçlü yönlerinizi ve potansiyelinizi ortaya çıkarın.")
        
        # PERFORMANS İYİLEŞTİRMESİ: Çoklu tıklamayı önle
        swot_button_disabled = bool(st.session_state.swot) or st.session_state.analysis_in_progress
        
        if st.button("SWOT Analizini Başlat", use_container_width=True, key="swot_btn", disabled=swot_button_disabled):
            st.session_state.analysis_in_progress = True
            with st.spinner("Kişisel analiziniz oluşturuluyor..."):
                try:
                    st.session_state.swot = get_swot_analysis(st.session_state.cv_text, GOOGLE_API_KEY)
                    st.success("SWOT Analiziniz hazır!")
                except Exception as e:
                    st.error(f"Analiz sırasında hata: {e}")
                finally:
                    st.session_state.analysis_in_progress = False
            st.rerun()
            
        if st.session_state.swot: 
            st.success("Analiz tamamlandı!")
        elif st.session_state.analysis_in_progress:
            st.info("Analiz devam ediyor...")

    with col2:
        st.subheader("2. Alanlarınızı Belirleyin")
        st.write("Deneyim ve yeteneklerinize en uygun kariyer alanlarını öğrenin.")
        
        # PERFORMANS İYİLEŞTİRMESİ: Çoklu tıklamayı önle
        career_button_disabled = bool(st.session_state.career) or st.session_state.analysis_in_progress
        
        if st.button("Bana Özel Alanları Göster", use_container_width=True, key="career_btn", disabled=career_button_disabled):
            st.session_state.analysis_in_progress = True
            with st.spinner("Potansiyelinizle eşleşen kariyerler bulunuyor..."):
                try:
                    st.session_state.career = get_career_paths(st.session_state.cv_text, GOOGLE_API_KEY)
                    st.success("Kariyer alanlarınız belirlendi!")
                except Exception as e:
                    st.error(f"Analiz sırasında hata: {e}")
                finally:
                    st.session_state.analysis_in_progress = False
            st.rerun()
            
        if st.session_state.career: 
            st.success("Öneriler hazır!")
        elif st.session_state.analysis_in_progress:
            st.info("Analiz devam ediyor...")

    with col3:
        st.subheader("3. Yol Haritanızı Çizin")
        st.write("Seçtiğiniz bir hedef için adım adım kişisel gelişim planınızı oluşturun.")
        
        chosen_career = None
        if st.session_state.career:
            career_list = extract_career_list(st.session_state.career)

            if career_list:
                chosen_career = st.selectbox(
                    "Bir kariyer hedefi seçin:", 
                    options=career_list, 
                    index=None, 
                    placeholder="Önerilerden birini seçin..."
                )
            else: 
                st.warning("Öneriler liste olarak alınamadı. Lütfen manuel girin.")
                chosen_career = st.text_input("Hedefinizi manuel girin:", placeholder="örn: Veri Bilimci")
        else:
            st.text_input("Hedefiniz için bir plan oluşturun", placeholder="Önce kariyer alanlarını keşfedin", disabled=True)

        # PERFORMANS İYİLEŞTİRMESİ: Çoklu tıklamayı önle ve gereksiz yeniden hesaplamayı önle
        plan_button_disabled = not chosen_career or st.session_state.analysis_in_progress or (st.session_state.plan and st.session_state.chosen_career_for_plan == chosen_career)
        
        if st.button("Yol Haritamı Çiz", use_container_width=True, key="plan_btn", disabled=plan_button_disabled):
            st.session_state.analysis_in_progress = True
            with st.spinner(f"'{chosen_career}' için yol haritanız çiziliyor..."):
                try:
                    st.session_state.plan = get_learning_plan(st.session_state.cv_text, chosen_career, GOOGLE_API_KEY)
                    st.session_state.chosen_career_for_plan = chosen_career
                    st.success("Yol haritanız hazır!")
                except Exception as e:
                    st.error(f"Plan oluşturulurken hata: {e}")
                finally:
                    st.session_state.analysis_in_progress = False
            st.rerun()
            
        if st.session_state.plan and st.session_state.chosen_career_for_plan == chosen_career: 
            st.success("Planınız hazır!")
        elif st.session_state.analysis_in_progress:
            st.info("Plan hazırlanıyor...")

# --- SWOT RENDER FONKSİYONU - Cache'li ---
@st.cache_data
def render_swot_items(items, section_type):
    """SWOT öğelerini render etmek için cache'li fonksiyon"""
    rendered_items = []
    if items:
        for item in items:
            rendered_items.append({
                'anahtar_kelime': item.anahtar_kelime,
                'kanit': item.kanit,
                'yorum': item.yorum
            })
    return rendered_items

def render_swot_section(title: str, items: list):
    if items:
        st.markdown(f'<h3 class="swot-section-title">{title}</h3>', unsafe_allow_html=True)
        # PERFORMANS İYİLEŞTİRMESİ: Cache'li render kullan
        cached_items = render_swot_items(items, title)
        for item in cached_items:
            with st.expander(f"{item['anahtar_kelime']}"):
                st.markdown(f'<p class="swot-detail-kanit"><b>CV\'den Kanıt:</b> {item["kanit"]}</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="swot-detail-yorum"><b>Analist Yorumu:</b> {item["yorum"]}</p>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

# --- SEKME İÇERİKLERİ ---
with tab_swot:
    st.header("SWOT Analiziniz: Hızlı Bakış")
    st.write("Aşağıda, analizin öne çıkan başlıklarını görebilirsiniz. Detayları görmek için başlıklara tıklayın.")
    st.markdown("---")
    
    if st.session_state.get('swot'):
        swot_data = st.session_state.swot
        render_swot_section("💪 Güçlü Yönleriniz", swot_data.guclu_yonler)
        render_swot_section("🌱 Gelişim Fırsatlarınız", swot_data.gelisim_firsatlari)
        render_swot_section("🎯 Piyasa Fırsatları", swot_data.firsatlar)
        render_swot_section("⚠️ Dikkate Alınması Gerekenler", swot_data.dikkate_alinmasi_gerekenler)
    else:
        st.info("Bu analizi görmek için 'Genel Bakış' panelindeki 'SWOT Analizini Başlat' butonuna tıklayın.")

with tab_career:
    st.header("Size Özel Kariyer Alanları")
    if st.session_state.get('career'):
        st.markdown(st.session_state.career)
    else:
        st.info("Bu önerileri görmek için 'Genel Bakış' panelindeki 'Bana Özel Alanları Göster' butonuna tıklayın.")

with tab_plan:
    st.header("Kişisel Gelişim Yol Haritanız")
    if st.session_state.get('plan'):
        st.markdown(st.session_state.plan)
    else:
        st.info("Bu planı görmek için 'Genel Bakış' panelinde bir kariyer seçip 'Yol Haritamı Çiz' butonuna tıklayın.")

# --- RAG BÖLÜMÜ - Performans iyileştirmeleri ile ---
with tab_rag:
    st.header("Mülakat Provası Yap!")
    st.write("Başvurmak istediğiniz pozisyonun iş ilanını yükleyin veya yapıştırın ve o ilana özel bir mülakat deneyimi yaşayın.")
    st.markdown("---")

    should_create_chain = False
    input_data = None
    
    # --- İŞ İLANI GİRİŞ ARAYÜZÜ ---
    input_tab1, input_tab2 = st.tabs(["İlanı PDF Olarak Yükle", "İlan Metnini Yapıştır"])

    with input_tab1:
        rag_uploaded_file = st.file_uploader("İş ilanı PDF'ini buraya yükleyin", type="pdf", key="interview_pdf_uploader")
        if rag_uploaded_file and st.session_state.processed_rag_file_id != rag_uploaded_file.file_id:
            if st.button("Bu İlanı Analiz Et", use_container_width=True, key="analyze_job_pdf"):
                should_create_chain = True
                input_data = rag_uploaded_file
                st.session_state.processed_rag_file_id = rag_uploaded_file.file_id
                st.session_state.processed_rag_text = None

    with input_tab2:
        job_ad_text = st.text_area("İş ilanı metnini buraya yapıştırın", height=250, key="job_ad_text", placeholder="İş ilanı metnini buraya yapıştırın...")
        if st.button("Bu Metni Analiz Et", use_container_width=True, key="job_text_submit"):
            if job_ad_text and st.session_state.processed_rag_text != job_ad_text:
                should_create_chain = True
                input_data = job_ad_text
                st.session_state.processed_rag_text = job_ad_text
                st.session_state.processed_rag_file_id = None

    # --- ZİNCİR OLUŞTURMA MANTIĞI ---
    if should_create_chain:
        with st.spinner("İlan analiz ediliyor..."):
            try:
                st.session_state.qa_chain = create_rag_chain(input_data, GOOGLE_API_KEY)
                st.session_state.interview_started = False
                st.session_state.interview_history = []
                if st.session_state.qa_chain:
                    st.success("İlan analiz edildi! Provanızı başlatmaya hazırsınız.")
                else:
                    st.error("İlan işlenirken bir sorun oluştu. API anahtarınızı veya dosyayı kontrol edin.")
            except Exception as e:
                st.error(f"RAG zinciri oluşturulurken hata: {e}")
        st.rerun()
    
    # --- MÜLAKAT SİMÜLASYONU ARAYÜZÜ ---
    if st.session_state.get('qa_chain') is not None:
        if not st.session_state.interview_started:
            if st.button("Mülakat Provasını Başlat", use_container_width=True, key="start_interview"):
                st.session_state.interview_started = True
                st.session_state.interview_history = []
                st.rerun()

        if st.session_state.interview_started:
            if not st.session_state.interview_history:
                with st.spinner("İlk mülakat sorunuz hazırlanıyor..."):
                    try:
                        initial_prompt = "Sen deneyimli bir işe alım yöneticisisin. Sana verdiğim iş ilanı metnini kullanarak bir mülakat simülasyonu başlat. İlk görevin, ilandaki en önemli teknik veya sosyal yetkinliğe odaklanan, adayın yeteneklerini ölçmeye yönelik yaratıcı ve açık uçlu bir soru sormak. Sadece soruyu sor, başka bir şey söyleme."
                        response_dict = st.session_state.qa_chain.invoke({"query": initial_prompt})
                        if response_dict and 'result' in response_dict:
                            st.session_state.interview_history.append({"role": "assistant", "content": response_dict['result']})
                        else:
                            st.error("İlk soru oluşturulamadı.")
                    except Exception as e:
                        st.error(f"Mülakat başlatılırken hata: {e}")
                    st.rerun()
            
            for message in st.session_state.interview_history:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            if user_answer := st.chat_input("Cevabınızı buraya yazın..."):
                st.session_state.interview_history.append({"role": "user", "content": user_answer})
                with st.spinner("Cevabınız değerlendiriliyor ve yeni soru hazırlanıyor..."):
                    try:
                        follow_up_prompt = f"Sen deneyimli bir işe alım yöneticisisin ve bir mülakat simülasyonu yapıyorsun. Sana verdiğim iş ilanı metnini ve adayın son cevabını dikkate alarak şu iki adımı uygula: 1. Geri Bildirim Ver: Adayın '{user_answer}' cevabını kısaca ve yapıcı bir dille değerlendir. 2. Yeni Soru Sor: İlandaki FARKLI bir yetkinliği ölçmek için yeni ve yaratıcı bir soruya geç. Tüm bu cevabını tek bir akıcı paragraf olarak sun."
                        response_dict = st.session_state.qa_chain.invoke({"query": follow_up_prompt})
                        if response_dict and 'result' in response_dict:
                            st.session_state.interview_history.append({"role": "assistant", "content": response_dict['result']})
                        else:
                            st.error("Yeni soru oluşturulamadı.")
                    except Exception as e:
                        st.error(f"Mülakat devam ettirilemedi: {e}")
                st.rerun()
                
            st.markdown("---")
            col_rag1, col_rag2 = st.columns(2)
            with col_rag1:
                if st.button("Mülakat Provasını Bitir", use_container_width=True, key="end_interview"):
                    st.session_state.interview_started = False
                    st.session_state.interview_history = []
                    st.success("Prova sonlandırıldı.")
                    st.rerun()
            with col_rag2:
                if st.button("Yeni İlanla Prova Yap", use_container_width=True, key="new_job_ad"):
                    st.session_state.qa_chain = None
                    st.session_state.interview_started = False
                    st.session_state.interview_history = []
                    st.session_state.processed_rag_file_id = None
                    st.session_state.processed_rag_text = None
                    st.info("Yeni bir iş ilanı yükleyebilirsiniz.")
                    st.rerun()
    else:
        st.info("Bir mülakat provası yapmak için lütfen bir iş ilanı yükleyin veya metnini yapıştırın.")

# --- FOOTER VE EK PERFORMANS ÖNERİLERİ ---
st.markdown("---")
st.markdown("### 💡 Performans İpuçları:")
st.info("""
**Streamlit Cloud'da En İyi Performans İçin:**
- Analizler bir kere yapıldıktan sonra otomatik olarak kaydedilir
- Sayfayı yenilemeden önce tüm analizlerinizin tamamlandığından emin olun
- Büyük dosyalar yüklerken sabırlı olun - cloud ortamı yerel makinenizden daha yavaş olabilir
""")



# === PERFORMANS İYİLEŞTİRME CHECKPOINT'LERİ ===

def add_performance_monitoring():
    """Performans izleme için ekstra fonksiyonlar"""
    
    # Session state boyutunu kontrol et
    if 'session_size_warning' not in st.session_state:
        st.session_state.session_size_warning = False
    
    # Büyük veri kontrolü
    total_size = 0
    for key, value in st.session_state.items():
        if isinstance(value, str):
            total_size += len(value.encode('utf-8'))
    
    # 5MB'dan büyükse uyarı ver
    if total_size > 5 * 1024 * 1024 and not st.session_state.session_size_warning:
        st.warning("⚠️ Session verisi büyük boyutta. Performansı artırmak için sayfayı yenilemeyi düşünün.")
        st.session_state.session_size_warning = True

# Performans izlemeyi etkinleştir
add_performance_monitoring()

# === HATA YAKALAMA VE LOGLAma ===

def safe_api_call(func, *args, **kwargs):
    """API çağrılarını güvenli şekilde yap"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        st.error(f"API çağrısı başarısız: {str(e)[:100]}...")
        return None

# === KULLANICI DENEYİMİ İYİLEŞTİRMELERİ ===

# Progress bar için yardımcı fonksiyon
def show_progress_with_message(message, steps=3):
    """Kullanıcı deneyimi için progress bar göster"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i in range(steps):
        progress_bar.progress((i + 1) / steps)
        status_text.text(f"{message} ({i+1}/{steps})")
        time.sleep(0.5)
    
    progress_bar.empty()
    status_text.empty()

# === DİĞER OPTİMİZASYONLAR ===

# Streamlit konfigürasyon önerileri (streamlit_config.toml için):
"""
[server]
# Daha hızlı yükleme için
enableCORS = false
enableXsrfProtection = false

# Bellek optimizasyonu için
maxUploadSize = 100
maxMessageSize = 100

[browser]
# Otomatik yenilemeyi kapat (performans için)
gatherUsageStats = false

[theme]
# Tema optimizasyonu
base = "light"
"""

# === CACHE CLEAR FONKSİYONU ===
def clear_all_caches():
    """Tüm cache'leri temizle"""
    st.cache_data.clear()
    if hasattr(st.cache_resource, 'clear'):
        st.cache_resource.clear()

# Gerektiğinde cache temizleme butonu ekle
if st.button("🔄 Performans Sorununda Cache Temizle", help="Eğer uygulama çok yavaş çalışıyorsa bu butona basın"):
    clear_all_caches()
    st.success("Cache temizlendi! Sayfa yenilenecek.")
    time.sleep(1)
    st.rerun()

# === MOBIL UYUMLULUK İÇİN EK CSS ===
mobile_css = """
<style>
@media (max-width: 768px) {
    .st-emotion-cache-1r4qj8v, 
    .st-emotion-cache-1jicfl2 {
        padding: 15px !important;
        margin: 5px 0 !important;
    }
    
    .stButton > button {
        font-size: 0.9rem;
        padding: 10px 20px;
    }
}
</style>
"""
st.markdown(mobile_css, unsafe_allow_html=True)