# Makaleden Hayata

@dytdemirhaner için kaynaklı Türkçe bilim içerikleri ve özgün veri kartları.

Her gün Türkiye saatiyle 06.17'de bulutta çalışır; 10.00, 13.00, 17.00 ve 20.00 için en fazla dört eksik gönderiyi Buffer'a kaydeder. Bilgisayarın açık olması gerekmez. GitHub zamanlayıcısı gecikebilir; yayın saatleri Buffer'a önceden kaydedilir. Kuyruk 10 gönderiyi aşmaz, mevcut gönderiler değiştirilmez.

## Gizli ayarlar

GitHub Actions Secrets: `GEMINI_API_KEY`, `BUFFER_API_KEY`. Anahtarları dosyaya veya çıktıya yazmayın. Buffer anahtarı 25 Ekim 2027'de sona erer; önceden yenileyin. Ücretli plan veya faturalandırma açmayın. Kota dolduğunda görev hata verir; ücretli modele geçmez.

## Kontroller

Actions → Makaleden Hayata → Run workflow → önce `check`, sonra `preview`, en son `publish`. `check` gönderi oluşturmaz. `preview` bilimsel kontrolden geçen bir metin ve görseli üretir. `publish` gerçek gönderileri zamanlar. Yayın hataları Actions çalışmasını başarısız yapar; GitHub bildirim ayarlarınızı kontrol edin.

Europe PMC/PubMed kayıtlarından erişilen özetler kullanılır. Bir üretim ve bağımsız eleştirel kontrol yapılır; kısa kanıt alıntıları özetle birebir eşleştirilir. Bunlar hatasızlık garantisi değildir. Kaynak doğrulanamazsa, kontrol başarısızsa veya belirsiz önceki bir yazma işlemi varsa yayın durur. Çalışma tasarımı, örneklem, karşılaştırma ve sınırlılıklar korunur. Gözlemsel ilişki nedensellik olarak sunulmaz. Sayı kartı kullanılır; kaynakta olmayan grafik verisi üretilmez.

Görseller, kod ve yayın kaynak kayıtları herkese açıktır. Anahtarlar yalnız Secrets'tadır. Gemini ücretsiz katmanı gönderilen açık bilim özetlerini ve içerik taslaklarını ürün geliştirme için kullanabilir. Kişisel/özel veri modele gönderilmez.

Resmi kaynaklar: [Buffer API](https://developers.buffer.com/), [Gemini](https://ai.google.dev/api/generate-content), [GitHub Actions](https://docs.github.com/en/actions).
