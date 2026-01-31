import pandas as pd

SUMMABLE_COLUMNS = [
    "Distans",
    "Tid",
    "Total stigning",
    "Steg",
    "Kalorier",
    "Aerobisk Training Effect",
    "Total stigning",
    "Totalt nedför",
    "Totalt antal årtag",
    "Totalt antal repetitioner",
    "Totalt antal set",
]


def convert_time_column_to_hours(df):
    df = df.copy()
    if "Tid" in df.columns:
        df["Tid"] = df["Tid"].dt.total_seconds() / 3600
    return df


def aggregate_over_time(s, freq, start=None, end=None):
    if start is None:
        start = s.index.min()
    if end is None:
        end = s.index.max()

    start = start.normalize()
    end = end.normalize()

    if freq == "ME":
        start += pd.offsets.MonthEnd(0)
        end += pd.offsets.MonthEnd(0)
    elif freq == "YE":
        end += pd.offsets.YearEnd(0)

    out = s.resample(freq).sum().reindex(pd.date_range(start, end, freq=freq)).fillna(0)

    return out


def get_activities(df):
    return df["Aktivitetstyp"].unique()


def get_days_without_activity(df):
    activity_days = df.index.normalize()

    start = activity_days.min()
    end = activity_days.max()

    all_days = pd.date_range(start=start, end=end, freq="D")

    missing_days = all_days.difference(activity_days)

    return pd.Series(1, index=missing_days)


def get_summable_metrics(df):
    valid_metrics = []
    for col in SUMMABLE_COLUMNS:
        if col in df.columns and not df[col].isna().any():
            valid_metrics.append(col)
    return valid_metrics


def select_metric_and_drop_zeros(df, metric):
    s = df[metric]
    return s[s != 0]
