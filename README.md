# 🐍 Template Python - Asociación Ops

### 🎯 Objetivo de este repositorio
Este repositorio sirve como **plantilla oficial** para todos los desarrollos basados en Python dentro de la asociación. Utiliza una arquitectura híbrida: la lógica y dependencias son gestionadas por **Python (pyproject.toml)**, mientras que el ciclo de vida de CI/CD se unifica mediante una interfaz de **Node.js (package.json)** para garantizar la compatibilidad con nuestro Pipeline Universal.

---

### 🚀 Cómo desplegar
Para comenzar un nuevo proyecto siguiendo nuestros estándares, sigue estos pasos:

1.  **Solicitud:** Solicita un nuevo repositorio basado en este *template* a través de una conversación en el canal oficial o contactando con tu **Coordinador de Proyecto**.
2.  **Asignación:** Una vez asignado, clónalo localmente:
    `git clone [https://github.com/tu-asociacion/nombre-de-tu-repo.git]`
3.  **Instalación:** 
    *   Crea y activa un entorno virtual: `python -m venv venv` y actívalo (`source venv/bin/activate` en Linux/macOS o `venv\Scripts\activate` en Windows).
    *   Instala las dependencias de Python: `pip install .[dev,test]`
    *   Instala la interfaz de comandos: `npm install`
4.  **Desarrollo:** Crea tu rama (`git checkout -b feature/funcionalidad`) y comienza a programar. Al hacer *push* a `main`, el sistema desplegará automáticamente.

---

### ⚡ Herramientas durante el desarrollo
Aunque el código sea Python, utilizamos los comandos de `npm` para disparar las herramientas internas de forma estandarizada:

*   **`npm run lint`**: Ejecuta **flake8**. Verifica que el código siga las normas de estilo y el uso de `camelCase` (según configuración en `pyproject.toml`).
*   **`npm test`**: Ejecuta **pytest**. Verifica la lógica de tus scripts. El pipeline está configurado para no detenerse si no hay tests, pero se recomienda su uso.
*   **`npm run build`**: Ejecuta `python -m build`. Genera los paquetes de distribución y prepara la carpeta `dist/` para el despliegue.

---

### 📏 Estándares de Uso
*   **Gestión de Dependencias**: Todas las librerías deben declararse en el archivo `pyproject.toml`.
*   **Estilo de Código**: Es obligatorio el uso de **camelCase** para funciones y variables públicas para mantener la consistencia con el ecosistema de la Asociación.
*   **Entorno**: Se requiere **Python 3.10+** y **Node.js v24+** (solo para el motor de despliegue).

---

### 🧪 Tests Unitarios
Los archivos de prueba deben ubicarse en la carpeta `tests/` o junto al código fuente con el prefijo `test_`. 

```text
project/
├── src/
│   └── main.py
└── tests/
    └── test_main.py     <-- Pytest lo encuentra aquí.
```

*Si una funcionalidad no tiene tests, el pipeline continuará, pero la salud del código será responsabilidad del desarrollador.*

---

### 🛠️ Solo para DevOps
Esta sección detalla cómo este template de Python se "disfraza" de Node.js para encajar en el Pipeline Universal de la asociación.

*   **`pyproject.toml`**: Es la fuente de verdad del proyecto Python. Define el sistema de construcción (`setuptools`), las dependencias del proyecto y las herramientas de desarrollo (`pytest`, `flake8`, `black`).
*   **`package.json`**: Actúa como un **Wrapper (Capa de abstracción)**. El Workflow Reutilizable de Ops no necesita saber que el código es Python; simplemente ejecuta `npm test` y `npm run build`. Estos comandos, internamente, llaman a `pytest` y `python -m build`.
*   **Integración Netlify**: Se utiliza `netlify-cli` como dependencia de desarrollo en el `package.json` para permitir que el paso final de despliegue (`npx netlify-cli deploy`) funcione de forma idéntica a los proyectos de Node.js.
*   **Pipeline Proxy**: `.github/workflows/ci.yml` redirige la ejecución al workflow central de la organización, pasando el input `language: python`.
