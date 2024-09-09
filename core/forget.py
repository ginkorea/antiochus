def forget(df):
    """
    Cleans the DataFrame by removing rows with nulls in the first column
    and dropping duplicates based on the first column.

    :param df: Pandas DataFrame to clean.
    :return: None (modifies DataFrame in place).
    """
    # Drop rows where the first column has null values
    df.dropna(subset=[df.columns[0]], inplace=True)

    # Drop duplicates based on the first column
    df.drop_duplicates(subset=[df.columns[0]], inplace=True)

    print("Knowledge cleaned: Dropped nulls and duplicates.")
