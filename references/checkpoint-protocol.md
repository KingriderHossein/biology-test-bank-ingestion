# Checkpoint Protocol

The checkpoint is the source of truth for cross-chat continuation.

## Update after every gate

Store:
- repository/workflow version;
- bank ID;
- active year;
- available year order;
- completed gate states;
- expected and observed counts;
- source hashes;
- unresolved exceptions;
- exact next action;
- last validated timestamp if available.

## Resume rule

When asked to continue:

1. Fetch the current checkpoint.
2. Verify the active year.
3. Read `next_action` and unresolved exceptions.
4. Inspect source/output artifacts needed for that action.
5. Continue only that year.
6. Persist the new checkpoint before ending the session.

If the checkpoint conflicts with conversation memory, prefer the checkpoint plus source files and explain the discrepancy.

## GitHub storage rule

Commit checkpoint and non-content metadata. Keep raw copyrighted exam documents and full question-image outputs outside the reusable public repository by default. Record hashes and local/external source identifiers instead.
