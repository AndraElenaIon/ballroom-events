from lxml import etree
import streamlit as st
import os
from io import BytesIO

def get_xsl_path(xml_content):
    try:
        xml_root = etree.parse(BytesIO(xml_content))
        # Căutăm instrucțiunea de procesare pentru XSL
        for pi in xml_root.xpath("//processing-instruction('xml-stylesheet')"):
            pi_text = str(pi)
            if "href" in pi_text:
                start = pi_text.find('href="') + len('href="')
                end = pi_text.find('"', start)
                return pi_text[start:end]
    except Exception as e:
        st.error(f"Eroare la parsarea XML: {e}")
    return None

st.title('Ballroom events')

uploaded_file_xml = st.file_uploader("Alege un fișier XML", type=['xml'])

def transform_xml(xml_content, xsl_path):
    try:
        xml_root = etree.parse(BytesIO(xml_content))
        with open(xsl_path, 'rb') as xsl_file:
            xsl_root = etree.parse(xsl_file)
            transform = etree.XSLT(xsl_root)
            result_tree = transform(xml_root)
            return str(result_tree)
    except Exception as e:
        return f"Eroare la transformarea XSLT: {e}"

if uploaded_file_xml is not None:
    xsl_path = get_xsl_path(uploaded_file_xml.getvalue())
    if xsl_path:
        xsl_full_path = os.path.join(os.path.dirname(__file__), xsl_path)
        transformed_content = transform_xml(uploaded_file_xml.getvalue(), xsl_full_path)
        st.markdown(transformed_content, unsafe_allow_html=True)
    else:
        st.error("Nu s-a putut găsi referința XSL în fișierul XML.")
