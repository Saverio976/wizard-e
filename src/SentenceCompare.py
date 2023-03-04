from sentence_transformers import SentenceTransformer, util

import config

class SentenceCompare:
    def __init__(self):
        self._model = SentenceTransformer(config.SENTENCE_COMPARE_MODEL)

    def estimate_correlation(self, text1, text2) -> float:
        """>0.80 is very similar"""
        embeddings1 = self._model.encode(text1)
        embeddings2 = self._model.encode(text2)
        sim = util.pytorch_cos_sim(embeddings1, embeddings2)
        return sim.item().real
