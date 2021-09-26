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


class Cert(MethodView):
    """
    證書相關
    """
    @login_required
    def get(self, certificate_number):
        if certificate_number is None:
            title = '查看證書紀錄'
            certificate_record = Certificate().get_record()
            return render_template('./root/certificate-table.html', **locals())
        else:
            try:
                Certificate().delete_certificate(certificate_number)
            except:
                flash('刪除失敗', category='error')
            else:
                flash('刪除成功', category='success-toast')
            return redirect(url_for('root.certificate'))

    @login_required
    def post(self):
        # Get form
        try:
            multiple_cert_input = request.files.getlist("multipleCertInput")
            # "serial_number" is deprecated.
            serial_number = request.values.to_dict()['serialNumber']
            if '' == multiple_cert_input[0].filename:
                raise Exception('01', 'multiple_cert_input can not be empty')
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
        score_array = TranscriptModel().multiple_extract(multiple_cert_input)
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


certificate_view = Cert.as_view('certificate')
app.add_url_rule('/certificate', view_func=certificate_view, methods=['POST'])
app.add_url_rule('/certificate', defaults={'certificate_number': None}, view_func=certificate_view, methods=['GET'])
app.add_url_rule('/certificate/<certificate_number>', view_func=certificate_view, methods=['GET'])


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
