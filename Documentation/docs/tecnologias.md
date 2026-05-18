# Tecnologías y Arquitectura del Sistema

El desarrollo de **KnowFlow** se ha llevado a cabo utilizando un conjunto de tecnologías modernas y consolidadas en el sector del desarrollo web, buscando siempre el equilibrio entre velocidad de desarrollo, seguridad, rendimiento y escalabilidad.

---

## 1. Arquitectura General: Cliente-Servidor Desacoplada

KnowFlow está diseñado bajo una arquitectura **desacoplada (Decoupled Architecture)**. Esto significa que el frontend (interfaz de usuario) y el backend (lógica de negocio y base de datos) funcionan de forma totalmente independiente, comunicándose únicamente a través de una **API RESTful** mediante intercambio de datos en formato JSON.

### Ventajas de este Diseño:
*   **Flexibilidad**: Facilita que en el futuro se puedan crear otros clientes (como una aplicación móvil nativa para iOS o Android) consumiendo los mismos endpoints del backend sin necesidad de reescribir la lógica de datos.
*   **Mantenimiento**: Permite realizar actualizaciones o corregir errores en la interfaz web de Vue sin alterar en absoluto el código de Python de Django, y viceversa.
*   **Velocidad**: Las páginas no se recargan por completo desde el servidor. El navegador descarga la aplicación una sola vez (Single Page Application) y a partir de ahí solo solicita datos ligeros por red, reduciendo el consumo de ancho de banda y mejorando la fluidez notablemente.

---

## 2. El Stack Tecnológico

A continuación, se detalla el propósito de cada herramienta integrada en la plataforma:

### 🎨 Frontend (La Interfaz Web)
*   **Vue 3 (Composition API)**: Framework progresivo de Javascript elegido por su excelente reactividad y sistema de componentes reutilizables.
*   **Vite**: El empaquetador de módulos más rápido y moderno de la actualidad, que reemplaza a Webpack para agilizar exponencialmente el tiempo de compilación y recarga en caliente durante el desarrollo.
*   **TypeScript**: Superconjunto de JavaScript que añade tipado estático al código, previniendo errores de programación en tiempo de compilación y facilitando la depuración.
*   **Tailwind CSS**: Framework CSS basado en clases de utilidad que permite un diseño visualmente atractivo, responsivo y adaptado a dispositivos móviles sin hojas de estilo masivas.
*   **Pinia**: Gestor de estado global (store) para almacenar de forma reactiva y centralizada los datos de sesión del usuario, el tema visual activo (oscuro/claro) y las restricciones de planes.
*   **Axios**: Cliente HTTP para realizar las peticiones a la API REST de Django con soporte para cookies y control de tokens.

### ⚙️ Backend (La API y Lógica de Datos)
*   **Python 3.14**: El lenguaje de programación base, conocido por su legibilidad, potencia y enorme ecosistema.
*   **Django 6.0**: Framework web robusto bajo el principio *"batteries-included"*, proporcionando un panel de administración incorporado, sistema de migraciones automatizado y protección nativa contra vulnerabilidades de seguridad comunes (inyecciones SQL, XSS, CSRF).
*   **Django REST Framework (DRF)**: Extensión de Django que facilita la serialización de modelos de datos y la creación rápida de APIs REST seguras.
*   **Redis & django-rq**: Base de datos en memoria utilizada como broker para gestionar colas de tareas asíncronas en segundo plano, ideal para operaciones pesadas como el envío de emails o el procesamiento de datos.

### 💾 Almacenamiento y Servidores
*   **PostgreSQL**: Base de datos relacional robusta elegida para el entorno de producción por su estabilidad y excelente rendimiento.
*   **SQLite**: Base de datos ligera sin configuración, ideal para el desarrollo local ágil.
*   **Nginx**: Servidor web de alto rendimiento que actúa como Proxy Inverso en producción, enrutando el tráfico de forma segura al frontend (estáticos) o backend (API).

---

## 3. Herramientas de Desarrollo y DevOps

*   **Docker & Docker Compose**: Permite empaquetar toda la aplicación (frontend, backend, Redis, Nginx, base de datos) en contenedores estandarizados, garantizando que el sistema funcione exactamente igual en el ordenador de desarrollo que en el servidor de producción.
*   **Git**: Sistema de control de versiones distribuido para coordinar el avance del proyecto de forma segura.
*   **npm**: Gestor de paquetes de Node.js para controlar las dependencias del frontend.
*   **Entornos Virtuales (venv)**: Para aislar las librerías de Python en el backend.
