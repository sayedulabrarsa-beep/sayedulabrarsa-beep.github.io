#!/usr/bin/env python3
"""Rebuild the picture sections of the EN + BN heartburn/GERD pages with the 25 new pictures,
add the interactive layer, and update head / schema / sitemap. Safe to re-run (works from a marker)."""
import re, pathlib, json
R = pathlib.Path(__file__).resolve().parent.parent.parent
IMG = "/assets/img/blog/reflux/"
SITE = "https://sayedulabrar.site"
WH = {"W": (1600, 900), "S": (1200, 1200), "T": (1200, 800)}

def pic(name, k, alt, cls="", lazy=True, ext="webp"):
    w, h = WH[k]
    return (f'<img src="{IMG}{name}.{ext}" alt="{alt}" width="{w}" height="{h}" decoding="async"'
            f'{" loading=\"lazy\"" if lazy else ""}{(" class=\"" + cls + "\"") if cls else ""}>')

# ---------------------------------------------------------------- language data
EN = dict(
 lang="en", hero_alt="Illustration of a torso showing acid reflux rising from the stomach into the food pipe, with the valve between them.",
 trio_label="Tap a term to compare:", trio=[("Heartburn", "The feeling: a burning sensation in the chest."),
   ("Acid reflux", "The event: stomach contents flowing back up into the food pipe (esophagus)."),
   ("GERD", "The repeating condition: reflux that keeps coming back and causes troublesome symptoms or problems.")],
 valve_alt="Close-up illustration of the lower esophageal sphincter (LES) closed between the food pipe and the stomach.",
 valve_cap="Illustration: the LES closed, like a one-way door. The picture shows the closed door; use the buttons to read what happens when it relaxes.",
 valve_chips=[("closed", "Door closed"), ("open", "Door relaxed")],
 valve_txt={"closed": "<p><b>Normal:</b> food goes down and the door (LES) closes behind it, so stomach contents stay in the stomach.</p>",
            "open": "<p><b>Reflux:</b> if the door relaxes at the wrong time or does not close well, stomach contents can move back up. The food pipe lining handles acid less well, so it may feel like a burn.</p>"},
 story_alts=["Illustration: Hasan eats a late, heavy dinner and then feels a burning chest.",
             "Illustration: Hasan with a lighter dinner and a short walk afterwards.",
             "Illustration: a warning sign, with a burning throat and a clock.",
             "Illustration: Hasan visits a doctor."],
 story=[("A late, heavy dinner", "Hasan works late. Most nights he eats a heavy, oily dinner at 11 pm and lies down right away. For weeks he wakes with a burning chest and a sour taste in his mouth. First he blames the tea."),
        ("A lighter routine", "He eats a smaller dinner earlier, stays upright for a few hours afterwards, and raises the head end of his bed. The burning eases."),
        ("A warning sign", "One week, though, he notices pain when swallowing."),
        ("He sees a doctor", "This time he does not wait. He books an appointment with a doctor.")],
 step_word="Step", back="← Back", nxt="Next →", dot="Go to step {n}",
 story_cap="Hasan’s week in four pictures: changing habits helps, but warning signs still need medical attention.",
 trig=[("trigger-spicy", "T", "Spicy food", "Red chillies, a spicy food."), ("trigger-late-dinner", "T", "Late dinner", "A late dinner served at night."),
       ("trigger-fried", "T", "Fried and fatty food", "Fried, fatty food."), ("trigger-fizzy", "S", "Fizzy drinks", "A glass of fizzy cola."),
       ("trigger-tea-coffee", "T", "Tea and coffee", "A cup of tea and a cup of coffee."), ("trigger-chocolate", "T", "Chocolate", "Pieces of chocolate.")],
 trig_hint="Tap the cards that you notice in your own life. Your triggers may differ from other people’s.",
 trig_none="You have not marked any card yet. Tap the ones you notice.", trig_some="You marked {n} possible trigger(s). A food and symptom diary can help you confirm them.",
 trig_more="All common triggers, in words:",
 slides=[("habit-smaller-meal", "W", "Eat smaller meals", "Smaller portions instead of a few very large meals.", "Illustration: a small, balanced portion on a plate."),
         ("habit-three-hours", "W", "Finish eating 2 to 3 hours before lying down", "Leave about 2 to 3 hours between your last meal and lying down. The “3 hours” in the picture is an example.", "Illustration: an hourglass and a clock showing 3 hours between eating and lying down."),
         ("habit-upright", "W", "Stay upright after eating", "Sit or walk gently after a meal instead of lying down at once.", "Illustration: a person sitting upright after a meal."),
         ("habit-raised-bed", "W", "Raise the head end of your bed", "Use sturdy blocks or a wedge, not extra pillows alone.", "Illustration: a bed with a wedge raising the head end."),
         ("habit-activity", "W", "Stay active and keep a healthy weight", "Keeping a healthy weight is one of the habits that may help.", "Illustration: walking shoes, a water bottle and a towel for gentle activity."),
         ("habit-loose-clothing", "W", "Wear loose clothing around the waist", "Tight clothes around the waist can be a trigger.", "Illustration: a man in loose, comfortable clothes.")],
 slide_word="Habit picture {n} of {t}", slide_note="The pictures show six of the seven habits. Tick the ones you already follow below.",
 check_label="My habit checklist: tick the ones you already follow", check_tpl="{n} of {t} habits ticked",
 warn_chips=[("green", "Green · Self-care"), ("amber", "Amber · See a doctor soon"), ("red", "Red · Emergency")],
 warn_alts={"green": "Illustration for mild, occasional heartburn where self-care may be enough.",
            "amber": "Illustration for symptoms that keep coming back and need a doctor soon.",
            "red": "Illustration for emergency warning signs that need urgent medical help."},
 warn_cap="Pictures are visual aids only. The lists in each panel are the full guidance. If in doubt, get help.",
 doctor_alt="Illustration of a doctor explaining reflux care to a patient.",
 quiz=dict(ok="Correct!", no="Not quite. The correct answer is now highlighted.", score="You got {n} of {t}",
           all="Well done. Remember: warning signs always need a doctor.",
           some="Good try. Read the sections above again, and remember that warning signs need a doctor.", again="Try again"),
 quiz_alt="Illustration of a check mark in a speech bubble.",
 myth_alt="Illustration contrasting common myths with facts about acid reflux.", myth_cap="Five common myths and the facts are in the table below.",
 take_alt="Illustration of pillars representing the key takeaways.",
 modified_tag='Updated <time datetime="2026-11-23">23 November 2026</time>',
 og_alt="Heartburn vs acid reflux vs GERD: a torso illustration of reflux, with the article title and author.",
 sm_titles=None,
)
BN = dict(
 lang="bn", hero_alt="একটি দেহকাণ্ডের চিত্র: পাকস্থলী থেকে খাদ্যনালিতে অ্যাসিড রিফ্লাক্স উঠছে, মাঝখানে ভাল্ভ।",
 trio_label="তুলনা দেখতে একটি শব্দে চাপ দিন:", trio=[("বুক জ্বালাপোড়া", "অনুভূতি: বুকে জ্বালা করা।"),
   ("অ্যাসিড রিফ্লাক্স", "ঘটনা: পাকস্থলীর ভেতরের জিনিস খাদ্যনালিতে উঠে আসা।"),
   ("GERD", "বারবার ফিরে আসা অবস্থা: রিফ্লাক্স যখন বারবার ফিরে আসে এবং কষ্টদায়ক উপসর্গ বা সমস্যা তৈরি করে।")],
 valve_alt="খাদ্যনালি ও পাকস্থলীর মাঝখানে বন্ধ অবস্থায় লোয়ার ইসোফেজিয়াল স্ফিংটার (LES)-এর ক্লোজ-আপ চিত্র।",
 valve_cap="চিত্র: LES বন্ধ অবস্থায়, একমুখী দরজার মতো। ছবিতে বন্ধ দরজা দেখানো হয়েছে; ঢিলা হলে কী হয় তা পড়তে বোতামে চাপ দিন।",
 valve_chips=[("closed", "দরজা বন্ধ"), ("open", "দরজা ঢিলা")],
 valve_txt={"closed": "<p><b>স্বাভাবিক:</b> খাবার নিচে যায় আর দরজা (LES) পেছনে বন্ধ হয়ে যায়, তাই পাকস্থলীর জিনিস পাকস্থলীতেই থাকে।</p>",
            "open": "<p><b>রিফ্লাক্স:</b> দরজা ভুল সময়ে ঢিলা হলে বা ঠিকমতো বন্ধ না হলে পাকস্থলীর জিনিস ওপরে উঠে আসতে পারে। খাদ্যনালির আস্তরণ অ্যাসিড তেমন সহ্য করতে পারে না, তাই জ্বালা অনুভূত হতে পারে।</p>"},
 story_alts=["চিত্র: হাসান দেরিতে ভারী রাতের খাবার খাচ্ছে, তারপর বুকে জ্বালা অনুভব করছে।",
             "চিত্র: হাসানের হালকা রাতের খাবার ও খাওয়ার পর অল্প হাঁটা।",
             "চিত্র: একটি বিপদ-সংকেত, গলায় জ্বালা ও একটি ঘড়ি।",
             "চিত্র: হাসান ডাক্তারের কাছে যাচ্ছে।"],
 story=[("দেরিতে ভারী রাতের খাবার", "হাসান দেরি করে কাজ করে। বেশির ভাগ রাতে সে রাত ১১টায় ভারী, তেলযুক্ত খাবার খায় এবং খেয়েই শুয়ে পড়ে। কয়েক সপ্তাহ ধরে সে বুকে জ্বালা আর মুখে টক স্বাদ নিয়ে জেগে ওঠে। প্রথমে সে দোষ দেয় চায়ের।"),
        ("হালকা নতুন রুটিন", "সে আগে আগে অল্প করে রাতের খাবার খায়, খাওয়ার পর কয়েক ঘণ্টা সোজা হয়ে থাকে এবং বিছানার মাথার দিকটা একটু উঁচু করে নেয়। জ্বালা কমে আসে।"),
        ("একটি বিপদ-সংকেত", "এক সপ্তাহে সে খেয়াল করে, গিলতে ব্যথা হচ্ছে।"),
        ("ডাক্তার দেখানো", "এবার সে অপেক্ষা করে না। ডাক্তারের অ্যাপয়েন্টমেন্ট নেয়।")],
 step_word="ধাপ", back="← আগের", nxt="পরের →", dot="{n} নম্বর ধাপে যান",
 story_cap="চারটি ছবিতে হাসানের সপ্তাহ: অভ্যাস বদল সাহায্য করে, তবে বিপদ-সংকেতে চিকিৎসকের পরামর্শ জরুরি।",
 trig=[("trigger-spicy", "T", "ঝাল খাবার", "লাল মরিচ, ঝাল খাবারের প্রতীক।"), ("trigger-late-dinner", "T", "দেরিতে রাতের খাবার", "রাতে পরিবেশন করা দেরির খাবার।"),
       ("trigger-fried", "T", "ভাজা ও চর্বিযুক্ত খাবার", "ভাজা, চর্বিযুক্ত খাবার।"), ("trigger-fizzy", "S", "কোমল পানীয়", "এক গ্লাস গ্যাসযুক্ত কোলা।"),
       ("trigger-tea-coffee", "T", "চা ও কফি", "এক কাপ চা ও এক কাপ কফি।"), ("trigger-chocolate", "T", "চকলেট", "চকলেটের টুকরো।")],
 trig_hint="নিজের জীবনে যেগুলো খেয়াল করেছেন, সেই কার্ডগুলোতে চাপ দিন। আপনার ট্রিগার অন্যদের মতো নাও হতে পারে।",
 trig_none="এখনও কোনো কার্ড চিহ্নিত করেননি। যেগুলো খেয়াল করেছেন সেগুলোতে চাপ দিন।", trig_some="আপনি {n}টি সম্ভাব্য ট্রিগার চিহ্নিত করেছেন। খাবার ও উপসর্গের ডায়েরি রাখলে নিশ্চিত হতে সুবিধা হয়।",
 trig_more="সাধারণ ট্রিগারগুলো কথায়:",
 slides=[("habit-smaller-meal", "W", "অল্প অল্প করে খান", "একবারে অনেক বেশি না খেয়ে ছোট ছোট খাবার খান।", "চিত্র: প্লেটে অল্প ও সুষম খাবার।"),
         ("habit-three-hours-bn", "W", "শোয়ার ২ থেকে ৩ ঘণ্টা আগে খাওয়া শেষ করুন", "শেষ খাবার আর শোয়ার মাঝখানে প্রায় ২ থেকে ৩ ঘণ্টা ফাঁক রাখুন। ছবির “৩ ঘণ্টা” একটি উদাহরণ।", "চিত্র: বালুঘড়ি ও ঘড়ি, খাওয়া আর শোয়ার মাঝে ৩ ঘণ্টার ফাঁক।"),
         ("habit-upright", "W", "খাওয়ার পর সোজা থাকুন", "খাওয়ার পরপরই না শুয়ে বসে থাকুন বা হালকা হাঁটুন।", "চিত্র: খাওয়ার পর সোজা হয়ে বসে থাকা একজন মানুষ।"),
         ("habit-raised-bed", "W", "বিছানার মাথার দিক উঁচু করুন", "মজবুত ব্লক বা ওয়েজ ব্যবহার করুন, শুধু বাড়তি বালিশ নয়।", "চিত্র: ওয়েজ দিয়ে মাথার দিক উঁচু করা বিছানা।"),
         ("habit-activity", "W", "সক্রিয় থাকুন, ওজন স্বাস্থ্যকর রাখুন", "স্বাস্থ্যকর ওজন বজায় রাখা সাহায্য করতে পারে এমন অভ্যাসগুলোর একটি।", "চিত্র: হালকা শারীরিক সক্রিয়তার জন্য হাঁটার জুতা, পানির বোতল ও তোয়ালে।"),
         ("habit-loose-clothing", "W", "কোমরে ঢিলেঢালা পোশাক পরুন", "কোমরে আঁটসাঁট পোশাক ট্রিগার হতে পারে।", "চিত্র: ঢিলেঢালা আরামদায়ক পোশাকে একজন পুরুষ।")],
 slide_word="অভ্যাসের ছবি {n}/{t}", slide_note="ছবিতে ৭টির মধ্যে ৬টি অভ্যাস দেখানো হয়েছে। নিচে যেগুলো আপনি আগে থেকেই মানেন সেগুলোতে টিক দিন।",
 check_label="আমার অভ্যাসের তালিকা: যেগুলো মানেন সেগুলোতে টিক দিন", check_tpl="{t}টির মধ্যে {n}টিতে টিক",
 warn_chips=[("green", "সবুজ · নিজে যত্ন"), ("amber", "হলুদ · শিগগির ডাক্তার"), ("red", "লাল · জরুরি")],
 warn_alts={"green": "চিত্র: মাঝেমধ্যে হালকা বুক জ্বালা, যেখানে নিজে যত্ন নেওয়াই যথেষ্ট হতে পারে।",
            "amber": "চিত্র: যে উপসর্গ বারবার ফিরে আসে এবং শিগগির ডাক্তার দেখানো দরকার।",
            "red": "চিত্র: জরুরি বিপদ-সংকেত, যেখানে এখনই চিকিৎসা নিতে হবে।"},
 warn_cap="ছবিগুলো শুধু বোঝার সুবিধার জন্য। প্রতিটি ট্যাবের তালিকাই পূর্ণ নির্দেশনা। সন্দেহ হলে সাহায্য নিন।",
 doctor_alt="চিত্র: একজন ডাক্তার রোগীকে রিফ্লাক্সের যত্ন বোঝাচ্ছেন।",
 quiz=dict(ok="সঠিক!", no="ঠিক হয়নি। সঠিক উত্তরটি এখন চিহ্নিত করা আছে।", score="আপনি {t}টির মধ্যে {n}টি সঠিক করেছেন",
           all="চমৎকার! মনে রাখবেন, বিপদ-সংকেত থাকলে ডাক্তার দেখানো জরুরি।",
           some="ভালো চেষ্টা। ওপরের অংশগুলো আবার পড়ুন, আর মনে রাখুন বিপদ-সংকেতে ডাক্তার দেখাতে হয়।", again="আবার চেষ্টা করুন"),
 quiz_alt="চিত্র: কথার বুদবুদে একটি টিক চিহ্ন।",
 myth_alt="চিত্র: অ্যাসিড রিফ্লাক্স নিয়ে ভুল ধারণা ও আসল তথ্যের তুলনা।", myth_cap="পাঁচটি ভুল ধারণা ও আসল তথ্য নিচের সারণিতে আছে।",
 take_alt="চিত্র: মূল কথাগুলো বোঝাতে কয়েকটি স্তম্ভ।",
 modified_tag='হালনাগাদ: <time datetime="2026-11-23">২৩ নভেম্বর ২০২৬</time>',
 og_alt="বুক জ্বালাপোড়া, অ্যাসিড রিফ্লাক্স ও GERD: রিফ্লাক্সের দেহচিত্র, সঙ্গে নিবন্ধের শিরোনাম ও লেখকের নাম।",
)
EN["sm"] = {"hero.webp": "Torso illustration of acid reflux rising from the stomach into the food pipe.",
  "valve.webp": EN["valve_alt"], "story-1-late-dinner.webp": EN["story_alts"][0], "story-2-lighter-routine.webp": EN["story_alts"][1],
  "story-3-warning-signs.webp": EN["story_alts"][2], "story-4-doctor-visit.webp": EN["story_alts"][3],
  "warning-green.webp": EN["warn_alts"]["green"], "warning-amber.webp": EN["warn_alts"]["amber"], "warning-red.webp": EN["warn_alts"]["red"],
  "doctor.webp": EN["doctor_alt"], "myth-vs-fact.webp": EN["myth_alt"], "key-takeaways.webp": EN["take_alt"]}
