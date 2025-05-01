from altres.imports import *


st.set_page_config(layout="wide")

conn = sqlitecloud.connect(cami_db)
cursor = conn.cursor()



# Pujar un fitxer Excel
uploaded_file = st.file_uploader("Puja un fitxer Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, header=1)
    # Eliminar columnes específiques
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

    df.drop(columns=columnas_a_eliminar, inplace = True)



    # Modificar los encabezados para dejar solo el texto antes del delimitador ":"
    df.columns = df.columns.astype(str).str.split('(').str[0]

    df.columns = df.columns.str.replace('-', '').str.replace(' ', '')


    st.write("Dades carregades:", df.head())

    # Crear la taula SQL

    table_name = "Fusion_per_dia"
    conn.execute(f"DROP TABLE {table_name}")
    df.to_sql(table_name, con=conn, if_exists="replace", index=False)

    st.success(f"Taula '{table_name}' creada correctament a SQLiteCloud!")


