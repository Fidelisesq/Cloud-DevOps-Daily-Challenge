import json
from datetime import datetime, timedelta

# Load the JSON file
with open('buckets.json') as file:
    buckets = json.load(file)

# Function to calculate days since last accessed
def days_since_last_accessed(last_accessed):
    last_accessed_date = datetime.strptime(last_accessed, '%Y-%m-%d')
    return (datetime.now() - last_accessed_date).days

# Function to print bucket summary
def print_bucket_summary(bucket):
    print(f"Name: {bucket['Name']}")
    print(f"Region: {bucket['Region']}")
    print(f"Size (GB): {bucket['SizeGB']}")
    print(f"Versioning: {'Enabled' if bucket['Versioning'] else 'Disabled'}\n")

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
    if bucket['SizeGB'] > 80 and days_since_last_accessed(bucket['LastAccessed']) > 90:
        large_unused_buckets.append(bucket)
    
    # Highlight buckets for cleanup and deletion queue
    if bucket['SizeGB'] > 50:
        cleanup_candidates.append(bucket)
    if bucket['SizeGB'] > 100 and days_since_last_accessed(bucket['LastAccessed']) > 20:
        deletion_queue.append(bucket)
    
    # Calculate costs for reports
    region_costs.setdefault(bucket['Region'], 0)
    region_costs[bucket['Region']] += bucket['SizeGB'] * bucket['CostPerGB']
    
    department_costs.setdefault(bucket['Department'], 0)
    department_costs[bucket['Department']] += bucket['SizeGB'] * bucket['CostPerGB']

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
    print(f"- {bucket['Name']} (Size: {bucket['SizeGB']} GB)")

# Print deletion queue
print("\nBuckets in Deletion Queue:")
for bucket in deletion_queue:
    print(f"- {bucket['Name']} (Size: {bucket['SizeGB']} GB)")

# Final list of buckets to delete or archive
print("\nFinal List of Buckets to Delete or Archive:")
for bucket in deletion_queue:
    if bucket['SizeGB'] > 100:
        print(f"- {bucket['Name']} (Size: {bucket['SizeGB']} GB) [Move to Glacier]")
    else:
        print(f"- {bucket['Name']} (Size: {bucket['SizeGB']} GB) [Delete]")
