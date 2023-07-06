# Index

1. [Alert](#1-alert)
2. [CDI](#2-cdi)
3. [Code](#3-code)
4. [Depth](#4-depth)
5. [Depth Error](#5-deptherror)
6. [Detail](#6-detail)
7. [Dmin](#7-dmin)
8. [Felt](#8-felt)
9. [Gap](#9-gap)
10. [Horizontal Error](#10-horizontalerror)
11. [ID](#11-id)
12. [IDs](#12-ids)
13. [Latitude](#13-latitude)
14. [Location Source](#14-locationsource)
15. [Longitude](#15-longitude)
16. [Magnitude](#16-mag)
17. [MagType](#17-magtype)
18. [MMI](#18-mmi)
19. [Net](#19-net)
20. [Nst](#20-nst)
21. [Place](#21-place)
22. [Rms](#22-rms)
23. [Sig](#23-sig)
24. [Sources](#24-sources)
25. [Status](#25-status)
26. [Time](#26-time)
27. [Title](#27-title)
28. [Tsunami](#28-tsunami)
29. [Type](#29-type)
30. [Types](#30-types)
31. [Tz](#31-tz)
32. [Updated](#32-updated)
33. [Url](#33-url)
---

## 1. Alert

**Data Type:** String

**Typical Values:** "green", "yellow", "orange", "red"

**Description:** The alert level from the PAGER earthquake impact scale.

---

## 2. CDI

**Data Type:** Decimal

**Typical Values:** [0.0, 10.0]

**Description:** The maximum reported intensity for the event. Computed by DYFI. While typically reported as a roman numeral, for the purposes of this API, intensity is expected as the decimal equivalent of the roman numeral.

---

## 3. Code

**Data Type:** String

**Description:** An identifying code assigned by - and unique from - the corresponding source for the event.

---

## 4. Depth

**Data Type:** Decimal

**Typical Values:** [0, 1000]

**Description:** Depth of the event in kilometers.
Additional Information: The depth where the earthquake begins to rupture...

---

## 5. Depth Error

**Data Type:** Decimal

**Typical Values:** [0, 100]

**Description:** Uncertainty of reported depth of the event in kilometers.
Additional Information: The depth error, in km, defined as the largest projection...

---

## 6. Detail

**Data Type:** String

**Description:** Link to GeoJSON detail feed from a GeoJSON summary feed.
NOTE: When searching and using geojson with callback, no callback is included in the detail url.

---

## 7. Dmin

**Data Type:** Decimal

**Typical Values:** [0.4, 7.1]

**Description:** Horizontal distance from the epicenter to the nearest station (in degrees). 1 degree is approximately 111.2 kilometers...

---

## 8. Felt

**Data Type:** Integer

**Typical Values:** [44, 843]

**Description:** The total number of felt reports submitted to the DYFI system.

---

## 9. Gap

**Data Type:** Decimal

**Typical Values:** [0.0, 180.0]

**Description:** The largest azimuthal gap between azimuthally adjacent stations (in degrees). In general, the smaller this number...

---

## 10. Horizontal Error

**Data Type:** Decimal

**Typical Values:** [0, 100]

**Description:** Uncertainty of reported location of the event in kilometers.
Additional Information: The horizontal location error, in km, defined as the length...

---

## 11. ID

**Data Type:** String

**Typical Values:** A (generally) two-character network identifier with a (generally) eight-character network-assigned code.

**Description:** A unique identifier for the event. This is the current preferred id for the event, and may change over time...

---

## 12. IDs

**Data Type:** String

**Typical Values:** ",ci15296281,us2013mqbd,at00mji9pf,"

**Description:** A comma-separated list of event ids that are associated to an event.

---

## 13. Latitude

**Data Type:** Decimal

**Typical Values:** [-90.0, 90.0]

**Description:** Decimal degrees latitude. Negative values for southern latitudes.
Additional Information: An earthquake begins to rupture at a hypocenter which is defined by a position on the surface...

---

## 14. Location Source

**Data Type:** String

**Typical Values:** ak, at, ci, hv, ld, mb, nc, nm, nn, pr, pt, se, us, uu, uw

**Description:** The network that originally authored the reported location of this event.

---

## 15. Longitude

**Data Type:** Decimal

**Typical Values:** [-180.0, 180.0]

**Description:** Decimal degrees longitude. Negative values for western longitudes.
Additional Information: An earthquake begins to rupture at a hypocenter which is defined by a position on the surface...

---

## 16. Magnitude

**Data Type:** Decimal

**Typical Values:** [-1.0, 10.0]

**Description:** The magnitude for the event. See also magType.
Additional Information: The magnitude reported is that which the U.S. Geological Survey considers official for this earthquake...

---

### 17. MagType

**Data Type:** String

**Description:** The type of magnitude associated with the event (e.g., "ml" for local magnitude, "mb" for body wave magnitude, "md" for duration magnitude, "mw" for moment magnitude).

---

### 18. Mmi

**Data Type:** Decimal

**Typical Values:** [0.0, 10.0]

**Description:** The Modified Mercalli Intensity (MMI) reported for the event. MMI is a measure of shaking intensity based on observed effects.

---

### 19. Net

**Data Type:** String

**Typical Values:** ak, at, ci, hv, ld, mb, nc, nm, nn, pr, pt, se, us, uu, uw

**Description:** The network that contributed to this event.

---

### 20. Nst

**Data Type:** Integer

**Description:** The total number of seismic stations used to determine earthquake location.

---

### 21. Place

**Data Type:** String

**Description:** Textual description of named geographic region near to the event. This may be a city name, or a FIPS code, depending on the availability of appropriate data.

---

### 22. Rms

**Data Type:** Decimal

**Description:** The root-mean-square (RMS) travel time residual, in seconds, using all weights. This parameter provides a measure of the fit of the observed arrival times to the predicted arrival times for this location. Smaller numbers indicate a better fit of the data.

---

### 23. Sig

**Data Type:** Integer

**Description:** A number describing how significant the event is. Larger numbers indicate a more significant event.

---

### 24. Sources

**Data Type:** String

**Description:** A comma-separated list of network contributors.

---

### 25. Status

**Data Type:** String

**Description:** The status of the event, such as "automatic" or "reviewed".

---

### 26. Time

**Data Type:** Integer

**Description:** The time when the event occurred, in milliseconds since the epoch.

---

### 27. Title

**Data Type:** String

**Description:** A brief summary of the event, suitable for display purposes.

---

### 28. Tsunami

**Data Type:** Integer

**Description:** A flag indicating whether or not a tsunami was generated by the event. The value is 1 for true, and 0 for false.

---

### 29. Type

**Data Type:** String

**Description:** The type of seismic event (e.g., "earthquake", "quarry blast", "sonic boom").

---

### 30. Types

**Data Type:** String

**Description:** A comma-separated list of product types associated with this event.

---

### 31. Tz

**Data Type:** Integer

**Description:** The number of seconds between the origin time and the time at which the tsunami wave was first recorded.

---

### 32. Updated

**Data Type:** Integer

**Description:** The time when the event was most recently updated, in milliseconds since the epoch.

---

### 33. Url

**Data Type:** String

**Description:** A URL for more information about the event.

