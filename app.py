import streamlit as st
from groq import Groq

st.set_page_config(page_title="Affiliate AI Studio", page_icon="⚡", layout="centered")

# Mengambil API Key Groq dari Secrets
try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=groq_api_key)
except Exception:
    client = None

st.title("⚡ AffiliateAI Studio")
st.caption("Engine: Groq AI (Llama 3 Fast & Free)")

st.divider()

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
    elif not client:
        st.error("API Key Groq belum terpasang di Streamlit Secrets!")
    else:
        with st.spinner("🧠 Groq AI sedang meracik naskah viral super cepat..."):
            prompt = f"""
            Kamu adalah konsultan affiliate marketing TikTok/Shopee Indonesia yang jenius.
            Buatkan naskah video pendek (durasi 30 detik) berdasarkan ide produk dari link ini: {url_input}.
            Target Avatar: {avatar_style}.
            Gaya Bahasa: {tone_style} (gunakan bahasa gaul anak muda Indonesia, sangat relatable, persuasif, tanpa kata-kata kaku).
            
            Buat dalam format struktur:
            1. HOOK (3 detik pertama - kalimat kontroversial/penasaran biar penonton tidak scroll)
            2. BODY (Problem + Solusi + Keunggulan produk)
            3. CTA (Call to Action - ajakan tegas klik keranjang kuning/link di bio)
            """
            
            try:
                response = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.1-8b-instant",
                    temperature=0.7
                )
                
                script_result = response.choices[0].message.content
                
                st.success("✅ Naskah Video AI Berhasil Dibuat!")
                st.markdown("### 📜 Draft Naskah Auto-Avatar:")
                st.info(script_result)
                
            except Exception as e:
                st.error(f"Gagal memproses AI: {str(e)}")

st.divider()
st.caption("Affiliate Studio v1.0 • Groq Engine Active")
