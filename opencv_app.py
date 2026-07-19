import streamlit as st
import cv2
import numpy as np
from pathlib import Path

# ==========================================
# KONFIGURASI HALAMAN & STYLE
# ==========================================
st.set_page_config(
    page_title="OpenCV Interactive Explorer",
    page_icon="👁️",
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
        color: #0f172a;
        font-family: 'Inter', sans-serif;
    }
    .highlight {
        background-color: #f1f5f9;
        padding: 2px 6px;
        border-radius: 4px;
        font-family: monospace;
        font-weight: bold;
        color: #0f172a;
    }
    .title-container {
        background: linear-gradient(135deg, #0f172a 0%, #2563eb 100%);
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
        border-left: 4px solid #2563eb;
        transform: translateX(5px);
        color: #0f172a !important;
    }
</style>
""", unsafe_allow_html=True)

# Header Utama Aplikasi
st.markdown("""
<div class="title-container">
    <h1 style="color: white; margin: 0;">👁️ OpenCV Interactive Explorer</h1>
    <p style="color: #bfdbfe; font-size: 1.1rem; margin-top: 10px; margin-bottom: 0;">
        Pelajari dasar-dasar pemrosesan gambar menggunakan OpenCV (cv2) dan NumPy secara interaktif dan visual.
        Semua modul berada dalam satu halaman, gunakan daftar isi di samping untuk berpindah modul secara instan.
    </p>
</div>
""", unsafe_allow_html=True)


# ==========================================
# GLOBAL IMAGE LOADING & ERROR HANDLING
# ==========================================
image_path = "images/sample.jpg"

if not Path(image_path).exists():
    st.error(f"Gambar tidak ditemukan di: {image_path}. Silakan pastikan gambar 'sample.jpg' berada di dalam folder 'images/'.")
    st.stop()

# Membaca gambar menggunakan OpenCV (BGR Format secara default)
# cv2.imread mengembalikan gambar dalam bentuk NumPy array berdimensi 3 (height, width, channels)
bgr_image = cv2.imread(image_path)

if bgr_image is None:
    st.error("Gagal memuat gambar. Pastikan format berkas didukung oleh OpenCV (seperti JPG atau PNG).")
    st.stop()

# Mendapatkan ukuran gambar asli dari NumPy array
height, width, channels = bgr_image.shape


# ==========================================
# SIDEBAR NAVIGATION (TABLE OF CONTENTS)
# ==========================================
st.sidebar.markdown("### 📚 Daftar Isi Modul")
st.sidebar.markdown("""
<a href="#sec1" class="sidebar-link">1. Read Image 📂</a>
<a href="#sec2" class="sidebar-link">2. BGR vs RGB 🎨</a>
<a href="#sec3" class="sidebar-link">3. Image Information 📊</a>
<a href="#sec4" class="sidebar-link">4. Resize 📐</a>
<a href="#sec5" class="sidebar-link">5. Crop ✂️</a>
<a href="#sec6" class="sidebar-link">6. Flip 🔄</a>
<a href="#sec7" class="sidebar-link">7. Rotate ↪️</a>
<a href="#sec8" class="sidebar-link">8. Save Image 💾</a>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.info(
    "Aplikasi ini didesain sebagai modul pembelajaran interaktif. "
    "Klik salah satu bab di atas untuk auto-slide (scroll halus) ke bagian tersebut."
)


# ==========================================
# MODULE 1: READ IMAGE
# ==========================================
st.header("1. Membaca Gambar dengan OpenCV", anchor="sec1")
st.write("Bagaimana cara OpenCV memuat gambar ke dalam memori komputer?")

# Kode utama untuk membaca gambar
st.code("""
# Membaca file gambar dari disk
image = cv2.imread("images/sample.jpg")
""", language="python")

# Mengonversi gambar BGR ke RGB khusus untuk visualisasi Streamlit agar warnanya tidak salah
rgb_for_display = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)

col1_disp, col2_attr = st.columns([2, 1])

with col1_disp:
    # Menampilkan gambar dengan warna yang dikonversi ke RGB
    st.image(rgb_for_display, caption="Gambar yang dibaca (Ditampilkan dengan RGB untuk Streamlit)", use_container_width=True)

