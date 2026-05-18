# Manual de Usuario y Guía Técnica de KnowFlow

¡Bienvenido a **KnowFlow**! Este documento combina el manual de usuario paso a paso y los detalles técnicos de la plataforma, diseñada para optimizar tu flujo de estudio, gestionar tus tareas, entender cómo funciona por dentro el sistema y mejorar tu retención de conocimiento.

---

## Índice

1. [Manual de Usuario](#manual-de-usuario)
    - [1. Introducción](#1-introducción)
    - [2. Tu Perfil y Dashboard](#2-tu-perfil-y-dashboard)
    - [3. Librerías (Libraries)](#3-librerías-libraries)
    - [4. Herramientas de Estudio (Contenidos)](#4-herramientas-de-estudio-contenidos)
    - [5. TimerFlow (Método Pomodoro)](#5-timerflow-método-pomodoro)
    - [6. Soporte y Tareas en Segundo Plano](#6-soporte-y-tareas-en-segundo-plano)
2. [Especificaciones y Funcionamiento del Sistema](#especificaciones-y-funcionamiento-del-sistema)
    - [7. Arquitectura del Sistema](#7-arquitectura-del-sistema)
    - [8. Módulos y Estructura de Apps Django](#8-módulos-y-estructura-de-apps-django)
    - [9. Funcionamiento y Flujos de Comunicación](#9-funcionamiento-y-flujos-de-comunicación)
    - [10. Tecnologías Utilizadas](#10-tecnologías-utilizadas)
    - [11. Cómo Ejecutar la Aplicación en Desarrollo](#11-cómo-ejecutar-la-aplicación-en-desarrollo)
    - [12. Estructura de Directorios y Archivos Clave](#12-estructura-de-directorios-y-archivos-clave)

---

# Manual de Usuario

## 1. Introducción

**KnowFlow** es un ecosistema integral para estudiantes y profesionales que unifica la toma de apuntes, la organización de tareas y el repaso activo (flashcards y quizzes) junto a un sistema de gestión de tiempo (Pomodoro). 

La filosofía principal de KnowFlow es que todo tu material se organiza dentro de **Librerías**, y cada pieza de conocimiento o acción (ya sea un apunte, un quiz o una tarea) se considera un **Contenido** de esa librería.

---

## 2. Tu Perfil y Dashboard

Al iniciar sesión, accederás a tu cuenta de usuario donde se registrará tu progreso:

*   **Rachas (Streaks):** KnowFlow cuenta los días consecutivos que te mantienes activo estudiando. ¡Mantén viva tu racha para mejorar tu constancia!
*   **Avatar y Datos:** Puedes personalizar tu imagen de perfil (avatar) y actualizar tus datos.
*   **Planes de Suscripción:** Dependiendo de tu cuenta, podrás ver tu plan actual y los límites correspondientes (límites de creación de carpetas o recursos para cuentas gratuitas).

---

## 3. Librerías (Libraries)

Las **Librerías** funcionan como tus carpetas principales o asignaturas. 

*   **Crear una Librería:** Asígnale un nombre descriptivo (ej. "Biología Celular" o "Proyecto Final") y una descripción.
*   Dentro de cada librería, podrás crear diferentes tipos de contenidos que comparten ese mismo espacio temático. 
*   Todos los elementos dentro de una librería se organizan de forma unificada.

---

## 4. Herramientas de Estudio (Contenidos)

Dentro de una Librería, puedes crear diferentes elementos o **Contenidos**. Un contenido puede marcarse como **Favorito** o **Público**. Existen cuatro grandes herramientas:

### Notes (Apuntes)
El módulo de apuntes te permite documentar tu aprendizaje.
*   **Editor de texto:** Escribe la teoría o resumen de tus temas de forma organizada.
*   **Archivos adjuntos:** Puedes subir archivos (como imágenes o documentos adicionales) y adjuntarlos directamente a tus apuntes para tener recursos de consulta a mano.

### TaskFlow (Tareas)
Un gestor de tareas avanzado para que no se te escape ninguna entrega o examen.
*   **Prioridades:** Clasifica tus tareas como *Baja*, *Media* o *Alta* (Low, Medium, High).
*   **Estados:** Rastrea el progreso moviendo tus tareas entre *Pendiente*, *En Progreso* o *Completada*.
*   **Fechas y Recordatorios:** Asigna una fecha límite (`due_date`), hora límite e incluso configura **Recordatorios** para recibir alertas antes de que expiren.

### FlowCards (Tarjetas de Estudio / Flashcards)
Las FlowCards están diseñadas para la memorización y el recuerdo activo (Active Recall).
*   **Término y Definición:** Por cada tarjeta defines un concepto (Término) y la respuesta o explicación (Definición).
*   Utilízalas para memorizar vocabulario, fórmulas o fechas importantes repasándolas de forma iterativa y tapando la respuesta hasta recordar.

### Knowtionaries (Cuestionarios / Quizzes)
Si quieres ponerte a prueba, crea un Knowtionary. Es una herramienta de autoevaluación interactiva.
*   **Preguntas Multirespuesta:** Crea preguntas con múltiples opciones, seleccionando cuál de ellas es la correcta.
*   **Imágenes de apoyo:** Puedes adjuntar una imagen a cada pregunta si necesitas apoyo visual (gráficos, diagramas, mapas).
*   **Puntuación:** Configura la puntuación máxima por pregunta y evalúa tus conocimientos en tiempo real obteniendo una puntuación final al completar el cuestionario.

---

## 5. TimerFlow (Método Pomodoro)

KnowFlow integra un sistema de estudio guiado por tiempos conocido como **TimerFlow**, fuertemente inspirado en la técnica Pomodoro.

*   **Configuración Personalizada:** Por defecto, los intervalos son de 25 minutos de concentración (Work) y 5 minutos de descanso corto (Short Break). Tras 4 ciclos de concentración, se te otorga un descanso largo (Long Break) de 15 minutos. Todos estos tiempos son modificables en tu configuración de TimerFlow.
*   **Sesiones de Estudio (Study Sessions):**
    *   Cada vez que inicias un temporizador, se crea una *Sesión de Estudio* en la base de datos.
    *   **Asociación con el contenido:** ¡Puedes vincular una sesión de estudio a un contenido específico de tu librería! Así sabrás exactamente cuánto tiempo has dedicado a estudiar un apunte, hacer tareas o repasar un Knowtionary en tus estadísticas.

---

## 6. Soporte y Tareas en Segundo Plano

La aplicación procesa ciertas operaciones pesadas de manera silenciosa en segundo plano (usando colas de tareas) para que tu navegación sea rápida y fluida. Acciones como el envío de correos de bienvenida al registrarte, recordatorios de tareas y el procesamiento de imágenes se gestionan automáticamente sin bloquear tu experiencia en la web.

---

# Especificaciones y Funcionamiento del Sistema

A continuación se detallan los aspectos técnicos de la arquitectura y la ingeniería detrás de KnowFlow.

## 7. Arquitectura del Sistema

KnowFlow sigue una arquitectura **cliente-servidor** moderna desacoplada en dos partes:

### Backend (Servidor de API)
*   **Tecnología**: Django REST Framework (Python 3.14).
*   **Función**: Gestiona la base de datos relacional, la autenticación, la seguridad de las peticiones, expone los endpoints de la API REST y procesa la lógica de negocio.
*   **Base de datos**: SQLite (en desarrollo local por su ligereza) y Postgres (en producción).

### Frontend (Cliente Web SPA)
*   **Tecnología**: Vue 3 (Composition API) + TypeScript + Vite + TailwindCSS.
*   **Función**: Interfaz de usuario interactiva y fluida. Es una Single Page Application (SPA).
*   **Gestión de estado**: Pinia para las tiendas reactivas globales.
*   **Comunicación**: Peticiones HTTPS a través de Axios con tokens de autenticación.

```
[Usuario / Navegador]
       ↓ (Renderiza la SPA)
[Frontend: Vue 3]  ←───(Peticiones API REST)───→  [Backend: Django]
                                                        ↓
                                                [Base de Datos]
```

---

## 8. Módulos y Estructura de Apps Django

El backend de KnowFlow está dividido en 8 aplicaciones Django específicas que se comunican entre sí:

| Aplicación Django | Función Principal |
| :--- | :--- |
| **`accounts`** | Gestión de autenticación de sesiones (login, registro de usuarios, logout). |
| **`users`** | Perfiles de usuario, fotos de perfil, estadísticas y tokens de acceso. |
| **`library`** | El core de la base de datos que organiza las colecciones principales (Librerías). |
| **`flashcards`** | Lógica de tarjetas de memorización activa (FlowCards). |
| **`notes`** | Gestión de notas con formateo enriquecido y subida de archivos adjuntos. |
| **`knowtionaries`** | Gestión de diccionarios de términos y cuestionarios de autocomprobación (quizzes). |
| **`tasks`** | Control de prioridades, estados y vencimientos de tareas pendientes (TaskFlow). |
| **`timerflow`** | Almacena configuraciones del Pomodoro y registra las sesiones de estudio dedicadas. |

---

## 9. Funcionamiento y Flujos de Comunicación

### Flujo típico de un usuario registrado:
1.  **Inicio de sesión**: El usuario envía sus credenciales al endpoint `/api/login/` en el backend.
2.  **Autenticación**: El servidor valida los datos y genera un token único de acceso que el frontend almacena y envía en las cabeceras de cada petición subsiguiente.
3.  **Dashboard**: Vue solicita las estadísticas del usuario y las renderiza en gráficos y barras de progreso.
4.  **Uso de herramientas**: Cada creación, actualización o eliminación de recursos (Notas, Tareas, etc.) realiza llamadas HTTP síncronas (`GET`, `POST`, `PUT`, `DELETE`).
5.  **Cierre de sesión**: Al pulsar logout, el token se destruye en el servidor y el usuario es redirigido a la landing page pública en `/`.

---

## 10. Tecnologías Utilizadas

*   **Backend**: Django 6.0, Django REST Framework, SQLite, Redis (Broker de mensajería para tareas en cola con `django-rq`).
*   **Frontend**: Vue 3, Vite, TypeScript, Tailwind CSS, Pinia, Axios.
*   **Contenedores y Despliegue**: Docker, Docker Compose, Nginx.

---

## 11. Cómo Ejecutar la Aplicación en Desarrollo

### Requisitos Previos:
*   Python 3.10 o superior instalado.
*   Node.js 18 o superior instalado.

### Pasos para iniciar el entorno local:

```bash
# 1. Clonar el repositorio del proyecto
git clone <url-del-repositorio>
cd knowflow

# 2. Levantar el Backend (Django)
cd Backend
python -m venv venv
source venv/bin/activate  # En Windows usa: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# 3. Levantar el Frontend (Vue 3, en otra terminal)
cd Frontend/KnowFlow
npm install
npm run dev
```

*   **Acceso al Frontend**: `http://localhost:5173`
*   **Acceso al Backend API**: `http://localhost:8000`

---

## 12. Estructura de Directorios y Archivos Clave

```
knowflow/
├── Backend/                 # Código del servidor (Django)
│   ├── main/                # Configuración global y settings del proyecto
│   ├── accounts/            # Vistas de acceso y contraseñas
│   ├── library/             # Core del sistema de carpetas
│   └── ...                  # Apps adicionales (notes, tasks, flashcards...)
├── Frontend/KnowFlow/       # Código del cliente (Vue 3)
│   ├── src/
│   │   ├── pages/           # Páginas completas (Dashboard, Home, etc.)
│   │   ├── components/      # Botones, modales y barras de navegación
│   │   ├── stores/          # Estado de Pinia (auth, theme)
│   │   └── router/          # Enrutador de Vue Router
│   └── vite.config.ts       # Configuración de compilación de Vite
├── docker-compose.yml       # Orquestador de desarrollo/producción
└── deploy.sh                # Script de automatización de despliegue
```
