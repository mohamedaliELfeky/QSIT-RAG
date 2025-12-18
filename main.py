import json
from data_classes.config.rag import RAGConfiguration
from utils.configuration_reader.collection_reader import CollectionReader
from utils.configuration_reader.file_reader import FileReader


json_content = None

with open("./config.json", 'r') as file:
    json_content = json.load(file)


rag_config = RAGConfiguration(**json_content)
        



# print(rag_config.collections)
file_reader = FileReader()
res = CollectionReader(file_reader).process_collection(rag_config.collections[0])

print(res)