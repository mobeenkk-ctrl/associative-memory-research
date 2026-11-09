# Associative Memory & Organisational Workflow Discovery

**Experimental research prototypes** exploring associative activation in AI memory and discovery of organisational workflows.

> Research status: working toy demonstrations using synthetic data. Not a trained cognitive model, not a production agent, and not evidence of performance superiority.

## Quick start

Requires Python 3.10+; no dependencies.

```bash
python3 demo.py
python3 -m unittest -v test_memory.py
python3 workflow_mapper.py
```

## Memory demonstration

`memory_engine.py` implements a graph of memory nodes containing text, goals, salience, timestamps, and weighted links. It scores direct lexical/goal relevance, then spreads activation one hop through associations. It supports explicit link updates and JSON persistence.

`demo.py` compares direct-only scoring with spreading activation over five synthetic procurement memories. A supplier-onboarding question can activate an indirectly related insurance-expiry memory. **The manually specified dependency edge is part of the example**, not automatically discovered causality.

`test_memory.py` checks association activation, persistence, link updates, and no-feedback mode.

## Workflow discovery

`workflow_mapper.py` takes synthetic process event traces, reconstructs transitions and human handoffs, and **proposes** a document-checking agent. It does not generate or deploy agents.

## Research questions

- How can memory associations be learned and updated from grounded evidence rather than lexical coincidence?
- How should salience, causal proximity, recency, uncertainty, goals, and usage affect activation?
- Can an agent infer undocumented workflows from incomplete observations?
- Can it safely generate, test, and deploy narrowly scoped capabilities after validating a discovered need?

## Limitations and evaluation plan

The current baseline is a local ablation (direct relevance with spreading disabled), **not** a benchmark against retrieval-augmented generation or commercial memory products. Future evaluations should use labelled multi-session tasks, matched context budgets, recall@k, task success, error rates, latency, and cost. Workflow discovery needs real permissioned traces and ground-truth process maps.

## Supporting documents

Research PDFs and an evidence/reproduction guide are available in the accompanying [portfolio ZIP](https://github.com/mobeenkk-ctrl/associative-memory-research) when uploaded separately. Source code and tests are available directly in this repository.

## Scope

This repository intentionally uses only synthetic business data. It contains no customer credentials, private company records, or production integrations.
