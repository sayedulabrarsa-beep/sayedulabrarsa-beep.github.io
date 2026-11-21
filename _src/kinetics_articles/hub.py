SLUG = "how-medicines-work-in-the-body-series"
DATE = "2026-11-28"
IMGDIR = "how-medicines-work-series"
PREFIX = "how-medicines-work-series"
COVER = "how-medicines-work-series-cover"
SITE = "https://sayedulabrar.site"
ITEMS = [
 ("drug-absorption-how-medicine-enters-bloodstream", "Drug Absorption: How Does Medicine Enter the Bloodstream?", "ওষুধের শোষণ: ওষুধ কীভাবে রক্তে প্রবেশ করে?", "How a medicine gets from the gut into the blood, and why routes differ.", "ওষুধ কীভাবে অন্ত্র থেকে রক্তে যায়, আর পথভেদে পার্থক্য কেন।"),
 ("drug-distribution-how-medicines-reach-their-target", "Drug Distribution: How Medicines Reach Their Target", "ওষুধের বণ্টন: ওষুধ কীভাবে শরীরের বিভিন্ন অংশে পৌঁছায়?", "Blood as the highway, protein binding and the blood–brain barrier.", "রক্ত যেন মহাসড়ক, প্রোটিন বাইন্ডিং ও ব্লাড–ব্রেইন ব্যারিয়ার।"),
 ("drug-metabolism-how-the-body-processes-medicines", "Drug Metabolism: How Does the Body Process Medicines?", "ওষুধের বিপাক: শরীর কীভাবে ওষুধকে পরিবর্তন করে?", "The liver, CYP enzymes, first-pass metabolism and prodrugs.", "যকৃত, CYP এনজাইম, first-pass metabolism ও prodrug।"),
 ("drug-excretion-how-medicines-leave-the-body", "Drug Excretion: How Do Medicines Leave the Body?", "ওষুধ নিঃসরণ: শরীর কীভাবে ওষুধ বের করে দেয়?", "Kidneys, bile and other exits, and why kidney health matters.", "কিডনি, পিত্ত ও অন্যান্য পথ, আর কিডনির সুস্থতা কেন জরুরি।"),
 ("drug-half-life-explained", "Drug Half-Life: How Long Does a Medicine Stay in the Body?", "ওষুধের হাফ-লাইফ: একটি ওষুধ শরীরে কতক্ষণ থাকে?", "The 4–5 half-lives rule, dosing times and steady state.", "৪–৫ হাফ-লাইফের নিয়ম, ডোজের সময় ও স্টেডি স্টেট।"),
 ("bioavailability-explained", "Bioavailability: How Much Medicine Reaches the Bloodstream?", "বায়োঅ্যাভেইলেবিলিটি: ওষুধের কতটুকু রক্তে পৌঁছায়?", "Why IV is 100%, food effects and bioequivalence of generics.", "কেন IV-তে ১০০%, খাবারের প্রভাব ও জেনেরিকের বায়োইকুইভ্যালেন্স।"),
 ("onset-peak-duration-of-drug-action", "Onset, Peak and Duration of Drug Action Explained", "ওষুধ কখন কাজ শুরু করে, কখন থামে?", "The time curve, the therapeutic window and why not to double a dose.", "সময়-রেখা, থেরাপিউটিক উইন্ডো, আর কেন ডোজ দ্বিগুণ নয়।"),
]
REFS = [
 ("MSD Manual Professional Edition. Overview of Pharmacokinetics", "https://www.msdmanuals.com/professional/clinical-pharmacology/pharmacokinetics/overview-of-pharmacokinetics"),
 ("StatPearls. Elimination Half-Life of Drugs. NCBI Bookshelf", "https://www.ncbi.nlm.nih.gov/books/NBK554498/"),
 ("StatPearls. Drug Bioavailability. NCBI Bookshelf", "https://www.ncbi.nlm.nih.gov/books/NBK557852/"),
]

def itemlist(lang):
    bn = lang == "bn"
    return {"@context": "https://schema.org", "@type": "ItemList", "name": "শরীরে ওষুধ কীভাবে কাজ করে: সিরিজ" if bn else "How Medicines Work in the Body: series",
            "itemListOrder": "https://schema.org/ItemListOrderAscending", "numberOfItems": len(ITEMS),
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f"{SITE}/blog/{s}{'-bangla' if bn else ''}/", "name": b if bn else e}
                                for i, (s, e, b, _, _) in enumerate(ITEMS)]}
