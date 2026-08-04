# Diagnostic Mechanism Recipes

**Standards metadata**

- ID: `reference.recipes.diagnostics`
- Role: `reference`
- Level: `ADVISORY`
- Applies when: A selected Diagnostics contract needs an illustrative implementation mechanism.
- Does not apply when: Diagnostic policy or mechanism selection is unresolved.
- Requires: `topic.diagnostics`
- Specializes: `none`
- Verification: Reference-boundary checks keep examples non-normative and linked to Diagnostics.
- Canonical owner: `reference/recipes/diagnostics.md`

This material is non-normative. Select purpose, audience, context, lifecycle,
disclosure, and failure behavior through [Diagnostics](../../topics/diagnostics.md)
before adapting a mechanism.

## Adapting A Mechanism

Use only the fields, lifecycle observations, propagation, and channel required
by the selected contract. Product APIs, logger calls, trace libraries, context
types, and identifier formats shown here are examples rather than defaults.

## Illustrative TypeScript Logger Adapter

After selecting a synchronous activity lifecycle and a logger channel, an
adapter might project selected start, completion, and failure observations:

```typescript
type ActivityContext = {
  operationId: string;
  parentOperationId?: string;
};

function withActivity<T>(context: ActivityContext, operation: () => T): T {
  logger.debug("operation started", selectedFields(context));
  try {
    const result = operation();
    logger.debug("operation completed", selectedFields(context));
    return result;
  } catch (error) {
    logger.error("operation failed", safeFailureFields(context, error));
    throw error;
  }
}
```

This example is not valid for asynchronous completion merely because the
callback returns a promise. It does not select the identifier format, logger,
events, fields, disclosure policy, or failure behavior, and it must not log raw
context or replace the operation outcome.
