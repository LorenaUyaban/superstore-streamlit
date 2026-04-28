# Superstore Sales Dashboard — Streamlit App

## Descripción
Dashboard interactivo que visualiza el dataset Sample Superstore de Kaggle, revelando 5 hallazgos clave sobre ventas, rentabilidad y comportamiento de descuentos en EE.UU. (2014–2017).

## Dataset
- **Fuente**: Kaggle — Sample Superstore
- **URL**: https://www.kaggle.com/datasets/vivek468/superstore-dataset-final
- **Descripción**: 9,994 órdenes de ventas minoristas en EE.UU. con variables de fecha, geografía, categoría de producto, ventas, profit y descuentos.

## Hallazgos Principales
1. **Furniture tiene margen mínimo**: Genera $742K en ventas pero solo 2.5% de margen vs 17.4% de Technology.
2. **3 sub-categorías venden a pérdida**: Tables (-$17.7K), Bookcases (-$3.5K) y Supplies (-$1.2K) tienen profit negativo.
3. **Descuentos >20% destruyen rentabilidad**: Correlación -0.22 entre descuento y profit; el umbral crítico es el 20%.
4. **Crecimiento del 51% en 4 años**: Ventas pasaron de $484K (2014) a $733K (2017) con pico estacional en noviembre.
5. **Central es el talón de Aquiles**: Buena facturación ($501K) pero el peor margen de las 4 regiones (7.9%).

## Visualizaciones Implementadas
1. Gráfico de barras comparativo de ventas y margen por categoría
2. Distribución de profit por sub-categoría (barras horizontales)
3. Scatter plot descuento vs profit con línea de tendencia
4. Serie temporal mensual de ventas 2014–2017
5. Donut + scatter de composición y margen por región

## Tecnologías Utilizadas
- **Framework**: Streamlit
- **Lenguaje**: Python 3.11
- **Bibliotecas**: Pandas, Plotly Express, scikit-learn (trendline)

## Instalación y Ejecución Local

### Requisitos Previos
- Python 3.9+
- pip

### Instrucciones
```bash
# Clonar repositorio
git clone https://github.com/USUARIO/superstore-streamlit.git
cd superstore-streamlit

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
streamlit run app.py
```

## Despliegue
URL en producción: [Enlace a la app desplegada en Streamlit Community Cloud]

## Autores
- [Nombre Apellido 1]
- [Nombre Apellido 2]
