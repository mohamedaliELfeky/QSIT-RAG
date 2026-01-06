from typing import List
from chunkwise import Chunker as CWChunker
from chunkwise.chunk import Chunk as CWChunk
from chunkwise.config import Strategy as CWStrategy


from data.base_model.base_models import BaseDocument
from data.base_model.chunk import Chunk as QSITChunk
from data.config.chunking_strategy import ChunkingStrategy


class ChunkingProcessor:
    """
    Wrapper around the ChunkWise library to integrate it with QSIT-RAG.
    """



    def __init__(self, strategy_config:ChunkingStrategy):
        self.config = strategy_config