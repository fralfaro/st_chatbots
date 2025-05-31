# cittripio_app.py

import streamlit as st
import requests
import json
import os
import toml


# ========================
# Sección: streamlit_magic
# ========================

VERBOSE = True

avatar_dict = {
    "user": os.path.join("app", "images", "user.png"),
    "assistant": os.path.join("app", "images", "assistant.png")
}

def hide_sidebar():
    if st.secrets["DISABLE_SIDEBAR"]:
        st.markdown("""
        <style>
            [data-testid="stSidebarCollapsedControl"] {
                display: none
            }
        </style>
        """, unsafe_allow_html=True)
    return

def apply_colors(token_list):
    colors = [":red-background[{}]", ":orange-background[{}]", ":green-background[{}]",
              ":blue-background[{}]", ":violet-background[{}]", ":gray-background[{}]"]
    color_str = ""
    for i, it in enumerate(token_list):
        color_format = colors[i % len(colors)]
        color_str += color_format.format(str(it))
    return color_str

def get_api_key(use_streamlit=True, verbose=VERBOSE):
    if use_streamlit:
        return st.secrets["OPENROUTER_API_KEY"]
    else:
        with open(".streamlit/secrets.toml", "r") as file:
            secrets = toml.load(file)
        return secrets["OPENROUTER_API_KEY"]

@st.dialog(title="Código de la aplicación", width="large")
def popup_code(filepath):
    with open(filepath, "r") as file:
        st.code(file.read(), language="python")

# =====================
# Sección: llm_magic
# =====================

available_models_dict = {
    "DeepSeek-V3 (free)": "deepseek/deepseek-chat-v3-0324:free",
    "QWEN-32b (free)": "qwen/qwq-32b:free",
    "Meta-Llama (free)": "meta-llama/llama-3.3-70b-instruct:free",
    "Mistral-Nemo (free)": "mistralai/mistral-nemo:free",
    "Gemini-Flash": "google/gemini-2.0-flash-001",
    "OpenAI-GPT-4o": "openai/gpt-4o-mini",
    "Phi-3-mini": "microsoft/phi-3-mini-128k-instruct",
}
DEFAULT_MODEL = list(available_models_dict.keys())[-1]



def get_answer(prompt="", messages=list(), model_name=DEFAULT_MODEL, api_key="", temperature=None, verbose=VERBOSE):
    if api_key == "":
        api_key = get_api_key(verbose=verbose)
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers_dict = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    if len(prompt) > 0:
        messages = messages + [{"role": "user", "content": prompt}]
    data_dict = {
        "model": available_models_dict[model_name],
        "messages": messages,
    }
    if temperature is not None:
        data_dict["temperature"] = temperature
    if verbose:
        print("*" * 100)
        print("Model:", model_name)
        print("Data sent to API:", json.dumps(data_dict, indent=2))
    raw_response = requests.post(url=url, headers=headers_dict, data=json.dumps(data_dict))
    response_dict = raw_response.json()
    if "choices" in response_dict:
        return response_dict["choices"][0]["message"]["content"]
    elif "message" in response_dict:
        return response_dict["message"]
    else:
        print("Error:", response_dict)
        return "Error: No response from the model"

# ========================
# Sección: Interfaz Streamlit
# ========================

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
hide_sidebar()

st.title("🐶 NUT-AI")
model_name = st.selectbox("Modelo LLM", list(available_models_dict.keys()))
context_str = st.text_area("Contexto:", value="Eres un asistente de IA que responde como pirata en español, aunque el usuario escriba en inglés.")
question_str = st.text_area("Pregunta:", value="¿Qué animal da leche y dice miau?", placeholder="Escribe tu pregunta")

c1, c2 = st.columns([10, 1])
button_clicked = c1.button("Enviar", type="primary", use_container_width=True, disabled=len(question_str) == 0)
if button_clicked:
    full_prompt = f"Contexto:\n{context_str}\n\nPregunta:\n{question_str}"
    answer = get_answer(prompt=full_prompt, model_name=model_name)
    st.caption("Respuesta:")
    st.write(answer)

if c2.button(":material/code:", use_container_width=True, type="secondary"):
    popup_code(__file__)
