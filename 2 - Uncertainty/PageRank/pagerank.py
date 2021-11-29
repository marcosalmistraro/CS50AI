import copy
import math
import numpy as np
import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # initialize the dictionary to be returned
    result_dict = dict()

    if corpus.get(page):

        # with probability ´1 - damping_factor´ pick a  random page from the corpus
        for item in list(corpus):
            if item != page:
                result_dict[item] = (1 - damping_factor)/(len(corpus) - 1)

        # with probability ´damping_factor´ pick an item among those linked by the page
        for item in list(corpus[page]):
            if item != page:
                result_dict[item] += (damping_factor / len(corpus[page]))

    # if page has no outgoing links within the corpus, pick one at random with equal probability
    else:
        for item in list(corpus):
            result_dict[item] = 1 / len(corpus)

    return result_dict


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # initialize function by picking a random page
    page = random.choice(list(corpus.keys()))
    ranks = dict()

    for page in corpus:
        ranks[page] = 0.0

    for iteration in range(n):

        # next page is generated based on the transition model
        land_page_prob = transition_model(corpus, page, damping_factor).items()

        land_page_list = []
        prob_list = []
        for i in land_page_prob:
            land_page, prob = i
            land_page_list.append(land_page)
            prob_list.append(prob)

        page = np.random.choice(a=land_page_list,
                                size=1,
                                p=prob_list)[0]

        # normalize the results
        ranks[page] += (1.0 / n)

    return ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # set conditions for initializing the loop
    ranks = dict()
    threshold = 0.001
    n = len(corpus)
    change = True

    # assign initial values to the pages in the corpus
    for page in corpus:
        ranks[page] = 1.0 / n

    # compute new pagerank values based on the current ones, in a loop
    while change:
        change = False
        # extract old_ranks dictionary to calculate threshold
        old_ranks = copy.deepcopy(ranks)
        # apply given formula for calculation of the pagerank value
        for page in corpus:
            ranks[page] = ((1 - damping_factor)/n) + \
                        (damping_factor * prob_link_page(corpus, ranks, page))

            # if change is bigger than the threshold, keep looping
            if abs(ranks[page] - old_ranks[page]) > threshold:
                change = True

    return ranks


def prob_link_page(corpus, ranks, i):
    # calculate probability of landing on a page from any other linking page
    prob_page = sum(ranks[page]/len(corpus[page]) for page in corpus if i in corpus[page])
    return prob_page


if __name__ == "__main__":
    main()
