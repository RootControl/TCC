import nltk
import csv
from nltk.metrics import ConfusionMatrix

from src.preprocessing.PreprocessingTokens import extract_words, database, verifyPhrase


def list_of_errors(complete_base_test, classified):
    errors = []
    for (phrase, classes) in complete_base_test:
        result = classified.classify(phrase)
        if result != phrase:
            errors.append((classes, result, phrase))

    for (classes, result, phrase) in errors:
        print(classes, result, phrase)


def metrics_array(complete_base_test, classified):
    expected = []
    provided = []
    for (phrase, classes) in complete_base_test:
        result = classified.classify(phrase)
        expected.append(classes)
        provided.append(result)
    return ConfusionMatrix(expected, provided)


base = database('../files/oneFile/classifyFget.csv')


# tmp = database1('../files/oneFile/teste.csv')


from sklearn.model_selection import train_test_split

base_train, base_test = train_test_split(base, test_size=0.33, random_state=14)
complete_base_train = nltk.classify.apply_features(extract_words, base_train)
complete_base_test = nltk.classify.apply_features(extract_words, base_test)



classified = nltk.NaiveBayesClassifier.train(complete_base_train)

print(nltk.classify.accuracy(classified, complete_base_test))



print(metrics_array(complete_base_test, classified))


print(f'{i}: {nltk.classify.accuracy(classified, complete_base_test)}')
# neg = 0
# neu = 0
# pos = 0
#
# with open('../files/oneFile/classify.csv', encoding='utf-8') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     line_count = 0
#     total = 0
#     for row in csv_reader:
#         if line_count == 0:
#             line_count += 1
#         # elif line_count == 801860:
#         #     break
#         elif line_count > 801860:
#             if row[1] == 'negativo':
#                 neg += 1
#             if row[1] == 'neutro':
#                 neu += 1
#             if row[1] == 'positivo':
#                 pos += 1
#             line_count += 1
#             total += 1
#         line_count += 1
#
# print(line_count)
# print(total)
# print(f'Neg: {neg}')
# print(f'Neu: {neu}')
# print(f'Pos: {pos}')
