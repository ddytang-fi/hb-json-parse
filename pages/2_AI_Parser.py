import streamlit as st
import numpy as np
import pandas as pd
import re
import json

st.set_page_config(
    page_title="Aggregate Intelligence Parser",
    page_icon="💰"
)
st.sidebar.header("Aggregate Intelligence Parser")

st.title("Aggregate Intelligence Parser")

ai_uploaded_file = st.file_uploader("Select json file to upload", type=["json"])

if ai_uploaded_file is not None:
    # Read JSON File
    df = pd.read_json(ai_uploaded_file)
    df["roomtype"] = np.where(df["ratedescription"].str.contains("1 sofa bed"), "Sofa Bed + ", "")
    df["roomtype"] = df["roomtype"] + np.where(df["status_code"] == 203, "Hotel not listed",
                            np.where(df["status_code"] == 202, "No rooms available",
                            np.where((df["ratedescription"].str.contains("1 queen")) & (df["ratedescription"].str.contains("1 king")), "King + Queen",
                            np.where(df["ratedescription"].str.contains("2 queen"), "Queen Queen",
                            np.where(df["ratedescription"].str.contains("1 queen"), "Queen",
                            np.where(df["ratedescription"].str.contains("2 king"), "King King",
                            np.where(df["ratedescription"].str.contains("1 king"), "King",
                            np.where(df["ratedescription"].str.contains("2 full"), "Double Double",
                            np.where(df["ratedescription"].str.contains("1 full"), "Double",
                            np.where(df["ratedescription"].str.contains("2 twin"), "Twin Twin",
                            np.where(df["ratedescription"].str.contains("1 twin"), "Twin",
                            np.where(df["ratedescription"].str.contains("4 bunk"), "Bunk Bunk Bunk Bunk",
                            "Other"))))))))))))
    df_export = df[["hotelcode", "ratedate", "roomtype", "onsiterate", "status_code", "ratedescription"]]

    with open("export_ai.csv","w") as f:
        df_export.to_csv(f)
    with open("export_ai.csv") as f:
        st.download_button(
            label="Download Parsed Rack Rates File", 
            data=f, 
            file_name="ai_rack_rates.csv",
            mime="text/csv"
        )