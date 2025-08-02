# RAG (Retrieval-Augmented Generation) Modülü

Bu modül, kullanıcının yüklediği bir PDF belgesi üzerinden soruları yanıtlayan bir yapay zeka sistemidir. Mevcut "AI Kariyer Koçu" projesine entegre edilmiştir.

## Amaç

Genel amaçlı dil modellerinin (LLM) bilgi dağarcığını, kullanıcı tarafından sağlanan spesifik bir belgeyle genişletmektir. Bu sayede model, genel cevaplar yerine, yüklenen PDF'in içeriğine dayalı, bağlama uygun ve doğru yanıtlar üretebilir.

## Kullanılan Teknolojiler

- **Arayüz:** Streamlit
- **Orkestrasyon:** LangChain
- **Dil Modeli (LLM):** Google Gemini (`gemini-1.5-flash`)
- **Embedding Modeli:** Google `embedding-001`
- **Belge Yükleyici:** `PyPDFLoader`
- **Metin Parçalayıcı:** `RecursiveCharacterTextSplitter`
- **Vector Database:** `ChromaDB` (In-memory)

## Çalışma Prensibi

Sistem, standart bir RAG akışını takip eder:

1.  **Belge Yükleme:** Kullanıcı, Streamlit arayüzündeki "Belge Soru-Cevap" sekmesinden bir PDF dosyası yükler.
2.  **Yükleme ve Parçalama (Load & Chunk):** `PyPDFLoader` ile yüklenen PDF içeriği, anlamsal bütünlüğü koruyarak daha küçük metin parçalarına (`chunks`) ayrılır.
3.  **Vektörleştirme (Embedding):** Her bir metin parçası, `GoogleGenerativeAIEmbeddings` kullanılarak sayısal bir vektöre dönüştürülür. Bu vektör, metnin anlamsal özünü temsil eder.
4.  **Depolama (Store):** Oluşturulan bu vektörler, geçici (in-memory) bir `ChromaDB` veritabanında indekslenir. Bu veritabanı, anlamsal benzerlik aramalarını çok hızlı yapabilir.
5.  **Sorgulama ve Cevaplama (Retrieve & Generate):**
    -   Kullanıcı bir soru sorduğunda, bu soru da aynı embedding modeliyle bir vektöre dönüştürülür.
    -   ChromaDB, soru vektörüne en çok benzeyen metin parçalarını (`chunks`) veritabanından bulur (Retrieve).
    -   Bu bulunan parçalar, kullanıcının sorusuyla birlikte Google Gemini modeline "işte bağlamın bu, bu bilgiye göre cevap ver" şeklinde bir komutla gönderilir.
    -   Model, kendisine sağlanan bu bağlamı kullanarak soruyu yanıtlar (Generate).

