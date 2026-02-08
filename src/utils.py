"""Utility functions for Document Generator."""

import os
from pathlib import Path

import yaml
from jinja2 import Template

from config.settings import settings


def ensure_directories_exist() -> None:
    """Ensure all required directories exist."""
    directories = [
        settings.upload_path,
        settings.output_path,
        settings.templates_path,
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


def validate_file_size(file_size_bytes: int) -> bool:
    """
    Validate if file size is within limit.

    Args:
        file_size_bytes: File size in bytes

    Returns:
        True if file size is valid
    """
    max_size_bytes = settings.max_file_size * 1024 * 1024
    return file_size_bytes <= max_size_bytes


def get_upload_file_path(filename: str) -> Path:
    """
    Get full path for uploaded file.

    Args:
        filename: Original filename

    Returns:
        Full path in uploads directory
    """
    return settings.upload_path / filename


def get_output_file_path(filename: str) -> Path:
    """
    Get full path for output file.

    Args:
        filename: Output filename

    Returns:
        Full path in outputs directory
    """
    return settings.output_path / filename


def cleanup_upload_file(filename: str) -> None:
    """
    Delete uploaded file after processing.

    Args:
        filename: Filename to delete
    """
    file_path = get_upload_file_path(filename)
    if file_path.exists():
        os.remove(file_path)


def prompt_parser(prompt_config_db, user_input):

    parsed_prompts_db = {}

    for prompt_name, prompt_config in prompt_config_db.items():

        # Extract sections
        role = prompt_config['prompt_config']['role'].strip()
        context = prompt_config['prompt_config']['context'].strip()
        fields = prompt_config['prompt_config']['extraction_fields'].strip()
        constraints = "\n".join([f"- {c}" for c in prompt_config['prompt_config']['constraints']])
        
        # Process the input template using Jinja2
        template_str = prompt_config['input_template']
        jinja_template = Template(template_str)
        rendered_input = jinja_template.render(input_text=user_input)

        # Assemble the final prompt
        final_prompt = f"""
            {role}

            {context}

            EXTRACTION TASKS:
            {fields}

            CONSTRAINTS:
            {constraints}

            {rendered_input}
        """

        parsed_prompts_db[prompt_name] = final_prompt.strip()  # Remove leading/trailing whitespace
    
    return parsed_prompts_db


def load_prompts(prompt_db_path: str) -> dict:

    # load prompt database
    prompt_db = {}

    # Loop through all the prompt files in the directory
    for filename in os.listdir(prompt_db_path):
        if filename.endswith(".yaml"):
            file_path = os.path.join(prompt_db_path, filename)
            with open(file_path, 'r') as file:
                config = yaml.safe_load(file)
                key = filename.rsplit('.', 1)[0]  # Use filename without extension as key
                prompt_db[key] = config

    return prompt_db