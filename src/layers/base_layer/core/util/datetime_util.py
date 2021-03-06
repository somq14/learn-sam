from datetime import datetime, timezone, tzinfo


def now(tz: tzinfo = timezone.utc) -> datetime:
    return datetime.now().astimezone(tz)


def format(dt: datetime, tz: tzinfo = timezone.utc) -> str:
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
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(tz).isoformat()


def parse(dt: str, tz: tzinfo = timezone.utc) -> datetime:
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
    res = datetime.fromisoformat(dt)

    if res.tzinfo is None:
        res = res.replace(tzinfo=timezone.utc)

    return res.astimezone(tz)
