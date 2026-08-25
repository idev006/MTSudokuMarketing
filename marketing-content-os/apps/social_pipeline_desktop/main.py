from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import Qt, QThread, QUrl, Signal
from PySide6.QtGui import QAction, QDesktopServices, QGuiApplication
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QFileDialog,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

try:
    from .pipeline_service import (
        CleanResult,
        build_gpt2_template,
        clean_folder,
        discover_raw_files,
        read_clean_rows,
    )
except ImportError:  # Allows: python marketing-content-os/apps/social_pipeline_desktop/main.py
    from pipeline_service import (  # type: ignore
        CleanResult,
        build_gpt2_template,
        clean_folder,
        discover_raw_files,
        read_clean_rows,
    )


class CleanWorker(QThread):
    finished_with_results = Signal(list)
    failed = Signal(str)

    def __init__(
        self,
        input_folder: Path,
        expected_rows: int,
        allow_visual_concentration: bool,
        allow_angle_concentration: bool,
    ) -> None:
        super().__init__()
        self.input_folder = input_folder
        self.expected_rows = expected_rows
        self.allow_visual_concentration = allow_visual_concentration
        self.allow_angle_concentration = allow_angle_concentration

    def run(self) -> None:
        try:
            results = clean_folder(
                self.input_folder,
                expected_rows=self.expected_rows,
                allow_visual_concentration=self.allow_visual_concentration,
                allow_angle_concentration=self.allow_angle_concentration,
            )
            self.finished_with_results.emit(results)
        except Exception as exc:  # noqa: BLE001 - UI must surface any failure.
            self.failed.emit(str(exc))


