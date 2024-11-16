import re

def generate_latex_table(input_file, input_file2, data_ml, output_file):
    # Initialize an empty list to store the rows
    rows = []
    rows1 = []
    rows2 = []

    # Read the file
    with open(input_file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            # Use regex to extract a and x
            match = re.match(r'f_bottom_up\((\d+),(\d+),(\d+)\)=([\d.]+) time = ([\d.]+)', line)
            if match:
                a, b, c, x, y = match.groups()
                x = float(x)
                rows.append(x)
    with open(input_file2, 'r') as file:
        lines = file.readlines()
        for line in lines:
            # Use regex to extract a and x
            match = re.match(r'f_bottom_up\((\d+),(\d+),(\d+)\)=([\d.]+) time = ([\d.]+)', line)
            if match:
                a1, b1, c1, x1, y1 = match.groups()
                x1 = float(x1)
                rows1.append(x1)
    with open(data_ml, 'r') as file:
        lines = file.readlines()
        for line in lines:
            # Use regex to extract a and x
            match = re.match(r'f\((\d+),([\d.]+)\) = ([\d.]+)', line)
            if match:
                a2, b2, x2 = match.groups()
                x2 = float(x2)
                rows2.append(x2)

    # Start the LaTeX table
    latex_code = "\\begin{tabular}{|c|c|c|}\n\\hline\n"
    latex_code += "n & d=500 & d=1000 & ml \\\\\n\\hline\n"

    # Add rows to the LaTeX table
    for i in range(len(rows)):    
        latex_code += f" {i+1} & {rows[i]} & {rows1[i]} & {rows2[i]}\\\\\n\hline\n"

    # End the LaTeX table
    latex_code += "\\hline\n\\end{tabular}"

    # Write the LaTeX code to the output file
    with open(output_file, 'w') as file:
        file.write(latex_code)

# Replace 'data.txt' and 'table.tex' with your actual file names
generate_latex_table('d500.txt', 'd1000.txt', 'data-memoryless.txt', 'full-table.tex')
