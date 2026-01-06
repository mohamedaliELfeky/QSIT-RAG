from pydantic import BaseModel, Field
from typing import Dict, Any

from enum import Enum

from pydantic import BaseModel, Field
from typing import Dict, Any
from enum import Enum

class Strategy(str, Enum):
    # === Basic Strategies ===
    CHARACTER = "character"
    TOKEN = "token"
    WORD = "word"
    SENTENCE = "sentence"
    MULTI_SENTENCE = "multi_sentence"
    PARAGRAPH = "paragraph"
    RECURSIVE = "recursive"
    SLIDING_WINDOW = "sliding_window"

    # === Document Structure ===
    MARKDOWN = "markdown"
    HTML = "html"
    CODE = "code"

    # === Format-Specific ===
    JSON = "json"
    LATEX = "latex"
    REGEX = "regex"

    # === Semantic & Embedding-Based ===
    SEMANTIC = "semantic"
    CLUSTER = "cluster"
    LATE = "late"

    # === LLM-Based ===
    AGENTIC = "agentic"
    PROPOSITION = "proposition"
    DOCUMENT_SUMMARY = "document_summary"
    KEYWORD_SUMMARY = "keyword_summary"
    CONTEXTUAL = "contextual"
    CONTEXTUAL_BM25 = "contextual_bm25"

    # === Retrieval-Optimized ===
    SENTENCE_WINDOW = "sentence_window"
    AUTO_MERGING = "auto_merging"
    PARENT_DOCUMENT = "parent_document"
    SMALL_TO_BIG = "small_to_big"
    BIG_TO_SMALL = "big_to_small"
    HIERARCHICAL = "hierarchical"

    # === Hybrid/Combined ===
    HYBRID = "hybrid"
    ADAPTIVE = "adaptive"

class ChunkingStrategy(BaseModel):
    class_: Strategy = Field(alias="class") 
    default_params: Dict[str, Any] = Field(default_factory=dict)