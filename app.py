import streamlit as st
from main import landing_page, builder_page, thank_you_page
from resume_generator import generate_resume

# ✅ Proper routing logic in one place
def main():
    if "page" not in st.session_state:
        st.session_state["page"] = "landing"

    # Debug sidebar (optional)
    # st.sidebar.markdown(f"**📄 Current Page:** `{st.session_state['page']}`")

    # Routing
    if st.session_state["page"] == "landing":
        landing_page()
    elif st.session_state["page"] == "builder":
        builder_page()
    elif st.session_state["page"] == "generate":
        generate_resume(st.session_state.generated_data)
        st.session_state["page"] = "thankyou"
        st.rerun()
    elif st.session_state["page"] == "thankyou":
        thank_you_page()

# ✅ Always call main (not __name__ check)
main()
