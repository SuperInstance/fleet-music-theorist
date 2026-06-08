# 📐 fleet-music-theorist

> *MIDI analysis engine — explains key, chords, voice leading, intervals*

Analyze any MIDI file and get a full music theory breakdown: key signature, part structure, note range, interval analysis, stepwise vs. leap-based motion detection.

```bash
python lib/theorist.py path/to/file.mid
```

## Output
```json
{
  "key": "C major",
  "parts": 2,
  "total_notes": 52,
  "avg_interval": 1.2,
  "stepwise_motion_pct": 85.3,
  "analysis": "Key C major, stepwise motion, 52 notes in Piano part"
}
```

## Ennsign: **Sage** — Fleet Theory Officer
**Summon:** `/ensign sage analyze path/to/file.mid`
