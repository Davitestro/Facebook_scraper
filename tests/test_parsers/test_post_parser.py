from src.parsers.post_parser import PostParser


class DummyElement:
    def __init__(
        self,
        text="Hello world",
        likes="10",
        comments="5",
        shares="2",
        author="Jane Reporter",
        publish_date="2026-07-01T12:00:00Z",
        comment="First comment",
        internal_link="https://www.facebook.com/example/posts/123",
    ):
        self.text = text
        self.likes = likes
        self.comments = comments
        self.shares = shares
        self.author = author
        self.publish_date = publish_date
        self.comment = comment
        self.internal_link = internal_link

    def get_attribute(self, name):
        if name == "data-testid":
            return "post"
        if name == "href":
            return self.internal_link
        if name == "datetime":
            return self.publish_date
        return None


class DummyCommentElement(DummyElement):
    def __init__(self):
        super().__init__(
            text="Belgium is crazy now",
            author=None,
            publish_date=None,
            comment="Olias Webos",
            internal_link="https://www.facebook.com/people/Olias-Webos/pfbid02c4xX4ioR3L4uougXhVhX6h8e1DAfaB5qBTBGNNiWdfxewARXuR4T8JwA7rxQP93Bl/?comment_id=Y29tbWVudDoxNDk2NDM2NjE5MTc2OTIxXzI3NjAxNjEzMDg5NDc1Nzk1&__tn__=R]-R",
        )


class DummyTextFallbackElement:
    def __init__(self):
        self.text = (
            "Reuters\n"
            " 7m\n"
            "  ·\n"
            "Mega-deals fuel record M&A as boards dream big on takeovers… See more\n"
            "All reactions:\n"
            "15\n"
            "1\n"
            "Like\n"
            "Comment\n"
            "Yiannis Kustas\n"
            "So MAGA didn't deliver? What a surprise\n"
            "1m"
        )
        self.likes = None
        self.comments = None
        self.shares = None

    def get_attribute(self, name):
        return None


def test_parse_returns_expected_fields():
    parser = PostParser()
    result = parser.parse(DummyElement())

    assert result["body"] == "Hello world"
    assert result["description"] == "Hello world"
    assert result["text"] == "Hello world"
    assert result["author"] == "Jane Reporter"
    assert result["publish_date"] == "2026-07-01T12:00:00Z"
    assert result["comment"] == "First comment"
    assert result["internal_link"] == "https://www.facebook.com/example/posts/123"
    assert result["likes"] == 10
    assert result["comments"] == 5
    assert result["shares"] == 2


def test_parse_accepts_custom_headers_and_mapping():
    parser = PostParser()
    row = {
        "post_body": "Header-based post",
        "post_author": "Column Author",
        "post_date": "2026-07-01",
        "post_comment": "Column comment",
        "post_link": "https://www.facebook.com/example/posts/456",
        "likes_count": "12",
        "comments_count": "7",
        "shares_count": "3",
    }

    result = parser.parse(
        row,
        headers=["body", "author", "publish_date", "comment", "internal_link", "likes", "comments", "shares"],
        mapping={
            "body": "post_body",
            "author": "post_author",
            "publish_date": "post_date",
            "comment": "post_comment",
            "internal_link": "post_link",
            "likes": "likes_count",
            "comments": "comments_count",
            "shares": "shares_count",
        },
    )

    assert result["body"] == "Header-based post"
    assert result["description"] == "Header-based post"
    assert result["text"] == "Header-based post"
    assert result["author"] == "Column Author"
    assert result["publish_date"] == "2026-07-01"
    assert result["comment"] == "Column comment"
    assert result["internal_link"] == "https://www.facebook.com/example/posts/456"
    assert result["likes"] == 12
    assert result["comments"] == 7
    assert result["shares"] == 3


def test_parse_many_accepts_header_based_rows():
    parser = PostParser()
    rows = [
        {"post_body": "One", "likes_count": "1", "comments_count": "2", "shares_count": "3"},
        {"post_body": "Two", "likes_count": "4", "comments_count": "5", "shares_count": "6"},
    ]

    results = parser.parse_many(
        rows,
        headers=["body", "likes", "comments", "shares"],
        mapping={
            "body": "post_body",
            "likes": "likes_count",
            "comments": "comments_count",
            "shares": "shares_count",
        },
    )

    assert len(results) == 2
    assert results[0]["body"] == "One"
    assert results[1]["likes"] == 4


def test_parse_skips_comment_like_elements():
    parser = PostParser()

    assert parser.parse(DummyCommentElement()) is None


def test_parse_infers_counts_date_and_comment_from_text():
    parser = PostParser()
    result = parser.parse(DummyTextFallbackElement())

    assert result["author"] == "Reuters"
    assert result["publish_date"] == "7m"
    assert result["likes"] == 15
    assert result["comments"] == 1
    assert result["comment"] == "So MAGA didn't deliver? What a surprise"
