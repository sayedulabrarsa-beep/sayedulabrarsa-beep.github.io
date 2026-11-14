#!/usr/bin/env python3
"""Builds /blog/how-to-read-a-prescription-abbreviations/ (English) and its -bangla page,
using the how-do-medicines-work-in-the-body pages as the layout template. Run from the repo root.
Images: _src/prescription_images/make_rx.py"""
import re, json, html, pathlib
R = pathlib.Path(__file__).resolve().parent.parent
B = "https://sayedulabrar.site"
SLUG = "how-to-read-a-prescription-abbreviations"
EN_URL, BN_URL = f"/blog/{SLUG}/", f"/blog/{SLUG}-bangla/"
DATE, DATE_EN, DATE_BN = "2026-11-14", "14 November 2026", "১৪ নভেম্বর ২০২৬"
IMG = "/assets/img/blog/prescription/"
TPL = "how-do-medicines-work-in-the-body"
esc = lambda x: html.escape(x, quote=True)

# key: (file stem, alt EN, caption EN, alt BN, caption BN)
F = {
 "cover": ("how-to-read-a-prescription-cover",
   "How to read a prescription: a doctor's hand beside a blank prescription pad, a pen, a stethoscope and a glass of water on a wooden desk. Decode the instructions, take medicines safely. By Sayedul Abrar, Pharmacist.",
   "A simple guide to the words and short forms on a prescription. Illustrative photo.",
   "প্রেসক্রিপশন পড়ার সহজ নিয়ম: কাঠের টেবিলে ডাক্তারের হাতের পাশে ফাঁকা প্রেসক্রিপশন প্যাড, কলম, স্টেথোস্কোপ ও পানির গ্লাস। নির্দেশনা বুঝুন, নিরাপদে ওষুধ খান। লিখেছেন ফার্মাসিস্ট সাইয়্যেদুল আবরার।",
   "প্রেসক্রিপশনের শব্দ ও সংক্ষেপ বোঝার সহজ গাইড। প্রতীকী ছবি।"),
 "parts": ("parts-of-a-prescription-labelled",
   "A sample prescription with eight numbered parts: 1 doctor's name, degrees and registration number; 2 patient's name, age and date; 3 the Rx symbol; 4 medicine name, form and strength; 5 how much and how often; 6 before or after food; 7 for how long; 8 signature and advice. Fictional doctor, patient and medicines.",
   "Sample only: fictional doctor, patient and medicines. Based on the WHO Guide to Good Prescribing.",
   "আটটি নম্বর দেওয়া অংশসহ একটি নমুনা প্রেসক্রিপশন: ১ ডাক্তারের নাম, ডিগ্রি ও রেজিস্ট্রেশন নম্বর; ২ রোগীর নাম, বয়স ও তারিখ; ৩ Rx চিহ্ন; ৪ ওষুধের নাম, ধরন ও শক্তি; ৫ কতটা ও কতবার; ৬ খাবারের আগে না পরে; ৭ কতদিন; ৮ স্বাক্ষর ও পরামর্শ। ডাক্তার, রোগী ও ওষুধ কাল্পনিক।",
   "শুধু নমুনা: ডাক্তার, রোগী ও ওষুধ কাল্পনিক। WHO Guide to Good Prescribing-এর ভিত্তিতে।"),
 "frequency": ("prescription-frequency-abbreviations-od-bd-tds",
   "A morning, midday and night pill organiser and a clock, with prescription frequency abbreviations: OD once a day (safer to write daily), BD twice a day, TDS three times a day, QDS or QID four times a day, mane in the morning, HS or nocte at night, PRN or SOS only when needed, STAT straight away.",
   "Based on ISMP and Australian health department guidance on prescribing terms.",
   "সকাল, দুপুর ও রাতের পিল অর্গানাইজার ও ঘড়ির ছবির পাশে কতবার খাবেন তার সংক্ষেপ: OD দিনে ১ বার, BD দিনে ২ বার, TDS দিনে ৩ বার, QDS বা QID দিনে ৪ বার, mane সকালে, HS বা nocte রাতে, PRN বা SOS শুধু দরকার হলে, STAT এখনই।",
   "ISMP ও অস্ট্রেলিয়ার স্বাস্থ্য বিভাগের নির্দেশনার ভিত্তিতে।"),
 "pattern": ("what-does-1-0-1-mean-on-a-prescription",
   "What 1+0+1 means on a prescription: three panels for morning, midday and night showing 1, 0 and 1. Examples: 1+0+1 is one in the morning and one at night; 1+1+1 is three times a day; 0+0+1 is one at night only; half+0+half is half a tablet morning and night. The numbers are tablets or doses, not hours.",
   "The morning + midday + night pattern is common on prescriptions in Bangladesh.",
   "প্রেসক্রিপশনে ১+০+১ মানে কী: সকাল, দুপুর ও রাতের তিনটি ঘরে ১, ০ ও ১। উদাহরণ: ১+০+১ মানে সকালে ১টি ও রাতে ১টি; ১+১+১ মানে দিনে ৩ বার; ০+০+১ মানে শুধু রাতে ১টি; ½+০+½ মানে সকালে ও রাতে আধা ট্যাবলেট। সংখ্যাগুলো ট্যাবলেট বা ডোজ, ঘণ্টা নয়।",
   "সকাল + দুপুর + রাতের এই লেখার ধরন বাংলাদেশের প্রেসক্রিপশনে খুব প্রচলিত।"),
 "food": ("before-or-after-food-ac-pc-meaning",
   "A Bangladeshi meal of rice, dal, fish and greens with a glass of water and a tablet strip, explaining AC (before food), PC (after or with food), empty stomach (often 1 hour before or 2 hours after food) and HS (at bedtime). Example: many PPIs such as omeprazole are usually taken before a meal.",
   "General meanings. Your medicine leaflet and pharmacist give the exact timing. Illustrative photo.",
   "ভাত, ডাল, মাছ ও শাকের প্লেট, পানির গ্লাস ও ট্যাবলেটের পাতার ছবির পাশে AC (খাবারের আগে), PC (খাবারের পরে বা সঙ্গে), খালি পেটে (সাধারণত খাবারের ১ ঘণ্টা আগে বা ২ ঘণ্টা পরে) ও HS (ঘুমানোর আগে) বোঝানো হয়েছে। উদাহরণ: অনেক PPI, যেমন ওমিপ্রাজল, সাধারণত খাবারের আগে খেতে বলা হয়।",
   "সাধারণ অর্থ। সঠিক সময় আপনার ওষুধের লিফলেট ও ফার্মাসিস্ট বলে দেবেন। প্রতীকী ছবি।"),
 "forms": ("medicine-forms-and-routes-tab-syp-inj",
   "A syrup bottle, measuring cup, syringe, vial, dropper bottle, tablets and capsules, with medicine form and route abbreviations: Tab tablet, Cap capsule, Syp syrup, Susp suspension (shake before use), Inj injection (IM into muscle, IV into a vein), Inh inhaler, drops, PO by mouth, and tsf one teaspoonful equal to 5 mL measured with the cup or syringe, not a kitchen spoon.",
   "Use the measuring cup or oral syringe that comes with the medicine (FDA, ISMP). Illustrative photo.",
   "সিরাপের বোতল, মাপার কাপ, সিরিঞ্জ, ভায়াল, ড্রপের বোতল, ট্যাবলেট ও ক্যাপসুলের ছবির পাশে ওষুধের ধরন ও প্রয়োগের পথের সংক্ষেপ: Tab ট্যাবলেট, Cap ক্যাপসুল, Syp সিরাপ, Susp সাসপেনশন (খাওয়ার আগে ঝাঁকিয়ে নিন), Inj ইনজেকশন (IM মাংসপেশিতে, IV শিরায়), Inh ইনহেলার, ড্রপ, PO মুখে খাওয়ার জন্য, আর tsf মানে ১ চা-চামচ বা ৫ mL, যা মাপার কাপ বা সিরিঞ্জে মাপবেন, রান্নাঘরের চামচে নয়।",
   "ওষুধের সঙ্গে দেওয়া মাপার কাপ বা সিরিঞ্জ ব্যবহার করুন (FDA, ISMP)। প্রতীকী ছবি।"),
 "mistakes": ("error-prone-prescription-abbreviations",
   "A magnifying glass over messy handwriting on a clipboard, with abbreviations that cause mistakes: OD can mean once daily or right eye; QD can be misread as QID; U for units can be misread as 0 or 4; 1.0 mg can be misread as 10 mg; .5 mg can be misread as 5 mg. If anything is unclear, ask the pharmacist and check with the doctor.",
   "Based on the ISMP List of Error-Prone Abbreviations. Illustrative photo.",
   "ক্লিপবোর্ডে অস্পষ্ট হাতের লেখার ওপর ম্যাগনিফাইং গ্লাসের ছবির পাশে যে সংক্ষেপে ভুল হয়: OD মানে দিনে একবার, আবার ডান চোখও; QD পড়া হতে পারে QID; ইউনিটের U পড়া হতে পারে ০ বা ৪; 1.0 mg পড়া হতে পারে 10 mg; .5 mg পড়া হতে পারে 5 mg। অস্পষ্ট লাগলে ফার্মাসিস্ট ও ডাক্তারকে জিজ্ঞেস করুন।",
   "ISMP-এর ভুল-প্রবণ সংক্ষেপের তালিকার ভিত্তিতে। প্রতীকী ছবি।"),
 "takeaways": ("how-to-read-a-prescription-key-takeaways",
   "A pharmacist explaining a medicine box to a patient holding a prescription. Ask, understand, take it right: five steps to read any prescription: check your name, date and the doctor's details; match the medicine name and strength with the pack; read how much, how often and how long; check before or after food; never guess, ask your pharmacist or doctor.",
   "Five steps to remember. Illustrative photo.",
   "প্রেসক্রিপশন হাতে রোগীকে একজন ফার্মাসিস্ট ওষুধের বাক্স বুঝিয়ে দিচ্ছেন। জিজ্ঞেস করুন, বুঝুন, ঠিকভাবে খান: প্রেসক্রিপশন পড়ার ৫টি ধাপ: নাম, তারিখ ও ডাক্তারের তথ্য মিলিয়ে নিন; ওষুধের নাম ও শক্তি প্যাকের সঙ্গে মেলান; কতটা, কতবার, কতদিন পড়ে নিন; খাবারের আগে না পরে দেখুন; অনুমান না করে ফার্মাসিস্ট বা ডাক্তারকে জিজ্ঞেস করুন।",
   "মনে রাখার পাঁচটি ধাপ। প্রতীকী ছবি।"),
}
def fig(k, bn=False, hero=False):
    stem, aen, cen, abn, cbn = F[k]
    src = f"{IMG}{stem}{'-bn' if bn else ''}.webp?v=2"
    alt, cap = (abn, cbn) if bn else (aen, cen)
    load = 'fetchpriority="high"' if hero else 'loading="lazy"'
    tip = 'বড় করে দেখতে ছবিতে চাপুন।' if bn else 'Tap the image to view it full size.'
    return f'<figure class="hero-visual"><a href="{src}" target="_blank" rel="noopener" aria-label="{esc(tip)}"><img src="{src}" alt="{esc(alt)}" width="1600" height="900" {load} decoding="async"></a><figcaption class="caption">{cap} {tip}</figcaption></figure>'

