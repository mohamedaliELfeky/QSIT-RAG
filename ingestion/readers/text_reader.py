from typing import Union
from pathlib import Path
from data.base_models.text_document import TextFileDocument

from .base_reader import BaseFileReader


class TextReader(BaseFileReader):

    def read(self, txt_path:Union[Path, str])-> TextFileDocument:
        content = None
        with open(txt_path, 'r') as file:
            content = file.read()

        return TextFileDocument(
            source_name=Path(txt_path).name,
            source_path=Path(txt_path),
            content=content
        )
