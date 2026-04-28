import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Superstore Sales Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

@st.cache_data
def load_data():
    df = pd.read_csv("superstore.csv", encoding="latin-1")
    df["Order Date"] = pd.to_datetime(df["Order Date"], format="%m/%d/%Y")
    df["Ship Date"]  = pd.to_datetime(df["Ship Date"],  format="%m/%d/%Y")
    df["Year"]       = df["Order Date"].dt.year
    df["Month"]      = df["Order Date"].dt.to_period("M").astype(str)
    df["Discount Bucket"] = pd.cut(
        df["Discount"],
        bins=[-0.01, 0, 0.10, 0.20, 0.30, 0.50, 0.81],
        labels=["0%", "1-10%", "11-20%", "21-30%", "31-50%", ">50%"],
    )
    return df

df = load_data()

COLOR_BLUE   = "#378ADD"
COLOR_GREEN  = "#1D9E75"
COLOR_RED    = "#E24B4A"
COLOR_AMBER  = "#BA7517"
SEQ_BLUES    = px.colors.sequential.Blues[2:]
REGION_COLORS = {
    "West": COLOR_GREEN, "East": COLOR_BLUE,
    "Central": COLOR_RED, "South": COLOR_AMBER,
}

# Sidebar
st.sidebar.header("Filtros")
years     = sorted(df["Year"].unique())
sel_years = st.sidebar.multiselect("Año",       years,                   default=years)
sel_cats  = st.sidebar.multiselect("Categoría", sorted(df["Category"].unique()), default=sorted(df["Category"].unique()))
sel_regs  = st.sidebar.multiselect("Región",    sorted(df["Region"].unique()),   default=sorted(df["Region"].unique()))
sel_segs  = st.sidebar.multiselect("Segmento",  sorted(df["Segment"].unique()),  default=sorted(df["Segment"].unique()))

mask = (
    df["Year"].isin(sel_years) &
    df["Category"].isin(sel_cats) &
    df["Region"].isin(sel_regs) &
    df["Segment"].isin(sel_segs)
)
dff = df[mask]

st.sidebar.markdown("---")
st.sidebar.metric("Órdenes",      f"{len(dff):,}")
st.sidebar.metric("Ventas",       f"${dff['Sales'].sum():,.0f}")
st.sidebar.metric("Profit",       f"${dff['Profit'].sum():,.0f}")
st.sidebar.metric("Margen",
    f"{(dff['Profit'].sum()/dff['Sales'].sum()*100):.1f}%" if dff['Sales'].sum() > 0 else "N/A")

# Header + KPIs
st.title("🛒 Superstore Sales — Análisis de Visualización")
st.caption("Dataset: Sample Superstore (Kaggle) · 9,994 órdenes · 2014-2017")
k1,k2,k3,k4,k5 = st.columns(5)
k1.metric("Órdenes",    f"{len(dff):,}")
k2.metric("Ventas",     f"${dff['Sales'].sum()/1e6:.2f}M")
k3.metric("Profit",     f"${dff['Profit'].sum()/1e3:.1f}K")
k4.metric("Margen",     f"{(dff['Profit'].sum()/dff['Sales'].sum()*100):.1f}%" if dff['Sales'].sum()>0 else "N/A")
k5.metric("Categorías", f"{dff['Category'].nunique()}")
st.markdown("---")

# H1 — Comparación por Categoría
st.subheader("H1 · Furniture vende casi tanto como Technology pero su margen es 7× menor")
cat_df = dff.groupby("Category", as_index=False).agg(Sales=("Sales","sum"), Profit=("Profit","sum"))
cat_df["Margin%"] = cat_df["Profit"] / cat_df["Sales"] * 100

col1, col2 = st.columns(2)
with col1:
    fig = go.Figure()
    fig.add_bar(x=cat_df["Category"], y=cat_df["Sales"],  name="Ventas", marker_color=COLOR_BLUE,  opacity=0.85)
    fig.add_bar(x=cat_df["Category"], y=cat_df["Profit"], name="Profit", marker_color=COLOR_GREEN, opacity=0.85)
    fig.update_layout(title="Ventas vs Profit por categoría ($)", barmode="group", plot_bgcolor="white",
                      xaxis_title=None, yaxis_title="USD", legend=dict(orientation="h", y=1.12), margin=dict(t=60,b=30))
    fig.update_yaxes(tickprefix="$", gridcolor="#f0f0f0")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig2 = px.bar(cat_df.sort_values("Margin%"), x="Margin%", y="Category", orientation="h",
                  color="Margin%", color_continuous_scale=["#E24B4A","#FAEEDA","#1D9E75"], color_continuous_midpoint=10,
                  text=cat_df.sort_values("Margin%")["Margin%"].apply(lambda v: f"{v:.1f}%"),
                  title="Margen de ganancia por categoría (%)")
    fig2.update_traces(textposition="outside")
    fig2.update_layout(plot_bgcolor="white", coloraxis_showscale=False,
                       xaxis_title="Margen %", yaxis_title=None, margin=dict(t=60,b=30))
    fig2.update_xaxes(ticksuffix="%", gridcolor="#f0f0f0")
    st.plotly_chart(fig2, use_container_width=True)

