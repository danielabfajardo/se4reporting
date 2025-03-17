# import streamlit as st
# import pandas as pd
# import requests
# import xml.etree.ElementTree as ET
# from datetime import datetime

# # --- Authentication (Simple RBAC Mock) ---
# USERS = {"admin": "admin123", "user": "user123"}
# ROLES = {"admin": "full_access", "user": "read_only"}

# def authenticate():
#     username = st.text_input("Username")
#     password = st.text_input("Password", type="password")
#     if st.button("Login"):
#         if username in USERS and USERS[username] == password:
#             st.session_state["authenticated"] = True
#             st.session_state["role"] = ROLES[username]
#         else:
#             st.error("Invalid credentials")

# def check_authentication():
#     if "authenticated" not in st.session_state:
#         authenticate()
#         return False
#     return True

# if not check_authentication():
#     st.stop()

# # --- Sustainability Standards Selection ---
# STANDARDS = {"EUDR": ["CO2 Emissions", "Energy Usage", "Water Consumption"],
#              "CSDR": ["GHG Emissions", "Sustainable Materials"],
#              "Scope 3": ["Logistics Emissions", "Waste Management"]}

# st.sidebar.title("Select Sustainability Standard")
# selected_standard = st.sidebar.selectbox("Choose a standard:", list(STANDARDS.keys()))
# required_fields = STANDARDS[selected_standard]

# # --- Upload Invoice ---
# st.title("Supply Chain Sustainability Tracker")
# uploaded_file = st.file_uploader("Upload Invoice (CSV/Excel)", type=["csv", "xlsx"])

# def process_invoice(file):
#     if file.name.endswith(".csv"):
#         return pd.read_csv(file)
#     else:
#         return pd.read_excel(file)

# if uploaded_file:
#     invoice_data = process_invoice(uploaded_file)
#     st.write("### Invoice Preview:")
#     st.dataframe(invoice_data)

# # --- Fetch Sustainability Data (Mock API Call) ---
# def fetch_sustainability_data():
#     return {"CO2 Emissions": "12.5 kg", "Energy Usage": "100 kWh", "Water Consumption": "50 L"}

# if st.button("Fetch Sustainability Data"):
#     sustainability_data = fetch_sustainability_data()
#     st.write("### Retrieved Sustainability Data:")
#     st.json(sustainability_data)

# # --- Generate Finvoice XML ---
# def generate_finvoice_xml(data, sustainability_data):
#     root = ET.Element("Finvoice")
#     invoice = ET.SubElement(root, "Invoice")
#     for col in data.columns:
#         ET.SubElement(invoice, col).text = str(data[col].iloc[0])
#     sustainability = ET.SubElement(invoice, "SustainabilityData")
#     for key, value in sustainability_data.items():
#         ET.SubElement(sustainability, key).text = value
#     return ET.tostring(root, encoding='unicode')

# if st.button("Generate Finvoice XML"):
#     if uploaded_file:
#         finvoice_xml = generate_finvoice_xml(invoice_data, fetch_sustainability_data())
#         st.code(finvoice_xml, language='xml')
#     else:
#         st.error("Please upload an invoice first.")

# # --- Versioning System (Delta-based) ---
# VERSION_HISTORY = []

# def save_version(data):
#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     delta = {"timestamp": timestamp, "data": data}
#     VERSION_HISTORY.append(delta)

# if st.button("Save Version"):
#     if uploaded_file:
#         save_version(fetch_sustainability_data())
#         st.success("Version saved!")
#     else:
#         st.error("No data to save.")

# if st.button("Show Version History"):
#     st.write(VERSION_HISTORY)

# # --- Dashboard Visualization ---
# st.title("Sustainability Dashboard")
# if len(VERSION_HISTORY) > 0:
#     df = pd.DataFrame(VERSION_HISTORY)
#     st.line_chart(df.set_index("timestamp"))
import streamlit as st
import pandas as pd
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

# --- Authentication (Simple RBAC Mock) ---
USERS = {"admin": "admin123", "user": "user123"}
ROLES = {"admin": "full_access", "user": "read_only"}

def authenticate():
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in USERS and USERS[username] == password:
            st.session_state["authenticated"] = True
            st.session_state["role"] = ROLES[username]
        else:
            st.error("Invalid credentials")

def check_authentication():
    if "authenticated" not in st.session_state:
        authenticate()
        return False
    return True

if not check_authentication():
    st.stop()

# --- Logout Button ---
if st.button("Logout"):
    st.session_state["authenticated"] = False
    st.experimental_rerun()

