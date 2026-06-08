"""Music theory analyzer for MIDI files. Explains key, chords, scales, voice leading."""
import json, music21

def analyze(midi_path: str) -> dict:
    """Analyze a MIDI file and return theory explanation."""
    score = music21.converter.parse(midi_path)
    
    try:
        key = score.analyze('key')
        key_str = str(key)
    except:
        key_str = "Unknown"
    
    parts_info = []
    all_notes = []
    for i, part in enumerate(score.parts):
        notes = list(part.flat.notes)
        note_count = len(notes)
        pitches = sorted(set(n.pitch.midi for n in notes if hasattr(n, 'pitch')))
        pitch_range = (min(pitches), max(pitches)) if pitches else (0, 0)
        
        parts_info.append({
            "part": i,
            "name": part.partName or f"Part {i+1}",
            "note_count": note_count,
            "pitch_range": list(pitch_range),
            "unique_pitches": len(pitches),
            "is_percussion": 128 in pitch_range if pitches else False
        })
        all_notes.extend([n.pitch.midi for n in notes if hasattr(n, 'pitch')])
    
    # Detect intervals
    intervals = []
    for i in range(len(all_notes) - 1):
        intervals.append(all_notes[i+1] - all_notes[i])
    
    avg_interval = sum(intervals) / len(intervals) if intervals else 0
    stepwise_pct = sum(1 for i in intervals if abs(i) <= 2) / len(intervals) * 100 if intervals else 0
    
    return {
        "key": key_str,
        "parts": len(score.parts),
        "part_details": parts_info,
        "total_notes": len(all_notes),
        "avg_interval": round(avg_interval, 2),
        "stepwise_motion_pct": round(stepwise_pct, 1),
        "analysis": f"Key {key_str}, "
                   f"{'stepwise' if stepwise_pct > 60 else 'leap-based'} motion "
                   f"(avg interval {avg_interval:.1f} semitones), "
                   f"{parts_info[0]['note_count'] if parts_info else 0} notes in "
                   f"{parts_info[0]['name'] if parts_info else 'lead'} part"
    }

if __name__ == "__main__":
    import sys
    result = analyze(sys.argv[1])
    print(json.dumps(result, indent=2))
    print(f"\n📊 Analysis: {result['analysis']}")
