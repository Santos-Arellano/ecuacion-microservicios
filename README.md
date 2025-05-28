# Ecuacion Microservicios

Este proyecto implementa una aplicación de microservicios para resolver ecuaciones matemáticas simples, desplegada en la nube pública utilizando **Railway**. La aplicación consta de cuatro microservicios (`suma`, `resta`, `ecuacion`, `almacena`) desarrollados en Python con FastAPI, y una base de datos MySQL (`resultados_db`) para almacenar resultados. Este repositorio forma parte del **Caso #20: Despliegue de Aplicaciones en la Nube Pública** del Instituto Tecnológico y de Estudios Superiores de Monterrey, Campus Guadalajara.

## Descripción
- **suma**: Realiza la suma de dos números (`a + b`).
- **resta**: Realiza la resta de dos números (`a - b`).
- **ecuacion**: Combina los resultados de `suma` y `resta` para resolver una ecuación (`(a + b) + (c - d)`).
- **almacena**: Llama al microservicio `ecuacion` y almacena los parámetros (`a`, `b`, `c`, `d`) y el resultado en la base de datos MySQL.
- **resultados_db**: Base de datos MySQL que persiste los resultados.

## Estructura del Proyecto
```
ecuacion-microservicios/
├── suma/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
├── resta/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
├── ecuacion/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
├── almacena/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
└── README.md
```

