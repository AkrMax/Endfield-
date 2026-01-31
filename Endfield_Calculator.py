import sys

def Input_Inspect(target, nullable):
	"""输入检查函数"""
	# 首先检查target是否为None
	if target is None and nullable == 1:
		print("输入错误，不能为空")
		return False
	# 然后检查是否为负数
	elif target < 0:
		print("输入错误，不能为负数")
		return False
	# 最后检查是否为零（当nullable=0时允许为零）
	elif target == 0 and nullable == 1:
		print("输入错误，不能为零")
		return False
	return True

def Speed_Cal(speed, level, demand_speed):
	"""分流器速度匹配函数"""
	# 初始化
	tc_list = []
	re_list = []
	li = 0
	demand_speed = round(demand_speed, 5) * 10000 # 提升数位
	# 计算分流器网络的运力
	for lv in range(level):
		speed = speed / 3
		tc_list.append(int(round(speed, 5) * 10000))  # 限制精度

	# 计算速度匹配
	while True:
		if demand_speed == 0:
			break
		if li == level:
			break
		if tc_list[li] <= demand_speed:
			demand_speed = demand_speed - tc_list[li]
			re_list.append(li)
		elif tc_list[li] > demand_speed:
			li = li + 1

	# 检查精度是否不足
	if not re_list:
		print("计算精度不足")
		return
	#输出结果
	print(f"2.每级分流器的运力(单位为每分钟){list(map(lambda x: x / 10000, tc_list))}")
	print(f"3.热能池需要的分流器出口运输的等级{list(map(lambda x: x + 1, re_list))}")
	print(f"4.剩余电力缺口{round((demand_speed / 10000), 4)}")

def main():
	"""主函数"""
	try:
		# 获取需要的发电量
		demand_input = input("请输入需要的发电量(按Enter继续)：")
		if demand_input.strip() == "":
			print("输入错误，不能为空")
			return
		Demand = int(demand_input)
		if not Input_Inspect(Demand, 1):
			return

		# 获取现在的发电量
		now_power_input = input("请输入现在的发电量(按Enter继续)：")
		if now_power_input.strip() == "":
			print("输入错误，不能为空")
			return
		Now_Power = int(now_power_input)
		if not Input_Inspect(Now_Power, 1):
			return

		# 获取电池发电量
		battery_input = input("请输入使用的电池发电量(按Enter继续)：")
		if battery_input.strip() == "":
			print("输入错误，不能为空")
			return
		Battery = int(battery_input)
		if not Input_Inspect(Battery, 1):
			return

		# 获取计算精度
		level_input = input("请输入计算的精度(最大10)：")
		if level_input.strip() == "":
			print("输入错误，不能为空")
			return
		Level = int(level_input)
		if not Input_Inspect(Level, 1):
			return

		if Level > 10:
			Level = 10
		elif Level < 5:
			Level = 5

		# 获取传送带速度
		speed_input = input("请输入传送带的速度(默认30/每分钟)：")
		if speed_input.strip() == "":
			Speed = 30
		else:
			Speed = int(speed_input)
			if not Input_Inspect(Speed, 0):
				return

		#检查溢出的电量
		if (Demand - Now_Power) >= Battery:
			Full_Speed = (Demand - Now_Power) / 1600
			Full_Speed = int(Full_Speed)
			print(f"\n需要{Full_Speed}个满功率的热能池")
			Demand = Demand - (Full_Speed * 1600)
		# 检查需求的电量
		if (Demand - Now_Power)>0:
			#开始计算结果
			if (Demand - Now_Power) < Battery:
				Gap = Demand - Now_Power
				Demand_Speed = 60*(1/(40/(Gap / Battery)))
				print("\n------------------以下为计算结果----------------------")
				print(f"1.每分钟需要{round(Demand_Speed, 8)}个电池")
				Speed_Cal(Speed, Level, Demand_Speed)
		else:
			print("电力需求已满")
	except ValueError as e:
		print(f"输入错误：{e}")
		print("请确保输入的是有效数字")
	except Exception as e:
		print(f"程序发生未知错误：{e}")

if __name__ == "__main__":
	main()
	# 保持控制台打开
	input("\n按Enter键退出程序...")