#!/usr/bin/env python3
"""Pharmacovigilance article (EN+BN): place the 12 pictures with legends/captions written in code, add Key takeaways, update head/schema."""
import re, json, html, pathlib
R = pathlib.Path(__file__).resolve().parent.parent.parent
SITE = "https://sayedulabrar.site"; IMG = "/assets/img/blog/pharmacovigilance/"
def esc(s): return html.escape(s, quote=True)

# key -> (alt, caption, kind, items)   kind: ol (sequence) | ul (tags) | two | flow
EN = {
 "cover": ("A pharmacist on a watchtower looks through a large magnifying glass over a town, with medicines nearby and a safety shield above.",
           "Medicine safety monitoring continues beyond the point of regulatory approval.", None, []),
 "why": ("Two scenes side by side: a small, selected group with a doctor in a clinic, then a large and varied crowd of children, pregnant women, older adults and families.",
         "Trials study a limited group. Real-world use reaches many more kinds of people.", "two",
         [("Before approval", "A limited, carefully selected group in controlled trials."), ("After approval", "Many more people, with different ages, illnesses and medicines.")]),
 "types": ("Five kinds of medicine-safety concern shown as icons around a medicine pack: a skin reaction, a vaccine event, a medicine mix-up, a damaged tablet and a tablet that seems to have no effect.",
           "Five kinds of concern that may be reported. A suspicion is enough; proof is not needed.", "ul",
           [("Suspected reaction", "an unwanted effect of a medicine"), ("Vaccine event (AEFI)", "a health event after vaccination"), ("Medication error", "a mistake in prescribing, dispensing or use"),
            ("Product-quality concern", "damaged, contaminated or wrongly labelled product"), ("Unusual lack of effect", "the product does not seem to work as expected")]),
 "cycle": ("Original picture of the pharmacovigilance cycle: six icons in a ring around a medicine pack with a shield, with arrows showing the direction.",
           "The cycle turns individual observations into learning, decisions and follow-up.", "ol",
           [("Notice", "a patient or professional sees a possible problem"), ("Document and report", "write down the facts and send them"), ("Assess the case", "check completeness, seriousness and clinical details"),
            ("Look for patterns", "signal detection across similar cases"), ("Evaluate risk, act and communicate", "choose a proportionate response"), ("Keep monitoring", "new reports show whether the action works")]),
 "signal": ("Grey dots drift towards a magnifying glass where orange dots cluster, beside three patient case report cards.",
            "A signal is a prompt to investigate, not proof of harm.", "ol",
            [("Reports arrive", "scattered cases from many places"), ("A pattern stands out", "reviewers look more closely"), ("Cases are checked", "a signal is a question, not a verdict")]),
 "causality": ("A person takes a tablet, time passes on a calendar, and later they feel unwell. Below, a magnifying glass lies over four clues: timing, stopping the medicine, other medicines and other possible causes.",
               "Timing alone does not prove cause. Reviewers weigh several clues together.", "ul",
               [("Timing", "when the medicine started and when the event began"), ("Stopping the medicine", "did the problem improve afterwards?"), ("Other medicines", "co-medications and doses"), ("Other possible causes", "illness, history and tests")]),
 "benefit": ("A balance scale compares a medicine's benefit with a possible risk. Below it, four steps rise like a staircase: keep watching, review evidence, communicate warnings, and change how the product is used.",
             "The response should match the evidence and the seriousness of the risk.", "ol",
             [("Keep monitoring", "watch for new reports"), ("Review more evidence", "studies and data"), ("Communicate new warnings", "update information and advice"), ("Change use if needed", "restrict, suspend or recall")]),
 "bd": ("Four report sources (a patient, a pharmacist or doctor, a hospital and another health facility) feed into a government office and then a national safety database.",
        "A simplified view of reporting in Bangladesh. Check the latest DGDA instructions before relying on any timeframe.", "flow",
        [("Patients and consumers", ""), ("Doctors, nurses and pharmacists", ""), ("Hospitals and clinics", "use the PV focal point where one exists"), ("Other health facilities", ""),
         ("DGDA · ADRM Cell", "national review"), ("National database", "WHO-UMC VigiFlow")]),
 "info": ("A clipboard report form with rows for the patient, the event, the suspected product, other medicines and reporter contact, with a padlock for privacy.",
          "A structured report supports follow-up and assessment. Share personal information only through authorised reporting channels.", "ul",
          [("Patient", "identifier, age, sex where relevant"), ("Event", "symptoms, dates, outcome"), ("Suspected product and dose", "name, strength, batch if known"),
           ("Other medicines and history", "what else was taken"), ("Reporter contact", "so reviewers can follow up"), ("Privacy", "use authorised channels only")]),
 "industry": ("A pharmaceutical company building with a staff member at a desk of case files, and a balance scale that weighs a safety shield against a sales chart.",
              "Safety information must be recorded and passed on, whatever the commercial pressure.", "ol",
              [("Receive and record", "every report, however informal"), ("Pass it on promptly", "to the responsible PV team"), ("Safety before targets", "sales goals never decide what is reported")]),
 "people": ("A patient reading a medicine leaflet with a doctor and a pharmacist beside a safety shield, with five icons below: write it down, medicine and timing, symptoms, talk to a professional, and report.",
            "Patients and professionals both help. Urgent symptoms always need care first.", "ul",
            [("Write down what happened", ""), ("Note medicine, dose and timing", ""), ("Watch symptoms", "get urgent help if severe"), ("Talk to a doctor or pharmacist", ""), ("Report through the right channel", "")]),
 "key": ("A staircase of five steps leading up to a shield: a medicine, a magnifying glass with an alert, a checklist, a group of people and a rising chart.",
         "Five ideas to take away.", "ol",
         [("Watched after approval", "medicines are monitored in real-world use"), ("Report without proof", "a suspected problem is enough"), ("Checked and assessed", "reports are reviewed, not just collected"),
          ("Everyone takes part", "patients, professionals, companies and regulators"), ("Evidence guides action", "responses are proportionate to the risk")]),
}
BN = {
 "cover": ("একটি পর্যবেক্ষণ-টাওয়ার থেকে ফার্মাসিস্ট বড় ম্যাগনিফাইং গ্লাসে শহরের দিকে তাকিয়ে আছেন; কাছে ওষুধ এবং ওপরে একটি নিরাপত্তা-ঢাল।",
           "ওষুধের নিরাপত্তা পর্যবেক্ষণ একটি চলমান প্রক্রিয়া—শুধু অনুমোদনের সময়ের পরীক্ষা নয়।", None, []),
 "why": ("পাশাপাশি দুটি দৃশ্য: ক্লিনিকে ডাক্তারসহ ছোট ও বাছাই করা একদল মানুষ, তারপর শিশু, গর্ভবতী নারী, বয়স্ক মানুষ ও পরিবারসহ বিশাল ও বৈচিত্র্যময় জনসমাগম।",
         "ট্রায়ালে সীমিত একদল মানুষকে দেখা হয়। বাস্তব ব্যবহারে ওষুধ আরও অনেক ধরনের মানুষের কাছে পৌঁছায়।", "two",
         [("অনুমোদনের আগে", "নিয়ন্ত্রিত ট্রায়ালে সীমিত, বাছাই করা একদল মানুষ।"), ("অনুমোদনের পরে", "অনেক বেশি মানুষ—ভিন্ন বয়স, অসুখ ও ওষুধ।")]),
 "types": ("ওষুধের প্যাকের চারপাশে পাঁচটি আইকনে ওষুধ-নিরাপত্তার পাঁচ ধরনের উদ্বেগ: ত্বকের প্রতিক্রিয়া, টিকার পর ঘটনা, ওষুধের গরমিল, ভাঙা ট্যাবলেট এবং কাজ না করা মনে হওয়া ট্যাবলেট।",
           "পাঁচ ধরনের উদ্বেগ রিপোর্ট করা যেতে পারে। সন্দেহই যথেষ্ট; প্রমাণ লাগে না।", "ul",
           [("সন্দেহজনক প্রতিক্রিয়া", "ওষুধের অনাকাঙ্ক্ষিত প্রভাব"), ("টিকার পর ঘটনা (AEFI)", "টিকা নেওয়ার পর স্বাস্থ্য-ঘটনা"), ("ওষুধ-সংক্রান্ত ভুল", "প্রেসক্রিপশন, বিতরণ বা ব্যবহারে ভুল"),
            ("পণ্যের মান-সংক্রান্ত সমস্যা", "ক্ষতিগ্রস্ত, দূষিত বা ভুল লেবেলযুক্ত পণ্য"), ("অস্বাভাবিক কম কাজ করা", "পণ্য প্রত্যাশামতো কাজ করছে না মনে হওয়া")]),
 "cycle": ("ফার্মাকোভিজিল্যান্স চক্রের মৌলিক চিত্র: নিরাপত্তা-ঢালসহ ওষুধের প্যাককে ঘিরে একটি বৃত্তে ছয়টি আইকন, তীর দিয়ে দিক দেখানো।",
           "চক্রটি আলাদা আলাদা পর্যবেক্ষণকে শেখা, সিদ্ধান্ত ও ফলো-আপে রূপ দেয়।", "ol",
           [("লক্ষ্য করুন", "রোগী বা স্বাস্থ্যকর্মী সম্ভাব্য সমস্যা দেখেন"), ("নথিভুক্ত ও রিপোর্ট করুন", "তথ্য লিখে পাঠান"), ("কেস মূল্যায়ন করুন", "সম্পূর্ণতা, গুরুতরতা ও চিকিৎসাগত বিবরণ দেখুন"),
            ("প্যাটার্ন খুঁজুন", "একই ধরনের কেসে সিগন্যাল শনাক্তকরণ"), ("ঝুঁকি মূল্যায়ন, ব্যবস্থা ও যোগাযোগ", "সমানুপাতিক সাড়া ঠিক করুন"), ("পর্যবেক্ষণ চালিয়ে যান", "নতুন রিপোর্ট দেখায় ব্যবস্থা কাজ করছে কি না")]),
 "signal": ("ধূসর বিন্দুগুলো ম্যাগনিফাইং গ্লাসের দিকে যাচ্ছে, যেখানে কমলা বিন্দুরা জড়ো হয়েছে; পাশে তিনটি রোগীর কেস রিপোর্ট কার্ড।",
            "সিগন্যাল মানে তদন্তের ইঙ্গিত; ক্ষতির প্রমাণ নয়।", "ol",
            [("রিপোর্ট আসে", "নানা জায়গা থেকে ছড়ানো কেস"), ("একটি প্যাটার্ন চোখে পড়ে", "পর্যালোচকরা আরও ভালো করে দেখেন"), ("কেস যাচাই হয়", "সিগন্যাল একটি প্রশ্ন, রায় নয়")]),
 "causality": ("একজন মানুষ ট্যাবলেট খান, ক্যালেন্ডারে সময় যায়, পরে তিনি অসুস্থ বোধ করেন। নিচে ম্যাগনিফাইং গ্লাসের নিচে চারটি সূত্র: সময়, ওষুধ বন্ধ করা, অন্যান্য ওষুধ ও অন্যান্য সম্ভাব্য কারণ।",
               "শুধু সময়ের মিল কারণ প্রমাণ করে না। পর্যালোচকরা কয়েকটি সূত্র একসঙ্গে বিবেচনা করেন।", "ul",
               [("সময়ের সম্পর্ক", "ওষুধ কখন শুরু ও ঘটনা কখন শুরু"), ("ওষুধ বন্ধ করলে", "পরে কি সমস্যা কমেছে?"), ("অন্যান্য ওষুধ", "একসঙ্গে নেওয়া ওষুধ ও ডোজ"), ("অন্যান্য সম্ভাব্য কারণ", "অসুখ, ইতিহাস ও পরীক্ষা")]),
 "benefit": ("দাঁড়িপাল্লায় ওষুধের উপকারের সঙ্গে সম্ভাব্য ঝুঁকির তুলনা। নিচে সিঁড়ির মতো চারটি ধাপ: পর্যবেক্ষণ, প্রমাণ যাচাই, সতর্কতা জানানো এবং পণ্যের ব্যবহারে পরিবর্তন।",
             "সাড়া হওয়া উচিত প্রমাণ ও ঝুঁকির গুরুত্ব অনুযায়ী।", "ol",
             [("পর্যবেক্ষণ চালিয়ে যান", "নতুন রিপোর্টের দিকে নজর রাখুন"), ("আরও প্রমাণ যাচাই", "গবেষণা ও তথ্য"), ("নতুন সতর্কতা জানান", "তথ্য ও পরামর্শ হালনাগাদ"), ("প্রয়োজনে ব্যবহারে পরিবর্তন", "সীমিত, স্থগিত বা প্রত্যাহার")]),
 "bd": ("চারটি রিপোর্ট-উৎস (রোগী, ফার্মাসিস্ট বা ডাক্তার, হাসপাতাল ও অন্য স্বাস্থ্যপ্রতিষ্ঠান) একটি সরকারি দপ্তরে এবং তারপর জাতীয় নিরাপত্তা ডাটাবেসে তথ্য পাঠাচ্ছে।",
        "বাংলাদেশে রিপোর্টিংয়ের সরল চিত্র। সময়সীমার ওপর নির্ভর করার আগে DGDA-এর সর্বশেষ নির্দেশনা দেখে নিন।", "flow",
        [("রোগী ও ভোক্তা", ""), ("চিকিৎসক, নার্স ও ফার্মাসিস্ট", ""), ("হাসপাতাল ও ক্লিনিক", "PV focal point থাকলে তার মাধ্যমে"), ("অন্যান্য স্বাস্থ্যপ্রতিষ্ঠান", ""),
         ("DGDA · ADRM Cell", "জাতীয় পর্যালোচনা"), ("জাতীয় ডাটাবেস", "WHO-UMC VigiFlow")]),
 "info": ("ক্লিপবোর্ডে রিপোর্ট ফর্ম: রোগী, ঘটনা, সন্দেহজনক পণ্য, অন্যান্য ওষুধ ও রিপোর্টারের যোগাযোগের সারি, সঙ্গে গোপনীয়তার তালা।",
          "কাঠামোবদ্ধ রিপোর্ট ফলো-আপ ও মূল্যায়নে সাহায্য করে। ব্যক্তিগত তথ্য শুধু অনুমোদিত রিপোর্টিং চ্যানেলে দিন।", "ul",
          [("রোগী", "পরিচয়সূচক, বয়স, প্রযোজ্য হলে লিঙ্গ"), ("ঘটনা", "উপসর্গ, তারিখ, ফলাফল"), ("সন্দেহজনক পণ্য ও ডোজ", "নাম, শক্তি, জানা থাকলে ব্যাচ"),
           ("অন্যান্য ওষুধ ও ইতিহাস", "আর কী নেওয়া হয়েছিল"), ("রিপোর্টারের যোগাযোগ", "যাতে পর্যালোচক ফলো-আপ করতে পারেন"), ("গোপনীয়তা", "শুধু অনুমোদিত চ্যানেল ব্যবহার করুন")]),
 "industry": ("ওষুধ কোম্পানির ভবন, কেস ফাইলের ডেস্কে একজন কর্মী, এবং এমন একটি দাঁড়িপাল্লা যেখানে নিরাপত্তা-ঢাল ও বিক্রির চার্ট তুলনা হচ্ছে।",
              "বাণিজ্যিক চাপ যাই হোক, নিরাপত্তা-তথ্য নথিভুক্ত ও এগিয়ে দিতে হবে।", "ol",
              [("গ্রহণ ও নথিভুক্ত করুন", "অনানুষ্ঠানিক হলেও প্রতিটি রিপোর্ট"), ("দ্রুত এগিয়ে দিন", "দায়িত্বপ্রাপ্ত PV দলের কাছে"), ("লক্ষ্যের আগে নিরাপত্তা", "বিক্রির লক্ষ্য কখনো ঠিক করে না কী রিপোর্ট হবে")]),
 "people": ("একজন রোগী ওষুধের লিফলেট পড়ছেন, পাশে ডাক্তার ও ফার্মাসিস্ট এবং ওপরে নিরাপত্তা-ঢাল; নিচে পাঁচটি আইকন: লিখে রাখা, ওষুধ ও সময়, উপসর্গ, পেশাজীবীর সঙ্গে কথা এবং রিপোর্ট।",
            "রোগী ও স্বাস্থ্যকর্মী দুজনেই সাহায্য করেন। জরুরি উপসর্গে আগে চিকিৎসা নিতে হবে।", "ul",
            [("কী ঘটেছে লিখে রাখুন", ""), ("ওষুধ, ডোজ ও সময় টুকে রাখুন", ""), ("উপসর্গ লক্ষ্য করুন", "গুরুতর হলে জরুরি সেবা নিন"), ("চিকিৎসক বা ফার্মাসিস্টের সঙ্গে কথা বলুন", ""), ("সঠিক মাধ্যমে রিপোর্ট করুন", "")]),
 "key": ("পাঁচ ধাপের একটি সিঁড়ি যা একটি ঢালে গিয়ে শেষ হয়েছে: ওষুধ, সতর্কতাসহ ম্যাগনিফাইং গ্লাস, চেকলিস্ট, একদল মানুষ ও ওপরে ওঠা চার্ট।",
         "মনে রাখার মতো পাঁচটি কথা।", "ol",
         [("অনুমোদনের পরেও নজর", "বাস্তব ব্যবহারে ওষুধ পর্যবেক্ষণ করা হয়"), ("প্রমাণ ছাড়াই রিপোর্ট", "সন্দেহজনক সমস্যাই যথেষ্ট"), ("যাচাই ও মূল্যায়ন", "রিপোর্ট শুধু জমা নয়, পর্যালোচনাও হয়"),
          ("সবাই অংশ নেয়", "রোগী, স্বাস্থ্যকর্মী, কোম্পানি ও নিয়ন্ত্রক সংস্থা"), ("প্রমাণ ঠিক করে ব্যবস্থা", "সাড়া ঝুঁকির সমানুপাতিক")]),
}
FILES = {"cover": "pv-cover", "why": "pv-why", "types": "pv-report-types", "cycle": "pv-cycle", "signal": "pv-signal", "causality": "pv-causality",
         "benefit": "pv-benefit-risk", "bd": "pv-bangladesh", "info": "pv-report-info", "industry": "pv-industry", "people": "pv-people", "key": "pv-takeaways"}
