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

    Params:
        corpus -- dict mapping a page name to a set of all pages linked to by that page.
        page -- string representing which page the surfer is on
        damping_factor -- float representing damping factor used for generating probabilities
    
    Return:
        dict with a key for each page in the corpus. 
        Each key should be mapped to a val representing the probability that a random surfer would choose that page next.
        Probabilties must sum to 1.
    """
    # Define initial model
    initial_model = {}

    # Set flag for page with links
    flag = False if len(corpus[page]) == 0  else True

    for key in corpus.keys():
        initial_model.update({key:0})
        initial_model[key] += (1-damping_factor) * (1/len(corpus.keys())) if flag else (1/len(corpus.keys()))

    # Determine probability distribution
    if flag:
        for val in corpus[page]:
            initial_model[val] += damping_factor * (1/len(corpus[page]))
    
    return initial_model 


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Determine first page at random
    current_page = random.sample(list(corpus.keys()), 1)[0]

    # Add a value to the first sample selected
    pagerank = corpus.fromkeys(corpus, 0)
    pagerank[current_page] += 1

    # Sample from 1->n-1
    for _ in range(1, n):
        choice_dist = transition_model(corpus=corpus, page=current_page, damping_factor=damping_factor)
        current_page = random.choices(list(choice_dist.keys()), weights=list(choice_dist.values()), k=1)[0]
        pagerank[current_page] += 1
    
    # Normalize pagerank
    total = sum(list(pagerank.values()))

    for key in pagerank.keys():
        pagerank[key] /= total
    
    return pagerank

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    N = len(corpus)
    pagerank = {page: 1 / N for page in corpus}  # Initialize each page's rank equally
    tolerance = 1e-3  # Convergence tolerance
    ite = 0  # Iteration counter

    while True:
        new_pagerank = {}

        # Calculate the new PageRank for each page
        for page in corpus:
            rank_sum = 0
            for other_page in corpus:
                if page in corpus[other_page]:  # If this page is linked by another page
                    rank_sum += pagerank[other_page] / len(corpus[other_page])
                if not corpus[other_page]:  # Handle pages with no outgoing links (dangling nodes)
                    rank_sum += pagerank[other_page] / N
            
            # Apply damping factor
            new_pagerank[page] = (1 - damping_factor) / N + damping_factor * rank_sum
        
        # Check for convergence
        total_change = sum(abs(new_pagerank[page] - pagerank[page]) for page in corpus)
        if total_change < tolerance:
            break

        # Update pagerank for the next iteration
        pagerank = new_pagerank
        ite += 1

    return pagerank




if __name__ == "__main__":
    main()
