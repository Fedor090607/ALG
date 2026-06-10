def find_first(nums, target):
    left, right = 0, len(nums) - 1
    result = -1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            result = mid
            right = mid - 1
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return result

def find_last(nums, target):
    left, right = 0, len(nums) - 1
    result = -1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            result = mid
            left = mid + 1
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return result

def main():
    nums = [2, 5, 5, 5, 6, 6, 8, 9, 9, 9]
    target = 4


    first = find_first(nums, target)
    
    if first == -1:
        print("Элемент не найден в массиве")
    else:
        last = find_last(nums, target)
        print(f"Первое вхождение элемента {target} находится на индексе {first}")
        print(f"Последнее вхождение элемента {target} находится на индексе {last}")

if __name__ == '__main__':
    main()