"""Pure MCP tool-catalog projection of an already compiled Engine interface.

Tool advertisement lives here; loading installations, connections, domain
execution and result framing remain with their respective composition owners.
"""
from __future__ import annotations

from enum import Enum

from tools.standards_contracts.standards_contracts import (
    CompiledContracts, schema_closure,
)
from .context_projection import Purpose, qualified_operations
from .contract_discovery import (operation_output_schema, output_schema_digest,
                                 OUTPUT_SCHEMA_DIGEST_KEY)


READ_ONLY_OPERATIONS = frozenset(
    {
        "read_many",
        "workflow_status",
        "workflow_details",
        "runtime_info",
        "describe_input",
        "describe_output",
        "resume",
        "find_snapshots",
        "find_proposals",
        "query",
        "query_proposal",
        "preview_application",
        "inspect",
    }
)
FOCUSED_OPERATIONS = frozenset(
    {
        "route",
        "read",
        "read_many",
        "relationship_groups",
        "related",
        "routing_facts",
        "inspect",
        "query_proposal",
        "preview_application",
        "propose",
        "revise",
        "analyze",
        "resolve_workflow",
        "resolve_many",
        "review",
        "apply",
        "recover",
        "workflow_status",
        "workflow_details",
        "runtime_info",
        "describe_input",
        "describe_output",
        "resume",
    }
)
DESCRIPTIONS = {
    "relationship_groups": "Discover registered relationship-group IDs, meanings and traversal policies in one snapshot. Omit snapshot to capture authority; reuse it for related. Default 8, maximum 32 whole records, 16 KiB per page. Follow next exactly. A registered group may have no edges for a target.",
    "describe_output": "Retrieve exact structured-result contracts only when needed. Start with operation; follow next for all records or select a referenced definition with expected_catalog. Combine root_schema_json with all records as $defs to validate a result. schema_digest binds the full output contract, not an approval. Ordinary successful results do not require this extra call.",
    "describe_input": "Discover exact input fields when declarations abbreviate them as unknown. Start with operation only. Read schema_json documents; $refs name selectable definitions. Select a referenced name with selector and expected_catalog from the result. Pages contain up to 16 whole records (default 8), 16 KiB result JSON; follow next unchanged for the complete selected closure. Reuse acquired shapes while catalog_digest matches. No standards state or permissions change.",
    "runtime_info": "Inspect this running interface, catalog and installation identity without opening the standards store. Supply expected_catalog to compare the client catalog. Restart and reconnect after implementation replacement; refresh tools when only the client catalog differs.",
    "resolve_many": "Record 1–128 explicit decisions bound to one exact Analysis context. Each decision retains its ordinary evidence and authorization checks; the final state is recorded atomically. A rejected batch records no decisions. Serialized submissions are limited to 256 KiB. Compact pending results include the first work page. Reuse context with the next explicit batch; fetch workflow_details only for remaining or supporting material.",
    "workflow_details": (
        "Read a section of an immutable historical Analysis. Compact pages contain "
        "up to 16 whole items (default 8) and 64 KiB of result JSON; byte pressure "
        "returns fewer items. Follow next exactly. If one record is oversized, a "
        "rejection offers an explicit detail=full retry for that exact record, "
        "without the compact byte cap. Full retrieval requires limit omitted or "
        "1 and resumes compact paging. Observation binds Analysis, section and "
        "contents, not live evidence. Decision and publication operations check "
        "current evidence and authorization."
    ),
    "read_many": "Read 1–32 selected items from one explicit snapshot in request order. Each item accepts the single-read options. The complete JSON result is limited to 2 MiB; a failed item rejects the whole request. Use the snapshot returned by route or read.",
    "propose": "Create a proposal from explicit change intent and immediately analyze it. Reuse returned context and the bounded pending work page. Omit snapshot to capture accepted authority. Stops at missing evidence or decisions; never reviews or applies automatically.",
    "revise": "Revise the exact proposal referenced by context and analyze the new revision. Supply an atomic change set; use returned pending work directly. Stale contexts cannot select a newer head implicitly.",
    "analyze": "Analyze the exact draft context and return pending work or complete analysis. Propose and revise already analyze; use their returned context and work directly.",
    "resolve_workflow": "Supply one actual evidence or owner-decision submission for pending workflow context. Return the new immutable context, bounded pending work and relative continuations. Prefer resolve_many when several explicit decisions are ready.",
    "review": "Explicitly accept complete analysis using three evidence-backed review decisions. Requires user authorization. Returns readiness as context, without applying.",
    "apply": "Explicitly verify and locally publish the exact accepted workflow context. Requires user authorization. Recovery-required continues only through recover; never retry an interrupted apply.",
    "recover": "Use observe to inspect the original admitted application, or explicitly select complete-publication to revalidate and publish that same candidate. Preserve the original readiness and current recovery authority.",
    "workflow_status": "Observe the exact context with lightweight counts and relative continuations. Use after reconnecting or an unknown outcome, rather than after every successful call. This observation omits inline work and performs no mutation.",
    "resume": "Explicitly select the current revision of the proposal identified by context. Returns a draft context; analysis is a separate next action. Recovery-required must be recovered first.",
    "routing_facts": "Discover snapshot-bound registered routing facts, meanings, types, allowed values, nullability and aliases. Supply known facts to route; missing facts remain unknown. Omit snapshot to capture new accepted authority.",
    "route": "Supply raw known values in facts; omit unknown facts or use a one-field state marker for unknown/known-absent. The selected snapshot supplies fact types. Old type/state/value envelopes are not focused inputs. Route explicit registered facts to applicable standards and required closure. Compact results include selected guidance, all unanswered questions and unresolved-policy counts; use the returned explanation request for full rule details. Omit snapshot to capture new accepted authority; reuse the returned snapshot for subsequent calls. Request content={} for exact selected policy text in this call (default 8, maximum 32 whole reads; 2 MiB total result). Follow content.next as route arguments. Preserve unresolved questions. Omit content for selection only; read_many accepts an explicit subset.",
    "read": "Read exact authoritative policy by canonical ID. Compact detail preserves text and essential authority; full detail includes all relationship rows. Omit snapshot to capture new authority or supply an exact returned snapshot. For navigation authoring, target navigation-indexes to discover registered entrypoint handles, then read a returned navigation ID for its exact content. Navigation results carry authority and are not normative policy.",
    "related": "Traverse explicit permitted relationship groups in an exact snapshot. Discover IDs and meanings with relationship_groups, not guesses. Unknown groups return a bounded vocabulary page. A valid group may return no edges. Preserve authoring-target handles.",
    "create_snapshot": "Capture canonical accepted standards for stable subsequent reads. Reuse the returned snapshot handle.",
    "find_snapshots": "Find durable snapshots to resume a standards workflow.",
    "delete_snapshot": "Delete a snapshot only for an explicitly requested lifecycle change.",
    "undelete_snapshot": "Restore an explicitly selected deleted snapshot.",
    "query": "Route explicit engineering facts to applicable standards and required closure, read authoritative policy by canonical ID, or traverse related policies within one snapshot. Read the router with include_routing to discover registered facts; do not infer missing facts.",
    "inspect": "Inspect a returned opaque handle for authoritative detail.",
    "prepare": "Analyze explicit changes between two accepted snapshots. For proposal authoring use analyze_proposal instead.",
    "resolve": "Submit actual evidence or an authorized owner decision for the current pending Analysis state. Follow returned next_operations.",
    "create_proposal": "Propose an atomic standards change with explicit domain intent and evidence against a snapshot.",
    "find_proposals": "Find durable proposals and their current revision handles.",
    "revise_proposal": "Append an atomic change to the exact expected proposal revision; stale revisions are rejected.",
    "query_proposal": "Read, route, or traverse authoring content within an exact immutable proposal revision. Use preview_application to inspect its application view.",
    "preview_application": "Inspect an exact unpublished revision as an application agent would receive it: every selected or named registered item is delivered with its review_state label (current, changed-since-review or not-reviewed). Supply one read, route, or related request. Results and continuations stay bound to the draft; this operation neither publishes content nor approves review or exposure.",
    "analyze_proposal": "Analyze an exact proposal revision and return unresolved consequences or complete analysis.",
    "review_proposal": "Accept complete current proposal analysis with explicit evidence-backed review decisions; return content-bound readiness. Requires user authorization for review.",
    "verify_proposal": "Verify the exact proposal candidate. Coverage audits require readiness. Verification does not supply review decisions or publish.",
    "apply_proposal": "Verify and publish the exact accepted readiness to the local canonical ref. Requires user authorization for application. On recovery-required use recover_application with the same readiness; never retry apply. Does not push a remote.",
    "recover_application": "Observe the original admitted application or explicitly authorize complete-publication after revalidation. Preserve the selected readiness and application identity.",
    "verify_repository": "Verify the working tree. Refreshing generated verification inputs is a mutation; inspect verification.passed.",
    "maintain_evidence": "Maintain the accepted repository evidence catalog at an exact revision, including explicit retirement of Engine certificates by exact subject and requirement. For draft-only consumers use register-consumer in propose/revise with separate policy relationships. This operation does not edit a proposal or certify coverage.",
}


