"""
GALAXY CODER — Universe Data
All planets, missions, concepts, battles, and certificates
"""

# ══════════════════════════════════════════════════════════════
# GALAXY MAP — Planets unlock in sequence
# ══════════════════════════════════════════════════════════════

GALAXY = {
    "mercury": {
        "id": "mercury",
        "name": "Mercury",
        "subtitle": "Planet of First Contact",
        "icon": "☿",
        "color": "#A8A8A8",
        "glow": "#C8C8C8",
        "xp_required": 0,
        "description": "Your first planet. Learn the language of the universe — Python basics.",
        "atmosphere": "rocky",
        "missions": [
            {
                "id": "m_001",
                "title": "Signal Transmission",
                "story": "🛸 ARIA detected: *'Alien signal received! Decode it by sending your first transmission to base camp.'*",
                "concept": "Print & Output",
                "xp": 50,
                "energy": 1,
                "difficulty": "⭐",
                "steps": [
                    {
                        "type": "story",
                        "content": "You've just landed on Mercury. ARIA boots up...\n\n**ARIA:** *'Commander! To communicate with Earth, we use Python's `print()` function. It sends messages across space!'*\n\n```python\nprint(\"Hello, Earth!\")\n```\n\nThis outputs: `Hello, Earth!`\n\nThe `print()` function displays anything inside the quotes on screen."
                    },
                    {
                        "type": "visual",
                        "content": "print_visual",
                        "caption": "print() sends your message to the output console"
                    },
                    {
                        "type": "quiz",
                        "question": "What does `print('Galaxy')` display?",
                        "options": ["print Galaxy", "Galaxy", "'Galaxy'", "Error"],
                        "answer": 1,
                        "explanation": "print() displays the text WITHOUT quotes. Output: Galaxy"
                    },
                    {
                        "type": "code",
                        "instruction": "🎯 Send 3 transmissions to Earth — print your name, your planet, and 'Transmission complete!'",
                        "starter": '# Mission: Send 3 transmissions\n# 1. Print your name\n\n# 2. Print "Mercury"\n\n# 3. Print "Transmission complete!"\n',
                        "solution": 'print("Commander Alex")\nprint("Mercury")\nprint("Transmission complete!")',
                        "check": ["Transmission complete"],
                        "hints": ["Use print() three times", "Each print() goes on a new line", 'print("your text here")']
                    }
                ],
                "reward": {"xp": 50, "badge": None, "unlock": "m_002"}
            },
            {
                "id": "m_002",
                "title": "Data Crystals",
                "story": "💎 ARIA: *'Commander! We found data crystals. Each stores different types of information. We need variables to hold them!'*",
                "concept": "Variables & Data Types",
                "xp": 75,
                "energy": 1,
                "difficulty": "⭐",
                "steps": [
                    {
                        "type": "story",
                        "content": "ARIA scans the crystals...\n\n**ARIA:** *'Variables are like labeled containers in your spaceship. Each holds a different type of data!'*\n\n```python\ncommander = \"Alex\"      # String — text\nfuel = 100              # Integer — whole number  \nspeed = 9.8             # Float — decimal\nshields_up = True       # Boolean — True/False\n```\n\n**4 Crystal Types:**\n| Type | Example | Stores |\n|------|---------|--------|\n| `str` | `\"Alex\"` | Text |\n| `int` | `42` | Whole numbers |\n| `float` | `3.14` | Decimals |\n| `bool` | `True` | Yes/No |"
                    },
                    {
                        "type": "visual",
                        "content": "variables_visual",
                        "caption": "Variables are labeled boxes storing different crystal types"
                    },
                    {
                        "type": "quiz",
                        "question": "What type is: `temperature = 36.6`?",
                        "options": ["string", "integer", "float", "boolean"],
                        "answer": 2,
                        "explanation": "36.6 has a decimal point → it's a float!"
                    },
                    {
                        "type": "quiz",
                        "question": "Which stores True or False?",
                        "options": ["str", "int", "float", "bool"],
                        "answer": 3,
                        "explanation": "Boolean (bool) stores only True or False values"
                    },
                    {
                        "type": "code",
                        "instruction": "🎯 Create a spaceship profile: name (string), speed (int), fuel_level (float), shields_active (bool). Print them all!",
                        "starter": '# Spaceship Profile\nname = ""          # your ship name\nspeed =            # speed in km/s\nfuel_level =       # fuel percentage\nshields_active =   # True or False\n\n# Print all variables\n',
                        "solution": 'name = "Stellar Eagle"\nspeed = 1200\nfuel_level = 87.5\nshields_active = True\nprint(name)\nprint(speed)\nprint(fuel_level)\nprint(shields_active)',
                        "check": [],
                        "hints": ["Strings need quotes", "Numbers don't need quotes", "Boolean: True or False (capital T/F)"]
                    }
                ],
                "reward": {"xp": 75, "badge": None, "unlock": "m_003"}
            },
            {
                "id": "m_003",
                "title": "The Navigation System",
                "story": "🧭 ARIA: *'Our navigation needs conditions — if fuel is low, change course. If shields are down, retreat!'*",
                "concept": "If/Else Conditions",
                "xp": 100,
                "energy": 2,
                "difficulty": "⭐⭐",
                "steps": [
                    {
                        "type": "story",
                        "content": "**ARIA:** *'Every smart system needs to make decisions. In Python, we use `if/elif/else`!'*\n\n```python\nfuel = 30\n\nif fuel > 75:\n    print(\"Fuel: Excellent\")\nelif fuel > 25:\n    print(\"Fuel: Low — find a station\")\nelse:\n    print(\"CRITICAL: Emergency landing!\")\n```\n\n**Comparison Operators:**\n```\n>   greater than       <   less than\n>=  greater or equal   <=  less or equal  \n==  exactly equal      !=  not equal\n```"
                    },
                    {
                        "type": "visual",
                        "content": "condition_visual",
                        "caption": "if/elif/else — the decision tree of your spaceship"
                    },
                    {
                        "type": "quiz",
                        "question": "fuel = 50. What does this print?\n```\nif fuel > 75: print('High')\nelif fuel > 25: print('Medium')\nelse: print('Low')\n```",
                        "options": ["High", "Medium", "Low", "Nothing"],
                        "answer": 1,
                        "explanation": "50 > 75? No. 50 > 25? Yes! → prints 'Medium'"
                    },
                    {
                        "type": "code",
                        "instruction": "🎯 Build a shield system: if shields > 80 print 'Shields: Strong', elif > 40 print 'Shields: Moderate', elif > 0 print 'Shields: Critical', else print 'SHIELDS DOWN!'",
                        "starter": 'shields = int(input("Enter shield level (0-100): "))\n\n# Build your shield checker\n',
                        "solution": 'shields = int(input("Enter shield level (0-100): "))\nif shields > 80:\n    print("Shields: Strong")\nelif shields > 40:\n    print("Shields: Moderate")\nelif shields > 0:\n    print("Shields: Critical")\nelse:\n    print("SHIELDS DOWN!")',
                        "check": [],
                        "hints": ["Start from highest value", "Use elif for middle cases", "else catches everything remaining"]
                    }
                ],
                "reward": {"xp": 100, "badge": "☿ Mercury Explorer", "unlock": "m_004"}
            },
            {
                "id": "m_004",
                "title": "Asteroid Belt Loop",
                "story": "☄️ ARIA: *'Commander! 50 asteroids ahead. We can't dodge them one by one — we need loops!'*",
                "concept": "For & While Loops",
                "xp": 125,
                "energy": 2,
                "difficulty": "⭐⭐",
                "steps": [
                    {
                        "type": "story",
                        "content": "**ARIA:** *'Loops repeat actions automatically. Perfect for asteroid dodging!'*\n\n```python\n# For loop — repeat a set number of times\nfor i in range(5):\n    print(f\"Dodging asteroid {i+1}\")\n\n# While loop — repeat while condition is true\nfuel = 100\nwhile fuel > 0:\n    print(f\"Flying... fuel: {fuel}\")\n    fuel -= 25\n    \nprint(\"Out of fuel!\")\n```\n\n**Loop Control:**\n```python\nfor i in range(10):\n    if i == 3: continue  # skip this one\n    if i == 7: break     # stop the loop\n    print(i)\n```"
                    },
                    {
                        "type": "visual",
                        "content": "loop_visual",
                        "caption": "Loops — your autopilot for repeating tasks"
                    },
                    {
                        "type": "quiz",
                        "question": "How many times does `for i in range(3)` loop?",
                        "options": ["2 times", "3 times", "4 times", "1 time"],
                        "answer": 1,
                        "explanation": "range(3) gives 0, 1, 2 — that's 3 iterations!"
                    },
                    {
                        "type": "code",
                        "instruction": "🎯 Print a countdown for rocket launch: from 10 down to 1, then print 'LAUNCH! 🚀'",
                        "starter": '# Rocket countdown\n# Hint: range(start, stop, step) — for countdown use range(10, 0, -1)\n',
                        "solution": 'for i in range(10, 0, -1):\n    print(f"T-minus {i}...")\nprint("LAUNCH! 🚀")',
                        "check": ["LAUNCH"],
                        "hints": ["range(10, 0, -1) counts 10,9,8...1", "Use f-string: f'T-minus {i}'", "Print LAUNCH after the loop"]
                    }
                ],
                "reward": {"xp": 125, "badge": None, "unlock": "m_005"}
            },
            {
                "id": "m_005",
                "title": "Crew Manifest",
                "story": "👨‍🚀 ARIA: *'We need to organize our crew data. Python has special containers — lists, dicts, tuples!'*",
                "concept": "Lists, Dicts & Tuples",
                "xp": 150,
                "energy": 2,
                "difficulty": "⭐⭐",
                "steps": [
                    {
                        "type": "story",
                        "content": "**ARIA:** *'Data collections are the backbone of every system!'*\n\n```python\n# List — ordered, changeable\ncrew = [\"Alex\", \"Zara\", \"Omar\"]\ncrew.append(\"Nova\")     # add\ncrew.remove(\"Omar\")     # remove\nprint(crew[0])           # access: Alex\n\n# Dictionary — key:value pairs  \nship = {\n    \"name\": \"Stellar Eagle\",\n    \"speed\": 9800,\n    \"crew\": 4\n}\nprint(ship[\"name\"])     # Stellar Eagle\n\n# Tuple — ordered, UNCHANGEABLE\ncoords = (40.7, -74.0)   # cannot modify!\n```"
                    },
                    {
                        "type": "visual",
                        "content": "collections_visual",
                        "caption": "List = ordered shelf | Dict = labeled drawer | Tuple = sealed capsule"
                    },
                    {
                        "type": "quiz",
                        "question": "Which collection uses key:value pairs?",
                        "options": ["List", "Tuple", "Dictionary", "Set"],
                        "answer": 2,
                        "explanation": "Dictionary uses key:value pairs like {'name': 'Alex'}"
                    },
                    {
                        "type": "code",
                        "instruction": "🎯 Create a crew dictionary with 3 members. Each member has: name, role, skill_level. Print each crew member's name and role.",
                        "starter": '# Crew Manifest\ncrew = [\n    {"name": "Alex", "role": "Commander", "skill": 95},\n    # Add 2 more crew members\n]\n\n# Print each member\'s name and role\n',
                        "solution": 'crew = [\n    {"name": "Alex", "role": "Commander", "skill": 95},\n    {"name": "Zara", "role": "Engineer", "skill": 88},\n    {"name": "Omar", "role": "Pilot", "skill": 92}\n]\nfor member in crew:\n    print(f"{member[\'name\']} — {member[\'role\']}")',
                        "check": ["Commander"],
                        "hints": ["Use a list of dictionaries", "Loop through crew with for", "Access with member['name']"]
                    }
                ],
                "reward": {"xp": 150, "badge": None, "unlock": "m_006"}
            },
            {
                "id": "m_006",
                "title": "Warp Engine Functions",
                "story": "⚡ ARIA: *'Commander, our warp engine needs reusable code modules — functions! Write once, use anywhere in the galaxy!'*",
                "concept": "Functions",
                "xp": 200,
                "energy": 3,
                "difficulty": "⭐⭐⭐",
                "steps": [
                    {
                        "type": "story",
                        "content": "**ARIA:** *'Functions are like pre-programmed ship modules. Define once, activate anytime!'*\n\n```python\ndef calculate_warp_speed(distance, time):\n    \"\"\"Calculate warp speed needed\"\"\"\n    speed = distance / time\n    return speed\n\n# Use the function\nresult = calculate_warp_speed(1000, 5)\nprint(f\"Required warp: {result} ly/hr\")\n\n# Default parameters\ndef launch_rocket(name, fuel=100, crew=1):\n    print(f\"{name} launching with {crew} crew, {fuel}% fuel\")\n\nlaunch_rocket(\"Eagle\")           # uses defaults\nlaunch_rocket(\"Falcon\", 85, 4)   # custom values\n```"
                    },
                    {
                        "type": "visual",
                        "content": "function_visual",
                        "caption": "Functions: Input → Process → Output. Like a machine!"
                    },
                    {
                        "type": "quiz",
                        "question": "What keyword returns a value from a function?",
                        "options": ["send", "output", "return", "give"],
                        "answer": 2,
                        "explanation": "The `return` keyword sends a value back from the function!"
                    },
                    {
                        "type": "code",
                        "instruction": "🎯 Write a function `fuel_status(fuel)` that returns: 'CRITICAL' if fuel<20, 'LOW' if fuel<50, 'GOOD' if fuel<80, else 'FULL'. Test with 4 different values.",
                        "starter": 'def fuel_status(fuel):\n    # Return the status based on fuel level\n    pass\n\n# Test with 4 values\nprint(fuel_status(10))\nprint(fuel_status(35))\nprint(fuel_status(65))\nprint(fuel_status(95))\n',
                        "solution": 'def fuel_status(fuel):\n    if fuel < 20:\n        return "CRITICAL"\n    elif fuel < 50:\n        return "LOW"\n    elif fuel < 80:\n        return "GOOD"\n    else:\n        return "FULL"\n\nprint(fuel_status(10))\nprint(fuel_status(35))\nprint(fuel_status(65))\nprint(fuel_status(95))',
                        "check": ["CRITICAL", "FULL"],
                        "hints": ["Use if/elif/else inside function", "Use 'return' not 'print'", "Test all 4 conditions"]
                    }
                ],
                "reward": {"xp": 200, "badge": "🚀 Mercury Master", "unlock": None}
            }
        ]
    },

    "venus": {
        "id": "venus",
        "name": "Venus",
        "subtitle": "Planet of Architecture",
        "icon": "♀",
        "color": "#FF8C42",
        "glow": "#FFB380",
        "xp_required": 600,
        "description": "Master Object-Oriented Programming. Build complex systems like blueprints.",
        "atmosphere": "volcanic",
        "missions": [
            {
                "id": "v_001",
                "title": "Starship Blueprint",
                "story": "🏗️ ARIA: *'Commander! To build a fleet, we need blueprints. In Python, these are called Classes!'*",
                "concept": "Classes & Objects",
                "xp": 250,
                "energy": 3,
                "difficulty": "⭐⭐⭐",
                "steps": [
                    {
                        "type": "story",
                        "content": "**ARIA:** *'A class is a blueprint. An object is the actual ship built from that blueprint!'*\n\n```python\nclass Spaceship:\n    # Blueprint for ALL spaceships\n    \n    def __init__(self, name, fuel):\n        self.name = name      # instance data\n        self.fuel = fuel\n        self.speed = 0\n    \n    def accelerate(self, amount):\n        self.speed += amount\n        self.fuel -= amount * 0.1\n        return f\"{self.name} speed: {self.speed}\"\n    \n    def status(self):\n        return f\"{self.name} | Speed:{self.speed} | Fuel:{self.fuel:.1f}\"\n    \n    def __str__(self):\n        return f\"🚀 Spaceship: {self.name}\"\n\n# Create ships from blueprint\neagle = Spaceship(\"Eagle\", 100)\nfalcon = Spaceship(\"Falcon\", 85)\n\nprint(eagle.accelerate(50))\nprint(falcon.status())\n```"
                    },
                    {
                        "type": "visual",
                        "content": "class_visual",
                        "caption": "Class = Blueprint | Object = Actual Ship built from blueprint"
                    },
                    {
                        "type": "quiz",
                        "question": "What is `__init__` in a Python class?",
                        "options": ["A loop", "The constructor — runs when object is created", "A return statement", "A variable"],
                        "answer": 1,
                        "explanation": "__init__ is the constructor. It runs automatically when you create a new object!"
                    },
                    {
                        "type": "code",
                        "instruction": "🎯 Create a `Planet` class with: name, size, has_water (bool). Methods: describe() returns full description, is_habitable() returns True if has_water. Create 3 planets and print their habitability.",
                        "starter": 'class Planet:\n    def __init__(self, name, size, has_water):\n        # Store the attributes\n        pass\n    \n    def describe(self):\n        # Return a description string\n        pass\n    \n    def is_habitable(self):\n        # Return True if has_water\n        pass\n\n# Create 3 planets and test them\n',
                        "solution": 'class Planet:\n    def __init__(self, name, size, has_water):\n        self.name = name\n        self.size = size\n        self.has_water = has_water\n    def describe(self):\n        return f"{self.name}: size={self.size}, water={self.has_water}"\n    def is_habitable(self):\n        return self.has_water\n\nearth = Planet("Earth", "medium", True)\nmars = Planet("Mars", "small", False)\nkepler = Planet("Kepler-22b", "large", True)\nfor p in [earth, mars, kepler]:\n    status = "✅ Habitable" if p.is_habitable() else "❌ Not habitable"\n    print(f"{p.name}: {status}")',
                        "check": ["Habitable"],
                        "hints": ["self.name = name stores the attribute", "is_habitable should return self.has_water", "Create objects: earth = Planet('Earth', 'medium', True)"]
                    }
                ],
                "reward": {"xp": 250, "badge": "♀ Venus Explorer", "unlock": "v_002"}
            },
            {
                "id": "v_002",
                "title": "Fleet Inheritance",
                "story": "🛸 ARIA: *'Every ship in our fleet shares base features, but each has special powers. This is Inheritance!'*",
                "concept": "Inheritance & Polymorphism",
                "xp": 300,
                "energy": 3,
                "difficulty": "⭐⭐⭐",
                "steps": [
                    {
                        "type": "story",
                        "content": "**ARIA:** *'Child classes inherit everything from parent, then add their own powers!'*\n\n```python\nclass Vehicle:          # Parent class\n    def __init__(self, name, speed):\n        self.name = name\n        self.speed = speed\n    \n    def move(self):\n        return f\"{self.name} moving at {self.speed}\"\n\nclass Spaceship(Vehicle):    # Child — inherits Vehicle\n    def __init__(self, name, speed, warp):\n        super().__init__(name, speed)  # Call parent\n        self.warp = warp\n    \n    def move(self):           # Override parent method\n        return f\"{self.name} warping at {self.warp}x!\"\n\nclass Fighter(Vehicle):      # Another child\n    def fire(self):\n        return f\"{self.name} fires lasers!\"\n\n# Polymorphism — same method, different behavior\nfleet = [Spaceship(\"Eagle\",1000,9), Fighter(\"Viper\",800,0)]\nfor ship in fleet:\n    print(ship.move())   # Each behaves differently!\n```"
                    },
                    {
                        "type": "visual",
                        "content": "inheritance_visual",
                        "caption": "Inheritance tree: parent passes powers to children"
                    },
                    {
                        "type": "quiz",
                        "question": "What does `super().__init__()` do?",
                        "options": ["Creates a new object", "Calls the parent class constructor", "Deletes the object", "Loops through parents"],
                        "answer": 1,
                        "explanation": "super().__init__() calls the parent's __init__ so you don't rewrite the same code!"
                    },
                    {
                        "type": "code",
                        "instruction": "🎯 Create a base class `Weapon` with damage and name. Create 2 subclasses: `LaserGun` (adds range attribute, fire() method) and `MissileLauncher` (adds ammo, launch() method). Show polymorphism.",
                        "starter": 'class Weapon:\n    def __init__(self, name, damage):\n        self.name = name\n        self.damage = damage\n    \n    def attack(self):\n        return f"{self.name} deals {self.damage} damage"\n\nclass LaserGun(Weapon):\n    def __init__(self, name, damage, range_km):\n        # Call parent + add range_km\n        pass\n    def fire(self):\n        pass\n\nclass MissileLauncher(Weapon):\n    def __init__(self, name, damage, ammo):\n        # Call parent + add ammo\n        pass\n    def launch(self):\n        pass\n\n# Test both weapons\n',
                        "solution": 'class Weapon:\n    def __init__(self, name, damage):\n        self.name = name\n        self.damage = damage\n    def attack(self):\n        return f"{self.name} deals {self.damage} damage"\n\nclass LaserGun(Weapon):\n    def __init__(self, name, damage, range_km):\n        super().__init__(name, damage)\n        self.range_km = range_km\n    def fire(self):\n        return f"⚡ {self.name} fires! Range: {self.range_km}km"\n\nclass MissileLauncher(Weapon):\n    def __init__(self, name, damage, ammo):\n        super().__init__(name, damage)\n        self.ammo = ammo\n    def launch(self):\n        self.ammo -= 1\n        return f"🚀 Missile launched! Ammo left: {self.ammo}"\n\nlaser = LaserGun("Photon Blaster", 50, 500)\nmissile = MissileLauncher("Titan Rocket", 200, 5)\nfor w in [laser, missile]:\n    print(w.attack())\nprint(laser.fire())\nprint(missile.launch())',
                        "check": ["damage"],
                        "hints": ["Use super().__init__(name, damage) in each child", "Add self.range_km = range_km after super()", "Loop through weapons list for polymorphism"]
                    }
                ],
                "reward": {"xp": 300, "badge": "🏗️ Venus Master", "unlock": None}
            }
        ]
    },

    "earth": {
        "id": "earth",
        "name": "Earth",
        "subtitle": "Data Science Hub",
        "icon": "🌍",
        "color": "#4ECDC4",
        "glow": "#80E8E0",
        "xp_required": 1200,
        "description": "Analyze real data! NumPy, Pandas, and visualization — the data scientist's toolkit.",
        "atmosphere": "data_streams",
        "missions": [
            {
                "id": "e_001",
                "title": "NumPy Star Charts",
                "story": "📊 ARIA: *'Earth scientists mapped every star! We use NumPy to analyze millions of data points instantly!'*",
                "concept": "NumPy Arrays",
                "xp": 350,
                "energy": 3,
                "difficulty": "⭐⭐⭐",
                "steps": [
                    {
                        "type": "story",
                        "content": "**ARIA:** *'NumPy arrays are 100x faster than Python lists for numbers!'*\n\n```python\nimport numpy as np\n\n# Creating arrays\nstars = np.array([8.2, 7.1, 9.5, 6.8, 8.9])\n\n# Math on ENTIRE array at once!\nstars * 2          # multiply all\nstars + 10         # add to all\nnp.sqrt(stars)     # square root of all\n\n# Statistics\nnp.mean(stars)     # average\nnp.std(stars)      # standard deviation\nnp.min(stars)      # minimum\nnp.max(stars)      # maximum\n\n# Boolean filtering (MAGIC!)\nbright = stars[stars > 8.0]  # only stars > 8.0\nprint(bright)  # [8.2 9.5 8.9]\n```"
                    },
                    {
                        "type": "visual",
                        "content": "numpy_visual",
                        "caption": "NumPy: Operations on entire arrays at once — no loops needed!"
                    },
                    {
                        "type": "quiz",
                        "question": "arr = np.array([1,2,3,4,5]). What is arr[arr > 3]?",
                        "options": ["[1,2,3]", "[4,5]", "[3,4,5]", "Error"],
                        "answer": 1,
                        "explanation": "arr > 3 creates [F,F,F,T,T] → filters to [4,5] only!"
                    },
                    {
                        "type": "code",
                        "instruction": "🎯 Create array of 10 planet temperatures (-200 to 500). Find: mean, min, max, std. Count planets above 0°C (habitable zone).",
                        "starter": 'import numpy as np\nnp.random.seed(42)\n\n# Create 10 random temperatures between -200 and 500\ntemps = np.random.randint(-200, 501, 10)\nprint("Temperatures:", temps)\n\n# Calculate statistics\n# Count habitable planets (temp > 0)\n',
                        "solution": 'import numpy as np\nnp.random.seed(42)\ntemps = np.random.randint(-200, 501, 10)\nprint("Temperatures:", temps)\nprint(f"Mean: {np.mean(temps):.1f}°C")\nprint(f"Min: {np.min(temps)}°C, Max: {np.max(temps)}°C")\nprint(f"Std Dev: {np.std(temps):.1f}")\nhabitable = np.sum(temps > 0)\nprint(f"Habitable planets: {habitable}")',
                        "check": ["Habitable"],
                        "hints": ["Use np.mean(), np.min(), np.max(), np.std()", "temps > 0 gives boolean array", "np.sum(temps > 0) counts True values"]
                    }
                ],
                "reward": {"xp": 350, "badge": "🌍 Earth Explorer", "unlock": "e_002"}
            },
            {
                "id": "e_002",
                "title": "Pandas Mission Control",
                "story": "🐼 ARIA: *'Mission Control has spreadsheet data on 1000 planets. We need Pandas to make sense of it!'*",
                "concept": "Pandas DataFrames",
                "xp": 400,
                "energy": 4,
                "difficulty": "⭐⭐⭐⭐",
                "steps": [
                    {
                        "type": "story",
                        "content": "**ARIA:** *'Pandas DataFrames are like Excel tables — but programmable!'*\n\n```python\nimport pandas as pd\n\nplanets = pd.DataFrame({\n    'name': ['Earth','Mars','Venus','Jupiter'],\n    'size': [12742, 6779, 12104, 139820],\n    'temp': [15, -60, 465, -145],\n    'moons': [1, 2, 0, 95]\n})\n\nplanets.head()           # first 5 rows\nplanets.describe()       # statistics\nplanets['temp']          # one column\nplanets[planets['temp'] > 0]  # filter rows\nplanets.sort_values('size')   # sort\nplanets['habitable'] = planets['temp'].between(-50, 50)  # new column\n\n# Group and aggregate\nplanets.groupby('habitable')['size'].mean()\n```"
                    },
                    {
                        "type": "visual",
                        "content": "pandas_visual",
                        "caption": "DataFrame = programmable spreadsheet with superpowers"
                    },
                    {
                        "type": "quiz",
                        "question": "How do you filter a DataFrame where column 'age' > 18?",
                        "options": ["df.filter(age>18)", "df[df['age'] > 18]", "df.where('age', 18)", "df.select(age=18)"],
                        "answer": 1,
                        "explanation": "df[df['age'] > 18] — the inner part creates a boolean mask!"
                    },
                    {
                        "type": "code",
                        "instruction": "🎯 Create a DataFrame of 5 crew members (name, age, role, missions_completed). Add a 'veteran' column (True if missions > 5). Find the average age of veterans vs non-veterans.",
                        "starter": 'import pandas as pd\n\ncrew = pd.DataFrame({\n    "name": ["Alex", "Zara", "Omar", "Nova", "Kai"],\n    "age": [32, 28, 35, 25, 40],\n    "role": ["Commander", "Engineer", "Pilot", "Scientist", "Doctor"],\n    "missions": [8, 3, 12, 2, 6]\n})\n\n# Add veteran column (True if missions > 5)\n\n# Average age by veteran status\n',
                        "solution": 'import pandas as pd\ncrew = pd.DataFrame({"name": ["Alex","Zara","Omar","Nova","Kai"],"age": [32,28,35,25,40],"role": ["Commander","Engineer","Pilot","Scientist","Doctor"],"missions": [8,3,12,2,6]})\ncrew["veteran"] = crew["missions"] > 5\nprint(crew)\nprint("\\nAverage age by veteran status:")\nprint(crew.groupby("veteran")["age"].mean())',
                        "check": ["veteran"],
                        "hints": ["crew['veteran'] = crew['missions'] > 5", "Use groupby('veteran')['age'].mean()", "Print the result"]
                    }
                ],
                "reward": {"xp": 400, "badge": "📊 Data Scientist", "unlock": None}
            }
        ]
    },

    "mars": {
        "id": "mars",
        "name": "Mars",
        "subtitle": "Machine Learning Colony",
        "icon": "♂",
        "color": "#EF4444",
        "glow": "#FF8080",
        "xp_required": 2000,
        "description": "Train AI models! Scikit-learn, neural networks, and real ML projects.",
        "atmosphere": "algorithmic",
        "missions": [
            {
                "id": "ml_001",
                "title": "Teaching the Colony AI",
                "story": "🤖 ARIA: *'Commander, the Mars colony AI needs training! We use Scikit-learn to teach machines from data!'*",
                "concept": "ML with Scikit-learn",
                "xp": 500,
                "energy": 4,
                "difficulty": "⭐⭐⭐⭐",
                "steps": [
                    {
                        "type": "story",
                        "content": "**ARIA:** *'Machine Learning: show the computer examples, it learns the pattern!'*\n\n```python\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.preprocessing import StandardScaler  \nfrom sklearn.ensemble import RandomForestClassifier\nfrom sklearn.metrics import accuracy_score\n\n# 1. Prepare data\nX = features   # what we know\ny = labels     # what we predict\n\n# 2. Split: 80% train, 20% test\nX_train, X_test, y_train, y_test = train_test_split(\n    X, y, test_size=0.2, random_state=42\n)\n\n# 3. Scale features\nscaler = StandardScaler()\nX_train = scaler.fit_transform(X_train)\nX_test = scaler.transform(X_test)\n\n# 4. Train\nmodel = RandomForestClassifier(n_estimators=100)\nmodel.fit(X_train, y_train)\n\n# 5. Evaluate  \ny_pred = model.predict(X_test)\nprint(f\"Accuracy: {accuracy_score(y_test, y_pred):.2%}\")\n```"
                    },
                    {
                        "type": "visual",
                        "content": "ml_visual",
                        "caption": "ML Pipeline: Data → Split → Scale → Train → Predict → Evaluate"
                    },
                    {
                        "type": "quiz",
                        "question": "Why do we split data into train and test sets?",
                        "options": ["To save memory", "To test on unseen data — like an exam!", "To speed up training", "Python requires it"],
                        "answer": 1,
                        "explanation": "Training on all data = cheating! Test set checks if model learned GENERAL patterns, not just memorized training data."
                    },
                    {
                        "type": "code",
                        "instruction": "🎯 Train a classifier on the Iris dataset. Split 80/20, scale, train KNN(k=5), print accuracy and predict for a new sample [5.1, 3.5, 1.4, 0.2].",
                        "starter": 'from sklearn.datasets import load_iris\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.neighbors import KNeighborsClassifier\nfrom sklearn.metrics import accuracy_score\n\niris = load_iris()\nX, y = iris.data, iris.target\n\n# Split, scale, train, evaluate\n',
                        "solution": 'from sklearn.datasets import load_iris\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.neighbors import KNeighborsClassifier\nfrom sklearn.metrics import accuracy_score\n\niris = load_iris()\nX, y = iris.data, iris.target\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\nscaler = StandardScaler()\nX_train = scaler.fit_transform(X_train)\nX_test = scaler.transform(X_test)\nmodel = KNeighborsClassifier(n_neighbors=5)\nmodel.fit(X_train, y_train)\ny_pred = model.predict(X_test)\nprint(f"Accuracy: {accuracy_score(y_test, y_pred):.2%}")\nnew = scaler.transform([[5.1, 3.5, 1.4, 0.2]])\nprint(f"Prediction: {iris.target_names[model.predict(new)[0]]}")',
                        "check": ["Accuracy"],
                        "hints": ["load_iris() gives you X and y", "train_test_split(X, y, test_size=0.2)", "KNeighborsClassifier(n_neighbors=5)"]
                    }
                ],
                "reward": {"xp": 500, "badge": "🤖 ML Engineer", "unlock": None}
            }
        ]
    },

    "jupiter": {
        "id": "jupiter",
        "name": "Jupiter",
        "subtitle": "AI & LangChain Nexus",
        "icon": "♃",
        "color": "#F59E0B",
        "glow": "#FCD34D",
        "xp_required": 3000,
        "description": "Build real AI applications with LangChain, RAG, and LangGraph agents.",
        "atmosphere": "neural",
        "missions": [
            {
                "id": "ai_001",
                "title": "The AI Nexus",
                "story": "🦜 ARIA: *'Commander! Jupiter is the AI capital of the galaxy. Here we build systems that THINK using LangChain!'*",
                "concept": "LangChain Basics",
                "xp": 700,
                "energy": 5,
                "difficulty": "⭐⭐⭐⭐⭐",
                "steps": [
                    {
                        "type": "story",
                        "content": "**ARIA:** *'LangChain lets you build apps powered by AI models!'*\n\n```python\nfrom langchain_anthropic import ChatAnthropic\nfrom langchain_core.prompts import ChatPromptTemplate\nfrom langchain_core.output_parsers import StrOutputParser\n\n# Initialize model\nllm = ChatAnthropic(model=\"claude-sonnet-4-20250514\")\n\n# Create a prompt template\nprompt = ChatPromptTemplate.from_messages([\n    (\"system\", \"You are a space exploration expert.\"),\n    (\"human\", \"Tell me about {planet} in 2 sentences.\")\n])\n\n# Build chain: prompt → AI → parse output\nchain = prompt | llm | StrOutputParser()\n\n# Run it!\nresult = chain.invoke({\"planet\": \"Jupiter\"})\nprint(result)\n```\n\n**Key concepts:**\n- **Prompt Templates** — structured input to AI\n- **Chains** — connect steps with `|` operator\n- **Output Parsers** — convert AI response to usable format"
                    },
                    {
                        "type": "visual",
                        "content": "langchain_visual",
                        "caption": "LangChain Chain: Prompt → LLM → Parser → Output"
                    },
                    {
                        "type": "quiz",
                        "question": "In LangChain, what does the `|` operator do?",
                        "options": ["OR comparison", "Connects chain steps (pipe)", "Divides numbers", "String separator"],
                        "answer": 1,
                        "explanation": "The | (pipe) operator connects chain components: prompt | llm | parser"
                    },
                    {
                        "type": "code",
                        "instruction": "🎯 Build a LangChain chain that takes a 'topic' and 'audience' and generates a 3-bullet explanation. Run it for topic='black holes', audience='beginners'.",
                        "starter": 'from langchain_anthropic import ChatAnthropic\nfrom langchain_core.prompts import ChatPromptTemplate\nfrom langchain_core.output_parsers import StrOutputParser\n\nllm = ChatAnthropic(model="claude-sonnet-4-20250514")\n\n# Create prompt template with {topic} and {audience}\nprompt = ChatPromptTemplate.from_messages([\n    ("system", "You are an expert science communicator."),\n    ("human", "Explain {topic} to {audience} in exactly 3 bullet points.")\n])\n\n# Build and run chain\n',
                        "solution": 'from langchain_anthropic import ChatAnthropic\nfrom langchain_core.prompts import ChatPromptTemplate\nfrom langchain_core.output_parsers import StrOutputParser\nllm = ChatAnthropic(model="claude-sonnet-4-20250514")\nprompt = ChatPromptTemplate.from_messages([\n    ("system", "You are an expert science communicator."),\n    ("human", "Explain {topic} to {audience} in exactly 3 bullet points.")\n])\nchain = prompt | llm | StrOutputParser()\nresult = chain.invoke({"topic": "black holes", "audience": "beginners"})\nprint(result)',
                        "check": [],
                        "hints": ["chain = prompt | llm | StrOutputParser()", "chain.invoke({'topic': ..., 'audience': ...})", "Print the result"]
                    }
                ],
                "reward": {"xp": 700, "badge": "🦜 AI Builder", "unlock": "ai_002"}
            },
            {
                "id": "ai_002",
                "title": "LangGraph Agent Protocol",
                "story": "🕸️ ARIA: *'The ultimate mission — build an AI Agent that can PLAN, EXECUTE, and REVIEW autonomously using LangGraph!'*",
                "concept": "LangGraph Agents",
                "xp": 1000,
                "energy": 5,
                "difficulty": "⭐⭐⭐⭐⭐",
                "steps": [
                    {
                        "type": "story",
                        "content": "**ARIA:** *'LangGraph builds stateful AI workflows — like flowcharts that AI follows!'*\n\n```python\nfrom langgraph.graph import StateGraph, END\nfrom typing import TypedDict, List\n\nclass AgentState(TypedDict):\n    task: str\n    steps: List[str]\n    result: str\n    done: bool\n\ndef planner(state: AgentState) -> AgentState:\n    plan = f\"Plan: Break down '{state['task']}'\" \n    return {\"steps\": [plan], \"done\": False}\n\ndef executor(state: AgentState) -> AgentState:\n    steps = state[\"steps\"] + [\"Executed the plan\"]\n    return {\"steps\": steps}\n\ndef reviewer(state: AgentState) -> AgentState:\n    return {\"result\": \"Task complete!\", \"done\": True}\n\ndef route(state: AgentState):\n    return END if state[\"done\"] else \"executor\"\n\n# Build the graph\nwf = StateGraph(AgentState)\nwf.add_node(\"planner\", planner)\nwf.add_node(\"executor\", executor)\nwf.add_node(\"reviewer\", reviewer)\nwf.set_entry_point(\"planner\")\nwf.add_edge(\"planner\", \"executor\")\nwf.add_edge(\"executor\", \"reviewer\")\nwf.add_conditional_edges(\"reviewer\", route)\n\napp = wf.compile()\nresult = app.invoke({\"task\": \"Deploy rocket\", \"steps\": [], \"result\": \"\", \"done\": False})\nprint(result)\n```"
                    },
                    {
                        "type": "visual",
                        "content": "langgraph_visual",
                        "caption": "LangGraph: Nodes (steps) + Edges (flow) = Intelligent Agent"
                    },
                    {
                        "type": "quiz",
                        "question": "In LangGraph, what is a 'node'?",
                        "options": ["A data type", "A processing step/function in the workflow", "A variable", "An API call"],
                        "answer": 1,
                        "explanation": "Nodes are functions that process state. Each node does one thing in the workflow."
                    },
                    {
                        "type": "code",
                        "instruction": "🎯 Build a 3-node LangGraph: researcher → analyzer → reporter. Each node adds its output to a 'findings' list. Run with task='Analyze Jupiter atmosphere'.",
                        "starter": 'from langgraph.graph import StateGraph, END\nfrom typing import TypedDict, List\n\nclass ResearchState(TypedDict):\n    task: str\n    findings: List[str]\n    final_report: str\n\ndef researcher(state):\n    # Add "Researched: {task}" to findings\n    pass\n\ndef analyzer(state):\n    # Add "Analyzed findings" to findings\n    pass\n\ndef reporter(state):\n    # Set final_report = "Report: " + all findings joined\n    pass\n\n# Build and compile the graph\n',
                        "solution": 'from langgraph.graph import StateGraph, END\nfrom typing import TypedDict, List\nclass ResearchState(TypedDict):\n    task: str\n    findings: List[str]\n    final_report: str\ndef researcher(state):\n    return {"findings": state["findings"] + [f"Researched: {state[\'task\']}"]}\ndef analyzer(state):\n    return {"findings": state["findings"] + ["Analyzed all data points"]}\ndef reporter(state):\n    report = "Report: " + " | ".join(state["findings"])\n    return {"final_report": report}\nwf = StateGraph(ResearchState)\nwf.add_node("researcher", researcher)\nwf.add_node("analyzer", analyzer)\nwf.add_node("reporter", reporter)\nwf.set_entry_point("researcher")\nwf.add_edge("researcher", "analyzer")\nwf.add_edge("analyzer", "reporter")\nwf.add_edge("reporter", END)\napp = wf.compile()\nresult = app.invoke({"task": "Analyze Jupiter atmosphere", "findings": [], "final_report": ""})\nprint(result["final_report"])',
                        "check": ["Report"],
                        "hints": ["state['findings'] + [new_item] adds to list", "set_entry_point('researcher')", "add_edge connects nodes in sequence"]
                    }
                ],
                "reward": {"xp": 1000, "badge": "🕸️ Agent Architect", "unlock": None}
            }
        ]
    }
}

