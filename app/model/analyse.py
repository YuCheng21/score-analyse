"""
資料分析功能。
"""

import pandas as pd

from .passed_course import PassedCourse


def skill_tree_label():
    course_rules = [
        [9, 12],
        [13, 12],
        [9, 12],
        [12, 9]
    ]
    course_type = [
        '核心課程',
        '應用課程'
    ]
    cls_dict = {
        '智慧電網暨電能學程': [
            [course_type[0], '電機機械', 3, course_rules[0][0]],
            [course_type[0], '電力系統', 3, course_rules[0][0]],
            [course_type[0], '電力電子學', 3, course_rules[0][0]],
            [course_type[1], '綠能科技', 3, course_rules[0][1]],
            [course_type[1], '圖形監控設計', 3, course_rules[0][1]],
            [course_type[1], '工業配電', 3, course_rules[0][1]],
            [course_type[1], '電力系統分析', 3, course_rules[0][1]],
            [course_type[1], '電力潮流分析', 3, course_rules[0][1]],
            [course_type[1], '計算機輔助電路分析', 3, course_rules[0][1]],
            [course_type[1], '積體電路應用', 3, course_rules[0][1]],
            [course_type[1], '數位信號處理', 3, course_rules[0][1]],
            [course_type[1], '工程電路模擬與設計', 3, course_rules[0][1]],
            [course_type[1], '綠色電能轉換', 3, course_rules[0][1]],
            [course_type[1], '智慧電網暨實習', 3, course_rules[0][1]],
            [course_type[1], '固態轉換器暨實習', 3, course_rules[0][1]],
            [course_type[1], '電力電子分析暨實習', 3, course_rules[0][1]],
            [course_type[1], '積體電路應用暨實習', 3, course_rules[0][1]],
            [course_type[1], 'MATLAB工程實務應用暨實習', 3, course_rules[0][1]]
        ],
        '電動車暨電能學程': [
            [course_type[0], '電機機械', 3, course_rules[1][0]],
            [course_type[0], '電力電子學', 3, course_rules[1][0]],
            [course_type[0], '微處理機', 3, course_rules[1][0]],
            [course_type[0], '微處理機實習', 1, course_rules[1][0]],
            [course_type[0], '自動控制', 3, course_rules[1][1]],
            [course_type[1], '電動車馬達驅動分析暨實習', 3, course_rules[1][1]],
            [course_type[1], '電力電子分析暨實習', 3, course_rules[1][1]],
            [course_type[1], '電動車馬達固態驅動', 3, course_rules[1][1]],
            [course_type[1], '電動車控制', 3, course_rules[1][1]],
            [course_type[1], '電動車能量管理與控制', 3, course_rules[1][1]],
            [course_type[1], '電機應用', 3, course_rules[1][1]],
            [course_type[1], 'MATLAB工程實務應用暨實習', 3, course_rules[1][1]],
            [course_type[1], '計算機輔助電路分析暨實習', 3, course_rules[1][1]],
            [course_type[1], '感測器佈建與應用實務', 3, course_rules[1][1]],
            [course_type[1], '積體電路應用', 3, course_rules[1][1]],
            [course_type[1], '工程電路模擬與設計', 3, course_rules[1][1]],
            [course_type[1], '積體電路應用暨實習', 3, course_rules[1][1]]
        ],
        '智慧機器人學程': [
            [course_type[0], '微處理機', 3, course_rules[2][0]],
            [course_type[0], '自動控制', 3, course_rules[2][0]],
            [course_type[0], '智慧型系統導論', 3, course_rules[2][0]],
            [course_type[0], '機器人學', 3, course_rules[2][0]],
            [course_type[0], '影像處理暨實習', 3, course_rules[2][0]],
            [course_type[0], '邏輯設計暨實習', 3, course_rules[2][0]],
            [course_type[0], '線性代數', 3, course_rules[2][0]],
            [course_type[1], '機器學習', 3, course_rules[2][1]],
            [course_type[1], '人工智慧', 3, course_rules[2][1]],
            [course_type[1], '資料結構', 3, course_rules[2][1]],
            [course_type[1], '最佳化原理', 3, course_rules[2][1]],
            [course_type[1], '圖形監控設計', 3, course_rules[2][1]],
            [course_type[1], '順序控制暨實習', 3, course_rules[2][1]],
            [course_type[1], '微處理機應用', 3, course_rules[2][1]],
            [course_type[1], '信號與系統', 3, course_rules[2][1]],
            [course_type[1], '數位控制', 3, course_rules[2][1]],
            [course_type[1], '電腦視覺暨實習', 3, course_rules[2][1]],
            [course_type[1], '物件導向程式設計', 3, course_rules[2][1]],
            [course_type[1], '嵌入式系統應用程式開發', 3, course_rules[2][1]],
            [course_type[1], '馬達固態驅動暨實習', 3, course_rules[2][1]],
            [course_type[1], '機器人控制暨實習', 3, course_rules[2][1]]
        ],
        '人工智慧與雲端計算學程': [
            [course_type[0], '人工智慧', 3, course_rules[3][0]],
            [course_type[0], '雲端計算概論', 3, course_rules[3][0]],
            [course_type[0], '機器學習', 3, course_rules[3][0]],
            [course_type[0], '計算機網路', 3, course_rules[3][0]],
            [course_type[0], '資料庫系統', 3, course_rules[3][0]],
            [course_type[0], '工程數學(二)', 3, course_rules[3][0]],
            [course_type[0], 'Python程式設計', 3, course_rules[3][0]],
            [course_type[1], 'Linux系統與程式設計', 3, course_rules[3][1]],
            [course_type[1], '物聯網應用', 3, course_rules[3][1]],
            [course_type[1], '嵌入式系統應用程式開發', 3, course_rules[3][1]],
            [course_type[1], '感測網路佈建與應用實務', 3, course_rules[3][1]],
            [course_type[1], '無線網路', 3, course_rules[3][1]],
            [course_type[1], '作業系統', 3, course_rules[3][1]],
            [course_type[1], '演算法', 3, course_rules[3][1]],
            [course_type[1], '影像處理', 3, course_rules[3][1]],
            [course_type[1], '電腦視覺暨實習', 3, course_rules[3][1]],
            [course_type[1], '工程機率與統計', 3, course_rules[3][1]],
            [course_type[1], '影像處理微學分-深度學習實作模組', 1, course_rules[3][1]],
            [course_type[1], '影像處理微學分-深度學習實作模組', 1, course_rules[3][1]],
            [course_type[1], '嵌入式系統與AI微學分-深度學習實作模組', 1, course_rules[3][1]],
            [course_type[1], '資料結構', 3, course_rules[3][1]]
        ],
    }

    return cls_dict


