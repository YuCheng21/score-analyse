from . import app
from flask import redirect, url_for, flash, request, session, render_template, make_response, abort
from flask.views import MethodView

from ...model.passed_course import PassedCourse
from ...model.certificate import Certificate
from ...model.transcript import TranscriptModel
from ...model.analyse import AnalyseModel


def login_required(func):
    def wrapper(*args, **kwargs):
        role = session.get('role')
        if role is None:
            return redirect(url_for('root.index'))

        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper


class MultipleCert(MethodView):
    """
    證書相關
    """
    def get(self):
        abort(404)

    @login_required
    def post(self):
        # Get form
        try:
            multipleCertInput = request.files.getlist("multipleCertInput")
            serial_number = request.values.to_dict()['serialNumber']
            if '' == multipleCertInput[0].filename:
                raise Exception('01', 'multipleCertInput can not be empty')
        except Exception as e:
            if e.args[0] == '01':
                return "Input file can not be empty"
            return "Server error"

        # Parse to integer
        try:
            serial_number = int(serial_number)
        except:
            serial_number = 1

        # Extract pdf
        score_array = TranscriptModel().multiple_extract(multipleCertInput)
        # Append transform course
        passed_array = AnalyseModel().multiple_student(score_array)

        # build a zip have all certificate and summary file
        try:
            file_zip = Certificate().generate_zip(passed_array, serial_number)
        except:
            print('build zip failed')

        # return response with a zip file
        response = make_response(file_zip)
        response.headers['Content-Disposition'] = "attachment; filename=folder.zip"
        response.mimetype = 'application/zip'
        return response


multiple_cert_view = MultipleCert.as_view('multiple_cert')
app.add_url_rule('/multiple-cert', view_func=multiple_cert_view)


class PassedTable(MethodView):
    """
    抵免相關
    """
    @login_required
    def get(self, index):
        if index is None:
            title = '查看抵免彙整表'
            passed_list = PassedCourse().get_all_table()
            return render_template('./root/passed-table.html', **locals())
        else:
            try:
                PassedCourse().delete_row(index)
            except:
                flash('刪除失敗', category='error')
            else:
                flash('刪除成功', category='success-toast')
            return redirect(url_for('root.passed'))

    @login_required
    def post(self):
        passed_table = request.files['passedTableExcel']
        try:
            PassedCourse().raw_data_filter(passed_table)
        except:
            flash('上傳失敗', category='error')
        else:
            flash('上傳成功', category='success')
        return redirect(url_for('root.index'))


passed_view = PassedTable.as_view('passed')
app.add_url_rule('/passed', view_func=passed_view, defaults={'index': None}, methods=['GET'])
app.add_url_rule('/passed', view_func=passed_view, methods=['POST'])
app.add_url_rule('/passed/<index>', view_func=passed_view, methods=['GET'])
