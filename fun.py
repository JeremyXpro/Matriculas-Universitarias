import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

# Conexión a la base de datos SQLite
conn = sqlite3.connect('matricula.db')

# Leer los datos de la tabla 'matricula' en el DataFrame
df = pd.read_sql_query("SELECT * FROM matricula", conn)

# Selección de columnas necesarias
columnas_necesarias = [
    'instituci_n_de_educaci_n_superior_ies', 
    'municipio_dedomicilio_de_la_ies', 
    'programa_acad_mico', 
    'departamento_de_oferta_del_programa',
    'id_g_nero', 
    'a_o', 
    'matriculados_2015'
]

df_procesado = df[columnas_necesarias]

# Diccionario para eliminar acentos manualmente
acentos = {
    'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U', 
    'Ñ': 'N', 'Ü': 'U', 'á': 'a', 'é': 'e', 'í': 'i', 
    'ó': 'o', 'ú': 'u', 'ñ': 'n', 'ü': 'u'
}

def quitar_acentos(texto):
    for acento, reemplazo in acentos.items():
        texto = texto.replace(acento, reemplazo)
    return texto

# Estandarizar nombres de los municipios
df_procesado['municipio_dedomicilio_de_la_ies'] = (
    df_procesado['municipio_dedomicilio_de_la_ies']
    .str.strip()  # Eliminar espacios al inicio y final
    .str.upper()  # Convertir a mayúsculas
    .apply(quitar_acentos)  # Eliminar acentos
)

# Verificar si hay valores nulos
valores_nulos = df_procesado.isnull().sum()
print("Valores nulos por columna:")
print(valores_nulos)

# Convertir las columnas a tipo int, manejando valores no numéricos
columnas_int = ['id_g_nero', 'a_o', 'matriculados_2015']
for columna in columnas_int:
    df_procesado[columna] = pd.to_numeric(df_procesado[columna], errors='coerce', downcast='integer')

# Rellenar valores nulos en columnas 'id_g_nero', 'a_o', 'matriculados_2015' con un valor predeterminado si es necesario
df_procesado['id_g_nero'].fillna(0, inplace=True)
df_procesado['a_o'].fillna(df_procesado['a_o'].mode()[0], inplace=True)  # Rellenar con el valor más común
df_procesado['matriculados_2015'].fillna(0, inplace=True)


df_procesado['id_g_nero'] = df_procesado['id_g_nero'].astype('category')


# Eliminar filas donde el valor de 'id_g_nero' sea 0.0
df_procesado = df_procesado[df_procesado['id_g_nero'] != 0.0]

# Convertir los valores de 'id_g_nero' a categorías más legibles
df_procesado['id_g_nero'] = df_procesado['id_g_nero'].map({1.0: 'Femenino', 2.0: 'Masculino'})

# Comprobar los valores únicos después de la eliminación
print(df_procesado['id_g_nero'].unique())

# Ahora, generar la gráfica
plt.figure(figsize=(8, 6))
sns.countplot(data=df_procesado, x='id_g_nero', palette='Set2')
plt.title('Distribución de Matriculados por Género', fontsize=14)
plt.xlabel('Género', fontsize=12)
plt.ylabel('Cantidad de Matriculados', fontsize=12)
plt.xticks([0, 1], ['Masculino', 'Femenino'])
plt.show()

# Gráfico 2: Evolución de los matriculados a lo largo de los años (Gráfico de líneas)
plt.figure(figsize=(10, 6))
matriculados_por_año = df_procesado.groupby('a_o')['matriculados_2015'].sum()
plt.plot(matriculados_por_año.index, matriculados_por_año.values, marker='o', color='b', linestyle='-', markersize=8)
plt.title('Evolución de los Matriculados a lo Largo de los Años', fontsize=14)
plt.xlabel('Año', fontsize=12)
plt.ylabel('Cantidad de Matriculados', fontsize=12)
plt.grid(True)
plt.xticks(matriculados_por_año.index, rotation=45)
plt.show()

# Gráfico 3: Distribución de matrícula por los 10 programas académicos con mayor matrícula (Gráfico de torta)
plt.figure(figsize=(8, 8))
top_10_programas = df_procesado['programa_acad_mico'].value_counts().head(10)
plt.pie(top_10_programas, labels=top_10_programas.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('Set3', len(top_10_programas)))
plt.title('Distribución de Matrícula por Programa Académico (Top 10)', fontsize=14)
plt.axis('equal')  # Para que el gráfico sea circular
plt.show()

# Guardar el DataFrame procesado como un nuevo archivo CSV
df_procesado.to_csv('matricula_procesada.csv', index=False, encoding='utf-8')

