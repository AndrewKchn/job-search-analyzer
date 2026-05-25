import pandas as pd


class TrendsService:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

        self.df["created_at"] = pd.to_datetime(self.df["created_at"], utc=True).dt.tz_convert(None)

    def daily_trends(self):
        return self.df.groupby(self.df["created_at"].dt.date).size()

    def weekly_trends(self):
        return self.df.groupby(self.df["created_at"].dt.to_period("W")).size()

    def monthly_trends(self):
        return self.df.groupby(self.df["created_at"].dt.to_period("M")).size()