BN["sm"] = {"hero.webp": "খাদ্যনালিতে অ্যাসিড রিফ্লাক্স ওঠার দেহচিত্র।",
  "valve.webp": BN["valve_alt"], "story-1-late-dinner.webp": BN["story_alts"][0], "story-2-lighter-routine.webp": BN["story_alts"][1],
  "story-3-warning-signs.webp": BN["story_alts"][2], "story-4-doctor-visit.webp": BN["story_alts"][3],
  "warning-green.webp": BN["warn_alts"]["green"], "warning-amber.webp": BN["warn_alts"]["amber"], "warning-red.webp": BN["warn_alts"]["red"],
  "doctor.webp": BN["doctor_alt"], "myth-vs-fact.webp": BN["myth_alt"], "key-takeaways.webp": BN["take_alt"]}

def dg(L, n):
    n = str(n)
    return n.translate(str.maketrans('0123456789', '০১২৩৪৫৬৭৮৯')) if L['lang'] == 'bn' else n

def esc(s): return s.replace("&", "&amp;").replace('"', "&quot;")

# ---------------------------------------------------------------- builders
def b_trio(L):
    chips = "".join(f'<button type="button" class="rx-chip" role="tab" data-rx-chip="t{i}" aria-selected="{"true" if i==0 else "false"}">{t}</button>' for i, (t, _) in enumerate(L["trio"]))
    panels = "".join(f'<div class="rx-panel" role="tabpanel" data-rx-panel="t{i}"><p><b>{t}</b> — {d}</p></div>' for i, (t, d) in enumerate(L["trio"]))
    return f'<div class="rx rx-trio rx-reveal" data-rx-switch><p class="rx-cap" style="margin:0 0 8px"><b>{L["trio_label"]}</b></p><div class="rx-chips" role="tablist">{chips}</div>{panels}</div>'

