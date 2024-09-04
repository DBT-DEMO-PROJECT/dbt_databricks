import json
import matplotlib.pyplot as plt
from collections import defaultdict
from collections import defaultdict, Counter  # Added Counter import


# Load manifest.json
with open('target/manifest.json') as f:
    manifest = json.load(f)

# Extract resource type counts
resource_types = defaultdict(int)
models = manifest['nodes']

for model_id, model in models.items():
    resource_type = model['resource_type']
    resource_types[resource_type] += 1

# Plot Resource Types
plt.figure(figsize=(12, 8))
plt.bar(resource_types.keys(), resource_types.values(), color='skyblue')
plt.xlabel('Resource Type')
plt.ylabel('Count')
plt.title('Distribution of Resource Types in dbt Manifest')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()  # Adjust layout to avoid clipping
plt.savefig('resource_types_distribution.png')  # Save the plot as an image
plt.close()

# Extract model configurations and metadata
model_configs = defaultdict(list)
model_materializations = defaultdict(int)

for model_id, model in models.items():
    if model['resource_type'] == 'model':
        model_name = model['name']
        materialization = model['config'].get('materialized', 'unknown')
        model_materializations[materialization] += 1
        model_configs[materialization].append(model_name)

# Plot Materialization Types
plt.figure(figsize=(12, 8))
bars = plt.bar(model_materializations.keys(), model_materializations.values(), color='salmon')

# Annotate bars with model names
for bar, mat_type in zip(bars, model_materializations.keys()):
    yval = bar.get_height()
    model_names = ', '.join(model_configs[mat_type])
    plt.text(bar.get_x() + bar.get_width() / 2, yval, model_names, ha='center', va='bottom', fontsize=6, rotation=45)

plt.xlabel('Materialization Type')
plt.ylabel('Count')
plt.title('Model Materialization Types in dbt Manifest')
plt.xticks(rotation=45, ha='right')
plt.subplots_adjust(bottom=0.3, left=0.2, right=0.9, top=0.9)  # Adjust margins to fit all elements
plt.savefig('materialization_types.png')  # Save the plot as an image
plt.close()

# Plot Node Details (Unique ID and File Path Lengths)
unique_ids = [len(node['unique_id']) for node in models.values()]
file_paths = [len(node['path']) for node in models.values()]

plt.figure(figsize=(12, 8))
plt.hist(unique_ids, bins=20, alpha=0.7, label='Unique ID Lengths', color='blue')
plt.hist(file_paths, bins=20, alpha=0.7, label='File Path Lengths', color='green')
plt.xlabel('Length')
plt.ylabel('Frequency')
plt.title('Lengths of Unique IDs and File Paths for Nodes')
plt.legend(loc='upper right')
plt.tight_layout()  # Adjust layout to avoid clipping
plt.savefig('node_details_plot.png')  # Save the plot as an image
plt.close()

# Extract schema information
schemas = defaultdict(int)

for model_id, model in models.items():
    schema = model.get('schema', 'unknown')
    schemas[schema] += 1

# Plot Schema Distribution
plt.figure(figsize=(12, 8))
plt.bar(schemas.keys(), schemas.values(), color='purple')
plt.xlabel('Schema')
plt.ylabel('Number of Tables')
plt.title('Number of Tables per Schema in dbt Manifest')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()  # Adjust layout to avoid clipping
plt.savefig('schema_distribution.png')  # Save the plot as an image
plt.close()

# Extract macro information
macros = manifest.get('macros', {})
macro_names = [macro['name'] for macro in macros.values()]
macro_counts = defaultdict(int)

for macro_name in macro_names:
    macro_counts[macro_name] += 1

# Plot Macro Distribution
plt.figure(figsize=(12, 8))
plt.bar(macro_counts.keys(), macro_counts.values(), color='orange')
plt.xlabel('Macro Name')
plt.ylabel('Count')
plt.title('Distribution of Macros in dbt Manifest')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()  # Adjust layout to avoid clipping
plt.savefig('macro_distribution.png')  # Save the plot as an image
plt.close()

# Load run_results.json
with open('target/run_results.json') as f:
    run_results = json.load(f)

# Extract test results status
statuses = [result['status'] for result in run_results['results']]
status_counts = Counter(statuses)  # Create a Counter object to count status occurrences

# Plot Test Results Status
plt.figure(figsize=(10, 6))
plt.bar(status_counts.keys(), status_counts.values(), color='lightcoral')
plt.xlabel('Test Status')
plt.ylabel('Count')
plt.title('Test Results Status Distribution')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()  # Adjust layout to avoid clipping
plt.savefig('test_results_status.png')  # Save the plot as an image
plt.close()



