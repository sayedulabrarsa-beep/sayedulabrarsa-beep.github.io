#!/usr/bin/env python3
"""Builds the product-cabinet block on /portfolio/ (between <!--PC-START--> and <!--PC-END-->).

Data = existing brand pages (manufacturer-listed, kept as they were) blended with the
monographs the owner pasted (general rabeprazole / ferric maltol reference).
Run:  python3 _src/portfolio_cabinet.py
"""
import html, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / "portfolio" / "index.html"
e = html.escape

# ---------------------------------------------------------------- shared Finix reference text
FX_IND_MFR = [
    "Healing of erosive or ulcerative gastro-oesophageal reflux disease (GERD)",
    "Maintenance of healing of erosive or ulcerative GERD",
    "Treatment of symptomatic GERD",
]
FX_IND_MUPS = FX_IND_MFR[:2] + [FX_IND_MFR[2],
    "Healing of gastric and duodenal ulcers",
    "Long-term treatment of pathological hypersecretory conditions, including Zollinger–Ellison syndrome",
    "With amoxicillin and clarithromycin for H. pylori eradication, as a prescribed regimen"]
FX_IND_GEN = [
    "Short-term treatment of active duodenal ulcer",
    "Zollinger–Ellison syndrome and other pathological hypersecretory conditions",
    "H. pylori eradication only as triple therapy with two antibiotics, never as monotherapy",
    "Active benign gastric ulcer and prevention of NSAID-associated gastric ulcers (guideline-supported; labelling varies by product)",
]
FX_DOSE = [
    ("Erosive / ulcerative GERD healing", "20 mg once daily", "4–8 weeks, may extend 8 more"),
    ("Maintenance of healed GERD", "20 mg once daily", "As directed by physician"),
    ("Symptomatic (non-erosive) GERD", "20 mg once daily", "Up to 4 weeks"),
    ("Active duodenal ulcer", "20 mg once daily after morning meal", "Up to 4 weeks"),
    ("Active benign gastric ulcer", "20 mg once daily", "4–8 weeks"),
    ("H. pylori (triple therapy)", "20 mg twice daily with amoxicillin 1000 mg and clarithromycin 500 mg, each twice daily", "7 days"),
    ("Zollinger–Ellison / hypersecretory", "60 mg once daily initially, titrated to 100–120 mg/day", "Individualised, may be long-term"),
]
FX_INTER = [
    "<b>Rilpivirine-containing HIV medicines:</b> contraindicated, because absorption falls sharply.",
    "<b>Atazanavir and some other HIV protease inhibitors:</b> not recommended together.",
    "<b>Warfarin:</b> INR / PT rises have been reported, so monitor at start and stop.",
    "<b>High-dose methotrexate:</b> levels may rise and persist, so a physician may pause the PPI.",
    "<b>Drugs that need stomach acid to be absorbed</b> (ketoconazole, itraconazole, some iron salts, erlotinib, mycophenolate): absorption may fall.",
    "<b>Digoxin:</b> absorption may increase, so watch for toxicity.",
    "<b>Clopidogrel:</b> minimal effect on its active metabolite; no routine adjustment, clinical judgement applies.",
]
FX_CONTRA = [
    "Known hypersensitivity to rabeprazole, other substituted benzimidazoles or any component.",
    "Use with rilpivirine-containing antiretrovirals.",
]
FX_SIDE = ("Usually mild and short-lived: headache, diarrhoea (less often constipation), abdominal pain, nausea or vomiting, "
           "flatulence and dry mouth. In H. pylori combination therapy, diarrhoea and taste disturbance are reported more often. "
           "Seek care for severe or persistent symptoms, allergic reactions or unexplained diarrhoea.")
FX_PREC = [
    "Symptom relief does not exclude gastric malignancy. Weight loss, recurrent vomiting, difficulty swallowing or GI bleeding need assessment.",
    "Long-term, high-dose use is linked with fractures, low magnesium (over about a year) and reduced vitamin B12 absorption (over about 3 years).",
    "May raise the risk of Clostridioides difficile diarrhoea. Persistent diarrhoea needs prompt review.",
    "Acute interstitial nephritis and, rarely, lupus-type reactions have been reported with PPIs.",
    "Stopping after prolonged use can cause rebound acid symptoms. Taper under physician guidance.",
    "Use the lowest effective dose for the shortest appropriate time.",
]
FX_PREG = ("Human pregnancy data are limited, so use only if clearly needed and the benefit outweighs the risk. "
           "It is not definitively known whether it passes into breast milk, so take advice before using it while breastfeeding.")
