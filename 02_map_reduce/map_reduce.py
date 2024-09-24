import string
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict

# Функція для видалення знаків пунктуації
def remove_punctuation(text:str) -> str:
    """removes punctuation from all text

    Args:
        text (str): full text

    Returns:
        str: text without punctuation
    """
    return text.translate(str.maketrans("", "", string.punctuation))

def map_function(word:str) -> tuple[str,int]:
    """mapping word with 1, like appearence in text

    Args:
        word (str): word to map

    Returns:
        tuple[str,int]: mapped tuple
    """
    return word, 1

def shuffle_function(mapped_values:list[tuple[str,int]])-> list[tuple[str, list[int]]]:
    """combines all appearences of a word for all words

    Args:
        mapped_values (list[tuple[str,int]]): list of tuples of word and appearence

    Returns:
        list[tuple[str, list[int]]]: list of words with list of their appearences
    """
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()

def reduce_function(key_values:tuple[str, list[int]]) -> tuple[str,int]:
    """counts word appearences

    Args:
        key_values (tuple[str, list[int]]): word with list of it appearences

    Returns:
        tuple[str,int]: word with it counted appearence
    """
    key, values = key_values
    return key, sum(values)

# Виконання MapReduce
def map_reduce(text:str, search_words:list[str]=None) -> dict[str,int]:
    """main MapReduce function that produces 3 phases of this pattern

    Args:
        text (str): full text to be produced
        search_words (list[str], optional): list of words to be searched. Defaults to None.

    Returns:
        dict[str,int]: dictionary of words and their appearence
    """
    # Видалення знаків пунктуації
    text = remove_punctuation(text)
    words = text.split()

    # Якщо задано список слів для пошуку, враховувати тільки ці слова
    if search_words:
        words = [word for word in words if word in search_words]

    # Паралельний Мапінг
    with ThreadPoolExecutor() as executor:
        mapped_values = list(executor.map(map_function, words))

    # Крок 2: Shuffle
    shuffled_values = shuffle_function(mapped_values)

    # Паралельна Редукція
    with ThreadPoolExecutor() as executor:
        reduced_values = list(executor.map(reduce_function, shuffled_values))

    return dict(reduced_values)
