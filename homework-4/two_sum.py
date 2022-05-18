# сложность O(N^2)

for i in range(len(nums)):
    for j in range(i + 1, len(nums)):
        if nums[i] + nums[j] == target:
            return i, j

# сложность O(N ln N)

numbers = [(i, nums[i]) for i in range(len(nums))]
numbers = sorted(numbers, key=lambda x: x[1])
for i in range(len(nums)):
    n = target - numbers[i][1]
    left = i + 1
    right = len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if n == numbers[mid][1]:
            return numbers[i][0], numbers[mid][0]
        elif n < numbers[mid][1]:
            right = mid - 1
        elif n > numbers[mid][1]:
            left = mid + 1

# сложность O(N)

d = {}
for i in range(len(nums)):
    n = target - nums[i]
    if n in d:
        return i, d.get(n)
    else:
        d[nums[i]] = i