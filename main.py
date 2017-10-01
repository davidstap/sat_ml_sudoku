import subprocess
import numpy as np
from pprint import pprint
from sudoku import load_data

def clean_output(output):
    statistics_list = []
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
        if statistics:
            statistics_list.append(statistics[0:10])
    column_names = ["Seconds", "Level", "Variables", "Used", "Original", "Conflicts","Learned","Limit","Agility", "Mb"]
    return column_names, np.array(statistics_list)

# Run sudoku and catch terminal output
proc = subprocess.Popen(["python", "-c", "import sudoku; sudoku"], stdout=subprocess.PIPE)
out = str(proc.communicate()[0])

# Analyze terminal output and return the relevant statistics
stat_names, statistics = clean_output(out)
nr_conflicts = statistics[:,5].astype(int)
print("nr_conflicts", nr_conflicts)
# Load features
feature_names, features = load_data()
print('Features:\n',feature_names,'\n\nStatistics:\n',stat_names)

# Remove puzzle, guesses and backtracks from features
for x in features:
    del x[0]
    del x[8]
    del x[7]
del feature_names[0]
del feature_names[8]
del feature_names[7]
feature_names.append("Conflicts")
features = np.array(features).astype(int)


# Save features along with the target (nr_conflicts)
data = np.column_stack((features, nr_conflicts))
data_names = np.array(feature_names).reshape((len(feature_names),1)).T
data = np.concatenate((data_names,data),axis=0)
# np.save('data/ML_data', data)
print('\nFeature matrix plus targets is saved to data/ML_data.npy\n')
print('Sample of data:')
print(data)
