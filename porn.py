import re

def categorize_urls(urls):
    domain_block_list = set()
    content_block_list = {}

    for url in urls:
        url = url.strip()

        # Extract domain and path
        match = re.match(r'(https?://[^/]+)(/.*)?', url)
        if not match:
            continue

        domain = match.group(1).replace('http://', '').replace('https://', '').split('/')[0]
        path = match.group(2)

        if path:
            # If there's a specific path, add to content block list
            if domain not in content_block_list:
                content_block_list[domain] = []
            content_block_list[domain].append(path)
        else:
            # If it's just the domain, add to domain block list
            domain_block_list.add(domain)

    return domain_block_list, content_block_list

# Read URLs from a text file
with open('urls.txt', 'r') as file:
    urls = file.readlines()

# Categorize URLs
domain_block_list, content_block_list = categorize_urls(urls)

# Open the output script file
with open('mikrotik_block_script.rsc', 'w') as script:

    # Create the address lists
    script.write('/ip firewall address-list\n')

    # Address list for full domain blocking
    for domain in domain_block_list:
        script.write(f'add list=block_domains address={domain} comment="Block entire domain: {domain}"\n')

    # Address list for content-based blocking
    for domain in content_block_list.keys():
        script.write(f'add list=layer7_domains address={domain} comment="Layer 7 inspect domain: {domain}"\n')

    # Create Layer 7 Protocols for specific paths
    script.write('/ip firewall layer7-protocol\n')
    
    for domain, paths in content_block_list.items():
        for i, path in enumerate(paths):
            regexp = f'^{re.escape(path)}$'
            script.write(f'add name=layer7_{domain}_{i} regexp="{regexp}"\n')

    # Create Firewall Rules
    script.write('/ip firewall filter\n')

    # Rule to block entire domains
    script.write('add chain=forward action=drop src-address-list=block_domains protocol=tcp dst-port=80,443\n')

    # Rules for Layer 7 inspection
    for domain in content_block_list.keys():
        for i in range(len(content_block_list[domain])):
            script.write(f'add chain=forward action=drop src-address-list=layer7_domains layer7-protocol=layer7_{domain}_{i} protocol=tcp dst-port=80,443\n')

print("MikroTik script generated successfully.")