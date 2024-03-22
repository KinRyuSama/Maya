from src.tools.forum_parser import _parse_forum


def _run_test(input_html: str, expected_result: str):
    actual_result = _parse_forum(input_html)
    print(actual_result)
    assert actual_result == expected_result


def test_forum_parser_works_on_example():
    with open("data/forum-parser-example.html") as f:
        input_html = f.read()

    _run_test(
        input_html=input_html,
        expected_result="""
""".strip(),
    )
