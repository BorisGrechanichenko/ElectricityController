#include "DeviceConfig.h"

#include "configEditorStrings.h"

using namespace ConfigEditor;

DeviceConfig::DeviceConfig( QString filePath, QObject *parent ) :
    QObject( parent )
{
    settings = new QSettings( filePath, QSettings::IniFormat, this );
    oneRelay = settings->value( RELAY_PINS_GROUP + RELAYS_AMOUNT ).toInt() == 1;
    relay1 = settings->value( RELAY_PINS_GROUP + RELAY1 ).toInt();
    if( !oneRelay )
        relay2 = settings->value( RELAY_PINS_GROUP + RELAY2 ).toInt();
    day = settings->value( CONDITIONS_GROUP + WEEKDAY ).toInt();
    active = settings->value( CONDITIONS_GROUP + ACTIVE_DEVICE ).toBool();
    beginTime.setHMS( settings->value( CONDITIONS_GROUP + BEGIN_HOUR ).toInt(), 0, 0 );
    endTime.setHMS( settings->value( CONDITIONS_GROUP + END_HOUR ).toInt(), 0, 0 );
}

bool DeviceConfig::IsActive() const
{
    return active;
}

int DeviceConfig::ConditionDay() const
{
    return day;
}

const QTime *DeviceConfig::BeginTime() const
{
    return &beginTime;
}

const QTime *DeviceConfig::EndTime() const
{
    return &endTime;
}

bool DeviceConfig::UseOneRelay() const
{
    return oneRelay;
}

ushort DeviceConfig::Relay1() const
{
    return relay1;
}

ushort DeviceConfig::Relay2() const
{
    return relay2;
}

void DeviceConfig::SetActive(bool flag)
{
    active = flag;
}

void DeviceConfig::SetConditionDay(const int &value)
{
    day = value;
    settings->setValue( CONDITIONS_GROUP + WEEKDAY, day );
}

void DeviceConfig::SetBeginTime(const QTime &time)
{
    beginTime = time;
    settings->setValue( CONDITIONS_GROUP + BEGIN_HOUR, beginTime.hour() );
}

void DeviceConfig::SetEndTime(const QTime &time)
{
    endTime = time;
    settings->setValue( CONDITIONS_GROUP + END_HOUR, endTime.hour() );
}

void DeviceConfig::RemoveRelay2()
{
    oneRelay = false;
    settings->setValue( RELAY_PINS_GROUP + RELAYS_AMOUNT, ( oneRelay ? 1 : 2 ) );
}

void DeviceConfig::SetRelay1(const int &number)
{
    relay1 = number;
    settings->setValue( RELAY_PINS_GROUP + RELAY1, relay1 );
}

void DeviceConfig::SetRelay2(const int &number)
{
    relay2 = number;
    oneRelay = false;

    settings->setValue( RELAY_PINS_GROUP + RELAY2, relay2 );
    settings->setValue( RELAY_PINS_GROUP + RELAYS_AMOUNT, 2 );
}
