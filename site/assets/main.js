/* ELVORRA OPERATIONS — shared site script */
(function(){
'use strict';
var $=function(s,c){return (c||document).querySelector(s)},$$=function(s,c){return Array.prototype.slice.call((c||document).querySelectorAll(s))};
var CFG=window.ELV_CONFIG||{};
var RM=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
var HOVER=window.matchMedia&&matchMedia('(hover:hover)').matches;

/* ---------- config-driven links ---------- */
(function(){
  var email=CFG.email||'';
  $$('[data-email]').forEach(function(el){el.href='mailto:'+email;if(el.hasAttribute('data-email-text'))el.textContent=email});
  $$('[data-email-text]').forEach(function(el){el.textContent=email});
  var num=(CFG.whatsapp||'').replace(/\D/g,'');
  $$('[data-wa]').forEach(function(el){
    if(num){el.href='https://wa.me/'+num+'?text='+encodeURIComponent('Hello ELVORRA OPERATIONS, I would like to discuss outsourcing support for my business.');el.target='_blank';el.rel='noopener'}
    else{el.href=el.getAttribute('data-wa-fallback')||'contact.html#whatsapp'}
  });
  $$('[data-consult]').forEach(function(el){
    if(CFG.calendly){el.href=CFG.calendly;el.target='_blank';el.rel='noopener'}
  });
})();

/* ---------- theme ---------- */
var tgl=$('#tgl');
if(tgl)tgl.addEventListener('click',function(){
  var r=document.documentElement,n=r.dataset.theme==='dark'?'light':'dark';
  r.classList.add('theme-fade');r.dataset.theme=n;
  try{localStorage.setItem('elvorra-theme',n)}catch(e){}
  tgl.setAttribute('aria-pressed',n==='dark');
  setTimeout(function(){r.classList.remove('theme-fade')},600);
});

/* ---------- mobile menu ---------- */
var burger=$('#burger'),mm=$('#mm');
function setMenu(open){if(!mm)return;mm.classList.toggle('open',open);burger.setAttribute('aria-expanded',open);document.body.style.overflow=open?'hidden':''}
if(burger&&mm){
  burger.addEventListener('click',function(){setMenu(!mm.classList.contains('open'))});
  $$('#mm a').forEach(function(a){a.addEventListener('click',function(){setMenu(false)})});
  document.addEventListener('keydown',function(e){if(e.key==='Escape')setMenu(false)});
  matchMedia('(min-width:1101px)').addEventListener&&matchMedia('(min-width:1101px)').addEventListener('change',function(e){if(e.matches)setMenu(false)});
}

/* ---------- reveal ---------- */
var io=('IntersectionObserver' in window)?new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.1,rootMargin:'0px 0px -40px 0px'}):null;
$$('.rv').forEach(function(el){
  var sib=Array.prototype.filter.call(el.parentElement.children,function(c){return c.classList.contains('rv')});
  el.style.transitionDelay=(sib.indexOf(el)%4)*90+'ms';
  io?io.observe(el):el.classList.add('in');
});

/* ---------- counters ---------- */
var cio=('IntersectionObserver' in window)?new IntersectionObserver(function(es){es.forEach(function(e){
  if(!e.isIntersecting)return;var el=e.target,end=+el.dataset.count,t0=performance.now();
  (function s(t){var p=Math.min(1,(t-t0)/1600);el.textContent=Math.round(end*(1-Math.pow(1-p,4)));if(p<1)requestAnimationFrame(s)})(t0);
  cio.unobserve(el)})},{threshold:.5}):null;
$$('[data-count]').forEach(function(el){cio?cio.observe(el):el.textContent=el.dataset.count});

/* ---------- marquee ---------- */
var track=$('#track');if(track)track.innerHTML+=track.innerHTML;

