REP: XXX
Title: NavSat Common Topics, Parameters, and Diagnostic Keys
Author: Chad Rockey <chadrockey@willowgarage.com>
Status: Draft
Type: Informational
Content-Type: text/x-rst
Created: 05-Mar-2013
Post-History: XX-Mar-2013


Abstract
========

This REP defines common topic names, parameter names, and diagnostic key names for Satellite Navigation System Devices, such as GPS receivers, also includes GLONASS, COMPASS, and other systems.

Specification
=============

Topics
----------

The following topics are expected to be common to most devices.  Note that some require multiple calculations from a single receiver.

Required for All Receivers
'''''''''''''''''''''''''''

* fix

  - Driver's suggested solution. (sensor_msgs/NavSatFix)

    This is the default topic that subscribers will expect from a NavSat driver.  The quality of data for this topic could vary depending on the originating receiver.  The driver should publish the most accurate and most compatible solution on this topic.  For example, a driver for a Novatel GPS unit is likely to publish "BESTPOS" (the 'best' currently available position solution) on this topic.  In the case that the device can publish multiple solutions, but the best is not given through hardware, the maintainer of the driver should determine which topic to advertise as "fix".

Strongly Recommended for All Receivers
''''''''''''''''''''''''''''''''''''''

* time_reference

  - Message correlating the current system time with the current time of the NavSat System (sensor_msgs/TimeReference)

    This topic serves to allow global, after-the-fact time-synchronization between multiple navsat connected devices.  In the simplest implementation, this message contains the timestamp of when the computer received a gps timestamp.  In more advanced implementations, this message may represent the system time of a hardware interrupt triggered by a sync signal.

    There are a few common values for the 'source' field within the output TimeReference message.  Some possibilities for this value include: "UTC" for Coordinate Universal Time; "GPS" if the time was sourced from the GPS weeks + offset; "Loran" if computed in Loran-C Long Range Navigation Time; "TAI" if computed in Temps Atomique International

Optional Topics for Multiple Solutions
''''''''''''''''''''''''''''''''''''''

Sometimes it is the case that a device can output more than one computed solution.  For these devices, the following topic names are suggested:

* fix_psuedorange

  - Solution computed using psuedorange information only. (sensor_msgs/NavSatFix)

    This topic represents the least-squares processed solution possible from the receiver.  Psuedorange positions are calculated without ground or satellite based augmentations and without additional filtering or prediction from the receiver.

* fix_augmented

  - Solution computed using augmented information. (sensor_msgs/NavSatFix)

    This topic represents a solution computed using ground or satellite based augmentation to eliminate systematic errors.  This solution should not have excessive filering.

* fix_filtered

  - Solution computed using predictive filtering. (sensor_msgs/NavSatFix)

    Some NavSat receivers can try to optimize a solution by predicting the motion of the device.  These filters can run the risk of diverging due to failed assumptions or invalid covariance estimates.

Parameters
----------

Devices should access as many of these parameters as are relevant.  For example, older devices connect via serial while newer often connect over ethernet.  In this case, newer devices would use ip_address/ip_port, while older devices would use serial_port/serial_baud.  If a parameter is not supported by hardware, it is not necessary to read/write to that parameter.

* ~ip_address (string)

  - Location of the device on the network (only valid for ethernet devices).

* ~ip_port (int)

  - IP port number. (1 to 65535)

* ~serial_port (string)

  - This represents the serial port device (COM4, /dev/tty/USB0).

* ~serial_baud (int)

  - Data transfer rate for a serial device (9600, 115200, and so on)

* ~frame_id (string)

  - The frame of reference reported by the receiver, usually the location of the antenna.  This is a Euclidean frame relative to the vehicle, not a reference ellipsoid.

* ~calibrate_time (boolean)

  - Whether the node should calibrate the device's time offset on startup. If true, the node will    
    exchange of series of messages with the device in order to determine the time delay in the 
    connection. This calibration step is necessary to produce accurate timestamps on
    messages.

* ~time_offset (double)

  - A manually calibrated offset (in seconds) to add to the timestamp before publication of a message.

* ~time_reference_source (string)

  - The string to use as 'source' if it is configurable or indeterminable for other reasons.

Diagnostic Keys
---------------

Devices should publish as many of the following keys that are easy to assume or read from hardware.  These key/value pairs are common among devices of this type.  This list is not considered to be exhaustive and drivers are encouraged to add key/value pairs specific to the hardware.

* "IP Address"

  - Location of the device on the network ex (192.168.1.10) (only valid for ethernet devices).

* "IP Port"

  - IP port number. ex (1 to 65535) (only valid for ethernet devices)

* "Serial Port"

  - This represents the serial port device ex (COM4, /dev/tty/USB0).

* "Serial Baud"

  - Data transfer rate for a serial device ex (9600, 115200)

* "Vendor Name"

  - Name of the device vendor. ex (Hokuyo Automatic Co, Ltd)

* "Product Name"

  - Name of the product or model. ex (UTM-30LX-EW)

* "Firmware Version"

  - Description of the current Firmware version if the hardware has programmable features.
    ex (3.3.01)

* "Firmware Date"

  - Date that the last Firmware version was compiled. ex (23 June 2008)

* "Protocol Version"

  - Description of the communication protocol used.  ex (SCIP 2.0), (LMS COLA-B UDP)

* "Device ID"

  - Serial number or other unique identifier ex (H0906091).'

* "Computed Latency"

  - Offset added to header timestamp to reflect latency in data stream.  ex (-0.013 s)

* "User Time Offset"

  - Offset added to the header timestamp from the parameter '~time_offset'.  ex (-0.551 s)

* Sources

  - Current NavSat systems used.  ex("GPS, GLONASS" or "COMPASS, GALILEO, GLONASS") 

* Available Augmentations

  - Which augmentation services are available.  ex (DGPS), (WAAS), (Basestation ABCD), (Omnistar)

* Used Augmentations

  - Which augmentation services are currently in use.  ex (DGPS), (WAAS), (Basestation ABCD), (Omnistar)

* Satellites Visible

  - Number of satellites visible to the receiver.  ex (10)

* Satellites Used

  - Number of satellites currently used by the receiver.  ex (7)

* GPS Satellites Visible ID

  - PRN (Psuedo Range Noise) identifier for the satellites visible.  ex(7, 19, 11, 28)

* GPS Satellites Visible Elevation

  - Elevation (z) of visible satellites in degrees relative to local horizon.  Order correlates to order reported in GPS Satellites Visible.  ex(25, 85, 42)

* GPS Satellites Visible Azimuth

  - Azimuth of visible satellites in degrees relative to true North.  Order correlates to order reported in GPS Satellites Visible.  ex(102, 346, 16)

* GPS Satellites Visible SNR

  - Signal-to-Noise ratio in decibels for visible satellites.  Order correlates to order reported in GPS Satellites Visible.  ex(42, 11, 25)

* GLONASS Satellites Visible ID

  - GLONASS Slot numbers for the satellites visible.  ex(1, 20, 12, 22)

* GLONASS Satellites Visible Elevation

  - Elevation (z) of visible satellites in degrees relative to local horizon.  Order correlates to order reported in GLONASS Satellites Visible.  ex(25, 85, 42)

* GLONASS Satellites Visible Azimuth

  - Azimuth of visible satellites in degrees relative to true North.  Order correlates to order reported in GLONASS Satellites Visible.  ex(102, 346, 16)

* GLONASS Satellites Visible SNR

  - Signal-to-Noise ratio in decibels for visible satellites.  Order correlates to order reported in GLONASS Satellites Visible.  ex(42, 11, 25)

* COMPASS Satellites Visible ID

  - Unique identifier for the future COMPASS satellite system.  ex(?)

* COMPASS Satellites Visible Elevation

  - Elevation (z) of visible satellites in degrees relative to local horizon.  Order correlates to order reported in COMPASS Satellites Visible.  ex(25, 85, 42)

* COMPASS Satellites Visible Azimuth

  - Azimuth of visible satellites in degrees relative to true North.  Order correlates to order reported in COMPASS Satellites Visible.  ex(102, 346, 16)

* COMPASS Satellites Visible SNR

  - Signal-to-Noise ratio in decibels for visible satellites.  Order correlates to order reported in COMPASS Satellites Visible.  ex(42, 11, 25)

* GALILEO Satellites Visible ID

  - Unique identifier for the future GALILEO satellite system.  ex(?)

* GALILEO Satellites Visible Elevation

  - Elevation (z) of visible satellites in degrees relative to local horizon.  Order correlates to order reported in GALILEO Satellites Visible.  ex(25, 85, 42)

* GALILEO Satellites Visible Azimuth

  - Azimuth of visible satellites in degrees relative to true North.  Order correlates to order reported in GALILEO Satellites Visible.  ex(102, 346, 16)

* GALILEO Satellites Visible SNR

  - Signal-to-Noise ratio in decibels for visible satellites.  Order correlates to order reported in GALILEO Satellites Visible.  ex(42, 11, 25)

* GLONASS Satellites Visible ID

  - GLONASS Slot numbers for the satellites visible.  ex(1, 20, 12, 22)

* GLONASS Satellites Visible Elevation

  - Elevation (z) of visible satellites in degrees relative to local horizon.  Order correlates to order reported in Satellites Visible.  ex(25, 85, 42)

* GLONASS Satellites Visible Azimuth

  - Azimuth of visible satellites in degrees relative to true North.  Order correlates to order reported in Satellites Visible.  ex(102, 346, 16)

* GLONASS Satellites Visible SNR

  - Signal-to-Noise ratio in decibels for visible satellites.  Order correlates to order reported in Satellites Visible.  ex(42, 11, 25)

* Total DOP

  - Total Dilution of Precision - the total of multiplicative effects on GPS accuracy.  ex(7.2)

* PDOP

  - Positional Dilution of Precision - the dilution of precision related to positional accuracy.  ex(5.4)

* HDOP

  - Horizontal Positional Dilution of Precision - the dilution of precision related to horizontal positional accuracy.  ex(1.0)

* VDOP

  - Vertical Positional Dilution of Precision - the dilution of precision related to vertical positional accuracy.  ex(9.0)

* TDOP

  - Temporal Dilution of Precision - the dilution of precision related to temporal accuracy.  ex(2.2)

Rationale
=========

ROS is built on common messages as interfaces to data.  These messages allow software written without the other's knowledge to work together the first time and produce valid output.  In much the same way as these common messages provide consistent software interfaces, this REP provides a consistent user interface to drivers.

The common topics provide easy to connect nodes via launch files between drivers and processing software. Common parameters provide a way to easily reuse configurations between different devices when applicable.  Finally, common topics, parameters, and diagnostic keys provide a consistent user experience between drivers.

The common names also provide a consistent and documented source of names and diagnostics - freeing the author to make better defined software that's more easily validated.

Backwards Compatibility
=======================

It is up to the maintainer of a driver to determine if the driver should be updated to follow this REP.  If a maintainer chooses to update the driver, the current usage should at minimum follow a tick tock pattern where the old usage is deprecated and warns the user, followed by removal of the old usage.  The maintainer may choose to support both standard and custom usage, as well as extend this usage or implement this usage partially depending on the specifics of the driver.


Copyright
=========

This document has been placed in the public domain.



..
   Local Variables:
   mode: indented-text
   indent-tabs-mode: nil
   sentence-end-double-space: t
   fill-column: 70
   coding: utf-8
   End:



