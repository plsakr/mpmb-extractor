# This Python file uses the following encoding: utf-8
import sys

from PySide2.QtWidgets import QApplication, QWidget, QGridLayout, QLineEdit, QPushButton, QLabel, QFileDialog
import json

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdftypes import resolve1
from pdfminer.psparser import PSLiteral, PSKeyword
from pdfminer.utils import decode_text

pdf_keys = ["PC Name", "HP Max", "AC", "Initiative bonus", "Str Mod", "Str ST Mod", "Dex Mod", "Dex ST Mod", "Con Mod",
            "Con ST Mod", "Int Mod", "Int ST Mod", "Wis Mod", "Wis ST Mod", "Cha Mod", "Cha ST Mod", "Acr", "Ani",
            "Arc", "Ath", "Dec", "His", "Ins", "Inti", "Inv Bonus", "Med", "Nat", "Perc", "Perf", "Pers", "Rel", "Sle",
            "Ste", "Sur"]

pdf_data = {}


def decode_value(value):

    # decode PSLiteral, PSKeyword
    if isinstance(value, (PSLiteral, PSKeyword)):
        value = value.name

    # decode bytes
    if isinstance(value, bytes):
        value = decode_text(value)

    return value


data = {
    "name": "",
    "HPMax": 0,
    "ac": 0,
    "init": 0,
    "str": 0,
    "str_save": 0,
    "dex": 0,
    "dex_save": 0,
    "con": 0,
    "con_save": 0,
    "int": 0,
    "int_save": 0,
    "wis": 0,
    "wis_save": 0,
    "char": -0,
    "char_save": 0,
    "acrobatics": 0,
    "animal handling": 0,
    "arcana": 0,
    "athletics": 0,
    "deception": -0,
    "history": 0,
    "insight": 0,
    "intimidation": -0,
    "investigation": 0,
    "medicine": 0,
    "nature": 0,
    "perception": 0,
    "performance": -0,
    "persuasion": 0,
    "religion": 0,
    "sleight of hand": 0,
    "stealth": 0,
    "survival": 0,
}