with col2_attr:
    st.subheader("Atribut NumPy Array Hasil cv2.imread()")
    st.write("OpenCV memuat gambar bukan sebagai objek khusus, melainkan langsung berupa **NumPy Array**:")
    
    st.metric(label="Tipe Objek (Object Type)", value=str(type(bgr_image)))
    st.metric(label="Bentuk Array (image.shape)", value=str(bgr_image.shape))
    st.metric(label="Tipe Data Piksel (image.dtype)", value=str(bgr_image.dtype))
    st.metric(label="Jumlah Dimensi (image.ndim)", value=str(bgr_image.ndim))

with st.expander("📚 Penjelasan Konsep: cv2.imread() & NumPy"):
    st.markdown("""
    ### Mengapa OpenCV Menggunakan NumPy Array?
    - Di masa lalu, library pemrosesan gambar sering mendefinisikan objek gambar buatan mereka sendiri. Hal ini menyulitkan integrasi antar-library.
    - Sejak OpenCV versi 2 ke atas di Python, OpenCV mengadopsi **NumPy Array** sebagai standar utama penyimpanan data gambar.
    - Keuntungan menggunakan NumPy:
      - Sangat cepat karena diimplementasikan dalam bahasa C.
      - Terintegrasi secara langsung dengan library Python lainnya (seperti Matplotlib, Scikit-Image, TensorFlow, dan PyTorch).
      - Memungkinkan manipulasi piksel secara langsung menggunakan operasi matriks matematika atau slicing.
    """)


# ==========================================
# MODULE 2: BGR VS RGB
# ==========================================
st.markdown("---")
st.header("2. Perbedaan Format BGR vs RGB", anchor="sec2")
st.write("Memahami susunan saluran warna (*channel*) default pada OpenCV.")

# Mengonversi gambar dari BGR (OpenCV default) ke RGB menggunakan cv2.cvtColor
rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)

col1_bgr, col2_rgb = st.columns(2)

with col1_bgr:
    st.subheader("🔴 Gambar BGR Asli (OpenCV Default)")
    # Menampilkan gambar BGR secara langsung di Streamlit. 
    # Karena Streamlit menganggap gambar ini berformat RGB, warna Merah dan Biru akan tertukar!
    st.image(bgr_image, caption="Warna biru/salah karena langsung ditampilkan tanpa konversi", use_container_width=True)
    st.info("Piksel dibaca dalam urutan: **[Blue, Green, Red]**")

with col2_rgb:
    st.subheader("🟢 Gambar Terkonversi (RGB)")
    # Menampilkan gambar setelah dikonversi ke RGB
    st.image(rgb_image, caption="Warna normal setelah dikonversi menggunakan cv2.cvtColor()", use_container_width=True)
    st.success("Piksel diatur ulang ke urutan: **[Red, Green, Blue]**")

st.subheader("Logika Kode Konversi")
st.code("""
# Konversi format BGR bawaan OpenCV ke RGB agar warna tampil normal pada library lain
rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
""", language="python")

with st.expander("📚 Mengapa OpenCV Menggunakan BGR Secara Default?"):
    st.markdown("""
    ### Sejarah BGR pada OpenCV:
    - OpenCV pertama kali dikembangkan oleh Intel pada tahun **1999**.
    - Pada masa itu, format **BGR** adalah standar yang sangat populer digunakan oleh produsen hardware kamera, kartu grafis, dan sistem operasi Windows (terutama pada representasi memori BMP).
    - Oleh karena alasan historis dan kompatibilitas hardware pada era tersebut, OpenCV mengadopsi urutan BGR.
    
    ### Kapan Kita Harus Melakukan Konversi?
    - **Kapan konversi BGR $\\rightarrow$ RGB diperlukan?** 
      Ketika Anda ingin menampilkan gambar menggunakan library Python lain yang mengharapkan input RGB (seperti Streamlit `st.image()`, Matplotlib `plt.imshow()`, atau Pillow `Image.fromarray()`).
    - **Kapan konversi tidak diperlukan?** 
      Jika Anda hanya melakukan pemrosesan matematika internal di OpenCV dan menyimpannya kembali ke file disk menggunakan `cv2.imwrite()`. OpenCV akan menulisnya kembali dengan benar karena ia tahu urutannya adalah BGR.
    """)


# ==========================================
# MODULE 3: IMAGE INFORMATION
# ==========================================
st.markdown("---")
st.header("3. Informasi Struktur Gambar & Piksel", anchor="sec3")
st.write("Menggunakan NumPy untuk membaca informasi data piksel gambar.")

