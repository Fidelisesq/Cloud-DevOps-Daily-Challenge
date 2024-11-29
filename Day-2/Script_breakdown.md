# Advanced S3 Bucket Metadata Manipulation

## Objective
Using a Python script to analyse, modify, and optimise AWS S3 bucket metadata from a JSON file. The script should achieve the following:
- Print a summary of each bucket: Name, region, size (in GB), and versioning status
- Identify buckets larger than 80 GB from every region which are unused for 90+ days.
- Generate a cost report: total s3 buckets cost grouped by region and department.
  Highlight buckets with:
  - Size > 50 GB: Recommend cleanup operations.
  - Size > 100 GB and not accessed in 20+ days should be added to a deletion queue.
- Provide a final list of buckets to delete (from the deletion queue). For archival candidates, suggest moving to Glacier.

### Script Documentation & Explanation
`
import json

from datetime import datetime, timedelta
`
- json: This module is used to parse JSON data.
- datetime, timedelta: These are used to handle dates and times.