# ══════════════════════════════════════════════════════════════
# BATTLE SYSTEM
# ══════════════════════════════════════════════════════════════

BATTLE_QUESTIONS = {
    "beginner": [
        {"q": "What does `len('hello')` return?", "options": ["4","5","6","Error"], "answer": 1, "topic": "strings"},
        {"q": "Which is a valid variable name?", "options": ["2name","my name","my_name","my-name"], "answer": 2, "topic": "variables"},
        {"q": "`range(1, 5)` produces how many numbers?", "options": ["3","4","5","6"], "answer": 1, "topic": "loops"},
        {"q": "What does `type(3.14)` return?", "options": ["int","str","float","number"], "answer": 2, "topic": "types"},
        {"q": "How do you start a comment in Python?", "options": ["//","/* */","#","--"], "answer": 2, "topic": "syntax"},
        {"q": "`[1,2,3].append(4)` — list is now?", "options": ["[4,1,2,3]","[1,2,3,4]","[1,2,4]","Error"], "answer": 1, "topic": "lists"},
        {"q": "What is `10 % 3`?", "options": ["3","1","0","3.3"], "answer": 1, "topic": "operators"},
        {"q": "Which keyword defines a function?", "options": ["function","func","def","define"], "answer": 2, "topic": "functions"},
        {"q": "`bool(0)` is?", "options": ["True","False","0","None"], "answer": 1, "topic": "booleans"},
        {"q": "Print `Hello` 3 times — shortest code?", "options": ['print("Hello"*3)','print("Hello" * 3)','for i in 3: print("Hello")','print("Hello","Hello","Hello")'], "answer": 1, "topic": "strings"},
    ],
    "intermediate": [
        {"q": "What is a list comprehension?", "options": ["A loop","A compact way to create lists","A function","A class"], "answer": 1, "topic": "comprehensions"},
        {"q": "`dict.get('key', 'default')` — what if key missing?", "options": ["Error","None","Returns default","Returns key"], "answer": 2, "topic": "dicts"},
        {"q": "What does `*args` capture?", "options": ["Keyword args","Any number of positional args","Pointer","Starred import"], "answer": 1, "topic": "functions"},
        {"q": "Lambda `f = lambda x: x**2` — `f(5)` is?", "options": ["10","25","52","Error"], "answer": 1, "topic": "lambda"},
        {"q": "What does `__init__` do in a class?", "options": ["Deletes object","Initializes new object","Inherits parent","Loops"], "answer": 1, "topic": "oop"},
        {"q": "To inherit from Parent: `class Child(?):`", "options": ["extends Parent","inherits Parent","Parent","super(Parent)"], "answer": 2, "topic": "inheritance"},
        {"q": "What does `enumerate(['a','b','c'])` give?", "options": ["Indices only","Tuples of (index, value)","Count","Reversed"], "answer": 1, "topic": "builtins"},
        {"q": "Which is NOT a valid dict access?", "options": ["d['key']","d.get('key')","d.key","d.get('key','default')"], "answer": 2, "topic": "dicts"},
    ],
    "advanced": [
        {"q": "What is a decorator in Python?", "options": ["A design pattern","A function that wraps another function","A class method","A module"], "answer": 1, "topic": "decorators"},
        {"q": "What does `yield` do in a function?", "options": ["Returns value","Makes it a generator","Raises exception","Imports module"], "answer": 1, "topic": "generators"},
        {"q": "Time complexity of dict lookup?", "options": ["O(n)","O(log n)","O(1)","O(n²)"], "answer": 2, "topic": "algorithms"},
        {"q": "What is `__slots__` used for?", "options": ["Memory optimization","Loops","Inheritance","Decorators"], "answer": 0, "topic": "optimization"},
        {"q": "In ML, what is overfitting?", "options": ["Model too simple","Model memorizes training data","Out of memory","Slow training"], "answer": 1, "topic": "ml"},
        {"q": "What is gradient descent?", "options": ["Data preprocessing","Optimization algorithm","Neural layer","Loss function"], "answer": 1, "topic": "ml"},
    ]
}

