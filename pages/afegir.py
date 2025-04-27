from altres.imports import *


st.set_page_config(layout="wide")

conn = sqlitecloud.connect(cami_db)
cursor = conn.cursor()

# Pujar un fitxer Excel
uploaded_file = st.file_uploader("Puja un fitxer Excel", type=["xlsx"])


# Carregar l'Excel
df = pd.read_excel(uploaded_file)

# Mostra les primeres files per verificar
st.write(df.head())