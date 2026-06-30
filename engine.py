# engine.py — knowledge-based system with forward chaining

# Knowledge base. Two kinds of rules:
#   - derivation rules  -> conclude a NEW FACT  (key "add_fact")
#   - action rules      -> conclude a DECISION  (key "action")
rules = [
    # --- Derivation rules (conclude intermediate facts) ---
    {"name": "assess_critical",  "priority": 100,
     "if": lambda f: f.get("enemy_hp", 100) < 20,
     "add_fact": ("is_critical", True)},

    {"name": "assess_surrounded", "priority": 100,
     "if": lambda f: f.get("enemies_nearby", 0) >= 2,
     "add_fact": ("is_surrounded", True)},

    {"name": "assess_trapped", "priority": 95,
     "if": lambda f: f.get("is_critical") and f.get("is_surrounded"),  # depends on DERIVED facts -> chaining
     "add_fact": ("must_escape", True)},

    # --- Action rules (conclude a decision) ---
    {"name": "retreat",     "priority": 80,
     "if": lambda f: f.get("must_escape") and f.get("escape_route_open"),
     "action": "RETREAT"},

    {"name": "call_backup", "priority": 80,
     "if": lambda f: f.get("must_escape") and not f.get("escape_route_open"),
     "action": "CALL_BACKUP"},

    {"name": "take_cover",  "priority": 60,
     "if": lambda f: f.get("is_critical") and not f.get("must_escape"),
     "action": "TAKE_COVER"},

    {"name": "attack",      "priority": 10,
     "if": lambda f: f.get("player_distance", 999) < 10,
     "action": "ATTACK"},
]


def infer(initial_facts):
    facts = dict(initial_facts)   # work on a copy
    derived = {}
    trace = []

    # PHASE 1 — Forward chaining: apply derivation rules until nothing new is concluded
    changed = True
    while changed:
        changed = False
        for r in rules:
            if "add_fact" in r and r["if"](facts):
                key, value = r["add_fact"]
                if facts.get(key) != value:          # only if it's actually new
                    facts[key] = value
                    derived[key] = value
                    trace.append(f"[{r['name']}] condition held  ->  {key} = {value}")
                    changed = True

    # PHASE 2 — Decision: highest-priority action rule that fires
    candidates = [r for r in rules if "action" in r and r["if"](facts)]
    if not candidates:
        return {"decision": "HOLD", "fired_rule": None, "derived_facts": derived, "trace": trace}

    winner = max(candidates, key=lambda r: r["priority"])
    trace.append(f"[{winner['name']}]  ->  decision: {winner['action']}")
    return {"decision": winner["action"], "fired_rule": winner["name"],
            "derived_facts": derived, "trace": trace}


if __name__ == "__main__":
    facts = {
        "enemy_hp": 15,
        "enemies_nearby": 3,
        "player_distance": 6,
        "escape_route_open": False,
    }
    result = infer(facts)
    print("Reasoning chain:")
    for step in result["trace"]:
        print("   ", step)
    print("Derived facts:", result["derived_facts"])
    print("Final decision:", result["decision"], "(rule:", result["fired_rule"], ")")