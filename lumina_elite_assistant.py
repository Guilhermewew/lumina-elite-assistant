import os
import streamlit as st
from groq import Groq
import time

# -----------------------------------------------------------------------------
# CONFIGURAÇÃO DE ELITE - INTERFACE & ANIMAÇÕES
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="LUMINA | Elite Programming Assistant",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS com Animações e Glassmorphism
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=Fira+Code:wght@400;500&display=swap');
    
    /* Variáveis de Cor */
    :root {
        --primary: #38bdf8;
        --bg-dark: #0f172a;
        --glass: rgba(30, 41, 59, 0.7);
        --border: rgba(255, 255, 255, 0.1);
    }

    .main { background-color: var(--bg-dark); }
    
    /* Animação de Entrada das Mensagens */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Efeito de Vidro no Chat */
    .stChatMessage {
        animation: fadeInUp 0.5s ease-out forwards;
        background: var(--glass) !important;
        backdrop-filter: blur(10px);
        border: 1px solid var(--border) !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        margin-bottom: 1.2rem !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s ease;
    }
    
    .stChatMessage:hover {
        transform: scale(1.01);
        border-color: var(--primary) !important;
    }

    /* Avatar Glow Animado */
    .stChatFloatingInputContainer {
        background-color: transparent !important;
    }

    /* Status Badge Dinâmico */
    .status-badge {
        padding: 6px 14px;
        border-radius: 30px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(56, 189, 248, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(56, 189, 248, 0); }
        100% { box-shadow: 0 0 0 0 rgba(56, 189, 248, 0); }
    }

    .status-online { background: rgba(6, 78, 59, 0.8); color: #34d399; border: 1px solid #059669; }
    .status-offline { background: rgba(69, 10, 10, 0.8); color: #f87171; border: 1px solid #b91c1c; }

    /* Typography */
    h1 { 
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        letter-spacing: -1px;
    }
    
    /* Botão Customizado */
    .stButton>button {
        background: linear-gradient(45deg, #0ea5e9, #6366f1);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(99, 102, 241, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# LÓGICA DE CONEXÃO
# -----------------------------------------------------------------------------
def validate_connection(api_key):
    if not api_key: return False, "Aguardando Chave"
    try:
        client = Groq(api_key=api_key)
        client.models.list()
        return True, "Sistema Online"
    except: return False, "Erro de Conexão"

# -----------------------------------------------------------------------------
# SIDEBAR
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>✨ LUMINA</h1>", unsafe_allow_html=True)
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=80)
    
    st.markdown("### 🛠️ Core Engine")
    api_key = st.text_input("Groq API Key", type="password", placeholder="gsk_...")
    
    is_online, status_text = validate_connection(api_key)
    status_class = "status-online" if is_online else "status-offline"
    st.markdown(f'<div class="status-badge {status_class}">● {status_text}</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    model_option = st.selectbox("Modelo de Elite", ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"])
    
    if st.button("🗑️ Resetar Sessão"):
        st.session_state.messages = []
        st.rerun()

# -----------------------------------------------------------------------------
# CHAT ENGINE
# -----------------------------------------------------------------------------
st.markdown("<h1>LUMINA | Intelligence Architecture</h1>", unsafe_allow_html=True)
st.caption("Desenvolvimento Elite com Performance em Tempo Real")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibição das mensagens com efeito de fade
for i, message in enumerate(st.session_state.messages):
    avatar = "👤" if message["role"] == "user" else "✨"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Input e Lógica de Resposta
if prompt := st.chat_input("Como posso elevar seu código hoje?"):
    if not api_key:
        st.error("⚠️ Chave de API necessária na barra lateral.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="✨"):
        placeholder = st.empty()
        full_response = ""
        
        try:
            client = Groq(api_key=api_key)
            system_prompt = "Você é LUMINA, uma IA de elite. Responda com arquitetura impecável, código Python elegante e insights profundos."
            
            stream = client.chat.completions.create(
                messages=[{"role": "system", "content": system_prompt}] + st.session_state.messages,
                model=model_option,
                temperature=0.3,
                stream=True,
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    placeholder.markdown(full_response + "▌")
            
            placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"🚨 Erro: {str(e)}")

# Rodapé Animado
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
    "<div style='text-align: center; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 20px; opacity: 0.5;'>"
    "LUMINA v3.0 | Glassmorphism UI | Elite Performance"
    "</div>", 
    unsafe_allow_html=True
)
