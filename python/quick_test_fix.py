import requests
import time

time.sleep(2)

corpus = ['the cat sat', 'the dog sat', 'the bird flew']
params = {
    'embedding_dim': 15,
    'window_size': 1,
    'negative_samples': 2,
    'epochs': 2,
    'capture_interval': 1,
    'learning_rate': 0.025,
    'method': 'pca'
}

try:
    r = requests.post('http://localhost:5000/demo/sgns-training-dynamics', 
                     json={'corpus': corpus, 'params': params, 'viz_type': 'animation'},
                     timeout=15)
    print(f'Status: {r.status_code}')
    if r.status_code == 200:
        print('✅ SUCCESS! Visualization generated')
        data = r.json()
        print(f'  Vocab size: {data["metadata"]["vocab_size"]}')
        print(f'  Epochs: {data["metadata"]["epochs"]}')
        print(f'  Method: {data["metadata"]["method"]}')
    else:
        print(f'Error: {r.text[:300]}')
except Exception as e:
    print(f'Error: {e}')
