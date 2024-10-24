# Two Sum Explanation

## Approach

To solve the Two Sum problem efficiently, we can utilize a hash map (dictionary) to keep track of the numbers we've seen so far and their corresponding indices. This allows us to find the complement of the current number in constant time.

### Step-by-Step Reasoning

1. **Initialize an empty dictionary** called `num_to_index`. This will map each number to its index in the `nums` array.

2. **Iterate through the list** using a loop. For each number `num` at index `i`:
   - **Calculate the complement**: `complement = target - num`.
   - **Check if the complement exists** in the `num_to_index` dictionary:
     - If it does, we've found the two numbers that add up to the target. Return their indices.
     - If it doesn't, add the current number and its index to the dictionary for future reference.

3. **If no solution is found** after iterating through the list, raise an error or handle it as per the problem's constraints.

## Time and Space Complexity

- **Time Complexity:** O(n), where n is the number of elements in `nums`. We traverse the list only once.
- **Space Complexity:** O(n), as we store up to n elements in the dictionary.

## Example Walkthrough

Let's walk through the example:


- **First iteration (index=0, num=2):**
  - Complement = 9 - 2 = 7
  - 7 is not in `num_to_index`.
  - Add 2 to `num_to_index`: `{2: 0}`

- **Second iteration (index=1, num=7):**
  - Complement = 9 - 7 = 2
  - 2 is in `num_to_index` (index=0).
  - Return `[0, 1]` as the solution.

## Python Implementation

```python
def two_sum(nums, target):
    num_to_index = {}  # Dictionary to store number and its index

    for index, num in enumerate(nums):
        complement = target - num
        if complement in num_to_index:
            return [num_to_index[complement], index]
        num_to_index[num] = index

    raise ValueError("No two sum solution")