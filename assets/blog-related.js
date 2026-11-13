(function(){
  'use strict';
  var main=document.querySelector('main');
  if(!main||document.querySelector('.ae-band'))return;
  var V='ae4-20261112';
  if(!document.querySelector('link[data-ae-style]')){
    var l=document.createElement('link');l.rel='stylesheet';l.href='/assets/article-end.css?v='+V;
    l.setAttribute('data-ae-style','');document.head.appendChild(l);
  }
  var B='/assets/img/blog/';
  /* slug: [tag_en, tag_bn, title_en, title_bn, desc_en, desc_bn, urlEn, urlBn, image, hasPaneBn] */
  var A={
    'drug-vs-medicine':['Pharmacy basics','ফার্মেসি বেসিক','Drug vs Medicine','ড্রাগ বনাম মেডিসিন','What the two words really mean in pharmacy.','ফার্মেসিতে শব্দ দুটির আসল অর্থ কী।','/blog/drug-vs-medicine/','/blog/drug-vs-medicine-bangla/',B+'drug-vs-medicine/drug-vs-medicine-thumbnail.webp'],
    'generic-name-vs-brand-name':['Medicine labels','ওষুধের লেবেল','Generic Name vs Brand Name','জেনেরিক নাম বনাম ব্র্যান্ড নাম','Find the ingredient name on any medicine pack.','ওষুধের প্যাকে উপাদানের নাম কোথায় পাবেন।','/blog/generic-name-vs-brand-name/','/blog/generic-name-vs-brand-name-bangla/',B+'generic-brand/which-name-is-the-real-medicine-generic-vs-brand-thumbnail.webp'],
    'expiry-date-vs-manufacturing-date-medicine':['Medicine safety','ওষুধের নিরাপত্তা','Expiry Date vs Manufacturing Date','মেয়াদোত্তীর্ণের তারিখ বনাম উৎপাদনের তারিখ','Read the dates printed on a medicine pack.','ওষুধের প্যাকের তারিখগুলো কীভাবে পড়বেন।','/blog/expiry-date-vs-manufacturing-date-medicine/','/blog/expiry-date-vs-manufacturing-date-medicine-bangla/',B+'expiry/expiry-date-vs-manufacturing-date-medicine-social.jpg'],
    'when-to-take-ppi-before-meals':['PPI guide','পিপিআই গাইড','When to Take a PPI','পিপিআই কখন খাবেন','Timing, common mistakes and missed doses.','সময়, সাধারণ ভুল ও ডোজ মিস হলে করণীয়।','/blog/when-to-take-ppi-before-meals/','/blog/when-to-take-ppi-before-meals-bangla/',B+'ppi-tablets/when-to-take-ppi-before-meals-thumbnail-16x9.webp'],
    'heartburn-vs-acid-reflux-vs-gerd':['Digestive health','হজম স্বাস্থ্য','Heartburn vs Acid Reflux vs GERD','হার্টবার্ন, অ্যাসিড রিফ্লাক্স ও জিইআরডি','How these common conditions differ.','এই সাধারণ অবস্থাগুলোর পার্থক্য কী।','/blog/heartburn-vs-acid-reflux-vs-gerd/','/blog/heartburn-vs-acid-reflux-vs-gerd-bangla/',B+'heartburn-gerd-index-card.webp'],
    'how-to-take-iron-tablets-properly':['Practical medicine use','ওষুধ ব্যবহার','How to Take Iron Tablets Properly','আয়রন ট্যাবলেট সঠিকভাবে খাওয়ার নিয়ম','Timing, food and interaction considerations.','সময়, খাবার ও ইন্টারঅ্যাকশনের বিষয়।','/blog/how-to-take-iron-tablets-properly/','/blog/how-to-take-iron-tablets-properly-bangla/',B+'iron-tablets/how-to-take-iron-tablets-properly-timing-food-interactions-thumbnail-16x9.webp'],
    'iron-deficiency-vs-anemia':['Iron & health','আয়রন ও স্বাস্থ্য','Iron Deficiency vs Anemia','আয়রনের ঘাটতি বনাম রক্তাল্পতা','Are they the same? A simple explanation.','দুটি কি একই? সহজ ব্যাখ্যা।','/blog/iron-deficiency-vs-anemia/','/blog/iron-deficiency-vs-anemia-bangla/',B+'iron-deficiency-vs-anemia-social.jpg'],
    'glucosamine-alzheimers-nature-metabolism-study':['Research review','রিসার্চ রিভিউ','Glucosamine & Alzheimer’s Study','গ্লুকোসামিন ও আলঝেইমার্স গবেষণা','How to read a research paper’s claims carefully.','গবেষণার দাবি সতর্কভাবে পড়ার উপায়।','/blog/glucosamine-alzheimers-nature-metabolism-study/','/blog/glucosamine-alzheimers-nature-metabolism-study-bangla/',B+'glucosamine/glucosamine-and-alzheimers-nature-metabolism-study-cover.webp'],
    'what-is-the-pharmaceutical-industry':['Industry','ফার্মা শিল্প','Pharmaceutical Industry in Bangladesh','বাংলাদেশের ফার্মাসিউটিক্যাল শিল্প','How medicines are made and reach patients.','ওষুধ কীভাবে তৈরি হয়ে রোগীর কাছে পৌঁছায়।','/blog/what-is-the-pharmaceutical-industry/','/blog/what-is-the-pharmaceutical-industry-bangla/',B+'pharma-industry/pharmaceutical-industry-in-bangladesh-how-medicines-reach-you-thumbnail-16x9.webp'],
    'how-do-medicines-work-in-the-body':['Pharmacology basics','ফার্মাকোলজি বেসিক','How Do Medicines Work in the Body?','মানবদেহে ওষুধ কীভাবে কাজ করে?','Understand how medicines interact with receptors and other targets.','ওষুধ কীভাবে receptor ও শরীরের অন্যান্য লক্ষ্যবস্তুর সঙ্গে কাজ করে বুঝুন।','/blog/how-do-medicines-work-in-the-body/','/blog/how-do-medicines-work-in-the-body-bangla/','/assets/img/blog/how-medicines-work/how-do-medicines-work-inside-the-human-body-cover.webp'],
    'why-complete-antibiotic-course-antibiotic-resistance':['Medicine safety','ওষুধের নিরাপত্তা','Why Complete an Antibiotic Course?','অ্যান্টিবায়োটিক কোর্স কেন শেষ করবেন?','Finishing the course, resistance, missed doses and leftovers.','কোর্স শেষ করা, রেজিস্ট্যান্স, ডোজ মিস ও বাকি ওষুধ।','/blog/why-complete-antibiotic-course-antibiotic-resistance/','/blog/why-complete-antibiotic-course-antibiotic-resistance-bangla/','/assets/img/blog/antibiotic-course/why-complete-antibiotic-course-cover-16x9.webp']
  };
  var R={
    'drug-vs-medicine':['generic-name-vs-brand-name','expiry-date-vs-manufacturing-date-medicine','what-is-the-pharmaceutical-industry'],
    'generic-name-vs-brand-name':['drug-vs-medicine','expiry-date-vs-manufacturing-date-medicine','when-to-take-ppi-before-meals'],
    'expiry-date-vs-manufacturing-date-medicine':['generic-name-vs-brand-name','drug-vs-medicine','how-to-take-iron-tablets-properly'],
    'when-to-take-ppi-before-meals':['heartburn-vs-acid-reflux-vs-gerd','generic-name-vs-brand-name','drug-vs-medicine'],
    'heartburn-vs-acid-reflux-vs-gerd':['when-to-take-ppi-before-meals','drug-vs-medicine','expiry-date-vs-manufacturing-date-medicine'],
    'how-to-take-iron-tablets-properly':['iron-deficiency-vs-anemia','expiry-date-vs-manufacturing-date-medicine','generic-name-vs-brand-name'],
    'iron-deficiency-vs-anemia':['how-to-take-iron-tablets-properly','drug-vs-medicine','glucosamine-alzheimers-nature-metabolism-study'],
    'glucosamine-alzheimers-nature-metabolism-study':['what-is-the-pharmaceutical-industry','drug-vs-medicine','generic-name-vs-brand-name'],
    'what-is-the-pharmaceutical-industry':['drug-vs-medicine','generic-name-vs-brand-name','glucosamine-alzheimers-nature-metabolism-study'],
    'how-do-medicines-work-in-the-body':['drug-vs-medicine','generic-name-vs-brand-name','when-to-take-ppi-before-meals'],
    'why-complete-antibiotic-course-antibiotic-resistance':['generic-name-vs-brand-name','expiry-date-vs-manufacturing-date-medicine','drug-vs-medicine']
  };
  var P='/assets/img/products/';
  var PR={
    finix:['Finix','Rabeprazole sodium · Opsonin Pharma','রেবিপ্রাজল সোডিয়াম · অপসোনিন ফার্মা','/brands/finix/',P+'finix-20-capsule-box.webp'],
    mups:['Finix MUPS 20','Rabeprazole · MUPS tablet','রেবিপ্রাজল · MUPS ট্যাবলেট','/brands/finix-mups/',P+'finix-mups-20-tablet-box.webp'],
    hp:['Finix HP','H. pylori therapy pack · prescribed use','এইচ. পাইলোরি থেরাপি প্যাক · প্রেসক্রিপশনে','/brands/finix-hp/',P+'finix-hp-pack-box.webp'],
    malifa:['Malifa 30 mg','Ferric maltol · Navana Pharmaceuticals','ফেরিক মালটল · নাভানা ফার্মাসিউটিক্যালস','/brands/malifa/',P+'malifa-30-capsule-box.webp']
  };
  var PM={
    'when-to-take-ppi-before-meals':['finix','mups','hp'],
    'heartburn-vs-acid-reflux-vs-gerd':['finix','mups','hp'],
    'how-to-take-iron-tablets-properly':['malifa'],
    'iron-deficiency-vs-anemia':['malifa']
  };
  var slug=location.pathname.replace(/\/$/,'').split('/').filter(Boolean).pop()||'';
  slug=slug.replace(/-bangla$/,'');
  if(!A[slug])return;
  var paneBn=document.getElementById('pane-bn');
  var htmlBn=document.documentElement.lang==='bn';
  function isBn(){return paneBn?!paneBn.hidden:htmlBn}
  /* remove the old static related block(s) */
  Array.prototype.forEach.call(document.querySelectorAll('main .related'),function(n){n.remove()});
  function el(t,c,h){var e=document.createElement(t);if(c)e.className=c;if(h!=null)e.textContent=h;return e}
  var band=el('section','ae-band');
  band.setAttribute('aria-labelledby','ae-title');
  var wrap=el('div','ae-wrap');band.appendChild(wrap);
  var head=el('div','ae-head');
  var eyebrow=el('p','ae-eyebrow');
  var h2=el('h2','ae-title');h2.id='ae-title';
  head.append(eyebrow,h2);
  var all=el('a','ae-all');all.href='/blog/';
  head.appendChild(all);
  var track=el('div','ae-track');
  var cards=R[slug].map(function(k){
    var a=A[k];
    var c=el('a','ae-card');
    var fig=el('span','ae-fig');
    var im=el('img');im.src=a[8];im.loading='lazy';im.decoding='async';im.width=1600;im.height=900;
    fig.appendChild(im);
    var tag=el('small'),t=el('strong'),d=el('em'),go=el('b','ae-go');
    var body=el('span','ae-body');body.append(tag,t,d,go);
    c.append(fig,body);track.appendChild(c);
    return {k:k,a:a,c:c,im:im,tag:tag,t:t,d:d,go:go};
  });
  wrap.append(head,track);
  var prods=(PM[slug]||[]).map(function(k){return PR[k]});
  var pbox=el('div','ae-prod');
  var ph=el('div','ae-prod-head'),pt=el('h3'),pn=el('p');
  ph.append(pt,pn);
  var pg=el('div','ae-prod-grid');
  var pcards=prods.map(function(p){
    var c=el('a','ae-pc');c.href=p[3];
    var im=el('img');im.src=p[4];im.alt='';im.loading='lazy';im.width=120;im.height=120;
    var s=el('span'),n=el('strong',null,p[0]),g=el('em'),go=el('b');
    s.append(n,g,go);c.append(im,s);pg.appendChild(c);
    return {p:p,im:im,g:g,go:go,c:c};
  });
  if(!prods.length){
    var c=el('a','ae-pc ae-pc-wide');c.href='/portfolio/';
    var s=el('span'),n=el('strong'),g=el('em'),go=el('b');
    s.append(n,g,go);c.appendChild(s);pg.appendChild(c);
    pcards=[{generic:true,n:n,g:g,go:go}];
  }
  pbox.append(ph,pg);wrap.appendChild(pbox);
  var note=el('p','ae-note');wrap.appendChild(note);
  function render(){
    var bn=isBn();
    band.lang=bn?'bn':'en';
    eyebrow.textContent=bn?'আরও জানুন':'Continue learning';
    h2.textContent=bn?'আরও পড়তে পারেন':'You can also read';
    all.textContent=bn?'সব আর্টিকেল ↗':'All articles ↗';
    cards.forEach(function(x){
      var a=x.a;
      x.c.href=bn?a[7]:a[6];
      x.im.alt=bn?a[3]:a[2];
      x.tag.textContent=bn?a[1]:a[0];
      x.t.textContent=bn?a[3]:a[2];
      x.d.textContent=bn?a[5]:a[4];
      x.go.textContent=bn?'পড়ুন →':'Read article →';
    });
    pt.textContent=bn?'সম্পর্কিত প্রোডাক্ট তথ্য':'Related product information';
    pn.textContent=bn?'পোর্টফোলিও থেকে — শুধু রেফারেন্সের জন্য':'From my portfolio — for reference only';
    pcards.forEach(function(x){
      if(x.generic){
        x.n.textContent=bn?'আমার পোর্টফোলিও দেখুন':'Explore my portfolio';
        x.g.textContent=bn?'ওষুধ ও প্রোডাক্ট সম্পর্কিত তথ্যপাতা':'Medicine and product information pages';
        x.go.textContent=bn?'পোর্টফোলিও →':'Portfolio →';
      }else{
        x.g.textContent=bn?x.p[2]:x.p[1];
        x.go.textContent=bn?'প্রোডাক্ট তথ্য →':'Product information →';
      }
    });
    note.textContent=bn
      ?'প্রোডাক্ট পাতাগুলো স্বাস্থ্যসেবা পেশাজীবী ও আগ্রহী পাঠকের জন্য সাধারণ তথ্য। ওষুধ নিজে থেকে শুরু বা বন্ধ করবেন না — চিকিৎসক বা ফার্মাসিস্টের পরামর্শ নিন।'
      :'Product pages are general information for professionals and interested readers. Do not start or stop a medicine on your own; ask your doctor or pharmacist.';
  }
  render();
  var foot=document.querySelector('body > footer');if(foot)document.body.insertBefore(band,foot);else document.body.appendChild(band);
  if(paneBn&&window.MutationObserver){
    new MutationObserver(render).observe(paneBn,{attributes:true,attributeFilter:['hidden']});
  }
})();
