from datetime import datetime, timezone


def get_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()
    ##return f"{datetime.now():%Y-%m-%d %H:%M:%S}"
  
