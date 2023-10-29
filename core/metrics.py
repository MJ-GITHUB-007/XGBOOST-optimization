from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

class Metrics():
    def __init__(self, y_true, y_pred) -> None:
        self.y_true = y_true
        self.y_pred = y_pred
    
    def report(self):
        return classification_report(self.y_true, self.y_pred, target_names=['Survived', 'Heart Attack'])
    
    def conf_matrix(self):
        return confusion_matrix(self.y_true, self.y_pred)
    
    def plot_conf_matrix(self):
        matrix = ConfusionMatrixDisplay(confusion_matrix=self.conf_matrix(), display_labels=['Survived', 'Heart Attack'])
        matrix.plot()
        plt.show()

if __name__ == '__main__':
    pass