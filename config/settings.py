"""Configuration management for Document Generator."""

import os
from pathlib import Path
#from pydantic import BaseSettings
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()  # Load environment variables from .env file


class Settings(BaseSettings):
    """Application settings."""

    # OpenAI Configuration
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "openai/gpt-4.1-nano")

    # OpenRouter Configuration
    openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY", "")
    openrouter_model: str = os.getenv("OPENROUTER_MODEL", "liquid/lfm-2.5-1.2b-thinking:free")

    # Application Settings
    upload_dir: str = os.getenv("UPLOAD_DIR", "uploads")
    output_dir: str = os.getenv("OUTPUT_DIR", "outputs")
    prompt_dir: str = os.getenv("PROMPT_DIR", "prompts")
    templates_dir: str = os.getenv("TEMPLATES_DIR", "templates")
    output_filename: str = os.getenv("OUTPUT_FILENAME", "generated_doc.docx")

    # File limits
    max_file_size: int = int(os.getenv("MAX_FILE_SIZE", "10"))  # MB

    @property
    def upload_path(self) -> Path:
        """Get upload directory path."""
        return Path(self.upload_dir)

    @property
    def output_path(self) -> Path:
        """Get output directory path."""
        return Path(self.output_dir)

    @property
    def templates_path(self) -> Path:
        """Get templates directory path."""
        return Path(self.templates_dir)
    
    @property
    def prompts_path(self) -> Path:
        """Get prompts directory path."""
        return Path(self.prompt_dir)

    class Config:
        """Pydantic config."""

        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()