def b_valve(L):
    chips = "".join(f'<button type="button" class="rx-chip" role="tab" data-rx-chip="{k}" aria-selected="{"true" if i==0 else "false"}">{t}</button>' for i, (k, t) in enumerate(L["valve_chips"]))
    panels = "".join(f'<div class="rx-panel" role="tabpanel" data-rx-panel="{k}">{L["valve_txt"][k]}</div>' for k, _ in L["valve_chips"])
    return (f'<div class="rx rx-card rx-reveal" data-rx-switch><div class="rx-valve-grid"><figure class="rx-valve-fig" style="margin:0" data-state="closed">'
            f'{pic("valve","W",esc(L["valve_alt"]))}<figcaption class="rx-cap">{L["valve_cap"]}</figcaption></figure>'
            f'<div><div class="rx-chips" role="tablist">{chips}</div>{panels}</div></div></div>')

def b_story(L):
    names = ["story-1-late-dinner", "story-2-lighter-routine", "story-3-warning-signs", "story-4-doctor-visit"]
    steps = ""
    for i, n in enumerate(names):
        t, d = L["story"][i]
        steps += (f'<div class="rx-story-stage" data-rx-step>{pic(n,"S",esc(L["story_alts"][i]))}'
                  f'<div class="rx-step"><span class="rx-num" aria-hidden="true">{dg(L,i+1)}</span><h3>{L["step_word"]} {dg(L,i+1)}: {t}</h3><p>{d}</p></div></div>')
    dots = "".join(f'<button type="button" class="rx-dot" aria-label="{L["dot"].format(n=dg(L,i+1))}"></button>' for i in range(4))
    return (f'<div class="rx rx-card rx-reveal" data-rx-steps role="group" aria-roledescription="carousel" aria-label="{esc(L["story_cap"])}">{steps}'
            f'<div class="rx-nav"><button type="button" class="rx-btn" data-rx-prev>{L["back"]}</button><div class="rx-dots">{dots}</div>'
            f'<button type="button" class="rx-btn" data-rx-next>{L["nxt"]}</button></div><p class="rx-cap" data-rx-live aria-live="polite" style="margin-top:8px">{""}</p>'
            f'<p class="rx-cap">{L["story_cap"]}</p></div>')

