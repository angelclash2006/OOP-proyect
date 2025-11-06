import unittest
import tempfile
import os
import json

from sourceCode.workSpace import WorkSpace, Component

class TestWorkSpace(unittest.TestCase):
    def setUp(self):
        self.ws = WorkSpace([], 1, "Test", "desc", [800,600], "px", 100, [], [], False, 0.0, False, [], "user", ["default"], "")

    def test_include_and_get(self):
        comp = self.ws.include_component({"type": "PowerSource", "position": (10, 20)})
        self.assertIsNotNone(comp.id)
        got = self.ws.get_component(comp.id)
        self.assertEqual(got.type, "PowerSource")

    def test_connect_and_connected(self):
        a = self.ws.include_component({"type": "PowerSource"})
        b = self.ws.include_component({"type": "LED"})
        self.ws.connect_components(a.id, b.id)
        connected = self.ws.get_connected_components(a.id)
        # get_connected_components returns Component objects
        connected_ids = [c.id for c in connected]
        self.assertIn(b.id, connected_ids)

    def test_save_load(self):
        a = self.ws.include_component({"type": "PowerSource"})
        b = self.ws.include_component({"type": "LED"})
        self.ws.connect_components(a.id, b.id)
        fd, path = tempfile.mkstemp(suffix='.json')
        os.close(fd)
        try:
            self.ws.save_to_file(path)
            loaded = WorkSpace.load_from_file(path)
            # after loading, components should be present
            self.assertIsNotNone(loaded)
            self.assertTrue(len(loaded.components) >= 2)
        finally:
            os.remove(path)

if __name__ == '__main__':
    unittest.main()
