import sys

from sentence_transformers import SentenceTransformer, util
from torch import Tensor

import config


class SentenceCompare:
    def __init__(self):
        self._model = SentenceTransformer(config.SENTENCE_COMPARE_MODEL, cache_folder=config.SENTENCE_COMPARE_CACHE_FOLDER)

    def estimate_correlation(self, text1: str, text2: str) -> float:
        """>0.80 is very similar"""
        embeddings1 = self._model.encode(text1)
        embeddings2 = self._model.encode(text2)
        if not isinstance(embeddings1, Tensor) or not isinstance(embeddings2, Tensor):
            print("ERROR[estimate_correlation failed]", file=sys.stderr)
            return 0
        sim = util.pytorch_cos_sim(embeddings1, embeddings2)
        return sim.item().real
