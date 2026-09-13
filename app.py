import streamlit as st
import requests
from bs4 import BeautifulSoup
from groq import Groq
import re

st.set_page_config(page_title="Affiliate AI Studio", page_icon="⚡", layout="centered")

st.title("⚡ AffiliateAI Studio")
st.caption("Engine: Groq AI + Web Content Scraper")

st.divider()

# Cek Keberadaan API Key
groq_api_key = st.secrets.get("GROQ_API_KEY", None)

if not groq_api_key:
    st.error("⚠️ GROQ_API_KEY belum ditemukan di Streamlit Secrets!")
    st.info("Buka share.streamlit.io -> Settings -> Secrets -> Masukkan GROQ_API_KEY = 'gsk_...'")
    st.stop()

# Inisialisasi Client Groq
client = Groq(api_key=groq_api_key)

# Fungsi Scraper Metadata Link
def extract_link_context(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=8)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Ambil judul dari Tag Meta OpenGraph
            title = soup.find("meta", property="og:title")
            description = soup.find("meta", property="og:description")
            
            title_text = title["content"] if title else soup.title.string if soup.title else ""
            desc_text = description["content"] if description else ""
            
            context = f"Judul Produk/Konten: {title_text}\nDeskripsi: {desc_text}"
            return context if title_text or desc_text else None
    except Exception:
        pass
    return None

st.subheader("🚀 Generate Script & Content AI")

url_input = st.text_input("Link Video / Produk Referensi (TikTok / Shopee)", placeholder="https://vt.tiktok.com/...")

col1, col2 = st.columns(2)
with col1:
    avatar_style = st.selectbox("Avatar AI Target", ["Pria Kasual (Indo)", "Wanita Hijab (Estetik)", "Pria Reviewer"])
with col2:
    tone_style = st.selectbox("Gaya Bahasa", ["Gaul & Santai", "Hypnotic Selling", "Kombinasi (Random)"])

if st.button("✨ Buat Naskah Sesuai Produk", use_container_width=True):
    if not url_input:
        st.error("Tolong masukkan link referensinya dulu!")
    else:
        with st.spinner("🔍 Membaca isi produk dari link & meracik naskah..."):
            
            # 1. Ekstraksi Data dari Link
            extracted_info = extract_link_context(url_input)
            
            if extracted_info:
                st.toast("✅ Berhasil membaca metadata produk dari link!", icon="📦")
                context_prompt = f"Informasi Produk yang didapatkan dari link:\n{extracted_info}"
            else:
                st.toast("⚠️ Metadata link tidak dapat di-scrape penuh. Menggunakan ekstraksi nama link...", icon="⚠️")
                clean_url_name = re.sub(r'https?://(www\.)?', '', url_input).split('/')[0]
                context_prompt = f"Link referensi: {url_input} (Domain: {clean_url_name})"

            # 2. Susun Prompt Spesifik
            prompt = f"""
            Kamu adalah konsultan affiliate marketing TikTok/Shopee Indonesia yang jenius.
            {context_prompt}

            Tugas utama: Buatkan naskah video pendek (durasi 30 detik) yang AKURAT membahas keunggulan produk di atas.
            Target Avatar: {avatar_style}.
            Gaya Bahasa: {tone_style} (bahasa gaul anak muda Indonesia, relatable, persuasif, tanpa kata-kata kaku).
            
            Format Output wajib:
            1. HOOK (3 detik pertama - kalimat kontroversial/penasaran spesifik tentang produk ini)
            2. BODY (Problem + Solusi + Keunggulan utama produk)
            3. CTA (Call to Action - ajakan tegas klik keranjang kuning/link di bio)
            """

            # 3. Kirim ke Groq AI
            candidate_models = [
                "llama-3.3-70b-versatile",
                "llama3-70b-8192",
                "mixtral-8x7b-32768"
            script_result = None
            last_error = None

            for model_name in candidate_models:
                try:
                    response = client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model=model_name,
                        temperature=0.7
                    )
                    script_result = response.choices[0].message.content
                    break
                except Exception as e:
                    last_error = str(e)
                    continue

            if script_result:
                st.success("✅ Naskah Video AI Berhasil Dibuat!")
                if extracted_info:
                    st.caption(f"📌 Informasi Produk Terdeteksi: {extracted_info[:100]}...")
                st.markdown("### 📜 Draft Naskah Auto-Avatar:")
                st.info(script_result)
            else:
                st.error(f"Gagal memproses AI: {last_error}")

st.divider()
st.caption("Affiliate Studio v1.1 • Web Scraper Active")
