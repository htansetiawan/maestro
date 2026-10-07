"""Compile a short explicitly timed vocal line from audio-derived phrase anchors."""
from pathlib import Path
import json,hashlib
import cmudict,mido
ROOT=Path(__file__).resolve().parents[1]
start,length=1.70,25.0
# Manually selected attack anchors from CQT/onset evidence, in original recording seconds.
anchors=[1.927,4.888,7.663,10.728,14.129,16.776,19.377,22.396,26.401]
# Anchor labels are harmonic interpretations of the audio, not an imported sheet.
chords=['F','Gm7/F-like upper voices','Bb/F','Bbm/F','F','Gm7/F-like upper voices','Bb/F','Bbm/F']
words=[['Red','brick','walls'],['hold','the','light'],['Old','trees','shade'],['our','dreams','at','night'],['Friends','we','found'],['will','walk','with','us'],['Here','our','love'],['will','live','and','last']]
pitches=[[57,60,57],[55,58,62],[53,58,62],[61,60,58,53],[57,60,57],[55,58,60,62],[53,58,62],[61,60,58,53]]
dict_en=cmudict.dict();events=[]
quant=lambda x:round(x/.02)*.02
for bar,(left,right,ws,ps,chord) in enumerate(zip(anchors,anchors[1:],words,pitches,chords),1):
 span=right-left
 # First three-syllable bars use quarter, quarter, half; four-syllable bars eighth-like lead-ins to a held ending.
 fractions=[0,.25,.5,1] if len(ws)==3 else [0,.20,.40,.60,1]
 for i,(word,pitch) in enumerate(zip(ws,ps)):
  a=quant(left-start+span*fractions[i]);b=quant(left-start+span*fractions[i+1])
  if i==len(ws)-1: b-=.14 if bar%2==0 else .04
  phones=dict_en[word.lower()][0]
  if word.lower()=='our':phones=['AW1','R']
  events.append(dict(word=word,syllable=word.lower(),start=round(a,3),end=round(b,3),midi=pitch,phonemes=phones,bar=bar,chord_estimate=chord,original_audio_start=round(start+a,3)))
sequence=[];cursor=0.
for event in events:
 if event['start']>cursor+.001:sequence.append(dict(word='<SP>',duration=round(event['start']-cursor,3),pitch=0,phoneme='<SP>',note_type=1))
 sequence.append(dict(word=event['word'],duration=round(event['end']-event['start'],3),pitch=event['midi'],phoneme='en_'+'-'.join(event['phonemes']),note_type=2))
 cursor=event['end']
if cursor<length:sequence.append(dict(word='<SP>',duration=round(length-cursor,3),pitch=0,phoneme='<SP>',note_type=1))
assert abs(sum(x['duration']for x in sequence)-length)<1e-8
assert all(e['end']>e['start'] for e in events)
assert all(a['end']<=b['start'] for a,b in zip(events,events[1:]))
phone_set=set(json.loads(Path('/tmp/maestro-soulx-singer/soulxsinger/utils/phoneme/phone_set.json').read_text()))
assert all('en_'+ph in phone_set for e in events for ph in e['phonemes'])
meta=[dict(index='yard_notes_25s',language='English',time=[0,25000],text=' '.join(s['word'] for s in sequence),duration=' '.join(str(s['duration']) for s in sequence),phoneme=' '.join(s['phoneme']for s in sequence),note_pitch=' '.join(str(s['pitch'])for s in sequence),note_type=' '.join(str(s['note_type'])for s in sequence))]
(ROOT/'inputs/target-metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
score=dict(source='theme_from_the_color_purple.mp3',source_sha256='1a6ab9f251f1bc1ef278583b976c582aee39a67cde57536757b9bd4c1b0824a7',excerpt_start=start,excerpt_seconds=length,control='Explicit MIDI pitches and per-syllable durations; 20 ms grid',timing_method='Audio onset/CQT evidence; manually selected phrase anchors. Intermediate onsets are composed by proportional subdivision, not measured beat annotations.',harmonic_method='F-centered pedal harmony inferred from audio. Upper-voice labels are tentative; no sheet imported.',source_anchor_seconds=anchors,lyrics='Red brick walls hold the light\nOld trees shade our dreams at night\nFriends we found will walk with us\nHere our love will live and last',events=events)
(ROOT/'inputs/score.json').write_text(json.dumps(score,indent=2)+'\n')
(ROOT/'inputs/lyrics.txt').write_text(score['lyrics']+'\n')
# MIDI uses 120 BPM solely as an exact time carrier: 960 ticks/second.
mid=mido.MidiFile(ticks_per_beat=480);track=mido.MidiTrack();mid.tracks.append(track)
track.append(mido.MetaMessage('set_tempo',tempo=500000,time=0))
messages=[]
for e in events:
 messages.extend([(round(e['start']*960),mido.MetaMessage('lyrics',text=e['word'])),(round(e['start']*960),mido.Message('note_on',note=e['midi'],velocity=80)),(round(e['end']*960),mido.Message('note_off',note=e['midi'],velocity=0))])
previous=0
for tick,msg in sorted(messages,key=lambda x:x[0]):
 msg.time=tick-previous;track.append(msg);previous=tick
mid.save(ROOT/'inputs/vocal.mid')
print('Prepared',len(events),'explicit notes; range',min(e['midi'] for e in events),max(e['midi'] for e in events))
