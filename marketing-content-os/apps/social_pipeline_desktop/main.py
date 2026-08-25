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
        except Exception as exc:  # noqa: BLE001 - UI must surface failures.
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
        self.resize(1400, 900)
        self.results: list[CleanResult] = []
        self.summary: PipelineBatchSummary | None = None
        self.worker: CleanWorker | None = None
        self.selected_folder: Path | None = None

        self.setStyleSheet(
            """
            QMainWindow { background: #f6f8fb; color: #10203a; }
            QLabel { color: #10203a; }
            QLabel#AppTitle { font-size: 24px; font-weight: 700; color: #172033; }
            QLabel#AppSubtitle { font-size: 13px; color: #556070; }
            QLabel#PanelTitle { font-size: 17px; font-weight: 700; color: #14315c; }
            QLabel#PanelHelp { font-size: 13px; color: #394a62; }
            QLabel#CoachTitle { font-size: 18px; font-weight: 700; color: #14315c; }
            QLabel#CoachText { font-size: 14px; color: #26364d; }
            QLabel#MetricBig { font-size: 22px; font-weight: 700; color: #14315c; }
            QLabel#MetricLabel { font-size: 12px; color: #5f6f86; }
            QLabel#EmptyState { color: #65758c; font-size: 14px; padding: 12px; }
            QFrame#Panel, QFrame#CoachCard, QFrame#CommandBar { background: #ffffff; border: 1px solid #dbe3ef; border-radius: 12px; }
            QFrame#StepBadge { background: #eef3fb; border: 1px solid #d5dfef; border-radius: 10px; }
            QFrame#StepBadge[active="true"] { background: #dff0ff; border: 2px solid #3b82f6; }
            QLabel#StepNumber { font-size: 18px; font-weight: 700; color: #1d4ed8; min-width: 26px; }
            QLabel#StepTitle { font-size: 13px; color: #26364d; }
            QPushButton { color: #10203a; padding: 9px 14px; border-radius: 8px; background: #e7edf7; border: 1px solid #cbd6e7; }
            QPushButton:hover { background: #dbe7f7; }
            QPushButton:disabled { color: #7c8797; background: #edf1f7; border: 1px solid #d8e0ee; }
            QPushButton#PrimaryButton { background: #2563eb; color: #ffffff; font-size: 15px; font-weight: 700; border: 1px solid #1d4ed8; padding: 12px 18px; }
            QPushButton#SuccessButton { background: #059669; color: #ffffff; font-weight: 700; border: 1px solid #047857; }
            QPushButton#DangerButton { background: #fee2e2; color: #991b1b; border: 1px solid #fecaca; }
            QPushButton#TinyButton { padding: 7px 11px; min-width: 34px; font-size: 16px; font-weight: 700; }
            QPushButton#CommandButton { font-size: 14px; font-weight: 700; padding: 12px 16px; }
            QLineEdit, QTextEdit { color: #10203a; background: #ffffff; border: 1px solid #cbd6e7; border-radius: 7px; padding: 8px; selection-background-color: #bfdbfe; selection-color: #0f172a; }
            QLineEdit:read-only { background: #f8fafc; color: #334155; }
            QLineEdit#NValue { font-size: 18px; font-weight: 700; }
            QTextEdit:read-only { background: #ffffff; }
            QTableWidget { color: #10203a; background: #ffffff; border: 1px solid #dbe3ef; border-radius: 8px; gridline-color: #edf2f7; selection-background-color: #dbeafe; selection-color: #10203a; }
            QTableWidget::item { padding: 4px; }
            QHeaderView::section { background: #334155; color: #ffffff; padding: 6px; border: 0; }
            QSplitter::handle { background: #d7e1f0; }
            QSplitter::handle:hover { background: #9db7dc; }
            QCheckBox { color: #10203a; }
            QProgressBar { color: #10203a; border: 1px solid #cbd6e7; border-radius: 7px; text-align: center; background: #ffffff; }
            QProgressBar::chunk { background: #2563eb; border-radius: 6px; }
            """
        )

        self.step_badges = [
            StepBadge("1", "ใส่ SKU + ตั้ง N"),
            StepBadge("2", "Copy GPT1 prompt"),
            StepBadge("3", "เลือก folder raw"),
            StepBadge("4", "Run pipeline"),
            StepBadge("5", "GPT2 + Review"),
        ]

        self.coach_title = QLabel("เริ่มจากใส่ SKU และตั้งจำนวนรายการ N")
        self.coach_title.setObjectName("CoachTitle")
        self.coach_text = QLabel("ใช้แถบสั่งงานด้านบน: Copy GPT1 Prompt → Choose Raw Folder → Run Pipeline")
        self.coach_text.setObjectName("CoachText")
        self.coach_text.setWordWrap(True)

        self.raw_count = self.metric_value("0")
        self.pass_count = self.metric_value("0")
        self.fail_count = self.metric_value("0")
        self.selected_count = self.metric_value("0")
        self.prompt_count = self.metric_value("0")

        self.sku_input = QLineEdit()
        self.sku_input.setPlaceholderText("เช่น BK-UP-MIX-EASY-01")
        self.sku_input.textChanged.connect(self.update_gpt1_prompt_preview)

        self.n_value = QLineEdit(str(DEFAULT_POST_COUNT))
        self.n_value.setObjectName("NValue")
        self.n_value.setFixedWidth(90)
        self.n_value.setAlignment(Qt.AlignCenter)
        self.n_value.editingFinished.connect(self.normalize_n_from_input)
        self.minus_button = QPushButton("−")
        self.minus_button.setObjectName("TinyButton")
        self.minus_button.clicked.connect(lambda: self.adjust_n(-1))
        self.plus_button = QPushButton("+")
        self.plus_button.setObjectName("TinyButton")
        self.plus_button.clicked.connect(lambda: self.adjust_n(1))

        self.gpt1_prompt_preview = QTextEdit()
        self.gpt1_prompt_preview.setReadOnly(True)
        self.gpt1_prompt_preview.setMinimumHeight(98)
        self.update_gpt1_prompt_preview()

        self.copy_gpt1_button = QPushButton("1. Copy GPT1 Prompt")
        self.copy_gpt1_button.setObjectName("SuccessButton")
        self.copy_gpt1_button.clicked.connect(self.copy_gpt1_prompt)

        self.input_folder = QLineEdit()
        self.input_folder.setReadOnly(True)
        self.input_folder.setPlaceholderText("ยังไม่ได้เลือกโฟลเดอร์ raw output จาก GPT1")
        self.choose_folder_button = QPushButton("2. Choose Raw Folder")
        self.choose_folder_button.setObjectName("CommandButton")
        self.choose_folder_button.clicked.connect(self.choose_folder)

        self.clean_button = QPushButton("3. Run Pipeline")
        self.clean_button.setObjectName("PrimaryButton")
        self.clean_button.clicked.connect(self.run_cleaner)
        self.clean_button.setEnabled(False)

        self.open_output_button = QPushButton("Open _cleaned Folder")
        self.open_output_button.setObjectName("CommandButton")
        self.open_output_button.clicked.connect(self.open_output_folder)
        self.open_output_button.setEnabled(False)

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

        self.results_empty = QLabel("ยังไม่มีผลลัพธ์: Copy GPT1 Prompt → save output เป็น .md/.txt → Choose Raw Folder → Run Pipeline")
        self.results_empty.setObjectName("EmptyState")
        self.results_empty.setAlignment(Qt.AlignCenter)

        self.preview = QTextEdit()
        self.preview.setReadOnly(True)
        self.preview.setPlainText(
            "พื้นที่นี้จะแสดงผลหลังไฟล์ PASS:\n"
            "- selected N rows\n"
            "- GPT2 prompt แรก\n"
            "- คำแนะนำขั้นถัดไป\n\n"
            "ใช้แถบสั่งงานด้านบนเพื่อเริ่มงาน"
        )

        self.copy_prompt_button = QPushButton("Copy First GPT2 Prompt")
        self.copy_prompt_button.setObjectName("SuccessButton")
        self.copy_prompt_button.clicked.connect(self.copy_first_prompt)
        self.open_selected_button = QPushButton("Open Selected N Rows")
        self.open_selected_button.clicked.connect(self.open_selected_file)
        self.open_prompts_button = QPushButton("Open GPT2 Prompts Folder")
        self.open_prompts_button.clicked.connect(self.open_prompt_folder)
        self.open_clean_button = QPushButton("Open Clean TSV")
        self.open_clean_button.clicked.connect(self.open_clean_file)
        self.open_report_button = QPushButton("Open Report")
        self.open_report_button.clicked.connect(self.open_report_file)
        self.reset_button = QPushButton("Reset")
        self.reset_button.setObjectName("DangerButton")
        self.reset_button.clicked.connect(self.reset_workflow)

        self.gpt2_buttons = [
            self.copy_prompt_button,
            self.open_selected_button,
            self.open_prompts_button,
            self.open_clean_button,
            self.open_report_button,
        ]

        self.setCentralWidget(self.build_ui())
        self.set_action_buttons(False)

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
        subtitle = QLabel("Document-driven operator cockpit: SKU + N → GPT1 raw files → clean TSV → N GPT2 prompts, where 1 <= N <= 60")
        subtitle.setObjectName("AppSubtitle")
        root_layout.addWidget(title)
        root_layout.addWidget(subtitle)

        steps = QHBoxLayout()
        for badge in self.step_badges:
            steps.addWidget(badge)
        root_layout.addLayout(steps)
        root_layout.addWidget(self.build_command_bar())

        main_splitter = QSplitter(Qt.Vertical)
        main_splitter.setChildrenCollapsible(False)
        main_splitter.addWidget(self.build_top_splitter())
        main_splitter.addWidget(self.build_results_panel())
        main_splitter.addWidget(self.build_preview_panel())
        main_splitter.setSizes([300, 260, 280])
        root_layout.addWidget(main_splitter, stretch=1)
        return root

    def build_command_bar(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("CommandBar")
        layout = QHBoxLayout(panel)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.addWidget(QLabel("Command Bar:"))
        layout.addWidget(self.copy_gpt1_button)
        layout.addWidget(self.choose_folder_button)
        layout.addWidget(self.clean_button)
        layout.addWidget(self.open_output_button)
        layout.addStretch(1)
        layout.addWidget(self.reset_button)
        return panel

    def build_top_splitter(self) -> QSplitter:
        top_splitter = QSplitter(Qt.Horizontal)
        top_splitter.setChildrenCollapsible(False)
        top_splitter.addWidget(self.wrap_scroll(self.build_setup_panel()))
        top_splitter.addWidget(self.wrap_scroll(self.build_status_panel()))
        top_splitter.setSizes([580, 760])
        return top_splitter

    def build_setup_panel(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("Panel")
        layout = QVBoxLayout(panel)
        layout.setSpacing(10)
        title = QLabel("1. Setup GPT1 request")
        title.setObjectName("PanelTitle")
        help_text = QLabel("กรอก SKU และจำนวน N จากนั้นใช้ปุ่มบน Command Bar เพื่อสั่งงาน")
        help_text.setObjectName("PanelHelp")
        help_text.setWordWrap(True)
        layout.addWidget(title)
        layout.addWidget(help_text)

        form = QGridLayout()
        form.addWidget(QLabel("SKU"), 0, 0)
        form.addWidget(self.sku_input, 0, 1, 1, 3)
        form.addWidget(QLabel("Post count N"), 1, 0)
        n_row = QHBoxLayout()
        n_row.addWidget(self.minus_button)
        n_row.addWidget(self.n_value)
        n_row.addWidget(self.plus_button)
        n_row.addStretch(1)
        form.addLayout(n_row, 1, 1, 1, 3)
        form.addWidget(QLabel("GPT1 prompt"), 2, 0)
        form.addWidget(self.gpt1_prompt_preview, 2, 1, 1, 3)
        form.addWidget(QLabel("Raw folder"), 3, 0)
        form.addWidget(self.input_folder, 3, 1, 1, 3)
        form.addWidget(self.advanced_toggle, 4, 1, 1, 3)
        form.addWidget(self.allow_visual, 5, 1, 1, 3)
        form.addWidget(self.allow_angle, 6, 1, 1, 3)
        form.addWidget(self.progress, 7, 0, 1, 4)
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
        guide = QLabel("Safe rule: raw GPT1 output is evidence only. Only PASS clean TSV and generated prompt files should go to GPT2. Human review remains required before publishing.")
        guide.setObjectName("PanelHelp")
        guide.setWordWrap(True)
        layout.addWidget(guide)
        layout.addStretch(1)
        return panel

    def build_results_panel(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("Panel")
        layout = QVBoxLayout(panel)
        title = QLabel("3. Batch results")
        title.setObjectName("PanelTitle")
        layout.addWidget(title)
        layout.addWidget(self.results_empty)
        layout.addWidget(self.table, stretch=1)
        return panel

    def build_preview_panel(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("Panel")
        layout = QVBoxLayout(panel)
        title = QLabel("4. Continue to GPT2")
        title.setObjectName("PanelTitle")
        layout.addWidget(title)
        action_layout = QHBoxLayout()
        for button in self.gpt2_buttons:
            action_layout.addWidget(button)
        action_layout.addStretch(1)
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

    def get_post_count(self) -> int:
        try:
            value = int(self.n_value.text().strip())
        except ValueError:
            value = DEFAULT_POST_COUNT
        return max(MIN_POST_COUNT, min(MAX_POST_COUNT, value))

    def set_post_count(self, value: int) -> None:
        value = max(MIN_POST_COUNT, min(MAX_POST_COUNT, value))
        self.n_value.setText(str(value))
        self.update_gpt1_prompt_preview()
        self.set_coach(1, f"ตั้งค่า N = {value} แล้ว", f"กด Copy GPT1 Prompt เพื่อสร้าง NUMBER_OF_ROWS={value}")

    def normalize_n_from_input(self) -> None:
        self.set_post_count(self.get_post_count())

    def adjust_n(self, delta: int) -> None:
        self.set_post_count(self.get_post_count() + delta)

    def gpt1_prompt_text(self) -> str:
        sku = self.sku_input.text().strip() or "<SKU>"
        n = self.get_post_count()
        return f"SKU: {sku}\nNUMBER_OF_ROWS: {n}\nPLATFORM: AUTO\nCAMPAIGN_GOAL: AUTO"

    def update_gpt1_prompt_preview(self) -> None:
        if hasattr(self, "gpt1_prompt_preview"):
            self.gpt1_prompt_preview.setPlainText(self.gpt1_prompt_text())

    def copy_gpt1_prompt(self) -> None:
        self.normalize_n_from_input()
        QGuiApplication.clipboard().setText(self.gpt1_prompt_text())
        self.set_coach(2, "คัดลอก GPT1 prompt แล้ว", "นำไปวางใน GPT1 แล้ว save output ทั้งหมดเป็นไฟล์ .md หรือ .txt ใน raw folder")
        QMessageBox.information(self, "Copied", "GPT1 prompt copied to clipboard.")

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
        self.preview.setPlainText("เลือกโฟลเดอร์แล้ว กด Run Pipeline เพื่อ clean, validate และเตรียม prompts")
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
        self.results_empty.setVisible(True)
        if raw_files:
            n = self.get_post_count()
            self.set_coach(3, f"พบไฟล์ raw {len(raw_files)} ไฟล์", f"กด Run Pipeline เพื่อ validate expected rows = {n} และสร้าง {n} GPT2 prompts ต่อไฟล์ที่ PASS")
        else:
            self.set_coach(2, "ยังไม่พบไฟล์ raw", "นำ output จาก GPT1 ไป save เป็น .md หรือ .txt ในโฟลเดอร์นี้ แล้วเลือกโฟลเดอร์อีกครั้ง")

    def run_cleaner(self) -> None:
        if self.selected_folder is None:
            QMessageBox.warning(self, "Missing folder", "Choose a raw folder first.")
            return
        self.normalize_n_from_input()
        self.clean_button.setEnabled(False)
        self.table.setRowCount(0)
        self.results_empty.setText("กำลัง clean และ validate ทุกไฟล์...")
        self.results_empty.setVisible(True)
        self.preview.setPlainText("กำลังประมวลผล โปรดรอจนกว่า Batch results จะแสดง PASS / FAIL")
        self.progress.setValue(10)
        self.set_action_buttons(False)
        n = self.get_post_count()
        self.set_coach(4, "กำลัง run pipeline", f"โปรแกรมกำลังเตรียม clean TSV และ N={n} GPT2 prompts ต่อไฟล์ที่ PASS")
        self.worker = CleanWorker(self.selected_folder, n, self.allow_visual.isChecked(), self.allow_angle.isChecked())
        self.worker.finished_with_summary.connect(self.on_clean_finished)
        self.worker.failed.connect(self.on_clean_failed)
        self.worker.start()

    def on_clean_failed(self, message: str) -> None:
        self.clean_button.setEnabled(True)
        self.progress.setValue(0)
        self.results_empty.setText("Cleaner failed: เปิด error แล้วแก้ environment หรือ raw input")
        self.set_coach(4, "Cleaner failed", "เปิดรายละเอียด error แล้วแก้ input หรือส่ง error กลับมาตรวจ")
        QMessageBox.critical(self, "Cleaner failed", message)

    def on_clean_finished(self, summary: PipelineBatchSummary) -> None:
        self.clean_button.setEnabled(True)
        self.summary = summary
        self.results = list(summary.results)
        self.progress.setValue(100)
        self.open_output_button.setEnabled(True)
        self.raw_count.setText(str(summary.raw_file_count))
        self.pass_count.setText(str(summary.pass_count))
        self.fail_count.setText(str(summary.fail_count))
        self.selected_count.setText(str(summary.selected_row_count))
        self.prompt_count.setText(str(summary.prompt_file_count))
        self.table.setRowCount(len(self.results))
        self.results_empty.setVisible(len(self.results) == 0)
        if len(self.results) == 0:
            self.results_empty.setText("ไม่พบไฟล์ .md / .txt / .text ในโฟลเดอร์นี้")
        for row_index, result in enumerate(self.results):
            values = [result.status, result.raw_file.name, f"{result.extracted_rows}/{result.expected_rows}", str(result.selected_rows), str(result.prompt_files), result.next_action]
            for col, value in enumerate(values):
                item = QTableWidgetItem(value)
                if col in {0, 2, 3, 4}:
                    item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_index, col, item)
        self.table.resizeRowsToContents()
        first_pass_index = next((i for i, result in enumerate(self.results) if result.status == "PASS"), None)
        if first_pass_index is not None:
            self.table.selectRow(first_pass_index)
            self.set_coach(5, "เตรียม GPT2 prompts เสร็จแล้ว", "เลือกไฟล์ PASS แล้วใช้ปุ่ม GPT2 ด้านล่างเพื่อทำงานต่อ")
        elif self.results:
            self.open_report_button.setEnabled(True)
            self.preview.setPlainText("ยังไม่มีไฟล์ PASS: เลือกแถว FAIL แล้วเปิด report เพื่อแก้ raw GPT1 output")
            self.set_coach(4, "ยังไม่มีไฟล์ PASS", "เปิด report ของแต่ละไฟล์ที่ FAIL แล้วแก้ raw GPT1 output ก่อนส่งเข้า GPT2")
        else:
            self.preview.setPlainText("ไม่พบ raw files ที่ใช้ได้ในโฟลเดอร์นี้")
            self.set_coach(3, "ไม่พบไฟล์ raw", "เพิ่มไฟล์ .md หรือ .txt จาก GPT1 แล้วเลือกโฟลเดอร์อีกครั้ง")

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
            self.preview.setPlainText("ไฟล์นี้ FAIL: เปิด report ก่อน ห้ามส่งเข้า GPT2")
            self.set_coach(4, "ไฟล์นี้ยังไม่ผ่าน", "อย่าส่งไฟล์นี้เข้า GPT2 ให้เปิด report แล้วแก้ก่อน")
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
        self.set_coach(5, "ไฟล์นี้ PASS และพร้อมเข้า GPT2", "กด Copy First GPT2 Prompt หรือเปิด prompts folder เพื่อทำ GPT2 ต่อทีละรายการ")

    def set_action_buttons(self, enabled: bool) -> None:
        for button in self.gpt2_buttons:
            button.setEnabled(enabled)
        if self.summary is not None:
            self.open_output_button.setEnabled(True)

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
        self.results_empty.setText("ยังไม่มีผลลัพธ์: Copy GPT1 Prompt → save output เป็น .md/.txt → Choose Raw Folder → Run Pipeline")
        self.results_empty.setVisible(True)
        self.preview.setPlainText(
            "พื้นที่นี้จะแสดงผลหลังไฟล์ PASS:\n"
            "- selected N rows\n"
            "- GPT2 prompt แรก\n"
            "- คำแนะนำขั้นถัดไป\n\n"
            "ใช้แถบสั่งงานด้านบนเพื่อเริ่มงาน"
        )
        self.raw_count.setText("0")
        self.pass_count.setText("0")
        self.fail_count.setText("0")
        self.selected_count.setText("0")
        self.prompt_count.setText("0")
        self.progress.setValue(0)
        self.clean_button.setEnabled(False)
        self.open_output_button.setEnabled(False)
        self.set_action_buttons(False)
        self.set_coach(1, "เริ่มจากใส่ SKU และตั้งจำนวนรายการ N", "ใช้แถบสั่งงานด้านบน: Copy GPT1 Prompt → Choose Raw Folder → Run Pipeline")


def main() -> int:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
