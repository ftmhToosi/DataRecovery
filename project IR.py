import csv
import string

import nltk
from nltk.stem import LancasterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize


# get csv filename and numbers of documents,
# return documents in object with document id
def get_csv_documents(filename, documents_number):
    file = open(filename)
    csvreader = csv.reader(file)
    # remove headers
    headers = next(csvreader)

    documents = {}
    document_id = 1

    for document in csvreader:
        # add new document -> key = id, value = document detail list
        documents[document_id] = document

        if document_id == documents_number: break
        document_id += 1

    return documents


# case folding, tokenize, lemmatizate documents
def preprocessing(documents: dict):
    preprocessed_documents = {}
    for document_id in documents:
        # just document title and plot
        text = documents[document_id][0] + ' ' + documents[document_id][1]
        text = text.casefold()  # case folding
        text = text.translate(str.maketrans('', '', string.punctuation))  # remove punctuations
        tokens = word_tokenize(text)  # get text tokens
        # stemming tokens
        lancaster = LancasterStemmer()
        tokens = [lancaster.stem(word) for word in tokens]
        # lemmatization tokens
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(word) for word in tokens]

        preprocessed_documents[document_id] = tokens

    return preprocessed_documents


def get_stop_words(preprocessed_documents: dict, number):
    stop_words = {}
    for document_id in preprocessed_documents:
        for token in preprocessed_documents[document_id]:
            if token not in stop_words:
                stop_words[token] = 1
            else:
                stop_words[token] += 1

    stop_words = dict(sorted(stop_words.items(), key=lambda item: item[1], reverse=True)[:number])

    return stop_words


def get_positional_index(preprocessed_documents: dict, stop_words: dict):
    positional_index = {}

    for document_id in preprocessed_documents:
        index_counter = -1
        for token in preprocessed_documents[document_id]:
            index_counter += 1
            # if token in stop-words skip token
            if token in stop_words: continue

            # if token not in positional_index yet, add them to positional_index without values
            if token not in positional_index:
                positional_index[token] = {}
                positional_index[token]['docFreq'] = 0
                positional_index[token]['positions'] = {}

            if document_id not in positional_index[token]['positions']:
                positional_index[token]['docFreq'] += 1
                positional_index[token]['positions'][document_id] = []

            positional_index[token]['positions'][document_id].append(index_counter)

    return positional_index


def get_number(message):
    input_text = input(f'{message}: ')
    if input_text.strip().isdigit():
        return int(input_text)
    else:
        return False


def menu():
    print()
    print('1 -> show a document')
    print('2 -> show all documents')
    print('3 -> add new document')
    print('4 -> delete a document')
    print('5 -> show a term positional index')
    print('6 -> show all terms positional index')
    print('7 -> show a document preprocessing')
    print('8 -> show all documents preprocessing')
    print('9 -> show stop-words')
    print('10 -> quit')
    input_number = get_number('select from menu')

    if input_number:
        return input_number
    else:
        return 10


def print_object(obj: dict):
    for item in obj:
        print(item, '-> ', obj[item])


def print_document(documents):
    id_checker = True
    while (id_checker):
        document_id = get_number('enter document id, enter something that is not number to cancel')
        if not document_id:
            print('show a documents canceled')
            id_checker = False
        if document_id in documents:
            print(documents[document_id])
            id_checker = False
        else:
            print('wrong id')


def print_term_positional_index(positional_index):
    id_checker = True
    while (id_checker):
        term = input('enter a term, enter + to cancel: ')
        if term == '+':
            print('show a term canceled')
            id_checker = False
        if term in positional_index:
            print(term, ': ', positional_index[term])
            id_checker = False
        else:
            print('wrong term')


def get_document():
    input_checker = True
    title = None
    plot = None
    while (input_checker):
        title = input('enter document title: ')
        plot = input('enter document plot: ')

        if title and plot:
            input_checker = False
        else:
            print('both fields are required.')

    return [title, plot]


def main():
    # nltk.download('punkt')
    # nltk.download('wordnet')
    # nltk.download('omw-1.4')

    documents = {}
    preprocessed_documents = {}
    stop_words = {}
    positional_index = {}

    input_checker = True

    while (input_checker):
        documents_number = get_number('enter number of documents for import')
        if documents_number and documents_number in range(50, 6000):
            input_checker = False
        else:
            print('enter a valid number, number must be in 50 to 6000')

    try:
        documents = get_csv_documents('train.csv', documents_number)
        print('documents loading done.')
    except:
        print('documents loading failed.')
        quit()

    try:
        preprocessed_documents = preprocessing(documents)
        print('preprocessing done.')
    except:
        print('preprocessing failed.')
        quit()

    input_checker = True
    while (input_checker):
        stop_words_numbers = get_number('enter number of stop-words')
        if stop_words_numbers and stop_words_numbers in range(10, 50):
            input_checker = False
        else:
            print('enter a valid number, stop-words must be in 10 to 50')

    try:
        stop_words = get_stop_words(preprocessed_documents, number=stop_words_numbers)
        print('stop-words done')
    except:
        print('stop-words failed')
        quit()

    try:
        positional_index = get_positional_index(preprocessed_documents, stop_words)
        print('positional index done')
    except:
        print('positional index failed')
        quit()

    input_checker = True

    while (input_checker):
        menu_input = menu()

        # exit
        if menu_input == 10:
            input_checker = False

        # print a document by id
        elif menu_input == 1:
            print_document(documents)

        # print all documents
        elif menu_input == 2:
            print_object(documents)

        # add a document
        elif menu_input == 3:
            new_document = get_document()
            key = (list(documents.keys())[-1]) + 1
            documents[key] = new_document
            print(f'document: {documents[key]} id: {key} inserted')

            # refresh preprocessing
            try:
                preprocessed_documents = {}
                preprocessed_documents = preprocessing(documents)
                print('refresh preprocessing done.')
            except:
                print('refresh preprocessing failed.')
                quit()

            # refresh positional index
            try:
                positional_index = {}
                positional_index = get_positional_index(preprocessed_documents, stop_words)
                print('refresh positional index done')
            except:
                print('refresh positional index failed')
                quit()


        # remove a document
        elif menu_input == 4:
            document_id = get_number('enter document id')
            if document_id in documents:
                del documents[document_id]
                print(f'document {document_id} was deleted.')
            else:
                print('document id doesnt exist.')

            # refresh preprocessing
            try:
                preprocessed_documents = {}
                preprocessed_documents = preprocessing(documents)
                print('refresh preprocessing done.')
            except:
                print('refresh preprocessing failed.')
                quit()

            # refresh positional index
            try:
                positional_index = {}
                positional_index = get_positional_index(preprocessed_documents, stop_words)
                print('refresh positional index done')
            except:
                print('refresh positional index failed')
                quit()

        # print a term
        elif menu_input == 5:
            print_term_positional_index(positional_index)

        # print all terms
        elif menu_input == 6:
            print_object(positional_index)

        # print a document preprocessing
        elif menu_input == 7:
            print_document(preprocessed_documents)

        # print all document preprocessing
        elif menu_input == 8:
            print_object(preprocessed_documents)

        # print stop-words
        elif menu_input == 9:
            print_object(stop_words)

        else:
            print('wrong number... please select from menu numbers.')

    print('end.')
    quit()


if __name__ == "__main__":
    main()