def table(label, head, rows):
    th = "".join(f"<th>{h}</th>" for h in head)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="table-scroll" role="region" aria-label="{esc(label)}" tabindex="0"><table class="compare-table"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'
def faq(items):
    return '<div class="faq">' + "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in items) + "</div>"

REFS = [
 ("https://medbox.org/index.php/dl/5e148832db60a2044c2d1e5a", "World Health Organization. Guide to Good Prescribing: A Practical Manual (WHO/DAP/94.11), chapter 9 “Write a prescription”", "what a prescription should contain; write clearly."),
 ("https://online.ecri.org/hubfs/ISMP/Resources/ISMP_ErrorProneAbbreviation_List.pdf", "Institute for Safe Medication Practices (ISMP). List of Error-Prone Abbreviations, Symbols, and Dose Designations (2024)", "QD, OD, U, trailing and leading zeros."),
 ("https://safetyandquality.gov.au/sites/default/files/2024-12/fact-sheet-recommendations-for-safe-use-of-medicines-terminology.pdf", "Australian Commission on Safety and Quality in Health Care. Recommendations for safe use of medicines terminology, fact sheet (November 2024)", "accepted abbreviations such as bd, tds, prn and stat; write “daily” in full."),
 ("https://fhhs.health.wa.gov.au/~/media/Files/Corporate/general-documents/WATAG/WAMSG/Acceptable-Prescribing-Terms-and-Abbreviations-Poster.pdf", "Department of Health, Western Australia. Acceptable Prescribing Terms and Abbreviations (2017)", "bd, tds, qid, mane, nocte, prn, stat, PO."),
 ("https://medlineplus.gov/medwords/abbreviations2.html", "MedlinePlus (U.S. National Library of Medicine). Abbreviations, part 2", "b-i-d from Latin bis in die, twice a day."),
 ("https://www.fda.gov/media/88498/download", "U.S. FDA / NCPDP. Standardize the dosing designations on prescription container labels for oral liquid medications to metric (mL) only", "kitchen spoons vary; use the dosing device."),
 ("https://www.consumermedsafety.org/safety-tips/liquid-medicines", "ISMP ConsumerMedSafety. Liquid medicines", "never use a household spoon; use oral syringes with mL markings."),
 ("https://doi.org/10.3329/bpj.v18i1.23509", "Sultana F, et al. Prescribing pattern and prescription errors: a study at a tertiary care hospital of Bangladesh. Bangladesh Pharmaceutical Journal 2015;18(1):20–24", "illegible names, missing strengths, improper abbreviations."),
 ("https://doi.org/10.3329/updcj.v1i2.13979", "Afsan M, et al. Audit of typical prescription format among the prescribers of a garment medical centre in Bangladesh. Update Dental College Journal 2011;1(2):7–12", "dose and duration missing on some prescriptions."),
]
def refs(bn=False):
    li = "".join(f'<li>{t}. <a href="{u}" target="_blank" rel="noopener noreferrer">{u.split("//")[1].split("/")[0]}</a> — {n}</li>' for u, t, n in REFS)
    h = "সূত্র ও আরও পড়ুন" if bn else "References and further reading"
    note = ("<p><strong>সম্পাদকীয় নোট:</strong> সূত্রগুলো ১৪ নভেম্বর ২০২৬-এ দেখা হয়েছে। সংক্ষেপের ব্যবহার দেশ, হাসপাতাল ও ডাক্তারভেদে আলাদা হতে পারে। সন্দেহ হলে প্রেসক্রিপশন যিনি লিখেছেন, তাঁর কাছ থেকে নিশ্চিত হোন।</p>" if bn else
            "<p><strong>Editorial note:</strong> Sources checked on 14 November 2026. How abbreviations are used can differ between countries, hospitals and doctors. If in doubt, confirm with the person who wrote the prescription.</p>")
    return f'<section class="references"><h2>{h}</h2><ol>{li}</ol>{note}</section>'

