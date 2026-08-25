from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import Qt, QThread, QUrl, Signal
from PySide6.QtGui import QAction, QDesktopServices, QGuiApplication
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
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
    QTabWidget,
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
except ImportError:
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

APP_DIR = Path(__file__).resolve().parent
CONTENT_OS_ROOT = APP_DIR.parents[1]
REPO_ROOT = CONTENT_OS_ROOT.parent
SKU_LOOKUP_PATH = CONTENT_OS_ROOT / "schemas" / "sku_lookup_v1.tsv"
OPERATOR_WORKSPACE_ROOT = REPO_ROOT / "_operator_workspace"

PLATFORM_CHOICES = [
    ("ให้ระบบเลือกช่องทางให้", "AUTO"),
    ("Facebook", "FACEBOOK"),
    ("LINE Official Account", "LINE_OA"),
    ("Marketplace", "MARKETPLACE"),
    ("หน้าเว็บสินค้า", "LANDING_PAGE"),
]

GOAL_CHOICES = [
    ("ให้ระบบเลือกเป้าหมายให้", "AUTO"),
    ("ทำให้คนรู้จักสินค้า", "BUILD_AWARENESS"),
    ("ให้ข้อมูลและอธิบายสินค้า", "EDUCATE"),
    ("ชวนให้คนมีส่วนร่วม", "CREATE_ENGAGEMENT"),
    ("แสดงคุณค่าและจุดเด่นของสินค้า", "SHOW_PRODUCT_VALUE"),
    ("สร้างความน่าเชื่อถือ", "BUILD_TRUST"),
    ("ช่วยให้ลูกค้าสนใจมากขึ้น", "DRIVE_CONSIDERATION"),
    ("กระตุ้นการตัดสินใจซื้อ", "DRIVE_CONVERSION"),
    ("ดูแลลูกค้าเดิมและชวนซื้อเพิ่ม", "RETENTION_CROSS_SELL"),
]

DURATION_CHOICES = [
    ("ไม่กำหนดระยะเวลา", "AUTO"),
    ("7 วัน", "7_DAYS"),
    ("14 วัน", "14_DAYS"),
    ("30 วัน", "30_DAYS"),
    ("60 วัน", "60_DAYS"),
    ("90 วัน", "90_DAYS"),
]

FLAG_CHOICES = [
    ("ให้ระบบเลือกช่องทางและรูปแบบให้เหมาะสม", "AUTO_PLATFORM_RESOLUTION"),
    ("ตรวจคำมาตรฐานของระบบ", "CONTROLLED_VOCAB_VALIDATION"),
    ("ใช้ข้อมูลสินค้าจากฐานข้อมูล", "SKU_LOOKUP_PROMPT_ASSEMBLY"),
    ("บังคับตรวจชุดข้อมูลอ้างอิงก่อนสร้าง", "KNOWLEDGE_MANIFEST_REQUIRED"),
]


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


def load_products() -> list[dict[str, str]]:
    if not SKU_LOOKUP_PATH.exists():
        return []
    lines = SKU_LOOKUP_PATH.read_text(encoding="utf-8").splitlines()
    if not lines:
        return []
    headers = lines[0].split("\t")
    products: list[dict[str, str]] = []
    for line in lines[1:]:
        values = line.split("\t")
        row = {header: values[index] if index < len(values) else "" for index, header in enumerate(headers)}
        if row.get("SKU"):
            products.append(row)
    return products


