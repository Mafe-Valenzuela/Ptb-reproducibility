import atexit
import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (QApplication, QMainWindow, QHBoxLayout, QWidget,
                             QLabel, QPushButton, QLineEdit, QSpacerItem, QSizePolicy,
                             QTableWidget, QTableWidgetItem, QHeaderView, QComboBox,
                             QStackedWidget, QCheckBox)
from utils.scripts import *
from utils.styles import *



class browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        #self.autosave_timer = QTimer(self)
        #self.autosave_timer.timeout.connect(self.autosave_data)
        #self.autosave_timer.start(60000)
        atexit.register(self.autosave_data)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)


    def init_ui(self):
        self.stacked_widget = QStackedWidget(self)
        self.cond_hmax = QApplication.desktop().screenGeometry().height() >= 900

        ##############
        ### PAGE 1 ###
        ##############
        page1 = QWidget()
        layout1 = QVBoxLayout(page1)
        layout1.setContentsMargins(20, 20, 20, 20)
        layout1.setSpacing(0)

        ## BOX FOR FOLDER SELECTION ##
        # Title for folder selection
        self.label_folder = QLabel("Main folder:")
        self.label_folder.setStyleSheet(label_selection_page1())
        layout1.addWidget(self.label_folder)

        # Create the box
        main_folder_box = QHBoxLayout()
        main_folder_box.setContentsMargins(0, 0, 0, 20)
        main_folder_box.setSpacing(0)
        layout1.addLayout(main_folder_box)

        # Input text
        self.folder_input = QLineEdit()
        self.folder_input.setStyleSheet(line_edit_page1())
        main_folder_box.addWidget(self.folder_input)

        # Selection with button
        self.folder_button = QPushButton("Select")
        self.folder_button.clicked.connect(self.show_folder_dialog)
        self.folder_button.setStyleSheet(select_button_page1())
        main_folder_box.addWidget(self.folder_button)


        ## SECTION TO CHOOSE EXISTING OR NEW REPORT ##
        # Title of the list
        self.label_report = QLabel("Select report:")
        self.label_report.setStyleSheet(label_selection_page1())
        layout1.addWidget(self.label_report)

        # Create the box that contains the button and list
        select_report_layout = QHBoxLayout()
        select_report_layout.setContentsMargins(0, 0, 0, 20)
        select_report_layout.setSpacing(0)
        layout1.addLayout(select_report_layout)

        # List
        self.report_combobox = QComboBox()
        self.report_combobox.addItems(["Existing", "New"])
        list_view = self.report_combobox.view()
        list_view.setStyleSheet(list_view_ss())
        self.report_combobox.setStyleSheet(combobox_ss())
        self.report_combobox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        select_report_layout.addWidget(self.report_combobox)

        # Button
        self.report_button = QPushButton("Select")
        self.report_button.clicked.connect(self.process_report)
        self.report_button.setStyleSheet(select_button_page1())
        select_report_layout.addWidget(self.report_button)
        self.set_content('report', 'reset')


        ## BOX FOR PATIENT INFORMATION ##
        # Title
        self.label_patient_info = QLabel("Patient information:")
        self.label_patient_info.setStyleSheet(label_selection_page1())
        layout1.addWidget(self.label_patient_info)

        # Create the box
        patient_info_box = QHBoxLayout()
        patient_info_box.setContentsMargins(0, 0, 0, 20)
        patient_info_box.setSpacing(0)
        layout1.addLayout(patient_info_box)

        # Input text
        self.patient_info_input = QLineEdit()
        self.patient_info_input.setStyleSheet(line_edit_page1())
        patient_info_box.addWidget(self.patient_info_input)

        # Selection with button
        self.patient_info_button = QPushButton("Select")
        self.patient_info_button.clicked.connect(self.show_patient_info_dialog)
        self.patient_info_button.setStyleSheet(select_button_page1())

        # Add the box
        patient_info_box.addWidget(self.patient_info_button)
        self.set_content('patient_info', 'reset')


        ## TABLE WITH THE PATIENT LIST ##
        # Print the title of the table
        title_label = QLabel("List of Patients")
        title_label.setAlignment(Qt.AlignHCenter)
        title_label.setStyleSheet(title_table_ss())
        layout1.addWidget(title_label)

        # Set table
        self.patient_table = QTableWidget()
        self.patient_table.horizontalHeader().setDefaultAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.patient_table.setColumnCount(3)
        self.patient_table.setHorizontalHeaderLabels(["Patient ID", "Images", "Completed"])
        self.patient_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.patient_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.patient_table.clicked.connect(self.on_patient_selected)
        self.patient_table.setShowGrid(False)
        self.patient_table.setStyleSheet(table_ss())
        layout1.addWidget(self.patient_table)
        self.patient_table.verticalHeader().setVisible(False)
        self.patient_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


        ## SAVE BUTTON ##
        button_save_layout = QVBoxLayout()
        button_save_layout.setContentsMargins(0, 20, 0, 0)
        self.button_save = QPushButton("Save")
        self.button_save.setFixedSize(120, 30)
        self.button_save.clicked.connect(self.autosave_data)
        self.button_save.setStyleSheet(button_new_report())
        button_save_layout.addWidget(self.button_save, alignment=Qt.AlignHCenter | Qt.AlignVCenter)
        layout1.addLayout(button_save_layout)


        ## ADD THE PAGE1 TO THE STACKED WIDGET ##
        self.stacked_widget.addWidget(page1)



        ##############
        ### PAGE 2 ###
        ##############
        page2 = QWidget()

        layout2 = QVBoxLayout(page2) if self.cond_hmax else QHBoxLayout(page2)
        layout2.setContentsMargins(40, 40, 40, 40)
        layout2.setSpacing(0)

        image_button = QVBoxLayout()
        image_button.setContentsMargins(0, 0, 20, 0) if not self.cond_hmax else None
        table_button = QVBoxLayout()


        ## IMAGE BOX ##
        # Show the image
        self.image_label = QLabel(alignment=Qt.AlignCenter)
        image_button.addWidget(self.image_label)
        #layout2.addWidget(self.image_label)


        ## PREVIOUS AND NEXT BUTTONS ##
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        button_layout.setContentsMargins(0, 20, 0, 20) if self.cond_hmax else button_layout.setContentsMargins(0, 20, 0, 0)

        # Previous buttons
        prev_button = QPushButton("Previous")
        prev_button.setStyleSheet(prev_button_ss())
        prev_button.setFixedSize(120, 30)
        prev_button.clicked.connect(self.prev_image)

        # Next button
        next_button = QPushButton("Next")
        next_button.setStyleSheet(next_button_ss())
        next_button.setFixedSize(120, 30)
        next_button.clicked.connect(self.next_image)

        # Add and center the buttons
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        button_layout.addItem(spacer)
        button_layout.addWidget(prev_button)
        button_layout.addWidget(next_button)
        button_layout.addItem(spacer)
        #layout2.addLayout(button_layout)


        ## DETAILS ##
        # Print the title of the table
        title_label_2 = QLabel("Details")
        title_label_2.setAlignment(Qt.AlignHCenter)
        title_label_2.setStyleSheet(title_table_ss())
        table_button.addWidget(title_label_2)
        #layout2.addWidget(title_label_2)

        # Set table
        self.table_details = QTableWidget()
        self.table_details.setColumnCount(3)
        self.table_details.setRowCount(6)
        self.table_details.horizontalHeader().setDefaultAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.table_details.setHorizontalHeaderLabels(["Field", "Fixed value", "User value"])
        self.table_details.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table_details.setShowGrid(False)
        self.table_details.setStyleSheet(table_ss())
        layout2.addWidget(self.table_details)
        self.table_details.verticalHeader().setVisible(False)
        self.table_details.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        rows = [
            ("Patient ID", "", ""),
            ("Image ID", "", ""),
            ("AP1 diameter [cm]", "", ""),
            ("AP2 diameter [cm]", "", ""),
            ("Cervical length [cm]", "", ""),
            ("Category", "", "")
        ]
        self.widget_data = {
            "Category": {"widget": QLineEdit(), "signal": lambda: self.update_data('Category')},
            "Cervical length [cm]": {"widget": QLineEdit(), "signal": lambda: self.update_data('Cervical length [cm]')},
            "AP1 diameter [cm]": {"widget": QLineEdit(), "signal": lambda: self.update_data('AP1 diameter [cm]')},
            "AP2 diameter [cm]": {"widget": QLineEdit(), "signal": lambda: self.update_data('AP2 diameter [cm]')}
        }
        for row, (label, value_col1, value_col2) in enumerate(rows):
            self.set_table_item(self.table_details, row, 0, label)
            self.set_table_item(self.table_details, row, 1, value_col1)
            self.set_table_item(self.table_details, row, 2, value_col2)


        # Category editable
        self.ecat = QLineEdit("")
        self.ecat.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.ecat.setStyleSheet(line_edit_page2())
        self.ecat.textChanged.connect(lambda: self.update_cat(self.idxs, self.location))
        self.table_details.setCellWidget(5, 1, self.ecat)

        # AP1 diameter editable
        self.eap1 = QLineEdit("")
        self.eap1.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.eap1.setStyleSheet(line_edit_page2())
        self.eap1.textChanged.connect(lambda: self.update_ap1(self.idxs, self.location))
        self.table_details.setCellWidget(2, 2, self.eap1)

        # AP2 diameter editable
        self.eap2 = QLineEdit("")
        self.eap2.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.eap2.setStyleSheet(line_edit_page2())
        self.eap2.textChanged.connect(lambda: self.update_ap2(self.idxs, self.location))
        self.table_details.setCellWidget(3, 2, self.eap2)

        # Cervical length editable
        self.ecl = QLineEdit("")
        self.ecl.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.ecl.setStyleSheet(line_edit_page2())
        self.ecl.textChanged.connect(lambda: self.update_cl(self.idxs, self.location))
        #self.ecl.editingFinished.connect(lambda: self.update_cl(self.idxs, self.location))
        self.table_details.setCellWidget(4, 2, self.ecl)

        # Add table
        self.table_details.setMinimumWidth(550)
        table_button.addWidget(self.table_details)
        #layout2.addWidget(self.table_details)


        ## HOME BUTTON AND CHECKBOX ##
        home_check = QHBoxLayout()
        home_check.setContentsMargins(0, 20, 0, 0)
        home_check.setSpacing(200)

        # Home button
        home_button = QPushButton("")
        home_button.setStyleSheet(home_button_ss())
        home_button.setFixedSize(120, 30)
        home_button.clicked.connect(lambda: self.patient_table.clearSelection())
        home_button.clicked.connect(lambda: self.patient_table.setCurrentCell(-1, -1))
        home_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(page1))

        # Checkbox
        self.checkbox = QCheckBox("Completed")
        self.checkbox.setStyleSheet(checkbox_ss())
        self.checkbox.stateChanged.connect(self.handle_checkbox_state)

        # Add home button and checkbox
        home_check.addItem(spacer)
        home_check.addWidget(home_button)
        home_check.addWidget(self.checkbox)
        home_check.addItem(spacer)
        #layout2.addLayout(home_check)


        ## ADD TABLE_BUTTON AND IMAGE_BUTTON LAYOUT ##
        table_button.addLayout(home_check) if self.cond_hmax else image_button.addLayout(home_check)
        image_button.addLayout(button_layout) if self.cond_hmax else table_button.addLayout(button_layout)
        layout2.addLayout(image_button)
        layout2.addLayout(table_button)


        ## ADD THE PAGE2 TO THE STACKED WIDGET ##
        self.stacked_widget.addWidget(page2)



        ###########################################
        ### SET INITIAL PAGE AND CENTRAL WIDGET ###
        ###########################################
        self.stacked_widget.setCurrentWidget(page1)
        self.setCentralWidget(self.stacked_widget)



    def autosave_data(self):
        if (not self.report.empty) and (self.report_path is not None):
            try:
                with pd.ExcelWriter(self.report_path, engine='openpyxl') as writer:
                    self.report.to_excel(writer, index=False)
            except PermissionError:
                pass
           #self.report.to_excel(self.report_path, index=False)


    def update_cat(self, idx, location):
        new_data = self.ecat.text()
        try:
            new_data = int(new_data)
        except ValueError:
            new_data = 0
        if self.categories[location] != new_data:
            self.categories[location] = new_data
            self.report.loc[idx[location], 'category'] = new_data


    def update_ap1(self, idx, location):
        new_data = self.eap1.text()
        try:
            new_data = float(new_data)
        except ValueError:
            new_data = " "
        if self.ap1[location] != new_data:
            self.ap1[location] = new_data
            self.report.loc[idx[location], 'ap1_diameter'] = new_data


    def update_ap2(self, idx, location):
        new_data = self.eap2.text()
        try:
            new_data = float(new_data)
        except ValueError:
            new_data = " "
        if self.ap2[location] != new_data:
            self.ap2[location] = new_data
            self.report.loc[idx[location], 'ap2_diameter'] = new_data


    def update_cl(self, idx, location):
        new_data = self.ecl.text()
        try:
            new_data = float(new_data)
        except ValueError:
            new_data = " "
        if self.cl[location] != new_data:
            self.cl[location] = new_data
            self.report.loc[idx[location], 'cervical_length'] = new_data


    def set_content(self, section, state):
        if (section in ['main_folder', 'pag1']) and state=='reset':
            self.main_path = []
            self.folder_input.setText('')

        if section in ['report', 'pag1']:
            if state=='reset':
                self.report_path = None
                self.report = pd.DataFrame()
                self.report_changed = False
                self.report_combobox.setCurrentText('Existing')
                self.report_combobox.hide()
                self.report_button.hide()
                self.label_report.hide()
            elif state=='show':
                self.report_combobox.setVisible(True)
                self.report_button.setVisible(True)
                self.label_report.setVisible(True)

        if section in ['patient_info', 'pag1']:
            if state=='reset':
                self.details = []
                self.details_path = []
                self.patient_info_changed = False
                self.patient_info_input.setText('')
                self.patient_info_input.hide()
                self.patient_info_button.hide()
                self.label_patient_info.hide()
            elif state=='show':
                self.patient_info_input.setVisible(True)
                self.patient_info_button.setVisible(True)
                self.label_patient_info.setVisible(True)

        if section in ['patient_table', 'pag1'] and state=='reset':
            self.patient_table.clearContents()
            self.patient_table.setRowCount(0)


    def show_folder_dialog(self):
        self.set_content('pag1', 'reset')
        dialog = custom_file_dialog(self)
        #options = QFileDialog.Options()
        options = QFileDialog.Option.DontUseNativeDialog
        self.main_path = dialog.file_dialog.getExistingDirectory(dialog, "Select folder", options=options)
        if self.main_path:
            self.folder_input.setText(self.main_path)
            self.set_content('report', 'show')
        dialog.deleteLater()


    def process_report(self):
        if self.report_changed:
            self.set_content('pag1', 'reset')
        else:
            selected_action = self.report_combobox.currentText()
            {'Existing': self.show_report_dialog, 'New': self.new_report_dialog}.get(selected_action, lambda: None)()


    def show_report_dialog(self):
        dialog = custom_file_dialog(self)
        dialog.file_dialog.setDirectory('./reports')
        #options = QFileDialog.Options()
        options = QFileDialog.Option.DontUseNativeDialog
        txt_opts = 'Excel files (*.xlsx);; Text CSV (*.csv);; All Files (*)'
        self.report_path, _ = dialog.file_dialog.getOpenFileName(dialog, "Existing report", "", txt_opts, options=options)
        if self.report_path:
            self.set_content('patient_info', 'show')
            self.report_changed = True
        dialog.deleteLater()


    def new_report_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("New report")
        dialog.resize(250, 100)
        dialog.setStyleSheet(window_new_report())
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(20, 20, 20, 20)
        label = QLabel("Report name:")
        label.setStyleSheet(label_new_report())
        layout.addWidget(label)
        report_name = QLineEdit()
        report_name.setStyleSheet(line_edit_new_report())
        layout.addWidget(report_name)
        confirm_button = QPushButton("Create")
        confirm_button.setStyleSheet(button_new_report())
        confirm_button.clicked.connect(dialog.accept)
        layout.addWidget(confirm_button, alignment=Qt.AlignCenter)

        if dialog.exec_() == QDialog.Accepted:
            new_report_name = report_name.text().strip().split('.')[0]
            new_report_name = "_".join(new_report_name.lower().split())
            if new_report_name:
                self.report_path = f'./reports/{new_report_name}.xlsx'
                create_new_report(self.main_path, self.report_path)
                self.set_content('patient_info', 'show')
                self.report_changed = True


    def show_patient_info_dialog(self):
        if self.patient_info_changed:
            self.set_content('pag1', 'reset')
        else:
            dialog = custom_file_dialog(self)
            #options = QFileDialog.Options()
            options = QFileDialog.Option.DontUseNativeDialog
            txt_opts = 'Excel files (*.xlsx);; Text CSV (*.csv);; All Files (*)'
            self.details_path, _ = dialog.file_dialog.getOpenFileName(dialog, "Patient information", "", txt_opts, options=options)
            if self.details_path:
                self.patient_info_input.setText(self.details_path)
                self.details = pd.read_excel(self.details_path, engine='openpyxl')
                self.details = correct_patient_id(self.details)
                self.load_table(self.report_path)
                self.patient_info_changed = True
            dialog.deleteLater()


    def set_table_item(self, table, row, col, value):
        item = QTableWidgetItem(str(value))
        item.setTextAlignment(int(Qt.AlignHCenter | Qt.AlignVCenter))
        table.setItem(row, col, item)


    def load_table(self, report_path):
        # Load report and obtain the number of images for each patient
        self.report = pd.read_excel(report_path, engine='openpyxl')
        patient_data = self.report.groupby('patient_id').agg(no_images=('patient_id', 'size'), completed=('completed', 'first')).reset_index()

        # Show the patient_id, number of images and completed value in the table
        self.patient_table.setRowCount(len(patient_data))
        for i, (_, d) in enumerate(patient_data.iterrows()):
            patient_id_item = d.patient_id
            num_images_item = str(d.no_images)
            completed_value = d.completed
            self.set_table_item(self.patient_table, i, 0, patient_id_item)
            self.set_table_item(self.patient_table, i, 1, num_images_item)
            self.set_table_item(self.patient_table, i, 2, completed_value)
            color = QColor(0, 255, 0) if completed_value == "Yes" else QColor(255, 0, 0)
            self.patient_table.item(i, 2).setForeground(color)
            self.patient_table.setRowHeight(i, 40)


    def on_patient_selected(self, index):
        self.selected_row = []
        self.images = []
        self.image_id = []
        self.categories = []
        self.cl = []
        self.ap1 = []
        self.ap2 = []
        self.idxs = []

        # Show page2
        self.stacked_widget.setCurrentIndex(1)

        # Get patient information
        patient_id = self.patient_table.item(index.row(), 0).text()
        patient_row = self.report[self.report.patient_id == patient_id]
        completed_value = self.patient_table.item(index.row(), 2).text()

        # Save patient details
        self.selected_row = index.row()
        self.images = [os.path.join(self.main_path, img) for img in list(patient_row.path)]
        self.image_id = list(patient_row.image_id)
        self.categories = list(patient_row.category)
        self.cl = list(patient_row.cervical_length)
        self.ap1 = list(patient_row.ap1_diameter)
        self.ap2 = list(patient_row.ap2_diameter)
        self.idxs = list(patient_row.index)

        # Set the first item for each patient
        self.location = 0
        self.load_image(self.images[self.location])
        self.ecat.setText(str(self.categories[self.location]))
        self.eap1.setText(str(self.ap1[self.location]))
        self.eap2.setText(str(self.ap2[self.location]))
        self.ecl.setText(str(self.cl[self.location]))

        # Show cervical length, ap1 diameter, and ap2 diameter
        self.set_table_item(self.table_details, 0, 1, patient_id)
        self.set_table_item(self.table_details, 1, 1, self.image_id[self.location])
        if patient_id in self.details['patient_id'].values:
            patient_data = self.details[self.details['patient_id'] == patient_id].iloc[0]
            ap1_diameter = patient_data['ap1_diameter']
            ap2_diameter = patient_data['ap2_diameter']
            cervical_length = patient_data['cervical_length']
            self.set_table_item(self.table_details, 2, 1, round(ap1_diameter * 0.1, 5))
            self.set_table_item(self.table_details, 3, 1, round(ap2_diameter * 0.1, 5))
            self.set_table_item(self.table_details, 4, 1, round(cervical_length * 0.1, 5))
        else:
            self.set_table_item(self.table_details, 2, 1, "")
            self.set_table_item(self.table_details, 3, 1, "")
            self.set_table_item(self.table_details, 4, 1, "")


        # Update checkbox
        self.checkbox.setChecked(completed_value == 'Yes')


    def load_image(self, path):
        if not path:
            return
        load_image(path, self.image_label)


    def prev_image(self):
        if self.images:
            self.location = (self.location - 1) % len(self.images)
            self.load_image(self.images[self.location])
            self.set_table_item(self.table_details, 1, 1, self.image_id[self.location])
            self.ecat.setText(str(self.categories[self.location]))
            self.ecl.setText(str(self.cl[self.location]))
            self.eap1.setText(str(self.ap1[self.location]))
            self.eap2.setText(str(self.ap2[self.location]))


    def next_image(self):
        if self.images:
            self.location = (self.location + 1) % len(self.images)
            self.load_image(self.images[self.location])
            self.set_table_item(self.table_details, 1, 1, self.image_id[self.location])
            self.ecat.setText(str(self.categories[self.location]))
            self.eap1.setText(str(self.ap1[self.location]))
            self.eap2.setText(str(self.ap2[self.location]))
            self.ecl.setText(str(self.cl[self.location]))


    def handle_checkbox_state(self, state):
        patient_id = self.patient_table.item(self.selected_row, 0).text()
        completed_value = "Yes" if state == Qt.Checked else "No"

        # Set value in patient table
        self.set_table_item(self.patient_table, self.selected_row, 2, completed_value)
        color = QColor(0, 255, 0) if completed_value == "Yes" else QColor(255, 0, 0)
        self.patient_table.item(self.selected_row, 2).setForeground(color)

        # Update report
        self.update_value = update_value_thread(self.report, self.idxs, 'completed', completed_value, self.report_path)
        self.update_value.finished.connect(self.update_value.quit)
        self.update_value.start()



if __name__ == '__main__':
    make_dir('./reports')
    app = QApplication(sys.argv)
    window = browser()
    window.setWindowTitle("Browser")
    window.resize(800, QApplication.desktop().screenGeometry().height())
    window.setStyleSheet(main_window_ss())
    window.show()
    sys.exit(app.exec_())