
import json
import zlib
import time
import random

def q_int8(val):
    return int((val + 1.0) * 127.5)

# Mock Concept Data
data = {
    'id': 'concept_test',
    'will': {'x': 0.1, 'y': -0.5, 'z': 0.8},
    'emotions': {'joy': 0.5, 'sadness': 0.1},
    'values': {'truth': 0.9},
    'sub_concepts': ['a', 'b', 'c'],
    'language_tokens': [],
    'mirror_phenomena_count': 5,
    'mirror_intensity': 0.2,
    'created_at': time.time(),
    'last_activated': time.time(),
    'activation_count': 10,
    'qubit': 0.5
}

# 1. Current Method (Dict + Quantization + Zlib)
def current_method(d):
    q_data = {
        'id': d['id'],
        'will': {'x': q_int8(d['will']['x']), 'y': q_int8(d['will']['y']), 'z': q_int8(d['will']['z'])},
        'emotions': {k: q_int8(v) for k,v in d['emotions'].items()},
        'values': {k: q_int8(v) for k,v in d['values'].items()},
        'sub_concepts': d['sub_concepts'],
        'language_tokens': d['language_tokens'],
        'mirror_phenomena_count': d['mirror_phenomena_count'],
        'mirror_intensity': q_int8(d['mirror_intensity']),
        'created_at': d['created_at'],
        'last_activated': d['last_activated'],
        'activation_count': d['activation_count'],
        'qubit': q_int8(d['qubit'])
    }
    return zlib.compress(json.dumps(q_data, ensure_ascii=False).encode('utf-8'))

# 2. Compact List Method (List + Quantization + Zlib)
def compact_method(d):
    # [id, [wx,wy,wz], emotions, values, subs, tokens, m_count, m_int, cat, lat, ac, q]
    q_data = [
        d['id'],
        [q_int8(d['will']['x']), q_int8(d['will']['y']), q_int8(d['will']['z'])],
        {k: q_int8(v) for k,v in d['emotions'].items()},
        {k: q_int8(v) for k,v in d['values'].items()},
        d['sub_concepts'],
        d['language_tokens'],
        d['mirror_phenomena_count'],
        q_int8(d['mirror_intensity']),
        int(d['created_at']), # Int timestamp
        int(d['last_activated']),
        d['activation_count'],
        q_int8(d['qubit'])
    ]
    return zlib.compress(json.dumps(q_data, ensure_ascii=False).encode('utf-8'))

c1 = current_method(data)
c2 = compact_method(data)

print(f"Current Size: {len(c1)} bytes")
print(f"Compact Size: {len(c2)} bytes")
print(f"Reduction: {100 * (1 - len(c2)/len(c1)):.1f}%")
