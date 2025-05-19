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
    "2. Análisis Gráfico de las Ventas",
    "3. Gráficos Compuestos",
    "4. Visualización 3D"
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
elif section == "2. Análisis Gráfico de las Ventas":
    st.subheader("2. Análisis Gráfico de las Ventas")

    st.markdown("### 2.1 📈 Evolución de las Ventas Totales")
    ventas_diarias = filtered_data.groupby('Date')['Total'].sum()
    fig, ax = plt.subplots(figsize=(14, 7))
    ventas_diarias.plot(kind='line', marker='o', ax=ax)
    ax.set_title('Ventas Diarias Totales')
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Ventas Totales')
    ax.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    # Mostrar en Streamlit
    st.pyplot(fig)

    st.markdown("### 2.2 📊 Ingresos por Línea de Productos")
    ventas_por_producto = filtered_data.groupby('Product line')['Total'].sum().reset_index()
    ventas_por_producto = ventas_por_producto.sort_values(by='Total', ascending=False)
    fig2, ax2 = plt.subplots(figsize=(14, 7))
    sns.barplot(data=ventas_por_producto, x='Total', y='Product line', color='steelblue', ax=ax2)
    ax2.set_title('Ventas Totales por Línea de Producto')
    ax2.set_xlabel('Total Ventas')
    ax2.set_ylabel('Línea de Producto')
    ax2.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    st.pyplot(fig2)

    st.markdown("### 2.3 ⭐ Distribución de la Calificación de Clientes")
    sns.set(style="white")
    fig3, ax3 = plt.subplots(figsize=(14, 7))
    sns.histplot(data=filtered_data, x='Rating', bins=40, kde=True, color='steelblue', edgecolor='black', ax=ax3)
    ax3.set_title('Distribución de la Calificación del Cliente', fontsize=16)
    ax3.set_xlabel('Rating')
    ax3.set_ylabel('Frecuencia')
    st.pyplot(fig3)

    st.markdown("### 2.4 📦 Comparación del Gasto por Tipo de Cliente")
    sns.set(style="white")
    custom_palette = {'Member': 'steelblue', 'Normal': '#F4A7B9'}
    fig4, ax4 = plt.subplots(figsize=(14, 7))
    sns.boxplot(data=filtered_data, x='Customer type', y='Total', hue='Customer type',
                palette=custom_palette, ax=ax4)
    ax4.set_title('Distribución del Gasto por Tipo de Cliente', fontsize=14)
    ax4.set_xlabel('Tipo de Cliente', fontsize=12)
    ax4.set_ylabel('Total', fontsize=12)
    st.pyplot(fig4)
    # ----- Estadísticas descriptivas por tipo de cliente -----
    st.markdown("#### 📊 Estadísticas Descriptivas por Tipo de Cliente")
    stats = filtered_data.groupby('Customer type')['Total'].describe()[['mean', '50%', 'std', 'min', '25%', '75%', 'max']].rename(columns={
        'mean': 'Media',
        '50%': 'Mediana',
        'std': 'Desviación estándar',
        'min': 'Mínimo',
        '25%': 'Q1',
        '75%': 'Q3',
        'max': 'Máximo'
    })
    st.dataframe(stats.style.format("{:.2f}"), use_container_width=True)

    st.markdown("### 2.5 📈 Relación entre Costo y Ganancia Bruta")
    sns.set(style="white")
    fig5, ax5 = plt.subplots(figsize=(14, 7))
    sns.scatterplot(data=filtered_data, x='cogs', y='gross income', alpha=0.6, color='steelblue', ax=ax5)
    sns.regplot(data=filtered_data, x='cogs', y='gross income', scatter=False, color='darkred', ax=ax5)
    ax5.set_title('Relación Costo de Bienes y Ganancia Bruta', fontsize=14)
    ax5.set_xlabel('Costo de Bienes Vendidos (cogs)')
    ax5.set_ylabel('Ganancia Bruta (gross income)')
    st.pyplot(fig5)
    correlacion = filtered_data[['cogs', 'gross income']].corr().iloc[0,1]
    st.markdown(f"#### 🔗 Coeficiente de correlación (Pearson): `{correlacion}`")

    st.markdown("### 2.6 💳 Métodos de Pago Preferidos")
    sns.set(style="white")
    custom_palette = {
        'Credit card': 'steelblue',
        'Cash': '#F4A7B9',
        'Ewallet': '#FFD580'
    }
    fig6, ax6 = plt.subplots(figsize=(14, 7))
    sns.countplot(data=filtered_data, x='Payment', hue='Payment', palette=custom_palette, legend=False, ax=ax6)
    ax6.set_title('Métodos de Pago Preferidos', fontsize=16)
    ax6.set_xlabel('Método de Pago')
    ax6.set_ylabel('Cantidad de Transacciones')
    for p in ax6.patches:
        height = p.get_height()
        ax6.annotate(f'{int(height)}', 
                    (p.get_x() + p.get_width() / 2., height / 2),
                    ha='center', va='center', color='white', fontsize=12, fontweight='bold')
    
    st.pyplot(fig6)

    st.markdown("### 2.7 🔍 Análisis de Correlación Numérica")
    variables_numericas = ['Unit price', 'Quantity', 'Tax 5%', 'Total', 'cogs', 'gross income', 'Rating']
    correlation_matrix = filtered_data[variables_numericas].corr()
    fig7, ax7 = plt.subplots(figsize=(14, 7))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5, ax=ax7)
    ax.set_title('Matriz de Correlación entre Variables Numéricas', fontsize=16)
    st.pyplot(fig7)


    

# Sección 3: Gráficos Compuestos
elif section == "3. Gráficos Compuestos":
    st.subheader("3. Gráficos Compuestos")
    st.markdown("### 3.1 Distribución del Total de Compras según Género y Tipo de Cliente")

    g = sns.FacetGrid(filtered_data, col="Gender", row="Customer type", margin_titles=True, height=4)
    g.map(sns.histplot, "Total", bins=20, kde=True)
    g.fig.subplots_adjust(top=0.9)
    g.fig.suptitle("Distribución del Total de Compras según Género y Tipo de Cliente")

    st.pyplot(g.fig)

# Sección 4: Visualización 3D
elif section == "4. Visualización 3D":
    st.subheader("4. Visualización en 3D")
    st.markdown("### 4.1 Visualización 3D: Unit Price vs Quantity vs Rating")

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
