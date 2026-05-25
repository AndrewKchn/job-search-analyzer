def apply_filters(df, filters):
    if filters["location"]:
        df = df[df["location"] == filters["location"]]

    if filters["remote_only"]:
        df = df[df["remote"] == True]

    if filters["keyword"]:
        df = df[df["title"].str.contains(filters["keyword"], case=False, na=False)]

    return df
