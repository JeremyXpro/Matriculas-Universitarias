import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar el archivo de datos procesado
df_procesado = pd.read_csv('matricula_procesada.csv')

# Título de la aplicación
st.title("Análisis de Matrícula Estadística en Educación Superior en Colombia")

# Agregar un filtro para seleccionar año
año = st.slider("Selecciona el año", min_value=int(df_procesado['a_o'].min()), max_value=int(df_procesado['a_o'].max()), step=1)
df_año = df_procesado[df_procesado['a_o'] == año]

# Gráfico 1: Distribución de Matriculados por Género
st.header("Distribución de Matriculados por Género")
fig, ax = plt.subplots(figsize=(8, 6))
sns.countplot(data=df_año, x='id_g_nero', palette='Set2', ax=ax)
ax.set_title('Distribución de Matriculados por Género', fontsize=14)
ax.set_xlabel('Género', fontsize=12)
ax.set_ylabel('Cantidad de Matriculados', fontsize=12)
ax.set_xticklabels(['Masculino', 'Femenino'])
st.pyplot(fig)

# Gráfico 2: Distribución de Matrícula por Departamento
st.header("Distribución de Matrícula por Departamento")
fig, ax = plt.subplots(figsize=(10, 6))
top_departamentos = df_año['departamento_de_oferta_del_programa'].value_counts().head(10)
sns.barplot(x=top_departamentos.index, y=top_departamentos.values, palette='Blues', ax=ax)
ax.set_title('Distribución de Matrícula por Departamento', fontsize=14)
ax.set_xlabel('Departamento', fontsize=12)
ax.set_ylabel('Cantidad de Matriculados', fontsize=12)
ax.set_xticklabels(top_departamentos.index, rotation=45)
st.pyplot(fig)

# Gráfico 3: Distribución de Matrícula por Programa Académico (Top 10)
st.header("Distribución de Matrícula por Programa Académico (Top 10)")
fig, ax = plt.subplots(figsize=(8, 8))
top_10_programas = df_año['programa_acad_mico'].value_counts().head(10)
plt.pie(top_10_programas, labels=top_10_programas.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('Set3', len(top_10_programas)))
plt.title('Distribución de Matrícula por Programa Académico (Top 10)', fontsize=14)
plt.axis('equal')  # Para que el gráfico sea circular
st.pyplot(fig)

# Mostrar estadísticas básicas
st.header("Estadísticas Básicas")
estadisticas = df_año.describe()
st.write(estadisticas)

# Mostrar insights relevantes
st.header("Insights Relevantes")
# Ejemplo: Ver el número de matriculados en un programa específico
programa_especifico = st.selectbox('Selecciona un programa académico', df_año['programa_acad_mico'].unique())
matriculados_programa = df_año[df_año['programa_acad_mico'] == programa_especifico].shape[0]
st.write(f"Total de matriculados en {programa_especifico}: {matriculados_programa}")

# Mostrar datos filtrados (si el usuario quiere)
if st.checkbox("Ver datos filtrados"):
    st.write(df_año)

