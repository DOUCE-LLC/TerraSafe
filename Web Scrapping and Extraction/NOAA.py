#!/usr/bin/env python
"""Query NCEI's Hazard Event Lookup (HazEL) API for earthquake information.  See the API documentation at
   https://www.ngdc.noaa.gov/hazel/view/swagger on how to perform this and other queries.
"""
# Module loading
import argparse
import json
import requests
import time as clock

__author__ = "Aaron Sweeney"
__credits__ = ["Aaron Sweeney"]
__license__ = "GNU General Public License, version 3.0"
__version__ = "1.0"
__email__ = "aaron.sweeney@colorado.edu"
__status__ = "Development"


def get_earthquakes(min_year, max_year, min_eq_magnitude):
    """Return information about all earthquakes occurring between min_year and max_year and greater than
    min_eq_magnitude. Consult the API docs at https://www.ngdc.noaa.gov/hazel/view/swagger for details.

    Args:
      min_year (int): minimum year of earthquake query
      max_year (int): maximum year of earthquake query
      min_eq_magnitude (float): minimum earthquake magnitude of query

    Returns:
      dict containing query results [JSON]
    """
    # Define components of Hazard Event Lookup (HazEL) query:
    protocol = "https://"
    host = "www.ngdc.noaa.gov"
    service = "/hazel/hazard-service/api/v1/earthquakes"
    # Consult the API docs at https://www.ngdc.noaa.gov/hazel/view/swagger for different "service" endpoints.

    payload = {
        'minYear': str(min_year),
        'maxYear': str(max_year),
        'minEqMagnitude': str(min_eq_magnitude)
    }

    data = {}
    with requests.Session() as s:
        download = s.get(protocol + host + service, params=payload)
        data = download.json()

    return data


if __name__ == "__main__":

    # Let's track how long this takes.
    program_start_time = clock.time()

    parser = argparse.ArgumentParser(
        description='Query the NCEI Hazard Event Lookup (HazEL) API for earthquakes, based on a given '
                    'min/max year and minimum magnitude.'
        )
    parser.add_argument('-y1', '--min_year', metavar='min_year', type=int,
                        required=True, help='Minimum year for query.')
    parser.add_argument('-y2', '--max_year', metavar='max_year', type=int,
                        required=True, help='Maximum year for query.')
    parser.add_argument('-m1', '--min_eq_magnitude', metavar='min_eq_magnitude', type=float,
                        required=True, help='Minimum earthquake magnitude for query.')
    args = parser.parse_args()

    min_year = args.min_year
    max_year = args.max_year
    min_eq_magnitude = args.min_eq_magnitude

    results = get_earthquakes(min_year, max_year, min_eq_magnitude)

    # Print JSON with human-readable spacing:
    print(json.dumps(results, sort_keys=True, indent=4, separators=(',', ': ')))

    # Capture the program's execution time.
    elapsed_time = clock.time() - program_start_time
    print('Program Execution Time [s]: {:0.3f}'.format(elapsed_time))
