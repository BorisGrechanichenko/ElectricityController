#ifndef CONFIGEDITORSTRINGS_H
#define CONFIGEDITORSTRINGS_H

#include <QString>

namespace ConfigEditor
{
const QString   DEFAULT_PATH =          "/home/pi/Documents/Projects/Controller/config";
const QString   GLOBAL_CONFIG =         "global_config.conf";

// settings file
const QString   RELAY_PINS_GROUP =      "relay_pins/";
const QString   RELAYS_AMOUNT =         "amount";
const QString   RELAY1 =                "relay1";
const QString   RELAY2 =                "relay2";
const QString   CONDITIONS_GROUP =      "conditions/";
const QString   ACTIVE_DEVICE =         "active";
const QString   WEEKDAY =               "weekday";
const QString   BEGIN_HOUR =            "begin_hour";
const QString   END_HOUR =              "end_hour";

// day modes
const QString   DAY_MODE_EVERY_DAY =    "Every day";
const QString   DAY_MODE_MON_TO_FRI =   "Monday - Friday 12am";
const QString   DAY_MODE_FRI_TO_SUN =   "Friday 12am - Sunday";
const QString   DAY_MODE_MONDAY =       "Monday";
const QString   DAY_MODE_TUESDAY =      "Tuesday";
const QString   DAY_MODE_WEDNESDAY =    "Wednesday";
const QString   DAY_MODE_THURSDAY =     "Thursday";
const QString   DAY_MODE_FRIDAY =       "Friday";
const QString   DAY_MODE_SATURDAY =     "Saturday";
const QString   DAY_MODE_SUNDAY =       "Sunday";
}

#endif // CONFIGEDITORSTRINGS_H