/* ---------- hero slider (home) ---------- */
(function(){
  var slides=$$('.slide');if(!slides.length)return;
  var heads=$$('.hd'),tabs=$$('.tab'),cur=0,timer;
  function go(n){
    if(n===cur)return;
    heads[cur].classList.remove('on');heads[cur].classList.add('out');var old=cur;setTimeout(function(){heads[old].classList.remove('out')},700);
    slides[cur].classList.remove('on');tabs[cur].classList.remove('on');
    cur=n;slides[cur].classList.add('on');heads[cur].classList.add('on');
    void tabs[cur].offsetWidth;tabs[cur].classList.add('on');
    var vn=$('#vn'),vb=$('#vbar');if(vn)vn.textContent='0'+(cur+1);if(vb)vb.style.top=(cur*33.5)+'%';
    restart();
  }
  function restart(){clearInterval(timer);if(!RM)timer=setInterval(function(){go((cur+1)%slides.length)},6500)}
  tabs.forEach(function(t,i){t.addEventListener('click',function(){go(i)})});restart();
})();

/* ---------- greeting rotator ---------- */
(function(){
  var gw=$$('#greet span');if(!gw.length||RM)return;var gl=['EN','FR','DE','ES'],gi=0,tag=$('#glang');
  setInterval(function(){var c=gw[gi];c.classList.remove('on');c.classList.add('out');setTimeout(function(){c.classList.remove('out')},800);gi=(gi+1)%gw.length;gw[gi].classList.add('on');if(tag)tag.textContent=gl[gi]},1900);
})();

