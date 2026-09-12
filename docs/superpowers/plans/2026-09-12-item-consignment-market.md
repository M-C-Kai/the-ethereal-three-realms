# Item Consignment Market Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the existing Zhao Gongming / screen-613 bridge into a persistent, real-item consignment market for protocol 1138, excluding pet consignment.

**Architecture:** `consignment_service.py` owns listing persistence, escrowed item instances, validation, instance-id allocation, and transaction rollback. `consignment_protocol.py` owns exact APK request parsing and response encoding. `server.py` only dispatches 1138 requests, calls the service, persists roles, and sends native client frames.

**Tech Stack:** Python 3.12, existing JSON persistence, unittest, custom TLV protocol encoder/decoder.

**Spec:** `docs/superpowers/specs/2026-09-12-consignment-market-design.md`

## Global Constraints

- Implement only item consignment (`object_type=1`); pet consignment (`object_type=3`) remains unsupported.
- Trade real `ItemInstance` dictionaries by their persisted `id`; never manufacture a replacement copy for whole-item trades.
- Whole-item listing removes that instance from the seller bag and places it in escrow.
- Partial stack listing allocates a globally unique new instance id for the escrowed split.
- Use the existing `role['currencies']['silver']` balance and existing bag-capacity rules.
- Actions 2, 4, 7, 9 and 13 must use APK-confirmed field order/types; do not guess response records.
- Any failed transaction must leave roles, escrow, balances and listing state unchanged.
- Do not implement pet market, stall protocol 1731, auction, bidding, cross-server market, mail return, or automatic expiration processing.

---

### Task 1: Reverse-engineer exact 1138 item records

**Files:**
- Modify: `implementation_staging/consignment_protocol.py`
- Test: `implementation_staging/tests/test_consignment_protocol.py`

**Interfaces:**
- Consumes: APK DEX handlers for `pmsj/work/main/e.al(...)` and relevant `pmsj/work/e/*` send sites.
- Produces: strict parsers for list/unlist/buy/my-listings/browse requests and exact native response encoders.

- [ ] **Step 1:** Add protocol tests that assert concrete field types/order for action 9 requests and action 13/7 list responses from the recovered APK structure.
- [ ] **Step 2:** Run `python -m unittest tests.test_consignment_protocol` and verify RED because the new parsers/encoders do not exist.
- [ ] **Step 3:** Implement only the recovered wire shapes in `consignment_protocol.py`, including a reusable item-listing record encoder.
- [ ] **Step 4:** Run the protocol tests and verify GREEN.
- [ ] **Step 5:** Commit `test/feat: define native 1138 item record contract`.

### Task 2: Persistent escrow and listing service

**Files:**
- Create: `implementation_staging/consignment_service.py`
- Create: `implementation_staging/data/consignment_listings.json`
- Test: `implementation_staging/tests/test_consignment_service.py`

**Interfaces:**
- Consumes: `ItemRegistry`, role dictionaries, role item lists, bag capacity, `currencies['silver']`.
- Produces: `ConsignmentService.list_item`, `search`, `my_listings`, `unlist`, `buy`, plus durable listing/escrow state.

- [ ] **Step 1:** Write failing tests for whole-item escrow, partial-stack splitting, unique id allocation, restart reload, own-listing query, category filtering, unlist, purchase, duplicate purchase, insufficient silver, full bag, and self-purchase rejection.
- [ ] **Step 2:** Run `python -m unittest tests.test_consignment_service` and verify RED because `consignment_service` does not exist.
- [ ] **Step 3:** Implement dataclasses/results, JSON load/save, escrow item payloads, listing-id allocation, instance-id scanning/allocation, snapshot rollback, and the five service operations.
- [ ] **Step 4:** Run the service tests and verify GREEN.
- [ ] **Step 5:** Commit `feat: add persistent item consignment service`.

### Task 3: Map item templates to APK consignment categories

**Files:**
- Modify: `implementation_staging/consignment_service.py`
- Test: `implementation_staging/tests/test_consignment_categories.py`

**Interfaces:**
- Consumes: resolved item template metadata such as equipment slot/kind/template category and the APK 28-category table.
- Produces: `consignment_category_for_item(item, registry) -> int` and category matching used by search.

- [ ] **Step 1:** Add failing category tests for weapons, each supported equipment slot, mount slot 17, outerwear, generic items and materials.
- [ ] **Step 2:** Run category tests and verify RED for missing mapping.
- [ ] **Step 3:** Implement deterministic metadata-based mapping; category 0 remains the aggregate weapon category rather than a persisted item category.
- [ ] **Step 4:** Run category/service tests and verify GREEN.
- [ ] **Step 5:** Commit `feat: map real items to native consignment categories`.

### Task 4: Wire 1138 to the service

**Files:**
- Modify: `implementation_staging/server.py`
- Test: `implementation_staging/tests/test_consignment_server.py`

**Interfaces:**
- Consumes: request parsers and `ConsignmentService` operations.
- Produces: server handling for action 2/4/7/9/13 and existing action 3 categories.

- [ ] **Step 1:** Add failing dispatch tests for list, browse, my listings, unlist, buy, unsupported pet listing, and successful silver/item refresh frames.
- [ ] **Step 2:** Run server consignment tests and verify RED.
- [ ] **Step 3:** Instantiate the service from settings, route all supported 1138 requests, call `RoleStore.save()` for changed role state, send native result frames, and explicitly reject pet object type without touching state.
- [ ] **Step 4:** Run server + service + protocol consignment tests and verify GREEN.
- [ ] **Step 5:** Commit `feat: connect protocol 1138 to real consignment transactions`.

### Task 5: End-to-end regression and launcher compatibility

**Files:**
- Modify only if required by latest launcher integration: `implementation_staging/server_dynamic_maps.py`, `implementation_staging/server_with_pets.py`, or current launcher selected by repository state.
- Test: existing consignment entry/category tests plus all new consignment tests.

**Interfaces:**
- Consumes: Zhao Gongming `service=consignment_merchant`, screen 613 bridge, server 1138 handler.
- Produces: one working flow from NPC entry to persistent transaction backend without changing pet protocol behavior.

- [ ] **Step 1:** Run `python -m py_compile consignment_protocol.py consignment_service.py server.py server_dynamic_maps.py` plus every current launcher module.
- [ ] **Step 2:** Run `python -m unittest tests.test_consignment_entry tests.test_consignment_categories tests.test_consignment_protocol tests.test_consignment_service tests.test_consignment_server`.
- [ ] **Step 3:** Run relevant item/mount/shop/pet regression tests so item ownership and launcher changes remain intact.
- [ ] **Step 4:** Fix only regressions caused by the consignment integration and rerun until GREEN.
- [ ] **Step 5:** Commit `test: verify integrated item consignment market`.

### Task 6: Final branch verification

**Files:**
- No production changes unless verification exposes a consignment defect.

**Interfaces:**
- Consumes: all previous tasks.
- Produces: verified feature branch ready for merge/rebase onto current master.

- [ ] **Step 1:** Re-fetch current master and compare for concurrent changes, especially role/pet/item persistence and launcher edits.
- [ ] **Step 2:** Rebase or replay onto the newest master if needed without dropping concurrent work.
- [ ] **Step 3:** Run the full targeted verification suite again and record exact passing commands/results.
- [ ] **Step 4:** Inspect the diff for pet-market leakage, duplicate item creation, non-transactional balance mutation, guessed protocol fields, or accidental data-file fixtures.
- [ ] **Step 5:** Commit any necessary verification-only fixes and report the branch head; merge only with explicit user approval if branch integration is not already authorized.
