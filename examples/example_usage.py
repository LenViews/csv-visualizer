#!/usr/bin/env python3
"""
Test suite for CSV Visualizer
Run with: python -m pytest test_visualize_data.py -v
"""

import pytest
import pandas as pd
import numpy as np
import tempfile
import os
import sys
import json
from pathlib import Path

# Add the app directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'app'))

from visualize_data import CSVVisualizer


def create_test_csv(content: str, suffix: str = '.csv') -> str:
    """Create a temporary CSV file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix=suffix, delete=False) as f:
        f.write(content)
        return f.name


class TestCSVVisualizer:
    """Test cases for CSVVisualizer class."""
    
    def setup_method(self):
        """Create test data before each test."""
        # Simple test data
        self.simple_csv = """name,age,salary,department
Lens View,30,50000,Engineering
Crystal Kimalel,25,55000,Marketing
Sarah Mutoni,35,60000,Engineering
Lexy Chebet,28,52000,HR
Joshua Rakitch,40,70000,Engineering
"""
        
        # CSV with missing values
        self.csv_with_missing = """A,B,C,D
1.0,2.0,3.0,4.0
5.0,,7.0,8.0
9.0,10.0,,12.0
13.0,14.0,15.0,
,18.0,19.0,20.0
"""
        
        # Large CSV for sampling test
        self.large_csv_data = []
        header = "id,value1,value2,value3\n"
        self.large_csv_data.append(header)
        for i in range(1000):
            row = f"{i},{i*1.5},{i*2.0},{i*0.5}\n"
            self.large_csv_data.append(row)
        self.large_csv = ''.join(self.large_csv_data)
        
        # CSV with special characters
        self.csv_special = """col_with_underscore,col-with-dash,"col with spaces",col.with.dots
