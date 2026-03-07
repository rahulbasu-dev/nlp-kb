"""Generate educational PPTX: HMM Forward-Backward Algorithm Step-by-Step.

Walks through the Forward-Backward algorithm on a concrete weather/umbrella
HMM example. Observation sequence: U, N, U with states Rainy/Sunny.
Reuses slide builder helpers from generate_topic_pptx.py.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from generate_topic_pptx import (
    _new_prs, add_title_slide, add_section_slide, add_content_slide,
    add_two_column_slide, add_formula_slide, add_table_slide,
    add_key_concept_slide,
    ACCENT_BLUE, ACCENT_GREEN, ACCENT_ORANGE, ACCENT_RED,
)

ACCENT_TEAL = __import__("pptx").dml.color.RGBColor(0x00, 0x89, 0x7B)


def build_hmm_forward_backward(prs):
    """Build all slides for the HMM Forward-Backward presentation."""

    # ── 1. Title ──
    add_title_slide(
        prs,
        "HMM Forward-Backward Algorithm:\nStep-by-Step",
        "A Complete Worked Example with the Weather/Umbrella HMM",
        ACCENT_TEAL,
    )

    # ── 2. Problem Setup ──
    add_content_slide(prs, "Problem Setup", [
        "Hidden states:  Rainy (R),  Sunny (S)",
        "Observations:   Umbrella (U),  No-umbrella (N)",
        "",
        "Observation sequence:  O = { U, N, U }   (3 time steps)",
        "",
        "Goal: For each time step, compute the posterior probability",
        "  P(state | full observation sequence)",
        "",
        "This requires BOTH the Forward AND Backward algorithms.",
    ], ACCENT_TEAL)

    # ── 3. HMM Parameters ──
    add_table_slide(prs, "HMM Parameters: Transition Matrix  A",
        ["From \\ To", "Rainy", "Sunny"],
        [
            ["Rainy",  "0.7", "0.3"],
            ["Sunny",  "0.4", "0.6"],
        ], ACCENT_TEAL)

    add_two_column_slide(prs, "HMM Parameters: Emission & Initial",
        "Emission Matrix  B", [
            "P(U | Rainy) = 0.9",
            "P(N | Rainy) = 0.1",
            "P(U | Sunny) = 0.2",
            "P(N | Sunny) = 0.8",
        ],
        "Initial Distribution  pi", [
            "P(Rainy) = 0.5",
            "P(Sunny) = 0.5",
            "",
            "(Equal prior over states)",
        ], ACCENT_TEAL)

    # ── 4. Trellis Overview ──
    add_content_slide(prs, "Trellis Diagram Overview", [
        "         t=1 (U)          t=2 (N)          t=3 (U)",
        "          ┌──┐             ┌──┐             ┌──┐",
        "          │ R│────────────►│ R│────────────►│ R│",
        "          └──┘╲           ╱└──┘╲           ╱└──┘",
        "               ╲         ╱      ╲         ╱",
        "                ╲       ╱        ╲       ╱",
        "          ┌──┐   ╲   ╱   ┌──┐    ╲   ╱   ┌──┐",
        "          │ S│────────────►│ S│────────────►│ S│",
        "          └──┘             └──┘             └──┘",
        "",
        "Each node stores forward (alpha) and backward (beta) values.",
        "Combining them gives the posterior gamma_t(i).",
    ], ACCENT_TEAL)

    # ══════════════════════════════════════════════════════════════════════
    # FORWARD ALGORITHM
    # ══════════════════════════════════════════════════════════════════════
    add_section_slide(prs, "Part 1: The Forward Algorithm", ACCENT_TEAL)

    # ── Forward Formula ──
    add_formula_slide(prs, "Forward Algorithm Formulas", [
        "Init:       alpha_1(j) = pi_j  x  b_j(o_1)",
        "Recursion:  alpha_t(j) = [ SUM_i  alpha_{t-1}(i) x a_{ij} ]  x  b_j(o_t)",
        "Termination:  P(O|lambda) = SUM_j  alpha_T(j)",
    ], [
        "Prior probability times emission at t=1",
        "Sum contributions from ALL previous states, then multiply by emission",
        "Total observation probability = sum of final alpha values",
    ], ACCENT_TEAL)

    # ── Forward t=1 ──
    add_content_slide(prs, "Forward t=1: Initialization  (o_1 = U)", [
        "alpha_1(R) = pi(R)  x  b_R(U)",
        "           = 0.5    x  0.9",
        "           = 0.45",
        "",
        "alpha_1(S) = pi(S)  x  b_S(U)",
        "           = 0.5    x  0.2",
        "           = 0.10",
        "",
        "Check: alpha_1(R) + alpha_1(S) = 0.55",
        "  (Does not sum to 1 — these are joint probabilities, not conditionals)",
    ], ACCENT_TEAL)

    # ── Forward t=2 ──
    add_content_slide(prs, "Forward t=2: Recursion  (o_2 = N)", [
        "alpha_2(R) = [ alpha_1(R) x a_RR  +  alpha_1(S) x a_SR ] x b_R(N)",
        "           = [ 0.45 x 0.7  +  0.10 x 0.4 ] x 0.1",
        "           = [ 0.315  +  0.04 ] x 0.1",
        "           = 0.355 x 0.1  =  0.0355",
        "",
        "alpha_2(S) = [ alpha_1(R) x a_RS  +  alpha_1(S) x a_SS ] x b_S(N)",
        "           = [ 0.45 x 0.3  +  0.10 x 0.6 ] x 0.8",
        "           = [ 0.135  +  0.06 ] x 0.8",
        "           = 0.195 x 0.8  =  0.156",
    ], ACCENT_TEAL)

    # ── Forward t=3 ──
    add_content_slide(prs, "Forward t=3: Recursion  (o_3 = U)", [
        "alpha_3(R) = [ alpha_2(R) x a_RR  +  alpha_2(S) x a_SR ] x b_R(U)",
        "           = [ 0.0355 x 0.7  +  0.156 x 0.4 ] x 0.9",
        "           = [ 0.02485  +  0.0624 ] x 0.9",
        "           = 0.08725 x 0.9  =  0.078525",
        "",
        "alpha_3(S) = [ alpha_2(R) x a_RS  +  alpha_2(S) x a_SS ] x b_S(U)",
        "           = [ 0.0355 x 0.3  +  0.156 x 0.6 ] x 0.2",
        "           = [ 0.01065  +  0.0936 ] x 0.2",
        "           = 0.10425 x 0.2  =  0.02085",
    ], ACCENT_TEAL)

    # ── Forward Termination ──
    add_key_concept_slide(prs, "Forward Termination",
        "P(O | lambda)  =  alpha_3(R) + alpha_3(S)  =  0.078525 + 0.02085  =  0.099375",
        [
            "This is the total probability of observing U, N, U under our HMM",
            "We will use this as the normalizing constant for posterior probabilities",
            "The Forward algorithm computed this in O(N^2 T) = O(4 x 3) = 12 multiplications",
            "Brute force would need N^T = 2^3 = 8 full-length paths (grows exponentially!)",
        ], ACCENT_TEAL)

    # ── Forward Summary Table ──
    add_table_slide(prs, "Forward Algorithm Summary:  alpha values",
        ["State", "t=1 (U)", "t=2 (N)", "t=3 (U)"],
        [
            ["Rainy",  "0.4500",  "0.0355",  "0.078525"],
            ["Sunny",  "0.1000",  "0.1560",  "0.020850"],
            ["Sum",    "0.5500",  "0.1915",  "0.099375"],
        ], ACCENT_TEAL)

    # ══════════════════════════════════════════════════════════════════════
    # BACKWARD ALGORITHM
    # ══════════════════════════════════════════════════════════════════════
    add_section_slide(prs, "Part 2: The Backward Algorithm", ACCENT_TEAL)

    # ── Backward Formula ──
    add_formula_slide(prs, "Backward Algorithm Formulas", [
        "Init:       beta_T(i) = 1       for all states i",
        "Recursion:  beta_t(i) = SUM_j  a_{ij} x b_j(o_{t+1}) x beta_{t+1}(j)",
        "Check:      P(O|lambda) = SUM_j  pi_j x b_j(o_1) x beta_1(j)",
    ], [
        "Convention: backward values at the last time step are 1",
        "Sum over all NEXT states: transition x emission x future backward",
        "Should equal the Forward termination result (consistency check)",
    ], ACCENT_TEAL)

    # ── Backward t=3 ──
    add_content_slide(prs, "Backward t=3: Initialization", [
        "beta_3(R) = 1.0",
        "beta_3(S) = 1.0",
        "",
        "By convention, the backward probability at the final time step",
        "is set to 1 for every state.",
        "",
        "(There are no future observations to account for.)",
    ], ACCENT_TEAL)

    # ── Backward t=2 ──
    add_content_slide(prs, "Backward t=2: Recursion  (o_3 = U)", [
        "beta_2(R) = a_RR x b_R(o_3) x beta_3(R)  +  a_RS x b_S(o_3) x beta_3(S)",
        "          = 0.7 x 0.9 x 1  +  0.3 x 0.2 x 1",
        "          = 0.63  +  0.06",
        "          = 0.69",
        "",
        "beta_2(S) = a_SR x b_R(o_3) x beta_3(R)  +  a_SS x b_S(o_3) x beta_3(S)",
        "          = 0.4 x 0.9 x 1  +  0.6 x 0.2 x 1",
        "          = 0.36  +  0.12",
        "          = 0.48",
    ], ACCENT_TEAL)

    # ── Backward t=1 ──
    add_content_slide(prs, "Backward t=1: Recursion  (o_2 = N)", [
        "beta_1(R) = a_RR x b_R(o_2) x beta_2(R)  +  a_RS x b_S(o_2) x beta_2(S)",
        "          = 0.7 x 0.1 x 0.69  +  0.3 x 0.8 x 0.48",
        "          = 0.0483  +  0.1152",
        "          = 0.1635",
        "",
        "beta_1(S) = a_SR x b_R(o_2) x beta_2(R)  +  a_SS x b_S(o_2) x beta_2(S)",
        "          = 0.4 x 0.1 x 0.69  +  0.6 x 0.8 x 0.48",
        "          = 0.0276  +  0.2304",
        "          = 0.2580",
    ], ACCENT_TEAL)

    # ── Backward Consistency Check ──
    add_key_concept_slide(prs, "Backward Consistency Check",
        "P(O|lambda) = pi(R) x b_R(U) x beta_1(R)  +  pi(S) x b_S(U) x beta_1(S)\n"
        "            = 0.5 x 0.9 x 0.1635  +  0.5 x 0.2 x 0.2580\n"
        "            = 0.073575  +  0.025800  =  0.099375   ✓",
        [
            "Matches the Forward termination result exactly!",
            "This confirms both computations are correct",
            "Forward and Backward give two independent ways to compute P(O|lambda)",
        ], ACCENT_TEAL)

    # ── Backward Summary Table ──
    add_table_slide(prs, "Backward Algorithm Summary:  beta values",
        ["State", "t=1 (U)", "t=2 (N)", "t=3 (U)"],
        [
            ["Rainy",  "0.1635",  "0.69",  "1.0"],
            ["Sunny",  "0.2580",  "0.48",  "1.0"],
        ], ACCENT_TEAL)

    # ══════════════════════════════════════════════════════════════════════
    # COMBINING: POSTERIOR PROBABILITIES
    # ══════════════════════════════════════════════════════════════════════
    add_section_slide(prs, "Part 3: Posterior Probabilities (gamma)", ACCENT_TEAL)

    # ── Gamma Formula ──
    add_formula_slide(prs, "Posterior Probability Formula", [
        "gamma_t(i) = P(q_t = i | O, lambda)",
        "           = alpha_t(i) x beta_t(i)  /  P(O|lambda)",
    ], [
        "Probability of being in state i at time t, given ALL observations",
        "Forward (past evidence) x Backward (future evidence) / normalizer",
    ], ACCENT_TEAL)

    # ── Gamma t=1 ──
    add_content_slide(prs, "Gamma t=1:  Posterior at t=1  (o_1 = U)", [
        "gamma_1(R) = alpha_1(R) x beta_1(R) / P(O|lambda)",
        "           = 0.45 x 0.1635 / 0.099375",
        "           = 0.073575 / 0.099375",
        "           = 0.7404  (74.0%)",
        "",
        "gamma_1(S) = alpha_1(S) x beta_1(S) / P(O|lambda)",
        "           = 0.10 x 0.2580 / 0.099375",
        "           = 0.025800 / 0.099375",
        "           = 0.2596  (26.0%)",
        "",
        "Check: 0.7404 + 0.2596 = 1.0  ✓    →  Umbrella seen → likely Rainy",
    ], ACCENT_TEAL)

    # ── Gamma t=2 ──
    add_content_slide(prs, "Gamma t=2:  Posterior at t=2  (o_2 = N)", [
        "gamma_2(R) = alpha_2(R) x beta_2(R) / P(O|lambda)",
        "           = 0.0355 x 0.69 / 0.099375",
        "           = 0.024495 / 0.099375",
        "           = 0.2465  (24.7%)",
        "",
        "gamma_2(S) = alpha_2(S) x beta_2(S) / P(O|lambda)",
        "           = 0.156 x 0.48 / 0.099375",
        "           = 0.074880 / 0.099375",
        "           = 0.7535  (75.3%)",
        "",
        "Check: 0.2465 + 0.7535 = 1.0  ✓    →  No umbrella → likely Sunny",
    ], ACCENT_TEAL)

    # ── Gamma t=3 ──
    add_content_slide(prs, "Gamma t=3:  Posterior at t=3  (o_3 = U)", [
        "gamma_3(R) = alpha_3(R) x beta_3(R) / P(O|lambda)",
        "           = 0.078525 x 1.0 / 0.099375",
        "           = 0.078525 / 0.099375",
        "           = 0.7902  (79.0%)",
        "",
        "gamma_3(S) = alpha_3(S) x beta_3(S) / P(O|lambda)",
        "           = 0.02085 x 1.0 / 0.099375",
        "           = 0.02085 / 0.099375",
        "           = 0.2098  (21.0%)",
        "",
        "Check: 0.7902 + 0.2098 = 1.0  ✓    →  Umbrella seen → likely Rainy",
    ], ACCENT_TEAL)

    # ── Full Posterior Table ──
    add_table_slide(prs, "Full Posterior Table:  gamma_t(i)",
        ["State", "t=1 (U)", "t=2 (N)", "t=3 (U)"],
        [
            ["P(Rainy | O)",  "0.7404 (74%)",  "0.2465 (25%)",  "0.7902 (79%)"],
            ["P(Sunny | O)",  "0.2596 (26%)",  "0.7535 (75%)",  "0.2098 (21%)"],
            ["Most likely",   "Rainy",          "Sunny",          "Rainy"],
        ], ACCENT_TEAL)

    # ── Key Insights ──
    add_two_column_slide(prs, "Key Insights",
        "What the Algorithm Shows", [
            "Umbrella observed → high P(Rainy)",
            "No umbrella → high P(Sunny)",
            "The model correctly captures the intuitive weather pattern",
            "Forward-Backward uses ALL observations (past AND future)",
        ],
        "Forward-Backward vs. Viterbi", [
            "Forward-Backward: marginal posteriors at each t",
            "  → P(q_t = i | O)  for each state i, each time t",
            "Viterbi: single BEST state sequence",
            "  → argmax  P(q_1...q_T | O)",
            "They can give different answers!",
        ], ACCENT_TEAL)

    # ── Summary / Takeaways ──
    add_content_slide(prs, "Summary & Takeaways", [
        "1. Forward algorithm computes alpha_t(i) — probability of observations",
        "   o_1...o_t AND being in state i at time t",
        "",
        "2. Backward algorithm computes beta_t(i) — probability of future",
        "   observations o_{t+1}...o_T given state i at time t",
        "",
        "3. Combining: gamma_t(i) = alpha_t(i) x beta_t(i) / P(O|lambda)",
        "   gives the posterior probability of each state at each time step",
        "",
        "4. Complexity: O(N^2 T) for both Forward and Backward",
        "   (vs. O(N^T) brute force)",
        "",
        "5. Foundation for Baum-Welch (EM) parameter learning",
    ], ACCENT_TEAL)


def main():
    """Generate the HMM Forward-Backward PPTX."""
    prs = _new_prs()
    build_hmm_forward_backward(prs)

    output_dir = os.path.join(os.path.dirname(__file__), "..", "html")
    output_path = os.path.join(output_dir, "hmm_forward_backward.pptx")
    prs.save(output_path)
    print(f"Saved: {output_path}")
    print(f"Total slides: {len(prs.slides)}")


if __name__ == "__main__":
    main()
