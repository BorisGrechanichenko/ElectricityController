#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QList>

#include "DeviceConfig.h"

#include "configEditorStrings.h"

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow( QWidget *parent = 0 );
    ~MainWindow();

private slots:
    void on_cbDevices_currentIndexChanged( int index );

private:
    Ui::MainWindow *ui;
    QList< DeviceConfig* > devices;
    DeviceConfig* currentDevice = nullptr;

    void SetLastDevicesList( QString path = ConfigEditor::DEFAULT_PATH );
    void ActivateEditor( bool flag );
};

#endif // MAINWINDOW_H
