# Chatbot FAQ AHC para Voluntarios

Asistente de preguntas frecuentes para voluntarios de la **Asociación Huella
de Carbono (AHC)**.

Stack: **Google Gemini** + **Streamlit** + SDK oficial `google-genai`.

## Instalación local

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
streamlit run app.py
```

Configura la credencial exclusivamente en `.streamlit/secrets.toml`:

```toml
GEMINI_API_KEY = "tu-clave"
```

Este archivo está excluido mediante `.gitignore` y nunca debe subirse.

## Despliegue

El repositorio conserva el workflow reutilizable de AHC Ops. Los cambios en
`main` activan el pipeline de la organización. En Streamlit Community Cloud,
selecciona `app.py` y configura `GEMINI_API_KEY` en Secrets.

## Mantenimiento del conocimiento

La base del asistente vive en `system_prompt.md`. Puede ampliarse con:

- Manual de voluntarios
- Guía del Campus
- Procedimientos internos
- Preguntas frecuentes ya respondidas

Los modelos Gemini Flash soportan hasta **1 millón de tokens** de contexto, suficiente para documentos enteros.

Tras editar, recarga la página del navegador. No se toca código.

### Cambiar el modelo de IA

En `config.py` la constante por defecto:

```python
DEFAULT_GEMINI_MODEL = "gemini-3.1-flash-lite"
```

También puede sobrescribirse sin cambiar código desde Streamlit Secrets:

```toml
GEMINI_MODEL = "gemini-3.1-flash-lite"
```

Antes de cambiarlo, comprueba el identificador en la
[documentación oficial de modelos](https://ai.google.dev/gemini-api/docs/models).

### Si la API deja de funcionar

La app maneja los errores comunes en pantalla:

- **`429 Too Many Requests`** → espera y reintento sin prometer un plazo fijo.
- **`401/403`** → aviso seguro para revisar la configuración.
- **`404`** → aviso de modelo no disponible.
- **`5xx`** → indisponibilidad temporal del proveedor.

Los detalles técnicos quedan en el registro del servidor y nunca se muestran al
voluntario.

---

## Integración con AHC Ops

- `pyproject.toml` mantiene metadatos, dependencias y herramientas Python.
- `package.json` adapta `lint`, `test` y `build` al pipeline universal.
- `.github/workflows/main.yml` invoca el workflow central de la organización.
- `.github/workflows/quality.yml` ejecuta además Ruff, Pytest y cobertura.

## Estructura

```
.
├── app.py                          punto de entrada e interfaz Streamlit
├── chat_logic.py                   validación y errores seguros
├── config.py                       rutas y carga de recursos locales
├── gemini_service.py               integración aislada con Gemini
├── ui.py                            componentes visuales Streamlit
├── system_prompt.md                base de conocimiento del bot (editable sin código)
├── casos_de_prueba.md              batería de QA según §7.2 de la guía V3
├── requirements.txt                dependencias Python
├── requirements-dev.txt            herramientas de calidad y pruebas
├── pyproject.toml                  configuración de Ruff y Pytest
├── tests/                           pruebas unitarias e integración UI
├── .github/workflows/quality.yml    control automático en GitHub
├── README.md                       este archivo
├── .gitignore                      excluye secrets, venv y artefactos
├── .streamlit/
│   ├── config.toml                 paleta de colores AHC para Streamlit
│   └── secrets.toml.example        plantilla para la API key
└── assets/
    ├── logo_ahc_oficial.jpg        logotipo oficial usado en cabecera
    ├── logo_ahc.svg                recurso vectorial auxiliar
    ├── favicon.svg                 favicon vectorial
    ├── favicon-32.png              favicon 32×32
    ├── favicon-192.png             favicon 192×192 (usado por Streamlit)
    ├── favicon-512.png             favicon 512×512
    └── styles.css                  estilos visuales AHC
```

## Calidad automática

Instala las herramientas de desarrollo y ejecuta los controles:

```bash
pip install -r requirements-dev.txt
ruff check .
ruff format --check .
pytest --cov --cov-report=term-missing
```

La cobertura mínima exigida es del **90 %** sobre la lógica comprobable. GitHub
Actions repite lint, formato, pruebas y cobertura en cada `push` y pull request.
Los casos de `casos_de_prueba.md` siguen siendo manuales porque evalúan la calidad
semántica de respuestas generadas por el modelo.

---

## Límites de Gemini

Los límites dependen del modelo, proyecto y nivel de uso; no deben codificarse
como cifras fijas en la interfaz. Consulta los valores activos en Google AI Studio
y la [documentación oficial](https://ai.google.dev/gemini-api/docs/rate-limits).

---

## Decisiones técnicas

- **SDK `google-genai`** (no el viejo `google-generativeai`, deprecated por Google).
- **System prompt en archivo `.md` aparte** — cualquier voluntario edita la base de conocimiento sin tocar código.
- **Logotipo oficial local** — usa el JPG proporcionado por la AHC sin depender
  de WordPress durante la ejecución.
- **Errores seguros** — la interfaz orienta sin revelar respuestas internas del SDK.
- **Entrada limitada** — cada consulta admite hasta 2.000 caracteres.
- **Conversación reiniciable** — el panel lateral permite empezar una sesión limpia.
- **Privacidad visible** — se advierte que no deben compartirse contraseñas ni
  datos sensibles y se redirige a Secretaría.

---

## Casos de prueba

La batería de validación está en `casos_de_prueba.md`. Cubre los 3 casos del documento V3 (Campus, MITECO, dato personal) más 2 extra de seguridad (compartir contraseña, intento de jailbreak).

Se recomienda ejecutar la batería tras cada cambio significativo en `system_prompt.md`.
