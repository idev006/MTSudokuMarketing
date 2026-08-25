from __future__ import annotations

import csv
import sys
from dataclasses import dataclass
from pathlib import Path

from PySide6.QtCore import Qt, QThread, QUrl, Signal
from PySide6.QtGui import QAction, QDesktopServices, QGuiApplication, QIcon
from PySide6.QtWidgets import (
    QApplication, QCheckBox, QComboBox, QFileDialog, QFrame, QGridLayout, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QListWidget, QListWidgetItem, QMainWindow,
    QMessageBox, QPlainTextEdit, QProgressBar, QPushButton, QScrollArea, QSizePolicy,
    QTabWidget, QTableWidget, QTableWidgetItem, QTextEdit, QVBoxLayout, QWidget,
)

try:
    from .pipeline_service import (
        DEFAULT_POST_COUNT, MAX_POST_COUNT, MIN_POST_COUNT, CleanResult,
        PipelineBatchSummary, clean_folder, discover_raw_files,
    )
except ImportError:
    from pipeline_service import (  # type: ignore
        DEFAULT_POST_COUNT, MAX_POST_COUNT, MIN_POST_COUNT, CleanResult,
        PipelineBatchSummary, clean_folder, discover_raw_files,
    )


@dataclass(frozen=True)
class Choice:
    label: str
    value: str
    help_text: str = ""


PLATFORM_CHOICES = [
    Choice("ให้ระบบเลือกช่องทางให้", "AUTO"),
    Choice("Facebook", "FACEBOOK"),
    Choice("LINE Official Account", "LINE_OA"),
    Choice("Marketplace", "MARKETPLACE"),
    Choice("หน้าเว็บสินค้า", "LANDING_PAGE"),
]

CAMPAIGN_GOAL_CHOICES = [
    Choice("ให้ระบบเลือกเป้าหมายให้", "AUTO"),
    Choice("ทำให้คนรู้จักสินค้า", "BUILD_AWARENESS"),
    Choice("ให้ข้อมูลและอธิบายสินค้า", "EDUCATE"),
    Choice("ชวนให้คนมีส่วนร่วม", "CREATE_ENGAGEMENT"),
    Choice("แสดงคุณค่าและจุดเด่นของสินค้า", "SHOW_PRODUCT_VALUE"),
    Choice("สร้างความน่าเชื่อถือ", "BUILD_TRUST"),
    Choice("ช่วยให้ลูกค้าสนใจมากขึ้น", "DRIVE_CONSIDERATION"),
    Choice("กระตุ้นการตัดสินใจซื้อ", "DRIVE_CONVERSION"),
    Choice("ดูแลลูกค้าเดิมและชวนซื้อเพิ่ม", "RETENTION_CROSS_SELL"),
]

CAMPAIGN_DURATION_CHOICES = [
    Choice("ไม่กำหนดระยะเวลา", "AUTO"),
    Choice("7 วัน", "7_DAYS"),
    Choice("14 วัน", "14_DAYS"),
    Choice("30 วัน", "30_DAYS"),
    Choice("60 วัน", "60_DAYS"),
    Choice("90 วัน", "90_DAYS"),
]

FLAG_CHOICES = [
    ("auto_platform_resolution", "ให้ระบบเลือกช่องทางและรูปแบบให้เหมาะสม", "AUTO_PLATFORM_RESOLUTION"),
    ("controlled_vocab_validation", "ตรวจความถูกต้องของคำที่ระบบใช้", "CONTROLLED_VOCAB_VALIDATION"),
    ("sku_lookup_prompt_assembly", "ดึงข้อมูลสินค้าจากฐานข้อมูลอัตโนมัติ", "SKU_LOOKUP_PROMPT_ASSEMBLY"),
    ("knowledge_manifest_required", "ตรวจข้อมูลอ้างอิงก่อนเริ่มสร้าง", "KNOWLEDGE_MANIFEST_REQUIRED"),
]


class PathManager:
    def __init__(self) -> None:
        self.app_dir = Path(__file__).resolve().parent
        self.content_os_root = self.app_dir.parents[1]
        self.repo_root = self.content_os_root.parent
        self.sku_lookup = self.content_os_root / "schemas" / "sku_lookup_v1.tsv"
        self.operator_workspace = self.repo_root / "_operator_workspace"
        self.icon_dir = self.app_dir / "assets" / "icons"

    def icon_path(self, name: str) -> Path:
        return self.icon_dir / name

    def icon_url(self, name: str) -> str:
        return self.icon_path(name).as_posix()


PATHS = PathManager()


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
            self.finished_with_summary.emit(clean_folder(
                self.input_folder,
                expected_rows=self.post_count,
                target_posts=self.post_count,
                allow_visual_concentration=self.allow_visual,
                allow_angle_concentration=self.allow_angle,
            ))
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
    if not PATHS.sku_lookup.exists():
        return []
    lines = PATHS.sku_lookup.read_text(encoding="utf-8").splitlines()
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
    name = row.get("THAI_NAME") or row.get("PRODUCT_NAME") or "ไม่พบชื่อสินค้า"
    return f"{name} — {row.get('SKU', '')}"


def read_tsv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle, delimiter="\t")]


