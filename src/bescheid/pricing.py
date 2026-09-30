"""Token prices used to report cost per document.

Prices are USD per million tokens, list prices as of 2026-09. Update them when
they change; results files store the computed cost, so old runs stay comparable.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Price:
    input_per_mtok: float
    output_per_mtok: float


PRICES: dict[str, Price] = {
    "claude-opus-5-5": Price(4.00, 20.00),
    "claude-sonnet-5-5": Price(2.00, 10.00),
    "claude-haiku-4-5": Price(1.00, 5.00),
}


def cost_usd(model: str, input_tokens: int, output_tokens: int) -> float | None:
    """Return the cost of one request, or None if the model has no known price."""
    price = PRICES.get(model)
    if price is None:
        return None
    return (input_tokens * price.input_per_mtok + output_tokens * price.output_per_mtok) / 1e6
