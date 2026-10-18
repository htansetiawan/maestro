# Music notations: what each one keeps, and where the corpora are

*October 2026. Written after the YuE2 score-conditioning trials showed that most of a printed piano arrangement never reaches the model. This note fixes the vocabulary and the sources so later experiments can say exactly which representation they tested.*

## 1. Definitions

A music notation is a symbolic record of a piece. Seeger (1958) separated two purposes that are still the useful split: **prescriptive** notation tells a performer what to do (a score), **descriptive** notation records what was done (a transcription of a performance). Common Western notation is prescriptive. A MIDI file captured from a pianist is descriptive. Converting between the two is lossy in both directions: a score has no velocities or rubato, a performance capture has no pitch spelling, voices, rests or bar lines.

Every representation in this note sits on one of four layers, and information drops at each step down:

| Layer | Example | Holds | Lacks |
|---|---|---|---|
| Image of the page | PDF or PNG scan | Everything the engraver wrote | Nothing is machine-readable |
| Notation encoding | MusicXML, MEI, Humdrum, ABC, LilyPond | Pitch spelling, notated rhythm, voices, staves, chords, harmony labels, lyrics, expression marks | Performed timing and dynamics |
| Performance encoding | Standard MIDI File, piano roll, event tokens | Sounding pitch, onset, offset, velocity, pedal | Spelling, voices, rests, beaming, tuplet grouping, most marks |
| Audio | WAV, FLAC, MP3 | The sound | Any symbol at all |

Optical music recognition (OMR) moves up from the image layer; automatic music transcription moves up from audio. Rendering and synthesis move down. The systems in this project have a fixed entry point: YuE2 reads a notation encoding (a restricted ABC), ACE-Step reads only audio and text, SheetSage2 reads audio and writes notation.

## 2. Notation encodings

| Format | Origin | Form | Keeps | Does not keep | Canonical reference |
|---|---|---|---|---|---|
| **MusicXML** | Recordare, 2004; W3C Music Notation Community Group since 2015; version 4.0 (2021) | XML, compressed as `.mxl` | Parts, staves, voices, note stacks, exact durations and tuplets, ties, slurs, articulations, dynamics, harmony (chord symbols), lyrics, layout | Nothing structural; it is the interchange format engravers export | Good (2001); W3C (2021) |
| **MEI** | Music Encoding Initiative, 2000s; MEI 5 (2023) | XML | Everything MusicXML keeps, plus editorial apparatus, variants, sources, mensural and neume notation | Wide tool support outside scholarship; Verovio renders it | Roland (2002); MEI Guidelines |
| **Humdrum `**kern`** | Huron, 1990s | Plain text, one spine per voice, one row per time slice | Pitch spelling, duration, voices, ties, beams, slurs, with parallel spines for harmony (`**harm`), lyrics and analysis | Layout; expression marks are partial | Huron (2002); Sapp (2005) |
| **ABC** (standard 2.1) | Walshaw, 1991; standard 2.1 (2011) | Plain text, one line of letters per voice | Melody with key-relative spelling, chords in `[ ]`, chord symbols in quotes, tuplets, grace notes, ornaments, repeats, lyrics on `w:` lines, multiple voices | Fine engraving control; polyphony is awkward beyond a few voices | Walshaw (2011) |
| **LilyPond** | Nienhuys and Nieuwenhuizen, 1996 | Text program for an engraver | Full engraving, including layout and typography | It is an input language, so parsing it back is hard | Nienhuys and Nieuwenhuizen (2003) |
| **Tablature** | Historical; Guitar Pro files today | Fret and string per note plus rhythm | Fingering, which pitch notation discards | Pitch as an abstraction; voice leading | Sarmento et al. (2021) for the ML corpus |
| **Lead sheet** | Jazz and popular practice | Melody plus chord symbols plus lyrics, in any of the above or in iReal Pro and ChordPro | The tune and the harmony as labels | Voicings, bass lines, accompaniment figures | Broze and Shanahan (2013) describe the iRb corpus |
| **Numbered notation (jianpu)** | Galin-Paris-Chevé method, 19th century; standard in China | Scale degrees 1 to 7 with dots for octave and lines for duration | Melody relative to a tonic, so it transposes freely | Absolute pitch unless the tonic is stated; polyphony | No single standards document |
| **Roman numerals** | Music theory; RomanText (2019) | Text keyed to measures and beats | Harmonic function relative to a key | Any melody or rhythm | Gotham, Tymoczko and Cuthbert (2019) |

