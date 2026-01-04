# CSV Summary Statistics CLI with Inline ASCII Histograms

A powerful command-line tool for analyzing CSV files, computing comprehensive statistics and visualizing data distributions with ASCII histograms.

## 📋 Features

- **📊 Comprehensive Statistics**: Min, max, mean, median, quartiles, standard deviation, skewness, kurtosis
- **📈 ASCII Visualization**: Inline and detailed ASCII histograms with customizable width
- **🎯 Flexible Column Selection**: Analyze specific columns or all numeric columns
- **⚡ Sampling Support**: Handle large datasets with random sampling
- **📤 Multiple Export Formats**: CSV, JSON, HTML, and plain text output
- **📐 Advanced Statistics**: Coefficient of variation, interquartile range, and more
- **🔧 Robust Error Handling**: Graceful handling of missing values, malformed files, edge cases

## 🚀 Quick Start

### Installation

1. Clone or download the project:
   ```bash
   git clone https://github.com/LenViews/csv-visualizer.git
   cd csv-visualizer
2. Run the setup script:
    ```bash
    chmod +x setup.sh
    ./setup.sh
3. Analyze a CSV file:
    ```bash
    python app/visualize_data.py data/sample.csv

4. Analyze specific columns:
    ```bash
    python app/visualize_data.py data/sample.csv --columns age salary

5. Customize histogram appearance:
    ```bash
    python app/visualize_data.py data/sample.csv --bins 15 --histogram-width 30

6. Sample large dataset:
    ```bash
    python app/visualize_data.py large_data.csv --sample 1000

7. Export results to different formats:
    ```bash
    python app/visualize_data.py data/sample.csv --export csv --output statistics.csv
    python app/visualize_data.py data/sample.csv --export json
    python app/visualize_data.py data/sample.csv --export html

8. Show all statistics:
    ```bash
    python app/visualize_data.py data/sample.csv --all-stats

9. Sample Output:
    ```bash
    =========================================
    CSV ANALYSIS REPORT: sample.csv
    =========================================
    Total Rows: 20, Numeric Columns: 4
    Histogram Bins: 10, Width: 20 chars
    =========================================

    SUMMARY STATISTICS:
    Column      | Min    | 25%    | Mean   | Median | 75%    | Max    | Std    | Histogram
    ----------- | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ----------
    age         | 22.0000| 27.2500| 32.8500| 32.5000| 37.7500| 45.0000| 6.6943 | ▁▂▅▇█▇▅▂▁
    salary      | 45000.0| 51500.0| 60000.0| 59500.0| 66250.0| 80000.0| 9743.5 | ▁▂▄▆██▆▄▂▁

