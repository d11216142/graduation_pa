#!/usr/bin/env python3
"""
Generate 50 random CPE (Common Platform Enumeration) data entries.
Fetches CPE data from NVD database and simulates additional fields.
"""

import json
import random
import requests
from datetime import datetime, timedelta
from typing import List, Dict
import time


def get_fallback_cpe_data(num_entries: int = 50) -> List[Dict]:
    """
    Generate CPE data from a fallback dataset of common CPE URIs.
    This is used when NVD API is not accessible or for faster testing.
    
    Args:
        num_entries: Number of CPE entries to generate
        
    Returns:
        List of CPE data dictionaries
    """
    # Common CPE URIs from various software and systems
    common_cpes = [
        "cpe:2.3:a:apache:http_server:2.4.41:*:*:*:*:*:*:*",
        "cpe:2.3:a:nginx:nginx:1.18.0:*:*:*:*:*:*:*",
        "cpe:2.3:a:mysql:mysql:8.0.23:*:*:*:*:*:*:*",
        "cpe:2.3:a:postgresql:postgresql:13.2:*:*:*:*:*:*:*",
        "cpe:2.3:a:php:php:7.4.16:*:*:*:*:*:*:*",
        "cpe:2.3:a:python:python:3.9.2:*:*:*:*:*:*:*",
        "cpe:2.3:a:oracle:jdk:1.8.0:update281:*:*:*:*:*:*",
        "cpe:2.3:a:google:chrome:89.0.4389.90:*:*:*:*:*:*:*",
        "cpe:2.3:a:mozilla:firefox:86.0:*:*:*:*:*:*:*",
        "cpe:2.3:o:microsoft:windows_10:1909:*:*:*:*:*:*:*",
        "cpe:2.3:o:canonical:ubuntu_linux:20.04:*:*:*:lts:*:*:*",
        "cpe:2.3:o:debian:debian_linux:10.0:*:*:*:*:*:*:*",
        "cpe:2.3:o:redhat:enterprise_linux:8.0:*:*:*:*:*:*:*",
        "cpe:2.3:a:docker:docker:20.10.5:*:*:*:*:*:*:*",
        "cpe:2.3:a:kubernetes:kubernetes:1.20.4:*:*:*:*:*:*:*",
        "cpe:2.3:a:redis:redis:6.2.1:*:*:*:*:*:*:*",
        "cpe:2.3:a:mongodb:mongodb:4.4.4:*:*:*:*:*:*:*",
        "cpe:2.3:a:nodejs:node.js:14.16.0:*:*:*:*:*:*:*",
        "cpe:2.3:a:wordpress:wordpress:5.7:*:*:*:*:*:*:*",
        "cpe:2.3:a:jenkins:jenkins:2.277.1:*:*:*:lts:*:*:*",
        "cpe:2.3:a:elastic:elasticsearch:7.11.1:*:*:*:*:*:*:*",
        "cpe:2.3:a:grafana:grafana:7.4.3:*:*:*:*:*:*:*",
        "cpe:2.3:a:mariadb:mariadb:10.5.9:*:*:*:*:*:*:*",
        "cpe:2.3:a:gitlab:gitlab:13.9.3:*:*:*:community:*:*:*",
        "cpe:2.3:a:atlassian:jira:8.14.0:*:*:*:*:*:*:*",
        "cpe:2.3:a:tomcat:tomcat:9.0.44:*:*:*:*:*:*:*",
        "cpe:2.3:a:jetbrains:intellij_idea:2021.1:*:*:*:community:*:*:*",
        "cpe:2.3:a:microsoft:visual_studio_code:1.54.3:*:*:*:*:*:*:*",
        "cpe:2.3:a:ansible:ansible:2.10.7:*:*:*:*:*:*:*",
        "cpe:2.3:a:terraform:terraform:0.14.8:*:*:*:*:*:*:*",
        "cpe:2.3:o:apple:macos:11.2.3:*:*:*:*:*:*:*",
        "cpe:2.3:o:google:android:11.0:*:*:*:*:*:*:*",
        "cpe:2.3:a:slack:slack:4.14.0:*:*:*:*:*:*:*",
        "cpe:2.3:a:zoom:zoom:5.5.4:*:*:*:*:*:*:*",
        "cpe:2.3:a:postman:postman:8.0.10:*:*:*:*:*:*:*",
        "cpe:2.3:a:wireshark:wireshark:3.4.4:*:*:*:*:*:*:*",
        "cpe:2.3:a:virtualbox:virtualbox:6.1.18:*:*:*:*:*:*:*",
        "cpe:2.3:a:vmware:workstation:16.1.0:*:*:*:*:*:*:*",
        "cpe:2.3:a:chef:chef:16.10.17:*:*:*:*:*:*:*",
        "cpe:2.3:a:puppet:puppet:7.4.1:*:*:*:*:*:*:*",
        "cpe:2.3:h:cisco:catalyst_2960:15.2.7:*:*:*:*:*:*:*",
        "cpe:2.3:h:dell:poweredge_r740:2.8.2:*:*:*:*:*:*:*",
        "cpe:2.3:h:hp:proliant_dl380:2.70:*:*:*:*:*:*:*",
        "cpe:2.3:h:raspberry_pi:raspberry_pi_4:1.0:*:*:*:*:*:*:*",
        "cpe:2.3:a:sqlite:sqlite:3.35.0:*:*:*:*:*:*:*",
        "cpe:2.3:a:openssl:openssl:1.1.1k:*:*:*:*:*:*:*",
        "cpe:2.3:a:curl:curl:7.75.0:*:*:*:*:*:*:*",
        "cpe:2.3:a:vim:vim:8.2.2580:*:*:*:*:*:*:*",
        "cpe:2.3:a:git:git:2.30.2:*:*:*:*:*:*:*",
        "cpe:2.3:a:subversion:subversion:1.14.1:*:*:*:*:*:*:*",
        "cpe:2.3:a:mercurial:mercurial:5.7.1:*:*:*:*:*:*:*",
        "cpe:2.3:a:golang:go:1.16.2:*:*:*:*:*:*:*",
        "cpe:2.3:a:rust:rust:1.51.0:*:*:*:*:*:*:*",
        "cpe:2.3:a:ruby:ruby:3.0.0:*:*:*:*:*:*:*",
        "cpe:2.3:a:perl:perl:5.32.1:*:*:*:*:*:*:*",
        "cpe:2.3:o:freebsd:freebsd:12.2:*:*:*:*:*:*:*",
        "cpe:2.3:o:openbsd:openbsd:6.8:*:*:*:*:*:*:*",
        "cpe:2.3:a:dovecot:dovecot:2.3.13:*:*:*:*:*:*:*",
        "cpe:2.3:a:postfix:postfix:3.5.9:*:*:*:*:*:*:*",
        "cpe:2.3:a:bind:bind:9.16.12:*:*:*:*:*:*:*",
        "cpe:2.3:a:squid:squid:4.14:*:*:*:*:*:*:*",
        "cpe:2.3:a:haproxy:haproxy:2.3.7:*:*:*:*:*:*:*",
        "cpe:2.3:a:prometheus:prometheus:2.25.0:*:*:*:*:*:*:*",
        "cpe:2.3:a:consul:consul:1.9.4:*:*:*:*:*:*:*",
        "cpe:2.3:a:vault:vault:1.6.3:*:*:*:*:*:*:*",
        "cpe:2.3:a:etcd:etcd:3.4.15:*:*:*:*:*:*:*",
        "cpe:2.3:a:rabbitmq:rabbitmq:3.8.14:*:*:*:*:*:*:*",
        "cpe:2.3:a:kafka:kafka:2.7.0:*:*:*:*:*:*:*",
        "cpe:2.3:a:zookeeper:zookeeper:3.6.2:*:*:*:*:*:*:*",
        "cpe:2.3:a:memcached:memcached:1.6.9:*:*:*:*:*:*:*",
        "cpe:2.3:a:varnish:varnish:6.5.2:*:*:*:*:*:*:*",
        "cpe:2.3:a:traefik:traefik:2.4.7:*:*:*:*:*:*:*",
        "cpe:2.3:a:minio:minio:2021-03-10:*:*:*:*:*:*:*",
        "cpe:2.3:a:cassandra:cassandra:3.11.10:*:*:*:*:*:*:*",
        "cpe:2.3:a:couchdb:couchdb:3.1.1:*:*:*:*:*:*:*",
        "cpe:2.3:a:influxdb:influxdb:1.8.4:*:*:*:*:*:*:*",
    ]
    
    # Randomly select entries
    if len(common_cpes) >= num_entries:
        selected_cpes = random.sample(common_cpes, num_entries)
    else:
        # If we need more, repeat with different versions
        selected_cpes = random.choices(common_cpes, k=num_entries)
    
    # Convert to the expected format
    result = []
    for cpe_uri in selected_cpes:
        result.append({
            'cpe': {
                'cpeName': cpe_uri
            }
        })
    
    return result


