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

    def test_out_of_scope_media_generation_is_quarantined_out(self):
        result = MODULE.classify_hf({
            "id": "example/text-to-image-reasoning-traces",
            "description": "Synthetic prompts for text-to-image generation",
        }, self.config)
        self.assertFalse(result["accepted"])
        self.assertEqual(result["reason"], "negative_keywords")

    def test_multimodal_reasoning_is_discoverable(self):
        result = MODULE.classify_hf({
            "id": "example/multimodal-reasoning-dataset",
            "description": "Multimodal reasoning dataset with visual reasoning traces for instruction tuning",
            "tags": ["modality:image"],
        }, self.config)
        self.assertTrue(result["accepted"])
        self.assertIn("multimodal_reasoning", {item["category"] for item in result["categories"]})

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

    def test_markdown_table_names_and_ids_link_to_official_sources(self):
        from dataset_markdown_links import link_dataset_table_entries
        item = self.doc["datasets"][0]
        assets = {item["id"]: item}
        row = f"| {item['name']}<br>`{item['id']}` |"
        linked = link_dataset_table_entries(row, assets)
        if item["source"]["url"].startswith("https://"):
            self.assertIn(f"[{item['name']}]({item['source']['url']})", linked)
            self.assertIn(f"[`{item['id']}`]({item['source']['url']})", linked)
        self.assertEqual(link_dataset_table_entries(linked, assets), linked)

    def test_markdown_linker_preserves_code_and_uses_explicit_aliases(self):
        from dataset_markdown_links import link_dataset_table_entries
        assets = {item["id"]: item for item in self.doc["datasets"]}
        row = "| `nvidia/OpenMathReasoning` | HelpSteer3 或 HelpSteer2；Dolly；M2Lingual |"
        linked = link_dataset_table_entries(row, assets)
        self.assertIn("`nvidia/OpenMathReasoning`", linked)
        self.assertNotIn("`nvidia/[", linked)
        self.assertIn("[HelpSteer3](https://huggingface.co/datasets/nvidia/HelpSteer3)", linked)
        self.assertIn("[Dolly](https://huggingface.co/datasets/databricks/databricks-dolly-15k)", linked)
        self.assertIn("[M2Lingual](https://huggingface.co/datasets/ServiceNow-AI/M2Lingual)", linked)
        self.assertEqual(link_dataset_table_entries(linked, assets), linked)

    def test_candidates_default_to_pending_review(self):
        state = {"candidates": {"example/new-data": {
            "repo_id": "example/new-data", "status": "pending_review",
        }}}
        rendered = yaml.safe_load(MODULE.render_candidates(state, "2026-11-09T00:00:00Z"))
        self.assertFalse(rendered["policy"]["auto_training_allowed"])
        self.assertEqual(rendered["candidates"][0]["status"], "pending_review")


if __name__ == "__main__":
    unittest.main()