# ================================================================= English
FAQ_EN = [
 ("What does BD mean on a prescription?", "BD means twice a day. It comes from the Latin <em>bis die</em>. BID means the same thing. It is usually taken in the morning and in the evening or at night. If the gap between doses matters for your medicine, ask your pharmacist."),
 ("What does TDS mean on a prescription?", "TDS means three times a day, from the Latin <em>ter die sumendum</em>. TID means the same. Three times a day does not always mean exactly every 8 hours, so ask your pharmacist if the timing matters for your medicine."),
 ("What does OD mean on a prescription?", "OD usually means once a day. But OD is also the abbreviation for the right eye (<em>oculus dexter</em>), which is why ISMP advises writing “daily” instead. If OD is written next to eye drops, ask whether it means once a day or the right eye."),
 ("What does 1+0+1 mean on a prescription?", "It shows how many tablets or doses to take in the morning, at midday and at night. 1+0+1 means one in the morning, none at midday and one at night, so twice a day. 1+1+1 means three times a day, and 0+0+1 means one at night only. The numbers are doses, not hours."),
 ("What is the difference between PRN and SOS?", "Both mean “only when needed”, for example for pain or fever. PRN comes from <em>pro re nata</em> and SOS from <em>si opus sit</em>. Ask your doctor or pharmacist the most you can take in a day and how long to wait between doses."),
 ("What does “continue” or “চলবে” mean on a prescription?", "It means keep taking the medicine until your doctor reviews it. It does not mean forever without a check-up. Do not stop on your own, and ask when you should go back for a review."),
 ("What should I do if I cannot read the doctor’s handwriting?", "Do not guess. Ask the pharmacist to read it with you. If the pharmacist is not sure either, call the doctor’s chamber. A Bangladesh hospital study found medicine names that were unclear because of handwriting, so checking is sensible, not rude."),
 ("Is 1 tsf (teaspoonful) the same as 5 mL?", "On a prescription, one teaspoonful (tsf) is usually meant as 5 mL. Kitchen teaspoons vary in size, so measure with the cup or oral syringe that comes with the medicine, not a household spoon (FDA, ISMP)."),
]
EN_BODY = f'''
<div class="quick"><strong>Quick answer:</strong> A prescription tells you which medicine to take, how much, how often, before or after food, and for how long. Common short forms: <strong>OD</strong> once a day, <strong>BD</strong> twice a day, <strong>TDS</strong> three times a day, <strong>QDS</strong> four times a day, <strong>HS</strong> at bedtime, <strong>AC</strong> before food, <strong>PC</strong> after food, <strong>PRN</strong> only when needed. In Bangladesh, <strong>1+0+1</strong> means one in the morning and one at night. If anything is unclear, ask your pharmacist. Never guess.</div>
<h2>A common moment (illustrative, fictional)</h2>
<p>Rina collects her father’s medicines from a pharmacy in Dhaka. The prescription says “Tab. … 20 mg 1+0+1 AC × 14 days” and “Syp. … 2 tsf TDS PC × 5 days”. She knows the medicine names, but not what 1+0+1, AC, TDS or tsf mean. This article explains each one, so you can check a prescription before you leave the pharmacy. Rina is an example, not a real patient.</p>
<h2>The 8 parts of a prescription</h2>
<p>The World Health Organization’s <em>Guide to Good Prescribing</em> lists what a prescription should contain: the prescriber’s name, address and phone number; the date; the medicine name and strength; the dosage form and total amount; instructions and warnings; the patient’s name, address and age; and the prescriber’s signature. In Bangladesh, the pad usually also shows the doctor’s degrees and BMDC registration number.</p>
{fig("parts")}
<p>Start with the basics: is it <strong>your</strong> name, today’s date, and a doctor you saw? Then read each medicine line from left to right: form and name, strength, how much, how often, before or after food, and for how long.</p>
<h2>What does Rx mean?</h2>
<p><strong>Rx</strong> (℞) is the traditional sign at the start of the medicine list. It comes from the Latin word <em>recipe</em>, meaning “take”. It is not a medicine name.</p>
<h2>How often: OD, BD, TDS, QDS</h2>
<p>Most frequency short forms come from Latin. Australian prescribing guidance accepts written bd, tds, qid, prn and stat, but recommends writing “once a day” or “daily” in full rather than OD.</p>
{fig("frequency")}
{table("Prescription frequency abbreviations and their meaning", ["Short form", "From the Latin", "Meaning"], [
 ["OD", "omni die", "Once a day (safer to write “daily”)"],
 ["BD / BID", "bis die / bis in die", "Twice a day"],
 ["TDS / TID", "ter die sumendum / ter in die", "Three times a day"],
 ["QDS / QID", "quater die sumendum / quater in die", "Four times a day"],
 ["Mane", "mane", "In the morning"],
 ["HS / Nocte", "hora somni / nocte", "At bedtime / at night"],
 ["PRN / SOS", "pro re nata / si opus sit", "Only when needed"],
 ["STAT", "statim", "Straight away"],
])}
<p>“Three times a day” is often taken morning, afternoon and night, spread across waking hours. For some medicines the gap matters more. If you are not sure how many hours to leave between doses, ask your pharmacist.</p>
<h2>What does 1+0+1 mean?</h2>
<p>Many prescriptions in Bangladesh use a simple number pattern instead of Latin: <strong>morning + midday + night</strong>. Each number is how many tablets (or doses) to take at that time. It may be written in English or Bangla digits (১+০+১).</p>
{fig("pattern")}
<ul><li><strong>1+0+1</strong>: one in the morning, none at midday, one at night (twice a day).</li><li><strong>1+1+1</strong>: one in the morning, at midday and at night (three times a day).</li><li><strong>0+0+1</strong>: one at night only.</li><li><strong>½+0+½</strong>: half a tablet in the morning and at night. Ask first whether your tablet can be split. Some, such as modified-release tablets, should not be broken.</li></ul>
<p>The numbers are doses, not hours. The strength (for example 20 mg) is written separately, so check it against the pack.</p>
<h2>Before or after food: AC, PC and “empty stomach”</h2>
<p><strong>AC</strong> (<em>ante cibum</em>) means before food. <strong>PC</strong> (<em>post cibum</em>) means after food. Doctors in Bangladesh often write this in Bangla instead: খাবারের আগে or খাবারের পরে. “Empty stomach” usually means about an hour before food or two hours after, but follow your own leaflet.</p>
{fig("food")}
<p>Timing can change how well some medicines work. For example, many proton pump inhibitors are taken before a meal (see <a href="/blog/when-to-take-ppi-before-meals/">when to take a PPI</a>), and iron tablets have their own food rules (see <a href="/blog/how-to-take-iron-tablets-properly/">how to take iron tablets properly</a>).</p>
<h2>For how long: “× 7 days”, “1 month” and “continue”</h2>
<p>The duration is often written as “× 5 days”, “7 days”, “1 month”, or “continue” (চলবে). <strong>Continue</strong> means keep taking it until your doctor reviews it, not forever without a check-up. For antibiotics, finish the course as written unless your doctor says otherwise. My article on <a href="/blog/why-complete-antibiotic-course-antibiotic-resistance/">why you must complete an antibiotic course</a> explains why.</p>
<h2>Forms and routes: Tab, Cap, Syp, Inj, PO</h2>
<p>The line usually starts with the dosage form: <strong>Tab.</strong> tablet, <strong>Cap.</strong> capsule, <strong>Syp.</strong> syrup, <strong>Susp.</strong> suspension (shake it before use), <strong>Inj.</strong> injection, <strong>Inh.</strong> inhaler, or drops. The route may follow: <strong>PO</strong> by mouth, <strong>IM</strong> into a muscle, <strong>IV</strong> into a vein.</p>
{fig("forms")}
<p>For liquids, <strong>tsf</strong> means teaspoonful, usually 5 mL. The FDA notes that kitchen spoons vary widely in size, and ISMP advises never to use a household spoon. Use the cup or oral syringe that comes with the medicine.</p>
<p>The medicine name on the prescription may be a brand name. The pack also shows the generic name (the active ingredient). My guide to <a href="/blog/generic-name-vs-brand-name/">generic name vs brand name</a> shows how to match them.</p>
<h2>Abbreviations that cause mistakes</h2>
<p>Some short forms are easy to misread. The Institute for Safe Medication Practices (ISMP) keeps a list of error-prone abbreviations. A few that matter to patients:</p>
{fig("mistakes")}
{table("Error-prone abbreviations and safer alternatives", ["Written", "Intended", "Can be misread as", "Safer"], [
 ["OD", "Once daily", "Right eye (oculus dexter)", "daily"],
 ["QD", "Every day", "QID (four times a day)", "daily"],
 ["U", "Units", "0 or 4 (a 10-fold error)", "units"],
 ["1.0 mg", "1 mg", "10 mg", "1 mg"],
 [".5 mg", "0.5 mg", "5 mg", "0.5 mg"],
])}
<p>This is not just theory. A study of 200 patients’ prescriptions at a tertiary hospital in Rajshahi found 35 medicine names unclear because of handwriting, dose strength missing for 279 medicines, and 31 medicines with an improper abbreviation. An audit at a garment medical centre in Dhaka found dose and duration written on only 66% and 70% of prescriptions. Both are older, single-site studies, so they do not describe every prescription in Bangladesh, but they show why checking matters.</p>
<h2>How to check your prescription at the pharmacy</h2>
<ol><li>Check your name, the date and the doctor’s details.</li><li>Match each medicine name and strength with the pack you are given.</li><li>Read how much, how often and for how long.</li><li>Check before or after food.</li><li>Ask about anything unclear before you leave, and look at the expiry date. My guide to <a href="/blog/expiry-date-vs-manufacturing-date-medicine/">expiry date vs manufacturing date</a> shows how to read it.</li></ol>
<p>If the words drug and medicine confuse you, see <a href="/blog/drug-vs-medicine/">drug vs medicine</a>.</p>
<h2>Key takeaways</h2>
{fig("takeaways")}
<div class="takeaways"><ul><li>OD once a day, BD twice, TDS three times, QDS four times a day.</li><li>1+0+1 means one in the morning and one at night.</li><li>AC is before food, PC is after food, HS is at bedtime, PRN or SOS is only when needed.</li><li>Measure liquids in mL with the device in the pack, not a kitchen spoon.</li><li>Never guess. Ask your pharmacist or doctor.</li></ul></div>
<h2>Frequently asked questions</h2>
{faq(FAQ_EN)}
'''

