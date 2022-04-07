class CharID:
    def __init__(self, name):
        self.name = name
        self.paimonmoe_link = f"https://paimon.moe/characters/{name.lower().replace(' ', '_')}" 
        self.emote = get_useremote(name)
def get_useremote(name):
    with open ("emotes_list.txt", "r") as f:
        data = f.readlines()
        for i in data:
            if name.lower().replace(" ", "_") in i:
                return(i)
p1 = CharID("Arataki Itto")

print(f"{p1.name}\n{p1.paimonmoe_link}\n{p1.emote}")
# Read data from txt file
