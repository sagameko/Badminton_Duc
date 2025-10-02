from datetime import datetime

dt = datetime(2025, 10, 6, 6, 0, 0)
print(f"isoformat(): {dt.isoformat()}")
print(f"strftime(): {dt.strftime('%Y-%m-%dT%H:%M:%S')}")
