def two_sum(nums, target):
    """
    Finds two numbers in 'nums' that add up to 'target' and returns their indices.

    Args:
        nums (List[int]): List of integers.
        target (int): The target sum.

    Returns:
        List[int]: Indices of the two numbers that add up to target.

    Raises:
        ValueError: If no two numbers sum up to the target.
    """
    num_to_index = {}  # Dictionary to store number and its index

    for index, num in enumerate(nums):
        complement = target - num
        if complement in num_to_index:
            return [num_to_index[complement], index]
        num_to_index[num] = index

    raise ValueError("No two sum solution")
