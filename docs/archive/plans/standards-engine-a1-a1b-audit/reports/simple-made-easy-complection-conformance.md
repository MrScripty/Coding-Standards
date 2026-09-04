# Simple Made Easy: Complection Standard Conformance Audit

**Status:** Post-audit research addendum. This report diagnoses the current
standard and proposes general corrections; it does not itself change normative
standards.

**Question:** Does the repository implement the concept of complection from
Rich Hickey's *Simple Made Easy* well enough to steer designs such as A1 and A1b
toward simplicity?

**Verdict:** Not end to end. The Core prose captures two important parts of
Hickey's argument: simplicity concerns entanglement rather than visible size,
and more named things can be simpler than fewer. It does not capture enough of
his operational model, and the planning, decision-fixture, policy-graph, and
admission mechanisms do not enforce even the prose that exists. The result is a
standard that can reward local separation while admitting a globally
complected composition.

## Sources And Transcript Handling

The user-supplied [YouTube URL](https://www.youtube.com/watch?v=8eXiWkPSb50)
currently identifies *Simple Made Easy - Prime Reacts*, a reaction video rather
than Hickey's original presentation. A direct caption track for that reaction
video was not available through the attempted public extraction paths.

The complete acquisition record, timestamped proposition map, quotation limits,
and source cautions are in the companion [primary-source research
report](simple-made-easy-primary-source-research.md). The analysis uses:

1. the official [Strange Loop 2011 session
   page](https://thestrangeloop.com/2011/simple-made-easy.html) and Strange Loop
   Conference's [restored original-talk
   upload](https://www.youtube.com/watch?v=SxdOUGdseq4) as the primary
   audiovisual record;
2. [InfoQ's presentation page and timestamped show
   notes](https://www.infoq.com/presentations/Simple-Made-Easy/) as a
   conference-publisher corroboration; and
3. the community-maintained [full talk
   transcript](https://github.com/matthiasn/talk-transcripts/blob/master/Hickey_Rich/SimpleMadeEasy.md)
   as a secondary cross-check.

The transcript was analyzed but is not reproduced here. This report paraphrases
the talk and supplies timestamps so claims can be checked against the recording.
It does not analyze the reaction host's independent commentary.

## Hickey's Model, Reconstructed As Design Claims

Hickey's argument is broader than “put independent concerns in different
modules.” The following propositions are the parts that can govern a
project-agnostic software standard.

| ID | Proposition | Talk evidence | Standards consequence |
| --- | --- | --- | --- |
| H1 | Simple and easy are different properties. Simple describes whether an artifact is interleaved; easy describes nearness, familiarity, or availability to a person. | 2:02-9:36 | A familiar tool, concise implementation, generated mechanism, or established repository pattern is not simplicity evidence. |
| H2 | Simplicity is an objective artifact property that can be probed. It is not decided by cardinality. | 3:34-4:49 | Counts may locate cost but cannot decide simplicity. One Module may be simple; many Modules may be simple; either may be complected. |
| H3 | Complection is interleaving concerns so they cannot be understood or changed in isolation. Its reasoning cost grows through combinations, not merely addition. | 13:24-13:45; 31:36 | A review must inspect necessary simultaneous knowledge and coordinated change, not just name owners. |
| H4 | Composition and decomposition are not synonyms for simplicity. Nominally modular components remain complex when highly interconnected. Simplicity enables useful partitioning; partitioning does not prove simplicity. | 33:08-35:40 | A file, package, Module, Interface, or service boundary is only evidence when it reduces knowledge or coordination across the boundary. |
| H5 | Constructs generate artifacts with characteristic forms of interleaving. State particularly interleaves value and time; objects may combine state, identity, and value; policies encoded as scattered control flow may interleave why with how. | 28:50; 35:40-46:55 | Reviews should inspect dimensions such as value, identity, time, place, mechanism, and policy. This is a probe, not a universal technology ban. |
| H6 | Simple systems are approached by separating what, who, how, when, where, and why; by keeping information as data; and by isolating implementation behind small abstractions. | 49:17-57:20 | Standards need a multi-dimensional complection review and should assess what callers and composition roots must know. |
| H7 | Tests, refactoring tools, and type systems help reliability but do not enforce simplicity. Every defect escaped the checks that existed before it was found. | 15:45-16:08; 58:10 | Verification evidence cannot be used as evidence that the architecture is simple. Necessity must precede mechanization. |
| H8 | Choosing simplicity may require more thought and initial effort. The relevant result is the produced artifact and its evolution, not the ease of authoring it. | 18:50-21:31; 59:53 | Planning must compare the composed artifacts and representative future changes before implementation, not infer quality from delivery fluency. |
| H9 | Some inherent or environmental complexity cannot be removed. The design task is to avoid adding incidental interleaving around it. | 19:35; 47:22 | A standard should require ownership and containment of necessary complexity, not pretend every hard problem can be made small. |

These propositions support the talk's main benefits: greater ability to
understand, change, debug, and adapt a system. They do not imply that Clojure,
queues, maps, functional programming, or any other specific mechanism must be
used in every repository.

## What The Current Standard Gets Right

The present [Core standard](../../../../../CORE-STANDARDS.md#simplicity-and-ownership)
is meaningfully influenced by the talk:

- It defines simplicity as reduced entanglement and reasoning load, not reduced
  files, types, dependencies, abstractions, or lines.
- It asks whether one concern can be understood or changed without unrelated
  transport, lifecycle, persistence, runtime, UI, timing, or diagnostics
  policy.
- It recognizes that more named components may be simpler and rejects
  cardinality-based decisions.
- It keeps coherent behavior together and permits a boundary when it separates
  independently changing decisions, establishes ownership, or enforces an
  invariant.
- It requires an abstraction to let callers safely ignore an owned concern.

Those are valid H2/H3 ideas. The current wording is much better than a
file-length or “fewest constructs” rule, and it should not be discarded.

The [plan template](../../../../../templates/PLAN-TEMPLATE.md#simplicity-and-ownership-review)
also identifies independent concepts, intentional and accidental coupling,
authority, versions, owners, and future independent changes. That is a useful
starting inventory.

## Where The Standard Is Incomplete

### 1. It lost the simple/easy distinction

Neither the Core section nor its decision fixture distinguishes an objectively
uninterleaved artifact from a tool or approach that is familiar, nearby,
succinct, generated, already available, or easy to author. H1 is not merely
motivational language. It blocks a common false argument:

> This approach is easy for the repository to generate, validate, version, and
> review, therefore it is simple.

A1b is an especially relevant case. Once declarative suites, policy-impact
graphs, generated contracts, exact review procedures, and custom verifiers were
available, adding another governed artifact could be locally routine. That ease
did not reduce the permanent artifact and coordination surface.

### 2. “Separate” is treated too much like the simplicity outcome

The executable
[core-simplicity suite](../../../../../evaluation/standards-effectiveness/suites/core-simplicity.toml)
has `default = "separate"`. Its only positive keep-together rule is one coherent
concern with one change axis. Its
[fixture](../../../../../evaluation/standards-effectiveness/fixtures/core/simplicity-decisions.tsv)
classifies multiple concerns, split ownership, or an invariant boundary as
`separate`.

That model can decide that a decomposition should be considered. It cannot
decide that the resulting system is simple. It has no representation of the
knowledge, ordering, state, version, lifecycle, policy, representation, or
change dependencies between the resulting parts. This misses H4: components
can be separately named and still be braided together.

The dangerous asymmetry is:

- the suite can reject keeping independently changing concerns together; but
- it cannot reject a decomposition whose resulting parts require synchronized
  knowledge and coordinated change.

The outcome vocabulary should therefore distinguish at least `keep-coherent`,
`introduce-boundary`, `composition-review-required`, `complected`, and
`insufficient-facts`. “Separate” is an action, not a simplicity verdict.

### 3. It inventories owners without probing the composed artifact

Current plan questions ask what the independent concepts and owners are. They
do not require answers to the artifact probes implied by H3, H4, and H6:

- What must a maintainer know simultaneously to change each concept?
- Which other owners must change for a representative semantic change, and
  why?
- Which dependencies communicate through stable values or Interfaces, and
  which depend on another Module's representation, lifecycle, ordering, or
  version details?
- What does the composition root need to know about every component?
- Does removing a proposed boundary eliminate responsibility, or only move it
  into callers?
- After decomposition, can the parts actually evolve, test, fail, and be
  replaced independently?

This is the missing distinction between local ownership and global
decomplection.

### 4. The talk's dimensions are only an incidental list

Core mentions transport, lifecycle, persistence, runtime, UI, timing, and
diagnostics. It does not establish a repeatable examination of what, who, how,
when, where, and why, or the common interleavings of state/identity/value/time,
policy/mechanism, and information/representation.

Without those dimensions, “independent concern” is easy to answer at the same
level as the proposed module names. A design can declare Identity, Contracts,
Authority, Engine, and Verification independent while the produced artifact
still requires their versions, codecs, handles, schemas, migrations, graphs,
and tests to move together.

### 5. It does not separate simplicity evidence from reliability evidence

The standards contain extensive acceptance, test, type, schema, verifier, and
coverage machinery. They do not clearly state H7: passing those mechanisms
does not establish simplicity. A correct complicated design remains
complicated, and additional checks can themselves become part of the
complection.

This omission helps create a review ratchet. Once a mechanism or guarantee is
admitted, later review asks whether it is correct, exhaustive, versioned,
persisted, and covered. There is no equally strong checkpoint asking whether
the artifact or guarantee should still exist in the composed design.

### 6. The planning projection is conditional and structurally unenforced

The template says to use the simplicity review for cross-layer, stateful,
contract-heavy, concurrent, or refactor work. The
[Planning workflow](../../../../../workflows/planning.md#required-active-plan-fields)
does not list that review among required active-plan fields. The
plan structure checker (historical path: `evaluation/standards-effectiveness/check-plan-structure.sh`)
does not require its heading or contents.

This is not a hypothetical gap. The initial A1b plan at `f41037bf` contained a
Simplicity And Ownership Review. Commit `44de7dff` replaced the design and
deleted the review. Subsequent C3-C7 replans did not restore it, the structural
checks did not fail, and A1b was ultimately accepted. The applicable standard
existed before A1b began: `f98272c5` had introduced the review in May 2026 and
`42133b83` had retained it in the newer plan template in July.

The governing path was therefore broken:

```text
Core principle
    -> optional template inventory
        -> omitted from replacement A1b plan
            -> not detected by plan validation or admission
                -> no cumulative simplicity decision at acceptance
```

### 7. Simplicity is not a first-class policy-graph unit

The suite is owned by the string `core.simplicity`, but there is no corresponding
fine-grained Core policy-unit declaration and no complete source-owned impact
projection that makes this concept applicable to planning, architecture,
implementation, and review consumers. The repository has machinery capable of
enforcing such relationships, but the simplicity principle itself is not fully
connected through it.

## A1b As A Complection Case Study

The completed A1/A1b audit supplies stronger evidence than file counts alone.
The relevant findings are in the
[architecture comparison](architecture-and-complexity-comparison.md) and
[final synthesis](final-synthesis.md).

### What A1b decomplected

A1b made several genuine improvements:

- JSON Schema validation was separated from identity and owner-local equality.
- Contracts became a deeper Adapter over an external standard instead of a
  second local semantic interpreter.
- Identity owns byte framing and hashing without deciding domain equality.
- Authority does not own domain semantics, and C7 removed significant C6
  machinery.
- Five schema semantic-extension families and the old local Draft interpreter
  were deleted.

These changes should survive an A1c design unless a still deeper replacement
passes the deletion test. The conclusion is not that all separation was bad.

### What remained or became globally complected

Relative to the A1b design base, internal package dependency directions grew
from 22 to 36. The main composition implementation grew from 1,600 to 2,539
lines. Fourteen public object kinds became independently identified, encoded,
stored, dependency-tracked, inspected, versioned, migrated, and verified. A new
public inspectable kind normally crosses nine owner and governance surfaces.

Those counts locate the issue; the change paths establish it. One semantic
addition or correction can require simultaneous knowledge of owner models,
identity, codecs, repository admission, public schema, Engine composition,
migration/policy relationships, coverage identity, and verification. The
2,539-line `engine.py` composition root must coordinate many of these details.

In Hickey's terms, A1b is best described as:

> locally decomplected semantic ownership inside a globally complected
> composition and governance system.

Each Module can have a defensible owner. Each version can have a defensible
scope. Each verifier can prove a real rule. Those local facts do not establish
that the collection can be reasoned about or changed independently.

### Why passing review did not settle simplicity

A1b acceptance established that its selected guarantees were implemented
coherently. It did not establish that all guarantees, independently public
stored kinds, versions, Interfaces, governance interpretations, or permanent
checks were necessary.

This is precisely H7. Testing and formal review made the admitted architecture
more reliable; they could not make it simple. In fact, review findings often
caused additional permanent machinery because the governing question had
already shifted from “should this responsibility exist?” to “is every case of
this responsibility exhaustively enforced?”

## Conformance Verdict

| Layer | Assessment | Reason |
| --- | --- | --- |
| Conceptual intent | **Substantially aligned but incomplete** | Entanglement, reasoning load, coherent concerns, non-cardinality, and abstraction value are present. Simple/easy, artifact focus, composition warning, dimensions, and reliability-tool limits are missing. |
| Normative decision rule | **Partially implemented** | The standard helps decide when concerns should not be co-located, but cannot decide whether the resulting dependencies remain complected. |
| Planning projection | **Weak** | The template contains a useful inventory but no required artifact/change probe or cumulative re-evaluation. |
| Executable fixture | **Mis-shaped for the source concept** | It defaults to separation and models concern attributes, not interconnections after separation. |
| Policy graph | **Incomplete** | Simplicity is not connected as a first-class, fine-grained policy unit across its consumers. |
| A1/A1b application | **Failed at whole-design level** | The applicable review disappeared from the A1b plan without detection, while local ownership and verification reviews admitted a tightly coordinated composition. |

The concise answer is therefore: the complection standard is not properly
implemented as a governing system. Its prose is directionally sound; its
decision model, routing, and admission consequences are not strong enough to
produce Hickey's intended design pressure.

## General Standards Changes Supported By This Analysis

These refinements are project-agnostic. A later normative change should connect
them through Core, Architecture, Planning, Implementation, Verification,
prompts, fixtures, suites, policy units, and policy-impact relationships.

### C1. Define simple, easy, complex, complect, and compose explicitly

- **Simple:** concerns are not interleaved in the produced artifact.
- **Easy:** an approach is familiar, nearby, available, or convenient to its
  current user or environment.
- **Complex/complected:** concerns must be reasoned about or changed together
  because their knowledge, state, timing, location, representation, or policy is
  interleaved.
- **Compose:** place components together; composition is not evidence of
  simplicity.

Require design decisions to use artifact evidence rather than ease of
authoring, generation, availability, familiarity, or existing machinery.

### C2. Pair decomposition with a post-boundary composition test

Retain the current direction to separate independently changing decisions, but
add:

> A boundary is not evidence of simplicity merely because it names an owner or
> moves code. Re-evaluate the resulting dependencies. The boundary reduces
> complection only when callers and peer Modules no longer need unrelated
> representation, state, lifecycle, ordering, location, policy, or version
> details.

This prevents “more components can be simpler” from being misread as “more
components are simpler.”

### C3. Require an objective artifact probe

For material designs and replans, record:

1. the independent concerns and the what/who/how/when/where/why dimensions;
2. state/identity/value/time and policy/mechanism interleavings;
3. caller and composition-root knowledge;
4. representative changes and every semantically forced touched owner;
5. dependencies that carry values or stable Interfaces versus hidden knowledge;
6. whether parts can evolve, test, fail, and be replaced independently;
7. the deletion result for every new permanent boundary or mechanism; and
8. necessary inherent complexity and where it is contained.

Counts remain diagnostic inputs, never verdicts.

### C4. Add cumulative simplicity admission

Re-run the artifact probe when:

- a material architecture is first admitted;
- a systemic finding replaces the design;
- several locally justified Modules, versions, stores, registries, validators,
  or verifiers compose into a new operational obligation; or
- final review observes materially broader change propagation or composition
  knowledge than the plan predicted.

The decision must be able to remove, aggregate, or decline a guarantee, not only
make its implementation more exhaustive.

### C5. Separate reliability evidence from simplicity evidence

State explicitly that tests, types, schemas, generated freshness, coverage,
formal review, and custom verifiers can establish selected correctness claims
but do not establish simplicity. Before permanently mechanizing an internal
failure, require the evidence-necessity and scoped threat/correctness-risk
analysis already proposed by the A1/A1b audit.

### C6. Make applicability and enforcement real

- Make the simplicity/complection review a required active-plan field for
  applicable material work.
- Make plan structure validation reject an applicable plan that omits it or
  leaves its artifact probes unanswered.
- Add a fine-grained Core policy unit for simple/easy/complection.
- Project it to Architecture, Planning, Implementation, Verification, review
  prompts, the plan template, and their policy-impact relationships.
- Require the review again after a replacement plan, rather than treating a
  prior design's review as inherited evidence.

### C7. Replace the current fixture's separation bias

Add cases such as:

| Case | Expected lesson |
| --- | --- |
| One coherent deep Module with one change axis | Keeping it together may be simple. |
| Many Modules sharing schema details, call order, version cutovers, and state | Nominal decomposition remains complected. |
| Familiar framework that scatters state and policy | Easy can be complex. |
| Initially unfamiliar immutable values and functions with independent evolution | Hard can be simple. |
| Modules composed through stable values or narrow Interfaces with no hidden lifecycle knowledge | Composition can remain simple. |
| Tests and verifiers covering every interaction in a braided design | Reliability evidence does not change the complection verdict. |
| Generated machinery requiring one semantic change across many authority surfaces | Generation ease does not remove artifact complection. |
| A boundary deleted with all responsibility absorbed by one coherent owner | Boundary failed the deletion test. |

### C8. Keep Hickey's technology examples advisory

The standards should not ban objects, state, actors, ORMs, conditionals, or
direct calls, nor mandate queues, maps, functional languages, or rule engines.
Those examples illuminate recurring interleavings. A general standard should
ask which dimensions a construct ties together in the actual artifact and
whether the domain requires that coupling.

For example, a direct call is not automatically a defect. It is complecting
when a caller unnecessarily owns the callee's timing or location. A queue is
not automatically simpler; its delivery, ordering, retry, and operational
lifecycle can introduce other interleavings. The standard must decide from the
owned semantics.

## Implication For A1c

Hickey's model supports an A1c design constraint, not a predetermined package
diagram:

> Preserve A1b's demonstrated semantic corrections, then minimize the concerns
> that must be known, changed, versioned, persisted, and verified together for
> each product behavior.

An A1c proposal should be rejected if it merely rearranges A1b into fewer files
or more attractive Modules. It should demonstrate simpler representative
change paths, a smaller composition-root knowledge set, fewer independently
promised lifetimes where no consumer needs them, and deletion of machinery when
its responsibility is not necessary. Conversely, it should retain deep Modules
whose deletion would scatter essential complexity into callers.

## Reproduction Notes

The principal repository observations can be reproduced with:

```bash
git show f98272c5 -- CODING-STANDARDS.md templates/PLAN-TEMPLATE.md
git show 44de7dff^:docs/archive/plans/standards-engine-a1b/plan.md
git show 44de7dff:docs/archive/plans/standards-engine-a1b/plan.md
rg -n 'Simplicity|Independent concepts|Intentional coupling|Accidental coupling' \
  docs/archive/plans/standards-engine-a1b/plan.md
sed -n '27,68p' CORE-STANDARDS.md
sed -n '1,80p' evaluation/standards-effectiveness/suites/core-simplicity.toml
sed -n '1,30p' evaluation/standards-effectiveness/fixtures/core/simplicity-decisions.tsv
sed -n '1,90p' evaluation/standards-effectiveness/check-plan-structure.sh
```
