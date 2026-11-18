"""Tests for agent_trace.py: what an agent read, and how large its context was at each model call."""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import agent_trace as tr  # noqa: E402


def jl(*events):
    return "\n".join(json.dumps(e) for e in events) + "\n"


OPENCODE = jl(
    {"type": "tool_use", "part": {"type": "tool", "tool": "read", "state": {"input": {"filePath": "/work/AGENTS.md"}}}},
    {"type": "step_finish", "part": {"tokens": {"input": 277, "output": 76, "cache": {"write": 0, "read": 20198}}}},
    {"type": "tool_use", "part": {"type": "tool", "tool": "read",
                                  "state": {"input": {"filePath": "/work/.agents/skills/geo-software-library/SKILL.md"}}}},
    {"type": "step_finish", "part": {"tokens": {"input": 8909, "output": 63, "cache": {"write": 10, "read": 20550}}}},
)
OPENCODE_ERR = ("level=ERROR AI_APICallError: request (40485 tokens) exceeds the available context size (32768 tokens)\n"
                "level=ERROR AI_APICallError: request (60087 tokens) exceeds the available context size (32768 tokens)\n")

GEMINI = jl(
    {"event": "init", "init": {"model": "m"}},
    {"event": "step_update", "step_update": {"step_index": 1, "step_type": "agent_response",
                                             "usage": {"input_tokens": 18787, "cache_read_tokens": 0}}},
    {"event": "step_update", "step_update": {"step_index": 2, "state": "ACTIVE", "step_type": "tool", "tool_name": "read_file",
                                             "tool_info": {"parameters": {"Path": "/work/task/README.md"}}}},
    {"event": "step_update", "step_update": {"step_index": 2, "state": "DONE", "step_type": "tool", "tool_name": "read_file",
                                             "tool_info": {"parameters": {"Path": "/work/task/README.md"}}}},
    {"event": "step_update", "step_update": {"step_index": 3, "step_type": "agent_response",
                                             "usage": {"input_tokens": 2291, "cache_read_tokens": 16734}}},
)

QODER = jl(
    {"type": "system", "subtype": "init"},
    {"type": "assistant", "message": {"usage": {"context_usage_ratio": 0.17}, "content": [
        {"type": "text", "text": "x"},
        {"type": "tool_use", "name": "Bash",
         "input": {"command": "cd /work/.agents/skills/geo-software-library; cat SKILL.md"}}]}},
    {"type": "assistant", "message": {"usage": {"context_usage_ratio": 0.2}, "content": [
        {"type": "tool_use", "name": "Bash",
         "input": {"command": "cd /work/.agents/skills/geo-software-library/references; cat libraries/machgl.md"}}]}},
)

KNOWN = [
    "geo-software-library/SKILL.md",
    "geo-software-library/references/libraries/machgl.md",
    "geo-software-library/references/libraries/geolonia-maps.md",
    "geo-software-provider/references/providers/geolonia-maps.md",
    "geo-software-provider/SKILL.md",
]


class Parse(unittest.TestCase):
    def test_opencode_context_is_input_plus_cache(self):
        t = tr.parse("opencode", OPENCODE)
        self.assertEqual(t["context"], [277 + 20198, 8909 + 10 + 20550])
        self.assertEqual([x["tool"] for x in t["tools"]], ["read", "read"])
        self.assertIn("/work/AGENTS.md", t["tools"][0]["input"])

    def test_opencode_overflow_requests_come_from_stderr(self):
        self.assertEqual(tr.overflows(OPENCODE_ERR), [40485, 60087])
        self.assertEqual(tr.overflows("nothing here"), [])

    def test_gemini_context_and_tools_once_per_step(self):
        t = tr.parse("gemini", GEMINI)
        self.assertEqual(t["context"], [18787, 2291 + 16734])
        self.assertEqual(len(t["tools"]), 1)
        self.assertEqual(t["tools"][0]["tool"], "read_file")

    def test_qoder_has_ratio_not_tokens(self):
        t = tr.parse("qoder", QODER)
        self.assertEqual(t["context"], [])
        self.assertEqual(t["ratio"], [0.17, 0.2])
        self.assertEqual(len(t["tools"]), 2)


class RefsRead(unittest.TestCase):
    def test_full_path(self):
        got = tr.refs_read(["/work/.agents/skills/geo-software-library/SKILL.md"], KNOWN)
        self.assertEqual(got, ["geo-software-library/SKILL.md"])

    def test_cd_then_relative_paths(self):
        cmds = [x["input"] for x in tr.parse("qoder", QODER)["tools"]]
        self.assertEqual(tr.refs_read(cmds, KNOWN),
                         ["geo-software-library/SKILL.md", "geo-software-library/references/libraries/machgl.md"])

    def test_same_basename_in_two_skills_is_told_apart(self):
        got = tr.refs_read(["cat /work/.agents/skills/geo-software-provider/references/providers/geolonia-maps.md"], KNOWN)
        self.assertEqual(got, ["geo-software-provider/references/providers/geolonia-maps.md"])

    def test_skill_md_needs_its_directory(self):
        self.assertEqual(tr.refs_read(["cat SKILL.md"], KNOWN), [])


class Summary(unittest.TestCase):
    def test_fixed_peak_and_sum(self):
        s = tr.summary([100, 300, 200])
        self.assertEqual((s["calls"], s["fixed"], s["peak"], s["read"]), (3, 100, 300, 600))

    def test_empty(self):
        self.assertEqual(tr.summary([])["calls"], 0)


if __name__ == "__main__":
    unittest.main()
