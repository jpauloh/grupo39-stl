
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

# Sidebar con filtros

# Filtro por fecha y año
min_date = data["Date"].min()
max_date = data["Date"].max()
date_range = st.sidebar.date_input("Rango de Fechas", [min_date, max_date], min_value=min_date, max_value=max_date)

# Extraer año como columna adicional
data["Month"] = data["Date"].dt.strftime("%B")
months = st.sidebar.multiselect("Mes", options=data["Month"].unique(), default=data["Month"].unique())

st.sidebar.title("Filtros de Segmentación")
cities = st.sidebar.multiselect("Ciudad", options=data["City"].unique(), default=data["City"].unique())
genders = st.sidebar.multiselect("Género", options=data["Gender"].unique(), default=data["Gender"].unique())
types = st.sidebar.multiselect("Tipo de Cliente", options=data["Customer type"].unique(), default=data["Customer type"].unique())
products = st.sidebar.multiselect("Línea de Producto", options=data["Product line"].unique(), default=data["Product line"].unique())
payments = st.sidebar.multiselect("Método de Pago", options=data["Payment"].unique(), default=data["Payment"].unique())
branches = st.sidebar.multiselect("Sucursal", options=data["Branch"].unique(), default=data["Branch"].unique())

# Navegación
st.sidebar.markdown("---")
section = st.sidebar.radio("Ir a la sección:", [
    "1. Selección de Variables Clave",
    "2. Visualización Básica de Datos",
    "3. Gráficos Compuestos",
    "4. Visualización Multivariada",
    "5. Visualización 3D"
])

# Aplicar filtros al dataframe
filtered_data = data[
    (data["Date"] >= pd.to_datetime(date_range[0])) &
    (data["Date"] <= pd.to_datetime(date_range[1])) &
    (data["Month"].isin(months)) &
    (data["City"].isin(cities)) &
    (data["Gender"].isin(genders)) &
    (data["Customer type"].isin(types)) &
    (data["Product line"].isin(products)) &
    (data["Payment"].isin(payments)) &
    (data["Branch"].isin(branches))
]

st.sidebar.info("Grupo 39 | Proyecto Final")

# Sección 1
if section == "1. Selección de Variables Clave":
    st.subheader("1. Selección de Variables Clave")
    st.markdown("""Se consideran variables clave para el análisis:
- City, Gender, Branch, Customer type
- Product line, Payment
- Unit price, Quantity, Total, Rating, Gross income
Las variables categóricas permiten segmentar los datos; las numéricas aportan contexto de comportamiento y rentabilidad.
""")

# Sección 2: Visualizaciones básicas
elif section == "2. Visualización Básica de Datos":
    st.subheader("2. Visualización Básica de Datos")

    st.markdown("### Ventas Totales Diarias")
    daily_sales = filtered_data.groupby('Date')['Total'].sum()
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(daily_sales.index, daily_sales.values, marker='o')
    ax.set_title('Ventas Totales por Día')
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Total ($)')
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

    st.markdown("### Total vs Rating por Método de Pago")
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    sns.scatterplot(data=filtered_data, x='Total', y='Rating', hue='Payment', ax=ax2)
    st.pyplot(fig2)

    st.markdown("### Boxplot: Total por Línea de Producto")
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    sns.boxplot(data=filtered_data, x='Product line', y='Total', ax=ax3, palette='Set2')
    ax3.tick_params(axis='x', rotation=45)
    st.pyplot(fig3)

# Sección 3: Gráficos Compuestos
elif section == "3. Gráficos Compuestos":
    st.subheader("3. Gráficos Compuestos")
    st.markdown("### Distribución del Total por Género y Tipo de Cliente")
    g = sns.FacetGrid(filtered_data, col="Gender", row="Customer type", height=3)
    g.map(sns.histplot, "Total", bins=20, kde=True)
    st.pyplot(g.fig)

# Sección 4: Multivariado
elif section == "4. Visualización Multivariada":
    st.subheader("4. Visualización Multivariada")
    st.markdown("### Pairplot entre variables numéricas")

    selected_vars = ['Unit price', 'Quantity', 'Total', 'gross income', 'Rating']
    fig4 = sns.pairplot(filtered_data[selected_vars], corner=True)
    st.pyplot(fig4)

# Sección 5: Visualización 3D
elif section == "5. Visualización 3D":
    st.subheader("5. Visualización en 3D")
    st.markdown("### Scatterplot 3D: Unit Price vs Quantity vs Rating")

    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')
    sc = ax.scatter(filtered_data['Unit price'], filtered_data['Quantity'], filtered_data['Rating'],
                    c=filtered_data['Rating'], cmap='viridis')
    ax.set_xlabel("Unit Price")
    ax.set_ylabel("Quantity")
    ax.set_zlabel("Rating")
    st.pyplot(fig)
