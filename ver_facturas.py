import pandas as pd
from sqlalchemy import create_engine

# Conectar a la base de datos SQLite
engine = create_engine("sqlite:///facturas.db")

# Leer la tabla 'facturas'
df = pd.read_sql("SELECT * FROM facturas", engine)

# Mostrar los datos
pd.set_option('display.float_format', '{:.2f}'.format)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
print(df)

# Cerrar la conexión
engine.dispose()
