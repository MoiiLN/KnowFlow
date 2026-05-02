# Explicación de KnowFlow - Aplicación de Aprendizaje Integral

## 1. ¿Qué es KnowFlow?

**KnowFlow** es una aplicación web educativa diseñada para ayudar a los estudiantes a organizar, estudiar y gestionar su aprendizaje de forma eficiente. La plataforma integra múltiples herramientas en una sola aplicación: **bibliotecas de documentos**, **flashcards** (tarjetas de estudio), **notas**, **diccionarios de conocimiento (knowtionaries)**, **tareas**, y un **temporizador de estudio (timerflow)**.

> Imagina una herramienta todo-en-uno que combine Dropbox (para guardar libros/pdf), Quizlet (para hacer fichas de estudio), Notion (para tomar notas), y un calendario de tareas.Eso es KnowFlow.

---

## 2. Arquitectura del Sistema

KnowFlow sigue una arquitectura **cliente-servidor** moderna,分成两个 partes:

### Backend (Servidor)
- **Tecnología**: Django 4.x (Python) con Django REST Framework
- **Función**: Gestiona la base de datos, autenticación, API REST y lógica de negocio.
- **Base de datos**: PostgreSQL (en producción) o SQLite (en desarrollo)
- **Autenticación**: Sessiones de Django (cookies cifradas) + tokens API.

### Frontend (Cliente)
- **Tecnología**: Vue 3 + TypeScript + Vite + TailwindCSS
- **Función**: Interfaz de usuario interactiva. Single Page Application (SPA).
- **Gestión de estado**: Pinia (Vue store).
- **Comunicación**: Axios con credenciales (cookies) para mantener sesión.

### Diagrama simple

```
[Usuario]
   ↓ (navegador)
[Frontend: Vue 3] ←→ [API REST] ←→ [Backend: Django]
                                         ↓
                                    [PostgreSQL]
```

---

## 3. Módulos de la Aplicación

KnowFlow tiene 8 aplicaciones Django que cumplen funciones específicas:

| Aplicación | Función Principal | Ejemplo de uso |
|------------|-------------------|---------------|
| **accounts** | Autenticación (login, signup, logout) | Crear cuenta, iniciar sesión |
| **users** | Perfiles de usuario, tokens, gestión de cuenta | Editar perfil, ver estadísticas |
| **library** | Álmacenes de documentos/libros en formato markdown | Subir y organizar apuntes PDF |
| **flashcards** | Tarjetas de estudio (pregunta/respuesta) | Crear fichas de vocabulario |
| **notes** | Notas personales con soporte markdown | Escribir resúmenes de clase |
| **knowtionaries** | Diccionarios de conocimiento + cuestionarios | Crear glosario y hacer quizzes |
| **tasks** | Gestión de tareas yWorkflows | Lista de tareas del trimestre |
| **timerflow** | Temporizador de estudio (Pomodoro) | 25 min de estudio + 5 min descanso |

---

## 4. Funcionamiento General

### Flujo typicalo de un usuario:

1. **Registro/Login**: El usuario se registra (accounts/api/signup/) o inicia sesión (accounts/api/login/).
2. **Dashboard**: Tras autenticarse, ve su panel principal con estadísticas y acceso rápido a funciones.
3. **Crear contenido**: Puede crear bibliotecas, flashcards, notas, etc. desde formularios en Vue.
4. **Estudiar**: Usa flashcards, knowtionaries (quizzes), o el temporizador de estudio.
5. **Gestionar tareas**: Añade tareas y las marca como completadas.

### Comunicación Cliente-Servidor:

- Las请求 (GET/POST/PUT/DELETE) se hacen a endpoints REST como `/api/libraries/`, `/api/flowcards/`, etc.
- Django responde con JSON (por ejemplo: `{"id": 1, "title": "Mi Biblioteca", ...}`).
- Vue renderiza los datos en la interfaz.

---

## 5. Tecnologías Utilizadas

### Backend
- **Django 4.x** - Framework web Python
- **Django REST Framework** - API REST
- **PostgreSQL** - Base de datos relacional
- **SQLite** - En desarrollo local
- **Docker** - Contenedores

### Frontend
- **Vue 3** - Framework reactivo
- **TypeScript** - JavaScript tipado
- **Vite** - Build tool
- **TailwindCSS** - Estilos utility-first
- **Pinia** - State management
- **Axios** - Cliente HTTP
- **Vue Router** - Enrutamiento SPA

### Herramientas de Desarrollo
- **Docker Compose** - Orquestación de servicios
- **NGINX** - Servidor web en producción
- **Git** - Control de versiones

---

## 6. Cómo Ejecutar la Aplicación (Desarrollo)

### Requisitos previos
- Python 3.10+
- Node.js 18+
- Docker Desktop (opcional)

### Pasos

```bash
# 1. Clonar el repositorio
git clone <repo-url>
cd knowflow

# 2. Iniciar servicios con Docker Compose
docker-compose up -d

# O manualmente:

# Backend
cd Backend
python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\Activate)
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# Frontend (otra terminal)
cd Frontend/KnowFlow
npm install
npm run dev
```

### URLs de acceso:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- Admin Django: http://localhost:8000/admin

---

## 7. Características Destacadas para la Presentación

### ✅ Sistema multi-herramienta
- No necesitas 5 aplicaciones distintas. Todo está integrado.

### ✅ Aprendizaje activo
- **Flashcards**: Repasar términos.
- **Knowtionaries**: Hacer cuestionarios.
- **Timerflow**: Técnica Pomodoro para no quemarse.

### ✅ Persistencia
- Toda la información se guarda en PostgreSQL. No se pierde al cerrar.

### ✅ Interfaz moderna
- Diseño limpio con TailwindCSS, responsive (móvil/escritorio).

### ✅ Pruebas automatizadas
- El proyecto incluye tests unitarios (`Backend/tests/`) para asegurar funcionalidad.

### ✅ Docker
- Fácil despliegue: `docker-compose up` levanta todo el sistema.

---

## 8. Estructura de Archivos Clave

```
knowflow/
├── Backend/                 # Proyecto Django
│   ├── accounts/         # Autenticación
│   ├── users/           # Perfiles
│   ├── library/         # Bibliotecas
│   ├── flashcards/      # Tarjetas
│   ├── notes/          # Notas
│   ├── knowtionaries/  # Diccionarios + quizzes
│   ├── tasks/          # Tareas
│   ├── timerflow/      # Temporizador
│   └── main/          # Configuración central
├── Frontend/KnowFlow/    # Proyecto Vue 3
│   ├── src/
│   │   ├── pages/     # Vistas (Login, Dashboard, etc.)
│   │   ├── components/# Componentes reutilizables
│   │   ├── stores/   # Pinia (estado)
│   │   ├── services/  # API client
│   │   └── router/   # Rutas
│   └── ...
├── docker-compose.yml   # Orquestación
└── README.md
```

---

## 9. Conclusión

**KnowFlow** es un proyecto completo de desarrollo web real que demuestra dominio de:
- Diseño de bases de datos relacionales
- API REST con Django
- Frontend SPA con Vue 3
- Contenedores con Docker
- Integración de múltiples sistemas

Es ideal para un trabajo de final de curso o portafolio profesional.
