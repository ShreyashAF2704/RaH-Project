import json

with open('acura_.json_rl_to_rsx.json') as f:
   data1 = json.load(f)

with open('acura_cl.json') as f:
   data2 = json.load(f)

with open('acura_csx_el_ilx_integra.json') as f:
   data3 = json.load(f)

with open('acura_legend-mdx-to-rdx.json') as f:
   data4 = json.load(f)

with open('acura_tl_to_zlx.json') as f:
   data5 = json.load(f)

print(len(data1))
print(len(data2))
print(len(data3))
print(len(data4))
print(len(data5))

data = data1+data2+data3+data4+data5
print(len(data))

with open("Acura_final.json", "w") as final:
    json.dump(data, final)



