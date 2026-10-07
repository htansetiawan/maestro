"""Wait for free GPU, generate once, then publish only this experiment."""
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
REPO = ROOT.parents[1]
RECORD = ROOT/'record'
STATUS = RECORD/'queue-status.json'
THRESHOLD = 24*1024


def status(state, **details):
    data = dict(state=state, updated_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                required_free_mib=THRESHOLD, **details)
    tmp = STATUS.with_suffix('.tmp')
    tmp.write_text(json.dumps(data,indent=2)+'\n')
    tmp.replace(STATUS)
    print(json.dumps(data),flush=True)


def digest():
    paths = sorted((ROOT/'inputs').glob('*')) + sorted(RECORD.glob('*.py'))
    return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}


def git(*args):
    return subprocess.check_output(['git',*args],cwd=REPO,text=True).strip()


def main():
    with (RECORD/'queue.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX | fcntl.LOCK_NB)
        frozen = digest()
        if (ROOT/'outputs/sheet-orchestral').exists():
            raise RuntimeError('Output already exists; refusing duplicate generation')
        ready = 0
        while True:
            if digest() != frozen:
                raise RuntimeError('Queued inputs or scripts changed; review before restarting')
            try:
                free = int(subprocess.check_output(['nvidia-smi','--id=0','--query-gpu=memory.free','--format=csv,noheader,nounits'],text=True,timeout=15).strip())
            except (OSError, ValueError, subprocess.SubprocessError) as error:
                ready = 0
                status('waiting',query_error=str(error))
            else:
                ready = ready+1 if free >= THRESHOLD else 0
                status('waiting',free_mib=free,consecutive_ready_checks=ready)
                if ready >= 2:
                    break
            time.sleep(30)
        env = dict(os.environ,HF_HUB_OFFLINE='1',OMP_NUM_THREADS='4',CUDA_VISIBLE_DEVICES='0',TOKENIZERS_PARALLELISM='false')
        status('generating',free_mib=free)
        with (RECORD/'generation.log').open('x') as log:
            subprocess.run([sys.executable,str(RECORD/'generate.py')],env=env,cwd=REPO,stdout=log,stderr=subprocess.STDOUT,check=True)
        subprocess.run([sys.executable,str(RECORD/'build_delivery.py')],cwd=REPO,check=True)
        status('generated_publishing')
        if git('branch','--show-current') != 'main':
            raise RuntimeError('Audio saved; automatic publication requires main')
        if git('remote','get-url','origin') != 'https://github.com/htansetiawan/maestro.git':
            raise RuntimeError('Audio saved; unexpected origin')
        scope = str(ROOT.relative_to(REPO))
        for path in ROOT.rglob('*'):
            if path.is_file() and path.suffix in ('.flac','.mp3') and path.stat().st_size >= 100*1024**2:
                raise RuntimeError('Audio saved; file exceeds GitHub size limit')
        # --only preserves unrelated staged changes and excludes them from this commit.
        with (RECORD/'publish.log').open('x') as log:
            for command in (['git','add','--',scope], ['git','diff','--cached','--check','--',scope],
                            ['git','commit','--only','-m','Generate sheet-conditioned orchestral Yard song','--',scope],
                            ['git','push','origin','main']):
                subprocess.run(command,cwd=REPO,stdout=log,stderr=subprocess.STDOUT,check=True)
        status('published',commit=git('rev-parse','HEAD'),mp3='https://raw.githubusercontent.com/htansetiawan/maestro/main/'+scope+'/outputs/sheet-orchestral/audio.mp3')


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        status('failed',error=str(error),audio_exists=(ROOT/'outputs/sheet-orchestral/audio.mp3').exists())
        raise