class AnalyseModel:
    def __init__(self):
        self.cls_dict = skill_tree_label()

    def progress_calc(self, score_list):
        cls_dfs = {
            '智慧電網暨電能學程': pd.DataFrame(self.cls_dict['智慧電網暨電能學程'], columns=['課程類別', '課程名稱', '學分數', '課程選修規定']),
            '電動車暨電能學程': pd.DataFrame(self.cls_dict['電動車暨電能學程'], columns=['課程類別', '課程名稱', '學分數', '課程選修規定']),
            '智慧機器人學程': pd.DataFrame(self.cls_dict['智慧機器人學程'], columns=['課程類別', '課程名稱', '學分數', '課程選修規定']),
            '人工智慧與雲端計算學程': pd.DataFrame(self.cls_dict['人工智慧與雲端計算學程'], columns=['課程類別', '課程名稱', '學分數', '課程選修規定']),
        }
        score_dfs = pd.DataFrame(score_list, columns=['科目名稱', '科目註記', '必選修', '修讀學期', '學分', '成績'])

        radar_list = []
        pass_dict = {}
        for key, value in enumerate(cls_dfs):
            course_cnt = 0
            temp_dict = {'核心課程': [], '應用課程': [], '核心課程通過學分': [], '應用課程通過學分': []}
            for course in cls_dfs[value]['課程名稱'].values.tolist():
                if course in score_dfs['科目名稱'].values.tolist():
                    course_filter = cls_dfs[value]['課程名稱'].isin([course])
                    course_type = cls_dfs[value][course_filter]['課程類別'].values.tolist()[0]
                    course_score = cls_dfs[value][course_filter]['學分數'].values.tolist()[0]

                    temp_dict[course_type].append(course)
                    temp_dict[f'{course_type}通過學分'].append(course_score)

                    course_cnt += course_score

            pass_dict[value] = temp_dict
            rule = cls_dfs[value][cls_dfs[value]['課程類別'].isin(['核心課程'])]['課程選修規定'].values.tolist()[0] + \
                   cls_dfs[value][cls_dfs[value]['課程類別'].isin(['應用課程'])]['課程選修規定'].values.tolist()[0]
            percent = round(course_cnt * 100 / rule)
            if percent > 100:
                percent = 100
            radar_list.append([value, course_cnt, rule, percent])

        # radar_dfs = pd.DataFrame(radar_list, columns=['學程', '已完成學分數', '最低通過學分數', '進度百分比'])
        return [pass_dict, radar_list]

    def multiple_student(self, student_array):
        passed_array = []
        for key, value in enumerate(student_array):
            student_id, student_name, score_list = value

            buffer = PassedCourse().get_target_table(student_id)
            score_list += list(i for i in buffer)

            _, radar_array = self.progress_calc(score_list)
            passed_type = list(i[0] for i in radar_array if i[3] >= 100)
            passed_array.append([student_id, student_name, passed_type])
        return passed_array
