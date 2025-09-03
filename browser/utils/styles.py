def main_window_ss():
    return """
        background-color: #242A38;
    """

def label_selection_page1():
    return """
        color: #FFF; 
        font-size: 14px; 
        margin-bottom: 5px;
    """

def line_edit_page1():
    return """
        QLineEdit {
            color: #FFF;
            background-color: #242A38;
            font-size: 14px;
            border: 1px solid #8853DE;
            padding: 5px;
            border-top-left-radius: 3px;
            border-bottom-left-radius: 3px;
        }
    """

def select_button_page1():
    return """
        QPushButton{
            color: #FFF;
            background-color: #8853DE;
            font-size: 14px;
            border-top-right-radius: 3px;
            border-bottom-right-radius: 3px;
            padding: 7px 16px 7px 16px;
        }
    """

def list_view_ss():
    return """
        QListView {
            color: #FFF;
            background-color: #242A38;
            padding: 10px 0px 0px 0px;
            border: 1px solid #8853DE;
        }  
    """

def combobox_ss():
    return """
        QComboBox {
            color: #FFF;
            font-size: 14px;
            border: 1px solid #8853DE;
            border-top-left-radius: 3px;
            border-bottom-left-radius: 3px;
            padding: 5px;
        }
    
        QComboBox::item{
            padding: 5px;
            max-height: 20px;            
        }
    
        QComboBox::item:selected{
            background-color: #30344B;
            font-size: 14px;
            border: none;
        }        
    
        QComboBox::indicator{
            border: none;
        }        
    
        QComboBox::drop-down {
            border: none;
        }    
    """

def title_table_ss():
    return """
        QLabel {
            background-color: #1A1C28;
            font-size: 20px; 
            color: #FFF; 
            padding: 20px;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
        }
    """

def table_ss():
    return """
        QTableWidget {
            font-size: 12px;
            color: #FFF;
            background-color: #1A1C28;
            border-bottom-left-radius: 10px;
            border-bottom-right-radius: 10px;
            padding: 20px;
        }
        
        QHeaderView::section:horizontal {
            background-color: #1A1C28;
            font-size: 12px;
            font-weight: bold;
            color: #FFFFFF;
            border: none;
            border-bottom: 1px solid #30344B;
            padding: 0px 0px 10px 0px;
        }
        
        QTableView::item {
            border: none;
            border-bottom: 1px solid #30344B;
            height: 30px;
        }
        
        QTableWidget::item:selected {
            background-color: #30344B;
        }
        
        QScrollBar:vertical {
            background-color: #1A1C28;
            border: none;
            width: 10px;
        }
        
        QScrollBar::handle:vertical {
            background-color: #8853DE;
            border: none;
            border-radius: 5px;
        }
        
        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {
            border: none;
            background: none;
        }
    """

def prev_button_ss():
    return """
        QPushButton{
            color: #FFF;
            background-color: #8853DE;
            font-size: 14px;
            border-radius: 3px;
            padding: 7px 16px 7px 16px;
        }
    """

def next_button_ss():
    return """
        QPushButton{
            color: #FFF;
            background-color: #8853DE;
            font-size: 14px;
            border-radius: 3px;
            padding: 7px 16px 7px 16px;
        }
    """

def line_edit_page2():
    return """
        QLineEdit{
            color: #FFF;
        }
    """

def home_button_ss():
    return """
        QPushButton{
            image: url('assets/home.png');
            color: #FFF;
            background-color: #8853DE;
            font-size: 14px;
            border-radius: 3px;
            padding: 7px 16px 7px 16px;
        }    
    """

def checkbox_ss():
    return """
        QCheckBox{
            color: #FFF;
            font-size: 14px;
        }
        
        QCheckBox::indicator:checked{
            image: url('assets/tick.png');
            background-color: #FFF;
        }    
          
        QCheckBox:indicator{
            width: 16px;
            height: 16px;
            border: 2px solid #FFF;
            border-radius: 3px;
        }
    """

def window_new_report():
    return """
        background-color: #242A38
    """

def label_new_report():
    return """
        color: #FFF;
        font-size: 14px
    """

def line_edit_new_report():
    return """
        QLineEdit{
            font-size: 14px;
            border: 1px solid #8853DE;
            border-radius: 3px;
            padding: 5px;
            color: #FFF;
            margin-bottom: 15px;
        }
    """

def button_new_report():
    return """
        QPushButton{
            color: #FFF;
            background-color: #8853DE;
            font-size: 14px;
            border-radius: 3px;
            padding: 7px 16px 7px 16px;
        }
    """

def custom_file_dialog_ss():
    return """
        background-color: #FFF;
    """