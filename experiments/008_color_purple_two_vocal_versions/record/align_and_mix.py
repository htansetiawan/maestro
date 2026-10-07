"""Version B: align isolated YuE2 vocals; leave the decoded original piano fixed.

Chroma DTW is a timing estimate, not a measured lyric/phoneme alignment.
Rubber Band's offline key-frame API changes vocal timing with pitch scale 1.0.
"""
import ctypes as C
import hashlib
from importlib.metadata import version
import json
from pathlib import Path
import subprocess

import librosa
import numpy as np
from scipy.interpolate import interp1d
from scipy.ndimage import median_filter
from scipy.spatial.distance import cdist
import soundfile as sf

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT.parent/'007_color_purple_sheet_yue2/outputs/sheet-piano-20261005/audio.mp3'


def write(path,data):
    path.write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')


def decode(path,sr=48000,channels=2):
    raw=subprocess.check_output(['ffmpeg','-nostdin','-v','error','-i',str(path),
        '-ar',str(sr),'-ac',str(channels),'-f','f32le','-'])
    return np.frombuffer(raw,dtype='<f4').reshape(-1,channels).copy()


def chroma(path):
    sr,hop=22050,2048
    mono=decode(path,sr,1)[:,0]
    raw=librosa.feature.chroma_cqt(y=mono,sr=sr,hop_length=hop,
            fmin=librosa.note_to_hz('C2'),n_octaves=5,tuning=0.0)
    smooth=librosa.feature.chroma_cens(C=raw,win_len_smooth=11)
    return smooth, len(mono)/sr


def align(source,target):
    a,duration_a=chroma(source)
    b,duration_b=chroma(target)
    n=int(round(max(duration_a,duration_b)*8))+1
    grid=np.linspace(0,1,n)
    def uniform(x):
        y=interp1d(np.linspace(0,1,x.shape[1]),x,axis=1)(grid)
        return y / np.maximum(np.linalg.norm(y,axis=0),1e-9)
    aa,bb=uniform(a),uniform(b)
    costs=cdist(aa.T,bb.T,metric='cosine')
    costs=np.nan_to_num(costs,nan=1.0)
    # Step choices bound local normalized tempo changes; 20% corridor limits drift.
    _,reverse=librosa.sequence.dtw(C=costs,step_sizes_sigma=np.array([[1,1],[1,2],[2,1]]),
          weights_mul=np.array([1.,1.5,1.5]),global_constraints=True,band_rad=.20)
    path=reverse[::-1]
    x,y=path[:,0],path[:,1]
    rawmap=np.interp(np.arange(n),x,y)
    smoothmap=median_filter(rawmap,size=9,mode='nearest')
    anchors=np.unique(np.r_[0,np.arange(1.5,duration_a,1.5),duration_a])
    mapped=np.interp(anchors/duration_a*(n-1),np.arange(n),smoothmap)/(n-1)*duration_b
    mapped[0],mapped[-1]=0,duration_b
    assert np.all(np.diff(mapped)>0)
    local_ratios=np.diff(mapped)/np.diff(anchors)
    before=np.sum(aa*bb,axis=0)
    warped=np.stack([np.interp(rawmap,np.arange(n),channel) for channel in bb])
    after=np.sum(aa*warped,axis=0)
    report=dict(method='CENS chroma, global DTW, normalized durations, monotone local time map',
        source_seconds=duration_a,target_seconds=duration_b,feature_rate_approx_hz=8,
        hop_length=2048,analysis_sample_rate=22050,dtw_band_fraction=.20,
        source_to_target_seconds=[[float(s),float(t)] for s,t in zip(anchors,mapped)],
        cosine_similarity_before_mean=float(before.mean()),
        cosine_similarity_after_mean=float(after.mean()),
        cosine_similarity_after_p10=float(np.quantile(after,.1)),
        target_source_duration_ratio=duration_b/duration_a,
        local_duration_ratio_min=float(local_ratios.min()),
        local_duration_ratio_max=float(local_ratios.max()),
        local_duration_ratio_median=float(np.median(local_ratios)),
        caveat='Harmonic feature match only. Repeated passages can align incorrectly; no syllable/phoneme synchronization claim.')
    return anchors,mapped,report


