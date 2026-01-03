# --- INITIALIZATION & SETUP ---

# 1. AUDIO CHANNELS
init python:
    renpy.music.register_channel("glitch_sfx", mixer="sfx", loop=True)

# 2. TRANSFORMS & VISUAL EFFECTS
transform glitch_shake:
    linear 0.05 xoffset -10
    linear 0.05 xoffset 10
    linear 0.05 xoffset -10
    linear 0.05 xoffset 10
    linear 0.05 xoffset 0

transform notify_appear:
    xalign 0.5 yalign 0.2 alpha 0.0
    linear 0.5 alpha 1.0 yalign 0.15
    pause 1.5
    linear 0.5 alpha 0.0

# 3. IMAGES (BACKGROUNDS)
# Using Placeholder("bg") creates a generic background placeholder
image apartment_morning_dull = Placeholder("bg", text="Apartment Morning")
image map_metro_line_a = Placeholder("bg", text="Map Line A")
image metro_entrance_routine = Placeholder("bg", text="Metro Entrance")
image metro_platform_normal = Placeholder("bg", text="Metro Platform")
image metro_platform_clock = Placeholder("bg", text="Clock 7:30")
image metro_platform_crowd = Placeholder("bg", text="Platform Crowd")
image bench_side_light = Placeholder("bg", text="Bench Light")
image metro_shadowed_corner = Placeholder("bg", text="Shadowed Corner")
image metro_platform_void = Placeholder("bg", text="Platform Void")
image metro_platform_light = Placeholder("bg", text="Platform Light")
image train_arrival_unexpected = Placeholder("bg", text="Green Train")
image white = Solid("#ffffff")

image static_overlay:
    Solid("#000000") 
    alpha 0.3
    block:
        linear 0.1 alpha 0.1
        linear 0.1 alpha 0.4
        repeat

# 4. CHARACTER SPRITES (PLACEHOLDERS)
# This uses Ren'Py's built-in placeholder system. 
# It creates a silhouette with the text name on it.

image alex = Placeholder("boy", text="Alex")
image amyra = Placeholder("girl", text="Amyra")
image rowan = Placeholder("boy", text="Rowan")
image daniel = Placeholder("boy", text="Daniel")

# 5. VARIABLES
default persistent.loop_count = 0

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

# 6. CHARACTERS
# We link the character to the image tag so "show alex" works naturally.
define alex = Character("Alex", color="#ffffff", image="alex")

# Internal Monologue: No image argument, so it won't auto-show a sprite.
define alex_inner = Character("Alex", color="#ffffff", what_italic=True, what_color="#cccccc")

define amyra = Character("Amyra", color="#98fb98", image="amyra") 
define rowan = Character("Rowan", color="#d3d3d3", image="rowan") 
define daniel = Character("Daniel", color="#add8e6", image="daniel") 
define intercom = Character("Intercom Voice", color="#ff6666") 


# --- CUSTOM SCREENS (UI) ---

screen stat_overlay():
    frame:
        xalign 0.02 yalign 0.02
        background Solid("#00000088")
        padding (10, 10)
        vbox:
            spacing 5
            text "Redemption: [redemption_score]" size 18 color "#fff"
            text "Reality Crack: [reality_crack]" size 18 color "#aaa"
            
            if trust_amyra > 0 and not saved_amyra:
                null height 10
                text "Amyra's Trust" size 16 color "#ffcccc"
                bar value trust_amyra range 3 xsize 200 ysize 20

screen karma_notify(amount):
    text "+ [amount] Redemption Karma" at notify_appear size 40 color "#ffffcc" outlines [(2, "#000", 0, 0)]

# --- HELPER LABELS ---

label trigger_reality_crack_effect(amount=1):
    $ reality_crack += amount
    show static_overlay
    play sound "audio/static_loud.mp3" 
    show layer master at glitch_shake
    with vpunch
    "The air hums violently." 
    hide static_overlay
    return

label award_karma(amount):
    $ redemption_score += amount
    show screen karma_notify(amount)
    play sound "audio/calm_release.mp3" volume 0.5 
    return


# --- START OF GAME ---

label start:
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

    show screen stat_overlay

    play music "audio/ambient_dull_hum.mp3" fadein 2.0 loop
    scene apartment_morning_dull

    if persistent.loop_count == 0:
        "The apartment is neat, clean, and perfectly beige. The alarm sounds at 07:00 AM."
        alex_inner "Same time. Same coffee. Same destination. There is a strange, profound comfort in knowing exactly how the next eight hours will unfold."
    else:
        "The apartment is neat. It is always neat. The alarm sounds at 07:00 AM... again."
        alex_inner "Same time. Same coffee. Same destination. Loop [persistent.loop_count]."

    alex_inner "Deviation is unnecessary. The predictability is the point."

    show map_metro_line_a
    
    alex_inner "Line A, Platform 3. The only line that matters. It always gets me there. It's reliable. It's predictable."
    alex_inner "And that predictability is my anchor."

    jump act_0_loop_initiation