# ══════════════════════════════════════════════════════════════
# ACHIEVEMENTS & CERTIFICATES
# ══════════════════════════════════════════════════════════════

ACHIEVEMENTS = {
    "☿ Mercury Explorer": {"desc": "Complete first Mercury mission", "xp": 50},
    "🚀 Mercury Master": {"desc": "Complete ALL Mercury missions", "xp": 200},
    "♀ Venus Explorer": {"desc": "Land on Venus", "xp": 100},
    "🏗️ Venus Master": {"desc": "Master OOP on Venus", "xp": 300},
    "🌍 Earth Explorer": {"desc": "Land on Earth", "xp": 150},
    "📊 Data Scientist": {"desc": "Complete all Data Science missions", "xp": 400},
    "🤖 ML Engineer": {"desc": "Train your first ML model", "xp": 500},
    "🦜 AI Builder": {"desc": "Build your first LangChain app", "xp": 700},
    "🕸️ Agent Architect": {"desc": "Build a LangGraph agent", "xp": 1000},
    "⚔️ Battle Winner": {"desc": "Win your first coding battle", "xp": 100},
    "🏆 Tournament Champion": {"desc": "Win 5 battles in a row", "xp": 500},
    "🔥 On Fire": {"desc": "7-day learning streak", "xp": 300},
    "💎 Perfect Coder": {"desc": "10 solutions on first try", "xp": 400},
    "⚡ Speed Demon": {"desc": "Complete a mission in under 3 minutes", "xp": 200},
    "🌟 Galaxy Explorer": {"desc": "Visit all 5 planets", "xp": 1000},
    "👑 Galaxy Hero": {"desc": "Complete ALL missions", "xp": 5000},
}