def product_display(row: dict[str, str]) -> str:
    return f"{row.get('THAI_NAME') or row.get('PRODUCT_NAME') or 'สินค้า'} — {row.get('SKU', '')}"


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("เครื่องมือเตรียมคอนเทนต์โซเชียล BiiigBee")
        self.resize(1360, 880)

        self.results: list[CleanResult] = []
        self.summary: PipelineBatchSummary | None = None
        self.worker: CleanWorker | None = None
        self.selected_folder: Path | None = None
        self.products = load_products()

        self.setStyleSheet(
            """
            QMainWindow { background: #f6f8fb; color: #10203a; }
            QLabel { color: #10203a; }
            QLabel#AppTitle { font-size: 24px; font-weight: 700; color: #172033; }
            QLabel#AppSubtitle { font-size: 13px; color: #556070; }
            QLabel#PanelTitle { font-size: 18px; font-weight: 700; color: #14315c; }
            QLabel#PanelHelp { font-size: 13px; color: #394a62; }
            QLabel#CoachTitle { font-size: 18px; font-weight: 700; color: #14315c; }
            QLabel#CoachText { font-size: 14px; color: #26364d; }
            QLabel#NextAction { font-size: 20px; font-weight: 800; color: #0f5132; background: #dcfce7; border: 1px solid #86efac; border-radius: 12px; padding: 14px; }
            QLabel#MetricBig { font-size: 22px; font-weight: 700; color: #14315c; }
            QLabel#MetricLabel { font-size: 12px; color: #5f6f86; }
            QLabel#EmptyState { color: #65758c; font-size: 14px; padding: 18px; }
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
            QPushButton#PresetButton { padding: 7px 10px; font-weight: 700; }
            QPushButton#CommandButton { font-size: 14px; font-weight: 700; padding: 12px 16px; }
            QLineEdit, QTextEdit, QComboBox { color: #10203a; background: #ffffff; border: 1px solid #94a3b8; border-radius: 7px; padding: 8px; selection-background-color: #bfdbfe; selection-color: #0f172a; }
            QComboBox { min-height: 28px; color: #0f172a; background-color: #ffffff; }
            QComboBox::drop-down { border-left: 1px solid #94a3b8; width: 30px; background: #e7edf7; }
            QComboBox::down-arrow { image: none; border-left: 5px solid transparent; border-right: 5px solid transparent; border-top: 7px solid #0f172a; width: 0; height: 0; margin-right: 8px; }
            QComboBox QAbstractItemView { color: #0f172a; background-color: #ffffff; selection-background-color: #2563eb; selection-color: #ffffff; outline: 0; border: 1px solid #94a3b8; }
            QLineEdit:read-only { background: #f8fafc; color: #334155; }
            QLineEdit#NValue { font-size: 18px; font-weight: 700; }
            QTableWidget { color: #10203a; background: #ffffff; border: 1px solid #dbe3ef; border-radius: 8px; gridline-color: #edf2f7; selection-background-color: #dbeafe; selection-color: #10203a; }
            QHeaderView::section { background: #334155; color: #ffffff; padding: 6px; border: 0; }
            QTabWidget::pane { border: 1px solid #dbe3ef; border-radius: 8px; background: #ffffff; }
            QTabBar::tab { background: #e7edf7; color: #10203a; border: 1px solid #cbd6e7; padding: 10px 18px; margin-right: 4px; border-top-left-radius: 8px; border-top-right-radius: 8px; }
            QTabBar::tab:selected { background: #2563eb; color: #ffffff; font-weight: 700; }
            QProgressBar { color: #10203a; border: 1px solid #cbd6e7; border-radius: 7px; text-align: center; background: #ffffff; }
            QProgressBar::chunk { background: #2563eb; border-radius: 6px; }
            QCheckBox { color: #10203a; }
            """
        )

        self.step_badges = [
            StepBadge("1", "เลือกสินค้า + จำนวนโพสต์"),
            StepBadge("2", "คัดลอกคำสั่ง GPT1"),
            StepBadge("3", "เก็บคำตอบจาก GPT1"),
            StepBadge("4", "ตรวจไฟล์และเตรียมส่งต่อ"),
            StepBadge("5", "ส่งเข้า GPT2 + ตรวจงาน"),
        ]
        self.next_action = QLabel("ขั้นต่อไป: เลือกสินค้าและจำนวนโพสต์ แล้วกด “คัดลอกคำสั่ง GPT1”")
        self.next_action.setObjectName("NextAction")
        self.next_action.setWordWrap(True)
        self.coach_title = QLabel("เลือกชื่อสินค้าได้เลย ไม่ต้องจำรหัสสินค้า")
        self.coach_title.setObjectName("CoachTitle")
        self.coach_text = QLabel("โปรแกรมจะแปลงชื่อสินค้าที่เลือกเป็นรหัส SKU ให้เอง")
        self.coach_text.setObjectName("CoachText")
        self.coach_text.setWordWrap(True)

        self.raw_count = self.metric_value("0")
        self.pass_count = self.metric_value("0")
        self.fail_count = self.metric_value("0")
        self.selected_count = self.metric_value("0")
        self.prompt_count = self.metric_value("0")

        self.product_combo = QComboBox()
        self.product_combo.setMinimumWidth(560)
        for product in self.products or [{"SKU": "<SKU>", "THAI_NAME": "ไม่พบรายการสินค้า"}]:
            self.product_combo.addItem(product_display(product), product)
        self.product_combo.currentIndexChanged.connect(self.on_product_changed)
        self.product_card = QTextEdit()
        self.product_card.setReadOnly(True)
        self.product_card.setMinimumHeight(122)

        self.n_value = QLineEdit(str(DEFAULT_POST_COUNT))
        self.n_value.setObjectName("NValue")
        self.n_value.setFixedWidth(90)
        self.n_value.setAlignment(Qt.AlignCenter)
        self.n_value.editingFinished.connect(self.normalize_n_from_input)
        self.minus_button = self.small_button("−", lambda: self.adjust_n(-1))
        self.plus_button = self.small_button("+", lambda: self.adjust_n(1))
        self.preset_buttons: list[QPushButton] = []
        for preset in (10, 20, 30, 60):
            button = QPushButton(str(preset))
            button.setObjectName("PresetButton")
            button.clicked.connect(lambda _checked=False, value=preset: self.set_post_count(value))
            self.preset_buttons.append(button)

        self.platform_combo = self.choice_combo(PLATFORM_CHOICES)
        self.goal_combo = self.choice_combo(GOAL_CHOICES)
        self.duration_combo = self.choice_combo(DURATION_CHOICES)
        for combo in (self.platform_combo, self.goal_combo, self.duration_combo):
            combo.currentIndexChanged.connect(self.update_gpt1_prompt_preview)

        self.flag_boxes: list[tuple[QCheckBox, str]] = []
        for label, token in FLAG_CHOICES:
            box = QCheckBox(label)
            box.stateChanged.connect(self.update_gpt1_prompt_preview)
            self.flag_boxes.append((box, token))

        self.gpt1_prompt_preview = QTextEdit()
        self.gpt1_prompt_preview.setReadOnly(True)
        self.gpt1_prompt_preview.setMinimumHeight(170)

        self.copy_gpt1_button = self.action_button("1. คัดลอกคำสั่ง GPT1", self.copy_gpt1_prompt, "SuccessButton")
        self.workspace_button = self.action_button("เปิดโฟลเดอร์สำหรับวางคำตอบ GPT1", self.create_or_open_sku_workspace, "CommandButton")
        self.choose_folder_button = self.action_button("2. เลือกโฟลเดอร์คำตอบ GPT1", self.choose_folder, "CommandButton")
        self.clean_button = self.action_button("3. ตรวจไฟล์และเตรียมส่งต่อ", self.run_cleaner, "PrimaryButton")
        self.clean_button.setEnabled(False)
        self.open_output_button = self.action_button("เปิดโฟลเดอร์ผลลัพธ์", self.open_output_folder, "CommandButton")
        self.open_output_button.setEnabled(False)
        self.reset_button = self.action_button("เริ่มใหม่", self.reset_workflow, "DangerButton")

        self.command_copy_gpt1_button = self.action_button("1. คัดลอกคำสั่ง GPT1", self.copy_gpt1_prompt, "SuccessButton")
        self.command_workspace_button = self.action_button("เปิดโฟลเดอร์สำหรับวางคำตอบ GPT1", self.create_or_open_sku_workspace, "CommandButton")
        self.command_choose_folder_button = self.action_button("2. เลือกโฟลเดอร์คำตอบ GPT1", self.choose_folder, "CommandButton")
        self.command_clean_button = self.action_button("3. ตรวจไฟล์และเตรียมส่งต่อ", self.run_cleaner, "PrimaryButton")
        self.command_clean_button.setEnabled(False)
        self.command_open_output_button = self.action_button("เปิดโฟลเดอร์ผลลัพธ์", self.open_output_folder, "CommandButton")
        self.command_open_output_button.setEnabled(False)
        self.command_reset_button = self.action_button("เริ่มใหม่", self.reset_workflow, "DangerButton")

        self.input_folder = QLineEdit()
        self.input_folder.setReadOnly(True)
        self.input_folder.setPlaceholderText("ยังไม่ได้เลือกโฟลเดอร์ที่เก็บคำตอบจาก GPT1")
        self.advanced_toggle = QCheckBox("แสดงตัวเลือกตรวจไฟล์ขั้นสูง")
        self.allow_visual = QCheckBox("ยอมให้รูปแบบภาพซ้ำกันมากขึ้น")
        self.allow_angle = QCheckBox("ยอมให้มุมขายซ้ำกันมากขึ้น")
        self.allow_visual.setVisible(False)
        self.allow_angle.setVisible(False)
        self.advanced_toggle.toggled.connect(self.toggle_advanced)
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)

        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(["สถานะ", "ไฟล์", "จำนวนแถว", "รายการที่เตรียมไว้", "คำสั่ง GPT2", "สิ่งที่ควรทำต่อ"])
        for col in (0, 2, 3, 4):
            self.table.horizontalHeader().setSectionResizeMode(col, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.itemSelectionChanged.connect(self.on_selection_changed)
        self.results_empty = QLabel("ยังไม่มีผลลัพธ์: คัดลอกคำสั่ง GPT1 → บันทึกคำตอบเป็นไฟล์ .md/.txt → เปิดโฟลเดอร์สำหรับวางคำตอบ → ตรวจไฟล์และเตรียมส่งต่อ")
        self.results_empty.setObjectName("EmptyState")
        self.results_empty.setAlignment(Qt.AlignCenter)
        self.preview = QTextEdit()
        self.preview.setReadOnly(True)
        self.preview.setPlainText("พื้นที่นี้จะแสดงผลหลังไฟล์ผ่านการตรวจ:\n- รายการที่เตรียมไว้\n- คำสั่ง GPT2 รายการแรก\n- คำแนะนำขั้นถัดไป")

        self.copy_prompt_button = self.action_button("คัดลอกคำสั่ง GPT2 รายการแรก", self.copy_first_prompt, "SuccessButton")
        self.open_selected_button = self.action_button("เปิดรายการที่เตรียมไว้", self.open_selected_file)
        self.open_prompts_button = self.action_button("เปิดโฟลเดอร์คำสั่ง GPT2", self.open_prompt_folder)
        self.open_clean_button = self.action_button("เปิดไฟล์ที่ตรวจผ่านแล้ว", self.open_clean_file)
        self.open_report_button = self.action_button("เปิดรายงานการตรวจ", self.open_report_file)
        self.gpt2_buttons = [self.copy_prompt_button, self.open_selected_button, self.open_prompts_button, self.open_clean_button, self.open_report_button]

        self.tabs = QTabWidget()
        self.tabs.currentChanged.connect(self.on_tab_changed)
        self.setCentralWidget(self.build_ui())
        self.set_action_buttons(False)
        self.on_product_changed()
        self.update_gpt1_prompt_preview()

        quit_action = QAction("ออก", self)
        quit_action.triggered.connect(self.close)
        self.menuBar().addAction(quit_action)
        self.set_stage(1)

    def choice_combo(self, choices: list[tuple[str, str]]) -> QComboBox:
        combo = QComboBox()
        combo.setMinimumWidth(260)
        for label, token in choices:
            combo.addItem(label, token)
        return combo

    def action_button(self, text: str, handler, object_name: str | None = None) -> QPushButton:
        button = QPushButton(text)
        button.clicked.connect(handler)
        if object_name:
            button.setObjectName(object_name)
        return button

    def small_button(self, text: str, handler) -> QPushButton:
        button = QPushButton(text)
        button.setObjectName("TinyButton")
        button.clicked.connect(handler)
        return button

    def build_ui(self) -> QWidget:
        root = QWidget()
        layout = QVBoxLayout(root)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)
        title = QLabel("เครื่องมือเตรียมคอนเทนต์โซเชียล BiiigBee")
        title.setObjectName("AppTitle")
        subtitle = QLabel("เลือกสินค้า → คัดลอกคำสั่งให้ GPT1 → วางคำตอบจาก GPT1 → ตรวจไฟล์ → ส่งต่อ GPT2")
        subtitle.setObjectName("AppSubtitle")
        layout.addWidget(title)
        layout.addWidget(subtitle)
        steps = QHBoxLayout()
        for badge in self.step_badges:
            steps.addWidget(badge)
        layout.addLayout(steps)
        layout.addWidget(self.next_action)
        layout.addWidget(self.build_command_bar())
        self.tabs.addTab(self.wrap_scroll(self.build_gpt1_tab()), "1. สร้างคำสั่งให้ GPT1")
        self.tabs.addTab(self.wrap_scroll(self.build_import_tab()), "2. นำคำตอบจาก GPT1 เข้าโปรแกรม")
        self.tabs.addTab(self.wrap_scroll(self.build_results_tab()), "3. ผลการตรวจ")
        self.tabs.addTab(self.wrap_scroll(self.build_handoff_tab()), "4. เตรียมส่งเข้า GPT2")
        self.tabs.addTab(self.wrap_scroll(self.build_review_tab()), "5. ตรวจงานก่อนใช้จริง")
        layout.addWidget(self.tabs, stretch=1)
        return root

    def build_command_bar(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("CommandBar")
        layout = QHBoxLayout(panel)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.addWidget(QLabel("ปุ่มหลัก:"))
        layout.addWidget(self.command_copy_gpt1_button)
        layout.addWidget(self.command_workspace_button)
        layout.addWidget(self.command_choose_folder_button)
        layout.addWidget(self.command_clean_button)
        layout.addWidget(self.command_open_output_button)
        layout.addStretch(1)
        layout.addWidget(self.command_reset_button)
        return panel

    def build_gpt1_tab(self) -> QWidget:
        panel = QFrame()
        panel.setObjectName("Panel")
        layout = QVBoxLayout(panel)
        title = QLabel("1. สร้างคำสั่งให้ GPT1")
        title.setObjectName("PanelTitle")
        help_text = QLabel("เลือกค่าจากรายการ โปรแกรมจะสร้างคำสั่งที่ถูกต้องให้ ไม่ต้องจำรหัสหรือพิมพ์คำอังกฤษเอง")
        help_text.setObjectName("PanelHelp")
        help_text.setWordWrap(True)
        layout.addWidget(title)
        layout.addWidget(help_text)
        form = QGridLayout()
        form.addWidget(QLabel("สินค้า"), 0, 0)
        form.addWidget(self.product_combo, 0, 1, 1, 4)
        form.addWidget(QLabel("รายละเอียดสินค้า"), 1, 0)
        form.addWidget(self.product_card, 1, 1, 1, 4)
        form.addWidget(QLabel("จำนวนโพสต์"), 2, 0)
        n_row = QHBoxLayout()
        n_row.addWidget(self.minus_button)
        n_row.addWidget(self.n_value)
        n_row.addWidget(self.plus_button)
        n_row.addWidget(QLabel("เลือกเร็ว:"))
        for button in self.preset_buttons:
            n_row.addWidget(button)
        n_row.addStretch(1)
        form.addLayout(n_row, 2, 1, 1, 4)
        form.addWidget(QLabel("ช่องทางโพสต์"), 3, 0)
        form.addWidget(self.platform_combo, 3, 1)
        form.addWidget(QLabel("เป้าหมายของโพสต์"), 3, 2)
        form.addWidget(self.goal_combo, 3, 3)
        form.addWidget(QLabel("ระยะเวลาแคมเปญ"), 4, 0)
        form.addWidget(self.duration_combo, 4, 1)
        flag_layout = QVBoxLayout()
        for box, _token in self.flag_boxes:
            flag_layout.addWidget(box)
        form.addLayout(flag_layout, 4, 2, 1, 2)
        form.addWidget(QLabel("คำสั่งที่จะส่งให้ GPT1"), 5, 0)
        form.addWidget(self.gpt1_prompt_preview, 5, 1, 1, 4)
        form.addWidget(self.copy_gpt1_button, 6, 1, 1, 4)
        layout.addLayout(form)
        note = QLabel("หลัง GPT1 ตอบ ให้บันทึกคำตอบทั้งหมดเป็นไฟล์ .md หรือ .txt ในโฟลเดอร์ของสินค้านี้ แล้วไปแท็บ 2")
        note.setObjectName("PanelHelp")
        note.setWordWrap(True)
        layout.addWidget(note)
        layout.addStretch(1)
        return panel

    def build_import_tab(self) -> QWidget:
        panel = QFrame()
        panel.setObjectName("Panel")
        layout = QVBoxLayout(panel)
        title = QLabel("2. นำคำตอบจาก GPT1 เข้าโปรแกรม")
        title.setObjectName("PanelTitle")
        help_text = QLabel("เปิดโฟลเดอร์ของสินค้า แล้ววางไฟล์คำตอบจาก GPT1 ลงไป โปรแกรมจะตรวจไฟล์ทั้งหมดในโฟลเดอร์นั้น")
        help_text.setObjectName("PanelHelp")
        help_text.setWordWrap(True)
        layout.addWidget(title)
        layout.addWidget(help_text)
        form = QGridLayout()
        form.addWidget(QLabel("โฟลเดอร์คำตอบ GPT1"), 0, 0)
        form.addWidget(self.input_folder, 0, 1)
        form.addWidget(self.workspace_button, 0, 2)
        form.addWidget(self.choose_folder_button, 0, 3)
        form.addWidget(self.clean_button, 1, 1, 1, 3)
        form.addWidget(self.progress, 2, 0, 1, 4)
        form.addWidget(self.advanced_toggle, 3, 1, 1, 3)
        form.addWidget(self.allow_visual, 4, 1, 1, 3)
        form.addWidget(self.allow_angle, 5, 1, 1, 3)
        layout.addLayout(form)
        layout.addWidget(self.build_status_panel())
        layout.addStretch(1)
        return panel

    def build_results_tab(self) -> QWidget:
        panel = QFrame()
        panel.setObjectName("Panel")
        layout = QVBoxLayout(panel)
        title = QLabel("3. ผลการตรวจไฟล์")
        title.setObjectName("PanelTitle")
        layout.addWidget(title)
        layout.addWidget(self.results_empty)
        layout.addWidget(self.table, stretch=1)
        return panel

    def build_handoff_tab(self) -> QWidget:
        panel = QFrame()
        panel.setObjectName("Panel")
        layout = QVBoxLayout(panel)
        title = QLabel("4. เตรียมส่งเข้า GPT2")
        title.setObjectName("PanelTitle")
        help_text = QLabel("เมื่อไฟล์ผ่านการตรวจแล้ว ใช้ปุ่มด้านล่างเพื่อคัดลอกคำสั่ง GPT2 หรือเปิดโฟลเดอร์คำสั่งที่โปรแกรมเตรียมไว้")
        help_text.setObjectName("PanelHelp")
        help_text.setWordWrap(True)
        layout.addWidget(title)
        layout.addWidget(help_text)
        actions = QHBoxLayout()
        for button in self.gpt2_buttons:
            actions.addWidget(button)
        actions.addStretch(1)
        actions.addWidget(self.open_output_button)
        layout.addLayout(actions)
        layout.addWidget(self.preview, stretch=1)
        return panel

    def build_review_tab(self) -> QWidget:
        panel = QFrame()
        panel.setObjectName("Panel")
        layout = QVBoxLayout(panel)
        title = QLabel("5. ตรวจงานก่อนใช้จริง")
        title.setObjectName("PanelTitle")
        layout.addWidget(title)
        text = QTextEdit()
        text.setReadOnly(True)
        text.setPlainText(
            "หลัง GPT2 ส่งผลลัพธ์แล้ว:\n\n"
            "1. ใช้คำสั่งสร้างภาพจาก GPT2 ไปสร้างภาพ\n"
            "2. ตรวจว่าภาพตรงกับสินค้าและไม่มีข้อความเกินจริง\n"
            "3. ตรวจข้อความโพสต์ หัวข้อ และปุ่มชวนคลิก\n"
            "4. เก็บชุดโพสต์และอัปเดตรายการงาน\n\n"
            "โปรแกรมนี้ยังไม่โพสต์ให้อัตโนมัติ และยังต้องมีคนตรวจงานก่อนใช้จริง"
        )
        layout.addWidget(text, stretch=1)
        return panel

    def build_status_panel(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("Panel")
        layout = QVBoxLayout(panel)
        title = QLabel("ตัวช่วยบอกขั้นตอน")
        title.setObjectName("PanelTitle")
        layout.addWidget(title)
        card = QFrame()
        card.setObjectName("CoachCard")
        card_layout = QVBoxLayout(card)
        card_layout.addWidget(self.coach_title)
        card_layout.addWidget(self.coach_text)
        layout.addWidget(card)
        metrics = QHBoxLayout()
        for name, value in (("ไฟล์จาก GPT1", self.raw_count), ("ผ่าน", self.pass_count), ("ไม่ผ่าน", self.fail_count), ("รายการที่เตรียมไว้", self.selected_count), ("คำสั่ง GPT2", self.prompt_count)):
            metrics.addWidget(self.metric_box(name, value))
        layout.addLayout(metrics)
        guide = QLabel("ข้อควรจำ: คำตอบดิบจาก GPT1 ยังไม่ควรส่งต่อ ต้องใช้เฉพาะไฟล์ที่ผ่านการตรวจและคำสั่ง GPT2 ที่โปรแกรมเตรียมไว้")
        guide.setObjectName("PanelHelp")
        guide.setWordWrap(True)
        layout.addWidget(guide)
        return panel

    def wrap_scroll(self, widget: QWidget) -> QScrollArea:
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setWidget(widget)
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

    def current_product(self) -> dict[str, str]:
        data = self.product_combo.currentData()
        return data if isinstance(data, dict) else {}

    def current_sku(self) -> str:
        return self.current_product().get("SKU") or "<SKU>"

    def on_product_changed(self) -> None:
        product = self.current_product()
        self.product_card.setPlainText(
            f"สินค้า: {product.get('THAI_NAME') or product.get('PRODUCT_NAME', '')}\n"
            f"รหัสสินค้า: {product.get('SKU', '')}\n"
            f"ช่วงชั้น: {product.get('GRADE_BAND', '')}\n"
            f"ระดับ: {product.get('DISPLAY_DIFFICULTY', '')}\n"
            f"จำนวนโจทย์: {product.get('PUZZLE_COUNT', '')}\n"
            f"เฉลย: {product.get('ANSWER_KEY_STATUS', '')}\n"
            f"ประเภทข้อความที่ปลอดภัย: {product.get('CLAIM_POLICY_CLASS', '')}"
        )
        self.update_gpt1_prompt_preview()
        self.set_coach(1, "เลือกสินค้าแล้ว", "ตรวจรายละเอียดสินค้า ตั้งจำนวนโพสต์ และเลือกเป้าหมายโพสต์ แล้วกดคัดลอกคำสั่ง GPT1")

    def set_stage(self, stage: int) -> None:
        for index, badge in enumerate(self.step_badges, start=1):
            badge.set_active(index == stage)
        if hasattr(self, "tabs"):
            tab_index = max(0, min(4, stage - 1))
            if self.tabs.currentIndex() != tab_index:
                self.tabs.setCurrentIndex(tab_index)

    def on_tab_changed(self, index: int) -> None:
        for step_index, badge in enumerate(self.step_badges, start=1):
            badge.set_active(step_index == index + 1)

    def set_coach(self, stage: int, title: str, text: str) -> None:
        self.set_stage(stage)
        self.coach_title.setText(title)
        self.coach_text.setText(text)
        self.next_action.setText(
            {
                1: "ขั้นต่อไป: ตรวจสินค้า ตั้งจำนวนโพสต์ แล้วกด “คัดลอกคำสั่ง GPT1”",
                2: "ขั้นต่อไป: วางคำสั่งใน GPT1 แล้วบันทึกคำตอบเป็นไฟล์ .md หรือ .txt",
                3: "ขั้นต่อไป: วางไฟล์คำตอบจาก GPT1 ในโฟลเดอร์ แล้วกด “ตรวจไฟล์และเตรียมส่งต่อ”",
                4: "ขั้นต่อไป: รอผลการตรวจไฟล์",
                5: "ขั้นต่อไป: คัดลอกคำสั่ง GPT2 สำหรับไฟล์ที่ผ่านการตรวจ",
            }.get(stage, "ขั้นต่อไป: ทำตามคำแนะนำในตัวช่วยบอกขั้นตอน")
        )

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
        self.set_coach(1, f"ตั้งจำนวนโพสต์ = {value} แล้ว", f"โปรแกรมจะสร้างคำสั่ง GPT1 ให้สร้าง {value} รายการ")

    def normalize_n_from_input(self) -> None:
        self.set_post_count(self.get_post_count())

    def adjust_n(self, delta: int) -> None:
        self.set_post_count(self.get_post_count() + delta)

    def gpt1_prompt_text(self) -> str:
        lines = [
            f"SKU: {self.current_sku()}",
            f"NUMBER_OF_ROWS: {self.get_post_count()}",
            f"PLATFORM: {self.platform_combo.currentData()}",
            f"CAMPAIGN_GOAL: {self.goal_combo.currentData()}",
        ]
        if self.duration_combo.currentData() != "AUTO":
            lines.append(f"CAMPAIGN_DURATION: {self.duration_combo.currentData()}")
        for box, token in self.flag_boxes:
            if box.isChecked():
                lines.append(token)
        return "\n".join(lines)

    def update_gpt1_prompt_preview(self) -> None:
        if hasattr(self, "gpt1_prompt_preview"):
            self.gpt1_prompt_preview.setPlainText(self.gpt1_prompt_text())

    def copy_gpt1_prompt(self) -> None:
        self.normalize_n_from_input()
        QGuiApplication.clipboard().setText(self.gpt1_prompt_text())
        self.set_coach(2, "คัดลอกคำสั่ง GPT1 แล้ว", "นำไปวางใน GPT1 แล้วบันทึกคำตอบทั้งหมดเป็นไฟล์ .md หรือ .txt ในโฟลเดอร์คำตอบ GPT1")
        QMessageBox.information(self, "คัดลอกแล้ว", "คัดลอกคำสั่ง GPT1 แล้ว")

    def sku_raw_folder(self) -> Path:
        return OPERATOR_WORKSPACE_ROOT / self.current_sku() / "raw"

    def create_or_open_sku_workspace(self) -> None:
        folder = self.sku_raw_folder()
        folder.mkdir(parents=True, exist_ok=True)
        self.selected_folder = folder
        self.input_folder.setText(str(folder))
        raw_files = discover_raw_files(folder)
        has_raw = len(raw_files) > 0
        self.raw_count.setText(str(len(raw_files)))
        self.clean_button.setEnabled(has_raw)
        self.command_clean_button.setEnabled(has_raw)
        self.set_action_buttons(False)
        self.set_coach(3, "เปิดโฟลเดอร์คำตอบ GPT1 แล้ว", "บันทึกคำตอบจาก GPT1 เป็นไฟล์ .md หรือ .txt ในโฟลเดอร์นี้ จากนั้นกดตรวจไฟล์และเตรียมส่งต่อ")
        self.open_path(folder)

    def toggle_advanced(self, checked: bool) -> None:
        self.allow_visual.setVisible(checked)
        self.allow_angle.setVisible(checked)

    def choose_folder(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "เลือกโฟลเดอร์ที่เก็บคำตอบจาก GPT1")
        if not folder:
            return
        self.selected_folder = Path(folder)
        self.input_folder.setText(str(self.selected_folder))
        self.reset_results_only()
        try:
            raw_files = discover_raw_files(self.selected_folder)
        except Exception as exc:  # noqa: BLE001
            QMessageBox.critical(self, "เปิดโฟลเดอร์ไม่ได้", str(exc))
            return
        has_raw = len(raw_files) > 0
        self.raw_count.setText(str(len(raw_files)))
        self.clean_button.setEnabled(has_raw)
        self.command_clean_button.setEnabled(has_raw)
        if has_raw:
            self.set_coach(3, f"พบไฟล์จาก GPT1 {len(raw_files)} ไฟล์", f"กดตรวจไฟล์และเตรียมส่งต่อ โปรแกรมจะตรวจว่ามี {self.get_post_count()} รายการตามที่กำหนดไว้")
        else:
            self.set_coach(3, "ยังไม่พบไฟล์จาก GPT1", "นำคำตอบจาก GPT1 ไปบันทึกเป็นไฟล์ .md หรือ .txt ในโฟลเดอร์นี้ แล้วเปิดโฟลเดอร์อีกครั้ง")

    def reset_results_only(self) -> None:
        self.results = []
        self.summary = None
        self.table.setRowCount(0)
        self.preview.setPlainText("เลือกโฟลเดอร์แล้ว กดตรวจไฟล์และเตรียมส่งต่อเพื่อเริ่มทำงาน")
        self.pass_count.setText("0")
        self.fail_count.setText("0")
        self.selected_count.setText("0")
        self.prompt_count.setText("0")
        self.progress.setValue(0)
        self.results_empty.setVisible(True)
        self.set_action_buttons(False)

    def run_cleaner(self) -> None:
        if self.selected_folder is None:
            QMessageBox.warning(self, "ยังไม่ได้เลือกโฟลเดอร์", "กรุณาเปิดหรือเลือกโฟลเดอร์คำตอบ GPT1 ก่อน")
            return
        self.normalize_n_from_input()
        self.clean_button.setEnabled(False)
        self.command_clean_button.setEnabled(False)
        self.table.setRowCount(0)
        self.results_empty.setText("กำลังตรวจไฟล์และเตรียมข้อมูลส่งต่อ...")
        self.results_empty.setVisible(True)
        self.preview.setPlainText("กำลังประมวลผล โปรดรอจนกว่าผลการตรวจจะแสดงว่าผ่านหรือไม่ผ่าน")
        self.progress.setValue(10)
        self.set_action_buttons(False)
        self.set_coach(4, "กำลังตรวจไฟล์และเตรียมส่งต่อ", f"โปรแกรมกำลังเตรียมไฟล์ที่ตรวจผ่านแล้ว และคำสั่ง GPT2 จำนวน {self.get_post_count()} รายการต่อไฟล์")
        self.worker = CleanWorker(self.selected_folder, self.get_post_count(), self.allow_visual.isChecked(), self.allow_angle.isChecked())
        self.worker.finished_with_summary.connect(self.on_clean_finished)
        self.worker.failed.connect(self.on_clean_failed)
        self.worker.start()

    def on_clean_failed(self, message: str) -> None:
        self.clean_button.setEnabled(True)
        self.command_clean_button.setEnabled(True)
        self.progress.setValue(0)
        self.results_empty.setText("ตรวจไฟล์ไม่สำเร็จ: เปิดข้อความผิดพลาดแล้วแก้ไฟล์หรือสภาพแวดล้อม")
        self.set_coach(4, "ตรวจไฟล์ไม่สำเร็จ", "อ่านข้อความผิดพลาด แล้วแก้ไฟล์คำตอบจาก GPT1 หรือส่งข้อความผิดพลาดกลับมาตรวจ")
        QMessageBox.critical(self, "ตรวจไฟล์ไม่สำเร็จ", message)

    def on_clean_finished(self, summary: PipelineBatchSummary) -> None:
        self.clean_button.setEnabled(True)
        self.command_clean_button.setEnabled(True)
        self.summary = summary
        self.results = list(summary.results)
        self.progress.setValue(100)
        self.open_output_button.setEnabled(True)
        self.command_open_output_button.setEnabled(True)
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
            self.set_coach(5, "เตรียมคำสั่ง GPT2 เสร็จแล้ว", "เปิดแท็บเตรียมส่งเข้า GPT2 แล้วใช้คำสั่งที่โปรแกรมเตรียมไว้")
        elif self.results:
            self.set_action_buttons(False)
            self.open_output_button.setEnabled(True)
            self.command_open_output_button.setEnabled(True)
            self.preview.setPlainText("ยังไม่มีไฟล์ที่ผ่าน: เปิดรายงานของไฟล์ที่ไม่ผ่าน แล้วแก้ไฟล์คำตอบจาก GPT1 ก่อนส่งเข้า GPT2")
            self.set_coach(3, "ยังไม่มีไฟล์ที่ผ่าน", "เปิดรายงานของแต่ละไฟล์ที่ไม่ผ่าน แล้วแก้ไฟล์คำตอบจาก GPT1")
        else:
            self.set_action_buttons(False)
            self.preview.setPlainText("ไม่พบไฟล์จาก GPT1 ที่ใช้ได้ในโฟลเดอร์นี้")
            self.set_coach(3, "ไม่พบไฟล์จาก GPT1", "เพิ่มไฟล์ .md หรือ .txt จาก GPT1 แล้วเลือกโฟลเดอร์อีกครั้ง")

    def selected_result(self) -> CleanResult | None:
        selected = self.table.selectionModel().selectedRows()
        if not selected:
            return None
        row = selected[0].row()
        return self.results[row] if 0 <= row < len(self.results) else None

    def on_selection_changed(self) -> None:
        result = self.selected_result()
        if result is None:
            self.set_action_buttons(False)
            return
        if result.status != "PASS":
            self.set_action_buttons(False)
            self.open_report_button.setEnabled(True)
            self.preview.setPlainText("ไฟล์นี้ยังไม่ผ่าน: เปิดรายงานก่อน ห้ามส่งเข้า GPT2")
            self.set_coach(3, "ไฟล์นี้ยังไม่ผ่าน", "อย่าส่งไฟล์นี้เข้า GPT2 ให้เปิดรายงานแล้วแก้ก่อน")
            return
        self.set_action_buttons(True)
        try:
            selected_rows = read_clean_rows(result.selected_file) if result.selected_file else []
            first_prompt = read_first_prompt(result.prompt_folder)
            preview_text = "รายการที่พร้อมส่งเข้า GPT2:\n\n" + "\n".join(selected_rows[: min(10, len(selected_rows))])
            if len(selected_rows) > 10:
                preview_text += f"\n\n... ยังมีอีก {len(selected_rows) - 10} รายการ"
            if first_prompt:
                preview_text += "\n\nตัวอย่างคำสั่ง GPT2 รายการแรก:\n\n" + first_prompt
            self.preview.setPlainText(preview_text)
        except Exception as exc:  # noqa: BLE001
            self.preview.setPlainText(f"อ่านผลลัพธ์ไม่ได้: {exc}")
        self.set_coach(5, "ไฟล์นี้ผ่านและพร้อมส่งเข้า GPT2", "กดคัดลอกคำสั่ง GPT2 รายการแรก หรือเปิดโฟลเดอร์คำสั่ง GPT2 เพื่อทำต่อทีละรายการ")

    def set_action_buttons(self, enabled: bool) -> None:
        for button in self.gpt2_buttons:
            button.setEnabled(enabled)
        output_enabled = enabled and self.summary is not None
        self.open_output_button.setEnabled(output_enabled)
        self.command_open_output_button.setEnabled(output_enabled)

    def copy_first_prompt(self) -> None:
        result = self.selected_result()
        if result is None or result.status != "PASS":
            QMessageBox.warning(self, "ยังไม่พร้อม", "กรุณาเลือกไฟล์ที่ผ่านการตรวจก่อน")
            return
        prompt = read_first_prompt(result.prompt_folder)
        if not prompt:
            QMessageBox.warning(self, "ไม่พบคำสั่ง", "ไม่พบไฟล์คำสั่ง GPT2 สำหรับรายการนี้")
            return
        QGuiApplication.clipboard().setText(prompt)
        self.set_coach(5, "คัดลอกคำสั่ง GPT2 แล้ว", "วางคำสั่งนี้ใน GPT2 แล้วทำรายการถัดไปจากโฟลเดอร์คำสั่ง")
        QMessageBox.information(self, "คัดลอกแล้ว", "คัดลอกคำสั่ง GPT2 รายการแรกแล้ว")

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
            QMessageBox.warning(self, "ไม่พบไฟล์", str(path))
            return
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(path)))

    def reset_workflow(self) -> None:
        self.results = []
        self.summary = None
        self.worker = None
        self.selected_folder = None
        self.input_folder.clear()
        self.table.setRowCount(0)
        self.results_empty.setText("ยังไม่มีผลลัพธ์: คัดลอกคำสั่ง GPT1 → บันทึกคำตอบเป็นไฟล์ .md/.txt → เปิดโฟลเดอร์สำหรับวางคำตอบ → ตรวจไฟล์และเตรียมส่งต่อ")
        self.results_empty.setVisible(True)
        self.preview.setPlainText("พื้นที่นี้จะแสดงผลหลังไฟล์ผ่านการตรวจ:\n- รายการที่เตรียมไว้\n- คำสั่ง GPT2 รายการแรก\n- คำแนะนำขั้นถัดไป")
        self.raw_count.setText("0")
        self.pass_count.setText("0")
        self.fail_count.setText("0")
        self.selected_count.setText("0")
        self.prompt_count.setText("0")
        self.progress.setValue(0)
        self.clean_button.setEnabled(False)
        self.command_clean_button.setEnabled(False)
        self.open_output_button.setEnabled(False)
        self.command_open_output_button.setEnabled(False)
        self.set_action_buttons(False)
        self.set_coach(1, "เลือกชื่อสินค้าได้เลย ไม่ต้องจำรหัสสินค้า", "โปรแกรมจะแปลงชื่อสินค้าที่เลือกเป็นรหัส SKU ให้เอง")


def main() -> int:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
