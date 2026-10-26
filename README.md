# Makaleden Hayata

@dytdemirhaner için ücretsiz GitHub Actions + Gemini + Buffer bulut akışı. Türkiye saatiyle 10, 13, 17 ve 20 için kaynaklı bilim içerikleri. Yeni içerikler üç gönderilik bağlı X zinciri olarak hazırlanır; ilk gönderide özgün bilgi kartı, ilk ve son gönderide kaynak bağlantısı bulunur. Anlatım: soru/baglam, araştırmanın güçlü bulgusu ve sayısal verisi, açıkça ayrılan kişisel editoryal yorum ve sınırlılık. Sahte deneyim, hasta hikâyesi veya kanıtsız vaat oluşturulmaz.

Buffer Free yalnız bir zinciri aynı anda kuyrukta tutar. Bu nedenle görev sıradaki boş saate bir zincir ekler; yayımlandıktan sonra takip eden çalışmada sıradakini planlar. Eski tek gönderiler korunur. GitHub zamanlayıcısı gecikebilir; ücretsiz hizmetler kesintisizlik garantisi vermez.

## Çalışma saatleri — Europe/Istanbul

- 06.17: durum kontrolü ve sıradaki zinciri hazırlama.
- 09.15: ilk saat için kuyruk kontrolü ve gerekiyorsa hazırlama.
- 10.45, 13.45, 17.45, 20.45: gerçekleşen yayını kontrol et, sıradaki zinciri ekle.
- Her gün 23.30: gönderi ölçümlerini kaydet.
- Pazar 23.45: haftalık rapor ve temkinli içerik değerlendirmesi.

Kontrol, üretimden önce ayrı adımda çalışır; hata kontrolü sıradaki gönderinin hazırlanmasını engellemez. Yayın veya üretim hatası görev sonucunu başarısız yapar; GitHub için başarısız çalışma e-posta bildirimi açıktır. `CLOUD_ENABLED=true` takvimli çalışmaları etkinleştirir.

## Secrets ve izinler

`GEMINI_API_KEY`, `BUFFER_API_KEY`, `BUFFER_INSIGHTS_KEY`. Ücretsiz tek Buffer anahtarı iki Secret alanında saklanır: account:read, posts:read, posts:write, insights:read. Anahtar 26 Ekim 2027'de sona erer. Anahtarları dosyaya veya loglara yazmayın. Ücretli plan/deneme/faturalandırma etkinleştirilmez.

## Performans ve raporlar

`analytics/snapshots.json`: tarihli gönderi kökü metrikleri; `analytics/latest-weekly.md`: son rapor; `analytics/weekly-YYYY-MM-DD.md`: arşiv; `analytics/editorial.json`: gelecek hafta denenebilecek anlatım tercihi. Raporlar Actions iş özetinde ve bu dosyalarda otomatik oluşur; haftalık rapor için ayrı e-posta gönderimi kurulmadı.

Eksik veri sıfır değildir. Buffer verileri günlük yenilenir; yeni gönderilerde boş ölçüm olabilir. Zincir kökü ölçümleri tüm zincirin toplamı sayılmaz. Kararlar için ilk 24–48 saatlik gözlem alınır; en az iki anlatım biçiminde beşer tam ölçüm ve belirlenmiş fark eşiği olmadan otomatik tercih değişmez. Çıkarım nedensel değildir. Tercih süresi sekiz günle sınırlıdır ve günde en çok bir zincirde uygulanır; kanıt kalitesi korunur.

**Takipçi kısıtı:** Kamuya açık belgelenmiş Buffer API, toplam takipçi sayısını sunmuyor. Son 683 takipçi gözlemi (26 Ekim 2026) canlı Insights ekranından elle doğrulandı. Bunun güncel bir otomatik seri olduğu iddia edilmez; yeni gerçek gözlem olmadan net takipçi artışı hesaplanmaz. Hedef 24 Kasım sonunda 2.683 toplam takipçi (+2.000 net), garanti değildir.

## Kontroller

Run workflow modları: check (bağlantı), preview (üç metin ve görsel, yayın yok), publish (gerçek zamanlama), monitor (yayın denetimi), cycle (denetim ve sıradaki zincir), analytics (gönderi metrikleri), report (haftalık rapor), alert-test (gönderilere dokunmayan kasıtlı hata).

Bilimsel kontrol: erişilen Europe PMC/PubMed özeti, konu filtresi, birebir kısa kanıt alıntıları, bağımsız model eleştirisi; oran/odds/risk ve belirsizlik korunur. Bunlar hatasızlık garantisi değildir. Belirsiz bir Buffer yazması körlemesine tekrarlanmaz. Görseller ve açık kaynak kayıtları herkese açıktır; Secrets gizlidir. Gemini'ye yalnız açık makale özetleri ve içerikler gönderilir.