# --- Sustainability Standards Selection ---
STANDARDS = {"EUDR": ["Scope 1 Emissions", "Scope 2 Emissions", "Scope 3 Emissions", "Energy Usage", "Water Consumption"],
             "CSDR": ["GHG Emissions", "Sustainable Materials"],
             "Scope 3": ["Logistics Emissions", "Waste Management"]}

st.sidebar.title("Select Sustainability Standard")
selected_standard = st.sidebar.selectbox("Choose a standard:", list(STANDARDS.keys()))
required_fields = STANDARDS[selected_standard]

# --- Upload Invoice ---
st.title("Supply Chain Sustainability Tracker")
st.write("### Step 1: Upload an Invoice or Enter Previous Finvoice URL")
uploaded_file = st.file_uploader("Upload Invoice", type=["json", "csv", "xlsx", "xml"])
previous_finvoice_url = st.text_input("Enter Previous Finvoice URL (if applicable)")

def process_invoice(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    else:
        return pd.read_excel(file)

if uploaded_file:
    invoice_data = process_invoice(uploaded_file)
    st.write("### Invoice Preview:")
    st.dataframe(invoice_data)

# --- Fetch Sustainability Data (Mock API Call) ---
st.write("### Step 2: Fetch or Enter Sustainability Data")
def fetch_sustainability_data():
    return {"Scope 1 Emissions": "10 kg", "Scope 2 Emissions": "15 kg", "Scope 3 Emissions": "5 kg", "Energy Usage": "100 kWh", "Water Consumption": "50 L"}

sustainability_data = fetch_sustainability_data()
user_sustainability_data = {}
st.write("Fill in Sustainability Data (Auto-Filled from API Where Available):")
for field in required_fields:
    user_sustainability_data[field] = st.text_input(field, sustainability_data.get(field, ""))

# --- Add Multiple Products ---
st.write("### Step 3: Add Products with Sustainability Data")
products = []
if "products" not in st.session_state:
    st.session_state["products"] = []

def add_product():
    product_data = {}
    for field in required_fields:
        product_data[field] = st.text_input(f"Product {len(st.session_state['products']) + 1} - {field}", key=f"{field}_{len(st.session_state['products'])}")
    st.session_state["products"].append(product_data)

if st.button("Add Product"):
    add_product()

for i, product in enumerate(st.session_state["products"]):
    st.write(f"### Product {i + 1}")
    for key, value in product.items():
        st.write(f"{key}: {value}")

# --- Generate Finvoice XML ---
st.write("### Step 4: Generate Finvoice XML with Embedded Sustainability Data")
def generate_finvoice_xml(data, sustainability_data, old_url):
    root = ET.Element("Finvoice")
    invoice = ET.SubElement(root, "Invoice")
    if old_url:
        ET.SubElement(invoice, "PreviousSustainabilityURL").text = old_url
    for col in data.columns:
        ET.SubElement(invoice, col).text = str(data[col].iloc[0])
    sustainability = ET.SubElement(invoice, "SustainabilityData")
    for key, value in sustainability_data.items():
        ET.SubElement(sustainability, key).text = value
    new_url = "https://sustainability.example.com/data/" + datetime.now().strftime("%Y%m%d%H%M%S")
    ET.SubElement(invoice, "NewSustainabilityURL").text = new_url
    return ET.tostring(root, encoding='unicode'), new_url

if st.button("Generate Finvoice XML"):
    if uploaded_file:
        finvoice_xml, new_url = generate_finvoice_xml(invoice_data, user_sustainability_data, previous_finvoice_url)
        st.code(finvoice_xml, language='xml')
        st.write("### New Sustainability Data URL:")
        st.write(new_url)
    else:
        st.error("Please upload an invoice first.")

# --- Versioning System (Delta-based) ---
st.write("### Step 5: Save Version and Track Changes")
VERSION_HISTORY = []

def save_version(data):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    delta = {"timestamp": timestamp, "data": data}
    VERSION_HISTORY.append(delta)

if st.button("Save Version"):
    if uploaded_file:
        save_version(user_sustainability_data)
        st.success("Version saved!")
    else:
        st.error("No data to save.")

if st.button("Show Version History"):
    st.write(VERSION_HISTORY)

# --- Dashboard Visualization ---
st.write("### Step 6: View Sustainability Dashboard")
if len(VERSION_HISTORY) > 0:
    df = pd.DataFrame(VERSION_HISTORY)
    st.line_chart(df.set_index("timestamp"))

# --- UI Enhancements ---
st.markdown("""
    <style>
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 24px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 8px;
        }
        .stTextInput>div>div>input {
            border: 2px solid #4CAF50;
            border-radius: 4px;
        }
        .stSidebar>div {
            background-color: #f0f0f0;
            padding: 10px;
            border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)