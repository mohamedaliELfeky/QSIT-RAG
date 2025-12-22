

from ingestion.collection_loader import CollectionLoader
from ingestion.readers.file_reader import FileReader
from ingestion.sources.file_source import FileSourceReader
from ingestion.sources.folder_source import FolderSourceReader

from data.config.collection_config import CollectionConfig


if __name__ == "__main__":
    file_reader = FileReader()

    source_readers = {
        "file": FileSourceReader(file_reader),
        "folder": FolderSourceReader(file_reader),
    }

    loader = CollectionLoader(source_readers)


# B. The JSON Configuration (from your prompt)
    collection_json = {
    "name": "documents",
    "description": "General documents collection",
    "data_sources": [
        {
            "type": "folder",
            "path": "./data/documents",
            "recursive": True,
            "file_patterns": ["*.pdf", "*.txt"],
            "exclude_patterns": ["*draft*"]
        },
        {
            "type": "file",
            "path": r"D:\Projects and POCs\RAG for everyone\qsit_rag\anything.txt"
        }
    ],
    "chunking_strategy": {
        "class": "SemanticChunker",
        "default_params": {
            "breakpoint_threshold": 0.7,
            "max_chunk_size": 1000,
            "min_chunk_size": 100,
            "buffer_size": 1
        }
    },
    "metadata_schema": {
        "source": "string",
        "category": "string",
        "date_created": "datetime",
        "author": "string",
        "tags": "array"
    }
  }



    documents = loader.from_json(collection_json)

    print(f"Ingested {documents.size} documents")
    
    # D. Output
    for doc in documents.documents:
        print(f"- {doc.get('filename')} (Source: {doc.get('source_type')})")
        print(doc.get("content"))