CERTIFICATES = [
    {
        "id": "cert_python_basics",
        "title": "Python Fundamentals",
        "subtitle": "Zero to Pythonista",
        "planet": "mercury",
        "required_missions": ["m_001", "m_002", "m_003", "m_004", "m_005", "m_006"],
        "color": "#A8A8A8",
        "icon": "☿"
    },
    {
        "id": "cert_oop",
        "title": "Object-Oriented Programming",
        "subtitle": "Architect of Code",
        "planet": "venus",
        "required_missions": ["v_001", "v_002"],
        "color": "#FF8C42",
        "icon": "🏗️"
    },
    {
        "id": "cert_data_science",
        "title": "Data Science Professional",
        "subtitle": "Master of Data",
        "planet": "earth",
        "required_missions": ["e_001", "e_002"],
        "color": "#4ECDC4",
        "icon": "📊"
    },
    {
        "id": "cert_ml",
        "title": "Machine Learning Engineer",
        "subtitle": "Teacher of Machines",
        "planet": "mars",
        "required_missions": ["ml_001"],
        "color": "#EF4444",
        "icon": "🤖"
    },
    {
        "id": "cert_ai",
        "title": "AI Application Developer",
        "subtitle": "Builder of Intelligence",
        "planet": "jupiter",
        "required_missions": ["ai_001", "ai_002"],
        "color": "#F59E0B",
        "icon": "🦜"
    },
    {
        "id": "cert_galaxy_hero",
        "title": "Galaxy Hero — Full Stack AI Developer",
        "subtitle": "From Zero to AI Hero",
        "planet": "all",
        "required_missions": ["m_001","m_002","m_003","m_004","m_005","m_006","v_001","v_002","e_001","e_002","ml_001","ai_001","ai_002"],
        "color": "#F5C518",
        "icon": "👑"
    }
]

