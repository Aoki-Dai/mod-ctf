import re
import base64

def solve():
    with open('queries.txt', 'r') as f:
        lines = f.readlines()
    
    encoded_parts = []
    seen = set()
    
    # regex to capture the part string between exfil. and .internal-sys.local
    # Example: exfil.pmrgq33toqrduise.internal-sys.local.
    pattern = re.compile(r'exfil\.([a-z0-9]+)\.internal-sys\.local')
    
    for line in lines:
        match = pattern.search(line)
        if match:
            # Check for duplicates? Or just append? 
            # Sometimes duplicate queries happen. 
            # Let's see if we should just take them in order.
            # But the pcap generally captures what was sent.
            # If the same exact query appears, it's likely a retransmission.
            # However, looking at the dump, the query IDs are different?
            # actually let's check the dump again.
            
            # Line 70 and 71 have same data?
            # 70: exfil.im5fyxcvonsxe424...
            # 71: exfil.lr2xgzlslroei33d...
            # 61: exfil.im5fyxcvonsxe424... (Same as 70? Wait)
            
            # Let's assume we need to handle duplicates or reordering based on ID maybe?
            # For now, let's just collect them and try to see if they make sense.
            pass

    # Let's just extract all occurrences in order.
    extracted = []
    for line in lines:
        match = pattern.search(line)
        if match:
            data = match.group(1)
            # Filter out immediate duplicates? 
            # Or maybe just all of them.
            extracted.append(data)
            
    # Removing exact adjacent duplicates is usually a good idea in DNS capture 
    # if the client retries simply.
    
    unique_ordered = []
    if extracted:
        unique_ordered.append(extracted[0])
        for x in extracted[1:]:
            if x != unique_ordered[-1]:
                unique_ordered.append(x)
                
    full_string = "".join(unique_ordered)
    print(f"Combined string: {full_string}")
    
    try:
        # Base32 decoding
        # Padding might be needed?
        # Python's b32decode handles padding if missing usually? 
        # No, it's strict about padding usually.
        # But let's try.
        
        # Standard Base32 requires padding '=' to be a multiple of 8 chars.
        # We can add padding manually.
        missing_padding = len(full_string) % 8
        if missing_padding:
            full_string += '=' * (8 - missing_padding)
            
        decoded = base64.b32decode(full_string.upper()) # Base32 is usually uppercase in Python methods?
        print(f"Decoded (Base32): {decoded}")
    except Exception as e:
        print(f"Base32 failed: {e}")
        
    try:
        # Base64 decoding just in case
        decoded64 = base64.b64decode(full_string)
        print(f"Decoded (Base64): {decoded64}")
    except:
        pass

if __name__ == '__main__':
    solve()