# Menghitung statistik piksel menggunakan fungsi bawaan NumPy
min_val = bgr_image.min()
max_val = bgr_image.max()

# Layout metrik informasi
col_info1, col_info2, col_info3 = st.columns(3)
col_info1.metric("Width (Lebar Gambar)", f"{width} px")
col_info2.metric("Height (Tinggi Gambar)", f"{height} px")
col_info3.metric("Number of Channels", f"{channels} (Blue, Green, Red)")

col_info4, col_info5, col_info6 = st.columns(3)
col_info4.metric("Shape Array", str(bgr_image.shape))
col_info5.metric("Data Type piksel", str(bgr_image.dtype))
col_info6.metric("Memory Size (Bytes)", f"{bgr_image.nbytes:,} bytes")

col_info7, col_info8 = st.columns(2)
col_info7.metric("Minimum Pixel Value (Gelap)", str(min_val))
col_info8.metric("Maximum Pixel Value (Terang)", str(max_val))

with st.expander("📚 Penjelasan Hubungan: Gambar -> NumPy -> Shape -> Piksel"):
    st.markdown(r"""
    ### Alur Representasi Citra Digital:
    
    1. **Gambar (Image File)**:
       File fisik yang disimpan di disk komputer (seperti `sample.jpg`). File ini dikompresi agar ukurannya kecil.
       
    2. **NumPy Array**:
       Saat kita memanggil `cv2.imread()`, OpenCV membaca file terkompresi tersebut, mendekode datanya, dan menyusunnya menjadi blok memori numerik 3 dimensi yang disebut **NumPy Array**.
       
    3. **Shape (Bentuk Matriks)**:
       *Shape* mendefinisikan dimensi ruang dari array tersebut: `(height, width, channels)`.
       - **`height` (Tinggi)**: Mewakili baris (*rows*), dihitung dari atas ke bawah.
       - **`width` (Lebar)**: Mewakili kolom (*columns*), dihitung dari kiri ke kanan.
       - **`channels` (Saluran Warna)**: Lapisan warna bertumpuk. Untuk gambar BGR, indeks 0 = Blue, indeks 1 = Green, indeks 2 = Red.
       
    4. **Pixel Values (Nilai Piksel)**:
       Setiap elemen angka di dalam array bernilai antara **0** hingga **255** (untuk tipe data `uint8` atau unsigned integer 8-bit). Nilai ini menentukan seberapa terang intensitas cahaya di titik koordinat tersebut.
    """)


# ==========================================
# MODULE 4: RESIZE
# ==========================================
st.markdown("---")
st.header("4. Mengubah Ukuran Gambar (Resize)", anchor="sec4")
st.write("Mengubah resolusi gambar menggunakan fungsi `cv2.resize()` .")

col_inp1, col_inp2 = st.columns(2)
with col_inp1:
    target_width = st.number_input(
        "Target Width (Lebar Baru)", 
        min_value=10, 
        max_value=2000, 
        value=300, 
        step=1, 
        key="resize_width_input"
    )
with col_inp2:
    target_height = st.number_input(
        "Target Height (Tinggi Baru)", 
        min_value=10, 
        max_value=2000, 
        value=300, 
        step=1, 
        key="resize_height_input"
    )

# Melakukan resize gambar langsung menggunakan OpenCV
# PENTING: Urutan parameter ukuran di cv2.resize adalah (Width, Height)
resized_bgr = cv2.resize(bgr_image, (target_width, target_height))

# Mengonversi format ke RGB untuk ditampilkan oleh Streamlit
orig_rgb = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
resized_rgb = cv2.cvtColor(resized_bgr, cv2.COLOR_BGR2RGB)

# Menampilkan kode implementasi
st.code(f"""
# Mengubah ukuran gambar dengan OpenCV
# Parameter: cv2.resize(gambar_asli, (lebar_target, tinggi_target))
resized_image = cv2.resize(image, ({target_width}, {target_height}))
""", language="python")

col_res1, col_res2 = st.columns(2)

with col_res1:
    st.subheader(f"Gambar Asli ({width}x{height})")
    st.image(orig_rgb, use_container_width=True)
    st.write(f"Rasio Aspek Asli: **{width/height:.4f}**")
    
