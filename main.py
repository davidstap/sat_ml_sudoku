import subprocess
proc = subprocess.Popen(["python", "-c", "import sudoku; sudoku"], stdout=subprocess.PIPE)
out = proc.communicate()[0]
print(out.upper())
