#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("update_datasets_catalog", ROOT / "scripts" / "update_datasets_catalog.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class DatasetCatalogAutomationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = yaml.safe_load((ROOT / "config" / "dataset-taxonomy.yaml").read_text(encoding="utf-8"))
        cls.doc = yaml.safe_load((ROOT / "datasets-list.yaml").read_text(encoding="utf-8"))

    def test_strong_title_classification_normalizes_hyphens(self):
        result = MODULE.classify_hf({
            "id": "example/verifiable-instruction",
            "description": "Instruction following constraints for language models",
            "tags": ["task_categories:text-generation"],
        }, self.config)
        self.assertTrue(result["accepted"])
        self.assertEqual(result["categories"][0]["category"], "instruction_following")
        self.assertGreaterEqual(result["categories"][0]["score"], 6.0)

    def test_negative_modality_is_quarantined_out(self):
        result = MODULE.classify_hf({
            "id": "example/multimodal-reasoning-traces",
            "description": "Vision-language reasoning traces with images",
        }, self.config)
        self.assertFalse(result["accepted"])
        self.assertEqual(result["reason"], "negative_keywords")

    def test_metadata_merge_is_idempotent_and_keeps_history(self):
        current = MODULE.normalize_hf({
            "id": "example/math-reasoning",
            "lastModified": "2026-11-01T00:00:00.000Z",
            "sha": "abc",
            "downloads": 10,
            "likes": 2,
            "cardData": {"license": "apache-2.0"},
        })
        record, changes = MODULE.merge_metadata(None, current, ["math_asset"], "2026-11-09T00:00:00Z")
        self.assertEqual(changes, {})
        record, changes = MODULE.merge_metadata(record, current, ["math_asset"], "2026-11-09T01:00:00Z")
        self.assertEqual(changes, {})
        self.assertEqual(record["history"], [])
        updated = dict(current, last_modified="2026-11-09T00:00:00.000Z", downloads=11)
        record, changes = MODULE.merge_metadata(record, updated, ["math_asset"], "2026-11-09T02:00:00Z")
        self.assertEqual(set(changes), {"last_modified", "downloads"})
        self.assertEqual(len(record["history"]), 1)
        self.assertEqual(record["current"]["downloads"], 11)

    def test_known_repository_mapping_and_canonical_validation(self):
        known = MODULE.known_repositories(self.doc)
        self.assertIn("allenai/tulu-3-sft-mixture", known)
        self.assertEqual(known["allenai/tulu-3-sft-mixture"], ["tulu3_sft_mixture"])
        errors, warnings, summary = MODULE.validate(ROOT / "datasets-list.yaml")
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])
        self.assertEqual(summary["total_assets"], len(self.doc["datasets"]))

    def test_candidate_reconciliation_follows_human_curation(self):
        state = {"candidates": {
            "example/accepted": {"repo_id": "example/accepted", "status": "pending_review"},
            "example/rejected": {"repo_id": "example/rejected", "status": "pending_review"},
            "example/pending": {"repo_id": "example/pending", "status": "pending_review"},
        }}
        MODULE.reconcile_candidates(state, {"example/accepted": ["accepted_asset"]}, {"example/rejected"})
        self.assertEqual(state["candidates"]["example/accepted"]["status"], "accepted")
        self.assertEqual(state["candidates"]["example/rejected"]["status"], "rejected")
        self.assertEqual(state["candidates"]["example/pending"]["status"], "pending_review")

    def test_candidates_default_to_pending_review(self):
        state = {"candidates": {"example/new-data": {
            "repo_id": "example/new-data", "status": "pending_review",
        }}}
        rendered = yaml.safe_load(MODULE.render_candidates(state, "2026-11-09T00:00:00Z"))
        self.assertFalse(rendered["policy"]["auto_training_allowed"])
        self.assertEqual(rendered["candidates"][0]["status"], "pending_review")


if __name__ == "__main__":
    unittest.main()