1,2,3,4
5,6,7,8
"""
    
    def teardown_method(self):
        """Clean up temporary files."""
        # This method will be extended to clean up any created files
        pass
    
    def test_load_simple_csv(self):
        """Test loading a simple CSV file."""
        csv_path = create_test_csv(self.simple_csv)
        try:
            visualizer = CSVVisualizer(csv_path)
            visualizer.load_and_prepare_data()
            
            assert visualizer.data is not None
            assert len(visualizer.data) == 5
            assert set(visualizer.numeric_columns) == {'age', 'salary'}
            assert visualizer.data['age'].iloc[0] == 30
        finally:
            os.unlink(csv_path)
    
    def test_column_selection(self):
        """Test selecting specific columns."""
        csv_path = create_test_csv(self.simple_csv)
        try:
            visualizer = CSVVisualizer(csv_path, columns=['age'])
            visualizer.load_and_prepare_data()
            
            assert visualizer.numeric_columns == ['age']
        finally:
            os.unlink(csv_path)
    
    def test_sampling(self):
        """Test sampling functionality."""
        csv_path = create_test_csv(self.large_csv)
        try:
            sample_size = 100
            visualizer = CSVVisualizer(csv_path, sample_size=sample_size)
            visualizer.load_and_prepare_data()
            
            assert len(visualizer.data) == sample_size
        finally:
            os.unlink(csv_path)
    
    def test_statistics_calculation(self):
        """Test statistics calculation."""
        csv_path = create_test_csv(self.simple_csv)
        try:
            visualizer = CSVVisualizer(csv_path)
            visualizer.load_and_prepare_data()
            
            stats = visualizer.calculate_statistics('age')
            
            assert stats['column'] == 'age'
            assert stats['count'] == 5
            assert stats['min'] == 25
            assert stats['max'] == 40
            assert stats['mean'] == 31.6
            assert stats['median'] == 30
            assert stats['missing'] == 0
            assert 'std' in stats
            assert 'q25' in stats
            assert 'q75' in stats
        finally:
            os.unlink(csv_path)
    
    def test_missing_values(self):
        """Test handling of missing values."""
        csv_path = create_test_csv(self.csv_with_missing)
        try:
            visualizer = CSVVisualizer(csv_path)
            visualizer.load_and_prepare_data()
            
            stats_b = visualizer.calculate_statistics('B')
            assert stats_b['missing'] == 1
            
            stats_c = visualizer.calculate_statistics('C')
            assert stats_c['missing'] == 1
            
            # Column D has a missing value (empty string that pandas reads as NaN)
            stats_d = visualizer.calculate_statistics('D')
            assert stats_d['missing'] == 1
        finally:
            os.unlink(csv_path)
    
    def test_ascii_histogram(self):
        """Test ASCII histogram generation."""
        csv_path = create_test_csv(self.simple_csv)
        try:
            visualizer = CSVVisualizer(csv_path, bins=5)
            visualizer.load_and_prepare_data()
            
            histogram = visualizer.create_ascii_histogram('age')
            assert isinstance(histogram, str)
            assert len(histogram) > 0
            assert '|' in histogram  # Should have separator
            
            inline_histogram = visualizer.create_inline_histogram('age')
            assert isinstance(inline_histogram, str)
            assert len(inline_histogram) == 5  # Should have 5 bins
        finally:
            os.unlink(csv_path)
    
    def test_inline_histogram_insufficient_data(self):
        """Test inline histogram with insufficient data."""
        csv_path = create_test_csv("col\n1")
        try:
            visualizer = CSVVisualizer(csv_path)
            visualizer.load_and_prepare_data()
            
            histogram = visualizer.create_inline_histogram('col')
            assert histogram == "[Insufficient data]"
        finally:
            os.unlink(csv_path)
    
    def test_table_formatting(self):
        """Test statistics table formatting."""
        csv_path = create_test_csv(self.simple_csv)
        try:
            visualizer = CSVVisualizer(csv_path)
            visualizer.load_and_prepare_data()
            
            all_stats = []
            for col in visualizer.numeric_columns:
                stats = visualizer.calculate_statistics(col)
                all_stats.append(stats)
            
            table = visualizer.format_statistics_table(all_stats)
            assert isinstance(table, str)
            assert 'Column' in table
            assert 'Mean' in table
            assert 'Histogram' in table
            assert '|' in table  # Should have column separators
        finally:
            os.unlink(csv_path)
    
    def test_all_stats_option(self):
        """Test show_all_stats option."""
        csv_path = create_test_csv(self.simple_csv)
        try:
            visualizer = CSVVisualizer(csv_path, show_all_stats=True)
            visualizer.load_and_prepare_data()
            
            stats = visualizer.calculate_statistics('age')
            assert 'skew' in stats
            assert 'kurtosis' in stats
            assert 'cv' in stats
            assert 'range' in stats
            assert 'iqr' in stats
        finally:
            os.unlink(csv_path)
    
    def test_invalid_csv(self):
        """Test handling of invalid CSV file."""
        # Create an empty file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            csv_path = f.name
        
        try:
            visualizer = CSVVisualizer(csv_path)
            
            with pytest.raises(ValueError, match="CSV file is empty"):
                visualizer.load_and_prepare_data()
        finally:
            os.unlink(csv_path)
    
    def test_nonexistent_file(self):
        """Test handling of non-existent file."""
        visualizer = CSVVisualizer('/nonexistent/file.csv')
        
        with pytest.raises(FileNotFoundError):
            visualizer.load_and_prepare_data()
    
    def test_special_column_names(self):
        """Test handling of special column names."""
        csv_path = create_test_csv(self.csv_special)
        try:
            visualizer = CSVVisualizer(csv_path)
            visualizer.load_and_prepare_data()
            
            # All columns should be numeric in this test CSV
            assert len(visualizer.numeric_columns) == 4
            
            # Test statistics calculation for one column
            stats = visualizer.calculate_statistics('col_with_underscore')
            assert stats['count'] == 2
            assert stats['min'] == 1
            assert stats['max'] == 5
        finally:
            os.unlink(csv_path)
    
    def test_export_json(self):
        """Test JSON export functionality."""
        csv_path = create_test_csv(self.simple_csv)
        try:
            visualizer = CSVVisualizer(csv_path)
            visualizer.load_and_prepare_data()
            
            all_stats = []
            for col in visualizer.numeric_columns:
                stats = visualizer.calculate_statistics(col)
                all_stats.append(stats)
            
            # Create temporary output file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                output_path = f.name
            
            try:
                visualizer.export_results(all_stats, 'json', output_path)
                
                # Verify JSON was created and has content
                assert os.path.exists(output_path)
                with open(output_path, 'r') as f:
                    data = json.load(f)
                    assert isinstance(data, list)
                    assert len(data) == 2  # age and salary
            finally:
                if os.path.exists(output_path):
                    os.unlink(output_path)
        finally:
            os.unlink(csv_path)
    
    def test_report_generation(self):
        """Test detailed report generation."""
        csv_path = create_test_csv(self.simple_csv)
        try:
            visualizer = CSVVisualizer(csv_path)
            visualizer.load_and_prepare_data()
            
            all_stats = []
            for col in visualizer.numeric_columns:
                stats = visualizer.calculate_statistics(col)
                all_stats.append(stats)
            
            report = visualizer.generate_detailed_report(all_stats)
            assert isinstance(report, str)
            assert 'CSV ANALYSIS REPORT:' in report
            assert 'SUMMARY STATISTICS:' in report
            assert 'DETAILED HISTOGRAMS:' in report
        finally:
            os.unlink(csv_path)


def test_command_line_interface():
    """Test the CLI interface."""
    import subprocess
    import tempfile
    
    # Create test CSV
    test_csv = """x,y,z
