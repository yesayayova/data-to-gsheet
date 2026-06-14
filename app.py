from flask import Flask, render_template, request, redirect, url_for, flash
import os
import tempfile
from services import transform_og, transform_gs

app = Flask(__name__, template_folder='templates')
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'change-me-123')

ALLOWED_EXTENSIONS = {'xls'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    upload_type = request.form.get('upload_type')
    file = request.files.get('file')
    if upload_type not in {'og', 'gs'} or file is None or file.filename == '':
        flash('Pilih file .xls dan tipe upload yang valid.', 'error')
        return redirect(url_for('index'))

    if not allowed_file(file.filename):
        flash('Hanya file .xls yang didukung.', 'error')
        return redirect(url_for('index'))

    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix='.xls', delete=False) as tmp_file:
            file.save(tmp_file.name)
            temp_path = tmp_file.name

        if upload_type == 'og':
            df = transform_og(temp_path)
            label = 'OG AOI'
        else:
            df = transform_gs(temp_path)
            label = 'GS AOI'

        flash(f'{label} berhasil diunggah. {len(df)} baris ditambahkan.', 'success')
    except Exception as exc:
        flash(f'Proses upload gagal: {exc}', 'error')
    finally:
        if temp_path and os.path.exists(temp_path):
            try:
                os.unlink(temp_path)
            except OSError:
                pass

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
