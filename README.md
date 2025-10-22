Compras Bot

## **¿Qué es comprasBot?**

comprasBot es un bot de discord  compuesto por tres funciones principales:

1. **Operación del bot de Discord**: Mantiene una conexión persistente con la API de Discord mediante el framework **`discord.py`**.
2. **Web scraping programado**: Ejecuta automatización de navegador diariamente a las 11:00 (zona horaria Europa/Madrid) para extraer datos de precios del a320 de [**fenixsim.com**](http://fenixsim.com/). El cual simula tráfico humano
3. **Notificación al usuario**: Envía la información de precios formateada directamente a un usuario de Discord configurado, mediante mensaje privado.

El bot funciona de forma autónoma tras su despliegue, sin necesidad de interacción ni comandos por parte del usuario.

Este sería el resultado del bot:

![image.png](./images/image.png)

---

## **Arquitectura del sistema**

El siguiente diagrama muestra la arquitectura completa del sistema, relacionando los componentes de alto nivel con sus implementaciones reales en el código:

![image.png](./images/image%201.png)

## **Componentes principales**

El sistema consta de dos módulos principales en Python y su infraestructura de soporte:

| **Componente** | **Archivo** | **Propósito** | **Entidades clave** |
| --- | --- | --- | --- |
| **Orquestador del bot** | **`src/main.py`** | Gestión del ciclo de vida del bot de Discord, programación de tareas y enrutamiento de mensajes | Instancia **`bot`** (de `commands.Bot`), función **`daily_task`** (con decorador `@tasks.loop`), manejador de evento **`on_ready`** |
| **Scraper web** | **`src/WebScrapping.py`** | Automatización del navegador y análisis del HTML para extraer precios | Clase **`WebScraper`**, método asíncrono **`scrape_fenixsim`** |
| **Definición del contenedor** | **`Dockerfile`** | Especificación del entorno de ejecución con Python 3.11, librerías del sistema y Chromium | Imagen base, instalación de dependencias, directiva `CMD` |
| **Orquestación del servicio** | **`docker-compose.yml`** | Gestión del ciclo de vida del contenedor e inyección de variables de entorno | Definición del servicio **`comprasbot`**, sección de entorno, política de reinicio |

## **Características clave**

### **1. Ejecución diaria programada**

El bot utiliza el decorador **`@tasks.loop`** de **`discord.ext.tasks`** para ejecutar el scraping a una hora específica:

```python
@tasks.loop(time=time(11, 00, tzinfo=ZoneInfo("Europe/Madrid")))
async def daily_task():
    # Lógica de scraping y notificación

```

La tarea se inicia automáticamente cuando el bot se conecta a Discord mediante el manejador de evento **`on_ready`** [**src/main.py#L28-L31**](https://github.com/Luisalberto2020/comprasBot/blob/aab653e9/src/main.py#L28-L31).

### **2. Automatización del navegador con medidas anti-detección**

La clase **`WebScraper`** inicia una instancia headless de Chromium con varias medidas para evitar la detección como bot:

- Simulación de *user-agent* mediante **`set_extra_http_headers`** [**src/WebScrapping.py#L30-L32**](https://github.com/Luisalberto2020/comprasBot/blob/aab653e9/src/WebScrapping.py#L30-L32)
- Inyección de JavaScript para ocultar propiedades del webdriver [**src/WebScrapping.py#L34-L40**](https://github.com/Luisalberto2020/comprasBot/blob/aab653e9/src/WebScrapping.py#L34-L40)
- Retrasos con comportamiento humanoide usando **`random.uniform`** [**src/WebScrapping.py#L44-L46**](https://github.com/Luisalberto2020/comprasBot/blob/aab653e9/src/WebScrapping.py#L44-L46)
- Argumentos de lanzamiento del navegador optimizados para entornos de servidor [**src/WebScrapping.py#L18-L24**](https://github.com/Luisalberto2020/comprasBot/blob/aab653e9/src/WebScrapping.py#L18-L24)

### **3. Manejo de contenido dinámico**

[fenixsim.com](http://fenixsim.com/) carga los datos de precios mediante JavaScript. El scraper espera a que el contenido se renderice:

```python
await page.wait_for_function(
    "document.body.innerText.includes('£')",
    timeout=30000
)

```

Esto garantiza que el precio esté visible antes de comenzar el análisis [**src/WebScrapping.py#L53-L56**](https://github.com/Luisalberto2020/comprasBot/blob/aab653e9/src/WebScrapping.py#L53-L56).

### **4. Arquitectura basada en callbacks**

El scraper acepta una función de *callback*, desacoplando la lógica de extracción de la entrega de notificaciones:

```python
await scraper.scrape_fenixsim(lambda message: asyncio.create_task(user.send(message)))

```

Este diseño permite reutilizar el scraper para distintos canales de notificación [**src/main.py#L23**](https://github.com/Luisalberto2020/comprasBot/blob/aab653e9/src/main.py#L23).

### **5. Reinicio automático ante fallos**

La configuración de Docker Compose incluye **`restart: unless-stopped`**, lo que asegura que el bot se recupere automáticamente tras caídas o fallos del contenedor [**docker-compose.yml#L6**](https://github.com/Luisalberto2020/comprasBot/blob/aab653e9/docker-compose.yml#L6).

## **Flujo de ejecución**

El siguiente diagrama muestra el flujo completo de ejecución, desde el arranque del contenedor hasta la entrega del mensaje, usando los nombres reales de las entidades del código:

![image.png](./images/image%202.png)

## **Inicio del bot**

Una vez construida la imagen, inicia el bot mediante Docker Compose. La configuración de Compose gestiona la inyección de variables de entorno y el ciclo de vida del contenedor.

### **Comando de inicio**

```bash
docker-compose up -d

```

La bandera **`-d`** ejecuta el contenedor en modo desacoplado (*background*). Omítela para ver los registros en la terminal.

**Diagrama: Flujo de inicio con Docker Compose**

![image.png](./images/image%203.png)