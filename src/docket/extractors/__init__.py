from docket.extractors.base import ExtractionResult, Extractor

__all__ = ["ExtractionResult", "Extractor", "get_extractor"]


def get_extractor(model: str, prompt_version: str = "extraction_v1") -> Extractor:
    """Return the extraction backend for a model name."""
    if model.startswith("claude-"):
        from docket.extractors.claude import ClaudeExtractor

        return ClaudeExtractor(model=model, prompt_version=prompt_version)
    raise ValueError(f"No extractor available for model {model!r}")
