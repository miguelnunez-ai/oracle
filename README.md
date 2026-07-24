# 🛒 Mercado Central 24h - Asistente IA

Un asistente virtual impulsado por Inteligencia Artificial (basado en arquitectura **RAG** - *Retrieval-Augmented Generation*) diseñado para responder consultas sobre políticas de la empresa, inventario, recursos humanos, y manuales de seguridad para el supermercado "Mercado Central 24h".

El sistema procesa documentos corporativos en formatos **PDF** y **Excel**, convirtiéndolos en una base de conocimientos consultable mediante modelos de lenguaje de última generación (LLMs).

---

## ✨ Características Principales

* **Soporte Multi-Proveedor (LLMs):** Compatible con **Google Gemini**, **Groq** y **OpenRouter**, permitiendo elegir entre modelos como Gemini 2.0 Flash, Llama 3.3, Mixtral y DeepSeek.
* **Procesamiento de Documentos:** Ingesta automática de manuales en PDF y hojas de inventario/empleados en Excel (`.xlsx`, `.xls`).
* **Base de Conocimientos Dinámica:** Lee automáticamente los archivos en la carpeta `/knowledge` al iniciar y permite subir archivos adicionales directamente desde la interfaz.
* **Interfaz Gráfica Intuitiva:** Interfaz de chat moderna y amigable construida con **Streamlit**.
* **Vector Store Local:** Utiliza **ChromaDB** y los embeddings de HuggingFace (`all-MiniLM-L6-v2`) para búsquedas rápidas y precisas.

---

## 📂 Estructura del Proyecto

```text
├── app.py                  # Código principal de la aplicación Streamlit
├── requirements.txt        # Dependencias del proyecto
├── .env                    # (Opcional) Archivo para almacenar las API Keys de forma segura
├── knowledge/              # Directorio para la base de conocimientos fija
│   ├── politicas_empresa_1.pdf
│   ├── manual_seguridad.pdf
│   ├── manual_operaciones.pdf
│   ├── gestion_empleados.xlsx
│   └── inventario_actual.xlsx
└── README.md               # Este archivo
```

---

## 🚀 Instalación y Ejecución

### Opción 1: Ejecución en Google Colab (Recomendado)

Si estás corriendo este proyecto en un cuaderno de Google Colab, la aplicación utiliza `pyngrok` para exponer el servidor local a la web.

1. **Instalar dependencias:**
   Ejecuta la siguiente celda en tu cuaderno:
   ```bash
   !pip install -r requirements.txt
   ```

2. **Configurar archivos:**
   Asegúrate de que la celda que crea la carpeta `knowledge/` y mueve tus PDFs/Excels a ella se haya ejecutado correctamente.

3. **Autenticar Ngrok y Ejecutar:**
   ```python
   from pyngrok import ngrok
   # Reemplaza 'TU_TOKEN_AQUI' por tu token real de ngrok
   ngrok.set_auth_token("TU_TOKEN_AQUI") 
   
   !streamlit run app.py &>/dev/null&
   
   public_url = ngrok.connect(addr="8501", proto="http")
   print(f"La aplicación está corriendo en: {public_url}")
   ```
4. Haz clic en el enlace generado por ngrok para abrir la interfaz del asistente.

### Opción 2: Ejecución Local

Si deseas correr este proyecto en tu propia computadora:

1. Clona el repositorio y navega a la carpeta del proyecto.
2. Crea un entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Crea la carpeta `knowledge` y coloca tus PDFs y archivos Excel dentro de ella.
5. Inicia la aplicación:
   ```bash
   streamlit run app.py
   ```

---

## ⚙️ Uso y Configuración de API Keys

<h3 style="color:red;">⚠️ ATENCIÓN: debes colocar tus claves API, porque fueron retiradas por motivo de seguridad.</h3>

Una vez que abras la interfaz del asistente en tu navegador:

1. Ve a la **barra lateral (Sidebar)** de la izquierda.
2. Selecciona tu **Proveedor de IA** favorito (Groq, Google Gemini u OpenRouter).
3. Pega tu **API Key** correspondiente en el campo de contraseña.
   * *Opcional:* Puedes crear un archivo `.env` en la raíz del proyecto con las variables `GOOGLE_API_KEY`, `GROQ_API_KEY` o `OPENROUTER_API_KEY` para que se carguen automáticamente.
4. Si necesitas agregar documentos extra en el momento, usa la zona de subida de archivos y haz clic en **"Reconstruir base de conocimiento"**.
5. ¡Escribe tu pregunta en el chat y el asistente te responderá basándose en los documentos!

---

## 📝 Preguntas Frecuentes Soportadas

El sistema está preparado para responder consultas como:
* *¿Cuáles son las políticas de devolución de Mercado Central 24h?*
* *¿Cómo puedo solicitar un cambio de turno?*
* *¿Cuál es el procedimiento para presentar una queja?*
* *¿Qué documentos necesito para una baja médica?*

---
*Desarrollado para la optimización de los procesos internos de Mercado Central 24h.*
