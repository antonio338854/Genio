import streamlit as st
import google.generativeai as genai

# --- O SEGREDO ESTÁ AQUI ---
# O código tenta pegar a chave do cofre do Streamlit
try:
    minha_chave = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("Ops! Falta a chave de segurança no painel do Streamlit.")
    st.stop()

# Configura a IA usando a variável, NUNCA a senha real
genai.configure(api_key=minha_chave)

# ... resto do código do chat ...
