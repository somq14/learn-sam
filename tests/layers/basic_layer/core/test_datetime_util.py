import datetime
import unittest

import core.datetime_util

jst_tz = datetime.timezone(datetime.timedelta(hours=9))


class TestDatetimeUtil(unittest.TestCase):
    def test_format(self) -> None:
        """
        JSTのdatetimeはUTCでフォーマットされる
        """
        input = datetime.datetime.fromisoformat("1994-12-05T12:34:56.000078+09:00")
        actual = core.datetime_util.format(input)
        expected = "1994-12-05T03:34:56.000078+00:00"
        self.assertEqual(actual, expected)

    def test_format_no_timezone(self) -> None:
        """
        タイムゾーンなしのdatetimeはUTCでフォーマットされる
        """
        input = datetime.datetime.fromisoformat("1994-12-05T12:34:56.000078")
        actual = core.datetime_util.format(input)
        expected = "1994-12-05T12:34:56.000078+00:00"
        self.assertEqual(actual, expected)

    def test_format_specify_timezone(self) -> None:
        """
        JSTを指定してフォーマットすることもできる
        """
        input = datetime.datetime.fromisoformat("1994-12-05T12:34:56.000078+00:00")
        actual = core.datetime_util.format(input, tz=jst_tz)
        expected = "1994-12-05T21:34:56.000078+09:00"
        self.assertEqual(actual, expected)

    def test_parse(self) -> None:
        """
        JSTの文字列をパースするとUTCで表現される
        """
        input = "1994-12-05T12:34:56.000078+09:00"
        actual = core.datetime_util.parse(input)
        expected = datetime.datetime.fromisoformat("1994-12-05T03:34:56.000078+00:00")
        self.assertEqual(actual, expected)

    def test_parse_no_timezone(self) -> None:
        """
        タイムゾーンなしの文字列をパースするとUTCで表現される
        """
        input = "1994-12-05T12:34:56.000078"
        actual = core.datetime_util.parse(input)
        expected = datetime.datetime.fromisoformat("1994-12-05T12:34:56.000078+00:00")
        self.assertEqual(actual, expected)

    def test_parse_specify_timezone(self) -> None:
        input = "1994-12-05T12:34:56.000078+09:00"
        actual = core.datetime_util.parse(input, tz=jst_tz)
        expected = datetime.datetime.fromisoformat("1994-12-05T12:34:56.000078+09:00")
        self.assertEqual(actual, expected)
