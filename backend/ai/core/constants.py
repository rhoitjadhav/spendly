from enum import StrEnum


class ModelProvider(StrEnum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE_GENAI = "google_genai"
    GROQ = "groq"
    MISTRAL = "mistralai"
    OLLAMA = "ollama"