class StepBadge(QFrame):
    def __init__(self, number: str, title: str) -> None:
        super().__init__()
        self.setObjectName("StepBadge")
        self.number = QLabel(number)
        self.number.setObjectName("StepNumber")
        self.title = QLabel(title)
        self.title.setObjectName("StepTitle")
        self.title.setWordWrap(True)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.addWidget(self.number)
        layout.addWidget(self.title, stretch=1)

    def set_active(self, active: bool) -> None:
        self.setProperty("active", active)
        self.style().unpolish(self)
        self.style().polish(self)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("BiiigBee Social Content Pipeline")
        self.resize(1280, 820)
        self.results: list[CleanResult] = []
        self.worker: CleanWorker | None = None

        self.setStyleSheet(
            """
            QMainWindow { background: #f6f8fb; }
            QLabel#AppTitle { font-size: 24px; font-weight: 700; color: #172033; }
            QLabel#AppSubtitle { font-size: 13px; color: #556070; }
            QFrame#CoachCard { background: #ffffff; border: 1px solid #dbe3ef; border-radius: 12px; }
            QLabel#CoachTitle { font-size: 19px; font-weight: 700; color: #14315c; }
            QLabel#CoachText { font-size: 15px; color: #26364d; }
            QLabel#MetricBig { font-size: 22px; font-weight: 700; color: #14315c; }
            QLabel#MetricLabel { font-size: 12px; color: #5f6f86; }
            QFrame#StepBadge { background: #eef3fb; border: 1px solid #d5dfef; border-radius: 10px; }
            QFrame#StepBadge[active="true"] { background: #dff0ff; border: 2px solid #3b82f6; }
            QLabel#StepNumber { font-size: 18px; font-weight: 700; color: #1d4ed8; min-width: 26px; }
            QLabel#StepTitle { font-size: 13px; color: #26364d; }
            QPushButton { padding: 9px 14px; border-radius: 8px; background: #e7edf7; border: 1px solid #cbd6e7; }
            QPushButton:hover { background: #dbe7f7; }
            QPushButton#PrimaryButton { background: #2563eb; color: #ffffff; font-size: 16px; font-weight: 700; border: 1px solid #1d4ed8; padding: 12px 18px; }
            QPushButton#PrimaryButton:disabled { background: #9fb6df; border: 1px solid #9fb6df; }
            QPushButton#SuccessButton { background: #059669; color: #ffffff; font-weight: 700; border: 1px solid #047857; }
            QPushButton#DangerButton { background: #fee2e2; color: #991b1b; border: 1px solid #fecaca; }
            QGroupBox { background: #ffffff; border: 1px solid #dbe3ef; border-radius: 10px; margin-top: 12px; padding: 12px; }
            QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 4px; color: #304158; font-weight: 700; }
            QTableWidget { background: #ffffff; border: 1px solid #dbe3ef; border-radius: 8px; gridline-color: #edf2f7; }
            QTextEdit { background: #ffffff; border: 1px solid #dbe3ef; border-radius: 8px; padding: 8px; }
            QLineEdit, QSpinBox { padding: 7px; border: 1px solid #cbd6e7; border-radius: 7px; background: #ffffff; }
            """
        )

        self.step_badges = [
            StepBadge("1", "เลือกโฟลเดอร์ raw จาก GPT1"),
            StepBadge("2", "กด Clean All Files"),
            StepBadge("3", "ดู PASS / FAIL"),
            StepBadge("4", "Copy prompt ไป GPT2"),
            StepBadge("5", "สร้างภาพและตรวจ"),
        ]

        self.app_title = QLabel("BiiigBee Social Content Pipeline")
        self.app_title.setObjectName("AppTitle")
        self.app_subtitle = QLabel("Guided desktop workflow: GPT1 raw files → clean TSV → GPT2 handoff. ผู้ใช้ทำตามปุ่มหลัก ไม่ต้องจำ pipeline")
        self.app_subtitle.setObjectName("AppSubtitle")

        self.coach_title = QLabel("ตอนนี้ให้เลือกโฟลเดอร์ที่เก็บ raw output จาก GPT1")
        self.coach_title.setObjectName("CoachTitle")
        self.coach_text = QLabel("โปรแกรมจะค้นหาไฟล์ .md / .txt / .text ในโฟลเดอร์นั้น แล้ว clean + validate ให้ทั้งหมด")
        self.coach_text.setObjectName("CoachText")
        self.coach_text.setWordWrap(True)

        coach_card = QFrame()
        coach_card.setObjectName("CoachCard")
        coach_layout = QVBoxLayout(coach_card)
        coach_layout.addWidget(self.coach_title)
        coach_layout.addWidget(self.coach_text)

        self.raw_count_value = QLabel("0")
        self.raw_count_value.setObjectName("MetricBig")
        self.pass_count_value = QLabel("0")
        self.pass_count_value.setObjectName("MetricBig")
        self.fail_count_value = QLabel("0")
        self.fail_count_value.setObjectName("MetricBig")
        self.current_stage_value = QLabel("1/5")
        self.current_stage_value.setObjectName("MetricBig")

        metrics = QHBoxLayout()
        metrics.addWidget(self.metric_box("Raw files", self.raw_count_value))
        metrics.addWidget(self.metric_box("PASS", self.pass_count_value))
        metrics.addWidget(self.metric_box("FAIL", self.fail_count_value))
        metrics.addWidget(self.metric_box("Stage", self.current_stage_value))

        self.input_folder = QLineEdit()
        self.input_folder.setPlaceholderText("ยังไม่ได้เลือกโฟลเดอร์")
        self.input_folder.setReadOnly(True)

        self.choose_folder_button = QPushButton("1. Choose Folder")
        self.choose_folder_button.clicked.connect(self.choose_folder)

        self.clean_button = QPushButton("2. Clean All Files")
        self.clean_button.setObjectName("PrimaryButton")
        self.clean_button.clicked.connect(self.run_cleaner)
        self.clean_button.setEnabled(False)

        self.expected_rows = QSpinBox()
        self.expected_rows.setRange(1, 1000)
        self.expected_rows.setValue(10)
        self.expected_rows.setToolTip("ปกติ GPT1 สร้าง 10 rows ต่อ SKU เพื่อให้เลือก 5 rows ที่ดีที่สุด")

        self.allow_visual_concentration = QCheckBox("Allow visual concentration")
        self.allow_angle_concentration = QCheckBox("Allow angle concentration")
        self.allow_visual_concentration.setVisible(False)
        self.allow_angle_concentration.setVisible(False)

        self.advanced_toggle = QCheckBox("Show advanced validation options")
        self.advanced_toggle.toggled.connect(self.toggle_advanced)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)

        control_group = QGroupBox("Start here")
        control_layout = QGridLayout(control_group)
        control_layout.addWidget(QLabel("Folder"), 0, 0)
        control_layout.addWidget(self.input_folder, 0, 1)
        control_layout.addWidget(self.choose_folder_button, 0, 2)
        control_layout.addWidget(QLabel("Expected rows per file"), 1, 0)
        control_layout.addWidget(self.expected_rows, 1, 1)
        control_layout.addWidget(self.clean_button, 1, 2)
        control_layout.addWidget(self.advanced_toggle, 2, 1)
        control_layout.addWidget(self.allow_visual_concentration, 3, 1)
        control_layout.addWidget(self.allow_angle_concentration, 4, 1)
        control_layout.addWidget(self.progress_bar, 5, 0, 1, 3)

        self.results_table = QTableWidget(0, 5)
        self.results_table.setHorizontalHeaderLabels(["Status", "File", "Rows", "Next Action", "Details"])
        self.results_table.horizontalHeader().setStretchLastSection(True)
        self.results_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.results_table.itemSelectionChanged.connect(self.on_selection_changed)

        self.row_preview = QTextEdit()
        self.row_preview.setReadOnly(True)
        self.row_preview.setPlaceholderText("หลัง Clean ผ่าน โปรแกรมจะแสดง clean rows และเตรียม prompt สำหรับ GPT2 ให้")

        self.copy_first_row_button = QPushButton("3. Copy GPT2 Prompt from Selected PASS File")
        self.copy_first_row_button.setObjectName("SuccessButton")
        self.copy_first_row_button.clicked.connect(self.copy_first_row_prompt)
        self.copy_first_row_button.setEnabled(False)

        self.open_clean_button = QPushButton("Open Clean TSV")
        self.open_clean_button.clicked.connect(self.open_selected_clean_file)
        self.open_clean_button.setEnabled(False)

        self.open_report_button = QPushButton("Open Report")
        self.open_report_button.clicked.connect(self.open_selected_report_file)
        self.open_report_button.setEnabled(False)

        self.open_output_folder_button = QPushButton("Open _cleaned Folder")
        self.open_output_folder_button.clicked.connect(self.open_cleaned_folder)
        self.open_output_folder_button.setEnabled(False)

        self.reset_button = QPushButton("Reset")
        self.reset_button.setObjectName("DangerButton")
        self.reset_button.clicked.connect(self.reset_workflow)

        action_layout = QHBoxLayout()
        action_layout.addWidget(self.copy_first_row_button)
        action_layout.addWidget(self.open_clean_button)
        action_layout.addWidget(self.open_report_button)
        action_layout.addWidget(self.open_output_folder_button)
        action_layout.addStretch(1)
        action_layout.addWidget(self.reset_button)

        steps_layout = QHBoxLayout()
        for badge in self.step_badges:
            steps_layout.addWidget(badge)

        top = QVBoxLayout()
        top.addWidget(self.app_title)
        top.addWidget(self.app_subtitle)
        top.addLayout(steps_layout)
        top.addWidget(coach_card)
        top.addLayout(metrics)
        top.addWidget(control_group)

        central = QWidget()
        layout = QVBoxLayout(central)
        layout.addLayout(top)
        layout.addWidget(self.results_table, stretch=2)
        layout.addLayout(action_layout)
        layout.addWidget(self.row_preview, stretch=1)
        self.setCentralWidget(central)

        quit_action = QAction("Exit", self)
        quit_action.triggered.connect(self.close)
        self.menuBar().addAction(quit_action)

        self.set_stage(1)

    def metric_box(self, title: str, value_label: QLabel) -> QFrame:
        frame = QFrame()
        frame.setObjectName("CoachCard")
        layout = QVBoxLayout(frame)
        label = QLabel(title)
        label.setObjectName("MetricLabel")
        label.setAlignment(Qt.AlignCenter)
        value_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(value_label)
        layout.addWidget(label)
        return frame

    def set_stage(self, stage: int) -> None:
        self.current_stage_value.setText(f"{stage}/5")
        for index, badge in enumerate(self.step_badges, start=1):
            badge.set_active(index == stage)

    def set_coach(self, stage: int, title: str, text: str) -> None:
        self.set_stage(stage)
        self.coach_title.setText(title)
        self.coach_text.setText(text)

    def toggle_advanced(self, checked: bool) -> None:
        self.allow_visual_concentration.setVisible(checked)
        self.allow_angle_concentration.setVisible(checked)

    def choose_folder(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Choose folder containing GPT1 raw output files")
        if not folder:
            return

        folder_path = Path(folder)
        self.input_folder.setText(str(folder_path))
        self.results = []
        self.results_table.setRowCount(0)
        self.row_preview.clear()
        self.pass_count_value.setText("0")
        self.fail_count_value.setText("0")
        self.progress_bar.setValue(0)

        try:
            raw_files = discover_raw_files(folder_path)
        except Exception as exc:  # noqa: BLE001
            QMessageBox.critical(self, "Folder error", str(exc))
            return

        self.raw_count_value.setText(str(len(raw_files)))
        self.clean_button.setEnabled(len(raw_files) > 0)
        self.open_output_folder_button.setEnabled(False)
        self.copy_first_row_button.setEnabled(False)
        self.open_clean_button.setEnabled(False)
        self.open_report_button.setEnabled(False)

        if raw_files:
            self.set_coach(
                2,
                f"พบไฟล์ raw {len(raw_files)} ไฟล์ พร้อม clean แล้ว",
                "กดปุ่มใหญ่ 2. Clean All Files ได้เลย ค่า expected rows ใช้ 10 เป็นค่าเริ่มต้นสำหรับการสร้าง 10 ideas ต่อสินค้า",
            )
        else:
            self.set_coach(
                1,
                "ยังไม่พบไฟล์ raw ที่ใช้ได้",
                "ใส่ output จาก GPT1 เป็นไฟล์ .md หรือ .txt ในโฟลเดอร์นี้ก่อน แล้วเลือกโฟลเดอร์อีกครั้ง",
            )

    def run_cleaner(self) -> None:
        folder_text = self.input_folder.text().strip()
        if not folder_text:
            QMessageBox.warning(self, "Missing folder", "Choose a folder first.")
            return

        self.clean_button.setEnabled(False)
        self.choose_folder_button.setEnabled(False)
        self.results_table.setRowCount(0)
        self.row_preview.clear()
        self.progress_bar.setRange(0, 0)
        self.set_coach(
            2,
            "กำลัง clean และ validate ทุกไฟล์ในโฟลเดอร์",
            "รอสักครู่ โปรแกรมจะจัดการแทนทั้งหมด: extract rows, validate schema, สร้าง clean TSV และ report",
        )

        self.worker = CleanWorker(
            Path(folder_text),
            self.expected_rows.value(),
            self.allow_visual_concentration.isChecked(),
            self.allow_angle_concentration.isChecked(),
        )
        self.worker.finished_with_results.connect(self.on_clean_finished)
        self.worker.failed.connect(self.on_clean_failed)
        self.worker.start()

    def on_clean_failed(self, message: str) -> None:
        self.clean_button.setEnabled(True)
        self.choose_folder_button.setEnabled(True)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.set_coach(2, "Cleaner failed", "เปิดข้อความ error แล้วแก้ input ก่อนส่งต่อ GPT2")
        QMessageBox.critical(self, "Cleaner failed", message)

    def on_clean_finished(self, results: list[CleanResult]) -> None:
        self.clean_button.setEnabled(True)
        self.choose_folder_button.setEnabled(True)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(100)
        self.results = results
        self.results_table.setRowCount(len(results))

        for row_index, result in enumerate(results):
            next_action = "Copy GPT2 prompt" if result.status == "PASS" else "Open report and fix"
            details = str(result.clean_file if result.status == "PASS" else result.report_file)
            values = [
                result.status,
                result.raw_file.name,
                f"{result.extracted_rows}/{result.expected_rows}",
                next_action,
                details,
            ]
            for col, value in enumerate(values):
                item = QTableWidgetItem(value)
                if col == 0:
                    item.setTextAlignment(Qt.AlignCenter)
                self.results_table.setItem(row_index, col, item)

        self.results_table.resizeColumnsToContents()
        pass_count = sum(1 for result in results if result.status == "PASS")
        fail_count = len(results) - pass_count
        self.pass_count_value.setText(str(pass_count))
        self.fail_count_value.setText(str(fail_count))
        self.open_output_folder_button.setEnabled(bool(results))

        if not results:
            self.set_coach(1, "ไม่พบไฟล์ raw", "เพิ่มไฟล์ .md / .txt จาก GPT1 ในโฟลเดอร์ แล้วลองใหม่")
            QMessageBox.information(self, "No files", "No .md/.txt/.text raw files found in the selected folder.")
            return

        first_pass_row = next((index for index, result in enumerate(results) if result.status == "PASS"), None)
        if first_pass_row is not None:
            self.results_table.selectRow(first_pass_row)
            self.set_coach(
                4,
                f"Clean เสร็จแล้ว: PASS={pass_count}, FAIL={fail_count}",
                "เลือกไฟล์ที่ PASS แล้วกดปุ่ม 3 เพื่อ copy prompt สำหรับ GPT2 โปรแกรมจะใส่ MODE: TEMPLATE_HANDOFF ให้เอง",
            )
        else:
            self.set_coach(
                3,
                f"Clean เสร็จแล้วแต่ยังไม่มีไฟล์ PASS: FAIL={fail_count}",
                "อย่าส่งต่อ GPT2 ให้เปิด report ดูสาเหตุ แล้ว rerun GPT1 หรือแก้ raw file ก่อน",
            )

    def selected_result(self) -> CleanResult | None:
        selected = self.results_table.selectionModel().selectedRows()
        if not selected:
            return None
        row = selected[0].row()
        if row < 0 or row >= len(self.results):
            return None
        return self.results[row]

    def on_selection_changed(self) -> None:
        result = self.selected_result()
        if result is None:
            return

        self.open_report_button.setEnabled(True)
        self.open_clean_button.setEnabled(result.status == "PASS")
        self.copy_first_row_button.setEnabled(result.status == "PASS")

        if result.status != "PASS":
            self.row_preview.setPlainText(
                "ไฟล์นี้ยังไม่พร้อมส่ง GPT2\n\n"
                f"Raw file: {result.raw_file}\n"
                f"Report: {result.report_file}\n\n"
                "Next action: เปิด report แล้วแก้ input หรือ rerun GPT1"
            )
            self.set_coach(3, "ไฟล์นี้ FAIL", "อย่าส่งต่อ GPT2 ให้เปิด report ก่อน")
            return

        try:
            rows = read_clean_rows(result.clean_file)
            preview_rows = "\n".join(rows[:5])
            self.row_preview.setPlainText(
                "ไฟล์นี้ PASS และพร้อมส่ง GPT2\n\n"
                "Default next step:\n"
                "1. กด Copy GPT2 Prompt from Selected PASS File\n"
                "2. เปิด GPT2: BiiigBee Visual Prompt Refiner\n"
                "3. Paste แล้วส่ง\n"
                "4. ทำซ้ำกับอีก 4 rows ที่เลือก\n\n"
                f"Clean TSV: {result.clean_file}\n\n"
                f"Preview first 5 rows:\n{preview_rows}"
            )
            self.set_coach(4, "ไฟล์นี้ PASS", "กดปุ่ม 3 เพื่อ copy prompt สำหรับ GPT2 ได้ทันที")
        except Exception as exc:  # noqa: BLE001
            self.row_preview.setPlainText(f"Could not read clean TSV: {exc}")

    def copy_first_row_prompt(self) -> None:
        result = self.selected_result()
        if result is None:
            QMessageBox.warning(self, "No selection", "Select a PASS result first.")
            return
        if result.status != "PASS":
            QMessageBox.warning(self, "Not ready", "This result is not PASS. Do not send it to GPT2.")
            return
        rows = read_clean_rows(result.clean_file)
        if not rows:
            QMessageBox.warning(self, "No rows", "No clean rows found in this TSV.")
            return
        prompt = build_gpt2_template(rows[0])
        QGuiApplication.clipboard().setText(prompt)
        self.set_coach(
            4,
            "Copied: GPT2 prompt พร้อม paste แล้ว",
            "ไปที่ GPT2 แล้ว paste ได้เลย หลัง GPT2 ผ่านแล้วค่อยสร้างภาพและตรวจ human review",
        )
        QMessageBox.information(self, "Copied", "GPT2 TEMPLATE_HANDOFF prompt copied to clipboard.")

    def open_selected_clean_file(self) -> None:
        result = self.selected_result()
        if result:
            self.open_path(result.clean_file)

    def open_selected_report_file(self) -> None:
        result = self.selected_result()
        if result:
            self.open_path(result.report_file)

    def open_cleaned_folder(self) -> None:
        folder_text = self.input_folder.text().strip()
        if folder_text:
            self.open_path(Path(folder_text) / "_cleaned")

    def open_path(self, path: Path) -> None:
        if not path.exists():
            QMessageBox.warning(self, "Missing file", str(path))
            return
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(path)))

    def reset_workflow(self) -> None:
        self.input_folder.clear()
        self.results = []
        self.results_table.setRowCount(0)
        self.row_preview.clear()
        self.raw_count_value.setText("0")
        self.pass_count_value.setText("0")
        self.fail_count_value.setText("0")
        self.progress_bar.setValue(0)
        self.clean_button.setEnabled(False)
        self.copy_first_row_button.setEnabled(False)
        self.open_clean_button.setEnabled(False)
        self.open_report_button.setEnabled(False)
        self.open_output_folder_button.setEnabled(False)
        self.set_coach(
            1,
            "ตอนนี้ให้เลือกโฟลเดอร์ที่เก็บ raw output จาก GPT1",
            "โปรแกรมจะค้นหาไฟล์ .md / .txt / .text ในโฟลเดอร์นั้น แล้ว clean + validate ให้ทั้งหมด",
        )


def main() -> int:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
