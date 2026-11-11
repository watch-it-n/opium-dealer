import unittest

from poppy.util.file_name import replace_last_filename_word


class ReplaceLastFilenameWordTests(unittest.TestCase):
    def test_normalizes_filename_components_for_video_extensions(self):
        examples = (
            ("a_bbs_primexofficial.mkv", "a.bbs.infinity.mkv"),
            ("a bbs primexofficial.mkv", "a.bbs.infinity.mkv"),
            ("a.bbs.primexofficial.mkv", "a.bbs.infinity.mkv"),
            ("a_bbs_primexofficial.mp4", "a.bbs.infinity.mp4"),
            ("a bbs primexofficial.mp4", "a.bbs.infinity.mp4"),
            ("a.bbs.primexofficial.mp4", "a.bbs.infinity.mp4"),
            (
                "VisionQuest (2026) S01E08 720p 10bit DSNP WEBRip HEVC x265 "
                "[ JHS Hindi DDP5.1 + English AAC2.0 ] ESub ~ LUCi ~ PSA.mkv",
                "VisionQuest.(2026).S01E08.720p.10bit.DSNP.WEBRip.HEVC.x265."
                "[.JHS.Hindi.DDP5.1.+.English.AAC2.0.].ESub.~.LUCi.~.infinity.mkv",
            ),
        )

        for original, expected in examples:
            with self.subTest(original=original):
                self.assertEqual(replace_last_filename_word(original), expected)


if __name__ == "__main__":
    unittest.main()
