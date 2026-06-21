from __future__ import annotations

import unittest

from pipeline.mastodon_discovery import canonical_youtube_url, youtube_links
from pipeline.categorize import classify


class YouTubeEvidenceTests(unittest.TestCase):
    def test_extracts_channel_from_profile_field(self) -> None:
        account = {
            "note": "<p>Tech videos and Linux things.</p>",
            "fields": [
                {
                    "name": "YouTube",
                    "value": '<a href="https://www.youtube.com/@ExampleTech">videos</a>',
                }
            ],
        }
        self.assertEqual(
            youtube_links(account),
            [("https://www.youtube.com/@ExampleTech", "field:YouTube")],
        )

    def test_text_claim_without_link_is_not_evidence(self) -> None:
        account = {
            "note": "<p>I make YouTube videos.</p>",
            "fields": [],
        }
        self.assertEqual(youtube_links(account), [])

    def test_video_link_is_not_mistaken_for_channel(self) -> None:
        self.assertIsNone(canonical_youtube_url("https://youtu.be/dQw4w9WgXcQ"))
        self.assertIsNone(canonical_youtube_url("https://www.youtube.com/watch?v=abc"))

    def test_channel_forms_are_accepted(self) -> None:
        self.assertEqual(
            canonical_youtube_url("http://youtube.com/channel/UC123?view_as=subscriber"),
            "https://www.youtube.com/channel/UC123",
        )
        self.assertEqual(
            canonical_youtube_url("https://m.youtube.com/@SomeCreator/videos"),
            "https://www.youtube.com/@SomeCreator/videos",
        )


class CategorizationTests(unittest.TestCase):
    def test_technology_profile(self) -> None:
        result = classify(
            {
                "acct": "example@mastodon.social",
                "display_name": "Linux Teacher",
                "note": "<p>Programming, open source and self-hosting videos.</p>",
                "fields": [],
            }
        )
        self.assertEqual(result.category, "technology")
        self.assertEqual(result.confidence, "high")
        self.assertEqual(result.account_type, "native")

    def test_rss_mirror_is_labeled(self) -> None:
        result = classify(
            {
                "acct": "youtube_example@rss-mstdn.studiofreesia.com",
                "display_name": "Game channel",
                "note": "<p>VTuber and gaming videos.</p>",
                "fields": [],
            }
        )
        self.assertEqual(result.category, "gaming")
        self.assertEqual(result.account_type, "rss-feed")


if __name__ == "__main__":
    unittest.main()
