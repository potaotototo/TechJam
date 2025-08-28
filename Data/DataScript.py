import json
import csv
import re
import gzip
from datetime import datetime
from typing import Dict, List, Any
import os
import stat

FILE_DATA_PATH = "D:\private\Techjam\Data\Alaska\review-Alaska.json\review-Alaska.json"
COMPRESSED_FILE_DATA_PATH = "D:\private\Techjam\Data\Alaska\review-Alaska.json.gz"
def test_file_access():
    import os
    import gzip
    
    # Test both files
    files_to_test = [
        COMPRESSED_FILE_DATA_PATH,  # Try .gz first
        FILE_DATA_PATH
    ]
    
    for file_path in files_to_test:
        print(f"\nTesting file: {file_path}")
        print(f"Absolute path: {os.path.abspath(file_path)}")
        print(f"File exists: {os.path.exists(file_path)}")
        
        if file_path.endswith('.gz'):
            try:
                with gzip.open(file_path, 'rt', encoding='utf-8') as f:
                    content = f.read(100)
                    print("✓ Gzip file works!")
                    return file_path  # Return working file path
            except Exception as e:
                print(f"✗ Gzip file failed: {e}")
        else:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read(100)
                    print("✓ Regular file works!")
                    return file_path  # Return working file path
            except Exception as e:
                print(f"✗ Regular file failed: {e}")
    
    return None

def load_json_file(filepath: str) -> List[Dict]:
    """Load JSON data from file. Handles JSON arrays, single objects, and JSONL format."""
    
    data_list = []
    
    # Check if it's a .gz file
    if filepath.endswith('.gz'):
        file_opener = lambda: gzip.open(filepath, 'rt', encoding='utf-8')
    else:
        file_opener = lambda: open(filepath, 'r', encoding='utf-8')
    
    with file_opener() as file:
        # First, try to load as regular JSON
        file_content = file.read()
        
        try:
            # Try parsing as single JSON object or array
            data = json.loads(file_content)
            if isinstance(data, dict):
                return [data]
            elif isinstance(data, list):
                return data
        except json.JSONDecodeError:
            # If that fails, try parsing as JSONL (one JSON object per line)
            print("Regular JSON parsing failed, trying JSONL format...")
            lines = file_content.strip().split('\n')
            
            for line_num, line in enumerate(lines, 1):
                line = line.strip()
                if line:  # Skip empty lines
                    try:
                        json_obj = json.loads(line)
                        data_list.append(json_obj)
                    except json.JSONDecodeError as e:
                        print(f"Warning: Could not parse line {line_num}: {e}")
                        print(f"Problematic line: {line[:100]}...")
                        continue
    
    if not data_list:
        raise ValueError("No valid JSON data found in file")
    
    print(f"Successfully loaded {len(data_list)} records")
    return data_list

def extract_review_features(review_data: Dict) -> Dict[str, Any]:
    """Extract features from review data only."""
    features = {}
    
    # Text - handle None/null values
    text_raw = review_data.get('text', '')
    features['text'] = text_raw if text_raw is not None else ''
    
    # Rating (int 1-5)
    features['rating'] = review_data.get('rating', 0)
    
    # UserID 
    features['user_id'] = review_data.get('user_id', '')
    
    # Picture link provided (1/0)
    pics = review_data.get('pics')
    features['picture_provided'] = 1 if pics and pics != 'null' and pics is not None else 0
    
    # Review length (normalize to every 10 words) - handle None text
    text = features['text']
    if text and isinstance(text, str):
        word_count = len(text.split())
    else:
        word_count = 0
    features['review_length_normalized'] = round(word_count / 10, 2)
    
    # Contains URI? (1/0) - handle None text
    if text and isinstance(text, str):
        uri_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        features['contains_uri'] = 1 if re.search(uri_pattern, text) else 0
    else:
        features['contains_uri'] = 0
    
    # Additional useful fields from review data
    features['author_name'] = review_data.get('name', '')
    features['review_timestamp'] = review_data.get('time', '')
    features['gmap_id'] = review_data.get('gmap_id', '')
    
    return features

def convert_timestamp_to_hour(timestamp: int) -> int:
    """Convert timestamp to hour of day (0-23)."""
    if timestamp:
        dt = datetime.fromtimestamp(timestamp / 1000)  # Convert from milliseconds
        return dt.hour
    return 0

def check_timing_match(review_timestamp: int, business_hours: str) -> int:
    """Check if review timing matches business opening hours."""
    if not business_hours or business_hours == 'null':
        return 0
    
    # Extract hour from timestamp
    review_hour = convert_timestamp_to_hour(review_timestamp)
    
    # Parse business hours (this would need to be customized based on actual format)
    # For now, return 0 as placeholder
    return 0

def process_review_file(review_file: str, output_csv: str):
    """Main function to process review JSON file and create CSV."""
    
    # Load data
    print(f"Loading review data from {review_file}...")
    reviews = load_json_file(review_file)
    
    # Process reviews and extract features
    processed_data = []
    
    for review in reviews:
        # Extract features from review only
        features = extract_review_features(review)
        processed_data.append(features)
    
    # Write to CSV
    if processed_data:
        fieldnames = processed_data[0].keys()
        
        print(f"Writing {len(processed_data)} records to {output_csv}...")
        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(processed_data)
        
        print(f"Successfully created {output_csv}")
        print(f"Features included: {list(fieldnames)}")
    else:
        print("No data to write to CSV")

# Function to handle single JSON object (for testing with your example data)
def process_single_review(review_json_str: str) -> Dict[str, Any]:
    """Process single review JSON object directly."""
    review_data = json.loads(review_json_str)
    return extract_review_features(review_data)

# Example usage
if __name__ == "__main__":
    # Test which file works first
    print("Testing file accessibility...")
    working_file = test_file_access()
    
    if working_file:
        print(f"\nUsing working file: {working_file}")
        review_json_file = working_file
    else:
        print("\nNo files accessible, trying manual copy...")
        # Try copying file to current directory
        import shutil
        try:
            shutil.copy("Data/Alaska/review-Alaska.json", "review-copy.json")
            review_json_file = "review-copy.json"
            print("✓ File copied successfully")
        except Exception as e:
            print(f"✗ Copy failed: {e}")
            print("Please manually copy the file to the current directory and rename it to 'review-copy.json'")
            exit(1)
    
    output_csv_file = "review_features.csv"
    
    try:
        process_review_file(review_json_file, output_csv_file)
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        print("Please ensure your JSON file is in the correct location.")
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        print("Please check that your JSON file is properly formatted.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example with your provided review data
example_review = '{"user_id": "109129804842686204152", "name": "Nicki Gore", "time": 1566331951619, "rating": 5, "text": "We always stay here when in Valdez for silver salmon fishing. The elderly couple that run it are amazing to talk to, extremely helpful. The campsites are very well maintained.", "pics": null, "resp": null, "gmap_id": "0x56b646ed2220b77f:0xd8975e316de80952"}'

# Uncomment to test with example data:
# result = process_single_review(example_review)
# print("Example output:", result)