st.caption("💡 Furniture genera $742K en ventas pero solo 2.5% de margen. Technology y Office Supplies operan al 17%.")
st.markdown("---")

# H2 — Distribución por Sub-Categoría
st.subheader("H2 · Tables, Bookcases y Supplies se venden a pérdida neta")
sub_df = dff.groupby("Sub-Category", as_index=False).agg(Sales=("Sales","sum"), Profit=("Profit","sum")).sort_values("Profit")
fig3 = px.bar(sub_df, x="Profit", y="Sub-Category", orientation="h",
              color="Profit", color_continuous_scale=["#E24B4A","#FAEEDA","#1D9E75"], color_continuous_midpoint=0,
              text=sub_df["Profit"].apply(lambda v: f"${v:,.0f}"),
              title="Profit total por sub-categoría — las rojas destruyen valor")
fig3.update_traces(textposition="outside")
fig3.update_layout(plot_bgcolor="white", coloraxis_showscale=False,
                   xaxis_title="Profit (USD)", yaxis_title=None, height=480, margin=dict(t=60,b=30))
fig3.update_xaxes(tickprefix="$", gridcolor="#f0f0f0")
fig3.add_vline(x=0, line_width=1.5, line_color="#888", line_dash="dash")
st.plotly_chart(fig3, use_container_width=True)
st.caption("💡 Tables pierde $17,725 vendiendo $207K. Copiers es la más rentable con $55,617.")
st.markdown("---")

# H3 — Relación Descuento vs Profit
st.subheader("H3 · Descuentos mayores al 20% invierten la rentabilidad")
col3, col4 = st.columns([1.2, 1])

with col3:
    disc_df = (dff.groupby("Discount Bucket", observed=True)
               .agg(avg_profit=("Profit","mean"), count=("Profit","count")).reset_index())
    fig4 = px.bar(disc_df, x="Discount Bucket", y="avg_profit",
                  color="avg_profit", color_continuous_scale=["#E24B4A","#FAEEDA","#1D9E75"], color_continuous_midpoint=0,
                  text=disc_df["avg_profit"].apply(lambda v: f"${v:,.0f}"),
                  title="Profit promedio por nivel de descuento")
    fig4.update_traces(textposition="outside")
    fig4.update_layout(plot_bgcolor="white", coloraxis_showscale=False,
                       xaxis_title="Nivel de descuento", yaxis_title="Profit promedio ($)", margin=dict(t=60,b=30))
    fig4.update_yaxes(tickprefix="$", gridcolor="#f0f0f0")
    fig4.add_hline(y=0, line_width=1.5, line_color="#888", line_dash="dash")
    st.plotly_chart(fig4, use_container_width=True)

with col4:
    sample = dff.sample(min(1500, len(dff)), random_state=42)
    fig5 = px.scatter(sample, x="Discount", y="Profit", color="Category",
                      color_discrete_map={"Furniture": COLOR_AMBER, "Office Supplies": COLOR_BLUE, "Technology": COLOR_GREEN},
                      opacity=0.45, trendline="lowess",
                      title="Scatter: Descuento vs Profit por categoría")
    fig5.update_layout(plot_bgcolor="white", xaxis_title="Descuento", yaxis_title="Profit ($)",
                       xaxis_tickformat=".0%", legend=dict(orientation="h", y=1.12), margin=dict(t=60,b=30))
    fig5.update_xaxes(gridcolor="#f0f0f0")
    fig5.update_yaxes(gridcolor="#f0f0f0", tickprefix="$")
    st.plotly_chart(fig5, use_container_width=True)

st.caption("💡 El umbral crítico es el 20%. Por encima, el profit promedio colapsa de +$25 a -$156.")
st.markdown("---")

# H4 — Evolución Temporal
st.subheader("H4 · Las ventas crecen +51% en 4 años con pico estacional cada noviembre")
time_df = dff.groupby("Month", as_index=False).agg(Sales=("Sales","sum"), Profit=("Profit","sum")).sort_values("Month")
fig6 = make_subplots(specs=[[{"secondary_y": True}]])
fig6.add_trace(go.Scatter(x=time_df["Month"], y=time_df["Sales"], name="Ventas",
                           line=dict(color=COLOR_BLUE, width=2), fill="tozeroy", fillcolor="rgba(55,138,221,0.10)"), secondary_y=False)
fig6.add_trace(go.Scatter(x=time_df["Month"], y=time_df["Profit"], name="Profit",
                           line=dict(color=COLOR_GREEN, width=2, dash="dot")), secondary_y=True)
fig6.update_layout(title="Evolución mensual de Ventas y Profit (2014–2017)", plot_bgcolor="white",
                   legend=dict(orientation="h", y=1.12), margin=dict(t=60,b=50), xaxis=dict(tickangle=45, gridcolor="#f0f0f0"))
