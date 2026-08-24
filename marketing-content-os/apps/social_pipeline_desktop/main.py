from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QAction, QGuiApplication
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QFileDialog,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

try:
    from .pipeline_service import CleanResult, build_gpt2_template, clean_folder, read_clean_rows
except ImportError:  # Allows: python marketing-content-os/apps/social_pipeline_desktop/main.py
    from pipeline_service import CleanResult, build_gpt2_template, clean_folder, read_clean_rows


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


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("BiiigBee Social Content Pipeline")
        self.resize(1180, 760)
        self.results: list[CleanResult] = []
        self.worker: CleanWorker | None = None

        self.input_folder = QLineEdit()
        self.input_folder.setPlaceholderText("Choose folder containing GPT1 raw .md/.txt files")

        browse_button = QPushButton("1. Choose Folder")
        browse_button.clicked.connect(self.choose_folder)

        self.expected_rows = QSpinBox()
        self.expected_rows.setRange(1, 1000)
        self.expected_rows.setValue(10)

        self.allow_visual_concentration = QCheckBox("Allow visual concentration")
        self.allow_angle_concentration = QCheckBox("Allow angle concentration")

        clean_button = QPushButton("2. Clean All Files")
        clean_button.clicked.connect(self.run_cleaner)
        self.clean_button = clean_button

        self.status_label = QLabel("Stage 1/6: Select a folder to start.")
        self.status_label.setWordWrap(True)

        self.results_table = QTableWidget(0, 7)
        self.results_table.setHorizontalHeaderLabels(
            ["Status", "Raw File", "Rows", "Clean TSV", "Report", "Exit", "Next Action"]
        )
        self.results_table.horizontalHeader().setStretchLastSection(True)
        self.results_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.results_table.itemSelectionChanged.connect(self.on_selection_changed)

        self.row_preview = QTextEdit()
        self.row_preview.setReadOnly(True)
        self.row_preview.setPlaceholderText("Select a PASS row to preview clean rows and prepare GPT2 handoff.")

        copy_first_row_button = QPushButton("3. Copy First Row GPT2 Prompt")
        copy_first_row_button.clicked.connect(self.copy_first_row_prompt)

        open_clean_button = QPushButton("Open Clean TSV")
        open_clean_button.clicked.connect(self.open_selected_clean_file)

        open_report_button = QPushButton("Open Report")
        open_report_button.clicked.connect(self.open_selected_report_file)

        control_group = QGroupBox("Input and deterministic cleansing")
        control_layout = QGridLayout(control_group)
        control_layout.addWidget(QLabel("Folder"), 0, 0)
        control_layout.addWidget(self.input_folder, 0, 1)
        control_layout.addWidget(browse_button, 0, 2)
        control_layout.addWidget(QLabel("Expected rows per file"), 1, 0)
        control_layout.addWidget(self.expected_rows, 1, 1)
        control_layout.addWidget(self.allow_visual_concentration, 2, 1)
        control_layout.addWidget(self.allow_angle_concentration, 3, 1)
        control_layout.addWidget(clean_button, 4, 2)

        actions_layout = QHBoxLayout()
        actions_layout.addWidget(copy_first_row_button)
        actions_layout.addWidget(open_clean_button)
        actions_layout.addWidget(open_report_button)
        actions_layout.addStretch(1)

        process_box = QGroupBox("Process engineering flow")
        process_layout = QVBoxLayout(process_box)
        process_layout.addWidget(
            QLabel(
                "1. GPT1 raw files → 2. Folder cleaner → 3. Clean TSV PASS → "
                "4. Select 5 rows → 5. GPT2 TEMPLATE_HANDOFF → 6. Image + human review"
            )
        )
        process_layout.addWidget(self.status_label)

        central = QWidget()
        layout = QVBoxLayout(central)
        layout.addWidget(control_group)
        layout.addWidget(process_box)
        layout.addWidget(self.results_table, stretch=2)
        layout.addLayout(actions_layout)
        layout.addWidget(self.row_preview, stretch=1)
        self.setCentralWidget(central)

        quit_action = QAction("Exit", self)
        quit_action.triggered.connect(self.close)
        self.menuBar().addAction(quit_action)

    def choose_folder(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Choose GPT1 raw output folder")
        if folder:
            self.input_folder.setText(folder)
            self.status_label.setText("Stage 2/6: Folder selected. Click Clean All Files.")

    def run_cleaner(self) -> None:
        folder_text = self.input_folder.text().strip()
        if not folder_text:
            QMessageBox.warning(self, "Missing folder", "Choose a folder first.")
            return

        self.clean_button.setEnabled(False)
        self.results_table.setRowCount(0)
        self.row_preview.clear()
        self.status_label.setText("Stage 2/6: Cleaning all raw GPT1 files in the selected folder...")

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
        self.status_label.setText("Stage 2/6: Cleaner failed.")
        QMessageBox.critical(self, "Cleaner failed", message)

    def on_clean_finished(self, results: list[CleanResult]) -> None:
        self.clean_button.setEnabled(True)
        self.results = results
        self.results_table.setRowCount(len(results))

        for row_index, result in enumerate(results):
            next_action = "Send selected clean rows to GPT2" if result.status == "PASS" else "Open report and fix before GPT2"
            values = [
                result.status,
                str(result.raw_file),
                f"{result.extracted_rows}/{result.expected_rows}",
                str(result.clean_file),
                str(result.report_file),
                str(result.exit_code),
                next_action,
            ]
            for col, value in enumerate(values):
                item = QTableWidgetItem(value)
                if col == 0:
                    item.setTextAlignment(Qt.AlignCenter)
                self.results_table.setItem(row_index, col, item)

        self.results_table.resizeColumnsToContents()
        pass_count = sum(1 for result in results if result.status == "PASS")
        fail_count = len(results) - pass_count
        self.status_label.setText(
            f"Stage 3/6: Cleaning complete. PASS={pass_count}, FAIL={fail_count}. "
            "Select a PASS row and copy GPT2 prompt."
        )
        if not results:
            QMessageBox.information(self, "No files", "No .md/.txt raw files found in the selected folder.")

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
        if result.status != "PASS":
            self.row_preview.setPlainText("This file failed validation. Open the report before using GPT2.")
            return
        try:
            rows = read_clean_rows(result.clean_file)
            preview = "Clean rows ready for GPT2:\n\n" + "\n".join(rows[:5])
            if len(rows) > 5:
                preview += f"\n\n... {len(rows) - 5} more rows"
            self.row_preview.setPlainText(preview)
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
        self.status_label.setText("Stage 4/6: First clean row GPT2 TEMPLATE_HANDOFF prompt copied to clipboard.")
        QMessageBox.information(self, "Copied", "GPT2 TEMPLATE_HANDOFF prompt copied to clipboard.")

    def open_selected_clean_file(self) -> None:
        result = self.selected_result()
        if result:
            self.open_path(result.clean_file)

    def open_selected_report_file(self) -> None:
        result = self.selected_result()
        if result:
            self.open_path(result.report_file)

    def open_path(self, path: Path) -> None:
        if not path.exists():
            QMessageBox.warning(self, "Missing file", str(path))
            return
        # Cross-platform via Qt service. No OS-specific command is used.
        from PySide6.QtCore import QUrl
        from PySide6.QtGui import QDesktopServices

        QDesktopServices.openUrl(QUrl.fromLocalFile(str(path)))


def main() -> int:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
