'''
# MythWeaver: Fantasy Character Forge
Healer - Cleric Clash Problem
Druid - Ranger Clash Problem
'''


import streamlit as st
import random
import os
import io
import zipfile
from PIL import Image

char_zip = zipfile.ZipFile("assets/character_images.zip", "r")
equip_zip = zipfile.ZipFile("assets/equipment.zip", "r")

def get_character_image_from_zip(char_class, race):
    file_base = f"{char_class.lower().replace(' ', '_')}_{race.lower().replace(' ', '_')}"
    for ext in ["webp", "png", "jpg", "jpeg"]:
        file_name = f"{file_base}.{ext}"
        if file_name in char_zip.namelist():
            img_data = char_zip.read(file_name)
            return Image.open(io.BytesIO(img_data))
    return Image.open("assets/character_images/default.webp")


# ---------------------------- CONFIGURATION ----------------------------
classes = {
    "Knight": {"STR": 90, "DEF": 70, "INT": 20, "AGI": 40},
    "Tank": {"STR": 70, "DEF": 90, "INT": 30, "AGI": 20},
    "Mage": {"STR": 20, "DEF": 20, "INT": 90, "AGI": 50},
    "Ranger": {"STR": 50, "DEF": 40, "INT": 60, "AGI": 90},
    "Assassin": {"STR": 60, "DEF": 30, "INT": 40, "AGI": 100},
    "Warlock": {"STR": 30, "DEF": 40, "INT": 100, "AGI": 40},
    "Healer": {"STR": 20, "DEF": 60, "INT": 90, "AGI": 50},
    "Bard": {"STR": 40, "DEF": 40, "INT": 60, "AGI": 60},
    "Druid": {"STR": 50, "DEF": 50, "INT": 90, "AGI": 50},
    "Shadow Knight": {"STR": 80, "DEF": 80, "INT": 75, "AGI": 50},
    "Cleric": {"STR": 30, "DEF": 60, "INT": 80, "AGI": 30}, #healer that can also fight
}

races = ["Elf", "Human", "Goblin", "Dwarf", "Fae", "Orc", "Dragonborn", "Tiefling", "Halfling", "Gnome", "Fairy", "Merfolk"]

# Equipment images must match filenames in assets/equipments

equipment_by_class = {
    "Knight": ["steel_armor", "tower_sheild", "longsword"],
    "Tank": ["reinforced_plate", "massive_shield", "warhammer"],
    "Mage": ["arcane_robe", "mana_staff", "arcane_ring"],
    "Ranger": ["leather_armor", "composite_bow", "tracking_goggles"],
    "Assassin": ["shadow_cloak", "dual_daggers", "smoke_bombs"],
    "Warlock": ["dark_robes", "cursed_staff", "demon_talisman"],
    "Healer": ["healing_staff", "holy_symbol", "blessed_bandages"],
    "Bard": ["enchanted_lute", "feathered_hat", "bardic_scroll"],
    "Druid": ["nature_staff", "spirit_cloak", "herbal_pouch"],
    "Shadow Knight": ["blacksteel_armor", "cursed_blade", "dark_shield"],
    "Cleric": ["lightbound_mace", "holy_book", "divine_amulet"],
}

# ---------------------------- FUNCTIONS ----------------------------

def generate_name():
    syllables = ["ar", "ven", "zor", "th", "el", "dra", "mor", "lyn", "ka"]
    return "".join(random.choices(syllables, k=2)).capitalize()

def generate_lore(name, char_class, race):
    templates = [
        f"{name}, a {race} born under a blood moon, destined to rise as a {char_class}.",
        f"Whispers of {name}, the {race}, speak of a forgotten prophecy tied to their {char_class}'s power.",
        f"In the shattered ruins of Eldra, {name} the {race} found their calling as a {char_class}.",
        f"Feared and revered, {name} of the {race} carved their legend as a {char_class} through blood and fire.",
        f"{name} was abandoned in the forest of whispers, raised by shadows to become a {race} {char_class}.",
        f"Trained in secret monasteries, {name} emerged as a {race} {char_class} when the realm needed them most.",
        f"As the stars aligned, {name} stepped from the ancient temple, chosen by fate to be a {race} {char_class}.",
        f"Born of chaos and forged by will, {name} the {race} defied prophecy to become a {char_class}.",
        f"In taverns across the realm, the tale of {name}, the {race} {char_class}, inspires warriors and wanderers alike.",
        f"When the veil between worlds thinned, {name} crossed over, becoming a {race} {char_class} of mythic renown.",
        f"Once a humble outcast, {name} the {race} now walks as a {char_class}, bearer of a forgotten oath.",
        f"{name}, bearer of the soulmark, awakened their destiny as a {race} {char_class} during the eclipse."
    ]
    return random.choice(templates)

def get_character_image_from_zip(char_class, race):
    file_base = f"{char_class.lower().replace(' ', '_')}_{race.lower().replace(' ', '_')}"
    for ext in ["webp", "png", "jpg", "jpeg"]:
        file_name = f"{file_base}.{ext}"
        if file_name in char_zip.namelist():
            img_data = char_zip.read(file_name)
            return Image.open(io.BytesIO(img_data))
    return Image.open("assets/character_images/default.webp")

def get_equipment_image_from_zip(item_name):
    base_name = item_name.rsplit(".", 1)[0]
    for ext in ["webp", "png", "jpg", "jpeg"]:
        file_name = f"{base_name}.{ext}"
        if file_name in equip_zip.namelist():
            img_data = equip_zip.read(file_name)
            return Image.open(io.BytesIO(img_data))
    return Image.open("assets/equipment/default.webp")

