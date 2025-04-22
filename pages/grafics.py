from altres.imports import *

st.set_page_config(layout="wide")

conn = sqlitecloud.connect(cami_db)
cursor = conn.cursor()


# Executar la consulta per obtenir les dades de la taula
query = "SELECT StatisticalPeriod, PVYield, Consumption, Export, SelfConsumptionRate FROM Fusion_per_dia"
df = pd.read_sql(query, conn)



# Eliminar la part 'DST' si causa problemes
df["StatisticalPeriod"] = df["StatisticalPeriod"].str.replace(" DST", "", regex=False)

# Convertir la columna a format datetime (data + hora)
df["StatisticalPeriod"] = pd.to_datetime(df["StatisticalPeriod"], format="%Y-%m-%d")


# Crear gráfico con dos variables en el eje Y
fig1 = px.line(df, x="StatisticalPeriod", y=["PVYield", "Consumption", "Export"],
              title="PVYield, Consumo y Export vs StatisticalPeriod",
              markers=True, template="plotly_white")


st.plotly_chart(fig1)





# Crear figura combinada
fig = go.Figure()

# Añadir líneas normales para PVYield, Consumption y Export
fig.add_trace(go.Scatter(x=df["StatisticalPeriod"], y=df["PVYield"], mode="lines+markers", name="PVYield"))
fig.add_trace(go.Scatter(x=df["StatisticalPeriod"], y=df["Consumption"], mode="lines+markers", name="Consumption"))
fig.add_trace(go.Scatter(x=df["StatisticalPeriod"], y=df["Export"], mode="lines+markers", name="Export"))

# Añadir burbujas para SelfConsumptionRate
fig.add_trace(go.Scatter(x=df["StatisticalPeriod"], y=[max(df["PVYield"])*1.1]*len(df),  # Posición en Y fuera del rango
                         mode="markers", marker=dict(size=df["SelfConsumptionRate"], color="red", opacity=0.6),
                         name="SelfConsumptionRate (burbujas)"))

# Configurar diseño
fig.update_layout(title="PVYield, Consumption y Export con SelfConsumptionRate en burbujas",
                  xaxis_title="StatisticalPeriod", yaxis_title="Medición (kWh)", template="plotly_white")

# Mostrar en Streamlit
st.plotly_chart(fig)