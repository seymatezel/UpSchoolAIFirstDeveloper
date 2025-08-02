#plan_agent.py
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser

def get_learning_plan(cv_text: str, career_choice: str, api_key: str):
    """
    Seçilen kariyer ve CV'ye göre LangChain kullanarak kişisel bir öğrenme planı oluşturur.
    """
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key, temperature=0.6)

    prompt_template = PromptTemplate.from_template(
        """
        Sen, bir öğrencinin mevcut durumunu anlayan ve onu hedefine ulaştırmak için en verimli yolu çizen kişisel bir mentorsun.
        
        **EN ÖNEMLİ GÖREVİN:** Bu öğrenme planını oluştururken, kullanıcının CV'sindeki **mevcut yetenekleri** ile hedeflediği **'{kariyer}'** rolü için gereken yetenekler arasındaki **boşluğu (gap)** analiz et. Planın, bu boşluğu kapatmaya yönelik olmalı. Kullanıcının zaten bildiği konuları atla ve doğrudan eksiklerini tamamlamaya odaklan.
        
        Cevabına, kullanıcıyla doğrudan bağ kuran kişisel bir girişle başla.

        ### 🗺️ **'{kariyer}' Olma Yol Haritanız**

        > Merhaba! CV'nizi inceledim ve hedefiniz olan '{kariyer}' rolü için harika bir temeliniz olduğunu gördüm. Özellikle **[Buraya CV'den pozitif bir örnek ekle, örn: "SQL bilginiz"]** sizi bir adım öne taşıyor. Şimdi bu temelin üzerine eksik parçaları ekleyerek sizi bu hedefe hazırlayalım. İşte size özel hazırladığım plan:

        #### **Aşama 1: Mevcut Bilgiyi İleri Taşıma**
        *   **Görev:** CV'nizde belirttiğiniz **[CV'den bir yetenek ekle]** yeteneğini, **[İleri seviye bir konu ekle]** ile bir üst seviyeye çıkarın.
        *   **Kaynak Önerisi:** [Bu ileri seviye konu için spesifik bir kaynak.]
        *   **Neden Önemli?** Bu, sizi başlangıç seviyesinden orta seviyeye taşıyacak kritik bir adımdır.

        #### **Aşama 2: Eksik Kritik Yeteneği Kazanma**
        *   **Görev:** '{kariyer}' rolü için olmazsa olmaz olan ama CV'nizde göremediğim **[Eksik olan kritik bir yetenek ekle, örn: bir bulut platformu (AWS/Azure)]** konusunda temel yetkinlik kazanın.
        *   **Kaynak Önerisi:** [Bu yeni yetenek için bir başlangıç kursu veya projesi.]
        *   **Neden Önemli?** Günümüz iş ilanlarının büyük çoğluğu bu yetkinliği aramaktadır.

        #### **Aşama 3: Portfolyoyu Güçlendirme**
        *   **Görev:** Öğrendiğiniz bu yeni becerileri birleştiren, baştan sona bir proje geliştirin. Bu proje, **[Proje fikri, örn: AWS üzerinde çalışan ve verileri analiz eden bir web uygulaması]** olabilir.
        *   **Kaynak Önerisi:** [Benzer projelerin olduğu bir GitHub reposu veya bir blog yazısı.]
        *   **Neden Önemli?** Bu proje, mülakatlarda gösterebileceğiniz en somut başarınız olacaktır.

        > Bu plan, sizin mevcut durumunuza göre optimize edilmiştir. Unutmayın, önemli olan hız değil, istikrarlı ilerlemedir. Başarılar!

        ---
        Kullanıcının CV Metni:
        {cv}
        """
    )
    chain = prompt_template | llm | StrOutputParser()
    response = chain.invoke({"cv": cv_text, "kariyer": career_choice})
    return response