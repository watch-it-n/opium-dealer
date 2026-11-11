import unittest

from poppy.util.file_name import (
    append_infinity_to_caption_filename,
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
    def test_appends_infinity_to_filename_at_caption_end(self):
        examples = (
            ("Movie Name.mkv", "Movie Name.Infinity.mkv"),
            ("Movie_Name.mp4", "Movie_Name.Infinity.mp4"),
            ("<b>Movie.Name.MKV</b>", "<b>Movie.Name.Infinity.MKV</b>"),
            ("Movie.Name.mkv extra text", "Movie.Name.mkv extra text"),
        )

        for original, expected in examples:
            with self.subTest(original=original):
                self.assertEqual(append_infinity_to_caption_filename(original), expected)

    def test_does_not_append_infinity_twice(self):
        caption = "Movie.Name.Infinity.mkv"
        self.assertEqual(append_infinity_to_caption_filename(caption), caption)

    def test_preserves_captions_without_video_filenames(self):
        caption = "<b>Watch this movie!</b>"
        self.assertEqual(append_infinity_to_caption_filename(caption), caption)


if __name__ == "__main__":
    unittest.main()
