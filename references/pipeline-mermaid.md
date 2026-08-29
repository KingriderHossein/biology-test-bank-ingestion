# End-to-End Pipeline

```mermaid
flowchart TD
    A[New test-bank source] --> B[Create or resume bank checkpoint]
    B --> C{Active year selected?}
    C -- No --> C1[Select exactly one year]
    C1 --> D
    C -- Yes --> D[Gate 0: Source audit and lock]

    D --> D1[Inventory files]
    D1 --> D2[Identify question booklet and official answer key]
    D2 --> D3[Hash immutable sources]
    D3 --> D4[Inspect PDF text quality]
    D4 --> E[Gate 1: Official answer mapping]

    E --> E1[Parse official key]
    E1 --> E2{Expected answers complete?}
    E2 -- No --> E3[OCR/manual recovery and exception handling]
    E3 --> E1
    E2 -- Yes --> F[Gate 2: Render and segment questions]

    F --> F1[Render authoritative pages at high resolution]
    F1 --> F2[Detect question boundaries using reliable layout cues]
    F2 --> F3[Create one source crop per question]
    F3 --> F4{Detected count equals expected count?}
    F4 -- No --> F5[Recalibrate or manually fix boundaries]
    F5 --> F2
    F4 -- Yes --> G[Gate 3: Structured transcription]

    G --> G1[OCR/transcribe each question block]
    G1 --> G2[Preserve raw OCR separately]
    G2 --> G3[Parse stem and options]
    G3 --> G4[Attach official answer and provenance]
    G4 --> H[Gate 4: Context and image handling]

    H --> H1[Detect shared passages and contexts]
    H1 --> H2[Detect image-bearing questions]
    H2 --> H3[Crop each required visual from source]
    H3 --> H4[Save deterministic image assets]
    H4 --> I[Gate 5: Internal extraction QA]

    I --> I1[Check boundaries and option order]
    I1 --> I2[Check mixed Persian/English, formulas, symbols and names]
    I2 --> I3[Check figure-question association]
    I3 --> J[Build Markdown review package]

    J --> J1[Generate one .md file in exam order]
    J1 --> J2[Insert shared contexts once]
    J2 --> J3[Embed relative image links under image questions]
    J3 --> J4[Create validation summary and optional ZIP]
    J4 --> K[Gate 6: Final package QA]

    K --> K1[Count all question headings]
    K1 --> K2[Check missing or duplicate numbers]
    K2 --> K3[Resolve every local image link]
    K3 --> K4[Open every figure crop and inspect clipping/association]
    K4 --> K5[Recheck first, middle, last and section-boundary questions]
    K5 --> K6{Package QA passes?}
    K6 -- No --> I
    K6 -- Yes --> L[Publish to Google Drive / 05_human_review]

    L --> M[Independent human review]
    M --> M1[Reviewer compares Markdown with original booklet]
    M1 --> M2[Reviewer highlights only incorrect parts using ==...==]
    M2 --> M3[If image crop is wrong, highlight its visible image label]
    M3 --> N{Any highlighted errors?}

    N -- Yes --> N1[Verify highlight against authoritative source]
    N1 --> N2[Correct structured dataset or image crop]
    N2 --> J

    N -- No --> O[Gate 7: Human review complete]
    O --> P[Persist final checkpoint]
    P --> Q[YEAR COMPLETE]
    Q --> R[Unlock next year]
    R --> C1

    subgraph Persistence[Persistent state]
        GH[GitHub control plane\nSkill + scripts + configs + checkpoints + Mermaid]
        GD[Google Drive data plane\nSources + working data + validated data + Markdown review package]
    end

    D -. checkpoint .-> GH
    E -. checkpoint .-> GH
    F -. checkpoint .-> GH
    G -. checkpoint .-> GH
    H -. checkpoint .-> GH
    K -. checkpoint .-> GH
    P -. final state .-> GH

    D3 -. source/working artifacts .-> GD
    F3 -. crops .-> GD
    H4 -. figure crops .-> GD
    L -. review package .-> GD
```

## Non-negotiable invariants

- Process one year at a time.
- Do not start the next year before the active year is complete.
- Original sources are immutable.
- Official answer keys are preferred over model inference.
- OCR is a draft, not verified truth.
- Every image-bearing question must preserve the required source visual.
- The canonical human-review deliverable is Markdown plus relative image assets.
- The Markdown package must be reopened and validated before publication.
- Human review remains minimal: highlight only errors; no forms or status tables.