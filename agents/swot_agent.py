#swot_gent.py
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser

def get_swot_analysis(cv_text: str, api_key: str):
    """
    Verilen CV metni için LangChain kullanarak SWOT analizi yapar.
    """
    # 1. Modeli Tanımla
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key, temperature=0.7)

    # 2. Prompt (Komut) Şablonunu Oluştur
    prompt_template = PromptTemplate.from_template(
        """
        Sen, son derece zeki ve insan odaklı bir kariyer analistisin. Görevin, sana sunulan CV'deki her bir önemli noktayı, bir "Kanıt" ve bir "Yorum" olarak ayrıştırarak sunmaktır. Bu, cevabının çok daha okunabilir ve etkili olmasını sağlayacak. Kesinlikle "Örnek:" kelimesini kullanma.

        **Kullanacağın Format:** Her bir madde için şu ikili yapıyı kullan:
        > **CV'den Kanıt:** "[Buraya CV'den kısa, doğrudan bir alıntı yap. Örneğin: 'Denizbank Denizaşırı Staj Programı'ndaki 5 haftalık deneyim']"
        > **Yorumum:** Bu kanıtın ne anlama geldiğini, adayın hangi yeteneğini gösterdiğini ve neden önemli olduğunu açıkla.

        Lütfen bu formatı SWOT analizinin her bölümü için uygula.

        ### 🎯 **Güçlü Yönler (Strengths)**
        (Buraya CV'den bulduğun güçlü yönler için Kanıt/Yorum çiftlerini ekle)

        ### 💪 **Gelişim Fırsatları (Weaknesses as Opportunities)**
        (Buraya CV'deki potansiyel gelişim alanları için Kanıt/Yorum çiftlerini ekle)

        ### ✨ **Fırsatlar (Opportunities)**
        (Buraya CV'deki yeteneklerle sektördeki fırsatları birleştiren Kanıt/Yorum çiftlerini ekle)

        ### 🤔 **Dikkate Alınması Gerekenler (Threats as Challenges)**
        (Buraya sektördeki zorlukları CV ile ilişkilendiren Kanıt/Yorum çiftlerini ekle)

        CV Metni:
        {cv}
        """
    )

    # 3. Zinciri (Chain) Oluştur: Prompt -> Model -> Çıktı Parser
    chain = prompt_template | llm | StrOutputParser()

    # 4. Zinciri Çalıştır ve Sonucu Döndür
    response = chain.invoke({"cv": cv_text})
    return response