FX_OD = "Experience is limited and there is no specific antidote. Treatment is supportive. Seek immediate medical help or poison control."
FX_STORE = "Store below 30 °C, away from light and moisture. Keep out of reach of children."
FX_SPECIAL = ("No routine dose change for mild-to-moderate renal impairment, mild hepatic impairment or age alone. "
              "Take physician guidance in significant hepatic impairment. "
              "Paediatric GERD (physician-supervised only): ages 1–11, 5 mg daily under 15 kg or 10 mg daily from 15 kg, up to 12 weeks; "
              "12 years and older, 20 mg daily for up to 8 weeks. Not established under 1 year.")
FX_MOA = ("Rabeprazole irreversibly inhibits the gastric H⁺/K⁺-ATPase (proton pump) on parietal cells, blocking the final step of acid secretion. "
          "Acid control lasts until new pumps are made, even though plasma half-life is only about 1–2 hours. "
          "It is absorbed in the small intestine (peak about 2–5 h, bioavailability about 52%) and metabolised in the liver, "
          "with less dependence on CYP2C19 than some other PPIs.")
FX_FAQ = [
    ("Is this a medicine for ordinary gas or bloating?", "No. A PPI lowers stomach acid and is used for specific acid-related conditions. A clinician should assess persistent or severe symptoms."),
    ("What if a dose is missed?", "Take it when remembered unless the next dose is close. Do not double up."),
    ("Is it the best or fastest PPI?", "This page makes no ranking or superiority claim. Choice depends on diagnosis, history, other medicines and the prescriber's judgement."),
]

# ---------------------------------------------------------------- products
P = []

def finix(id_, name, strength, form, pack, img, alt, ac, lead, admin, ind, ref_label, extra_facts=(), extra_note=None, hp=False):
    return dict(id=id_, name=name, short=strength, form=form, pack=pack, img=img, alt=alt, ac=ac, co="Opsonin Pharma Ltd.",
                brand_page="/brands/finix-mups/" if id_ == "finix-mups-20" else "/brands/finix/", kind="finix",
                lead=lead, admin=admin, ind=ind, ref_label=ref_label, extra_facts=extra_facts, extra_note=extra_note)

P.append(finix("finix-10", "Finix 10", "Rabeprazole Sodium BP 10 mg", "Delayed-release sprinkle capsule",
    "10 × 10 capsules, 10 capsules per sachet",
    "/assets/img/products/finix-10-capsule-box.webp",
    "Finix 10 (rabeprazole sodium BP 10 mg) delayed-release sprinkle capsule carton and sachet by Opsonin Pharma", "#1d9a5b",
    "Finix 10 is the 10 mg delayed-release sprinkle capsule of rabeprazole sodium, a proton pump inhibitor, in the Finix range from Opsonin Pharma.",
    ["Open the sprinkle capsule and scatter the contents on a small amount of soft food or liquid. Take it at once, within 15 minutes, without chewing the granules, about 30 minutes before a meal.",
     "Check the pack insert for any form-specific instruction."],
    FX_IND_MFR, "Finix range · manufacturer-listed"))
P.append(finix("finix-20-capsule", "Finix 20 capsule", "Rabeprazole Sodium BP 20 mg", "Delayed-release capsule",
    "10 × 9 capsules, 10 capsules per sachet",
    "/assets/img/products/finix-20-capsule-box.webp",
    "Finix 20 (rabeprazole sodium BP 20 mg) capsule sachet and carton by Opsonin Pharma", "#e8741c",
    "Finix 20 capsule is the 20 mg delayed-release capsule presentation of rabeprazole sodium in the Finix range.",
    ["Follow the pack insert on whether the capsule may be opened. If it is not stated, swallow the capsule whole with water and do not chew it.",
     "Usually taken once daily, at the same time each day, as the prescriber directs."],
    FX_IND_MFR, "Finix range · manufacturer-listed"))
