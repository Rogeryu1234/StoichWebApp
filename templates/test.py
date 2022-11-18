# This is test file.
SumAbundance = 0
ReportStr = ""
ReportStr += 'Input data:\n'.format()
ReportStr += '{}\t\t{}\n'.format('Element', "Counts")
Q = {"O": 4000, "Mg": 2000, "Si": 1000}
# Q = {"O": 0.01, "Mg": 0.02, "Si": 0.05}
for El, Abund in Q.items():
    SumAbundance += Abund
    if Abund > 0.1:
        # Report straightforward percentages.
        ReportStr += '{}\t\t{:.3f}\n'.format(El, Abund)
        # ReportStr += str(El) + "\t\t {:.3f}\n".format(Abund)
    else:
        # For trace elements report ppm.
        ReportStr += '{}\t\t{:.0f} ppm\n'.format(El, Abund*1e4)
        # ReportStr += str(El) + "\t\t" + str(Abund) + "\n"
ReportStr += '{:}\t\t{:.3f}\n'.format('Total:', SumAbundance)
ReportStr += '\n'.format()
print(ReportStr)