with col_res2:
    st.subheader(f"Gambar Hasil Resize ({target_width}x{target_height})")
    st.image(resized_rgb, use_container_width=True)
    st.write(f"Rasio Aspek Hasil: **{target_width/target_height:.4f}**")

with st.expander("📚 Analisis Distorsi & Hubungan Aspect Ratio"):
    st.markdown(f"""
    ### Peringatan Distorsi pada Direct Resize:
    - Rasio Aspek (*Aspect Ratio*) gambar asli adalah **{width/height:.4f}**.
    - Rasio Aspek target Anda saat ini adalah **{target_width/target_height:.4f}**.
    
    Jika kedua rasio aspek di atas berbeda, gambar hasil resize akan tampak **peyot, memanjang, atau memendek** secara tidak proporsional. 
    Hal ini dikarenakan setiap piksel ditarik secara paksa agar menempati ukuran koordinat baru tanpa memedulikan proporsionalitas objek di dalamnya.
    """)


# ==========================================
# MODULE 5: CROP
# ==========================================
st.markdown("---")
st.header("5. Pemotongan Gambar (Crop)", anchor="sec5")
st.write("Menggunakan teknik indexing/slicing NumPy Array untuk memotong area spesifik gambar.")

st.subheader("Tentukan Koordinat Area Pemotongan (Crop)")

col_sl1, col_sl2 = st.columns(2)
with col_sl1:
    x_start = st.slider("X Start (Batas Kiri)", 0, width - 2, 0, key="crop_x_start_slider")
    x_end = st.slider("X End (Batas Kanan)", x_start + 1, width, width, key="crop_x_end_slider")
with col_sl2:
    y_start = st.slider("Y Start (Batas Atas)", 0, height - 2, 0, key="crop_y_start_slider")
    y_end = st.slider("Y End (Batas Bawah)", y_start + 1, height, height, key="crop_y_end_slider")

# Slicing matriks NumPy untuk pemotongan gambar [y1:y2, x1:x2]
cropped_bgr = bgr_image[y_start:y_end, x_start:x_end]

# Mengonversi format ke RGB untuk ditampilkan
cropped_rgb = cv2.cvtColor(cropped_bgr, cv2.COLOR_BGR2RGB)

st.code(f"""
# Crop menggunakan slicing matriks NumPy [y_start:y_end, x_start:x_end]
cropped_image = image[{y_start}:{y_end}, {x_start}:{x_end}]
""", language="python")

col_crop1, col_crop2 = st.columns(2)

with col_crop1:
    st.subheader("Gambar Asli (Dengan Batas Crop)")
    # Membuat visualisasi kotak batas hijau
    visual_orig = bgr_image.copy()
    cv2.rectangle(
        visual_orig, 
        (x_start, y_start), 
        (x_end, y_end), 
        (0, 255, 0), 
        4 
    )
    visual_orig_rgb = cv2.cvtColor(visual_orig, cv2.COLOR_BGR2RGB)
    st.image(visual_orig_rgb, use_container_width=True)
    st.write(f"Koordinat terpilih: **X=[{x_start}:{x_end}], Y=[{y_start}:{y_end}]**")

with col_crop2:
    st.subheader("Hasil Pemotongan (Cropped)")
    st.image(cropped_rgb, use_container_width=True)
    st.write(f"Ukuran Hasil Crop: **{cropped_bgr.shape[1]}x{cropped_bgr.shape[0]} px**")

with st.expander("📚 Penjelasan Eksplisit Slicing: [y1:y2, x1:x2]"):
    st.markdown(r"""
    ### Mengapa pemotongan ditulis sebagai `image[y1:y2, x1:x2]`?
    
    Dalam NumPy, array 2D/3D diakses menggunakan standar indeks baris (*row*) terlebih dahulu, baru diikuti indeks kolom (*column*):
    
    $$\text{array}[\text{baris}, \text{kolom}]$$
    
    - **Baris (Row)** bergerak secara vertikal dari atas ke bawah. Ini mewakili sumbu **Y**. Sehingga `row_start:row_end` sama dengan `y_start:y_end`.
    - **Kolom (Column)** bergerak secara horizontal dari kiri ke kanan. Ini mewakili sumbu **X**. Sehingga `column_start:column_end` sama dengan `x_start:x_end`.
    
    Oleh karena itu:
    - `image[y_start:y_end, x_start:x_end]` secara eksplisit berarti `image[row_start:row_end, column_start:column_end]`.
    """)