# ================================================================= Bangla
FAQ_BN = [
 ("প্রেসক্রিপশনে BD মানে কী?", "BD মানে দিনে ২ বার। এটি এসেছে ল্যাটিন <em>bis die</em> থেকে। BID-ও একই অর্থ। সাধারণত সকালে আর সন্ধ্যায় বা রাতে খাওয়া হয়। আপনার ওষুধে দুই ডোজের মাঝের সময় গুরুত্বপূর্ণ হলে ফার্মাসিস্টকে জিজ্ঞেস করুন।"),
 ("প্রেসক্রিপশনে TDS মানে কী?", "TDS মানে দিনে ৩ বার, ল্যাটিন <em>ter die sumendum</em> থেকে। TID-ও একই। দিনে ৩ বার মানে সবসময় ঠিক ৮ ঘণ্টা পরপর নয়, তাই আপনার ওষুধে সময় গুরুত্বপূর্ণ কি না, ফার্মাসিস্টকে জিজ্ঞেস করুন।"),
 ("প্রেসক্রিপশনে OD মানে কী?", "OD সাধারণত দিনে ১ বার বোঝায়। কিন্তু OD ডান চোখেরও (<em>oculus dexter</em>) সংক্ষেপ, তাই ISMP এর বদলে “daily” লিখতে বলে। চোখের ড্রপের পাশে OD লেখা থাকলে জিজ্ঞেস করুন, এর মানে দিনে ১ বার নাকি ডান চোখ।"),
 ("প্রেসক্রিপশনে ১+০+১ মানে কী?", "এটি বোঝায় সকালে, দুপুরে ও রাতে কয়টি ট্যাবলেট বা ডোজ খাবেন। ১+০+১ মানে সকালে ১টি, দুপুরে নয়, রাতে ১টি, অর্থাৎ দিনে ২ বার। ১+১+১ মানে দিনে ৩ বার, আর ০+০+১ মানে শুধু রাতে ১টি। সংখ্যাগুলো ডোজ, ঘণ্টা নয়।"),
 ("PRN আর SOS-এর পার্থক্য কী?", "দুটোরই মানে “শুধু দরকার হলে”, যেমন ব্যথা বা জ্বর হলে। PRN এসেছে <em>pro re nata</em> থেকে, SOS এসেছে <em>si opus sit</em> থেকে। দিনে সর্বোচ্চ কতবার খাওয়া যাবে এবং দুই ডোজের মাঝে কতক্ষণ অপেক্ষা করতে হবে, ডাক্তার বা ফার্মাসিস্টের কাছ থেকে জেনে নিন।"),
 ("প্রেসক্রিপশনে “চলবে” বা “continue” মানে কী?", "এর মানে ডাক্তার আবার দেখা পর্যন্ত ওষুধটি চালিয়ে যাবেন। এর মানে চেকআপ ছাড়া সারাজীবন নয়। নিজে নিজে বন্ধ করবেন না, আর কবে আবার দেখাতে হবে তা জিজ্ঞেস করুন।"),
 ("ডাক্তারের হাতের লেখা পড়তে না পারলে কী করব?", "অনুমান করবেন না। ফার্মাসিস্টকে আপনার সঙ্গে পড়ে দিতে বলুন। ফার্মাসিস্টও নিশ্চিত না হলে ডাক্তারের চেম্বারে ফোন করুন। বাংলাদেশের একটি হাসপাতালের গবেষণায় হাতের লেখার কারণে কিছু ওষুধের নাম অস্পষ্ট পাওয়া গেছে, তাই যাচাই করা অভদ্রতা নয়, বুদ্ধিমানের কাজ।"),
 ("১ tsf (চা-চামচ) কি ৫ mL-এর সমান?", "প্রেসক্রিপশনে ১ চা-চামচ (tsf) বলতে সাধারণত ৫ mL বোঝানো হয়। রান্নাঘরের চামচের মাপ একেক রকম, তাই ওষুধের সঙ্গে দেওয়া মাপার কাপ বা মুখে খাওয়ানোর সিরিঞ্জ দিয়ে মাপুন, ঘরের চামচ দিয়ে নয় (FDA, ISMP)।"),
]
BN_BODY = f'''
<div class="quick"><strong>সহজ উত্তর:</strong> প্রেসক্রিপশন বলে দেয় কোন ওষুধ, কতটা, কতবার, খাবারের আগে না পরে, আর কতদিন খাবেন। প্রচলিত সংক্ষেপ: <strong>OD</strong> দিনে ১ বার, <strong>BD</strong> দিনে ২ বার, <strong>TDS</strong> দিনে ৩ বার, <strong>QDS</strong> দিনে ৪ বার, <strong>HS</strong> ঘুমানোর আগে, <strong>AC</strong> খাবারের আগে, <strong>PC</strong> খাবারের পরে, <strong>PRN</strong> শুধু দরকার হলে। বাংলাদেশে <strong>১+০+১</strong> মানে সকালে ১টি ও রাতে ১টি। কিছু অস্পষ্ট লাগলে ফার্মাসিস্টকে জিজ্ঞেস করুন, অনুমান করবেন না।</div>
<h2>একটি পরিচিত মুহূর্ত (উদাহরণমূলক, কাল্পনিক)</h2>
<p>রিনা ঢাকার একটি ফার্মেসি থেকে বাবার ওষুধ কিনছেন। প্রেসক্রিপশনে লেখা “Tab. … 20 mg 1+0+1 AC × 14 days” আর “Syp. … 2 tsf TDS PC × 5 days”। ওষুধের নাম তিনি চেনেন, কিন্তু 1+0+1, AC, TDS বা tsf মানে কী, জানেন না। এই লেখায় প্রতিটির মানে বোঝানো হয়েছে, যাতে ফার্মেসি ছাড়ার আগেই আপনি প্রেসক্রিপশন মিলিয়ে নিতে পারেন। রিনা একটি উদাহরণ, আসল রোগী নন।</p>
<h2>প্রেসক্রিপশনের ৮টি অংশ</h2>
<p>বিশ্ব স্বাস্থ্য সংস্থার (WHO) <em>Guide to Good Prescribing</em> অনুযায়ী একটি প্রেসক্রিপশনে থাকা উচিত: প্রেসক্রাইবারের নাম, ঠিকানা ও ফোন নম্বর; তারিখ; ওষুধের নাম ও শক্তি; ওষুধের ধরন ও মোট পরিমাণ; নির্দেশনা ও সতর্কতা; রোগীর নাম, ঠিকানা ও বয়স; এবং প্রেসক্রাইবারের স্বাক্ষর। বাংলাদেশে প্যাডে সাধারণত ডাক্তারের ডিগ্রি ও BMDC রেজিস্ট্রেশন নম্বরও থাকে।</p>
{fig("parts", True)}
<p>শুরু করুন মৌলিক বিষয় দিয়ে: নামটি কি <strong>আপনার</strong>, তারিখ কি আজকের, আর ডাক্তার কি তিনিই যাঁকে দেখিয়েছেন? তারপর প্রতিটি ওষুধের লাইন বাঁ থেকে ডানে পড়ুন: ধরন ও নাম, শক্তি, কতটা, কতবার, খাবারের আগে না পরে, আর কতদিন।</p>
<h2>Rx মানে কী?</h2>
<p><strong>Rx</strong> (℞) হলো ওষুধের তালিকার শুরুতে দেওয়া প্রচলিত চিহ্ন। এটি এসেছে ল্যাটিন শব্দ <em>recipe</em> থেকে, যার মানে “গ্রহণ করুন”। এটি কোনো ওষুধের নাম নয়।</p>
<h2>কতবার খাবেন: OD, BD, TDS, QDS</h2>
<p>কতবার খাবেন, তার বেশিরভাগ সংক্ষেপ ল্যাটিন থেকে এসেছে। অস্ট্রেলিয়ার প্রেসক্রিপশন নির্দেশনা হাতে লেখা bd, tds, qid, prn ও stat গ্রহণযোগ্য বলে, কিন্তু OD-এর বদলে পুরো “once a day” বা “daily” লিখতে বলে।</p>
{fig("frequency", True)}
{table("প্রেসক্রিপশনে কতবার খাবেন, তার সংক্ষেপ ও অর্থ", ["সংক্ষেপ", "ল্যাটিন উৎস", "অর্থ"], [
 ["OD", "omni die", "দিনে ১ বার (নিরাপদ লেখা: “daily”)"],
 ["BD / BID", "bis die / bis in die", "দিনে ২ বার"],
 ["TDS / TID", "ter die sumendum / ter in die", "দিনে ৩ বার"],
 ["QDS / QID", "quater die sumendum / quater in die", "দিনে ৪ বার"],
 ["Mane", "mane", "সকালে"],
 ["HS / Nocte", "hora somni / nocte", "ঘুমানোর আগে / রাতে"],
 ["PRN / SOS", "pro re nata / si opus sit", "শুধু দরকার হলে"],
 ["STAT", "statim", "এখনই, সঙ্গে সঙ্গে"],
])}
<p>“দিনে ৩ বার” সাধারণত সকাল, বিকেল ও রাতে, জেগে থাকার সময়ের মধ্যে ভাগ করে খাওয়া হয়। কিছু ওষুধে দুই ডোজের ফাঁক বেশি গুরুত্বপূর্ণ। কত ঘণ্টা পরপর খাবেন, নিশ্চিত না হলে ফার্মাসিস্টকে জিজ্ঞেস করুন।</p>
<h2>১+০+১ মানে কী?</h2>
<p>বাংলাদেশের অনেক প্রেসক্রিপশনে ল্যাটিনের বদলে একটি সহজ সংখ্যার ধরন ব্যবহার হয়: <strong>সকাল + দুপুর + রাত</strong>। প্রতিটি সংখ্যা বোঝায় ওই সময়ে কয়টি ট্যাবলেট (বা ডোজ) খাবেন। এটি ইংরেজি বা বাংলা অঙ্কে (১+০+১) লেখা থাকতে পারে।</p>
{fig("pattern", True)}
<ul><li><strong>১+০+১</strong>: সকালে ১টি, দুপুরে নয়, রাতে ১টি (দিনে ২ বার)।</li><li><strong>১+১+১</strong>: সকাল, দুপুর ও রাতে ১টি করে (দিনে ৩ বার)।</li><li><strong>০+০+১</strong>: শুধু রাতে ১টি।</li><li><strong>½+০+½</strong>: সকালে ও রাতে আধা ট্যাবলেট। আগে জেনে নিন আপনার ট্যাবলেট ভাঙা যাবে কি না। কিছু ট্যাবলেট, যেমন মডিফায়েড-রিলিজ ট্যাবলেট, ভাঙা উচিত নয়।</li></ul>
<p>সংখ্যাগুলো ডোজ, ঘণ্টা নয়। শক্তি (যেমন 20 mg) আলাদা করে লেখা থাকে, তাই প্যাকের সঙ্গে মিলিয়ে নিন।</p>
<h2>খাবারের আগে না পরে: AC, PC ও “খালি পেটে”</h2>
<p><strong>AC</strong> (<em>ante cibum</em>) মানে খাবারের আগে। <strong>PC</strong> (<em>post cibum</em>) মানে খাবারের পরে। বাংলাদেশের ডাক্তাররা প্রায়ই এটি বাংলায় লেখেন: খাবারের আগে বা খাবারের পরে। “খালি পেটে” সাধারণত খাবারের প্রায় ১ ঘণ্টা আগে বা ২ ঘণ্টা পরে বোঝায়, তবে নিজের ওষুধের লিফলেট মেনে চলুন।</p>
{fig("food", True)}
<p>সময়ের কারণে কিছু ওষুধ কতটা ভালো কাজ করবে, তা বদলে যেতে পারে। যেমন, অনেক প্রোটন পাম্প ইনহিবিটর খাবারের আগে খাওয়া হয় (দেখুন <a href="/blog/when-to-take-ppi-before-meals-bangla/">PPI কখন খাবেন</a>), আর আয়রন ট্যাবলেটের খাবার নিয়ে আলাদা নিয়ম আছে (দেখুন <a href="/blog/how-to-take-iron-tablets-properly-bangla/">আয়রন ট্যাবলেট খাওয়ার সঠিক নিয়ম</a>)।</p>
<h2>কতদিন: “× ৭ দিন”, “১ মাস” ও “চলবে”</h2>
<p>মেয়াদ সাধারণত লেখা থাকে “× 5 days”, “৭ দিন”, “১ মাস” বা “চলবে” (continue)। <strong>চলবে</strong> মানে ডাক্তার আবার দেখা পর্যন্ত খেয়ে যাবেন, চেকআপ ছাড়া সারাজীবন নয়। অ্যান্টিবায়োটিক হলে ডাক্তার অন্য কিছু না বললে লেখা অনুযায়ী পুরো কোর্স শেষ করুন। কেন, তা ব্যাখ্যা করেছি <a href="/blog/why-complete-antibiotic-course-antibiotic-resistance-bangla/">অ্যান্টিবায়োটিক কোর্স শেষ করা কেন জরুরি</a> লেখায়।</p>
<h2>ধরন ও প্রয়োগের পথ: Tab, Cap, Syp, Inj, PO</h2>
<p>লাইনের শুরুতে সাধারণত ওষুধের ধরন থাকে: <strong>Tab.</strong> ট্যাবলেট, <strong>Cap.</strong> ক্যাপসুল, <strong>Syp.</strong> সিরাপ, <strong>Susp.</strong> সাসপেনশন (খাওয়ার আগে ঝাঁকিয়ে নিন), <strong>Inj.</strong> ইনজেকশন, <strong>Inh.</strong> ইনহেলার, বা ড্রপ। এরপর প্রয়োগের পথ থাকতে পারে: <strong>PO</strong> মুখে খাওয়ার জন্য, <strong>IM</strong> মাংসপেশিতে, <strong>IV</strong> শিরায়।</p>
{fig("forms", True)}
<p>তরল ওষুধে <strong>tsf</strong> মানে চা-চামচ, সাধারণত ৫ mL। FDA বলছে রান্নাঘরের চামচের মাপ অনেক রকম হয়, আর ISMP ঘরের চামচ কখনও ব্যবহার না করতে বলে। ওষুধের সঙ্গে দেওয়া মাপার কাপ বা মুখে খাওয়ানোর সিরিঞ্জ ব্যবহার করুন।</p>
<p>প্রেসক্রিপশনে ওষুধের নামটি ব্র্যান্ড নাম হতে পারে। প্যাকে জেনেরিক নামও (সক্রিয় উপাদান) লেখা থাকে। কীভাবে মেলাবেন, তা দেখুন <a href="/blog/generic-name-vs-brand-name-bangla/">জেনেরিক নাম বনাম ব্র্যান্ড নাম</a> লেখায়।</p>
<h2>যে সংক্ষেপে ভুল হয়</h2>
<p>কিছু সংক্ষেপ সহজেই ভুল পড়া যায়। Institute for Safe Medication Practices (ISMP) ভুল-প্রবণ সংক্ষেপের একটি তালিকা রাখে। রোগীদের জন্য গুরুত্বপূর্ণ কয়েকটি:</p>
{fig("mistakes", True)}
{table("ভুল-প্রবণ সংক্ষেপ ও নিরাপদ বিকল্প", ["লেখা", "উদ্দেশ্য", "যা ভুল পড়া হতে পারে", "নিরাপদ লেখা"], [
 ["OD", "দিনে ১ বার", "ডান চোখ (oculus dexter)", "daily"],
 ["QD", "প্রতিদিন", "QID (দিনে ৪ বার)", "daily"],
 ["U", "ইউনিট", "০ বা ৪ (১০ গুণ ভুল)", "units"],
 ["1.0 mg", "1 mg", "10 mg", "1 mg"],
 [".5 mg", "0.5 mg", "5 mg", "0.5 mg"],
])}
<p>এটি শুধু তত্ত্ব নয়। রাজশাহীর একটি টারশিয়ারি হাসপাতালে ২০০ রোগীর প্রেসক্রিপশন নিয়ে এক গবেষণায় দেখা গেছে, হাতের লেখার কারণে ৩৫টি ওষুধের নাম অস্পষ্ট ছিল, ২৭৯টি ওষুধের শক্তি লেখা ছিল না, আর ৩১টি ওষুধে ভুল সংক্ষেপ ছিল। ঢাকার একটি গার্মেন্টস মেডিকেল সেন্টারের অডিটে মাত্র ৬৬% প্রেসক্রিপশনে ডোজ ও ৭০%-এ মেয়াদ লেখা পাওয়া গেছে। দুটিই পুরোনো ও একটি করে প্রতিষ্ঠানের গবেষণা, তাই বাংলাদেশের সব প্রেসক্রিপশনের চিত্র নয়, তবে যাচাই কেন জরুরি তা বোঝায়।</p>
<h2>ফার্মেসিতে প্রেসক্রিপশন যেভাবে মিলিয়ে নেবেন</h2>
<ol><li>নিজের নাম, তারিখ ও ডাক্তারের তথ্য মিলিয়ে নিন।</li><li>প্রতিটি ওষুধের নাম ও শক্তি হাতে পাওয়া প্যাকের সঙ্গে মেলান।</li><li>কতটা, কতবার ও কতদিন, পড়ে নিন।</li><li>খাবারের আগে না পরে, দেখে নিন।</li><li>ফার্মেসি ছাড়ার আগে অস্পষ্ট সব কিছু জিজ্ঞেস করুন, আর মেয়াদের তারিখ দেখুন। কীভাবে পড়বেন, তা আছে <a href="/blog/expiry-date-vs-manufacturing-date-medicine-bangla/">মেয়াদ শেষের তারিখ ও উৎপাদনের তারিখ</a> লেখায়।</li></ol>
<p>ড্রাগ আর মেডিসিন শব্দ দুটি নিয়ে দ্বিধা থাকলে পড়ুন <a href="/blog/drug-vs-medicine-bangla/">ড্রাগ বনাম মেডিসিন</a>।</p>
<h2>মনে রাখুন</h2>
{fig("takeaways", True)}
<div class="takeaways"><ul><li>OD দিনে ১ বার, BD ২ বার, TDS ৩ বার, QDS দিনে ৪ বার।</li><li>১+০+১ মানে সকালে ১টি ও রাতে ১টি।</li><li>AC খাবারের আগে, PC খাবারের পরে, HS ঘুমানোর আগে, PRN বা SOS শুধু দরকার হলে।</li><li>তরল ওষুধ প্যাকের মাপার কাপ বা সিরিঞ্জে mL দিয়ে মাপুন, রান্নাঘরের চামচে নয়।</li><li>অনুমান করবেন না। ফার্মাসিস্ট বা ডাক্তারকে জিজ্ঞেস করুন।</li></ul></div>
<h2>সাধারণ প্রশ্নোত্তর</h2>
{faq(FAQ_BN)}
'''

