# Save this as test_option_chain_provider.py in your project root

from src.data.option_chain_provider import get_option_expirations, get_put_option_chain

def test_get_option_expirations(ticker="TSLA"):
    print(f"Testing expiration dates for {ticker}...")
    expirations = get_option_expirations(ticker)
    if not expirations:
        print("❌ No expiration dates found.")
    else:
        print(f"✅ Found {len(expirations)} expiration dates.")
        print("Sample:", expirations[:3])

def test_get_put_option_chain(ticker="TSLA"):
    expirations = get_option_expirations(ticker)
    if not expirations:
        print("❌ Cannot test option chain: No expirations.")
        return

    selected_exp = expirations[0]
    print(f"\nTesting PUT chain for {ticker} | Expiration: {selected_exp}")
    df = get_put_option_chain(ticker, selected_exp)

    if df is None or df.empty:
        print("❌ No PUT option data returned.")
    else:
        print(f"✅ PUT option data fetched. Rows: {len(df)}, Columns: {len(df.columns)}")
        print("Sample:\n", df.head(3))

if __name__ == "__main__":
    test_get_option_expirations()
    test_get_put_option_chain()
