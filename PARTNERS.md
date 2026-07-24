# Partners: complete the category

An action layer addresses what an agent **does**. The incidents in this registry classified `needs_judge_or_org` or `out_of_scope` are owned by other reliability and security disciplines. This is an open map. If your product owns one of these lanes, you are invited to map your coverage onto it.

## Open lanes

- Output hallucination / retrieval grounding
- Content safety
- Model alignment / bias
- Evaluation / classification quality
- Context management / long-context degradation
- API security / object-level authorization
- Multi-agent coordination and concurrency
- SDLC / CI-CD controls
- Org data governance / freshness

## How to claim a lane

Open a pull request (see [`CONTRIBUTING.md`](CONTRIBUTING.md)) that maps your product's coverage onto the incidents in a lane: for each incident, a one-line "here is how we handle this" with a link. We review for accuracy and add attribution.

## Principles

- **Honesty first.** Claims are mapped to what a product actually does. We do not overstate coverage, ours or a partner's.
- **One convener, many lanes.** AgentX-Core maintains the registry as the ARE Numbering Authority. It is also one vendor among the lanes: its coverage claims (the action-enforcement and recovery lane) live in its own namespaced rows, held to the same terms as any partner's. Partners own their lanes. This is a standard, not a bake-off.
