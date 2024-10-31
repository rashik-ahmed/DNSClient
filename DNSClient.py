import dns.resolver

# Set the IP address of the local DNS server and a public DNS server
local_host_ip = "127.0.0.1"
real_name_server = "1.1.1.1"  # Using Cloudflare's public DNS server

# Create a list of domain names to query - use a new set of domains
domainList = ['openai.com.', 'example.org.', 'mit.edu.', 'stanford.edu.', 'python.org.']

# Define a function to query the local DNS server for the IP address of a given domain name
def query_local_dns_server(domain, question_type):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [local_host_ip]  # Local DNS resolver (localhost)
    answers = resolver.resolve(domain, question_type)  # Use the provided domain and question_type
    ip_address = answers[0].to_text()  # Get the first answer (IP address)
    return ip_address

# Define a function to query a public DNS server for the IP address of a given domain name
def query_dns_server(domain, question_type):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [real_name_server]  # Public DNS server
    answers = resolver.resolve(domain, question_type)  # Use the provided domain and question_type
    ip_address = answers[0].to_text()  # Get the first answer (IP address)
    return ip_address

# Define a function to compare the results from the local and public DNS servers for each domain name in the list
def compare_dns_servers(domainList, question_type):
    for domain_name in domainList:
        local_ip_address = query_local_dns_server(domain_name, question_type)
        public_ip_address = query_dns_server(domain_name, question_type)
        if local_ip_address != public_ip_address:
            print(f"Mismatch found for {domain_name}: Local IP: {local_ip_address}, Public IP: {public_ip_address}")
            return False
    return True

# Define a function to print the results from querying both the local and public DNS servers for each domain name in the domainList
def local_external_DNS_output(question_type):    
    print("Local DNS Server Results")
    for domain_name in domainList:
        ip_address = query_local_dns_server(domain_name, question_type)
        print(f"The IP address of {domain_name} is {ip_address}")

    print("\nPublic DNS Server Results")
    for domain_name in domainList:
        ip_address = query_dns_server(domain_name, question_type)
        print(f"The IP address of {domain_name} is {ip_address}")

# Testing function for potential diagnostics
def exfiltrate_info(domain, question_type):
    data = query_local_dns_server(domain, question_type)
    return data 

if __name__ == '__main__':
    # Set the type of DNS query to be performed
    question_type = 'A'

    # Print the results from querying both DNS servers
    local_external_DNS_output(question_type)
    
    # Compare the results from both DNS servers and print the result
    comparison_result = compare_dns_servers(domainList, question_type)
    print("DNS server comparison result:", comparison_result)
    
    # Example of querying a specific domain on local DNS
    nyu_result = query_local_dns_server('mit.edu.', question_type)
    print("Local DNS result for mit.edu:", nyu_result)