1,2,3
4,5,6
7,8,9
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write(test_csv)
        csv_path = f.name
    
    try:
        # Test basic usage
        result = subprocess.run(
            ['python', 'app/visualize_data.py', csv_path],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert 'SUMMARY STATISTICS:' in result.stdout
        
        # Test with columns option
        result = subprocess.run(
            ['python', 'app/visualize_data.py', csv_path, '--columns', 'x', 'y'],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert 'Column' in result.stdout
        
        # Test with bins option
        result = subprocess.run(
            ['python', 'app/visualize_data.py', csv_path, '--bins', '5'],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        
        # Test with sample option
        result = subprocess.run(
            ['python', 'app/visualize_data.py', csv_path, '--sample', '2'],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        
        # Test invalid file
        result = subprocess.run(
            ['python', 'app/visualize_data.py', '/nonexistent/file.csv'],
            capture_output=True,
            text=True
        )
        
        assert result.returncode != 0
        assert 'not found' in result.stderr or 'Error' in result.stderr
        
    finally:
        os.unlink(csv_path)


def test_edge_cases():
    """Test various edge cases."""
    import tempfile
    
    # Test CSV with only one row
    csv_content = "a,b,c\n1,2,3\n"
    csv_path = create_test_csv(csv_content)
    try:
        visualizer = CSVVisualizer(csv_path)
        visualizer.load_and_prepare_data()
        
        # Should still work with one row
        assert len(visualizer.data) == 1
        assert len(visualizer.numeric_columns) == 3
        
        # Statistics should still be calculable
        stats = visualizer.calculate_statistics('a')
        assert stats['count'] == 1
        assert stats['min'] == 1
        assert stats['max'] == 1
        assert stats['mean'] == 1
        
        # Histogram with insufficient data
        histogram = visualizer.create_inline_histogram('a')
        assert histogram == "[Insufficient data]"
    finally:
        os.unlink(csv_path)
    
    # Test CSV with all NaN values
    csv_content = "col1,col2\n,\n,\n"
    csv_path = create_test_csv(csv_content)
    try:
        visualizer = CSVVisualizer(csv_path)
        
        with pytest.raises(ValueError, match="No numeric columns found"):
            visualizer.load_and_prepare_data()
    finally:
        os.unlink(csv_path)


if __name__ == "__main__":
    # Run tests directly if script is executed
    pytest.main([__file__, "-v"])