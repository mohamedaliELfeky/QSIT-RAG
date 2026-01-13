from pydantic import BaseModel
from typing import List

# --- 4. Preprocessing Config ---
class TextCleaningConfig(BaseModel):
    remove_html: bool
    remove_urls: bool
    remove_emails: bool
    normalize_whitespace: bool
    lowercase: bool
    remove_special_chars: bool

class PdfParsingConfig(BaseModel):
    extract_images: bool
    ocr_enabled: bool
    preserve_tables: bool

class HtmlParsingConfig(BaseModel):
    extract_main_content: bool
    remove_scripts: bool
    remove_styles: bool

class DocumentParsingConfig(BaseModel):
    pdf: PdfParsingConfig
    html: HtmlParsingConfig

class MetadataExtractorConfig(BaseModel):
    name: str
    pattern: str

class MetadataExtractionConfig(BaseModel):
    extract_titles: bool
    extract_dates: bool
    extract_authors: bool
    custom_extractors: List[MetadataExtractorConfig]

class PreprocessingConfig(BaseModel):
    text_cleaning: TextCleaningConfig
    document_parsing: DocumentParsingConfig
    metadata_extraction: MetadataExtractionConfig

