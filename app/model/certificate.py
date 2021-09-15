"""
證書相關功能，例如產生證書。
"""

import os
import io
import zipfile
from datetime import datetime
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListItem, ListFlowable, Frame, Image

from ..config.base import project_path


class Certificate:
    def __init__(self):
        self.reportlab_path = os.path.join(project_path, "app", "model", "reportlab")

    def generate(self, student_id, student_name, passed_type, certificate_number, now):
        styles = getSampleStyleSheet()
        pdfmetrics.registerFont(TTFont('Ngaan', os.path.join(self.reportlab_path, "I.Ngaan.ttf")))
        pdfmetrics.registerFont(TTFont('edukai', os.path.join(self.reportlab_path, "edukai-4.0.ttf")))
        h1_fontsize = 32
        h1 = ParagraphStyle(
            'h1',
            fontName='Ngaan',
            parent=styles["Normal"],
            fontSize=h1_fontsize,
            leading=h1_fontsize * 2,
            alignment=TA_CENTER,
        )
        h2_fontsize = 40
        h2 = ParagraphStyle(
            'h2',
            fontName='Ngaan',
            parent=styles["Normal"],
            fontSize=h2_fontsize,
            leading=h2_fontsize * 1.5,
            alignment=TA_CENTER,
        )
        paragraph_fontsize = 20
        paragraph = ParagraphStyle(
            'paragraph',
            fontName='edukai',
            parent=styles["Normal"],
            fontSize=paragraph_fontsize,
            leading=paragraph_fontsize * 1.5,
            alignment=TA_LEFT,
        )
        mark_fontsize = 18
        mark = ParagraphStyle(
            'mark',
            fontName='edukai',
            parent=styles["Normal"],
            fontSize=mark_fontsize,
            leading=mark_fontsize * 1.5,
            alignment=TA_LEFT,
        )
        header_fontsize = 10
        header_font = ParagraphStyle(
            'header',
            fontName='edukai',
            parent=styles["Normal"],
            fontSize=header_fontsize,
            leading=header_fontsize * 1.5,
            alignment=TA_LEFT,
        )

        temp = io.BytesIO()
        a4_width = 21 * cm
        a4_height = 29.7 * cm
        indent_width = 2.54 * cm
        indent_height = 2.54 * cm
        pdf_template = SimpleDocTemplate(temp,
                                         pagesize=A4,
                                         title='certificate',
                                         author='國立高雄科技大學電機工程系',
                                         subject='學成證書',
                                         topMargin=8 * cm,
                                         bottomMargin=1 * cm)
        story = []
        story.append(Paragraph("國立高雄科技大學電機工程系", h1))
        story.append(Paragraph("學 程 證 書", h1))
        story.append(Paragraph(f'學生 {student_name}', paragraph))

        if len(passed_type) > 0:
            story.append(Paragraph(f'完成修課學程，綜合評分表現優異，特頒此證以玆證明。', paragraph))
            story.append(Paragraph(f'學程名稱：', paragraph))
            course_list = []
            course_test = ['智慧電網暨電能學程', '電動車暨電能學程', '智慧機器人學程', '人工智慧與雲端計算學程']
            for i in passed_type:
                course_list.append(ListItem(Paragraph(f'{i}', paragraph), leftIndent=32))

            story.append(
                ListFlowable(
                    course_list,
                    bulletType='bullet',
                    start='circle',
                    bulletFontSize=10,
                    bulletOffsetY=-8,
                    bulletDedent=26
                )
            )
        else:
            story.append(Paragraph(f'學期評分未達標準，尚未通過修課學程，待通過評分後再予以頒發證書。', paragraph))

        def water_mark(canvas, doc):

            badge_width = a4_width
            badge_height = a4_height
            badge = [
                Image(os.path.join(self.reportlab_path, "background.png"), width=badge_width - 0.45 * cm,
                      height=badge_height - 0.45 * cm)
            ]
            Frame(
                # 貼邊============
                # (0 - 0.25) * cm,
                # (0 - 0.25) * cm,
                # badge_width + 0.45 * cm,
                # badge_height + 0.45 * cm
                # 出血範圍=========
                0,
                0,
                badge_width,
                badge_height
            ).addFromList(badge, canvas)
            header = [
                Paragraph(f'電機證字第{certificate_number}號', header_font),
            ]
            Frame(
                14.5 * cm,
                25 * cm,
                a4_width - (indent_width * 2),
                1 * cm
            ).addFromList(header, canvas)

            footer = [
                Spacer(0.5 * cm, 0),
                Paragraph(f'系主任', mark),
                Spacer(0, 1.5 * cm),
                Paragraph(f'學號：{student_id}', mark),
                Paragraph(f'中華民國 {now.year - 1911} 年 {now.month} 月 {now.day} 日', mark, )
            ]
            Frame(
                indent_width,
                2.5 * cm,
                a4_width - (indent_width * 2),
                5 * cm
            ).addFromList(footer, canvas)

        pdf_template.build(story, onFirstPage=water_mark, onLaterPages=water_mark)

        certificate = temp.getvalue()
        temp.close()

        return certificate

    def generate_zip(self, passed_array, serial_number):
        temp_zip = io.BytesIO()
        temp_txt = io.StringIO()
        f_zip = zipfile.ZipFile(temp_zip, mode="a")
        for key, value in enumerate(passed_array):
            student_id, student_name, passed_type = value
            if len(passed_type) > 0:
                now = datetime.now()
                certificate_number = f'{now.year - 1911}{serial_number:04d}'

                certificate = self.generate(student_id, student_name, passed_type, certificate_number, now)
                serial_number += 1
                try:
                    f_zip.writestr(f'{student_id}.pdf', certificate)
                except Exception as e:
                    print("異常物件的型別是:%s" % type(e))
                    print("異常物件的內容是:%s" % e)
            temp_txt.write(f'{student_id},{student_name},{passed_type},\n')
        file_txt = temp_txt.getvalue()
        temp_txt.close()
        f_zip.writestr(f'Summary.txt', file_txt)
        f_zip.close()
        file_zip = temp_zip.getvalue()
        temp_zip.close()
        return file_zip
