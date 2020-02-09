from datetime import datetime

date = datetime.strptime("2020-02-09", "%Y-%m-%d")

start = datetime(year=2020, month=2, day=9)
end = datetime(year=2020, month=2, day=9)

print(start, end)

print(date >= start and date <= end)