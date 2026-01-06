import logging
import uuid
import re
from typing import List, Dict, Any

from chunkwise import Chunker as CWChunker
from chunkwise.chunk import Chunk as CWChunk
from chunkwise.config import ChunkConfig as CWChunkConfig

from data.base_model.base_models import BaseDocument
from data.base_model.chunk import Chunk as QSITChunk
from data.config.chunking_strategy import ChunkingStrategy

logger = logging.getLogger(__name__)


class ChunkingProcessor:
    """
    Wrapper around the ChunkWise library to integrate it with QSIT-RAG.
    """

    def __init__(self, strategy_config:ChunkingStrategy):
        self.config = strategy_config
        self.chunker = self._intialize_chunker()


    def _intialize_chunker(self) -> CWChunker:
        cw_config = CWChunkConfig(
            strategy=self.config.class_.value,
            **self.config.default_params
        )

        logger.info(f"Intialized ChunkWise with strategy: {self.config.class_.value}")

        return CWChunker(cw_config)
    

    def process(self, documents:List[BaseDocument]) -> List[QSITChunk]:

        all_chunks:List[QSITChunk] = []

        logger.info(f"Chunking {len(documents)} Documents...")

        for doc in documents:

            if not hasattr(doc, 'content') or not doc.content:
                logger.warning(f"Document {doc.id} ({doc.source_name}) has no content. Skipping.")
                continue

            try:
                cw_chunks:List[CWChunk] = self.chunker.chunk(text=doc.content)
            except Exception as e:
                logger.error(f"Faild to chunk document {doc.source_name}: {e}")
                continue

            for cw_chunk in cw_chunks:
                chunk_id = str(uuid.uuid4)

                merged_metadata = doc.metadata.copy()
                merged_metadata.update(cw_chunk.metadata)


                merged_metadata['start_char'] = cw_chunk.start_char
                merged_metadata['end_char'] = cw_chunk.end_char

                qsit_chunk = QSITChunk(
                    id=chunk_id,
                    document_id=doc.id,
                    content=cw_chunk.content,
                    index=cw_chunk.index,
                    metadata=merged_metadata
                )

                all_chunks.append(qsit_chunk)

        logger.info(f"Generated {len(all_chunks)} chunks.")

        return all_chunks

        
