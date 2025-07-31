import requests
import json
import os
import sys
from requests.auth import HTTPBasicAuth

def get_argocd_token(argocd_server, username, password):
    """Get Argo CD authentication token"""
    auth_url = f"{argocd_server}/api/v1/session"
    try:
        response = requests.post(
            auth_url,
            json={"username": username, "password": password},
            verify=False  # For self-signed certificates, use True in production
        )
        response.raise_for_status()
        return response.json()['token']
    except requests.exceptions.RequestException as e:
        print(f"Error getting Argo CD token: {e}")
        sys.exit(1)

def check_application_status(argocd_server, token, app_name):
    """Check application sync status and auto-sync settings"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Get application details
    app_url = f"{argocd_server}/api/v1/applications/{app_name}"
    try:
        response = requests.get(
            app_url,
            headers=headers,
            verify=False  # For self-signed certificates, use True in production
        )
        response.raise_for_status()
        app_data = response.json()
        
        # Extract relevant information
        sync_status = app_data['status']['sync']['status']
        health_status = app_data['status']['health']['status']
        auto_sync = app_data['spec'].get('syncPolicy', {}).get('automated', {})
        is_auto_sync = bool(auto_sync)
        
        # Print status
        print(f"\nApplication Status for {app_name}:")
        print(f"Sync Status: {sync_status}")
        print(f"Health Status: {health_status}")
        print(f"Auto-Sync Enabled: {is_auto_sync}")
        
        if is_auto_sync:
            print("Auto-Sync Settings:")
            print(f"  Prune: {auto_sync.get('prune', False)}")
            print(f"  Self Heal: {auto_sync.get('selfHeal', False)}")
        
        return {
            'sync_status': sync_status,
            'health_status': health_status,
            'auto_sync_enabled': is_auto_sync,
            'auto_sync_settings': auto_sync if is_auto_sync else None
        }
    
    except requests.exceptions.RequestException as e:
        print(f"Error checking application status: {e}")
        sys.exit(1)

def main():
    # Get environment variables
    argocd_server = os.getenv('ARGOCD_SERVER')
    username = os.getenv('ARGOCD_USERNAME')
    password = os.getenv('ARGOCD_PASSWORD')
    app_name = os.getenv('ARGOCD_APP_NAME', 'sample-html-app')
    
    if not all([argocd_server, username, password]):
        print("Please set ARGOCD_SERVER, ARGOCD_USERNAME, and ARGOCD_PASSWORD environment variables")
        sys.exit(1)
    
    # Get authentication token
    token = get_argocd_token(argocd_server, username, password)
    
    # Check application status
    status = check_application_status(argocd_server, token, app_name)
    
    # Exit with status code based on sync status
    if status['sync_status'] != 'Synced':
        sys.exit(1)

if __name__ == "__main__":
    main() 