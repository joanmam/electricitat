from altres.imports import *


st.set_page_config(layout="wide")

conn = sqlitecloud.connect(cami_db)
cursor = conn.cursor()



unio = st.radio(
    "Que vols fer?",
    ["Unir", "No unir"],
)

if unio == "Unir":
    st.write("Unir")
else:
    st.write("No unir")
    st.switch_page("pages/electricitat.py")