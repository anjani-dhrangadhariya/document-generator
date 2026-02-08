import os
import time
import logging
import tempfile
from pathlib import Path
import streamlit as st

# Backend imports
from src.document_handler import DocumentHandler
from src.pipeline import Extractor, Generator
from config.settings import settings

# --- 1. BOILERPLATE SETUP ---
def setup_logging():
    timestr = time.strftime("%Y%m%d-%H%M%S")
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        filename=f"logs/app_{timestr}.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger(__name__)

logger = setup_logging()

# --- 2. UI COMPONENTS ---
st.set_page_config(page_title="Factsheet Generator", layout="wide")
st.title("📄 Clinical Factsheet Generator")

with st.expander("ℹ️ About this application"):
    st.caption("This application generates a draft of clinical trial factsheets... "
               "It should be reviewed by a medical writer.")

# --- 3. CORE LOGIC ---
uploaded_file = st.file_uploader("Upload Clinical Trial Summary", type=["pdf", "docx", "txt"])

if uploaded_file:
    # Use a separator to clean up the UI
    st.divider()
    
    # Process file
    if 'extracted_text' not in st.session_state:
        logger.info(f"New upload: {uploaded_file.name}")
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp:
            tmp.write(uploaded_file.getbuffer())
            tmp_path = tmp.name
        
        st.session_state.extracted_text = DocumentHandler.extract_input_text(tmp_path).replace("\n", " ")
        st.success("File processed!")

    if st.button("🚀 Generate Factsheet"):
        try:
            # Extraction
            with st.spinner("Extracting information..."):
                extractor = Extractor()
                info = extractor.extraction(st.session_state.extracted_text, settings.prompts_path)
                logger.info("Extraction successful.")

            # Generation
            with st.spinner("Writing document..."):
                gen = Generator()
                out_path = settings.output_path / settings.output_filename
                gen.generate_factsheet(info, f"{settings.templates_path}/dummy_trial_factsheet_template.docx", str(out_path))
                logger.info("Generation successful.")
            st.success("✅ Factsheet Ready!")
            
            with open(out_path, "rb") as f:
                st.download_button("Download Factsheet", f, file_name=settings.output_filename)
                
        except Exception as e:
            logger.error(f"Pipeline Error: {e}", exc_info=True)
            st.error("An error occurred during generation.")