# ==========================================
# MODULE 6: FLIP
# ==========================================
st.markdown("---")
st.header("6. Membalik Gambar (Flip)", anchor="sec6")
st.write("Membalik orientasi gambar secara horizontal, vertikal, atau kedua arah menggunakan `cv2.flip()`.")

flip_mode = st.radio(
    "Pilih Arah Pembalikan (Flip Mode):",
    ["Horizontal Flip", "Vertical Flip", "Horizontal & Vertical Flip (Both)"],
    key="flip_mode_radio"
)

if flip_mode == "Horizontal Flip":
    flip_code = 1
    flip_desc = "Membalik arah kiri-kanan (cermin horizontal)"
elif flip_mode == "Vertical Flip":
    flip_code = 0
    flip_desc = "Membalik arah atas-bawah (cermin vertikal)"
else:
    flip_code = -1
    flip_desc = "Membalik kedua arah sekaligus (rotasi 180 derajat)"

# Melakukan operasi pembalikan gambar
flipped_bgr = cv2.flip(bgr_image, flip_code)
flipped_rgb = cv2.cvtColor(flipped_bgr, cv2.COLOR_BGR2RGB)

st.code(f"""
# Membalik gambar menggunakan OpenCV
# Parameter flipCode: 1 = Horizontal, 0 = Vertical, -1 = Both
flipped_image = cv2.flip(image, {flip_code})
""", language="python")

col_flip1, col_flip2 = st.columns(2)

with col_flip1:
    st.subheader("Gambar Asli")
    st.image(rgb_for_display, use_container_width=True)

with col_flip2:
    st.subheader(f"Hasil Flip ({flip_mode})")
    st.image(flipped_rgb, use_container_width=True)
    st.write(f"Deskripsi Aksi: **{flip_desc}**")


# ==========================================
# MODULE 7: ROTATE
# ==========================================
st.markdown("---")
st.header("7. Memutar Gambar (Rotate)", anchor="sec7")
st.write("Memutar arah gambar menggunakan fungsi bawaan `cv2.rotate()` .")

rotate_mode = st.radio(
    "Pilih Sudut Rotasi:",
    ["Rotate 90 Clockwise", "Rotate 90 Counterclockwise", "Rotate 180"],
    key="rotate_mode_radio"
)

if rotate_mode == "Rotate 90 Clockwise":
    rotate_code = cv2.ROTATE_90_CLOCKWISE
    rotate_str = "cv2.ROTATE_90_CLOCKWISE"
elif rotate_mode == "Rotate 90 Counterclockwise":
    rotate_code = cv2.ROTATE_90_COUNTERCLOCKWISE
    rotate_str = "cv2.ROTATE_90_COUNTERCLOCKWISE"
else:
    rotate_code = cv2.ROTATE_180
    rotate_str = "cv2.ROTATE_180"

# Melakukan pemutaran gambar
rotated_bgr = cv2.rotate(bgr_image, rotate_code)
rotated_rgb = cv2.cvtColor(rotated_bgr, cv2.COLOR_BGR2RGB)

st.code(f"""
# Memutar gambar menggunakan kode bawaan OpenCV
# Pilihan: cv2.ROTATE_90_CLOCKWISE, cv2.ROTATE_90_COUNTERCLOCKWISE, cv2.ROTATE_180
rotated_image = cv2.rotate(image, {rotate_str})
""", language="python")

col_rot1, col_rot2 = st.columns(2)

with col_rot1:
    st.subheader("Gambar Asli")
    st.image(rgb_for_display, use_container_width=True)
    st.write(f"Dimensi Asli: **{width}x{height} px**")

with col_rot2:
    st.subheader(f"Hasil Rotasi ({rotate_mode})")
    st.image(rotated_rgb, use_container_width=True)
    st.write(f"Dimensi Baru: **{rotated_bgr.shape[1]}x{rotated_bgr.shape[0]} px**")


# ==========================================
# MODULE 8: SAVE IMAGE
# ==========================================
st.markdown("---")
st.header("8. Menyimpan Gambar ke Penyimpanan (Disk)", anchor="sec8")
st.write("Menggunakan fungsi `cv2.imwrite()` untuk menulis data array kembali menjadi file gambar.")

