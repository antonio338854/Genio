import streamlit as st
import google.generativeai as genai

# --- Configuração ---
st.set_page_config(page_title="Gemini 2.5", page_icon="⚡")
st.title("⚡ Gemini 2.5 Flash")

# 1. PEGAR A CHAVE
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("Coloque a chave GOOGLE_API_KEY nos Secrets!")
    st.stop()

# 2. SELEÇÃO DE MODELO (MODO TEIMOSO)
# Vamos tentar os nomes possíveis do 2.5 até um funcionar
nomes_para_testar = [
    "gemini-2.5-flash",
    "models/gemini-2.5-flash", 
    "gemini-2.0-flash-exp", 
    "gemini-1.5-flash"
]

modelo_ativo = None
nome_final = ""

with st.spinner("Conectando no satélite do Google..."):
    for nome in nomes_para_testar:
        try:
            teste_modelo = genai.GenerativeModel(nome)
            # Teste de vida rápido
            teste_modelo.generate_content("Oi")
            # Se não deu erro, achamos!
            modelo_ativo = teste_modelo
            nome_final = nome
            break
        except:
            continue

if modelo_ativo:
    st.toast(f"Conectado com sucesso no: {nome_final} 🚀", icon="✅")
else:
    st.error("❌ ERRO CRÍTICO: Nenhum modelo funcionou. Verifique se sua chave API tem permissão ou atualize o requirements.txt")
    st.stop()

# 3. CHAT
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Manda ver..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.mensagens.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        try:
            chat = modelo_ativo.start_chat(history=[
                {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]}
                for m in st.session_state.mensagens[:-1]
            ])
            response = chat.send_message(prompt, stream=True)
            
            texto = st.write_stream(response)
            st.session_state.mensagens.append({"role": "assistant", "content": texto})
        except Exception as e:
            st.error(f"Erro: {e}")
