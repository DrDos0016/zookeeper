import hashlib
import unittest
import os

import zookeeper


class TestWorldParsingMethods(unittest.TestCase):
    def setUp(self):
        self.z = zookeeper.Zookeeper()
        self.z.load_file(os.path.join("resources", "ZOOKEEPR.zzt"))
        self.z.parse_world()
        
    def tearDown(self):
        self.z.close_file()

    def test_parse_world(self):
        self.assertEqual(self.z.world.identifier, 65535)
        self.assertEqual(self.z.world.engine, "ZZT")
        self.assertEqual(self.z.world.ammo, 42)
        self.assertEqual(self.z.world.torches, 1)
        self.assertEqual(self.z.world.gems, 65)
        self.assertEqual(self.z.world.health, 512)
        self.assertEqual(self.z.world.score, 8)

        keys_dict = {"Blue": True, "Green": False, "Cyan": False, "Red": False,
                     "Purple": True, "Yellow": False, "White": True}
        self.assertEqual(self.z.world.keys, keys_dict)

        self.assertEqual(self.z.world.torch_cycles, 1)
        self.assertEqual(self.z.world.energizer_cycles, 2)
        self.assertEqual(self.z.world.time_passed, 3)

        self.assertEqual(self.z.world.world_name, "ZOOKEEPR")
        self.assertEqual(self.z.world.world_name_length, len("ZOOKEEPR"))

        self.assertEqual(self.z.world.saved_game, False)

    def test_world_flags(self):
        self.assertEqual(self.z.world.flags[0].name, "ONE")
        self.assertEqual(self.z.world.flags[1].name, "TWO")
        self.assertEqual(self.z.world.flags[3].name, "FOUR")

        for idx in range(0, 10):
            self.assertEqual(self.z.world.flags[idx].length,
                             len(self.z.world.flags[idx].name)
                             )
            if idx not in [0, 1, 3]:
                self.assertEqual(self.z.world.flags[idx].name, "")


class TestFontMethods(unittest.TestCase):
    def test_font_export(self):
        z = zookeeper.Zookeeper()
        z.export_font(os.path.join("resources", "INVERTED.COM"),
                      os.path.join("output", "cp437-inverted.png")
                      )

        # Compare the generated PNG with the original.
        path = os.path.join("..", "zookeeper", "charsets",
                            "cp437-inverted.png")
        with open(path, "rb") as source_fh:
            source_png = source_fh.read()

        path = os.path.join("output", "cp437-inverted.png")
        with open(path, "rb") as test_fh:
            test_png = test_fh.read()

        self.assertEqual(source_png, test_png, "Charset PNGs do not match.")

    def tearDown(self):
        os.remove(os.path.join("output", "cp437-inverted.png"))


class TestWorldConstructionMethods(unittest.TestCase):
    def test_new_world(self):
        z = zookeeper.Zookeeper()
        key_dict = {"Blue": True, "Purple": True, "White": True}
        z.new_world(engine="ZZT", health=255, ammo=32, torches=8, gems=4,
                    score=2, keys=key_dict)

        self.assertEqual(z.world.engine, "ZZT")
        self.assertEqual(z.world.health, 255)
        self.assertEqual(z.world.ammo, 32)
        self.assertEqual(z.world.torches, 8)
        self.assertEqual(z.world.gems, 4)
        self.assertEqual(z.world.score, 2)
        self.assertEqual(z.world.keys["Purple"], True)
        self.assertEqual(z.world.keys.get("Yellow", False), False)

    def test_new_world_against_kevedit(self):
        z = zookeeper.Zookeeper()
        z.new_world(engine="ZZT", name="BLANK-KE")
        self.assertEqual(z.save(os.path.join("output", "BLANK-ZK.zzt")), True)

        # Compare md5s
        with open(os.path.join("resources", "BLANK-KE.zzt"), "rb") as fh:
            kev_blank = fh.read()
        kev_md5 = hashlib.md5(kev_blank).hexdigest()
        with open(os.path.join("output", "BLANK-ZK.zzt"), "rb") as fh:
            zoo_blank = fh.read()
        zoo_md5 = hashlib.md5(zoo_blank).hexdigest()
        self.assertEqual(kev_md5, zoo_md5)

        os.remove(os.path.join("output", "BLANK-ZK.zzt"))


if __name__ == '__main__':
    unittest.main(verbosity=2)
