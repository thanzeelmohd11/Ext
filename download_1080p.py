import requests
import os
from urllib.parse import urljoin

def download_m3u8_segments(m3u8_url, output_dir="segments"):
    """Download all segments from a 1080p M3u8 playlist"""
    
    # Create output directory
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    try:
        # Fetch the M3u8 playlist
        print(f"Fetching M3u8 from: {m3u8_url}")
        response = requests.get(m3u8_url, timeout=10)
        response.raise_for_status()
        
        lines = response.text.strip().split('\n')
        
        # Extract segment URLs
        segments = []
        for line in lines:
            line = line.strip()
            # Skip comments and empty lines
            if line and not line.startswith('#'):
                # Convert relative URLs to absolute URLs
                segment_url = urljoin(m3u8_url, line)
                segments.append(segment_url)
        
        print(f"\nFound {len(segments)} segments\n")
        
        # Display segment URLs
        print("Segment URLs:")
        print("-" * 80)
        for i, segment in enumerate(segments, 1):
            print(f"{i}. {segment}")
        
        # Option to download
        print("\n" + "-" * 80)
        download_choice = input("Download all segments? (y/n): ").lower()
        
        if download_choice == 'y':
            downloaded = 0
            for i, segment_url in enumerate(segments, 1):
                try:
                    print(f"\nDownloading segment {i}/{len(segments)}...", end=" ")
                    seg_response = requests.get(segment_url, timeout=30)
                    seg_response.raise_for_status()
                    
                    # Save segment
                    filename = os.path.join(output_dir, f"segment_{i:04d}.ts")
                    with open(filename, 'wb') as f:
                        f.write(seg_response.content)
                    
                    print(f"✓ Saved: {filename}")
                    downloaded += 1
                    
                except Exception as e:
                    print(f"✗ Error: {e}")
            
            print(f"\n✓ Downloaded {downloaded}/{len(segments)} segments to '{output_dir}/'")
        else:
            print("Download cancelled.")
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching M3u8: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    url = "https://mzaalombr.pc.cdn.bitgravity.com/mzaalombr/output/Thazhuara/stream_1080p.m3u8"
    download_m3u8_segments(url)