# --- ACT 0: LOOP INITIATION ---

label act_0_loop_initiation:
    scene metro_entrance_routine
    "Alex walks, not runs, into the metro—a portrait of automated existence."

    scene metro_platform_normal
    
    alex_inner "07:28 AM. Two minutes to Line A. The perfect amount of time to wait. Any shorter, and I'd feel rushed."
    alex_inner "Any longer, and I'd have to think."
    pause 1.0

    stop music fadeout 1.0
    play glitch_sfx "audio/ambient_low_hum.mp3" fadein 0.5 loop

    "The expected whoosh of approaching air never comes. A faint, sickening hum begins."

    scene metro_platform_clock
    "The station clock reads 07:30:00. The seconds hand ticks once, twitches violently, and then freezes."
    
    call trigger_reality_crack_effect(0) from _call_trigger_reality_crack_effect

    "The air feels heavy."

    play sound "audio/train_missed_whoosh.mp3"
    
    intercom "We apologize for the delay. Line A is temporarily suspended. Please wait."

    alex_inner "Suspended? That's not normal. Line A is the engine of the city."
    "(Scans the platform, recognizing the others.)"
    alex_inner "The faces... I've seen this exact disappointment before. I've felt this exact moment of inertia."

    call trigger_reality_crack_effect(2) from _call_trigger_reality_crack_effect_1

    jump act_i_ordinary_wait

# --- ACT I: THE ORDINARY WAIT ---

label act_i_ordinary_wait:
    scene metro_platform_crowd
    alex_inner "Another deviation. Can't people just maintain order?"

    menu:
        "Help Amyra":
            $ trust_amyra += 1
            $ reality_crack += 1
            jump encounter_amyra_bag
        "Don't help Amyra":
            jump ignore_amyra_bag

label ignore_amyra_bag:
    "You step back and do not help."
    $ despair += 1
    jump check_reality_crack_after_bag

label encounter_amyra_bag:
    # Because Alex talks first, we show him.
    show alex at left with dissolve
    
    alex "It's all right. Are you always on Line A?"

    # Amyra responds, so we show her.
    show amyra at right with dissolve
    amyra "Yes. My fiancé insists I stick to the schedule. He says control is important now. (A nervous laugh.)"
    
    # Alex thinks, no visual change needed
    alex_inner "Control. That's her lock. She's waiting for someone else to maintain her schedule, just like I wait for Line A."

    # End of scene - hide them
    hide alex
    hide amyra
    with dissolve

label check_reality_crack_after_bag:
    scene metro_platform_normal
    alex_inner "07:28 AM. Two minutes to Line A. The perfect amount of time to wait. Any shorter, and I'd feel rushed."
    alex_inner "Any longer, and I'd have to think."
    
    pause 1.0
    "The expected whoosh of approaching air never comes. A faint, sickening hum begins."

    scene metro_platform_clock
    play sound "audio/train_missed_whoosh.mp3"
    intercom "We apologize for the delay. Line A is temporarily suspended. Please wait."

    if reality_crack >= 2:
        jump act_ii_cracks_in_routine
    else:
        $ reality_crack = 2
        jump act_ii_cracks_in_routine

# --- ACT II: CRACKS IN ROUTINE ---

label act_ii_cracks_in_routine:
    play glitch_sfx "audio/ambient_low_hum.mp3" loop
    
    scene metro_platform_crowd
    "The platform is still, silent, waiting for Alex to make a move."

    jump encounter_amyra_full