STYLE = ('<style>.article-content .faq details{border:1px solid var(--line);border-radius:12px;margin:10px 0;padding:14px 16px}'
         '.article-content .faq summary{font-weight:700;cursor:pointer;min-height:24px}.article-content .faq details p{margin:12px 0 0}'
         '.article-content .table-scroll{max-width:100%;overflow-x:auto;border-radius:12px;margin:18px 0 26px;border:1px solid var(--line)}'
         '.article-content .compare-table{width:100%;border-collapse:collapse;min-width:520px}.article-content .compare-table th,.article-content .compare-table td{padding:12px 14px;text-align:left;vertical-align:top;border-bottom:1px solid var(--line)}'
         '.article-content .compare-table th{background:#edf6f3;color:#173d43}.article-content .compare-table tr:last-child td{border-bottom:0}</style>')

META = {
 "en": dict(url=EN_URL, lang="en", locale="en_BD",
   title="How to Read a Prescription: BD, TDS, OD & 1+0+1 Explained",
   h1="How to Read a Prescription: BD, TDS, OD and Common Abbreviations",
   short="How to Read a Prescription",
   desc="What do BD, TDS, OD, AC, PC and 1+0+1 mean? A pharmacist explains how to read a prescription in Bangladesh, step by step, with a sample and FAQs.",
   ogdesc="BD, TDS, OD, 1+0+1, AC/PC and tsf explained by a pharmacist, plus the abbreviations that cause mistakes. With WHO and ISMP sources.",
   kw="how to read a prescription, prescription abbreviations, BD meaning, TDS meaning, OD meaning, 1+0+1 meaning, AC PC meaning, PRN SOS, tsf 5 mL, Rx meaning, prescription Bangladesh, pharmacist Sayedul Abrar",
   eyebrow="PHARMA BLOG · MEDICINE SAFETY · 8 MIN READ", lead="BD, TDS, OD, 1+0+1 and the other short forms on a prescription, explained simply.",
   by=f'By <a href="/about/" rel="author">Sayedul Abrar</a>, pharmacist · Published <time datetime="{DATE}">{DATE_EN}</time>',
   body=EN_BODY, faq=FAQ_EN, section="Medicine Safety",
   disc='<div class="disclaimer"><strong>Educational disclaimer:</strong> This article is for general learning and is not personal medical advice. Do not start, stop or change a medicine or its dose based only on this article. Follow your own prescription and ask a registered doctor or pharmacist if anything is unclear.</div>',
   related=('<section class="related"><h2>Continue learning</h2><div class="related-track">'
     '<a class="related-card" href="/blog/generic-name-vs-brand-name/"><strong>Generic Name vs Brand Name</strong><span>Find the active ingredient on any medicine pack.</span></a>'
     '<a class="related-card" href="/blog/expiry-date-vs-manufacturing-date-medicine/"><strong>Expiry Date vs Manufacturing Date</strong><span>Read the dates on a medicine pack in seconds.</span></a>'
     '<a class="related-card" href="/blog/why-complete-antibiotic-course-antibiotic-resistance/"><strong>Why Complete an Antibiotic Course?</strong><span>Finishing the course, resistance and missed doses.</span></a>'
     '<a class="related-card" href="/blog/when-to-take-ppi-before-meals/"><strong>When to Take a PPI</strong><span>Before meals, and common mistakes.</span></a></div></section>')),
 "bn": dict(url=BN_URL, lang="bn", locale="bn_BD",
   title="প্রেসক্রিপশন পড়ার নিয়ম: BD, TDS, OD ও ১+০+১ মানে কী",
   h1="প্রেসক্রিপশন পড়ার নিয়ম: BD, TDS, OD ও প্রচলিত সংক্ষেপের মানে",
   short="প্রেসক্রিপশন পড়ার নিয়ম",
   desc="BD, TDS, OD, AC, PC ও ১+০+১ মানে কী? বাংলাদেশে প্রেসক্রিপশন পড়ার নিয়ম ধাপে ধাপে, নমুনা ও প্রশ্নোত্তরসহ, ফার্মাসিস্টের সহজ ব্যাখ্যা।",
   ogdesc="BD, TDS, OD, ১+০+১, AC/PC ও tsf-এর মানে, আর যে সংক্ষেপে ভুল হয়। WHO ও ISMP-এর সূত্রসহ ফার্মাসিস্টের ব্যাখ্যা।",
   kw="প্রেসক্রিপশন পড়ার নিয়ম, প্রেসক্রিপশনের সংক্ষেপ, BD মানে কি, TDS মানে কি, OD মানে কি, ১+০+১ মানে কি, খাবারের আগে না পরে, AC PC মানে, ডাক্তারের প্রেসক্রিপশন বোঝার উপায়, ফার্মাসিস্ট সাইয়্যেদুল আবরার",
   eyebrow="PHARMA BLOG · ওষুধের নিরাপত্তা · ৮ মিনিটে পড়ুন", lead="প্রেসক্রিপশনের BD, TDS, OD, ১+০+১ আর অন্যান্য সংক্ষেপের মানে, সহজ ভাষায়।",
   by=f'লিখেছেন <a href="/about/" rel="author">Sayedul Abrar</a>, ফার্মাসিস্ট · প্রকাশিত <time datetime="{DATE}">{DATE_BN}</time>',
   body=BN_BODY, faq=FAQ_BN, section="ওষুধের নিরাপত্তা",
   disc='<div class="disclaimer"><strong>শিক্ষামূলক সতর্কতা:</strong> এই লেখাটি সাধারণ জ্ঞানের জন্য, ব্যক্তিগত চিকিৎসা পরামর্শ নয়। শুধু এই লেখা পড়ে কোনো ওষুধ শুরু, বন্ধ বা ডোজ পরিবর্তন করবেন না। নিজের প্রেসক্রিপশন মেনে চলুন, আর কিছু অস্পষ্ট লাগলে রেজিস্টার্ড ডাক্তার বা ফার্মাসিস্টকে জিজ্ঞেস করুন।</div>',
   related=('<section class="related"><h2>আরও পড়ুন</h2><div class="related-track">'
     '<a class="related-card" href="/blog/generic-name-vs-brand-name-bangla/"><strong>জেনেরিক নাম বনাম ব্র্যান্ড নাম</strong><span>ওষুধের প্যাকে উপাদানের নাম খুঁজে নিন।</span></a>'
     '<a class="related-card" href="/blog/expiry-date-vs-manufacturing-date-medicine-bangla/"><strong>মেয়াদ শেষের তারিখ ও উৎপাদনের তারিখ</strong><span>ওষুধের প্যাকের তারিখ সহজে পড়ুন।</span></a>'
     '<a class="related-card" href="/blog/why-complete-antibiotic-course-antibiotic-resistance-bangla/"><strong>অ্যান্টিবায়োটিক কোর্স শেষ করা কেন জরুরি?</strong><span>কোর্স শেষ করা, রেজিস্ট্যান্স ও ডোজ মিস।</span></a>'
     '<a class="related-card" href="/blog/when-to-take-ppi-before-meals-bangla/"><strong>PPI কখন খাবেন?</strong><span>খাবারের আগে, আর প্রচলিত ভুল।</span></a></div></section>')),
}