## Prerrequisitos
- **Docker Desktop** instalado en macOS.
- Cuenta en **Docker Hub** (usuario: `santosaro`).
- Cuenta en **Railway** ([railway.app](https://railway.app/)).
- **Postman** para probar las APIs.
- Acceso a internet.

## Instalación y Configuración

### 1. Clonar el Repositorio
```bash
git clone <URL-del-repositorio>
cd ecuacion-microservicios
```

### 2. Verificar Archivos `requirements.txt`
Asegúrate de que cada microservicio tenga un archivo `requirements.txt` con las dependencias necesarias. Ejemplo:

- **suma** y **resta**:
  ```
  fastapi
  uvicorn
  pydantic
  ```
- **ecuacion**:
  ```
  fastapi
  uvicorn
  pydantic
  httpx==0.24.1
  ```
- **almacena**:
  ```
  fastapi
  uvicorn
  pydantic
  httpx==0.24.1
  mysql-connector-python
  ```

**Nota**: La inclusión de `httpx==0.24.1` en `ecuacion` y `almacena` resuelve el error `ModuleNotFoundError: No module named 'httpx'`.

### 3. Verificar Dockerfiles
Cada microservicio debe tener un `Dockerfile` en su carpeta con el siguiente contenido:
```Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 4. Autenticarse en Docker Hub
```bash
docker login
```
Ingresa tu usuario (`santosaro`) y contraseña.

### 5. Construir y Subir Imágenes Docker
Construye y sube las imágenes a Docker Hub con la versión `1.0.3` para evitar problemas de caché:
```bash
# Para suma
docker build --platform linux/amd64 -t santosaro/suma:1.0.3 ./suma
docker push santosaro/suma:1.0.3
docker tag santosaro/suma:1.0.3 santosaro/suma:latest
docker push santosaro/suma:latest

# Para resta
docker build --platform linux/amd64 -t santosaro/resta:1.0.3 ./resta
docker push santosaro/resta:1.0.3
docker tag santosaro/resta:1.0.3 santosaro/resta:latest
docker push santosaro/resta:latest

# Para ecuacion
docker build --platform linux/amd64 -t santosaro/ecuacion:1.0.3 ./ecuacion
docker push santosaro/ecuacion:1.0.3
docker tag santosaro/ecuacion:1.0.3 santosaro/ecuacion:latest
docker push santosaro/ecuacion:latest

# Para almacena
docker build --platform linux/amd64 -t santosaro/almacena:1.0.3 ./almacena
docker push santosaro/almacena:1.0.3
docker tag santosaro/almacena:1.0.3 santosaro/almacena:latest
docker push santosaro/almacena:latest
```

Verifica las imágenes en [hub.docker.com](https://hub.docker.com/).

### 6. Desplegar en Railway
1. **Crear un proyecto en Railway**:
   - Ve a [railway.app](https://railway.app/), inicia sesión, y haz clic en **"New Project"** > **"Empty Project"**.

2. **Añadir servicios para microservicios**:
   - Crea cuatro servicios: `suma-service`, `resta-service`, `ecuacion-service`, `almacena-service`.
   - Para cada servicio:
     - En **"Settings"** > **"Source"**, selecciona **"Docker Image"** y configura:
       - `santosaro/suma:1.0.3` para `suma-service`
       - `santosaro/resta:1.0.3` para `resta-service`
       - `santosaro/ecuacion:1.0.3` para `ecuacion-service`
       - `santosaro/almacena:1.0.3` para `almacena-service`
     - En **"Networking"** > **"Port"**, establece `8000`.
     - En **"Networking"**, genera una URL pública (por ejemplo, `https://suma-service.up.railway.app`).

3. **Añadir base de datos MySQL**:
   - Haz clic en **"New"** > **"Database"** > **"MySQL"**.
   - Nombra el servicio `resultados_db`.
   - En **"Variables"**, añade:
     ```
     MYSQL_ROOT_PASSWORD=rootpassword123
     MYSQL_USER=myuser
     MYSQL_PASSWORD=mypassword123
     MYSQL_DATABASE=resultados_db
     ```
   - Copia el valor de `DATABASE_URL`.

4. **Configurar variables de entorno**:
   - Para `ecuacion-service`:
     ```
     SUMA_URL=https://suma-service.up.railway.app/sumar
     RESTA_URL=https://resta-service.up.railway.app/restar
     ```
   - Para `almacena-service`:
     ```
     DATABASE_URL=<pega DATABASE_URL>
     ECUACION_URL=https://ecuacion-service.up.railway.app/ecuacion
     MYSQLHOST=<host de DATABASE_URL>
     MYSQLPORT=<port de DATABASE_URL>
     MYSQLUSER=myuser
     MYSQLPASSWORD=mypassword123
     MYSQLDATABASE=resultados_db
     ```

5. **Inicializar la base de datos**:
   - En `resultados_db`, ve a **"Connect"** y ejecuta:
     ```sql
     CREATE DATABASE IF NOT EXISTS resultados_db;
     USE resultados_db;
     CREATE TABLE IF NOT EXISTS resultados (
         id INT AUTO_INCREMENT PRIMARY KEY,
         a FLOAT NOT NULL,
         b FLOAT NOT NULL,
         c FLOAT NOT NULL,
         d FLOAT NOT NULL,
         resultado FLOAT NOT NULL,
         fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
     );
     ```

6. **Desplegar servicios**:
   - Para cada servicio, ve a **"Deploy"** y haz clic en **"Deploy"**.
   - Revisa los logs para confirmar que no hay errores.

## Probar la Aplicación
1. **Usar Postman**:
   - Crea peticiones **POST** con cuerpo **raw** > **JSON**:
     - `suma`: `https://suma-service.up.railway.app/sumar`
       ```json
       {
           "a": 15,
           "b": 17
       }
       ```
       Resultado: `32`
     - `resta`: `https://resta-service.up.railway.app/restar`
       ```json
       {
           "a": 10,
           "b": 3
       }
       ```
       Resultado: `7`
     - `ecuacion`: `https://ecuacion-service.up.railway.app/ecuacion`
       ```json
       {
           "a": 15,
           "b": 5,
           "c": 10,
           "d": 3
       }
       ```
       Resultado: `{"a": 15, "b": 5, "c": 10, "d": 3, "result": 27}`
     - `almacena`: `https://almacena-service.up.railway.app/almacena`
       ```json
       {
           "a": 1,
           "b": 2,
           "c": 3,
           "d": 4
       }
       ```

2. **Verificar datos en MySQL**:
   - En `resultados_db` > **"Connect"**, ejecuta:
     ```sql
     USE resultados_db;
     SELECT * FROM resultados;
     ```

## Limpieza
1. **Eliminar proyecto en Railway**:
   - En el **Dashboard**, selecciona el proyecto.
   - Ve a **"Settings"** > **"Danger Zone"** > **"Remove Project"**.

2. **Eliminar imágenes en Docker Hub** (opcional):
   - Ve a [hub.docker.com](https://hub.docker.com/) y elimina `santosaro/suma:1.0.3`, etc.

## Resolución de Errores
- **ModuleNotFoundError: No module named 'httpx'**:
  - **Causa**: Falta `httpx` en `requirements.txt` para `ecuacion` y `almacena`.
  - **Solución**: Se añadió `httpx==0.24.1` y se reconstruyeron las imágenes.
- **Connection refused**:
  - Verifica las URLs en las variables de entorno (`SUMA_URL`, `RESTA_URL`, `ECUACION_URL`).
- **Database error**:
  - Confirma que `DATABASE_URL` y las variables MySQL sean correctas.

## Contribuir
Para contribuir, crea un *pull request* con tus cambios. Asegúrate de seguir las convenciones de código y documentar cualquier modificación.

## Licencia
Este proyecto es para fines educativos y no tiene una licencia específica.