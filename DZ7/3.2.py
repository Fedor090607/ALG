def f(nums, target, find_first_flag):
    left, right = 0, len(nums) - 1
    result = -1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            result = mid
            if find_first_flag:
                right = mid - 1
            else:
                left = mid + 1
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return result

def main():
    nums = list(map(int, input().split()))
    target = int(input())

    first = f(nums, target, True)
    
    if first == -1:
        print("Элемент не найден в массиве")
    else:
        last = f(nums, target, False)
        print(f"Первое вхождение элемента {target} находится на индексе {first}")
        print(f"Последнее вхождение элемента {target} находится на индексе {last}")

if __name__ == '__main__':
    main()