DAYS = {"en": [("15", "calendar days", "Serious event: the completed form should reach the ADRM Cell within"), ("30", "calendar days", "Non-serious report: no later than, after being reported to the health facility,")],
        "bn": [("১৫", "ক্যালেন্ডার দিন", "গুরুতর ঘটনা: সম্পূর্ণ ফর্ম ADRM Cell-এ পৌঁছানো উচিত"), ("৩০", "ক্যালেন্ডার দিন", "গুরুতর নয়: স্বাস্থ্যপ্রতিষ্ঠানে রিপোর্ট হওয়ার পর সর্বোচ্চ")]}
# plain-language day chips (cleaner wording)
DAYS["en"] = [("Serious event", "15", "calendar days for the completed form to reach the ADRM Cell"), ("Non-serious report", "30", "calendar days after it is reported to the health facility")]
DAYS["bn"] = [("গুরুতর ঘটনা", "১৫", "ক্যালেন্ডার দিনের মধ্যে সম্পূর্ণ ফর্ম ADRM Cell-এ পৌঁছাতে হবে"), ("গুরুতর নয় এমন রিপোর্ট", "৩০", "ক্যালেন্ডার দিনের মধ্যে, স্বাস্থ্যপ্রতিষ্ঠানে রিপোর্ট হওয়ার পর")]

