"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel


def clean_campaign_data():
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    """
    import glob
    import os
    import zipfile
    import pandas as pd

    input_dir = "files/input"
    output_dir = "files/output"
    os.makedirs(output_dir, exist_ok=True)
    file_pattern = os.path.join(input_dir, "*.csv.zip")
    csv_zip_files = glob.glob(file_pattern)

    dfs = []
    for file in csv_zip_files:
        df_part = pd.read_csv(file, compression="zip")
        dfs.append(df_part)

    if not dfs:
        return
    
    df_base = pd.concat(dfs, ignore_index=True)


    client_df = df_base[["client_id", "age", "job", "marital", "education", "credit_default", "mortgage"]].copy()
    
    client_df["job"] = client_df["job"].str.replace(".", "", regex=False).str.replace("-", "_", regex=False)
    client_df["education"] = client_df["education"].str.replace(".", "_", regex=False).replace("unknown", pd.NA)
    client_df["credit_default"] = client_df["credit_default"].apply(lambda x: 1 if x == "yes" else 0)
    client_df["mortgage"] = client_df["mortgage"].apply(lambda x: 1 if x == "yes" else 0)

    campaign_df = df_base[[
        "client_id", "number_contacts", "contact_duration", 
        "previous_campaign_contacts", "previous_outcome", "campaign_outcome", "day", "month"
    ]].copy()

    campaign_df["previous_outcome"] = campaign_df["previous_outcome"].apply(lambda x: 1 if x == "success" else 0)
    campaign_df["campaign_outcome"] = campaign_df["campaign_outcome"].apply(lambda x: 1 if x == "yes" else 0)

    
    months_map = {
        "jan": "01", "feb": "02", "mar": "03", "apr": "04", "may": "05", "jun": "06",
        "jul": "07", "aug": "08", "sep": "09", "oct": "10", "nov": "11", "dec": "12"
    }
    
    
    campaign_df["month_num"] = campaign_df["month"].str.lower().map(months_map)
    campaign_df["day_str"] = campaign_df["day"].astype(str).str.zfill(2)
    campaign_df["last_contact_date"] = "2022-" + campaign_df["month_num"] + "-" + campaign_df["day_str"]

    
    campaign_df = campaign_df.drop(columns=["day", "month", "month_num", "day_str"])

    
    economics_df = df_base[["client_id", "cons_price_idx", "euribor_three_months"]].copy()
    economics_df.columns = ["client_id", "cons_price_idx", "euribor_three_months"]

    
    client_df.to_csv(os.path.join(output_dir, "client.csv"), index=False)
    campaign_df.to_csv(os.path.join(output_dir, "campaign.csv"), index=False)
    economics_df.to_csv(os.path.join(output_dir, "economics.csv"), index=False)

    return


if __name__ == "__main__":
    clean_campaign_data()