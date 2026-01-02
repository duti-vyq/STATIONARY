
default redemption_score = 0
default reality_crack = 0
default trust_amyra = 0
default guilt_thief = 0
default forgiveness_daniel = 0

default saved_amyra = False
default saved_thief = False
default saved_daniel = False

default hope = 0
default despair = 0
default failed_any = False

define alex = Character("Alex")
define amyra = Character("Amyra")
define rowan = Character("Rowan")
define daniel = Character("Daniel")
define intercom = Character("Intercom Voice", color="#888888")


image apartment_morning_dull = Solid("#cfc6b9")
image map_metro_line_a = Solid("#999999")
image metro_entrance_routine = Solid("#bbbbbb")
image metro_platform_normal = Solid("#dddddd")
image metro_platform_clock = Solid("#cccccc")
image metro_platform_crowd = Solid("#d0d0d0")
image bench_side_light = Solid("#eeeeee")
image metro_shadowed_corner = Solid("#bfbfbf")
image metro_platform_void = Solid("#222222")
image metro_platform_light = Solid("#ffffff")
image train_arrival_unexpected = Solid("#00aa66")


# --- Start label ---
label start:
    # initialize / reset variables that should be reset each playthrough
    $ redemption_score = 0
    $ reality_crack = 0
    $ trust_amyra = 0
    $ guilt_thief = 0
    $ forgiveness_daniel = 0
    $ saved_amyra = False
    $ saved_thief = False
    $ saved_daniel = False
    $ hope = 0
    $ despair = 0
    $ failed_any = False

    play music "audio/ambient_dull_hum.mp3" loop
    scene apartment_morning_dull

    "The apartment is neat, clean, and perfectly beige. The alarm sounds at 07:00 AM."

    "Alex (internal):

Same time. Same coffee. Same destination. There is a strange, profound comfort in knowing exactly how the next eight hours will unfold. Deviation is unnecessary. The predictability is the point."

    show map_metro_line_a
    "Alex (internal):

Line A, Platform 3. The only line that matters. It always gets me there. It’s reliable. It’s predictable. And that predictability is my anchor."

    jump act_0_loop_initiation

# --- Act 0: Loop initiation ---
label act_0_loop_initiation:
    scene metro_entrance_routine
    "Alex walks, not runs, into the metro—a portrait of automated existence."

    scene metro_platform_normal
    "Alex (internal):

07:28 AM. Two minutes to Line A. The perfect amount of time to wait. Any shorter, and I'd feel rushed. Any longer, and I'd have to think."
    pause 1.0

    "The expected whoosh of approaching air never comes. A faint, sickening hum begins."

    scene metro_platform_clock
    "The station clock reads 07:30:00. The seconds hand ticks once, twitches violently, and then freezes. The air feels heavy."

    play sound "audio/train_missed_whoosh.mp3"
    intercom "\"We apologize for the delay. Line A is temporarily suspended. Please wait.\""

    "Alex (internal):

Suspended? That's not normal. Line A is the engine of the city. (Scans the platform, recognizing the others.) The faces... I’ve seen this exact disappointment before. I’ve felt this exact moment of inertia."

    # This is internal logic; not displayed. Increase reality_crack to progress the game.
    $ reality_crack += 2

    jump act_i_ordinary_wait

# --- Act I: The Ordinary Wait ---
label act_i_ordinary_wait:
    scene metro_platform_crowd
    "Alex (internal):

Another deviation. Can’t people just maintain order?"

    menu:
        "Help Amyra":
            $ trust_amyra += 1
            $ reality_crack += 1
            jump encounter_amyra_bag
        "Don’t help Amyra":
            jump ignore_amyra_bag

label ignore_amyra_bag:
    # If player chooses not to help, proceed through encounters but with consequences
    "You step back and do not help."
    $ despair += 1
    jump check_reality_crack_after_bag

label encounter_amyra_bag:
    # Help branch initial interaction
    "Alex:"
    "It’s alright. Are you always on Line A?"
    amyra "Yes. My fiancé insists I stick to the schedule. He says control is important now. (A nervous laugh.)"
    "Alex (internal):

Control. That's her lock. She's waiting for someone else to maintain her schedule, just like I wait for Line A."
    # trust_amyra already incremented by menu choice

label check_reality_crack_after_bag:
    # Continue with the normal flow; this label handles both branches
    scene metro_platform_normal
    "Alex (internal):

07:28 AM. Two minutes to Line A. The perfect amount of time to wait. Any shorter, and I'd feel rushed. Any longer, and I'd have to think."
    pause 1.0
    "The expected whoosh of approaching air never comes. A faint, sickening hum begins."

    scene metro_platform_clock
    play sound "audio/train_missed_whoosh.mp3"
    intercom "\"We apologize for the delay. Line A is temporarily suspended. Please wait.\""

    # Proceed to Act II if reality_crack threshold met
    if reality_crack >= 2:
        $ renpy.pause(0.5)
        jump act_ii_cracks_in_routine
    else:
        jump act_ii_cracks_in_routine

