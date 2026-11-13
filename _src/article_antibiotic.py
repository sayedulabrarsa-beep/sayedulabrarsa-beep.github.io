#!/usr/bin/env python3
"""Builds /blog/why-complete-antibiotic-course-antibiotic-resistance/ (English) and its -bangla page,
using the how-do-medicines-work-in-the-body pages as the layout template. Run from the repo root."""
import re, json, html, pathlib
R = pathlib.Path(__file__).resolve().parent.parent
B = "https://sayedulabrar.site"
SLUG = "why-complete-antibiotic-course-antibiotic-resistance"
EN_URL, BN_URL = f"/blog/{SLUG}/", f"/blog/{SLUG}-bangla/"
DATE, DATE_EN, DATE_BN = "2026-11-13", "13 November 2026", "১৩ নভেম্বর ২০২৬"
IMG = "/assets/img/blog/antibiotic-course/"
TPL = "how-do-medicines-work-in-the-body"
esc = lambda x: html.escape(x, quote=True)

# key: (file stem, alt EN, caption EN, alt BN, caption BN)
F = {
 "cover": ("why-complete-antibiotic-course-cover-16x9",
   "Why you must complete an antibiotic course: teal-and-white capsules in a blister strip, a seven-day pill organiser and a glass of water on a pharmacy counter, with glowing bacteria above. By Sayedul Abrar, Pharmacist.",
   "Finish the course your doctor prescribed. AI-generated photo; no real product shown.",
   "অ্যান্টিবায়োটিক কোর্স শেষ করা কেন জরুরি: ফার্মেসির টেবিলে ব্লিস্টারে সাদা-সবুজ ক্যাপসুল, সাত দিনের পিল অর্গানাইজার, এক গ্লাস পানি এবং ওপরে ব্যাকটেরিয়ার ছবি। লিখেছেন ফার্মাসিস্ট সাইয়্যেদুল আবরার।",
   "ডাক্তার যতদিনের কোর্স দিয়েছেন, ততদিন শেষ করুন। AI দিয়ে তৈরি ছবি, কোনো আসল পণ্য নয়।"),
 "resistance": ("how-antibiotic-resistance-develops-simplified",
   "Rod-shaped bacteria in a petri dish (teal sensitive, red resistant, grey killed), with text explaining how antibiotic resistance develops in three simplified steps: an infection contains many bacteria and a few are less sensitive; the antibiotic kills the sensitive bacteria; the resistant survivors multiply and can spread. Resistance happens to the bacteria, not to your body.",
   "Simplified illustration based on WHO and MedlinePlus explanations.",
   "পেট্রি ডিশে দণ্ডাকার ব্যাকটেরিয়া (সবুজ সংবেদনশীল, লাল প্রতিরোধী, ধূসর মৃত), পাশে লেখা, অ্যান্টিবায়োটিক রেজিস্ট্যান্স কীভাবে তৈরি হয়, তিনটি সরল ধাপে: সংক্রমণে অনেক ব্যাকটেরিয়া থাকে, কয়েকটি কম সংবেদনশীল; অ্যান্টিবায়োটিক সংবেদনশীলগুলোকে মারে; প্রতিরোধী ব্যাকটেরিয়া টিকে গিয়ে বাড়ে ও ছড়াতে পারে। রেজিস্ট্যান্স হয় ব্যাকটেরিয়ার, শরীরের নয়।",
   "WHO ও MedlinePlus-এর ব্যাখ্যার ভিত্তিতে সরল চিত্র।"),
 "viruses": ("antibiotics-treat-bacteria-not-viruses-cold-flu",
   "A bedside table with tissues, a thermometer and hot tea, with text: antibiotics treat bacteria, not viruses. Antibiotics may be prescribed for bacterial infections, but they do not work on viral illnesses such as colds and flu.",
   "Based on CDC guidance.",
   "টিস্যু, থার্মোমিটার ও গরম চায়ের ছবির পাশে লেখা: অ্যান্টিবায়োটিক ব্যাকটেরিয়ার জন্য, ভাইরাসের জন্য নয়। ব্যাকটেরিয়াজনিত সংক্রমণে ডাক্তার অ্যান্টিবায়োটিক দিতে পারেন, কিন্তু সর্দি-কাশি বা ফ্লুর মতো ভাইরাসজনিত অসুখে এটি কাজ করে না।",
   "CDC-এর নির্দেশনার ভিত্তিতে।"),
 "dosdonts": ("antibiotic-dos-and-donts-take-as-prescribed",
   "A pharmacist's hands with a plain medicine box and capsules, beside a list of antibiotic do's and don'ts. Do: take them exactly as prescribed, finish the course unless your doctor says otherwise, take each dose on time, report side effects. Don't: stop early on your own, save leftovers, share them or take someone else's, or buy them without a prescription.",
   "Based on CDC, NHS and MedlinePlus advice.",
   "ফার্মাসিস্টের হাতে একটি সাদা ওষুধের বাক্স ও ক্যাপসুলের ছবির পাশে অ্যান্টিবায়োটিকের করণীয় ও বর্জনীয়। করণীয়: প্রেসক্রিপশন অনুযায়ী খান, ডাক্তার না বললে কোর্স শেষ করুন, সময়মতো ডোজ খান, পার্শ্বপ্রতিক্রিয়া জানান। বর্জনীয়: নিজে বন্ধ করা, বাকি ওষুধ রেখে দেওয়া, অন্যকে দেওয়া বা অন্যের ওষুধ খাওয়া, প্রেসক্রিপশন ছাড়া কেনা।",
   "CDC, NHS ও MedlinePlus-এর পরামর্শের ভিত্তিতে।"),
 "missed": ("missed-antibiotic-dose-what-to-do",
   "An alarm clock, a pill organiser and a glass of water, with advice for a missed antibiotic dose: take it as soon as you remember; if the next dose is almost due, skip the missed dose; never take a double dose; if unsure, ask your doctor or pharmacist.",
   "General advice from an NHS patient leaflet. Your own leaflet may differ.",
   "অ্যালার্ম ঘড়ি, পিল অর্গানাইজার ও পানির গ্লাসের ছবির পাশে লেখা, অ্যান্টিবায়োটিকের ডোজ মিস হলে: মনে পড়লেই খান; পরের ডোজের সময় প্রায় হয়ে গেলে বাদ পড়া ডোজটি বাদ দিন; কখনও দ্বিগুণ ডোজ নয়; নিশ্চিত না হলে ডাক্তার বা ফার্মাসিস্টকে জিজ্ঞেস করুন।",
   "NHS রোগী-তথ্য লিফলেটের সাধারণ পরামর্শ। আপনার ওষুধের লিফলেটে ভিন্ন নির্দেশনা থাকতে পারে।"),
 "redlabel": ("bangladesh-red-mark-on-antibiotic-packs-dgda",
   "A plain unbranded white medicine box with a red stripe beside a blister strip of capsules, with text explaining the DGDA decision to put a red identification mark and the warning 'Do not use without a prescription of registered physician' on antibiotic packs in Bangladesh from December 2022. Not a real product.",
   "AI-generated photo, not a real product. Source: WHO Bangladesh.",
   "লাল দাগওয়ালা একটি সাদা, নামহীন ওষুধের বাক্স ও ক্যাপসুলের ছবি। ডিসেম্বর ২০২২ থেকে বাংলাদেশে অ্যান্টিবায়োটিকের প্যাকে লাল চিহ্ন ও প্রেসক্রিপশন ছাড়া ব্যবহার না করার সতর্কবার্তা দেওয়ার DGDA সিদ্ধান্ত ব্যাখ্যা করা হয়েছে। আসল পণ্য নয়।",
   "AI দিয়ে তৈরি ছবি, আসল পণ্য নয়। সূত্র: WHO বাংলাদেশ।"),
 "sideeffects": ("antibiotic-side-effects-when-to-get-help",
   "A stethoscope and a glass of water on a doctor's desk, with a guide to antibiotic side effects and when to get help. Common: feeling or being sick, bloating or indigestion, diarrhoea. Tell your doctor: severe or watery diarrhoea, severe or worrying side effects, extra doses taken by mistake. Emergency: swelling of the face, lips or tongue, or difficulty breathing.",
   "Not a complete list. Check your own medicine leaflet.",
   "ডাক্তারের টেবিলে স্টেথোস্কোপ ও পানির গ্লাসের ছবির পাশে অ্যান্টিবায়োটিকের পার্শ্বপ্রতিক্রিয়া ও কখন সাহায্য নেবেন। সাধারণ: বমি ভাব বা বমি, পেট ফাঁপা বা বদহজম, পাতলা পায়খানা। ডাক্তারকে জানান: তীব্র বা পানির মতো পাতলা পায়খানা, তীব্র বা দুশ্চিন্তার পার্শ্বপ্রতিক্রিয়া, ভুল করে বাড়তি ডোজ। জরুরি: মুখ, ঠোঁট বা জিহ্বা ফুলে যাওয়া, শ্বাসকষ্ট।",
   "এটি পূর্ণ তালিকা নয়। নিজের ওষুধের লিফলেট দেখুন।"),
 "takeaways": ("antibiotics-key-takeaways",
   "A hand holding one teal-and-white capsule next to a glass of water, with five things to remember about antibiotics: finish the course unless your doctor says otherwise; use them only with a prescription; they do not work on colds and flu; do not save or share them; never double a missed dose.",
   "Five points to remember.",
   "হাতের তালুতে একটি ক্যাপসুল ও পানির গ্লাসের ছবির পাশে অ্যান্টিবায়োটিক নিয়ে পাঁচটি কথা: ডাক্তার না বললে কোর্স শেষ করুন; শুধু প্রেসক্রিপশনে খান; সর্দি-কাশি ও ফ্লুতে কাজ করে না; রেখে দেবেন না, ভাগ করবেন না; ডোজ মিস হলে দ্বিগুণ খাবেন না।",
   "মনে রাখার পাঁচটি কথা।"),
}
def fig(k, bn=False, hero=False):
    stem, aen, cen, abn, cbn = F[k]
    src = f"{IMG}{stem}{'-bn' if bn else ''}.webp?v=5"
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
 ("https://www.royalberkshire.nhs.uk/media/j2kn3hg3/antibiotics_jun25.pdf", "Royal Berkshire NHS Foundation Trust. Antibiotics, patient information leaflet (June 2025)", "finishing the course, missed doses, side effects, alcohol, when to get help."),
 ("https://www.nhs.uk/conditions/pneumonia/treatment/", "NHS. Pneumonia: treatment", "keep taking antibiotics until finished, even if you start to feel better."),
 ("https://www.cdc.gov/antibiotic-use/about/index.html", "U.S. Centers for Disease Control and Prevention (CDC). Healthy Habits: Antibiotic Do’s and Don’ts", "take as prescribed, do not save or share, antibiotics do not work on viruses."),
 ("https://www.medlineplus.gov/ency/patientinstructions/000959.htm", "MedlinePlus (U.S. National Library of Medicine). Using antibiotics wisely", "complete the course, never save, do not take antibiotics given to another person."),
 ("https://medlineplus.gov/ency/patientinstructions/000957.htm", "MedlinePlus. Antibiotic resistance", "what antibiotic resistance means."),
 ("https://www.who.int/news-room/fact-sheets/detail/antimicrobial-resistance", "World Health Organization. Antimicrobial resistance, fact sheet", "definition, burden and drivers of AMR."),
 ("https://www.who.int/news/item/13-10-2025-who-warns-of-widespread-resistance-to-common-antibiotics-worldwide", "World Health Organization. WHO warns of widespread resistance to common antibiotics worldwide (13 October 2025)", "GLASS 2025 report, 2023 data."),
 ("https://www.who.int/bangladesh/news/detail/07-03-2023-establishing-red-label-of-antibiotics-for-curbing-antimicrobial-resistance-in-bangladesh", "WHO Bangladesh. Establishing red label of antibiotics for curbing antimicrobial resistance in Bangladesh (7 March 2023)", "DGDA red identification mark from December 2022."),
 ("https://doi.org/10.1136/bmj.j3418", "Llewelyn MJ, et al. The antibiotic course has had its day. BMJ 2017;358:j3418", "analysis questioning the “complete the course” message."),
]
def refs(bn=False):
    li = "".join(f'<li>{t}. <a href="{u}" target="_blank" rel="noopener noreferrer">{u.split("//")[1].split("/")[0]}</a> — {n}</li>' for u, t, n in REFS)
    h = "সূত্র ও আরও পড়ুন" if bn else "References and further reading"
    note = ("<p><strong>সম্পাদকীয় নোট:</strong> সূত্রগুলো ১৩ নভেম্বর ২০২৬-এ দেখা হয়েছে। যুক্তরাজ্য ও যুক্তরাষ্ট্রের নির্দেশনা বাংলাদেশের প্রতিটি পণ্যের লেবেলের সঙ্গে হুবহু নাও মিলতে পারে, তাই নিজের প্রেসক্রিপশন ও প্যাকের লিফলেট মেনে চলুন।</p>" if bn else
            "<p><strong>Editorial note:</strong> Sources checked on 13 November 2026. UK and US guidance may not match every product label in Bangladesh word for word, so follow your own prescription and pack leaflet.</p>")
    return f'<section class="references"><h2>{h}</h2><ol>{li}</ol>{note}</section>'

