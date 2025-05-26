import streamlit as st
import requests

# --- Configuración de la API ---
API_KEY = 'sk-53751d5c6f344a5dbc0571de9f51313e'  # ⚠️ ¡NO usar directamente en producción!
API_URL = 'https://api.deepseek.com/v1/chat/completions'

# --- Función para enviar mensaje a la API ---
def enviar_mensaje(mensaje, modelo="deepseek-chat"):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": modelo,
        "messages": st.session_state.messages + [{"role": "user", "content": mensaje}]
    }

    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code == 200:
        respuesta = response.json()["choices"][0]["message"]
        return respuesta
    else:
        st.error(f"Error en la API: {response.status_code}")
        return {"role": "assistant", "content": "Lo siento, ocurrió un error."}

# --- Inicializar historial de conversación ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Mostrar historial de mensajes ---
st.title("💬 Chat con DeepSeek")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Entrada del usuario ---
mensaje_usuario = st.chat_input("Escribe tu mensaje aquí...")

if mensaje_usuario:
    # Agregar mensaje del usuario al historial
    st.session_state.messages.append({"role": "user", "content": mensaje_usuario})

    # Mostrar mensaje del usuario
    with st.chat_message("user"):
        st.markdown(mensaje_usuario)

    # Obtener y mostrar respuesta
    respuesta = enviar_mensaje(mensaje_usuario)
    st.session_state.messages.append(respuesta)

    with st.chat_message("assistant"):
        st.markdown(respuesta["content"])
