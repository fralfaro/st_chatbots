# 🤖 st_chatbots

Aplicación de chatbots personalizados construida con [Streamlit](https://streamlit.io) y modelos de lenguaje de código abierto mediante la API de [OpenRouter](https://openrouter.ai).

Ideal para demostraciones, actividades educativas y experimentación con prompts creativos.



## 🚀 Características

- Chat interactivo configurable con distintos modelos LLM (Gemini, GPT-4o, Llama, etc.).
- Personalización del contexto del asistente (¡puede hablar como pirata, por ejemplo! 🏴‍☠️).
- Interfaz intuitiva con diseño colapsado por defecto.
- Código desplegable para aprender cómo funciona el backend.



## 📦 Instalación

```bash
git clone https://github.com/fralfaro/st_chatbots.git
cd st_chatbots
pip install -r requirements.txt
````

### 🔐 Configuración de API Key

Agrega tu clave de API de OpenRouter en un archivo `.streamlit/secrets.toml`:

```toml
OPENROUTER_API_KEY = "tu_api_key_aqui"
DISABLE_SIDEBAR = true
```

