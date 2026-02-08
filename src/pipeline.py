"""LangChain LLM integration for document processing."""

import logging
import streamlit as st
from docxtpl import DocxTemplate
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

from config.settings import settings
from src.utils import load_prompts, prompt_parser

logger = logging.getLogger(__name__)


class Extractor:
    """Handles LLM operations using LangChain."""

    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=settings.openai_api_key,
            base_url="https://openrouter.ai/api/v1",
            model="openai/gpt-4.1-nano", #. openai/gpt-5-nano , openai/gpt-4.1-nano
            temperature=0,
            max_tokens=256,
        )

    def extract_information(self, document_text: str, instructions: str) -> str:
        """
        Extract relevant information from source document.

        Args:
            document_text: Raw text from the source document

        Returns:
            Dictionary with extracted information mapped to template fields
        """
        prompt = PromptTemplate.from_template(
            """
            {instructions}
            Please provide the extracted information.
            """
        )

        chain = prompt | self.llm
        result = chain.invoke({"instructions": instructions})
        return result.content
    
    def default_value(self) -> dict:
        return {
            "s1_study_design":"A two-part, randomized, double-blind, placebo-controlled study.",
            "s1_participant_bmi":"null",
            "s1_participant_age_range":"18 to 55",
            "s1_mode_drug_admin":"subcutaneous",
            "s0_study_title":"A Randomized, Double-Blind, Placebo-Controlled, First-in-Human, Phase I Study to Assess the Safety, Tolerability, and Pharmacokinetics of ZS98987 and DM68831 Following Subcutaneous Administration in Healthy Volunteers",
            "s1_study_phase":"Phase I"
        }
    

    def extraction(self, document_text: str, prompt_db_path: str) -> dict:
        """
        Extract information based on a prompt database.

        Args:
            document_text: Raw text from the source document
            prompt_db: Dictionary containing prompts for different fields

        Returns:
            Dictionary with extracted information mapped to template fields
        """

        # load prompt database
        prompt_db = load_prompts(prompt_db_path)

        # Parse and fill prompts
        prompts_parsed = prompt_parser(prompt_db, document_text)

        extracted_info = {}
        for field, prompt in prompts_parsed.items():
            extracted_unit = self.extract_information(document_text, prompt)
            #st.write(f"Extracted information for field '{field}': {extracted_unit}")
            logger.info(f"Extracting field: {field}")
            extracted_info[field] = extracted_unit
        #extracted_info = self.default_value()

        return extracted_info
    

class Generator:
    """Handles filling in the clinical trial factsheet template."""

    def generate_factsheet(self, extracted_info: dict, template_path: str, output_path: str) -> None:
        """Fills the DOCX template dynamically using the extracted dictionary."""
        try:
            doc = DocxTemplate(template_path)
            
            # Smart Mapping: Instead of hardcoding, we pass the whole dict.
            # Use .get() in the word template itself or handle defaults here.
            context = {k: (v if v and v.lower() != 'null' else 'N/A') 
                      for k, v in extracted_info.items()}

            doc.render(context)
            doc.save(output_path)
            logger.info(f"Factsheet saved successfully to {output_path}")
        except Exception as e:
            logger.error(f"Failed to generate docx: {e}")
            raise