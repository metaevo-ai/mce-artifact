import json
import random
from pathlib import Path

def shuffle_test_data():
    """Shuffle the test dataset and save it."""
    data_dir = Path(__file__).parent / 'data'
    test_file = data_dir / 'test.jsonl'
    
    # Read all lines
    with open(test_file, 'r', encoding='utf-8') as f:
        lines = [json.loads(line) for line in f]
    
    print(f"📊 Original test data: {len(lines)} samples")
    
    # Shuffle
    random.shuffle(lines)
    
    # Write back
    with open(test_file, 'w', encoding='utf-8') as f:
        for item in lines:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    print(f"✅ Shuffled test data saved to {test_file}")
    
    # Show first few IDs to verify shuffle
    print(f"\n📋 First 5 sample IDs after shuffle:")
    for i, item in enumerate(lines[:5]):
        print(f"  {i+1}. ID: {item.get('id', 'N/A')}")

if __name__ == "__main__":
    shuffle_test_data()
