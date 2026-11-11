(function(){
  'use strict';
  if(!document.querySelector('link[data-blog-next-style]')){
    var styleLink=document.createElement('link');
    styleLink.rel='stylesheet';styleLink.href='/assets/style.css?v=pb-next-20261111';styleLink.setAttribute('data-blog-next-style','');
    document.head.appendChild(styleLink);
  }
  var path=location.pathname.replace(/\\/+$/,'');
  if(!path.startsWith('/blog/')||path==='/blog')return;
  var article=document.querySelector('main article');
  if(!article||article.querySelector('.article-next-reading'))return;
  var catalog={
    'drug-vs-medicine':[
      ['GENERIC NAME & BRAND','Generic Name vs Brand Name','See how an ingredient name differs from a product brand.','/blog/generic-name-vs-brand-name/','/assets/img/blog/generic-brand/which-name-is-the-real-medicine-generic-vs-brand-thumbnail.webp'],
      ['MEDICINE SAFETY','Expiry Date vs Manufacturing Date','Learn how to read key dates on a medicine pack.','/blog/expiry-date-vs-manufacturing-date-medicine/','/assets/img/blog/expiry/expiry-date-vs-manufacturing-date-medicine-social.jpg']],
    'generic-name-vs-brand-name':[
      ['PHARMACY BASICS','Drug vs Medicine','Understand two essential terms used in pharmacy.','/blog/drug-vs-medicine/','/assets/img/blog/drug-vs-medicine/drug-vs-medicine-thumbnail.webp'],
      ['PRACTICAL MEDICINE USE','When to Take a PPI','Explore a practical example of reading medicine instructions.','/blog/when-to-take-ppi-before-meals/','/assets/img/blog/ppi-tablets/when-to-take-ppi-before-meals-thumbnail-16x9.webp']],
    'expiry-date-vs-manufacturing-date-medicine':[
      ['MEDICINE LABELS','Generic Name vs Brand Name','Learn where to find the ingredient name on a pack.','/blog/generic-name-vs-brand-name/','/assets/img/blog/generic-brand/which-name-is-the-real-medicine-generic-vs-brand-thumbnail.webp'],
      ['MEDICINE SAFETY','How to Take Iron Tablets Properly','Understand timing, food and medicine interactions.','/blog/how-to-take-iron-tablets-properly/','/assets/img/blog/iron-tablets/how-to-take-iron-tablets-properly-timing-food-interactions-thumbnail-16x9.webp']],
    'when-to-take-ppi-before-meals':[
      ['DIGESTIVE HEALTH','Heartburn vs Acid Reflux vs GERD','Understand symptoms, triggers and when to seek care.','/blog/heartburn-vs-acid-reflux-vs-gerd/','/assets/img/blog/heartburn-gerd-index-card.webp'],
      ['PHARMACY BASICS','Drug vs Medicine','Understand the difference between a drug and a medicine.','/blog/drug-vs-medicine/','/assets/img/blog/drug-vs-medicine/drug-vs-medicine-thumbnail.webp']],
    'how-to-take-iron-tablets-properly':[
      ['IRON & HEALTH','Iron Deficiency vs Anemia','Understand how iron deficiency and anemia differ.','/blog/iron-deficiency-vs-anemia/','/assets/img/blog/iron-deficiency-vs-anemia-social.jpg'],
      ['MEDICINE LABELS','Expiry Date vs Manufacturing Date','Learn how to read medicine pack dates.','/blog/expiry-date-vs-manufacturing-date-medicine/','/assets/img/blog/expiry/expiry-date-vs-manufacturing-date-medicine-social.jpg']],
    'iron-deficiency-vs-anemia':[
      ['PRACTICAL MEDICINE USE','How to Take Iron Tablets Properly','Read about timing, food and interactions.','/blog/how-to-take-iron-tablets-properly/','/assets/img/blog/iron-tablets/how-to-take-iron-tablets-properly-timing-food-interactions-thumbnail-16x9.webp'],
      ['RESEARCH REVIEW','Reading Medical Research','Explore how to assess a pharmaceutical research study.','/blog/glucosamine-alzheimers-nature-metabolism-study/','/assets/img/blog/glucosamine-alzheimers-en-thumbnail.svg']],
    'heartburn-vs-acid-reflux-vs-gerd':[
      ['PPI GUIDE','When to Take a PPI','Understand PPI timing and common medicine-use mistakes.','/blog/when-to-take-ppi-before-meals/','/assets/img/blog/ppi-tablets/when-to-take-ppi-before-meals-thumbnail-16x9.webp'],
      ['PHARMACY BASICS','Drug vs Medicine','Understand common medicine terminology.','/blog/drug-vs-medicine/','/assets/img/blog/drug-vs-medicine/drug-vs-medicine-thumbnail.webp']],
    'glucosamine-alzheimers-nature-metabolism-study':[
      ['RESEARCH & EVIDENCE','Pharmaceutical Industry in Bangladesh','Explore how medicine development and quality systems work.','/blog/what-is-the-pharmaceutical-industry/','/assets/img/blog/pharma-industry/pharmaceutical-industry-in-bangladesh-how-medicines-reach-you-thumbnail-16x9.webp'],
      ['PHARMACY BASICS','Drug vs Medicine','Revisit the difference between a drug and a medicine.','/blog/drug-vs-medicine/','/assets/img/blog/drug-vs-medicine/drug-vs-medicine-thumbnail.webp']],
    'what-is-the-pharmaceutical-industry':[
      ['PHARMACY BASICS','Drug vs Medicine','Understand the terms behind pharmaceutical products.','/blog/drug-vs-medicine/','/assets/img/blog/drug-vs-medicine/drug-vs-medicine-thumbnail.webp'],
      ['MEDICINE LABELS','Generic Name vs Brand Name','Understand ingredient names and product brands.','/blog/generic-name-vs-brand-name/','/assets/img/blog/generic-brand/which-name-is-the-real-medicine-generic-vs-brand-thumbnail.webp']]
  };
  var slug=path.split('/').filter(Boolean).pop().replace(/-bangla$/,'');
  var picks=catalog[slug]||catalog['drug-vs-medicine'];
  var section=document.createElement('section');
  section.className='article-next-reading';
  section.setAttribute('aria-labelledby','article-next-title');
  section.innerHTML='<div class="article-next-heading"><div><p>Keep learning</p><h2 id="article-next-title">Suggested next reads</h2></div></div><div class="article-next-grid"></div>';
  var grid=section.querySelector('.article-next-grid');
  picks.forEach(function(item){
    var link=document.createElement('a');
    link.className='article-next-card';
    link.href=item[3];
    var img=document.createElement('img');img.src=item[4];img.alt='';img.loading='lazy';
    var copy=document.createElement('span');
    var tag=document.createElement('small');tag.textContent=item[0];
    var title=document.createElement('strong');title.textContent=item[1];
    var desc=document.createElement('em');desc.textContent=item[2];
    copy.append(tag,title,desc);link.append(img,copy);grid.appendChild(link);
  });
  var author=article.querySelector('.author-card');
  if(author)article.insertBefore(section,author);
  else article.appendChild(section);
})();