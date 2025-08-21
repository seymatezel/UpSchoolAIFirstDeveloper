# TAM VE GÜNCEL APP.PY KODU - PERFORMANS OPTİMİZE EDİLMİŞ VERSİYON

import streamlit as st
import os
from dotenv import load_dotenv
import time 
import PyPDF2 as pdf
from docx import Document
import re
import io

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

# --- CSS'i cache'le ---
@st.cache_data
def get_custom_css():
    # ... CSS kodunuz burada, hiç değişiklik yapmadım ...
    # Bu kısım zaten optimize olduğu için olduğu gibi bırakıyorum.
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

st.markdown(get_custom_css(), unsafe_allow_html=True)

### YENİ/DEĞİŞTİ ###
# Streamlit Cloud'un Secrets yönetimini kullanmak için API anahtarını alıyoruz.
# .env dosyası sadece yerel geliştirme içindir.
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
except (FileNotFoundError, KeyError):
    # Yerel geliştirme için .env dosyasından yükle
    load_dotenv()
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


# --- HAFIZA (SESSION STATE) ---
# DEĞİŞİKLİK: Mülakat provası için session state'i basitleştirdim.
# 'processed_rag_file_id' ve 'processed_rag_text' gibi karmaşık kontrollere gerek kalmadı.
for key in ['swot', 'career', 'plan', 'cv_text', 'qa_chain', 'interview_history', 'interview_started', 'cv_uploaded']:
    if key not in st.session_state:
        if key == 'cv_text': st.session_state[key] = ""
        elif key == 'interview_history': st.session_state[key] = []
        elif key == 'cv_uploaded' or key == 'interview_started': st.session_state[key] = False
        else: st.session_state[key] = None

if not GOOGLE_API_KEY:
    st.error("Google API Anahtarı bulunamadı! Lütfen Streamlit Cloud Secrets'e ekleyin.")
    st.stop()


def initialize_session_state():
    # Bu fonksiyon zaten iyi, olduğu gibi bırakıyorum.
    # ...
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
        'analysis_in_progress': False,  
        'chosen_career_for_plan': None  
    }
    
    for key, default_value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

initialize_session_state()

# Dosya okuma fonksiyonları zaten cache'li ve optimize, olduğu gibi bırakıyorum.
@st.cache_data
def get_pdf_text(file_content):
    try:
        pdf_reader = pdf.PdfReader(io.BytesIO(file_content))
        return "".join(page.extract_text() for page in pdf_reader.pages if page.extract_text())
    except Exception as e:
        st.error(f"PDF okunurken bir hata oluştu: {e}")
        return None

@st.cache_data
def get_docx_text(file_content):
    try:
        document = Document(io.BytesIO(file_content))
        return "\n".join([para.text for para in document.paragraphs])
    except Exception as e:
        st.error(f"Word dosyası okunurken bir hata oluştu: {e}")
        return None

@st.cache_data
def extract_career_list(career_text):
    # Bu fonksiyon zaten cache'li ve optimize, olduğu gibi bırakıyorum.
    # ...
    try:
        titles = re.findall(r"Kariyer Yolu Önerisi:\s*(.*)", str(career_text))
        return [title.replace('**', '').replace('🚀', '').strip() for title in titles]
    except Exception:
        return []


