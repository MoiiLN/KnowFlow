## Tecnologías Utilizadas

Se han integrado las siguientes herramientas:

- **Vite**: como herramienta de construcción y servidor de desarrollo rápido.
- **Vue Router**: para la gestión de rutas y navegación dentro de la aplicación.
- **Axios**: para la comunicación con la API REST del backend.
- **Tailwind CSS**: para el diseño de la interfaz, proporcionando un enfoque basado en utilidades que permite crear diseños modernos y consistentes de forma ágil.

## Arquitectura

Knowflow sigue una arquitectura **cliente-servidor desacoplada**, donde:

- El backend actúa como proveedor de datos mediante una API REST.
- El frontend consume dicha API y se encarga de la presentación e interacción con el usuario.

Esta separación permite una mayor flexibilidad, facilitando la escalabilidad del proyecto, el mantenimiento del código y la posibilidad de integrar nuevos clientes (por ejemplo, aplicaciones móviles) en el futuro.

## Herramientas de desarrollo

Durante el desarrollo se han utilizado diversas herramientas que mejoran la productividad y el control del proyecto:

- **Git**: para el control de versiones.
- **npm**: para la gestión de dependencias del frontend.
- **Entornos virtuales (venv)**: para aislar las dependencias de Python.
- **Docker (previsto)**: para la contenerización y despliegue del sistema en entornos productivos.
