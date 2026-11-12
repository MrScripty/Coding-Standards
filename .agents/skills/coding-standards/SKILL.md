---
name: coding-standards
description: Obtain the engineering standards that apply to a coding task from the Standards Engine application tools. Use at the start of any task that plans, writes, changes, reviews, tests, builds, documents, commits or releases code, before planning or editing, and again when the task grows. Not for maintaining the standards themselves; that is the standards-engine authoring skill.
---

# Coding Standards

The Standards Engine holds the engineering standards as modules. You state facts
about your task; it returns every module that applies, with its full text. Read
them before you plan or edit, then follow them.

Use the application-purpose Standards Engine MCP tools. The tool-name prefix
depends on the client (for example `mcp__standards-engine__route`); the operation
names below are exact.

## The Sequence

1. **Get the vocabulary once.** Call `routing_facts` with no arguments. It lists
   every fact: its exact name, meaning and allowed values. Keep the `snapshot` it
   returns.
2. **Route.** Call `route` with that snapshot, the facts that are true of your
   task, and `content: {}`.
3. **Read every page.** `reading_plan` lists every module that applies.
   `content.items` holds the full text of the modules on this page. While
   `content.next` is present, call `route` again with exactly the arguments in
   `content.next`.
4. **Work from what you hold.** Pass the same `snapshot` in every later call. A
   module you already hold at that snapshot has not changed; do not read it
   again.

## Worked Example

Task: implement a Rust function that is called from C.

`route` request:

```json
{
  "snapshot": {"kind": "snapshot-handle", "id": "snapshot:v1:...", "schema_version": 5},
  "facts": {
    "routing.activities": ["implementation"],
    "routing.languages": ["rust"],
    "routing.boundaries": ["interop"]
  },
  "content": {}
}
```

Response outline (nine modules apply; this first page carries two of them):

```text
kind: application-route-result
snapshot: the same handle; keep passing it
status: needs-facts
reading_plan:
  core                           review_state: current
  router                         review_state: current
  workflow.verification          review_state: current
  topic.contracts                review_state: current
  topic.security                 review_state: current
  profile.boundary.interop       review_state: not-reviewed
  profile.language.rust          review_state: current
  profile.language.rust.interop  review_state: not-reviewed
  workflow.implementation        review_state: current
unresolved_questions: routing.applications, routing.details, routing.frameworks,
                      routing.topics, routing.workflow-profiles
content:
  offset: 0
  total: 9
  items:
    - policy.id: core    review_state: current   content: "# Core Standards ..."
    - policy.id: router  review_state: current   content: "# Standards Router ..."
  next: {snapshot, facts, content: {offset: 2, limit: 8}}
```

Call `route` with `content.next` exactly as given, and repeat until a page has no
`next`. All nine modules, including the two labelled `not-reviewed`, are then in
hand.

`status: needs-facts` means some facts were not stated, so the selection may be
incomplete. Look at `unresolved_questions`: if one of those facts is true of your
task, route again with it added and the same snapshot. The modules already
returned still apply.

## Choosing Facts

- Supply what is true of the task. Copy names and values exactly from
  `routing_facts`; a near spelling is rejected, never guessed.
- Omit what you do not know. An omitted fact stays unknown and comes back in
  `unresolved_questions`.
- `[]` states that none of the values apply. Supply it only when you know that;
  do not use it to silence a question.
- Do not delete a true fact to make a call succeed or to shrink the result. A
  rejection tells you what to correct. Fewer facts means missing standards.
- When the task grows (another language, a new boundary), route again with the
  added facts and the same snapshot. Read only the modules you do not yet hold.

## Reading In Small Batches

Most clients show about 50 KB of a tool result inline and divert anything larger
to a file. Route pages are sized to fit: about 40 KB each, and always at least
one whole module. Follow `content.next` until it is absent.

Use `read` for one module by ID and `read_many` for a few. Ask `read_many` for
two or three modules per call so the whole result is shown. IDs come from a
`route`, `read` or `related` result; use them exactly.

## Snapshot Reuse

- Every result returns a `snapshot`. Pass it unchanged in later calls so that
  everything you read comes from one version of the standards.
- Omitting `snapshot` captures the current accepted standards afresh. Do that at
  the start of a new task, not in the middle of one.
- Text held at a snapshot never changes. Do not re-read it to be safe.

## Review Labels

Every `reading_plan` entry and every delivered module carries `review_state`.

| Label | Meaning |
| --- | --- |
| `current` | This exact text was approved for application use. |
| `changed-since-review` | The text was edited after it was approved. |
| `not-reviewed` | The text has never been approved for application use. |

All three are delivered and all apply to your task. The label tells you how
settled the wording is; it is not permission to skip a module. If a module's
wording is unclear, or two modules seem to disagree, tell the user which modules
and what their labels are instead of silently choosing.

## When A Call Is Rejected

| Code | What to do |
| --- | --- |
| `APPLICATION.INPUT_INVALID` | Correct the field named in `input_feedback`. Check fact names and values against `routing_facts`. Keep the facts that are true. |
| `APPLICATION.UNKNOWN_TARGET` | The ID is not registered. Use an ID exactly as `route`, `read` or `related` returned it. |
| `APPLICATION.UNKNOWN_GROUP`, `APPLICATION.TRAVERSAL_NOT_PERMITTED` | Use a group and direction that `relationship_groups` lists. |
| `APPLICATION.RESULT_LIMIT` | Ask for fewer modules in one call. |
| `APPLICATION.INTERNAL_UNAVAILABLE`, `APPLICATION.UNSUPPORTED_CAPTURE` | The server could not answer. Report it to the user; do not guess the standards. |

`related` and `relationship_groups` show how modules relate when you need to
follow a prerequisite. `describe_input` shows an exact argument shape when your
client abbreviates one.
