import streamlit as st
import openai
import time

st.set_page_config(page_title="Affiliate AI Studio", page_icon="⚡", layout="centered")

# Mengambil API Key dari Secrets Streamlit
try:
    openai_api_key = st.secrets["OPENAI_API_KEY"]
    client = openai.OpenAI(api_key=openai_api_key)
except Exception:
    client = None

st.title("⚡ AffiliateAI Studio")
st.caption("Engine: OpenAI GPT-4o-mini Auto-Script Generator")

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
        st.error("API Key belum terpasang di Streamlit Secrets!")
    else:
        with st.spinner("🧠 AI sedang menganalisis konten & menyusun naskah viral..."):
            # Prompt Engineering khusus Affiliate Indonesia
            prompt = f"""
            Kamu adalah konsultan affiliate marketing TikTok/Shopee Indonesia yang jenius.
            Buatkan naskah video pendek (durasi 30 detik) berdasarkan ide produk dari link ini: {url_input}.
            Target Avatar: {avatar_style}.
            Gaya Bahasa: {tone_style} (gunakan bahasa gaul anak muda Indonesia, relatable, tanpa kata-kata kaku).
            
            Buat dalam format struktur:
            1. HOOK (3 detik pertama - harus bikin orang berhenti scroll!)
            2. BODY (Problem + Solusi + Value produk)
            3. CTA (Call to Action - ajakan klik keranjang kuning/link bio)
            """
            
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )
                
                script_result = response.choices[0].message.content
                
                st.success("✅ Naskah Video AI Berhasil Dibuat!")
                st.markdown("### 📜 Draft Naskah Auto-Avatar:")
                st.info(script_result)
                
                st.warning("⚡ Langkah Selanjutnya: Mengirim naskah ini ke Engine Avatar AI untuk render video 30 detik...")
                
            except Exception as e:
                st.error(f"Gagal memproses AI: {str(e)}")

st.divider()
st.caption("Affiliate Studio v1.0 • PWA Ready")