fig6.update_yaxes(title_text="Ventas ($)", tickprefix="$", gridcolor="#f0f0f0", secondary_y=False)
fig6.update_yaxes(title_text="Profit ($)", tickprefix="$", secondary_y=True)
st.plotly_chart(fig6, use_container_width=True)

yr_df = dff.groupby("Year", as_index=False).agg(Sales=("Sales","sum"), Profit=("Profit","sum"))
yr_df["Growth%"] = yr_df["Sales"].pct_change() * 100
col5, col6 = st.columns(2)
with col5:
    fig7 = px.bar(yr_df, x="Year", y="Sales", color="Sales", color_continuous_scale=SEQ_BLUES,
                  text=yr_df["Sales"].apply(lambda v: f"${v/1e3:.0f}K"), title="Ventas anuales totales")
    fig7.update_traces(textposition="outside")
    fig7.update_layout(plot_bgcolor="white", coloraxis_showscale=False, xaxis_title=None, yaxis_title="Ventas ($)", margin=dict(t=60,b=30))
    fig7.update_yaxes(tickprefix="$", gridcolor="#f0f0f0")
    st.plotly_chart(fig7, use_container_width=True)

with col6:
    yr_growth = yr_df.dropna(subset=["Growth%"])
    fig8 = px.bar(yr_growth, x="Year", y="Growth%",
                  color="Growth%", color_continuous_scale=["#E24B4A","#FAEEDA","#1D9E75"], color_continuous_midpoint=0,
                  text=yr_growth["Growth%"].apply(lambda v: f"{v:.1f}%"), title="Crecimiento anual (%)")
    fig8.update_traces(textposition="outside")
    fig8.update_layout(plot_bgcolor="white", coloraxis_showscale=False, xaxis_title=None, yaxis_title="Crecimiento %", margin=dict(t=60,b=30))
    fig8.update_yaxes(ticksuffix="%", gridcolor="#f0f0f0")
    fig8.add_hline(y=0, line_width=1.2, line_color="#888", line_dash="dash")
    st.plotly_chart(fig8, use_container_width=True)

st.caption("💡 Caída del 2.8% en 2015, recuperación fuerte: +29% en 2016 y +20% en 2017. Nov es el mes récord cada año.")
st.markdown("---")

# H5 — Composición por Región
st.subheader("H5 · West lidera en rentabilidad — Central factura mucho pero gana poco")
reg_df = dff.groupby("Region", as_index=False).agg(Sales=("Sales","sum"), Profit=("Profit","sum"))
reg_df["Margin%"] = reg_df["Profit"] / reg_df["Sales"] * 100

col7, col8, col9 = st.columns(3)
with col7:
    fig9 = px.pie(reg_df, values="Sales", names="Region", color="Region",
                  color_discrete_map=REGION_COLORS, title="Composición de ventas por región", hole=0.4)
    fig9.update_traces(textinfo="percent+label", textposition="outside")
    fig9.update_layout(showlegend=False, margin=dict(t=60,b=30))
    st.plotly_chart(fig9, use_container_width=True)

with col8:
    fig10 = px.bar(reg_df.sort_values("Sales", ascending=False), x="Region", y=["Sales","Profit"],
                   barmode="group", color_discrete_map={"Sales": COLOR_BLUE, "Profit": COLOR_GREEN},
                   title="Ventas vs Profit por región")
    fig10.update_layout(plot_bgcolor="white", legend_title=None, legend=dict(orientation="h", y=1.12),
                        xaxis_title=None, yaxis_title="USD", margin=dict(t=60,b=30))
    fig10.update_yaxes(tickprefix="$", gridcolor="#f0f0f0")
    st.plotly_chart(fig10, use_container_width=True)

with col9:
    fig11 = px.bar(reg_df.sort_values("Margin%"), x="Margin%", y="Region", orientation="h",
                   color="Margin%", color_continuous_scale=["#E24B4A","#FAEEDA","#1D9E75"], color_continuous_midpoint=12,
                   text=reg_df.sort_values("Margin%")["Margin%"].apply(lambda v: f"{v:.1f}%"),
                   title="Margen de ganancia por región")
    fig11.update_traces(textposition="outside")
    fig11.update_layout(plot_bgcolor="white", coloraxis_showscale=False,
                        xaxis_title="Margen %", yaxis_title=None, margin=dict(t=60,b=30))
    fig11.update_xaxes(ticksuffix="%", gridcolor="#f0f0f0")
    st.plotly_chart(fig11, use_container_width=True)

st.caption("💡 West: $725K y 14.9% de margen — la mejor región. Central: $501K pero solo 7.9% — el peor del negocio.")
st.markdown("---")
st.markdown("<div style='text-align:center;color:gray;font-size:12px'>Herramientas y Visualización de Datos · Proyecto 2 · Fundación Universitaria Los Libertadores</div>", unsafe_allow_html=True)
