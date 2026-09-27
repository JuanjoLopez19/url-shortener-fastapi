<div align="center">
  <img src="src/static/logo.webp" alt="" width="72" height="72" />
  <h1>URL Shortener</h1>
  <p><strong>Enlaces cortos. Compartir sin fricción.</strong></p>
  <p>Convierte una URL larga en un enlace breve, listo para copiar y compartir.</p>
</div>

## Acorta, copia y comparte

URL Shortener hace que compartir direcciones largas sea más sencillo. Pega la URL de destino, crea un enlace compacto y cópialo con un clic. Cuando alguien lo abre, llega directamente a la página original.

La interfaz está diseñada para funcionar bien en móvil y escritorio, e incluye temas claro y oscuro con preferencia guardada en el navegador.

## Una experiencia directa

1. **Pega** una dirección web completa que empiece por `http://` o `https://`.
2. **Acórtala** y obtén un enlace listo para compartir.
3. **Cópialo** con un clic. Al abrirlo, se redirige a la URL original.

Los enlaces se guardan en MongoDB. En cada redirección, el servicio actualiza el contador de accesos y la fecha del último acceso.

## Pruébalo en local

Necesitas Python 3.13 o posterior, [UV](https://docs.astral.sh/uv/) y una base de datos MongoDB accesible desde tu entorno.

1. Clona el repositorio e instala las dependencias:

   ```bash
   git clone https://github.com/JuanjoLopez19/url-shortener-fastapi.git
   cd url-shortener-fastapi
   uv sync
   ```

2. Crea `src/.env` con las credenciales de MongoDB:

   ```dotenv
   DATABASE_USER=tu_usuario
   DATABASE_PASSWORD=tu_contraseña
   DATABASE_NAME=url_shortener
   DATABASE_HOST=tu_cluster.mongodb.net
   DATABASE_PORT=27017
   DEVELOPMENT=True
   ```

3. Inicia la aplicación:

   ```bash
   uv run python main.py
   ```

   Abre [http://localhost:8000](http://localhost:8000).

## Despliegue

El repositorio incluye configuración para Vercel. Importa el proyecto y define estas variables de entorno en la configuración del despliegue:

| Variable            | Descripción                                               |
| ------------------- | --------------------------------------------------------- |
| `DATABASE_USER`     | Usuario de MongoDB                                        |
| `DATABASE_PASSWORD` | Contraseña de MongoDB                                     |
| `DATABASE_NAME`     | Nombre de la base de datos                                |
| `DATABASE_HOST`     | Host del clúster MongoDB                                  |
| `DATABASE_PORT`     | Valor requerido por la configuración; normalmente `27017` |

Comprueba también que el clúster permita conexiones desde el entorno de despliegue. La aplicación detecta el entorno serverless de Vercel mediante `VERCEL=1`.

## Rutas disponibles

| Ruta                   | Comportamiento                                                                  |
| ---------------------- | ------------------------------------------------------------------------------- |
| `GET /`                | Muestra el formulario para acortar una URL.                                     |
| `POST /api/v1/shorten` | Recibe el campo de formulario `url` y muestra la página con el enlace generado. |
| `GET /{token}`         | Redirige al destino asociado al token y actualiza sus datos de acceso.          |

## Tecnologías

- **Aplicación:** FastAPI y Python.
- **Persistencia:** MongoDB con Beanie.
- **Interfaz:** plantillas Jinja2, HTML, CSS y JavaScript.
- **Despliegue:** Vercel.

## Contacto

Creado por [Juanjo López](https://portfolio.jjlopez.dev). Para consultas: [contact@jjlopez.dev](mailto:contact@jjlopez.dev).