label encounter_amyra_full:
    scene bench_side_light
    
    # Show Amyra first as she is speaking first in this block
    show amyra at center with dissolve

    amyra "If I miss this train, I'll be late. He'll call. And if I stay quiet, he gets angry."
    amyra "But if I talk back, he says I'm making things difficult."

    # Alex enters the conversation
    show alex at left with dissolve
    alex "Amyra, your husband's control is just a form of extreme routine. But if the routine causes this much stress, it's broken."
    alex "You need to choose a different line."

    amyra "I don't want a different line. I want to be worthy of this line. He took my choice."
    amyra "I'm waiting for the strength to take it back. My incentive is self-ownership."

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
    
    amyra "Fragment 1 — Career: \"He said my teaching career was 'too emotional.' He implied I'm too sensitive to be a good mother and a professional. Should I have quit?\""
    menu:
        "He has a point; your health comes first.":
            $ trust_amyra -= 1
            "She shrinks back."
        "But did you want to quit? Or did you just want to avoid the argument and the stress?":
            $ trust_amyra += 1
            "She nods slowly."

    amyra "Fragment 2 — Communication: \"Sometimes, when he's angry, he just… stops talking for days. It makes the air toxic. I feel like I have to beg for a conversation.\""
    menu:
        "That kind of silence is louder than any shout. It's a form of absolute control.":
            $ trust_amyra += 1
            "Her eyes widen in realization."
        "You need to confront him directly. He can't stonewall you.":
            $ trust_amyra -= 1
            "She shakes her head, fearful."

    amyra "Fragment 3 — Self-Blame: \"I feel so selfish, even thinking this. I must be the problem, right? A good wife wouldn't feel this trapped.\""
    menu:
        "Your value isn't dependent on your usefulness to him. It's about your survival and joy.":
            $ hope += 1
        "A mother needs to protect her child, even if it means leaving comfort behind.":
            pass

    if trust_amyra >= 2:
        
        amyra "(Tears streaming, but a firm chin) \"Love shouldn’t feel like fear… should it? It shouldn’t make me a ghost in my own life.\""
        amyra "\"That wooden bird—my mother said it was a reminder that you can always fly away from a cage, even if the cage is comfortable.\""
        amyra "\"He never wanted me to have the option to fly. The train is late… but I don’t have to stay stuck on this platform, waiting for a destination he chose for me. I can choose my own train. And my child's.\""
        
        $ saved_amyra = True
        $ hope += 1
        call award_karma(10) from _call_award_karma

        "(Amyra breathes easier, the tension leaving her shoulders.)"
        
        # She fades away
        hide amyra with dissolve
    else:
        amyra "Maybe he's right. Maybe I am too emotional. Maybe I'm just the problem. I shouldn't have wished for more."
        $ saved_amyra = False
        $ failed_any = True
        $ despair += 1
        
        hide amyra with dissolve

    jump after_amyra_encounter

label after_amyra_encounter:
    # Clean up sprites
    hide alex
    hide amyra
    jump encounter_rowan

label encounter_rowan:
    scene metro_shadowed_corner
    
    show rowan at center with dissolve
    # Show Alex again because we are in a new scene
    show alex at left with dissolve

    rowan "Funny place to pretend you’re in control, Alex. The way you watched the pregnant woman. You think you know her story. You think you can fix it."
    rowan "Everyone here is waiting for a rescue, and you’re just a tourist."

    alex "You didn't steal the bag. You had the chance. You looked at the ultrasound and you hesitated."

    rowan "I guess I'm tired of the noise. The noise of my own stomach, the noise of my own failure."
    rowan "Stealing a bag from a scared, pregnant woman? That’s not slipping through the cracks. That’s just being a bad guy."
    rowan "I'm trying to be ambiguous, not evil."

    alex_inner "He's not justifying the theft; he's trying to rationalize his existence. He seeks validation for his vulnerability."
    alex_inner "I need to acknowledge the humanity behind the choices."

    menu:
        "The law is the law. You made your choice.":
            $ despair += 1
            jump rowan_outcome_no
        "Your moral scale is different, but you are aware of your choices.":
            $ guilt_thief += 1
            jump rowan_outcome_yes

label rowan_outcome_yes:
    
    rowan "I didn't think anyone would see me like that. Not a walking moral failure, but a guy trying to make a hard choice."
    rowan "I've been running on this platform my whole life, thinking the next train would take me to a place where the rules made sense."
    rowan "But maybe the real train is the one you build yourself. Thanks for the light."
    
    $ saved_thief = True
    $ hope += 1
    call award_karma(10) from _call_award_karma_1
    
    "(Rowan walks into the dim light. His outline wavers.)"
    hide rowan with dissolve
    jump encounter_daniel

label rowan_outcome_no:
    rowan "Figures. The world is exactly what I expected. Cold."
    $ saved_thief = False
    $ failed_any = True
    $ despair += 1
    "(Static consumes his figure rapidly.)"
    hide rowan with dissolve
    jump encounter_daniel

