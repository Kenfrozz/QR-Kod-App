# QR Kod Üretici ve Okuyucu

Bu proje, **Python** ve **PyQt5** kullanarak geliştirilmiş bir QR kod oluşturucu ve okuyucu uygulamasıdır. Kullanıcılar, uygulama üzerinden metin veya URL gibi verileri QR koda dönüştürebilir ve QR kod içeren resim dosyalarından verileri okuyabilirler.

## Özellikler

- **QR Kod Oluşturma:** Girilen metin veya URL'yi QR koda dönüştürün ve PNG formatında kaydedin.
- **QR Kod Okuma:** QR kod içeren bir resim dosyasını seçerek içerisindeki veriyi tespit edin.
- **Grafiksel Arayüz:** PyQt5 tabanlı modern ve kullanıcı dostu arayüz ile kolay kullanım.

## Gereksinimler

Projenin çalışması için aşağıdaki Python kütüphanelerine ihtiyaç vardır:

- Python 3.x
- [qrcode](https://pypi.org/project/qrcode/) (PIL desteğiyle birlikte)
- [Pillow (PIL)](https://pypi.org/project/Pillow/)
- [pyzbar](https://pypi.org/project/pyzbar/)
- [PyQt5](https://pypi.org/project/PyQt5/)

> **Not:** `pyzbar` kütüphanesi, sisteminizde [ZBar](https://github.com/ZBar/ZBar) kütüphanesinin kurulu olmasını gerektirebilir. İşletim sisteminize göre ZBar kurulumuna ilişkin dokümantasyonu inceleyiniz.
