from typing import Dict
import logging


logger = logging.getLogger(__file__)

from data.base_models.collection import Collection
from data.config.collection_config import CollectionConfig
from data.config.collection_config import ChunkingStrategy
from data.config.data_sources_config import DataSourceConfig

from .sources.folder_source import FolderSourceReader
from .sources.file_source import FileSourceReader
from .sources.base_source import BaseSourceReader

from ingestion.readers.file_reader import FileReader


class CollectionLoader:
    def __init__(self, source_readers: Dict[str, BaseSourceReader]):
        self.source_readers = source_readers

    def from_json(self, collection_json: dict) -> Collection:
        """
        Convert JSON into CollectionConfig (Pydantic) and load Collection.
        Automatically converts nested objects like ChunkingStrategy and DataSourceConfig.
        """
        # Convert chunking_strategy dict → ChunkingStrategy
        if "chunking_strategy" in collection_json and isinstance(collection_json["chunking_strategy"], dict):
            collection_json["chunking_strategy"] = ChunkingStrategy(**collection_json["chunking_strategy"])

        # Convert each data_source dict → DataSourceConfig
        data_sources = collection_json.get("data_sources", [])
        collection_json["data_sources"] = [
            DataSourceConfig(**ds) if isinstance(ds, dict) else ds for ds in data_sources
        ]

        # Convert JSON → CollectionConfig
        config = CollectionConfig(**collection_json)

        # Load the collection
        return self.process_collection(config)


    def process_collection(self, config: CollectionConfig) -> Collection:
        logger.info(f"Processing collection: {config.name}")

        collection = Collection(
            name=config.name,
            description=config.description,
            metadata_schema=config.metadata_schema,
            chunking_strategy=config.chunking_strategy,
        )

        for source_cfg in config.data_sources:
            reader = self.source_readers.get(source_cfg.type)

            if not reader:
                logger.warning(
                    f"No source reader registered for '{source_cfg.type}'"
                )
                continue

            documents = reader.fetch(source_cfg)

            for doc in documents:
                doc.metadata["collection_source_type"] = source_cfg.type

            collection.documents.extend(documents)

        logger.info(
            f"Collection '{collection.name}' loaded with {collection.size} documents"
        )

        return collection


if __name__ == "__main__":
    file_reader = FileReader()

    source_readers = {
        "file": FileSourceReader(file_reader),
        "folder": FolderSourceReader(file_reader),
    }

    loader = CollectionLoader(source_readers)

    collection_config = CollectionConfig.from_json("collection.json")
    documents = loader.process_collection(collection_config)

    print(f"Ingested {len(documents)} documents")
    
    # D. Output
    print(f"\nTotal Documents Ingested: {len(documents)}")
    for doc in documents:
        print(f"- {doc.get('filename')} (Source: {doc.get('source_type')})")
        print(doc.get("content"))