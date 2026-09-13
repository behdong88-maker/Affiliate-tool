import streamlit as st
import time

# Konfigurasi Tampilan HP
st.set_page_config(page_title="Affiliate AI Studio", page_icon="⚡", layout="centered")

# Header Dashboard
st.title("⚡ AffiliateAI Studio")
st.caption("Auto-Post & Content Generator Ready")

st.divider()

# Form Input di HP
st.subheader("🚀 Generate Video Baru")

url = st.text_input("Link Video Referensi (TikTok / Shopee)", placeholder="https://vt.tiktok.com/...")

col1, col2 = st.columns(2)
with col1:
    avatar = st.selectbox("Avatar AI", ["Pria Kasual (Indo)", "Wanita Hijab (Estetik)", "Pria Reviewer"])
with col2:
    tone = st.selectbox("Gaya Bahasa", ["Gaul & Santai", "Hypnotic Selling", "Kombinasi (Random)"])

if st.button("✨ Buat Video Sekarang", use_container_width=True):
    if not url:
        st.error("Tolong tempelkan link video referensinya dulu!")
    else:
        st.info("⏳ Video sedang diproses di cloud server... Anda bisa menutup halaman ini.")
        # Simulasi pemrosesan backend
        time.sleep(3)
        st.success("✅ Proses pembuatan video AI telah dimulai dan akan diposting otomatis!")

st.divider()

# Live Analytics Quick View
st.subheader("🔥 Winning Product Today")
st.metric(label="Lampung Mini Fan Portable", value="HOT", delta="Est. Komisi: Rp 12.500/pcs")
