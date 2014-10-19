from scripts.scraper import get_scripts
import unittest

class TestRemoveSceneDirection(unittest.TestCase):
    """
    Tests for remove_scene_direction()
    """
    def test_remove_scene_direction_no_scene_direction(self):
        """
        Test remove_scene_direction() on strings with no scene direction
        """
        text = "no scene direciton here"
        without_direction = get_scripts.remove_scene_direction(text)
        self.assertEquals(without_direction, text)

    def test_remove_scene_direction_simple(self):
        """
        Test remove_scene_direction() on strings with just one set of parens
        """
        text = "out (in)"
        without_direction = get_scripts.remove_scene_direction(text)
        self.assertEquals(without_direction, "out ")

        text = "(in) out"
        without_direction = get_scripts.remove_scene_direction(text)
        self.assertEquals(without_direction, " out")

    def test_remove_scene_direction_multiple(self):
        """
        Test remove_scene_direction() on strings multiple scene directions
        """
        text = "(in1) out1 (in2)"
        without_direction = get_scripts.remove_scene_direction(text)
        self.assertEquals(without_direction, " out1 ")

        text = "(in1) (in2) out"
        without_direction = get_scripts.remove_scene_direction(text)
        self.assertEquals(without_direction, "  out")

        text = "out (in1) (in2)"
        without_direction = get_scripts.remove_scene_direction(text)
        self.assertEquals(without_direction, "out  ")

        text = "out (in1) out2 (in2)"
        without_direction = get_scripts.remove_scene_direction(text)
        self.assertEquals(without_direction, "out  out2 ")

        text = "out (in1) out2 (in2) out3"
        without_direction = get_scripts.remove_scene_direction(text)
        self.assertEquals(without_direction, "out  out2  out3")
