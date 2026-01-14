from enum import Enum

class IntrinsicMetadataType(str, Enum):
    """
    Standard keys for metadata extracted natively by the system.
    """
    # File System Stats
    FILE_NAME = "file_name"
    FILE_SIZE = "file_size_bytes"
    FILE_EXTENSION = "file_extension"
    CREATION_DATE = "creation_date"
    LAST_MODIFIED = "last_modified"
    
    # System Capabilities
    REGEX_MATCH = "regex_match"