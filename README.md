# Kent Kafe – Marka Stratejisi Simülatörü

Üniversite öğrencilerinin bir ilçe belediyesine ait kafede marka yöneticisi rolünü üstlenerek stratejik kararların marka, finans ve toplumsal erişilebilirlik üzerindeki etkilerini incelemesi için hazırlanmış etkileşimli bir Streamlit uygulamasıdır.

Uygulama; marka kimliği seçimi, fiyat politikası, hizmet kalitesi yatırımı ve tanıtım bütçesi kararlarını karşılaştırır. Kural Tabanlı Strateji Danışmanı, seçilen kararlara göre açıklanabilir öneriler sunar. Harici bir yapay zekâ servisi, API anahtarı, veritabanı veya kullanıcı girişi kullanılmaz.

Öğrenciler her ay için strateji, fiyat, kalite ve bütçe kararlarını değiştirip **Bir Ay İlerle** seçeneğiyle sonuçları kaydedebilir. Simülasyon en fazla altı ay sürer; aylık finans sonuçları ve marka göstergeleri grafiklerle izlenir. Karşılaştırma bölümü, üç konumlandırmayı aynı karar varsayımları altında değerlendirir.

Uygulama açıldığında dört temel göstergenin ve marka sağlığı puanlarının yer aldığı **Yönetim Paneli** görüntülenir. Sol navigasyondan Marka Kimliği, Stratejik Kararlar, Aylık Simülasyon, Performans Analizi ve Strateji Danışmanı bölümlerine geçilir. Marka kimliği sayfasında stratejiler renk kodlu seçim kartlarıyla sunulur.

## Gereksinimler

- Python 3.11 veya üzeri
- `requirements.txt` dosyasındaki Streamlit ve Plotly kütüphaneleri

## Yerel Çalıştırma

Proje klasöründe aşağıdaki komutları çalıştırın:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

Windows'ta sanal ortamı etkinleştirmek için `.venv\Scripts\activate` komutunu kullanın. Uygulama tarayıcıda genellikle `http://localhost:8501` adresinde açılır.

## Başlangıç Senaryosu

- Marka: Kent Kafe
- Strateji: Sosyal ve Ekonomik
- Fiyat politikası: Çok uygun
- Hizmet kalitesi yatırımı: 3/5
- Aylık tanıtım bütçesi: 20.000 TL
- Hedef kitle: Öğrenciler, emekliler ve aileler
- Marka vaadi: Herkesin Kafesi

Başlangıç senaryosunda model puanları Marka Gücü 86,0, Finansal Denge 46,0 ve Toplumsal Erişilebilirlik 74,0 olarak hesaplanır. Aylık finans tahmini 2.700 müşteri, 106 TL ortalama harcama, 286.200 TL ciro, 285.084 TL toplam gider ve 1.116 TL faaliyet sonucu gösterir.

## Simülasyon Varsayımları

Tüm veriler eğitim amacıyla kullanılan varsayımsal verilerdir; gerçek belediye verisi kullanılmaz. Stratejilerin erişilebilirlik ve marka gücü temel puanları şöyledir:

| Strateji | Erişilebilirlik temel puanı | Marka gücü temel puanı |
| --- | ---: | ---: |
| Sosyal ve Ekonomik | 80 | 70 |
| Yerel ve Özgün | 66 | 86 |
| Modern ve Kaliteli | 58 | 75 |

Fiyat politikası indeksi Çok uygun için 0'dan Premium için 4'e kadar ilerler. Kalite yatırımı 1–5, tanıtım bütçesi 0–50.000 TL aralığındadır. Hesaplama formülleri:

- Erişilebilirlik = strateji erişilebilirlik temel puanı − (fiyat indeksi × 9) − (kalite yatırımı × 2)
- Finansal Denge = 55 + (fiyat indeksi × 11) − (kalite yatırımı × 5) + (tanıtım bütçesi / 10.000 × 3)
- Marka Gücü = strateji marka gücü temel puanı + (kalite yatırımı × 4) + (tanıtım bütçesi / 10.000 × 2)

Sonuçlar 0–100 aralığında sınırlandırılır. Bütçe etkisi hesaplamalarda kesirli değerlerle korunur, ekranda bir ondalık basamakla gösterilir. Bu formüller bilimsel olarak doğrulanmış tahmin modelleri değil, kararlar arasındaki ilişkileri öğretmek için tasarlanmış basitleştirilmiş bir simülasyondur.

### Aylık Finans Varsayımları

Finans modeli de yalnızca eğitim için belirlenmiş sentetik katsayılar kullanır. Fiyat indeksi Çok uygun için 0, Premium için 4'tür.

- Aylık müşteri = en az 0 olacak şekilde yuvarla(2.700 + (Marka Gücü − 86) × 18 + (Erişilebilirlik − 74) × 10 + ((bütçe − 20.000) / 5.000) × 40)
- Ortalama harcama = 100 TL + fiyat indeksi × 18 TL + kalite yatırımı × 2 TL
- Ciro = aylık müşteri × ortalama harcama
- Ürün maliyeti = ciro × (%32 + fiyat indeksi başına 1,5 yüzde puan)
- Personel gideri = 100.000 TL + kalite yatırımı × 10.000 TL
- İşletme gideri = 30.000 TL + aylık müşteri × 5 TL
- Toplam gider = ürün maliyeti + personel gideri + işletme gideri + tanıtım bütçesi
- Faaliyet sonucu = ciro − toplam gider

Faaliyet sonucu pozitif veya negatif olabilir; uygulama sonucu pozitif yapmak için düzeltmez. Tanıtım bütçesi ayrıca müşteri tahmininde de kullanılan basitleştirilmiş talep girdisidir. Her ayın kararları ve sonuçları Streamlit `session_state` içinde saklanır; “Simülasyonu Sıfırla” aylık geçmişi temizler, “Başlangıç Ayarlarına Dön” ise karar kontrollerini başlangıç değerlerine alır. Her kaydedilen ay için üç kısa yönetici değerlendirmesi gösterilir.

Grafikler aylık ciro ve toplam giderleri, faaliyet sonucunu, marka gücünü ve toplumsal erişilebilirliği izler. Alternatif strateji tablosu ve grafikleri mevcut fiyat, kalite ve bütçeyi sabit tutarak strateji etkisini karşılaştırır.

Gider terimleri: **Ciro** satışların toplam parasal değeridir. **Faaliyet sonucu**, olağan işletme gelirleri ile ürün, personel, işletme ve tanıtım giderleri arasındaki farktır. Bu varsayımlar gerçek belediye maliyetlerini veya talebini temsil etmez.

## Streamlit Community Cloud'da Yayımlama

1. Bu dosyaları içeren GitHub deposunu oluşturun veya mevcut depoya gönderin.
2. [share.streamlit.io](https://share.streamlit.io/) adresinden GitHub hesabınızla giriş yapın.
3. **Create app** seçeneğini kullanıp depoyu, dalı ve ana dosya yolu olarak `app.py` değerini belirleyin.
4. Uygulamayı yayımlayın. Bağımlılıklar dağıtım sırasında `requirements.txt` dosyasından kurulur; gizli anahtar veya ek yapılandırma gerekmez.

## Dosyalar

- `app.py`: Arayüz, simülasyon hesaplamaları, danışman kuralları ve TXT raporu
- `requirements.txt`: Python bağımlılıkları
- `.gitignore`: Yerel ve geçici dosyalar için Git kuralları