def txt(h): return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", h))).strip()

def build(lang):
    m = META[lang]; bn = lang == "bn"
    tpl = (R / "blog" / (TPL + ("-bangla" if bn else "")) / "index.html").read_text(encoding="utf-8")
    a = tpl.index('<main id="main">'); z = tpl.index("</article>")
    head, tail = tpl[:a], tpl[z:]
    author = re.search(r'<section class="author-card".*?</section>', tpl, re.S).group(0)
    full = B + m["url"]
    cover = f'{IMG}{F["cover"][0]}{"-bn" if bn else ""}.webp'
    social = f'{B}{IMG}{SLUG}-social{"-bn" if bn else ""}.jpg'
    head = re.sub(r"<title>.*?</title>", f"<title>{html.escape(m['title'])} | Sayedul Abrar</title>", head, count=1, flags=re.S)
    def meta(attr, name, val):
        nonlocal head
        pat = rf'(<meta {attr}="{re.escape(name)}" content=")[^"]*(")'
        assert re.search(pat, head), name
        head = re.sub(pat, lambda x: x.group(1) + esc(val) + x.group(2), head, count=1)
    meta("name", "description", m["desc"]); meta("name", "keywords", m["kw"])
    meta("property", "article:published_time", DATE); meta("property", "article:modified_time", DATE)
    meta("property", "og:title", m["short"]); meta("property", "og:description", m["ogdesc"]); meta("property", "og:url", full)
    meta("property", "og:image", social); meta("property", "og:image:alt", m["short"]); meta("property", "og:image:width", "1200"); meta("property", "og:image:height", "630")
    meta("name", "twitter:title", m["short"]); meta("name", "twitter:description", m["ogdesc"]); meta("name", "twitter:image", social); meta("name", "twitter:image:alt", m["short"])
    head = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{full}">', head, count=1)
    head = re.sub(r'<link rel="alternate" hreflang="en" href="[^"]*"><link rel="alternate" hreflang="bn" href="[^"]*"><link rel="alternate" hreflang="x-default" href="[^"]*">',
                  f'<link rel="alternate" hreflang="en" href="{B}{EN_URL}"><link rel="alternate" hreflang="bn" href="{B}{BN_URL}"><link rel="alternate" hreflang="x-default" href="{B}{EN_URL}">', head, count=1)
    # JSON-LD
    imgs = [B + cover] + [f"{B}{IMG}{F[k][0]}{'-bn' if bn else ''}.webp" for k in F if k != "cover"]
    blog = {"@context": "https://schema.org", "@type": "BlogPosting", "@id": full + "#article", "headline": m["short"], "alternativeHeadline": m["h1"],
            "description": m["desc"], "inLanguage": "bn-BD" if bn else "en-BD", "articleSection": m["section"], "datePublished": DATE, "dateModified": DATE,
            "image": imgs, "thumbnailUrl": B + cover,
            "author": {"@type": "Person", "@id": B + "/#person", "name": "Sayedul Abrar", "url": B + "/about/", "jobTitle": "Pharmacist"},
            "publisher": {"@type": "Person", "@id": B + "/#person", "name": "Sayedul Abrar", "url": B + "/"},
            "mainEntityOfPage": {"@type": "WebPage", "@id": full}, "keywords": m["kw"], "isAccessibleForFree": True,
            "about": [{"@type": "Thing", "name": "Medical prescription"}, {"@type": "Thing", "name": "Prescription abbreviations"}],
            "audience": {"@type": "PeopleAudience", "audienceType": "General public"},
            "citation": [{"@type": "CreativeWork", "name": t, "url": u} for u, t, _ in REFS],
            "wordCount": len(txt(m["body"]).split()),
            "isPartOf": {"@type": "WebSite", "@id": B + "/#website", "url": B + "/", "name": "Sayedul Abrar"}}
    if bn: blog["translationOfWork"] = {"@id": B + EN_URL + "#article"}
    else: blog["workTranslation"] = {"@id": B + BN_URL + "#article"}
    faqld = {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": "bn-BD" if bn else "en-BD", "mainEntity": [{"@type": "Question", "name": txt(q), "acceptedAnswer": {"@type": "Answer", "text": txt(an)}} for q, an in m["faq"]]}
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": B + "/"}, {"@type": "ListItem", "position": 2, "name": "Pharma Blog", "item": B + "/blog/"},
        {"@type": "ListItem", "position": 3, "name": m["short"], "item": full}]}
    lds = re.findall(r'<script type="application/ld\+json">.*?</script>', head, re.S)
    assert len(lds) >= 2, len(lds)
    j = lambda d: '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + "</script>"
    head = head.replace(lds[0], j(blog) + j(faqld) + j(crumbs), 1)
    for extra in lds[1:]: head = head.replace(extra, "", 1)
    head = head.replace("</head>", STYLE + "</head>", 1)
    sw = ('<nav class="lang-switch" aria-label="Language">'
          f'<a{"" if bn else " class=\"active\""} href="{EN_URL}" lang="en">English</a><a{" class=\"active\"" if bn else ""} href="{BN_URL}" lang="bn">বাংলা</a></nav>')
    main = (f'<main id="main"><section class="page-head"><div class="wrap"><p class="eyebrow">{m["eyebrow"]}</p><h1>{m["h1"]}</h1><p>{m["lead"]}</p></div></section>'
            f'<section class="wrap"><article class="article-content">\n{sw}\n{fig("cover", bn, hero=True)}\n<p class="byline-seo">{m["by"]}</p>\n'
            f'{m["body"]}\n{refs(bn)}\n{m["disc"]}\n{author}\n{m["related"]}\n')
    out = head + main + tail
    for part in (head, tail):
        assert TPL not in part, "template slug leaked: " + part[part.index(TPL)-200:part.index(TPL)+50]
    out = re.sub(r"/assets/blog-related\.js\?v=[^\"]*", "/assets/blog-related.js?v=ae5-20261113", out)
    d = R / "blog" / (SLUG + ("-bangla" if bn else "")); d.mkdir(exist_ok=True)
    (d / "index.html").write_text(out, encoding="utf-8")
    print(lang, len(out), "words", blog["wordCount"], "desc", len(m["desc"]))

for L in ("en", "bn"): build(L)
