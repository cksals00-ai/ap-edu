// reveal on scroll · YouTube modal
(function(){
  var io=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target)}})},{rootMargin:'0px 0px -8% 0px'});
  document.querySelectorAll('.ccard,.ecard,.ngrid article,.fgrid4 article,.steps li').forEach(function(el){el.classList.add('rv');io.observe(el)});
  var m=document.getElementById('yt-modal');if(!m)return;
  var fr=m.querySelector('.yt-frame');
  function close(){m.hidden=true;fr.innerHTML='';document.body.style.overflow=''}
  document.addEventListener('click',function(e){
    var a=e.target.closest('[data-yt]');
    if(a){e.preventDefault();var id=a.getAttribute('data-yt');fr.innerHTML='<iframe src="https://www.youtube-nocookie.com/embed/'+id+'?autoplay=1&rel=0" title="YouTube" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen></iframe>';m.hidden=false;document.body.style.overflow='hidden';return}
    if(e.target===m||e.target.closest('.yt-x'))close();
  });
  document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!m.hidden)close()});
  if(location.hash){var t=document.querySelector(location.hash);if(t){t.classList.add('in')}}
})();
;(function(){var n=document.querySelector('.top nav'),a=n&&n.querySelector('a.on');if(a&&n.scrollWidth>n.clientWidth)n.scrollLeft=a.offsetLeft-n.clientWidth/2+a.offsetWidth/2;})();
