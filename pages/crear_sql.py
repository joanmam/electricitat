from altres.imports import *


st.set_page_config(layout="wide")

conn = sqlitecloud.connect(cami_db)
cursor = conn.cursor()



# Pujar un fitxer Excel
uploaded_file = st.file_uploader("Puja un fitxer Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.write("Dades carregades:", df.head())

    # Crear la taula SQL

    table_name = "Fusion_per_dia"
    conn.execute(f"DROP TABLE {table_name}")
    df.to_sql(table_name, con=conn, if_exists="replace", index=False)

    st.success(f"Taula '{table_name}' creada correctament a SQLiteCloud!")

