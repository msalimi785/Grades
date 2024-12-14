import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit, QVBoxLayout, QPushButton, QFileDialog
from PyQt6.QtCore import Qt
from gui import Ui_MainWindow

class MainApp(QMainWindow):
    """
    Main application class for the Grades project.
    Handles dynamic input boxes, grading logic, field clearing, CSV file modification, and file operations.
    """

    def __init__(self):
        """
        Initialize the main application, setup UI, and connect signals to their respective slots.
        """
        super(MainApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.score_inputs = []

        self.ui.spinBoxAttempts.valueChanged.connect(self.addInputBoxes)
        self.ui.buttonSubmit.clicked.connect(self.submitScores)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.ui.layoutScores.setLayout(layout)

        self.clear_button = QPushButton("Clear Fields", self)
        self.clear_button.setObjectName("clearButton")
        self.clear_button.setFixedWidth(100)
        self.ui.centralwidget.layout().addWidget(self.clear_button)
        self.clear_button.clicked.connect(self.clearFields)

        self.modify_csv_button = QPushButton("Modify CSV File", self)
        self.modify_csv_button.setObjectName("modifyCsvButton")
        self.modify_csv_button.setFixedWidth(150)
        self.ui.centralwidget.layout().addWidget(self.modify_csv_button)
        self.modify_csv_button.clicked.connect(self.modifyCsvFile)

    def addInputBoxes(self):
        """
        Dynamically creates input boxes for scores based on the number of attempts.
        Clears previous inputs before adding new ones.
        """
        for score_input in self.score_inputs:
            self.ui.layoutScores.layout().removeWidget(score_input)
            score_input.deleteLater()
        self.score_inputs.clear()

        attempts = self.ui.spinBoxAttempts.value()
        for i in range(attempts):
            score_input = QLineEdit()
            score_input.setObjectName(f"scoreInput{i+1}")
            score_input.setFixedHeight(30)
            score_input.setFixedWidth(100)
            score_input.setPlaceholderText(f"Score {i+1}")
            self.score_inputs.append(score_input)
            self.ui.layoutScores.layout().addWidget(score_input)

    def submitScores(self):
        """
        Collects the student's name and scores, calculates their grade,
        displays the result, and saves it to a file.
        """
        student_name = self.ui.lineEditStudentName.text()
        scores = []

        for i, score_input in enumerate(self.score_inputs):
            score_text = score_input.text()
            if score_text:
                try:
                    score = int(score_text)
                    if score < 1 or score > 100:
                        raise ValueError("Score must be between 1 and 100")
                    scores.append(score)
                except ValueError:
                    self.ui.labelMessage.setText(f"Invalid input for Score {i + 1}. Please enter a number between 1 and 100.")
                    return
            else:
                scores.append(0)

        final_score = max(scores) if scores else 0
        grade = self.calculateGrade(final_score)

        self.ui.labelMessage.setText(f"{student_name}'s grade: {grade}")

        self.saveResults(student_name, scores, final_score)

    def calculateGrade(self, score):
        """
        Determines the grade based on the score.

        Args:
            score (int): The final score.

        Returns:
            str: The grade (A, B, C, D, F).
        """
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"

    def saveResults(self, name, scores, final_score):
        """
        Saves the student's results to a file named 'grades.txt'.

        Args:
            name (str): Student's name.
            scores (list): List of scores.
            final_score (int): Final score.
        """
        with open("grades.txt", "a") as file:
            scores += [0] * (4 - len(scores))
            scores_str = "\t".join(str(score) for score in scores)
            file.write(f"{name}\t{scores_str}\t{final_score}\n")

    def clearFields(self):
        """
        Clears all input fields, including student name and score inputs.
        """
        self.ui.lineEditStudentName.clear()
        for score_input in self.score_inputs:
            score_input.clear()
        self.ui.labelMessage.clear()

    def modifyCsvFile(self):
        """
        Opens a dialog to select a CSV file and modify it by appending data.

        The user can add a new student name and scores directly to the file.
        """
        file_name, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
        if not file_name:
            return

        student_name = self.ui.lineEditStudentName.text()
        scores = [int(score_input.text()) if score_input.text().isdigit() else 0 for score_input in self.score_inputs]
        scores += [0] * (4 - len(scores))  # Ensure 4 columns for scores
        final_score = max(scores)

        with open(file_name, "a") as file:
            scores_str = ",".join(str(score) for score in scores)
            file.write(f"{student_name},{scores_str},{final_score}\n")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainApp()
    mainWindow.show()
    sys.exit(app.exec())













