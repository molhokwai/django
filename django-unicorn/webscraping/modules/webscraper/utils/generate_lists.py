#!/usr/bin/env python3
# -*- coding: utf8 -*-
import random, json


# ---------
# FULL NAMES
# ---------
if False:
    first_names = ["Liam", "Noah", "Oliver", "James", "Elijah", "William", "Matthew", "Ethan", "Alexander", "Henry"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
    print(first_names)
    print(last_names)

    full_names = []
    for f in first_names:
        for l in last_names:
            full_names.append(f"{f} {l}")

    random.shuffle(full_names)
    print(full_names)

    with open("full-names.json", "w") as f:
        f.write(json.dumps(full_names))

if True:
    l = ["Oliver Jones", "William Smith", "Elijah Jones", "Ethan Miller", "Henry Garcia", "Liam Miller", "Henry Jones", "Liam Davis", "Ethan Davis", "Alexander Smith", "Oliver Martinez", "James Johnson", "William Brown", "Alexander Brown", "Noah Martinez", "Matthew Garcia", "Liam Smith", "Henry Smith", "Matthew Davis", "Alexander Williams", "Alexander Rodriguez", "Oliver Davis", "Elijah Brown", "Ethan Rodriguez", "James Brown", "Oliver Johnson", "James Rodriguez", "William Jones", "William Garcia", "Noah Davis", "James Miller", "James Davis", "Elijah Davis", "James Williams", "Matthew Johnson", "Elijah Garcia", "Liam Martinez", "Noah Jones", "Liam Jones", "Matthew Jones", "Henry Brown", "Oliver Miller", "Alexander Martinez", "Elijah Smith", "Matthew Williams", "Henry Williams", "Oliver Smith", "Noah Johnson", "Alexander Jones", "Matthew Smith", "Elijah Williams", "Matthew Brown", "Matthew Miller", "Alexander Garcia", "Ethan Williams", "Henry Johnson", "James Jones", "Henry Davis", "Oliver Williams", "Liam Rodriguez", "Noah Garcia", "William Miller", "William Davis", "William Martinez", "Alexander Davis", "William Rodriguez", "Noah Miller", "Alexander Miller", "Matthew Rodriguez", "Elijah Miller", "Oliver Brown", "Alexander Johnson", "Noah Williams", "Elijah Rodriguez", "William Williams", "Ethan Martinez", "Liam Garcia", "Liam Brown", "Oliver Rodriguez", "James Smith", "Henry Miller", "Oliver Garcia", "Ethan Garcia", "Elijah Johnson", "Noah Rodriguez", "James Martinez", "Ethan Brown", "Henry Rodriguez", "Liam Johnson", "Ethan Smith", "Ethan Jones", "Matthew Martinez", "Ethan Johnson", "Noah Brown", "Henry Martinez", "Liam Williams", "William Johnson", "Noah Smith", "James Garcia", "Elijah Martinez"]
    print("\n".join(l))
