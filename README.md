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
   git clone <repository-url>
   cd csv-visualizer
2. Run the setup script:
    ```bash
    chmod +x setup.sh
    ./setup.sh
3. Basic Usage:
    Analyze a CSV file
    ```bash
    python app/visualize_data.py data/sample.csv

    Analyze specific columns
    ```bash
    python app/visualize_data.py data/sample.csv --columns age salary

    Customize histogram appearance
    ```bash
    python app/visualize_data.py data/sample.csv --bins 15 --histogram-width 30

    Sample large dataset
    ```bash
    python app/visualize_data.py large_data.csv --sample 1000

    Export results to different formats
    python app/visualize_data.py data/sample.csv --export csv --output statistics.csv
    python app/visualize_data.py data/sample.csv --export json
    python app/visualize_data.py data/sample.csv --export html

    Show all statistics
    python app/visualize_data.py data/sample.csv --all-stats

4. Sample Output:

python app/visualize_data.py data/sample.csv --columns age salary
================================================================================
CSV ANALYSIS REPORT: sample.csv
Generated: 2026-01-04 13:20:26
Total Rows: 20, Numeric Columns: 2
Histogram Bins: 10, Width: 20 chars
================================================================================

SUMMARY STATISTICS:
Column | Min        | 25%        | Mean       | Median     | 75%        | Max        | Std       | Histogram 
-------+------------+------------+------------+------------+------------+------------+-----------+-----------
age    | 22.0000    | 27.7500    | 32.7500    | 32.5000    | 37.2500    | 45.0000    | 6.4797    | ▅▅▅█▅▅█▂▅▂
salary | 45000.0000 | 51750.0000 | 60000.0000 | 59500.0000 | 66500.0000 | 80000.0000 | 9856.8704 | ▅██▂█▅▅▅▂▂
