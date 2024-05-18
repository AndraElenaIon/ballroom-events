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
            xml_tree = etree.parse(uploaded_file_xml)
            xml_root = xml_tree.getroot()

            # Inițializarea unui container pentru a stoca datele extrase
            extracted_data = []

            # Parcurgerea fiecărui element 'event' și extragerea datelor
            for event in xml_root.findall('event'):
                event_id = event.get('id')
                date = event.find('date').text
                start_time = event.find('.//start_time').text
                duration = event.find('.//duration').text
                participant_number = event.find('.//participant_number').text
                arrangement = event.find('.//arrangement').text
                organizer_name = event.find('.//organizer').text
                organizer_email = event.find('.//organizer').get('email')
                client_name = event.find('.//client').text
                client_email = event.find('.//client').get('email')
                hall = event.find('.//hall').text
                max_capacity = event.find('.//max_capacity').text
                suppliers = [supplier.get('name') for supplier in event.findall('.//supplier')]

                # Adăugarea datelor extrase în container
                extracted_data.append({
                    "Event ID": event_id,
                    "Date": date,
                    "Start Time": start_time,
                    "Duration": duration,
                    "Participants": participant_number,
                    "Arrangement": arrangement,
                    "Organizer Name": organizer_name,
                    "Organizer Email": organizer_email,
                    "Client Name": client_name,
                    "Client Email": client_email,
                    "Hall": hall,
                    "Max Capacity": max_capacity,
                    "Suppliers": ", ".join(suppliers)
                })
            # Aplicarea transformării XSLT pentru afișarea întregului document XML
            xsl_path = os.path.join(os.path.dirname(__file__), 'ProiectIonElenaAndra.xsl')
            xsl_tree = etree.parse(xsl_path)
            transform = etree.XSLT(xsl_tree)
            result_tree = transform(xml_tree)
            st.markdown(str(result_tree), unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error processing XML: {e}")

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