def fig(L, lang, key, lazy=True, extra=""):
    alt, cap, kind, items = L[key]
    cls = "pv-fig pv-key" if key == "key" else "pv-fig"
    img = f'<img src="{IMG}{FILES[key]}.webp" alt="{esc(alt)}" width="1600" height="900" {"loading=\"lazy\" " if lazy else ""}decoding="async">'
    leg = ""
    if kind:
        tag = "ol" if kind == "ol" else "ul"
        c = "pv-legend" + (" pv-two" if kind == "two" else "") + (" pv-flow" if kind == "flow" else "")
        li = []
        for i, (t, d) in enumerate(items):
            e = " class=\"pv-end\"" if kind == "flow" and i >= 4 else ""
            li.append(f"<li{e}><div><b>{esc(t)}</b>" + (f"<span>{esc(d)}</span>" if d else "") + "</div></li>")
        leg = f'<{tag} class="{c}">' + "".join(li) + f"</{tag}>"
    if key == "bd":
        leg += '<ul class="pv-days">' + "".join(f"<li><strong>{esc(t)}</strong><br><b>{esc(n)}</b> {esc(u)}</li>" for t, n, u in DAYS[lang]) + "</ul>"
    return f'<figure class="{cls}">{img}{leg}<figcaption class="caption">{esc(cap)}</figcaption></figure>'

