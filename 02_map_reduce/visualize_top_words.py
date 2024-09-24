import matplotlib.pyplot as plt
from collections import Counter

def visualize_top_words(words:dict[str,int], top_n:int=20):
    """visualizes most frequent words

    Args:
        words (dict[str,int]): dict of words with their frequency
        top_n (int, optional): amount of words to visualize. Defaults to 20.
    """
    top_words = Counter(words).most_common(top_n)

    msg = f"Top {top_n} offrequent  words"
    print(msg)
    for word, freq in top_words:
        print(f"{word}: {freq}")

    words, counts = zip(*top_words)

    plt.figure(figsize=(10, 8))
    plt.barh(words, counts, color="skyblue")
    plt.xlabel("Frequency")
    plt.ylabel("Words")
    plt.title(msg)
    plt.gca().invert_yaxis()
    plt.show()
