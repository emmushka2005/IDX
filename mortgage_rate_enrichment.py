import pandas as pd

# Fetch Mortgage Rates
def fetch_mortgage_rates():
    url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"

    mortgage = pd.read_csv(url)
    mortgage.columns = ["date", "rate_30yr_fixed"]

    mortgage["date"] = pd.to_datetime(
        mortgage["date"], errors="coerce"
    )

    return mortgage

# Turn weekly data into monthly averages
def make_monthly_rates(mortgage):
    mortgage["year_month"] = mortgage["date"].dt.to_period("M")

    mortgage_monthly = (
        mortgage.groupby("year_month")["rate_30yr_fixed"]
        .mean()
        .reset_index()
    )

    return mortgage_monthly

# Add mortgage rates to each dataset
def add_mortgage_rates(df, date_col, mortgage_monthly):
    df = df.copy()

    df[date_col] = pd.to_datetime(
        df[date_col], errors="coerce"
    )

    df["year_month"] = df[date_col].dt.to_period("M")

    enriched = df.merge(
        mortgage_monthly,
        on="year_month",
        how="left"
    )

    return enriched

def main():

    sold_data = pd.read_csv("sold.csv", low_memory=False)
    listings_data = pd.read_csv("listed.csv", low_memory=False)

    # Fetch and prepare mortgage rates
    mortgage = fetch_mortgage_rates()
    mortgage_monthly = make_monthly_rates(mortgage)

    # Add mortgage rates to each dataset
    sold_with_rates = add_mortgage_rates(
        sold_data,
        "CloseDate",
        mortgage_monthly
    )

    listings_with_rates = add_mortgage_rates(
        listings_data,
        "ListingContractDate",
        mortgage_monthly
    )

    # Convert to CSV's and save
    sold_with_rates.to_csv(
        "sold_with_rates.csv",
        index=False
    )

    listings_with_rates.to_csv(
        "listed_with_rates.csv",
        index=False
    )


if __name__ == "__main__":
    main()