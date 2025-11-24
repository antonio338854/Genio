import streamlit as st
import google.generativeai as genai
import time

st.set_page_config(page_title="Teste do Vovô", page_icon="🔧")

st.title("🔧 Modo de Diagnóstico")
st.write("1. Iniciando o aplicativo... OK")

# --- TESTE DA CHAVE ---
st.write("2. Verificando a chave de segurança...")

if "GOOGLE_API_KEY" in st.secrets:
    st.success("✅ Chave encontrada nos Secrets!")
    chave = st.secrets["GOOGLE_API_KEY"]
else:
    st.error("❌ ERRO: A chave 'GOOGLE_API_KEY' não está nos Secrets.")
    st.info("Vá em Settings -> Secrets e cole: GOOGLE_API_KEY = 'sua-chave'")
    st.stop() # Para aqui se der erro

# --- TESTE DE CONEXÃO ---
st.write("3. Conectando com o Google Gemini...")

try:
    genai.configure(api_key=chave)
    # Vamos usar o modelo mais estável para teste
    modelo = genai.GenerativeModel('gemini-1.5-flash')
    st.success("✅ Conexão com Google OK!")
except Exception as e:
    st.error(f"❌ Erro ao conectar no Google: {e}")
    st.stop()

# --- CHAT ---
st.write("4. Carregando interface do Chat...")
st.divider()

# Histórico
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

# Mostra msg inicial se estiver vazio
if not st.session_state.mensagens:
    st.info("O Chat está pronto! Olhe para baixo 👇")

for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- O CAMPO DE DIGITAR ---
prompt = st.chat_input("Digita um 'Oi' aqui embaixo...")

if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.mensagens.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        try:
            response = modelo.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.mensagens.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Erro ao responder: {e}")
