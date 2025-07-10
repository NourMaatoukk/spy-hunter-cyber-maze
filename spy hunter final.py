import pygame
import random
import sys
import hashlib

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spy Hunter: Cyber Maze")

# Colors
WHITE = (255, 255, 255)

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
GRAY = (50, 50, 50)
ORANGE = (255, 165, 0)

# Image paths (update to match your files)
IMAGE_PATHS = {
    "player": "assets/player.png.png",
    "firewall": "assets/firewall.png.png",
    "malware": "assets/malware.png.png",
    "key": "assets/key.png.png",
    "lock": "assets/lock.png.png",
    "unlock": "assets/unlock.png.png",
    "background": "assets/background.png",
    "fake_key": "assets/fake_key.png.png",      # <-- your fake key icon
    "ransomware": "assets/ransomwere.png.png",  # <-- your ransomware icon
    "patch": "assets/patch.png",
    "shield": "assets/shield.png"
}

def load_image(name, path, size=(40, 40), color=BLUE):
    try:
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, size)
    except Exception as e:
        if name == "fake_key":
            raise FileNotFoundError(f"Fake key icon not found at {path}. Please check the filename and location.")
        print(f"Warning: {name} not found at {path}, using placeholder.")
        surface = pygame.Surface(size)
        surface.fill(color)
        return surface

images = {
    "player": load_image("player", IMAGE_PATHS["player"], (40, 40), BLUE),
    "firewall": load_image("firewall", IMAGE_PATHS["firewall"], (80, 80), RED),
    "malware": load_image("malware", IMAGE_PATHS["malware"], (40, 40), GREEN),
    "key": load_image("key", IMAGE_PATHS["key"], (50, 50), YELLOW),
    "lock": load_image("lock", IMAGE_PATHS["lock"], (30, 30), WHITE),
    "unlock": load_image("unlock", IMAGE_PATHS["unlock"], (30, 30), CYAN),
    "background": load_image("background", IMAGE_PATHS["background"], (WIDTH, HEIGHT), GRAY),
    "fake_key": load_image("fake_key", IMAGE_PATHS["fake_key"], (30, 30)),
    "ransomware": load_image("ransomware", IMAGE_PATHS["ransomware"], (80, 80)),
    "patch": load_image("patch", IMAGE_PATHS["patch"], (30, 30)),
    "shield": load_image("shield", IMAGE_PATHS["shield"], (30, 30))
}

try:
    title_font = pygame.font.Font(None, 72)
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)
except:
    title_font = pygame.font.SysFont('arial', 72)
    font = pygame.font.SysFont('arial', 36)
    small_font = pygame.font.SysFont('arial', 24)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = images["player"]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed = 7
        self.health = 100
        self.keys = 0
        self.max_health = 100
        self.locked_until = 0
        self.invincible_until = 0

    def update(self):
        if pygame.time.get_ticks() < self.locked_until:
            return
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed
        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, HEIGHT - self.rect.height))

    def draw_health_bar(self, surface):
        health_ratio = self.health / self.max_health
        bar_width = 200
        bar_height = 20
        fill_width = int(bar_width * health_ratio)
        outline_rect = pygame.Rect(10, 10, bar_width, bar_height)
        fill_rect = pygame.Rect(10, 10, fill_width, bar_height)
        pygame.draw.rect(surface, RED, fill_rect)
        pygame.draw.rect(surface, WHITE, outline_rect, 2)

class Firewall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = images["firewall"]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Malware(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = images["malware"]
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)
        self.speed_x = random.choice([-3, -2, -1, 1, 2, 3])
        self.speed_y = random.choice([-3, -2, -1, 1, 2, 3])

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.speed_x *= -1
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.speed_y *= -1

class Key(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = images["key"]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, surface):
        # Draw a yellow glow/outline
        outline_rect = self.rect.inflate(12, 12)
        pygame.draw.ellipse(surface, (255, 255, 100), outline_rect)
        surface.blit(self.image, self.rect)