Two facts matter for the current experiments. First, MusicXML is the only format in this table that every OMR engine and every notation editor emits, so it is the natural output of score reading. Second, the ABC accepted by YuE2 is not the ABC standard: it allows exactly two monophonic voices, chord symbols from fifteen qualities, durations on a power-of-two grid, no tuplets, graces, stacks, repeats, slurs or lyric lines, and an accidental rule of its own. It is a lead sheet, not a score. Every conversion from MusicXML into it is a reduction.

## 3. Performance encodings and tokenizations

The **Standard MIDI File** (MIDI Association, 1988 onward) stores note-on and note-off events with velocity on 16 channels, with tempo and time-signature meta events and continuous controllers such as the sustain pedal (CC 64). It has no notion of pitch spelling, rests, voices within a channel, or notated duration, so a score exported to MIDI and read back is a transcription problem.

Sequence models tokenize MIDI rather than read it directly. The main schemes are the performance-event vocabulary of Oore et al. (2020), which interleaves note-on, note-off, time-shift and velocity tokens; REMI (Huang and Yang, 2020), which adds bar and beat position tokens so metre is explicit; compound and multi-attribute tokens that pack one note into one step; and the arrival-time encoding of the Anticipatory Music Transformer (Thickstun et al., 2023). The MidiTok library (Fradet et al., 2021) implements most of them. All of them keep what MIDI keeps and nothing more.

## 4. Repositories and datasets

Counts are the published ones. Rights vary: most score repositories hold public-domain works, most MIDI corpora are of unverified provenance, and most pop lead-sheet corpora are redistributed without rights.

| Representation | Corpus | Content | Reference |
|---|---|---|---|
| Page images | IMSLP (Petrucci Music Library) | Public-domain scores as scanned PDFs, the largest open collection | imslp.org |
| Page images for OMR | PrIMuS | 87,678 real incipits from RISM with semantic and agnostic encodings | Calvo-Zaragoza and Rizo (2018) |
| | MUSCIMA++ | 140 handwritten pages with symbol-level annotation | Hajič and Pecina (2017) |
| | DeepScores | Synthetic rendered pages for symbol detection | Tuggener et al. (2018) |
| | GrandStaff | Synthetic pianoform systems, the first end-to-end two-staff OMR benchmark | Ríos-Vila et al. (2023) |
| MusicXML and MuseScore | OpenScore Lieder Corpus | Over 1,300 public-domain art songs, transcribed and reviewed | Gotham and Jonas (2022) |
| | OpenScore String Quartets | Complete quartets by Haydn, Mozart, Beethoven and others | Gotham et al. (2023) |
| | ASAP | 222 scores in MusicXML aligned to 1,068 MIDI performances and audio | Foscarin et al. (2020) |
| Humdrum | KernScores | Thousands of classical scores in `**kern`, including the 371 Bach chorales | Sapp (2005); kern.ccarh.org |
| ABC | The Session | Irish traditional tunes with public data dumps, the folk-rnn training source | thesession.org; Sturm et al. (2016) |
| | abcnotation.com | Index of folk and traditional tune collections in ABC | Walshaw |
| | Nottingham Music Database | About 1,200 British and American folk tunes with chords | Foxley; used by Boulanger-Lewandowski et al. (2012) |
| LilyPond | Mutopia Project | Public-domain scores as LilyPond source and PDF | mutopiaproject.org |
| Lead sheets and harmony | Hooktheory TheoryTab | Crowd-sourced melody and chord transcriptions of popular songs; SheetSage's training data | Donahue, Thickstun and Liang (2022) |
| | iRb | 1,186 jazz standards as chord charts | Broze and Shanahan (2013) |
| | Weimar Jazz Database | 456 transcribed jazz solos with chords and metadata | Pfleiderer et al. (2017) |
| | McGill Billboard | Expert chord annotations of Billboard Hot 100 songs, 1958 to 1991 | Burgoyne, Wild and Fujinaga (2011) |
| | Chordonomicon | 666,000 chord progressions scraped from guitar tabs | Kantarelis et al. (2024) |
| | When in Rome | Roman-numeral analyses in RomanText | Gotham, Tymoczko and Cuthbert (2019) |
| Tablature | DadaGP | 26,181 Guitar Pro songs with a token encoding | Sarmento et al. (2021) |
| MIDI | Lakh MIDI Dataset | 176,581 files, 45,129 matched to the Million Song Dataset | Raffel (2016) |
| | MetaMIDI Dataset | 436,631 files linked to audio and metadata | Ens and Pasquier (2021) |
| | MAESTRO | About 200 hours of piano competition performances as aligned MIDI and audio | Hawthorne et al. (2019) |
| | GiantMIDI-Piano | 10,855 classical piano works, transcribed from audio by a neural model | Kong et al. (2022) |
| | POP909 | 909 pop songs as piano arrangements with melody, bridge and accompaniment tracks | Wang et al. (2020) |
| Aligned audio and symbols | MusicNet | 330 classical recordings with note-level labels | Thickstun, Harchaoui and Kakade (2017) |
| | Slakh2100 | 2,100 Lakh MIDI songs synthesized to multitrack audio | Manilow et al. (2019) |