label encounter_daniel:
    hide alex
    hide rowan
    
    scene metro_platform_void
    
    show daniel at center with dissolve
    show alex at left with dissolve
    
    daniel "Waiting orders. They’re coming. The train will carry the orders. I can’t leave my post."

    alex "You're not waiting for an order, Daniel. You're waiting for punishment."
    alex "You are waiting for someone to tell you the war is over, and your duty to yourself has begun."

    daniel "I am waiting for absolution. I am the only one who survived the line I commanded them to hold."
    daniel "My courage kept me alive, but that survival became the heaviest guilt. If I get on a train, I am running away from their ghosts."
    daniel "I must stand here until I'm worthy of peace."

    jump minigame_memory_weight

label minigame_memory_weight:
    "Memory 1 — The Order: A dark, muddy battlefield. Daniel's eyes are wide with shock. Daniel: \"I held the line.\""
    menu:
        "A leader's true burden is knowing when a mission is truly, honorably over.":
            $ forgiveness_daniel += 1
        "A soldier's first duty is to the mission. You followed orders.":
            $ despair += 1

    "Memory 2 — The Ghosts: A ghostly hand reaches out, disappearing before Daniel can grab it. Daniel: \"I couldn't save them. I let go.\""
    menu:
        "You can't save the dead. Your duty is to the living you became.":
            $ forgiveness_daniel += 1
        "You must honor their memory by standing guard here.":
            $ despair += 1

    "Memory 3 — The Uniform: Daniel's reflection in a puddle, the uniform dissolving into civilian clothes. Daniel: \"I came home. I abandoned them.\""
    menu:
        "You didn't abandon them. You carried their memory out of the battle.":
            $ hope += 1
        "Your sacrifice is necessary until the guilt is purged.":
            $ despair += 1

    if forgiveness_daniel >= 1:
        
        daniel "(Whispering) I did what I could. I was a man first. A soldier second. I can let go of the line."
        $ saved_daniel = True
        $ hope += 1
        call award_karma(10) from _call_award_karma_2
        
        "(Daniel straightens, the military rigidity replaced by simple weariness. He salutes once—a final respect to his past—and fades.)"
        hide daniel with dissolve
    else:
        daniel "Then I stay. I failed. I accept the punishment."
        $ saved_daniel = False
        $ failed_any = True
        $ despair += 1
        "(Daniel fractures into cold, digital static.)"
        hide daniel with dissolve

    jump act_iii_station_reveals

# --- ACT III: CLIMAX & ENDINGS ---

label act_iii_station_reveals:
    hide alex
    hide daniel
    
    scene metro_platform_void
    show alex at center with dissolve
    
    alex_inner "I spent so long trying to fix Line A, but Line A was never the problem."
    alex_inner "The problem was my willingness to let routine define me."

    if saved_amyra and saved_thief and saved_daniel: 
        jump ending_good_train
    elif redemption_score >= 10 and redemption_score < 30:
        jump ending_bad_loop
    elif redemption_score < 10:
        jump ending_bad_oblivion
    else:
        jump ending_bad_loop

label ending_bad_loop:
    scene metro_platform_normal
    play sound "audio/train_missed_whoosh.mp3"
    "The platform is bright again. The clocks are still frozen at 00:00. Other people stand apart, staring down the tunnel."
    "Among them, a young woman clutches her bag tightly. A man in the corner tosses a coin. A soldier stands rigid by a pillar."
    "You missed the train."
    
    $ persistent.loop_count += 1
    "(The loop resets.)"
    
    menu:
        "Try again":
            jump start
        "Quit":
            return

label ending_bad_oblivion:
    scene white
    play sound "audio/static_loud.mp3"
    "You convinced them all to stay. You reinforced the cages they had built for themselves. The silence is complete."
    "There is no train. There is no platform. There is nothing left to wait for."
    "The only choice is the oblivion of the eternal wait."
    menu:
        "End game":
            return

label ending_good_train:
    stop glitch_sfx fadeout 2.0
    play music "audio/calm_release.mp3" fadein 2.0
    
    scene metro_platform_light
    
    "A distant rumble—not the distorted hum, but the clear, deep sound of heavy machinery approaching."
    "The platform lights suddenly steady, the sickly yellow replaced by a warm, clean light."
    
    scene train_arrival_unexpected
    
    alex_inner "I no longer need the comfort of the predictable line. I have created a new path."
    
    "An unfamiliar train arrives. It is colored bright Emerald Green—a sign of growth and difference."
    "The destination sign flashes: LINE Z – POTENTIAL."
    
    "Redemption Complete. You successfully guided all three by breaking the logic of stagnation."
    "The Final Train has arrived, not on the schedule you knew (Line A), but on the path you created (Line Z)."
    "The routine is now conscious choice."
    
    menu:
        "End game":
            return