P.append(finix("finix-20-tablet", "Finix 20 tablet", "Rabeprazole Sodium BP 20 mg", "Enteric-coated tablet",
    "20 × 7 tablets",
    "/assets/img/products/finix-20-tablet-box.webp",
    "Finix 20 (rabeprazole sodium BP 20 mg) enteric-coated tablet carton and foil sachet by Opsonin Pharma", "#c8202f",
    "Finix 20 tablet is the 20 mg enteric-coated tablet of rabeprazole sodium. The enteric coating protects the acid-labile drug from gastric acid.",
    ["Swallow whole with water. Do not chew, crush or split, because that destroys the enteric coating.",
     "May be taken with or without food. Taking it after the morning meal at a regular time is commonly advised."],
    FX_IND_MFR, "Finix range · manufacturer-listed"))
P.append(finix("finix-mups-20", "Finix MUPS 20", "Rabeprazole Sodium BP 20 mg", "Enteric-coated MUPS tablet",
    "Alu-Alu blister in Alu-Alu sachet (per manufacturer insert)",
    "/assets/img/products/finix-mups-20-tablet-box.webp",
    "Finix MUPS 20 (rabeprazole sodium BP 20 mg) enteric-coated Multiple-Unit Pellet System tablet carton by Opsonin Pharma", "#2b6cc4",
    "Finix MUPS 20 is a rabeprazole sodium 20 mg PPI presented as an enteric-coated Multiple-Unit Pellet System (MUPS) tablet. The dose is carried in multiple coated units rather than one monolithic core.",
    ["Swallow whole with water, without chewing or crushing, unless the manufacturer insert says otherwise.",
     "Usually once daily at a consistent time, as the prescriber directs."],
    FX_IND_MUPS, "Finix MUPS · manufacturer-listed"))

HP = dict(id="finix-hp", name="Finix HP", short="Rabeprazole 20 mg + Amoxicillin 500 mg + Clarithromycin 500 mg",
    form="H. pylori eradication combination pack", pack="7 sachets per carton, one combination blister in each",
    img="/assets/img/logos/finix-hp-clarithromycin-amoxicillin-rabeprazole-logo.png",
    alt="Finix HP logo, rabeprazole, amoxicillin and clarithromycin combination pack by Opsonin Pharma", ac="#7a3fb0",
    co="Opsonin Pharma Ltd.", brand_page="/brands/finix-hp/", kind="hp", logo=True,
    lead="Finix HP is a combination pack of rabeprazole, amoxicillin and clarithromycin. The manufacturer lists it for Helicobacter pylori eradication in specified ulcer conditions. It is not for routine acidity, gas or bloating.")

MALIFA = dict(id="malifa-30", name="Malifa 30", short="Ferric maltol 30 mg", form="Capsule (oral)",
    pack="6 × 10 capsules (6 strips of 10)", img="/assets/img/products/malifa-30-capsule-box.webp",
    alt="Malifa 30 (ferric maltol 30 mg) capsule carton and blister strip by Navana Pharmaceuticals", ac="#d3202a",
    co="Navana Pharmaceuticals PLC", brand_page="/brands/malifa/", kind="malifa",
    lead="Malifa 30 is a ferric maltol 30 mg capsule, an oral iron preparation listed by Navana Pharmaceuticals for the treatment of iron deficiency in adults. It is part of my earlier work as a Brand Executive.")

# ---------------------------------------------------------------- HTML helpers
def ul(items, raw=False):
    return "<ul>" + "".join(f"<li>{i if raw else e(i)}</li>" for i in items) + "</ul>"

def acc(title, body, open_=False):
    return f'<details class="cab-acc"{" open" if open_ else ""}><summary>{e(title)}</summary><div class="cab-acc-b">{body}</div></details>'

def facts(rows):
    return '<dl class="cab-facts">' + "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in rows) + "</dl>"

def dose_table():
    r = "".join(f"<tr><th scope='row'>{e(a)}</th><td>{e(b)}</td><td>{e(c)}</td></tr>" for a, b, c in FX_DOSE)
    return ('<div class="cab-tw"><table class="cab-tbl"><thead><tr><th>Indication</th><th>Adult dose</th><th>Duration</th></tr></thead>'
            f'<tbody>{r}</tbody></table></div><p class="cab-small">Doses are general rabeprazole reference values. Always follow the prescriber and the current insert.</p>')

