import math
import nltk
from string import punctuation
import sys
import os

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    file_contents = dict()

    for file in os.listdir(directory):
        file_location = os.path.join(directory, file)
        with open(file_location, 'r') as f:
            file_contents[file] = f.read()

    return file_contents


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    document = document.lower()
    tokens = nltk.word_tokenize(document)

    stop_words = nltk.corpus.stopwords.words("english")

    words = [word for word in tokens if word not in stop_words and word not in punctuation]
    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idfs = dict()
    total_documents = len(documents)

    words = set()
    for sublist in documents.values():
        for word in sublist:
            words.add(word)

    for word in words:
        num_doc_with_word = 0

        for document in documents.values():
            if word in document:
                num_doc_with_word += 1

        idf = math.log(total_documents / num_doc_with_word)
        idfs[word] = idf

    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    file_scores = dict()

    for file in files:
        total_tf_idf = 0
        for word in query:
            cumulative = files[file].count(word) * idfs[word]
            total_tf_idf += cumulative
        file_scores[file] = total_tf_idf

    ranked_files = sorted(file_scores.items(), key=lambda x: x[1])
    ranked_files = ranked_files[::-1]
    ranked_files = [x[0] for x in ranked_files]
    ranked_files = ranked_files[:n]

    return ranked_files


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sentence_scores = dict()

    for sentence in sentences:
        words = sentences.get(sentence)
        words_in_query = query.intersection(words)

        idf = 0
        count_words_query = 0
        for word in words_in_query:
            idf += idfs[word]
            count_words_query += 1

        term_density = count_words_query / len(words)

        sentence_scores[sentence] = dict()
        sentence_scores.get(sentence)['idf'] = idf
        sentence_scores.get(sentence)['td'] = term_density

    ranked_sentences = sorted(sentence_scores.items(), key=lambda x: (x[1]['idf'], x[1]['td']))
    ranked_sentences = ranked_sentences[::-1]
    ranked_sentences = [x[0] for x in ranked_sentences]
    ranked_sentences = ranked_sentences[:n]

    return ranked_sentences


if __name__ == "__main__":
    main()
