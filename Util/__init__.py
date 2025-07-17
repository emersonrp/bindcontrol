import re
# https://stackoverflow.com/questions/11245481/find-the-smallest-unique-substring-for-each-string-in-an-array
#
# Oho I see that I used the "brute force" method from the above URL instead
# of the "elegant" one.  Still it's blazingly fast for these six short strings,
# enough so that we can use it on every TextCtrl change.  If people start to
# complain of lag, we can experiment with the elegant one.
def FindSmallestUniqueSubstring(names):
    uniqueNames = [''] * len(names)
    ### For each name
    for nameInd, name in enumerate(names):
        ### For each possible substring length
        for windowSize in range(1,len(name)+1):
            ### For each starting index of a substring
            for substrInd in range(0, len(name)-windowSize+1):
                substr = name[substrInd:substrInd+windowSize].lower()
                foundMatch = False
                ### For each other name
                for otherNameInd in range(0, len(names)):
                    if (nameInd != otherNameInd) and (names[otherNameInd].lower().find(substr) >= 0):
                        foundMatch = True
                        break

                if not foundMatch:
                    ### This substr works!
                    # If it contains a space, put "" around it
                    if re.match(r'\s', substr):
                        substr = f'"{substr}"'
                    uniqueNames[nameInd] = substr
                    break
            else:
                # continue if the inner loop did not break
                continue
            # Inner loop broke, break again
            break

    return uniqueNames