# --- Act II: Cracks in Routine (Encounters) ---
label act_ii_cracks_in_routine:
    play music "audio/ambient_low_hum.mp3" loop
    scene metro_platform_crowd
    "The platform is still, silent, waiting for Alex to make a move."

    # Amyra encounter
    jump encounter_amyra_full

label encounter_amyra_full:
    scene bench_side_light
    amyra "If I miss this train, I’ll be late. He’ll call. And if I stay quiet, he gets angry. But if I talk back, he says I’m making things difficult."

    alex "Amyra, your husband’s control is just a form of extreme routine. But if the routine causes this much stress, it’s broken. You need to choose a different line."

    amyra "I don't want a different line, I want to be worthy of this line. He took my choice. I'm waiting for the strength to take it back. My incentive is self-ownership."

    menu:
        "Tell me about the wooden bird.":
            $ trust_amyra += 1
            jump minigame_trust_fragments
        "Look, the platform lights are flickering.":
            $ despair += 1
            jump amyra_deflect

label amyra_deflect:
    "You deflect the conversation. Amyra looks away, wrapped in worry."
    jump after_amyra_encounter

label minigame_trust_fragments:
    # Fragment 1
    amyra "
Fragment 1 — career: 
\"he said my teaching career was 'too emotional.' he implied i’m too sensitive to be a good mother and a professional. should i have quit?\""
    menu:
        "He has a point; your health comes first.":
            $ trust_amyra -= 1
        "But did you want to quit? or did you just want to avoid the argument and the stress?":
            $ trust_amyra += 1
    # Fragment 2
    amyra "
Fragment 2 — communication: 
\"sometimes, when he’s angry, he just… stops talking for days. It makes the air toxic. I feel like I have to beg for a conversation.\""
    menu:
        "That kind of silence is louder than any shout. it’s a form of absolute control.":
            $ trust_amyra += 1
        "You need to confront him directly. he can't stonewall you.":
            $ trust_amyra -= 1
    # Fragment 3
    amyra "
Fragment 3 — self-blame: 
\"i feel so selfish, even thinking this. i must be the problem, right? a good wife wouldn't feel this trapped.\""
    menu:
        "Your value isn't dependent on your usefulness to him. it's about your survival and joy.":
            $ hope += 1
        "A mother needs to protect her child, even if it means leaving comfort behind.":
            pass

    # Check result
    if trust_amyra >= 2:
        amyra "(tears streaming, but a firm chin)
\"Love shouldn’t feel like fear… should it? it shouldn’t make me a ghost in my own life. that wooden bird—my mother said it was a reminder that you can always fly away from a cage, even if the cage is comfortable. He never wanted me to have the option to fly. the train is late… but i don’t have to stay stuck on this platform, waiting for a destination he chose for me. I can choose my own train. and my child's.\""
        $ saved_amyra = True
        $ redemption_score += 10
        $ hope += 1
        "(Amyra breathes easier, the tension leaving her shoulders.)"
    else:
        amyra "Maybe he’s right. Maybe I am too emotional. Maybe I'm just the problem. I shouldn't have wished for more."
        $ saved_amyra = False
        $ failed_any = True
        $ despair += 1

    jump after_amyra_encounter

label after_amyra_encounter:
    # Proceed to Rowan encounter
    jump encounter_rowan

label encounter_rowan:
    scene metro_shadowed_corner
    rowan "funny place to pretend you’re in control, Alex. The way you watched the pregnant woman. you think you know her story. You think you can fix it. Everyone here is waiting for a rescue, and you’re just a tourist."

    alex "You didn't steal the bag. You had the chance. You looked at the ultrasound and you hesitated."

    rowan "I guess I'm tired of the noise. the noise of my own stomach, the noise of my own failure. stealing a bag from a scared, pregnant woman? that’s not slipping through the cracks. that’s just being a bad guy. I'm trying to be ambiguous, not evil."

    menu:
        "The law is the law. You made your choice.":
            $ despair += 1
            jump rowan_outcome_no
        "Your moral scale is different, but you are aware of your choices.":
            $ guilt_thief += 1
            jump rowan_outcome_yes

label rowan_outcome_yes:
    rowan "didn’t think anyone would see me like that. not a walking moral failure, but a guy trying to make a hard choice. i’ve been running on this platform my whole life, thinking the next train would take me to a place where the rules made sense. but maybe the real train is the one you build yourself. thanks for the light."
    $ saved_thief = True
    $ redemption_score += 10
    $ hope += 1
    "(Rowan walks into the dim light. His outline wavers.)"
    jump encounter_daniel

