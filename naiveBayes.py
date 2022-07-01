import math

#John Howard
#932528265
#Due 5/31/2022

#Consider this read training data, was easier to debug this way.  Each class represents one word.
#Each of the four probs represents the probability that that word is T,F given the Class label being T, F
class prob_table:
    def __init__(self, word,TgiveF,TgiveT,FgiveT,FgiveF):
        self.word = word
        self.probTgiveF = TgiveF
        self.probTgiveT = TgiveT
        self.probFgiveT = FgiveT
        self.probFgiveF = FgiveF



#easiest way to nest arrays
class feature:
    def __init__(self): 
        self.vector = []

#trim's repeat words from the wordlist
def list_trim(wordlist):
    res = []
    [res.append(x) for x in wordlist if x not in res]
    return res

#strips the sentences of punctuation, truncates into individual words
def create_vocab(wordlist, trainingList):

    punc = '''!()[]{}:?,.;'"<>/@#$%^&*~`_+=|'''
    spacing = '''-'''

    for i in range(len(trainingList)):
        newString = trainingList[i]

        for ele in newString:
            if ele in punc:
                newString = newString.replace(ele, "")
            if ele in spacing:
                newString = newString.replace(ele, " ")

        newString = newString.lower()
        newString = newString.split()
    
        for j in range(len(newString)-1):
            wordlist.append(newString[j])

    return wordlist

#removes digits from the vocab list
def remove_num(feature_list):
    #Iterate through feature list words and eliminate numbers#

    num = '''1234567890'''
    index = 0

    for i in range(len(feature_list)):
        for ele in feature_list[i]:
            if ele in num:
                index = index +1

    feature_list.sort(reverse=True)

    for i in range(index-1):
        feature_list.pop()

    for i in range(len(feature_list)):
        for ele in feature_list[i]:
            if ele in num:
                index = index +1

    return feature_list

#Creates the prob table objects for each word, forms a list from them, returns that list of prob table objects            
def create_table(wordlist, feature_list,cdF,cdT,end):
    #Create a prob object for each word in wordlist
    prob = []
    #print(cdF, cdT)
    cdF = cdF+2
    cdT = cdT+2

    for i in range(len(wordlist)-1):
        temp_count = 1
        for j in range(len(feature_list)):
            if feature_list[j].vector[i] == '1' and feature_list[j].vector[end] == '1':
                temp_count = temp_count+1
        
        TgiveT = temp_count/cdT
        
        temp_count = 1
        for j in range(len(feature_list)):
            if feature_list[j].vector[i] == '1' and feature_list[j].vector[end] == '0':
                temp_count = temp_count+1
        TgiveF = temp_count/cdF

        temp_count = 1
        for j in range(len(feature_list)):
            if feature_list[j].vector[i] == '0' and feature_list[j].vector[end] == '1':
                temp_count = temp_count+1
        
        FgiveT = temp_count/cdT
        
        temp_count = 1
        for j in range(len(feature_list)):
            if feature_list[j].vector[i] == '0' and feature_list[j].vector[end] == '0':
                temp_count = temp_count+1
        FgiveF = temp_count/cdF
        temp_table = prob_table(wordlist[i],TgiveF,TgiveT,FgiveT,FgiveF)
        prob.append(temp_table)
    #print("Bad review: ", cdF, " Good Review: ", cdT)


    return prob

#calculates the accuraccy based off of results
def accuracy(results, feature_list, end):
    count = 0
    total = 499

    for i in range(len(results)):
        if results[i] == feature_list[i].vector[end]:
            count = count +1
        #else:
            #print(i)

    acc = count/total*100
    return acc

#Test to strip sentences of punctuation#
#Opening Files#
file_object = open('trainingSet.txt','r')
file_object2 = open('testSet.txt','r')

clear_object = open('preprocessed_train.txt', 'w')
clear_object.write("")
clear_object.close()

clear_object = open('preprocessed_test.txt', 'w')
clear_object.write("")
clear_object.close()

write_object = open('preprocessed_train.txt','a')

trainingList = file_object.readlines()
testList = file_object2.readlines()

##
##Creating pre processed training data
##
wordlist = []
feature_list = []

wordlist = create_vocab(wordlist, trainingList)
wordlist = remove_num(wordlist)
wordlist = list_trim(wordlist)
wordlist.sort()
wordlist.append("classlabel")
M = len(wordlist)

for i in range(len(trainingList)):
    newvector = feature()

    for j in range(M-1):
        if wordlist[j] in trainingList[i]:
            newvector.vector.append('1')
        else:
            newvector.vector.append('0')
    if " 1" in trainingList[i]:
        newvector.vector.append('1')
    else:
        newvector.vector.append('0')
    feature_list.append(newvector)

write_object.write(wordlist[0])
for i in range(len(wordlist)-1):
    write_object.write(", ")
    write_object.write(wordlist[i+1])

write_object.write("\n")

for i in range(len(feature_list)):
    write_object.write(feature_list[i].vector[0])
    for j in range(len(feature_list[i].vector)-1):
        write_object.write(", ")
        write_object.write(feature_list[i].vector[j+1])
    write_object.write("\n")

write_object.close()

##
##Creating Preprocessed test Data##
##

write_object= open('preprocessed_test.txt', 'a')

