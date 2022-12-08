import streamlit as st
import pandas as pd
import numpy as np
import json

st.title('Hotelbeds Booking Parser')

uploaded_file = st.file_uploader("Select json file to upload", type=["json"])

if uploaded_file is not None:
    # Read and unnest JSON file
    data = json.load(uploaded_file)
    df_bookings = pd.json_normalize(data, record_path=["bookings", "bookings"])
    df_pax = pd.json_normalize(data, record_path=["bookings", "bookings", "hotel", "rooms", "paxes"], 
                        meta=[["bookings", "bookings", "reference"], ["bookings", "bookings", "hotel", "rooms", "id"], ["bookings", "bookings", "hotel", "rooms", "code"]], 
                        errors="ignore")
    df_rate = pd.json_normalize(data, record_path=["bookings", "bookings", "hotel", "rooms", "rates"], 
                        meta=[["bookings", "bookings", "reference"], ["bookings", "bookings", "hotel", "rooms", "id"], ["bookings", "bookings", "hotel", "rooms", "code"]], 
                        errors="ignore")

    # Re-join unnested JSON files, combine into single dataframe
    df_pax["full_name"] = df_pax["name"] + " " + df_pax["surname"]
    df_pax_group = df_pax.groupby(["bookings.bookings.reference", "roomId"])["full_name"].apply(list).reset_index()
    df_pax_group = df_pax_group.rename(columns={"bookings.bookings.reference": "reference", "full_name": "guest_names"})
    df_rate_group = df_rate.groupby(["bookings.bookings.reference", "bookings.bookings.hotel.rooms.id", "bookings.bookings.hotel.rooms.code", "rooms"])["amount"].sum().reset_index()
    df_rate_group = df_rate_group.rename(columns={"bookings.bookings.reference": "reference", "bookings.bookings.hotel.rooms.id": "roomId", "bookings.bookings.hotel.rooms.code": "roomCode", "amount": "roomAmount"})
    df_bookings["holderFullname"] = df_bookings["holder.name"] + " " + df_bookings["holder.surname"]
    df_export = df_bookings[["hotel.code", "hotel.name", "hotel.checkIn", "hotel.checkOut", "holderFullname", "totalNet", "status", "creationUser", "reference", "clientReference"]]
    df_export = df_export.merge(df_pax_group, how="left", on="reference")
    df_export = df_export.merge(df_rate_group, how="left", on=["reference", "roomId"])

    with open('export.csv','w') as f:
        df_export.to_csv(f)
    with open('export.csv') as f:
        st.download_button(
            label='Download Parsed Bookings File', 
            data=f, 
            file_name='hotelbeds_bookings.csv',
            mime='text/csv'
        )