def b_triggers(L):
    cards = ""
    for n, k, lab, alt in L["trig"]:
        cards += f'<button type="button" class="rx-trig" aria-pressed="false">{pic(n,k,esc(alt))}<span>{lab}</span></button>'
    return (f'<div class="rx rx-card rx-reveal" data-rx-triggers data-none="{esc(L["trig_none"])}" data-some="{esc(L["trig_some"])}">'
            f'<p class="rx-cap" style="margin:0 0 10px"><b>{L["trig_hint"]}</b></p><div class="rx-grid">{cards}</div><p class="rx-tally" data-rx-tally aria-live="polite">{L["trig_none"]}</p></div>')

def b_habits(L, ol_items):
    slides = ""
    nslide = len(L["slides"])
    for i, (n, k, t, d, alt) in enumerate(L["slides"]):
        slides += (f'<div class="rx-slide" data-rx-step>{pic(n,k,esc(alt))}<div><p class="rx-count">{L["slide_word"].format(n=dg(L,i+1),t=dg(L,nslide))}</p>'
                   f'<h3>{t}</h3><p>{d}</p></div></div>')
    dots = "".join(f'<button type="button" class="rx-dot" aria-label="{L["dot"].format(n=dg(L,i+1))}"></button>' for i in range(nslide))
    car = (f'<div class="rx rx-card rx-reveal" data-rx-steps role="group" aria-roledescription="carousel" aria-label="{esc(L["slide_note"])}">{slides}'
           f'<div class="rx-nav"><button type="button" class="rx-btn" data-rx-prev>{L["back"]}</button><div class="rx-dots">{dots}</div>'
           f'<button type="button" class="rx-btn" data-rx-next>{L["nxt"]}</button></div><p class="rx-cap" data-rx-live aria-live="polite" style="margin-top:8px"></p><p class="rx-cap">{L["slide_note"]}</p></div>')
    lis = "".join(f'<li><label><input type="checkbox"><span>{x}</span></label></li>' for x in ol_items)
    chk = (f'<div class="rx rx-card"><p style="margin:0 0 6px"><b>{L["check_label"]}</b></p><ol class="rx-check" data-rx-checklist data-tpl="{esc(L["check_tpl"])}">{lis}</ol>'
           f'<div class="rx-bar" aria-hidden="true"><i></i></div><p class="rx-progress" data-rx-progress aria-live="polite"></p></div>')
    return car + chk

