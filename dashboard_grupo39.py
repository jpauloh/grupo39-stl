import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D

# Configuración inicial
st.set_page_config(page_title="Dashboard Grupo 39", layout="wide")
st.title("Dashboard Interactivo - Grupo 39")

# Cargar datos
data = pd.read_csv('data.csv')
data['Date'] = pd.to_datetime(data['Date'], format='%m/%d/%Y')

st.sidebar.info("Grupo 39 | Proyecto Final")
# Navegación
st.sidebar.markdown("---")
section = st.sidebar.radio("Ir a la sección:", [
    "1. Selección de Variables Clave",
    "2. Visualización Básica de Datos",
    "3. Gráficos Compuestos",
    "4. Visualización Multivariada",
    "5. Visualización 3D"
])

# Sidebar con filtros
st.sidebar.title("Filtros de Segmentación")

# Filtro por fecha y año
min_date = data["Date"].min()
max_date = data["Date"].max()
date_range = st.sidebar.date_input("Rango de Fechas", [min_date, max_date], min_value=min_date, max_value=max_date)
# Otros Filtros
cities = st.sidebar.multiselect("Ciudad (City)", options=data["City"].unique(), default=data["City"].unique())
genders = st.sidebar.multiselect("Género (Gender)", options=data["Gender"].unique(), default=data["Gender"].unique())
types = st.sidebar.multiselect("Tipo de Cliente (Customer type)", options=data["Customer type"].unique(), default=data["Customer type"].unique())
products = st.sidebar.multiselect("Línea de Producto (Product line)", options=data["Product line"].unique(), default=data["Product line"].unique())
payments = st.sidebar.multiselect("Método de Pago (Payment)", options=data["Payment"].unique(), default=data["Payment"].unique())
branches = st.sidebar.multiselect("Sucursal (Branch)", options=data["Branch"].unique(), default=data["Branch"].unique())

# Aplicar filtros al dataframe
filtered_data = data[
    (data["Date"] >= pd.to_datetime(date_range[0])) &
    (data["Date"] <= pd.to_datetime(date_range[1])) &
    (data["City"].isin(cities)) &
    (data["Gender"].isin(genders)) &
    (data["Customer type"].isin(types)) &
    (data["Product line"].isin(products)) &
    (data["Payment"].isin(payments)) &
    (data["Branch"].isin(branches))
]

# Sección 1
if section == "1. Selección de Variables Clave":
    st.subheader("1. Selección de Variables Clave")
    st.markdown("""
    #### Variables relevantes para el análisis del negocio

    | Variable  | Análisis de Negocio  |
    |-----------|-----------|
    |**Branch** |Segmentar o agrupar las ventas según las distintas sucursales|
    |**City**   |Clasificar las ventas según ubicación geográfica|
    |**Customer Type**|Segmentar las ventas según el tipo de cliente (Miembro o Normal)|
    |**Gender**|Clasificar y comparar las ventas según el género de las personas (Masculino o Femenino)|
    |**Product line**|Clasificar y comparar las ventas por línea de productos, observar cuál tiene más incidencia en el negocio|
    |**Unit price**|Analizar cómo influye el precio en la demanda de productos y satisfacción del cliente|
    |**Quantity**|Analizar la demanda de producto bajo el contexto del negocio|
    |**Total**|Evaluar el rendimiento del negocio|
    |**Date**|Analizar la evolución del negocio a través del tiempo|
    |**Time**|Observar momentos del día en qué se vende más|
    |**Payment**|Observar los métodos de pago preferidos por el cliente|
    |**gross income**|Evaluar la rentabilidad del negocio ¿dónde se está generando más valor?|
    |**Rating**|Analizar la satisfacción del cliente|
    """)
    #- City, Gender, Branch, Customer type
    #- Product line, Payment
    #- Unit price, Quantity, Total, Rating, Gross income
    #Las variables categóricas permiten segmentar los datos; las numéricas aportan contexto de comportamiento y rentabilidad.
    
    # Sección 2: Visualizaciones básicas
elif section == "2. Visualización Básica de Datos":
    st.subheader("2. Visualización Básica de Datos")

    st.markdown("### Ventas Totales Diarias")
    daily_sales = filtered_data.groupby('Date')['Total'].sum()
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.plot(daily_sales.index, daily_sales.values, marker='o')
    ax.set_title('Ventas Totales por Día')
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Total ($)')
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

    st.markdown("### Total vs Rating por Método de Pago")
    fig2, ax2 = plt.subplots(figsize=(14, 7))
    sns.scatterplot(data=filtered_data, x='Total', y='Rating', hue='Payment', ax=ax2)
    st.pyplot(fig2)

    st.markdown("### Boxplot: Total por Línea de Producto")
    fig3, ax3 = plt.subplots(figsize=(14, 7))
    sns.boxplot(data=filtered_data, x='Product line', y='Total', ax=ax3, palette='Set2')
    ax3.tick_params(axis='x', rotation=45)
    st.pyplot(fig3)

    st.markdown("### Matriz de Correlación entre Variables Numéricas")
    corr_vars = filtered_data[['Unit price', 'Quantity', 'Total', 'gross income', 'Rating']]
    corr_matrix = corr_vars.corr()
    fig4, ax4 = plt.subplots(figsize=(14, 7))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', ax=ax4)
    ax4.set_title('Matriz de Correlación')

    st.pyplot(fig4)
    

# Sección 3: Gráficos Compuestos
elif section == "3. Gráficos Compuestos":
    st.subheader("3. Gráficos Compuestos")
    st.markdown("### Distribución del Total de Compras según Género y Tipo de Cliente")

    g = sns.FacetGrid(filtered_data, col="Gender", row="Customer type", margin_titles=True, height=4)
    g.map(sns.histplot, "Total", bins=20, kde=True)
    g.fig.subplots_adjust(top=0.9)
    g.fig.suptitle("Distribución del Total de Compras según Género y Tipo de Cliente")

    st.pyplot(g.fig)

# Sección 4: Multivariado
elif section == "4. Visualización Multivariada":
    st.subheader("4. Visualización Multivariada")
    st.markdown("### Pairplot entre variables numéricas")

    selected_vars = ['Unit price', 'Quantity', 'Total', 'gross income', 'Rating']
    fig4 = sns.pairplot(filtered_data[selected_vars], diag_kind='hist' ,corner=True)
    st.pyplot(fig4)

# Sección 5: Visualización 3D
elif section == "5. Visualización 3D":
    st.subheader("5. Visualización en 3D")
    st.markdown("### Visualización 3D: Unit Price vs Quantity vs Rating")

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    x = filtered_data['Unit price']
    y = filtered_data['Quantity']
    z = filtered_data['Rating']

    sc = ax.scatter(x, y, z, c=z, cmap='viridis', alpha=0.8)
    ax.set_xlabel('Unit Price')
    ax.set_ylabel('Quantity')
    ax.set_zlabel('Rating')
    ax.set_title('Visualización 3D: Unit Price vs Quantity vs Rating')

    cbar = plt.colorbar(sc, ax=ax, shrink=0.5)
    cbar.set_label('Rating')

    plt.tight_layout()
    st.pyplot(fig)
