from lxml import etree
import streamlit as st
import os
import pandas as pd
import json
from io import BytesIO

# Titlul aplicației
st.title('Ballroom Events')

# Crearea taburilor
tab1, tab2 = st.tabs(["XML", "JSON"])

# Tabul pentru XML
with tab1:
    st.header("Încărcare și afișare fișier XML")

    uploaded_file_xml = st.file_uploader("Alege un fișier XML", type=['xml'], key='xml')

    if uploaded_file_xml is not None:
        # Procesează și afișează XML
        st.subheader("Conținutul XML transformă:")

        try:
            xml_root = etree.parse(uploaded_file_xml)
            # Presupunem că fișierul XSL este în același director cu scriptul
            xsl_path = os.path.join(os.path.dirname(__file__), 'event_management.xsl')
            xsl_root = etree.parse(xsl_path)
            transform = etree.XSLT(xsl_root)
            result_tree = transform(xml_root)
            st.markdown(str(result_tree), unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Eroare la transformarea XML: {e}")

with tab2:
    st.header("Încărcare și afișare fișier JSON")

    uploaded_file_json = st.file_uploader("Alege un fișier JSON", type=['json'], key='json2')

    if uploaded_file_json is not None:
        # Parsarea conținutului JSON
        json_content = json.load(uploaded_file_json)

        # Extragerea listei de evenimente din JSON
        events = json_content.get("event_management", {}).get("event", [])

        # Crearea unei liste pentru a stoca datele procesate
        data_for_table = []
        for event in events:
            # Extragerea detaliilor fiecărui eveniment
            organizer = event.get("details", {}).get("organizer", {})
            client = event.get("details", {}).get("client", {})
            suppliers_list = event.get("suppliers", {}).get("supplier", [])
            suppliers_names = ', '.join([supplier.get("name", "") for supplier in suppliers_list])

            row = {
                "ID": event.get("id", ""),
                "Date": event.get("date", ""),
                "Start Time": event.get("time", {}).get("start_time", ""),
                "Duration": event.get("time", {}).get("duration", ""),
                "Participants": event.get("details", {}).get("participant_number", ""),
                "Arrangement": event.get("details", {}).get("arrangement", ""),
                "Organizer Name": organizer.get("name", ""),
                "Organizer Email": organizer.get("email", ""),
                "Client Name": client.get("name", ""),
                "Client Email": client.get("email", ""),
                "Hall": event.get("location", {}).get("hall", ""),
                "Max Capacity": event.get("location", {}).get("max_capacity", ""),
                "Suppliers": suppliers_names
            }
            data_for_table.append(row)

        # Convertirea listei de date într-un DataFrame pentru afișare
        df = pd.DataFrame(data_for_table)
        st.table(df)