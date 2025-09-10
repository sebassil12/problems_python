"""
On a social network consisting of m users and some friendships between users, two users can communicate with each other if they know a common language.

You are given an integer n, an array languages, and an array friendships where:

    There are n languages numbered 1 through n,
    languages[i] is the set of languages the ith user knows, and
    friendships[i] = [ui, vi] denotes a friendship between the users ui and vi.

You can choose one language and teach it to some users so that all friends can communicate with each other. Return the minimum number of users you need to teach.
Note that friendships are not transitive, meaning if x is a friend of y and y is a friend of z, this doesn't guarantee that x is a friend of z.

Example 1:

Input: n = 2, languages = [[1],[2],[1,2]], friendships = [[1,2],[1,3],[2,3]]
Output: 1
Explanation: You can either teach user 1 the second language or user 2 the first language.

Example 2:

Input: n = 3, languages = [[2],[1,3],[1,2],[3]], friendships = [[1,4],[1,2],[3,4],[2,3]]
Output: 2
Explanation: Teach the third language to users 1 and 3, yielding two users to teach.
"""

from typing import List

class Solution:
    def minimumTeachings(self, n: int, languages: List[List[int]], friendships: List[List[int]]) -> int:
        # Added a setter for faster lookup and to avoid duplicates
        lang_sets = [set(l) for l in languages]
        
        problem_friendships = []
        for u, v in friendships:
            # Adapt to index 0-based for search int he list of languages according the user
            u_idx, v_idx = u - 1, v - 1
            # If the user u and user v don't share any language, it's a problem friendship
            if not (lang_sets[u_idx] & lang_sets[v_idx]):
                problem_friendships.append((u_idx, v_idx))

        if not problem_friendships:
            return 0
        # the min try is to teach all the users a new language 
        min_teachings = len(languages)

        # A loop for each language n 
        for target_lang in range(1, n + 1):
            users_to_teach = set()
            for u_idx, v_idx in problem_friendships:
                # For this case we iterate all the languages and check if the user that have problems knows it
                if target_lang not in lang_sets[u_idx]:
                    users_to_teach.add(u_idx)
                if target_lang not in lang_sets[v_idx]:
                    users_to_teach.add(v_idx)
            
            min_teachings = min(min_teachings, len(users_to_teach))

        return min_teachings

Solution().minimumTeachings(3, [[2],[1,3],[1,2],[3]], [[1,4],[1,2],[3,4],[2,3]])