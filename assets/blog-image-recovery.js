(function(){
  'use strict';
  var fallback={
    '/assets/img/blog/api/api-social-en-w750.webp':'/assets/img/blog/api/api-social-en.jpg',
    '/assets/img/blog/drug-distribution/drug-distribution-social-en-w750.webp':'/assets/img/blog/drug-distribution/drug-distribution-cover-cinematic.webp',
    '/assets/img/blog/drug-absorption/drug-absorption-social-w750.webp':'/assets/img/blog/drug-absorption/drug-absorption-cover-cinematic.webp',
    '/assets/img/blog/antibiotic-course/why-complete-antibiotic-course-cover-16x9-w750.webp':'/assets/img/blog/antibiotic-course/why-complete-antibiotic-course-cover-16x9.webp',
    '/assets/img/blog/how-medicines-work/how-do-medicines-work-inside-the-human-body-cover-w750.webp':'/assets/img/blog/how-medicines-work/how-do-medicines-work-inside-the-human-body-cover.webp',
    '/assets/img/blog/pharma-industry/pharmaceutical-industry-in-bangladesh-how-medicines-reach-you-thumbnail-16x9-w750.webp':'/assets/img/blog/pharma-industry/pharmaceutical-industry-in-bangladesh-how-medicines-reach-you-thumbnail-16x9.webp',
    '/assets/img/blog/ppi-tablets/when-to-take-ppi-before-meals-thumbnail-16x9-w750.webp':'/assets/img/blog/ppi-tablets/when-to-take-ppi-before-meals-thumbnail-16x9.webp',
    '/assets/img/blog/glucosamine-alzheimers-social-w750.webp':'/assets/img/blog/glucosamine-alzheimers-social.webp',
    '/assets/img/blog/expiry/expiry-thumbnail-1200x630-w750.webp':'/assets/img/blog/expiry/expiry-social-en.jpg',
    '/assets/img/blog/generic-brand/which-name-is-the-real-medicine-generic-vs-brand-thumbnail-w750.webp':'/assets/img/blog/generic-brand/which-name-is-the-real-medicine-generic-vs-brand-thumbnail.webp',
    '/assets/img/blog/iron-tablets/how-to-take-iron-tablets-properly-timing-food-interactions-thumbnail-16x9-w750.webp':'/assets/img/blog/iron-tablets/how-to-take-iron-tablets-properly-timing-food-interactions-thumbnail-16x9.webp',
    '/assets/img/blog/iron-deficiency/iron-deficiency-vs-anemia-are-they-the-same-thumbnail-16x9-w750.webp':'/assets/img/blog/iron-deficiency/iron-deficiency-vs-anemia-are-they-the-same-thumbnail-16x9.webp',
    '/assets/img/blog/drug-vs-medicine/drug-vs-medicine-thumbnail-w750.webp':'/assets/img/blog/drug-vs-medicine/drug-vs-medicine-thumbnail.webp',
    '/assets/img/blog/reflux/reflux-card-w750.webp':'/assets/img/blog/reflux/reflux-card.webp'
  };
  function recover(img){
    if(!img||img.dataset.imageRecovery)return;
    var raw=img.getAttribute('src')||'';
    var path=raw.split('?')[0];
    var next=fallback[path];
    if(next){img.dataset.imageRecovery='1';img.src=next;return;}
    img.classList.add('image-unavailable');
  }
  document.addEventListener('error',function(e){
    var img=e.target;
    if(img&&img.tagName==='IMG'&&img.src.indexOf('/assets/img/blog/')!==-1)recover(img);
  },true);
  document.querySelectorAll('img[src*="/assets/img/blog/"]').forEach(function(img){
    img.addEventListener('load',function(){img.classList.add('image-ready')},{once:true});
  });
})();