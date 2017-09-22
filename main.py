import subprocess

def clean_output(output):
    clean_output = []
    output = [a.split() for a in out.split('*'*80)]
    for line in output:
        statistics = []
        for item in line:
            try:
                statistics.append(float(item))
            except ValueError:
                continue
        if len(statistics) == 21:
            del statistics[10]
        elif len(statistics) == 22:
            del statistics[10]
            del statistics[10]
        clean_output.append(statistics)
    column_names = ["seconds", "level", "variables", "used", "original", "conflicts","learned","limit","agility", "mb"]
    return column_names, clean_output


# run sudoku and catch terminal output
proc = subprocess.Popen(["python", "-c", "import sudoku; sudoku"], stdout=subprocess.PIPE)
out = str(proc.communicate()[0])
column_names, clean_output = clean_output(out)
print(len(column_names), len(clean_output))
