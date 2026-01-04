#!/usr/bin/env python3
"""
CSV Summary Statistics CLI with Inline ASCII Histograms
Author: Lens View <lenoxviews@gmail.com>
Description: A command-line tool to analyze CSV files, compute statistics, and display inline ASCII histograms.
"""

import argparse
import sys
import os
import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any
import math
from datetime import datetime
import json
import warnings

warnings.filterwarnings('ignore')


class CSVVisualizer:
    """Main class for CSV visualization and statistics."""

    def __init__(self, csv_path: str, columns: Optional[List[str]] = None,
                 bins: int = 10, sample_size: Optional[int] = None,
                 histogram_width: int = 20, show_all_stats: bool = False,
                 random_state: int = 42):
        self.csv_path = csv_path
        self.columns = columns
        self.bins = bins
        self.sample_size = sample_size
        self.histogram_width = histogram_width
        self.show_all_stats = show_all_stats
        self.random_state = random_state
        self.data = None
        self.numeric_columns = []
        self.quiet_mode = False

        # Statistics templates
        self.stat_templates = {
            'min': '{:.4f}',
            'max': '{:.4f}',
            'mean': '{:.4f}',
            'median': '{:.4f}',
            'q25': '{:.4f}',
            'q75': '{:.4f}',
            'std': '{:.4f}',
            'count': '{:,.0f}',
            'missing': '{:,.0f}',
            'skew': '{:.3f}',
            'kurtosis': '{:.3f}',
            'range': '{:.4f}',
            'iqr': '{:.4f}',
            'cv': '{:.2%}',
        }

    def load_and_prepare_data(self) -> None:
        """Load CSV file and prepare data for analysis."""
        try:
            self.data = pd.read_csv(self.csv_path)

            if self.data.empty:
                raise ValueError("CSV file contains no data")

            # Sample data if requested
            if self.sample_size and self.sample_size < len(self.data):
                self.data = self.data.sample(n=self.sample_size, random_state=self.random_state)
                if not getattr(self, "quiet_mode", False):
                    print(f"[INFO] Sampled {self.sample_size} rows from dataset")

            # Identify numeric columns
            numeric_cols = self.data.select_dtypes(include=["number"]).columns.tolist()

            # Remove numeric columns that have all NaN values
            numeric_cols = [c for c in numeric_cols if self.data[c].notna().any()]

            # Filter to requested columns if specified
            if self.columns:
                valid_columns = [c for c in self.columns if c in self.data.columns]
                if not getattr(self, "quiet_mode", False):
                    for c in self.columns:
                        if c not in self.data.columns:
                            print(f"[WARNING] Column '{c}' not found in CSV file")
                numeric_cols = [c for c in numeric_cols if c in valid_columns]

            self.numeric_columns = numeric_cols

            if not self.numeric_columns:
                raise ValueError("No numeric columns found")

        except FileNotFoundError:
            raise FileNotFoundError(f"CSV file not found: {self.csv_path}")
        except pd.errors.EmptyDataError:
            raise ValueError("CSV file is empty")
        except ValueError:
            raise
        except Exception as e:
            raise RuntimeError(f"Error loading CSV file: {str(e)}")

    def calculate_statistics(self, column: str) -> Dict[str, Any]:
        """Calculate comprehensive statistics for a single column."""
        col_data = self.data[column].dropna()

        if len(col_data) == 0:
            return {}

        stats = {
            'column': column,
            'count': len(col_data),
            'missing': self.data[column].isna().sum(),
            'min': float(col_data.min()),
            'max': float(col_data.max()),
            'mean': float(col_data.mean()),
            'median': float(col_data.median()),
            'q25': float(col_data.quantile(0.25)),
            'q75': float(col_data.quantile(0.75)),
            'std': float(col_data.std()),
            'range': float(col_data.max() - col_data.min()),
            'iqr': float(col_data.quantile(0.75) - col_data.quantile(0.25)),
            'cv': float(col_data.std() / col_data.mean() if col_data.mean() != 0 else 0),
        }

        if self.show_all_stats:
            try:
                from scipy import stats as scipy_stats
                stats['skew'] = float(scipy_stats.skew(col_data))
                stats['kurtosis'] = float(scipy_stats.kurtosis(col_data))
            except ImportError:
                stats['skew'] = float(col_data.skew())
                stats['kurtosis'] = float(col_data.kurtosis())

        return stats

    def create_ascii_histogram(self, column: str) -> str:
        """Create ASCII histogram for a column."""
        col_data = self.data[column].dropna()

        if len(col_data) < 2:
            return "[Insufficient data]"

        try:
            hist, bin_edges = np.histogram(col_data, bins=self.bins)
        except Exception:
            return "[Error creating histogram]"

        if hist.sum() == 0:
            return "[No data in bins]"

        max_count = hist.max()
        if max_count == 0:
            return "[Empty histogram]"

        scaled_hist = (hist / max_count * self.histogram_width).astype(int)
        histogram_lines = []

        for i in range(self.bins):
            bar_length = scaled_hist[i]
            if bar_length > 0:
                bar = '█' * bar_length
            elif hist[i] > 0:
                bar = '▁'
            else:
                bar = ' '

            try:
                bin_label = f"{bin_edges[i]:.2f}-{bin_edges[i+1]:.2f}"
            except:
                bin_label = f"Bin {i+1}"
            histogram_lines.append(f"{bin_label:15} |{bar}")

        return "\n".join(histogram_lines)

    def create_inline_histogram(self, column: str) -> str:
        """Create a single-line inline ASCII histogram."""
        col_data = self.data[column].dropna()

        if len(col_data) < 2:
            return "[Insufficient data]"

        try:
            hist, _ = np.histogram(col_data, bins=self.bins)
        except Exception:
            return "[Error]"

        if hist.sum() == 0:
            return "[No data]"

        max_count = hist.max()
        if max_count == 0:
            return "[ ]"

        normalized = (hist / max_count * 8).astype(int)
        ascii_chars = " ▁▂▃▄▅▆▇█"
        histogram_chars = [ascii_chars[min(level, len(ascii_chars)-1)] for level in normalized]
        return ''.join(histogram_chars)

    def format_statistics_table(self, all_stats: List[Dict[str, Any]]) -> str:
        """Format statistics into a readable ASCII table."""
        if self.show_all_stats:
            stat_keys = ['min', 'q25', 'mean', 'median', 'q75', 'max', 'std', 'skew', 'kurtosis', 'range', 'iqr', 'cv']
            headers = ['Column', 'Min', '25%', 'Mean', 'Median', '75%', 'Max', 'Std', 'Skew', 'Kurt', 'Range', 'IQR', 'CV%', 'Histogram']
        else:
            stat_keys = ['min', 'q25', 'mean', 'median', 'q75', 'max', 'std']
            headers = ['Column', 'Min', '25%', 'Mean', 'Median', '75%', 'Max', 'Std', 'Histogram']

        col_widths = [len(h) for h in headers]
        rows = []

        for stats in all_stats:
            row = [stats['column'][:20]]
            for key in stat_keys:
                row.append(self.stat_templates.get(key, '{:.4f}').format(stats.get(key, 0)))
            row.append(self.create_inline_histogram(stats['column']))
            rows.append(row)
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))

        table_lines = []
        header_line = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
        separator = "-+-".join("-" * col_widths[i] for i in range(len(headers)))
        table_lines.append(header_line)
        table_lines.append(separator)

        for row in rows:
            row_line = " | ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row))
            table_lines.append(row_line)

        return "\n".join(table_lines)

    def generate_detailed_report(self, all_stats: List[Dict[str, Any]]) -> str:
        """Generate a detailed report with full histograms."""
        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append(f"CSV ANALYSIS REPORT: {os.path.basename(self.csv_path)}")
        report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"Total Rows: {len(self.data):,}, Numeric Columns: {len(self.numeric_columns)}")
        if self.sample_size:
            report_lines.append(f"Sampled: {self.sample_size} rows")
        report_lines.append(f"Histogram Bins: {self.bins}, Width: {self.histogram_width} chars")
        report_lines.append("=" * 80)
        report_lines.append("")
        report_lines.append("SUMMARY STATISTICS:")
        report_lines.append(self.format_statistics_table(all_stats))
        report_lines.append("")
        report_lines.append("DETAILED HISTOGRAMS:")
        report_lines.append("")

        for i, stats in enumerate(all_stats, 1):
            report_lines.append(f"{i}. {stats['column']}:")
            report_lines.append(f"   Count: {stats['count']:,}, Missing: {stats['missing']:,}")
            report_lines.append(f"   Range: [{stats['min']:.4f}, {stats['max']:.4f}], Mean: {stats['mean']:.4f}, Std: {stats['std']:.4f}")
            histogram = self.create_ascii_histogram(stats['column'])
            report_lines.append("   Distribution:")
            for line in histogram.split('\n'):
                report_lines.append(f"   {line}")
            report_lines.append("")

        return "\n".join(report_lines)

    def run_analysis(self) -> Tuple[List[Dict[str, Any]], str]:
        self.load_and_prepare_data()
        all_stats = [self.calculate_statistics(c) for c in self.numeric_columns if self.calculate_statistics(c)]
        report = self.generate_detailed_report(all_stats)
        return all_stats, report

    def export_results(self, all_stats: List[Dict[str, Any]], format: str = 'txt',
                       output_path: Optional[str] = None) -> None:
        if format == 'csv':
            df_stats = pd.DataFrame(all_stats)
            if not output_path:
                base_name = os.path.splitext(os.path.basename(self.csv_path))[0]
                output_path = f"{base_name}_statistics.csv"
            df_stats.to_csv(output_path, index=False)
            if not self.quiet_mode:
                print(f"[INFO] Statistics exported to {output_path}")
        elif format == 'json':
            if not output_path:
                base_name = os.path.splitext(os.path.basename(self.csv_path))[0]
                output_path = f"{base_name}_statistics.json"
            with open(output_path, 'w') as f:
                json.dump(all_stats, f, indent=2, default=str)
            if not self.quiet_mode:
                print(f"[INFO] Statistics exported to {output_path}")
        elif format == 'html':
            self.export_html_report(all_stats, output_path)
        else:
            if not self.quiet_mode:
                print(f"[WARNING] Export format '{format}' not supported")

    def export_html_report(self, all_stats: List[Dict[str, Any]], output_path: Optional[str] = None) -> None:
        try:
            import plotly.graph_objects as go
        except ImportError:
            if not self.quiet_mode:
                print("[WARNING] Plotly not installed. Install with: pip install plotly")
            return
        # HTML export code can be added here if needed