def quiz_to_class(traits, tags):
    
    best_match = None
    best_score = float('-inf')

    for cls, base in classes.items():
        score = 0
        for stat in traits:
            diff = abs(traits[stat] - base[stat])
            score -= diff * 0.8

        # Tag influences
        if cls == "Druid" and "nature" in tags: score += 90
        if cls == "Cleric" and "holy" in tags: score += 45
        if cls == "Shadow Knight" and "dark" in tags: score += 85
        if cls == "Healer" and "support" in tags: score += 30
        if cls == "Bard" and "loyal" in tags: score += 30
        if cls == "Assassin" and "stealth" in tags: score += 30
        if cls == "Knight" and "leadership" in tags: score += 30

        if cls == "Warlock" and "dark" in tags: score += 25
        if cls == "Ranger" and "nature" in tags: score += 50
        if cls == "Mage" and "arcane" in tags: score += 10
        if cls == "Tank" and "loyal" in tags: score += 10
        if cls == "Healer" and "holy" in tags: score += 30

        if score > best_score:
            best_score = score
            best_match = cls

    print(f"Class: {cls}, Score: {score}, Traits: {traits}, Tags: {tags}")
    return best_match or "Knight"  # Knight matlab fallback

# ---------------------------- STREAMLIT APP ----------------------------
st.set_page_config(page_title="MythWeaver", layout="centered")
st.title("🧝 MythWeaver: Fantasy Character Forge")
st.markdown("Craft your destiny through soulbound choices.")

st.sidebar.title("🧭 Settings")
selected_race = st.sidebar.selectbox("Choose your race", races)

st.markdown("## 💫 The Soulforge Quiz")
traits = {"STR": 0, "INT": 0, "AGI": 0, "DEF": 0}
personality_tags = []

st.set_page_config(page_title="MythWeaver", layout="centered")

# 7 Quiz Questions
questions = [
    ("Your combat style?", ["Brute force", "Strategic spells", "Fast and agile", "Shield wall"]),
    ("You prefer to...", ["Lead from the front", "Think before acting", "Strike from shadows", "Support allies"]),
    ("Pick a relic:", ["Flaming Greatsword", "Ancient Spellbook", "Shadow Dagger", "Blessed Shield"]),
    ("What drives you?", ["Power", "Wisdom", "Speed", "Loyalty"]),
    ("In a team, you are the...", ["Frontliner", "Strategist", "Scout", "Medic"]),
    ("Choose a domain:", ["Battlefield", "Library", "Shadows", "Sacred Temple"]),
    ("Your soul aligns with:", ["The Wild", "The Arcane", "The Light", "The Void"])
]

for i, (q, options) in enumerate(questions):
    response = st.radio(q, options, key=f"q{i}")
    if response in ["Brute force", "Lead from the front", "Flaming Greatsword", "Power", "Frontliner", "Battlefield", "The Void"]:
        traits["STR"] += 10 if i != 0 else 20
        if response == "Lead from the front": personality_tags.append("leadership")
        if response == "The Void": personality_tags.append("dark")
    elif response in ["Strategic spells", "Think before acting", "Ancient Spellbook", "Wisdom", "Strategist", "Library", "The Arcane"]:
        traits["INT"] += 10 if i != 0 else 20
    elif response in ["Fast and agile", "Strike from shadows", "Shadow Dagger", "Speed", "Scout", "Shadows", "The Wild"]:
        traits["AGI"] += 10 if i != 0 else 20
        if response == "Strike from shadows": personality_tags.append("stealth")
        if response == "The Wild": personality_tags.append("nature")
    elif response in ["Shield wall", "Support allies", "Blessed Shield", "Loyalty", "Medic", "Sacred Temple", "The Light"]:
        traits["DEF"] += 10 if i != 0 else 20
        if response in ["Support allies", "Medic"]: personality_tags.append("support")
        if response == "Loyalty": personality_tags.append("loyal")
        if response == "The Light": personality_tags.append("holy")

# Final Button
if st.button("⚔️ Forge My Character"):
    char_class = quiz_to_class(traits, personality_tags)
    if char_class == "Adventurer":
        st.warning("⚠️ No strong class match found. Defaulting to Adventurer.")
    name = generate_name()
    base_stats = classes[char_class]
    final_stats = {stat: base_stats[stat] + traits.get(stat, 0) for stat in base_stats}
    lore = generate_lore(name, char_class, selected_race)

    st.markdown(f"### 🎭 Name: **{name}**")
    st.markdown(f"**Race:** {selected_race} | **Class:** {char_class}")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🧬 Stats")
        for stat, val in final_stats.items():
            st.markdown(f"**{stat}:** {val}")

    with col2:
        st.markdown("#### 🛡️ Equipment")
        items = equipment_by_class.get(char_class, ["tunic.png", "rusty_sword.png"])
        for item_file in items:
            readable_name = item_file.replace("_", " ").replace(".png", "").title()
            st.markdown(f"- **{readable_name}**")
            try:
                path = get_equipment_image_from_zip(item_file)
                st.image(get_equipment_image_from_zip(item_file), use_container_width=True)
            except:
                st.warning(f"[Missing image: {item_file}]")


    st.markdown("---")
    st.markdown("#### 📖 Origin Lore")
    st.info(lore)

    try:
        char_img_path = get_character_image_from_zip(char_class, selected_race)
        st.image(get_character_image_from_zip(char_class, selected_race), use_container_width=True)
    except:
        st.warning("[No character art available]")

    # Download
    sheet = f"""
    Name: {name}
    Race: {selected_race}
    Class: {char_class}
    Stats: {final_stats}
    Equipment: {', '.join(items)}
    Lore: {lore}
    """
    st.download_button("📜 Download Character Sheet", sheet, file_name="MyCharacter.txt")
