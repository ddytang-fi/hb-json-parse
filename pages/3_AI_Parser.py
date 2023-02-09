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
    export_filename = ai_uploaded_file.name.replace(".json","") + ".csv"

    # Read JSON File
    df = pd.read_json(ai_uploaded_file)
    df["roomtype"] = np.where(df["ratedescription"].str.contains("1 sofa bed"), "Sofa Bed + ", "")
    df["roomtype"] = np.where(df["ratedescription"].str.contains("Sofa Bed"), "Sofa Bed + ", "")
    df["roomtype"] = df["roomtype"] + np.where(df["status_code"] == 203, "Hotel not listed",
                            np.where(df["status_code"] == 202, "No rooms available",
                            np.where((df["ratedescription"].str.contains("1 queen")) & (df["ratedescription"].str.contains("1 king")), "King + Queen",
                            np.where((df["ratedescription"].str.contains("1 Queen")) & (df["ratedescription"].str.contains("1 King")), "King + Queen",
                            np.where(df["ratedescription"].str.contains("2 queen"), "Queen Queen",
                            np.where(df["ratedescription"].str.contains("2 Queen"), "Queen Queen",
                            np.where(df["ratedescription"].str.contains("1 queen"), "Queen",
                            np.where(df["ratedescription"].str.contains("1 Queen"), "Queen",
                            np.where(df["ratedescription"].str.contains("2 king"), "King King",
                            np.where(df["ratedescription"].str.contains("2 King"), "King King",
                            np.where(df["ratedescription"].str.contains("1 king"), "King",
                            np.where(df["ratedescription"].str.contains("1 King"), "King",
                            np.where(df["ratedescription"].str.contains("2 double"), "Double Double",
                            np.where(df["ratedescription"].str.contains("2 Double"), "Double Double",
                            np.where(df["ratedescription"].str.contains("2 full"), "Double Double",
                            np.where(df["ratedescription"].str.contains("2 Full"), "Double Double",
                            np.where(df["ratedescription"].str.contains("1 full"), "Double",
                            np.where(df["ratedescription"].str.contains("1 Full"), "Double",
                            np.where(df["ratedescription"].str.contains("1 double"), "Double",
                            np.where(df["ratedescription"].str.contains("1 Double"), "Double",
                            np.where(df["ratedescription"].str.contains("2 twin"), "Twin Twin",
                            np.where(df["ratedescription"].str.contains("2 Twin"), "Twin Twin",
                            np.where(df["ratedescription"].str.contains("2 single"), "Twin Twin",
                            np.where(df["ratedescription"].str.contains("2 Single"), "Twin Twin",
                            np.where(df["ratedescription"].str.contains("2 Large Single"), "Twin Twin",
                            np.where(df["ratedescription"].str.contains("1 twin"), "Twin",
                            np.where(df["ratedescription"].str.contains("1 Twin"), "Twin",
                            np.where(df["ratedescription"].str.contains("4 bunk"), "Bunk Bunk Bunk Bunk",
                            np.where(df["ratedescription"].str.contains("4 Bunk"), "Bunk Bunk Bunk Bunk",
                            "Other")))))))))))))))))))))))))))))
    df_export = df[["websitecode", "hotelcode", "ratedate", "roomtype", "onsiterate", "status_code", "ratedescription", "taxtype", "sourceurl"]]

    with open("export_ai.csv","w") as f:
        df_export.to_csv(f)
    with open("export_ai.csv") as f:
        st.download_button(
            label="Download Parsed Rack Rates File", 
            data=f, 
            file_name=export_filename,
            mime="text/csv"
        )
