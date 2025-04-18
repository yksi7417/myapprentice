import streamlit as st
from streamlit.navigation.page import StreamlitPage
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    st.set_page_config(
        layout="wide",
        initial_sidebar_state="expanded"
    )

    page_dir = "./pages"
    pages: list[StreamlitPage] = [
        st.Page(f"{page_dir}/introduction.py", title="Introduction", icon="🏠"),
    ]
    pages.append(st.Page(f"{page_dir}/acknowledgement.py", title="Acknowledgement", icon="📝"))
    pg = st.navigation(pages, position="sidebar", expanded=len(pages) > 1)
    pg.run()
