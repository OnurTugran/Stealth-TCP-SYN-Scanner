# -*- coding: utf-8 -*-
from scapy.all import IP, TCP , sr1 , send
import sys

#Fecade Kalıbı kullanarak  ağ dinleme işlerini bu sınıfın içine gizliyoruz

class StealthScanner:

    def __init__(self, target_ip):
        self.target_ip = target_ip

    def scan_port(self, port):
        print(f"[*] Port {port} taranıyor (Hedef: {self.target_ip})...")

        #IP katmanını oluşturuyoruz
        ip_layer = IP(dst=self.target_ip)

        #Tcp SYN paketi oluşturuyoruz
        tcp_layer = TCP(dport=port , flags="S")

        packet = ip_layer / tcp_layer

        # Paketi gönderip cevap bekliyoruz
        response = sr1(packet, timeout=2, verbose=0)

        if response is None:
            return "Filtrelemiş/Kapalı (Güvenlik Duvarı Olabilir)"

        elif response.haslayer(TCP):
            #Eğer TCP katmanı varsa ve SYN-ACK bayrağı set edilmişse port açıktır
            if response.getlayer(TCP).flags == 0x12:

                #İzi silmek için RST paketi gönderiyoruz
                rst_packet = IP(dst=self.target_ip) / TCP(dport=port, flags="R")
                send(rst_packet, verbose=0)
                return "Açık"

            elif response.getlayer(TCP).flags == 0x14:
                return "Kapalı"

        return "Bilinmeyen Durum"

if __name__ == "__main__":
    # Test için kendi izole Docker ağındaki veya VirtualBox'taki hedef IP'yi buraya yaz
    HEDEF_IP = "127.0.0.1" # Kendi lab IP'n ile değiştir
    TEST_PORTLARI = [21, 22, 80, 443, 8080]
    
    # Facade sınıfından nesnemizi üretiyoruz
    scanner = StealthScanner(HEDEF_IP)
    
    print("-" * 40)
    print("KIRMIZI TAKIM: SYN Tarayıcı Başlatıldı")
    print("-" * 40)
    
    for port in TEST_PORTLARI:
        sonuc = scanner.scan_port(port)
        print(f"--> Port {port}: {sonuc}")