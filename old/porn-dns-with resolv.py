import re
import socket
import unicodedata
import os

def extract_domain(url):
    """
    Extracts the domain name from a URL.
    Handles URLs with http, https, or without a protocol prefix, and ignores paths or query strings.
    """
    # Remove extraneous spaces and tabs
    url = url.strip().replace('"', '').replace('\t', '').replace(' ', '')
    
    # Regular expression to match the domain part of the URL
    match = re.match(r'(https?://)?([^/]+)', url)
    if match:
        # Extract the domain name
        return match.group(2).split('?')[0].split('/')[0]
    return None

def normalize_domain(domain):
    """
    Normalize domain by converting it to ASCII and replacing non-ASCII characters
    with their closest equivalents.
    """
    domain = unicodedata.normalize('NFKD', domain)
    return domain.encode('ascii', 'ignore').decode('ascii')

def is_resolvable(domain):
    """
    Check if the domain resolves to an IP address.
    """
    try:
        socket.gethostbyname(domain)
        return True
    except socket.error:
        return False

# Set to store unique domains
domains = set()

# Iterate over all .txt files in the directory
for filename in os.listdir():
    if filename.endswith('.txt'):
        # Read URLs from each .txt file
        with open(filename, 'r') as file:
            urls = file.readlines()

        # Extract and normalize domains from each file
        for url in urls:
            domain = extract_domain(url)
            if domain:
                domain = normalize_domain(domain)
                domains.add(domain)

# Lists to store resolving and non-resolving domains
resolving_domains = []
non_resolving_domains = []

# Check which domains resolve and sort them into the appropriate lists
for domain in domains:
    if is_resolvable(domain):
        resolving_domains.append(domain)
    else:
        non_resolving_domains.append(domain)

# Write the resolving domains to a text file
with open('resolving_domains.txt', 'w') as file:
    for domain in resolving_domains:
        file.write(domain + '\n')

# Write the non-resolving domains to a separate text file
with open('non_resolving_domains.txt', 'w') as file:
    for domain in non_resolving_domains:
        file.write(domain + '\n')

# Open the output script file for resolvable domains
with open('blocklist.rsc', 'w') as script:
    
    # Write DNS static entries for each resolvable domain
    script.write('/ip dns static\n')
    
    for domain in resolving_domains:
        script.write(f'add name={domain} address=10.85.0.8\n')

print("MikroTik DNS script generated successfully.")
