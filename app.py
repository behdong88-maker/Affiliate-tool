import streamlit as st
from groq import Groq

st.set_page_config(page_title="Affiliate AI Studio", page_icon="⚡", layout="centered")

st.title("⚡ AffiliateAI Studio")
st.caption("Engine: Groq AI Auto-Script Generator")

st.divider()

# Cek Keberadaan API Key
groq_api_key = st.secrets.get("GROQ_API_KEY", None)

if not groq_api_key:
    st.error("⚠️ GROQ_API_KEY belum ditemukan di Streamlit Secrets!")
    st.info("Buka share.streamlit.io -> Settings -> Secrets -> Masukkan GROQ_API_KEY = 'gsk_...'")
    st.stop()

# Inisialisasi Client
client = Groq(api_key=groq_api_key)

st.subheader("🚀 Generate Script & Content AI")

url_input = st.text_input("Link Video Referensi (TikTok / Shopee)", placeholder="https://vt.tiktok.com/...")

col1, col2 = st.columns(2)
with col1:
    avatar_style = st.selectbox("Avatar AI Target", ["Pria Kasual (Indo)", "Wanita Hijab (Estetik)", "Pria Reviewer"])
with col2:
    tone_style = st.selectbox("Gaya Bahasa", ["Gaul & Santai", "Hypnotic Selling", "Kombinasi (Random)"])

if st.button("✨ Buat Naskah & Video", use_container_width=True):
    if not url_input:
        st.error("Tolong masukkan link video referensinya dulu!")
    else:
        with st.spinner("🧠 Groq AI sedang meracik naskah viral..."):
            prompt = f"""
            Kamu adalah konsultan affiliate marketing TikTok/Shopee Indonesia yang jenius.
            Buatkan naskah video pendek (durasi 30 detik) berdasarkan ide produk dari link ini: {url_input}.
            Target Avatar: {avatar_style}.
            Gaya Bahasa: {tone_style} (gunakan bahasa gaul anak muda Indonesia, relatable, persuasif).
            
            Buat dalam format struktur:
            1. HOOK (3 detik pertama - kalimat kontroversial/penasaran)
            2. BODY (Problem + Solusi + Keunggulan produk)
            3. CTA (Call to Action - ajakan klik keranjang kuning/link di bio)
            """
            
            # Daftar pilihan model dari yang paling umum hingga alternatif
            candidate_models = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "openai/gpt-oss-120b", "openai/gpt-oss-20b"]
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
                    break # Jika berhasil, keluar dari loop
                except Exception as e:
                    last_error = str(e)
                    continue

            if script_result:
                st.success("✅ Naskah Video AI Berhasil Dibuat!")
                st.markdown("### 📜 Draft Naskah Auto-Avatar:")
                st.info(script_result)
            else:
                st.error(f"Gagal memproses AI: {last_error}")

st.divider()
st.caption("Affiliate Studio v1.0 • Groq Engine Active")
