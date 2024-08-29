# Open the input file with domain names
with open('prepend.txt', 'r') as infile:
    # Read all lines from the input file
    domains = infile.readlines()

# Open a new file to write the modified URLs
with open('prepended.txt', 'w') as outfile:
    # Loop through each domain and prepend 'https://'
    for domain in domains:
        domain = domain.strip()  # Remove any leading/trailing whitespace or newlines
        if domain:
            outfile.write(f'https://{domain}\n')  # Write the modified URL to the new file

print("URLs have been modified and saved to 'urls_with_protocol.txt'")
