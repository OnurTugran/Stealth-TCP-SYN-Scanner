# Stealth-TCP-SYN-Scanner

##  🕵️‍♂️ Stealth TCP SYN Scanner (Gizli Port Tarayıcı)

**Bu proje, hedef sistemlerdeki açık portları tespit etmek için tam bir TCP bağlantısı (3-way handshake) kurmak yerine, gizlilik odaklı (stealth) SYN paketleri kullanan nesne yönelimli (OOP) bir port tarayıcıdır.**

---
#### Sistemin Çalışma Mantığı ve Mimarisi:
- Temel Bağımlılıklar: Ağ paketlerini manipüle etmek için scapy.all kütüphanesinden IP, TCP, sr1, ve send modülleri ile sistem argümanları için sys kütüphanesi sisteme entegre edilmiştir.

- Nesne Yönelimli Yapı (OOP): Kodun modülerliği ve tekrar kullanılabilirliği için sistem bir Class (Sınıf) yapısı üzerine inşa edilmiştir. Constructor (Yapıcı metod) başlatıldığında, hedefin IP adresi sınıfa tanımlanır.

* Paket İnşası (Packet Crafting): scan_port fonksiyonu çağrıldığında, Scapy kullanılarak iki katmanlı bir ağ paketi oluşturulur:
 * Network Layer (Ağ Katmanı): Hedef IP adresi IP() katmanına yerleştirilir.
 * Transport Layer (Taşıma Katmanı): Taranacak hedef port numarası ve SYN bayrağı TCP() katmanına tanımlanır.
 * Son olarak bu iki katman (IP / TCP) birbirine kapsüllenerek (encapsulation) hedefe gönderilmeye hazır hale getirilir.


*  Durum Analizi ve Gizlilik (Stealth Logic):
 *  Cevap Yoksa (Timeout): Port "Filtrelenmiş" (Filtered) olarak kabul edilir.Muhtemelen bir Güvenlik Duvarı (Firewall) paketi sessizce düşürmüştür.

 *  0x12 (SYN-ACK) Dönerse: Portun Açık (Open) olduğu anlaşılır. Sistemin loglarında iz bırakmamak ve bağlantıyı açık bırakmamak adına, anında bir RST (Sıfırlama) paketi gönderilerek bağlantı sessizce sonlandırılır.

 * 0x14 (RST-ACK) Dönerse: Portun Kapalı (Closed) olduğu tespit edilir.

---


 *  Ana Döngü (Main Execution): Programın ana bloğunda hedef IP ve taranacak port havuzu belirlenir. Tarayıcı nesnesi (Scanner Object) örneklendirilerek, belirlenen portlar bir for döngüsü içerisinde sırasıyla analiz edilir.
