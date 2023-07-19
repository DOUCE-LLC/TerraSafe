# Unearth the Secrets of NOAA API! 🌊🔍📈

Welcome to the grand adventure of uncovering the treasures hidden within the majestic NOAA API! In this mystical .md file, we shall embark on a data quest like no other, exploring, transforming, and understanding the seismic wonders that await us! 🗺️💫

The raw API boasts an impressive array of <b>51 columns</b>, each containing unique insights into seismic events and their mesmerizing details:

Columns: id, year, month, day, hour, locationName, latitude, longitude, eqMagnitude, intensity, damageAmountOrder, housesDestroyedAmountOrder, tsunamiEventId, eqMagMs, publish, deathsTotal, deathsAmountOrderTotal, damageAmountOrderTotal, housesDestroyedAmountOrderTotal, country, regionCode, minute, deaths, deathsAmountOrder, injuries, injuriesAmountOrder, housesDamagedAmountOrder, injuriesTotal, injuriesAmountOrderTotal, housesDamagedAmountOrderTotal, eqDepth, second, eqMagMw, eqMagMb, eqMagUnk, damageMillionsDollars, housesDestroyed, damageMillionsDollarsTotal, housesDestroyedTotal, housesDamaged, housesDamagedTotal, eqMagMl, volcanoEventId, eqMagMfa, missing, missingAmountOrder, missingTotal, missingAmountOrderTotal.

- `id`: 🆔 A unique identifier for each earthquake. Let it guide us through the seismic labyrinth!

- `tsunamiEventId`: 🌊 A unique identifier for the tsunami event associated with the earthquake. A key to unraveling the links between earthquakes and their watery counterparts.

- `volcanoEventId`: 🌋 A unique identifier for the volcanic event associated with the earthquake. An exciting clue that connects seismic activity with volcanic wonders!

- `publish`: 📰 An indicator that reveals if the earthquake information has been published. A glimpse into the dissemination of seismic knowledge!

- `year`, `month`, `day`, `hour`, `minute`, `second`: 🗓️ Time components that construct the timeline of each seismic moment. Let's delve into the history of the earth's tremors!

- `locationName`: 📍 The name of the earthquake's location. An enchanting geographical gem!

- `latitude`, `longitude`: 🌐 Coordinates that guide us to the exact spot of each seismic occurrence. A magical map to the world of quakes!

- `country`, `regionCode`: 🌍 Details about the country and region where the earthquake took place. Unveil the seismic secrets of different corners of the world!

- `eqDepth`: 🚀 The depth of the earthquake in kilometers. A captivating dimension that takes us beneath the surface!

- `eqMagnitude`: 🌋 The magnitude of the earthquake, measuring the unleashed energy at its source. The seismic powerhouses that we seek to understand!

- `intensity`: 🏞️ The intensity of the earthquake, represented by the Mercalli Intensity Scale (mmi). The shaking that reverberates through communities!

Now, brace yourself for the mighty transformations that will elevate our seismic journey to new heights! We'll bid farewell to columns that no longer serve our grand quest and unite similar ones to reveal the true essence of seismic data!

### Columns to Bid Farewell: 🚀

- 'regionCode': A debatable companion, but we can select countries directly in Power BI. Farewell, dear one!

- `id`, `tsunamiEventId`, `publish`, `volcanoEventId`: They served as informative guides but have no place in our ML and analytics endeavors. Farewell, as they journey into the shadows of unrelated tables.

- 'missing', 'missingAmountOrder', 'missingTotal', 'missingAmountOrderTotal': Inessential messengers of missing data that shall not distract us. Farewell!

- 'eqMagMw', 'eqMagMb', 'eqMagUnk', 'eqMagMl', 'eqMagMfa': Diverse magnitudes, but we shall select the most relevant one, `eqMagnitude`. Farewell to the lesser-used, the nulls, and the space they occupy!

Majestic Columns to Unite: 🌟

- `deaths`, `deathsAmountOrder`, `deathsTotal`, `deathsAmountOrderTotal`: Unite these grand columns to reveal the true magnitude of seismic loss. The greatest value shall prevail, and a single column shall showcase the total number of deaths caused by the quake!

- `damageAmountOrder`, `damageAmountOrderTotal`: Merge these fine columns to illuminate the seismic impact on damage. The highest order shall shine!