def b_warning(L, blocks):
    chips = "".join(f'<button type="button" class="rx-chip {k}" role="tab" data-rx-chip="{k}" aria-selected="{"true" if i==0 else "false"}">{t}</button>' for i, (k, t) in enumerate(L["warn_chips"]))
    panels = ""
    for k, _ in L["warn_chips"]:
        panels += (f'<div class="rx-panel rx-warn-grid" role="tabpanel" data-rx-panel="{k}">{pic("warning-"+k,"W",esc(L["warn_alts"][k]))}{blocks[k]}</div>')
    return (f'<div class="rx rx-card rx-reveal" data-rx-switch><div class="rx-chips" role="tablist">{chips}</div>{panels}<p class="rx-cap">{L["warn_cap"]}</p></div>')

def b_result(L):
    q = L["quiz"]
    return (f'<div class="rx-result rx-card" hidden>{pic("quiz-check","W",esc(L["quiz_alt"]))}<div><h3 data-rx-score></h3>'
            f'<p data-rx-msg></p><button type="button" class="rx-btn" data-rx-again>{q["again"]}</button></div></div>')

# ---------------------------------------------------------------- page edit
def section(html, sid):
    m = re.search(rf'<section id="{sid}">.*?</section>', html, re.S)
    assert m, sid
    return m

