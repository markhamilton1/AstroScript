# astrodate - the Package

The ```astrodate``` package is the base functionality of the ```astrocore``` module. As the name implies it contains the functionality to create and manipulate date/time objects. Everything else in the ```astrocore``` module depends on time, so it is strongly recommended that you be familiar with how this package works.

The ```astrodate``` package currently supports 5 time standards: **Local Civil Time**, **Coordinated Universal Time**, **Greenwich Sidereal Time**, **Local Sidereal Time**, and **Terrestrial Dynamic Time**.

* **Local Civil Time (LCT)** - Refers to statutory time scales designated by civilian authorities, or to local time indicated by clocks. This time scale is generally the standard time in a time zone at a fixed offset from Coordinated Universal Time.
* **Coordinated Universal Time (UTC)** - Is the primary time standard by which the world regulates clocks and time. It is within 1 second of mean solar time at 0 degrees longitude; it does NOT observe daylight saving time. This time standard is based on the rotation of the earth with respect to the mean position of the sun.
* **Greenwich Sidereal Time (GST)** - Sidereal time is the measure of the earth's rotation with respect to celestial markers. By convention GST is the measure at the Greenwich Meridian of when the earth's equator intersects with the ecliptic (earth's orbit), called the vernal equinox. This is really just a measure of the average position of the vernal equinox because it neglects the short term effects of nutation.
* **Local Sidereal Time (LST)** - This is the sidereal time adjusted by the observers longitude. This is the time commonly display on an observatory's sidereal clock.
* **Terrestrial Dynamic Time (TDT)** - This is a uniform time standard that was established for computation of planetary motion.

This package includes a number of convenience functions, as well as the AstroDate class itself. For most calculations the AstroDate class will be used, allowing more than one date/time to be used and manipulated at once.

While most of the parameters used by the functions in this package may be well understood, the following is a summary of those that are used and what they mean.

* year - an integer representing the year, and while any whole value can be used for the year, it must be understood that historical and future years will introduce error in some calculations where the equations have been derived from available historical observations, and any values beyond the limits of the available observations are extrapolations.
* month - an integer representing the month starting with 1 for January and ending with 12 for December.
* day - an integer representing the day of the month starting with 1.
* hours - an integer representing an hour value in a 24 hour clock, 0 - 23.
* minutes - an integer representing a minute value, 0 - 59.
* seconds - a float representing a second value, 0.0 - 59.99.
* mode - the indicator of the time scale being used, 'lct', 'utc', 'gst', 'lst', 'tdt'.
* jd - a float representing a julian date value.
* jde - a float representing a Terrestrial Dynamical Time julian date value.
* epochTD - a float representing a Terrestrial Dynamical Time starting point, usually specified as a decimal year (i.e. 1990.0 is the starting point, or epoch, for January 1, 1990 0 hours, 0 minutes, 0.0 seconds).
* dat - a tuple of date/time elements, usually (year, month, day[, hours, minutes, seconds[, mode]]).

The ```astrodate``` package is imported the same as any standard Python package.

```import astrodate as ad```

---

## AstroDate - the Class

The primary functionality of the ```astrodate``` package is the ```AstroDate``` class.

An instance of the AstroDate class can be created using the default constructor. This allocates an EMPTY AstroDate instance.

```a = ad.AstroDate()```

Once allocated, an instance can have the date/time set using a variety of methods. These include:

* ```now(mode='lct')```
* ```set(year, month=1, day=1, hours=0, minutes=0, seconds=0.0, mode='utc')```
* ```set_with_julian(jd, mode='utc')```
* ```set_with_tuple(dat)```

Examples of using these methods are as follows:

```a.now()```

This sets the instance with the current date and local civil time.

```a.set(1980, 6, 27, 10, 30, 45.3, 'utc')```

This sets the instance to the date June 27, 1980 at 10:30:45.3 a.m. UTC.

```a.set_from_julian(2448988.5)``` or ```a.set_from_julian(2448988.5, 'lct')```

If the mode is not specified, then it defaults to 'utc'.

This sets the date to January 1, 1993 0:0:0.0 with either UTC (the default) or LCT (specified).

There are a number of static methods in the AstroDate class to facilitate allocating the instance and setting it with a valid date/time. These methods include:

* ```alloc_with_now(mode='lct')```
* ```alloc(year, month=1, day=1, hours=0, minutes=0, seconds=0.0, mode='utc')```
* ```alloc_with_julian(jd, mode='utc')```
* ```alloc_with_tuple(dat)```
* ```alloc_with_date(date)```

Since these are static methods they must be referenced from the class. For example:

```a = ad.AstroDate().alloc_with_now()```

Once an ```AstroDate``` object has been constructed and populated with the date and time it is often necessary to convert the time to a different standard. This is easily accomplished with the available methods, but there are a number of other properties that should be set to make sure the conversion can take place.

Two of these properties are associated with Local Civil Time and must be set before converting to or from this time standard. They are time zone correction and daylight savings.

The last property needed for conversion is longitude, which is typically needed for conversion to Terrestrial Dynamic Time.

The methods to set these properties are:

* ```set_daylight_savings(ds)```
* ```set_zone_correction(zc)```
* ```set_longitude(lng)```

Examples of use these are:

```a.set_daylight_savings(False)```

The daylight_savings property is a boolean value indicating if daylight_savings is in effect. Set True for yea or False for No.

```a.set_zone_correction(-7)```

The zone_correction property is an integer value that adjusts the time for a particular region. In the above example the time zone correction value of -7 is for the mountain time zone of the United States.

```a.set_longitude(-111.0)```

The longitude property is a float value that is used to adjust to Local Sidereal Time from Greenwich Sidereal Time.

Once the properties have been set, performing conversions is very simple. The available conversion methods are:

* ```to_gst()```
* ```to_lct()```
* ```to_lst()```
* ```to_tdt()```
* ```to_utc()```

```a.to_utc()```

Converts the current time standard to Coordinated Universal Time.

This covers all of the core functionality fo the ```AstroDate``` class. The following is a more complete example of using this functionality.

---

## Example 1:

```python
import astrodate as ad

d = ad.AstroDate().alloc_with_now()
d.set_daylight_savings(False)
d.set_zone_correction(-7)
d.set_longitude(-111.6585)
print d.get_pretty_string()
d.to_utc()
print "%s  (%.2f)" % (d.get_pretty_string(), d.get_julian())
d.to_gst()
print d.get_pretty_string()
d.to_lst()
print d.get_pretty_string()
d.to_tdt()
print "%s  (%.2f)" % (d.get_pretty_string(), d.get_julian())
```