- `damageMillionsDollars`, `damageMillionsDollarsTotal`: Unite these splendid columns to expose the financial toll of seismic events. A single total shall suffice!

- `housesDestroyed`, `housesDestroyedTotal`, `housesDestroyedAmountOrder`, `housesDestroyedAmountOrderTotal`: Unify these columns to reveal the seismic destruction on homes. A consolidated view shall emerge!

- `injuries`, `injuriesAmountOrder`, `injuriesTotal`, `injuriesAmountOrderTotal`: Merge these columns to illuminate the true toll on human injuries. The highest order shall stand tall!

With these grand transformations, we shall reduce 15 columns to a magnificent 5 to 8, uncovering the essence of seismic data and unlocking invaluable insights into our planet's seismic soul! Let the data adventure begin! 🌏💥📊

## Columns 🌟📊

Here, in our data exploration voyage, we've carefully selected and transformed the most captivating columns from the magnificent NOAA API! Let's unveil the chosen ones and explore their fascinating potential:

- `id`: 🆔 Unique identifier of the earthquake. An essential cornerstone for distinguishing and tracking seismic events.

- `locationName`: 📍 Name of the earthquake location. This captivating column adds geographic charm to our data.

- `latitude`: 🌐 Latitude coordinate of the earthquake. A geographical gem that helps us map the seismic world.

- `longitude`: 🌐 Longitude coordinate of the earthquake. The perfect companion to latitude, guiding us to the exact quake location.

- `eqMagnitude`: 🌋 Magnitude of the earthquake. The powerhouse that measures the energy released during the quake.

- `tsunami`: 🌊 Indicator for a tsunami event associated with the earthquake. An essential piece for assessing tsunami potential.

- `volcano`: 🌋 Indicator for a volcano event associated with the earthquake. A thrilling addition that ties seismic activity with volcanoes!

- `country`: 🌍 Country where the seismic event occurred. An international treasure trove of seismic exploration.

- `eqDepth`: 🚀 Depth of the earthquake in km. A fascinating glimpse into the quake's underground adventures.

- `intensity`: 🏞️ Intensity of the earthquake, measured on the Mercalli Intensity Scale (mmi). Reveals the quake's impact on communities.

- `date`: 🗓️ Date of the earthquake event, combining year, month, day, hour, minute, and second. The timeline that places us in the heart of each seismic moment.

Now, let's delve into the masterful transformations that will truly elevate our data:

- `updatedDeaths`: 💔 Total number of deaths caused by the earthquake and other associated events (tsunami, explosions, etc). A concise and comprehensive view of the seismic impact on human lives.

- `updatedDeathsAmountOrder`: 💔 Ordering of the total number of deaths in comparison with other earthquakes and associated events. Let's identify the most significant seismic tragedies!

- `updatedInjuries`: 🚑 Total number of people injured due to the earthquake. An important factor in understanding the human toll of seismic events.

- `updatedInjuriesAmountOrder`: 🚑 Ordering of the total number of injured people compared to other earthquakes and associated events. Discover the seismic events with the most significant human impact.

- `updatedHousesDamaged`: 🏠 Total number of houses damaged by the earthquake. A crucial metric for assessing infrastructure damage.

- `updatedHousesDamagedAmountOrder`: 🏠 Ordering of the total number of houses damaged in comparison with other earthquakes. Unveil the quakes that left a mark on our dwellings!

- `updatedHousesDestroyed`: 🏚️ Total number of houses destroyed by the earthquake. A powerful indicator of the quake's destruction.

- `updatedHousesDestroyedAmountOrder`: 🏚️ Ordering of the total number of houses destroyed compared to other earthquakes. Unearth the quakes with the most significant impact on homes!

- `updatedDamage`: 💥 Total amount of damage caused by the earthquake in millions of dollars. A monetary reflection of the quake's impact.

- `updatedDamageAmountOrder`: 💥 Ordering of the total amount of damage in comparison with other earthquakes. Discover the most financially impactful seismic events!

With these carefully selected and transformed columns, we've unlocked the true potential of the NOAA API data, allowing us to embark on thrilling seismic analyses and gain invaluable insights into our planet's seismic activity! 🌏🔍📈