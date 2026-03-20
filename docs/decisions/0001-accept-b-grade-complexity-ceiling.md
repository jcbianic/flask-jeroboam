# 0001. Accept B-grade complexity ceiling for intrinsically complex blocks

**Date**: 2026-03-20

**Status**: Accepted

## Context

During the integration of xenon complexity enforcement (issue #134), all
functions in `flask_jeroboam/` were audited using radon. Two blocks ranked C
(complexity 11) were refactored down to B. Three further B-ranked blocks were
cleanly reduced to A by extracting focused helpers:

- `_format_error()` extracted from `SolvedArgument.validate_request`
- `_get_body_schema()` extracted from `_get_openapi_operation_request_body`
- `_collect_models_from_view()` extracted from
  `_get_flat_models_from_jeroboam_views`
- `_unpack_body_values()` extracted from `_parse_and_validate_inbound_data`
- `_collect_jeroboam_views()` and `_filter_definitions()` extracted from
  `build_openapi`

Nine B-ranked blocks (complexity 6-9) remained after these refactors. The
question was whether to force all of them to A grade (complexity <= 5) to
enable a stricter xenon threshold.

## Decision

Keep the xenon threshold at `--max-absolute B --max-modules B --max-average A`.
The nine remaining B-ranked blocks are not refactored because their complexity
is intrinsic to the problem they solve, not incidental. Forcing them to A would
require artificial fragmentation that harms readability without improving
correctness.

The nine blocks and their justification:

- **`InboundHandler._build_body_field` (9)** - Acknowledged tech debt; existing
  TODO comments in source flag it for a future refactor.
- **`build_openapi` (8)** - Orchestration function; extracting the loop creates
  awkward multi-argument helpers with no semantic benefit.
- **`SolvedArgument.validate_request` (7)** - Just refactored to B; further
  splitting would obscure the validation flow.
- **`OutboundHandler._adapt_datastructure_of` (7)** - Type-dispatch by design;
  the elif chain is the correct pattern for this use case.
- **`_unwrap_optional` (7)** - Handles two Union syntaxes (`typing.Union` and
  `types.UnionType`); complexity is the spec, not the implementation.
- **`_build_openapi_path_item` (7)** - Orchestration function; same
  fragmentation risk as `build_openapi`.
- **`InboundHandler._solve_body_field_info` (6)** - Three content-type
  branches plus one sub-check; inherent to the logic.
- **`_add_responses` (6)** - Two independent conditionals on different
  concerns; no natural extraction point.
- **`SolvedBodyArgument` class (6)** - Class-level metric reported by radon;
  not a function that can be reduced by extraction.

## Consequences

### Positive

- All future code is blocked at complexity B by CI; no new C or worse blocks
  can be introduced unnoticed.
- The nine existing blocks are documented here as deliberate exceptions, making
  the threshold meaningful rather than arbitrary.
- The `--max-average A` threshold remains strict, preventing overall drift even
  if individual B blocks persist.

### Negative

- `InboundHandler._build_body_field` (score 9) sits close to C territory and
  should be the first candidate for refactoring when the inbound handler is
  revisited. Its existing TODO comments already flag this.
- The B ceiling means a contributor adding a moderately complex function
  (score 6-9) would not be caught by xenon, even though A is preferred.

## Alternatives Considered

### Force all blocks to A (--max-absolute A)

Would require breaking all nine functions into smaller pieces. For type-dispatch
functions (`_adapt_datastructure_of`) and Union-handling utilities
(`_unwrap_optional`), this means introducing unnecessary indirection or
restructuring code in ways that make it harder to follow. Rejected because the
metric improvement would come at the cost of code clarity.

### Keep the C threshold as baseline

The initial xenon integration proposed `--max-absolute C` to match the two
C-ranked functions that existed before refactoring. Rejected because C is too
permissive for a library codebase and would provide weak protection against
complexity creep.
