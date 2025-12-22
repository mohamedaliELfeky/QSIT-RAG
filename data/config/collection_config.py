from pydantic import BaseModel, Field
from typing import List, Dict, Any

from .data_sources_config import DataSourceConfig

from enum import Enum

class Strategy(str, Enum):
    # === Basic Strategies ===
    CHARACTER = "CharacterChunker"
    TOKEN = "TokenChunker"
    WORD = "WordChunker"
    SENTENCE = "SentenceChunker"
    MULTI_SENTENCE = "MultiSentenceChunker"
    PARAGRAPH = "ParagraphChunker"
    RECURSIVE = "RecursiveChunker"
    SLIDING_WINDOW = "SlidingWindowChunker"

    # === Document Structure ===
    MARKDOWN = "MarkdownChunker"
    HTML = "HTMLChunker"
    CODE = "CodeChunker"

    # === Format-Specific ===
    JSON = "JSONChunker"
    LATEX = "LaTeXChunker"
    REGEX = "RegexChunker"

    # === Semantic & Embedding-Based ===
    SEMANTIC = "SemanticChunker"
    CLUSTER = "ClusterChunker"
    LATE = "LateChunker"

    # === LLM-Based ===
    AGENTIC = "AgenticChunker"
    PROPOSITION = "PropositionChunker"
    DOCUMENT_SUMMARY = "DocumentSummaryChunker"
    KEYWORD_SUMMARY = "KeywordSummaryChunker"
    CONTEXTUAL = "ContextualChunker"
    CONTEXTUAL_BM25 = "ContextualBM25Chunker"

    # === Retrieval-Optimized ===
    SENTENCE_WINDOW = "SentenceWindowChunker"
    AUTO_MERGING = "AutoMergingChunker"
    PARENT_DOCUMENT = "ParentDocumentChunker"
    SMALL_TO_BIG = "SmallToBigChunker"
    BIG_TO_SMALL = "BigToSmallChunker"
    HIERARCHICAL = "HierarchicalChunker"

    # === Hybrid/Combined ===
    HYBRID = "HybridChunker"
    ADAPTIVE = "AdaptiveChunker"


class ChunkingStrategy(BaseModel):
    class_: Strategy = Field(alias="class") # 'class' is reserved in Python
    default_params: Dict[str, Any] = Field(default_factory=dict)


class CollectionConfig(BaseModel):
    name: str
    description: str
    data_sources: List[DataSourceConfig]
    chunking_strategy: ChunkingStrategy
    metadata_schema: Dict[str, str]