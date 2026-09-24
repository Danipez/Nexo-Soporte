"""Mide recuperación sin confundir extractos con respuestas de un LLM."""
from pathlib import Path
import argparse
import json
import statistics
import sys
import time
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from nexo.core import ROOT, Retriever, answer

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--mode',choices=['documental','llm'],default='documental')
    args=parser.parse_args()
    cases=json.loads((ROOT/'data/consultas.json').read_text(encoding='utf-8'))
    engine=Retriever()
    rows=[]
    for case in cases:
        start=time.perf_counter()
        result=answer(case['question'],mode=args.mode,retriever=engine)
        elapsed=(time.perf_counter()-start)*1000
        ids=list(dict.fromkeys(d['id'] for d in result['sources']))
        wanted=set(case['relevant'])
        recall=len(wanted.intersection(ids))/len(wanted) if wanted else None
        rr=next((1/(i+1) for i,d in enumerate(ids) if d in wanted),0) if wanted else None
        rows.append({**case,'retrieved':ids,'recall_at_4':recall,'reciprocal_rank':rr,'abstained':not ids,'latency_ms':round(elapsed,3),'result':result})
    positive=[r for r in rows if r['relevant']]
    negative=[r for r in rows if not r['relevant']]
    summary={'mode':args.mode,'cases':len(rows),'recall_at_4':statistics.mean(r['recall_at_4'] for r in positive),'mrr':statistics.mean(r['reciprocal_rank'] for r in positive),'abstention_accuracy':statistics.mean(r['abstained'] for r in negative),'mean_latency_ms':round(statistics.mean(r['latency_ms'] for r in rows),3),'llm_semantic_faithfulness':'requiere revisión humana' if args.mode=='llm' else 'no medida: modo documental','corpus_sha256':engine.signature}
    out=ROOT/'evidencias'/f'evaluacion_{args.mode}.json'
    out.write_text(json.dumps({'summary':summary,'cases':rows},ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
