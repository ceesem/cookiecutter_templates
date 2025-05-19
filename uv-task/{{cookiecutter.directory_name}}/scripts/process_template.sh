#!/bin/bash

# Check for correct number of arguments
if [[ $# -ne 2 ]]; then
  echo "Usage: $0 <env_file1> <env_file2>"
  exit 1
fi

# Check if environment files exist and are readable
if [[ ! -r "$1" ]]; then
  echo "Error: Environment file '$1' not found or not readable."
  exit 1
fi

if [[ ! -r "$2" ]]; then
  echo "Error: Environment file '$2' not found or not readable."
  exit 1
fi

# Source environment files with error checking
set -a
if ! source "$1"; then
  echo "Error: Failed to source environment file '$1'."
  exit 1
fi

if ! source "$2"; then
  echo "Error: Failed to source environment file '$2'."
  exit 1
fi
set +a

# Check if template files exist
if [[ ! -r "templates/kube-task.yml" ]]; then
        echo "Error: template file templates/kube-task.yml does not exist or is not readable"
        exit 1
fi

if [[ ! -r "templates/make_cluster.sh" ]]; then
        echo "Error: template file templates/make_cluster.sh does not exist or is not readable"
        exit 1
fi

# Run envsubst with error checking and redirect output
if ! envsubst < "templates/kube-task.yml" > "scripts/kube-task.yml"; then
  echo "Error: Failed to run envsubst on templates/kube-task.yml"
  exit 1
fi

if ! envsubst < "templates/make_cluster.sh" > "scripts/make_cluster.sh"; then
  echo "Error: Failed to run envsubst on templates/make_cluster.sh"
  exit 1
fi

if ! envsubst < "templates/delete_cluster.sh" > "scripts/delete_cluster.sh"; then
  echo "Error: Failed to run envsubst on templates/delete_cluster.sh"
  exit 1
fi

echo "Templates configured successfully."
exit 0