/* ---------- live widgets ---------- */
(function(){
  var wave=$('#wave');
  if(wave){for(var i=0;i<24;i++){var b=document.createElement('i');b.style.animationDelay=(Math.random()*-1.1)+'s';b.style.animationDuration=(.7+Math.random()*.8)+'s';wave.appendChild(b)}}
  var tm=$('#timer');if(tm){var sec=0;setInterval(function(){sec=(sec+1)%600;tm.textContent=String(sec/60|0).padStart(2,'0')+':'+String(sec%60).padStart(2,'0')},1000)}
  var tks=$$('#tickets .st');
  if(tks.length){var states=[['open','New'],['prog','In progress'],['done','Resolved']],n=0;
    setInterval(function(){var s=tks[n%tks.length],c=0;states.forEach(function(x,i){if(s.classList.contains(x[0]))c=i});var nx=states[(c+1)%3];s.className='st '+nx[0];s.textContent=nx[1];n++},1400)}
  function tick(){
    $$('[data-tz]').forEach(function(el){try{el.textContent=new Date().toLocaleTimeString('en-GB',{hour:'2-digit',minute:'2-digit',timeZone:el.dataset.tz})}catch(e){}});
    var ring=$('#dayring');if(ring){var p=new Date().toLocaleTimeString('en-GB',{timeZone:'Africa/Lagos',hour12:false}).split(':');ring.style.strokeDashoffset=326.7*(1-(+p[0]*3600+ +p[1]*60+ +p[2])/86400)}
  }
  tick();setInterval(tick,10000);
  var cal=$('#cal');
  if(cal){for(var d=1;d<=21;d++){var i2=document.createElement('i');i2.textContent=d;cal.appendChild(i2)}
    setInterval(function(){var c=$$('#cal i');c.forEach(function(x){x.className=''});for(var k=0;k<4;k++)c[Math.random()*21|0].className=Math.random()>.5?'on':'b'},1600)}
  /* score bars */
  var sc=$$('.vis-card[data-score]');
  if(sc.length&&'IntersectionObserver' in window){var so=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');so.unobserve(e.target)}})},{threshold:.3});sc.forEach(function(s){so.observe(s)})}
  else sc.forEach(function(s){s.classList.add('in')});
})();

/* ---------- globe ---------- */
(function(){
  var cv=$('#globe');if(!cv||!window.ELV_LAND)return;
  var ctx=cv.getContext('2d'),bin=atob(window.ELV_LAND);
  function bit(i){return (bin.charCodeAt(i>>3)>>(7-(i&7)))&1}
  function isLand(lat,lon){var r=Math.max(0,Math.min(89,Math.round((89-lat)/2))),c=((Math.round((lon+179)/2)%180)+180)%180;return bit(r*180+c)}
  var D=Math.PI/180;function v(a,o){return [Math.cos(a*D)*Math.sin(o*D),Math.sin(a*D),Math.cos(a*D)*Math.cos(o*D)]}
  var pts=[];
  for(var lat=-80;lat<=84;lat+=2.1){var n=Math.max(1,Math.round(360*Math.cos(lat*D)/2.1));for(var k=0;k<n;k++){var lon=-180+k*360/n;if(isLand(lat,lon))pts.push(v(lat,lon))}}
  var HQ=v(9.06,7.49);
  var cities=[["NEW YORK",40.7,-74],["",43.65,-79.4],["LONDON",51.5,-.12],["",52.37,4.9],["",52.52,13.4],["DUBAI",25.2,55.27],["SINGAPORE",1.35,103.8]].map(function(c){return {n:c[0],p:v(c[1],c[2])}});
  function arc(a,b){var d=Math.acos(Math.min(1,a[0]*b[0]+a[1]*b[1]+a[2]*b[2])),s=Math.sin(d),o=[];for(var i=0;i<=48;i++){var t=i/48,k1=Math.sin((1-t)*d)/s,k2=Math.sin(t*d)/s,h=1+Math.sin(Math.PI*t)*d*.18;o.push([(a[0]*k1+b[0]*k2)*h,(a[1]*k1+b[1]*k2)*h,(a[2]*k1+b[2]*k2)*h])}return o}
  var arcs=cities.map(function(c,i){return {p:arc(HQ,c.p),off:i*.17}});
  var W,H,R,vis=false;
  function size(){var d=Math.min(2,window.devicePixelRatio||1),r=cv.getBoundingClientRect();W=r.width;H=r.height;cv.width=W*d;cv.height=H*d;ctx.setTransform(d,0,0,d,0,0);R=Math.min(W,H*.82)*.40}
  size();addEventListener('resize',size);
  if('IntersectionObserver' in window)new IntersectionObserver(function(e){vis=e[0].isIntersecting}).observe(cv);else vis=true;
  var drag=0,dn=false,lx=0,vel=0;
  cv.addEventListener('pointerdown',function(e){dn=true;lx=e.clientX;cv.setPointerCapture(e.pointerId)});
  cv.addEventListener('pointermove',function(e){if(!dn)return;var dx=e.clientX-lx;lx=e.clientX;drag+=dx*.006;vel=dx*.006});
  cv.addEventListener('pointerup',function(){dn=false});
  var ct=Math.cos(.38),st=Math.sin(.38);
  function P(p,ca,sa,cy){var x=p[0]*ca+p[2]*sa,z0=-p[0]*sa+p[2]*ca,y=p[1]*ct-z0*st,z=p[1]*st+z0*ct;return [W/2+x*R,cy-y*R,z,x,y]}
  function on(q){return q[2]>0||(q[3]*q[3]+q[4]*q[4])>1}
  function f(t){
    if(!RM)requestAnimationFrame(f);if(!vis&&!RM)return;
    if(!dn){drag+=vel;vel*=.94}
    var a=.28+Math.sin(t*.00018)*.75+drag,ca=Math.cos(a),sa=Math.sin(a),cy=H*.44;ctx.clearRect(0,0,W,H);
    var g=ctx.createRadialGradient(W/2-R*.35,cy-R*.4,R*.1,W/2,cy,R);g.addColorStop(0,'rgba(36,78,170,.6)');g.addColorStop(.7,'rgba(10,28,70,.6)');g.addColorStop(1,'rgba(5,14,36,.35)');
    ctx.fillStyle=g;ctx.beginPath();ctx.arc(W/2,cy,R,0,7);ctx.fill();ctx.strokeStyle='rgba(120,160,255,.3)';ctx.stroke();
    pts.forEach(function(p){var q=P(p,ca,sa,cy);if(q[2]<0)return;ctx.fillStyle='rgba(190,210,255,'+(.18+q[2]*.75)+')';var s=1.1+q[2]*.9;ctx.fillRect(q[0]-s/2,q[1]-s/2,s,s)});
    arcs.forEach(function(A){ctx.beginPath();var pen=false;A.p.forEach(function(p){var q=P(p,ca,sa,cy);if(on(q)){pen?ctx.lineTo(q[0],q[1]):ctx.moveTo(q[0],q[1]);pen=true}else pen=false});
      ctx.strokeStyle='rgba(230,200,120,.5)';ctx.lineWidth=1.2;ctx.stroke();
      var q=P(A.p[Math.floor(((t*.00022+A.off)%1)*48)],ca,sa,cy);
      if(on(q)){ctx.fillStyle='#f6e3a8';ctx.shadowColor='#f1d894';ctx.shadowBlur=12;ctx.beginPath();ctx.arc(q[0],q[1],2.6,0,7);ctx.fill();ctx.shadowBlur=0}});
    ctx.font='600 10px Sora,sans-serif';
    cities.forEach(function(c){var q=P(c.p,ca,sa,cy);if(q[2]<.05)return;ctx.fillStyle='#d4af5f';ctx.beginPath();ctx.arc(q[0],q[1],3,0,7);ctx.fill();if(c.n){ctx.fillStyle='rgba(255,255,255,'+(.35+q[2]*.5)+')';ctx.fillText(c.n,q[0]+7,q[1]+3)}});
    var h=P(HQ,ca,sa,cy);
    if(h[2]>0){var pr=(t%2200)/2200;ctx.strokeStyle='rgba(241,216,148,'+(1-pr)+')';ctx.lineWidth=1.5;ctx.beginPath();ctx.arc(h[0],h[1],4+pr*20,0,7);ctx.stroke();ctx.fillStyle='#f6e3a8';ctx.beginPath();ctx.arc(h[0],h[1],5,0,7);ctx.fill();ctx.font='700 11px Sora,sans-serif';ctx.fillStyle='#f1d894';ctx.fillText('ABUJA HQ',h[0]+10,h[1]+4)}
  }
  requestAnimationFrame(f);
})();

/* ---------- scroll text, nav, progress, stacked cards ---------- */
var stx=$('#scrolltext'),wds=[];
if(stx){var gW=['managed','people,','structured','operations','scalable','support'];
  stx.innerHTML=stx.textContent.split(' ').map(function(w){return '<span class="wd'+(gW.indexOf(w)>-1?' g':'')+'">'+w+'</span>'}).join(' ');wds=$$('.wd',stx)}
var nav=$('#nav'),prog=$('#progress'),cards=$$('.scard'),heroEl=$('.hero')||$('.page-hero');
function onScroll(){
  var y=window.scrollY||0,dh=document.documentElement.scrollHeight-innerHeight;
  if(prog)prog.style.width=(dh>0?y/dh*100:0)+'%';
  if(nav)nav.classList.toggle('solid',heroEl?y>heroEl.offsetHeight-120:y>40);
  if(stx){var r=stx.getBoundingClientRect(),p=Math.min(1,Math.max(0,(innerHeight*.85-r.top)/(r.height+innerHeight*.35))),n=Math.round(p*wds.length);wds.forEach(function(w,i){w.classList.toggle('lit',i<n)})}
  cards.forEach(function(c,i){var k=0;for(var j=i+1;j<cards.length;j++){if(cards[j].getBoundingClientRect().top<=parseFloat(getComputedStyle(cards[j]).top)+2)k++}c.style.transform='scale('+(1-k*.04)+')';c.style.filter='brightness('+(1-k*.15)+')'});
}
addEventListener('scroll',onScroll,{passive:true});onScroll();

/* ---------- pointer effects ---------- */
var glow=$('#glow');
if(glow&&HOVER){var gx=innerWidth/2,gy=innerHeight/2,tx=gx,ty=gy;
  addEventListener('pointermove',function(e){tx=e.clientX;ty=e.clientY});
  (function g(){gx+=(tx-gx)*.12;gy+=(ty-gy)*.12;glow.style.transform='translate('+(gx-260)+'px,'+(gy-260)+'px)';requestAnimationFrame(g)})()}
$$('.lb').forEach(function(c){c.addEventListener('pointermove',function(e){var r=c.getBoundingClientRect();c.style.setProperty('--mx',e.clientX-r.left+'px');c.style.setProperty('--my',e.clientY-r.top+'px')})});
if(HOVER&&!RM){
  $$('.mag').forEach(function(b){b.addEventListener('pointermove',function(e){var r=b.getBoundingClientRect();b.style.transform='translate('+(e.clientX-r.left-r.width/2)*.22+'px,'+(e.clientY-r.top-r.height/2)*.3+'px)'});b.addEventListener('pointerleave',function(){b.style.transform=''})});
  $$('.sc').forEach(function(c){c.addEventListener('pointermove',function(e){var r=c.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;c.style.transform='perspective(900px) rotateY('+x*8+'deg) rotateX('+(-y*8)+'deg) translateY(-6px)'});c.addEventListener('pointerleave',function(){c.style.transform=''})});
}

/* ---------- accordion panes ---------- */
var panes=$$('#acc .pane');
panes.forEach(function(p){function a(){panes.forEach(function(x){x.classList.toggle('on',x===p)})}p.addEventListener('mouseenter',a);p.addEventListener('click',a);p.addEventListener('focus',a);p.setAttribute('tabindex','0')});

/* ---------- FAQ: one open at a time ---------- */
$$('.faq details').forEach(function(d){d.addEventListener('toggle',function(){if(d.open)$$('.faq details').forEach(function(o){if(o!==d)o.open=false})})});

/* ---------- lead form (contact page) ---------- */
(function(){
  var card=$('#lead');if(!card)return;
  var form=$('#leadform'),step=1,mode='proposal';
  var titles={proposal:['What do you need?','Tell us about the operation','Your details'],consult:['What shall we discuss?','When suits you?','Your details']};
  var hints={proposal:'Select every service you are interested in.',consult:'Choose the topics you would like to cover on the call.'};
  function setMode(m){
    mode=m;card.dataset.mode=m;
    $$('.mode button').forEach(function(b){b.classList.toggle('on',b.dataset.mode===m);b.setAttribute('aria-pressed',b.dataset.mode===m)});
    var h=$('#hint');if(h)h.textContent=hints[m];
    $('#submitlabel').textContent=m==='proposal'?'Submit request ':'Request consultation ';
    show();
  }
  function show(){
    $$('.step',form).forEach(function(s){s.classList.toggle('on',+s.dataset.s===step)});
    $('#wbar').style.width=Math.min(100,step/3*100)+'%';
    if(step<=3){$('#wtitle').textContent=titles[mode][step-1];$('#wcount').textContent='Step '+step+' of 3'}
    else{$('#wtitle').textContent='All done';$('#wcount').textContent=''}
    $('#wnav').style.display=step>3?'none':'flex';
    $('#wback').style.visibility=step===1?'hidden':'visible';
    $('#wnext').firstChild.nodeValue=step===3?($('#submitlabel').textContent):'Continue ';
    clearErr();
  }
  function err(msg,el){var e=$('#err');e.textContent=msg;e.classList.add('show');if(el){el.classList.add('bad');el.focus()}}
  function clearErr(){var e=$('#err');e.classList.remove('show');$$('.bad',form).forEach(function(x){x.classList.remove('bad')})}
  $$('.mode button').forEach(function(b){b.addEventListener('click',function(){step=1;setMode(b.dataset.mode)})});
  $$('.opts',form).forEach(function(g){g.addEventListener('click',function(e){var o=e.target.closest('.opt');if(!o)return;
    if(g.hasAttribute('data-single')){var was=o.classList.contains('sel');$$('.opt',g).forEach(function(x){x.classList.remove('sel')});if(!was)o.classList.add('sel')}else o.classList.toggle('sel');clearErr()})});
  function vals(name){var g=$('[data-name="'+name+'"]',form);return g?$$('.opt.sel',g).map(function(o){return o.textContent.trim()}):[]}
  function collect(){
    var f=form.elements;
    return {type:mode==='proposal'?'Proposal request':'Consultation request',services:vals('services'),teamSize:vals('teamSize').join(', '),coverage:vals('coverage').join(', '),languages:vals('languages'),
      preferredDate:f.date.value,preferredTime:f.time.value,timezone:f.timezone.value,
      name:f.name.value.trim(),company:f.company.value.trim(),email:f.email.value.trim(),country:f.country.value,message:f.message.value.trim(),
      website:f.website.value,page:location.href,submitted:new Date().toISOString()}
  }
  function validate3(){
    var f=form.elements;
    if(!f.name.value.trim()){err('Please enter your full name.',f.name);return false}
    if(!f.company.value.trim()){err('Please enter your company name.',f.company);return false}
    if(!/^\S+@\S+\.\S+$/.test(f.email.value.trim())){err('Please enter a valid business email address.',f.email);return false}
    return true}
  function plain(d){
    var L=[d.type,'','Name: '+d.name,'Company: '+d.company,'Email: '+d.email,'Country: '+d.country,'','Services: '+(d.services.join(', ')||'—')];
    if(d.type==='Proposal request'){L.push('Team size: '+(d.teamSize||'—'),'Coverage: '+(d.coverage||'—'),'Languages: '+(d.languages.join(', ')||'—'))}
    else{L.push('Preferred date: '+(d.preferredDate||'—'),'Preferred time: '+(d.preferredTime||'—'),'Time zone: '+(d.timezone||'—'))}
    L.push('','Message: '+(d.message||'—'));return L.join('\n')}
  function done(extra){
    step=4;show();var m=$('#donemsg');if(extra)m.textContent=extra;
    var wa=$('#donewa');if(wa){wa.hidden=false}
    card.scrollIntoView({behavior:RM?'auto':'smooth',block:'start'})}
  function submit(){
    var d=collect();if(d.website){done();return}  /* honeypot */
    var btn=$('#wnext');btn.disabled=true;btn.style.opacity=.7;
    function fallback(){
      var sub=encodeURIComponent('['+d.type+'] '+d.company+' — '+d.name);
      location.href='mailto:'+(CFG.email||'')+'?subject='+sub+'&body='+encodeURIComponent(plain(d));
      btn.disabled=false;btn.style.opacity=1;
      done('Your email app has opened with your request ready to send. Please press send to complete it. You can also message us on WhatsApp.')}
    if(!CFG.endpoint){fallback();return}
    var ctl=('AbortController' in window)?new AbortController():null,to=setTimeout(function(){ctl&&ctl.abort()},15000);
    fetch(CFG.endpoint,{method:'POST',mode:'no-cors',headers:{'Content-Type':'text/plain;charset=utf-8'},body:JSON.stringify(d),signal:ctl?ctl.signal:undefined})
      .then(function(){clearTimeout(to);btn.disabled=false;btn.style.opacity=1;done()})
      .catch(function(){clearTimeout(to);btn.disabled=false;btn.style.opacity=1;fallback()});
  }
  $('#wnext').addEventListener('click',function(){
    clearErr();
    if(step===1){if(!vals('services').length){err('Please select at least one option to continue.');return}}
    if(step===3){if(!validate3())return;submit();return}
    step++;show();
  });
  $('#wback').addEventListener('click',function(){if(step>1){step--;show()}});
  form.addEventListener('submit',function(e){e.preventDefault();$('#wnext').click()});
  form.addEventListener('keydown',function(e){if(e.key==='Enter'&&e.target.tagName!=='TEXTAREA'){e.preventDefault();$('#wnext').click()}});
  /* min date today */
  var dt=form.elements.date;if(dt){var n=new Date();dt.min=n.getFullYear()+'-'+String(n.getMonth()+1).padStart(2,'0')+'-'+String(n.getDate()).padStart(2,'0')}
  /* timezone guess */
  var tz=form.elements.timezone;try{var g=Intl.DateTimeFormat().resolvedOptions().timeZone;if(g&&tz&&!tz.value)tz.value=g}catch(e){}
  /* preselect from hash / query: #consultation, ?service=... */
  function fromHash(){var h=location.hash.replace('#','');if(h==='consultation'){step=1;setMode('consult')}else if(h==='proposal'){step=1;setMode('proposal')}}
  addEventListener('hashchange',fromHash);
  var q=new URLSearchParams(location.search).get('service');
  if(q){$$('[data-name="services"] .opt').forEach(function(o){if(o.textContent.trim().toLowerCase().indexOf(q.toLowerCase())>-1)o.classList.add('sel')})}
  setMode('proposal');fromHash();
})();

})();
