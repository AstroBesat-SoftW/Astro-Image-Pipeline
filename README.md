# Astro-Image-Pipeline
A Python-based image processing pipeline for enhancing amateur astrophotography. It improves deep-sky images by combining BM3D denoising, histogram stretching, and unsharp masking.



```markdown
# 🌌 Amatör Astronomi - Görüntü İşleme Pipeline

[cite_start]Bu proje, kentsel ışık kirliliği ve CMOS sensör gürültüsü gibi amatör astrofotografi dezavantajlarını aşmak için geliştirilmiş Python tabanlı bir görüntü işleme ardışık düzenidir (pipeline)[cite: 13, 15]. [cite_start]Özellikle Seestar S50 gibi kompakt akıllı teleskopların ham yığınlanmış (stacked) görüntülerini iyileştirmek, gri arka planı temizlemek ve gök cisimlerini belirginleştirmek için tasarlanmıştır[cite: 14, 68].

## 🖼️ Öncesi ve Sonrası

| Orijinal (Gri ve Solgun) | Keskinleştirilmiş, Temiz ve Siyah Uzay |
| :---: | :---: |
| ![Orijinal](gorsel_1.png) | ![İşlenmiş](temiz_uzay_1.png) |
| *Işık kirliliği nedeniyle grileşmiş ve gürültülü ham görüntü.* | *BM3D ile temizlenmiş, siyah noktası ayarlanmış sonuç.* |

## 🚀 Özellikler ve Algoritma Adımları

[cite_start]Script, tek bir fonksiyon çağrısı ile üç temel işlemi sırasıyla gerçekleştirir[cite: 22]:

1. **BM3D ile Gürültü Temizleme (Block Matching 3D):**
   [cite_start]Görüntüdeki benzer küçük blokları bularak üç boyutlu bir diziye yığar ve frekans dönüşümü ile gürültüyü bastırır[cite: 37]. [cite_start]İnce kumlanmayı temizlerken yıldız ve nebula kenarlarını korur[cite: 39].
2. **Histogram Germe ve Siyah Nokta (Black Point) Ayarı:**
   [cite_start]Işık kirliliğinden dolayı düşük değerlerde yığılan histogramı düzenler[cite: 42]. [cite_start]Parlaklığın alt %15'lik dilimini (varsayılan `black_point = 15`) gerçek siyah olarak yeniden tanımlar[cite: 43]. [cite_start]Ayrıca yüksek dinamik aralığa sahip (örn. Orion Nebulası) hedeflerde çekirdek patlamasını önlemek için üst persentil %99.9 olarak sınırlandırılmıştır[cite: 58, 59].
3. **Unsharp Masking (Keskinleştirme):**
   [cite_start]Görüntü Gaussian algoritması ile bulanıklaştırılır (`sigma = 2.0`) ve orijinal görüntü ile ağırlıklı olarak karıştırılarak kenarlar sivriltilir[cite: 46]. [cite_start]Yıldızlar daha nokta benzeri hale getirilirken, 0-1 aralığında kırpılarak (clipping) parlama artefaktları engellenir[cite: 47].

## 🛠️ Gereksinimler ve Kurulum

Projeyi çalıştırmak için aşağıdaki Python kütüphanelerine ihtiyacınız vardır:

```bash
pip install opencv-python numpy matplotlib scikit-image bm3d
```

## 💻 Kullanım

Ana fonksiyon olan `astro_black_point_and_denoise`, özelleştirilebilir parametreler sunar. Projenize dahil edip aşağıdaki gibi kullanabilirsiniz:

```python
from main import astro_black_point_and_denoise

# Temel Kullanım
astro_black_point_and_denoise(
    input_path="gorsel_1.png", 
    output_path="temiz_uzay_1.png", 
    noise_std=0.10,        # BM3D gürültü yoğunluğu
    black_point=15,        # Arka plan siyah nokta persentili
    sharpen_amount=1.2     # Unsharp Masking katsayısı
)
```

### Parametre İpuçları:
* [cite_start]**Çok gürültülü görsellerde:** `noise_std` değerini `0.15 - 0.20` bandına çıkarabilirsiniz[cite: 40].
* **Keskinlik ayarı:** Varsayılan `sharpen_amount` 1.2'dir. Görüntü çok keskin gelirse 0.8'e düşürebilir veya yapıları daha da belirginleştirmek için 1.5 - 2.0 arasına çıkarabilirsiniz.

## ⚠️ Sınırlandırmalar

* [cite_start]**İşlem Süresi:** BM3D algoritması, yüksek çözünürlüklü görüntülerde işlemci gücüne bağlı olarak birkaç dakika sürebilir[cite: 62].
* [cite_start]**Uydu İzleri:** Bu pipeline uydu izlerini temizlemez; bunun için yığınlama (stacking) aşamasında sigma-clipping gibi yöntemler uygulanmalıdır[cite: 62].
* [cite_start]**Halka Artefaktları:** `sharpen_amount` değerinin çok yüksek (>1.8) tutulması, parlak yıldızların etrafında siyah halkalar (ringing artifact) oluşmasına neden olabilir[cite: 63].

## 🔮 Gelecek Planları

[cite_start]Projeye ilerleyen aşamalarda şu özelliklerin eklenmesi planlanmaktadır[cite: 66]:
- Boş arka plan bölgesinden otomatik gürültü tahmini.
- Richardson-Lucy dekonvolüsyonu ile daha keskin PSF elde edilmesi.
- Renk kalibrasyonu için referans yıldızı kullanımı.

---
**Geliştirici:** Besat Arif Çıngar
```