# Each application description opens with what the tool is for, in plain words.
APPLICATION_DESCRIPTIONS = {
    "routing_facts": "Lists the facts you can state about a task: each fact's exact name, meaning, type and allowed values. Call it once, before your first route, and copy names and values exactly as listed. Omit snapshot to capture the current accepted standards; keep the returned snapshot and pass it to later calls.",
    "route": "Returns the standards that apply to your task. Put the facts that are true of the task in facts, with names and values exactly as routing_facts lists them. Leave out a fact you do not know: it stays unknown and comes back in unresolved_questions. Do not remove a true fact to make a call succeed. For a fact you know is absent use {\"state\":\"known-absent\"}. Pass content={} to receive the text with the selection: reading_plan lists every selected module with its review_state, and content.items holds whole modules for this page. A page is sized for inline display (about 40 KB by default, at most content.limit items, default 8, maximum 32) and always holds at least one whole module. While content.next is present, call route again with exactly those arguments. Every selected module is delivered; review_state (current, changed-since-review or not-reviewed) says whether its text was approved for application use, not whether it applies. Omit snapshot on the first call and pass the returned snapshot afterwards. Omit content for the selection only.",
    "read": "Returns the full text of one standard, example or operational aid by its ID, with its review_state. Use an ID exactly as a route, read or related result gave it; an unregistered ID is rejected, never guessed. detail=full adds the module's relationships. Pass the snapshot you already hold: a module you have read at that snapshot has not changed.",
    "read_many": "Returns the full text of several modules by ID in one call, in the order asked, each with its review_state. Requires the snapshot returned by route or read. Each item gives target and optional detail. Ask for two or three modules per call so your client can show the whole result; the hard limits are 32 items and 2 MiB. An unregistered ID rejects the whole call and returns no items.",
    "related": "Lists how one module relates to others, such as what it requires, specializes or affects. Name the groups to follow: relationship_groups lists the valid group IDs and the directions and transitive traversal each permits. An unknown group returns the valid choices. A valid query with no relationships is a normal empty result.",
    "relationship_groups": "Lists the relationship group IDs that related accepts, with each group's meaning, permitted directions and whether transitive traversal is allowed. Pages hold 8 groups by default (maximum 32, 16 KiB); follow next exactly. Omit snapshot to capture the current accepted standards and reuse the returned snapshot with related. A listed group may have no relationships for a given module.",
    "inspect": "Returns the detail behind a handle that an earlier result gave you: a policy handle returns that module in full, a relationship handle returns that relationship. Pass the handle unchanged.",
    "query": "Advanced form of route, read and related: one native request against an explicit snapshot. Results carry the same review_state labels. Prefer route, read and related.",
    "describe_input": "Shows the exact argument shape of a tool when your client abbreviates a field as unknown. Start with operation only. Read schema_json documents; $refs name selectable definitions. Select a referenced name with selector and expected_catalog from the result. Pages contain up to 16 whole records (default 8), 16 KiB result JSON; follow next unchanged for the complete selected closure. Reuse acquired shapes while catalog_digest matches. No standards state or permissions change.",
    "describe_output": "Shows the exact result shape of a tool. Ordinary results are already structured, so you rarely need it. Start with operation; follow next for all records or select a referenced definition with expected_catalog. Combine root_schema_json with all records as $defs to validate a result. schema_digest binds the full output contract, not an approval.",
    "runtime_info": "Reports which interface version, tool catalog and installation this running server has, without reading any standards. Supply expected_catalog to compare your client's catalog. Restart and reconnect after the server is replaced; refresh tools when only the client catalog differs.",
}


