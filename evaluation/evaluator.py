"""
Day 4 - Evaluation: Agent Evaluator

Runs automated evaluation across all agents and returns a structured report.
Checks:
  - Response schema correctness (required fields present)
  - Score range validity
  - Intent detection accuracy
  - Response latency
"""

import time
import json
from typing import Optional

from agents.resume_agent import critique_resume
from agents.jd_agent import extract_jd_requirements
from tools.jd_matcher import match_resume_to_jd
from agents.orchestrator import detect_intent
from evaluation.test_cases import (
    RESUME_CRITIQUE_TEST_CASES,
    JD_ANALYSIS_TEST_CASES,
    JD_MATCH_TEST_CASES,
    INTENT_DETECTION_TEST_CASES,
)


def _check_fields(result: dict, expected_fields: list) -> tuple[bool, list]:
    """Returns (all_present, list_of_missing_fields)."""
    missing = [f for f in expected_fields if f not in result]
    return len(missing) == 0, missing


def run_resume_critique_eval(model) -> dict:
    results = []
    for case in RESUME_CRITIQUE_TEST_CASES:
        start = time.time()
        try:
            result = critique_resume(case["parsed_resume"], model)
            latency = round(time.time() - start, 2)

            all_present, missing = _check_fields(result, case["expected_fields"])
            score = result.get("overall_score", None)
            score_valid = (
                isinstance(score, (int, float))
                and case["score_range"][0] <= score <= case["score_range"][1]
            ) if score is not None else False

            results.append({
                "id": case["id"],
                "description": case["description"],
                "passed": all_present and score_valid,
                "schema_ok": all_present,
                "missing_fields": missing,
                "score_valid": score_valid,
                "overall_score": score,
                "latency_s": latency,
                "error": None,
            })
        except Exception as e:
            results.append({
                "id": case["id"],
                "description": case["description"],
                "passed": False,
                "error": str(e),
                "latency_s": round(time.time() - start, 2),
            })

    passed = sum(1 for r in results if r["passed"])
    return {
        "agent": "resume_agent",
        "total": len(results),
        "passed": passed,
        "failed": len(results) - passed,
        "pass_rate": round(passed / len(results) * 100, 1) if results else 0,
        "cases": results,
    }


def run_jd_analysis_eval(model) -> dict:
    results = []
    for case in JD_ANALYSIS_TEST_CASES:
        start = time.time()
        try:
            result = extract_jd_requirements(case["jd_text"], model)
            latency = round(time.time() - start, 2)

            all_present, missing = _check_fields(result, case["expected_fields"])
            results.append({
                "id": case["id"],
                "description": case["description"],
                "passed": all_present,
                "schema_ok": all_present,
                "missing_fields": missing,
                "latency_s": latency,
                "error": None,
            })
        except Exception as e:
            results.append({
                "id": case["id"],
                "description": case["description"],
                "passed": False,
                "error": str(e),
                "latency_s": round(time.time() - start, 2),
            })

    passed = sum(1 for r in results if r["passed"])
    return {
        "agent": "jd_agent",
        "total": len(results),
        "passed": passed,
        "failed": len(results) - passed,
        "pass_rate": round(passed / len(results) * 100, 1) if results else 0,
        "cases": results,
    }


def run_jd_match_eval(model) -> dict:
    results = []
    for case in JD_MATCH_TEST_CASES:
        start = time.time()
        try:
            result = match_resume_to_jd(case["parsed_resume"], case["jd_text"], model)
            latency = round(time.time() - start, 2)

            all_present, missing = _check_fields(result, case["expected_fields"])
            score = result.get("score", None)
            verdict = result.get("verdict", "")

            score_ok = True
            if "min_score" in case and score is not None:
                score_ok = score >= case["min_score"]
            if "max_score" in case and score is not None:
                score_ok = score <= case["max_score"]

            verdict_ok = verdict in case.get("expected_verdict_options", [verdict])

            passed = all_present and score_ok and verdict_ok
            results.append({
                "id": case["id"],
                "description": case["description"],
                "passed": passed,
                "schema_ok": all_present,
                "missing_fields": missing,
                "score": score,
                "score_ok": score_ok,
                "verdict": verdict,
                "verdict_ok": verdict_ok,
                "latency_s": latency,
                "error": None,
            })
        except Exception as e:
            results.append({
                "id": case["id"],
                "description": case["description"],
                "passed": False,
                "error": str(e),
                "latency_s": round(time.time() - start, 2),
            })

    passed = sum(1 for r in results if r["passed"])
    return {
        "agent": "jd_matcher",
        "total": len(results),
        "passed": passed,
        "failed": len(results) - passed,
        "pass_rate": round(passed / len(results) * 100, 1) if results else 0,
        "cases": results,
    }


def run_intent_detection_eval(model) -> dict:
    results = []
    for case in INTENT_DETECTION_TEST_CASES:
        start = time.time()
        try:
            detected = detect_intent(case["message"], model)
            latency = round(time.time() - start, 2)
            passed = detected == case["expected_intent"]
            results.append({
                "message": case["message"],
                "expected": case["expected_intent"],
                "detected": detected,
                "passed": passed,
                "latency_s": latency,
                "error": None,
            })
        except Exception as e:
            results.append({
                "message": case["message"],
                "expected": case["expected_intent"],
                "passed": False,
                "error": str(e),
                "latency_s": round(time.time() - start, 2),
            })

    passed = sum(1 for r in results if r["passed"])
    return {
        "agent": "orchestrator_intent",
        "total": len(results),
        "passed": passed,
        "failed": len(results) - passed,
        "pass_rate": round(passed / len(results) * 100, 1) if results else 0,
        "cases": results,
    }


def run_full_evaluation(model) -> dict:
    """Run all evaluations and return combined report."""
    report = {
        "resume_critique": run_resume_critique_eval(model),
        "jd_analysis": run_jd_analysis_eval(model),
        "jd_match": run_jd_match_eval(model),
        "intent_detection": run_intent_detection_eval(model),
    }

    total_cases = sum(v["total"] for v in report.values())
    total_passed = sum(v["passed"] for v in report.values())
    report["summary"] = {
        "total_cases": total_cases,
        "total_passed": total_passed,
        "total_failed": total_cases - total_passed,
        "overall_pass_rate": round(total_passed / total_cases * 100, 1) if total_cases else 0,
    }
    return report
