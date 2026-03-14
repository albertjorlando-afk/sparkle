# Archived Reference: Merkle DAG for Research

**User:** Anonymous (albertjorlando@gmail.com)  
**Created:** 2026-03-14 11:08:26  
**Updated:** 2026-03-14 11:11:48  
**Exported:** 2026-03-14 11:12:37  
**Original Link:** https://chatgpt.com/c/69b579e3-3cf8-8331-8d8d-185381cbbb01

This file preserves the original concept conversation that shaped Sparkle's first MVP.

---

## Prompt

I've recently learned about merkle trees and i had an idea about I recently learned about Merkle trees, and I had an idea a while ago that you could create a Git-styled pathfinding program that allowed you to do research down particular paths of inquiry and loop back if they didn't meet your needs for whatever reason, and that allowed you to preserve like a distinct path with provenance through the chain of thoughts and select one or more research paths to then extract or use for a particular idea.

## Response

Yes — that idea is genuinely solid.

What you’re describing is basically a research version of a Merkle DAG, where each step in inquiry is a content-addressed node, and each branch represents a distinct reasoning or evidence path. That gives you a few really powerful properties:

**Provenance.**  
Every note, source, summary, inference, or decision can point to its parents. So when you end up with a conclusion, you can reconstruct exactly how you got there.

**Branching without loss.**  
You can explore “maybe this theory is right” on one branch and “maybe the opposite is right” on another, without overwriting anything. If one path turns out weak, you just stop advancing it.

**Reproducibility.**  
Because nodes are hashed by content, identical intermediate results collapse naturally. Two different research paths that arrive at the same synthesis can literally share structure.

**Selective extraction.**  
You could “check out” a branch or merge several branches into a final artifact: a memo, design doc, literature review, proposal, or plan.

The interesting part is that this is not just note-taking and not quite a normal knowledge graph either. It’s closer to:

- Git’s object model
- a lab notebook
- a claim/evidence graph
- a decision tree with reversible history

A good mental model is:

- **Blob** = source excerpt, note, quote, observation
- **Tree** = organized bundle of related items
- **Commit** = “at this point, my working interpretation is X”
- **Branch** = line of inquiry
- **Merge** = combine multiple lines into a synthesis
- **Tag** = “candidate final,” “publishable,” “discarded,” “needs verification”

What makes this version especially interesting is the phrase “distinct path with provenance through the chain of thoughts.” That suggests each node should probably distinguish between different types of things:

- raw evidence
- interpretations
- hypotheses
- decisions
- open questions
- extracted outputs

That separation matters, because otherwise the graph becomes a pile of thoughts with no boundary between “what the source said” and “what I inferred.”

A minimal schema could look like this:

```text
Node {
  id: hash(content + metadata + parent_ids)
  type: source | note | claim | question | synthesis | decision
  content: ...
  parents: [node_id...]
  citations: [source_node_id...]
  author: ...
  timestamp: ...
  confidence: ...
  status: active | abandoned | superseded | merged
}
```

Then a “research path” is just a traversable subgraph ending in some synthesis node.

The most valuable feature would probably be first-class branch evaluation. For example, each branch could carry:

- confidence score
- evidence coverage
- unresolved objections
- cost/time spent
- reason for abandonment

That way “looping back” is not just deleting work — it becomes a documented decision: “this path was explored, here’s why it was not good enough.”

That is something normal docs and notebooks are terrible at.

The main design trap is this: if you model everything as immutable thought nodes, the system can become noisy and hard to use. In practice, you’d likely want:

- immutable underlying provenance objects
- editable working views on top
- curated “checkpoints” rather than saving every micro-thought

Otherwise it turns into a chain-of-thought archive instead of a research tool.

So the strongest version of the idea is probably:

**A Git-like research environment built on a Merkle DAG, where questions, evidence, claims, and syntheses are content-addressed nodes; branches represent competing lines of inquiry; merges produce reusable outputs; and every conclusion remains traceable to its source path.**

The next thing to define is whether the primary unit is a claim graph or a workspace snapshot. Claim graph makes it more semantic and reasoning-oriented; workspace snapshot makes it feel more like Git. For research, the recommendation was a claim graph underneath with snapshot-style views on top.

## Prompt

right now, thinking of this a solo research tool. I am leaning more toward a claim graph

## Response

That makes sense. For a solo tool, a claim graph is probably the better foundation than a Git-style filesystem model.

Git is great for versioning files, but what you actually care about is more like:

- what am I trying to establish
- what supports it
- what weakens it
- what alternative paths did I explore
- why did I keep or reject each path

That is much closer to a claim-centered research notebook than a document tree.

A strong core model would be:

- **Claim**: A statement you might want to use later.
- **Evidence**: A source, quote, observation, or experiment result that supports or challenges a claim.
- **Inference**: A reasoning step that connects evidence to a claim.
- **Question**: An unresolved point that opens a new branch.
- **Counterclaim / objection**: Something that pressures the claim.
- **Decision**: A recorded choice like “good enough to keep,” “needs more support,” or “abandon this branch.”

That gives you a graph where the important edges are things like:

- supports
- contradicts
- refines
- depends_on
- answers
- derived_from
- supersedes

The nice part is that this naturally preserves provenance without forcing you to think in files and folders first.

For a solo workflow, the main object should not be the note but the claim card. Each claim card would show:

- the claim itself
- confidence
- status
- supporting evidence
- objections
- descendant claims
- source path back to origin

Then branching becomes intuitive. A claim can spawn:

- a supporting branch: “what would strengthen this?”
- an adversarial branch: “what would make this false?”
- an application branch: “how would this be used in practice?”
- a reframing branch: “is this actually the wrong question?”

That is more useful for research than ordinary mind maps, because the branches are typed and evaluable.

For immutability, the recommendation was to avoid storing “thoughts” as one long chain. Instead, store atomic research objects as content-addressed nodes, and let the UI present editable views on top. That way:

- the underlying provenance stays stable
- you can revise wording without corrupting history
- duplicate evidence can be reused across multiple claims
- converging branches can merge cleanly

The distinction:

- **Immutable layer**: node contents, links, timestamps, source references
- **Working layer**: labels, grouping, drafting, temporary views, ranking

For a solo tool, the most important UX feature is branch triage. Not every branch should feel equally alive. Each branch should have a visible state such as:

- active
- stalled
- weakly supported
- promising
- abandoned
- harvested

“Harvested” is useful because it means “I’m done exploring this path, but I want to reuse its outputs elsewhere.”

That gives you the loop-back behavior: not deleting a path, but marking it as explored and preserving the reason.

The MVP proposed in the conversation was:

1. Create a claim.
2. Attach evidence, objections, and child claims.
3. Let every node be linkable and content-addressed.
4. Show lineage for any claim.
5. Allow exporting a selected subgraph into a linear narrative.

The design principle to anchor the whole tool:

**The tool should help you build claims that are inspectable, challengeable, and reusable.**

One especially good constraint for a solo version:

- What is the claim?
- Why do I think it?
- What would change my mind?
- What depends on this being true?
- What branch did this come from?

The final framing from the conversation:

- **Conceptually:** claim graph
- **Operationally:** branching inquiry workspace
- **Technically:** Merkle DAG underneath