class OutputSchemaDelivery(str, Enum):
    """Host-selected transmission of an unchanged canonical result contract."""

    EAGER = "eager"
    ON_DEMAND = "on-demand"


def tool_catalog(
    interface: CompiledContracts, *, purpose: Purpose | str, advanced: bool = False,
    output_schemas: OutputSchemaDelivery | str = OutputSchemaDelivery.EAGER,
) -> list[dict]:
    # Loading the installation belongs to the caller; this projection is pure.
    contract = interface.project().agent_tools
    definitions = contract["$defs"]
    result = []
    purpose = Purpose(purpose)
    delivery = OutputSchemaDelivery(output_schemas)
    for operation in qualified_operations(contract, purpose):
        name = operation["id"]
        if not advanced and name not in FOCUSED_OPERATIONS:
            continue
        application = purpose is Purpose.APPLICATION
        description = APPLICATION_DESCRIPTIONS[name] if application else DESCRIPTIONS[name]
        if name != "describe_input":
            hint = (
                f'For abbreviated input fields, call describe_input(operation="{name}") '
                "and reuse the returned contract while its catalog matches."
            )
            # An application agent reads the tool's purpose first; the hint follows.
            description = f"{description} {hint}" if application else f"{hint} {description}"
        if purpose is Purpose.AUTHORING and "agent" in operation.get("variants", {}):
            description += (
                " Optional evidence maps request-local names to complete exact evidence references; "
                'use {"evidence_ref":"name"} only in evidence-reference positions. Maximum 128 entries; '
                "every entry must be used. Native validation, expanded size limits and current "
                "evidence/authorization checks still apply. Names do not survive this request."
            )
        output = operation_output_schema(operation, definitions)
        if delivery is OutputSchemaDelivery.ON_DEMAND and name != "describe_output":
            description += f' Exact result contracts: describe_output(operation="{name}") when needed.'
        result.append(
            {
                "name": name,
                "description": description,
                "annotations": {"readOnlyHint": purpose is Purpose.APPLICATION or name in READ_ONLY_OPERATIONS},
                "inputSchema": schema_closure(
                    definitions[operation["input_definition"]], definitions
                ),
                **({"outputSchema": output} if delivery is OutputSchemaDelivery.EAGER else
                   {"_meta": {OUTPUT_SCHEMA_DIGEST_KEY: output_schema_digest(output)}}),
            }
        )
    return result
