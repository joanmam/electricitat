from altres.imports import *


st.set_page_config(layout="wide")

conn = sqlitecloud.connect(cami_db)
cursor = conn.cursor()



folder_path = r"D:\La meva unitat\Drive\Altres\FusionSolar\*.xlsx"
folder_path = folder_path.replace("\\", "/")
file_list = glob.glob(folder_path)


dataframes = [pd.read_excel(file, header=1) for file in file_list]
df_final = pd.concat(dataframes, ignore_index=True)

df_final.to_excel("combinat.xlsx", index=False)

with open("combinat.xlsx", "rb") as file:
    st.download_button("Descarregar arxiu combinat", data=file.read(), file_name="combinat.xlsx")
