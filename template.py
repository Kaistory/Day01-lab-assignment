"""
Day 1 — LLM API Foundation
AICB-P1: AI Practical Competency Program, Phase 1

Instructions:
    1. Fill in every section marked with TODO.
    2. Do NOT change function signatures.
    3. Copy this file to solution/solution.py when done.
    4. Run: pytest tests/ -v
"""

import os
import time
from pathlib import Path
from typing import Any, Callable


def _load_dotenv() -> None:
    """Lightweight .env loader (no external dependency).

    Reads KEY=VALUE lines from a .env file next to this script and sets any
    that are not already present in the environment.
    """
    env_path = Path(__file__).with_name(".env")
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_dotenv()

# ---------------------------------------------------------------------------
# Estimated costs per 1K OUTPUT tokens (USD) — update if pricing changes
# ---------------------------------------------------------------------------
COST_PER_1K_OUTPUT_TOKENS = {
    "gpt-4o": 0.010,
    "gpt-4o-mini": 0.0006,
}

OPENAI_MODEL = "gpt-4o"
OPENAI_MINI_MODEL = "gpt-4o-mini"


# ---------------------------------------------------------------------------
# Task 1 — Call GPT-4o
# ---------------------------------------------------------------------------
def call_openai(
    prompt: str,
    model: str = OPENAI_MODEL,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float]:
    """
    Call the OpenAI Chat Completions API and return the response text + latency.

    Args:
        prompt:      The user message to send.
        model:       The OpenAI model to use (default: gpt-4o).
        temperature: Sampling temperature (0.0 – 2.0).
        top_p:       Nucleus sampling threshold.
        max_tokens:  Maximum number of tokens to generate.

    Returns:
        A tuple of (response_text: str, latency_seconds: float).

    Hint:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    """
    from openai import OpenAI

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    start = time.time()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
    )
    latency = time.time() - start

    response_text = response.choices[0].message.content
    return response_text, latency


# ---------------------------------------------------------------------------
# Task 2 — Call GPT-4o-mini
# ---------------------------------------------------------------------------
def call_openai_mini(
    prompt: str,
    temperature: float = 0.7,
    top_p: float = 0.9,
    max_tokens: int = 256,
) -> tuple[str, float]:
    """
    Call the OpenAI Chat Completions API using gpt-4o-mini and return the
    response text + latency.

    Args:
        prompt:      The user message to send.
        temperature: Sampling temperature (0.0 – 2.0).
        top_p:       Nucleus sampling threshold.
        max_tokens:  Maximum number of tokens to generate.

    Returns:
        A tuple of (response_text: str, latency_seconds: float).

    Hint:
        Reuse call_openai() by passing model=OPENAI_MINI_MODEL.
    """
    return call_openai(
        prompt,
        model=OPENAI_MINI_MODEL,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
    )


# ---------------------------------------------------------------------------
# Task 3 — Compare GPT-4o vs GPT-4o-mini
# ---------------------------------------------------------------------------
def compare_models(prompt: str) -> dict:
    """
    Call both gpt-4o and gpt-4o-mini with the same prompt and return a
    comparison dictionary.

    Args:
        prompt: The user message to send to both models.

    Returns:
        A dict with keys:
            - "gpt4o_response":      str
            - "mini_response":       str
            - "gpt4o_latency":       float
            - "mini_latency":        float
            - "gpt4o_cost_estimate": float  (estimated USD for the response)

    Hint:
        Cost estimate = (len(response.split()) / 0.75) / 1000 * COST_PER_1K_OUTPUT_TOKENS["gpt-4o"]
        (0.75 words ≈ 1 token is a rough approximation)
    """
    gpt4o_response, gpt4o_latency = call_openai(prompt)
    mini_response, mini_latency = call_openai_mini(prompt)

    # Rough token estimate: ~0.75 words per token
    gpt4o_tokens = len(gpt4o_response.split()) / 0.75
    gpt4o_cost_estimate = gpt4o_tokens / 1000 * COST_PER_1K_OUTPUT_TOKENS["gpt-4o"]

    return {
        "gpt4o_response": gpt4o_response,
        "mini_response": mini_response,
        "gpt4o_latency": gpt4o_latency,
        "mini_latency": mini_latency,
        "gpt4o_cost_estimate": gpt4o_cost_estimate,
    }


