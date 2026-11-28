#!/usr/bin/env python3
"""Place the 10 medicine-label pictures (EN+BN) in the noindex draft 'How to read a medicine label'."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import apply3 as a3
a3.V = "?v=q6-20261128"
a3.ART["lb"] = dict(slug="how-to-read-a-medicine-label", dir="medicine-label", pre="lb", order=["cover","which","brand","strength","dirs","warn","dates","storage","checklist","takeaways"],
  idx={0:"which",1:"brand",2:"strength",3:"dirs",4:"warn",5:"dates",6:"storage",7:"checklist",8:"takeaways"})
EN, BN = a3.EN, a3.BN
def add(k, en, bn): EN[("lb", k)] = en; BN[("lb", k)] = bn
S, SB = " AI-generated photo-style illustration.", " AI-তৈরি ছবি-ধাঁচের চিত্র।"
add("cover",("A pharmacist in a white coat holding a medicine bottle and a clipboard, with bottles and blister packs on the counter in front of him.","Read the label before you take a medicine: name, strength, directions, warnings, dates and storage."+S),
    ("সাদা কোট পরা একজন ফার্মাসিস্ট ওষুধের বোতল ও ক্লিপবোর্ড হাতে, সামনে কাউন্টারে বোতল ও ব্লিস্টার প্যাক।","ওষুধ খাওয়ার আগে লেবেল পড়ুন: নাম, শক্তি, নির্দেশনা, সতর্কতা, তারিখ ও সংরক্ষণ।"+SB))
add("which",("Medicine bottles, blister packs and a shopping trolley beside a magnifying glass, showing the different labels on a medicine pack.","A medicine has more than one label: the outer carton, the strip or bottle, and the leaflet."+S),
    ("ওষুধের বোতল, ব্লিস্টার প্যাক ও শপিং ট্রলির পাশে আতশকাচ, যা ওষুধের প্যাকের বিভিন্ন লেবেল বোঝায়।","একটি ওষুধে একাধিক লেবেল থাকে: বাইরের কার্টন, স্ট্রিপ বা বোতল এবং লিফলেট।"+SB))
add("brand",("An example Finix rabeprazole 20 mg box with call-outs explaining the brand name, the trade name given by the company, and the generic name, the INN of the active ingredient.","The brand name is the company's trade name; the generic name is the international non-proprietary name of the active ingredient. Example pack for illustration."+S),
    ("উদাহরণ হিসেবে Finix রাবেপ্রাজল ২০ mg-এর বাক্স, কলআউটে ব্র্যান্ড নাম (কোম্পানির দেওয়া ট্রেড নাম) ও জেনেরিক নাম (সক্রিয় উপাদানের INN) ব্যাখ্যা করা।","ব্র্যান্ড নাম কোম্পানির ট্রেড নাম; জেনেরিক নাম সক্রিয় উপাদানের আন্তর্জাতিক নন-প্রোপ্রাইটারি নাম। ছবিটি উদাহরণ-প্যাক।"+SB))
add("strength",("An example Finix rabeprazole 20 mg box with call-outs for strength, dosage form and dose, with a tablet and blister strip in front.","Strength is the amount of active ingredient in each dose, the dosage form is the physical form, and the dose is how much to take as directed. Example only, not a dosing instruction."+S),
    ("উদাহরণ হিসেবে Finix রাবেপ্রাজল ২০ mg-এর বাক্স, শক্তি, ডোজ ফর্ম ও ডোজের কলআউটসহ; সামনে ট্যাবলেট ও ব্লিস্টার স্ট্রিপ।","শক্তি হলো প্রতি ডোজে সক্রিয় উপাদানের পরিমাণ, ডোজ ফর্ম হলো ওষুধের শারীরিক রূপ, আর ডোজ হলো নির্দেশমতো কতটুকু খেতে হবে। শুধু উদাহরণ, ডোজের নির্দেশনা নয়।"+SB))
add("dirs",("A clock, a blister pack, a syrup bottle, a vial, a glass of water and a syringe on a pharmacy counter, representing how much, how often and for how long to take a medicine.","Follow the prescriber's directions on how much, how often, by which route and for how long, and ask if anything is unclear."+S),
    ("ফার্মেসি কাউন্টারে ঘড়ি, ব্লিস্টার প্যাক, সিরাপের বোতল, ভায়াল, পানির গ্লাস ও সিরিঞ্জ, যা কতটুকু, কতবার ও কতদিন ওষুধ খেতে হবে তা বোঝায়।","কতটুকু, কতবার, কোন পথে ও কতদিন, তা চিকিৎসকের নির্দেশমতো মানুন; অস্পষ্ট হলে জিজ্ঞাসা করুন।"+SB))
add("warn",("An example Finix box with a Warnings and Precautions panel enlarged beside it, listing advice to use as advised, to tell the doctor about pregnancy, breastfeeding, other medicines, and liver or kidney disease.","Read the warnings and precautions, and tell your doctor about pregnancy, breastfeeding, other medicines and liver or kidney problems. Example pack, not full prescribing information."+S),
    ("উদাহরণ Finix বাক্সের পাশে বড় করে দেখানো 'Warnings & Precautions' প্যানেল: চিকিৎসকের পরামর্শমতো ব্যবহার, গর্ভাবস্থা, বুকের দুধ খাওয়ানো, অন্য ওষুধ এবং লিভার বা কিডনি রোগ জানানো।","সতর্কতা পড়ুন এবং গর্ভাবস্থা, বুকের দুধ খাওয়ানো, অন্য ওষুধ ও লিভার বা কিডনির সমস্যা চিকিৎসককে জানান। উদাহরণ-প্যাক, সম্পূর্ণ প্রেসক্রাইবিং তথ্য নয়।"+SB))
add("dates",("An example medicine box side showing Mfg. Date, Exp. Date and Batch No. fields, with call-outs explaining each.","Check the manufacturing date, the expiry date and the batch number, which identifies a production batch for quality tracking. The dates and batch number shown are examples."+S),
    ("উদাহরণ ওষুধের বাক্সের পাশে Mfg. Date, Exp. Date ও Batch No. এবং প্রতিটির কলআউট ব্যাখ্যা।","উৎপাদনের তারিখ, মেয়াদোত্তীর্ণের তারিখ ও ব্যাচ নম্বর দেখুন; ব্যাচ নম্বর মান-ট্র্যাকিংয়ের জন্য উৎপাদন ব্যাচ শনাক্ত করে। ছবির তারিখ ও ব্যাচ নম্বর উদাহরণ।"+SB))
add("storage",("An example medicine box with a Storage panel and call-outs for storage conditions and pack integrity, comparing an intact blister strip with a torn one.","Follow the storage instructions on the label and do not use a pack that is torn, opened or damaged. The storage conditions shown are an example."+S),
    ("উদাহরণ ওষুধের বাক্সে 'Storage' প্যানেল এবং সংরক্ষণের শর্ত ও প্যাকের অখণ্ডতার কলআউট, অক্ষত ও ছেঁড়া ব্লিস্টার স্ট্রিপের তুলনাসহ।","লেবেলে দেওয়া সংরক্ষণ-নির্দেশনা মানুন এবং ছেঁড়া, খোলা বা ক্ষতিগ্রস্ত প্যাক ব্যবহার করবেন না। ছবির সংরক্ষণ-শর্ত উদাহরণ।"+SB))
add("checklist",("A blank clipboard with a pen beside medicine bottles, blister packs and tablets on a pharmacy counter, for a simple medicine-label checklist.","A simple checklist: name and strength, directions and warnings, MFG, EXP and batch, and storage and pack."+S),
    ("ফার্মেসি কাউন্টারে ওষুধের বোতল, ব্লিস্টার প্যাক ও ট্যাবলেটের পাশে কলমসহ ফাঁকা ক্লিপবোর্ড, ওষুধের লেবেলের সহজ চেকলিস্টের জন্য।","সহজ চেকলিস্ট: নাম ও শক্তি, নির্দেশনা ও সতর্কতা, MFG, EXP ও ব্যাচ, এবং সংরক্ষণ ও প্যাক।"+SB))
add("takeaways",("An amber bottle of yellow tablets, a bottle of blue and white capsules, a mortar and pestle and blister packs on a pharmacy counter.","Key takeaways: read the label, check the details, and ask a pharmacist when in doubt."+S),
    ("ফার্মেসি কাউন্টারে হলুদ ট্যাবলেটের অ্যাম্বার বোতল, নীল-সাদা ক্যাপসুলের বোতল, হামানদিস্তা ও ব্লিস্টার প্যাক।","মূল কথা: লেবেল পড়ুন, তথ্য মিলিয়ে দেখুন এবং সন্দেহ হলে ফার্মাসিস্টকে জিজ্ঞাসা করুন।"+SB))
if __name__ == "__main__":
    for lg in ("en", "bn"): a3.process("lb", lg)
