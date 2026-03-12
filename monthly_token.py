def solve_linear_combination(nums, M):
    # --- 第一步：寻找最接近 M 的最大和 S_max ---
    # dp[i] 表示和 i 是否可以实现
    dp = [False] * (M + 1)
    dp[0] = True
    
    # 为了后续回溯方便，我们排序数字
    nums = sorted(list(set(nums))) 
    
    for num in nums:
        for i in range(num, M + 1):
            if dp[i - num]:
                dp[i] = True
                
    # 找到最大可能的和 S_max
    s_max = 0
    for i in range(M, -1, -1):
        if dp[i]:
            s_max = i
            break
            
    print(f"目标值 M: {M}")
    print(f"能达到的最接近和 S_max: {s_max}")
    print("-" * 30)

    # --- 第二步：回溯寻找所有组合 ---
    results = []
    
    def backtrack(remaining, start_index, current_combination):
        if remaining == 0:
            results.append(list(current_combination))
            return
        
        for i in range(start_index, len(nums)):
            num = nums[i]
            if remaining >= num:
                current_combination.append(num)
                # 因为可以重复使用，所以 index 依然从 i 开始
                backtrack(remaining - num, i, current_combination)
                current_combination.pop() # 回溯

    backtrack(s_max, 0, [])

    # --- 第三步：格式化输出系数 ---
    if not results:
        print("没有找到符合条件的组合。")
        return

    print(f"共有 {len(results)} 种组合方式达到和 {s_max}：\n")
    for idx, combo in enumerate(results, 1):
        # 统计系数 (数字: 出现次数)
        coeffs = {num: combo.count(num) for num in nums}
        parts = [f"({count} * {num})" for num, count in coeffs.items() if count > 0]
        print(f"方案 {idx}: {' + '.join(parts)} = {s_max}")

# --- 测试 ---
my_nums = [180, 2800, 800, 3800, 1800, 6800, 3000]
my_target = 9081

solve_linear_combination(my_nums, my_target)