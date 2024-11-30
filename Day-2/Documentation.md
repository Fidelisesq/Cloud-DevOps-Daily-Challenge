# Advanced S3 Bucket Metadata Manipulation
![Output](https://github.com/Fidelisesq/Cloud-DevOps-Daily-Challenge/blob/main/Day-2/Script_output3.png)
## Objective
Using a Python script to analyse, modify, and optimise AWS S3 bucket metadata from a JSON file. The script should achieve the following:
- Print a summary of each bucket: Name, region, size (in GB), and versioning status
- Identify buckets larger than 80 GB from every region which are unused for 90+ days.
- Generate a cost report: total s3 buckets cost grouped by region and department.
  Highlight buckets with:
  - Size > 50 GB: Recommend cleanup operations.
  - Size > 100 GB and not accessed in 20+ days should be added to a deletion queue.
- Provide a final list of buckets to delete (from the deletion queue). For archival candidates, suggest moving to Glacier.

## Script Documentation & Explanation
### Task 1: Importing Necessary Modules
```python
import json
from datetime import datetime, timedelta
```
- json: This module is used to parse JSON data.
- datetime, timedelta: These are used to handle dates and times.

### Task 2: Load & Parse the JSON file
```python
with open('buckets.json') as file:
    data = json.load(file)
    buckets = data["buckets"]
```
- Opens the buckets.json file.
- Parses the JSON data from the file.
- Extracts the list of buckets from the parsed data.

### Task 3: Define Helper Function
```python
def days_since_created(created_on):
    created_date = datetime.strptime(created_on, '%Y-%m-%d')
    return (datetime.now() - created_date).days

def print_bucket_summary(bucket):
    print(f"Name: {bucket['name']}")
    print(f"Region: {bucket['region']}")
    print(f"Size (GB): {bucket['sizeGB']}")
    print(f"Versioning: {'Enabled' if bucket['versioning'] else 'Disabled'}\n")
```
- days_since_created: Calculates the number of days since a bucket was created.
- print_bucket_summary: Prints a summary of each bucket’s details (name, region, size, and versioning status).

### Task 4: Initialise Data Structure for Report
```python
large_unused_buckets = []
cleanup_candidates = []
deletion_queue = []
region_costs = {}
department_costs = {}
```
- large_unused_buckets, cleanup_candidates, deletion_queue: Lists to store specific buckets based on defined criteria.
- region_costs, department_costs: Dictionaries to store cost data grouped by region and department.

### Task 5: Analyse & Modify Bucket Data
```python
for bucket in buckets:
    print_bucket_summary(bucket)
    
    if bucket['sizeGB'] > 80 and days_since_created(bucket['createdOn']) > 90:
        large_unused_buckets.append(bucket)
    
    if bucket['sizeGB'] > 50:
        cleanup_candidates.append(bucket)
    if bucket['sizeGB'] > 100 and days_since_created(bucket['createdOn']) > 20:
        deletion_queue.append(bucket)
    
    cost_per_gb = 0.023
    region_costs.setdefault(bucket['region'], 0)
    region_costs[bucket['region']] += bucket['sizeGB'] * cost_per_gb
    
    department = bucket['tags']['team']
    department_costs.setdefault(department, 0)
    department_costs[department] += bucket['sizeGB'] * cost_per_gb
```
- Loop through buckets: Iterates over each bucket in the list.
- Print summary: Calls print_bucket_summary to display details.
- Identify large unused buckets: Adds buckets larger than 80 GB and unused for over 90 days to large_unused_buckets.
- Highlight cleanup candidates: Adds buckets larger than 50 GB to cleanup_candidates.
- Add to deletion queue: Adds buckets larger than 100 GB and not accessed for more than 20 days to deletion_queue.
- Calculate costs: Computes and updates the costs for each region and department.

### Task 6: Generate Cost Report & Cleanup Recommendation
```python
print("\nCost Report by Region:")
for region, cost in region_costs.items():
    print(f"{region}: ${cost:.2f}")

print("\nCost Report by Department:")
for department, cost in department_costs.items():
    print(f"{department}: ${cost:.2f}")
print("\nBuckets Recommended for Cleanup:")
for bucket in cleanup_candidates:
    print(f"- {bucket['name']} (Size: {bucket['sizeGB']} GB)")
```
- Cost Report by Region: Prints the total cost grouped by region.
- Cost Report by Department: Prints the total cost grouped by department.
- Buckets Recommended for Cleanup: Prints the list of buckets recommended for cleanup (those larger than 50 GB).

### Task 7: Generate Deletion Queue & Buckets to Archive
```python
print("\nBuckets in Deletion Queue:")
for bucket in deletion_queue:
    print(f"- {bucket['name']} (Size: {bucket['sizeGB']} GB)")
print("\nFinal List of Buckets to Delete or Archive:")
for bucket in deletion_queue:
    if bucket['sizeGB'] > 100:
        print(f"- {bucket['name']} (Size: {bucket['sizeGB']} GB) [Move to Glacier]")
    else:
        print(f"- {bucket['name']} (Size: {bucket['sizeGB']} GB) [Delete]")
```
- Buckets in Deletion Queue: Prints the list of buckets in the deletion queue (those larger than 100 GB and not accessed for more than 20 days).
- Final List of Buckets to Delete or Archive: Prints the final list of buckets to delete or move to Glacier, based on their size.

## Sample Output
Here is my output when I ran `python s3-analysis.py`
```
Input: Name: prod-data, Region: us-west-2, Size: 120 GB, Versioning: Enabled
Name: dev-app-logs, Region: us-east-1, Size: 10 GB, Versioning: Disabled
Name: backup, Region: eu-central-1, Size: 80 GB, Versioning: Enabled
Name: audit-logs, Region: ap-southeast-1, Size: 50 GB, Versioning: Enabled
Name: test-results, Region: us-west-1, Size: 15 GB, Versioning: Disabled
Name: old-backups, Region: us-east-2, Size: 200 GB, Versioning: Enabled
Name: staging-resources, Region: eu-west-1, Size: 30 GB, Versioning: Disabled
Name: app-analytics, Region: ap-northeast-1, Size: 250 GB, Versioning: Enabled
Name: raw-data, Region: us-west-2, Size: 90 GB, Versioning: Disabled
Name: compliance-data, Region: ca-central-1, Size: 300 GB, Versioning: Enabled

Cost Report by Region:
us-west-2: $4.83
us-east-1: $0.23
eu-central-1: $1.84
ap-southeast-1: $1.15
us-west-1: $0.34
us-east-2: $4.60
eu-west-1: $0.69
ap-northeast-1: $5.75
ca-central-1: $6.90

Cost Report by Department:
analytics: $8.51
engineering: $0.23
ops: $6.44
security: $1.15
qa: $0.34
development: $0.69
data-engineering: $2.07
compliance: $6.90
```

```
Buckets Recommended for Cleanup:
- Name: prod-data, Region: us-west-2, Size: 120 GB
- Name: backup, Region: eu-central-1, Size: 80 GB
- Name: old-backups, Region: us-east-2, Size: 200 GB
- Name: app-analytics, Region: ap-northeast-1, Size: 250 GB
- Name: raw-data, Region: us-west-2, Size: 90 GB
- Name: compliance-data, Region: ca-central-1, Size: 300 GB

Buckets in Deletion Queue:
- Name: prod-data, Region: us-west-2, Size: 120 GB, Days Unused: 414
- Name: old-backups, Region: us-east-2, Size: 200 GB, Days Unused: 1567
- Name: app-analytics, Region: ap-northeast-1, Size: 250 GB, Days Unused: 1352
- Name: compliance-data, Region: ca-central-1, Size: 300 GB, Days Unused: 1063

Final List of Buckets to Delete or Archive:
- Name: prod-data, Region: us-west-2, Size: 120 GB, Days Unused: 414 [Move to Glacier]
- Name: old-backups, Region: us-east-2, Size: 200 GB, Days Unused: 1567 [Move to Glacier]
- Name: app-analytics, Region: ap-northeast-1, Size: 250 GB, Days Unused: 1352 [Move to Glacier]
- Name: compliance-data, Region: ca-central-1, Size: 300 GB, Days Unused: 1063 [Move to Glacier]
Name: prod-data, Region: us-west-2, Size: 120 GB, Versioning: Enabled
Name: dev-app-logs, Region: us-east-1, Size: 10 GB, Versioning: Disabled
Name: backup, Region: eu-central-1, Size: 80 GB, Versioning: Enabled
Name: audit-logs, Region: ap-southeast-1, Size: 50 GB, Versioning: Enabled
Name: test-results, Region: us-west-1, Size: 15 GB, Versioning: Disabled
Name: old-backups, Region: us-east-2, Size: 200 GB, Versioning: Enabled
Name: staging-resources, Region: eu-west-1, Size: 30 GB, Versioning: Disabled
Name: app-analytics, Region: ap-northeast-1, Size: 250 GB, Versioning: Enabled
Name: raw-data, Region: us-west-2, Size: 90 GB, Versioning: Disabled
Name: compliance-data, Region: ca-central-1, Size: 300 GB, Versioning: Enabled

Cost Report by Region:
us-west-2: $4.83
us-east-1: $0.23
eu-central-1: $1.84
ap-southeast-1: $1.15
us-west-1: $0.34
us-east-2: $4.60
eu-west-1: $0.69
ap-northeast-1: $5.75
ca-central-1: $6.90
```

```
Cost Report by Department:
analytics: $8.51
engineering: $0.23
ops: $6.44
security: $1.15
qa: $0.34
development: $0.69
data-engineering: $2.07
compliance: $6.90

Buckets Recommended for Cleanup:
- Name: prod-data, Region: us-west-2, Size: 120 GB
- Name: backup, Region: eu-central-1, Size: 80 GB
- Name: old-backups, Region: us-east-2, Size: 200 GB
- Name: app-analytics, Region: ap-northeast-1, Size: 250 GB
- Name: raw-data, Region: us-west-2, Size: 90 GB
- Name: compliance-data, Region: ca-central-1, Size: 300 GB

Buckets in Deletion Queue:
- Name: prod-data, Region: us-west-2, Size: 120 GB, Days Unused: 414
- Name: old-backups, Region: us-east-2, Size: 200 GB, Days Unused: 1567
- Name: app-analytics, Region: ap-northeast-1, Size: 250 GB, Days Unused: 1352
- Name: compliance-data, Region: ca-central-1, Size: 300 GB, Days Unused: 1063

Final List of Buckets to Delete or Archive:
- Name: prod-data, Region: us-west-2, Size: 120 GB, Days Unused: 414 [Move to Glacier]
- Name: old-backups, Region: us-east-2, Size: 200 GB, Days Unused: 1567 [Move to Glacier]
- Name: app-analytics, Region: ap-northeast-1, Size: 250 GB, Days Unused: 1352 [Move to Glacier]
- Name: compliance-data, Region: ca-central-1, Size: 300 GB, Days Unused: 1063 [Move to Glacier]
```

## Challenges
- Data Parsing Issues: Initially faced issues with JSON parsing due to structure variations. 🛠️
- Colorisation in Terminal: Implementing colored output for better readability took some trial and error. Copilot helped me here 🎨
- Debugging and Validation: Ensuring accurate bucket metadata and handling edge cases was critical. 🕵️‍♂️

## Conclusion
This analysis is crucial for organisations to manage their cloud resources effectively, optimise costs, and ensure efficient storage utilisation. Regular audits and optimisations can lead to significant savings and better resource allocation.

