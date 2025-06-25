#include "mainwindow.h"
#include <QApplication>
#include <opencv2/core.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>
#include <iostream>

using namespace std;
using namespace cv;

int main(int argc, char *argv[]) {



    QApplication a(argc, argv);
    MainWindow w;
    w.show();

    return a.exec();
}
