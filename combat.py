import random

def roll_d20():
    return random.randint(1, 20)

def attack(attacker, defender):
    attack_roll = roll_d20() + attacker.stats['str']
    defense_roll = roll_d20() + defender.stats['def']
    damage = max(0, attack_roll - defense_roll)
    defender.stats['hp'] -= damage
    print(f"Attacked! {defender.stats['hp']} HP remaining for defender")