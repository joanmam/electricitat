from altres.imports import *

st.set_page_config(layout="wide")

conn = sqlitecloud.connect(cami_db)
cursor = conn.cursor()


# Executar la consulta per obtenir les dades de la taula
query = "SELECT StatisticalPeriod, PVYield, Consumption, Charge, Discharge, Selfconsumption, Export, Import, SelfConsumptionRate FROM Fusion_per_dia"
df = pd.read_sql(query, conn)



# Eliminar la part 'DST' si causa problemes
df["StatisticalPeriod"] = df["StatisticalPeriod"].str.replace(" DST", "", regex=False)

# Convertir la columna a format datetime (data + hora)
df["StatisticalPeriod"] = pd.to_datetime(df["StatisticalPeriod"], format="%Y-%m-%d")
df["Prod_Autoconsum"] = df["Consumption"] - df["Import"] - df["Discharge"] + df["Charge"]
df["Consum_FV1"] = df["Consumption"] - df["Import"]
df["Consum_FV2"] = df["Prod_Autoconsum"] + df["Discharge"] - df["Charge"]

# Crear gráfico con dos variables en el eje Y
fig1 = px.line(df, x="StatisticalPeriod", y=["Consumption", "Export", "Import", "Prod_Autoconsum", "Consum_FV1"],
              title="Varies vs StatisticalPeriod",
              markers=True, template="plotly_white")



# Configurar la llegenda correctament
fig1.update_layout(
    legend=dict(
        orientation="h",  # Horitzontal
        x=0.5,  # Centrat horitzontalment
        y=-0.3,  # Sota el gràfic
        xanchor="center",
        yanchor="top"
    )
)


st.plotly_chart(fig1)


# Crear figura combinada
fig = go.Figure()



# Añadir líneas normales para PVYield, Consumption y Export
fig.add_trace(go.Scatter(x=df["StatisticalPeriod"], y=df["PVYield"], mode="lines+markers", name="PVYield"))
fig.add_trace(go.Scatter(x=df["StatisticalPeriod"], y=df["Consumption"], mode="lines+markers", name="Consumption"))
fig.add_trace(go.Scatter(x=df["StatisticalPeriod"], y=df["Export"], mode="lines+markers", name="Export"))
fig.add_trace(go.Scatter(x=df["StatisticalPeriod"], y=df["Import"], mode="lines+markers", name="Import"))

# Añadir burbujas para SelfConsumptionRate
fig.add_trace(go.Scatter(x=df["StatisticalPeriod"], y=df["SelfconsumptionRate"],  # Posición en Y fuera del rango
                         mode="lines+markers",
                         marker=dict(size=df["SelfconsumptionRate"],
                        color="#99cc00", opacity=0.6),
                         name="SelfconsumptionRate (burbujas)",
                         yaxis="y2",
                        text = df["SelfconsumptionRate"].astype(str) + "%",  # Texto en el hover con el porcentaje correcto
                        ))

# Configurar diseño con corrección en yaxis2
fig.update_layout(
    title="PVYield, Consumption, Export e Import con SelfconsumptionRate en burbujas",
    xaxis_title="StatisticalPeriod",
    yaxis=dict(title="Medición (kWh)"),
    yaxis2=dict(title="Autoconsumo", overlaying="y", side="right"),
    template="plotly_white",
    legend=dict(
        orientation="h",  # Fa que la llegenda sigui horitzontal
        x=0.5,  # Centra la llegenda horitzontalment
        y=-0.3,  # La situa sota el gràfic
        xanchor="center",
        yanchor="top")
)
# Mostrar en Streamlit
st.plotly_chart(fig)

