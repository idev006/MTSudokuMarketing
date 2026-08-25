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
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSpinBox,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

try:
    from .pipeline_service import (
        DEFAULT_POST_COUNT,
        MAX_POST_COUNT,
        MIN_POST_COUNT,
        CleanResult,
        PipelineBatchSummary,
        clean_folder,
        discover_raw_files,
        read_clean_rows,
        read_first_prompt,
    )
except ImportError:  # Allows direct file launch.
    from pipeline_service import (  # type: ignore
        DEFAULT_POST_COUNT,
        MAX_POST_COUNT,
        MIN_POST_COUNT,
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

    def __init__(self, input_folder: Path, post_count: int, allow_visual: bool, allow_angle: bool) -> None:
        super().__init__()
        self.input_folder = input_folder
        self.post_count = post_count
        self.allow_visual = allow_visual
        self.allow_angle = allow_angle

    def run(self) -> None:
        try:
            summary = clean_folder(
                self.input_folder,
                expected_rows=self.post_count,
                target_posts=self.post_count,
                allow_visual_concentration=self.allow_visual,
                allow_angle_concentration=self.allow_angle,
            )
            self.finished_with_summary.emit(summary)
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
        self.resize(1360, 860)
        self.results: list[CleanResult] = []
        self.summary: PipelineBatchSummary | None = None
        self.worker: CleanWorker | None = None
        self.selected_folder: Path | None = None

        self.setStyleSheet(
            """
            QMainWindow { background: #f6f8fb; }
            QLabel#AppTitle { font-size: 24px; font-weight: 700; color: #172033; }
            QLabel#AppSubtitle { font-size: 13px; color: #556070; }
            QLabel#PanelTitle { font-size: 17px; font-weight: 700; color: #14315c; }
            QLabel#PanelHelp { font-size: 13px; color: #394a62; }
            QLabel#CoachTitle { font-size: 18px; font-weight: 700; color: #14315c; }
            QLabel#CoachText { font-size: 14px; color: #26364d; }
            QLabel#MetricBig { font-size: 22px; font-weight: 700; color: #14315c; }
            QLabel#MetricLabel { font-size: 12px; color: #5f6f86; }
            QFrame#Panel, QFrame#CoachCard { background: #ffffff; border: 1px solid #dbe3ef; border-radius: 12px; }
            QFrame#StepBadge { background: #eef3fb; border: 1px solid #d5dfef; border-radius: 10px; }
            QFrame#StepBadge[active="true"] { background: #dff0ff; border: 2px solid #3b82f6; }
            QLabel#StepNumber { font-size: 18px; font-weight: 700; color: #1d4ed8; min-width: 26px; }
            QLabel#StepTitle { font-size: 13px; color: #26364d; }
            QPushButton { padding: 9px 14px; border-radius: 8px; background: #e7edf7; color: #172033; border: 1px solid #cbd6e7; }
            QPushButton:hover { background: #dbe7f7; }
            QPushButton:disabled { color: #64748b; background: #edf1f7; }
            QPushButton#PrimaryButton { background: #2563eb; color: #ffffff; font-size: 15px; font-weight: 700; border: 1px solid #1d4ed8; padding: 12px 18px; }
            QPushButton#SuccessButton { background: #059669; color: #ffffff; font-weight: 700; border: 1px solid #047857; }
            QPushButton#DangerButton { background: #fee2e2; color: #991b1b; border: 1px solid #fecaca; }
            QTableWidget { background: #ffffff; color: #172033; border: 1px solid #dbe3ef; border-radius: 8px; gridline-color: #edf2f7; }
            QTableWidget::item { padding: 4px; }
            QTextEdit { background: #ffffff; color: #172033; selection-background-color: #bfdbfe; selection-color: #0f172a; border: 1px solid #dbe3ef; border-radius: 8px; padding: 8px; }
            QLineEdit { background: #ffffff; color: #172033; selection-background-color: #bfdbfe; selection-color: #0f172a; padding: 7px; border: 1px solid #94a3b8; border-radius: 7px; }
            QLineEdit:disabled { background: #f1f5f9; color: #475569; }
            QSpinBox { background: #ffffff; color: #172033; selection-background-color: #bfdbfe; selection-color: #0f172a; padding: 7px 28px 7px 8px; border: 1px solid #94a3b8; border-radius: 7px; min-height: 28px; }
            QSpinBox::up-button { subcontrol-origin: border; subcontrol-position: top right; width: 22px; border-left: 1px solid #94a3b8; border-bottom: 1px solid #cbd5e1; background: #e2e8f0; border-top-right-radius: 7px; }
            QSpinBox::down-button { subcontrol-origin: border; subcontrol-position: bottom right; width: 22px; border-left: 1px solid #94a3b8; background: #e2e8f0; border-bottom-right-radius: 7px; }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover { background: #cbd5e1; }
            QSpinBox::up-arrow { image: none; width: 0; height: 0; border-left: 5px solid transparent; border-right: 5px solid transparent; border-bottom: 7px solid #0f172a; }
            QSpinBox::down-arrow { image: none; width: 0; height: 0; border-left: 5px solid transparent; border-right: 5px solid transparent; border-top: 7px solid #0f172a; }
            QSplitter::handle { background: #d7e1f0; }
            QSplitter::handle:hover { background: #9db7dc; }
            """
        )

        self.step_badges = [
            StepBadge("1", "ตั้งค่า N + GPT1"),
            StepBadge("2", "เลือกโฟลเดอร์ raw"),
            StepBadge("3", "Clean + Validate"),
            StepBadge("4", "เตรียม prompts"),
            StepBadge("5", "GPT2 + Review"),
        ]

        self.coach_title = QLabel("ตั้งจำนวนรายการ N แล้วเริ่มจาก GPT1")
        self.coach_title.setObjectName("CoachTitle")
        self.coach_text = QLabel("ใช้ prompt skeleton ด้านซ้ายใน GPT1 ก่อน จากนั้น save output เป็น .md หรือ .txt แล้วเลือกโฟลเดอร์ raw")
        self.coach_text.setObjectName("CoachText")
        self.coach_text.setWordWrap(True)

        self.raw_count = self.metric_value("0")
        self.pass_count = self.metric_value("0")
        self.fail_count = self.metric_value("0")
        self.selected_count = self.metric_value("0")
        self.prompt_count = self.metric_value("0")

        self.post_count = QSpinBox()
        self.post_count.setRange(MIN_POST_COUNT, MAX_POST_COUNT)
        self.post_count.setValue(DEFAULT_POST_COUNT)
        self.post_count.setToolTip("จำนวนรายการต่อไฟล์/SKU: 1 ถึง 60. ให้ GPT1 ใช้ NUMBER_OF_ROWS=N เดียวกัน")
        self.post_count.valueChanged.connect(self.on_post_count_changed)

        self.gpt1_prompt_preview = QTextEdit()
        self.gpt1_prompt_preview.setReadOnly(True)
        self.gpt1_prompt_preview.setMinimumHeight(96)
        self.update_gpt1_prompt_preview()

        self.input_folder = QLineEdit()
        self.input_folder.setReadOnly(True)
        self.input_folder.setPlaceholderText("ยังไม่ได้เลือกโฟลเดอร์")

        self.choose_folder_button = QPushButton("1. Choose Folder")
        self.choose_folder_button.clicked.connect(self.choose_folder)

        self.clean_button = QPushButton("2. Clean All Files + Prepare N GPT2 Prompts")
        self.clean_button.setObjectName("PrimaryButton")
        self.clean_button.clicked.connect(self.run_cleaner)
        self.clean_button.setEnabled(False)

        self.advanced_toggle = QCheckBox("Show advanced validation options")
        self.allow_visual = QCheckBox("Allow visual concentration")
        self.allow_angle = QCheckBox("Allow angle concentration")
        self.allow_visual.setVisible(False)
        self.allow_angle.setVisible(False)
        self.advanced_toggle.toggled.connect(self.toggle_advanced)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)

        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(["Status", "File", "Rows", "Selected", "Prompts", "Next Action"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.itemSelectionChanged.connect(self.on_selection_changed)

        self.preview = QTextEdit()
        self.preview.setReadOnly(True)
        self.preview.setPlaceholderText("หลัง PASS โปรแกรมจะแสดง selected rows และ prompt แรกสำหรับ GPT2 ที่นี่")

        self.copy_prompt_button = QPushButton("3. Copy First GPT2 Prompt")
        self.copy_prompt_button.setObjectName("SuccessButton")
        self.copy_prompt_button.clicked.connect(self.copy_first_prompt)
        self.copy_prompt_button.setEnabled(False)

        self.open_selected_button = QPushButton("Open Selected N Rows")
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

        self.setCentralWidget(self.build_ui())

        quit_action = QAction("Exit", self)
        quit_action.triggered.connect(self.close)
        self.menuBar().addAction(quit_action)
        self.set_stage(1)

    def build_ui(self) -> QWidget:
        root = QWidget()
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(8, 8, 8, 8)
        root_layout.setSpacing(8)

        title = QLabel("BiiigBee Social Content Pipeline")
        title.setObjectName("AppTitle")
        subtitle = QLabel("Document-driven operator cockpit: GPT1 raw files → clean TSV → N GPT2 prompts, where 1 <= N <= 60")
        subtitle.setObjectName("AppSubtitle")
        root_layout.addWidget(title)
        root_layout.addWidget(subtitle)

        steps = QHBoxLayout()
        for badge in self.step_badges:
            steps.addWidget(badge)
        root_layout.addLayout(steps)

        main_splitter = QSplitter(Qt.Vertical)
        main_splitter.setChildrenCollapsible(False)
        main_splitter.addWidget(self.build_top_splitter())
        main_splitter.addWidget(self.build_results_panel())
        main_splitter.addWidget(self.build_preview_panel())
        main_splitter.setSizes([300, 260, 260])
        root_layout.addWidget(main_splitter, stretch=1)
        return root

    def build_top_splitter(self) -> QSplitter:
        top_splitter = QSplitter(Qt.Horizontal)
        top_splitter.setChildrenCollapsible(False)
        top_splitter.addWidget(self.wrap_scroll(self.build_setup_panel()))
        top_splitter.addWidget(self.wrap_scroll(self.build_status_panel()))
        top_splitter.setSizes([520, 760])
        return top_splitter

    def build_setup_panel(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("Panel")
        layout = QVBoxLayout(panel)
        layout.setSpacing(10)

        title = QLabel("1. Setup")
        title.setObjectName("PanelTitle")
        help_text = QLabel("ตั้งค่า N ให้ตรงกับ GPT1 แล้วเลือกโฟลเดอร์ที่เก็บ raw output")
        help_text.setObjectName("PanelHelp")
        help_text.setWordWrap(True)
        layout.addWidget(title)
        layout.addWidget(help_text)

        form = QGridLayout()
        form.addWidget(QLabel("Post count N"), 0, 0)
        form.addWidget(self.post_count, 0, 1)
        form.addWidget(QLabel("GPT1 prompt skeleton"), 1, 0)
        form.addWidget(self.gpt1_prompt_preview, 1, 1, 1, 2)
        form.addWidget(QLabel("Raw folder"), 2, 0)
        form.addWidget(self.input_folder, 2, 1)
        form.addWidget(self.choose_folder_button, 2, 2)
        form.addWidget(self.clean_button, 3, 1, 1, 2)
        form.addWidget(self.advanced_toggle, 4, 1, 1, 2)
        form.addWidget(self.allow_visual, 5, 1, 1, 2)
        form.addWidget(self.allow_angle, 6, 1, 1, 2)
        form.addWidget(self.progress, 7, 0, 1, 3)
        layout.addLayout(form)
        layout.addStretch(1)
        return panel

    def build_status_panel(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("Panel")
        layout = QVBoxLayout(panel)
        layout.setSpacing(10)

        title = QLabel("2. Workflow coach")
        title.setObjectName("PanelTitle")
        layout.addWidget(title)

        coach_card = QFrame()
        coach_card.setObjectName("CoachCard")
        coach_layout = QVBoxLayout(coach_card)
        coach_layout.addWidget(self.coach_title)
        coach_layout.addWidget(self.coach_text)
        layout.addWidget(coach_card)

        metrics = QHBoxLayout()
        metrics.addWidget(self.metric_box("Raw files", self.raw_count))
        metrics.addWidget(self.metric_box("PASS", self.pass_count))
        metrics.addWidget(self.metric_box("FAIL", self.fail_count))
        metrics.addWidget(self.metric_box("Selected rows", self.selected_count))
        metrics.addWidget(self.metric_box("GPT2 prompts", self.prompt_count))
        layout.addLayout(metrics)

        guide = QLabel(
            "Safe rule: raw GPT1 output is evidence only. Only PASS clean TSV and generated prompt files should go to GPT2. Human review remains required before publishing."
        )
        guide.setObjectName("PanelHelp")
        guide.setWordWrap(True)
        layout.addWidget(guide)
        layout.addStretch(1)
        return panel

    def build_results_panel(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("Panel")
        layout = QVBoxLayout(panel)
        row = QHBoxLayout()
        title = QLabel("3. Batch results")
        title.setObjectName("PanelTitle")
        row.addWidget(title)
        row.addStretch(1)
        layout.addLayout(row)
        layout.addWidget(self.table, stretch=1)
        return panel

    def build_preview_panel(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("Panel")
        layout = QVBoxLayout(panel)
        title = QLabel("4. Selected output and next action")
        title.setObjectName("PanelTitle")
        layout.addWidget(title)

        action_layout = QHBoxLayout()
        action_layout.addWidget(self.copy_prompt_button)
        action_layout.addWidget(self.open_selected_button)
        action_layout.addWidget(self.open_prompts_button)
        action_layout.addWidget(self.open_clean_button)
        action_layout.addWidget(self.open_report_button)
        action_layout.addWidget(self.open_output_button)
        action_layout.addStretch(1)
        action_layout.addWidget(self.reset_button)
        layout.addLayout(action_layout)
        layout.addWidget(self.preview, stretch=1)
        return panel

    def wrap_scroll(self, widget: QWidget) -> QScrollArea:
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setWidget(widget)
        scroll.setMinimumWidth(360)
        return scroll

    def metric_value(self, text: str) -> QLabel:
        label = QLabel(text)
        label.setObjectName("MetricBig")
        label.setAlignment(Qt.AlignCenter)
        return label

    def metric_box(self, title: str, value: QLabel) -> QFrame:
        frame = QFrame()
        frame.setObjectName("CoachCard")
        frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
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

    def update_gpt1_prompt_preview(self) -> None:
        n = self.post_count.value()
        self.gpt1_prompt_preview.setPlainText(
            f"SKU: <SKU>\nNUMBER_OF_ROWS: {n}\nPLATFORM: AUTO\nCAMPAIGN_GOAL: AUTO"
        )

    def on_post_count_changed(self) -> None:
        self.update_gpt1_prompt_preview()
        self.set_coach(
            1,
            f"ตั้งค่า N = {self.post_count.value()} แล้ว",
            f"ให้ใช้ NUMBER_OF_ROWS={self.post_count.value()} ใน GPT1 ก่อน จากนั้น save output เป็น .md หรือ .txt แล้วเลือกโฟลเดอร์",
        )

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
        self.set_action_buttons(False)

        if raw_files:
            n = self.post_count.value()
            self.set_coach(
                2,
                f"พบไฟล์ raw {len(raw_files)} ไฟล์ พร้อมให้โปรแกรมจัดการแล้ว",
                f"กดปุ่ม 2. Clean All Files + Prepare N GPT2 Prompts โปรแกรมจะตรวจ expected rows = {n} และสร้าง prompt ตาม N",
            )
        else:
            self.set_coach(
                1,
                "ยังไม่พบไฟล์ raw",
                "นำ output จาก GPT1 ไป save เป็น .md หรือ .txt ในโฟลเดอร์นี้ แล้วเลือกโฟลเดอร์อีกครั้ง",
            )

    def run_cleaner(self) -> None:
        if self.selected_folder is None:
            QMessageBox.warning(self, "Missing folder", "Choose a folder first.")
            return
        self.clean_button.setEnabled(False)
        self.table.setRowCount(0)
        self.preview.clear()
        self.progress.setValue(10)
        self.set_action_buttons(False)
        n = self.post_count.value()
        self.set_coach(3, "กำลัง clean และ validate ทุกไฟล์", f"โปรแกรมกำลังเตรียม clean TSV และ N={n} GPT2 prompts ต่อไฟล์ที่ PASS")

        self.worker = CleanWorker(self.selected_folder, n, self.allow_visual.isChecked(), self.allow_angle.isChecked())
        self.worker.finished_with_summary.connect(self.on_clean_finished)
        self.worker.failed.connect(self.on_clean_failed)
        self.worker.start()

    def on_clean_failed(self, message: str) -> None:
        self.clean_button.setEnabled(True)
        self.progress.setValue(0)
        self.set_coach(2, "Cleaner failed", "เปิดรายละเอียด error แล้วแก้ input หรือส่ง error กลับมาตรวจ")
        QMessageBox.critical(self, "Cleaner failed", message)

    def on_clean_finished(self, summary: PipelineBatchSummary) -> None:
        self.clean_button.setEnabled(True)
        self.summary = summary
        self.results = list(summary.results)
        self.progress.setValue(100)
        self.open_output_button.setEnabled(True)

        self.pass_count.setText(str(summary.pass_count))
        self.fail_count.setText(str(summary.fail_count))
        self.selected_count.setText(str(summary.selected_row_count))
        self.prompt_count.setText(str(summary.prompt_file_count))
        self.raw_count.setText(str(summary.raw_file_count))

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
        self.table.resizeRowsToContents()

        first_pass_index = next((i for i, result in enumerate(self.results) if result.status == "PASS"), None)
        if first_pass_index is not None:
            self.table.selectRow(first_pass_index)
            self.set_coach(
                4,
                "เตรียม GPT2 prompts เสร็จแล้ว",
                "เลือกไฟล์ PASS แล้วกด Copy First GPT2 Prompt หรือเปิด GPT2 Prompts Folder เพื่อใช้ prompt ทีละไฟล์",
            )
        elif self.results:
            self.set_coach(3, "ยังไม่มีไฟล์ PASS", "เปิด report ของแต่ละไฟล์ที่ FAIL แล้วแก้ raw GPT1 output ก่อนส่งเข้า GPT2")
        else:
            self.set_coach(1, "ไม่พบไฟล์ raw", "เพิ่มไฟล์ .md หรือ .txt จาก GPT1 แล้วเลือกโฟลเดอร์อีกครั้ง")
            QMessageBox.information(self, "No files", "No .md/.txt/.text raw files found in the selected folder.")

    def selected_result(self) -> CleanResult | None:
        selected = self.table.selectionModel().selectedRows()
        if not selected:
            return None
        row = selected[0].row()
        if row < 0 or row >= len(self.results):
            return None
        return self.results[row]

    def on_selection_changed(self) -> None:
        result = self.selected_result()
        if result is None:
            self.set_action_buttons(False)
            return

        if result.status != "PASS":
            self.set_action_buttons(False)
            self.open_report_button.setEnabled(True)
            self.open_output_button.setEnabled(self.summary is not None)
            self.preview.setPlainText("This file failed validation. Open the report before using GPT2.")
            self.set_coach(3, "ไฟล์นี้ยังไม่ผ่าน", "อย่าส่งไฟล์นี้เข้า GPT2 ให้เปิด report แล้วแก้ก่อน")
            return

        self.set_action_buttons(True)
        try:
            selected_rows = read_clean_rows(result.selected_file) if result.selected_file else []
            first_prompt = read_first_prompt(result.prompt_folder)
            preview_text = "Selected rows ready for GPT2:\n\n" + "\n".join(selected_rows[: min(10, len(selected_rows))])
            if len(selected_rows) > 10:
                preview_text += f"\n\n... {len(selected_rows) - 10} more selected rows"
            if first_prompt:
                preview_text += "\n\nFirst GPT2 prompt preview:\n\n" + first_prompt
            self.preview.setPlainText(preview_text)
        except Exception as exc:  # noqa: BLE001
            self.preview.setPlainText(f"Could not read generated outputs: {exc}")

        self.set_coach(4, "ไฟล์นี้ PASS และพร้อมเข้า GPT2", "กด Copy First GPT2 Prompt หรือเปิด prompts folder เพื่อทำ GPT2 ต่อทีละรายการ")

    def set_action_buttons(self, enabled: bool) -> None:
        self.copy_prompt_button.setEnabled(enabled)
        self.open_selected_button.setEnabled(enabled)
        self.open_prompts_button.setEnabled(enabled)
        self.open_clean_button.setEnabled(enabled)
        self.open_report_button.setEnabled(enabled)
        self.open_output_button.setEnabled(self.summary is not None)

    def copy_first_prompt(self) -> None:
        result = self.selected_result()
        if result is None or result.status != "PASS":
            QMessageBox.warning(self, "Not ready", "Select a PASS result first.")
            return
        prompt = read_first_prompt(result.prompt_folder)
        if not prompt:
            QMessageBox.warning(self, "No prompt", "No GPT2 prompt file found for this result.")
            return
        QGuiApplication.clipboard().setText(prompt)
        self.set_stage(5)
        self.set_coach(5, "Copied GPT2 prompt", "วาง prompt นี้ใน GPT2 Visual Prompt Refiner แล้วทำ prompt ถัดไปจาก folder handoff")
        QMessageBox.information(self, "Copied", "First GPT2 TEMPLATE_HANDOFF prompt copied to clipboard.")

    def open_selected_file(self) -> None:
        result = self.selected_result()
        if result and result.selected_file:
            self.open_path(result.selected_file)

    def open_prompt_folder(self) -> None:
        result = self.selected_result()
        if result and result.prompt_folder:
            self.open_path(result.prompt_folder)

    def open_clean_file(self) -> None:
        result = self.selected_result()
        if result:
            self.open_path(result.clean_file)

    def open_report_file(self) -> None:
        result = self.selected_result()
        if result:
            self.open_path(result.report_file)

    def open_output_folder(self) -> None:
        if self.summary:
            self.open_path(self.summary.output_root)
        elif self.selected_folder:
            self.open_path(self.selected_folder / "_cleaned")

    def open_path(self, path: Path) -> None:
        if not path.exists():
            QMessageBox.warning(self, "Missing file", str(path))
            return
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(path)))

    def reset_workflow(self) -> None:
        self.results = []
        self.summary = None
        self.worker = None
        self.selected_folder = None
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
        self.set_action_buttons(False)
        self.set_coach(1, "ตั้งจำนวนรายการ N แล้วเริ่มจาก GPT1", "ใช้ prompt skeleton ด้านซ้ายใน GPT1 ก่อน จากนั้น save output เป็น .md หรือ .txt แล้วเลือกโฟลเดอร์ raw")


def main() -> int:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
