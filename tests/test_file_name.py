import unittest

from poppy.util.file_name import (
    replace_caption_filename_word,
    replace_last_filename_word,
)


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


class ReplaceCaptionFilenameWordTests(unittest.TestCase):
    def test_replaces_filename_word_before_video_extension(self):
        examples = (
            ("Movie Name.mkv", "Movie infinity.mkv"),
            ("Movie_Name.mp4", "Movie_infinity.mp4"),
            ("<b>Movie.Name.MKV</b>", "<b>Movie.infinity.MKV</b>"),
            (
                "First Movie.mkv and Second Movie.mp4",
                "First infinity.mkv and Second infinity.mp4",
            ),
        )

        for original, expected in examples:
            with self.subTest(original=original):
                self.assertEqual(replace_caption_filename_word(original), expected)

    def test_preserves_captions_without_video_filenames(self):
        caption = "<b>Watch this movie!</b>"
        self.assertEqual(replace_caption_filename_word(caption), caption)


if __name__ == "__main__":
    unittest.main()