def after_para(h, sec, n, block):
    pos = h.index(f'<h2 id="{sec}"')
    for _ in range(n):
        pos = h.index("</p>", pos) + 4
    return h[:pos] + "\n" + block + h[pos:]

def process(lang):
    L = EN if lang == "en" else BN
    d = R / "blog" / ("pharmacovigilance-medicine-safety-monitoring" + ("" if lang == "en" else "-bangla")) / "index.html"
    h = d.read_text(encoding="utf-8")
    assert "pv-figures.css" not in h, "already applied"
    h = h.replace('<link rel="stylesheet" href="/assets/site-polish.css?v=sa-20261122">',
                  '<link rel="stylesheet" href="/assets/site-polish.css?v=sa-20261122"><link rel="stylesheet" href="/assets/pv-figures.css?v=pv-20261123">', 1)
    # cover + existing svg figures
    figs = re.findall(r'<figure class="hero-visual">.*?</figure>', h, re.S)
    assert len(figs) == 3, len(figs)
    cap = re.search(r'<figcaption class="caption">(.*?)</figcaption>', figs[0], re.S).group(1)
    cover = (f'<figure class="hero-visual"><img src="{IMG}pv-cover.webp" alt="{esc(L["cover"][0])}" width="1600" height="900" fetchpriority="high" decoding="async">'
             f'<figcaption class="caption">{cap}</figcaption></figure>')
    h = h.replace(figs[0], cover).replace(figs[1], fig(L, lang, "cycle")).replace(figs[2], fig(L, lang, "info"))
    h = after_para(h, "why", 1, fig(L, lang, "why"))
    pos = h.index('<h2 id="what"'); u = h.index("<ul>", pos); h = h[:u] + fig(L, lang, "types") + "\n" + h[u:]
    h = after_para(h, "signal", 1, fig(L, lang, "signal"))
    h = after_para(h, "assessment", 1, fig(L, lang, "causality"))
    h = after_para(h, "assessment", 3, fig(L, lang, "benefit"))
    h = after_para(h, "bangladesh", 3, fig(L, lang, "bd"))
    h = after_para(h, "industry", 1, fig(L, lang, "industry"))
    h = after_para(h, "takeaway", 2, fig(L, lang, "people"))
    # key takeaways section before the final note
    title = "Key takeaways" if lang == "en" else "মূল কথাগুলো"
    k = h.index('<div class="note">')
    h = h[:k] + f'<h2 id="key-takeaways">{title}</h2>\n' + fig(L, lang, "key") + "\n" + h[k:]
    # toc
    m = re.search(r'(<li><a href="#takeaway">[^<]*</a></li>)', h); assert m
    h = h.replace(m.group(1), m.group(1) + f'<li><a href="#key-takeaways">{title}</a></li>', 1)
    # head/social
    soc = f"{SITE}{IMG}pv-social-{lang}.jpg"
    og_alt = ("Pharmacovigilance: How Are Medicines Monitored for Safety? A pharmacist on a watchtower with a magnifying glass and a safety shield." if lang == "en"
              else "ফার্মাকোভিজিল্যান্স: ওষুধের নিরাপত্তা কীভাবে পর্যবেক্ষণ করা হয়? পর্যবেক্ষণ-টাওয়ারে ম্যাগনিফাইং গ্লাসহাতে ফার্মাসিস্ট এবং নিরাপত্তা-ঢাল।")
    h = re.sub(r'(<meta property="og:image" content=")[^"]*', r'\g<1>' + soc, h)
    h = re.sub(r'(<meta property="og:image:secure_url" content=")[^"]*', r'\g<1>' + soc, h)
    h = re.sub(r'(<meta name="twitter:image" content=")[^"]*', r'\g<1>' + soc, h)
    h = re.sub(r'(<meta property="og:image:type" content=")[^"]*', r'\g<1>image/jpeg', h)
    h = re.sub(r'(<meta property="og:image:width" content=")[^"]*', r'\g<1>1200', h)
    h = re.sub(r'(<meta property="og:image:height" content=")[^"]*', r'\g<1>630', h)
    h = re.sub(r'(<meta property="og:image:alt" content=")[^"]*', r'\g<1>' + esc(og_alt), h)
    h = re.sub(r'(<meta name="twitter:image:alt" content=")[^"]*', r'\g<1>' + esc(og_alt), h)
    # schema images
    CRE = {"@type": "Person", "name": "Sayedul Abrar", "url": SITE + "/about/"}
    def obj(name, cap, w, hh):
        u_ = SITE + IMG + name
        return {"@type": "ImageObject", "contentUrl": u_, "url": u_, "width": w, "height": hh, "caption": cap, "creator": CRE,
                "creditText": "Sayedul Abrar", "copyrightNotice": "© Sayedul Abrar, sayedulabrar.site", "acquireLicensePage": SITE + "/contact/"}
    lst = [obj(f"pv-social-{lang}.jpg", og_alt, 1200, 630)] + [obj(FILES[k] + ".webp", L[k][0], 1600, 900) for k in FILES]
    new = json.dumps(lst, ensure_ascii=False, separators=(",", ":"))
    h, n = re.subn(r'"image":\[[^\]]*\]', lambda _: '"image":' + new, h, count=1); assert n == 1
    assert ".svg" not in h, [m for m in re.findall(r'[^"]{0,60}\.svg', h)][:3]
    d.write_text(h, encoding="utf-8")
    return lst
if __name__ == "__main__":
    for lg in ("en", "bn"):
        process(lg); print("ok", lg)