class FakeKey(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = images["fake_key"]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Patch(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = images["patch"]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Shield(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = images["shield"]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class LockedFile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = images["lock"]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.locked = True

    def unlock(self):
        self.locked = False
        self.image = images["unlock"]

def show_start_screen():
    screen.fill(GRAY)
    title_text = title_font.render("Spy Hunter: Cyber Maze", True, CYAN)
    start_text = font.render("Press any key to start", True, WHITE)
    tip_text = small_font.render("Use arrow keys or WASD to move", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
    screen.blit(tip_text, (WIDTH // 2 - tip_text.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False

def show_level_complete(level):
    screen.fill(GRAY)
    complete_text = title_font.render(f"Level {level} Complete!", True, GREEN)
    next_text = font.render("Press any key for next level", True, WHITE)
    tips = [
        "Tip: Firewalls protect your system.",
        "Tip: Don't open unknown links.",
        "Tip: Use strong, unique passwords.",
        "Tip: Keep your software updated.",
        "Tip: Encryption protects your data.",
        "Tip: Never click suspicious links or attachments.",
        "Tip: Use two-factor authentication.",
        "Tip: Beware of phishing emails!"
    ]
    tip_text = small_font.render(tips[min(level-1, len(tips)-1)], True, YELLOW)
    screen.blit(complete_text, (WIDTH // 2 - complete_text.get_width() // 2, HEIGHT // 3))
    screen.blit(next_text, (WIDTH // 2 - next_text.get_width() // 2, HEIGHT // 2))
    screen.blit(tip_text, (WIDTH // 2 - tip_text.get_width() // 2, HEIGHT // 2 + 100))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False

def show_game_over(level):
    screen.fill(GRAY)
    over_text = title_font.render("Game Over!", True, RED)
    level_text = font.render(f"You reached level {level}", True, WHITE)
    restart_text = font.render("Press R to restart or ESC to quit", True, WHITE)
    screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 3))
    screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, HEIGHT // 2))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 100))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_r:
                    waiting = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def create_level(level):
    all_sprites = pygame.sprite.Group()
    firewalls = pygame.sprite.Group()
    malwares = pygame.sprite.Group()
    keys = pygame.sprite.Group()
    fake_keys = pygame.sprite.Group()
    patches = pygame.sprite.Group()
    shields = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)

    # Place firewalls
    for i in range(3 + level):
        fw = Firewall(random.randint(0, WIDTH-60), random.randint(0, HEIGHT-60))
        all_sprites.add(fw)
        firewalls.add(fw)

    # Place malwares
    for i in range(5 + level * 2):
        mw = Malware()
        all_sprites.add(mw)
        malwares.add(mw)

    # Helper function to check overlap
    def is_overlapping(rect, group):
        for sprite in group:
            if rect.colliderect(sprite.rect):
                return True
        return False

    keys_needed = min(3 + level // 2, 7)
    # Place keys without overlap
    for i in range(keys_needed):
        placed = False
        while not placed:
            k = Key(random.randint(0, WIDTH-25), random.randint(0, HEIGHT-25))
            if not (is_overlapping(k.rect, firewalls) or is_overlapping(k.rect, malwares) or is_overlapping(k.rect, keys) or is_overlapping(k.rect, fake_keys)):
                all_sprites.add(k)
                keys.add(k)
                placed = True

    # Place fake keys without overlap
    for i in range(1 + level // 2):
        placed = False
        while not placed:
            fk = FakeKey(random.randint(0, WIDTH-25), random.randint(0, HEIGHT-25))
            if not (is_overlapping(fk.rect, firewalls) or is_overlapping(fk.rect, malwares) or is_overlapping(fk.rect, keys) or is_overlapping(fk.rect, fake_keys)):
                all_sprites.add(fk)
                fake_keys.add(fk)
                placed = True

    # Place patches and shields
    if random.random() < 0.7:
        patch = Patch(random.randint(0, WIDTH-25), random.randint(0, HEIGHT-25))
        all_sprites.add(patch)
        patches.add(patch)
    if random.random() < 0.7:
        shield = Shield(random.randint(0, WIDTH-25), random.randint(0, HEIGHT-25))
        all_sprites.add(shield)
        shields.add(shield)

    lf = LockedFile(WIDTH - 100, HEIGHT - 100)
    all_sprites.add(lf)
    return player, all_sprites, firewalls, malwares, keys, fake_keys, patches, shields, lf, keys_needed

def show_story_intro():
    screen.fill(GRAY)
    lines = [
        "In a world overrun by cyber threats,",
        "you are the last hope: the Spy Hunter.",
        "",
        "Your mission: infiltrate the cyber maze,",
        "collect encryption keys, avoid malware,",
        "and unlock the files to save the digital world.",
        "",
        "Press any key to begin your mission..."
    ]
    y = HEIGHT // 4
    for line in lines:
        text = font.render(line, True, CYAN if "Spy Hunter" in line else WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y))
        y += 50
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False

def show_mission_objective(level):
    screen.fill(GRAY)
    objectives = [
        f"Level {level} Mission:",
        "",
        "• Collect all the keys.",
        "• Avoid malware and fake keys.",
        "• Use firewalls, patches, and shields to survive.",
        "• Unlock the encrypted file to advance.",
        "",
        "Press any key to start this level."
    ]
    y = HEIGHT // 4
    for line in objectives:
        text = font.render(line, True, YELLOW if "Mission" in line else WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y))
        y += 40
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False

def show_security_quiz():
    questions = [
        {
            "q": "What should you do if you receive a suspicious email?",
            "a": ["A) Open all attachments", "B) Click all links", "C) Delete or report it", "D) Reply with your password"],
            "correct": 2
        },
        {
            "q": "What is a strong password?",
            "a": ["A) 123456", "B) Your name", "C) A mix of letters, numbers, and symbols", "D) password"],
            "correct": 2
        },
        {
            "q": "What does a firewall do?",
            "a": ["A) Cools your computer", "B) Blocks unauthorized access", "C) Stores files", "D) Makes your computer faster"],
            "correct": 1
        },
        {
            "q": "What is encryption?",
            "a": ["A) Deleting files", "B) Scrambling data to protect it", "C) Making files larger", "D) Compressing files"],
            "correct": 1
        },
        {
            "q": "Which is a symmetric encryption algorithm?",
            "a": ["A) RSA", "B) AES", "C) ECC", "D) DSA"],
            "correct": 1
        },
        {
            "q": "Which is an asymmetric encryption algorithm?",
            "a": ["A) DES", "B) AES", "C) RSA", "D) 3DES"],
            "correct": 2
        },
        {
            "q": "What does a hash function do?",
            "a": ["A) Encrypts data", "B) Compresses data", "C) Converts data to a fixed-size value", "D) Decrypts data"],
            "correct": 2
        },
        {
            "q": "What is decryption?",
            "a": ["A) Making data unreadable", "B) Turning encrypted data back to readable form", "C) Backing up data", "D) Copying data"],
            "correct": 1
        },
        {
            "q": "Which of these is NOT a hashing algorithm?",
            "a": ["A) SHA-256", "B) MD5", "C) AES", "D) SHA-1"],
            "correct": 2
        },
        {
            "q": "What is the main difference between symmetric and asymmetric encryption?",
            "a": ["A) Symmetric uses one key, asymmetric uses two", "B) Asymmetric is faster", "C) Symmetric is only for emails", "D) Asymmetric can't encrypt files"],
            "correct": 0
        },
        {
            "q": "What does AES stand for?",
            "a": ["A) Advanced Encryption Standard", "B) Automatic Email System", "C) Advanced Electronic Security", "D) Asymmetric Encryption Standard"],
            "correct": 0
        },
        {
            "q": "What does DES stand for?",
            "a": ["A) Data Encryption Standard", "B) Digital Email Service", "C) Data Electronic Security", "D) Digital Encryption System"],
            "correct": 0
        },
        {
            "q": "What is a public key used for in asymmetric encryption?",
            "a": ["A) Decrypting messages", "B) Encrypting messages", "C) Hashing data", "D) Compressing files"],
            "correct": 1
        },
        {
            "q": "Which of these is a property of a good hash function?",
            "a": ["A) Easy to reverse", "B) Produces same output for different inputs", "C) One-way and collision-resistant", "D) Slow to compute"],
            "correct": 2
        },
        {
            "q": "What is two-factor authentication?",
            "a": ["A) Using two passwords", "B) Using password and another method (like SMS)", "C) Using two usernames", "D) Using two computers"],
            "correct": 1
        },
        {
            "q": "What is phishing?",
            "a": ["A) A type of malware", "B) A fake website or message to steal info", "C) Encrypting data", "D) A backup method"],
            "correct": 1
        },
        {
            "q": "Which is an example of malware?",
            "a": ["A) Firewall", "B) Antivirus", "C) Ransomware", "D) VPN"],
            "correct": 2
        },
        {
            "q": "What is the purpose of a VPN?",
            "a": ["A) Speed up your internet", "B) Encrypt your internet traffic", "C) Store files", "D) Block pop-ups"],
            "correct": 1
        },
        {
            "q": "What is social engineering?",
            "a": ["A) Hacking computers", "B) Tricking people to reveal info", "C) Encrypting data", "D) Building networks"],
            "correct": 1
        },
        {
            "q": "What is a digital certificate?",
            "a": ["A) A software license", "B) A file that verifies identity online", "C) A backup file", "D) A password manager"],
            "correct": 1
        },
        {
            "q": "What is a brute-force attack?",
            "a": ["A) Guessing passwords by trying all combinations", "B) Encrypting data", "C) Sending spam emails", "D) Updating software"],
            "correct": 0
        },
        {
            "q": "What is ransomware?",
            "a": ["A) Software that locks files for payment", "B) Antivirus software", "C) A backup tool", "D) A firewall"],
            "correct": 0
        },
        {
            "q": "What is a backup?",
            "a": ["A) Copying data to another location", "B) Encrypting data", "C) Deleting files", "D) Compressing files"],
            "correct": 0
        },
        {
            "q": "What is biometric authentication?",
            "a": ["A) Using a password", "B) Using fingerprints or face recognition", "C) Using a PIN", "D) Using a backup"],
            "correct": 1
        },
        {
            "q": "What is a security patch?",
            "a": ["A) A software update fixing vulnerabilities", "B) A backup file", "C) A password", "D) A firewall"],
            "correct": 0
        },
        {
            "q": "What is a Trojan horse?",
            "a": ["A) A type of malware disguised as legitimate software", "B) A firewall", "C) A password manager", "D) A VPN"],
            "correct": 0
        },
        {
            "q": "What is the purpose of a digital signature?",
            "a": ["A) Encrypt data", "B) Verify authenticity and integrity", "C) Compress files", "D) Backup data"],
            "correct": 1
        },
        {
            "q": "What is shoulder surfing?",
            "a": ["A) Watching someone enter their password", "B) Surfing the web securely", "C) Encrypting data", "D) Using a VPN"],
            "correct": 0
        },
        {
            "q": "What is multi-factor authentication?",
            "a": ["A) Using multiple passwords", "B) Using two or more authentication methods", "C) Using two computers", "D) Using a backup"],
            "correct": 1
        },
        {
            "q": "What is a worm?",
            "a": ["A) A type of malware that spreads itself", "B) A firewall", "C) A password manager", "D) A VPN"],
            "correct": 0
        },
        {
            "q": "What is the main purpose of hashing passwords?",
            "a": ["A) To store them securely", "B) To make them longer", "C) To encrypt them", "D) To delete them"],
            "correct": 0
        }
    ]
    q = random.choice(questions)
    screen.fill(GRAY)
    y = HEIGHT // 4
    question_text = font.render(q["q"], True, YELLOW)
    screen.blit(question_text, (WIDTH // 2 - question_text.get_width() // 2, y))
    y += 60
    answer_rects = []
    for i, ans in enumerate(q["a"]):
        ans_text = font.render(ans, True, WHITE)
        rect = ans_text.get_rect(center=(WIDTH // 2, y))
        screen.blit(ans_text, rect)
        answer_rects.append(rect)
        y += 40
    pygame.display.flip()
    waiting = True
    selected = None
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_KP1]:
                    selected = 0
                elif event.key in [pygame.K_2, pygame.K_KP2]:
                    selected = 1
                elif event.key in [pygame.K_3, pygame.K_KP3]:
                    selected = 2
                elif event.key in [pygame.K_4, pygame.K_KP4]:
                    selected = 3
                if selected is not None:
                    waiting = False
    # Show feedback
    screen.fill(GRAY)
    if selected == q["correct"]:
        feedback = font.render("Correct! Stay cyber safe!", True, GREEN)
    else:
        feedback = font.render("Incorrect. Learn and try again!", True, RED)
    screen.blit(feedback, (WIDTH // 2 - feedback.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(2000)

def password_challenge():
    password_questions = [
        {
            "q": "Choose the strongest password:",
            "a": [
                "A) password123",
                "B) John2024",
                "C) $tr0ng!Passw0rd",
                "D) 123456"
            ],
            "correct": 2
        },
        {
            "q": "Which password is most secure?",
            "a": [
                "A) football",
                "B) QwErTy!2023",
                "C) 111111",
                "D) letmein"
            ],
            "correct": 1
        },
        {
            "q": "Which password should you avoid?",
            "a": [
                "A) MyDog$Barks2",
                "B) 12345678",
                "C) !SecurePass2024",
                "D) 9x!Tg#2Lp"
            ],
            "correct": 1
        }
    ]
    q = random.choice(password_questions)
    screen.fill(GRAY)
    question = font.render(q["q"], True, YELLOW)
    screen.blit(question, (WIDTH // 2 - question.get_width() // 2, HEIGHT // 3))
    y = HEIGHT // 3 + 50
    for i, opt in enumerate(q["a"]):
        opt_text = font.render(opt, True, WHITE)
        screen.blit(opt_text, (WIDTH // 2 - opt_text.get_width() // 2, y))
        y += 40
    pygame.display.flip()
    waiting = True
    selected = None
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_KP1]:
                    selected = 0
                elif event.key in [pygame.K_2, pygame.K_KP2]:
                    selected = 1
                elif event.key in [pygame.K_3, pygame.K_KP3]:
                    selected = 2
                elif event.key in [pygame.K_4, pygame.K_KP4]:
                    selected = 3
                if selected is not None:
                    waiting = False
    # Show feedback
    screen.fill(GRAY)
    if selected == q["correct"]:
        feedback = font.render("Correct! That's a strong password.", True, GREEN)
    else:
        feedback = font.render("Incorrect. Use a mix of letters, numbers, and symbols.", True, RED)
    screen.blit(feedback, (WIDTH // 2 - feedback.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(2000)

achievements = {
    "phishing_avoided": False,
    "all_keys_collected": False,
    "no_damage_level": False
}

def check_achievements(player, keys_needed, took_damage):
    if player.keys == keys_needed:
        achievements["all_keys_collected"] = True
    if not took_damage:
        achievements["no_damage_level"] = True

def show_achievements():
    screen.fill(GRAY)
    y = HEIGHT // 4
    title = font.render("Achievements Unlocked:", True, CYAN)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, y))
    y += 50
    for name, unlocked in achievements.items():
        text = f"{name.replace('_', ' ').title()}: {'Yes' if unlocked else 'No'}"
        ach_text = font.render(text, True, GREEN if unlocked else WHITE)
        screen.blit(ach_text, (WIDTH // 2 - ach_text.get_width() // 2, y))
        y += 40
    pygame.display.flip()
    pygame.time.wait(2000)

def main():
    clock = pygame.time.Clock()
    level = 1
    game_over = False
    running = True
    show_story_intro()
    show_start_screen()
    show_security_quiz()  # <-- Ask a question before starting the game
    player, all_sprites, firewalls, malwares, keys, fake_keys, patches, shields, lf, keys_needed = create_level(level)
    show_mission_objective(level)
    cyber_tips = [
        "Collect keys to unlock the encrypted file!",
        "Avoid malware!",
        "Firewalls protect you from attacks!",
        "Each key brings you closer to decryption.",
        "Health decreases when you hit threats.",
        "Never click suspicious links or attachments.",
        "Use strong, unique passwords for every account.",
        "Enable two-factor authentication.",
        "Update your software regularly.",
        "Beware of phishing emails!",
        "Apply security patches to stay safe.",
        "Use shields to restore your health.",
        "Never share your password with anyone.",
        "Check URLs for typos before clicking.",
        "Don't reuse passwords across sites.",
        "Lock your computer when away.",
        "Backup your data regularly.",
        "Beware of urgent messages asking for info."
    ]
    current_tip = random.choice(cyber_tips)
    tip_time = pygame.time.get_ticks()
    ransomware_cooldown = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        if not game_over:
            all_sprites.update()
            now = pygame.time.get_ticks()
            if now - tip_time > 10000:
                current_tip = random.choice(cyber_tips)
                tip_time = now

            malware_hits = pygame.sprite.spritecollide(player, malwares, False)
            firewall_protection = pygame.sprite.spritecollide(player, firewalls, False)
            if not firewall_protection and now > player.invincible_until:
                for hit in malware_hits:
                    if now > ransomware_cooldown and random.random() < 0.1:
                        player.locked_until = now + 5000
                        current_tip = "Ransomware attack! You are locked for 5 seconds!"
                        tip_time = now
                        ransomware_cooldown = now + 10000

                        # Show a ransomware-specific tip or quiz
                        ransomware_tips = [
                            "Tip: Ransomware can lock your files. Always keep backups!",
                            "Tip: Never pay the ransom. Restore from backups if possible.",
                            "Tip: Keep your software updated to avoid ransomware.",
                            "Tip: Don't open suspicious email attachments."
                        ]
                        # Randomly choose to show a tip or a question
                        if random.random() < 0.5:
                            # Show a ransomware tip
                            tip = random.choice(ransomware_tips)
                            tip_font = pygame.font.Font(None, 40)
                            tip_text = tip_font.render(tip, True, BLACK)
                            tip_bg_width = tip_text.get_width() + 40
                            tip_bg_height = tip_text.get_height() + 20
                            tip_bg_x = WIDTH // 2 - tip_bg_width // 2
                            tip_bg_y = HEIGHT // 2 - tip_bg_height // 2
                            pygame.draw.rect(screen, YELLOW, (tip_bg_x, tip_bg_y, tip_bg_width, tip_bg_height), border_radius=15)
                            screen.blit(tip_text, (tip_bg_x + 20, tip_bg_y + 10))
                            pygame.display.flip()
                            pygame.time.wait(2500)
                        else:
                            # Ask a ransomware-related security question
                            ransomware_questions = [
                                {
                                    "q": "What is the best way to recover from a ransomware attack?",
                                    "a": [
                                        "A) Pay the ransom",
                                        "B) Restore from backups",
                                        "C) Ignore it",
                                        "D) Restart your computer"
                                    ],
                                    "correct": 1
                                },
                                {
                                    "q": "How can you best prevent ransomware infections?",
                                    "a": [
                                        "A) Open all email attachments",
                                        "B) Keep software updated",
                                        "C) Disable antivirus",
                                        "D) Use weak passwords"
                                    ],
                                    "correct": 1
                                },
                                {
                                    "q": "What should you do if you receive a suspicious file?",
                                    "a": [
                                        "A) Open it immediately",
                                        "B) Scan it with antivirus",
                                        "C) Forward it to friends",
                                        "D) Ignore security warnings"
                                    ],
                                    "correct": 1
                                },
                                {
                                    "q": "What is a common delivery method for ransomware?",
                                    "a": [
                                        "A) Phishing emails",
                                        "B) Printed letters",
                                        "C) Phone calls",
                                        "D) Social media posts"
                                    ],
                                    "correct": 0
                                },
                                {
                                    "q": "Which is NOT a good defense against ransomware?",
                                    "a": [
                                        "A) Regular backups",
                                        "B) Clicking unknown links",
                                        "C) Using antivirus",
                                        "D) Updating your OS"
                                    ],
                                    "correct": 1
                                }
                            ]
                            question = random.choice(ransomware_questions)
                            screen.fill(GRAY)
                            question_text = font.render(question["q"], True, YELLOW)
                            screen.blit(question_text, (WIDTH // 2 - question_text.get_width() // 2, HEIGHT // 2 - 60))
                            y = HEIGHT // 2
                            for i, ans in enumerate(question["a"]):
                                ans_text = font.render(ans, True, WHITE)
                                screen.blit(ans_text, (WIDTH // 2 - ans_text.get_width() // 2, y))
                                y += 40
                            pygame.display.flip()
                            waiting = True
                            selected = None
                            while waiting:
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        pygame.quit()
                                        sys.exit()
                                    if event.type == pygame.KEYDOWN:
                                        if event.key in [pygame.K_1, pygame.K_KP1]:
                                            selected = 0
                                        elif event.key in [pygame.K_2, pygame.K_KP2]:
                                            selected = 1
                                        elif event.key in [pygame.K_3, pygame.K_KP3]:
                                            selected = 2
                                        elif event.key in [pygame.K_4, pygame.K_KP4]:
                                            selected = 3
                                        if selected is not None:
                                            waiting = False
                            # Show feedback
                            screen.fill(GRAY)
                            if selected == question["correct"]:
                                feedback = font.render("Correct! Stay cyber safe!", True, GREEN)
                            else:
                                feedback = font.render("Incorrect. Learn and try again!", True, RED)
                            screen.blit(feedback, (WIDTH // 2 - feedback.get_width() // 2, HEIGHT // 2))
                            pygame.display.flip()
                            pygame.time.wait(2000)
                    else:
                        player.health -= 0.5
                        if player.health <= 0:
                            game_over = True

            fake_key_hits = pygame.sprite.spritecollide(player, fake_keys, True)
            for hit in fake_key_hits:
                player.health -= 15
                player.keys = 0  # <-- Only here!
                current_tip = "Phishing trap! Your keys are reset. Beware of fake keys!"
                tip_time = pygame.time.get_ticks()
                # New learning tip display
                learning_tip = small_font.render("Tip: Always check for phishing signs!", True, YELLOW)
                screen.blit(learning_tip, (WIDTH // 2 - learning_tip.get_width() // 2, HEIGHT - 60 - 76))  # Move up by 2 cm (~76px)
                pygame.display.flip()
                pygame.time.wait(1200)

            patch_hits = pygame.sprite.spritecollide(player, patches, True)
            for hit in patch_hits:
                player.invincible_until = now + 7000
                current_tip = "Security patch applied! Invincible for 7 seconds."
                tip_time = now

            shield_hits = pygame.sprite.spritecollide(player, shields, True)
            for hit in shield_hits:
                player.health = min(player.max_health, player.health + 30)
                current_tip = "Shield collected! Health restored."
                tip_time = now

            key_hits = pygame.sprite.spritecollide(player, keys, True)
            for hit in key_hits:
                player.keys += 1
                current_tip = f"Key {player.keys}/{keys_needed} collected!"
                tip_time = pygame.time.get_ticks()
            if pygame.sprite.collide_rect(player, lf) and player.keys >= keys_needed and lf.locked:
                password_challenge()
                lf.unlock()
                show_level_complete(level)
                show_security_quiz()
                show_achievements()
                level += 1

                # --- Encryption challenge now happens EVERY level ---
                passed = encryption_challenge_level()
                if not passed:
                    fail_msg = font.render("Encryption challenge failed! Try again.", True, RED)
                    screen.fill(GRAY)
                    screen.blit(fail_msg, (WIDTH//2 - fail_msg.get_width()//2, HEIGHT//2))
                    pygame.display.flip()
                    pygame.time.wait(2000)
                    continue  # Don't advance level
                # --- End encryption challenge block ---

                player, all_sprites, firewalls, malwares, keys, fake_keys, patches, shields, lf, keys_needed = create_level(level)
                show_mission_objective(level)

        screen.blit(images["background"], (0, 0))
        # Instead of:
        # all_sprites.draw(screen)

        # Use:
        for sprite in all_sprites:
            if isinstance(sprite, Key):
                sprite.draw(screen)
            else:
                screen.blit(sprite.image, sprite.rect)

        health_text = font.render(f"Health: {int(player.health)}%", True, WHITE)
        keys_text = font.render(f"Keys: {player.keys}/{keys_needed}", True, WHITE)
        level_text = font.render(f"Level: {level}", True, WHITE)
        player.draw_health_bar(screen)
        screen.blit(health_text, (220, 10))
        screen.blit(keys_text, (WIDTH - 200, 10))
        screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, 10))
        # --- Add this line for header instructions ---
        instructions = "Move: Arrow keys or WASD | Collect all keys | Avoid malware & fake keys | Unlock the file!"
        header_text = small_font.render(instructions, True, YELLOW)
        screen.blit(header_text, (WIDTH // 2 - header_text.get_width() // 2, 40))
        # --- End header instructions ---
        # Bold black tip text at the bottom
        small_font.set_bold(True)
        tip_text = small_font.render(current_tip, True, BLACK)
        small_font.set_bold(False)
        screen.blit(tip_text, (WIDTH // 2 - tip_text.get_width() // 2, HEIGHT - 30))
        # New warning notification for cyber tip
        tip_font = pygame.font.Font(None, 40)  # Larger font for visibility
        tip_text = tip_font.render(current_tip, True, BLACK)
        tip_bg_width = tip_text.get_width() + 40
        tip_bg_height = tip_text.get_height() + 20
        tip_bg_x = WIDTH // 2 - tip_bg_width // 2
        tip_bg_y = 90  # Near the top, below the header

        # Draw yellow rounded rectangle as background
        pygame.draw.rect(screen, YELLOW, (tip_bg_x, tip_bg_y, tip_bg_width, tip_bg_height), border_radius=15)
        # Optional: Draw a warning icon (triangle with exclamation)
        pygame.draw.polygon(screen, ORANGE, [
            (tip_bg_x + 20, tip_bg_y + tip_bg_height // 2 + 12),
            (tip_bg_x + 10, tip_bg_y + tip_bg_height - 10),
            (tip_bg_x + 30, tip_bg_y + tip_bg_height - 10)
        ])
        pygame.draw.line(screen, BLACK, (tip_bg_x + 20, tip_bg_y + tip_bg_height // 2 + 12), (tip_bg_x + 20, tip_bg_y + tip_bg_height - 18), 3)
        pygame.draw.circle(screen, BLACK, (tip_bg_x + 20, tip_bg_y + tip_bg_height - 14), 2)

        # Draw the tip text
        screen.blit(tip_text, (tip_bg_x + 40, tip_bg_y + 10))

        # New instruction text at the top
        if player.locked_until > pygame.time.get_ticks():
            icon = images["ransomware"]
            screen.blit(icon, (WIDTH // 2 - icon.get_width() // 2, HEIGHT // 2 - icon.get_height() // 2 - 40))
            locked_text = font.render("You are locked by ransomware!", True, RED)
            screen.blit(locked_text, (WIDTH // 2 - locked_text.get_width() // 2, HEIGHT // 2 + 40))
        if player.invincible_until > pygame.time.get_ticks():
            inv_text = font.render("Invincible!", True, CYAN)
            screen.blit(inv_text, (WIDTH // 2 - inv_text.get_width() // 2, HEIGHT // 2 + 80))
        if game_over:
            show_game_over(level)
            game_over = False
            level = 1
            player, all_sprites, firewalls, malwares, keys, fake_keys, patches, shields, lf, keys_needed = create_level(level)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    sys.exit()

# --- Playfair Cipher Utilities ---
def generate_playfair_matrix(key_phrase):
    key_phrase = key_phrase.upper().replace('J', 'I')
    seen = set()
    matrix = []
    for c in key_phrase + "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if c.isalpha() and c not in seen:
            seen.add(c)
            matrix.append(c)
    return [matrix[i*5:(i+1)*5] for i in range(5)]

def playfair_find(matrix, char):
    for i, row in enumerate(matrix):
        for j, c in enumerate(row):
            if c == char:
                return i, j
    return None, None

def playfair_prepare(text):
    text = text.upper().replace('J', 'I')
    result = ""
    i = 0
    while i < len(text):
        a = text[i]
        b = text[i+1] if i+1 < len(text) else 'X'
        if a == b:
            result += a + 'X'
            i += 1
        else:
            result += a + b
            i += 2
    if len(result) % 2 != 0:
        result += 'X'
    return result

def playfair_encrypt(plaintext, matrix):
    plaintext = playfair_prepare(plaintext)
    ciphertext = ""
    for i in range(0, len(plaintext), 2):
        a, b = plaintext[i], plaintext[i+1]
        row1, col1 = playfair_find(matrix, a)
        row2, col2 = playfair_find(matrix, b)
        if row1 == row2:
            ciphertext += matrix[row1][(col1+1)%5] + matrix[row2][(col2+1)%5]
        elif col1 == col2:
            ciphertext += matrix[(row1+1)%5][col1] + matrix[(row2+1)%5][col2]
        else:
            ciphertext += matrix[row1][col2] + matrix[row2][col1]
    return ciphertext

def playfair_decrypt(ciphertext, matrix):
    plaintext = ""
    for i in range(0, len(ciphertext), 2):
        a, b = ciphertext[i], ciphertext[i+1]
        row1, col1 = playfair_find(matrix, a)
        row2, col2 = playfair_find(matrix, b)
        if row1 == row2:
            plaintext += matrix[row1][(col1-1)%5] + matrix[row2][(col2-1)%5]
        elif col1 == col2:
            plaintext += matrix[(row1-1)%5][col1] + matrix[(row2-1)%5][col2]
        else:
            plaintext += matrix[row1][col2] + matrix[row2][col1]
    return plaintext

def sha256_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()

# --- Simulated Fingerprint Authentication ---
def fingerprint_authentication():
    screen.fill(GRAY)
    prompt = font.render("Place your finger on the scanner (press SPACE)", True, CYAN)
    screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, HEIGHT//2 - 60))
    pygame.draw.rect(screen, BLUE, (WIDTH//2-60, HEIGHT//2, 120, 60), border_radius=20)
    pygame.display.flip()
    waiting = True
    success = True  # Always succeed
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Always succeed, no random failure
                    # if random.random() > 0.15:
                    #     success = True
                    waiting = False
    screen.fill(GRAY)
    if success:
        msg = font.render("Fingerprint matched!", True, GREEN)
    else:
        msg = font.render("Fingerprint mismatch! Access denied.", True, RED)
    screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2))
    pygame.display.flip()
    pygame.time.wait(1500)
    return success

# --- Encryption Mini-Game Level ---
def encryption_challenge_level():
    # 1. Prompt user for key phrase
    key_phrase = ""
    input_active = True
    while input_active:
        screen.fill(GRAY)
        title = font.render("Encryption Challenge", True, YELLOW)
        prompt = font.render("Enter a key phrase for the Playfair cipher (A-Z, no spaces):", True, CYAN)
        key_text = font.render(key_phrase, True, GREEN)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 60))
        screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, 150))
        screen.blit(key_text, (WIDTH//2 - key_text.get_width()//2, 220))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(key_phrase) >= 4:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    key_phrase = key_phrase[:-1]
                elif event.unicode.isalpha() and len(key_phrase) < 20:
                    key_phrase += event.unicode.upper()

    # 2. Prompt user for message to encrypt
    plaintext = ""
    input_active = True
    while input_active:
        screen.fill(GRAY)
        title = font.render("Encryption Challenge", True, YELLOW)
        prompt = font.render("Enter a message to encrypt (A-Z, no spaces):", True, CYAN)
        msg_text = font.render(plaintext, True, GREEN)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 60))
        screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, 150))
        screen.blit(msg_text, (WIDTH//2 - msg_text.get_width()//2, 220))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(plaintext) >= 4:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    plaintext = plaintext[:-1]
                elif event.unicode.isalpha() and len(plaintext) < 30:
                    plaintext += event.unicode.upper()

    # Now proceed with the rest of your function as before...
    # (Show the word and key, matrix puzzle, fingerprint, encryption/decryption, etc.)
    # 1. Show the word and key to be used
    matrix = generate_playfair_matrix(key_phrase)

    # Show the word and key
    screen.fill(GRAY)
    title = font.render("Encryption Challenge", True, YELLOW)
    word_text = font.render(f"Word to encrypt: {plaintext}", True, CYAN)
    key_text = font.render(f"Key: {key_phrase}", True, GREEN)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 60))
    screen.blit(word_text, (WIDTH//2 - word_text.get_width()//2, 150))
    screen.blit(key_text, (WIDTH//2 - key_text.get_width()//2, 200))
    pygame.display.flip()
    pygame.time.wait(2000)

    # 2. Show Playfair matrix with keyword, let player fill the rest
    screen.fill(GRAY)
    title = font.render("Fill the Playfair Matrix Puzzle!", True, YELLOW)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 60))
    cell_size = 50

    # Prepare the matrix with keyword filled, rest empty
    keyword = key_phrase.upper().replace('J', 'I')
    seen = []
    for c in keyword:
        if c.isalpha() and c not in seen:
            seen.append(c)
    alphabet = [chr(i) for i in range(ord('A'), ord('Z')+1) if chr(i) != 'J']
    remaining = [c for c in alphabet if c not in seen]
    matrix_letters = seen + [''] * (25 - len(seen))

    idx = len(seen)
    input_active = True
    while input_active:
        # Draw matrix
        screen.fill(GRAY)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 60))
        for i in range(5):
            for j in range(5):
                pygame.draw.rect(screen, WHITE, (WIDTH//2-125+j*cell_size, 150+i*cell_size, cell_size, cell_size), 2)
                letter = matrix_letters[i*5+j]
                if letter:
                    ltr = font.render(letter, True, CYAN if letter in seen else GREEN)
                    screen.blit(ltr, (WIDTH//2-125+j*cell_size+15, 150+i*cell_size+10))
        # Show prompt for next letter
        if idx < 25:
            prompt = font.render(f"Type next letter: {remaining[0]}", True, YELLOW)
            screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, 450))
        else:
            prompt = font.render("Matrix complete! Press ENTER to continue.", True, GREEN)
            screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, 450))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if idx < 25 and event.type == pygame.KEYDOWN:
                key = event.unicode.upper()
                if key == remaining[0]:
                    matrix_letters[idx] = key
                    idx += 1
                    remaining.pop(0)
            elif idx == 25 and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = FalseB

    # Now build the matrix from matrix_letters
    matrix = [matrix_letters[i*5:(i+1)*5] for i in range(5)]
    pygame.time.wait(500)

    # 3. Fingerprint authentication
    if not fingerprint_authentication():
        return False  # Failed authentication

    # 4. Encrypt the message (animated)
    hash_val = sha256_hash(plaintext)
    prepared = playfair_prepare(plaintext)
    ciphertext = ""
    for i in range(0, len(prepared), 2):
        a, b = prepared[i], prepared[i+1]
        row1, col1 = playfair_find(matrix, a)
        row2, col2 = playfair_find(matrix, b)
        if row1 == row2:
            enc_a = matrix[row1][(col1+1)%5]
            enc_b = matrix[row2][(col2+1)%5]
        elif col1 == col2:
            enc_a = matrix[(row1+1)%5][col1]
            enc_b = matrix[(row2+1)%5][col2]
        else:
            enc_a = matrix[row1][col2]
            enc_b = matrix[row2][col1]
        ciphertext += enc_a + enc_b

        # Show the encryption step
        screen.fill(GRAY)
        msg1 = font.render("Encrypting message...", True, CYAN)
        msg2 = font.render(f"Plaintext pair: {a+b}", True, WHITE)
        msg3 = font.render(f"Encrypted pair: {enc_a+enc_b}", True, YELLOW)
        msg4 = font.render(f"Ciphertext so far: {ciphertext}", True, GREEN)
        screen.blit(msg1, (WIDTH//2 - msg1.get_width()//2, 100))
        screen.blit(msg2, (WIDTH//2 - msg2.get_width()//2, 180))
        screen.blit(msg3, (WIDTH//2 - msg3.get_width()//2, 240))
        screen.blit(msg4, (WIDTH//2 - msg4.get_width()//2, 320))
        pygame.display.flip()
        pygame.time.wait(900)  # Pause for visibility

    # Show hash after encryption
    screen.fill(GRAY)
    msg1 = font.render("Encryption complete!", True, CYAN)
    msg2 = font.render(f"Ciphertext: {ciphertext}", True, GREEN)
    msg3 = font.render(f"SHA-256: {hash_val[:16]}...", True, YELLOW)
    screen.blit(msg1, (WIDTH//2 - msg1.get_width()//2, 120))
    screen.blit(msg2, (WIDTH//2 - msg2.get_width()//2, 200))
    screen.blit(msg3, (WIDTH//2 - msg3.get_width()//2, 260))
    pygame.display.flip()
    pygame.time.wait(2000)

    # 5. Show sending phase
    screen.fill(GRAY)
    msg = font.render("Sending encrypted message...", True, CYAN)
    screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2))
    pygame.display.flip()
    pygame.time.wait(1200)

    # 6. Show receiver side
    screen.fill(GRAY)
    msg1 = font.render("Received encrypted message!", True, CYAN)
    msg2 = font.render(f"Ciphertext: {ciphertext}", True, WHITE)
    msg3 = font.render(f"SHA-256: {hash_val[:16]}...", True, YELLOW)
    screen.blit(msg1, (WIDTH//2 - msg1.get_width()//2, 120))
    screen.blit(msg2, (WIDTH//2 - msg2.get_width()//2, 200))
    screen.blit(msg3, (WIDTH//2 - msg3.get_width()//2, 260))
    pygame.display.flip()
    pygame.time.wait(2000)

    # 7. Decrypt and verify (animated)
    decrypted = ""
    for i in range(0, len(ciphertext), 2):
        a, b = ciphertext[i], ciphertext[i+1]
        row1, col1 = playfair_find(matrix, a)
        row2, col2 = playfair_find(matrix, b)
        if row1 == row2:
            dec_a = matrix[row1][(col1-1)%5]
            dec_b = matrix[row2][(col2-1)%5]
        elif col1 == col2:
            dec_a = matrix[(row1-1)%5][col1]
            dec_b = matrix[(row2-1)%5][col2]
        else:
            dec_a = matrix[row1][col2]
            dec_b = matrix[row2][col1]
        decrypted += dec_a + dec_b

        # Show the decryption step
        screen.fill(GRAY)
        msg1 = font.render("Decrypting message...", True, CYAN)
        msg2 = font.render(f"Ciphertext pair: {a+b}", True, WHITE)
        msg3 = font.render(f"Decrypted pair: {dec_a+dec_b}", True, YELLOW)
        msg4 = font.render(f"Decrypted so far: {decrypted}", True, GREEN)
        screen.blit(msg1, (WIDTH//2 - msg1.get_width()//2, 100))
        screen.blit(msg2, (WIDTH//2 - msg2.get_width()//2, 180))
        screen.blit(msg3, (WIDTH//2 - msg3.get_width()//2, 240))
        screen.blit(msg4, (WIDTH//2 - msg4.get_width()//2, 320))
        pygame.display.flip()
        pygame.time.wait(900)  # Pause for visibility

    new_hash = sha256_hash(decrypted)
    screen.fill(GRAY)
    msg1 = font.render("Verifying integrity...", True, YELLOW)
    msg2 = font.render(f"SHA-256: {new_hash[:16]}...", True, CYAN)
    screen.blit(msg1, (WIDTH//2 - msg1.get_width()//2, 200))
    screen.blit(msg2, (WIDTH//2 - msg2.get_width()//2, 260))
    pygame.display.flip()
    pygame.time.wait(2000)

    # 8. Show result and the final message
    screen.fill(GRAY)
    if new_hash == hash_val:
        msg = font.render("Integrity Verified! Message Secure.", True, GREEN)
        msg2 = font.render(f"Final Message: {decrypted}", True, CYAN)
    else:
        msg = font.render("Integrity Compromised! Message Tampered.", True, RED)
        msg2 = font.render(f"Decrypted: {decrypted}", True, CYAN)
    screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - 40))
    screen.blit(msg2, (WIDTH//2 - msg2.get_width()//2, HEIGHT//2 + 20))
    pygame.display.flip()
    pygame.time.wait(2500)
    return new_hash == hash_valcyber


if __name__ == "__main__":
    main()