import argparse
import json
from .core import answer

parser = argparse.ArgumentParser(description='Nexo Soporte')
parser.add_argument('question', nargs='?')
parser.add_argument('--mode', choices=['documental','llm'], default='documental')
parser.add_argument('--serve', action='store_true')
args = parser.parse_args()
if args.serve:
    from .web import serve
    serve()
elif args.question:
    print(json.dumps(answer(args.question,mode=args.mode),ensure_ascii=False,indent=2))
else:
    parser.print_help()