st.subheader("Langkah 1: Pilih Efek Pemrosesan untuk Disimpan")
effect = st.selectbox(
    "Pilih efek manipulasi gambar sebelum disimpan:",
    ["Tanpa Pemrosesan (Asli)", "Flipped Horizontal", "Rotated 180", "Crop Area Tengah"],
    key="save_effect_select"
)

# Memproses gambar berdasarkan pilihan efek
if effect == "Tanpa Pemrosesan (Asli)":
    processed_bgr = bgr_image.copy()
    eff_desc = "Gambar Asli"
elif effect == "Flipped Horizontal":
    processed_bgr = cv2.flip(bgr_image, 1)
    eff_desc = "Flipped Horizontal"
elif effect == "Rotated 180":
    processed_bgr = cv2.rotate(bgr_image, cv2.ROTATE_180)
    eff_desc = "Rotated 180"
else:
    # Potong area tengah gambar
    h_crop, w_crop = height // 2, width // 2
    y1, y2 = h_crop - min(h_crop, 150), h_crop + min(h_crop, 150)
    x1, x2 = w_crop - min(w_crop, 150), w_crop + min(w_crop, 150)
    processed_bgr = bgr_image[y1:y2, x1:x2]
    eff_desc = "Cropped Area Tengah (300x300 px)"

# Mengonversi hasil pemrosesan ke RGB agar warna di Streamlit benar
processed_rgb = cv2.cvtColor(processed_bgr, cv2.COLOR_BGR2RGB)

col_save_img, col_save_action = st.columns([2, 1])

with col_save_img:
    st.subheader("Pratinjau Gambar Hasil Pemrosesan")
    st.image(processed_rgb, caption=f"Efek: {eff_desc}", use_container_width=True)

with col_save_action:
    st.subheader("Langkah 2: Tentukan Nama Berkas & Simpan")
    
    output_filename = st.text_input(
        "Nama File Output (.jpg atau .png):", 
        value="images/processed_output.jpg",
        key="save_filename_input"
    )
    
    # PENTING: cv2.imwrite() mengharapkan array dalam format BGR.
    if st.button("💾 Simpan Gambar ke Disk", key="save_image_button"):
        output_path = Path(output_filename)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Melakukan penyimpanan gambar ke disk
        success = cv2.imwrite(str(output_path), processed_bgr)
        
        if success:
            st.success(f"Gambar berhasil disimpan! File tersimpan di: **{output_path.absolute()}**")
        else:
            st.error("Gagal menyimpan gambar. Pastikan Anda memiliki akses tulis ke direktori target.")

st.subheader("Logika & Hal Penting Mengenai cv2.imwrite")
st.code(f"""
# Menyimpan matriks array gambar kembali menjadi file gambar fisik di disk komputer
# Parameter: cv2.imwrite("nama_path_berkas", array_gambar_BGR)
cv2.imwrite("{output_filename}", processed_bgr)
""", language="python")

with st.expander("📚 PENTING: Mengapa kita harus memberikan BGR ke cv2.imwrite()?"):
    st.markdown(r"""
    ### Peringatan Terkait Format Warna Saat Menyimpan:
    - Fungsi `cv2.imwrite()` dirancang untuk bekerja secara internal dengan sistem bawaan OpenCV. 
    - Karena OpenCV membaca gambar sebagai **BGR**, maka fungsi `cv2.imwrite()` juga mengharapkan input array berformat **BGR** agar dapat mengompresi dan memetakan warna dengan benar ke file fisik (.jpg atau .png).
    
    #### Apa yang terjadi jika kita memberikan array RGB ke `cv2.imwrite()`?
    Jika Anda mengirimkan array yang telah dikonversi ke **RGB** (misalnya `rgb_image`) ke dalam `cv2.imwrite()`, fungsi tersebut akan mengira saluran pertama (Red) adalah Blue, dan saluran ketiga (Blue) adalah Red.
    Akibatnya, berkas gambar yang tersimpan di disk akan mengalami **kerusakan warna** (tampak kebiru-biruan)!
    
    Oleh karena itu:
    - Gunakan **RGB** hanya untuk keperluan **tampilan luar** (Streamlit, Matplotlib).
    - Gunakan **BGR** asli untuk operasi pemrosesan **OpenCV internal** dan pemanggilan **`cv2.imwrite()`**.
    """)
