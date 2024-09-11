import sweetviz as sv
import os

def generate_sweetviz_report(df):
    # Generate Sweetviz report
    report = sv.analyze(df)
    
    # Create a 'reports' directory if it doesn't exist
    if not os.path.exists('reports'):
        os.makedirs('reports')
    
    # Save the report
    report_path = os.path.join('reports', 'sweetviz_report.html')
    report.show_html(report_path, open_browser=False)
    
    return report_path
