import requests
import os 
import dotenv
import json

dotenv.load_dotenv()


IGN_UUID_MAPPING = {
    '51895754843541519014af134ab184a0': 'Developer_Joshua',
    '5a64fd9f390b4f328e65072724d125c2': 'Creative_Josiah',
    '8163575164934e90b096b8fd3396f131': 'Hyperoin',
    '71a92d38b6c1443cb950cfc4cf96ca0a': 'SkysBane',
    '20e77726be984f7cb7dcbeb8ff2e6aea': 'srekul',
}

UUID = [
    '51895754843541519014af134ab184a0',
    '5a64fd9f390b4f328e65072724d125c2',
    '8163575164934e90b096b8fd3396f131',
    '71a92d38b6c1443cb950cfc4cf96ca0a',
    '20e77726be984f7cb7dcbeb8ff2e6aea',
]

# UUID = []

# for i in IGN:
#     mojanginfo = requests.get(
#         url = f"https://api.mojang.com/users/profiles/minecraft/{i}"
#     ).json()
#     UUID.append(mojanginfo["id"])

# for ii in UUID:
#     print(f"'{ii}',")

for person in UUID:
    data = requests.get(
        url = "https://api.hypixel.net/player",
        params = {
            "key": os.getenv('HYPIXEL'),
            "uuid": person
        }
    ).json()

    file_name = f"./V4/data/{IGN_UUID_MAPPING[person]}_bedwars_data.json"

    with open(file_name, 'w') as json_file:
        # Write the data to the JSON file
        json.dump(data, json_file, indent=4)

    print(f"Data for {IGN_UUID_MAPPING[person]} has been written to {file_name}")
