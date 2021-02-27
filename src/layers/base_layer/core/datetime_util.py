import datetime


def now(tz: datetime.tzinfo = datetime.timezone.utc) -> datetime.datetime:
    return datetime.datetime.now().astimezone(tz)


def format(dt: datetime.datetime, tz: datetime.tzinfo = datetime.timezone.utc) -> str:
    """
    datetime型からISO8601文字列への変換
    タイムゾーン情報が存在しない場合はUTCと解釈する

    Parameters
    ----------
    dt:
        変換対象
    tz:
        変換後のdatetime型のタイムゾーン指定
    """
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=datetime.timezone.utc)
    return dt.astimezone(tz).isoformat()


def parse(dt: str, tz: datetime.tzinfo = datetime.timezone.utc) -> datetime.datetime:
    """
    ISO8601文字列からdatetime型への変換
    タイムゾーン情報が存在しない場合はUTCと解釈する

    Parameters
    ----------
    dt:
        変換対象
    tz:
        変換後のdatetime型のタイムゾーン指定

    Raises
    ------
    ValueError
        ISO8601文字列のパースに失敗したとき
    """
    res = datetime.datetime.fromisoformat(dt)

    if res.tzinfo is None:
        res = res.replace(tzinfo=datetime.timezone.utc)

    return res.astimezone(tz)
