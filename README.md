# 📐 music-theorist

**Drop a MIDI file. Get a complete theory analysis.**

---

## Wait, show me

```bash
python lib/theorist.py path/to/file.mid
```

```json
{
  "key": "C major",
  "parts": 3,
  "total_notes": 48,
  "avg_interval": -0.51,
  "stepwise_motion_pct": 25.5,
  "analysis": "Key C major, leap-based motion (avg interval -0.5 semitones), 32 notes in Piano part"
}
```

That's a full theory breakdown of any MIDI file — key signature, part structure, interval content, motion characterization. All from one command.

---

## What it tells you

| Output | What it means | Why it matters |
|--------|---------------|----------------|
| `key: C major` | The tonal center | Everything else follows from this |
| `parts: 3` | Three instrument tracks | Piano, Bass, Drums — or any arrangement |
| `avg_interval: -0.51` | Average step is ~half a semitone down | Descending tendency (melodic contour) |
| `stepwise_motion: 25.5%` | Only 25% of intervals are steps | This is a leap-based melody — dramatic, wide-ranging |

---

## 5 things you'll analyze

### 1. A MIDI file from the fleet

```bash
python lib/theorist.py /tmp/jam-output.mid
# → "Key C major, leap-based motion, 48 notes in Piano part"
```

### 2. A file from any source

```bash
python lib/theorist.py ~/Downloads/song.mid
# → Analyze any MIDI you've ever downloaded
```

### 3. Your own compositions

```bash
# 1. Export from your DAW as MIDI
# 2. Drop it into theorist
# 3. Read what it says about your harmonic tendencies
```

### 4. Compare two arrangements

```python
# Run on two versions of the same piece
# Compare: key, avg_interval, stepwise_motion
# Find out which one is more stepwise (vocal) vs more leaping (dramatic)
```

### 5. Analyze an entire fleet session

Pipe multiple MIDI files through the theorist to see how agent state transitions map to harmonic changes over time.

---

## How analysis works

```
MIDI file → music21 parse → Pitch extraction → Interval analysis
                                               ├── Key detection
                                               ├── Part counting
                                               ├── Note range
                                               └── Motion characterization
```

---

## Cross-pollination

- Feed MIDI from [text2midi](https://github.com/SuperInstance/fleet-midi-text2midi) → theorist tells you what Rhapsodia generated
- Feed output from [jam-engine](https://github.com/SuperInstance/fleet-jam-engine) → see the arrangement structure
- Compare agent states from [ternary-music](https://github.com/SuperInstance/fleet-ternary-music) → correlate vector patterns with analysis
- Use with [markov](https://github.com/SuperInstance/fleet-midi-markov) → analyze whether generated sequences match the training style

**Next:** [fleet-midi-visualizer](https://github.com/SuperInstance/fleet-midi-visualizer) — see what you just analyzed  
**Next:** [fleet-sheet-music](https://github.com/SuperInstance/fleet-sheet-music) — print what you just analyzed  
**Next:** [fleet-ternary-music](https://github.com/SuperInstance/fleet-ternary-music) — understand the math behind it