def fetch_cpe_from_nvd(num_entries: int = 50, use_fallback: bool = True) -> List[Dict]:
    """
    Fetch CPE entries from NVD API or use fallback data.
    
    Args:
        num_entries: Number of CPE entries to fetch
        use_fallback: If True, use fallback data instead of API
        
    Returns:
        List of CPE data dictionaries
    """
    if use_fallback:
        print("Using fallback CPE dataset for faster generation...")
        return get_fallback_cpe_data(num_entries)
    
    base_url = "https://services.nvd.nist.gov/rest/json/cpes/2.0"
    
    # Common product keywords to search for
    keywords = [
        "linux", "windows", "apache", "nginx", "mysql", "postgresql",
        "php", "python", "java", "chrome", "firefox", "android",
        "ios", "ubuntu", "debian", "centos", "docker", "kubernetes",
        "redis", "mongodb", "node", "react", "angular", "wordpress"
    ]
    
    all_cpes = []
    
    # Fetch CPEs for different keywords
    for keyword in keywords:
        if len(all_cpes) >= num_entries:
            break
            
        try:
            params = {
                'keywordSearch': keyword,
                'resultsPerPage': 20
            }
            
            response = requests.get(base_url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if 'products' in data:
                    all_cpes.extend(data['products'])
                    print(f"Fetched {len(data['products'])} CPEs for keyword: {keyword}")
            else:
                print(f"Failed to fetch CPEs for keyword: {keyword}, status: {response.status_code}")
            
            # Respect API rate limits
            time.sleep(6)  # NVD API has rate limits
            
        except Exception as e:
            print(f"Error fetching CPEs for keyword {keyword}: {e}")
            continue
    
    # Randomly select entries
    if len(all_cpes) > num_entries:
        selected_cpes = random.sample(all_cpes, num_entries)
    else:
        selected_cpes = all_cpes
    
    return selected_cpes


def parse_cpe_uri(cpe_uri: str) -> Dict[str, str]:
    """
    Parse CPE URI to extract components.
    CPE format: cpe:2.3:part:vendor:product:version:update:edition:language:sw_edition:target_sw:target_hw:other
    
    Args:
        cpe_uri: CPE URI string
        
    Returns:
        Dictionary with parsed CPE components
    """
    parts = cpe_uri.split(':')
    
    result = {
        'category': '*',
        'vendor': '*',
        'product': '*',
        'version': '*'
    }
    
    if len(parts) >= 5:
        # parts[2] is the part (a/o/h)
        result['category'] = parts[2] if parts[2] != '*' else 'a'
        # parts[3] is the vendor
        result['vendor'] = parts[3] if parts[3] != '*' else 'unknown'
        # parts[4] is the product
        result['product'] = parts[4] if parts[4] != '*' else 'unknown'
        # parts[5] is the version if available
        if len(parts) > 5:
            result['version'] = parts[5] if parts[5] != '*' else '1.0'
    
    return result


def generate_simulated_data() -> Dict[str, str]:
    """
    Generate simulated data for date, location, and size.
    
    Returns:
        Dictionary with simulated fields
    """
    # Generate random date within last 2 years
    days_ago = random.randint(0, 730)
    date = datetime.now() - timedelta(days=days_ago)
    
    # Random locations
    locations = [
        "/usr/local/bin", "/opt/software", "/home/user/apps",
        "/var/lib", "/usr/share", "/Applications",
        "C:\\Program Files", "C:\\Users\\Public", "/srv/www",
        "/etc/config", "/data/apps", "/mnt/storage"
    ]
    
    # Random size in MB (between 0.1 and 500 MB)
    size_mb = round(random.uniform(0.1, 500.0), 2)
    
    return {
        'date': date.strftime('%Y-%m-%d'),
        'location': random.choice(locations),
        'size_mb': size_mb
    }


def process_cpe_data(cpe_products: List[Dict]) -> List[Dict]:
    """
    Process CPE products and add simulated data.
    
    Args:
        cpe_products: List of CPE product dictionaries from NVD
        
    Returns:
        List of processed CPE data with all fields
    """
    processed_data = []
    
    for product in cpe_products:
        try:
            cpe_info = product.get('cpe', {})
            cpe_name = cpe_info.get('cpeName', '')
            
            if not cpe_name:
                continue
            
            # Parse CPE URI
            parsed_cpe = parse_cpe_uri(cpe_name)
            
            # Generate simulated data
            simulated = generate_simulated_data()
            
            # Combine all data
            entry = {
                'category': parsed_cpe['category'],
                'product': parsed_cpe['product'],
                'version': parsed_cpe['version'],
                'vendor': parsed_cpe['vendor'],
                'date': simulated['date'],
                'location': simulated['location'],
                'size_mb': simulated['size_mb']
            }
            
            processed_data.append(entry)
            
        except Exception as e:
            print(f"Error processing CPE entry: {e}")
            continue
    
    return processed_data


def save_to_json(data: List[Dict], filename: str = 'cpe_data.json'):
    """Save CPE data to JSON file."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(data)} entries to {filename}")


def save_to_csv(data: List[Dict], filename: str = 'cpe_data.csv'):
    """Save CPE data to CSV file."""
    import csv
    
    if not data:
        print("No data to save")
        return
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['category', 'product', 'version', 'vendor', 'date', 'location', 'size_mb']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(data)
    
    print(f"Saved {len(data)} entries to {filename}")


def print_summary(data: List[Dict]):
    """Print summary of generated data."""
    print("\n" + "="*80)
    print("CPE Data Generation Summary")
    print("="*80)
    print(f"Total entries: {len(data)}")
    
    # Category breakdown
    categories = {}
    for entry in data:
        cat = entry['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    print("\nCategory breakdown:")
    category_names = {'a': 'Application', 'o': 'Operating System', 'h': 'Hardware'}
    for cat, count in categories.items():
        cat_name = category_names.get(cat, cat)
        print(f"  {cat_name} ({cat}): {count}")
    
    # Show first 5 entries as examples
    print("\nFirst 5 entries:")
    print("-"*80)
    for i, entry in enumerate(data[:5], 1):
        print(f"\n{i}. Category: {entry['category']} | Product: {entry['product']} | "
              f"Version: {entry['version']}")
        print(f"   Vendor: {entry['vendor']}")
        print(f"   Date: {entry['date']} | Location: {entry['location']} | "
              f"Size: {entry['size_mb']} MB")
    print("="*80 + "\n")


def main():
    """Main function to generate CPE data."""
    import sys
    
    # Check if user wants to use NVD API (slower but real-time data)
    use_api = '--api' in sys.argv
    
    print("Starting CPE data generation...")
    if use_api:
        print("Using NVD API (this may take several minutes due to rate limits)...\n")
    else:
        print("Using fallback dataset (faster generation)...")
        print("Use --api flag to fetch from NVD API instead.\n")
    
    # Fetch CPE data from NVD or fallback
    cpe_products = fetch_cpe_from_nvd(num_entries=50, use_fallback=not use_api)
    
    if not cpe_products:
        print("Failed to fetch CPE data")
        return
    
    # Process and add simulated data
    processed_data = process_cpe_data(cpe_products)
    
    if not processed_data:
        print("No valid CPE data was processed")
        return
    
    # Ensure we have at least 50 entries (or as many as possible)
    if len(processed_data) < 50:
        print(f"Warning: Only generated {len(processed_data)} entries (requested 50)")
    
    # Save to files
    save_to_json(processed_data)
    save_to_csv(processed_data)
    
    # Print summary
    print_summary(processed_data)


if __name__ == '__main__':
    main()
