#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <opencv2/core.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>
#include <iostream>

MainWindow::MainWindow(QWidget *parent) : QMainWindow(parent), ui(new Ui::MainWindow) {

    for (int i = 0; i < 25; i++) {
        r[i] = i * 10;
        g[i] = i * 10;
        b[i] = i * 10;
    }

    for (int j = 49; j > 24 ; j--) {
        r[j] = 250 - ((j-25) * 10);
        g[j] = 250 - ((j-25) * 10);
        b[j] = 250 - ((j-25) * 10);
    }

    ui->setupUi(this);
    this->update(); // Using this just in case qt has an update method too
}

MainWindow::~MainWindow() {
    delete ui;
}

void MainWindow::update() {
    int values[SIZE][SIZE];
    int depth = 0;
    double ii;
    double jj;
    double zr;
    double zi;

    diffx = right_x - left_x;
    diffy = top_y - bottom_y;

    //#pragma omp parallel for
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            ii = left_x + (i * (diffx / SIZE));
            jj = top_y - (j * (diffy / SIZE));
            zr = 0;
            zi = 0;
            depth = 0;

            while ( (zr * zr + zi * zi <= 4.0) && depth < ITERATIONS) {
                depth += 1;
                double temp = zr * zr - zi * zi + ii;
                zi = zr * zi * 2 + jj;
                zr = temp;
            }
            values[j][i] = depth;
        }
    }

    uchar* p;
    for (int i = 0; i < newImg.rows; i++) {
        p = newImg.ptr<uchar>(i);
        for (int j = 0; j < newImg.cols * newImg.channels(); j++) {
            depth = values[i][j/3];
            p[j] = b[depth % 50];
            p[j+1] = g[depth % 50];
            p[j+2] = r[depth % 50];
            j += 2;
        }
    }
    updateLabels();
}

void MainWindow::updateLabels() {
    ui->label_xval->setText( QString().number( ((left_x + right_x) / 2), 'f', 15)   );
    ui->label_yval->setText( QString().number( ((top_y + bottom_y) / 2), 'f', 15)   );
    ui->label_img->setPixmap(QPixmap::fromImage(QImage(newImg.data, newImg.cols, newImg.rows, newImg.step, QImage::Format_RGB888)));

}

void MainWindow::on_pushButton_Down_clicked() {
    top_y -= diffy * PERCENT_SHIFT_ZOOM;
    bottom_y -= diffy * PERCENT_SHIFT_ZOOM;
    this->update();
}

void MainWindow::on_pushButton_Up_clicked() {
    top_y += diffy * PERCENT_SHIFT_ZOOM;
    bottom_y += diffy * PERCENT_SHIFT_ZOOM;
    this->update();
}

void MainWindow::on_pushButton_Left_clicked() {
    left_x -= diffx * PERCENT_SHIFT_ZOOM;
    right_x -= diffx * PERCENT_SHIFT_ZOOM;
    this->update();
}

void MainWindow::on_pushButton_Right_clicked() {
    left_x += diffx * PERCENT_SHIFT_ZOOM;
    right_x += diffx * PERCENT_SHIFT_ZOOM;
    this->update();
}

void MainWindow::on_pushButton_ZoomIn_clicked() {
    left_x += diffx * PERCENT_SHIFT_ZOOM;
    right_x -= diffx * PERCENT_SHIFT_ZOOM;
    top_y -= diffy * PERCENT_SHIFT_ZOOM;
    bottom_y += diffy * PERCENT_SHIFT_ZOOM;
    this->update();
}

void MainWindow::on_pushButton_ZoomOut_clicked() {
    left_x -= diffx * PERCENT_SHIFT_ZOOM;
    right_x += diffx * PERCENT_SHIFT_ZOOM;
    top_y += diffy * PERCENT_SHIFT_ZOOM;
    bottom_y -= diffy * PERCENT_SHIFT_ZOOM;
    this->update();
}
