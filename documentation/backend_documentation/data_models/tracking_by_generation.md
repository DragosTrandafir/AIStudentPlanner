# Generation Tracking (generation_id)

The `generation_id` is a UUID that groups all plans and tasks created from a single schedule generation.

## Purpose

- Track schedule versions
- Link feedback to specific generations
- Enable regeneration workflows
- Maintain complete history

## Lifecycle

### Initial Generation

```
User submits subjects and time availability
         ↓
Backend creates generation_id (UUID)
         ↓
Backend creates Plan records for each day with this generation_id
         ↓
Backend creates AITask records linked to Plans
         ↓
User sees schedule in frontend
```

### After Feedback

```
User submits feedback for current generation
         ↓
Backend stores Feedback with same generation_id
         ↓
User clicks "Regenerate"
         ↓
Backend creates NEW generation_id (different UUID)
         ↓
Backend creates NEW Plan & AITask records with new generation_id
         ↓
Previous generation remains (for history)
         ↓
User sees improved schedule
```

## Example

```
Generation 1: gen-abc123
├─ Plan (date: 2026-01-13, generation_id: gen-abc123)
│  ├─ AITask: Calculus Chapter 3 (120 min)
│  └─ AITask: Physics Lab Report (180 min)
├─ Plan (date: 2026-01-14, generation_id: gen-abc123)
│  └─ AITask: Calculus Problem Set (150 min)
└─ Feedback: rating 3/5, "too busy on Jan 13"

Generation 2: gen-def456 (after feedback)
├─ Plan (date: 2026-01-13, generation_id: gen-def456)
│  ├─ AITask: Calculus Chapter 3 (90 min)
│  └─ AITask: Physics Lab Prep (60 min)
├─ Plan (date: 2026-01-14, generation_id: gen-def456)
│  ├─ AITask: Calculus Problem Set (150 min)
│  └─ AITask: Physics Lab Report (120 min)
└─ Feedback: (none yet)
```

## Key Properties

- UUID format, unique per generation
- Created when `/plans/generate` is called
- All plans from same generation share same generation_id
- New generation_id for each regeneration (after feedback)