def prompt_title(prompt_path: Path, order: int, rows: list[dict[str, str]]) -> str:
    row = rows[order - 1] if order - 1 < len(rows) else {}
    visual = row.get("VISUAL_TYPE", "")
    headline = row.get("HEADLINE", "")
    row_id = row.get("ROW_ID", prompt_path.stem)
    useful = " — ".join(part for part in [visual, headline] if part)
    return f"{order:02d}. {useful or row_id}"


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("เครื่องมือเตรียมคอนเทนต์โซเชียล BiiigBee")
        self.resize(1420, 900)
        self.products = load_products()
        self.results: list[CleanResult] = []
        self.summary: PipelineBatchSummary | None = None
        self.worker: CleanWorker | None = None
        self.selected_folder: Path | None = None
        self.current_prompt_files: list[Path] = []
        self.copied_prompt_paths: set[Path] = set()
        self.setStyleSheet(self.build_stylesheet())

        self.step_badges = [
            StepBadge("1", "เลือกสินค้าและจำนวนโพสต์"),
            StepBadge("2", "คัดลอกคำสั่ง GPT1"),
            StepBadge("3", "เก็บคำตอบจาก GPT1"),
            StepBadge("4", "ตรวจไฟล์และเตรียมคำสั่ง GPT2"),
            StepBadge("5", "ส่งเข้า GPT2 และตรวจงาน"),
        ]
        self.next_action = QLabel("ขั้นต่อไป: เลือกสินค้าและจำนวนโพสต์ แล้วกด “คัดลอกคำสั่ง GPT1”")
        self.next_action.setObjectName("NextAction")
        self.next_action.setWordWrap(True)

        self.product_combo = QComboBox()
        self.product_combo.setMinimumWidth(620)
        for product in self.products or [{"SKU": "<SKU>", "THAI_NAME": "ไม่พบไฟล์รายการสินค้า"}]:
            self.product_combo.addItem(product_display(product), product)
        self.product_combo.currentIndexChanged.connect(self.on_product_changed)
        self.product_card = QTextEdit()
        self.product_card.setReadOnly(True)
        self.product_card.setMinimumHeight(120)

        self.n_value = QLineEdit(str(DEFAULT_POST_COUNT))
        self.n_value.setObjectName("NValue")
        self.n_value.setFixedWidth(88)
        self.n_value.setAlignment(Qt.AlignCenter)
        self.n_value.editingFinished.connect(self.normalize_n_from_input)
        self.minus_button = self.stepper_button("minus.svg", "ลดจำนวนโพสต์", lambda: self.adjust_n(-1))
        self.plus_button = self.stepper_button("plus.svg", "เพิ่มจำนวนโพสต์", lambda: self.adjust_n(1))
        self.preset_buttons: list[QPushButton] = []
        for preset in (10, 20, 30, 60):
            button = QPushButton(str(preset))
            button.setObjectName("PresetButton")
            button.clicked.connect(lambda _checked=False, value=preset: self.set_post_count(value))
            self.preset_buttons.append(button)

        self.platform_combo = self.choice_combo(PLATFORM_CHOICES)
        self.goal_combo = self.choice_combo(CAMPAIGN_GOAL_CHOICES)
        self.duration_combo = self.choice_combo(CAMPAIGN_DURATION_CHOICES)
        for combo in (self.platform_combo, self.goal_combo, self.duration_combo):
            combo.currentIndexChanged.connect(self.update_gpt1_prompt_preview)

        self.flag_checks: dict[str, QCheckBox] = {}
        for key, label, _token in FLAG_CHOICES:
            check = QCheckBox(label)
            check.stateChanged.connect(self.update_gpt1_prompt_preview)
            self.flag_checks[key] = check

        self.gpt1_prompt_preview = QPlainTextEdit()
        self.gpt1_prompt_preview.setReadOnly(True)
        self.gpt1_prompt_preview.setMinimumHeight(160)

        self.copy_gpt1_button = self.action_button("1. คัดลอกคำสั่ง GPT1", self.copy_gpt1_prompt, "SuccessButton")
        self.workspace_button = self.action_button("เปิดโฟลเดอร์สำหรับวางคำตอบ GPT1", self.create_or_open_sku_workspace, "CommandButton")
        self.choose_folder_button = self.action_button("2. เลือกโฟลเดอร์คำตอบ GPT1", self.choose_folder, "CommandButton")
        self.clean_button = self.action_button("3. ตรวจไฟล์และเตรียมคำสั่ง GPT2", self.run_cleaner, "PrimaryButton")
        self.clean_button.setEnabled(False)
        self.open_output_button = self.action_button("เปิดโฟลเดอร์ผลลัพธ์", self.open_output_folder, "CommandButton")
        self.open_output_button.setEnabled(False)
        self.reset_button = self.action_button("เริ่มใหม่", self.reset_workflow, "DangerButton")
        self.command_copy_gpt1_button = self.action_button("1. คัดลอกคำสั่ง GPT1", self.copy_gpt1_prompt, "SuccessButton")
        self.command_workspace_button = self.action_button("เปิดโฟลเดอร์สำหรับวางคำตอบ GPT1", self.create_or_open_sku_workspace, "CommandButton")
        self.command_choose_folder_button = self.action_button("2. เลือกโฟลเดอร์คำตอบ GPT1", self.choose_folder, "CommandButton")
        self.command_clean_button = self.action_button("3. ตรวจไฟล์และเตรียมคำสั่ง GPT2", self.run_cleaner, "PrimaryButton")
        self.command_clean_button.setEnabled(False)
        self.command_open_output_button = self.action_button("เปิดโฟลเดอร์ผลลัพธ์", self.open_output_folder, "CommandButton")
        self.command_open_output_button.setEnabled(False)
        self.command_reset_button = self.action_button("เริ่มใหม่", self.reset_workflow, "DangerButton")

        self.input_folder = QLineEdit()
        self.input_folder.setReadOnly(True)
        self.input_folder.setPlaceholderText("ยังไม่ได้เลือกโฟลเดอร์ที่เก็บคำตอบจาก GPT1")
        self.advanced_toggle = QCheckBox("แสดงตัวเลือกตรวจไฟล์ขั้นสูง")
        self.allow_visual = QCheckBox("อนุญาตให้รูปแบบภาพซ้ำมากขึ้น")
        self.allow_angle = QCheckBox("อนุญาตให้มุมขายซ้ำมากขึ้น")
        self.allow_visual.setVisible(False)
        self.allow_angle.setVisible(False)
        self.advanced_toggle.toggled.connect(self.toggle_advanced)
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)

        self.raw_count = self.metric_value("0")
        self.pass_count = self.metric_value("0")
        self.fail_count = self.metric_value("0")
        self.selected_count = self.metric_value("0")
        self.prompt_count = self.metric_value("0")
        self.coach_title = QLabel("เลือกชื่อสินค้าได้เลย ไม่ต้องจำรหัสสินค้า")
        self.coach_title.setObjectName("CoachTitle")
        self.coach_text = QLabel("โปรแกรมจะแปลงชื่อสินค้าที่เลือกเป็นรหัส SKU ให้เอง")
        self.coach_text.setObjectName("CoachText")
        self.coach_text.setWordWrap(True)

        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(["สถานะ", "ไฟล์", "จำนวนแถว", "รายการที่เตรียมไว้", "คำสั่ง GPT2", "สิ่งที่ควรทำต่อ"])
        for col in (0, 2, 3, 4):
            self.table.horizontalHeader().setSectionResizeMode(col, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.itemSelectionChanged.connect(self.on_result_selection_changed)
        self.results_empty = QLabel("ยังไม่มีผลลัพธ์: คัดลอกคำสั่ง GPT1 → บันทึกคำตอบเป็นไฟล์ .md/.txt → ตรวจไฟล์")
        self.results_empty.setObjectName("EmptyState")
        self.results_empty.setAlignment(Qt.AlignCenter)

        self.prompt_list = QListWidget()
        self.prompt_list.setMinimumWidth(420)
        self.prompt_list.itemSelectionChanged.connect(self.on_prompt_selection_changed)
        self.prompt_preview = QPlainTextEdit()
        self.prompt_preview.setReadOnly(True)
        self.prompt_preview.setPlainText("เมื่อไฟล์ผ่านการตรวจ โปรแกรมจะแสดงคำสั่ง GPT2 ที่พร้อมคัดลอกที่นี่\n\nผู้ใช้ไม่ต้องคัดลอก TSV row เอง")
        self.copy_selected_prompt_button = self.action_button("คัดลอกคำสั่งนี้", self.copy_selected_gpt2_prompt, "SuccessButton")
        self.copy_first_prompt_button = self.action_button("คัดลอกคำสั่งแรก", self.copy_first_gpt2_prompt, "CommandButton")
        self.next_prompt_button = self.action_button("ไปคำสั่งถัดไป", self.select_next_prompt, "CommandButton")
        self.open_prompts_button = self.action_button("เปิดโฟลเดอร์คำสั่ง GPT2", self.open_prompt_folder, "CommandButton")
        self.open_selected_rows_button = self.action_button("เปิดรายการที่เตรียมไว้", self.open_selected_file, "CommandButton")
        self.open_clean_button = self.action_button("เปิดไฟล์ที่ตรวจผ่านแล้ว", self.open_clean_file, "CommandButton")
        self.open_report_button = self.action_button("เปิดรายงานการตรวจ", self.open_report_file, "CommandButton")
        self.gpt2_buttons = [self.copy_selected_prompt_button, self.copy_first_prompt_button, self.next_prompt_button, self.open_prompts_button, self.open_selected_rows_button, self.open_clean_button, self.open_report_button]
        self.set_gpt2_actions_enabled(False)

        self.tabs = QTabWidget()
        self.tabs.currentChanged.connect(self.on_tab_changed)
        self.setCentralWidget(self.build_ui())
        self.on_product_changed()
        self.update_gpt1_prompt_preview()
        self.set_stage(1)
        quit_action = QAction("Exit", self)
        quit_action.triggered.connect(self.close)
        self.menuBar().addAction(quit_action)

    def build_stylesheet(self) -> str:
        chevron = PATHS.icon_url("chevron-down.svg")
        check = PATHS.icon_url("check.svg")
        return f'''
            QMainWindow {{ background: #f6f8fb; color: #10203a; }} QLabel {{ color: #10203a; }}
            QLabel#AppTitle {{ font-size: 24px; font-weight: 800; color: #172033; }} QLabel#AppSubtitle {{ font-size: 13px; color: #556070; }}
            QLabel#PanelTitle {{ font-size: 18px; font-weight: 800; color: #14315c; }} QLabel#PanelHelp {{ font-size: 13px; color: #394a62; }}
            QLabel#CoachTitle {{ font-size: 18px; font-weight: 800; color: #14315c; }} QLabel#CoachText {{ font-size: 14px; color: #26364d; }}
            QLabel#NextAction {{ font-size: 20px; font-weight: 800; color: #0f5132; background: #dcfce7; border: 1px solid #86efac; border-radius: 12px; padding: 14px; }}
            QLabel#MetricBig {{ font-size: 22px; font-weight: 800; color: #14315c; }} QLabel#MetricLabel {{ font-size: 12px; color: #5f6f86; }} QLabel#EmptyState {{ color: #65758c; font-size: 14px; padding: 18px; }}
            QFrame#Panel, QFrame#CoachCard, QFrame#CommandBar {{ background: #ffffff; border: 1px solid #dbe3ef; border-radius: 12px; }}
            QFrame#StepBadge {{ background: #eef3fb; border: 1px solid #d5dfef; border-radius: 10px; }} QFrame#StepBadge[active="true"] {{ background: #dff0ff; border: 2px solid #3b82f6; }}
            QLabel#StepNumber {{ font-size: 18px; font-weight: 800; color: #1d4ed8; min-width: 26px; }} QLabel#StepTitle {{ font-size: 13px; color: #26364d; }}
            QPushButton {{ color: #10203a; padding: 9px 14px; border-radius: 8px; background: #e7edf7; border: 1px solid #cbd6e7; }} QPushButton:hover {{ background: #dbeafe; border: 1px solid #60a5fa; }} QPushButton:pressed {{ background: #bfdbfe; }} QPushButton:disabled {{ color: #7c8797; background: #edf1f7; border: 1px solid #d8e0ee; }}
            QPushButton#PrimaryButton {{ background: #2563eb; color: #ffffff; font-size: 15px; font-weight: 800; border: 1px solid #1d4ed8; padding: 12px 18px; }} QPushButton#SuccessButton {{ background: #059669; color: #ffffff; font-weight: 800; border: 1px solid #047857; }} QPushButton#DangerButton {{ background: #fee2e2; color: #991b1b; border: 1px solid #fecaca; }}
            QPushButton#StepperButton {{ min-width: 40px; max-width: 40px; min-height: 40px; max-height: 40px; border-radius: 8px; padding: 0; background: #eef3fb; }} QPushButton#PresetButton {{ padding: 7px 10px; font-weight: 800; }} QPushButton#CommandButton {{ font-size: 14px; font-weight: 800; padding: 12px 16px; }}
            QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, QListWidget {{ color: #10203a; background: #ffffff; border: 1px solid #94a3b8; border-radius: 7px; padding: 8px; selection-background-color: #bfdbfe; selection-color: #0f172a; }}
            QComboBox {{ min-height: 28px; color: #0f172a; background-color: #ffffff; }} QComboBox::drop-down {{ border-left: 1px solid #94a3b8; width: 32px; background: #e7edf7; border-top-right-radius: 7px; border-bottom-right-radius: 7px; }} QComboBox::down-arrow {{ image: url("{chevron}"); width: 14px; height: 14px; }}
            QComboBox QAbstractItemView {{ color: #0f172a; background-color: #ffffff; selection-background-color: #2563eb; selection-color: #ffffff; outline: 0; border: 1px solid #94a3b8; padding: 6px; }}
            QLineEdit:read-only {{ background: #f8fafc; color: #334155; }} QLineEdit#NValue {{ font-size: 18px; font-weight: 800; }}
            QTableWidget {{ color: #10203a; background: #ffffff; border: 1px solid #dbe3ef; border-radius: 8px; gridline-color: #edf2f7; selection-background-color: #dbeafe; selection-color: #10203a; }} QHeaderView::section {{ background: #334155; color: #ffffff; padding: 6px; border: 0; }}
            QListWidget::item {{ padding: 8px; border-bottom: 1px solid #eef2f7; }} QListWidget::item:selected {{ background: #dbeafe; color: #10203a; }}
            QTabWidget::pane {{ border: 1px solid #dbe3ef; border-radius: 8px; background: #ffffff; }} QTabBar::tab {{ background: #e7edf7; color: #10203a; border: 1px solid #cbd6e7; padding: 10px 18px; margin-right: 4px; border-top-left-radius: 8px; border-top-right-radius: 8px; }} QTabBar::tab:selected {{ background: #2563eb; color: #ffffff; font-weight: 800; }}
            QProgressBar {{ color: #10203a; border: 1px solid #cbd6e7; border-radius: 7px; text-align: center; background: #ffffff; }} QProgressBar::chunk {{ background: #2563eb; border-radius: 6px; }}
            QCheckBox {{ spacing: 10px; color: #10203a; font-size: 13px; padding: 4px; }} QCheckBox::indicator {{ width: 18px; height: 18px; border-radius: 4px; border: 1px solid #94a3b8; background: #ffffff; }} QCheckBox::indicator:hover {{ border: 2px solid #2563eb; background: #f8fbff; }} QCheckBox::indicator:checked {{ image: url("{check}"); border: 1px solid #1d4ed8; background: #2563eb; }} QCheckBox::indicator:checked:hover {{ image: url("{check}"); border: 1px solid #1e40af; background: #1d4ed8; }} QCheckBox::indicator:disabled {{ border: 1px solid #cbd5e1; background: #f1f5f9; }}
        '''

    def build_ui(self) -> QWidget:
        root = QWidget(); layout = QVBoxLayout(root); layout.setContentsMargins(8, 8, 8, 8); layout.setSpacing(8)
        title = QLabel("เครื่องมือเตรียมคอนเทนต์โซเชียล BiiigBee"); title.setObjectName("AppTitle")
        subtitle = QLabel("เลือกสินค้า → คัดลอกคำสั่งให้ GPT1 → วางคำตอบจาก GPT1 → ตรวจไฟล์ → คัดลอกคำสั่งให้ GPT2"); subtitle.setObjectName("AppSubtitle")
        layout.addWidget(title); layout.addWidget(subtitle)
        steps = QHBoxLayout()
        for badge in self.step_badges: steps.addWidget(badge)
        layout.addLayout(steps); layout.addWidget(self.next_action); layout.addWidget(self.build_command_bar())
        self.tabs.addTab(self.wrap_scroll(self.build_gpt1_tab()), "1. สร้างคำสั่ง GPT1")
        self.tabs.addTab(self.wrap_scroll(self.build_import_tab()), "2. นำคำตอบจาก GPT1 เข้ามา")
        self.tabs.addTab(self.wrap_scroll(self.build_results_tab()), "3. ผลการตรวจ")
        self.tabs.addTab(self.wrap_scroll(self.build_handoff_tab()), "4. คำสั่ง GPT2 ที่พร้อมใช้")
        self.tabs.addTab(self.wrap_scroll(self.build_review_tab()), "5. ตรวจงานก่อนใช้จริง")
        layout.addWidget(self.tabs, stretch=1)
        return root

    def build_command_bar(self) -> QFrame:
        panel = QFrame(); panel.setObjectName("CommandBar"); layout = QHBoxLayout(panel); layout.setContentsMargins(10, 8, 10, 8)
        layout.addWidget(QLabel("ปุ่มหลัก:")); layout.addWidget(self.command_copy_gpt1_button); layout.addWidget(self.command_workspace_button); layout.addWidget(self.command_choose_folder_button); layout.addWidget(self.command_clean_button); layout.addWidget(self.command_open_output_button); layout.addStretch(1); layout.addWidget(self.command_reset_button)
        return panel

    def build_gpt1_tab(self) -> QWidget:
        panel = QFrame(); panel.setObjectName("Panel"); layout = QVBoxLayout(panel)
        title = QLabel("1. สร้างคำสั่งให้ GPT1"); title.setObjectName("PanelTitle")
        help_text = QLabel("เลือกสินค้า จำนวนโพสต์ และตัวเลือกที่ต้องการ โปรแกรมจะสร้างคำสั่งให้ GPT1 อัตโนมัติ"); help_text.setObjectName("PanelHelp"); help_text.setWordWrap(True)
        layout.addWidget(title); layout.addWidget(help_text)
        form = QGridLayout(); form.addWidget(QLabel("สินค้า"), 0, 0); form.addWidget(self.product_combo, 0, 1, 1, 4); form.addWidget(QLabel("รายละเอียดสินค้า"), 1, 0); form.addWidget(self.product_card, 1, 1, 1, 4); form.addWidget(QLabel("จำนวนโพสต์"), 2, 0)
        n_row = QHBoxLayout(); n_row.addWidget(self.minus_button); n_row.addWidget(self.n_value); n_row.addWidget(self.plus_button); n_row.addWidget(QLabel("เลือกเร็ว:"))
        for button in self.preset_buttons: n_row.addWidget(button)
        n_row.addStretch(1); form.addLayout(n_row, 2, 1, 1, 4)
        form.addWidget(QLabel("ช่องทางโพสต์"), 3, 0); form.addWidget(self.platform_combo, 3, 1); form.addWidget(QLabel("เป้าหมายของโพสต์"), 3, 2); form.addWidget(self.goal_combo, 3, 3); form.addWidget(QLabel("ระยะเวลาแคมเปญ"), 4, 0); form.addWidget(self.duration_combo, 4, 1)
        flags = QVBoxLayout()
        for key, _label, _token in FLAG_CHOICES: flags.addWidget(self.flag_checks[key])
        form.addLayout(flags, 4, 2, 1, 2); form.addWidget(QLabel("คำสั่งที่จะส่งให้ GPT1"), 5, 0); form.addWidget(self.gpt1_prompt_preview, 5, 1, 1, 4); form.addWidget(self.copy_gpt1_button, 6, 1, 1, 4); layout.addLayout(form)
        note = QLabel("หลัง GPT1 ตอบ ให้บันทึกคำตอบทั้งหมดเป็นไฟล์ .md หรือ .txt แล้วไปขั้นตอน 2"); note.setObjectName("PanelHelp"); note.setWordWrap(True); layout.addWidget(note); layout.addStretch(1); return panel

    def build_import_tab(self) -> QWidget:
        panel = QFrame(); panel.setObjectName("Panel"); layout = QVBoxLayout(panel)
        title = QLabel("2. นำคำตอบจาก GPT1 เข้ามาในโปรแกรม"); title.setObjectName("PanelTitle")
        help_text = QLabel("เลือกหรือเปิดโฟลเดอร์สำหรับวางคำตอบจาก GPT1 แล้วบันทึกไฟล์ .md หรือ .txt ไว้ในนั้น"); help_text.setObjectName("PanelHelp"); help_text.setWordWrap(True)
        layout.addWidget(title); layout.addWidget(help_text)
        form = QGridLayout(); form.addWidget(QLabel("โฟลเดอร์คำตอบ GPT1"), 0, 0); form.addWidget(self.input_folder, 0, 1); form.addWidget(self.workspace_button, 0, 2); form.addWidget(self.choose_folder_button, 0, 3); form.addWidget(self.clean_button, 1, 1, 1, 3); form.addWidget(self.progress, 2, 0, 1, 4); form.addWidget(self.advanced_toggle, 3, 1, 1, 3); form.addWidget(self.allow_visual, 4, 1, 1, 3); form.addWidget(self.allow_angle, 5, 1, 1, 3)
        layout.addLayout(form); layout.addWidget(self.build_status_panel()); layout.addStretch(1); return panel

    def build_results_tab(self) -> QWidget:
        panel = QFrame(); panel.setObjectName("Panel"); layout = QVBoxLayout(panel); title = QLabel("3. ผลการตรวจไฟล์"); title.setObjectName("PanelTitle"); layout.addWidget(title); layout.addWidget(self.results_empty); layout.addWidget(self.table, stretch=1); return panel

    def build_handoff_tab(self) -> QWidget:
        panel = QFrame(); panel.setObjectName("Panel"); layout = QVBoxLayout(panel)
        title = QLabel("4. คำสั่ง GPT2 ที่พร้อมใช้"); title.setObjectName("PanelTitle")
        help_text = QLabel("เลือกคำสั่งจากรายการด้านซ้าย แล้วกด “คัดลอกคำสั่งนี้” เพื่อนำไปวางใน GPT2 ทีละรายการ"); help_text.setObjectName("PanelHelp"); help_text.setWordWrap(True)
        layout.addWidget(title); layout.addWidget(help_text)
        actions = QHBoxLayout()
        for button in self.gpt2_buttons: actions.addWidget(button)
        actions.addStretch(1); actions.addWidget(self.open_output_button); layout.addLayout(actions)
        body = QHBoxLayout(); left = QVBoxLayout(); label = QLabel("รายการคำสั่ง GPT2"); label.setObjectName("PanelHelp"); left.addWidget(label); left.addWidget(self.prompt_list); body.addLayout(left, stretch=1)
        right = QVBoxLayout(); preview_label = QLabel("เนื้อหาคำสั่งที่เลือก"); preview_label.setObjectName("PanelHelp"); right.addWidget(preview_label); right.addWidget(self.prompt_preview); body.addLayout(right, stretch=2); layout.addLayout(body, stretch=1); return panel

    def build_review_tab(self) -> QWidget:
        panel = QFrame(); panel.setObjectName("Panel"); layout = QVBoxLayout(panel); title = QLabel("5. ตรวจงานก่อนนำไปใช้จริง"); title.setObjectName("PanelTitle"); layout.addWidget(title)
        text = QTextEdit(); text.setReadOnly(True); text.setPlainText("หลัง GPT2 ส่งผลลัพธ์ PASS / PASS_WITH_WARNING:\n\n1. ใช้ final image prompt ไปสร้างภาพ\n2. ตรวจภาพว่าตรงสินค้าและไม่มีข้อความเสี่ยง\n3. ตรวจ caption / headline / CTA ว่าอ่านเข้าใจง่าย\n4. เก็บ post package และอัปเดต inventory\n\nโปรแกรมนี้ยังไม่เผยแพร่โพสต์อัตโนมัติ และยังต้องมีคนตรวจงานก่อนใช้จริง")
        layout.addWidget(text, stretch=1); return panel

    def build_status_panel(self) -> QFrame:
        panel = QFrame(); panel.setObjectName("Panel"); layout = QVBoxLayout(panel); title = QLabel("ตัวช่วยบอกขั้นตอน"); title.setObjectName("PanelTitle"); layout.addWidget(title)
        card = QFrame(); card.setObjectName("CoachCard"); card_layout = QVBoxLayout(card); card_layout.addWidget(self.coach_title); card_layout.addWidget(self.coach_text); layout.addWidget(card)
        metrics = QHBoxLayout()
        for name, value in (("ไฟล์จาก GPT1", self.raw_count), ("ผ่าน", self.pass_count), ("ไม่ผ่าน", self.fail_count), ("รายการที่เตรียมไว้", self.selected_count), ("คำสั่ง GPT2", self.prompt_count)): metrics.addWidget(self.metric_box(name, value))
        layout.addLayout(metrics)
        guide = QLabel("ข้อควรจำ: คำตอบดิบจาก GPT1 ยังไม่ควรส่งต่อ ให้ใช้เฉพาะไฟล์ที่ผ่านการตรวจและคำสั่ง GPT2 ที่โปรแกรมสร้างให้เท่านั้น"); guide.setObjectName("PanelHelp"); guide.setWordWrap(True); layout.addWidget(guide); return panel

    def wrap_scroll(self, widget: QWidget) -> QScrollArea:
        scroll = QScrollArea(); scroll.setWidgetResizable(True); scroll.setFrameShape(QFrame.NoFrame); scroll.setWidget(widget); return scroll
    def action_button(self, text: str, handler, object_name: str | None = None) -> QPushButton:
        button = QPushButton(text); button.clicked.connect(handler)
        if object_name: button.setObjectName(object_name)
        return button
    def stepper_button(self, icon_name: str, tooltip: str, handler) -> QPushButton:
        button = QPushButton(); button.setObjectName("StepperButton"); button.setIcon(QIcon(str(PATHS.icon_path(icon_name)))); button.setToolTip(tooltip); button.clicked.connect(handler); return button
    def choice_combo(self, choices: list[Choice]) -> QComboBox:
        combo = QComboBox()
        for choice in choices: combo.addItem(choice.label, choice)
        combo.setMinimumWidth(260); return combo
    def current_choice_value(self, combo: QComboBox) -> str:
        data = combo.currentData(); return data.value if isinstance(data, Choice) else combo.currentText()
    def metric_value(self, text: str) -> QLabel:
        label = QLabel(text); label.setObjectName("MetricBig"); label.setAlignment(Qt.AlignCenter); return label
    def metric_box(self, title: str, value: QLabel) -> QFrame:
        frame = QFrame(); frame.setObjectName("CoachCard"); frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed); layout = QVBoxLayout(frame); label = QLabel(title); label.setObjectName("MetricLabel"); label.setAlignment(Qt.AlignCenter); layout.addWidget(value); layout.addWidget(label); return frame
    def current_product(self) -> dict[str, str]:
        data = self.product_combo.currentData(); return data if isinstance(data, dict) else {}
    def current_sku(self) -> str: return self.current_product().get("SKU") or "<SKU>"

    def on_product_changed(self) -> None:
        product = self.current_product(); self.product_card.setPlainText(f"สินค้า: {product.get('THAI_NAME') or product.get('PRODUCT_NAME', '')}\nSKU: {product.get('SKU', '')}\nช่วงชั้น: {product.get('GRADE_BAND', '')}\nระดับ: {product.get('DISPLAY_DIFFICULTY', '')}\nจำนวนโจทย์: {product.get('PUZZLE_COUNT', '')}\nเฉลย: {product.get('ANSWER_KEY_STATUS', '')}\nระดับการเคลม: {product.get('CLAIM_POLICY_CLASS', '')}"); self.update_gpt1_prompt_preview(); self.set_coach(1, "เลือกสินค้าแล้ว", "ตรวจรายละเอียดสินค้า ตั้งจำนวนโพสต์ แล้วกดคัดลอกคำสั่ง GPT1")
    def set_stage(self, stage: int) -> None:
        for index, badge in enumerate(self.step_badges, start=1): badge.set_active(index == stage)
        if hasattr(self, "tabs"):
            tab_index = max(0, min(4, stage - 1))
            if self.tabs.currentIndex() != tab_index: self.tabs.setCurrentIndex(tab_index)
    def on_tab_changed(self, index: int) -> None:
        for step_index, badge in enumerate(self.step_badges, start=1): badge.set_active(step_index == index + 1)
    def set_coach(self, stage: int, title: str, text: str) -> None:
        self.set_stage(stage); self.coach_title.setText(title); self.coach_text.setText(text); self.next_action.setText({1: "ขั้นต่อไป: ตรวจสินค้า ตั้งจำนวนโพสต์ แล้วกดคัดลอกคำสั่ง GPT1", 2: "ขั้นต่อไป: วางคำสั่งใน GPT1 แล้วบันทึกคำตอบเป็นไฟล์ .md หรือ .txt", 3: "ขั้นต่อไป: วางคำตอบจาก GPT1 ในโฟลเดอร์ แล้วกดตรวจไฟล์และเตรียมคำสั่ง GPT2", 4: "ขั้นต่อไป: รอผลว่าไฟล์ผ่านหรือไม่ผ่าน", 5: "ขั้นต่อไป: เลือกคำสั่ง GPT2 แล้วคัดลอกไปวางใน GPT2"}.get(stage, "ขั้นต่อไป: ทำตามคำแนะนำบนหน้าจอ"))
    def get_post_count(self) -> int:
        try: value = int(self.n_value.text().strip())
        except ValueError: value = DEFAULT_POST_COUNT
        return max(MIN_POST_COUNT, min(MAX_POST_COUNT, value))
    def set_post_count(self, value: int) -> None:
        value = max(MIN_POST_COUNT, min(MAX_POST_COUNT, value)); self.n_value.setText(str(value)); self.update_gpt1_prompt_preview(); self.set_coach(1, f"ตั้งจำนวนโพสต์ = {value} แล้ว", f"กดคัดลอกคำสั่ง GPT1 เพื่อสร้าง {value} รายการ")
    def normalize_n_from_input(self) -> None: self.set_post_count(self.get_post_count())
    def adjust_n(self, delta: int) -> None: self.set_post_count(self.get_post_count() + delta)
    def gpt1_prompt_text(self) -> str:
        lines = [f"SKU: {self.current_sku()}", f"NUMBER_OF_ROWS: {self.get_post_count()}", f"PLATFORM: {self.current_choice_value(self.platform_combo)}", f"CAMPAIGN_GOAL: {self.current_choice_value(self.goal_combo)}"]
        duration = self.current_choice_value(self.duration_combo)
        if duration != "AUTO": lines.append(f"CAMPAIGN_DURATION: {duration}")
        for key, _label, token in FLAG_CHOICES:
            if self.flag_checks[key].isChecked(): lines.append(token)
        return "\n".join(lines)
    def update_gpt1_prompt_preview(self) -> None:
        if hasattr(self, "gpt1_prompt_preview"): self.gpt1_prompt_preview.setPlainText(self.gpt1_prompt_text())
    def copy_gpt1_prompt(self) -> None:
        self.normalize_n_from_input(); QGuiApplication.clipboard().setText(self.gpt1_prompt_text()); self.set_coach(2, "คัดลอกคำสั่ง GPT1 แล้ว", "นำไปวางใน GPT1 แล้วบันทึกคำตอบเป็นไฟล์ .md หรือ .txt"); QMessageBox.information(self, "คัดลอกแล้ว", "คัดลอกคำสั่ง GPT1 แล้ว")
    def sku_raw_folder(self) -> Path: return PATHS.operator_workspace / self.current_sku() / "raw"
    def create_or_open_sku_workspace(self) -> None:
        folder = self.sku_raw_folder(); folder.mkdir(parents=True, exist_ok=True); self.selected_folder = folder; self.input_folder.setText(str(folder)); raw_files = discover_raw_files(folder); has_raw = len(raw_files) > 0; self.raw_count.setText(str(len(raw_files))); self.clean_button.setEnabled(has_raw); self.command_clean_button.setEnabled(has_raw); self.set_gpt2_actions_enabled(False); self.set_coach(3, "เปิดโฟลเดอร์สำหรับวางคำตอบ GPT1 แล้ว", "บันทึกคำตอบจาก GPT1 เป็นไฟล์ .md หรือ .txt ในโฟลเดอร์นี้"); self.open_path(folder)
    def toggle_advanced(self, checked: bool) -> None:
        self.allow_visual.setVisible(checked); self.allow_angle.setVisible(checked)
    def choose_folder(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "เลือกโฟลเดอร์ที่เก็บคำตอบจาก GPT1")
        if not folder: return
        self.selected_folder = Path(folder); self.input_folder.setText(str(self.selected_folder)); self.reset_results_only()
        try: raw_files = discover_raw_files(self.selected_folder)
        except Exception as exc: QMessageBox.critical(self, "เลือกโฟลเดอร์ไม่ได้", str(exc)); return
        has_raw = len(raw_files) > 0; self.raw_count.setText(str(len(raw_files))); self.clean_button.setEnabled(has_raw); self.command_clean_button.setEnabled(has_raw)
        if has_raw: self.set_coach(3, f"พบไฟล์จาก GPT1 {len(raw_files)} ไฟล์", f"กดตรวจไฟล์เพื่อเตรียมคำสั่ง GPT2 จำนวน {self.get_post_count()} รายการ")
        else: self.set_coach(3, "ยังไม่พบไฟล์จาก GPT1", "บันทึกคำตอบจาก GPT1 เป็นไฟล์ .md หรือ .txt ในโฟลเดอร์นี้ก่อน")
    def reset_results_only(self) -> None:
        self.results = []; self.summary = None; self.table.setRowCount(0); self.prompt_list.clear(); self.current_prompt_files = []; self.copied_prompt_paths = set(); self.prompt_preview.setPlainText("เลือกโฟลเดอร์แล้ว กดตรวจไฟล์เพื่อเตรียมคำสั่ง GPT2"); self.pass_count.setText("0"); self.fail_count.setText("0"); self.selected_count.setText("0"); self.prompt_count.setText("0"); self.progress.setValue(0); self.results_empty.setVisible(True); self.set_gpt2_actions_enabled(False)
    def run_cleaner(self) -> None:
        if self.selected_folder is None:
            QMessageBox.warning(self, "ยังไม่ได้เลือกโฟลเดอร์", "กรุณาเลือกหรือเปิดโฟลเดอร์สำหรับวางคำตอบ GPT1 ก่อน"); return
        self.normalize_n_from_input(); self.clean_button.setEnabled(False); self.command_clean_button.setEnabled(False); self.table.setRowCount(0); self.prompt_list.clear(); self.current_prompt_files = []; self.copied_prompt_paths = set(); self.results_empty.setText("กำลังตรวจไฟล์และเตรียมคำสั่ง GPT2..."); self.results_empty.setVisible(True); self.prompt_preview.setPlainText("กำลังประมวลผล โปรดรอจนกว่าผลการตรวจจะแสดง"); self.progress.setValue(10); self.set_gpt2_actions_enabled(False); self.set_coach(4, "กำลังตรวจไฟล์", f"โปรแกรมกำลังเตรียมคำสั่ง GPT2 จำนวน {self.get_post_count()} รายการต่อไฟล์ที่ผ่าน"); self.worker = CleanWorker(self.selected_folder, self.get_post_count(), self.allow_visual.isChecked(), self.allow_angle.isChecked()); self.worker.finished_with_summary.connect(self.on_clean_finished); self.worker.failed.connect(self.on_clean_failed); self.worker.start()
    def on_clean_failed(self, message: str) -> None:
        self.clean_button.setEnabled(True); self.command_clean_button.setEnabled(True); self.progress.setValue(0); self.results_empty.setText("ตรวจไฟล์ไม่สำเร็จ"); self.set_coach(4, "ตรวจไฟล์ไม่สำเร็จ", "อ่านข้อความผิดพลาด แล้วแก้คำตอบจาก GPT1 หรือส่ง error กลับมาตรวจ"); QMessageBox.critical(self, "ตรวจไฟล์ไม่สำเร็จ", message)
    def on_clean_finished(self, summary: PipelineBatchSummary) -> None:
        self.clean_button.setEnabled(True); self.command_clean_button.setEnabled(True); self.summary = summary; self.results = list(summary.results); self.progress.setValue(100); self.open_output_button.setEnabled(True); self.command_open_output_button.setEnabled(True); self.raw_count.setText(str(summary.raw_file_count)); self.pass_count.setText(str(summary.pass_count)); self.fail_count.setText(str(summary.fail_count)); self.selected_count.setText(str(summary.selected_row_count)); self.prompt_count.setText(str(summary.prompt_file_count)); self.table.setRowCount(len(self.results)); self.results_empty.setVisible(len(self.results) == 0)
        if not self.results: self.results_empty.setText("ไม่พบไฟล์ .md / .txt / .text ในโฟลเดอร์นี้")
        for row_index, result in enumerate(self.results):
            for col, value in enumerate([result.status, result.raw_file.name, f"{result.extracted_rows}/{result.expected_rows}", str(result.selected_rows), str(result.prompt_files), self.friendly_next_action(result)]):
                item = QTableWidgetItem(value)
                if col in {0, 2, 3, 4}: item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_index, col, item)
        self.table.resizeRowsToContents(); first_pass = next((i for i, result in enumerate(self.results) if result.status == "PASS"), None)
        if first_pass is not None: self.table.selectRow(first_pass); self.set_coach(5, "เตรียมคำสั่ง GPT2 เสร็จแล้ว", "เลือกคำสั่งด้านซ้าย แล้วกดคัดลอกไปวางใน GPT2")
        elif self.results: self.set_gpt2_actions_enabled(False); self.prompt_preview.setPlainText("ยังไม่มีไฟล์ที่ผ่าน: เปิดรายงานการตรวจเพื่อแก้คำตอบจาก GPT1 ก่อน"); self.set_coach(3, "ยังไม่มีไฟล์ที่ผ่าน", "เปิดรายงานของไฟล์ที่ไม่ผ่าน แล้วแก้คำตอบจาก GPT1 ก่อน")
        else: self.set_gpt2_actions_enabled(False); self.prompt_preview.setPlainText("ไม่พบไฟล์จาก GPT1 ที่ใช้ได้ในโฟลเดอร์นี้"); self.set_coach(3, "ไม่พบไฟล์จาก GPT1", "เพิ่มไฟล์ .md หรือ .txt จาก GPT1 แล้วเลือกโฟลเดอร์อีกครั้ง")
    def friendly_next_action(self, result: CleanResult) -> str: return f"คัดลอกคำสั่ง GPT2 จำนวน {result.prompt_files} รายการ" if result.status == "PASS" else "เปิดรายงานแล้วแก้ไฟล์ก่อนส่งต่อ"
    def selected_result(self) -> CleanResult | None:
        selected = self.table.selectionModel().selectedRows()
        if not selected: return None
        row = selected[0].row(); return self.results[row] if 0 <= row < len(self.results) else None
    def on_result_selection_changed(self) -> None:
        result = self.selected_result()
        if result is None: self.set_gpt2_actions_enabled(False); return
        if result.status != "PASS": self.set_gpt2_actions_enabled(False); self.open_report_button.setEnabled(True); self.prompt_list.clear(); self.prompt_preview.setPlainText("ไฟล์นี้ยังไม่ผ่าน ห้ามส่งเข้า GPT2 ให้เปิดรายงานและแก้ก่อน"); self.set_coach(3, "ไฟล์นี้ยังไม่ผ่าน", "อย่าส่งไฟล์นี้เข้า GPT2 ให้เปิดรายงานแล้วแก้ก่อน"); return
        self.load_prompt_queue(result); self.set_coach(5, "ไฟล์นี้ผ่านและมีคำสั่ง GPT2 พร้อมใช้", "เลือกคำสั่ง แล้วกดคัดลอกคำสั่งนี้เพื่อส่งเข้า GPT2")
    def load_prompt_queue(self, result: CleanResult) -> None:
        self.prompt_list.clear(); self.current_prompt_files = []
        if not result.prompt_folder or not result.prompt_folder.exists(): self.set_gpt2_actions_enabled(False); self.prompt_preview.setPlainText("ไม่พบโฟลเดอร์คำสั่ง GPT2"); return
        prompt_files = sorted(result.prompt_folder.glob("*_gpt2_prompt.txt")); self.current_prompt_files = prompt_files; rows = read_tsv_rows(result.selected_file) if result.selected_file and result.selected_file.exists() else []
        for index, prompt_file in enumerate(prompt_files, start=1):
            item = QListWidgetItem(prompt_title(prompt_file, index, rows)); item.setData(Qt.UserRole, prompt_file); item.setToolTip(str(prompt_file)); self.prompt_list.addItem(item)
        ready = len(prompt_files) > 0; self.set_gpt2_actions_enabled(ready)
        if ready: self.prompt_list.setCurrentRow(0)
        else: self.prompt_preview.setPlainText("ยังไม่มีคำสั่ง GPT2 ที่สร้างไว้")
    def on_prompt_selection_changed(self) -> None:
        prompt_file = self.selected_prompt_file()
        if prompt_file is None: self.prompt_preview.setPlainText("เลือกคำสั่ง GPT2 จากรายการด้านซ้าย"); return
        try: self.prompt_preview.setPlainText(prompt_file.read_text(encoding="utf-8"))
        except Exception as exc: self.prompt_preview.setPlainText(f"อ่านคำสั่งนี้ไม่ได้: {exc}")
    def selected_prompt_file(self) -> Path | None:
        item = self.prompt_list.currentItem()
        if item is None: return None
        data = item.data(Qt.UserRole); return data if isinstance(data, Path) else None
    def set_gpt2_actions_enabled(self, enabled: bool) -> None:
        for button in self.gpt2_buttons: button.setEnabled(enabled)
        output_ready = self.summary is not None; self.open_output_button.setEnabled(output_ready); self.command_open_output_button.setEnabled(output_ready)
    def copy_selected_gpt2_prompt(self) -> None:
        prompt_file = self.selected_prompt_file()
        if prompt_file is None: QMessageBox.warning(self, "ยังไม่ได้เลือกคำสั่ง", "เลือกคำสั่ง GPT2 จากรายการก่อน"); return
        QGuiApplication.clipboard().setText(prompt_file.read_text(encoding="utf-8")); self.copied_prompt_paths.add(prompt_file); row = self.prompt_list.currentRow(); item = self.prompt_list.currentItem()
        if item is not None and not item.text().endswith(" ✓ คัดลอกแล้ว"): item.setText(item.text() + " ✓ คัดลอกแล้ว")
        self.set_coach(5, "คัดลอกคำสั่ง GPT2 แล้ว", "วางคำสั่งนี้ใน GPT2 แล้วกลับมาคัดลอกรายการถัดไป"); QMessageBox.information(self, "คัดลอกแล้ว", "คัดลอกคำสั่ง GPT2 แล้ว")
        if row + 1 < self.prompt_list.count(): self.prompt_list.setCurrentRow(row + 1)
    def copy_first_gpt2_prompt(self) -> None:
        if self.prompt_list.count() == 0: QMessageBox.warning(self, "ยังไม่มีคำสั่ง", "ยังไม่มีคำสั่ง GPT2 ที่พร้อมใช้"); return
        self.prompt_list.setCurrentRow(0); self.copy_selected_gpt2_prompt()
    def select_next_prompt(self) -> None:
        if self.prompt_list.count() == 0: return
        self.prompt_list.setCurrentRow(min(self.prompt_list.currentRow() + 1, self.prompt_list.count() - 1))
    def open_selected_file(self) -> None:
        result = self.selected_result()
        if result and result.selected_file: self.open_path(result.selected_file)
    def open_prompt_folder(self) -> None:
        result = self.selected_result()
        if result and result.prompt_folder: self.open_path(result.prompt_folder)
    def open_clean_file(self) -> None:
        result = self.selected_result()
        if result: self.open_path(result.clean_file)
    def open_report_file(self) -> None:
        result = self.selected_result()
        if result: self.open_path(result.report_file)
    def open_output_folder(self) -> None:
        if self.summary: self.open_path(self.summary.output_root)
        elif self.selected_folder: self.open_path(self.selected_folder / "_cleaned")
    def open_path(self, path: Path) -> None:
        if not path.exists(): QMessageBox.warning(self, "ไม่พบไฟล์", str(path)); return
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(path)))
    def reset_workflow(self) -> None:
        self.results = []; self.summary = None; self.worker = None; self.selected_folder = None; self.current_prompt_files = []; self.copied_prompt_paths = set(); self.input_folder.clear(); self.table.setRowCount(0); self.prompt_list.clear(); self.results_empty.setText("ยังไม่มีผลลัพธ์: คัดลอกคำสั่ง GPT1 → บันทึกคำตอบเป็นไฟล์ .md/.txt → ตรวจไฟล์"); self.results_empty.setVisible(True); self.prompt_preview.setPlainText("เมื่อไฟล์ผ่านการตรวจ โปรแกรมจะแสดงคำสั่ง GPT2 ที่พร้อมคัดลอกที่นี่"); self.raw_count.setText("0"); self.pass_count.setText("0"); self.fail_count.setText("0"); self.selected_count.setText("0"); self.prompt_count.setText("0"); self.progress.setValue(0); self.clean_button.setEnabled(False); self.command_clean_button.setEnabled(False); self.open_output_button.setEnabled(False); self.command_open_output_button.setEnabled(False); self.set_gpt2_actions_enabled(False); self.set_coach(1, "เลือกชื่อสินค้าได้เลย ไม่ต้องจำรหัสสินค้า", "โปรแกรมจะแปลงชื่อสินค้าที่เลือกเป็นรหัส SKU ให้เอง")


def main() -> int:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