def body_finix(p):
    ind = ul(p["ind"]) + '<p class="cab-small"><b>Also described in general rabeprazole references:</b></p>' + ul(FX_IND_GEN)
    admin = ul(p["admin"]) + dose_table()
    return "".join([
        acc("Indications", ind, True),
        acc("Dosage & administration", admin),
        acc("How it works", f"<p>{e(FX_MOA)}</p>"),
        acc("Interactions", ul(FX_INTER, True) + '<p class="cab-small">Tell the doctor or pharmacist about all medicines, supplements and herbal products.</p>'),
        acc("Contraindications", ul(FX_CONTRA)),
        acc("Side effects", f"<p>{e(FX_SIDE)}</p>"),
        acc("Precautions & warnings", ul(FX_PREC)),
        acc("Pregnancy, lactation & special populations", f"<p>{e(FX_PREG)}</p><p>{e(FX_SPECIAL)}</p>"),
        acc("Overdose & storage", f"<p><b>Overdose.</b> {e(FX_OD)}</p><p><b>Storage.</b> {e(FX_STORE)}</p>"),
        acc("Quick answers", "".join(f"<p><b>{e(q)}</b><br>{e(a)}</p>" for q, a in FX_FAQ)),
    ])

def body_hp(p):
    comp = ul(["Rabeprazole Sodium BP 20 mg tablet", "Amoxicillin BP 500 mg capsule", "Clarithromycin USP 500 mg tablet"])
    return "".join([
        acc("Composition", comp + "<p>The manufacturer insert describes seven sachets per carton, with one combination blister in each sachet.</p>", True),
        acc("Manufacturer-listed use", "<p>Eradication of H. pylori in active chronic gastric and duodenal ulcer disease, as stated in the manufacturer's product information.</p>"),
        acc("How the components work", "<p>Rabeprazole inhibits the gastric H⁺/K⁺-ATPase proton pump and reduces acid secretion. Amoxicillin interferes with bacterial cell-wall synthesis. Clarithromycin inhibits bacterial protein synthesis through the 50S ribosomal subunit.</p>"),
        acc("Prescribing considerations", "<p>Suitability depends on confirmed diagnosis, allergy history, previous antibiotic exposure, interactions, organ function and local antimicrobial resistance. Clarithromycin-containing regimens may not suit every setting. A qualified prescriber must choose the regimen. Do not self-start, share or reuse this combination.</p>"),
        acc("Quick answers", "<p><b>Can it be taken for ordinary gas or heartburn?</b><br>No. It contains two antibiotics and needs a diagnosis and a prescription.</p><p><b>Does everyone with H. pylori need the same treatment?</b><br>No. A clinician weighs resistance, prior antibiotics, allergies, interactions and patient factors.</p>"),
    ])

def body_malifa(p):
    return "".join([
        acc("Indication", "<p>Treatment of iron deficiency in adults (Bangladesh listing).</p><p class='cab-small'>Some other regional labels describe iron-deficiency anaemia and include patients from 10 years of age. Follow the local approved insert.</p>", True),
        acc("Dosage & administration", ul([
            "30 mg twice daily, preferably on an empty stomach, at least 1 hour before or 2 hours after meals.",
            "Do not open, break or chew the capsule.",
            "Treatment is generally at least 12 weeks and continues until ferritin is in the normal range.",
            "Paediatric: safety and effectiveness are not established in the Bangladesh listing. Some other labels differ, so follow the local insert.",
        ])),
        acc("How it works", "<p>Ferric maltol delivers iron for uptake across the intestinal wall and transfer to transferrin and ferritin. It has been shown to raise serum iron parameters, including ferritin and transferrin saturation (TSAT). It is described as a ferric–maltol complex that limits free iron in the gut.</p>"),
        acc("Interactions", ul([
            "<b>Dimercaprol:</b> may raise the risk of nephrotoxicity, so avoid the combination.",
            "<b>Some oral drugs</b> (mycophenolate, ethinyl estradiol, ciprofloxacin, doxycycline): bioavailability may fall. Separate doses by at least 4 hours where it matters.",
            "<b>Levothyroxine, bisphosphonates, penicillamine:</b> iron may reduce absorption, so separate the doses.",
            "<b>Antacids and PPIs:</b> may reduce absorption of iron by altering gastric pH. Avoid together where possible.",
            "<b>Food:</b> reduces iron bioavailability. Dairy, tea and coffee do so too.",
        ], True)),
        acc("Contraindications", ul([
            "Known hypersensitivity to ferric maltol or any component.",
            "History of haemochromatosis or other iron-overload syndromes.",
            "Patients receiving repeated blood transfusions.",
            "Anaemia not caused by iron deficiency (per general reference).",
        ])),
        acc("Side effects", "<p>Most common: flatulence, diarrhoea, constipation, discoloured (dark) faeces, abdominal pain, nausea and vomiting. Dark stools can interfere with occult-blood stool tests.</p>"),
        acc("Precautions & warnings", ul([
            "Avoid during an active inflammatory bowel disease (IBD) flare.",
            "Do not give with evidence of iron overload or with intravenous iron.",
            "Assess iron parameters before starting and monitor during therapy.",
            "Accidental iron overdose is a leading cause of fatal poisoning in children under 6.",
        ])),
        acc("Pregnancy, lactation & special populations", "<p>After oral use ferric maltol is not absorbed systemically as an intact complex, so fetal exposure and infant exposure through milk are not expected. There are no data on human milk presence, effects on the breastfed child or on milk production. No well-established dose change is defined for renal or hepatic impairment, so use physician oversight.</p>"),
        acc("Overdose & storage", "<p><b>Overdose.</b> No overdose data are available for Malifa. Early signs of iron overload include nausea, vomiting, abdominal pain and diarrhoea, and serious cases can progress to systemic toxicity. Seek immediate help.</p><p><b>Storage.</b> Cool place below 25 °C (listing), dry and protected from light. Some references quote below 30 °C, so follow the pack. Keep out of reach of children.</p>"),
        acc("Listed price (MedEx)", "<p>Unit ৳11.00 · strip ৳110.00 · pack of 6 × 10 ৳660.00. Prices change, so confirm at the pharmacy.</p>"),
    ])

