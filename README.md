# Naive-Bayes-Classifier
Very basic attempt at a naive bayes classifier.

This is a single file python script that reads in two sets of restaurant review data that has been marked positive '1' or negative '0'.  The training data is used to form feature vectors, which are then used to predict the classifier of the test data.  Currently only about 70% accurate

##Edit-1##
In order to fix an error with the list trim function, which was caused by improper use of list comprehension, the method of removing duplicate words from the word list has been changed to a different method (casting to set then back to list)
