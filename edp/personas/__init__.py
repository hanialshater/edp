"""
Persona sources.

  parametric:  fixed (mu, sigma) over 14 signals (paper Section 2.1)
  llm:         text descriptions -> LLM-generated exemplars + needs

Both expose the same interface:

  source.persona_names() -> list[str]
  source.mixture_weights() -> dict[str, float]
  source.true_needs(name) -> dict[need_name, importance]
  source.sample_session(rng, name) -> dict[signal_name, float]
"""
