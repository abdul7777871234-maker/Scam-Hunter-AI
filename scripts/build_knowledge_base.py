
from config.settings import Settings
from rag.ingestion import KnowledgeBase

if __name__ == "__main__":
    settings = Settings.from_runtime()
    kb = KnowledgeBase(settings)
    result = kb.build()
    print("Knowledge base updated:")
    for key, value in result.items():
        print(f"  {key}: {value}")
