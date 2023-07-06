# Dictionary

## Prevalent Columns

The following columns provide relevant information for subsequent analysis and/or use in machine learning:

- "time": Timestamp of the earthquake event.
- "mag": Magnitude of the earthquake.
- "cdi": Community Internet Intensity Map, representing the shaking experienced by the community.
- "mmi": Modified Mercalli Intensity, representing the shaking intensity at specific locations.
- "dmin": Minimum distance to the earthquake location.
- "place": Location description of the earthquake.
- "earthquakeType": Type of earthquake.
- "coordinates": Geographic coordinates of the earthquake.
- "alert": Alert level associated with the earthquake.
- "sig": Significance of the earthquake event.
- "tsunami": Tsunami potential associated with the earthquake.
- "country": Country where the seismic event occurred.

---
## Discarded Columns

The following columns have been discarded:

### Code

Removed due to specificity.

### Depth

Removed as its information is used to determine the magnitude, which is already provided.

### Depth Error

Removed because it measures the quality of an unused column (depth).

### Detail

Removed due to specificity.

### Felt

Removed due to highly specific information.

### Gap

Removed because it measures the quality of an unused column (horizontalPos).

### Horizontal Error

Removed because it measures the quality of an unused column (horizontalPos).

### ID

Removed due to excessive specificity. It does not provide information for analysis.

### IDs

Removed due to excessive specificity. It does not provide information for analysis.

### MagError

Removed because it only provides quality information for a single data point (mag).

### MagType

Removed because it contains irrelevant information for analysis.

### MagSource

Removed because it contains irrelevant information for analysis.

### Net

Removed due to excessive specificity of the data.

### NST

Removed because it contains irrelevant information for analysis.

### RMS

Removed due to lack of utility in the analysis, and the complexity of the data makes it difficult to link with other fields.

### Sources

Removed due to excessively incomplete data.

### Status

Removed due to lack of relevance to the topic.

### Title

Removed because it contains redundant information. It is a concatenation of mag + place.

### Types

Removed due to lack of information about provided values.

### TZ

Removed as a consequence of previous decisions. Hours and minutes were eliminated.

### Updated

Removed because it provides information about the website from which the data is extracted.

### URL

Removed due to individuality and lack of contribution to the analysis.