def sub_section(html, sid, fn):
    m = section(html, sid)
    return html[:m.start()] + fn(m.group(0)) + html[m.end():]

def process(path, L, social, title_prefix):
    p = R / path
    h = p.read_text(encoding="utf-8")
    first = "rx-reveal" not in h
    assert first or True
    # undo a previous run is not supported: this script is meant to run once on the original markup
    assert "reflux-interactive.css" not in h, "already applied"
    # head: css
    h = h.replace('<link rel="stylesheet" href="/assets/nav-pill.css?v=sa-20261122">', '<link rel="stylesheet" href="/assets/nav-pill.css?v=sa-20261122"><link rel="stylesheet" href="/assets/reflux-interactive.css?v=rx-20261123">', 1)
    assert "reflux-interactive.css" in h
    # hero
    h = re.sub(r'<figure class="hero-visual"><img src="/assets/img/blog/heartburn-gerd-hero\.webp"[^>]*alt="[^"]*" width="1600" height="900">',
               lambda m: f'<figure class="hero-visual"><img src="{IMG}hero.webp" fetchpriority="high" decoding="async" alt="{esc(L["hero_alt"])}" width="1600" height="900">', h, count=1)
    assert f'{IMG}hero.webp' in h
    # difference: add trio
    def f_diff(s): return s.replace("</section>", b_trio(L) + "</section>")
    h = sub_section(h, "difference", f_diff)
    # door
    def f_door(s):
        s = re.sub(r'<figure class="article-visual infographic">.*?</figure>', "", s, flags=re.S)
        return s.replace("</section>", b_valve(L) + "</section>")
    h = sub_section(h, "door", f_door)
    # story: keep heading and the final bold line; replace paragraphs + figure
    def f_story(s):
        learned = re.search(r'<p><b>[^<]*</b>[^<]*</p>', s).group(0)
        head = re.search(r'<h2>.*?</h2>', s).group(0)
        return f'<section id="story">{head}{b_story(L)}{learned}</section>'
    h = sub_section(h, "story", f_story)
    # triggers: intro paragraph, cards, then list in words (inside details-free list)
    def f_trig(s):
        head = re.search(r'<h2>.*?</h2>', s).group(0)
        intro = re.search(r'</h2>(<p>.*?</p>)', s, re.S).group(1)
        ul = re.search(r'<ul>.*?</ul>', s, re.S).group(0)
        return f'<section id="triggers">{head}{intro}{b_triggers(L)}<h3>{L["trig_more"]}</h3>{ul}</section>'
    h = sub_section(h, "triggers", f_trig)
    # habits
    def f_hab(s):
        head = re.search(r'<h2>.*?</h2>', s).group(0)
        items = re.findall(r'<li>(.*?)</li>', re.search(r'<ol>.*?</ol>', s, re.S).group(0), re.S)
        tail = re.search(r'</ol>(<p>.*?</p>)', s, re.S).group(1)
        return f'<section id="habits">{head}{b_habits(L, items)}{tail}</section>'
    h = sub_section(h, "habits", f_hab)
    # warning
    def f_warn(s):
        head = re.search(r'<h2>.*?</h2>', s).group(0)
        blocks = {}
        for k in ("green", "amber", "red"):
            m = re.search(rf'<div class="warning {k}">.*?</div>', s, re.S)
            blocks[k] = m.group(0)
        return f'<section id="warning">{head}{b_warning(L, blocks)}</section>'
    h = sub_section(h, "warning", f_warn)
    # doctors
    def f_doc(s):
        head = re.search(r'<h2>.*?</h2>', s).group(0)
        para = re.search(r'</h2>(<p>.*?</p>)', s, re.S).group(1)
        return f'<section id="doctors">{head}<div class="rx-split rx-reveal">{para}{pic("doctor","W",esc(L["doctor_alt"]))}</div></section>'
    h = sub_section(h, "doctors", f_doc)
    # quiz
    q = L["quiz"]
    def f_quiz(s):
        s = s.replace('<section id="quiz">', f'<section id="quiz" data-ok="{esc(q["ok"])}" data-no="{esc(q["no"])}" data-score="{esc(q["score"])}" data-all="{esc(q["all"])}" data-some="{esc(q["some"])}">', 1)
        return s.replace("</section>", b_result(L) + "</section>")
    h = sub_section(h, "quiz", f_quiz)
    # myths
    def f_myth(s):
        fig = f'<figure class="rx-fig rx-reveal">{pic("myth-vs-fact","W",esc(L["myth_alt"]))}<figcaption class="caption">{L["myth_cap"]}</figcaption></figure>'
        return s.replace('<div class="table-wrap">', fig + '<div class="table-wrap">', 1)
    h = sub_section(h, "myths", f_myth)
    # takeaways
    h = h.replace('<div class="takeaways">', f'<div class="takeaways"><figure class="rx-fig">{pic("key-takeaways","W",esc(L["take_alt"]))}</figure>', 1)
    assert "key-takeaways.webp" in h
    # replace old quiz script
    h, n = re.subn(r'<script>\s*\(function\(\)\{var q=document\.querySelectorAll\(\'\.quiz button\'\).*?</script>', '<script src="/assets/reflux-interactive.js?v=rx-20261123" defer></script>', h, flags=re.S)
    assert n == 1, "quiz script"
    # head social + dates
    soc = f"{SITE}{IMG}reflux-social-{L['lang']}.jpg"
    h = h.replace("https://sayedulabrar.site/assets/img/blog/heartburn-gerd-hero.jpg\">", soc + '">')  # og/twitter image meta content
    h = re.sub(r'(<meta property="og:image:alt" content=")[^"]*(")', lambda m: m.group(1) + esc(L["og_alt"]) + m.group(2), h)
    h = re.sub(r'(<meta property="og:image:width" content=")\d+(")', r'\g<1>1200\2', h)
    h = re.sub(r'(<meta property="og:image:height" content=")\d+(")', r'\g<1>630\2', h)
    h = re.sub(r'(<meta property="article:modified_time" content=")[^"]*(")', r'\g<1>2026-11-23\2', h)
    h = re.sub(r'"dateModified": "[^"]*"', '"dateModified": "2026-11-23"', h)
    # byline
    if L["lang"] == "en":
        h = h.replace('Updated <time datetime="2026-11-08">8 November 2026</time>', L["modified_tag"])
    else:
        h = re.sub(r'(প্রকাশ: <time datetime="2026-10-30">৩০ অক্টোবর ২০২৬</time>)', r'\1 · ' + L["modified_tag"], h, count=1)
    assert "2026-11-23" in h
    p.write_text(h, encoding="utf-8")
    return h

def schema_images(L, lang):
    """Replace the ImageObject list in the Article JSON-LD."""
    items = [("reflux-social-%s.jpg" % lang, L["og_alt"])] + [(k, v) for k, v in L["sm"].items()]
    return items

if __name__ == "__main__":
    for path, L in (("blog/heartburn-vs-acid-reflux-vs-gerd/index.html", EN), ("blog/heartburn-vs-acid-reflux-vs-gerd-bangla/index.html", BN)):
        process(path, L, None, None)
        print("ok", path)