def dialog(p, idx, total):
    if p["kind"] == "finix":
        body = body_finix(p)
        rows = [("Brand", p["name"]), ("Active ingredient", p["short"]), ("Form", p["form"]), ("Pack", p["pack"]),
                ("Class", "Proton pump inhibitor (PPI)"), ("Company", p["co"])]
        src = "Sources: manufacturer-listed Finix product information (Opsonin Pharma) and a general rabeprazole monograph compiled from public references. This is not the manufacturer insert."
        links = ('<a class="cab-btn" href="https://www.opsonin-pharma.com/" target="_blank" rel="noopener">Opsonin Pharma ↗</a>')
    elif p["kind"] == "hp":
        body = body_hp(p)
        rows = [("Brand", p["name"]), ("Components", p["short"]), ("Form", p["form"]), ("Pack", p["pack"]),
                ("Class", "PPI + two antibacterials"), ("Company", p["co"])]
        src = "Source: manufacturer-listed Finix HP product information (Opsonin Pharma)."
        links = ""
    else:
        body = body_malifa(p)
        rows = [("Brand", "Malifa 30 mg Capsule"), ("Generic", "Ferric maltol 30 mg"), ("Form", p["form"]), ("Pack", p["pack"]),
                ("Class", "Oral iron preparation"), ("Company", p["co"])]
        src = "Sources: Bangladesh drug listing (MedEx) as used on the Malifa brand page, plus a general ferric maltol monograph. Not a manufacturer insert."
        links = ""
    img = (f'<img src="{p["img"]}" alt="{e(p["alt"])}" loading="lazy" decoding="async"'
           f'{" class=cab-logo" if p.get("logo") else ""}>')
    return f'''<dialog class="cab-dlg" id="cab-{p["id"]}" aria-labelledby="cab-{p["id"]}-t" style="--ac:{p["ac"]}">
<div class="cab-dlg-in">
<header class="cab-dlg-top"><span class="cab-dlg-count">{idx+1} / {total}</span>
<div class="cab-dlg-nav"><button type="button" data-cab-prev aria-label="Previous product">‹</button><button type="button" data-cab-next aria-label="Next product">›</button><button type="button" data-cab-close aria-label="Close">✕</button></div></header>
<div class="cab-dlg-grid">
<aside class="cab-dlg-side"><div class="cab-dlg-shot">{img}<i class="cab-dlg-shelf"></i></div>
<p class="cab-dlg-co">{e(p["co"])}</p><h3 id="cab-{p["id"]}-t">{e(p["name"])}</h3><p class="cab-dlg-sub">{e(p["short"])}</p>{facts(rows)}
<div class="cab-dlg-links"><a class="cab-btn cab-btn-p" href="{p["brand_page"]}">Full brand page →</a>{links}</div></aside>
<div class="cab-dlg-main"><p class="cab-lead">{e(p["lead"])}</p>{body}
<p class="cab-note"><b>Medical information notice.</b> Independent educational overview for a personal portfolio, not an official manufacturer page, advertisement, diagnosis or substitute for medical advice. Confirm the current approved insert and local guidance before prescribing, dispensing or using any medicine. Nothing here claims superiority over alternatives.</p>
<p class="cab-small">{e(src)} Pack images come from third-party listings, and any watermarks belong to their sources. Trademarks belong to their owners.</p></div>
</div></div></dialog>'''