XP_PER_LEVEL = 300

# ── Merge extra planets & content at import time ─────────────────────────────
try:
    from data.extra_content import EXTRA_PLANETS, EXTRA_CERTIFICATES, EXTRA_BATTLE_QUESTIONS, PORTFOLIO_PROJECTS
    GALAXY.update(EXTRA_PLANETS)
    CERTIFICATES.extend(EXTRA_CERTIFICATES)
    BATTLE_QUESTIONS.update(EXTRA_BATTLE_QUESTIONS)
except ImportError:
    try:
        from extra_content import EXTRA_PLANETS, EXTRA_CERTIFICATES, EXTRA_BATTLE_QUESTIONS, PORTFOLIO_PROJECTS
        GALAXY.update(EXTRA_PLANETS)
        CERTIFICATES.extend(EXTRA_CERTIFICATES)
        BATTLE_QUESTIONS.update(EXTRA_BATTLE_QUESTIONS)
    except ImportError:
        PORTFOLIO_PROJECTS = []

ACHIEVEMENTS.update({
    "🪐 API Architect": {"desc": "Build your first FastAPI endpoint", "xp": 800},
    "💾 Database Commander": {"desc": "Master SQLAlchemy & databases", "xp": 900},
    "🧠 RAG Engineer": {"desc": "Build a RAG system on Neptune", "xp": 1000},
    "👑 Galaxy Hero": {"desc": "Complete ALL missions in the galaxy", "xp": 5000},
})
