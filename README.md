# Astro-Image-Pipeline
A Python-based image processing pipeline for enhancing amateur astrophotography. It improves deep-sky images by combining BM3D denoising, histogram stretching, and unsharp masking.


<div align="center">

[ 🇬🇧 English ](#-english) | [ 🇹🇷 Türkçe ](#-türkçe)

</div>

---

## 🇬🇧 English

# 🌌 Amateur Astronomy - Image Processing Pipeline

This project is a Python-based image processing pipeline developed to overcome the disadvantages of amateur astrophotography, such as urban light pollution and CMOS sensor noise. It is specifically designed to enhance raw stacked images from compact smart telescopes like the Seestar S50, clean the gray background, and highlight celestial objects.

### 🖼️ Before and After

| Original (Gray and Pale) | Sharpened, Clean, and Black Space |
| :---: | :---: |
| ![Original](gorsel_1.png) | ![Processed](temiz_uzay_1.png) |
| *Raw image, gray and noisy due to light pollution.* | *Result after BM3D denoising and black point adjustment.* |

### 🚀 Features and Algorithm Steps

The script performs three main operations sequentially with a single function call:

1. **Denoising with BM3D (Block Matching 3D):**
   Finds similar small blocks in the image, stacks them into a 3D array, and suppresses noise using frequency transformation. It cleans up fine grain while preserving star and nebula edges.
2. **Histogram Stretching & Black Point Adjustment:**
   Fixes the histogram that clusters at low values due to light pollution. It redefines the bottom 15% of brightness (default `black_point = 15`) as true black. Additionally, to prevent core blowout in high dynamic range targets (e.g., the Orion Nebula), the upper percentile is limited to 99.9%.
3. **Unsharp Masking (Sharpening):**
   The image is blurred using the Gaussian algorithm (`sigma = 2.0`) and blended with the original image to sharpen edges. Stars are made more pinpoint, and blooming artifacts are prevented by clipping the values between 0.0 and 1.0.

### 🛠️ Requirements and Installation

You need the following Python libraries to run the project:

```bash
pip install opencv-python numpy matplotlib scikit-image bm3d
