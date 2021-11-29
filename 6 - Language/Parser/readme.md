# 6. Questions

This question-answering system performs two tasks: document retrieval and passage retrieval. 
The system has have access to a corpus of text documents; when presented with a query (a question in English asked by the user), the program first identifies which documents are most relevant. Once the top documents are found, they are subdivided into passages so that the most relevant one can be determined.

To find the most relevant documents **tf-idf** is used to rank documents based both on term-related and inverse document frequency for words in the query. 
Once the most relevant documents are found, there many possible metrics for scoring passages; in this case a combination of inverse document frequency and a query term density measure is employed.

## Usage

`$ python questions.py corpus`