def stretch(audio,sr,anchors,mapped,target_frames):
    lib=C.CDLL('librubberband.so.2')
    state_type=C.c_void_p
    fptr=C.POINTER(C.c_float)
    arrayptr=C.POINTER(fptr)
    signatures={
        'new':([C.c_uint,C.c_uint,C.c_int,C.c_double,C.c_double],state_type),
        'delete':([state_type],None),
        'set_expected_input_duration':([state_type,C.c_uint],None),
        'set_max_process_size':([state_type,C.c_uint],None),
        'set_key_frame_map':([state_type,C.c_uint,C.POINTER(C.c_uint),C.POINTER(C.c_uint)],None),
        'study':([state_type,arrayptr,C.c_uint,C.c_int],None),
        'process':([state_type,arrayptr,C.c_uint,C.c_int],None),
        'available':([state_type],C.c_int),
        'retrieve':([state_type,arrayptr,C.c_uint],C.c_uint),
        'get_engine_version':([state_type],C.c_int)}
    for name,(args,result) in signatures.items():
        f=getattr(lib,'rubberband_'+name);f.argtypes=args;f.restype=result
    # Offline R3, preserve formants, stereo channels together, one worker.
    options=0x20000000|0x01000000|0x10000000|0x00010000
    state=lib.rubberband_new(sr,audio.shape[1],options,target_frames/len(audio),1.0)
    if not state: raise RuntimeError('Rubber Band could not create a stretcher')
    size=4096
    source=np.ascontiguousarray(audio.T,dtype=np.float32)
    def pointers(x):
        return (fptr*x.shape[0])(*(channel.ctypes.data_as(fptr) for channel in x))
    left=np.asarray(np.round(anchors*sr),dtype=np.uint32)
    right=np.asarray(np.round(mapped*sr),dtype=np.uint32)
    left[-1]=len(audio);right[-1]=target_frames
    # Overall duration is specified by the ratio; only interior points go in the map.
    # Supplying endpoint keys can create a zero-length final interval in R3.
    interior=(left>0)&(left<len(audio))&(right>0)&(right<target_frames)
    left,right=left[interior].copy(),right[interior].copy()
    output=[]
    try:
        engine=lib.rubberband_get_engine_version(state)
        lib.rubberband_set_expected_input_duration(state,len(audio))
        lib.rubberband_set_max_process_size(state,size)
        lib.rubberband_set_key_frame_map(state,len(left),left.ctypes.data_as(C.POINTER(C.c_uint)),right.ctypes.data_as(C.POINTER(C.c_uint)))
        for start in range(0,len(audio),size):
            block=np.ascontiguousarray(source[:,start:start+size])
            lib.rubberband_study(state,pointers(block),block.shape[1],int(start+size>=len(audio)))
        for start in range(0,len(audio),size):
            block=np.ascontiguousarray(source[:,start:start+size])
            lib.rubberband_process(state,pointers(block),block.shape[1],int(start+size>=len(audio)))
            while (available:=lib.rubberband_available(state))>0:
                chunk=np.empty((source.shape[0],available),dtype=np.float32)
                got=lib.rubberband_retrieve(state,pointers(chunk),available)
                output.append(chunk[:,:got].T.copy())
        result=np.concatenate(output)
    finally:
        lib.rubberband_delete(state)
    raw_frames=len(result)
    if len(result)<target_frames:
        result=np.pad(result,((0,target_frames-len(result)),(0,0)))
    result=result[:target_frames]
    return result,dict(engine=engine,pitch_scale=1.0,keyframes=len(left),raw_frames=raw_frames,
                       target_frames=target_frames,tail_pad_or_trim_frames=target_frames-raw_frames,
                       method='Rubber Band offline key-frame time map applied to isolated vocals only')


def active_rms(x):
    # Exclude silent blocks so a long piano-only intro does not boost vocal gain.
    energies=np.array([np.mean(block.astype(np.float64)**2) for block in np.array_split(x,max(1,len(x)//24000))])
    audible=energies[energies>max(1e-8,float(energies.max())*.01)]
    return float(np.sqrt(audible.mean()))


def main():
    out=ROOT/'outputs/existing-piano-vocal'
    out.mkdir(parents=True,exist_ok=False)
    accompaniment=ROOT/'outputs/separated/accompaniment.flac'
    vocal_path=ROOT/'outputs/separated/vocals.flac'
    print('Estimating accompaniment alignment',flush=True)
    anchors,mapped,alignment=align(accompaniment,BASE)
    write(out/'alignment.json',alignment)
    vocal,sr=sf.read(vocal_path,dtype='float32',always_2d=True)
    piano=decode(BASE,sr,2)
    print('Warping vocals; piano remains fixed',flush=True)
    aligned,warp=stretch(vocal,sr,anchors,mapped,len(piano))
    assert np.isfinite(aligned).all()
    piano_level,vocal_level=active_rms(piano),active_rms(aligned)
    assert vocal_level>1e-5
    vocal_gain=float(np.clip(piano_level/vocal_level*10**(-2/20),.25,4.))
    summed=piano+vocal_gain*aligned
    global_gain=min(1.,.95/float(np.abs(summed).max()))
    mixed=summed*global_gain
    sf.write(out/'vocals-aligned.flac',aligned,sr,subtype='PCM_24')
    sf.write(out/'audio.flac',mixed,sr,subtype='PCM_24')
    encoded,_=sf.read(out/'audio.flac',dtype='float32',always_2d=True)
    # Reconstruct the original piano from the actual lossless output, allowing PCM rounding.
    recovered=encoded/global_gain-vocal_gain*aligned
    reconstruction_error=float(np.max(np.abs(recovered-piano)))
    assert reconstruction_error<2e-6
    for stem in ['audio','vocals-aligned']:
        subprocess.run(['ffmpeg','-nostdin','-v','error','-i',str(out/(stem+'.flac')),
                        '-c:a','libmp3lame','-b:a','256k',str(out/(stem+'.mp3'))],check=True)
    write(out/'mix.json',dict(operation='existing piano plus separated, timing-adjusted YuE2 singing',
        base_source='experiment 007 audio.mp3, decoded by ffmpeg to 48 kHz stereo float32',
        base_sha256=hashlib.sha256(BASE.read_bytes()).hexdigest(),
        vocal_source_sha256=hashlib.sha256(vocal_path.read_bytes()).hexdigest(),
        samples=len(piano),sample_rate=sr,seconds=len(piano)/sr,vocal_gain=vocal_gain,global_gain=global_gain,
        piano_time_stretched=False,piano_regenerated=False,piano_reconstruction_max_error=reconstruction_error,
        peak=float(np.abs(mixed).max()),rms=float(np.sqrt(np.mean(mixed.astype(np.float64)**2))),
        vocal_active_rms=vocal_level,piano_active_rms=piano_level,
        warp=warp,librosa_version=version('librosa'),
        audible_alignment_verified=False,caveat='Separation leakage and time-stretch artifacts remain possible. Chroma DTW is not phoneme alignment.'))
    print(json.dumps(dict(output=str(out),seconds=len(piano)/sr,alignment=alignment['cosine_similarity_after_mean'],
                         piano_reconstruction_error=reconstruction_error)),flush=True)


if __name__=='__main__':
    main()
