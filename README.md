# fleet-music-theorist

MIDI file → structured music theory analysis. One function, one dependency (music21), real output.

## Problem

You have a MIDI file. You want to know what's in it — not the bytes, but the music. What key is it in? How many parts? Does the melody move stepwise or by leaps? What's the pitch range per instrument?

music21 can answer all of this, but its API is a 2,000-page documentation project. This repo wraps the 20% you actually need into a single `analyze()` call.

## Insight

Most "music theory analysis" for MIDI boils down to four questions:
1. **Key** — Krumhansl-Schmuckler key-finding algorithm (music21 built-in)
2. **Parts** — how many instrument tracks and what's in each
3. **Intervals** — consecutive pitch differences reveal melodic contour
4. **Motion character** — stepwise vs. leap-based (percentage of intervals ≤ 2 semitones)

These four answers tell you most of what matters about a piece's harmonic structure.

## How It Works

```
MIDI file
  → music21.converter.parse()
  → score.analyze('key')           # Krumhansl-Schmuckler
  → iterate score.parts
    → extract notes, pitches, ranges per part
  → compute consecutive intervals across all notes
  → classify motion (stepwise >60% = "stepwise", else "leap-based")
  → return dict
```

The core function `analyze(midi_path) -> dict` in `lib/theorist.py` is ~50 lines. It parses a MIDI file through music21, extracts key, part structure, pitch ranges, and interval statistics, then returns everything as a plain dict.

## Code

```python
from lib.theorist import analyze

result = analyze("examples/demo-jam-output.mid")
# {
#   "key": "a minor",
#   "parts": 3,
#   "part_details": [
#     {"part": 0, "name": "Piano", "note_count": 32, "pitch_range": [60, 71], ...},
#     {"part": 1, "name": "Electric Bass", "note_count": 16, "pitch_range": [36, 40], ...},
#     {"part": 2, "name": "Percussion", "note_count": 32, "pitch_range": [0, 0], ...}
#   ],
#   "total_notes": 48,
#   "avg_interval": -0.51,
#   "stepwise_motion_pct": 25.5,
#   "analysis": "Key a minor, leap-based motion (avg interval -0.5 semitones), ..."
# }
```

CLI usage:

```bash
python lib/theorist.py path/to/file.mid
```

## Module Map

```
lib/
  theorist.py    — analyze() function + CLI entrypoint
examples/
  demo-jam-output.mid  — sample MIDI file (3-part: Piano, Bass, Percussion)
```

That's it. One source file. One function.

## Design Decisions

### What was chosen

- **music21 as sole dependency.** It's the standard Python library for musicology. Key detection uses the Krumhansl-Schmuckler algorithm, which is good enough for most tonal music. No point reimplementing.
- **Flat interval computation.** All notes across all parts are flattened into a single list before computing intervals. This means interval statistics reflect the total note stream, not individual melodic lines. Useful as a rough summary; misleading if you want per-voice contour.
- **Pitch range as [min, max] MIDI numbers.** Simple, unambiguous, easy to plot.

### Known limitations

1. **Unpitched percussion handling.** Parts with `Unpitched` notes (drums) report `pitch_range: [0, 0]` and `unique_pitches: 0`. The note count is correct, but all pitch-derived stats are empty. The code guards with `hasattr(n, 'pitch')`, which correctly filters them out of pitch analysis — but the empty range `[0, 0]` is the fallback and could be confused with actual MIDI note 0. Should return `null` or skip pitch stats for percussion parts.

2. **`.flat` deprecation.** Uses `part.flat.notes` which triggers a music21 deprecation warning. Should migrate to `part.flatten().notes`.

3. **No chord handling.** Chords in MIDI are silently passed over — only `Note` objects with `.pitch` are extracted. A chord's constituent pitches won't appear in the analysis.

4. **Bare except on key detection.** `score.analyze('key')` is wrapped in a bare `except:` that falls back to "Unknown". This swallows real errors (corrupt files, unsupported formats).

5. **No per-voice interval analysis.** The interval computation concatenates all parts, so the "average interval" and "stepwise motion" metrics don't reflect any single melodic line. A two-part counterpoint piece will report misleading averages.

6. **No tests, no packaging.** The module has zero tests and no `pyproject.toml` / `setup.py`. It runs as a script.

### What this is not

- Not a chord analyzer. No chord labeling, no Roman numeral analysis.
- Not a rhythm analyzer. No tempo detection, no time signature extraction.
- Not a form analyzer. No phrase detection, no section labeling.

It answers four questions well. Everything else is out of scope.

## Status

**Functional, minimal, single-purpose.** The `analyze()` function works correctly for pitched MIDI files with tonal content. The output matches what music21's Krumhansl-Schmuckler implementation produces. The demo file (`examples/demo-jam-output.mid`) analyzes to "a minor" with 3 parts and leap-based motion — consistent with visual inspection of the MIDI.

**Not packaged.** No `pyproject.toml`, no tests, no CI. Usable as a library import or CLI script but not installable via pip.

**Known bugs:** Percussion pitch_range fallback, `.flat` deprecation, bare except, no chord support.

## PyPI Readiness

See `pyproject.toml` for the packaging metadata. The module is simple enough to publish: one dependency (music21), one public function, no native extensions. Before publishing, fix at minimum the `.flat` deprecation and the percussion `pitch_range` bug.
