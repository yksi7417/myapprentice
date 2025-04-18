import streamlit as st
import os
from streamlit.navigation.page import StreamlitPage
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Disable Streamlit's watcher to prevent it from trying to reload the page
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"


if __name__ == "__main__":
    st.set_page_config(
        layout="wide",
        initial_sidebar_state="expanded"
    )

    page_dir = "./pages"
    pages: list[StreamlitPage] = [
        st.Page(f"{page_dir}/introduction.py", title="Introduction", icon="🏠"),
    ]
    pages.append(st.Page(f"{page_dir}/acknowledgement.py",
                         title="Acknowledgement", icon="📝"))
    pages.append(st.Page(f"{page_dir}/test_llm.py",
                         title="Test LLM", icon="🧪"))
    pg = st.navigation(pages, position="sidebar", expanded=len(pages) > 1)
    pg.run()
