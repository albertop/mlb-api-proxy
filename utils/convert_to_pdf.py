"""
Convert MLB API Documentation from Markdown to PDF (via HTML)
This creates a beautifully styled HTML file that can be opened in a browser
and printed/saved as PDF using the browser's built-in functionality.
"""
import markdown
from pathlib import Path

# Read the markdown file
md_file = Path('MLB_API_Documentation.md')
with open(md_file, 'r', encoding='utf-8') as f:
    md_content = f.read()

# Convert markdown to HTML
md = markdown.Markdown(extensions=[
    'tables',
    'fenced_code',
    'codehilite',
    'toc',
    'attr_list'
])
html_content = md.convert(md_content)

# Create a beautiful HTML template with CSS styling
html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MLB Stats API Documentation</title>
    <style>
        @page {{
            size: Letter;
            margin: 0.75in 0.75in 0.75in 1in;
        }}
        
        @media print {{
            body {{
                margin: 0;
                padding: 0;
            }}
            
            h1, h2, h3, h4 {{
                page-break-after: avoid;
            }}
            
            pre, table, blockquote {{
                page-break-inside: avoid;
            }}
            
            .no-print {{
                display: none;
            }}
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 100%;
            margin: 0;
            padding: 20px 20px 20px 40px;
        }}
        
        h1 {{
            color: #002D72;
            border-bottom: 3px solid #002D72;
            padding-bottom: 10px;
            margin-top: 30px;
            font-size: 28pt;
            page-break-after: avoid;
        }}
        
        h2 {{
            color: #D50032;
            border-bottom: 2px solid #D50032;
            padding-bottom: 8px;
            margin-top: 25px;
            font-size: 20pt;
            page-break-after: avoid;
        }}
        
        h3 {{
            color: #002D72;
            margin-top: 20px;
            font-size: 16pt;
            page-break-after: avoid;
        }}
        
        h4 {{
            color: #555;
            margin-top: 15px;
            font-size: 13pt;
            page-break-after: avoid;
        }}
        
        code {{
            background-color: #f4f4f4;
            border: 1px solid #ddd;
            border-radius: 3px;
            padding: 2px 6px;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            font-size: 9pt;
            color: #d14;
        }}
        
        pre {{
            background-color: #f8f8f8;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 15px;
            overflow-x: auto;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            font-size: 9pt;
            line-height: 1.4;
            page-break-inside: avoid;
        }}
        
        pre code {{
            background-color: transparent;
            border: none;
            padding: 0;
            color: #333;
        }}
        
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 15px 0;
            font-size: 10pt;
            page-break-inside: avoid;
        }}
        
        table thead {{
            background-color: #002D72;
            color: white;
        }}
        
        table th {{
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }}
        
        table td {{
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }}
        
        table tbody tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        
        table tbody tr:hover {{
            background-color: #f0f0f0;
        }}
        
        blockquote {{
            border-left: 4px solid #D50032;
            padding-left: 15px;
            margin: 15px 0;
            color: #666;
            background-color: #f9f9f9;
            padding: 10px 15px;
            border-radius: 3px;
        }}
        
        ul, ol {{
            margin: 10px 0;
            padding-left: 30px;
        }}
        
        li {{
            margin: 5px 0;
        }}
        
        a {{
            color: #002D72;
            text-decoration: none;
        }}
        
        a:hover {{
            text-decoration: underline;
        }}
        
        hr {{
            border: none;
            border-top: 2px solid #ddd;
            margin: 30px 0;
        }}
        
        .page-break {{
            page-break-before: always;
        }}
        
        strong {{
            color: #002D72;
        }}
        
        em {{
            color: #555;
        }}
        
        /* First page styling */
        h1:first-of-type {{
            font-size: 36pt;
            text-align: center;
            border-bottom: none;
            margin-top: 100px;
            margin-bottom: 20px;
        }}
        
        /* Ensure code blocks and tables don't break across pages */
        table, pre, blockquote {{
            page-break-inside: avoid;
        }}
    </style>
</head>
<body>
    <div class="no-print" style="position: fixed; top: 10px; right: 10px; background: #002D72; color: white; padding: 15px 25px; border-radius: 5px; box-shadow: 0 2px 10px rgba(0,0,0,0.2); z-index: 1000;">
        <strong>📄 Ready to Print/Save as PDF</strong><br>
        <small>Press Ctrl+P or use File → Print → Save as PDF</small>
    </div>
    {html_content}
</body>
</html>
"""

# Save the HTML file
output_html = 'MLB_API_Documentation.html'
with open(output_html, 'w', encoding='utf-8') as f:
    f.write(html_template)

print(f"✓ HTML file successfully created: {output_html}")
print(f"  File size: {Path(output_html).stat().st_size / 1024:.2f} KB")
print()
print("🌐 Opening in browser...")
print("   To create PDF: Press Ctrl+P → 'Save as PDF' → Save")
print()

# Open in default browser
import webbrowser
import os
webbrowser.open('file://' + os.path.abspath(output_html))

print("✓ Browser opened! Use the print dialog to save as PDF.")
