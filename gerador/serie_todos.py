# Junta todos os lotes da série. Ao criar um lote novo, acrescente o nome dele em LOTES.
import sys, os, importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
LOTES = ["serie_lote1", "serie_lote2", "serie_lote3"]
DIAS = {}
for _n in LOTES:
    DIAS.update(importlib.import_module(_n).DIAS)
CARROSSEIS = [c for v in DIAS.values() for c in v]