class PdfExtractor(QWidget):

    def click_import(self):
        fname = QFileDialog.getOpenFileName(self, 'Choose PDF File', filter='PDF (*.pdf)')

        if fname[0] != '':
            print(fname[0])
            self.path_edit.setText(fname[0])

    def click_extract(self):
        p = self.path_edit.text()
        if p == '':
            return
        with open(p, 'rb') as fp:
            parser = PDFParser(fp)

            doc = PDFDocument(parser)
            res = resolve1(doc.catalog)

            if 'AcroForm' not in res:
                raise ValueError("No AcroForm Found")

            fields = resolve1(doc.catalog['AcroForm'])['Fields']  # may need further resolving

            for f in fields:
                field = resolve1(f)
                name, values = field.get('T'), field.get('V')

                # decode name
                name = decode_text(name)

                # resolve indirect obj
                values = resolve1(values)

                # decode value(s)
                if isinstance(values, list):
                    values = [decode_value(v) for v in values]
                else:
                    values = decode_value(values)

                pdf_data.update({name: values})

        data.update({
            "name": pdf_data[pdf_keys[0]],
            "HPMax": pdf_data[pdf_keys[1]],
            "ac": pdf_data[pdf_keys[2]],
            "init": pdf_data[pdf_keys[3]],
            "str": pdf_data[pdf_keys[4]],
            "str_save": pdf_data[pdf_keys[5]],
            "dex": pdf_data[pdf_keys[6]],
            "dex_save": pdf_data[pdf_keys[7]],
            "con": pdf_data[pdf_keys[8]],
            "con_save": pdf_data[pdf_keys[9]],
            "int": pdf_data[pdf_keys[10]],
            "int_save": pdf_data[pdf_keys[11]],
            "wis": pdf_data[pdf_keys[12]],
            "wis_save": pdf_data[pdf_keys[13]],
            "char": pdf_data[pdf_keys[14]],
            "char_save": pdf_data[pdf_keys[15]],
            "acrobatics": pdf_data[pdf_keys[16]],
            "animal handling": pdf_data[pdf_keys[17]],
            "arcana": pdf_data[pdf_keys[18]],
            "athletics": pdf_data[pdf_keys[19]],
            "deception": pdf_data[pdf_keys[20]],
            "history": pdf_data[pdf_keys[21]],
            "insight": pdf_data[pdf_keys[22]],
            "intimidation": pdf_data[pdf_keys[23]],
            "investigation": pdf_data[pdf_keys[24]],
            "medicine": pdf_data[pdf_keys[25]],
            "nature": pdf_data[pdf_keys[26]],
            "perception": pdf_data[pdf_keys[27]],
            "performance": pdf_data[pdf_keys[28]],
            "persuasion": pdf_data[pdf_keys[29]],
            "religion": pdf_data[pdf_keys[30]],
            "sleight of hand": pdf_data[pdf_keys[31]],
            "stealth": pdf_data[pdf_keys[32]],
            "survival": pdf_data[pdf_keys[33]],
        })

        self.update_texts()

    def click_export(self):
        self.update_data()

        if self.is_valid:
            fname = QFileDialog.getSaveFileName(self, 'Export to JSON', filter='JSON (*.json)')

            if fname[0] != '':
                with open(fname[0], 'w') as f:
                    json.dump(data, f, indent=4)


    def __init__(self):
        QWidget.__init__(self)
        self.is_valid = False
        self.setWindowTitle('Character Sheet Data Extractor')
        self.path_edit = QLineEdit()
        self.button_browse = QPushButton('Browse...')
        self.button_browse.clicked.connect(self.click_import)

        self.button_extract = QPushButton('Import Data')
        self.button_extract.clicked.connect(self.click_extract)

        self.button_export_data = QPushButton('Export Character...')
        self.button_export_data.clicked.connect(self.click_export)


        self.line_ch_name = QLineEdit()
        self.line_hp = QLineEdit()
        self.line_ac = QLineEdit()
        self.line_init = QLineEdit()
        self.line_str = QLineEdit()
        self.line_dex = QLineEdit()
        self.line_con = QLineEdit()
        self.line_int = QLineEdit()
        self.line_wis = QLineEdit()
        self.line_char = QLineEdit()
        self.line_str_save = QLineEdit()
        self.line_dex_save = QLineEdit()
        self.line_con_save = QLineEdit()
        self.line_int_save = QLineEdit()
        self.line_wis_save = QLineEdit()
        self.line_char_save = QLineEdit()
        self.line_arcana = QLineEdit()
        self.line_athletics = QLineEdit()
        self.line_deception = QLineEdit()
        self.line_history = QLineEdit()
        self.line_insight = QLineEdit()
        self.line_intimidation = QLineEdit()
        self.line_investigation = QLineEdit()
        self.line_medicine = QLineEdit()
        self.line_nature = QLineEdit()
        self.line_perception = QLineEdit()
        self.line_performance = QLineEdit()
        self.line_persuasion = QLineEdit()
        self.line_religion = QLineEdit()
        self.line_sleight = QLineEdit()
        self.line_stealth = QLineEdit()
        self.line_survival = QLineEdit()

        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()

        layout.addWidget(self.path_edit, 0, 0, 1, 2)
        layout.addWidget(self.button_browse, 0, 2)
        layout.addWidget(self.button_extract, 0, 3)

        layout.addWidget(QLabel('Character Name:'), 1, 0)
        layout.addWidget(self.line_ch_name, 1, 1)
        layout.addWidget(QLabel('Max HP:'), 1, 2)
        layout.addWidget(self.line_hp, 1, 3)

        layout.addWidget(QLabel('AC:'), 2, 0)
        layout.addWidget(self.line_ac, 2, 1)
        layout.addWidget(QLabel('Initiative:'), 2, 2)
        layout.addWidget(self.line_init, 2, 3)

        layout.addWidget(QLabel('Strength:'), 3, 0)
        layout.addWidget(self.line_str, 3, 1)
        layout.addWidget(QLabel('Dexterity:'), 3, 2)
        layout.addWidget(self.line_dex, 3, 3)

        layout.addWidget(QLabel('Constitution:'), 4, 0)
        layout.addWidget(self.line_con, 4, 1)
        layout.addWidget(QLabel('Intelligence:'), 4, 2)
        layout.addWidget(self.line_int, 4, 3)

        layout.addWidget(QLabel('Wisdom:'), 5, 0)
        layout.addWidget(self.line_wis, 5, 1)
        layout.addWidget(QLabel('Charisma:'), 5, 2)
        layout.addWidget(self.line_char, 5, 3)

        layout.addWidget(QLabel('Strength Save:'), 6, 0)
        layout.addWidget(self.line_str_save, 6, 1)
        layout.addWidget(QLabel('Dexterity Save:'), 6, 2)
        layout.addWidget(self.line_dex_save, 6, 3)
        layout.addWidget(QLabel('Constitution Save:'), 7, 0)
        layout.addWidget(self.line_con_save, 7, 1)
        layout.addWidget(QLabel('Intelligence Save:'), 7, 2)
        layout.addWidget(self.line_int_save, 7, 3)

        layout.addWidget(QLabel('Wisdom Save:'), 8, 0)
        layout.addWidget(self.line_wis_save, 8, 1)
        layout.addWidget(QLabel('Charisma Save:'), 8, 2)
        layout.addWidget(self.line_char_save, 8, 3)

        layout.addWidget(QLabel('Arcana:'), 9, 0)
        layout.addWidget(self.line_arcana, 9, 1)
        layout.addWidget(QLabel('Athletics:'), 9, 2)
        layout.addWidget(self.line_athletics, 9, 3)

        layout.addWidget(QLabel('Deception:'), 10, 0)
        layout.addWidget(self.line_deception, 10, 1)
        layout.addWidget(QLabel('History:'), 10, 2)
        layout.addWidget(self.line_history, 10, 3)

        layout.addWidget(QLabel('Insight:'), 11, 0)
        layout.addWidget(self.line_insight, 11, 1)
        layout.addWidget(QLabel('Intimidation:'), 11, 2)
        layout.addWidget(self.line_intimidation, 11, 3)

        layout.addWidget(QLabel('Investigation:'), 12, 0)
        layout.addWidget(self.line_investigation, 12, 1)
        layout.addWidget(QLabel('Medicine:'), 12, 2)
        layout.addWidget(self.line_medicine, 12, 3)

        layout.addWidget(QLabel('Nature:'), 13, 0)
        layout.addWidget(self.line_nature, 13, 1)
        layout.addWidget(QLabel('Perception:'), 13, 2)
        layout.addWidget(self.line_perception, 13, 3)

        layout.addWidget(QLabel('Performance:'), 14, 0)
        layout.addWidget(self.line_performance, 14, 1)
        layout.addWidget(QLabel('Persuasion:'), 14, 2)
        layout.addWidget(self.line_persuasion, 14, 3)

        layout.addWidget(QLabel('Religion:'), 15, 0)
        layout.addWidget(self.line_religion, 15, 1)
        layout.addWidget(QLabel('Sleight of Hand:'), 15, 2)
        layout.addWidget(self.line_sleight, 15, 3)

        layout.addWidget(QLabel('Stealth:'), 16, 0)
        layout.addWidget(self.line_stealth, 16, 1)
        layout.addWidget(QLabel('Survival:'), 16, 2)
        layout.addWidget(self.line_survival, 16, 3)

        layout.addWidget(self.button_export_data, 17, 0, 1, 4)

        self.setLayout(layout)

    def update_texts(self):
        self.line_ch_name.setText(data["name"])
        self.line_hp.setText(data["HPMax"])
        self.line_ac.setText(data["ac"])
        self.line_init.setText(data["init"])
        self.line_str.setText(data["str"])
        self.line_dex.setText(data["dex"])
        self.line_con.setText(data["con"])
        self.line_int.setText(data["int"])
        self.line_wis.setText(data["wis"])
        self.line_char.setText(data["char"])
        self.line_str_save.setText(data["str_save"])
        self.line_dex_save.setText(data["dex_save"])
        self.line_con_save.setText(data["con_save"])
        self.line_int_save.setText(data["int_save"])
        self.line_wis_save.setText(data["wis_save"])
        self.line_char_save.setText(data["char_save"])
        self.line_arcana.setText(data["arcana"])
        self.line_athletics.setText(data["athletics"])
        self.line_deception.setText(data["deception"])
        self.line_history.setText(data["history"])
        self.line_insight.setText(data["insight"])
        self.line_intimidation.setText(data["intimidation"])
        self.line_investigation.setText(data["investigation"])
        self.line_medicine.setText(data["medicine"])
        self.line_nature.setText(data["nature"])
        self.line_perception.setText(data["perception"])
        self.line_performance.setText(data["performance"])
        self.line_persuasion.setText(data["persuasion"])
        self.line_religion.setText(data["religion"])
        self.line_sleight.setText(data["sleight of hand"])
        self.line_stealth.setText(data["stealth"])
        self.line_survival.setText(data["survival"])

    def update_data(self):
        data["name"] = self.line_ch_name.text()
        data["HPMax"] = self.line_hp.text()
        data["ac"] = self.line_ac.text()
        data["init"] = self.line_init.text()
        data["str"] = self.line_str.text()
        data["dex"] = self.line_dex.text()
        data["con"] = self.line_con.text()
        data["int"] = self.line_int.text()
        data["wis"] = self.line_wis.text()
        data["char"] = self.line_char.text()
        data["str_save"] = self.line_str_save.text()
        data["dex_save"] = self.line_dex_save.text()
        data["con_save"] = self.line_con_save.text()
        data["int_save"] = self.line_int_save.text()
        data["wis_save"] = self.line_wis_save.text()
        data["char_save"] = self.line_char_save.text()
        data["arcana"] = self.line_arcana.text()
        data["athletics"] = self.line_athletics.text()
        data["deception"] = self.line_deception.text()
        data["history"] = self.line_history.text()
        data["insight"] = self.line_insight.text()
        data["intimidation"] = self.line_intimidation.text()
        data["investigation"] = self.line_investigation.text()
        data["medicine"] = self.line_medicine.text()
        data["nature"] = self.line_nature.text()
        data["perception"] = self.line_perception.text()
        data["performance"] = self.line_performance.text()
        data["persuasion"] = self.line_persuasion.text()
        data["religion"] = self.line_religion.text()
        data["sleight of hand"] = self.line_sleight.text()
        data["stealth"] = self.line_stealth.text()
        data["survival"] = self.line_survival.text()

        for k in data.keys():
            if k != 'name':
                try:
                    data[k] = int(data[k])
                except ValueError:
                    self.is_valid = False
                    return

        self.is_valid = True



if __name__ == "__main__":
    app = QApplication([])
    window = PdfExtractor()
    window.show()
    sys.exit(app.exec_())
