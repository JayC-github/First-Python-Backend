import json

data = {
    "houses": [
        {
            "streetNumber": 5.5,
            "streetName": "abc",       
            "suburb": "phillip"
        },
        {
            "streetNumber": 6.18,
            "streetNmae": "edg",
            "suburb": "Marsfield"
        }
    ]
}

# after json
print(json.dumps(data))
