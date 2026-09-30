
from __future__ import annotations
from pathlib import Path
import hashlib, json
import numpy as np
from rag.extraction import extract_document, clean_text
from rag.chunking import chunk_text
from rag.embeddings import Embedder
from rag.vector_store import VectorStore

SUPPORTED = {".pdf", ".docx", ".txt", ".md"}

class KnowledgeBase:
    def __init__(self, settings):
        self.settings = settings
        self.doc_dir = settings.data_dir / "documents"
        self.chunk_dir = settings.data_dir / "chunks"
        self.faiss_dir = settings.data_dir / "faiss"
        self.manifest_path = settings.data_dir / "manifest.json"
        self.chunks_path = settings.data_dir / "all_chunks.json"
        self.doc_dir.mkdir(parents=True, exist_ok=True)
        self.chunk_dir.mkdir(parents=True, exist_ok=True)
        self.manifest = self._load_manifest()
        self.all_chunks = self._load_chunks()
        self.embedder = None
        self.store = VectorStore(self.faiss_dir)

    def _load_manifest(self):
        if self.manifest_path.exists():
            return json.loads(self.manifest_path.read_text(encoding="utf-8"))
        return {}

    def _load_chunks(self):
        if self.chunks_path.exists():
            return json.loads(self.chunks_path.read_text(encoding="utf-8"))
        return []

    @staticmethod
    def sha256(path: Path) -> str:
        h = hashlib.sha256()
        with path.open("rb") as f:
            for block in iter(lambda: f.read(1024 * 1024), b""):
                h.update(block)
        return h.hexdigest()

    def _all_source_files(self):
        return [p for p in self.doc_dir.rglob("*") if p.is_file() and p.suffix.lower() in SUPPORTED]

    def _chunks_for_file(self, path: Path, digest: str) -> list[dict]:
        doc_id = digest[:16]
        chunks = []
        for page in extract_document(path):
            cleaned = clean_text(page["text"])
            for n, chunk in enumerate(
                chunk_text(cleaned, self.settings.chunk_size, self.settings.chunk_overlap)
            ):
                chunks.append({
                    "document_id": doc_id,
                    "filename": path.name,
                    "file_type": path.suffix.lower(),
                    "source_type": "knowledge_base",
                    "page": page.get("page", 1),
                    "section": page.get("section", ""),
                    "chunk_id": f"{doc_id}-{n:04d}",
                    "text": chunk,
                })
        return chunks

    def build(self) -> dict:
        files = self._all_source_files()
        current = {}
        changed = []
        removed_ids = set()

        for path in files:
            rel = str(path.relative_to(self.doc_dir))
            digest = self.sha256(path)
            doc_id = digest[:16]
            current[rel] = {"sha256": digest, "document_id": doc_id, "filename": path.name}
            old = self.manifest.get(rel)
            if not old or old.get("sha256") != digest:
                changed.append((rel, path, digest, doc_id))

        for rel, old in self.manifest.items():
            if rel not in current:
                removed_ids.add(old.get("document_id"))

        # Remove chunks belonging to deleted/changed documents.
        changed_ids = {doc_id for _, _, _, doc_id in changed}
        old_changed_ids = {
            self.manifest[rel]["document_id"]
            for rel, _, _, _ in changed
            if rel in self.manifest
        }
        drop_ids = removed_ids | old_changed_ids
        if drop_ids:
            self.all_chunks = [
                c for c in self.all_chunks if c.get("document_id") not in drop_ids
            ]

        # Only extract/chunk NEW or CHANGED source files.
        added_chunks = []
        for _, path, digest, _ in changed:
            added_chunks.extend(self._chunks_for_file(path, digest))
        self.all_chunks.extend(added_chunks)

        if changed or removed_ids or not self.store.count:
            texts = [c["text"] for c in self.all_chunks]
            if texts:
                if self.embedder is None:
                    self.embedder = Embedder(self.settings.embedding_model)
                vectors = self.embedder.encode(texts)
                self.store.replace(vectors, self.all_chunks)
            else:
                # Do not create a fake-dimension index. The empty state is represented
                # by absent/empty metadata until a real document is indexed.
                self.store.index = None
                self.store.metadata = []
                if self.store.index_path.exists():
                    self.store.index_path.unlink()
                self.store.meta_path.write_text("[]", encoding="utf-8")

        self.manifest = current
        self.manifest_path.write_text(
            json.dumps(current, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        self.chunks_path.write_text(
            json.dumps(self.all_chunks, indent=2, ensure_ascii=False), encoding="utf-8"
        )

        return {
            "documents": len(files),
            "chunks": len(self.all_chunks),
            "vectors": len(self.all_chunks),
            "changed_documents": len(changed),
            "removed_documents": len(removed_ids),
            "reembedded": bool(changed or removed_ids or not self.store.count),
        }

    def add_upload(self, source_path: str | Path) -> Path:
        source_path = Path(source_path)
        target = self.doc_dir / source_path.name
        target.write_bytes(source_path.read_bytes())
        return target
