import importlib.util, tempfile, unittest, json
from pathlib import Path
spec=importlib.util.spec_from_file_location("gate",Path(__file__).parents[1]/"scripts/preflight.py")
gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
class GateTests(unittest.TestCase):
    def test_missing_sources(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertFalse(gate.validate(Path(d),Path(d))["ok"])
    def test_rejected_deck(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);(p/"di-pmo-pitch").mkdir()
            (p/"di-pmo-pitch/RELEASE-STATUS.json").write_text(json.dumps({"status":"rejected"}))
            self.assertTrue(any("not operator-approved" in e for e in gate.validate(p,p,True)["errors"]))
    def test_changed_bytes(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);(p/"di-pmo-pitch").mkdir();(p/"deck.pptx").write_bytes(b"changed")
            (p/"di-pmo-pitch/RELEASE-STATUS.json").write_text(json.dumps({"status":"approved","artifact":"deck.pptx","sha256":"old"}))
            self.assertTrue(any("bytes differ" in e for e in gate.validate(p,p,True)["errors"]))
if __name__=="__main__":unittest.main()
