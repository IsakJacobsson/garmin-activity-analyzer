import pandas as pd


def min_sec_to_deltatime_format(s):
    return "00:" + s


def load_data(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)

    # Strings
    str_cols = ["Aktivitetstyp", "Namn", "Medelkontakttidsbalans"]
    for col in str_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # Boolean columns
    df["Favorit"] = (
        df["Favorit"].astype(str).str.lower().map({"true": True, "false": False})
    )
    df["Dekompression"] = (
        df["Dekompression"].astype(str).str.strip().map({"Ja": True, "Nej": False})
    )

    # Datetime
    df["Datum"] = pd.to_datetime(df["Datum"], errors="coerce")
    df = df.set_index("Datum")

    # 'Steg' reformatted from 6,123 to 6123
    if "Steg" in df.columns:
        df["Steg"] = df["Steg"].str.replace(",", "")

    # Some activites messure in meters, we want to convert to km, e.g., 1,000 (m) to 1.0 (km)
    df["Distans"] = df["Distans"].str.replace(",", ".")

    # Numeric columns (floats)
    numeric_cols = [
        "Distans",
        "Kalorier",
        "Medelpuls",
        "Maxpuls",
        "Aerobisk Training Effect",
        "Medellöpkadens",
        "Maximal löpkadens",
        "Total stigning",
        "Totalt nedför",
        "Medelsteglängd",
        "Medelvärde för vertikal kvot",
        "Medelvärde för vertikal rörelse",
        "Medeltid för markkontakt",
        "Normalized Power® (NP®)",
        "Training Stress Score®",
        "Med. kraft",
        "Maxkraft",
        "Totalt antal årtag",
        "Medel-Swolf",
        "Medelårtagstempo",
        "Steg",
        "Totalt antal repetitioner",
        "Totalt antal set",
        "Urladdning av Body Battery",
        "Minsta temperatur",
        "Antal varv",
        "Maximal temperatur",
        "Genomsnittlig andning",
        "Minsta andningshastighet",
        "Maximal andningshastighet",
        "Stressändring",
        "Medestress",
        "Maxbelastning",
        "Min. höjd",
        "Max. höjd",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col]
                .replace("--", pd.NA)
                .astype(str)
                .str.replace(",", ".", regex=False),
                errors="coerce",
            )

    min_sec_cols = ["Medeltempo", "Bästa tempo"]
    for col in min_sec_cols:
        if col in df.columns:
            df[col] = df[col].map(min_sec_to_deltatime_format)

    # Time/duration columns
    time_cols = [
        "Tid",
        "Medeltempo",
        "Bästa tempo",
        "Medelvärde GAP",
        "Bästa varvtid",
        "Start för stress",
        "Slut för stress",
        "Färdtid",
        "Total tid",
    ]
    for col in time_cols:
        if col in df.columns:
            df[col] = pd.to_timedelta(df[col], errors="coerce")

    return df