label rowan_outcome_no:
    rowan "figures. the world is exactly what i expected. cold."
    $ saved_thief = False
    $ failed_any = True
    $ despair += 1
    "(Static consumes his figure rapidly.)"
    jump encounter_daniel

label encounter_daniel:
    scene metro_platform_void
    daniel "waiting orders. they’re coming. the train will carry the orders. i can’t leave my post."

    alex "You're not waiting for an order, Daniel. You're waiting for punishment. You are waiting for someone to tell you the war is over, and your duty to yourself has begun."

    daniel "I am waiting for absolution. I am the only one who survived the line I commanded them to hold. My courage kept me alive, but that survival became the heaviest guilt. If I get on a train, I am running away from their ghosts. I must stand here until I'm worthy of peace."

    jump minigame_memory_weight

label minigame_memory_weight:
    # Memory 1
    "Memory 1 — the order: a dark, muddy battlefield. Daniel's eyes are wide with shock. Daniel: \"I held the line.\""
    menu:
        "A leader's true burden is knowing when a mission is truly, honorably over.":
            $ forgiveness_daniel += 1
        "A soldier's first duty is to the mission. you followed orders.":
            $ despair += 1
    # Memory 2
    "Memory 2 — the ghosts: a ghostly hand reaches out, disappearing before Daniel can grab it. Daniel: \"I couldn't save them. I let go.\""
    menu:
        "You can't save the dead. your duty is to the living you became.":
            $ forgiveness_daniel += 1
        "You must honor their memory by standing guard here.":
            $ despair += 1
    # Memory 3
    "Memory 3 — the uniform: Daniel's reflection in a puddle, the uniform dissolving into civilian clothes. Daniel: \"I came home. I abandoned them.\""
    menu:
        "You didn't abandon them. you carried their memory out of the battle.":
            $ hope += 1
        "Your sacrifice is necessary until the guilt is purged.":
            $ despair += 1

    # Check result
    if forgiveness_daniel >= 1:
        daniel "(whispering) I did what I could. I was a man first. A soldier second. I can let go of the line."
        $ saved_daniel = True
        $ redemption_score += 10
        $ hope += 1
        "(Daniel straightens, the military rigidity replaced by simple weariness. He salutes once—a final respect to his past—and fades.)"
    else:
        daniel "then i stay. i failed. i accept the punishment."
        $ saved_daniel = False
        $ failed_any = True
        $ despair += 1
        "(Daniel fractures into cold, digital static.)"

    jump act_iii_station_reveals

# --- Act III: Climax & Endings ---
label act_iii_station_reveals:
    scene metro_platform_void
    "Alex (internal):

I spent so long trying to fix Line A, but Line A was never the problem. The problem was my willingness to let routine define me."

    # Determine ending based on redemption_score and saved flags
    if saved_amyra and saved_thief and saved_daniel:
        jump ending_good_train
    elif redemption_score >= 10 and redemption_score < 30:
        jump ending_bad_loop
    elif redemption_score < 10:
        jump ending_bad_oblivion
    else:
        # default fallback
        jump ending_bad_loop

label ending_bad_loop:
    scene metro_platform_normal
    play sound "audio/train_missed_whoosh.mp3"
    "The platform is bright again. The clocks are still frozen at 00:00. Other people stand apart, staring down the tunnel. Among them, a young woman clutches her bag tightly. A man in the corner tosses a coin. A soldier stands rigid by a pillar. You missed the train."
    "(The loop resets.)"
    menu:
        "Try again":
            jump start
        "Quit":
            return

label ending_bad_oblivion:
    scene white
    play sound "audio/static_loud.mp3"
    "You convinced them all to stay. You reinforced the cages they had built for themselves. The silence is complete. There is no train. There is no platform. There is nothing left to wait for. The only choice is the oblivion of the eternal wait."
    menu:
        "End game":
            return

label ending_good_train:
    scene metro_platform_light
    play music "audio/calm_release.mp3"
    "A distant rumble—not the distorted hum, but the clear, deep sound of heavy machinery approaching. The platform lights suddenly steady, the sickly yellow replaced by a warm, clean light."
    scene train_arrival_unexpected
    "Alex (internal):

I no longer need the comfort of the predictable line. I have created a new path."
    "An unfamiliar train arrives. It is colored bright Emerald Green—a sign of growth and difference. The destination sign flashes: LINE Z – POTENTIAL."
    "Redemption Complete. You successfully guided all three by breaking the logic of stagnation. The Final Train has arrived, not on the schedule you knew (Line A), but on the path you created (Line Z). The routine is now conscious choice."
    menu:
        "End game":
            return

# End of script
