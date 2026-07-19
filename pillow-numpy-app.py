import streamlit as st
import numpy as np
from PIL import Image
from pathlib import Path
import matplotlib.pyplot as plt

# ==========================================
# KONFIGURASI HALAMAN & STYLE
# ==========================================
st.set_page_config(
    page_title="Image Preprocessing Explorer",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk memperindah tampilan aplikasi dan mengaktifkan smooth scrolling
st.markdown("""
<style>
    /* Mengaktifkan transisi scroll yang halus */
    html {
        scroll-behavior: smooth;
    }
    .main {
        background-color: #f8f9fa;
    }
    .stAlert {
        border-radius: 10px;
    }
    .css-1r6g72h {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    h1, h2, h3 {
        color: #1e293b;
        font-family: 'Inter', sans-serif;
    }
    .highlight {
        background-color: #e2e8f0;
        padding: 2px 6px;
        border-radius: 4px;
        font-family: monospace;
        font-weight: bold;
    }
    .title-container {
        background: linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%);
        padding: 40px;
        border-radius: 15px;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    
    /* Style khusus untuk link daftar isi di sidebar */
    .sidebar-link {
        display: block;
        padding: 10px 15px;
        color: #334155 !important;
        text-decoration: none !important;
        border-radius: 8px;
        margin-bottom: 8px;
        background-color: #f1f5f9;
        font-weight: 500;
        border-left: 4px solid #cbd5e1;
        transition: all 0.2s ease-in-out;
    }
    .sidebar-link:hover {
        background-color: #e2e8f0;
        border-left: 4px solid #4f46e5;
        transform: translateX(5px);
        color: #0f172a !important;
    }
</style>
""", unsafe_allow_html=True)

# Header Aplikasi
st.markdown("""
<div class="title-container">
    <h1 style="color: white; margin: 0;">🖼️ Image Preprocessing Explorer</h1>
    <p style="color: #e0e7ff; font-size: 1.1rem; margin-top: 10px; margin-bottom: 0;">
        Aplikasi interaktif untuk mempelajari konsep dasar preprocessing gambar dalam Computer Vision.
        Dibuat khusus untuk pemula dengan visualisasi langkah-demi-langkah menggunakan Python, Pillow, dan NumPy.
    </p>
</div>
""", unsafe_allow_html=True)


# ==========================================
# GLOBAL IMAGE LOADING & NUMPY ARRAY INITIALIZATION
# ==========================================
# Mendefinisikan path gambar secara tetap (fixed) sesuai instruksi
image_path = Path("images/sample.jpg")

# Mengecek apakah file gambar ada sebelum dibuka
if not image_path.exists():
    st.error(f"Gambar tidak ditemukan di: {image_path}. Silakan letakkan file gambar 'sample.jpg' di dalam folder 'images/'.")
    st.stop()

# Membuka gambar menggunakan Pillow dan memastikan formatnya RGB
# convert("RGB") digunakan untuk memastikan gambar memiliki 3 channel (Red, Green, Blue)
image = Image.open(image_path).convert("RGB")

# Mengonversi PIL Image menjadi NumPy array.
# Gambar sekarang direpresentasikan sebagai matriks angka multidimensi.
image_array = np.array(image)
height, width, channels = image_array.shape


# ==========================================
# SIDEBAR NAVIGATION (TABLE OF CONTENTS)
# ==========================================
st.sidebar.markdown("### 📚 Daftar Isi Modul")
st.sidebar.markdown("""
<a href="#sec1" class="sidebar-link">1. Load Image & Metadata 📂</a>
<a href="#sec2" class="sidebar-link">2. Convert to NumPy 📊</a>
<a href="#sec3" class="sidebar-link">3. Pixel Inspector 🔍</a>
<a href="#sec4" class="sidebar-link">4. RGB Slicing 🎨</a>
<a href="#sec5" class="sidebar-link">5. Grayscale Conversion 🌓</a>
<a href="#sec6" class="sidebar-link">6. Normalization 📉</a>
<a href="#sec7" class="sidebar-link">7. Preprocessing Pipeline ⚙️</a>
<a href="#sec8" class="sidebar-link">8. Histogram Explorer 📊</a>
<a href="#sec9" class="sidebar-link">9. Resize & Aspect Ratio 📐</a>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.info(
    "Aplikasi ini didesain sebagai modul pembelajaran interaktif. "
    "Klik salah satu bab di atas untuk auto-slide (scroll halus) ke bagian tersebut."
)


# ==========================================
# 1. IMAGE LOADING & METADATA
# ==========================================
st.header("1. Load Gambar & Metadata", anchor="sec1")

# Layout dengan dua kolom: kiri untuk gambar, kanan untuk metadata
col1_img, col2_meta = st.columns([2, 1])

with col1_img:
    st.image(image, caption="Gambar Asli (sample.jpg)", use_container_width=True)

with col2_meta:
    st.subheader("Metadata Gambar (PIL)")
    st.write("Informasi file gambar yang dibaca langsung menggunakan library Pillow:")
    
    # Menampilkan informasi gambar dengan metrik yang rapi
    st.metric(label="Width (Lebar)", value=f"{image.width} px")
    st.metric(label="Height (Tinggi)", value=f"{image.height} px")
    st.metric(label="Color Mode", value=image.mode)
    st.metric(label="Original Format", value=image.format if image.format else "RGB (Converted)")

    with st.expander("📚 Penjelasan Konsep Metadata"):
        st.markdown("""
        - **Width & Height**: Ukuran dimensi gambar dalam satuan piksel (px). Menentukan resolusi spasial gambar.
        - **Mode**: Format representasi warna piksel. Mode `RGB` berarti setiap piksel terdiri dari komponen Red, Green, dan Blue.
        - **Format**: Format kompresi file asli (seperti JPEG, PNG). Ketika kita melakukan `.convert("RGB")`, Pillow memuat data piksel mentah ke memori dalam format RGB terstandarisasi.
        """)


# ==========================================
# 2. CONVERT TO NUMPY ARRAY
# ==========================================
st.markdown("---")
st.header("2. Konversi Gambar ke NumPy Array", anchor="sec2")

col1_array_stats, col2_array_explanation = st.columns([1, 1])

with col1_array_stats:
    st.subheader("Atribut NumPy Array")
    st.write("Ketika gambar diubah menjadi NumPy Array, kita bisa melihat strukturnya melalui beberapa atribut berikut:")
    
    # Menampilkan informasi teknis array menggunakan metrik
    st.metric(label="Python Object Type", value=str(type(image_array)))
    st.metric(label="Array Shape (Height, Width, Channels)", value=str(image_array.shape))
    st.metric(label="Number of Dimensions (ndim)", value=str(image_array.ndim))
    st.metric(label="Data Type (dtype)", value=str(image_array.dtype))
    st.metric(label="Total Elements (Size)", value=f"{image_array.size:,}")
    # Menampilkan penggunaan memori dalam Kilobyte agar lebih mudah dibaca
    st.metric(label="Memory Usage", value=f"{image_array.nbytes / 1024:.2f} KB ({image_array.nbytes:,} bytes)")

with col2_array_explanation:
    st.subheader("Penjelasan Konsep")
    
    with st.expander("🤔 Mengapa Gambar diubah menjadi NumPy Array?", expanded=True):
        st.markdown("""
        Komputer tidak memahami gambar secara visual seperti manusia. Komputer melihat gambar sebagai **kumpulan angka** (piksel). 
        
        NumPy Array adalah struktur data yang sangat efisien untuk menyimpan dan memanipulasi matriks angka berukuran besar. 
        Dengan mengubah gambar menjadi NumPy array, kita dapat melakukan operasi matematika (seperti filtering, normalisasi, pemotongan, dll.) pada piksel dengan sangat cepat.
        """)
        
    with st.expander("📐 Apa arti Shape dan Format (Height, Width, Channels)?"):
        st.markdown(f"""
        Nilai `shape` dari array ini adalah **{image_array.shape}**. 
        
        Artinya:
        1. **Tinggi (Height) = {image_array.shape[0]}**: Jumlah baris piksel dari atas ke bawah.
        2. **Lebar (Width) = {image_array.shape[1]}**: Jumlah kolom piksel dari kiri ke kanan.
        3. **Saluran (Channels) = {image_array.shape[2]}**: Lapisan warna yang menyusun gambar.
        
        Perhatikan bahwa urutannya di NumPy adalah `(Height, Width, Channels)`. Ini adalah standar representasi gambar pada sebagian besar library image processing di Python.
        """)

    with st.expander("🔴🟢🔵 Mengapa Gambar RGB memiliki 3 Channels?"):
        st.markdown("""
        Warna pada layar digital dibentuk dari kombinasi tiga warna primer cahaya: **Red (Merah)**, **Green (Hijau)**, dan **Blue (Biru)**.
        
        Setiap channel (saluran) merepresentasikan intensitas masing-masing warna tersebut. 
        Dengan menggabungkan ketiga channel ini pada intensitas yang berbeda-beda, kita dapat menciptakan jutaan kombinasi warna lainnya (misalnya, merah penuh + hijau penuh = kuning).
        """)


# ==========================================
# 3. PIXEL INSPECTOR
# ==========================================
st.markdown("---")
st.header("3. Pixel Inspector (Melihat Nilai Piksel Spesifik)", anchor="sec3")
st.write("Silakan masukkan koordinat piksel yang ingin Anda periksa. Aplikasi akan mengambil nilai warna pada koordinat tersebut.")

col1_coord, col2_pixel_val = st.columns([1, 1])

with col1_coord:
    st.subheader("Pilih Koordinat")
    
    # Input koordinat X dengan batas 0 sampai width-1
    pixel_x = st.number_input(
        f"X Coordinate (Lebar / Horizontal: 0 hingga {width - 1})",
        min_value=0,
        max_value=width - 1,
        value=min(100, width - 1),
        step=1,
        key="inspector_pixel_x"
    )
    
    # Input koordinat Y dengan batas 0 sampai height-1
    pixel_y = st.number_input(
        f"Y Coordinate (Tinggi / Vertikal: 0 hingga {height - 1})",
        min_value=0,
        max_value=height - 1,
        value=min(100, height - 1),
        step=1,
        key="inspector_pixel_y"
    )

    # Mengambil nilai piksel dari array.
    # PENTING: Indexing pada array NumPy menggunakan format [y, x] atau [baris, kolom].
    pixel = image_array[pixel_y, pixel_x]

with col2_pixel_val:
    st.subheader("Hasil Pemeriksaan Piksel")
    st.write(f"Piksel pada Koordinat **(X={pixel_x}, Y={pixel_y})**:")
    
    st.metric(label="RGB Array Value [R, G, B]", value=str(list(pixel)))
    
    # Visualisasi warna piksel terpilih menggunakan box kecil berisi warna tersebut
    hex_color = f"#{pixel[0]:02x}{pixel[1]:02x}{pixel[2]:02x}"
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 20px;">
            <span>Visualisasi Warna Piksel:</span>
            <div style="width: 40px; height: 40px; background-color: {hex_color}; border: 2px solid #ccc; border-radius: 5px;"></div>
            <span><b>{hex_color.upper()}</b></span>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Menampilkan detail nilai setiap channel warna
    col_r, col_g, col_b = st.columns(3)
    col_r.metric(label="🔴 Red Channel", value=str(pixel[0]))
    col_g.metric(label="🟢 Green Channel", value=str(pixel[1]))
    col_b.metric(label="🔵 Blue Channel", value=str(pixel[2]))

with st.container():
    st.subheader("Penjelasan Konsep & Logika Kode")
    
    with st.expander("🔄 Mengapa menggunakan indexing [y, x] bukan [x, y]?"):
        st.markdown("""
        Dalam grafik matematika atau layar komputer, kita terbiasa dengan koordinat `(x, y)` di mana `x` adalah sumbu horizontal dan `y` adalah sumbu vertikal.
        
        Namun, NumPy memperlakukan gambar sebagai matriks 2D (atau 3D dengan channel). Struktur matriks diakses menggunakan aturan **`[Baris, Kolom]`**:
        - **Baris (Row)**: Mewakili pergerakan secara vertikal (sumbu **Y** atau Tinggi).
        - **Kolom (Column)**: Mewakili pergerakan secara horizontal (sumbu **X** atau Lebar).
        
        Oleh karena itu, untuk mengambil nilai piksel pada koordinat kartesian `(x, y)`, kita harus menulis indeks array-nya sebagai:
        ```python
        # y mewakili baris, x mewakili kolom
        pixel = image_array[y, x]
        ```
        """)

    with st.expander("🎨 Mengapa satu piksel RGB memiliki tiga nilai?"):
        st.markdown("""
        Karena gambar kita menggunakan mode warna **RGB**. Setiap piksel tunggal pada layar dibentuk oleh tiga sub-piksel (merah, hijau, dan biru) yang sangat kecil dan terletak berdekatan.
        
        Kombinasi intensitas cahaya dari ketiga sub-piksel inilah yang dilihat mata kita sebagai satu warna tunggal. Jadi, array NumPy pada koordinat `[y, x]` mengembalikan array berukuran 3: `[Nilai_Red, Nilai_Green, Nilai_Blue]`.
        """)

    with st.expander("🔢 Mengapa nilai setiap channel berada pada rentang 0 hingga 255?"):
        st.markdown(r"""
        Secara standar, warna digital disimpan dalam format **8-bit per channel**. 
        
        Dalam biner, 8 bit dapat menampung \(2^8 = 256\) nilai unik. Nilai ini dimulai dari:
        - **0**: Tidak ada warna sama sekali (hitam/gelap sepenuhnya).
        - **255**: Intensitas warna maksimum (terang sepenuhnya).
        
        Jika ketiga channel bernilai `[0, 0, 0]`, hasilnya adalah hitam. Jika ketiganya `[255, 255, 255]`, hasilnya adalah putih bersih.
        """)


# ==========================================
# 4. RGB CHANNELS
# ==========================================
st.markdown("---")
st.header("4. Memisahkan Channel Warna (RGB Slicing)", anchor="sec4")
st.write("Di sini kita akan membelah gambar berwarna kita menjadi tiga saluran warna penyusunnya (Red, Green, dan Blue).")

# Melakukan slicing array menggunakan NumPy untuk memisahkan channel warna
# Sintaks [:, :, 0] artinya:
# - ":" pertama: ambil seluruh baris (Height)
# - ":" kedua: ambil seluruh kolom (Width)
# - "0", "1", "2": ambil indeks channel ke-0 (Red), ke-1 (Green), atau ke-2 (Blue)
red_channel = image_array[:, :, 0]
green_channel = image_array[:, :, 1]
blue_channel = image_array[:, :, 2]

# Menampilkan hasil slicing masing-masing channel
col_ch_r, col_ch_g, col_ch_b = st.columns(3)

with col_ch_r:
    st.subheader("🔴 Red Channel")
    # Menampilkan channel sebagai gambar grayscale untuk menunjukkan intensitas merah
    st.image(red_channel, caption=f"Shape: {red_channel.shape}", use_container_width=True)
    st.write("Piksel yang lebih terang menunjukkan bahwa warna merah pada area tersebut sangat dominan.")

with col_ch_g:
    st.subheader("🟢 Green Channel")
    st.image(green_channel, caption=f"Shape: {green_channel.shape}", use_container_width=True)
    st.write("Piksel yang lebih terang menunjukkan dominasi warna hijau pada area tersebut.")

with col_ch_b:
    st.subheader("🔵 Blue Channel")
    st.image(blue_channel, caption=f"Shape: {blue_channel.shape}", use_container_width=True)
    st.write("Piksel yang lebih terang menunjukkan dominasi warna biru pada area tersebut.")

with st.container():
    st.subheader("Penjelasan Konsep Slicing")
    
    with st.expander("✂️ Apa arti tanda \":\" pada NumPy slicing?"):
        st.markdown("""
        Tanda titik dua (`:`) dalam NumPy slicing berarti **"ambil semua elemen pada dimensi ini"** (dari awal hingga akhir).
        
        Ketika kita menulis `image_array[:, :, 0]`:
        1. Indeks ke-1 (`:`): Mengambil semua baris (dari atas ke bawah).
        2. Indeks ke-2 (`:`): Mengambil semua kolom (dari kiri ke kanan).
        3. Indeks ke-3 (`0`): Hanya mengambil indeks ke-0 pada dimensi channel (yaitu warna Merah/Red).
        
        Dengan kata lain, kita mengekstrak "lembaran" warna merah untuk seluruh area gambar.
        """)

    with st.expander("📐 Mengapa shape image_array adalah (height, width, 3) sedangkan satu channel menjadi (height, width)?"):
        st.markdown(f"""
        - **`image_array.shape` = {image_array.shape}**: Gambar berwarna adalah objek 3 dimensi (Tinggi, Lebar, dan 3 Saluran Warna bertumpuk).
        
        - **`channel.shape` = {red_channel.shape}**: Ketika kita melakukan slicing (seperti `image_array[:, :, 0]`), kita mengambil salah satu dari 3 lembaran saluran warna tersebut. 
        Karena kita hanya mengambil satu saluran, dimensi ketiganya hilang. Matriks yang tersisa adalah matriks 2 dimensi yang hanya berisi informasi intensitas warna tunggal (tinggi dan lebar). 
        Itulah mengapa gambar saluran warna tunggal dirender oleh komputer sebagai gambar hitam-putih (grayscale) — nilai pikselnya mewakili tingkat kecerahan dari warna tersebut.
        """)


# ==========================================
# 5. GRAYSCALE CONVERSION
# ==========================================
st.markdown("---")
st.header("5. Konversi Gambar ke Grayscale", anchor="sec5")
st.write("Mengubah gambar berwarna (RGB) menjadi gambar hitam-putih (Grayscale).")

# Mengubah PIL image menjadi grayscale menggunakan Pillow
# Mode "L" pada Pillow singkatan dari "Luminance" (Grayscale / Kecerahan)
gray_image = image.convert("L")
gray_array = np.array(gray_image)

col_gray_rgb, col_gray_res = st.columns(2)

with col_gray_rgb:
    st.subheader("Gambar RGB Asli")
    st.image(image, caption="RGB Image", use_container_width=True)
    st.markdown(f"**Shape**: `{image_array.shape}` (3 Channels)")

with col_gray_res:
    st.subheader("Gambar Grayscale (Pillow Mode 'L')")
    st.image(gray_image, caption="Grayscale Image", use_container_width=True)
    st.markdown(f"**Shape**: `{gray_array.shape}` (1 Channel / 2D Matrix)")

with st.container():
    st.subheader("Perbandingan Struktur Array")
    
    # Menampilkan tabel perbandingan
    st.markdown(
        f"""
        | Karakteristik | RGB Image | Grayscale Image |
        |---|---|---|
        | **Dimensi Array** | 3 Dimensi (Height, Width, Channels) | 2 Dimensi (Height, Width) |
        | **Shape** | `{image_array.shape}` | `{gray_array.shape}` |
        | **Channel Warna** | 3 (Red, Green, Blue) | 1 (Luminance / Kecerahan) |
        | **Nilai Piksel** | Array 3 angka (contoh: `[120, 85, 200]`) | Nilai angka tunggal (contoh: `108`) |
        """
    )
    
    with st.expander("💡 Mengapa Grayscale hanya memiliki 1 channel?"):
        st.markdown(r"""
        Gambar grayscale hanya menunjukkan tingkat kecerahan cahaya (dari hitam ke putih), tanpa informasi warna (rona). 
        
        Karena tidak ada perbedaan warna merah, hijau, atau biru, kita tidak memerlukan 3 lembar channel. Kita hanya membutuhkan **satu nilai intensitas** per piksel:
        - **0**: Hitam pekat.
        - **255**: Putih terang.
        
        Pillow mengonversi RGB ke Grayscale menggunakan rumus standar sensitivitas mata manusia terhadap cahaya (luminance formula):
        \[Y = 0.299 \cdot R + 0.587 \cdot G + 0.114 \cdot B\]
        
        Rumus ini memberi bobot lebih tinggi pada warna Hijau (Green) karena mata manusia lebih sensitif terhadap warna hijau dibandingkan merah atau biru.
        """)


# ==========================================
# 6. NORMALIZATION
# ==========================================
st.markdown("---")
st.header("6. Normalisasi Gambar (Normalization)", anchor="sec6")
st.write("Mengubah rentang nilai piksel gambar dari integer 0-255 menjadi float 0.0-1.0.")

# Langkah-langkah normalisasi:
# 1. Konversi tipe data array ke float32 agar bisa menampung nilai desimal.
# 2. Bagi seluruh elemen array dengan 255.0.
normalized_image = image_array.astype(np.float32) / 255.0

col_norm_stats, col_norm_exp = st.columns([1, 1])

with col_norm_stats:
    st.subheader("Statistik Sebelum vs Sesudah Normalisasi")
    
    col_pre, col_post = st.columns(2)
    
    with col_pre:
        st.markdown("**Sebelum Normalisasi:**")
        st.metric(label="Min Value", value=str(image_array.min()))
        st.metric(label="Max Value", value=str(image_array.max()))
        st.metric(label="Data Type", value=str(image_array.dtype))
        st.metric(label="Shape", value=str(image_array.shape))
        
    with col_post:
        st.markdown("**Sesudah Normalisasi:**")
        st.metric(label="Min Value", value=f"{normalized_image.min():.4f}")
        st.metric(label="Max Value", value=f"{normalized_image.max():.4f}")
        st.metric(label="Data Type", value=str(normalized_image.dtype))
        st.metric(label="Shape", value=str(normalized_image.shape))

with col_norm_exp:
    st.subheader("Penjelasan Konsep Normalisasi")
    
    with st.expander("📉 Mengubah rentang 0-255 menjadi 0.0-1.0"):
        st.markdown("""
        Piksel gambar asli bertipe integer 8-bit (`uint8`) dengan rentang nilai **0 hingga 255**.
        
        Ketika kita membagi nilai array tersebut dengan `255.0` (angka float), NumPy secara otomatis melakukan pembagian untuk setiap elemen piksel gambar. Hasilnya adalah array bertipe float dengan nilai desimal antara **0.0** (hitam) hingga **1.0** (putih/warna penuh).
        """)
        
    with st.expander("🤖 Mengapa Normalisasi sangat penting sebelum masuk ke Model Machine/Deep Learning?"):
        st.markdown("""
        1. **Stabilitas Gradien (Gradient Stability)**: Algoritma Deep Learning menggunakan optimasi Gradient Descent. Menyuplai input dengan rentang nilai yang kecil (0 hingga 1 or -1 hingga 1) membantu mencegah masalah gradien meledak (*exploding gradients*) atau gradien hilang (*vanishing gradients*), sehingga model belajar lebih cepat dan stabil.
        2. **Skala Input Seragam**: Jika kita melatih model dengan gambar-gambar yang memiliki pencahayaan berbeda, normalisasi membantu menyamakan skala fitur input agar model tidak bias terhadap gambar yang terlalu terang atau terlalu gelap.
        3. **Kemudahan Komputasi**: Nilai floating-point kecil lebih disukai oleh operasi matematika matriks di GPU karena menyederhanakan perhitungan bobot model (*weights*).
        """)


# ==========================================
# 7. MINI PREPROCESSING PIPELINE
# ==========================================
st.markdown("---")
st.header("7. Mini Preprocessing Pipeline", anchor="sec7")
st.write("Ini adalah simulasi pipeline preprocessing standar yang biasa dilalui oleh sebuah gambar sebelum diberikan ke model deep learning (seperti ResNet atau MobileNet).")

# Visualisasi alur pipeline menggunakan diagram teks
st.code("""
Original Image (sample.jpg)
        ↓
Convert to RGB (3 Channels)
        ↓
Resize ke 224 × 224 (Standard Model Input Size)
        ↓
Convert ke NumPy Array
        ↓
Normalize (Divide by 255.0, range 0.0 - 1.0)
        ↓
Check Final Shape & Value Range
""", language="text")

# --- Implementasi Pipeline ---
# Langkah 1: Load dan pastikan format RGB
pipeline_image = Image.open(image_path).convert("RGB")

# Langkah 2: Resize menjadi 224 x 224 piksel
# Ukuran 224x224 adalah resolusi input standar untuk sebagian besar model klasifikasi gambar (ImageNet)
resized_image = pipeline_image.resize((224, 224))

# Langkah 3: Konversi ke NumPy Array
pipeline_array = np.array(resized_image)

# Langkah 4: Normalisasi nilai piksel ke rentang 0.0 - 1.0
pipeline_normalized = pipeline_array.astype(np.float32) / 255.0

# Menampilkan hasil pipeline
col_pipe_img1, col_pipe_img2, col_pipe_metrics = st.columns([1.5, 1.5, 1.5])

with col_pipe_img1:
    st.subheader("Gambar Asli")
    st.image(image, caption=f"Original Size: {image.width}x{image.height}", use_container_width=True)

with col_pipe_img2:
    st.subheader("Hasil Preprocessing")
    st.image(resized_image, caption="Resized Size: 224x224", use_container_width=True)
    st.info("Perhatikan bahwa gambar diperkecil ukurannya untuk mempercepat proses komputasi model ML.")

with col_pipe_metrics:
    st.subheader("Spesifikasi Akhir Array")
    st.write("Data yang siap dimasukkan ke dalam model neural network:")
    
    st.metric(label="Final Shape", value=str(pipeline_normalized.shape))
    st.metric(label="Data Type", value=str(pipeline_normalized.dtype))
    st.metric(label="Min Value", value=f"{pipeline_normalized.min():.4f}")
    st.metric(label="Max Value", value=f"{pipeline_normalized.max():.4f}")
    st.metric(label="Total Piksel (Size)", value=f"{pipeline_normalized.size:,}")


# ==========================================
# 8. HISTOGRAM EXPLORER
# ==========================================
st.markdown("---")
st.header("8. Histogram Explorer", anchor="sec8")
st.write("Menganalisis distribusi frekuensi kecerahan piksel pada setiap saluran warna.")

# 1. Tampilkan informasi / statistik statistik dasar gambar
st.subheader("Informasi Statistik Piksel Gambar")
col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)

col_m1.metric("Image Shape", str(image_array.shape))
col_m2.metric("Image Mode", image.mode)
col_m3.metric("Minimum Pixel Value", str(image_array.min()))
col_m4.metric("Maximum Pixel Value", str(image_array.max()))
col_m5.metric("Mean Pixel Value", f"{image_array.mean():.2f}")

# Memisahkan channel untuk histogram
red_channel = image_array[:, :, 0]
green_channel = image_array[:, :, 1]
blue_channel = image_array[:, :, 2]

# Membuat versi grayscale gambar
gray_image_hist = image.convert("L")
gray_array_hist = np.array(gray_image_hist)

# 10. Perbandingan Layout
col_rgb_layout, col_gray_layout = st.columns(2)

# Kolom Kiri: RGB Image & RGB Histograms
with col_rgb_layout:
    st.subheader("Gambar RGB Asli")
    st.image(image, caption="RGB Image (sample.jpg)", use_container_width=True)
    st.markdown("""
    **Alur Grafik:**
    RGB Image $\\rightarrow$ Red, Green, Blue Histograms
    """)
    
    # Plot Red Histogram
    fig_r, ax_r = plt.subplots(figsize=(6, 2.5))
    ax_r.hist(red_channel.ravel(), bins=256, range=(0, 256), color='red', alpha=0.7)
    ax_r.set_title("🔴 Red Channel Histogram", color='red')
    ax_r.set_xlabel("Pixel Value (0-255)")
    ax_r.set_ylabel("Frequency")
    ax_r.grid(True, linestyle='--', alpha=0.5)
    st.pyplot(fig_r)
    plt.close(fig_r)
    
    # Plot Green Histogram
    fig_g, ax_g = plt.subplots(figsize=(6, 2.5))
    ax_g.hist(green_channel.ravel(), bins=256, range=(0, 256), color='green', alpha=0.7)
    ax_g.set_title("🟢 Green Channel Histogram", color='green')
    ax_g.set_xlabel("Pixel Value (0-255)")
    ax_g.set_ylabel("Frequency")
    ax_g.grid(True, linestyle='--', alpha=0.5)
    st.pyplot(fig_g)
    plt.close(fig_g)
    
    # Plot Blue Histogram
    fig_b, ax_b = plt.subplots(figsize=(6, 2.5))
    ax_b.hist(blue_channel.ravel(), bins=256, range=(0, 256), color='blue', alpha=0.7)
    ax_b.set_title("🔵 Blue Channel Histogram", color='blue')
    ax_b.set_xlabel("Pixel Value (0-255)")
    ax_b.set_ylabel("Frequency")
    ax_b.grid(True, linestyle='--', alpha=0.5)
    st.pyplot(fig_b)
    plt.close(fig_b)

# Kolom Kanan: Grayscale Image & Grayscale Histogram
with col_gray_layout:
    st.subheader("Gambar Grayscale")
    st.image(gray_image_hist, caption="Grayscale Image (convert('L'))", use_container_width=True)
    st.markdown("""
    **Alur Grafik:**
    Grayscale Image $\\rightarrow$ Grayscale Histogram
    """)
    
    # Plot Grayscale Histogram
    fig_gray, ax_gray = plt.subplots(figsize=(6, 2.5))
    ax_gray.hist(gray_array_hist.ravel(), bins=256, range=(0, 256), color='gray', alpha=0.7)
    ax_gray.set_title("⚫ Grayscale Histogram", color='dimgray')
    ax_gray.set_xlabel("Pixel Value (0-255)")
    ax_gray.set_ylabel("Frequency")
    ax_gray.grid(True, linestyle='--', alpha=0.5)
    st.pyplot(fig_gray)
    plt.close(fig_gray)

# 11. Expander konsep penjelasan
with st.expander("📚 What does this mean? (Penjelasan Konsep Histogram Gambar)"):
    st.markdown(r"""
    ### Apa itu Histogram Gambar?
    **Histogram gambar** adalah sebuah diagram atau grafik batang yang menunjukkan **distribusi intensitas warna atau tingkat kecerahan** dari seluruh piksel di dalam sebuah gambar. 
    Melalui histogram, kita dapat menganalisis apakah sebuah gambar memiliki pencahayaan yang seimbang, terlalu gelap, terlalu terang, atau buram (kontras rendah).

    ---

    ### Elemen Grafik Histogram:
    - **Sumbu X (Horizontal - Pixel Value)**: 
      Mewakili intensitas kecerahan warna dari nilai **0 hingga 255**.
      - Nilai **`0`**: Piksel berwarna **Hitam Pekat** (tidak ada intensitas cahaya/warna).
      - Nilai **`255`**: Piksel berwarna **Putih Bersih** (intensitas cahaya/warna maksimal).
    - **Sumbu Y (Vertikal - Frequency / Pixel Count)**: 
      Menunjukkan jumlah total piksel di dalam gambar yang memiliki nilai intensitas kecerahan tersebut.

    ---

    ### Cara Membaca Bentuk Distribusi Histogram:

    1. **Histogram yang Berkumpul di Sisi Kiri (Skewed Left / Dark)**:
       - **Artinya**: Sebagian besar piksel memiliki nilai mendekati `0`. 
       - **Dampak pada Gambar**: Gambar cenderung **gelap** atau kurang cahaya (*underexposed*), seperti foto di malam hari tanpa bantuan lampu kilat.
    
    2. **Histogram yang Berkumpul di Sisi Kanan (Skewed Right / Bright)**:
       - **Artinya**: Sebagian besar piksel memiliki nilai mendekati `255`. 
       - **Dampak pada Gambar**: Gambar cenderung **sangat terang** atau berlebihan cahaya (*overexposed*), seperti foto di bawah sinar matahari langsung yang terik.

    3. **Distribusi Histogram yang Sempit (Narrow Distribution)**:
       - **Artinya**: Grafik menumpuk tinggi hanya di satu area kecil (misal hanya di sekitar nilai 120-140) dan tidak menyebar.
       - **Dampak pada Gambar**: Gambar memiliki **kontras rendah** (terlihat kusam, berkabut, atau abu-abu flat) karena perbedaan kecerahan antarpiksel sangat sedikit.

    4. **Distribusi Histogram yang Luas (Wide Distribution)**:
       - **Artinya**: Grafik menyebar merata dari ujung kiri (mendekati 0) hingga ujung kanan (mendekati 255).
       - **Dampak pada Gambar**: Gambar memiliki **kontras tinggi** yang baik (tajam dan mudah dibedakan batas antarsubjeknya) karena variasi kecerahan antarpiksel sangat kaya.
    """)


# ==========================================
# 9. RESIZE & ASPECT RATIO EXPLORER
# ==========================================
st.markdown("---")
st.header("9. Resize & Aspect Ratio Explorer", anchor="sec9")
st.write(
    "Modul ini membantu Anda memahami perbedaan antara memotong gambar (*crop*) "
    "dan mengubah ukurannya (*resize*), serta bagaimana rasio aspek memengaruhi distorsi."
)

# 1. IMAGE INFORMATION
# Menghitung aspect ratio gambar asli
original_width = image.width
original_height = image.height
original_aspect_ratio = original_width / original_height

st.subheader("Informasi Ukuran Gambar Asli")
col_orig_w, col_orig_h, col_orig_ar = st.columns(3)
col_orig_w.metric("Original Width", f"{original_width} px")
col_orig_h.metric("Original Height", f"{original_height} px")
# Menampilkan aspect ratio dengan label matematika rasio pembagiannya
col_orig_ar.metric("Original Aspect Ratio", f"{original_aspect_ratio:.4f} (W:H)")

st.markdown("---")
st.subheader("Pengaturan Target Ukuran (Target Size)")
st.write("Masukkan target ukuran wadah baru untuk melihat perbandingan hasil dari 3 teknik resize:")

col_inp_w, col_inp_h = st.columns(2)
with col_inp_w:
    target_width = st.number_input(
        "Target Width (Lebar Target)",
        min_value=10,
        max_value=2000,
        value=300,
        step=1,
        key="ratio_target_width_input"
    )
with col_inp_h:
    target_height = st.number_input(
        "Target Height (Tinggi Target)",
        min_value=10,
        max_value=2000,
        value=300,
        step=1,
        key="ratio_target_height_input"
    )

target_aspect_ratio = target_width / target_height

# 2. DIRECT RESIZE
# Direct resize memaksa dimensi gambar menjadi tepat target_width dan target_height
resized_image_direct = image.resize((target_width, target_height))
aspect_ratio_direct = target_width / target_height

# 3. ASPECT RATIO PRESERVED RESIZE
# Menghitung faktor skala minimum agar gambar muat di dalam target box tanpa meluber
scale_pres = min(target_width / original_width, target_height / original_height)
new_width = int(original_width * scale_pres)
new_height = int(original_height * scale_pres)
resized_image_pres = image.resize((new_width, new_height))
aspect_ratio_pres = new_width / new_height

# 4. CENTER CROP
# Langkah A: Resize gambar mempertahankan aspect ratio tetapi harus menutupi seluruh target box (menggunakan max scale)
scale_crop = max(target_width / original_width, target_height / original_height)
resized_width = int(original_width * scale_crop)
resized_height = int(original_height * scale_crop)
resized_image_temp = image.resize((resized_width, resized_height))

# Langkah B: Crop bagian tengah gambar agar ukurannya tepat target_width dan target_height
# Menghitung margin koordinat batas crop kiri dan atas
left = (resized_width - target_width) // 2
top = (resized_height - target_height) // 2
right = left + target_width
bottom = top + target_height
cropped_image = resized_image_temp.crop((left, top, right, bottom))
aspect_ratio_crop = target_width / target_height

# 5. PERBANDINGAN TIGA METODE (SIDE-BY-SIDE)
st.markdown("---")
st.subheader("Perbandingan Visual & Ukuran")

col_res_dir, col_res_pres, col_res_crop = st.columns(3)

with col_res_dir:
    st.subheader("1. Direct Resize")
    st.image(resized_image_direct, caption="Hasil Direct Resize (Dipaksa)", use_container_width=True)
    st.metric("Width", f"{resized_image_direct.width} px")
    st.metric("Height", f"{resized_image_direct.height} px")
    st.metric("Aspect Ratio Hasil", f"{aspect_ratio_direct:.4f}")
    st.warning("⚠️ Objek akan tampak peyang/melar jika rasio target berbeda dengan rasio asli.")

with col_res_pres:
    st.subheader("2. Aspect Ratio Preserved")
    st.image(resized_image_pres, caption="Hasil Preserved Resize (Muat di Box)", use_container_width=True)
    st.metric("Width", f"{resized_image_pres.width} px")
    st.metric("Height", f"{resized_image_pres.height} px")
    st.metric("Aspect Ratio Hasil", f"{aspect_ratio_pres:.4f}")
    st.success("✅ Proporsi gambar tetap terjaga (tidak penyok). Ukuran akhir menyesuaikan rasio asli.")

with col_res_crop:
    st.subheader("3. Center Crop")
    st.image(cropped_image, caption="Hasil Center Crop (Dipotong)", use_container_width=True)
    st.metric("Width", f"{cropped_image.width} px")
    st.metric("Height", f"{cropped_image.height} px")
    st.metric("Aspect Ratio Hasil", f"{aspect_ratio_crop:.4f}")
    st.info("ℹ️ Ukuran tepat sesuai target tanpa distorsi, tetapi area pinggir gambar dipotong.")

# 6. EDUCATIONAL EXPLANATION
st.markdown("---")
with st.expander("📚 What does this mean? (Penjelasan Analisis Teknik Resizing)"):
    st.markdown(f"""
    Dalam Computer Vision, model Deep Learning (seperti CNN) biasanya menuntut input gambar dengan ukuran yang seragam (misalnya `224x224` piksel).
    Ada tiga cara umum untuk menyesuaikan dimensi gambar ke target ukuran:

    ---

    ### A. Direct Resize (Resize Langsung)
    - **Cara Kerja**: Memaksa lebar gambar menjadi `{target_width}px` dan tinggi menjadi `{target_height}px` menggunakan `image.resize()`.
    - **Dampak**: 
      - Jika rasio gambar asli (misalnya `{original_width}:{original_height}`) berbeda jauh dengan rasio target (misalnya `{target_width}:{target_height}`), objek di dalam gambar akan mengalami **distorsi** (tampak memanjang secara horizontal atau vertikal).
    - **Contoh**: Gambar `1920x1080` dipaksa menjadi `224x224` akan membuat subjek di dalam foto tampak kurus dan gepeng.

    ---

    ### B. Aspect Ratio Preserved (Mempertahankan Rasio)
    - **Cara Kerja**: Menghitung faktor skala terkecil agar seluruh bagian gambar muat di dalam target box. Rumusnya menggunakan:
      ```python
      scale = min(target_width / original_width, target_height / original_height)
      ```
    - **Dampak**:
      - Tidak ada distorsi sama sekali pada gambar.
      - Hasil ukuran gambar tidak akan melebihi target box, tetapi **bisa lebih kecil** pada salah satu dimensinya jika rasionya tidak cocok.
    - **Contoh**: Gambar lanskap yang di-resize ke target kotak `300x300` mungkin menghasilkan gambar berdimensi `300x168`.

    ---

    ### C. Center Crop (Potong Tengah)
    - **Cara Kerja**: 
      1. Terlebih dahulu melakukan resize dengan mempertahankan rasio, namun mencari kecocokan skala terbesar agar gambar menutupi *seluruh* bidang target box (`scale = max(...)`).
      2. Menghitung koordinat tengah gambar, lalu membuang area gambar yang meluber keluar dari batas target box menggunakan fungsi `image.crop()`.
    - **Dampak**:
      - Hasil gambar memiliki dimensi tepat sesuai target (misalnya pas `{target_width}x{target_height}`).
      - Gambar bebas distorsi, tetapi **sebagian informasi visual di tepi gambar akan hilang** (terpotong).
    """)
