"""Mide recuperación sin confundir extractos con respuestas de un LLM."""
from pathlib import Path
import argparse
import json
import os
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
    runtime = None
    if args.mode == 'llm':
        runtime = {'chat_model':os.getenv('CHAT_MODEL','qwen3:4b'),'embedding_model':os.getenv('EMBED_MODEL','embeddinggemma'),'temperature':0.1,'seed':42,'think':False,'num_ctx':8192,'num_predict':2048}
    for case in cases:
        start=time.perf_counter()
        result=answer(case['question'],mode=args.mode,retriever=engine)
        elapsed=(time.perf_counter()-start)*1000
        ids=list(dict.fromkeys(d['id'] for d in result['sources']))
        wanted=set(case['relevant'])
        recall=len(wanted.intersection(ids))/len(wanted) if wanted else None
        rr=next((1/(i+1) for i,d in enumerate(ids) if d in wanted),0) if wanted else None
        rows.append({**case,'retrieved':ids,'recall_at_4':recall,'reciprocal_rank':rr,'abstained':not ids,'latency_ms':round(elapsed,3),'result':result})
        print(f"{case['id']}: {result['status']} ({elapsed/1000:.2f} s)",flush=True)
        (ROOT/'evidencias'/f'progreso_{args.mode}.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    positive=[r for r in rows if r['relevant']]
    negative=[r for r in rows if not r['relevant']]
    summary={'mode':args.mode,'cases':len(rows),'recall_at_4':statistics.mean(r['recall_at_4'] for r in positive),'mrr':statistics.mean(r['reciprocal_rank'] for r in positive),'abstention_accuracy':statistics.mean(r['abstained'] for r in negative),'mean_latency_ms':round(statistics.mean(r['latency_ms'] for r in rows),3),'llm_semantic_faithfulness':'requiere revisión humana' if args.mode=='llm' else 'no medida: modo documental','corpus_sha256':engine.signature}
    out=ROOT/'evidencias'/f'evaluacion_{args.mode}.json'
    summary['generation_calls'] = sum(r['result']['generation'] is not None for r in rows)
    summary['answers_with_valid_citations'] = sum(r['result']['status']=='respuesta_con_citas' for r in rows)
    summary['answers_requiring_review'] = sum(r['result']['status']=='revision_requerida' for r in rows)
    summary['median_latency_ms'] = round(statistics.median(r['latency_ms'] for r in rows),3)
    generated_times = [r['latency_ms'] for r in rows if r['result']['generation'] is not None]
    summary['median_generation_query_latency_ms'] = round(statistics.median(generated_times),3) if generated_times else None
    out.write_text(json.dumps({'summary':summary,'runtime':runtime,'cases':rows},ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
