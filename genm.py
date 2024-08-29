# Example Python script to create MikroTik DNS static entries

# Read the list of domains from the urls.txt file
with open('urls.txt', 'r') as file:
    domains = file.readlines()

# Specify the IP address to which all domains should be redirected
redirect_ip = "142.250.78.110"

# Open a file to save the MikroTik script
with open('mikrotik_dns_script.rsc', 'w') as script_file:
    for domain in domains:
        domain = domain.strip()
        if domain:
            script_file.write(f'/ip dns static add address={redirect_ip} name={domain}\n')

print("MikroTik DNS script has been generated as 'mikrotik_dns_script.rsc'")
