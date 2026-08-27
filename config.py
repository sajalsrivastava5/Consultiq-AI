"""
config.py
---------
Central configuration for ConsultIQ AI.

Every tunable in the platform (model choice, chunking, thresholds, provider
credentials) is read from environment variables so the app can move between
dev / staging / prod without code changes. See .env.example for the full list.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "sample_data"
INDEX_DIR = BASE_DIR / "storage" / "faiss_index"
DB_PATH = BASE_DIR / "storage" / "consultiq.db"
LOG_DIR = BASE_DIR / "logs"

INDEX_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

LLMProvider = Literal["openai", "azure_openai", "ollama", "demo"]


def _bool(name: str, default: bool) -> bool:
    val = os.getenv(name)
    return default if val is None else val.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    # --- App ---
    app_name: str = "ConsultIQ AI"
    environment: str = os.getenv("APP_ENV", "development")
    debug: bool = _bool("APP_DEBUG", True)

    # --- LLM provider (configurable per Tech Stack requirement) ---
    llm_provider: LLMProvider = os.getenv("LLM_PROVIDER", "demo")  # type: ignore[assignment]
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    azure_openai_api_key: str = os.getenv("AZURE_OPENAI_API_KEY", "")
    azure_openai_endpoint: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    azure_openai_deployment: str = os.getenv("AZURE_OPENAI_DEPLOYMENT", "")
    azure_openai_api_version: str = os.getenv("AZURE_OPENAI_API_VERSION", "2024-06-01")

    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.1")

    # --- Embeddings ---
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    embedding_dim_fallback: int = int(os.getenv("EMBEDDING_DIM_FALLBACK", "2048"))

    # --- Chunking ---
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "800"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "120"))

    # --- Retrieval ---
    top_k: int = int(os.getenv("TOP_K", "5"))
    similarity_threshold: float = float(os.getenv("SIMILARITY_THRESHOLD", "0.25"))

    # --- Security ---
    max_upload_mb: int = int(os.getenv("MAX_UPLOAD_MB", "25"))
    allowed_extensions: tuple[str, ...] = field(
        default_factory=lambda: (".pdf", ".docx", ".pptx", ".xlsx", ".txt")
    )

    # --- Auth (demo-grade; swap for SSO/OAuth in production) ---
    session_timeout_minutes: int = int(os.getenv("SESSION_TIMEOUT_MINUTES", "60"))


settings = Settings()
