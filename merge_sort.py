def merge_sort(nums: list [int]) -> None:
    if len(nums) > 1:
        num1 = nums[0:len(nums)//2]
        num2 = nums[len(nums)//2:len(nums)]

        merge_sort(num1)
        merge_sort(num2)
        
        new_list = nums.copy()
        merge(new_list, num1, num2)

        for i in range(len(new_list)):
            nums[i] = new_list[i]


def merge(merged_list: list [int], list1: list [int], list2: list [int]) -> None:
    i = 0
    j = 0

    while i < len(list1) and j < len(list2):
        if (list1[i] <= list2[j]):
            merged_list[i + j] = list1[i]
            i += 1
        else:
            merged_list[i + j] = list2[j]
            j += 1

    while i < len(list1):
        merged_list[i + j] = list1[i]
        i += 1

    while j < len(list2):
        merged_list[i + j] = list2[j]
        j += 1
