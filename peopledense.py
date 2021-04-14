import numpy as np


class DensityDetector():
    def __init__(self):
        self.group_num = 5
        self.depth_coeff = 1

    def convertVector(self, pos_list):
        # [top, left, bottom, right]
        num_vector = len(pos_list)
        if num_vector == 0:
            return False
        pos_list = np.array(pos_list)

        pos_vector = np.zeros((num_vector, 5))
        # x position
        pos_vector[:, 0] = (pos_list[:, 1] + pos_list[:, 3]) / 2
        # y position
        pos_vector[:, 1] = (pos_list[:, 0] + pos_list[:, 2]) / 2
        # width
        pos_vector[:, 2] = abs(pos_list[:, 3] - pos_list[:, 1])
        # height
        for i in range(num_vector):
            pos_vector[i, 3] = abs(pos_list[i, 2] - pos_list[i, 0])
            if pos_vector[i, 3] < pos_vector[i, 2]:
                pos_vector[i, 3] = 4 * pos_vector[i, 2]
            # area
            pos_vector[i, 4] = pos_vector[i, 2] * pos_vector[i, 3]
        return pos_vector


    def groupDepth(self, area_dict):
        main_list = []
        main_list_range = []
        # dict {area: area_range}
        area_range = [[a*0.5, a*2] for a in area_dict.values()]
        area_range = dict(zip(area_dict.keys(), area_range))
        for key in area_dict:
            need_flag = True
            if main_list == []:
                main_list.append([key])
                main_list_range.append(area_range[key])
            else:
                for i, range in enumerate(main_list_range):
                    if area_dict[key] > min(range) and area_dict[key] < max(range):
                        main_list[i].append(key)
                        main_list_range[i].append(area_range[key][0])
                        main_list_range[i].append(area_range[key][1])
                        need_flag = False
                    else:
                        continue
                if need_flag:
                    main_list.append([key])
                    main_list_range.append(area_range[key])
        return main_list


    def getGroup(self, x_dict, w_dict):
        main_list = []
        main_list_range = []
        dis_range = {}
        for key in x_dict:
            dis_range[key] = [x_dict[key]-w_dict[key], x_dict[key]+w_dict[key]]
        
            
        for key in x_dict:
            need_flag = True
            if main_list == []:
                main_list.append([key])
                main_list_range.append(dis_range[key])
            else:
                for i, range in enumerate(main_list_range):
                    if x_dict[key] > min(range) and x_dict[key] < max(range):
                        main_list[i].append(key)
                        main_list_range[i].append(dis_range[key][0])
                        main_list_range[i].append(dis_range[key][1])
                        need_flag = False
                    else:
                        continue
                if need_flag:
                    main_list.append([key])
                    main_list_range.append(dis_range[key])
        return main_list

  
    def checkDensity(self, pos_list):
        vector_num = len(pos_list)
        pos_vector = self.convertVector(pos_list)
        area_list = (pos_vector[:, 4]).tolist()
        area_dict = dict(zip([i for i in range(vector_num)], area_list))
        area_dict = {k: v for k, v in sorted(area_dict.items(), key=lambda item: item[1])}
        depth_list = self.groupDepth(area_dict)
        
        main_list = []
        for depth_block in depth_list:
            temp_x_list = [pos_vector[i, 0] for i in depth_block]
            temp_x_dict = dict(zip(depth_block, temp_x_list))
            temp_x_dict = {k: v for k, v in sorted(temp_x_dict.items(), key=lambda item: item[1])}
            temp_w_list = [pos_vector[i, 2] for i in depth_block]
            temp_w_dict = dict(zip(depth_block, temp_w_list))
            temp_block_list = self.getGroup(temp_x_dict, temp_w_dict)
            for block in temp_block_list:
                main_list.append(block)
        return main_list
            

if __name__ == "__main__":
    demo_list = np.array([[20, 70, 90, 90], [19, 71, 90, 90], [5, 10, 10, 13]])
    demo = DensityDetector()
    dense_list = demo.checkDensity(demo_list)