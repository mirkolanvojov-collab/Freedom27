import unittest

from Framework.safe_test_planner import build_test_plan, valid_https_source
from Framework.security_research_engine import Hypothesis, Target

TARGET = Target("iPhone 16 Plus", "iPhone17,4", "iOS 26.6.1", "23G83")


class SafeTestPlannerTests(unittest.TestCase):
    def test_only_https_sources_are_accepted(self):
        self.assertTrue(valid_https_source("https://example.org/report"))
        self.assertFalse(valid_https_source("http://example.org/report"))
        self.assertFalse(valid_https_source("file:///tmp/payload"))
        self.assertFalse(valid_https_source("https://user:pass@example.org/"))

    def test_plan_is_not_ready_without_sources(self):
        hypothesis = Hypothesis(
            hypothesis_id="H-PLAN-1",
            boundary="app sandbox",
            claim="Example",
            expected_observation="A harmless marker is visible",
            falsifying_observation="The marker is not visible",
        )
        plan = build_test_plan(TARGET, hypothesis)
        self.assertFalse(plan["ready_for_review"])
        self.assertTrue(plan["blockers"])
        self.assertEqual(plan["execution_mode"], "human-reviewed, non-destructive only")

    def test_plan_has_explicit_stop_conditions(self):
        hypothesis = Hypothesis(
            hypothesis_id="H-PLAN-2",
            boundary="app sandbox",
            claim="Example",
            expected_observation="A harmless marker is visible",
            falsifying_observation="The marker is not visible",
            source_urls=("https://example.org/report",),
        )
        plan = build_test_plan(TARGET, hypothesis)
        self.assertEqual(len(plan["steps"]), 5)
        self.assertTrue(all(step["stop_if"] for step in plan["steps"]))


if __name__ == "__main__":
    unittest.main()
