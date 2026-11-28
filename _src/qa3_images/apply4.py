#!/usr/bin/env python3
"""Place the Dosage Forms, IR/SR/EC and Routes pictures (EN+BN) in the three noindex draft articles."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import apply3 as a3
a3.V = "?v=q4-20261128"
a3.ART.update({
 "df": dict(slug="different-types-of-medicine-dosage-forms", dir="dosage-forms", pre="df", order=["cover", "solid", "liquid", "topical"], idx={1: "solid", 2: "liquid", 3: "topical"}),
 "sr": dict(slug="immediate-sustained-enteric-coated-medicines", dir="release-designs", pre="sr", order=["cover", "ir", "sr", "ec", "compare", "abbr", "crush", "checklist"], idx={0: "ir", 1: "sr", 2: "ec", 3: "compare", 4: "abbr", 5: "crush", 6: "checklist"}),
 "rt": dict(slug="routes-of-drug-administration", dir="routes-of-administration", pre="rt", order=["cover", "oral", "inj", "inh", "local", "speed"], idx={1: "oral", 2: "inj", 3: "inh", 4: "local", 5: "speed"}),
})
EN, BN = a3.EN, a3.BN
def add(a, k, en, bn): EN[(a, k)] = en; BN[(a, k)] = bn
add("df", "cover", ("Assorted medicine dosage forms on a bright pharmacy counter: bottles of syrup, a nasal spray, an inhaler, tablets, capsules, powder and a cream tube.", "Medicine dosage forms: tablets, capsules, liquids, creams, sprays and inhalers, and why the form matters."),
    ("উজ্জ্বল ফার্মেসি কাউন্টারে ওষুধের নানা রূপ: সিরাপের বোতল, নাকের স্প্রে, ইনহেলার, ট্যাবলেট, ক্যাপসুল, পাউডার ও ক্রিমের টিউব।", "ওষুধের ডোজ ফর্ম: ট্যাবলেট, ক্যাপসুল, তরল, ক্রিম, স্প্রে ও ইনহেলার, এবং রূপ কেন গুরুত্বপূর্ণ।"))
add("df", "solid", ("An amber pill bottle, blister packs of blue capsules and pink tablets, and loose tablets and capsules beside a plant.", "Solid oral dosage forms include tablets and capsules, often packed in blisters or bottles."),
    ("একটি অ্যাম্বার পিল বোতল, নীল ক্যাপসুল ও গোলাপি ট্যাবলেটের ব্লিস্টার প্যাক এবং পাশে ছড়ানো ট্যাবলেট ও ক্যাপসুল।", "কঠিন মুখে-খাওয়া ডোজ ফর্মের মধ্যে ট্যাবলেট ও ক্যাপসুল আছে, যা প্রায়ই ব্লিস্টার বা বোতলে থাকে।"))
add("df", "liquid", ("Bottles of orange, red and pink liquid medicine with a measuring cup, an oral syringe and a dropper bottle.", "Liquid medicines such as syrups, drops and suspensions should be measured with the device supplied."),
    ("কমলা, লাল ও গোলাপি তরল ওষুধের বোতল, সঙ্গে মাপার কাপ, ওরাল সিরিঞ্জ ও ড্রপার বোতল।", "সিরাপ, ড্রপ ও সাসপেনশনের মতো তরল ওষুধ সঙ্গে থাকা মাপক দিয়ে মাপতে হয়।"))
add("df", "topical", ("A cream jar, tubes of cream and gel, a nasal spray, eye-drop bottle, an inhaler and a skin patch on a marble surface.", "Topical and inhaled forms include creams, ointments, patches, nasal sprays and inhalers."),
    ("মার্বেল টেবিলে ক্রিমের জার, ক্রিম ও জেলের টিউব, নাকের স্প্রে, আই-ড্রপের বোতল, ইনহেলার ও ত্বকের প্যাচ।", "ত্বকে ও শ্বাসে ব্যবহারের রূপের মধ্যে ক্রিম, মলম, প্যাচ, নাকের স্প্রে ও ইনহেলার আছে।"))
add("sr", "cover", ("An hourglass beside a stomach illustration with a dissolving tablet, with a tablet, a capsule and a softgel on the table.", "Release designs control how and when a medicine is released in the body over time."),
    ("পাকস্থলীর চিত্রের পাশে বালুঘড়ি, যেখানে একটি ট্যাবলেট গলছে; টেবিলে একটি ট্যাবলেট, ক্যাপসুল ও সফটজেল।", "রিলিজ ডিজাইন ঠিক করে সময়ের সঙ্গে শরীরে ওষুধ কীভাবে ও কখন ছাড়বে।"))
add("sr", "checklist", ("A clipboard checklist with four ticked icons (medicine, clock, water, doctor) beside a glass of water, a pill bottle and a blister strip.", "A safe-use checklist: check the product and form, take at the stated time and ask a doctor or pharmacist if unsure."),
    ("চারটি টিক-চিহ্নসহ ক্লিপবোর্ড চেকলিস্ট (ওষুধ, ঘড়ি, পানি, চিকিৎসক), পাশে পানির গ্লাস, পিল বোতল ও ব্লিস্টার স্ট্রিপ।", "নিরাপদ ব্যবহারের তালিকা: পণ্য ও রূপ দেখুন, লেখা সময়ে সেবন করুন এবং সন্দেহ হলে চিকিৎসক বা ফার্মাসিস্টকে জিজ্ঞাসা করুন।"))
add("sr", "compare", ("Three glowing release-profile dials above a plain tablet, a pellet-filled capsule and a coated pink tablet.", "Immediate-release, sustained-release and enteric-coated medicines are designed to release in different ways."),
    ("একটি সাধারণ ট্যাবলেট, দানাভরা ক্যাপসুল ও আবরণযুক্ত গোলাপি ট্যাবলেটের উপরে তিনটি আলোকিত রিলিজ-প্রোফাইল ডায়াল।", "ইমিডিয়েট-রিলিজ, সাস্টেইনড-রিলিজ ও এন্টেরিক-কোটেড ওষুধ ভিন্ন ভিন্ন ভাবে ছাড়ার নকশায় তৈরি।"))
add("sr", "ir", ("A broken white tablet with a fast release-curve dial pointing to a stomach illustration.", "Immediate-release medicines are designed to release the drug soon after they are swallowed."),
    ("একটি ভাঙা সাদা ট্যাবলেট ও দ্রুত রিলিজ-কার্ভের ডায়াল, যা পাকস্থলীর চিত্রের দিকে নির্দেশ করছে।", "ইমিডিয়েট-রিলিজ ওষুধ গিলে ফেলার অল্পক্ষণ পরেই ওষুধ ছাড়ার নকশায় তৈরি।"))
add("sr", "sr", ("A capsule filled with coated pellets and a cut-away capsule with arrows, beside a slow release-curve dial and a stomach illustration.", "Sustained-release medicines are designed to release the drug gradually over a longer time."),
    ("আবরণযুক্ত দানাভরা ক্যাপসুল ও তীর-চিহ্নসহ কাটা ক্যাপসুল, পাশে ধীর রিলিজ-কার্ভের ডায়াল ও পাকস্থলীর চিত্র।", "সাস্টেইনড-রিলিজ ওষুধ দীর্ঘ সময় ধরে ধীরে ধীরে ওষুধ ছাড়ার নকশায় তৈরি।"))
add("sr", "ec", ("A pink coated tablet cut open beside a shield-over-stomach icon, with a crossed-out tablet in the stomach and a ticked tablet in the intestine.", "An enteric coating is designed to resist stomach acid so the medicine releases further along the gut."),
    ("কেটে দেখানো গোলাপি আবরণযুক্ত ট্যাবলেট, পাশে পাকস্থলী-সুরক্ষার ঢাল; ট্যাবলেট পাকস্থলী পেরিয়ে অন্ত্রে পৌঁছানো দেখানো হয়েছে।", "এন্টেরিক আবরণ পাকস্থলীর অ্যাসিড সামলে অন্ত্রের দিকে গিয়ে ওষুধ ছাড়ার নকশায় তৈরি।"))
add("sr", "abbr", ("Three stacked medicine boxes labelled IR, SR and EC beside a notepad explaining the abbreviations, with a blister strip and tablets.", "Common abbreviations on medicine packs: IR is immediate-release, SR is sustained-release and EC is enteric-coated."),
    ("IR, SR ও EC লেখা তিনটি ওষুধের বাক্স একটির উপর একটি, পাশে সংক্ষেপগুলোর ব্যাখ্যাসহ নোটপ্যাড, সঙ্গে ব্লিস্টার স্ট্রিপ ও ট্যাবলেট।", "ওষুধের প্যাকের সাধারণ সংক্ষেপ: IR মানে ইমিডিয়েট-রিলিজ, SR মানে সাস্টেইনড-রিলিজ ও EC মানে এন্টেরিক-কোটেড।"))
add("sr", "crush", ("A coated tablet cut open with a tick, beside a mortar of crushed pink powder marked with a red cross.", "Modified-release tablets should not be crushed, split or chewed unless the label or a professional says it is safe."),
    ("সবুজ টিকসহ কেটে দেখানো আবরণযুক্ত ট্যাবলেট, পাশে লাল ক্রস-চিহ্নসহ হামানদিস্তায় গুঁড়ো গোলাপি পাউডার।", "লেবেল বা পেশাদার নিরাপদ বললে তবেই মডিফাইড-রিলিজ ট্যাবলেট গুঁড়ো, ভাঙা বা চিবানো যাবে।"))
add("rt", "cover", ("A translucent human body figure surrounded by circles showing oral, nasal, inhaled, eye, injection, skin and patch routes of drug administration.", "Routes of drug administration: how medicine enters the body by mouth, injection, inhalation, skin and other sites."),
    ("স্বচ্ছ মানবদেহের চিত্রকে ঘিরে বৃত্তে মুখ, নাক, ইনহেলার, চোখ, ইনজেকশন, ত্বক ও প্যাচের মাধ্যমে ওষুধ প্রয়োগের পথ।", "ওষুধ প্রয়োগের পথ: মুখ, ইনজেকশন, শ্বাস, ত্বক ও অন্যান্য স্থান দিয়ে ওষুধ কীভাবে শরীরে ঢোকে।"))
add("rt", "oral", ("A man swallowing a tablet with a stomach and gut illustration, beside a close-up of a tablet under the tongue and the bloodstream.", "Oral routes: swallowed medicines pass through the gut, while under-the-tongue forms are absorbed in the mouth."),
    ("একজন পুরুষ ট্যাবলেট গিলছেন, সঙ্গে পাকস্থলী ও অন্ত্রের চিত্র; পাশে জিহ্বার নিচে ট্যাবলেট ও রক্তপ্রবাহের ক্লোজ-আপ।", "মুখের পথ: গিলে খাওয়া ওষুধ পরিপাকতন্ত্র দিয়ে যায়, আর জিহ্বার নিচের ওষুধ মুখেই শোষিত হয়।"))
add("rt", "inj", ("A gloved hand giving an intramuscular injection in an upper arm, beside an intravenous drip bag and a cannula in a hand.", "Parenteral routes include intramuscular injections and intravenous infusions given by trained staff."),
    ("গ্লাভস পরা হাত বাহুতে মাংসপেশিতে ইনজেকশন দিচ্ছে, পাশে শিরায় ড্রিপ ব্যাগ ও হাতে ক্যানুলা।", "প্যারেন্টেরাল পথের মধ্যে প্রশিক্ষিত কর্মীর দেওয়া মাংসপেশির ইনজেকশন ও শিরায় ইনফিউশন আছে।"))
add("rt", "inh", ("Three panels showing a man using an inhaler, a nasal spray and a skin cream, each with a close-up of lungs, nose and skin layers.", "Inhalers reach the airways, nasal sprays act in the nose and creams are applied to the skin."),
    ("তিনটি প্যানেলে একজন পুরুষ ইনহেলার, নাকের স্প্রে ও ত্বকের ক্রিম ব্যবহার করছেন, সঙ্গে ফুসফুস, নাক ও ত্বকের স্তরের ক্লোজ-আপ।", "ইনহেলার শ্বাসনালিতে পৌঁছায়, নাকের স্প্রে নাকে কাজ করে এবং ক্রিম ত্বকে লাগানো হয়।"))
add("rt", "local", ("A man putting eye drops in his eye, with panels for ear drops, a rectal suppository and a vaginal applicator, each with an anatomy close-up.", "Other local routes include eye drops, ear drops and rectal or vaginal forms."),
    ("একজন পুরুষ চোখে ড্রপ দিচ্ছেন; পাশে কানের ড্রপ, রেক্টাল সাপোজিটরি ও ভ্যাজাইনাল অ্যাপ্লিকেটরের প্যানেল, প্রতিটিতে শরীরতত্ত্বের ক্লোজ-আপ।", "অন্যান্য স্থানীয় পথের মধ্যে চোখের ড্রপ, কানের ড্রপ এবং রেক্টাল বা ভ্যাজাইনাল রূপ আছে।"))
add("rt", "speed", ("Five routes ranked by onset speed with animal icons, from intravenous and injection to oral, tablet and skin cream, beside a speedometer-style stopwatch.", "Onset generally varies by route, but it also depends on the medicine; this illustration is not a dosing guide."),
    ("পাঁচটি পথ কাজ শুরুর গতি অনুযায়ী প্রাণীর আইকনসহ সাজানো, শিরা ও ইনজেকশন থেকে মুখ, ট্যাবলেট ও ত্বকের ক্রিম পর্যন্ত; পাশে স্পিডোমিটার-ধাঁচের স্টপওয়াচ।", "কাজ শুরুর সময় সাধারণত পথভেদে ভিন্ন, তবে ওষুধের ধরনের ওপরও নির্ভর করে; এই চিত্র ডোজের নির্দেশিকা নয়।"))
if __name__ == "__main__":
    for a in sys.argv[1:] or ("df", "sr", "rt"):
        for lg in ("en", "bn"): a3.process(a, lg)
