from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import Qt, QThread, QUrl, Signal
from PySide6.QtGui import QDesktopServices, QGuiApplication
from PySide6.QtWidgets import (
    QApplication,
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
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

try:
    from .workspace_parallel_service import (
        DEFAULT_POST_COUNT,
        MAX_POST_COUNT,
        MIN_POST_COUNT,
        ParallelWorkspaceSummary,
        WorkspaceJobResult,
        READY_DIR_NAME,
        process_workspace_parallel,
    )
except ImportError:
    from workspace_parallel_service import (  # type: ignore
        DEFAULT_POST_COUNT,
        MAX_POST_COUNT,
        MIN_POST_COUNT,
        ParallelWorkspaceSummary,
        WorkspaceJobResult,
        READY_DIR_NAME,
        process_workspace_parallel,
    )


class PathManager:
    def __init__(self) -> None:
        self.app_dir = Path(__file__).resolve().parent
        self.content_os_root = self.app_dir.parents[1]
        self.repo_root = self.content_os_root.parent
        self.default_workspace = self.repo_root / "_operator_workspace"
        self.sku_lookup = self.content_os_root / "schemas" / "sku_lookup_v1.tsv"

    def sku_workspace(self, sku: str) -> Path:
        return self.default_workspace / sku

    def raw_folder(self, sku: str) -> Path:
        return self.sku_workspace(sku) / "raw"


def load_products(sku_lookup: Path) -> list[dict[str, str]]:
    if not sku_lookup.exists():
        return []
    lines = sku_lookup.read_text(encoding="utf-8").splitlines()
    if not lines:
        return []
    headers = lines[0].split("\t")
    products: list[dict[str, str]] = []
    for line in lines[1:]:
        if not line.strip():
            continue
        values = line.split("\t")
        row = {header: values[index] if index < len(values) else "" for index, header in enumerate(headers)}
        if row.get("SKU"):
            products.append(row)
    return products


def product_display(row: dict[str, str]) -> str:
    name = row.get("THAI_NAME") or row.get("PRODUCT_NAME") or "สินค้า"
    return f"{name} — {row.get('SKU', '')}"


class ParallelWorker(QThread):
    finished_with_summary = Signal(object)
    failed = Signal(str)

    def __init__(self, root: Path, post_count: int, max_workers: int) -> None:
        super().__init__()
        self.root = root
        self.post_count = post_count
        self.max_workers = max_workers

    def run(self) -> None:
        try:
            self.finished_with_summary.emit(
                process_workspace_parallel(
                    self.root,
                    post_count=self.post_count,
                    max_workers=self.max_workers,
                )
            )
        except Exception as exc:  # noqa: BLE001
            self.failed.emit(str(exc))


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.paths = PathManager()
        self.products = load_products(self.paths.sku_lookup)
        self.setWindowTitle("เครื่องมือเตรียมคอนเทนต์ BiiigBee — เริ่มจาก GPT1 แล้วส่งต่อ GPT2")
        self.resize(1550, 930)
        self.selected_root: Path | None = None
        self.summary: ParallelWorkspaceSummary | None = None
        self.results: list[WorkspaceJobResult] = []
        self.current_prompt_files: list[Path] = []
        self.current_prompt_index = 0
        self.copied_prompts: set[Path] = set()
        self.worker: ParallelWorker | None = None
        self.setStyleSheet(self.qss())
        self.setCentralWidget(self.build_ui())
        self.set_default_workspace()
        self.update_gpt1_preview()

    def qss(self) -> str:
        return """
            QMainWindow { background: #f6f8fb; color: #10203a; }
            QLabel { color: #10203a; }
            QLabel#Title { font-size: 24px; font-weight: 800; color: #172033; }
            QLabel#Subtitle { font-size: 13px; color: #475569; }
            QLabel#PanelTitle { font-size: 18px; font-weight: 800; color: #14315c; }
            QLabel#SectionTitle { font-size: 15px; font-weight: 800; color: #1e3a8a; }
            QLabel#Help { font-size: 13px; color: #334155; }
            QLabel#NextAction { font-size: 18px; font-weight: 800; color: #0f5132; background: #dcfce7; border: 1px solid #86efac; border-radius: 12px; padding: 12px; }
            QLabel#Metric { font-size: 22px; font-weight: 800; color: #14315c; }
            QLabel#MetricText { font-size: 12px; color: #64748b; }
            QFrame#Panel, QFrame#CommandBar, QFrame#MetricCard { background: #ffffff; border: 1px solid #dbe3ef; border-radius: 12px; }
            QFrame#StartCard { background: #ffffff; border: 2px solid #bfdbfe; border-radius: 12px; }
            QPushButton { color: #10203a; padding: 9px 14px; border-radius: 8px; background: #e7edf7; border: 1px solid #cbd6e7; }
            QPushButton:hover { background: #dbeafe; border: 1px solid #93c5fd; }
            QPushButton:disabled { color: #7c8797; background: #edf1f7; border: 1px solid #d8e0ee; }
            QPushButton#PrimaryButton { background: #2563eb; color: #ffffff; font-size: 15px; font-weight: 800; border: 1px solid #1d4ed8; padding: 12px 18px; }
            QPushButton#SuccessButton { background: #059669; color: #ffffff; font-weight: 800; border: 1px solid #047857; }
            QPushButton#DangerButton { background: #fee2e2; color: #991b1b; border: 1px solid #fecaca; }
            QPushButton#TinyButton { padding: 7px 12px; font-weight: 800; min-width: 36px; }
            QLineEdit, QTextEdit, QComboBox { color: #10203a; background: #ffffff; border: 1px solid #94a3b8; border-radius: 8px; padding: 8px; selection-background-color: #bfdbfe; selection-color: #0f172a; }
            QLineEdit:read-only { background: #f8fafc; color: #334155; }
            QLineEdit#NValue { font-size: 18px; font-weight: 800; }
            QComboBox::drop-down { border-left: 1px solid #94a3b8; width: 30px; background: #e7edf7; }
            QComboBox QAbstractItemView { color: #0f172a; background-color: #ffffff; selection-background-color: #2563eb; selection-color: #ffffff; outline: 0; border: 1px solid #94a3b8; }
            QTableWidget { color: #10203a; background: #ffffff; border: 1px solid #dbe3ef; border-radius: 8px; gridline-color: #edf2f7; selection-background-color: #dbeafe; selection-color: #10203a; }
            QHeaderView::section { background: #334155; color: #ffffff; padding: 6px; border: 0; }
            QProgressBar { color: #10203a; border: 1px solid #cbd6e7; border-radius: 7px; text-align: center; background: #ffffff; }
            QProgressBar::chunk { background: #2563eb; border-radius: 6px; }
        """

    def build_ui(self) -> QWidget:
        root = QWidget()
        layout = QVBoxLayout(root)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        title = QLabel("เครื่องมือเตรียมคอนเทนต์ BiiigBee")
        title.setObjectName("Title")
        subtitle = QLabel("เริ่มจากสร้างคำสั่ง GPT1 → เก็บคำตอบใน raw folder → ตรวจหลายสินค้าแบบขนาน → ส่งต่อ GPT2")
        subtitle.setObjectName("Subtitle")
        layout.addWidget(title)
        layout.addWidget(subtitle)

        self.next_action = QLabel("ขั้นต่อไป: เลือกสินค้าและจำนวนโพสต์ แล้วกด “คัดลอกคำสั่ง GPT1”")
        self.next_action.setObjectName("NextAction")
        self.next_action.setWordWrap(True)
        layout.addWidget(self.next_action)

        layout.addWidget(self.build_gpt1_panel())
        layout.addWidget(self.build_command_bar())
        layout.addWidget(self.build_metrics())

        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(self.build_jobs_panel())
        splitter.addWidget(self.build_prompt_panel())
        splitter.setSizes([400, 340])
        layout.addWidget(splitter, stretch=1)
        return root

    def build_gpt1_panel(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("StartCard")
        layout = QGridLayout(panel)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setHorizontalSpacing(12)
        layout.setVerticalSpacing(8)

        title = QLabel("0. เริ่มงาน: สร้างคำสั่งสำหรับ GPT1")
        title.setObjectName("PanelTitle")
        help_text = QLabel("เลือกสินค้าและจำนวนโพสต์ โปรแกรมจะสร้างคำสั่ง GPT1 ให้ copy ไปวางได้ทันที")
        help_text.setObjectName("Help")
        help_text.setWordWrap(True)
        layout.addWidget(title, 0, 0, 1, 2)
        layout.addWidget(help_text, 1, 0, 1, 2)

        layout.addWidget(QLabel("เลือกสินค้า:"), 2, 0)
        self.product_combo = QComboBox()
        self.product_combo.setMinimumWidth(560)
        if self.products:
            for product in self.products:
                self.product_combo.addItem(product_display(product), product)
        else:
            self.product_combo.addItem("ไม่พบฐานข้อมูลสินค้า — กรุณาตรวจ sku_lookup_v1.tsv", {"SKU": "<SKU>"})
        self.product_combo.currentIndexChanged.connect(self.on_product_changed)
        layout.addWidget(self.product_combo, 2, 1)

        self.product_card = QTextEdit()
        self.product_card.setReadOnly(True)
        self.product_card.setMinimumHeight(82)
        layout.addWidget(self.product_card, 3, 0, 1, 2)

        prompt_title = QLabel("คำสั่ง GPT1 ที่จะนำไปวาง:")
        prompt_title.setObjectName("SectionTitle")
        layout.addWidget(prompt_title, 0, 2)
        self.gpt1_preview = QTextEdit()
        self.gpt1_preview.setReadOnly(True)
        self.gpt1_preview.setMinimumHeight(170)
        layout.addWidget(self.gpt1_preview, 1, 2, 3, 1)

        action_row = QHBoxLayout()
        self.copy_gpt1_button = self.action_button("คัดลอกคำสั่ง GPT1", self.copy_gpt1_prompt, "SuccessButton")
        self.open_raw_button = self.action_button("เปิดโฟลเดอร์ raw ของสินค้านี้", self.open_current_raw_folder)
        self.save_prompt_button = self.action_button("บันทึกคำสั่ง GPT1 ไว้ในโฟลเดอร์สินค้า", self.save_gpt1_request_file)
        for button in (self.copy_gpt1_button, self.open_raw_button, self.save_prompt_button):
            action_row.addWidget(button)
        action_row.addStretch(1)
        layout.addLayout(action_row, 4, 0, 1, 3)

        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 1)
        return panel

    def build_command_bar(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("CommandBar")
        layout = QHBoxLayout(panel)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.addWidget(QLabel("จำนวนโพสต์ต่อสินค้า:"))
        self.minus_button = self.tiny_button("−", lambda: self.adjust_n(-1))
        self.n_value = QLineEdit(str(DEFAULT_POST_COUNT))
        self.n_value.setObjectName("NValue")
        self.n_value.setFixedWidth(80)
        self.n_value.setAlignment(Qt.AlignCenter)
        self.n_value.editingFinished.connect(self.normalize_n)
        self.plus_button = self.tiny_button("+", lambda: self.adjust_n(1))
        layout.addWidget(self.minus_button)
        layout.addWidget(self.n_value)
        layout.addWidget(self.plus_button)
        for preset in (10, 20, 30, 60):
            button = self.tiny_button(str(preset), lambda _=False, value=preset: self.set_n(value))
            layout.addWidget(button)
        layout.addSpacing(16)
        layout.addWidget(QLabel("ทำงานพร้อมกัน:"))
        self.worker_combo = QComboBox()
        for value in (1, 2, 3, 4, 6, 8):
            self.worker_combo.addItem(f"{value} งาน", value)
        self.worker_combo.setCurrentIndex(3)
        layout.addWidget(self.worker_combo)
        layout.addSpacing(16)
        self.folder_path = QLineEdit()
        self.folder_path.setReadOnly(True)
        self.folder_path.setPlaceholderText("ยังไม่ได้เลือกโฟลเดอร์")
        layout.addWidget(self.folder_path, stretch=1)
        self.choose_button = self.action_button("เลือกโฟลเดอร์", self.choose_folder)
        self.run_button = self.action_button("ตรวจหลายสินค้าแบบขนาน", self.run_parallel, "PrimaryButton")
        self.open_root_button = self.action_button("เปิดโฟลเดอร์ที่เลือก", self.open_selected_root)
        self.open_summary_button = self.action_button("เปิดสรุปรวม", self.open_parallel_summary)
        self.open_summary_button.setEnabled(False)
        layout.addWidget(self.choose_button)
        layout.addWidget(self.run_button)
        layout.addWidget(self.open_root_button)
        layout.addWidget(self.open_summary_button)
        return panel

    def build_metrics(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("CommandBar")
        layout = QHBoxLayout(panel)
        layout.setContentsMargins(10, 8, 10, 8)
        self.job_metric = self.metric("0", "สินค้า")
        self.pass_metric = self.metric("0", "ผ่าน")
        self.fail_metric = self.metric("0", "ไม่ผ่าน")
        self.raw_metric = self.metric("0", "ไฟล์ GPT1")
        self.prompt_metric = self.metric("0", "คำสั่ง GPT2")
        for widget in (self.job_metric, self.pass_metric, self.fail_metric, self.raw_metric, self.prompt_metric):
            layout.addWidget(widget)
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        layout.addWidget(self.progress, stretch=1)
        return panel

    def metric(self, value: str, label: str) -> QFrame:
        frame = QFrame()
        frame.setObjectName("MetricCard")
        frame.setMinimumWidth(140)
        layout = QVBoxLayout(frame)
        value_label = QLabel(value)
        value_label.setObjectName("Metric")
        value_label.setAlignment(Qt.AlignCenter)
        text_label = QLabel(label)
        text_label.setObjectName("MetricText")
        text_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(value_label)
        layout.addWidget(text_label)
        frame.value_label = value_label  # type: ignore[attr-defined]
        return frame

    def build_jobs_panel(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("Panel")
        layout = QVBoxLayout(panel)
        title = QLabel("1. ผลการตรวจหลายสินค้า")
        title.setObjectName("PanelTitle")
        help_text = QLabel("ถ้าเลือก _operator_workspace โปรแกรมจะไล่ดู child folder ของแต่ละ SKU แล้วเก็บผลไว้ใน SKU/_cleaned แยกกัน")
        help_text.setObjectName("Help")
        help_text.setWordWrap(True)
        layout.addWidget(title)
        layout.addWidget(help_text)
        self.table = QTableWidget(0, 9)
        self.table.setHorizontalHeaderLabels(["สถานะ", "สินค้า", "ไฟล์ GPT1", "ผ่าน", "ไม่ผ่าน", "คำสั่ง GPT2", "พร้อมส่ง GPT2", "โฟลเดอร์ผลลัพธ์", "ต้องทำต่อ"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(7, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(8, QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.itemSelectionChanged.connect(self.on_job_selected)
        layout.addWidget(self.table, stretch=1)
        return panel

    def build_prompt_panel(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("Panel")
        layout = QGridLayout(panel)
        title = QLabel("2. คำสั่ง GPT2 ที่พร้อมใช้")
        title.setObjectName("PanelTitle")
        help_text = QLabel(f"เลือกสินค้าที่ผ่านจากตารางด้านบน แล้วใช้ไฟล์ใน {READY_DIR_NAME} เพื่อส่งเข้า GPT2 ทีละรายการ")
        help_text.setObjectName("Help")
        help_text.setWordWrap(True)
        layout.addWidget(title, 0, 0, 1, 2)
        layout.addWidget(help_text, 1, 0, 1, 2)
        self.prompt_list = QTableWidget(0, 3)
        self.prompt_list.setHorizontalHeaderLabels(["ลำดับ", "ไฟล์คำสั่ง", "สถานะ"])
        self.prompt_list.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.prompt_list.setSelectionBehavior(QTableWidget.SelectRows)
        self.prompt_list.itemSelectionChanged.connect(self.on_prompt_selected)
        self.prompt_preview = QTextEdit()
        self.prompt_preview.setReadOnly(True)
        self.prompt_preview.setPlainText("หลังจากตรวจผ่านแล้ว รายการคำสั่ง GPT2 จะแสดงตรงนี้")
        layout.addWidget(self.prompt_list, 2, 0)
        layout.addWidget(self.prompt_preview, 2, 1)
        actions = QHBoxLayout()
        self.copy_prompt_button = self.action_button("คัดลอกคำสั่งนี้", self.copy_selected_prompt, "SuccessButton")
        self.next_prompt_button = self.action_button("คำสั่งถัดไป", self.next_prompt)
        self.open_prompts_button = self.action_button("เปิดโฟลเดอร์พร้อมส่ง GPT2", self.open_prompt_folder)
        self.open_output_button = self.action_button("เปิดผลลัพธ์สินค้านี้", self.open_selected_output)
        for button in (self.copy_prompt_button, self.next_prompt_button, self.open_prompts_button, self.open_output_button):
            button.setEnabled(False)
            actions.addWidget(button)
        actions.addStretch(1)
        layout.addLayout(actions, 3, 0, 1, 2)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 2)
        return panel

    def action_button(self, text: str, handler, object_name: str | None = None) -> QPushButton:
        button = QPushButton(text)
        if object_name:
            button.setObjectName(object_name)
        button.clicked.connect(handler)
        return button

    def tiny_button(self, text: str, handler) -> QPushButton:
        button = QPushButton(text)
        button.setObjectName("TinyButton")
        button.clicked.connect(handler)
        return button

    def set_default_workspace(self) -> None:
        self.paths.default_workspace.mkdir(parents=True, exist_ok=True)
        self.selected_root = self.paths.default_workspace
        self.folder_path.setText(str(self.selected_root))

    def current_product(self) -> dict[str, str]:
        data = self.product_combo.currentData()
        return data if isinstance(data, dict) else {"SKU": "<SKU>"}

    def current_sku(self) -> str:
        return self.current_product().get("SKU", "<SKU>")

    def product_details_text(self) -> str:
        product = self.current_product()
        lines = [
            f"สินค้า: {product.get('THAI_NAME') or product.get('PRODUCT_NAME') or '-'}",
            f"SKU: {product.get('SKU', '-')}",
            f"ชื่อสินค้าในระบบ: {product.get('PRODUCT_NAME', '-')}",
        ]
        for key in ("GRADE_BAND", "GRID_SIZE", "DIFFICULTY", "PUZZLE_COUNT", "ANSWER_KEY_STATUS"):
            if product.get(key):
                lines.append(f"{key}: {product.get(key)}")
        return "\n".join(lines)

    def build_gpt1_prompt(self) -> str:
        return (
            f"SKU: {self.current_sku()}\n"
            f"NUMBER_OF_ROWS: {self.get_n()}\n"
            "PLATFORM: AUTO\n"
            "CAMPAIGN_GOAL: AUTO\n"
        )

    def update_gpt1_preview(self) -> None:
        if hasattr(self, "product_card"):
            self.product_card.setPlainText(self.product_details_text())
        if hasattr(self, "gpt1_preview"):
            self.gpt1_preview.setPlainText(self.build_gpt1_prompt())

    def on_product_changed(self) -> None:
        self.update_gpt1_preview()
        self.next_action.setText("ขั้นต่อไป: คัดลอกคำสั่ง GPT1 แล้ววางใน GPT1")

    def copy_gpt1_prompt(self) -> None:
        prompt = self.build_gpt1_prompt()
        QGuiApplication.clipboard().setText(prompt)
        self.save_gpt1_request_file(silent=True)
        self.next_action.setText("คัดลอกคำสั่ง GPT1 แล้ว: ให้นำไปวางใน GPT1 แล้วบันทึกคำตอบไว้ในโฟลเดอร์ raw ของสินค้านี้")
        QMessageBox.information(self, "คัดลอกแล้ว", "คัดลอกคำสั่ง GPT1 แล้ว ให้นำไปวางใน GPT1")

    def save_gpt1_request_file(self, silent: bool = False) -> None:
        sku = self.current_sku()
        workspace = self.paths.sku_workspace(sku)
        workspace.mkdir(parents=True, exist_ok=True)
        request_file = workspace / "GPT1_REQUEST.txt"
        request_file.write_text(self.build_gpt1_prompt(), encoding="utf-8")
        if not silent:
            QMessageBox.information(self, "บันทึกแล้ว", f"บันทึกคำสั่ง GPT1 แล้ว:\n{request_file}")

    def open_current_raw_folder(self) -> None:
        raw_folder = self.paths.raw_folder(self.current_sku())
        raw_folder.mkdir(parents=True, exist_ok=True)
        self.selected_root = self.paths.default_workspace
        self.folder_path.setText(str(self.selected_root))
        self.save_gpt1_request_file(silent=True)
        self.open_path(raw_folder)
        self.next_action.setText("ขั้นต่อไป: บันทึกคำตอบจาก GPT1 เป็นไฟล์ .md หรือ .txt ในโฟลเดอร์ raw แล้วกดตรวจหลายสินค้าแบบขนาน")

    def get_n(self) -> int:
        try:
            value = int(self.n_value.text().strip())
        except ValueError:
            value = DEFAULT_POST_COUNT
        return max(MIN_POST_COUNT, min(MAX_POST_COUNT, value))

    def set_n(self, value: int) -> None:
        self.n_value.setText(str(max(MIN_POST_COUNT, min(MAX_POST_COUNT, value))))
        self.update_gpt1_preview()

    def adjust_n(self, delta: int) -> None:
        self.set_n(self.get_n() + delta)

    def normalize_n(self) -> None:
        self.set_n(self.get_n())

    def choose_folder(self) -> None:
        start = str(self.selected_root or self.paths.default_workspace or self.paths.repo_root)
        folder = QFileDialog.getExistingDirectory(self, "เลือก _operator_workspace หรือโฟลเดอร์สินค้า", start)
        if not folder:
            return
        self.selected_root = Path(folder)
        self.folder_path.setText(str(self.selected_root))
        self.next_action.setText("ขั้นต่อไป: กด “ตรวจหลายสินค้าแบบขนาน”")

    def run_parallel(self) -> None:
        if self.selected_root is None:
            QMessageBox.warning(self, "ยังไม่ได้เลือกโฟลเดอร์", "กรุณาเลือก _operator_workspace หรือโฟลเดอร์สินค้าก่อน")
            return
        self.normalize_n()
        max_workers = int(self.worker_combo.currentData())
        self.run_button.setEnabled(False)
        self.table.setRowCount(0)
        self.prompt_list.setRowCount(0)
        self.prompt_preview.setPlainText("กำลังตรวจหลายสินค้าแบบขนาน...")
        self.progress.setValue(10)
        self.next_action.setText("กำลังตรวจไฟล์ GPT1 หลายสินค้าแบบขนาน กรุณารอสักครู่")
        self.worker = ParallelWorker(self.selected_root, self.get_n(), max_workers)
        self.worker.finished_with_summary.connect(self.on_finished)
        self.worker.failed.connect(self.on_failed)
        self.worker.start()

    def on_failed(self, message: str) -> None:
        self.run_button.setEnabled(True)
        self.progress.setValue(0)
        self.next_action.setText("ตรวจไม่สำเร็จ: เปิดรายละเอียด error แล้วแก้ไขก่อน")
        QMessageBox.critical(self, "ตรวจไม่สำเร็จ", message)

    def on_finished(self, summary: ParallelWorkspaceSummary) -> None:
        self.run_button.setEnabled(True)
        self.summary = summary
        self.results = list(summary.results)
        self.progress.setValue(100)
        self.open_summary_button.setEnabled(summary.summary_file is not None)
        self.set_metric(self.job_metric, str(summary.job_count))
        self.set_metric(self.pass_metric, str(summary.pass_job_count))
        self.set_metric(self.fail_metric, str(summary.fail_job_count))
        self.set_metric(self.raw_metric, str(summary.raw_file_count))
        self.set_metric(self.prompt_metric, str(summary.ready_prompt_file_count))
        self.populate_jobs()
        if summary.pass_job_count > 0:
            self.next_action.setText("ขั้นต่อไป: เลือกสินค้าที่ผ่าน แล้วคัดลอกคำสั่ง GPT2 ทีละรายการ")
            first_pass = next((index for index, result in enumerate(self.results) if result.status == "PASS"), 0)
            self.table.selectRow(first_pass)
        else:
            self.next_action.setText("ยังไม่มีสินค้าที่ผ่าน: เปิดรายงานในแต่ละ SKU แล้วแก้ไฟล์ GPT1")

    def set_metric(self, frame: QFrame, value: str) -> None:
        frame.value_label.setText(value)  # type: ignore[attr-defined]

    def populate_jobs(self) -> None:
        self.table.setRowCount(len(self.results))
        for row, result in enumerate(self.results):
            ready_dir = result.ready_gpt2_dir or (result.job.workspace_dir / READY_DIR_NAME)
            next_action = "เปิดโฟลเดอร์พร้อมส่ง GPT2" if result.status == "PASS" else "เปิดรายงานและแก้ก่อน"
            values = [
                result.status,
                result.job.sku,
                str(result.raw_file_count),
                str(result.pass_count),
                str(result.fail_count),
                str(result.prompt_file_count),
                str(result.ready_prompt_count),
                str(ready_dir if result.status == "PASS" else result.output_root),
                next_action if not result.error_message else result.error_message,
            ]
            for col, value in enumerate(values):
                item = QTableWidgetItem(value)
                if col in {0, 2, 3, 4, 5, 6}:
                    item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, col, item)
        self.table.resizeRowsToContents()

    def selected_result(self) -> WorkspaceJobResult | None:
        selected = self.table.selectionModel().selectedRows()
        if not selected:
            return None
        index = selected[0].row()
        return self.results[index] if 0 <= index < len(self.results) else None

    def on_job_selected(self) -> None:
        result = self.selected_result()
        self.current_prompt_files = []
        self.current_prompt_index = 0
        self.prompt_list.setRowCount(0)
        self.prompt_preview.clear()
        enable = bool(result and result.status == "PASS" and result.ready_gpt2_dir and result.ready_gpt2_dir.exists())
        for button in (self.copy_prompt_button, self.next_prompt_button, self.open_prompts_button, self.open_output_button):
            button.setEnabled(enable)
        if not enable:
            self.prompt_preview.setPlainText("สินค้านี้ยังไม่พร้อมส่ง GPT2 กรุณาดูรายงานการตรวจ")
            return
        self.current_prompt_files = sorted(result.ready_gpt2_dir.glob("*_gpt2_prompt.txt"))
        self.populate_prompts()
        if self.current_prompt_files:
            self.prompt_list.selectRow(0)

    def populate_prompts(self) -> None:
        self.prompt_list.setRowCount(len(self.current_prompt_files))
        for row, path in enumerate(self.current_prompt_files):
            status = "✓ คัดลอกแล้ว" if path in self.copied_prompts else "ยังไม่ได้คัดลอก"
            for col, value in enumerate([str(row + 1), path.name, status]):
                item = QTableWidgetItem(value)
                if col in {0, 2}:
                    item.setTextAlignment(Qt.AlignCenter)
                self.prompt_list.setItem(row, col, item)
        self.prompt_list.resizeRowsToContents()

    def on_prompt_selected(self) -> None:
        selected = self.prompt_list.selectionModel().selectedRows()
        if not selected:
            return
        self.current_prompt_index = selected[0].row()
        path = self.current_prompt_files[self.current_prompt_index]
        self.prompt_preview.setPlainText(path.read_text(encoding="utf-8"))

    def copy_selected_prompt(self) -> None:
        if not self.current_prompt_files:
            return
        path = self.current_prompt_files[self.current_prompt_index]
        QGuiApplication.clipboard().setText(path.read_text(encoding="utf-8"))
        self.copied_prompts.add(path)
        self.populate_prompts()
        self.prompt_list.selectRow(self.current_prompt_index)
        self.next_action.setText(f"คัดลอกแล้ว: {path.name} — ให้วางใน GPT2 แล้วกลับมาคัดลอกรายการถัดไป")

    def next_prompt(self) -> None:
        if not self.current_prompt_files:
            return
        next_index = min(len(self.current_prompt_files) - 1, self.current_prompt_index + 1)
        self.prompt_list.selectRow(next_index)

    def open_prompt_folder(self) -> None:
        result = self.selected_result()
        if result and result.ready_gpt2_dir:
            self.open_path(result.ready_gpt2_dir)
            return
        if self.current_prompt_files:
            self.open_path(self.current_prompt_files[0].parent)

    def open_selected_output(self) -> None:
        result = self.selected_result()
        if result:
            self.open_path(result.ready_gpt2_dir or result.output_root)

    def open_selected_root(self) -> None:
        if self.selected_root:
            self.open_path(self.selected_root)

    def open_parallel_summary(self) -> None:
        if self.summary and self.summary.summary_file:
            self.open_path(self.summary.summary_file)

    def open_path(self, path: Path) -> None:
        if not path.exists():
            QMessageBox.warning(self, "ไม่พบไฟล์หรือโฟลเดอร์", str(path))
            return
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(path)))


def main() -> int:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
