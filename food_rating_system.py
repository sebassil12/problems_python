"""
Design a food rating system that can do the following:

    Modify the rating of a food item listed in the system.
    Return the highest-rated food item for a type of cuisine in the system.

Implement the FoodRatings class:

    FoodRatings(String[] foods, String[] cuisines, int[] ratings) Initializes the system. The food items are described by foods, cuisines and ratings, all of which have a length of n.
        foods[i] is the name of the ith food,
        cuisines[i] is the type of cuisine of the ith food, and
        ratings[i] is the initial rating of the ith food.
    void changeRating(String food, int newRating) Changes the rating of the food item with the name food.
    String highestRated(String cuisine) Returns the name of the food item that has the highest rating for the given type of cuisine. If there is a tie, return the item with the lexicographically smaller name.

Note that a string x is lexicographically smaller than string y if x comes before y in dictionary order, that is, either x is a prefix of y, or if i is the first position such that x[i] != y[i], then x[i] comes before y[i] in alphabetic order.

 

Example 1:

Input
["FoodRatings", "highestRated", "highestRated", "changeRating", "highestRated", "changeRating", "highestRated"]
[[["kimchi", "miso", "sushi", "moussaka", "ramen", "bulgogi"], ["korean", "japanese", "japanese", "greek", "japanese", "korean"], [9, 12, 8, 15, 14, 7]], ["korean"], ["japanese"], ["sushi", 16], ["japanese"], ["ramen", 16], ["japanese"]]
Output
[null, "kimchi", "ramen", null, "sushi", null, "ramen"]

Explanation
FoodRatings foodRatings = new FoodRatings(["kimchi", "miso", "sushi", "moussaka", "ramen", "bulgogi"], ["korean", "japanese", "japanese", "greek", "japanese", "korean"], [9, 12, 8, 15, 14, 7]);
foodRatings.highestRated("korean"); // return "kimchi"
                                    // "kimchi" is the highest rated korean food with a rating of 9.
foodRatings.highestRated("japanese"); // return "ramen"
                                      // "ramen" is the highest rated japanese food with a rating of 14.
foodRatings.changeRating("sushi", 16); // "sushi" now has a rating of 16.
foodRatings.highestRated("japanese"); // return "sushi"
                                      // "sushi" is the highest rated japanese food with a rating of 16.
foodRatings.changeRating("ramen", 16); // "ramen" now has a rating of 16.
foodRatings.highestRated("japanese"); // return "ramen"
                                      // Both "sushi" and "ramen" have a rating of 16.
                                      // However, "ramen" is lexicographically smaller than "sushi".

 

Constraints:

    1 <= n <= 2 * 104
    n == foods.length == cuisines.length == ratings.length
    1 <= foods[i].length, cuisines[i].length <= 10
    foods[i], cuisines[i] consist of lowercase English letters.
    1 <= ratings[i] <= 108
    All the strings in foods are distinct.
    food will be the name of a food item in the system across all calls to changeRating.
    cuisine will be a type of cuisine of at least one food item in the system across all calls to highestRated.
    At most 2 * 104 calls in total will be made to changeRating and highestRated.

"""

import heapq
from collections import defaultdict
from typing import List

class FoodRatings:
    """
    Implements a system to rate foods and find the highest-rated food per cuisine.

    This class uses two main data structures for efficiency:
    1. A dictionary `food_info` for O(1) lookup of a food's rating and cuisine.
    2. A dictionary `cuisine_foods` mapping each cuisine to a max-heap. The heap
       stores tuples of (-rating, food_name) to quickly find the highest-rated
       food in O(log N) time, handling ties lexicographically.
    """

    def __init__(self, foods: List[str], cuisines: List[str], ratings: List[int]):
        """
        Initializes the food rating system.
        Time Complexity: O(n * log(k)), where n is the number of foods and k is
        the maximum number of foods in a single cuisine.
        """
        # {food: [rating, cuisine]} for quick O(1) lookups and updates.
        # The rating is in a list to be mutable.
        self.food_info = {}
        
        # {cuisine: min_heap_of_(-rating, food)} to get highest rating quickly.
        # We use a min-heap with negative ratings to simulate a max-heap.
        self.cuisine_foods = defaultdict(list)

        for i in range(len(foods)):
            food = foods[i]
            cuisine = cuisines[i]
            rating = ratings[i]
            
            self.food_info[food] = [rating, cuisine]
            # Push (-rating, food) to handle tie-breaking correctly.
            # Python's heap will sort by the first element, then the second.
            heapq.heappush(self.cuisine_foods[cuisine], (-rating, food))

    def changeRating(self, food: str, newRating: int) -> None:
        """
        Changes the rating of a food item and updates the corresponding cuisine heap.
        This uses a "lazy update" by adding the new rating without removing the old one.
        Time Complexity: O(log(k)), where k is the number of foods in that cuisine.
        """
        # Update the rating in the main info dictionary
        self.food_info[food][0] = newRating
        
        # Get the cuisine for the food
        cuisine = self.food_info[food][1]
        
        # Push the new rating onto the heap for that cuisine.
        # The old rating entry remains but will be ignored by highestRated.
        heapq.heappush(self.cuisine_foods[cuisine], (-newRating, food))

    def highestRated(self, cuisine: str) -> str:
        """
        Returns the name of the food with the highest rating for a given cuisine.
        It cleans up any "stale" ratings at the top of the heap before returning.
        Time Complexity: Amortized O(log(k)), where k is the number of foods in the cuisine.
        In the worst case, it could be O(m * log(k)) where m is the number of rating changes
        for the top food, but this averages out over all calls.
        """
        heap = self.cuisine_foods[cuisine]
        
        # Peek at the top element of the heap.
        top_food_candidate = heap[0]
        
        # The current rating stored for this food in our info dictionary.
        current_rating_for_candidate = self.food_info[top_food_candidate[1]][0]
        
        # Loop to discard stale entries from the top of the heap.
        # A stale entry is one where the rating in the heap does not match
        # the current rating of the food in food_info.
        # -top_food_candidate[0] is the positive rating from the heap.
        while -top_food_candidate[0] != current_rating_for_candidate:
            heapq.heappop(heap)
            top_food_candidate = heap[0]
            current_rating_for_candidate = self.food_info[top_food_candidate[1]][0]
            
        # The top of the heap is now a valid, non-stale entry.
        return top_food_candidate[1]


# Your FoodRatings object will be instantiated and called as such:
# obj = FoodRatings(foods, cuisines, ratings)
# obj.changeRating(food,newRating)
# param_2 = obj.highestRated(cuisine)        