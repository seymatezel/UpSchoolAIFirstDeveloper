# 🤖 AI Kariyer Rehberiniz

Bu proje, kullanıcıların CV'lerini analiz ederek onlara kişiselleştirilmiş kariyer rehberliği sunan, Streamlit ile geliştirilmiş bir web uygulamasıdır. Google Gemini yapay zeka modeli kullanılarak, kullanıcının potansiyelini ortaya çıkarmayı ve kariyer yolculuğunda somut adımlar sunmayı hedefler.

## ✨ Ana Özellikler

- **Çoklu CV Formatı**: PDF, DOCX ve doğrudan metin girişi desteği
- **Kişiselleştirilmiş Analizler**: SWOT Analizi, Kariyer Yolu Önerileri ve Kişisel Öğrenme Planı
- **Agent Mimarisi**: LangChain kullanılarak oluşturulmuş modüler ve akıllı agent yapısı
- **Modern Arayüz**: Streamlit ile oluşturulmuş interaktif ve kullanıcı dostu bir arayüz

## 🚀 Kurulum ve Çalıştırma

Bu projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin.

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
