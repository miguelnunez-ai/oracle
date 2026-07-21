# 🛒 Asistente IA RAG - Mercado Central 24h

> ⚠️ **Nota de Uso:** Para utilizar este asistente, **debes colocar tu propia API Key** en la barra lateral de la aplicación. Cuentas con **tres opciones distintas de proveedores**: **Google Gemini**, **Groq** y **OpenRouter**. Además, **debes cargar los archivos (PDF o Excel) que deseas consultar** para que el sistema construya la base de conocimiento en tiempo real.

Sistema de asistencia virtual basado en **RAG (Retrieval-Augmented Generation)** diseñado para la gestión de consultas sobre inventario, recursos humanos, políticas y seguridad del supermercado **Mercado Central 24h**.

## 🚀 Características Principales
- **Soporte Multi-Proveedor de LLM:** Integración dinámica para **Google Gemini**, **Groq** y **OpenRouter** con selección de modelos e ingreso de API Keys desde la interfaz.
- **Procesamiento Multiformato:** Lectura y extracción semántica de documentos en formato PDF y hojas de cálculo Excel (`.xlsx`, `.xls`).
- **Embeddings Locales:** Uso del modelo `all-MiniLM-L6-v2` mediante Sentence-Transformers para realizar búsquedas vectoriales rápidas y sin consumir cuotas de API.
- **Interfaz Web Interactiva:** Desarrollada en **Streamlit** con tema oscuro optimizado y despliegue público rápido vía **ngrok**.

## 🛠️ Tecnologías Utilizadas
- **Python 3.10+**
- **LangChain** (LCEL)
- **Streamlit**
- **ChromaDB**
- **Pandas & PyPDF**

## 🔧 Instalación y Ejecución
1. Clona el repositorio:
   ```bash
   git clone [https://github.com/TU_USUARIO/mercado-central-asistente.git](https://github.com/TU_USUARIO/mercado-central-asistente.git)
   cd mercado-central-asistente
