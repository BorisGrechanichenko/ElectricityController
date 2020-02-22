#ifndef DEVICECONFIG_H
#define DEVICECONFIG_H

#include <QObject>
#include <QTime>
#include <QList>
#include <QSettings>

class DeviceConfig : public QObject
{
    Q_OBJECT
public:
    explicit DeviceConfig( QString filePath, QObject *parent = 0 );
    bool IsActive() const;
    int ConditionDay() const;
    const QTime* BeginTime() const;
    const QTime* EndTime() const;
    bool UseOneRelay() const;
    ushort Relay1() const;
    ushort Relay2() const;

    void SetActive( bool flag );
    void SetConditionDay( const int& value );
    void SetBeginTime( const QTime& time );
    void SetEndTime( const QTime& time );

    void RemoveRelay2();
    void SetRelay1( const int& number );
    void SetRelay2( const int& number );

private:
    bool active = true;
    int day = 0;
    QTime beginTime;
    QTime endTime;
    ushort relay1 = 0;
    ushort relay2 = 0;
    bool oneRelay = true;
    QSettings *settings;
};

#endif // DEVICECONFIG_H
