# Walkthrough: Does Music Help You Code?

Every developer has a take on coding with music. The lo-fi crowd swears by it. The silence purists think you're all fooling yourselves. Most of those takes are vibes, not evidence.

Let's fix that. We're going to use Sparkle to build a claim graph — starting with the hot take, stress-testing it with real research, and seeing where structured thinking actually leads.

---

## Act 1: The Claim

Every investigation starts somewhere. Ours starts with the thing half your team believes and the other half rolls their eyes at.

```bash
PYTHONPATH=src python3 -m sparkle --store demo/.sparkle/graph.json add-node \
  --type claim \
  --title "Listening to music while coding improves productivity and flow state" \
  --content "The widespread belief among developers that background music enhances coding performance..." \
  --confidence 0.5 --status active --tags root music coding productivity
```

<details>
<summary>Output</summary>

```
Added node e036ff896ceafc7b39391b43d5139b4bcc3a31812d6c516af55add5fcc10ccb2
```
</details>

Confidence starts at 0.5 — we genuinely don't know yet. That's the point. A claim graph isn't about defending your priors, it's about mapping the terrain.

---

## Act 2: The Evidence

Time to find what actually supports this claim. Not "my friend says so" — actual research.

### The arousal and mood hypothesis

Husain et al. (2002) showed that music modulates arousal and mood, which in turn affect cognitive performance. The famous "Mozart Effect" turned out to be about arousal, not Mozart. If music puts you in a good mood and at the right energy level, you think better.

```bash
PYTHONPATH=src python3 -m sparkle --store demo/.sparkle/graph.json add-node \
  --type evidence \
  --title "The arousal and mood hypothesis: music elevates mood and arousal, improving task performance" \
  --content "..." --confidence 0.7 --status active
```

### Developer self-reports

About 70% of developers in the JetBrains 2022 survey listen to music while coding. That's a lot of anecdotal evidence. But self-report data has obvious limitations — people aren't great at measuring their own productivity.

### The lo-fi effect

Here's the interesting one. Research on auditory habituation shows the brain deprioritizes predictable stimuli. Familiar, repetitive music becomes "sonic wallpaper." This is exactly why lo-fi hip hop streams work — the music is *deliberately boring enough* not to grab your attention.

### Noise masking

Open office research shows music can mask distracting speech. But this might be about masking noise rather than music helping per se — white noise could do the same thing.

<details>
<summary>All four evidence nodes linked to the claim</summary>

```
PYTHONPATH=src python3 -m sparkle --store demo/.sparkle/graph.json add-edge \
  --from 904a9ec508dc --to e036ff896cea --relation supports
PYTHONPATH=src python3 -m sparkle --store demo/.sparkle/graph.json add-edge \
  --from 7d03d6edf299 --to e036ff896cea --relation supports
PYTHONPATH=src python3 -m sparkle --store demo/.sparkle/graph.json add-edge \
  --from 6add940e9a0a --to e036ff896cea --relation supports
PYTHONPATH=src python3 -m sparkle --store demo/.sparkle/graph.json add-edge \
  --from 3e7c596aaa90 --to e036ff896cea --relation supports
```
</details>

Four pieces of evidence, all supporting the claim. If we stopped here, we'd conclude music definitely helps. But that's not how good thinking works.

---

## Act 3: The Pushback

Now let's stress-test the claim. What weakens it?

### Lyrics kill your code-reading ability

Perham & Vizard (2011) found that music with lyrics significantly impairs reading comprehension and serial recall. Since coding is fundamentally reading and parsing text — variable names, function signatures, error messages — lyrical music creates a dual-task conflict. Your brain literally cannot process two streams of language without cost.

### Novel music hijacks attention

That death metal album you just discovered? Terrible debugging music. Cognitive load theory explains why: novel, complex music demands attention because your brain treats unpredictable stimuli as worth monitoring. The unexpected breakdown at 3:47 just derailed your stack trace.

### The selection bias problem

Here's a sneaky one: people often put on music when they're *already* settling into focus mode. The music gets associated with flow states it didn't cause. The ritual of putting on headphones says "do not disturb" — and it might be the signal, not the sound, doing the work.

<details>
<summary>Three objections linked to the claim</summary>

```
PYTHONPATH=src python3 -m sparkle --store demo/.sparkle/graph.json add-edge \
  --from dac49e388092 --to e036ff896cea --relation contradicts
PYTHONPATH=src python3 -m sparkle --store demo/.sparkle/graph.json add-edge \
  --from 3ea2353452f9 --to e036ff896cea --relation contradicts
PYTHONPATH=src python3 -m sparkle --store demo/.sparkle/graph.json add-edge \
  --from 0ac25a502795 --to e036ff896cea --relation contradicts
```
</details>

Now our graph has tension. Evidence on both sides. This is where most Slack debates stop — "well, it depends" — and everyone goes back to their existing opinion. But we can do better.

---

## Act 4: The Pivot

The best move in structured thinking isn't finding more evidence — it's asking better questions.

### Does the music type matter?

Instead of "does music help?" we should ask "which music, under what conditions?" Instrumental vs. lyrical, familiar vs. novel, simple vs. complex — these dimensions matter more than the yes/no binary.

### Does the task type matter?

Writing boilerplate CRUD endpoints is cognitively very different from debugging a race condition. Routine tasks leave spare cognitive capacity that music can fill. Complex tasks demand full working memory, leaving no room for music processing.

### Are we measuring the wrong thing?

Maybe productivity isn't the point. If music makes an 8-hour coding day more sustainable, does a small performance hit matter? This is a valid reframe, but it moves us from empirical territory into values — so we park it.

