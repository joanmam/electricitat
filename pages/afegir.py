from altres.imports import *


st.set_page_config(layout="wide")

conn = sqlitecloud.connect(cami_db)
cursor = conn.cursor()



# Executar la consulta
query = "SELECT * FROM Fusion_per_dia ORDER BY StatisticalPeriod DESC LIMIT 2;"
df_sql= pd.read_sql(query, conn)

# Obtenir la penúltima fila
penultima_registre = df_sql.iloc[1]  # Segona fila (penúltima data)
penultima_data = pd.to_datetime(df_sql.iloc[1]["StatisticalPeriod"], format="%Y-%m-%d")
st.write(penultima_data)



st.title("Pujar fitxers Excel 📂")

fitxer1 = st.file_uploader("Selecciona el primer fitxer", type=["xlsx"])
fitxer2 = st.file_uploader("Selecciona el segon fitxer", type=["xlsx"])

if fitxer1 and fitxer2:
    df1 = pd.read_excel(fitxer1, skiprows=1)
    df2 = pd.read_excel(fitxer2, skiprows=1)
    df_final = pd.concat([df1, df2], ignore_index=True)
    st.dataframe(df_final)

elif fitxer2:  # Si només s'ha pujat fitxer2
    df_final = pd.read_excel(fitxer2, skiprows=1)
    st.dataframe(df_final)

elif fitxer1:  # Si només s'ha pujat fitxer1
    df_final = pd.read_excel(fitxer1, skiprows=1)
    st.dataframe(df_final)
else:
    st.warning("Si us plau, puja almenys un fitxer per continuar.")

columnas_a_eliminar = [
        'Total String Capacity (kWp)',
        'Global Irradiation (kWh/㎡)',
        'Theoretical Yield (kWh)',
        'Total Yield (kWh)',
        'Specific Energy (kWh/kWp)',
        'Loss Due to Export Limitation (kWh)',
        'Loss Due to Export Limitation(€)',
        'Peak Power (kW)',
        'Performance Ratio(%)',
        'CO₂ Avoided (t)',
        'Standard Coal Saved (t)',
        'Revenue (€)']

df_final.drop(columns=columnas_a_eliminar, inplace = True)



# Modificar los encabezados para dejar solo el texto antes del delimitador ":"
df_final.columns = df_final.columns.astype(str).str.split('(').str[0]

df_final.columns = df_final.columns.str.replace('-', '').str.replace(' ', '')

df_final["StatisticalPeriod"] = pd.to_datetime(df_final["StatisticalPeriod"], format="%Y-%m-%d")
df_filtrat = df_final[df_final["StatisticalPeriod"] > penultima_data]
df_filtrat["StatisticalPeriod"] = df_filtrat["StatisticalPeriod"].dt.strftime('%Y-%m-%d')  # Format personalitzat
st.write("el filtrat es")
st.write(df_filtrat)

cursor.executemany(
    "INSERT INTO Fusion_per_dia (StatisticalPeriod, PVYield, InverterYield, Export,"
    "Import, Consumption, Selfconsumption, SelfconsumptionRate,"
    "Charge, Discharge) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
    df_filtrat.values.tolist()
)

st.success("Les dades s'han pujat")
conn.commit()