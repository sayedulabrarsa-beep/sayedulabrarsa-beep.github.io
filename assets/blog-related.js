(function(){
  'use strict';
  if(!document.querySelector('link[data-blog-next-style]')){
    var css=document.createElement('link');
    css.rel='stylesheet';css.href='/assets/style.css?v=pb-next-20261111';
    css.setAttribute('data-blog-next-style','');document.head.appendChild(css);
  }
  var related=document.querySelector('main .related');
  if(!related)return;
  var path=location.pathname.replace(/\/$/,'');
  var slug=path.split('/').filter(Boolean).pop()||'';
  slug=slug.replace(/-bangla$/,'');
  var catalog={
    'drug-vs-medicine':[
      ['PHARMACY BASICS','Generic Name vs Brand Name','Understand how an ingredient name differs from a product brand.','/blog/generic-name-vs-brand-name/','/assets/img/blog/generic-brand/which-name-is-the-real-medicine-generic-vs-brand-thumbnail.webp'],
      ['MEDICINE SAFETY','Expiry Date vs Manufacturing Date','Learn to read the important dates printed on medicine packs.','/blog/expiry-date-vs-manufacturing-date-medicine/','/assets/img/blog/expiry/expiry-date-vs-manufacturing-date-medicine-social.jpg']],
    'generic-name-vs-brand-name':[
      ['PHARMACY BASICS','Drug vs Medicine','Understand two essential terms used in pharmacy.','/blog/drug-vs-medicine/','/assets/img/blog/drug-vs-medicine/drug-vs-medicine-thumbnail.webp'],
      ['PRACTICAL MEDICINE USE','When to Take a PPI','Explore practical guidance on medicine timing and instructions.','/blog/when-to-take-ppi-before-meals/','/assets/img/blog/ppi-tablets/when-to-take-ppi-before-meals-thumbnail-16x9.webp']],
    'expiry-date-vs-manufacturing-date-medicine':[
      ['MEDICINE LABELS','Generic Name vs Brand Name','Learn where to find the ingredient name on a medicine pack.','/blog/generic-name-vs-brand-name/','/assets/img/blog/generic-brand/which-name-is-the-real-medicine-generic-vs-brand-thumbnail.webp'],
      ['MEDICINE SAFETY','How to Take Iron Tablets Properly','Explore timing, food and medicine-use considerations.','/blog/how-to-take-iron-tablets-properly/','/assets/img/blog/iron-tablets/how-to-take-iron-tablets-properly-timing-food-interactions-thumbnail-16x9.webp']],
    'when-to-take-ppi-before-meals':[
      ['DIGESTIVE HEALTH','Heartburn vs Acid Reflux vs GERD','Understand the differences between common digestive conditions.','/blog/heartburn-vs-acid-reflux-vs-gerd/','/assets/img/blog/heartburn-gerd-index-card.webp'],
      ['PHARMACY BASICS','Drug vs Medicine','Understand the difference between a drug and a medicine.','/blog/drug-vs-medicine/','/assets/img/blog/drug-vs-medicine/drug-vs-medicine-thumbnail.webp']],
    'how-to-take-iron-tablets-properly':[
      ['IRON & HEALTH','Iron Deficiency vs Anemia','Understand how iron deficiency and anemia differ.','/blog/iron-deficiency-vs-anemia/','/assets/img/blog/iron-deficiency-vs-anemia-social.jpg'],
      ['MEDICINE LABELS','Expiry Date vs Manufacturing Date','Learn how to read medicine pack dates.','/blog/expiry-date-vs-manufacturing-date-medicine/','/assets/img/blog/expiry/expiry-date-vs-manufacturing-date-medicine-social.jpg']],
    'iron-deficiency-vs-anemia':[
      ['PRACTICAL MEDICINE USE','How to Take Iron Tablets Properly','Read about timing, food and common interactions.','/blog/how-to-take-iron-tablets-properly/','/assets/img/blog/iron-tablets/how-to-take-iron-tablets-properly-timing-food-interactions-thumbnail-16x9.webp'],
      ['RESEARCH REVIEW','Research Review','Explore how to assess pharmaceutical and medical research.','/blog/glucosamine-alzheimers-nature-metabolism-study/','/assets/img/blog/glucosamine-alzheimers-en-thumbnail.svg']],
    'heartburn-vs-acid-reflux-vs-gerd':[
      ['PPI GUIDE','When to Take a PPI','Understand PPI timing and common medicine-use mistakes.','/blog/when-to-take-ppi-before-meals/','/assets/img/blog/ppi-tablets/when-to-take-ppi-before-meals-thumbnail-16x9.webp'],
      ['PHARMACY BASICS','Drug vs Medicine','Understand common medicine terminology.','/blog/drug-vs-medicine/','/assets/img/blog/drug-vs-medicine/drug-vs-medicine-thumbnail.webp']],
    'glucosamine-alzheimers-nature-metabolism-study':[
      ['RESEARCH & EVIDENCE','Pharmaceutical Industry in Bangladesh','Explore how medicines are developed and reach patients.','/blog/what-is-the-pharmaceutical-industry/','/assets/img/blog/pharma-industry/pharmaceutical-industry-in-bangladesh-how-medicines-reach-you-thumbnail-16x9.webp'],
      ['PHARMACY BASICS','Drug vs Medicine','Revisit the difference between a drug and a medicine.','/blog/drug-vs-medicine/','/assets/img/blog/drug-vs-medicine/drug-vs-medicine-thumbnail.webp']],
    'what-is-the-pharmaceutical-industry':[
      ['PHARMACY BASICS','Drug vs Medicine','Understand the terms behind pharmaceutical products.','/blog/drug-vs-medicine/','/assets/img/blog/drug-vs-medicine/drug-vs-medicine-thumbnail.webp'],
      ['MEDICINE LABELS','Generic Name vs Brand Name','Understand ingredient names and product brands.','/blog/generic-name-vs-brand-name/','/assets/img/blog/generic-brand/which-name-is-the-real-medicine-generic-vs-brand-thumbnail.webp']]
  };
  var picks=catalog[slug]||catalog['drug-vs-medicine'];
  var isBangla=/-bangla\\/?$/.test(location.pathname);
  related.innerHTML='<div class="article-next-heading"><div><p>'+(isBangla?'আরও জানুন · বাছাইকৃত পাঠ':'CONTINUE LEARNING · SELECTED FOR YOU')+'</p><h2 id="article-next-title">'+(isBangla?'এরপর যা পড়তে পারেন':'What to read next')+'</h2><span class="article-next-intro">'+(isBangla?'এই বিষয়ের সঙ্গে সম্পর্কিত আরও দুটি শিক্ষামূলক লেখা পড়ুন।':'Explore two closely related topics to build on what you have just learned.')+'</span></div></div><div class="article-next-grid"></div>';
  related.classList.add('article-next-reading');
  related.setAttribute('aria-labelledby','article-next-title');
  related.querySelector('h2').id='article-next-title';
  var grid=related.querySelector('.article-next-grid');
  picks.forEach(function(item){
    var link=document.createElement('a');link.className='article-next-card';link.href=item[3];
    var img=document.createElement('img');img.src=item[4];img.alt=item[1];img.loading='lazy';
    var copy=document.createElement('span');
    var tag=document.createElement('small');tag.textContent=item[0];
    var title=document.createElement('strong');title.textContent=item[1];
    var desc=document.createElement('em');desc.textContent=item[2];
    copy.append(tag,title,desc);link.append(img,copy);grid.appendChild(link);
  });
})();