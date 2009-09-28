import re

comment_pattern = re.compile("//.*")

def parse(problem_set):
    data = {}
    columns = {}
    with open("../prog1data/{0}/{0}.names".format(problem_set)) as names_file:
        i = 0
        for line in names_file:
            line = line.strip()
#            match = comment_pattern.search(line)
            line = re.sub(comment_pattern, "", line)
            if line:
               line = re.sub(r"\s+", "", line)
               line = line.strip(".")
               if i == 0:
                   #First line has to be class labels
                   if "0,1" in line:
                       i += 1
                       continue
               else:
                   label, values = line.split(":")
                   columns[i-1] = (label, values.split(","))
                   i += 1
        columns[len(columns)] = ("class label", ["0","1"])
            
    with open("../prog1data/{0}/{0}.data".format(problem_set)) as data_file:
        for line in data_file:
            line = line.strip()
            line = re.sub(comment_pattern, "", line)
            if line:
                line = re.sub(r"\s+", "", line)
                line = line.strip(".")
                parts = line.split(",")
                if parts[0] in columns[0][1]:
                    data[parts[0]] = []
                else:
                    continue
                for i in range(1,len(parts)):
                    part = parts[i]
                    if part in columns[i][1]:
                        data[parts[0]].append(part)
                    elif "continuous" in columns[i][1]:
                        try:
                            part = float(part)
                            data[parts[0]].append(part)
                        except ValueError:
                            if part in "?":
                                data[parts[0]].append(None)
                    elif part in "?":
                        data[parts[0]].append(None)
    return (columns, data)