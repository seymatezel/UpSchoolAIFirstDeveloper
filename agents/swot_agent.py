# swot_agent.py (GÜNCELLENMİŞ)

import streamlit as st  # <- 1. EKLENEN SATIR
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field 
from langchain.output_parsers import PydanticOutputParser
from typing import List

# Veri yapıları (Bunlar sizde zaten vardı)
class SwotItem(BaseModel):
    anahtar_kelime: str = Field(description="Maddenin özünü özetleyen 1-2 kelimelik anahtar yetkinlik. Örneğin: 'Takım Çalışması', 'Proaktif Olma', 'Teknik Yetkinlik'.")
    kanit: str = Field(description="Bu anahtar kelimeyi destekleyen, CV'den alınan kısa ve doğrudan kanıt cümlesi.")
    yorum: str = Field(description="Bu kanıtın kariyer açısından ne anlama geldiğine dair kısa ve net analist yorumu.")

class SwotAnalysis(BaseModel):
    guclu_yonler: List[SwotItem] = Field(description="Kullanıcının CV'sindeki güçlü yönlerin listesi.")
    gelisim_firsatlari: List[SwotItem] = Field(description="Zayıflık olarak değil, gelişim fırsatı olarak görülen alanların listesi.")
    dikkate_alinmasi_gerekenler: List[SwotItem] = Field(description="Kariyer yolunda dikkat edilmesi gereken potansiyel zorluklar veya tehditler.")
    firsatlar: List[SwotItem] = Field(description="Kullanıcının yetenekleriyle eşleşen potansiyel dış fırsatların listesi.")

@st.cache_data  # <- 2. EKLENEN SATIR
def get_swot_analysis(cv_text: str, api_key: str) -> SwotAnalysis:
    """
    Verilen CV metni için anahtar kelime odaklı yapılandırılmış bir SWOT analizi nesnesi döndürür.
    Bu fonksiyon önbelleğe alınmıştır.
    """
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key, temperature=0.5)
    
    parser = PydanticOutputParser(pydantic_object=SwotAnalysis)

    prompt_template = PromptTemplate(
        template="""
        Sen, son derece zeki ve insan odaklı bir kariyer analistisin. Görevin, sana sunulan CV'yi analiz ederek yapılandırılmış bir SWOT analizi oluşturmak.

        Her bir madde için şu üç adımı izle:
        1.  **Anahtar Kelime (`anahtar_kelime`):** İlk olarak, bulduğun yetkinliği veya durumu özetleyen 1-2 kelimelik bir anahtar kelime belirle. (Örnek: 'Liderlik', 'Teknik Beceri', 'İngilizce Seviyesi'). Bu çok önemli.
        2.  **Kanıt (`kanit`):** Sonra, bu anahtar kelimeyi destekleyen somut kanıtı CV'den bul.
        3.  **Yorum (`yorum`):** Son olarak, bu kanıtın ne anlama geldiğini yorumla.

        Cevabını, istenen JSON formatına birebir uyacak şekilde hazırla.

        {format_instructions}

        CV Metni:
        {cv}
        """,
        input_variables=["cv"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt_template | llm | parser
    response = chain.invoke({"cv": cv_text})
    return response