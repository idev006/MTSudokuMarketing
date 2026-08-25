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
        PipelineBatchSummary,
        clean_folder,
        discover_raw_files,
        read_clean_rows,
        read_first_prompt,
    )
except ImportError:  # Allows direct file launch.
    from pipeline_service import (  # type: ignore
        CleanResult,
        PipelineBatchSummary,
        clean_folder,
        discover_raw_files,
        read_clean_rows,
        read_first_prompt,
    )


class CleanWorker(QThread):
    finished_with_summary = Signal(object)
    failed = Signal(str)

    def __init__(self, input_folder: Path, expected_rows: int, allow_visual: bool, allow_angle: bool) -> None:
        super().__init__()
        self.input_folder = input_folder
        self.expected_rows = expected_rows
        self.allow_visual = allow_visual
        self.allow_angle = allow_angle

    def run(self) -> None:
        try:
            summary = clean_folder(
                self.input_folder,
                expected_rows=self.expected_rows,
                allow_visual_concentration=self.allow_visual,
                allow_angle_concentration=self.allow_angle,
            )
            self.finished_with_summary.emit(summary)
        except Exception as exc:  # noqa: BLE001
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
        self.resize(1320, 860)
        self.results: list[CleanResult] = []
        self.summary: PipelineBatchSummary | None = None
        self.worker: CleanWorker | None = None
        self.selected_folder: Path | None = None

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
            QPushButton:disabled { color: #7c8797; background: #edf1f7; }
            QPushButton#PrimaryButton { background: #2563eb; color: #ffffff; font-size: 16px; font-weight: 700; border: 1px solid #1d4ed8; padding: 12px 18px; }
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
            StepBadge("2", "Clean + Validate ทุกไฟล์"),
            StepBadge("3", "Auto เลือก 5 rows + สร้าง prompt"),
            StepBadge("4", "Copy prompt ไป GPT2"),
            StepBadge("5", "สร้างภาพ + Human Review"),
        ]

        title = QLabel("BiiigBee Social Content Pipeline")
        title.setObjectName("AppTitle")
        subtitle = QLabel("Operator cockpit: โปรแกรมจัดการ workflow ระหว่าง GPT1 → Cleaner → GPT2 ให้มากที่สุด")
        subtitle.setObjectName("AppSubtitle")

        self.coach_title = QLabel("ตอนนี้ให้เลือกโฟลเดอร์ที่เก็บ raw output จาก GPT1")
        self.coach_title.setObjectName("CoachTitle")
        self.coach_text = QLabel("ใส่ไฟล์ .md / .txt / .text จาก GPT1 ไว้ในโฟลเดอร์เดียว แล้วกด Choose Folder")
        self.coach_text.setObjectName("CoachText")
        self.coach_text.setWordWrap(True)
        coach_card = QFrame()
        coach_card.setObjectName("CoachCard")
        coach_layout = QVBoxLayout(coach_card)
        coach_layout.addWidget(self.coach_title)
        coach_layout.addWidget(self.coach_text)

        self.raw_count = self.metric_value("0")
        self.pass_count = self.metric_value("0")
        self.fail_count = self.metric_value("0")
        self.selected_count = self.metric_value("0")
        self.prompt_count = self.metric_value("0")
        metrics = QHBoxLayout()
        metrics.addWidget(self.metric_box("Raw files", self.raw_count))
        metrics.addWidget(self.metric_box("PASS", self.pass_count))
        metrics.addWidget(self.metric_box("FAIL", self.fail_count))
        metrics.addWidget(self.metric_box("Selected rows", self.selected_count))
        metrics.addWidget(self.metric_box("GPT2 prompts", self.prompt_count))

        self.input_folder = QLineEdit()
        self.input_folder.setReadOnly(True)
        self.input_folder.setPlaceholderText("ยังไม่ได้เลือกโฟลเดอร์")
        self.choose_folder_button = QPushButton("1. Choose Folder")
        self.choose_folder_button.clicked.connect(self.choose_folder)
        self.clean_button = QPushButton("2. Clean All Files + Prepare GPT2 Prompts")
        self.clean_button.setObjectName("PrimaryButton")
        self.clean_button.clicked.connect(self.run_cleaner)
        self.clean_button.setEnabled(False)
        self.expected_rows = QSpinBox()
        self.expected_rows.setRange(1, 1000)
        self.expected_rows.setValue(10)
        self.advanced_toggle = QCheckBox("Show advanced validation options")
        self.allow_visual = QCheckBox("Allow visual concentration")
        self.allow_angle = QCheckBox("Allow angle concentration")
        self.allow_visual.setVisible(False)
        self.allow_angle.setVisible(False)
        self.advanced_toggle.toggled.connect(self.toggle_advanced)
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)

        start_group = QGroupBox("Start here")
        start_layout = QGridLayout(start_group)
        start_layout.addWidget(QLabel("Folder"), 0, 0)
        start_layout.addWidget(self.input_folder, 0, 1)
        start_layout.addWidget(self.choose_folder_button, 0, 2)
        start_layout.addWidget(QLabel("Expected rows per file"), 1, 0)
        start_layout.addWidget(self.expected_rows, 1, 1)
        start_layout.addWidget(self.clean_button, 1, 2)
        start_layout.addWidget(self.advanced_toggle, 2, 1)
        start_layout.addWidget(self.allow_visual, 3, 1)
        start_layout.addWidget(self.allow_angle, 4, 1)
        start_layout.addWidget(self.progress, 5, 0, 1, 3)

        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(["Status", "File", "Rows", "Selected", "Prompts", "Next Action"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.itemSelectionChanged.connect(self.on_selection_changed)

        self.preview = QTextEdit()
        self.preview.setReadOnly(True)
        self.preview.setPlaceholderText("โปรแกรมจะแสดง 5 selected rows และ prompt แรกสำหรับ GPT2 ที่นี่")

        self.copy_prompt_button = QPushButton("3. Copy First GPT2 Prompt")
        self.copy_prompt_button.setObjectName("SuccessButton")
        self.copy_prompt_button.clicked.connect(self.copy_first_prompt)
        self.copy_prompt_button.setEnabled(False)
        self.open_selected_button = QPushButton("Open Selected 5 Rows")
        self.open_selected_button.clicked.connect(self.open_selected_file)
        self.open_selected_button.setEnabled(False)
        self.open_prompts_button = QPushButton("Open GPT2 Prompts Folder")
        self.open_prompts_button.clicked.connect(self.open_prompt_folder)
        self.open_prompts_button.setEnabled(False)
        self.open_clean_button = QPushButton("Open Clean TSV")
        self.open_clean_button.clicked.connect(self.open_clean_file)
        self.open_clean_button.setEnabled(False)
        self.open_report_button = QPushButton("Open Report")
        self.open_report_button.clicked.connect(self.open_report_file)
        self.open_report_button.setEnabled(False)
        self.open_output_button = QPushButton("Open _cleaned Folder")
        self.open_output_button.clicked.connect(self.open_output_folder)
        self.open_output_button.setEnabled(False)
        self.reset_button = QPushButton("Reset")
        self.reset_button.setObjectName("DangerButton")
        self.reset_button.clicked.connect(self.reset_workflow)

        action_layout = QHBoxLayout()
        action_layout.addWidget(self.copy_prompt_button)
        action_layout.addWidget(self.open_selected_button)
        action_layout.addWidget(self.open_prompts_button)
        action_layout.addWidget(self.open_clean_button)
        action_layout.addWidget(self.open_report_button)
        action_layout.addWidget(self.open_output_button)
        action_layout.addStretch(1)
        action_layout.addWidget(self.reset_button)

        steps = QHBoxLayout()
        for badge in self.step_badges:
            steps.addWidget(badge)

        central = QWidget()
        layout = QVBoxLayout(central)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addLayout(steps)
        layout.addWidget(coach_card)
        layout.addLayout(metrics)
        layout.addWidget(start_group)
        layout.addWidget(self.table, stretch=2)
        layout.addLayout(action_layout)
        layout.addWidget(self.preview, stretch=1)
        self.setCentralWidget(central)

        quit_action = QAction("Exit", self)
        quit_action.triggered.connect(self.close)
        self.menuBar().addAction(quit_action)
        self.set_stage(1)

    def metric_value(self, text: str) -> QLabel:
        label = QLabel(text)
        label.setObjectName("MetricBig")
        label.setAlignment(Qt.AlignCenter)
        return label

    def metric_box(self, title: str, value: QLabel) -> QFrame:
        frame = QFrame()
        frame.setObjectName("CoachCard")
        layout = QVBoxLayout(frame)
        label = QLabel(title)
        label.setObjectName("MetricLabel")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(value)
        layout.addWidget(label)
        return frame

    def set_stage(self, stage: int) -> None:
        for index, badge in enumerate(self.step_badges, start=1):
            badge.set_active(index == stage)

    def set_coach(self, stage: int, title: str, text: str) -> None:
        self.set_stage(stage)
        self.coach_title.setText(title)
        self.coach_text.setText(text)

    def toggle_advanced(self, checked: bool) -> None:
        self.allow_visual.setVisible(checked)
        self.allow_angle.setVisible(checked)

    def choose_folder(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Choose folder containing GPT1 raw output files")
        if not folder:
            return
        self.selected_folder = Path(folder)
        self.input_folder.setText(str(self.selected_folder))
        self.results = []
        self.summary = None
        self.table.setRowCount(0)
        self.preview.clear()
        self.pass_count.setText("0")
        self.fail_count.setText("0")
        self.selected_count.setText("0")
        self.prompt_count.setText("0")
        self.progress.setValue(0)

        try:
            raw_files = discover_raw_files(self.selected_folder)
        except Exception as exc:  # noqa: BLE001
            QMessageBox.critical(self, "Folder error", str(exc))
            return

        self.raw_count.setText(str(len(raw_files)))
        self.clean_button.setEnabled(len(raw_files) > 0)
        self.copy_prompt_button.setEnabled(False)
        self.open_selected_button.setEnabled(False)
        self.open_prompts_button.setEnabled(False)
        self.open_clean_button.setEnabled(False)
        self.open_report_button.setEnabled(False)
        self.open_output_button.setEnabled(False)

        if raw_files:
            self.set_coach(
                2,
                f"พบไฟล์ raw {len(raw_files)} ไฟล์ พร้อมให้โปรแกรมจัดการแล้ว",
                "กดปุ่ม 2. Clean All Files + Prepare GPT2 Prompts โปรแกรมจะ clean, validate, เลือก 5 rows และสร้าง prompt สำหรับ GPT2 ให้เอง",
            )
        else:
            self.set_coach(1, "ยังไม่พบไฟล์ raw", "นำ output จาก GPT1 ไป save เป็น .md หรือ .txt ในโฟลเดอร์นี้ แล้วเลือกโฟลเดอร์อีกครั้ง")

    def run_cleaner(self) -> None:
        if self.selected_folder is None:
            QMessageBox.warning(self, "Missing folder", "Choose a folder first.")
            return
        self.clean_button.setEnabled(False)
        self.table.setRowCount(0)
        self.preview.clear()
        self.progress.setRange(0, 0)
        self.set_coach(2, "กำลัง clean และเตรียม handoff", "โปรแกรมกำลังจัดการไฟล์ทั้งหมด: clean → validate → select 5 rows → generate GPT2 prompts")

        self.worker = CleanWorker(
            self.selected_folder,
            self.expected_rows.value(),
            self.allow_visual.isChecked(),
            self.allow_angle.isChecked(),
        )
        self.worker.finished_with_summary.connect(self.on_clean_finished)
        self.worker.failed.connect(self.on_clean_failed)
        self.worker.start()

    def on_clean_failed(self, message: str) -> None:
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.clean_button.setEnabled(True)
        self.set_coach(2, "Cleaner failed", "เปิดรายละเอียด error แล้วแก้ input ก่อนรันใหม่")
        QMessageBox.critical(self, "Cleaner failed", message)

    def on_clean_finished(self, summary: PipelineBatchSummary) -> None:
        self.progress.setRange(0, 100)
        self.progress.setValue(100)
        self.clean_button.setEnabled(True)
        self.summary = summary
        self.results = summary.results
        self.raw_count.setText(str(summary.raw_file_count))
        self.pass_count.setText(str(summary.pass_count))
        self.fail_count.setText(str(summary.fail_count))
        self.selected_count.setText(str(summary.selected_row_count))
        self.prompt_count.setText(str(summary.prompt_file_count))
        self.open_output_button.setEnabled(True)

        self.table.setRowCount(len(self.results))
        for row_index, result in enumerate(self.results):
            values = [
                result.status,
                result.raw_file.name,
                f"{result.extracted_rows}/{result.expected_rows}",
                str(result.selected_rows),
                str(result.prompt_files),
                result.next_action,
            ]
            for col, value in enumerate(values):
                item = QTableWidgetItem(value)
                if col in {0, 2, 3, 4}:
                    item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_index, col, item)
        self.table.resizeColumnsToContents()

        if summary.pass_count > 0:
            first_pass_index = next(index for index, result in enumerate(self.results) if result.status == "PASS")
            self.table.selectRow(first_pass_index)
            self.set_coach(
                4,
                f"เสร็จแล้ว: PASS={summary.pass_count}, FAIL={summary.fail_count}",
                "โปรแกรมเลือกไฟล์ PASS แรกให้แล้ว และสร้าง selected 5 rows + GPT2 prompts ไว้ใน _cleaned แล้ว กด Copy First GPT2 Prompt เพื่อส่งเข้า GPT2",
            )
        elif self.results:
            self.set_coach(3, "ยังไม่มีไฟล์ที่ PASS", "เปิด Report ของไฟล์ FAIL เพื่อดูสาเหตุ แล้วแก้ raw input หรือ rerun GPT1")
        else:
            self.set_coach(1, "ไม่พบไฟล์ raw", "เพิ่มไฟล์ .md หรือ .txt จาก GPT1 ก่อน")

    def selected_result(self) -> CleanResult | None:
        selected = self.table.selectionModel().selectedRows()
        if not selected:
            return None
        index = selected[0].row()
        if index < 0 or index >= len(self.results):
            return None
        return self.results[index]

    def on_selection_changed(self) -> None:
        result = self.selected_result()
        if result is None:
            return
        is_pass = result.status == "PASS"
        self.copy_prompt_button.setEnabled(is_pass and result.prompt_folder is not None)
        self.open_selected_button.setEnabled(is_pass and result.selected_file is not None)
        self.open_prompts_button.setEnabled(is_pass and result.prompt_folder is not None)
        self.open_clean_button.setEnabled(result.clean_file.exists())
        self.open_report_button.setEnabled(result.report_file.exists())

        if not is_pass:
            self.preview.setPlainText("ไฟล์นี้ FAIL: อย่าส่งเข้า GPT2 ให้กด Open Report ก่อน")
            self.set_coach(3, "ไฟล์นี้ยังไปต่อไม่ได้", "เปิด Report เพื่อดูสาเหตุ ห้าม copy raw หรือ clean file ที่ FAIL ไป GPT2")
            return

        selected_lines = []
        if result.selected_file and result.selected_file.exists():
            selected_lines = read_clean_rows(result.selected_file)
        first_prompt = read_first_prompt(result.prompt_folder)
        preview = "Selected 5 rows ready for GPT2:\n\n" + "\n".join(selected_lines)
        preview += "\n\n--- First GPT2 prompt preview ---\n" + first_prompt[:2500]
        self.preview.setPlainText(preview)
        self.set_coach(4, "ไฟล์นี้พร้อมส่ง GPT2", "โปรแกรมเลือก 5 rows และสร้าง prompt ให้แล้ว กด Copy First GPT2 Prompt แล้ววางใน GPT2 Visual Prompt Refiner")

    def copy_first_prompt(self) -> None:
        result = self.selected_result()
        if result is None or result.status != "PASS":
            QMessageBox.warning(self, "Not ready", "Select a PASS file first.")
            return
        prompt = read_first_prompt(result.prompt_folder)
        if not prompt:
            QMessageBox.warning(self, "No prompt", "No GPT2 prompt found for this file.")
            return
        QGuiApplication.clipboard().setText(prompt)
        self.set_coach(5, "คัดลอก prompt แล้ว", "เปิด GPT2 Visual Prompt Refiner แล้ว paste prompt นี้ เมื่อ GPT2 ส่งผลกลับมา ใช้ image prompt ไปสร้างภาพและตรวจงานก่อนโพสต์")
        QMessageBox.information(self, "Copied", "First GPT2 prompt copied to clipboard.")

    def open_path(self, path: Path | None) -> None:
        if path is None or not path.exists():
            QMessageBox.warning(self, "Missing file", str(path or ""))
            return
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(path)))

    def open_selected_file(self) -> None:
        result = self.selected_result()
        self.open_path(result.selected_file if result else None)

    def open_prompt_folder(self) -> None:
        result = self.selected_result()
        self.open_path(result.prompt_folder if result else None)

    def open_clean_file(self) -> None:
        result = self.selected_result()
        self.open_path(result.clean_file if result else None)

    def open_report_file(self) -> None:
        result = self.selected_result()
        self.open_path(result.report_file if result else None)

    def open_output_folder(self) -> None:
        if self.summary:
            self.open_path(self.summary.output_root)
        elif self.selected_folder:
            self.open_path(self.selected_folder / "_cleaned")

    def reset_workflow(self) -> None:
        self.selected_folder = None
        self.summary = None
        self.results = []
        self.input_folder.clear()
        self.table.setRowCount(0)
        self.preview.clear()
        self.raw_count.setText("0")
        self.pass_count.setText("0")
        self.fail_count.setText("0")
        self.selected_count.setText("0")
        self.prompt_count.setText("0")
        self.progress.setValue(0)
        self.clean_button.setEnabled(False)
        self.copy_prompt_button.setEnabled(False)
        self.open_selected_button.setEnabled(False)
        self.open_prompts_button.setEnabled(False)
        self.open_clean_button.setEnabled(False)
        self.open_report_button.setEnabled(False)
        self.open_output_button.setEnabled(False)
        self.set_coach(1, "ตอนนี้ให้เลือกโฟลเดอร์ที่เก็บ raw output จาก GPT1", "ใส่ไฟล์ .md / .txt / .text จาก GPT1 ไว้ในโฟลเดอร์เดียว แล้วกด Choose Folder")


def main() -> int:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
