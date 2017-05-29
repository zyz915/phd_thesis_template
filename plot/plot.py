import matplotlib.pyplot as plt

colorsm= ['#729ece', '#ff9e4a', '#67bf5c', '#ed665d', '#ad8bc9', '#a87861']
colors = ['#1F78B4', '#FF7F0E', '#2CA02C', '#D63728', '#9467BD', '#A8786E', '#DD97CA']
cores = [4, 8, 12, 16]

def get(lst, idx):
    ret = []
    l = len(lst)
    for i in range(0, l):
        try:
            ret.append(lst[i][idx])
        except:
            print lst
    ret.sort()
    return sum(ret) / l

def parse(fname):
    f = file(fname, "r")
    #print fname
    dic = {}
    while (True):
        line = f.readline();
        if (not line): break;
        if (line.startswith("$")):
            cont = line.strip().split(" ")
            prog = cont[1]
            data = cont[2]
            core = int(cont[3])
            time = int(cont[4])
            if (not prog in dic):
                dic[prog] = {}
            if (not data in dic[prog]):
                dic[prog][data] = {}
            if (not core in dic[prog][data]):
                dic[prog][data][core] = []
            step = 0
            while (True):
                line = f.readline()
                if (line.startswith("Dump")):
                    break
                if (line.startswith("Superstep")):
                    step += 1
                if (line.startswith("Communication Time :")):
                    comm = float(line.split(" ")[3])
                if (line.startswith("Communication Time:")):
                    comm = float(line.split(" ")[2])
                if (line.startswith("Total Computational")):
                    comp = float(line.split(" ")[4])
                if (line.startswith("Total Running")):
                    comp = float(line.split(" ")[3])
            print prog, data, time, core, comp, comm, step
            dic[prog][data][core].append((core, comp, comm, step))
    f.close()
    return dic

dic0 = parse("raw-pregel.txt");
dic1 = parse("raw-palgol.txt");
dic2 = parse("raw-custom.txt");

cores = [4, 8, 12, 16]
M = 3.0

# print value
for prog in dic0:
    d0 = dic0[prog]
    d1 = dic1[prog]
    d2 = dic2[prog]
    for data in d0:
        lst = []
        out = prog + " : " + data
        for c in cores:
            out += (" & %.2f" % (get(d0[data][c], 1)))
            out += (" & %.2f" % (get(d1[data][c], 1)))
            out += (" & %.2f" % (get(d2[data][c], 1)))
        out += " \\\\"
        print out
print ""


# bar plot for execution and communication
'''
for prog0 in dic0:
    tot = 1 + len(mp[prog0])
    for data in dic0[prog0]:
        d = dic0[prog0]
        base = -tot * 0.5
        x  = []
        y1 = []
        y2 = []
        for c in cores:
            x.append(d[data][c][0]/M+base*0.5)
            y1.append(d[data][c][1])
            y2.append(d[data][c][2])
        plt.title(prog0 + " " + data)
        plt.bar(x, y1, 0.4, color=colors[0], label="pregel")
        plt.bar(x, y2, 0.4, color=colorsm[0], bottom=y1)
        plt.xticks([x/2-0.05 for x in cores], cores)
        plt.xlim(xmin=4/M-0.15-tot*0.25, xmax=16/M+0.05+tot*0.25)
        shf = 1
        for prog1 in mp[prog0]:
            d = dic1[prog1]
            x  = []
            y1 = []
            y2 = []
            for c in cores:
                x.append(d[data][c][0]/M+(base+shf)*0.5)
                y1.append(d[data][c][1])
                y2.append(d[data][c][2])
            plt.bar(x, y1, 0.4, color=colors[shf], label="palgol")
            plt.bar(x, y2, 0.4, color=colorsm[shf], bottom=y1)
            shf += 1
        shf = 2
        plt.xlabel("number of cores")
        plt.ylabel("execution time (s)")
        plt.legend(loc="upper right")
        plt.savefig("time_" + prog0 + "_" + data + ".pdf")
        plt.clf()
'''

exit()

for prog in dic0:
    lst = {}
    for data in dic1[prog]:
        lst[data] = []
        lst[data].append(get(dic1[prog][data][4], 3))
    for data in dic0[prog]:
        lst[data].append(get(dic0[prog][data][4], 3))
    for data in lst:
        x = lst[data][0]
        y = lst[data][1]
        print prog, data, lst[data], ("%.1f%%" % ((x-y)*100./y))

for prog0 in dic0:
    tot = 1 + len(mp[prog0])
    for data in dic0[prog0]:
        base = -tot * 0.5
        d = dic0[prog0]
        x  = []
        y1 = []
        for c in [0, 1, 2, 3]:
            x.append(d[data][c][0]/M+base*0.5)
            y1.append(d[data][c][3])
        plt.title(prog0 + " " + data)
        plt.bar(x, y1, 0.4, color=colors[0], label="pregel")
        plt.xticks([x/M-0.05 for x in cores], cores)
        plt.xlim(xmin=4/M-0.15-tot*0.25, xmax=16/M+0.05+tot*0.25)
        shf = 1
        for prog1 in mp[prog0]:
            d = dic1[prog1]
            x  = []
            y1 = []
            for c in [0, 1, 2, 3]:
                x.append(d[data][c][0]/M+(base+shf)*0.5)
                y1.append(d[data][c][3])
            plt.bar(x, y1, 0.4, color=colors[shf], label="palgol")
            shf += 1
        plt.xlabel("number of cores")
        plt.ylabel("number of supersteps")
        plt.legend(loc="lower right")
        plt.savefig("step_" + prog0 + "_" + data + ".pdf")
        plt.clf()