EXTRA_LD = [itemlist]

def lst(bn):
    out = '<ol class="series-list">'
    for i, (s, e, b, de, db) in enumerate(ITEMS):
        out += (f'<li{" class=\"later\"" if i >= 4 else ""}><div><b><a href="/blog/{s}{"-bangla" if bn else ""}/">{b if bn else e}</a></b><span>{db if bn else de}</span></div></li>')
    return out + "</ol>"

EN = dict(
 title="How Medicines Work in the Body: A 7-Part Series",
 h1="How Medicines Work in the Body: The Complete Series",
 description="A simple 7-part guide to how medicines work in the body: absorption, distribution, metabolism, excretion, half-life, bioavailability and onset.",
 keywords="how medicines work in the body, pharmacokinetics, ADME, absorption distribution metabolism excretion, pharmacology basics",
 eyebrow="PHARMA BLOG · SERIES · 7 ARTICLES",
 lead="Follow one medicine from the moment you swallow it to the moment it leaves your body, in seven short articles, in English and Bangla.",
 cover_alt="Series cover: a translucent human figure with glowing pathways carrying tablets from the stomach to the liver and kidneys, and the title How medicines work in the body.",
 cover_caption="How Medicines Work in the Body · A 7-part pharmacology series by Sayedul Abrar",
 quick="Pharmacists describe the journey of a medicine with four steps called ADME: Absorption, Distribution, Metabolism and Excretion. Three more ideas explain timing and amount: half-life, bioavailability, and onset, peak and duration. Read them in this order.",
 sections=[
  dict(h2="Read the series in order", html=lst(False),
       fig=("how-medicines-work-series-roadmap", "Roadmap of the 7-part series: 1 Absorption, 2 Distribution, 3 Metabolism, 4 Excretion, then 5 Half-life, 6 Bioavailability and 7 Onset, peak and duration.", "The seven steps, from ADME to timing and amount.")),
  dict(h2="Why this order?", html="<p>The first four articles follow the medicine itself: it enters the blood (absorption), spreads through the body (distribution), is changed, mostly in the liver (metabolism), and leaves, mostly through the kidneys (excretion). Together these are called <strong>ADME</strong>.</p><p>The last three use that journey to answer everyday questions: how long a medicine stays (half-life), how much of a dose actually arrives (bioavailability), and when it starts and stops working (onset, peak and duration).</p><p>If you are new to the topic, start with <a href=\"/blog/how-do-medicines-work-in-the-body/\">How Do Medicines Work Inside the Human Body?</a> for the big picture.</p>"),
 ],
 faqs=[
  ("What does ADME stand for?", "ADME stands for Absorption, Distribution, Metabolism and Excretion. These four steps describe how a medicine enters the body, spreads, is changed and leaves."),
  ("Do I need to read the articles in order?", "No, each article stands on its own. Reading in order makes the later ideas, like half-life and bioavailability, easier to follow."),
  ("Is the series available in Bangla?", "Yes. Every article in the series has a full Bangla version; use the language switch at the top of each page."),
 ],
 related=[("/blog/how-do-medicines-work-in-the-body/", "How Do Medicines Work Inside the Human Body?"),
          ("/blog/drug-vs-medicine/", "Drug vs Medicine"),
          ("/blog/why-complete-antibiotic-course-antibiotic-resistance/", "Why You Must Complete an Antibiotic Course")],
)
BN = dict(
 title="শরীরে ওষুধ কীভাবে কাজ করে: ৭ পর্বের সিরিজ",
 h1="শরীরে ওষুধ কীভাবে কাজ করে: পুরো সিরিজ",
 description="শরীরে ওষুধ কীভাবে কাজ করে, ৭ পর্বের সহজ গাইড: শোষণ, বণ্টন, বিপাক, নিঃসরণ, হাফ-লাইফ, বায়োঅ্যাভেইলেবিলিটি ও অনসেট।",
 keywords="শরীরে ওষুধ কীভাবে কাজ করে, ফার্মাকোকাইনেটিক্স, ADME, শোষণ বণ্টন বিপাক নিঃসরণ",
 eyebrow="PHARMA BLOG · সিরিজ · ৭টি লেখা",
 lead="ওষুধ গেলার মুহূর্ত থেকে শরীর থেকে বেরিয়ে যাওয়া পর্যন্ত একটি ওষুধের যাত্রা, সাতটি ছোট লেখায়, ইংরেজি ও বাংলায়।",
 cover_alt="সিরিজের কভার: স্বচ্ছ মানবদেহে আলোকিত পথ ধরে ট্যাবলেট পাকস্থলী থেকে যকৃত ও কিডনিতে যাচ্ছে, শিরোনাম ‘শরীরে ওষুধ কীভাবে কাজ করে’।",
 cover_caption="শরীরে ওষুধ কীভাবে কাজ করে · সাইয়্যেদুল আবরারের ৭ পর্বের ফার্মাকোলজি সিরিজ",
 quick="ফার্মাসিস্টরা ওষুধের যাত্রাকে চারটি ধাপে ব্যাখ্যা করেন, যার নাম ADME: শোষণ (Absorption), বণ্টন (Distribution), বিপাক (Metabolism) ও নিঃসরণ (Excretion)। আরও তিনটি ধারণা সময় ও পরিমাণ ব্যাখ্যা করে: হাফ-লাইফ, বায়োঅ্যাভেইলেবিলিটি, এবং অনসেট, পিক ও ডিউরেশন। এই ক্রমে পড়ুন।",
 sections=[
  dict(h2="এই ক্রমে সিরিজটি পড়ুন", html=lst(True),
       fig=("how-medicines-work-series-roadmap", "৭ পর্বের সিরিজের পথনকশা: ১ শোষণ, ২ বণ্টন, ৩ বিপাক, ৪ নিঃসরণ, তারপর ৫ হাফ-লাইফ, ৬ বায়োঅ্যাভেইলেবিলিটি ও ৭ শুরু, সর্বোচ্চ ও স্থায়িত্ব।", "ADME থেকে সময় ও পরিমাণ: সাতটি ধাপ।")),
  dict(h2="কেন এই ক্রম?", html="<p>প্রথম চারটি লেখা ওষুধের নিজের পথ অনুসরণ করে: এটি রক্তে ঢোকে (শোষণ), শরীরে ছড়ায় (বণ্টন), মূলত যকৃতে বদলায় (বিপাক), এবং মূলত কিডনি দিয়ে বেরিয়ে যায় (নিঃসরণ)। এই চারটিকে একসাথে বলে <strong>ADME</strong>।</p><p>শেষ তিনটি লেখা এই যাত্রা দিয়ে রোজকার প্রশ্নের উত্তর দেয়: ওষুধ কতক্ষণ থাকে (হাফ-লাইফ), ডোজের কতটুকু আসলে পৌঁছায় (বায়োঅ্যাভেইলেবিলিটি), আর কখন কাজ শুরু ও শেষ হয় (অনসেট, পিক ও ডিউরেশন)।</p><p>বিষয়টি নতুন হলে বড় চিত্রের জন্য শুরু করুন <a href=\"/blog/how-do-medicines-work-in-the-body-bangla/\">ওষুধ শরীরে কীভাবে কাজ করে?</a> লেখা দিয়ে।</p>"),
 ],
 faqs=[
  ("ADME মানে কী?", "ADME হলো Absorption (শোষণ), Distribution (বণ্টন), Metabolism (বিপাক) ও Excretion (নিঃসরণ)। এই চারটি ধাপ বলে ওষুধ কীভাবে শরীরে ঢোকে, ছড়ায়, বদলায় ও বেরিয়ে যায়।"),
  ("লেখাগুলো কি ক্রম অনুযায়ী পড়তে হবে?", "না, প্রতিটি লেখা আলাদাভাবে পড়া যায়। তবে ক্রমে পড়লে হাফ-লাইফ ও বায়োঅ্যাভেইলেবিলিটির মতো পরের ধারণাগুলো সহজে বোঝা যায়।"),
  ("সিরিজটি কি বাংলায় আছে?", "হ্যাঁ। সিরিজের প্রতিটি লেখার পূর্ণ বাংলা সংস্করণ আছে; প্রতিটি পাতার ওপরের ভাষা-বাটন ব্যবহার করুন।"),
 ],
 related=[("/blog/how-do-medicines-work-in-the-body-bangla/", "ওষুধ শরীরে কীভাবে কাজ করে?"),
          ("/blog/drug-vs-medicine-bangla/", "ড্রাগ বনাম মেডিসিন"),
          ("/blog/why-complete-antibiotic-course-antibiotic-resistance-bangla/", "কেন অ্যান্টিবায়োটিকের পুরো কোর্স শেষ করতে হয়")],
)
