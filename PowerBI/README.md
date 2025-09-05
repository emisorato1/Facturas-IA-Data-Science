# Conexión de la base de datos SQLite con Power BI

Sigue estos pasos para conectar tu archivo `facturas.db` a Power BI y visualizar tus datos:

---

## 1. Instalar el controlador ODBC para SQLite

- Descarga el controlador desde: [SQLite ODBC Driver](https://www.ch-werner.de/sqliteodbc/)
- Elige el instalador adecuado para tu sistema (32 o 64 bits) y ejecútalo.

---

## 2. Abrir el Administrador de fuentes de datos ODBC

- Presiona `Windows + R`, escribe `odbcad32` y presiona Enter.
- Si tu Power BI es de 64 bits, usa el administrador de 64 bits; si es de 32 bits, usa el de 32 bits.

---

## 3. Agregar una nueva fuente de datos

- Ve a la pestaña **DSN de usuario** o **DSN de sistema**.
- Haz clic en **Agregar**.
- Selecciona **SQLite3 ODBC Driver** y haz clic en **Finalizar**.

---

## 4. Configurar la fuente de datos

- En **Data Source Name** pon un nombre, por ejemplo: `FacturasSQLite`.
- En **Database Name** haz clic en **Browse** y selecciona tu archivo `facturas.db`.
- Haz clic en **OK** para guardar.

---

## 5. Conectar desde Power BI

- Ve a **Obtener datos** → **ODBC**.
- Selecciona la fuente de datos que creaste (por ejemplo, `FacturasSQLite`).
- Conéctate y selecciona la tabla `facturas`.

---

¡Listo! Ahora puedes crear tus visualizaciones y dashboards en Power BI usando los datos de tus facturas.