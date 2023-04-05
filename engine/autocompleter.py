from typing import List

from engine.term_index import TermIndex, Term


class Autocompleter:
    """
    A class that provides autocomplete suggestions based on a given term index.
    """

    def __init__(self, term_index: TermIndex) -> None:
        """
        Initialize an Autocompleter object.

        Args:
            term_index (TermIndex): An instance of the TermIndex class.
        """
        self.term_index = term_index

    @staticmethod
    def generate_combinations(my_list):
        """
        Generate all possible combinations of terms from the given list.

        Args:
            my_list (list): A list of lists, where each inner list contains Term objects.

        Returns:
            list: A list of lists, where each inner list contains Term objects.
        """
        # If the list is empty, return an empty list
        if len(my_list) == 0:
            return []
        # If the list has only one element, return a list of lists, where each inner list contains one element
        if len(my_list) == 1:
            return [[elem] for elem in my_list[0]]

        # Recursively generate all possible combinations of terms from the remaining list of lists
        sub_combinations = Autocompleter.generate_combinations(my_list[1:])
        result = []
        # Combine the first list element with each sublist from the sub_combinations list
        for elem in my_list[0]:
            for sub_combination in sub_combinations:
                result.append([elem] + sub_combination)

        return result

    def return_matching_terms_deeply(self, matching_terms, input_terms, i):
        """
        Return a list of matching terms taking into account whether the input terms are a substring of a term. finally,
        return the updated index in the input terms list.

         Args:
             matching_terms (list): A list of Term objects that
            match the current input term. input_terms (list): A list of input terms. i (int): The current index in the input terms list.

        Returns:
            tuple: A tuple containing a list of matching terms and the updated index in the input terms list.
        """
        matched_terms = matching_terms
        term_to_evaluate = input_terms[i]
        # Check if there are more input terms and whether they form a substring of a matching term
        while i < len(input_terms) - 1:
            term_to_evaluate += " " + input_terms[i + 1]
            temporal_matching_terms = self.term_index.search(term_to_evaluate)
            if len(temporal_matching_terms) == 0:
                break
            else:
                matched_terms = temporal_matching_terms
                i += 1
        return matched_terms, i + 1

    def suggestions(self, input: str) -> List[List[Term]]:
        """
        Generate autocomplete suggestions based on a given input string.

        Args:
            input (str): The input string to generate suggestions for.

        Returns:
            list: A list of lists, where each inner list contains Term objects.
        """
        # Split the input string into separate terms
        input_terms = input.split()
        input_length = len(input_terms)

        # Return an empty list if the input string is empty
        if input_length == 0:
            return []

        # Create an empty list to store the list of terms for each input term
        list_of_terms = []
        i = 0

        # Iterate through each input term
        while i < input_length:

            # Find all the terms in the term index that match the current input term
            matching_terms = self.term_index.search(input_terms[i])

            # If there are matching terms, try to find deeper matching terms by adding subsequent input terms
            if matching_terms:
                matching_terms2, i = self.return_matching_terms_deeply(matching_terms, input_terms, i)
                # If there are deeper matching terms, add them to the list of terms for the current input term
                list_of_terms.append(matching_terms2 if matching_terms2 else matching_terms)
            else:
                # If there are no matching terms, return an empty list
                return []

        # Generate all possible combinations of terms from the list of terms for each input term
        return Autocompleter.generate_combinations(list_of_terms)


if __name__ == "__main__":
    term = TermIndex()
    autocompleter = Autocompleter(term_index=term)
    print(autocompleter.suggestions("apple doesntexist"))
