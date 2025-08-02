# Proje: AI Kariyer Koçu - Agent Mimarisi ve Otomasyon

## 1. Projenin Amacı

Bu projenin amacı, bir kullanıcının CV'sini analiz ederek ona kişiselleştirilmiş kariyer rehberliği sunmaktır. Bu süreç, LangChain framework'ü kullanılarak oluşturulmuş modüler bir agent mimarisi ile yönetilmektedir.

## 2. Agent Mimarisi ve Yaklaşım

Projede, her biri belirli bir görevde uzmanlaşmış üç farklı "agent" bulunmaktadır. Bu agent'lar, ana uygulama (`app.py`) tarafından yönetilen ve çağrılan ayrı Python modülleri (`agents/` klasörü altında) olarak tasarlanmıştır. Bu modüler yapı, kodun okunabilirliğini, bakımını ve gelecekteki geliştirmeleri kolaylaştırır.

Kullanılan teknoloji **LangChain** ve **Google Gemini Pro** modelidir. LangChain, prompt şablonları, LLM entegrasyonu ve çıktı yönetimi gibi işlemleri basitleştiren bir "zincir" (chain) yapısı sunar.

### Agent'lar ve Görevleri:

1.  **SWOT Agent (`swot_agent.py`)**:
    *   **Görevi**: CV'yi analiz ederek kullanıcının Güçlü Yönlerini, Zayıf Yönlerini, Fırsatlarını ve Tehditlerini (SWOT) belirler.
    *   **Tetiklenme**: Kullanıcı tarafından manuel olarak veya otomasyon sürecinin bir parçası olarak çağrılır.

2.  **Kariyer Agent (`career_agent.py`)**:
    *   **Görevi**: CV'deki yetenek ve deneyimlere dayanarak kullanıcıya 4-5 adet potansiyel kariyer yolu önerir.
    *   **Tetiklenme**: Kullanıcı tarafından manuel olarak veya otomasyon sürecinin ilk adımı olarak çağrılır.

3.  **Öğrenme Planı Agent (`plan_agent.py`)**:
    *   **Görevi**: Kullanıcının belirttiği bir kariyer hedefi için, CV'sini de göz önünde bulundurarak kişiselleştirilmiş bir öğrenme yol haritası (kaynaklar, projeler, zaman çizelgesi) oluşturur.
    *   **Tetiklenme**: Sadece kullanıcı manuel olarak bir kariyer hedefi girip butona bastığında çalışır.

## 3. Otomasyon Süreci

Uygulama, "Tüm Analiz Sürecini Başlat!" butonu ile tetiklenen basit bir otomasyon akışı içerir. Bu akış, agent'ların belirli bir sırada çalışarak kullanıcıya tek seferde kapsamlı bir rapor sunmasını sağlar.

**Otomasyon Akışı:**

1.  **Başlatma**: Kullanıcı, otomasyon butonuna tıklar.
2.  **Adım 1: Kariyer Analizi**: `app.py`, ilk olarak `career_agent`'ı çağırır. Agent, CV'yi analiz eder ve potansiyel kariyer yollarını üretir. Sonuç ekrana yazdırılır.
3.  **Adım 2: SWOT Analizi**: Kariyer analizi tamamlandıktan sonra, `app.py` bu sefer `swot_agent`'ı çağırır. Agent, aynı CV üzerinden SWOT analizini yapar ve sonucu ekrana yazdırır.
4.  **Sonuç**: Kullanıcı, tek bir tıklama ile hem kariyer önerilerini hem de kişisel SWOT analizini almış olur. Bu, manuel olarak iki farklı butona basma ihtiyacını ortadan kaldırarak süreci otomatize eder.