Two caveats. GiantMIDI-Piano and every "transcribed" corpus inherit the errors of the transcriber, so they are descriptive data of a model, not of a performer. Wikifonia, the lead-sheet collection cited in many older papers, closed in 2013 and survives only as unofficial copies.

## 5. What the generators in this project actually read

| System | Symbolic input | Layer |
|---|---|---|
| YuE2 | Two monophonic voices and chord symbols in a restricted ABC dialect; or none, in which case it writes that plan itself | Lead sheet |
| SheetSage2 (YuE2's transcriber) | Audio in; melody, chords, beats, key and structure out as ABC and MIDI | Audio to lead sheet |
| ACE-Step 1.5 | None; audio latents, text and lyrics | Performance encoding of its own |
| SoulX-Singer | Note list with MIDI pitch, duration and phonemes on a 20 ms grid | Performance encoding |
| Anticipatory Music Transformer | MIDI event tokens | Performance encoding |

None of them reads a score. The chain for a composer who has a printed arrangement is therefore image, then MusicXML through OMR, then a reduction into whatever the chosen model accepts, and the reduction is where the arrangement is lost. Experiments 013 and 014 measure the first and last of those steps.

## References

Boulanger-Lewandowski, N., Bengio, Y., and Vincent, P. (2012). Modeling temporal dependencies in high-dimensional sequences: Application to polyphonic music generation and transcription. *ICML 2012*.

Broze, Y., and Shanahan, D. (2013). Diachronic changes in jazz harmony: A cognitive perspective. *Music Perception*, 31(1), 32–45.

Burgoyne, J. A., Wild, J., and Fujinaga, I. (2011). An expert ground truth set for audio chord recognition and music analysis. *ISMIR 2011*.

Calvo-Zaragoza, J., and Rizo, D. (2018). End-to-end neural optical music recognition of monophonic scores. *Applied Sciences*, 8(4), 606.

Calvo-Zaragoza, J., Hajič, J., and Pacha, A. (2020). Understanding optical music recognition. *ACM Computing Surveys*, 53(4), 1–35.

Cuthbert, M. S., and Ariza, C. (2010). music21: A toolkit for computer-aided musicology and symbolic music data. *ISMIR 2010*.

Donahue, C., Thickstun, J., and Liang, P. (2022). Melody transcription via generative pre-training. *ISMIR 2022*.

Ens, J., and Pasquier, P. (2021). Building the MetaMIDI Dataset: Linking symbolic and audio musical data. *ISMIR 2021*.

Foscarin, F., McLeod, A., Rigaux, P., Jacquemard, F., and Sakai, M. (2020). ASAP: A dataset of aligned scores and performances for piano transcription. *ISMIR 2020*.

Fradet, N., Briot, J.-P., Chhel, F., El Fallah Seghrouchni, A., and Gutowski, N. (2021). MidiTok: A Python package for MIDI file tokenization. *ISMIR 2021, late-breaking demo*.

Good, M. (2001). MusicXML: An internet-friendly format for sheet music. *XML Conference and Expo 2001*.

Gotham, M., and Jonas, P. (2022). The OpenScore Lieder Corpus. *Music Encoding Conference Proceedings 2021*.

Gotham, M., Redbond, M., Bower, B., and Jonas, P. (2023). The "OpenScore String Quartet" corpus. *Digital Libraries for Musicology (DLfM) 2023*.

Gotham, M., Tymoczko, D., and Cuthbert, M. S. (2019). The RomanText format: A flexible and standard method for representing Roman numeral analyses. *ISMIR 2019*.

Hajič, J., and Pecina, P. (2017). The MUSCIMA++ dataset for handwritten optical music recognition. *ICDAR 2017*.

Hawthorne, C., Stasyuk, A., Roberts, A., Simon, I., Huang, C.-Z. A., Dieleman, S., Elsen, E., Engel, J., and Eck, D. (2019). Enabling factorized piano music modeling and generation with the MAESTRO dataset. *ICLR 2019*.

Huang, Y.-S., and Yang, Y.-H. (2020). Pop Music Transformer: Beat-based modeling and generation of expressive pop piano compositions. *ACM Multimedia 2020*.

Huron, D. (2002). Music information processing using the Humdrum Toolkit: Concepts, examples, and lessons. *Computer Music Journal*, 26(2), 11–26.

Kantarelis, S., Dervakos, T., Kotsani, N., and Stamou, G. (2024). Chordonomicon: A dataset of 666,000 songs and their chord progressions. arXiv:2410.22046.

Kong, Q., Li, B., Chen, J., and Wang, Y. (2022). GiantMIDI-Piano: A large-scale MIDI dataset for classical piano music. *Transactions of the International Society for Music Information Retrieval*, 5(1), 87–98.

Manilow, E., Wichern, G., Seetharaman, P., and Le Roux, J. (2019). Cutting music source separation some Slakh: A dataset to study the impact of training data quality and quantity. *WASPAA 2019*.

MIDI Association. *MIDI 1.0 Detailed Specification* and *Standard MIDI Files 1.0*. midi.org.

Music Encoding Initiative. *MEI Guidelines*, version 5. music-encoding.org.

Nienhuys, H.-W., and Nieuwenhuizen, J. (2003). LilyPond, a system for automated music engraving. *XIV Colloquium on Musical Informatics (CIM 2003)*.

Oore, S., Simon, I., Dieleman, S., Eck, D., and Simonyan, K. (2020). This time with feeling: Learning expressive musical performance. *Neural Computing and Applications*, 32, 955–967.

Pfleiderer, M., Frieler, K., Abeßer, J., Zaddach, W.-G., and Burkhart, B. (Eds.) (2017). *Inside the Jazzomat: New Perspectives for Jazz Research*. Schott Campus.

Raffel, C. (2016). *Learning-Based Methods for Comparing Sequences, with Applications to Audio-to-MIDI Alignment and Matching*. PhD thesis, Columbia University.

Ríos-Vila, A., Rizo, D., Iñesta, J. M., and Calvo-Zaragoza, J. (2023). End-to-end optical music recognition for pianoform sheet music. *International Journal on Document Analysis and Recognition*, 26, 347–362.

Roland, P. (2002). The Music Encoding Initiative (MEI). *First International Conference on Musical Applications Using XML*.

Sapp, C. S. (2005). Online database of scores in the Humdrum file format. *ISMIR 2005*.

Sarmento, P., Kumar, A., Carr, C. J., Zukowski, Z., Barthet, M., and Yang, Y.-H. (2021). DadaGP: A dataset of tokenized GuitarPro songs for sequence models. *ISMIR 2021*.

Seeger, C. (1958). Prescriptive and descriptive music-writing. *The Musical Quarterly*, 44(2), 184–195.

Sturm, B. L., Santos, J. F., Ben-Tal, O., and Korshunova, I. (2016). Music transcription modelling and composition using deep learning. arXiv:1604.08723.

Thickstun, J., Hall, D., Donahue, C., and Liang, P. (2023). Anticipatory Music Transformer. arXiv:2306.08620.

Thickstun, J., Harchaoui, Z., and Kakade, S. (2017). Learning features of music from scratch. *ICLR 2017*.

Tuggener, L., Elezi, I., Schmidhuber, J., Pelillo, M., and Stadelmann, T. (2018). DeepScores: A dataset for segmentation, detection and classification of tiny objects. *ICPR 2018*.

W3C Music Notation Community Group (2021). *MusicXML 4.0*. w3.org/2021/06/musicxml40.

Walshaw, C. (2011). *The ABC music standard 2.1*. abcnotation.com/wiki/abc:standard:v2.1.

Wang, Z., Chen, K., Jiang, J., Zhang, Y., Xu, M., Dai, S., Gu, X., and Xia, G. (2020). POP909: A pop-song dataset for music arrangement generation. *ISMIR 2020*.

Yuan, R., et al. (2026). YuE2: Unifying symbolic and audio music generation at frontier quality. arXiv:2609.33757.
