import requests
import time


def test_cache_performance():
    url = "http://localhost:8000/api/users/"
    
    print("Testing cache performance...")
    
    # First call (cache miss)
    start = time.time()
    try:
        response1 = requests.get(url)
        time1 = time.time() - start
        print(f"First call (cache miss): {time1:.4f}s - Status: {response1.status_code}")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to server. Make sure Django is running on localhost:8000")
        return
    
    # Second call (cache hit)
    start = time.time()
    response2 = requests.get(url)
    time2 = time.time() - start
    print(f"Second call (cache hit): {time2:.4f}s - Status: {response2.status_code}")
    
    if time1 > 0 and time2 > 0:
        speedup = time1 / time2
        print(f"Cache speedup: {speedup:.2f}x faster")
    
    # Test cache stats
    stats_url = "http://localhost:8000/api/users/cache-stats/"
    try:
        stats_response = requests.get(stats_url)
        if stats_response.status_code == 200:
            stats = stats_response.json()
            print(f"\nCache Statistics:")
            print(f"Total cached keys: {stats.get('total_keys', 0)}")
            print(f"Cache keys: {stats.get('cache_keys', [])}")
    except Exception as e:
        print(f"Could not fetch cache stats: {e}")


if __name__ == "__main__":
    test_cache_performance()