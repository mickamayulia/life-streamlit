import sys
sys.path.append('.')
from src.data.loader import load_cleaned_data, load_raw_data, get_dataset_summary
from src.analytics.metrics import compute_global_kpis, compute_yearly_trends, compute_country_comparison_data, compute_correlation_matrix, get_country_rankings
from src.analytics.anomaly import compute_anomaly_flags, get_anomaly_summary

def run_all_qa_tests():
    print("--- QA TEST 1: INGESTION & DATASET SUMMARY ---")
    df = load_cleaned_data()
    summary = get_dataset_summary()
    assert len(df) == 2938, f"Expected 2938 rows, got {len(df)}"
    assert df['Country'].nunique() == 193, f"Expected 193 countries, got {df['Country'].nunique()}"
    assert df['iso_alpha'].isnull().sum() == 0, "Found unmapped ISO codes!"
    assert summary['raw_rows'] == 2938, f"Raw rows expected 2938, got {summary['raw_rows']}"
    assert summary['clean_nulls'] == 0, f"Expected 0 nulls, got {summary['clean_nulls']}"
    print("Passed: Dataset Ingestion & ISO Mapping consistent.")

    print("\n--- QA TEST 2: KPI CONSISTENCY (2014) ---")
    kpi_2014 = compute_global_kpis(df, year=2014)
    sub_2014 = df[df['Year'] == 2014]
    assert round(sub_2014['Life_expectancy'].mean(), 2) == kpi_2014['mean_life_expectancy']
    assert round(sub_2014['Life_expectancy'].median(), 2) == kpi_2014['median_life_expectancy']
    assert sub_2014['Country'].nunique() == kpi_2014['total_countries']
    print(f"Passed: KPI calculation matches raw Pandas computation. Mean: {kpi_2014['mean_life_expectancy']}")

    print("\n--- QA TEST 3: CORRELATION ENGINE CONSISTENCY ---")
    corr_p = compute_correlation_matrix(df, method='pearson')
    corr_s = compute_correlation_matrix(df, method='spearman')
    assert not corr_p.isnull().values.any(), "NaNs in Pearson correlation matrix!"
    assert not corr_s.isnull().values.any(), "NaNs in Spearman correlation matrix!"
    assert corr_p.loc['Life_expectancy', 'Life_expectancy'] == 1.0
    print("Passed: Correlation matrices full rank & symmetric.")

    print("\n--- QA TEST 4: EDGE CASES HANDLING ---")
    _, empty_comp = compute_country_comparison_data(df, [])
    assert empty_comp.empty, "Expected empty dataframe for no countries."

    kpi_2015 = compute_global_kpis(df, year=2015)
    assert kpi_2015['total_countries'] == 183
    rank_2015 = get_country_rankings(df, year=2015, top_n=5)
    assert len(rank_2015) == 5
    print("Passed: Edge cases (empty filters, year 2015) handled gracefully.")

    print("\n==============================================")
    print("ALL AUTOMATED QA TESTS PASSED SUCCESSFULLY!")
    print("==============================================")

if __name__ == '__main__':
    run_all_qa_tests()
