spnSet = set()
spnAttributeFile1D = {}
spnAttributeFile2D = {}
isdata = ''
testSPN = 'Motor/Generator4InverterControlLimitsRequestOverrideMaximum_spn11929'

# Old file
inF1 = open("python_J1939_Nira_DM_20201121_b_20201121.py", "r")

for line in inF1:

    bitsObtained = ''
    index = 0

    # checking to see if the current line has any data to parse
    try:
        isdata = (line.split(' ')[4].split('[')[0])
    except IndexError:
        pass

    # Different line splits for parsing
    spaceSplit = line.split(' ')
    intSplit = line.split('int')


    if isdata == 'data':

        # Grabbing the SPN
        try:
            spn = line.split(' ')[4].split("'")[1]
            spnSet.add(spn)
        except IndexError:
            pass

        # Grabbing the bits obtained
        for item in spaceSplit:

            if item.find('msg[') != -1:

                index += 1
                bits = item.split('(')[-1].split(",")[0]
                if index > 1:
                    bitsObtained += ',' + bits
                else:
                    bitsObtained += bits
        index = 0
        shifts = ''
        # Grabbing the shifts
        for item in intSplit:

            if item.find('msg[') != -1:
                index += 1
                if spn == testSPN:
                    #print(item.split('),'))
                    pass
                if index > 1:

                    shifts += (', int(' + ','.join(' '.join((item.strip(' (+').split('),')[0:1])).split(',')[0:2]).strip(')')).strip(' ')
                    
                else:
                    shifts = ('int(' + ','.join(''.join((item.strip(' (+').split('))')[0:2])).split(',')[0:2]).strip(')')).strip(' ')

        maxVal = item.split(',')[2].split(')')[0]
        resolution = (float(item.split(',')[2].split(')')[1].strip(' *')))
        #print(resolution)

        try:
            spnAttributeFile1D[spn] = [bitsObtained, shifts, maxVal, resolution]
        except NameError:
            pass


inF1.close()

isdata = ''
# New file
inF2 = open("python_J1939_Nira_DM_20201121_b_20210628.py", "r")

for line in inF2:
    bitsObtained = ''
    index = 0

    try:
        isdata = (line.split(' ')[4].split('[')[0])
    except IndexError:
        pass

    spaceSplit = line.split(' ')
    intSplit = line.split('int')



    if isdata == 'data':

        try:
            spn = line.split(' ')[4].split("'")[1]
            spnSet.add(spn)

        except IndexError:
            pass
        index = 0
        for item in spaceSplit:

            if item.find('msg[') != -1:
                if spn == testSPN:

                    #print(line)
                    pass
                index += 1
                bits = item.split('(')[-1].split(",")[0]
                if index > 1:
                    bitsObtained += ',' + bits
                else:
                    bitsObtained += bits
        shifts = ''
        if spn == testSPN:
            #print(intSplit)
            pass
        index = 0
        for item in intSplit:
            if item.find('msg[') != -1:
                index += 1
                if index > 1:
                    shifts += ', int(' + ','.join(''.join((item.strip(' (+').split('))')[0:2])).split(',')[0:2]).strip(')')# + ')'

                else:
                    shifts += 'int(' + ','.join(''.join((item.strip(' (+').split('))')[0:2])).split(',')[0:2]).strip(')')# + ')'
                    pass

        maxVal = item.split(',')[-1].split(')')[0]
        resolutionSplit = item.split(')')

        for thing in resolutionSplit:
            if thing.find('*') != -1:
                resolution = (float(thing.strip(' *')))


        try:
            spnAttributeFile2D[spn] = [bitsObtained, shifts, maxVal, resolution]
        except NameError:
            pass

inF2.close()

#print(spnAttributeFile1D[testSPN])
#print(spnAttributeFile2D[testSPN])

errors = 0
nices = 0
differences = 0
diff_data = []
error_data = []

for spn in spnSet:
    try:
        if spnAttributeFile1D[spn] == spnAttributeFile2D[spn]:
            if spn == testSPN:
                #print(str(spnAttributeFile1D[spn]) + ' VS ' + str(spnAttributeFile2D[spn]))
                pass
            #print('NICE')
            nices += 1
        else:
         #   print('NOT THE SAME')
            #if spn == testSPN:
            #print(str(spnAttributeFile1D[spn]) + ' VS ' + str(spnAttributeFile2D[spn]))
            #print(spn)
            differences += 1
            diff_data.append(spn)
    except KeyError:
        #print('ERROR')
        error_data.append(spn)
        errors += 1

print('New == Old: ' + str(nices), ', New != Old: ' + str(differences), ', Missing SPNs: ' + str(errors))
print(error_data)