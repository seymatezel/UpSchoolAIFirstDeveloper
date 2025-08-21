# 🤖 AI Kariyer Rehberiniz

Bu proje, kullanıcıların CV'lerini analiz ederek onlara kişiselleştirilmiş kariyer rehberliği sunan, Streamlit ile geliştirilmiş bir web uygulamasıdır. Google Gemini yapay zeka modeli kullanılarak, kullanıcının potansiyelini ortaya çıkarmayı ve kariyer yolculuğunda somut adımlar sunmayı hedefler.

## ✨ Özellikler

**Çoklu Format:** PDF, DOCX, metin desteği 
**AI Analizler:** SWOT, Kariyer Yolu, Öğrenme Planı
**Smart Agents:** LangChain tabanlı modüler sistem
**RAG Pipeline:** Doküman işleme ve semantik arama

## 🛠️ Teknolojiler

**AI:** Google Gemini Pro + LangChain
**RAG:** Vektör embedding ve retrieval
**UI:** Streamlit
**Dosya İşleme:** PyPDF2, python-docx

## AI Mimarisi
### Agent Sistemi

**CareerAgent:** Kariyer analizi ve öneriler
**SWOTAgent:** Güçlü/zayıf yan analizi
**LearningAgent:** Öğrenme yol haritası

### RAG Pipeline

**Document Processing:** CV'den metin çıkarma
**Embedding:** Vektör dönüşümü (LangChain)
**Retrieval:** Semantik arama
**Generation:** Gemini ile yanıt üretimi

## Kurulum ve Çalıştırma

Bu projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin.

### Gereksinimler

Python 3.8 veya üzeri
Google API anahtarı

### 1. Projeyi İndirin

```bash
git clone https://github.com/seymatezel/UpSchoolAIFirstDeveloper.git
cd UpSchoolAIFirstDeveloper
```

### 2. Gerekli Kütüphaneleri Yükleyin

```bash
pip install -r requirements.txt
```

### 3. API Anahtarınızı Ekleyin

1. [Google AI Studio](https://aistudio.google.com/) adresinden ücretsiz bir API anahtarı alın
2. Proje klasöründe `.env` adında yeni bir dosya oluşturun
3. Bu dosyanın içine aşağıdaki satırı ekleyin:

```env
GOOGLE_API_KEY="BURAYA_KENDİ_API_ANAHTARINIZI_YAPIŞTIRIN"
```

### 4. Uygulamayı Başlatın

```bash
streamlit run app.py
```

## 🌐 Canlı Demo

**Alternatif Olarak:** [Bu linkten](https://upschoolaifirstdeveloper-b2ndx2hpy4ks4fw7e4lxpc.streamlit.app/) direkt uygulamayı çalıştırıp kullanabilirsiniz.


## 📸 Uygulma İçinden Bazı Ekran Görüntüleri
<img width="1916" height="967" alt="image" src="https://github.com/user-attachments/assets/cac94a1d-2ba7-430a-bb1b-5ae007242858" />
<img width="1917" height="969" alt="image" src="https://github.com/user-attachments/assets/761f279f-f2f0-4188-b127-b620da784660" />
<img width="1919" height="963" alt="image" src="https://github.com/user-attachments/assets/1af38a9d-65c4-46fe-a921-f8daa14d1cae" />

*Ana sayfa görünümü, CV anliz edildikten sonraki ekran, SWOT analizi sonuçları*


## 📁 Proje Yapısı

```
UpSchoolAIFirstDeveloper/
│
├── app.py                    # Ana Streamlit uygulaması - UI ve ana logic
├── requirements.txt          # Python bağımlılıkları listesi
├── README.md                # Proje dokümantasyonu
├── automation.md            # Otomasyon süreçleri dokümantasyonu
├── .env                     # Environment değişkenleri (API anahtarları)
│
├── agents/                  # AI Agent sınıfları
│   ├── __init__.py          # Python paketi tanımlayıcısı
│   ├── career_agent.py      # Kariyer analizi ve öneriler
│   ├── swot_agent.py        # SWOT analizi (Güçlü/Zayıf yanlar)
│   └── plan_agent.py        # Öğrenme planı ve yol haritası
│
└── rag/                     # RAG (Retrieval Augmented Generation) sistemi
    ├── rag_module.py        # Doküman işleme ve semantik arama
    └── rag_readme.md        # RAG sistemi dokümantasyonu
```

## Demo Videosu:
Dilerseniz demo videoma [buradan](https://drive.google.com/file/d/1axTT7jkcnEfGD1dkwhnaW6LPuzUyOhka/view?usp=drive_link) ulaşabilirsiniz!

## 👨‍💻 Geliştirici

**Seyma Tezel** - [GitHub](https://github.com/seymatezel) / [LinkedIn](https://www.linkedin.com/in/seymatezel)