<details>
<summary>Three reframing questions linked to the claim</summary>

```
PYTHONPATH=src python3 -m sparkle --store demo/.sparkle/graph.json add-edge \
  --from 02643de22a09 --to e036ff896cea --relation refines
PYTHONPATH=src python3 -m sparkle --store demo/.sparkle/graph.json add-edge \
  --from bbbf66cdb1b7 --to e036ff896cea --relation refines
PYTHONPATH=src python3 -m sparkle --store demo/.sparkle/graph.json add-edge \
  --from 076dde2c5212 --to e036ff896cea --relation refines
```
</details>

Notice how Q3 got status `abandoned` — not because it's wrong, but because it takes us off-track. A good claim graph tracks dead ends too, so you know why they were abandoned.

---

## Act 5: Putting It Together

Now the fun part. We've got evidence, objections, and better questions. What emerges?

### Two inferences

**Music helps routine work, hurts complex work.** Combining cognitive load evidence with the task-type question: when coding is mechanical, music fills spare capacity productively. When it demands full working memory, music is a tax.

**The "safe zone" is instrumental + familiar + low-complexity.** Cross-referencing the music-type question with the lyrics objection and habituation evidence: lo-fi, ambient, and video game soundtracks aren't just popular — they're cognitively optimal.

### The decision

We can't make any general claim without separating task type and music type. The original question was too coarse. A 2x2 matrix (routine vs. complex × low-load vs. high-load music) is the minimum useful framework.

### The synthesis

> **Music while coding is context-dependent: instrumental/familiar music helps routine work; silence is better for complex debugging and design.**

Neither the "always on" crowd nor the "silence purists" are right. The interaction between music characteristics and task demands is the key insight.

And here's why lo-fi hip hop became the unofficial coding soundtrack: it *accidentally optimizes for all three safe-zone dimensions* — low complexity, no lyrics, instant familiarity. The "lofi girl" streams aren't just a meme. They're an emergent solution to a real cognitive optimization problem.

### The recommendation

**Match your music to your task.** Routine work → lo-fi playlist. Complex debugging → silence. The meta-skill isn't finding the perfect playlist — it's knowing when music helps and when it steals resources you need.

<details>
<summary>Full provenance chain for the synthesis</summary>

```
$ PYTHONPATH=src python3 -m sparkle --store demo/.sparkle/graph.json show ae9ed38241fc

SYNTHESIS  promising  0.80
Music while coding is context-dependent: instrumental/familiar music helps routine work;
silence is better for complex debugging and design

Incoming
  derived_from
    C claim      f39877ad639f  Developers should consciously match music choice...
Outgoing
  derived_from
    ~ inference  a5fca945779c  Instrumental, familiar, low-complexity music is the safe zone
    C claim      e036ff896cea  Listening to music while coding improves productivity...
    ~ inference  bb49a450f527  Music helps for routine/mechanical coding but hurts...
```

The synthesis derives from the root claim + both inferences, and the recommendation derives from the synthesis. Every link is explicit. No hand-waving.
</details>

---

## The Full Picture

Let's see what we built:

```
$ PYTHONPATH=src python3 -m sparkle --store demo/.sparkle/graph.json home

SPARKLE HOME
Store: demo/.sparkle/graph.json
Nodes: 17
Edges: 19

By type
  claim              2
  decision           1
  evidence           4
  inference          2
  objection          3
  question           3
  synthesis          2

By status
  abandoned          1
  active             11
  promising          3
  stalled            1
  weakly_supported   1
```

```
$ PYTHONPATH=src python3 -m sparkle --store demo/.sparkle/graph.json tree e036ff896cea

claim e036ff896cea  Listening to music while coding improves productivity and flow state
Incoming:
├─ contradicts  objection  3ea2353452f9  Complex or novel music draws attention...
├─ contradicts  objection  dac49e388092  Music with lyrics competes for verbal working memory...
├─ contradicts  objection  0ac25a502795  Selection bias...
├─ derived_from synthesis  ae9ed38241fc  Music while coding is context-dependent...
├─ refines      question   bbbf66cdb1b7  Does it depend on the TYPE of coding task...
├─ refines      question   02643de22a09  Does the answer depend on the TYPE of music...
├─ refines      question   076dde2c5212  Is productivity even the right metric...
├─ refines      decision   469f2284789f  Must separate task type and music type first
├─ supports     evidence   7d03d6edf299  Developers self-report higher focus...
├─ supports     evidence   3e7c596aaa90  Music can mask distracting office noise...
├─ supports     evidence   6add940e9a0a  Repetitive and familiar music reduces novelty...
└─ supports     evidence   904a9ec508dc  The arousal and mood hypothesis...
```

17 nodes. 19 edges. One root claim → evidence and objections → reframing questions → inferences → synthesis → actionable recommendation. That's what structured thinking looks like.

---

## What Did We Learn?

Not just about music — about the *process*:

1. **Start with the claim, not the conclusion.** We began at 0.5 confidence and let the graph tell us where to land.
2. **Objections are features, not bugs.** The contradictions forced us to refine the question instead of cherry-picking evidence.
3. **Reframing > more evidence.** The breakthrough was Q1 and Q2 — asking *better* questions, not finding more data points.
4. **Dead ends are valuable.** Q3 (abandoned) and O3 (stalled) are still in the graph. Future investigators can see why we parked them.
5. **Provenance is accountability.** Every synthesis traces back to specific evidence and reasoning. No vibes.

The next time someone on your team says "music definitely helps me code," you'll know the real answer is: *it depends, and here's exactly how.*

---

*Built with [Sparkle](../README.md) — claim-graph research with content-addressed provenance.*
