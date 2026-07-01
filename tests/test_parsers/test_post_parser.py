from src.parsers.post_parser import PostParser


class DummyElement:
    def __init__(self, text="Hello world", likes="10", comments="5", shares="2"):
        self.text = text
        self.likes = likes
        self.comments = comments
        self.shares = shares

    def get_attribute(self, name):
        if name == "data-testid":
            return "post"
        return None


def test_parse_returns_expected_fields():
    parser = PostParser()
    result = parser.parse(DummyElement())

    assert result["text"] == "Hello world"
    assert result["likes"] == 10
    assert result["comments"] == 5
    assert result["shares"] == 2


def test_parse_accepts_custom_headers_and_mapping():
    parser = PostParser()
    row = {
        "post_text": "Header-based post",
        "likes_count": "12",
        "comments_count": "7",
        "shares_count": "3",
    }

    result = parser.parse(
        row,
        headers=["text", "likes", "comments", "shares"],
        mapping={
            "text": "post_text",
            "likes": "likes_count",
            "comments": "comments_count",
            "shares": "shares_count",
        },
    )

    assert result["text"] == "Header-based post"
    assert result["likes"] == 12
    assert result["comments"] == 7
    assert result["shares"] == 3


def test_parse_many_accepts_header_based_rows():
    parser = PostParser()
    rows = [
        {"post_text": "One", "likes_count": "1", "comments_count": "2", "shares_count": "3"},
        {"post_text": "Two", "likes_count": "4", "comments_count": "5", "shares_count": "6"},
    ]

    results = parser.parse_many(
        rows,
        headers=["text", "likes", "comments", "shares"],
        mapping={
            "text": "post_text",
            "likes": "likes_count",
            "comments": "comments_count",
            "shares": "shares_count",
        },
    )

    assert len(results) == 2
    assert results[0]["text"] == "One"
    assert results[1]["likes"] == 4
