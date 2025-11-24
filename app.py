import streamlit as st
import google.generativeai as genai

# --- Configuração ---
st.set_page_config(page_title="Gemini 2.5 Flash", page_icon="⚡")
st.title("⚡ Gemini 2.5 Flash")

# 1. PEGAR A CHAVE (Secrets)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("Coloque a chave GOOGLE_API_KEY nos Secrets!")
    st.stop()

# 2. SELEÇÃO DE MODELO (MODO TEIMOSO)
nomes_para_testar = [
    "gemini-2.5-flash", 
    "gemini-2.0-flash-exp", 
    "gemini-1.5-flash",
    "gemini-pro"
]

modelo_ativo = None

# Tenta achar um modelo que funcione
for nome in nomes_para_testar:
    try:
        teste = genai.GenerativeModel(nome)
        modelo_ativo = teste
        # st.toast(f"Usando: {nome}", icon="🤖") # Comentei pra não poluir
        break
    except:
        continue

if not modelo_ativo:
    st.error("Erro: Nenhum modelo disponível. Verifique a chave.")
    st.stop()

# 3. BOTÃO DE RESET (IMPORTANTE PARA CORRIGIR SEU ERRO)
if st.button("🗑️ Limpar Conversa (Resolver Erros)"):
    st.session_state.mensagens = []
    st.rerun()

# 4. CHAT
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

# Mostra histórico na tela
for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. ENVIAR MENSAGEM
if prompt := st.chat_input("Digite aqui..."):
    # Mostra mensagem do usuário
    st.chat_message("user").markdown(prompt)
    st.session_state.mensagens.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            # --- A CORREÇÃO DO ERRO ESTÁ AQUI ---
            # Vamos criar um histórico limpo, convertendo tudo para TEXTO PURO
            historico_limpo = []
            for m in st.session_state.mensagens[:-1]: # Pega tudo menos a última
                role_google = "user" if m["role"] == "user" else "model"
                # Forçamos virar string (str) para evitar o erro de "Content Object"
                historico_limpo.append({
                    "role": role_google,
                    "parts": [str(m["content"])] 
                })

            # Inicia o chat com o histórico limpo
            chat = modelo_ativo.start_chat(history=historico_limpo)
            
            # Envia a mensagem nova
            response = chat.send_message(prompt, stream=True)
            
            texto_completo = ""
            for pedaco in response:
                if pedaco.text:
                    texto_completo += pedaco.text
                    message_placeholder.markdown(texto_completo + "▌")
            
            message_placeholder.markdown(texto_completo)
            
            # Salva resposta
            st.session_state.mensagens.append({"role": "assistant", "content": texto_completo})
            
        except Exception as e:
            # Se der erro, mostramos de forma amigável
            st.error(f"Erro: {e}")
            st.info("Dica: Clique no botão 'Limpar Conversa' lá em cima!")
