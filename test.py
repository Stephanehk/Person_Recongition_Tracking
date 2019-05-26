import numpy as np

# xs = {"target1":1,"unkown1":2, "target2":3, "unkown2":3}
# ys = {"target1":1,"unkown1":2, "target2":3, "unkown2":3}
#
# def split_dict (dict1,target_key):
#     target_vals = {}
#     non_target_vals = {}
#     for key,value in dict1.items():
#         if target_key in key:
#             target_vals[key] = value
#         else:
#             non_target_vals[key] = value
#     return target_vals, non_target_vals
#
# def calc_distance (targetxs,targetys, otherxs, otherys):
#     total_dist = 0
#     for i in range (len(targetxs)):
#         tkey,tx = list(targetxs.items())[i]
#         tkey,ty = list(targetys.items())[i]
#         okey,ox = list(otherxs.items())[i]
#         okey,oy = list(otherys.items())[i]
#         distance = np.sqrt(np.power(ox-tx,2) + np.power(oy-ty,2))
#         total_dist+=distance
#     return total_dist
#
# target_valsx, non_target_valsx = split_dict (xs,"target")
# target_valsy, non_target_valsy = split_dict (ys,"target")
#
# calc_distance (target_valsx,target_valsy, non_target_valsx, non_target_valsy)
# print (np.mean([8992, 70445, 70013, 8177, 69049, 8266, 7834, 68690, 7345, 65385, 7066, 67009, 452, 73562, 98309, 925, 853,
# 73457, 765, 94961, 985, 73445, 1040, 96850, 95626, 1009, 1314, 72586, 90050, 1469, 1993, 88289, 2410, 86788, 71730, 1314, 2610, 85892,
# 71117, 1069, 71012, 1037, 65245, 1402, 3625, 31501, 3169, 30685, 3474, 30610, 79300, 202516, 243581, 2405, 32650, 2260, 34285, 2371,
# 70, 86485, 146, 45344, 2088, 82244, 2477, 80765, 2593, 80884, 260, 85874, 81509, 2900, 520, 84221, 77828, 3060, 657, 85520, 76744, 30,
# 37, 1157, 86210, 6445, 73076, 3924, 2000, 86164, 3688, 78880, 3764, 79757, 3610, 81040, 72826, 78548, 3177, 78548, 3145, 3125, 79141,
# 80081, 4610, 37060, 191701, 74581, 5717, 3085, 81090]))
