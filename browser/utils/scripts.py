import cv2
import errno
import glob
import numpy as np
import os
import pandas as pd
import re
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QVBoxLayout, QFileDialog, QDialog
from .styles import *


def make_dir(path):
    try:
        os.mkdir(path)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
    pass


def load_image(path, label):
    max_h, max_w = 500, 700
    image = cv2.imread(path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    h, w, c = image.shape
    if (h>max_h) or (w>max_w):
        scale_ratio = max_h/h if h>=w else max_w/w
        image = cv2.resize(image, None, fx=scale_ratio, fy=scale_ratio, interpolation=cv2.INTER_LINEAR)
        h, w, _ = image.shape
    bytes_per_line = 3 * w
    rescaled = QImage(image.data, w, h, bytes_per_line, QImage.Format_RGB888)
    label.setPixmap(QPixmap.fromImage(rescaled))


def convert_to_int(value):
    try:
        return int(value)
    except ValueError:
        return None


def correct_patient_id(df):
    # Correct the patient_id format (F-PP-0000 or F-PP-S-0000)
    rgx = r'([A-Z]{1})(-+)?([A-Z]{2})(-+)?([A-Z]{0,1})(-+)?(\d{4})'
    df['patient_id'] = df.patient_id.str.replace(rgx, r'\1-\3-\5-\7', regex=True)
    df['patient_id'] = df.patient_id.str.replace(r'--+', '-', regex=True)

    # Extract only the valid format
    rgx = r'[A-Z]{1}-[A-Z]{2}-\d{4}|[A-Z]{1}-[A-Z]{2}-[A-Z]{1}-\d{4}'
    df['patient_id'] = df.patient_id.str.findall(rgx, flags=re.IGNORECASE).str[0]

    return df


def create_new_report(main_path, save_path):
    valid_ext = ['bmp', 'gif', 'jpg', 'jpeg', 'png', 'tiff'] # List of valid image extensions
    rm_folders = {'ZELEITA_MECHE116860935 HDC': '', 'H-PP-0046': '', 'F-PP-0222': 'F-PP-0218'} # Folders or subfolders to be removed ('folder':'subfolder') - ('' -> any subfolder)

    # Obtain all the images
    path_imgs = []
    for ext in valid_ext:
        path_imgs = path_imgs + glob.glob(os.path.join(main_path, '**/*.'+ext), recursive=True)

    # Create the dataframe
    df = pd.DataFrame(data=path_imgs, columns=['path'])

    # Remove the main path from the full path
    escaped_main_path = re.escape(os.path.join(main_path, ''))
    df['path'].replace(escaped_main_path, '', regex=True, inplace=True)
    df['path'] = df['path'].str.replace('\\', '/')
    #df['path'].replace(os.path.join(main_path, ''), '', regex=True, inplace=True)

    # Define the patient_id based on the path
    df['patient_id'] = df.path.str.split('/')

    # Obtain the date
    cond1 = df.patient_id.str.len()==3
    df['date'] = np.NaN
    df.loc[cond1, 'date'] = df.loc[cond1, 'patient_id'].str[1]

    # Obatin all information about the image
    df['image_id'] = df.path.str.split('/').str[-1].str.split('.').str[0]
    #df['image_no'] = df.image_id.str.split('_').str[-1].astype(int)
    df['image_no'] = df.image_id.str.split('_').str[-1].apply(convert_to_int)
    df['image_type'] = df.path.str.split('/').str[-1].str.split('.').str[1]

    # Remove data without a main subfolder or with subfolders within the main subfolder
    # and
    # remove a specific folder or subfolder
    rm_idx = df[(df.patient_id.str.len()<2) |
                (df.patient_id.str.len()>3) |
                (df.patient_id.str[0].isin(rm_folders.keys()) & df.date.isin([d for d in rm_folders.values() if d])) |
                (df.patient_id.str[0].isin([p for p, d in rm_folders.items() if d == '']))
                ].index
    df.drop(rm_idx, inplace=True)
    df.reset_index(drop=True, inplace=True)

    # Obtain only the patient_id
    df['patient_id'] = df.patient_id.str[0]

    # Correct the patient_id format (F-PP-0000 or F-PP-S-0000)
    rgx = r'([A-Z]{1})(-+)?([A-Z]{2})(-+)?([A-Z]{0,1})(-+)?(\d{4})'
    df['patient_id'] = df.patient_id.str.replace(rgx, r'\1-\3-\5-\7', regex=True)
    df['patient_id'] = df.patient_id.str.replace(r'--+', '-', regex=True)

    # Extract only the valid format
    rgx = r'[A-Z]{1}-[A-Z]{2}-\d{4}|[A-Z]{1}-[A-Z]{2}-[A-Z]{1}-\d{4}'
    df['patient_id'] = df.patient_id.str.findall(rgx, flags=re.IGNORECASE).str[0]

    # Reorder dataframe
    df.sort_values(by=['patient_id', 'image_no'], ascending=[True, True], inplace=True)

    # Set default values for the following columns
    df['category'] = 0
    df['cervical_length'] = " "
    df['ap1_diameter'] = " "
    df['ap2_diameter'] = " "
    df['completed'] = 'No'

    # Save the report
    df.to_excel(save_path, index=False)


class custom_file_dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.setStyleSheet(custom_file_dialog_ss())
        self.file_dialog = QFileDialog()
        layout.addWidget(self.file_dialog)


class update_value_thread(QThread):
    update_signal = pyqtSignal()

    def __init__(self, report, location, column_name, new_value, report_path):
        super().__init__()
        self.report = report
        self.location = location
        self.column_name = column_name
        self.new_value = new_value
        self.report_path = report_path

    def run(self):
        self.report.loc[self.location, self.column_name] = self.new_value
        try:
            with pd.ExcelWriter(self.report_path, engine='openpyxl') as writer:
                self.report.to_excel(writer, index=False)
        except PermissionError:
            pass
        #self.report.to_excel(self.report_path, index=False)
        self.update_signal.emit()