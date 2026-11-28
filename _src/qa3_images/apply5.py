#!/usr/bin/env python3
"""Place the Drug Interactions and Side Effects vs ADR pictures (EN+BN) in the two noindex draft articles."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import apply3 as a3
a3.V = "?v=q5-20261128"
a3.ART.update({
 "di": dict(slug="drug-interactions-explained", dir="drug-interactions", pre="di", order=["cover","mech","types","outcome","checklist","list"], idx={1:"mech",2:"types",3:"outcome",4:"checklist",5:"list"}),
 "se": dict(slug="side-effects-vs-adverse-drug-reactions", dir="side-effects-adr", pre="se", order=["cover","se","adr","vs","warn","report"], idx={0:"se",1:"adr",3:"vs",5:"warn",6:"report"}),
})
EN, BN = a3.EN, a3.BN
def add(a, k, en, bn): EN[(a, k)] = en; BN[(a, k)] = bn
add("di","cover",("Grapefruit juice, coffee, a herb sprig, a warning triangle and two spilled pill bottles on a pharmacy counter, illustrating drug interactions.","A medicine can be affected by other medicines, food, drinks and herbal products. This is an AI-generated photo-style illustration."),
    ("ফার্মেসি কাউন্টারে জাম্বুরার রস, কফি, ভেষজ পাতা, সতর্কতা-চিহ্ন ও দুটি উল্টানো ওষুধের বোতল, যা ওষুধের ইন্টারঅ্যাকশন বোঝায়।","ওষুধ অন্য ওষুধ, খাবার, পানীয় ও ভেষজ পণ্যের দ্বারা প্রভাবিত হতে পারে। AI-তৈরি ছবি-ধাঁচের চিত্র।"))
add("di","mech",("Two panels: a liver with an enzyme, where a second medicine can raise or lower another's level, and a cell receptor where two medicines can strengthen or block each other.","Interactions may work by changing how a medicine is handled in the body (for example in the liver) or by acting together at the same target. AI-generated photo-style illustration."),
    ("দুটি প্যানেল: যকৃৎ ও এনজাইম, যেখানে একটি ওষুধ অন্যটির মাত্রা বাড়াতে বা কমাতে পারে; এবং কোষের রিসেপ্টর, যেখানে দুটি ওষুধ একে অপরকে বাড়াতে বা আটকাতে পারে।","ইন্টারঅ্যাকশন হতে পারে শরীরে ওষুধ কীভাবে সামলানো হয় (যেমন যকৃতে) তা বদলে, অথবা একই লক্ষ্যে একসঙ্গে কাজ করার মাধ্যমে। AI-তৈরি ছবি-ধাঁচের চিত্র।"))
add("di","types",("Four panels showing medicine with medicine, medicine with food or drink (grapefruit and coffee), medicine with a herbal product, and medicine with a health condition such as kidney disease.","Common types of interaction: medicine with medicine, food or drink, herbal products and health conditions. AI-generated photo-style illustration."),
    ("চারটি প্যানেলে ওষুধের সঙ্গে ওষুধ, ওষুধের সঙ্গে খাবার বা পানীয় (জাম্বুরা ও কফি), ওষুধের সঙ্গে ভেষজ পণ্য এবং ওষুধের সঙ্গে কিডনি রোগের মতো স্বাস্থ্য-অবস্থা।","ইন্টারঅ্যাকশনের সাধারণ ধরন: ওষুধের সঙ্গে ওষুধ, খাবার বা পানীয়, ভেষজ পণ্য ও স্বাস্থ্য-অবস্থা। AI-তৈরি ছবি-ধাঁচের চিত্র।"))
add("di","outcome",("Two medicines passing through interlocking gears, leading either to a stable blood pressure reading or to a warning reading.","Not every interaction is dangerous: some are minor and some need care or a change in plan from a doctor. AI-generated photo-style illustration."),
    ("দুটি ওষুধ পরস্পর-আটকানো গিয়ারের ভেতর দিয়ে গিয়ে হয় স্থিতিশীল রক্তচাপ, নয়তো সতর্কতা-সূচক রিডিং দেখাচ্ছে।","সব ইন্টারঅ্যাকশন বিপজ্জনক নয়: কিছু সামান্য, কিছুতে সতর্কতা বা চিকিৎসকের পরিকল্পনা বদলানো লাগতে পারে। AI-তৈরি ছবি-ধাঁচের চিত্র।"))
add("di","checklist",("A checklist on a clipboard for telling the doctor and pharmacist about all medicines, supplements and herbal products before starting a new one.","Tell your doctor and pharmacist about everything you take, including supplements and herbal products. AI-generated photo-style illustration."),
    ("ক্লিপবোর্ডে চেকলিস্ট: নতুন ওষুধ শুরুর আগে সব ওষুধ, সাপ্লিমেন্ট ও ভেষজ পণ্যের কথা চিকিৎসক ও ফার্মাসিস্টকে জানানো।","আপনি যা কিছু খান, সাপ্লিমেন্ট ও ভেষজ পণ্যসহ, সব চিকিৎসক ও ফার্মাসিস্টকে জানান। AI-তৈরি ছবি-ধাঁচের চিত্র।"))
add("di","list",("A printed 'My Medicine List' sheet for writing down each medicine, supplement and herbal product to carry to appointments.","Keep an up-to-date medicine list and bring it to every appointment. AI-generated photo-style illustration."),
    ("'আমার ওষুধের তালিকা' লেখা ছাপা শিট, যেখানে প্রতিটি ওষুধ, সাপ্লিমেন্ট ও ভেষজ পণ্য লিখে অ্যাপয়েন্টমেন্টে নেওয়া যায়।","ওষুধের হালনাগাদ তালিকা রাখুন এবং প্রতিটি অ্যাপয়েন্টমেন্টে সঙ্গে নিন। AI-তৈরি ছবি-ধাঁচের চিত্র।"))
add("se","cover",("A balance scale weighing a green shield with a tick against a red warning triangle with medicines, with common symptoms around it, illustrating benefit and risk.","Every medicine has benefits and risks; side effects and adverse drug reactions describe those risks differently. AI-generated photo-style illustration."),
    ("সবুজ টিক-চিহ্নের ঢাল ও লাল সতর্কতা-ত্রিভুজসহ ওষুধ মাপা একটি দাঁড়িপাল্লা, চারপাশে সাধারণ উপসর্গ; উপকার ও ঝুঁকির তুলনা বোঝায়।","প্রতিটি ওষুধেই উপকার ও ঝুঁকি আছে; সাইড ইফেক্ট ও অ্যাডভার্স ড্রাগ রিঅ্যাকশন এই ঝুঁকিকে ভিন্নভাবে বোঝায়। AI-তৈরি ছবি-ধাঁচের চিত্র।"))
add("se","se",("A man taking a pill with a glass of water, with a mild stomach upset on a small panel beside him.","Side effects are often mild and predictable, such as an upset stomach, but tell a professional if they bother you. AI-generated photo-style illustration."),
    ("পানির গ্লাসসহ ট্যাবলেট খাচ্ছেন একজন পুরুষ, পাশে ছোট প্যানেলে মৃদু পেটের অস্বস্তি।","সাইড ইফেক্ট প্রায়ই মৃদু ও আগে থেকে অনুমানযোগ্য, যেমন পেটের অস্বস্তি; তবে বিরক্ত করলে পেশাদারকে জানান। AI-তৈরি ছবি-ধাঁচের চিত্র।"))
add("se","adr",("An arm with a red skin rash and swelling around the eyes, shown as signs of a possible allergic-type reaction.","Some adverse reactions, such as rash or swelling, need prompt medical advice. AI-generated photo-style illustration."),
    ("হাতে লালচে ত্বকের র‍্যাশ ও চোখের চারপাশে ফোলা, যা সম্ভাব্য অ্যালার্জি-ধরনের প্রতিক্রিয়ার লক্ষণ হিসেবে দেখানো।","র‍্যাশ বা ফোলার মতো কিছু অ্যাডভার্স রিঅ্যাকশনে দ্রুত চিকিৎসা-পরামর্শ দরকার। AI-তৈরি ছবি-ধাঁচের চিত্র।"))
add("se","vs",("Side-by-side comparison: a man with a mild stomach upset on the left, and a man with facial swelling, a rash and a hand at his throat on the right.","Mild, expected side effects compared with a reaction that may be serious. Not every adverse reaction is an allergy. AI-generated photo-style illustration."),
    ("পাশাপাশি তুলনা: বাঁদিকে মৃদু পেটের অস্বস্তিতে একজন পুরুষ, ডানদিকে মুখ ফোলা, র‍্যাশ ও গলায় হাত দেওয়া একজন পুরুষ।","মৃদু, প্রত্যাশিত সাইড ইফেক্টের সঙ্গে সম্ভাব্য গুরুতর প্রতিক্রিয়ার তুলনা। সব অ্যাডভার্স রিঅ্যাকশনই অ্যালার্জি নয়। AI-তৈরি ছবি-ধাঁচের চিত্র।"))
add("se","warn",("A doctor holding up a hand in a stop gesture beside panels of swollen eyes, rash, throat tightness, chest discomfort and breathing difficulty, with an ambulance heading to a hospital.","Severe signs such as swelling, trouble breathing or chest pain need urgent medical help. AI-generated photo-style illustration."),
    ("থামার ভঙ্গিতে হাত তোলা চিকিৎসক, পাশে ফোলা চোখ, র‍্যাশ, গলা চেপে ধরা, বুকে অস্বস্তি ও শ্বাসকষ্টের প্যানেল, এবং হাসপাতালের দিকে অ্যাম্বুলেন্স।","ফোলা, শ্বাসকষ্ট বা বুকে ব্যথার মতো গুরুতর লক্ষণে জরুরি চিকিৎসা-সহায়তা নিন। AI-তৈরি ছবি-ধাঁচের চিত্র।"))
add("se","report",("A phone screen showing an 'ADR Report' form with fields for the medicine, the reaction and the patient.","Suspected adverse reactions can be reported through the national reporting system. AI-generated photo-style illustration."),
    ("ফোনের পর্দায় 'ADR Report' ফর্ম, যেখানে ওষুধ, প্রতিক্রিয়া ও রোগীর তথ্যের ঘর আছে।","সন্দেহজনক অ্যাডভার্স রিঅ্যাকশন জাতীয় রিপোর্টিং ব্যবস্থার মাধ্যমে জানানো যায়। AI-তৈরি ছবি-ধাঁচের চিত্র।"))
if __name__ == "__main__":
    for a in sys.argv[1:] or ("di", "se"):
        for lg in ("en", "bn"): a3.process(a, lg)
