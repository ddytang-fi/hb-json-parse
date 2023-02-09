import streamlit as st
import numpy as np
import pandas as pd
import json

st.set_page_config(
    page_title="Priceline Availability Parser",
    page_icon="🛎️"
)
st.sidebar.header("Priceline Availability Parser")

st.title("Priceline Availability Parser")

pla_uploaded_file = st.file_uploader("Select json file to upload", type=["json"])

if pla_uploaded_file is not None:
    export_filename = pla_uploaded_file.name.replace(".json","") + ".csv"

    # Read and unnest JSON file
    data = json.load(pla_uploaded_file)
    df_availability = pd.json_normalize(data, record_path=["getHotelExpress.Availability", "results", "hotel_data", "room_data", "rate_data"]
                      , meta=[["getHotelExpress.Availability", "results", "hotel_data", "id"], ["getHotelExpress.Availability", "results", "hotel_data", "name"], ["getHotelExpress.Availability", "results", "hotel_data", "room_data", "title"]]
                      , errors="ignore")
    df_export = df_availability[["getHotelExpress.Availability.results.hotel_data.id", "getHotelExpress.Availability.results.hotel_data.name", "getHotelExpress.Availability.results.hotel_data.room_data.title", "price_details.baseline_total"]]

    with open("export_pla.csv","w") as f:
        df_export.to_csv(f)
    with open("export_pla.csv") as f:
        st.download_button(
            label="Download Parsed Availability File", 
            data=f, 
            file_name=export_filename,
            mime="text/csv"
        )
