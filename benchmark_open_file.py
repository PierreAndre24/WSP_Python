import os, time
import sequence_splitter as seqspl

if __name__ == '__main__':
    filepath ='/Users/pierre-andremortemousque/Documents/Research/GitHub/Data'
    filename = 'stat8_1124.lvm' # 10 MB
    filename = 'stat8_1229_uspm.lvm' # 47 MB
    #filename = 'stat8_1325_00000.lvm' #400 MB

    filein = open(filepath + os.sep + filename, 'r') # ~ 12 ms / 10MB file
    filein_txt = filein.readlines()
    filein.close()

    filein_txt = filein_txt[81:]
    # ~ 35 ms / 10 MB file
    # ~ 298 ms / 47 MB file
    # ~ 2.9 s / 400 MB file
    seq = seqspl.ssplit2(filein_txt,['\r\n'])

    print len(seq)
    print 101 * 101

    # ti = time.clock()
    # tf = time.clock()
    # print (tf-ti)

    #print seq
