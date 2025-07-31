#!/bin/bash

# Configuration
ARGO_SERVER=${ARGO_SERVER:-"https://kubernetes.default.svc"}
ARGO_APP_NAME=${ARGO_APP_NAME:-"sample-html-app"}

# Function to check sync status using service account token
check_sync_status() {
    # Get the service account token
    local token=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)
    
    # Get application status
    local response=$(curl -sk \
        -H "Authorization: Bearer ${token}" \
        "${ARGO_SERVER}/api/v1/applications/${ARGO_APP_NAME}")
    
    # Extract sync status
    local sync_status=$(echo $response | jq -r '.status.sync.status')
    local health_status=$(echo $response | jq -r '.status.health.status')
    
    # Check if auto-sync is enabled
    local auto_sync_enabled=$(echo $response | jq -r '.spec.syncPolicy.automated != null')
    
    # Print status
    echo "Application: ${ARGO_APP_NAME}"
    echo "Sync Status: ${sync_status}"
    echo "Health Status: ${health_status}"
    echo "Auto-Sync Enabled: ${auto_sync_enabled}"
    
    # If auto-sync is enabled, show additional details
    if [ "$auto_sync_enabled" = "true" ]; then
        local prune=$(echo $response | jq -r '.spec.syncPolicy.automated.prune')
        local self_heal=$(echo $response | jq -r '.spec.syncPolicy.automated.selfHeal')
        echo "Auto-Sync Settings:"
        echo "  Prune: ${prune}"
        echo "  Self Heal: ${self_heal}"
    fi
    
    # Exit with status code based on sync status
    if [ "$sync_status" != "Synced" ]; then
        return 1
    fi
    return 0
}

main() {
    # Check sync status
    echo "Checking application sync status..."
    if check_sync_status; then
        echo "Application is synced successfully"
        exit 0
    else
        echo "Application is not in sync"
        exit 1
    fi
}

# Run main function
main 