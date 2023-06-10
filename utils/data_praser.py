import pandas as pd


def extract_pass_detail(
    event_df: pd.DataFrame = None,
) -> pd.DataFrame:
    """
    Input: event_df DataFrame contains match events
    Output: Pass detail contains passers, starting locations ending locations, and outcomes.
    """

    # The example data contains nested json columns and they don't work well with csv file.
    # Need to convert a column with nested json to list
    from ast import literal_eval

    event_df.loc[:, "qualifiers"] = event_df["qualifiers"].apply(literal_eval)

    # Code starts here
    col_names = [
        "start_x",
        "start_y",
        "event_type",
        "event_outcome",
        "player_id",
        "end_x",
        "end_y",
        "length",
        "is_keypass",
    ]
    passes = []

    for row in event_df.itertuples():
        if row[10] == "Pass":
            qualifier_dict = {
                "pass_end_x": 0,
                "pass_end_y": 0,
                "length": 0,
                "is_keypass": False,
            }
            for qualifier in row[12]:
                qualifier_name = qualifier["type"]["displayName"]
                qualifier_value = qualifier.get("value", None)
                if not all([qualifier_name, qualifier_value]):
                    pass
                if qualifier_name == "PassEndX":
                    qualifier_dict["pass_end_x"] = float(qualifier_value)
                elif qualifier_name == "PassEndY":
                    qualifier_dict["pass_end_y"] = float(qualifier_value)
                elif qualifier_name == "Length":
                    qualifier_dict["length"] = float(qualifier_value)
                elif qualifier_name == "KeyPass":
                    qualifier_dict["is_keypass"] = True

            passes.append(
                [row[6], row[7], row[10], row[11], int(row[15])]
                + list(qualifier_dict.values())
            )

    pass_detail_df = pd.DataFrame(passes, columns=col_names)
    col_names = [
        "player_id",
        "start_x",
        "start_y",
        "end_x",
        "end_y",
        "length",
        "event_type",
        "event_outcome",
        "is_keypass",
    ]

    return pass_detail_df[col_names]
