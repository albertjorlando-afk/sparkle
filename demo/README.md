# Demo: Does Music Help You Code?

We used Sparkle to investigate a question every developer argues about. Here's the claim graph.

## The Graph

```mermaid
graph TD
    C1["<b>C1: Music improves coding<br/>productivity and flow state</b>"]

    E1["E1: Arousal & mood hypothesis<br/>(Husain et al. 2002)"]
    E2["E2: Developer self-reports<br/>(surveys, blogs)"]
    E3["E3: Lo-fi effect — habituation<br/>reduces distraction"]
    E4["E4: Noise masking in<br/>open offices"]

    O1["O1: Lyrics compete for<br/>verbal working memory"]
    O2["O2: Novel/complex music<br/>fragments attention"]
    O3["O3: Selection bias —<br/>correlation ≠ causation"]

    Q1{"Q1: Does it depend on<br/>MUSIC TYPE?"}
    Q2{"Q2: Does it depend on<br/>TASK TYPE?"}
    Q3{"Q3: Is 'productivity' even<br/>the right metric?"}

    I1[/"I1: Music helps routine coding,<br/>hurts complex problem-solving"/]
    I2[/"I2: Instrumental + familiar +<br/>low-complexity = safe zone"/]

    D1{{"D1: Must separate task type<br/>and music type first"}}

    S1(["S1: Context-dependent:<br/>match music to task"])
    S2(["S2: Lo-fi streams work because<br/>they hit the sweet spot"])

    A1["A1: Match music choice<br/>to task complexity"]

    E1 -->|supports| C1
    E2 -->|supports| C1
    E3 -->|supports| C1
    E4 -->|supports| C1

    O1 -.->|contradicts| C1
    O2 -.->|contradicts| C1
    O3 -.->|contradicts| C1

    Q1 ==>|refines| C1
    Q2 ==>|refines| C1
    Q3 ==>|refines| C1
    D1 ==>|refines| C1

    I1 -->|derived_from| Q2
    I2 -->|derived_from| Q1

    S1 -->|derived_from| C1
    S1 -->|derived_from| I1
    S1 -->|derived_from| I2

    S2 -->|derived_from| E3
    S2 -->|derived_from| I2

    A1 -->|derived_from| S1

    classDef claim fill:#4A90D9,stroke:#2C5F8A,color:#fff
    classDef evidence fill:#5CB85C,stroke:#3D7A3D,color:#fff
    classDef objection fill:#D9534F,stroke:#A13A37,color:#fff
    classDef question fill:#F0AD4E,stroke:#C77D1A,color:#000
    classDef inference fill:#9B59B6,stroke:#6C3483,color:#fff
    classDef decision fill:#E67E22,stroke:#A85C16,color:#fff
    classDef synthesis fill:#1ABC9C,stroke:#117A65,color:#fff

    class C1,A1 claim
    class E1,E2,E3,E4 evidence
    class O1,O2,O3 objection
    class Q1,Q2,Q3 question
    class I1,I2 inference
    class D1 decision
    class S1,S2 synthesis
```

> **Legend** &mdash;
> Claims (blue) &nbsp; Evidence (green) &nbsp; Objections (red) &nbsp; Questions (yellow) &nbsp; Inferences (purple) &nbsp; Decision (orange) &nbsp; Synthesis (teal)

## The Takeaway

The original claim — "music helps you code" — is too simple. The graph converges on a nuanced answer:

| Task type | Best audio |
|-----------|-----------|
| Routine (tests, refactors, docs) | Instrumental, familiar, low-complexity music (lo-fi, ambient, game OSTs) |
| Complex (debugging, architecture, code review) | Silence or very minimal ambient sound |

Lo-fi hip hop became the unofficial coding soundtrack because it accidentally optimizes for all three safe-zone dimensions: low complexity, no lyrics, instant familiarity.

## What This Demonstrates

This isn't really about music. It's about what happens when you **structure your thinking** instead of arguing from vibes:

- **Evidence + objections** on the same claim reveal that the real question is more nuanced than the hot take
- **Reframing questions** (Q1, Q2) were the actual breakthrough — not more data
- **Dead ends are tracked**, not hidden — Q3 (abandoned) and O3 (stalled) are still in the graph so you know why they were parked
- **Every conclusion traces back to its sources** — `sparkle why` shows provenance, not hand-waving

## Try It Locally

```bash
git clone <this-repo> && cd sparkle

# Dashboard — see all 17 nodes and 19 edges at a glance
PYTHONPATH=src python3 -m sparkle --store demo/.sparkle/graph.json home

# The root claim's neighborhood — evidence, objections, questions all converging
PYTHONPATH=src python3 -m sparkle --store demo/.sparkle/graph.json tree e036ff896cea

# How was the synthesis derived?
PYTHONPATH=src python3 -m sparkle --store demo/.sparkle/graph.json show ae9ed38241fc

# Full detail on any node
PYTHONPATH=src python3 -m sparkle --store demo/.sparkle/graph.json show dac49e388092
```

## What's in This Directory

| File | What it is |
|------|------------|
| [WALKTHROUGH.md](WALKTHROUGH.md) | The full story — a conversational, 5-act walkthrough of building this graph |
| [exported-research.md](exported-research.md) | Sparkle's markdown export of the complete graph (all node content + edges) |
| `.sparkle/graph.json` | The raw graph data — 17 nodes, 19 edges, fully explorable via CLI |

---

*Built with [Sparkle](../README.md) — claim-graph research with content-addressed provenance.*
