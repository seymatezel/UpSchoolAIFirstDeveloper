# 🤖 AI Kariyer Rehberiniz

Bu proje, kullanıcıların CV'lerini analiz ederek onlara kişiselleştirilmiş kariyer rehberliği sunan, Streamlit ile geliştirilmiş bir web uygulamasıdır. Google Gemini yapay zeka modeli kullanılarak, kullanıcının potansiyelini ortaya çıkarmayı ve kariyer yolculuğunda somut adımlar sunmayı hedefler.

## 📸 Uygulma İçinden Bazı Ekran Görüntüleri
<img width="1916" height="967" alt="image" src="https://github.com/user-attachments/assets/cac94a1d-2ba7-430a-bb1b-5ae007242858" />
<img width="1917" height="969" alt="image" src="https://github.com/user-attachments/assets/761f279f-f2f0-4188-b127-b620da784660" />
<img width="1919" height="963" alt="image" src="https://github.com/user-attachments/assets/1af38a9d-65c4-46fe-a921-f8daa14d1cae" />

*Ana sayfa görünümü, CV anliz edildikten sonraki ekran, SWOT analizi sonuçları*


## ✨ Ana Özellikler

- **Çoklu CV Formatı**: PDF, DOCX ve doğrudan metin girişi desteği
- **Kişiselleştirilmiş Analizler**: SWOT Analizi, Kariyer Yolu Önerileri ve Kişisel Öğrenme Planı
- **Agent Mimarisi**: LangChain kullanılarak oluşturulmuş modüler ve akıllı agent yapısı
- **Modern Arayüz**: Streamlit ile oluşturulmuş interaktif ve kullanıcı dostu bir arayüz

## 🔧 Teknik Detaylar
AI Agent Sistemi
Her agent belirli bir analiz türünden sorumludur:

🎯 CareerAgent: Mevcut becerileri analiz eder, kariyer fırsatlarını değerlendirir
📊 SWOTAgent: Güçlü/zayıf yanları, fırsat/tehditleri belirler
📚 LearningAgent: Eksik becerileri tespit eder, öğrenme yol haritası çizer

### RAG Pipeline

Document Processing: CV'den metin çıkarma ve temizleme
Embedding: Metni vektör formatına dönüştürme
Storage: Vektör veritabanında saklama
Retrieval: İlgili bilgi parçalarını bulma
Generation: Gemini ile contextualized yanıt üretme

### Kullanılan AI Teknolojileri

Google Gemini Pro: Ana dil modeli
LangChain: Agent framework ve RAG sistemi
Embeddings: Semantic arama için vektör represantasyonları
Streamlit: Real-time UI ve kullanıcı etkileşimi

## 🛠️ Kullanılan Teknolojiler

Frontend: Streamlit
AI Model: Google Gemini Pro
Framework: LangChain
Dosya İşleme: PyPDF2, python-docx
Environment: python-dotenv

## 🚀 Kurulum ve Çalıştırma

Bu projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin.

### 📋 Gereksinimler

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
├── app.py                 # Ana Streamlit uygulaması
├── requirements.txt       # Python bağımlılıkları
├── .env.example          # Environment değişkenleri örneği
├── README.md             # Proje dokümantasyonu
└── agents/               # AI agent sınıfları (varsa)
```

## 🤝 Katkıda Bulunma

1. Bu repository'yi fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/YeniOzellik`)
3. Değişikliklerinizi commit edin (`git commit -m 'Yeni özellik eklendi'`)
4. Branch'inizi push edin (`git push origin feature/YeniOzellik`)
5. Pull Request oluşturun


## 👨‍💻 Geliştirici

**Seyma Tezel** - [GitHub](https://github.com/seymatezel)


