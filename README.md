# 🤖 AI Kariyer Rehberiniz
Bu proje, kullanıcıların CV'lerini analiz ederek onlara kişiselleştirilmiş kariyer rehberliği sunan, Streamlit ile geliştirilmiş bir web uygulamasıdır. Google Gemini yapay zeka modeli kullanılarak, kullanıcının potansiyelini ortaya çıkarmayı ve kariyer yolculuğunda somut adımlar sunmayı hedefler.
## ✨ Ana Özellikler
Çoklu CV Formatı: PDF, DOCX ve doğrudan metin girişi desteği.
Kişiselleştirilmiş Analizler: SWOT Analizi, Kariyer Yolu Önerileri ve Kişisel Öğrenme Planı.
Agent Mimarisi: LangChain kullanılarak oluşturulmuş modüler ve akıllı agent yapısı.
Modern Arayüz: Streamlit ile oluşturulmuş interaktif ve kullanıcı dostu bir arayüz.
## 🚀 Kurulum ve Çalıştırma
Bu projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin.
### 1. Projeyi İndirin
Generated bash
git clone https://github.com/seymatezel/UpSchool-AIFD.git
cd UpSchool-AIFD
Use code with caution.
Bash
### 2. Gerekli Kütüphaneleri Yükleyin
Generated bash
pip install -r requirements.txt
Use code with caution.
Bash
### 3. API Anahtarınızı Ekleyin
Projenin çalışabilmesi için bir Google API anahtarına ihtiyacınız vardır.
Google AI Studio adresinden ücretsiz bir API anahtarı alın.
Proje klasöründe .env adında yeni bir dosya oluşturun.
Oluşturduğunuz bu dosyanın içine aşağıdaki satırı ekleyin ve kendi API anahtarınızı yapıştırın:

GOOGLE_API_KEY="BURAYA_KENDİ_API_ANAHTARINIZI_YAPIŞTIRIN"

### 4. Uygulamayı Başlatın
Terminalizine "streamlit run app.py" yazarak tarayıcınızda otomatik olarak çalıştırabilirsiniz.
https://upschoolaifirstdeveloper-b2ndx2hpy4ks4fw7e4lxpc.streamlit.app/ Buradan direkt uygulmayı çalıştırıp kullanabilirsiniz.
