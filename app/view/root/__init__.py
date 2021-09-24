from flask import Blueprint, render_template, request, flash, redirect, url_for, session, abort, current_app
from flask.views import MethodView

from ...model.transcript import TranscriptModel
from ...model.passed_course import PassedCourse
from ...model.analyse import AnalyseModel, skill_tree_label

from ...model.jinja import col_len, is_pass

app = Blueprint('root', __name__)


@app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
    title = '首頁'
    if request.method == 'GET':
        return render_template('./root/index.html', **locals())
    elif request.method == 'POST':
        form_data = request.values.to_dict()
        abort(404)


class Result(MethodView):
    def get(self):
        title = '分析結果'
        # custom template function
        current_app.jinja_env.globals['is_pass'] = is_pass
        current_app.jinja_env.globals['col_len'] = col_len
        # get results session
        student_id = session.get('student_id')
        student_name = session.get('student_name')
        score_list = session.get('score_list')
        skill_tree = session.get('skill_tree')
        passed_skill_tree = session.get('passed_skill_tree')
        radar_array = session.get('radar_array')
        passed_type = session.get('passed_type')

        return render_template('./root/result.html', **locals())

    def post(self):
        # Get PDF file
        singleCertInput = request.files['singleCertInput']
        try:
            # Extract the PDF into a dictionary from the keys student_id, student_name and score_list
            pdf_info = TranscriptModel().extract(singleCertInput)
        except:
            # check file is right or not
            flash('檔案內容錯誤！請確認上傳校務系統下載的成績單檔案。', category='error')
            return redirect(url_for('root.index'))
        # processing and analyse pdf
        student_id, student_name, score_list = pdf_info
        buffer = PassedCourse().get_target_table(student_id)
        score_list += list(i for i in buffer)
        del buffer

        skill_tree = skill_tree_label()
        result_info = AnalyseModel().progress_calc(score_list)
        passed_skill_tree, radar_array = result_info
        passed_type = list(i[0] for i in radar_array if i[3] >= 100)
        # save results in session
        session['student_id'] = student_id
        session['student_name'] = student_name
        session['score_list'] = score_list
        session['skill_tree'] = skill_tree
        session['passed_skill_tree'] = passed_skill_tree
        session['radar_array'] = radar_array
        session['passed_type'] = passed_type

        return redirect(url_for('root.result'))


result_view = Result.as_view('result')
app.add_url_rule('/result', view_func=result_view)


from . import user
from . import manager