# ================================================================= English
FAQ_EN = [
 ("Can I stop taking antibiotics when I feel better?", "Not on your own. NHS guidance says it is essential to finish the full prescribed course, even if you feel better, unless a healthcare professional tells you otherwise. If you think you need to stop, for example because of side effects, speak to your doctor or pharmacist first."),
 ("Is it true that some experts question the “complete the course” advice?", "Yes. A 2017 analysis in the BMJ argued that the message has little evidence behind it and that taking antibiotics for longer than needed may also add to resistance. It did not tell patients to stop early by themselves. The practical message is the same: the length of the course is your prescriber’s decision, so follow the prescription and ask before changing it."),
 ("Can I keep leftover antibiotics or give them to family?", "No. The CDC advises not to save antibiotics for later, not to share them and not to take antibiotics prescribed for someone else. MedlinePlus says never to save antibiotics. Ask your pharmacist how to dispose of any that are left."),
 ("Do antibiotics help a cold or the flu?", "No. The CDC says antibiotics do not work on viruses, such as those that cause colds and flu, and will not make you feel better if you have a virus."),
 ("What should I do if I miss a dose?", "An NHS leaflet says to take it as soon as you remember, unless the next dose is almost due, in which case skip the missed dose. Never take a double dose to make up for it. MedlinePlus advises asking your provider what to do, so check with your doctor or pharmacist if you are unsure."),
 ("Does my body become resistant to antibiotics?", "No. Antibiotic resistance means the bacteria no longer respond well to the antibiotic. It is the bacteria that change, not your body, but resistant bacteria can then cause infections that are harder to treat."),
 ("Can I drink alcohol while taking antibiotics?", "It depends on the antibiotic. The NHS leaflet notes that some antibiotics can react unpredictably with alcohol and other medicines. Read your medicine leaflet and ask your pharmacist."),
 ("How can I tell if a medicine is an antibiotic in Bangladesh?", "Look for the red identification mark. Following a DGDA decision, antibiotic packs from December 2022 should carry a red label reading “antibiotic” and the warning “Do not use without a prescription of registered physician” (WHO Bangladesh). You can also read the generic name on the pack."),
]
EN_BODY = f'''
<div class="quick"><strong>Quick answer:</strong> Finish your antibiotic course exactly as your doctor prescribed, even if you feel better, unless a doctor tells you to stop. Stopping on your own, skipping doses, saving leftovers or sharing them can leave an infection under-treated and adds to antibiotic resistance, which makes future infections harder to treat.</div>
<h2>A common story (illustrative, fictional)</h2>
<p>Karim, 38, is prescribed a seven-day antibiotic for a chest infection. By day three he feels much better, so he stops. He keeps the remaining tablets in a drawer, and a month later gives them to his brother for a cough. Each of those steps feels sensible. Each one goes against official advice. This is an example, not a real patient.</p>
<h2>What is an antibiotic, and what can it treat?</h2>
<p>An antibiotic is a medicine that treats infections caused by bacteria. It does not treat viruses. The CDC states that antibiotics do not work on viruses, such as those that cause colds and flu, and will not make you feel better if you have a virus. The CDC also notes that some common bacterial infections do not need antibiotics at all. That is why the decision belongs to a doctor, not to a fever or a cough on its own. If the words are confusing, my article on <a href="/blog/drug-vs-medicine/">drug vs medicine</a> explains the basics.</p>
{fig("viruses")}
<h2>What is antibiotic resistance?</h2>
<p>MedlinePlus describes antibiotic resistance as bacteria no longer responding well to one or more antibiotics. WHO defines the wider problem, antimicrobial resistance (AMR), as bacteria, viruses, fungi and parasites no longer responding to antimicrobial medicines. Two points are easy to miss:</p>
<ul><li><strong>It is the bacteria that become resistant, not your body.</strong></li><li><strong>Resistant bacteria can spread</strong> to other people, so one person’s misuse can affect a family or a community.</li></ul>
<p>WHO says that the misuse and overuse of antimicrobials are driving the development and spread of drug-resistant germs. MedlinePlus says the same about antibiotics.</p>
{fig("resistance")}
<h2>How big is the problem?</h2>
<p>According to WHO’s 2025 global surveillance report, one in six laboratory-confirmed bacterial infections worldwide was resistant to antibiotic treatment in 2023. Resistance was highest in WHO’s South-East Asia and Eastern Mediterranean regions, where one in three reported infections was resistant. Bangladesh is in WHO’s South-East Asia region, although regional figures do not describe any single country. The WHO fact sheet also estimates that bacterial AMR was associated with more than 4.7 million deaths globally in 2021.</p>
<h2>Why finish the course, even if you feel better?</h2>
<p>Official patient advice is consistent on this point:</p>
{table("What official sources say about finishing antibiotics", ["Source", "What it says"], [
 ["NHS patient leaflet (2025)", "It is essential to finish the full prescribed course, even if you feel better, unless a healthcare professional tells you otherwise."],
 ["NHS, pneumonia treatment", "If you are given antibiotics to take at home, keep taking them until you have finished them all, even if you start to feel better."],
 ["MedlinePlus", "It is important to complete the course of treatment. Never skip a dose."],
 ["CDC", "Take antibiotics exactly as prescribed."]])}
<p>Feeling better tells you the medicine is working. It does not tell you how long your particular infection needs treatment. Your doctor chose the dose and the number of days for your infection, and that is the plan to follow.</p>
<h2>What about the debate on shorter courses?</h2>
<p>To be fair to the science: in 2017, a group of UK infection specialists argued in the <em>BMJ</em> that the “complete the course” message has little evidence behind it, and that taking antibiotics for longer than needed may also add to resistance. That analysis is about how doctors and guidelines should set the length of treatment. It is not permission to stop early on your own.</p>
<p>The practical rule does not change: <strong>the length of the course is your prescriber’s decision.</strong> If your doctor prescribes a short course, that is fine. If you think you should stop, ask first.</p>
<h2>Antibiotic do’s and don’ts</h2>
{fig("dosdonts")}
{table("Antibiotic do's and don'ts", ["Do", "Don’t"], [
 ["Take them exactly as prescribed (CDC)", "Stop early on your own"],
 ["Finish the course unless a healthcare professional says otherwise (NHS)", "Save leftovers for later (CDC, MedlinePlus)"],
 ["Take each dose at the right time, as the label says", "Share them, or take antibiotics prescribed for someone else (CDC)"],
 ["Tell a healthcare professional about side effects (CDC)", "Buy them without a registered doctor’s prescription"]])}
<p>Keep the pack until you finish it. The pack shows the generic name, strength and expiry date. My guides on <a href="/blog/generic-name-vs-brand-name/">generic name vs brand name</a> and <a href="/blog/expiry-date-vs-manufacturing-date-medicine/">expiry date vs manufacturing date</a> show how to read them.</p>
<h2>What if you miss a dose?</h2>
<p>An NHS patient leaflet gives this general advice: take the missed dose as soon as you remember and carry on as normal. If the next dose is almost due, skip the missed one. Do not take a double dose to make up for it. MedlinePlus advises asking your provider what to do. Some antibiotics have specific timing rules, so your own leaflet and your pharmacist come first.</p>
{fig("missed")}
<h2>Side effects: when to get help</h2>
<p>The same NHS leaflet says most antibiotics do not cause problems when used properly and serious side effects are rare. Common ones include feeling or being sick, bloating or indigestion, and diarrhoea. Report severe or watery diarrhoea to your doctor. Swelling of the face or tongue and difficulty breathing can be signs of a serious allergic reaction, which is a medical emergency. If you have ever had an allergic reaction to an antibiotic, tell every doctor and pharmacist who treats you.</p>
{fig("sideeffects")}
<h2>In Bangladesh: look for the red mark</h2>
<p>WHO Bangladesh reports that the Drug Control Committee approved a “RED identification mark for antibiotics” for human and veterinary use, starting from December 2022. Manufacturers were asked to add a red label reading “antibiotic” and the message “Do not use without a prescription of registered physician” to every antibiotic pack. If you see the red mark, you are holding an antibiotic. Take it only with a registered doctor’s prescription.</p>
{fig("redlabel")}
<h2>What to do with leftover antibiotics</h2>
<p>If you follow the prescription, there should be little or nothing left. Leftovers usually mean doses were missed or the course was stopped early. Do not keep them for the next illness and do not give them to anyone else. MedlinePlus says never to save antibiotics and to dispose of leftovers as your local rules direct. Ask your pharmacist how to dispose of them safely where you live.</p>
<h2>Key takeaways</h2>
{fig("takeaways")}
<div class="takeaways"><ul><li>Finish the course as prescribed, unless a healthcare professional tells you otherwise.</li><li>Use antibiotics only with a registered doctor’s prescription.</li><li>Antibiotics do not work on colds and flu.</li><li>Do not save, share or borrow antibiotics.</li><li>Never take a double dose to make up for a missed one.</li></ul></div>
<h2>Frequently asked questions</h2>
{faq(FAQ_EN)}
'''

