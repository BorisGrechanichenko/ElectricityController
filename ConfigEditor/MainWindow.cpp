#include "MainWindow.h"
#include "ui_MainWindow.h"

#include <QDir>
#include <QStringList>

using namespace ConfigEditor;

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi( this );
    SetLastDevicesList();
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::SetLastDevicesList( QString path )
{
    QDir dir( path );

    QStringList devices = dir.entryList( QDir::Files );
    ui->cbDevices->addItems( devices );
    ui->cbDevices->setCurrentIndex( -1 );

    QSettings relaysConf( path + "/" + GLOBAL_CONFIG );
    QStringList relays;
    for( QString relay : relaysConf.allKeys() )
        relays.append( relaysConf.value( relay ).toString() );
    ui->cbRelay1->addItems( relays );
    ui->cbRelay2->addItems( relays );

    ActivateEditor( false );

    for( auto& file : devices )
    {
        this->devices.append( new DeviceConfig( path + "/" + file, this ) );
    }
}

void MainWindow::ActivateEditor( bool flag )
{
    QList< QWidget* > widgets =
    {
        ui->cbActiveDevice,
        ui->fDeviceSettings
    };
    for( QWidget* widget : widgets )
        widget->setEnabled( flag );
}

void MainWindow::on_cbDevices_currentIndexChanged( int index )
{
    if( index == -1 || index > devices.size() )
        return;

    currentDevice = devices[ index ];

    ui->cbActiveDevice->setChecked( currentDevice->IsActive() );
    ui->cbRelay1->setCurrentText( QString::number( currentDevice->Relay1() ) );
    ui->gbRelay2->setChecked( !currentDevice->UseOneRelay() );
    if( !currentDevice->UseOneRelay() )
        ui->cbRelay2->setCurrentText( QString::number( currentDevice->Relay2() ) );

    ActivateEditor( index != -1 );
}
