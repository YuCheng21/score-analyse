import os
import pandas as pd

from ..config.base import csv_path as csv_file


class PassedCourse:
    def __init__(self, csv_path=csv_file):
        self.passed_filename = csv_path

    def raw_data_filter(self, input_xlsx):
        table = pd.DataFrame(pd.read_excel(input_xlsx, header=None, usecols=[0, 6, 14, 16, 17, 18, 19]))
        table.columns = ['狀態', '學號', '成績', '學期', '修別', '學分', '課程名稱']
        table = table[table['狀態'].isin(['通過'])]

        if os.path.exists(self.passed_filename):
            tb_pass = pd.DataFrame(pd.read_csv(self.passed_filename, encoding='utf-8-sig'))
            tb_pass = pd.concat([tb_pass, table], axis=0, ignore_index=True)
            tb_pass['成績'] = tb_pass['成績'].astype(int)
            tb_pass.drop_duplicates(inplace=True)
            tb_pass.to_csv(self.passed_filename, encoding='utf-8-sig', index=False)
        else:
            table.to_csv(self.passed_filename, encoding='utf-8-sig', index=False)

    def get_target_table(self, student_id):
        if not os.path.exists(self.passed_filename):
            return []
        table = pd.read_csv(self.passed_filename, encoding='utf-8-sig')
        # 將學號的型態從 numpy.int64 轉為 str，用來跟 stu_id 判斷
        table['學號'] = table['學號'].astype(str)
        # 篩選【學號】欄位中包含 stu_id 值的內容
        tb_pass = table[table['學號'].isin([student_id])]
        # 增加一個 col 欄位為【科目註記】，並且內容為【抵免】
        tb_pass = tb_pass.assign(科目註記='抵免課程')
        # col 按順序排序
        tb_pass = tb_pass[['課程名稱', '科目註記', '修別', '學期', '學分', '成績']]
        # 將 DataFrame 轉為 list
        tb_pass = tb_pass.values.tolist()
        return tb_pass

    def get_all_table(self):
        if not os.path.exists(self.passed_filename):
            return []
        tb_pass = pd.read_csv(self.passed_filename, encoding='utf-8-sig')
        # col 按順序排序
        tb_pass = tb_pass[['狀態', '學號', '成績', '學期', '修別', '學分', '課程名稱']]
        # 將 DataFrame 轉為 list
        tb_pass = tb_pass.values.tolist()
        return tb_pass

    def delete_row(self, index):
        if os.path.exists(self.passed_filename):
            tb_pass = pd.DataFrame(pd.read_csv(self.passed_filename, encoding='utf-8-sig'))
            tb_pass.drop([tb_pass.index[int(index) - 1]], inplace=True)
            tb_pass.reset_index(drop=True)
            tb_pass.to_csv(self.passed_filename, encoding='utf-8-sig', index=False)