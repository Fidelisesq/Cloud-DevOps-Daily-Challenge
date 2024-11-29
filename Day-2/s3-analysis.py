import json
from datetime import datetime, timedelta

# Load the JSON file
with open('buckets.json') as file:
    data = json.load(file)
    buckets = data["buckets"]

# Function to calculate days since last accessed
def days_since_created(created_on):
    created_date = datetime.strptime(created_on, '%Y-%m-%d')
    return (datetime.now() - created_date).days

# Function to print bucket summary
def print_bucket_summary(bucket):
    print(f"Name: {bucket['name']}")
    print(f"Region: {bucket['region']}")
    print(f"Size (GB): {bucket['sizeGB']}")
    print(f"Versioning: {'Enabled' if bucket['versioning'] else 'Disabled'}\n")

# Initialize data structures for reports
large_unused_buckets = []
cleanup_candidates = []
deletion_queue = []
region_costs = {}
department_costs = {}

# Analyze and modify bucket data
for bucket in buckets:
    # Print bucket summary
    print_bucket_summary(bucket)
    
    # Identify buckets larger than 80 GB and unused for 90+ days
    if bucket['sizeGB'] > 80 and days_since_created(bucket['createdOn']) > 90:
        large_unused_buckets.append(bucket)
    
    # Highlight buckets for cleanup and deletion queue
    if bucket['sizeGB'] > 50:
        cleanup_candidates.append(bucket)
    if bucket['sizeGB'] > 100 and days_since_created(bucket['createdOn']) > 20:
        deletion_queue.append(bucket)
    
    # Calculate costs for reports
    cost_per_gb = 0.023 # Assuming a cost per GB
    region_costs.setdefault(bucket['region'], 0)
    region_costs[bucket['region']] += bucket['sizeGB'] * cost_per_gb
    
    department = bucket['tags']['team']
    department_costs.setdefault(department, 0)
    department_costs[department] += bucket['sizeGB'] * cost_per_gb

# Generate cost reports
print("\nCost Report by Region:")
for region, cost in region_costs.items():
    print(f"{region}: ${cost:.2f}")

print("\nCost Report by Department:")
for department, cost in department_costs.items():
    print(f"{department}: ${cost:.2f}")

# Print cleanup recommendations
print("\nBuckets Recommended for Cleanup:")
for bucket in cleanup_candidates:
    print(f"- {bucket['name']} (Size: {bucket['sizeGB']} GB)")

# Print deletion queue
print("\nBuckets in Deletion Queue:")
for bucket in deletion_queue:
    print(f"- {bucket['name']} (Size: {bucket['sizeGB']} GB)")

# Final list of buckets to delete or archive
print("\nFinal List of Buckets to Delete or Archive:")
for bucket in deletion_queue:
    if bucket['sizeGB'] > 100:
        print(f"- {bucket['name']} (Size: {bucket['sizeGB']} GB) [Move to Glacier]")
    else:
        print(f"- {bucket['name']} (Size: {bucket['sizeGB']} GB) [Delete]")
