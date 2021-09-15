"""
成績單相關功能，例如匯出 PDF。
"""

import pdfplumber
import re


class TranscriptModel:
    def __init__(self):
        self.ERROR = 'something wrong'

    #  移植自瑋軒專案。
    def extract(self, file):
        # 必選修、科目、年級、成績 註記列表
        mark_dict = {
            "compulsory_elective": {
                "必": "必修", "選": "選修", "暑": "暑修", "寒": "寒修"
            },
            "subject": {
                "\[§\]": "學分與成績不列入計算", "\*": "預研生先修課程", "\[@\]": "上修課程", "\[◇\]": "教育學程",
                "\[◆\]": "學程科目", "\[★\]": "預官選修", "\[⊕\]": "專業選修", "\[△\]": "通識科目",
                "\[▲\]": "抵修科目", "\[☆\]": "核心通識", "\[※\]": "輔系", "\[◎\]": "雙主修", "\[$\]": "全英語授課",
                "\[([0-9]{2}.|[1][0-9]{2}.)([12]{1})\]": "重修",
                "\[#([0-9]{2}.|[1][0-9]{2}.)([12]{1})\]": "抵充科目",
                "\[%([0-9]{2}.|[1][0-9]{2}.)([12]{1})\]": "畢業補考"
            },
            "grade": {
                "1": "一", "2": "二", "3": "三", "4": "四"
            },
            "score": {
                "抵": "抵免", "免": "免修", "減": "減修", "/": "選修學年課未修完", "P": "通過", "F": "未通過", "停": "停修"
            }
        }
        # 讀取PDF
        pdf = pdfplumber.open(file)
        # 科目名稱 正規表示式
        subject_pattern = re.compile("(.{2,32})(\*|\[.\])")
        # 記錄解析出來並格式化的成績資訊
        score_list = []

        correct_file = False
        # PDF解析為表格，逐列分析 (  以下暫不考慮延畢、復學情況 )
        for line in pdf.pages[0].extract_table():
            if '學      號：' in line:
                student_id = line[2]
                correct_file = True
            if not correct_file:
                raise Exception(self.ERROR)
            if '姓      名：' in line:
                student_name = line[2]
            # 當該列存在「必、選、暑、寒」字之一，便認為該列包含科目訊息
            if ("必" in line) or ("選" in line) or ("暑" in line) or ("寒" in line):
                # 每列基本上有28欄，其中4欄為None
                # 建立新列，擷取舊列中包含文字與空值的欄位，理論上為24個
                new_line = []
                for e in line:
                    if e:
                        new_line.append(e)
                    elif e is None:
                        pass
                    else:
                        new_line.append("x")
                # 一列中，每6欄為一個學年，因此每列分為4次來分析。6欄分別為:
                # [必選修, 科目名稱, 第一學期學分, 第一學期成績, 第二學期學分, 第二學期成績]
                for g in range(4):
                    # 當【必選修】欄位不為空值，代表選取欄位有成績資訊
                    if new_line[0 + 6 * g] != "x":
                        # 檢查【上學期學分】是否有值，判斷該科目的開課學期
                        semester_flag = new_line[2 + 6 * g] not in ["x", "-"]
                        # 記錄"科目名稱"與"科目註記"
                        # 檢查【科目名稱】格式，若有註記符號，需分離並取代為其符號的實際名稱
                        # Ex: 電信概論[⊕] => "電信概論", "專業選修"
                        if subject_pattern.match(new_line[1 + 6 * g]):
                            subject_name = subject_pattern.match(new_line[1 + 6 * g]).group(1)
                            subject_mark = ""
                            for pattern in mark_dict["subject"].keys():
                                if re.match(pattern, subject_pattern.match(new_line[1 + 6 * g]).group(2)):
                                    subject_mark = mark_dict["subject"][pattern]
                                    break
                        else:
                            subject_name = new_line[1 + 6 * g]
                            subject_mark = ""
                        # 記錄"必選修"、"年級-學期"、"學分"
                        subject_type = mark_dict['compulsory_elective'][new_line[0 + 6 * g]]
                        subject_semester = "{}{}".format(mark_dict['grade']["{}".format(g + 1)],
                                                         "上" if semester_flag else "下")
                        subject_unit = new_line[(2 if semester_flag else 4) + 6 * g]
                        # 記錄"成績"
                        # 若兩個學期均有成績，則選擇第二學期成績
                        if (new_line[3 + 6 * g] not in ["-"]) and (new_line[5 + 6 * g] not in ["-"]):
                            subject_grade = new_line[5 + 6 * g]
                        else:
                            subject_grade = new_line[(3 if semester_flag else 5) + 6 * g]
                        # 若成績為註記符號，則取代為其符號的實際名稱
                        subject_grade = mark_dict['score'][subject_grade] \
                            if subject_grade in mark_dict['score'].keys() \
                            else subject_grade
                        # 暫存成績資訊
                        score_list.append([
                            subject_name, subject_mark, subject_type,
                            subject_semester, subject_unit, subject_grade
                        ])

        pdf.close()

        # 按照學年排序並列印
        grade_asc_list = ["一上", "一下", "二上", "二下", "三上", "三下", "四上", "四下"]
        score_list = sorted(score_list, key=lambda row: grade_asc_list.index(row[3]))
        return [student_id, student_name, score_list]

    def multiple_extract(self, files):
        student_array = []
        for key, value in enumerate(files):
            try:
                student_info = self.extract(value)
            except:
                print(self.ERROR)
                continue

            student_array.append(student_info)
        return student_array
