import streamlit as st
import numpy as np
import pandas as pd
import json

st.set_page_config(
    page_title="Hotelbeds Availability Parser",
    page_icon="💡"
)
st.sidebar.header("Hotelbeds Availability Parser")

st.title("Hotelbeds Availability Parser")

hba_uploaded_file = st.file_uploader("Select json file to upload", type=["json"])

if hba_uploaded_file is not None:
    export_filename = hba_uploaded_file.name.replace(".json","") + ".csv"

    # Read and unnest JSON file
    data = json.load(hba_uploaded_file)
    df_availability = pd.json_normalize(data, record_path=["hotels", "hotels", "rooms", "rates"]
                      , meta=[["hotels", "hotels", "currency"], ["hotels", "hotels", "code"], ["hotels", "hotels", "name"], ["hotels", "hotels", "rooms", "code"], ["hotels", "hotels", "rooms", "name"]]
                      , errors="ignore")
    df_export = df_availability[["hotels.hotels.code", "hotels.hotels.name", "hotels.hotels.rooms.code", "hotels.hotels.rooms.name", "hotels.hotels.currency", "net", "packaging", "rateType", "rateKey"]]

    with open("export_hba.csv","w") as f:
        df_export.to_csv(f)
    with open("export_hba.csv") as f:
        st.download_button(
            label="Download Parsed Availability File", 
            data=f, 
            file_name=export_filename,
            mime="text/csv"
        )
