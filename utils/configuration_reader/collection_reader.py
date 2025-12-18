import os
from pathlib import Path
from typing import List, Dict, Any, Union
import logging


logger = logging.getLogger(__file__)


from data_classes.config.data_sources import DataSourceConfig, CollectionConfig
from .base_source_reader import BaseSourceReader
from .folder_reader import FolderSourceReader
from .file_reader import FileSourceReader, FileReader



class CollectionReader:
    def __init__(self, file_loader:BaseSourceReader):
        self.file_loader = file_loader
        
        self.source_readers = {
            "folder": FolderSourceReader(file_loader),
            "file": FileSourceReader(file_loader),
            # Easy to add "s3", "google_drive", "database" later
        }

    def process_collection(self, collection_config: CollectionConfig) -> List[Dict[str, Any]]:
        collection_name = collection_config.name
        print(f"=== Processing Collection: {collection_name} ===")
        
        all_documents = []

        # 1. Loop through Data Sources
        for source in collection_config.data_sources:
            
            # Convert JSON dict to Config Object
            cfg = DataSourceConfig(
                type=source.type,
                path=source.path,
                urls=source.urls,
                recursive=source.recursive,
                file_patterns=source.file_patterns,
                exclude_patterns=source.exclude_patterns,
                crawl_depth=source.crawl_depth
            )

            # 2. Get the correct reader
            reader = self.source_readers.get(cfg.type)
            
            if reader:
                # 3. Fetch data
                docs = reader.fetch(cfg)
                
                # 4. Inject Metadata (from the schema or source info)
                if cfg.type == "file":
                    docs = [docs]
                
                for doc in docs:
                    doc["source_type"] = cfg.type
                    doc["collection"] = collection_name
                    # Here you would apply the 'metadata_schema' validation logic
                
                all_documents.extend(docs)
            else:
                logger.warning(f"Warning: No reader found for source type '{cfg.type}'")

        return all_documents
    


if __name__ == "__main__":
    file_reader = FileReader()
    collection_reader = CollectionReader(file_reader)

    # B. The JSON Configuration (from your prompt)
    collection_json = {
      "name": "documents",
      "description": "General documents collection",
      "data_sources": [
        {
          "type": "folder",
          "path": "./data/documents", # Ensure this folder exists to test
          "recursive": True,
          "file_patterns": ["*.pdf", "*.txt"],
          "exclude_patterns": ["*draft*"]
        },
        {
          "type": "file",
          "path": r"D:\Projects and POCs\RAG for everyone\qsit_rag\anything.txt"
        }
      ]
    }

    # C. Run
    documents = collection_reader.process_collection(collection_json)
    
    # D. Output
    print(f"\nTotal Documents Ingested: {len(documents)}")
    for doc in documents:
        print(f"- {doc.get('filename')} (Source: {doc.get('source_type')})")
        print(doc.get("content"))