# Extract execution times
execution_times = [result['execution_time'] for result in run_results['results'] if 'execution_time' in result]

# Plot Execution Times
plt.figure(figsize=(12, 8))
plt.hist(execution_times, bins=20, color='orchid', edgecolor='black')
plt.xlabel('Execution Time (seconds)')
plt.ylabel('Frequency')
plt.title('Distribution of Test Execution Times')
plt.tight_layout()  # Adjust layout to avoid clipping
plt.savefig('test_execution_times_distribution.png')  # Save the plot as an image
plt.close()


# Extract error messages
error_messages = [result['message'] for result in run_results['results'] if result['status'] == 'error']

# Count occurrences of each error message
error_message_counts = Counter(error_messages)

# Plot Error Messages Frequency
plt.figure(figsize=(12, 8))
plt.barh(list(error_message_counts.keys()), list(error_message_counts.values()), color='tomato')
plt.xlabel('Count')
plt.ylabel('Error Message')
plt.title('Frequency of Error Messages')
plt.tight_layout()  # Adjust layout to avoid clipping
plt.savefig('error_messages_frequency.png')  # Save the plot as an image
plt.close()

import json
import matplotlib.pyplot as plt

# Load run_results.json


# Initialize counters
total_tests = len(run_results['results'])
passed_tests = sum(1 for result in run_results['results'] if result['status'] == 'pass')
failed_tests = sum(1 for result in run_results['results'] if result['status'] == 'error')
tests_with_timing = sum(1 for result in run_results['results'] if 'timing' in result)
tests_with_execution = sum(1 for result in run_results['results'] if 'execution_time' in result)
unknown_timelines = total_tests - tests_with_timing
consistent_tests = passed_tests  # Assuming passed tests are consistent for this example

# Calculate metrics
accuracy = (passed_tests / total_tests) * 100
completeness = (tests_with_timing / total_tests) * 100
unknown_timelines_percent = (unknown_timelines / total_tests) * 100
consistency = (consistent_tests / total_tests) * 100

# Create a bar plot for metrics
metrics = {
    'Accuracy (%)': accuracy,
    'Completeness (%)': completeness,
    'Unknown Timelines (%)': unknown_timelines_percent,
    'Consistency (%)': consistency
}

plt.figure(figsize=(10, 6))
plt.bar(metrics.keys(), metrics.values(), color=['green', 'blue', 'orange', 'red'])
plt.xlabel('Metrics')
plt.ylabel('Percentage')
plt.title('dbt Data Quality Metrics')
plt.ylim(0, 100)  # Set the y-axis limit to 100%
plt.tight_layout()  # Adjust layout to avoid clipping
plt.savefig('dbt_data_quality_metrics.png')  # Save the plot as an image
plt.close()

import json
import matplotlib.pyplot as plt
from collections import defaultdict, Counter



# Extract test results
test_results = [result for result in run_results['results'] if 'test' in result['unique_id']]

# Initialize counters
status_counts = Counter()
timeliness_counts = Counter()
unknown_counts = Counter()

for result in test_results:
    status = result['status']
    if status == 'error':
        # Extract errors related to unknowns and timeliness
        if 'unknown' in result['message'].lower():
            unknown_counts['unknown'] += 1
        elif 'timeliness' in result['message'].lower():
            timeliness_counts['timeliness'] += 1
    else:
        status_counts[status] += 1

# Create separate plots for unknown and timeliness
plt.figure(figsize=(14, 6))

# Plot Accuracy and Completeness
plt.subplot(1, 2, 1)
plt.bar(status_counts.keys(), status_counts.values(), color='skyblue')
plt.xlabel('Test Status')
plt.ylabel('Count')
plt.title('Test Status Counts (Accuracy & Completeness)')
plt.xticks(rotation=45, ha='right')

# Plot Unknown and Timeliness
plt.subplot(1, 2, 2)
labels = ['Unknown', 'Timeliness']
counts = [unknown_counts['unknown'], timeliness_counts['timeliness']]
plt.bar(labels, counts, color=['orange', 'green'])
plt.xlabel('Issue Type')
plt.ylabel('Count')
plt.title('Unknown and Timeliness Issues')
plt.xticks(rotation=45, ha='right')

# Adjust layout
plt.tight_layout()
plt.savefig('test_status_summary.png')  # Save the plot as an image
plt.close()
