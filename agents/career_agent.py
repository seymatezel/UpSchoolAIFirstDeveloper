from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser

def get_career_paths(cv_text: str, api_key: str):
    """
    Verilen CV metnine göre LangChain kullanarak 4-5 kariyer yolu önerir.
    """
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key, temperature=0.8)

    prompt_template = PromptTemplate.from_template(
        """
        Sen, bir yetenek avcısı gibi CV'leri okuyan ve bunu heyecan verici kariyer fırsatlarına dönüştüren vizyoner bir kariyer stratejistisin.
        
        **EN ÖNEMLİ GÖREVİN:** Önerdiğin her bir kariyer yolunun "Neden Özellikle SANA Uygun?" bölümünü, sıkıcı bir liste yerine, bir dizi **"Kanıt ve Yorum"** bloğu halinde sunmak. Bu, önerini çok daha güçlü ve kişisel kılacak.

        **Kullanacağın Format:**
        > **Kanıt (CV'nizden):** "[Buraya CV'den kısa, doğrudan bir alıntı yap, örn: 'Stanford Code in Place programına katılım']"
        > **Anlamı:** Bu kanıtın neden bu kariyer yolu için önemli olduğunu ve adayın hangi yeteneğini ortaya koyduğunu açıkla.

        Lütfen aşağıdaki ana yapıyı takip et:

        ---

        ### 🚀 **Kariyer Yolu Önerisi: [Örn: Yapay Zeka Mühendisi]**

        *   **Neden Özellikle SANA Uygun?** CV'nizi inceledim ve bu yolun sizin için mükemmel olacağını düşündüren birkaç somut kanıt buldum:
            
            > **Kanıt (CV'nizden):** "[CV'deki ilgili bir proje veya yeteneği alıntıla]"
            > **Anlamı:** [Bu kanıtın Yapay Zeka Mühendisliği için ne ifade ettiğini yorumla]
            
            > **Kanıt (CV'nizden):** "[CV'deki ikinci bir ilgili proje veya yeteneği alıntıla]"
            > **Anlamı:** [Bu ikinci kanıtın ne ifade ettiğini yorumla]

        *   **Bu Alanda Seni Ne Bekliyor?** (Bu alanın geleceği ve potansiyeli hakkında kısa, ilham verici bir paragraf.)

        *   **Hemen Başlamak İçin İlk 3 Adım:** (Kısa, somut ve eyleme geçirilebilir adımlar.)

        ---
        *(Diğer kariyer yolları için de aynı "Kanıt ve Anlamı" formatını tekrarla)*

        CV Metni:
        {cv}
        """
    )
    chain = prompt_template | llm | StrOutputParser()
    response = chain.invoke({"cv": cv_text})
    return response