# ---------------------------------------------------------------------------
# Task 4 — Streaming chatbot with conversation history
# ---------------------------------------------------------------------------
def streaming_chatbot() -> None:
    """
    Run an interactive streaming chatbot in the terminal.

    Behaviour:
        - Streams tokens from OpenAI as they arrive (print each chunk).
        - Maintains the last 3 conversation turns in history.
        - Typing 'quit' or 'exit' ends the loop.

    Hints:
        - Keep a list `history` of {"role": ..., "content": ...} dicts.
        - Use stream=True in client.chat.completions.create() and iterate:
            for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                print(delta, end="", flush=True)
        - After each turn, append the assistant reply to history.
        - Trim history to the last 3 turns: history = history[-3:]
    """
    from openai import OpenAI

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    history: list[dict] = []

    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in ("quit", "exit"):
            print("Goodbye!")
            break

        history.append({"role": "user", "content": user_input})

        stream = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=history,
            stream=True,
        )

        print("Assistant: ", end="", flush=True)
        reply = ""
        for chunk in stream:
            delta = chunk.choices[0].delta.content or ""
            print(delta, end="", flush=True)
            reply += delta
        print()  # newline after the streamed reply

        history.append({"role": "assistant", "content": reply})
        # Keep only the last 3 turns (a turn = user + assistant = 6 messages)
        history = history[-6:]


# ---------------------------------------------------------------------------
# Bonus Task A — Retry with exponential backoff
# ---------------------------------------------------------------------------
def retry_with_backoff(
    fn: Callable,
    max_retries: int = 3,
    base_delay: float = 0.1,
) -> Any:
    """
    Call fn(). If it raises an exception, retry up to max_retries times
    with exponential backoff (base_delay * 2^attempt).

    Args:
        fn:          Zero-argument callable to execute.
        max_retries: Maximum number of retry attempts.
        base_delay:  Initial delay in seconds before the first retry.

    Returns:
        The return value of fn() on success.

    Raises:
        The last exception raised by fn() after all retries are exhausted.
    """
    last_exc: Exception | None = None
    for attempt in range(max_retries + 1):
        try:
            return fn()
        except Exception as exc:  # noqa: BLE001 — retry on any error
            last_exc = exc
            if attempt == max_retries:
                break
            time.sleep(base_delay * (2 ** attempt))
    raise last_exc


# ---------------------------------------------------------------------------
# Bonus Task B — Batch compare
# ---------------------------------------------------------------------------
def batch_compare(prompts: list[str]) -> list[dict]:
    """
    Run compare_models on each prompt in the list.

    Args:
        prompts: List of prompt strings.

    Returns:
        List of dicts, each being the compare_models result with an extra
        key "prompt" containing the original prompt string.
    """
    results = []
    for prompt in prompts:
        result = compare_models(prompt)
        result["prompt"] = prompt
        results.append(result)
    return results


# ---------------------------------------------------------------------------
# Bonus Task C — Format comparison table
# ---------------------------------------------------------------------------
def format_comparison_table(results: list[dict]) -> str:
    """
    Format a list of compare_models results as a readable text table.

    Args:
        results: List of dicts as returned by batch_compare.

    Returns:
        A formatted string table with columns:
        Prompt | GPT-4o Response | Mini Response | GPT-4o Latency | Mini Latency

    Hint:
        Truncate long text to 40 characters for readability.
    """
    def trunc(text: str, n: int = 40) -> str:
        text = str(text).replace("\n", " ")
        return text if len(text) <= n else text[: n - 1] + "…"

    headers = ["Prompt", "GPT-4o Response", "Mini Response", "GPT-4o Latency", "Mini Latency"]
    widths = [40, 40, 40, 14, 14]

    def row(cells: list[str]) -> str:
        return " | ".join(str(c).ljust(w) for c, w in zip(cells, widths))

    lines = [row(headers), "-+-".join("-" * w for w in widths)]
    for r in results:
        lines.append(row([
            trunc(r.get("prompt", "")),
            trunc(r.get("gpt4o_response", "")),
            trunc(r.get("mini_response", "")),
            f"{r.get('gpt4o_latency', 0):.3f}s",
            f"{r.get('mini_latency', 0):.3f}s",
        ]))
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Compatibility shim
# ---------------------------------------------------------------------------
# When this file is loaded under a module name containing characters that are
# invalid in a dotted import path (e.g. a hyphen, as in "Day01-lab-assignment"),
# unittest.mock.patch("<module>.call_openai") fails on Python 3.12+ because
# pkgutil.resolve_name rejects the name. The test suite patches
# f"{compare_models.__module__}.call_openai", so we expose the functions under a
# clean alias registered in sys.modules and point their __module__ at it.
import sys as _sys

_MODULE_ALIAS = "day01_lab_solution"
_sys.modules[_MODULE_ALIAS] = _sys.modules[__name__]
for _fn in (
    call_openai,
    call_openai_mini,
    compare_models,
    streaming_chatbot,
    retry_with_backoff,
    batch_compare,
    format_comparison_table,
):
    _fn.__module__ = _MODULE_ALIAS


# ---------------------------------------------------------------------------
# Entry point for manual testing
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    test_prompt = "Explain the difference between temperature and top_p in one sentence."
    print("=== Comparing models ===")
    result = compare_models(test_prompt)
    for key, value in result.items():
        print(f"{key}: {value}")

    print("\n=== Starting chatbot (type 'quit' to exit) ===")
    streaming_chatbot()
