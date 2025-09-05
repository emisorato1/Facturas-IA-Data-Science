# Facturas-IA-Data-Science
Procesamiento automático de facturas PDF usando Inteligencia Artificial. Extrae datos estructurados (fecha, proveedor, concepto, importe) de facturas en cualquier formato, los almacena en base de datos SQLite y permite visualización con Power BI. Ideal para automatizar la gestión de gastos empresariales.

# 📊 Proyecto de Facturas con IA

## 📑 Índice

- [🎯 Contexto y necesidad de negocio](#-contexto-y-necesidad-de-negocio)
- [🚀 Solución propuesta](#-solución-propuesta)
- [🛠️ Tecnologías utilizadas](#️-tecnologías-utilizadas)
- [📋 Requisitos previos](#-requisitos-previos)
- [🚀 Instalación paso a paso](#-instalación-paso-a-paso)
- [🔄 Funcionamiento detallado del sistema](#-funcionamiento-detallado-del-sistema)
- [📊 Uso del sistema](#-uso-del-sistema)
- [📁 Estructura del proyecto](#-estructura-del-proyecto)
- [🔧 Configuración avanzada](#-configuración-avanzada)
- [🚨 Solución de problemas comunes](#-solución-de-problemas-comunes)
- [📈 Procesamiento incremental](#-procesamiento-incremental)
- [🎯 Objetivo final](#-objetivo-final)
- [📊 Próximos pasos](#-próximos-pasos)
- [💡 Consejos útiles](#-consejos-útiles)
- [🆘 ¿Necesitas ayuda?](#-¿necesitas-ayuda)

## 🎯 Contexto y necesidad de negocio

En muchas empresas, la gestión de facturas de gastos es un proceso complicado debido a la variedad de formatos que utilizan los diferentes proveedores. Extraer manualmente información clave como fecha, importe y concepto de cada factura es una tarea laboriosa, propensa a errores y consume mucho tiempo. Las empresas grandes suelen contratar personal administrativo para esta labor, mientras que en las pequeñas, este trabajo recae en los propios dueños o se descuida por falta de tiempo.

## 🚀 Solución propuesta

Este proyecto automatiza la extracción y gestión de datos clave de facturas en PDF utilizando Python e Inteligencia Artificial. La solución permite:

1. **Cargar facturas**: Procesar todas las facturas en PDF desde un directorio organizado
2. **Extracción inteligente**: Usar IA para extraer datos clave (fecha, importe, concepto, proveedor) sin importar el formato
3. **Estructuración**: Convertir la información extraída en datos estructurados
4. **Almacenamiento**: Guardar los datos en una base de datos SQLite
5. **Visualización**: Crear dashboards interactivos con Power BI

## 🛠️ Tecnologías utilizadas

- **Python 3.13**: Scripts y procesamiento de datos
- **OpenAI GPT-4o-mini**: Inteligencia Artificial para extracción de información
- **PyMuPDF**: Extracción de texto de archivos PDF
- **Pandas**: Manipulación y análisis de datos
- **SQLAlchemy**: Gestión de base de datos
- **SQLite**: Base de datos para almacenamiento
- **Power BI**: Visualización y dashboards

## 📋 Requisitos previos

### Software necesario:
- Python 3.13 o superior
- Power BI Desktop (opcional, para visualización)
- Controlador ODBC para SQLite (para conectar con Power BI)

### Cuenta de API:
- Cuenta de OpenAI con API key válida





## 🔄 Funcionamiento detallado del sistema

### Paso 1: Extracción de texto (funciones.py - extraer_texto_pdf)
```python
def extraer_texto_pdf(ruta_pdf):
    doc = fitz.open(ruta_pdf)  # Abre el PDF
    text = "\n".join([page.get_text("text") for page in doc])  # Extrae todo el texto
    return text
```
- **¿Qué hace?**: Abre cada archivo PDF y extrae todo el texto contenido
- **Tecnología**: PyMuPDF (fitz) para lectura de PDFs
- **Resultado**: Texto plano sin formato de la factura

### Paso 2: Estructuración con IA (funciones.py - estructurar_texto)
```python
def estructurar_texto(texto):
    cliente = openai.OpenAI(api_key=OPENAI_API_KEY)
    respuesta = cliente.chat.completions.create(
        model="gpt-4o-mini",
        messages=[...]
    )
    return csv_respuesta
```
- **¿Qué hace?**: Envía el texto extraído a OpenAI para que lo estructure
- **Proceso**: 
  - Usa el prompt definido en `prompt.py` que especifica exactamente qué extraer
  - La IA identifica: fecha, proveedor, concepto, importe y moneda
  - Devuelve los datos en formato CSV estructurado
- **Resultado**: CSV con columnas: fecha_factura;proveedor;concepto;importe;moneda

### Paso 3: Conversión a DataFrame (funciones.py - csv_a_dataframe)
```python
def csv_a_dataframe(csv):
    df_temp = pd.read_csv(StringIO(csv), delimiter=";", dtype=dtype_cols)
    df_temp["importe"] = pd.to_numeric(
        df_temp["importe"].str.replace(",", "."), errors="coerce"
    )
    return df_temp
```
- **¿Qué hace?**: Convierte el CSV de la IA en un DataFrame de Pandas
- **Procesamiento**: 
  - Convierte el importe a formato numérico
  - Maneja diferentes formatos de números (comas, puntos)
  - Valida los tipos de datos

### Paso 4: Procesamiento principal (main.py)
```python
# Recorre todas las carpetas de facturas
for carpeta in sorted(os.listdir("./facturas")):
    for archivo in os.listdir(ruta_carpeta):
        # Extrae texto del PDF
        texto_no_estructurado = funciones.extraer_texto_pdf(ruta_pdf)
        
        # Estructura con IA
        texto_estructurado = funciones.estructurar_texto(texto_no_estructurado)
        
        # Convierte a DataFrame
        df_factura = funciones.csv_a_dataframe(texto_estructurado)
        
        # Añade al DataFrame general
        df = pd.concat([df, df_factura], ignore_index=True)
```

**Proceso completo**:
1. **Exploración**: Recorre todas las carpetas en `./facturas/`
2. **Procesamiento individual**: Para cada PDF:
   - Extrae el texto
   - Lo envía a la IA para estructurar
   - Convierte el resultado a DataFrame
   - Lo añade al conjunto general
3. **Conversión de monedas**: Convierte dólares a pesos argentinos (×1300)
4. **Limpieza**: Elimina columnas no esenciales
5. **Almacenamiento**: Guarda todo en la base de datos SQLite

### Paso 5: Almacenamiento en base de datos
```python
engine = create_engine("sqlite:///facturas.db")
df.to_sql("facturas", engine, if_exists="append", index=False)
```
- **¿Qué hace?**: Guarda todos los datos procesados en una base de datos SQLite
- **Ventaja**: Los datos se añaden (no se reemplazan), permitiendo procesamiento incremental
- **Resultado**: Archivo `facturas.db` con tabla `facturas` estructurada

## 📊 Uso del sistema

### 1. Procesar facturas
```bash
python main.py
```
- Procesa todas las facturas en la carpeta `facturas/`
- Muestra el progreso en consola
- Guarda los resultados en `facturas.db`

### 2. Ver los datos procesados
```bash
python ver_facturas.py
```
- Conecta a la base de datos
- Muestra todos los datos en formato tabla
- Configuración optimizada para visualización

### 3. Visualizar con Power BI
1. Sigue las instrucciones en `PowerBI/README.md`
2. Conecta Power BI a la base de datos SQLite
3. Crea dashboards interactivos

## 🔧 Configuración avanzada

### Personalizar el prompt de IA
Edita `prompt.py` para modificar:
- Qué datos extraer de las facturas
- Formato de salida
- Reglas de conversión de monedas
- Criterios de validación

### Ajustar conversión de monedas
En `main.py`, línea 32:
```python
df.loc[df["moneda"] == "dolares", "importe"] *= 1300  # Cambia 1300 por tu tasa
```

### Modificar estructura de base de datos
La tabla `facturas` tiene las columnas:
- `fecha_factura` (TEXT): Fecha en formato dd/mm/aaaa
- `proveedor` (TEXT): Nombre del proveedor
- `concepto` (TEXT): Descripción del producto/servicio
- `importe` (FLOAT): Monto en pesos argentinos





# 🚀 Guía de Instalación Detallada - Proyecto de Facturas con IA

Esta guía está diseñada para usuarios que no tienen mucha experiencia con Python o desarrollo de software.

## 📋 Antes de empezar

### ¿Qué necesitas?
1. **Una computadora con Windows, Mac o Linux**
2. **Conexión a internet**
3. **Una cuenta de OpenAI** (gratuita o de pago)
4. **Archivos PDF de facturas** para procesar

### ¿Qué vas a instalar?
- Python (lenguaje de programación)
- Conda (gestor de entornos)
- Librerías de Python necesarias
- El proyecto de facturas

## 🔧 Instalación paso a paso

### Paso 1: Instalar Anaconda/Miniconda

#### Opción A: Anaconda (Recomendado para principiantes)
1. Ve a [https://www.anaconda.com/download](https://www.anaconda.com/download)
2. Descarga la versión para tu sistema operativo
3. Ejecuta el instalador
4. **IMPORTANTE**: Marca la casilla "Add Anaconda to my PATH environment variable"
5. Completa la instalación

#### Opción B: Miniconda (Más ligero)
1. Ve a [https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html)
2. Descarga la versión para tu sistema operativo
3. Ejecuta el instalador
4. Sigue las instrucciones en pantalla

### Paso 2: Verificar la instalación

Abre la terminal/consola y escribe:
```bash
conda --version
```

Si aparece un número de versión (ej: conda 23.x.x), ¡perfecto! Si no, reinicia la terminal y prueba de nuevo.

### Paso 3: Descargar el proyecto

#### Opción A: Si tienes Git instalado
```bash
git clone [URL_DEL_REPOSITORIO]
cd "Proyecto de Facturas con IA"
```

#### Opción B: Descarga manual
1. Ve al repositorio del proyecto
2. Haz clic en "Code" → "Download ZIP"
3. Extrae el archivo ZIP en una carpeta de tu elección
4. Abre la terminal en esa carpeta

### Paso 4: Crear el entorno virtual

En la terminal, navega a la carpeta del proyecto y ejecuta:

```bash
# Crear el entorno desde el archivo de configuración
conda env create -f entorno.yml

# Activar el entorno
conda activate gestor_gastos
```

**¿Qué hace esto?**
- Crea un "entorno virtual" con todas las librerías necesarias
- Es como tener una caja de herramientas separada para este proyecto
- Evita conflictos con otros programas

### Paso 5: Verificar que todo funciona

```bash
python --version
```

Debería mostrar: `Python 3.13.x`

```bash
python -c "import pandas; print('Pandas instalado correctamente')"
```

Debería mostrar: `Pandas instalado correctamente`

### Paso 6: Configurar la API de OpenAI

**Configurar el proyecto**:
   - En la carpeta del proyecto, crea un archivo llamado `.env`
   - Abre el archivo `.env` con un editor de texto
   - Escribe exactamente esto (reemplaza con tu clave):
   ```
   OPENAI_API_KEY=sk-tu_clave_real_aqui
   ```
   - Guarda el archivo

### Paso 7: Organizar tus facturas

1. **Crear la estructura de carpetas**:
   ```
   Proyecto de Facturas con IA/
   └── facturas/
       ├── factura mes 1/
       ├── factura mes 2/
       └── factura mes 3/
   ```

2. **Colocar tus PDFs**:
   - Pon tus facturas PDF en las carpetas correspondientes
   - Puedes organizarlas como quieras (por mes, por proveedor, etc.)
   - El sistema procesará todas las carpetas automáticamente

## 🚀 Primera ejecución

### 1. Procesar las facturas
```bash
# Asegúrate de estar en el entorno correcto
conda activate gestor_gastos

# Ejecutar el procesamiento
python main.py
```

**¿Qué verás?**
- Mensajes como "📄 Procesando factura: ./facturas/factura mes 1/factura1.pdf"
- El progreso de cada factura
- Al final: "Proceso de extracción y estructuración de facturas completado exitosamente"

### 2. Ver los resultados
```bash
python ver_facturas.py
```

**¿Qué verás?**
- Una tabla con todas las facturas procesadas
- Columnas: fecha_factura, proveedor, concepto, importe
- Los datos ya estructurados y listos para usar

## 🔍 Verificar que todo funciona

### Test básico
1. **Ejecuta el procesamiento**: `python main.py`
2. **Verifica que no hay errores** en la consola
3. **Revisa los resultados**: `python ver_facturas.py`
4. **Confirma que aparece el archivo**: `facturas.db`