test_wordlist = []
test_featurelist = []

test_wordlist = create_vocab(test_wordlist, testList)
test_wordlist = remove_num(test_wordlist)
test_wordlist = list_trim(test_wordlist)
test_wordlist.append("classlabel")
test_wordlist.sort()
test_M = len(test_wordlist)

#print("M", test_M)

for i in range(len(testList)):
    newvector = feature()

    for j in range(test_M):
        if test_wordlist[j] in testList[i]:
            newvector.vector.append('1')
        else:
            newvector.vector.append('0')
    if " 1" in testList[i]:
        newvector.vector.append('1')
    else:
        newvector.vector.append('0')
    test_featurelist.append(newvector)

write_object.write(test_wordlist[0])
for i in range(len(test_wordlist)-1):
    write_object.write(", ")
    write_object.write(test_wordlist[i+1])

write_object.write("\n")

for i in range(len(test_featurelist)):
    write_object.write(test_featurelist[i].vector[0])
    for j in range(len(test_featurelist[i].vector)-1):
        write_object.write(", ")
        write_object.write(test_featurelist[i].vector[j+1])
    write_object.write("\n")

############################

#Going to run on training set.txt#
#already have training list, need to re read into training data, first do the training step#
#Each word will have a probability word = T given CD = 1 and word = T given CD = 0 





cdF = 0
cdT = 0
end = len(wordlist)-1
prob_list = []

for i in range(len(feature_list)):
    if feature_list[i].vector[end] == '1':
        cdT = cdT +1
    else:
        cdF = cdF +1

total = cdF+cdT
ProbCDT = cdT/total
ProbCDF = 1-ProbCDT

prob_list = create_table(wordlist,feature_list,cdF,cdT,end)
#print(prob_list[0].word, ": ", prob_list[0].probTgiveT, ", ", prob_list[0].probTgiveF, ", ", prob_list[0].probFgiveT, ", ", prob_list[0].probFgiveF)


##Below is the predictions on the feature_list that came from training data##
results = []
for i in range(len(feature_list)):
    prediction_list = []
    for j in range(len(wordlist)-1):
        if feature_list[i].vector[j] == '0':
            prediction_list.append(prob_list[j].probFgiveT)
            #print(prob_list[j].probFgiveT)
        else:
            prediction_list.append(prob_list[j].probTgiveT)
    prediction_list.append(ProbCDT)

    for k in range(len(prediction_list)):
        prediction_list[k] = math.log(prediction_list[k])
    finalT = sum(prediction_list)
    #finalT = math.log(finalT)
    #print('finalT: ', finalT)

    prediction_list_F = []
    for j in range(len(wordlist)-1):
        if feature_list[i].vector[j] == '0':
            prediction_list_F.append(prob_list[j].probFgiveF)
            #print(prob_list[j].probFgiveT)
        else:
            prediction_list_F.append(prob_list[j].probTgiveF)
    prediction_list_F.append(ProbCDF)

    for k in range(len(prediction_list_F)):
        prediction_list_F[k] = math.log(prediction_list_F[k])
    finalF = sum(prediction_list_F)
    #finalF = math.log(finalF)
    #print("finalF: ", finalF)

    if finalT > finalF:
        results.append('1')
    else:
        results.append('0')

write_object = open('results.txt', 'w')


acc = accuracy(results, feature_list,end)
print("Accuracy on training data: ", acc, "%")

write_object.write("Accuracy on training data: ")
stracc = str(acc)
write_object.write(stracc)
write_object.write("%,  Used trainingSet.txt for both training and testing\n")


##Below is the predictions on the feature_list that came from test data##
results = []
#print(test_featurelist[0].vector[1345])

for i in range(len(test_featurelist)):
    prediction_list = []
    for j in range(len(wordlist)-1):
        if test_featurelist[i].vector[j] == '0':
            prediction_list.append(prob_list[j].probFgiveT)
            #print(prob_list[j].probFgiveT)
        else:
            prediction_list.append(prob_list[j].probTgiveT)
    prediction_list.append(ProbCDT)

    for k in range(len(prediction_list)):
        prediction_list[k] = math.log(prediction_list[k])
    finalT = sum(prediction_list)
    #finalT = math.log(finalT)
    #print('finalT: ', finalT)

    prediction_list_F = []
    for j in range(len(wordlist)-1):
        if test_featurelist[i].vector[j] == '0':
            prediction_list_F.append(prob_list[j].probFgiveF)
            #print(prob_list[j].probFgiveT)
        else:
            prediction_list_F.append(prob_list[j].probTgiveF)
    prediction_list_F.append(ProbCDF)

    for k in range(len(prediction_list_F)):
        prediction_list_F[k] = math.log(prediction_list_F[k])
    finalF = sum(prediction_list_F)
    #finalF = math.log(finalF)
    #print("finalF: ", finalF)

    if finalT > finalF:
        results.append('1')
    else:
        results.append('0')

acc = accuracy(results, test_featurelist,end)
print("Accuracy on test data: ", acc, "%")


write_object.write("Accuracy on test data: ")
stracc = str(acc)
write_object.write(stracc)
write_object.write("%,  Used trainingSet.txt for training and testSet.txt for testing")
write_object.close()
