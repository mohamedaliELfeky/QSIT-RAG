import logging
from typing import List

from data.config.rag_config import RAGConfiguration
from ingestion.collection_loader import CollectionLoader
from ingestion.readers.file_reader import FileReader
from ingestion.sources.file_source import FileSourceReader
from ingestion.sources.folder_source import FolderSourceReader
from ingestion.preprocessors.chunking.chunking_processor import ChunkingProcessor

from embedding.embedding_factory import EmbeddingFactory
from vector_db.vector_factory import VectorDBFactory


logger = logging.getLogger(__name__)


class IndexingPipeline:
    """
    Pipeline responsible for the offline process:
    1. Loading documents from configured sources.
    2. Chunking them based on the strategy.
    3. Generating embeddings.
    4. Indexing them into the Vector Database.
    """

    def __init__(self, config:RAGConfiguration):
        self.config = config


        self.file_reader = FileReader()

        self.source_readers = {
            "file": FileSourceReader(self.file_reader),
            "folder": FolderSourceReader(self.file_reader)
        }

        self.loader = CollectionLoader(self.source_readers)

        self.vector_db = VectorDBFactory.create_vector_db(self.config.database)

        self.embedder = EmbeddingFactory.get_dense_model(self.config.embedding)


    def run(self):
        total_chunks = 0

        logger.info("Starting Indexing Pipeline")

        for collection_cfg in self.config.collections:

            logger.info(f"--- processing {collection_cfg.name} ---")

            collection = self.loader.process_collection(collection_cfg)

            if not collection.documents:
                logger.warning(f"No documents found for collection {collection.name}. Skipping.")
                continue

            chunker = ChunkingProcessor(collection_cfg.chunking_strategy)
            chunks = chunker.process(collection.documents)

            if not chunks:
                logger.warning(f"No Chunks generated for the collection '{collection.name}")
                continue

            logger.info(f"Generating embedding for {len(chunks)} chunks..")

            texts = [chunk.content for chunk in chunks]

            try:
                vectors = self.embedder.embed_batch(texts=texts)

            except Exception as e:
                logger.error(f"Embdding failed for collection {collection.name}: {e}")
                continue

            vector_size = self.config.embedding.dimensions
            
            self.vector_db.create_collection(
                collection_name=collection.name,
                vector_size=vector_size
            )

            # Insert into DB
            ids = [chunk.id for chunk in chunks]
            metadata = [chunk.metadata for chunk in chunks]
            
            logger.info(f"Inserting {len(vectors)} vectors into {self.config.database.provider}...")
            self.vector_db.insert(
                collection_name=collection.name,
                vectors=vectors,
                metadata=metadata,
                ids=ids
            )
            
            total_chunks += len(chunks)
            logger.info(f"✅ Collection '{collection.name}' indexed successfully.")

        logger.info(f"🏁 Pipeline Finished. Total Chunks Indexed: {total_chunks}")
