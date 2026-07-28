"""The published brief must start at its own heading.

Four early briefs shipped with the agent's narration still attached
("Now I have everything needed for the brief."), which reads as raw model
output in a document meant for clients. strip_preamble is the gate.
"""
from dispatch.analyst.brief import strip_preamble

BRIEF = "# NEM Daily Brief - 2026-07-26\n\n## Yesterday at a glance\nJuly 25 was mild.\n"


def test_leading_narration_is_removed():
    assert strip_preamble("Now I have everything needed for the brief.\n\n" + BRIEF) == BRIEF


def test_repair_round_explanation_is_removed():
    noisy = (
        "Verified - the TAS1 figure of 8.9% was correct, but the query had an "
        "extra `region` column. Corrected brief below.\n\n" + BRIEF
    )
    assert strip_preamble(noisy) == BRIEF


def test_clean_brief_is_untouched():
    assert strip_preamble(BRIEF) == BRIEF


def test_body_after_the_heading_is_preserved():
    out = strip_preamble("chatter\n\n" + BRIEF)
    assert "## Yesterday at a glance" in out
    assert "July 25 was mild." in out
    assert "chatter" not in out


def test_text_without_a_heading_is_left_alone():
    """Never silently empty a brief - publish something odd instead."""
    assert strip_preamble("no heading here") == "no heading here"


def test_hash_inside_the_body_does_not_confuse_the_cut():
    assert strip_preamble("lead-in\n\n" + BRIEF + "\n#hashtag not a heading\n").startswith(
        "# NEM Daily Brief"
    )
