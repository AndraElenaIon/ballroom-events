from lxml import etree
import streamlit as st
import os
import pandas as pd
import json



st.title('Ballroom Events')

tab1, tab2 = st.tabs(["XML", "JSON"])

with tab1:
    st.header("Load XML & see report")

    uploaded_file_xml = st.file_uploader("Choose XML file", type=['xml'], key='xml')

    if uploaded_file_xml is not None:
        try:
            xml_root = etree.parse(uploaded_file_xml)

            xsl_path = os.path.join(os.path.dirname(__file__), 'event_management.xsl')
            xsl_root = etree.parse(xsl_path)
            transform = etree.XSLT(xsl_root)
            result_tree = transform(xml_root)
            st.markdown(str(result_tree), unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Eroare la transformarea XML: {e}")

with tab2:
    st.header("Load JSON & see report")

    uploaded_file_json = st.file_uploader("Alege un fișier JSON", type=['json'], key='json2')

    if uploaded_file_json is not None:

        json_content = json.load(uploaded_file_json)

        events = json_content.get("event_management", {}).get("event", [])

        data_for_table = []
        for event in events:

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

        df = pd.DataFrame(data_for_table)


        st.dataframe(df, width=2000)