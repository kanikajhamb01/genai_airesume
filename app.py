import streamlit as st

# Set default page
if "page" not in st.session_state:
    st.session_state["page"] = "landing"

# Page routing
from main import landing_page, builder_page, thank_you_page

if st.session_state["page"] == "landing":
    landing_page()
elif st.session_state["page"] == "builder":
    builder_page()
elif st.session_state["page"] == "thankyou":
    thank_you_page()
