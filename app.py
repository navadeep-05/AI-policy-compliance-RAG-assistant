import streamlit as st 

# Configure the main Streamlit application
st.set_page_config(
    page_title="AI Policy Compliance Assistant",
    page_icon="📋",
    layout="wide"
)


# Define the application pages
app_page = st.Page(
    "app_page.py",
    title="App",
    icon="🏠"
)

about_page = st.Page(
    "about.py",
    title="About",
    icon="ℹ️"
)


# Create the application navigation
pg = st.navigation(
    {
        "Dashboard": [app_page, about_page]
    }
)

# Run the selected page
pg.run()