def bay(p, n):
    logo = " dw-shot--logo" if p.get("logo") else ""
    nm = e(p["name"])
    return f'''<li class="dw" style="--ac:{p["ac"]};--i:{n}">
<div class="dw-cavity"><i class="dw-led" aria-hidden="true"></i>
<button type="button" class="dw-x" aria-label="Close the {nm} drawer">✕</button>
<button type="button" class="dw-view" data-cab-open="cab-{p["id"]}" aria-haspopup="dialog" aria-label="View full details of {nm}" tabindex="-1">
<span class="dw-shot{logo}"><img src="{p["img"]}" alt="{e(p["alt"])}" loading="lazy" decoding="async"><i class="dw-shadow"></i></span>
<span class="dw-more">View full details <i>→</i></span></button></div>
<div class="dw-front"><button type="button" class="dw-toggle" aria-expanded="false" aria-label="Open the {nm} drawer"><span class="dw-handle" aria-hidden="true"></span></button>
<span class="dw-plate"><b>{nm}</b><small>{e(p["form"])}</small></span>
<span class="dw-mid" aria-hidden="true"><em>{n+1:02d}</em><span>{e(p["co"])}</span></span>
<button type="button" class="dw-cta" tabindex="-1"><span class="dw-cta-t">Open to see my portfolio</span><i>+</i></button></div></li>'''

def build():
    order = [P[0], P[1], P[2], P[3], HP, MALIFA]
    bays = [bay(p, i) for i, p in enumerate(order)]
    dlgs = "\n".join(dialog(p, i, len(order)) for i, p in enumerate(order))
    block = f'''<!--PC-START-->
<section class="cab-sec" id="cabinet" aria-labelledby="cab-h"><div class="wrap">
<div class="portfolio-section-heading cab-head"><p class="eyebrow">Product portfolio · Opsonin Pharma &amp; Navana Pharmaceuticals</p><h2 id="cab-h">Portfolio I’m proud to be part of</h2>
<p>Six pharmaceutical brands, each one built through planning, positioning and teamwork. Every pack sits in its own drawer. Open a drawer to see the product, then step inside for the full reference.</p>
<button type="button" class="cab-all" id="cab-all" aria-pressed="false">Open all drawers</button></div>
<div class="cab" id="cab">
<div class="cab-cornice"><span class="cab-lamp" aria-hidden="true"></span><span class="cab-title">Portfolio cabinet</span><span class="cab-lamp" aria-hidden="true"></span></div>
<div class="cab-body">
<div class="cab-tier"><p class="cab-tag"><b>Opsonin Pharma</b> · Gastro portfolio · current</p><ul class="cab-row">{"".join(bays[:3])}</ul></div>
<div class="cab-tier"><p class="cab-tag"><b>Opsonin Pharma</b> · MUPS &amp; H. pylori pack · current <span class="cab-sep">|</span> <b>Navana Pharmaceuticals</b> · Malifa · previous</p><ul class="cab-row">{"".join(bays[3:])}</ul></div>
</div>
<div class="cab-base" aria-hidden="true"><i></i><i></i></div>
</div>
<p class="cab-foot">Product details are an independent educational overview, not a manufacturer page. Brand marks and pack images belong to their owners.</p>
</div>
{dlgs}
</section>
<!--PC-END-->'''
    s = PAGE.read_text(encoding="utf-8")
    s = re.sub(r"<!--PC-START-->.*?<!--PC-END-->\n?", "", s, flags=re.S)
    k = s.index('<section class="partner-wall')
    s = s[:k] + block + "\n" + s[k:]
    PAGE.write_text(s, encoding="utf-8")
    print("ok", len(block))

if __name__ == "__main__":
    build()
