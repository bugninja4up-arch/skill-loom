"""Portable launcher: python start.py --root /path/to/skills"""
import argparse
import os
from pathlib import Path
import secrets

parser = argparse.ArgumentParser(description='Skill Loom — local skill enrichment editor')
parser.add_argument('--root', action='append', help='Allowed skills folder; may be repeated. Default: your home folder.')
parser.add_argument('--port', type=int, default=8765)
parser.add_argument('--host', default='127.0.0.1', help='Use 0.0.0.0 only behind a trusted firewall or authenticated tunnel.')
parser.add_argument('--endpoint', help='OpenAI-compatible base URL, normally ending in /v1')
parser.add_argument('--model', help='Model ID supported by your provider')
args = parser.parse_args()
os.environ['SKILL_LOOM_ROOTS'] = os.pathsep.join(str(Path(p).expanduser().resolve()) for p in (args.root or [str(Path.home())]))
os.environ['PORT'] = str(args.port)
os.environ['HOST'] = args.host
os.environ.setdefault('SKILL_LOOM_TOKEN', secrets.token_urlsafe(32))
if args.endpoint:
    os.environ['OPENAI_API_BASE'] = args.endpoint
if args.model:
    os.environ['SKILL_LOOM_MODEL'] = args.model
import app
import uvicorn
print(f'Open: http://localhost:{args.port}/#token={app.TOKEN}', flush=True)
print('Keep this session link private. API keys are entered in the UI or OPENAI_API_KEY environment variable.', flush=True)
uvicorn.run(app.app,host=args.host,port=args.port,access_log=False)
