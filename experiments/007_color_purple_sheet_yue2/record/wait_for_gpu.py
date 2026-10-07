"""Queue exactly one prepared generation when GPU 0 has 17 GiB free.

Run under the user service manager so polling survives the chat turn.
No process is killed and no inference attempt is retried automatically.
"""
import datetime
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT/'record'
STATUS = RECORD/'gpu-wait-status.json'
REQUEST = ROOT/'prepared/request.json'
THRESHOLD_MIB = 17*1024


def status(state, **details):
    data = dict(state=state, updated_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                required_free_mib=THRESHOLD_MIB, pid=os.getpid(), **details)
    temporary = STATUS.with_suffix('.tmp')
    temporary.write_text(json.dumps(data, indent=2)+'\n')
    temporary.replace(STATUS)
    with (RECORD/'gpu-wait.log').open('a') as log:
        log.write(json.dumps(data)+'\n')
    print(json.dumps(data), flush=True)


def digest():
    return hashlib.sha256(REQUEST.read_bytes()).hexdigest()


def main():
    lock = (RECORD/'gpu-wait.lock').open('a')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    request_hash = digest()
    request = json.loads(REQUEST.read_text())
    out = ROOT/'outputs'/request['id']
    if out.exists():
        raise RuntimeError(f'An attempt already exists at {out}; refusing duplicate generation')
    command = [sys.executable, str(RECORD/'run.py')]
    env = dict(os.environ, HF_HUB_OFFLINE='1', OMP_NUM_THREADS='4',
               TOKENIZERS_PARALLELISM='false', CUDA_VISIBLE_DEVICES='0')
    subprocess.run(command, env=env, check=True)
    consecutive = 0
    while True:
        if digest() != request_hash:
            raise RuntimeError('Prepared request changed while queued; review before restarting')
        try:
            value = subprocess.check_output(['nvidia-smi','--id=0','--query-gpu=memory.free',
                                              '--format=csv,noheader,nounits'], text=True, timeout=15)
            free = int(value.strip())
        except (OSError, ValueError, subprocess.SubprocessError) as error:
            consecutive = 0
            status('waiting', query_error=str(error), request_sha256=request_hash)
            time.sleep(30)
            continue
        consecutive = consecutive + 1 if free >= THRESHOLD_MIB else 0
        status('waiting', free_mib=free, consecutive_ready_checks=consecutive,
               request_sha256=request_hash)
        if consecutive >= 2:
            break
        time.sleep(30)
    status('generating', free_mib=free, request_sha256=request_hash, output=str(out))
    with (RECORD/'generation.log').open('a') as log:
        completed = subprocess.run(command+['--generate'], env=env, stdout=log,
                                   stderr=subprocess.STDOUT, cwd=ROOT.parents[1])
    if completed.returncode:
        status('failed', returncode=completed.returncode, log=str(RECORD/'generation.log'))
        return completed.returncode
    measurement = json.loads((out/'measurement.json').read_text())
    state = 'completed_truncated' if any(measurement['truncated'].values()) else 'completed'
    status(state, output=str(out), mp3=str(out/'audio.mp3'),
           listening_review='Pending; successful generation does not prove score adherence.')
    # Refresh the local player while retaining the separate notation guide.
    page = ROOT/'index.html'
    content = page.read_text()
    content = content.replace('Queued. Waiting for GPU memory before YuE2 generation.',
                              'YuE2 generation saved. Musical fidelity awaits listening review.' if state=='completed'
                              else 'YuE2 audio saved, but generation reached its token limit. Review required.')
    marker = '<h2>Listen to the input melody</h2>'
    generated = ('<h2>YuE2 generated piano</h2><audio controls preload="metadata" '
                 f'src="outputs/{request["id"]}/audio.mp3"></audio><p>'
                 f'<a href="outputs/{request["id"]}/audio.flac">Lossless audio</a> · '
                 f'<a href="outputs/{request["id"]}/measurement.json">Run measurements</a></p>')
    page.write_text(content.replace(marker, generated+marker))
    readme = ROOT/'README.md'
    content = readme.read_text().replace('**Status: queued; waiting for GPU memory before generation.**',
                                       f'**Status: {state}; see the local listening page and outputs.**')
    readme.write_text(content)
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as error:
        status('failed', error=str(error))
        raise