### YENİ/DEĞİŞTİ ###
# Bu render fonksiyonunu cache'lemek gereksiz ve performansı düşürebilir.
# Sadece ekrana çizim yaptığı için cache'e gerek yok. Hesaplama yapan ana
# fonksiyonlar (get_swot_analysis vb.) zaten session_state'te tutuluyor.
def render_swot_section(title: str, items: list):
    """SWOT bölümünü ekrana çizen basit bir yardımcı fonksiyon."""
    if not items:
        return
        
    st.markdown(f'<h3 class="swot-section-title">{title}</h3>', unsafe_allow_html=True)
    for item in items:
        # Pydantic objelerinden veriyi güvenli bir şekilde alalım
        anahtar_kelime = getattr(item, 'anahtar_kelime', 'Başlık Yok')
        kanit = getattr(item, 'kanit', 'Kanıt bulunamadı.')
        yorum = getattr(item, 'yorum', 'Yorum bulunamadı.')
        
        with st.expander(f"{anahtar_kelime}"):
            st.markdown(f'<p class="swot-detail-kanit"><b>CV\'den Kanıt:</b> {kanit}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="swot-detail-yorum"><b>Analist Yorumu:</b> {yorum}</p>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)


# --- ANA UYGULAMA AKIŞI ---
# Bu kısımlarda bir değişiklik yapmadım, mantığınız zaten doğru çalışıyor.
# Sidebar, ana ekran butonları ve sekmeleriniz olduğu gibi kalabilir.
# ... (Sidebar kodunuz) ...
# ... (Ana Ekran kodunuz) ...
# ... (Sekme içerikleriniz, SADECE render_swot_section çağrısını kontrol edin) ...

# Kenar çubuğu ve ana ekran mantığınızı buraya yapıştırabilirsiniz.
# Aşağıdaki SWOT sekmesi örneği gibi.
# ...
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
                    text = get_pdf_text(uploaded_file.getvalue()) if uploaded_file.type == "application/pdf" else get_docx_text(uploaded_file.getvalue())
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

            # 'file_uploader_key' dışındaki tüm session_state anahtarlarını sil.
            # Bu widget'a bağlı olduğu için ona dokunmuyoruz.
            for key in list(st.session_state.keys()):
                if key != 'file_uploader_key':
                    del st.session_state[key]
                    
            # Diğer tüm veriler silindi. Uygulamayı yeniden çalıştır.
            st.rerun()

            for key in list(st.session_state.keys()):
                if key != 'file_uploader_key':
                    del st.session_state[key]



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
        
        plan_button_disabled = bool(not chosen_career or st.session_state.analysis_in_progress or (st.session_state.plan and st.session_state.chosen_career_for_plan == chosen_career))
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


with tab_rag:
    st.header("Mülakat Provası Yap!")
    st.write("Başvurmak istediğiniz pozisyonun iş ilanını yükleyin veya yapıştırın ve o ilana özel bir mülakat deneyimi yaşayın.")
    st.markdown("---")

    # DEĞİŞİKLİK: İşlemleri doğrudan ilgili butonların içine taşıyarak mantığı basitleştirdik.
    # Bu, her yeniden çalıştırmada gereksiz kontrolleri engeller.
    def reset_interview_state():
        """Mülakatla ilgili tüm session state'leri temizler."""
        st.session_state.qa_chain = None
        st.session_state.interview_started = False
        st.session_state.interview_history = []

    # Eğer mülakat zinciri henüz oluşturulmadıysa, kullanıcıya seçenekleri sun.
    if 'qa_chain' not in st.session_state or st.session_state.qa_chain is None:
        st.subheader("İş İlanını Yükleyin")
        input_tab1, input_tab2 = st.tabs(["İlanı PDF Olarak Yükle", "İlan Metnini Yapıştır"])

        with input_tab1:
            rag_uploaded_file = st.file_uploader("İş ilanı PDF'ini buraya yükleyin", type="pdf", key="interview_pdf_uploader")
            if st.button("Bu İlanı Analiz Et", use_container_width=True, key="analyze_job_pdf"):
                if rag_uploaded_file is not None:
                    # Zincir oluşturma işlemini doğrudan butonun içine taşıdık
                    st.session_state.qa_chain = create_rag_chain(rag_uploaded_file, GOOGLE_API_KEY)
                    if st.session_state.qa_chain:
                        st.success("İlan analiz edildi! Provanızı başlatmaya hazırsınız.")
                        st.rerun() # Arayüzü güncellemek için yeniden çalıştır
                    else:
                        st.error("İlan işlenirken bir sorun oluştu. API anahtarınızı veya dosyayı kontrol edin.")
                else:
                    st.warning("Lütfen önce bir PDF dosyası yükleyin.")

        with input_tab2:
            job_ad_text = st.text_area("İş ilanı metnini buraya yapıştırın", height=250, key="job_ad_text", placeholder="İş ilanı metnini buraya yapıştırın...")
            if st.button("Bu Metni Analiz Et", use_container_width=True, key="job_text_submit"):
                if job_ad_text.strip():
                    st.session_state.qa_chain = create_rag_chain(job_ad_text, GOOGLE_API_KEY)
                    if st.session_state.qa_chain:
                        st.success("İlan analiz edildi! Provanızı başlatmaya hazırsınız.")
                        st.rerun()
                    else:
                        st.error("İlan işlenirken bir sorun oluştu. API anahtarınızı kontrol edin.")
                else:
                    st.warning("Lütfen metin alanına iş ilanını yapıştırın.")
    
    # Eğer mülakat zinciri başarıyla oluşturulduysa, mülakat arayüzünü göster.
    else:
        st.success("İş ilanı hazır. Mülakat provasına başlayabilirsiniz.")

        # Mülakat başlatma ve bitirme butonları
        col1, col2 = st.columns(2)
        with col1:
            if not st.session_state.interview_started:
                if st.button("Mülakat Provasını Başlat", use_container_width=True):
                    st.session_state.interview_started = True
                    st.rerun()
        
        with col2:
             if st.button("Yeni İlanla Prova Yap (Sıfırla)", use_container_width=True):
                reset_interview_state()
                st.rerun()

        st.markdown("---")

        # Mülakat sohbet arayüzü
        if st.session_state.interview_started:
            # Eğer sohbet geçmişi boşsa, ilk soruyu oluştur
            if not st.session_state.interview_history:
                with st.spinner("İlk mülakat sorunuz hazırlanıyor..."):
                    initial_prompt = "Sen deneyimli bir işe alım yöneticisisin. Sana verdiğim iş ilanı metnini kullanarak bir mülakat simülasyonu başlat. İlk görevin, ilandaki en önemli teknik veya sosyal yetkinliğe odaklanan, adayın yeteneklerini ölçmeye yönelik yaratıcı ve açık uçlu bir soru sormak. Sadece soruyu sor, başka bir şey söyleme."
                    response_dict = st.session_state.qa_chain.invoke({"query": initial_prompt})
                    if response_dict and 'result' in response_dict:
                        st.session_state.interview_history.append({"role": "assistant", "content": response_dict['result']})
                        st.rerun()
                    else:
                        st.error("İlk soru oluşturulamadı. Lütfen sıfırlayıp tekrar deneyin.")
            
            # Sohbet geçmişini ekrana yazdır
            for message in st.session_state.interview_history:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            # Kullanıcıdan cevap al
            if user_answer := st.chat_input("Cevabınızı buraya yazın..."):
                st.session_state.interview_history.append({"role": "user", "content": user_answer})
                
                with st.spinner("Cevabınız değerlendiriliyor ve yeni soru hazırlanıyor..."):
                    follow_up_prompt = f"Sen deneyimli bir işe alım yöneticisisin ve bir mülakat simülasyonu yapıyorsun. Sana verdiğim iş ilanı metnini ve adayın son cevabını dikkate alarak şu iki adımı uygula: 1. Geri Bildirim Ver: Adayın '{user_answer}' cevabını kısaca ve yapıcı bir dille değerlendir. 2. Yeni Soru Sor: İlandaki FARKLI bir yetkinliği ölçmek için yeni ve yaratıcı bir soruya geç. Tüm bu cevabını tek bir akıcı paragraf olarak sun. Konuşma geçmişi: {st.session_state.interview_history}"
                    response_dict = st.session_state.qa_chain.invoke({"query": follow_up_prompt})
                    if response_dict and 'result' in response_dict:
                        st.session_state.interview_history.append({"role": "assistant", "content": response_dict['result']})
                    else:
                        st.error("Yeni soru oluşturulamadı. Lütfen sıfırlayıp tekrar deneyin.")
                st.rerun()