# ================================================================= Bangla
FAQ_BN = [
 ("ভালো লাগলে কি অ্যান্টিবায়োটিক বন্ধ করতে পারি?", "নিজে নিজে নয়। NHS-এর নির্দেশনা বলছে, ভালো লাগলেও প্রেসক্রিপশনের পুরো কোর্স শেষ করা জরুরি, যদি না কোনো স্বাস্থ্যকর্মী অন্য কথা বলেন। পার্শ্বপ্রতিক্রিয়া বা অন্য কারণে বন্ধ করতে চাইলে আগে ডাক্তার বা ফার্মাসিস্টের সঙ্গে কথা বলুন।"),
 ("কিছু বিশেষজ্ঞ কি “কোর্স শেষ করুন” পরামর্শ নিয়ে প্রশ্ন তুলেছেন?", "হ্যাঁ। ২০১৭ সালে BMJ-তে প্রকাশিত একটি বিশ্লেষণে বলা হয়, এই বার্তার পক্ষে প্রমাণ কম এবং প্রয়োজনের চেয়ে বেশি দিন অ্যান্টিবায়োটিক খাওয়াও রেজিস্ট্যান্স বাড়াতে পারে। তবে সেখানে রোগীদের নিজে থেকে আগেভাগে বন্ধ করতে বলা হয়নি। বাস্তব কথা একটাই: কোর্স কতদিনের হবে, তা ঠিক করবেন প্রেসক্রাইবার। তাই প্রেসক্রিপশন মেনে চলুন, বদলানোর আগে জিজ্ঞেস করুন।"),
 ("বাকি অ্যান্টিবায়োটিক কি রেখে দিতে বা পরিবারের কাউকে দিতে পারি?", "না। CDC পরামর্শ দেয়, অ্যান্টিবায়োটিক পরের জন্য রেখে দেবেন না, অন্যকে দেবেন না এবং অন্যের জন্য লেখা অ্যান্টিবায়োটিক খাবেন না। MedlinePlus বলছে, কখনও অ্যান্টিবায়োটিক জমিয়ে রাখবেন না। বাকি ওষুধ কীভাবে ফেলবেন, ফার্মাসিস্টকে জিজ্ঞেস করুন।"),
 ("সর্দি-কাশি বা ফ্লুতে কি অ্যান্টিবায়োটিক কাজ করে?", "না। CDC বলছে, সর্দি-কাশি ও ফ্লুর মতো ভাইরাসে অ্যান্টিবায়োটিক কাজ করে না এবং ভাইরাসজনিত অসুখে এটি খেয়ে আপনি ভালো বোধ করবেন না।"),
 ("একটি ডোজ মিস হলে কী করব?", "NHS-এর একটি লিফলেট বলছে, মনে পড়ার সঙ্গে সঙ্গে খেয়ে নিন, তবে পরের ডোজের সময় প্রায় হয়ে গেলে বাদ পড়া ডোজটি বাদ দিন। পূরণ করতে কখনও দ্বিগুণ ডোজ খাবেন না। MedlinePlus পরামর্শ দেয় চিকিৎসকের কাছে জেনে নিতে, তাই নিশ্চিত না হলে ডাক্তার বা ফার্মাসিস্টকে জিজ্ঞেস করুন।"),
 ("আমার শরীর কি অ্যান্টিবায়োটিকের প্রতি প্রতিরোধী হয়ে যায়?", "না। অ্যান্টিবায়োটিক রেজিস্ট্যান্স মানে ব্যাকটেরিয়া আর অ্যান্টিবায়োটিকে ঠিকমতো সাড়া দেয় না। বদলায় ব্যাকটেরিয়া, শরীর নয়। তবে প্রতিরোধী ব্যাকটেরিয়া এমন সংক্রমণ ঘটাতে পারে, যার চিকিৎসা কঠিন।"),
 ("অ্যান্টিবায়োটিক খাওয়ার সময় কি অ্যালকোহল চলে?", "অ্যান্টিবায়োটিকের ধরনের ওপর নির্ভর করে। NHS-এর লিফলেটে বলা আছে, কিছু অ্যান্টিবায়োটিক অ্যালকোহল ও অন্য ওষুধের সঙ্গে অপ্রত্যাশিত প্রতিক্রিয়া করতে পারে। ওষুধের লিফলেট পড়ুন এবং ফার্মাসিস্টকে জিজ্ঞেস করুন।"),
 ("বাংলাদেশে কোনো ওষুধ অ্যান্টিবায়োটিক কি না, কীভাবে বুঝব?", "লাল চিহ্ন দেখুন। DGDA-এর সিদ্ধান্ত অনুযায়ী ডিসেম্বর ২০২২ থেকে অ্যান্টিবায়োটিকের প্যাকে “antibiotic” লেখা লাল লেবেল এবং “রেজিস্টার্ড চিকিৎসকের প্রেসক্রিপশন ছাড়া ব্যবহার করবেন না” ধরনের সতর্কবার্তা থাকার কথা (WHO বাংলাদেশ)। প্যাকে লেখা জেনেরিক নামও দেখে নিতে পারেন।"),
]
BN_BODY = f'''
<div class="quick"><strong>সহজ উত্তর:</strong> ডাক্তার যেভাবে লিখেছেন, ঠিক সেভাবে অ্যান্টিবায়োটিকের পুরো কোর্স শেষ করুন, ভালো লাগলেও। শুধু ডাক্তার বললে আগে বন্ধ করবেন। নিজে থেকে বন্ধ করা, ডোজ বাদ দেওয়া, বাকি ওষুধ রেখে দেওয়া বা অন্যকে দেওয়া সংক্রমণ পুরোপুরি না সারার ঝুঁকি তৈরি করে এবং অ্যান্টিবায়োটিক রেজিস্ট্যান্স বাড়ায়, ফলে ভবিষ্যতের সংক্রমণ সারানো কঠিন হয়।</div>
<h2>একটি পরিচিত গল্প (উদাহরণমূলক, কাল্পনিক)</h2>
<p>৩৮ বছরের করিম বুকের সংক্রমণের জন্য সাত দিনের অ্যান্টিবায়োটিক পেলেন। তৃতীয় দিনেই অনেক ভালো লাগায় তিনি ওষুধ বন্ধ করে দিলেন। বাকি ট্যাবলেট ড্রয়ারে রেখে দিলেন, এক মাস পর ভাইয়ের কাশির জন্য সেগুলো দিয়ে দিলেন। প্রতিটি কাজই তাঁর কাছে যুক্তিসংগত মনে হয়েছে, কিন্তু প্রতিটিই সরকারি পরামর্শের উল্টো। এটি একটি উদাহরণ, কোনো বাস্তব রোগী নন।</p>
<h2>অ্যান্টিবায়োটিক কী, আর কোন অসুখে কাজ করে?</h2>
<p>অ্যান্টিবায়োটিক এমন ওষুধ, যা ব্যাকটেরিয়াজনিত সংক্রমণের চিকিৎসা করে। ভাইরাসে এটি কাজ করে না। CDC বলছে, সর্দি-কাশি ও ফ্লুর মতো ভাইরাসে অ্যান্টিবায়োটিক কাজ করে না, আর ভাইরাসজনিত অসুখে এটি খেয়ে আপনি ভালোও বোধ করবেন না। CDC আরও বলছে, কিছু সাধারণ ব্যাকটেরিয়াজনিত সংক্রমণেও অ্যান্টিবায়োটিক লাগে না। তাই জ্বর বা কাশি দেখে নিজে সিদ্ধান্ত নয়, সিদ্ধান্ত নেবেন ডাক্তার। শব্দগুলো গুলিয়ে গেলে আমার <a href="/blog/drug-vs-medicine-bangla/">ড্রাগ বনাম মেডিসিন</a> লেখাটি পড়ে নিতে পারেন।</p>
{fig("viruses", True)}
<h2>অ্যান্টিবায়োটিক রেজিস্ট্যান্স কী?</h2>
<p>MedlinePlus-এর ব্যাখ্যায়, অ্যান্টিবায়োটিক রেজিস্ট্যান্স মানে ব্যাকটেরিয়া এক বা একাধিক অ্যান্টিবায়োটিকে আর ঠিকমতো সাড়া দেয় না। WHO বড় পরিসরের সমস্যাটিকে বলে অ্যান্টিমাইক্রোবিয়াল রেজিস্ট্যান্স (AMR), যখন ব্যাকটেরিয়া, ভাইরাস, ছত্রাক ও পরজীবী জীবাণুনাশক ওষুধে আর সাড়া দেয় না। দুটি বিষয় অনেকেই ভুল বোঝেন:</p>
<ul><li><strong>প্রতিরোধী হয় ব্যাকটেরিয়া, আপনার শরীর নয়।</strong></li><li><strong>প্রতিরোধী ব্যাকটেরিয়া অন্যের শরীরে ছড়াতে পারে।</strong> তাই একজনের ভুল ব্যবহার পুরো পরিবার বা এলাকার ওপর প্রভাব ফেলতে পারে।</li></ul>
<p>WHO বলছে, জীবাণুনাশক ওষুধের অপব্যবহার ও অতিরিক্ত ব্যবহারই প্রতিরোধী জীবাণু তৈরি ও ছড়িয়ে পড়ার প্রধান চালিকাশক্তি। অ্যান্টিবায়োটিক নিয়ে MedlinePlus-ও একই কথা বলে।</p>
{fig("resistance", True)}
<h2>সমস্যাটি কত বড়?</h2>
<p>WHO-এর ২০২৫ সালের বৈশ্বিক নজরদারি প্রতিবেদন অনুযায়ী, ২০২৩ সালে বিশ্বজুড়ে ল্যাবে নিশ্চিত হওয়া প্রতি ছয়টি ব্যাকটেরিয়াজনিত সংক্রমণের একটি অ্যান্টিবায়োটিকে প্রতিরোধী ছিল। WHO-এর দক্ষিণ-পূর্ব এশিয়া ও পূর্ব ভূমধ্যসাগরীয় অঞ্চলে হার সবচেয়ে বেশি, সেখানে প্রতি তিনটির একটি সংক্রমণ প্রতিরোধী পাওয়া গেছে। বাংলাদেশ WHO-এর দক্ষিণ-পূর্ব এশিয়া অঞ্চলের অন্তর্ভুক্ত, যদিও আঞ্চলিক হিসাব কোনো একক দেশের চিত্র নয়। WHO-এর ফ্যাক্ট শিট অনুযায়ী, ২০২১ সালে বিশ্বে ৪৭ লাখের বেশি মৃত্যুর সঙ্গে ব্যাকটেরিয়ার AMR জড়িত ছিল বলে অনুমান করা হয়।</p>
<h2>ভালো লাগলেও কোর্স শেষ করবেন কেন?</h2>
<p>এ বিষয়ে রোগীদের জন্য সরকারি পরামর্শ একই রকম:</p>
{table("অ্যান্টিবায়োটিক কোর্স শেষ করা নিয়ে সরকারি সূত্র কী বলে", ["সূত্র", "কী বলা হয়েছে"], [
 ["NHS রোগী-তথ্য লিফলেট (২০২৫)", "ভালো লাগলেও প্রেসক্রিপশনের পুরো কোর্স শেষ করা জরুরি, যদি না স্বাস্থ্যকর্মী অন্য কথা বলেন।"],
 ["NHS, নিউমোনিয়ার চিকিৎসা", "বাড়িতে খাওয়ার জন্য অ্যান্টিবায়োটিক দেওয়া হলে, ভালো লাগতে শুরু করলেও সব শেষ না হওয়া পর্যন্ত খেতে থাকুন।"],
 ["MedlinePlus", "চিকিৎসার কোর্স শেষ করা গুরুত্বপূর্ণ। কখনও ডোজ বাদ দেবেন না।"],
 ["CDC", "প্রেসক্রিপশনে যেভাবে লেখা, ঠিক সেভাবে অ্যান্টিবায়োটিক খান।"]])}
<p>ভালো লাগা মানে ওষুধ কাজ করছে। কিন্তু আপনার সংক্রমণে কতদিন চিকিৎসা লাগবে, তা এতে বোঝা যায় না। ডাক্তার আপনার সংক্রমণ বুঝে ডোজ ও দিনের সংখ্যা ঠিক করেছেন, সেই পরিকল্পনাই মেনে চলুন।</p>
<h2>ছোট কোর্স নিয়ে বিতর্কের কী হবে?</h2>
<p>বিজ্ঞানের প্রতি সৎ থাকতে বলি: ২০১৭ সালে যুক্তরাজ্যের একদল সংক্রমণ বিশেষজ্ঞ <em>BMJ</em>-তে যুক্তি দেন যে “কোর্স শেষ করুন” বার্তার পক্ষে প্রমাণ কম, এবং প্রয়োজনের চেয়ে বেশি দিন অ্যান্টিবায়োটিক খাওয়াও রেজিস্ট্যান্স বাড়াতে পারে। এই বিশ্লেষণ ডাক্তার ও গাইডলাইন কীভাবে চিকিৎসার মেয়াদ ঠিক করবে, সে বিষয়ে। নিজে থেকে আগেভাগে ওষুধ বন্ধ করার অনুমতি এটি নয়।</p>
<p>বাস্তব নিয়ম তাই একই থাকে: <strong>কোর্স কতদিনের হবে, তা ঠিক করবেন প্রেসক্রাইবার।</strong> ডাক্তার ছোট কোর্স দিলে সেটাই ঠিক। বন্ধ করা উচিত মনে হলে আগে জিজ্ঞেস করুন।</p>
<h2>অ্যান্টিবায়োটিকের করণীয় ও বর্জনীয়</h2>
{fig("dosdonts", True)}
{table("অ্যান্টিবায়োটিকের করণীয় ও বর্জনীয়", ["করণীয়", "বর্জনীয়"], [
 ["প্রেসক্রিপশনে যেভাবে লেখা, ঠিক সেভাবে খান (CDC)", "নিজে থেকে মাঝপথে বন্ধ করা"],
 ["স্বাস্থ্যকর্মী অন্য কথা না বললে কোর্স শেষ করুন (NHS)", "বাকি ওষুধ পরের জন্য রেখে দেওয়া (CDC, MedlinePlus)"],
 ["লেবেল অনুযায়ী প্রতিটি ডোজ সঠিক সময়ে খান", "অন্যকে দেওয়া, বা অন্যের জন্য লেখা অ্যান্টিবায়োটিক খাওয়া (CDC)"],
 ["পার্শ্বপ্রতিক্রিয়া হলে স্বাস্থ্যকর্মীকে জানান (CDC)", "রেজিস্টার্ড ডাক্তারের প্রেসক্রিপশন ছাড়া কেনা"]])}
<p>কোর্স শেষ না হওয়া পর্যন্ত প্যাকটি রেখে দিন। প্যাকে জেনেরিক নাম, শক্তি ও মেয়াদের তারিখ লেখা থাকে। কীভাবে পড়বেন, তা আমার <a href="/blog/generic-name-vs-brand-name-bangla/">জেনেরিক নাম বনাম ব্র্যান্ড নাম</a> এবং <a href="/blog/expiry-date-vs-manufacturing-date-medicine-bangla/">মেয়াদ শেষের তারিখ ও উৎপাদনের তারিখ</a> লেখায় দেখানো আছে।</p>
<h2>ডোজ মিস হলে কী করবেন?</h2>
<p>NHS-এর একটি রোগী-তথ্য লিফলেটে সাধারণ পরামর্শ: মনে পড়ার সঙ্গে সঙ্গে বাদ পড়া ডোজটি খেয়ে নিন, তারপর আগের মতো চালিয়ে যান। পরের ডোজের সময় প্রায় হয়ে গেলে বাদ পড়া ডোজটি বাদ দিন। পূরণ করতে দ্বিগুণ ডোজ খাবেন না। MedlinePlus বলছে চিকিৎসকের কাছে জেনে নিতে। কিছু অ্যান্টিবায়োটিকের সময় নিয়ে আলাদা নিয়ম থাকে, তাই আপনার ওষুধের লিফলেট ও ফার্মাসিস্টের কথাই আগে।</p>
{fig("missed", True)}
<h2>পার্শ্বপ্রতিক্রিয়া: কখন সাহায্য নেবেন</h2>
<p>একই NHS লিফলেট বলছে, ঠিকভাবে ব্যবহার করলে বেশির ভাগ অ্যান্টিবায়োটিকে সমস্যা হয় না, গুরুতর পার্শ্বপ্রতিক্রিয়া বিরল। সাধারণ পার্শ্বপ্রতিক্রিয়ার মধ্যে আছে বমি ভাব বা বমি, পেট ফাঁপা বা বদহজম এবং পাতলা পায়খানা। তীব্র বা পানির মতো পাতলা পায়খানা হলে ডাক্তারকে জানান। মুখ বা জিহ্বা ফুলে যাওয়া ও শ্বাসকষ্ট গুরুতর অ্যালার্জির লক্ষণ হতে পারে, যা জরুরি অবস্থা। কোনো অ্যান্টিবায়োটিকে আগে অ্যালার্জি হয়ে থাকলে প্রত্যেক ডাক্তার ও ফার্মাসিস্টকে তা জানান।</p>
{fig("sideeffects", True)}
<h2>বাংলাদেশে: লাল চিহ্ন খেয়াল করুন</h2>
<p>WHO বাংলাদেশ জানিয়েছে, ড্রাগ কন্ট্রোল কমিটি মানুষ ও প্রাণীর জন্য অ্যান্টিবায়োটিকে “লাল শনাক্তকরণ চিহ্ন” অনুমোদন করেছে, যা ডিসেম্বর ২০২২ থেকে কার্যকর। প্রস্তুতকারকদের প্রতিটি অ্যান্টিবায়োটিকের প্যাকে “antibiotic” লেখা লাল লেবেল এবং “Do not use without a prescription of registered physician” (রেজিস্টার্ড চিকিৎসকের প্রেসক্রিপশন ছাড়া ব্যবহার করবেন না) বার্তা দিতে বলা হয়েছে। প্যাকে লাল চিহ্ন দেখলে বুঝবেন এটি অ্যান্টিবায়োটিক। শুধু রেজিস্টার্ড চিকিৎসকের প্রেসক্রিপশনেই খাবেন।</p>
{fig("redlabel", True)}
<h2>বাকি অ্যান্টিবায়োটিক কী করবেন?</h2>
<p>প্রেসক্রিপশন মেনে খেলে বাকি থাকার কথা নয়, থাকলেও খুব কম। বাকি থাকা মানে সাধারণত ডোজ বাদ গেছে বা কোর্স আগেই বন্ধ হয়েছে। পরের অসুখের জন্য রেখে দেবেন না, কাউকে দেবেন না। MedlinePlus বলছে, কখনও অ্যান্টিবায়োটিক জমিয়ে রাখবেন না এবং স্থানীয় নিয়ম অনুযায়ী ফেলে দিন। আপনার এলাকায় নিরাপদে কীভাবে ফেলবেন, ফার্মাসিস্টকে জিজ্ঞেস করুন।</p>
<h2>মূল কথা</h2>
{fig("takeaways", True)}
<div class="takeaways"><ul><li>স্বাস্থ্যকর্মী অন্য কথা না বললে প্রেসক্রিপশন অনুযায়ী পুরো কোর্স শেষ করুন।</li><li>শুধু রেজিস্টার্ড ডাক্তারের প্রেসক্রিপশনে অ্যান্টিবায়োটিক খান।</li><li>সর্দি-কাশি ও ফ্লুতে অ্যান্টিবায়োটিক কাজ করে না।</li><li>অ্যান্টিবায়োটিক রেখে দেবেন না, অন্যকে দেবেন না, অন্যেরটা খাবেন না।</li><li>ডোজ মিস হলে কখনও দ্বিগুণ খাবেন না।</li></ul></div>
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
   title="Why Complete an Antibiotic Course? Resistance Explained",
   h1="Why You Must Complete an Antibiotic Course (and How Antibiotic Resistance Starts)",
   short="Why You Must Complete an Antibiotic Course",
   desc="Why finish an antibiotic course even if you feel better? A pharmacist explains antibiotic resistance, missed doses, leftovers and Bangladesh's red label.",
   ogdesc="Finish the course, don't save or share antibiotics, and why resistance matters. A pharmacist explains with NHS, CDC and WHO sources.",
   kw="complete antibiotic course, finish antibiotics even if you feel better, antibiotic resistance, antimicrobial resistance, missed antibiotic dose, leftover antibiotics, antibiotics cold flu, red label antibiotic Bangladesh, DGDA antibiotic, pharmacist Sayedul Abrar",
   eyebrow="PHARMA BLOG · ANTIBIOTICS · 8 MIN READ", lead="Why finishing the prescribed course matters, and how antibiotic resistance starts.",
   by=f'By <a href="/about/" rel="author">Sayedul Abrar</a>, pharmacist · Published <time datetime="{DATE}">{DATE_EN}</time>',
   body=EN_BODY, faq=FAQ_EN, section="Medicine Safety",
   disc='<div class="disclaimer"><strong>Educational disclaimer:</strong> This article is for general learning and is not personal medical advice. Do not start, stop or change an antibiotic or its dose based only on this article. Follow your prescription and consult a registered doctor or pharmacist.</div>',
   related=('<section class="related"><h2>Continue learning</h2><div class="related-track">'
     '<a class="related-card" href="/blog/generic-name-vs-brand-name/"><strong>Generic Name vs Brand Name</strong><span>Find the active ingredient on any medicine pack.</span></a>'
     '<a class="related-card" href="/blog/expiry-date-vs-manufacturing-date-medicine/"><strong>Expiry Date vs Manufacturing Date</strong><span>Read the dates on a medicine pack in seconds.</span></a>'
     '<a class="related-card" href="/blog/drug-vs-medicine/"><strong>Drug vs Medicine</strong><span>What the two words really mean in pharmacy.</span></a>'
     '<a class="related-card" href="/blog/how-do-medicines-work-in-the-body/"><strong>How Do Medicines Work in the Body?</strong><span>The journey of a medicine, explained simply.</span></a></div></section>')),
 "bn": dict(url=BN_URL, lang="bn", locale="bn_BD",
   title="অ্যান্টিবায়োটিক কোর্স শেষ করা কেন জরুরি? রেজিস্ট্যান্স সহজ ভাষায়",
   h1="অ্যান্টিবায়োটিক কোর্স শেষ করা কেন জরুরি? (অ্যান্টিবায়োটিক রেজিস্ট্যান্স কীভাবে শুরু হয়)",
   short="অ্যান্টিবায়োটিক কোর্স শেষ করা কেন জরুরি?",
   desc="ভালো লাগলেও অ্যান্টিবায়োটিক কোর্স কেন শেষ করবেন? রেজিস্ট্যান্স, ডোজ মিস, বাকি ওষুধ, পার্শ্বপ্রতিক্রিয়া ও প্যাকের লাল চিহ্ন নিয়ে ফার্মাসিস্টের সহজ গাইড।",
   ogdesc="কোর্স শেষ করুন, অ্যান্টিবায়োটিক রেখে দেবেন না বা কাউকে দেবেন না, আর রেজিস্ট্যান্স কেন বিপজ্জনক। NHS, CDC ও WHO-এর সূত্রসহ।",
   kw="অ্যান্টিবায়োটিক কোর্স শেষ করা কেন জরুরি, অ্যান্টিবায়োটিক রেজিস্ট্যান্স, অ্যান্টিবায়োটিক খাওয়ার নিয়ম, অ্যান্টিবায়োটিক ডোজ মিস, অ্যান্টিবায়োটিক লাল চিহ্ন, সর্দি কাশিতে অ্যান্টিবায়োটিক, antibiotic course Bangla",
   eyebrow="PHARMA BLOG · অ্যান্টিবায়োটিক · ৮ মিনিটে পড়ুন", lead="প্রেসক্রিপশনের পুরো কোর্স শেষ করা কেন জরুরি, আর অ্যান্টিবায়োটিক রেজিস্ট্যান্স কীভাবে শুরু হয়।",
   by=f'লিখেছেন <a href="/about/" rel="author">Sayedul Abrar</a>, ফার্মাসিস্ট · প্রকাশিত <time datetime="{DATE}">{DATE_BN}</time>',
   body=BN_BODY, faq=FAQ_BN, section="ওষুধের নিরাপত্তা",
   disc='<div class="disclaimer"><strong>শিক্ষামূলক সতর্কতা:</strong> এই লেখাটি সাধারণ জ্ঞানের জন্য, ব্যক্তিগত চিকিৎসা পরামর্শ নয়। শুধু এই লেখা পড়ে কোনো অ্যান্টিবায়োটিক শুরু, বন্ধ বা ডোজ পরিবর্তন করবেন না। প্রেসক্রিপশন মেনে চলুন এবং রেজিস্টার্ড ডাক্তার বা ফার্মাসিস্টের পরামর্শ নিন।</div>',
   related=('<section class="related"><h2>আরও পড়ুন</h2><div class="related-track">'
     '<a class="related-card" href="/blog/generic-name-vs-brand-name-bangla/"><strong>জেনেরিক নাম বনাম ব্র্যান্ড নাম</strong><span>ওষুধের প্যাকে উপাদানের নাম খুঁজে নিন।</span></a>'
     '<a class="related-card" href="/blog/expiry-date-vs-manufacturing-date-medicine-bangla/"><strong>মেয়াদ শেষের তারিখ ও উৎপাদনের তারিখ</strong><span>ওষুধের প্যাকের তারিখ সহজে পড়ুন।</span></a>'
     '<a class="related-card" href="/blog/drug-vs-medicine-bangla/"><strong>ড্রাগ বনাম মেডিসিন</strong><span>ফার্মেসিতে শব্দ দুটির আসল অর্থ।</span></a>'
     '<a class="related-card" href="/blog/how-do-medicines-work-in-the-body-bangla/"><strong>মানবদেহে ওষুধ কীভাবে কাজ করে?</strong><span>ওষুধের যাত্রা সহজ ভাষায়।</span></a></div></section>')),
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
            "about": [{"@type": "MedicalCondition", "name": "Antimicrobial resistance"}, {"@type": "DrugClass", "name": "Antibiotics"}],
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
