import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True, db=1)

print(r.get('1324271506'))
print(r.get('216935'))