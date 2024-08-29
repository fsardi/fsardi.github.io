import re

def extract_domain(url):
    """
    Extracts the domain name from a URL.
    Handles URLs with http, https, or without a protocol prefix.
    """
    match = re.match(r'(https?://)?([^/]+)', url)
    if match:
        return match.group(2)
    return None

# Read URLs from a text file
with open('urls.txt', 'r') as file:
    urls = file.readlines()

# Set to store unique domains
domains = set()

# Extract domains from the list of URLs
for url in urls:
    url = url.strip()
    domain = extract_domain(url)
    if domain:
        domains.add(domain)

# Open the output script file
with open('mikrotik_dns_script.rsc', 'w') as script:
    
    # Write DNS static entries for each domain
    script.write('/ip dns static\n')
    
    for domain in domains:
        script.write(f'add name={domain} address=10.85.0.8 comment="Blocked domain {domain}"\n')

print("MikroTik DNS script generated successfully.")
