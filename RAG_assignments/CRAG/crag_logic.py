"""CRAG evaluation and corrective retrieval logic."""

import re
from dataclasses import dataclass
from typing import Optional

from crag_prompt import CRAG_EVALUATION_PROMPT, CRAG_SYSTEM_PROMPT


@dataclass
class CRAGResult:
    """Parsed result from CRAG evaluator LLM response."""
    overall_quality: str  # Excellent, Good, Fair, Poor
    action: str  # PROCEED_WITH_ANSWER or Retrieve_again
    refined_query: Optional[str] = None
    reasoning: Optional[str] = None
    confidence: Optional[str] = None
    answer: Optional[str] = None
    raw_response: str = ""


def parse_crag_response(response: str) -> CRAGResult:
    """Parse the LLM response into structured CRAGResult."""
    raw = response.strip()
    quality = "Fair"
    action = "PROCEED_WITH_ANSWER"
    refined_query = None
    reasoning = None
    confidence = None
    answer = None

    # Overall quality (Step 1 or Step 3)
    quality_match = re.search(
        r"\*\*Overall quality:\*\*\s*\[?(Excellent|Good|Fair|Poor)\]?",
        raw, re.IGNORECASE
    )
    if not quality_match:
        quality_match = re.search(
            r"\*\*Context Quality:\*\*\s*\[?(Excellent|Good|Fair|Poor)\]?",
            raw, re.IGNORECASE
        )
    if quality_match:
        quality = quality_match.group(1).strip()

    # Action
    if "Retrieve_again" in raw or "retrieve_again" in raw.lower():
        action = "Retrieve_again"
    elif "PROCEED_WITH_ANSWER" in raw or "proceed_with_answer" in raw.lower():
        action = "PROCEED_WITH_ANSWER"

    # New Query (refined)
    new_query_match = re.search(
        r"\*\*New Query:\*\*\s*(.+?)(?=\n\*\*|$)",
        raw, re.DOTALL | re.IGNORECASE
    )
    if new_query_match:
        refined_query = new_query_match.group(1).strip()

    # REASONING
    reason_match = re.search(
        r"\*\*REASONING:\*\*\s*(.+?)(?=\n##|\n\*\*|$)",
        raw, re.DOTALL | re.IGNORECASE
    )
    if reason_match:
        reasoning = reason_match.group(1).strip()

    # Confidence
    conf_match = re.search(
        r"\*\*Confidence(?:\s*Level)?:\*\*\s*\[?(High|Medium|Low)\]?",
        raw, re.IGNORECASE
    )
    if conf_match:
        confidence = conf_match.group(1).strip()

    # Answer (after "Answer:" in Step 3)
    answer_match = re.search(
        r"\*\*Answer:\*\*\s*(.+?)$",
        raw, re.DOTALL | re.IGNORECASE
    )
    if answer_match:
        answer = answer_match.group(1).strip()

    return CRAGResult(
        overall_quality=quality,
        action=action,
        refined_query=refined_query,
        reasoning=reasoning,
        confidence=confidence,
        answer=answer,
        raw_response=raw,
    )


def build_evaluation_prompt(user_query: str, retrieved_context: str) -> str:
    """Build the CRAG evaluation prompt with query and context."""
    return CRAG_EVALUATION_PROMPT.format(
        user_query=user_query,
        retrieved_context=retrieved_context or "(No context retrieved)",
    )


def is_good_quality(quality: str) -> bool:
    """True if quality is Excellent or Good."""
    return quality.lower() in ("excellent", "good")


def should_retrieve_again(result: CRAGResult) -> bool:
    """True if we should refine query and re-retrieve."""
    return result.action == "Retrieve_again" and result.refined_query