# ----------------------- CLI -----------------------

def main():
    parser = argparse.ArgumentParser(
        description="CSV Summary Statistics with Inline ASCII Histograms",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('csv_file', help='Path to CSV file to analyze')
    parser.add_argument('--columns', '-c', nargs='+', help='Column names to analyze (default: all numeric columns)')
    parser.add_argument('--bins', '-b', type=int, default=10, help='Number of bins for histograms (default: 10)')
    parser.add_argument('--sample', '-s', type=int, help='Sample size for large datasets (random sampling)')
    parser.add_argument('--histogram-width', '-w', type=int, default=20, help='Width of ASCII histograms in characters (default: 20)')
    parser.add_argument('--export', '-e', choices=['csv', 'json', 'html', 'txt'], default='txt', help='Export format (default: txt/console output)')
    parser.add_argument('--output', '-o', help='Output file path for exported results')
    parser.add_argument('--all-stats', '-a', action='store_true', help='Show all statistics including skewness and kurtosis')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output with progress information')
    parser.add_argument('--quiet', '-q', action='store_true', help='Suppress non-essential output')
    parser.add_argument('--version', action='version', version='CSV Visualizer 1.0.0')

    args = parser.parse_args()

    if not os.path.exists(args.csv_file):
        print(f"❌ Error: CSV file '{args.csv_file}' not found", file=sys.stderr)
        sys.exit(1)

    try:
        visualizer = CSVVisualizer(
            csv_path=args.csv_file,
            columns=args.columns,
            bins=args.bins,
            sample_size=args.sample,
            histogram_width=args.histogram_width,
            show_all_stats=args.all_stats
        )
        visualizer.quiet_mode = args.quiet
        all_stats, report = visualizer.run_analysis()

        if args.export == 'txt':
            if not args.quiet:
                print(report)
        else:
            visualizer.export_results(all_stats, args.export, args.output)

        if not args.quiet and args.export == 'txt':
            print("\n" + "=" * 60)
            print("✅ Analysis complete!")
            print("=" * 60)
            print(f"  📁 File: {args.csv_file}")
            print(f"  📊 Rows analyzed: {len(visualizer.data):,}")
            print(f"  📈 Columns analyzed: {len(visualizer.numeric_columns)}")
            if args.sample:
                print(f"  🎯 Sample size: {args.sample}")
            print(f"  📐 Histogram bins: {args.bins}")
            print("=" * 60)
        sys.exit(0)

    except Exception as e:
        print(f"❌ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
