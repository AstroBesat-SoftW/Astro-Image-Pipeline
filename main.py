import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.exposure import rescale_intensity
import bm3d

# algoitmalardan sadece 1 tanesi de denenebilir. örnek olarak ben 3 tane ekledim ve bu kaliteye göre yavaş sonuç verebiliyor.

def astro_black_point_and_denoise(input_path, output_path, noise_std=0.10, black_point=15, sharpen_amount=1.2):
    # 1. Görseli Oku, Normalize Et (0-1) ve RGB'ye Çevir
    img = cv2.imread(input_path)
    if img is None:
        print(f"Hata: {input_path} bulunamadı. Lütfen dosya yolunu kontrol edin.")
        return
        
    img_float = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0

    print(f"[{input_path}] 1. Adım: Gürültü temizleniyor (Bu işlem biraz sürebilir)...")
    
    # 2. BM3D Gürültü Azaltma (Kumlanmayı pürüzsüzleştirir)
    denoised = bm3d.bm3d(img_float, sigma_psd=noise_std, stage_arg=bm3d.BM3DStages.ALL_STAGES)

    print(f"[{input_path}] 2. Adım: Arka plan siyah noktası ayarlanıyor ve yıldızlar parlatılıyor...")
    
    # 3. Siyah Nokta (Black Point) Ayarı ve Germe
    lower_bound = np.percentile(denoised, black_point)
    upper_bound = np.percentile(denoised, 99.9) 

    # Sinyali yeni sınırlara göre ger
    enhanced = rescale_intensity(denoised, in_range=(lower_bound, upper_bound), out_range=(0.0, 1.0))

    print(f"[{input_path}] 3. Adım: Gerçekçi keskinleştirme (Unsharp Masking) uygulanıyor...")
    
    # --- YENİ EKLENEN KESKİNLEŞTİRME ADIMI ---
    # Görseli hafifçe bulanıklaştırıyoruz (sigma=2.0)
    blurred = cv2.GaussianBlur(enhanced, (0, 0), 2.0)
    # Orijinal gerilmiş görüntü ile bulanık görüntüyü harmanlayarak kenarları (yıldızları) sivriltiyoruz
    sharpened = cv2.addWeighted(enhanced, 1.0 + sharpen_amount, blurred, -sharpen_amount, 0)
    # İşlem sonrası piksellerin 0-1 sınırını aşmasını (bembeyaz patlamaları veya kapkara hataları) engelliyoruz
    sharpened = np.clip(sharpened, 0.0, 1.0)
    # ------------------------------------------

    # 4. Görüntüyü 8-bit formatına geri çevir ve kaydet (Artık 'sharpened' değişkenini kullanıyoruz)
    final_img_uint8 = (sharpened * 255.0).astype(np.uint8)
    final_bgr = cv2.cvtColor(final_img_uint8, cv2.COLOR_RGB2BGR)
    cv2.imwrite(output_path, final_bgr)
    
    print(f"[{input_path}] İşlem tamamlandı! Sonuç şuraya kaydedildi: {output_path}\n")

    # 5. Karşılaştırmalı Gösterim
    plt.figure(figsize=(16, 8))
    
    plt.subplot(1, 2, 1)
    plt.title('Orijinal (Gri ve Solgun) Görüntü')
    plt.imshow(img_float)
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.title('Keskinleştirilmiş, Temiz ve Siyah Uzay')
    plt.imshow(sharpened)
    plt.axis('off')

    plt.tight_layout()
    plt.show()

# Kodu çalıştırmak için:
# 'sharpen_amount' varsayılan olarak 1.2'dir. Çok keskin gelirse 0.8'e düşürebilir, 
# daha da belirginleştirmek istersen 1.5 - 2.0 arasına çıkarabilirsin.
astro_black_point_and_denoise("gorsel_1.png", "temiz_uzay_1.png", noise_std=0.10, black_point=15, sharpen_amount=1.2)

astro_black_point_and_denoise("gorsel_3.png", "temiz_uzay_3.png", noise_std=0.10, black_point=15, sharpen_amount=1.2)
astro_black_point_and_denoise("gorsel_4.png", "temiz_uzay_4.png")
astro_black_point_and_denoise("gorsel_5.png", "temiz_uzay_5.png") 
astro_black_point_and_denoise("gorsel_6.png", "temiz_uzay_6.png")
