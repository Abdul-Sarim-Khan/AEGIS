from __future__ import annotations
from __future__ import annotations
import glob,os,time
from dataclasses import dataclass,field
from typing import List
import faiss,numpy as np
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

KNOWLEDGE_BASE_DIR=os.path.join(os.path.dirname(__file__),'knowledge_base')
EMBED_MODEL_NAME='sentence-transformers/all-MiniLM-L6-v2'
CHUNK_SIZE=600;CHUNK_OVERLAP=100;DEFAULT_TOP_K=4

@dataclass
class Chunk:
    text:str
    source:str

@dataclass
class RetrievalResult:
    chunk:Chunk
    score:float

@dataclass
class RagEngine:
    model_name:str=EMBED_MODEL_NAME
    chunks:List[Chunk]=field(default_factory=list)
    _model:SentenceTransformer|None=field(default=None,repr=False)
    _index:faiss.Index|None=field(default=None,repr=False)
    build_seconds:float=0.0

    def load_knowledge_base(self,kb_dir:str=KNOWLEDGE_BASE_DIR)->List[Chunk]:
        splitter=RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE,chunk_overlap=CHUNK_OVERLAP,separators=["\n## ","\n### ","\n\n","\n",". "," ",""])
        chunks:List[Chunk]=[]
        md_paths=sorted(glob.glob(os.path.join(kb_dir,'*.md')))
        if not md_paths: raise FileNotFoundError(f"No .md files found in {kb_dir!r}")
        for path in md_paths:
            with open(path,'r',encoding='utf-8') as fh: content=fh.read()
            source=os.path.basename(path)
            for piece in splitter.split_text(content):
                piece=piece.strip()
                if piece: chunks.append(Chunk(text=piece,source=source))
        self.chunks=chunks;return chunks

    def _get_model(self)->SentenceTransformer:
        if self._model is None: self._model=SentenceTransformer(self.model_name)
        return self._model

    def encode_chunks(self,parallel:bool=False,batch_size:int=32)->np.ndarray:
        model=self._get_model();texts=[c.text for c in self.chunks]
        if parallel:
            pool=model.start_multi_process_pool()
            try:embeddings=model.encode_multi_process(texts,pool,batch_size=batch_size,normalize_embeddings=True)
            finally:model.stop_multi_process_pool(pool)
        else:embeddings=model.encode(texts,batch_size=batch_size,normalize_embeddings=True,show_progress_bar=False)
        return np.asarray(embeddings,dtype='float32')

    def build(self,parallel:bool=False)->'RagEngine':
        start=time.perf_counter()
        if not self.chunks: self.load_knowledge_base()
        embeddings=self.encode_chunks(parallel=parallel);dim=embeddings.shape[1]
        index=faiss.IndexFlatIP(dim);index.add(embeddings);self._index=index
        self.build_seconds=time.perf_counter()-start;return self

    def search(self,query:str,top_k:int=DEFAULT_TOP_K)->List[RetrievalResult]:
        if self._index is None: raise RuntimeError('Index not built. Call build() first.')
        model=self._get_model();q_vec=model.encode([query],normalize_embeddings=True,show_progress_bar=False).astype('float32')
        scores,indices=self._index.search(q_vec,top_k)
        results:List[RetrievalResult]=[]
        for score,idx in zip(scores[0],indices[0]):
            if idx==-1: continue
            results.append(RetrievalResult(chunk=self.chunks[idx],score=float(score)))
        return results

    def stats(self)->dict:
        return {"documents":len({c.source for c in self.chunks}),"chunks":len(self.chunks),"embedding_model":self.model_name,"vector_dim":self._index.d if self._index else None,"build_seconds":round(self.build_seconds,3)}

def build_engine(parallel:bool=False)->RagEngine: return RagEngine().build(parallel=parallel)

if __name__=='__main__':
    print('Building RAG engine (sequential)...')
    engine=build_engine(parallel=False);print('Stats:',engine.stats())
    sample=('cursor.execute("SELECT * FROM users WHERE name = \'" + username + "\'")')
    print('\nQuery snippet:\n  ',sample) ;print('\nTop matches:')
    for r in engine.search(sample,top_k=3):
        first_line=r.chunk.text.splitlines()[0]
        print(f"  [{r.score:.3f}] {r.chunk.source:32s} | {first_line}")
