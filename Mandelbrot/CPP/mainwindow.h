#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <opencv2/core.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>
#include <QMainWindow>

#define SIZE 600
#define ITERATIONS 100
#define PERCENT_SHIFT_ZOOM 0.1

namespace Ui {
    class MainWindow;
}

class MainWindow : public QMainWindow {
    Q_OBJECT

    public:
        explicit MainWindow(QWidget *parent = 0);
        void update();
        void updateLabels();

        ~MainWindow();

    private slots:
            void on_pushButton_Down_clicked();
            void on_pushButton_Up_clicked();
            void on_pushButton_Left_clicked();
            void on_pushButton_Right_clicked();
            void on_pushButton_ZoomIn_clicked();
            void on_pushButton_ZoomOut_clicked();

    private:
            double left_x = 0;
            double right_x = 3.0;
            double top_y = 2.0;
            double bottom_y = -1.0;

            // Mostly because they are used often, not necessarily
            // because they need to be accessible
            double difference;
            double diffx = right_x - left_x;
            double diffy = top_y - bottom_y;

            double x = 2.3;
            double y = 1.49;
            double zoom = 3.0;
            int r[50];
            int g[50];
            int b[50];
            cv::Mat newImg = cv::Mat(SIZE, SIZE, CV_16UC3);
            Ui::MainWindow *ui;
};

#endif // MAINWINDOW_H
