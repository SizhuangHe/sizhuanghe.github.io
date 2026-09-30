(()=>{"use strict";
const D=document,H=D.documentElement,$=(s,r=D)=>r.querySelector(s),$$=(s,r=D)=>[...r.querySelectorAll(s)];
const RM=matchMedia('(prefers-reduced-motion: reduce)').matches,now=()=>performance.now(),raf=requestAnimationFrame,rnd=n=>Math.random()*n|0;
const LS=(k,v)=>{try{return v==null?localStorage.getItem(k):localStorage.setItem(k,v)}catch(e){return null}};
const shuffle=a=>{for(let i=a.length-1;i>0;i--){const j=rnd(i+1);[a[i],a[j]]=[a[j],a[i]]}return a};
const AZ='abcdefghijklmnopqrstuvwxyz';
/* permutation p (p[i] = where i goes, 0-based) → list of cycles, 1-based, fixed points dropped */
const cycles=p=>{const s=[],o=[];p.forEach((_,i)=>{if(s[i]||p[i]===i)return;const c=[];for(let j=i;!s[j];j=p[j]){s[j]=1;c.push(j+1)}o.push(c)});return o};
const fmt=cs=>cs.map(c=>'('+c.join(' ')+')').join('')||'id';

/* ---- A1 · name denoise (random unmasking order, 1–2 random glyphs per char, ≤ 900 ms, once per session) ---- */
const nm=$('#name'),NAME=nm.textContent.trim();let dn=0;
function denoise(){if(RM||dn)return;dn=1;nm.setAttribute('aria-label',NAME);
  nm.innerHTML=[...NAME].map(c=>c===' '?' ':`<span class="ch m" aria-hidden="true">${c}</span>`).join('');
  const cs=$$('.ch',nm),T=40+(cs.length-1)*62+140;
  shuffle([...cs.keys()]).forEach((ci,k)=>{const el=cs[ci],up=el.textContent!==el.textContent.toLowerCase(),at=40+k*62,h=1+rnd(2);
    for(let i=0;i<h;i++)setTimeout(()=>{const g=AZ[rnd(26)];el.dataset.g=up?g.toUpperCase():g;el.className='ch hot'},at+i*60);
    setTimeout(()=>{el.className='ch'},at+h*60)});
  const fin=()=>{if(!dn)return;nm.textContent=NAME;nm.removeAttribute('aria-label');dn=0;digits()};setTimeout(fin,T+60)}

/* ---- A6 · scholar digits resolve from noise ---- */
function digits(){if(RM)return;$$('.dg').forEach(el=>{if(el._r)return;el._r=1;const v=el.dataset.v,t0=now(),L=[...v].map(()=>150+Math.random()*350);let lt=0;
  setTimeout(()=>{el.textContent=el.dataset.v;el._r=0},520);const f=t=>{const e=t-t0;if(e>=500||!el._r){el.textContent=el.dataset.v;return}if(t-lt>45){lt=t;el.textContent=[...v].map((c,i)=>e>=L[i]?c:rnd(10)).join('')}raf(f)};raf(f)})}
const sch=$('.scholar');sch.addEventListener('pointerenter',digits);sch.addEventListener('focusin',digits);
/* live Scholar numbers: gs_data.json on the google-scholar-stats branch (refreshed weekly by the update-scholar
   workflow). The HTML carries the last known numbers; these replace them in place, so nothing shifts. */
if(sch.dataset.src&&window.fetch)fetch(sch.dataset.src,{cache:'no-cache'}).then(r=>r.ok?r.json():null).then(d=>{if(!d)return;
  [['citations',d.citedby],['h-index',d.hindex]].forEach(([k,v])=>{const el=$(`.dg[data-k="${k}"]`,sch);if(!el||!Number.isFinite(v)||v<0)return;el.dataset.v=String(v);if(!el._r)el.textContent=el.dataset.v})}).catch(()=>{});

/* ---- A7 · avatar flip ---- */
const av=$('#avatar');av.addEventListener('click',()=>{const k=av.classList.toggle('on');av.setAttribute('aria-pressed',k);$('#avcap').textContent=(k?'2':'1')+' / 2 · flip'});

/* ---- A4 · section labels flicker 3–4 glyphs on first sight (text stays readable) ---- */
function flick(el){const t=$('.t',el),s=t.textContent,ix=shuffle([...s].map((c,i)=>/\w/.test(c)?i:-1).filter(i=>i>=0)).slice(0,3+rnd(2));let n=0;
  const iv=setInterval(()=>{if(++n>4){clearInterval(iv);t.textContent=s;return}t.textContent=[...s].map((c,i)=>ix.includes(i)&&Math.random()<.85?AZ[rnd(26)].toUpperCase():c).join('')},70)}
if(!RM&&'IntersectionObserver' in window)setTimeout(()=>{const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){io.unobserve(e.target);flick(e.target)}}),{threshold:1});$$('.lbl').forEach(l=>io.observe(l))},950);

/* ---- A5 · filter = permutation (FLIP, spring, 25 ms stagger) ---- */
const list=$('#pubs'),orig=$$('.pub',list),chips=$$('.chip'),sgo=$('#sigma'),cnt=$('#count');let cur='all';
chips.forEach(c=>c.addEventListener('click',()=>{const g=c.dataset.f;if(g===cur)return;cur=g;chips.forEach(x=>x.setAttribute('aria-pressed',x===c));
  const before=$$('.pub',list),top=new Map(before.map(r=>[r,r.getBoundingClientRect().top])),hit=r=>g==='all'||r.dataset.g.split(' ').includes(g),
    after=[...orig.filter(hit),...orig.filter(r=>!hit(r))],k=orig.filter(hit).length;
  after.forEach(r=>{r.classList.toggle('masked',!hit(r));list.appendChild(r)});
  sgo.textContent='σ = '+fmt(cycles(before.map(r=>after.indexOf(r))));
  cnt.textContent=g==='all'?orig.length+' papers':k+' of '+orig.length+' · rest masked';
  if(RM)return;
  after.forEach(r=>{const dy=top.get(r)-r.getBoundingClientRect().top;r.style.transition='none';r.style.transform=dy?`translateY(${dy}px)`:''});
  list.offsetHeight;
  after.forEach((r,i)=>{r.style.transition=`transform 450ms cubic-bezier(.34,1.56,.64,1) ${i*25}ms`;r.style.transform=''})}));

/* ---- abstracts ---- */
D.addEventListener('click',e=>{const b=e.target.closest('.abs-t');if(!b)return;const o=b.getAttribute('aria-expanded')!=='true';b.setAttribute('aria-expanded',o);D.getElementById(b.getAttribute('aria-controls')).classList.toggle('open',o)});

/* ================= Thumbnails: one small canvas per paper =================
   Each .tb holds a canvas that draws its paper's scene as a pure function of time t, so any
   frame (the reduced-motion final frame, a resize) can be drawn directly. A thumbnail plays once
   when it first scrolls into view, then rests on its final frame. Only visible, playing thumbnails
   tick; hover, tap, or Enter replays. Text appears only when the thumbnail is wide enough. */
const FM=(px,w=500)=>`${w} ${px}px "IBM Plex Mono", ui-monospace, Menlo, monospace`,FSI=px=>`italic 400 ${px}px Newsreader, Georgia, serif`;
const MX=D.createElement('canvas').getContext('2d'),TWc=new Map(),tw=(s,f)=>{const k=f+'|'+s;let w=TWc.get(k);if(w==null){MX.font=f;w=MX.measureText(s).width;TWc.set(k,w)}return w};
let C={},X=null;
function colors(){const s=getComputedStyle(H),g=n=>s.getPropertyValue(n).trim();C={ink:g('--ink'),graphite:g('--graphite'),mask:g('--mask'),rule:g('--rule'),accent:g('--yale'),signal:g('--signal'),paper:g('--paper')}}
const cl=(v,a=0,b=1)=>v<a?a:v>b?b:v,lerp=(a,b,u)=>a+(b-a)*u,sm=u=>u*u*(3-2*u),eo=u=>1-Math.pow(1-cl(u),3),bz=(a,b,c,d,q)=>(1-q)**3*a+3*(1-q)**2*q*b+3*(1-q)*q*q*c+q**3*d;
const mk=seed=>()=>{seed=seed+0x6D2B79F5|0;let t=Math.imul(seed^seed>>>15,1|seed);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296};
const gs=g=>Math.sqrt(-2*Math.log(1-g.rng()))*Math.cos(6.2832*g.rng()),shufG=(g,a)=>{for(let i=a.length-1;i>0;i--){const j=g.rng()*(i+1)|0;[a[i],a[j]]=[a[j],a[i]]}return a};
/* drawing helpers: the "engines" the scenes share */
const A=a=>{X.globalAlpha=a};
function dot(x,y,r,c,a=1){A(a);X.fillStyle=c;X.beginPath();X.arc(x,y,r,0,6.283);X.fill()}
function box(x,y,w,h,r,c,a=1){A(a);X.fillStyle=c;if(r&&X.roundRect){X.beginPath();X.roundRect(x,y,w,h,r);X.fill()}else X.fillRect(x,y,w,h)}
function lineP(p,c,w=1,a=1,dash){if(p.length<2)return;A(a);X.strokeStyle=c;X.lineWidth=w;X.setLineDash(dash||[]);X.beginPath();X.moveTo(p[0][0],p[0][1]);for(let i=1;i<p.length;i++)X.lineTo(p[i][0],p[i][1]);X.stroke();X.setLineDash([])}
function strand(p,c,w,a){X.beginPath();X.moveTo(p[0][0],p[0][1]);for(let k=1;k<p.length-1;k++){const q=p[k],r=p[k+1];X.quadraticCurveTo(q[0],q[1],(q[0]+r[0])/2,(q[1]+r[1])/2)}const e=p[p.length-1];X.lineTo(e[0],e[1]);
  X.lineCap='round';A(1);X.strokeStyle=C.paper;X.lineWidth=w+2.6;X.stroke();A(a);X.strokeStyle=c;X.lineWidth=w;X.stroke();X.lineCap='butt'}
function txt(s,x,y,c,px,a=1,al='center',w=500){A(a);X.font=FM(px,w);X.textAlign=al;X.fillStyle=c;X.fillText(s,x,y)}
function dust(g,lv){if(lv<=.01)return;X.fillStyle=C.mask;A(.12+.55*lv);for(const d of g.du){X.beginPath();X.arc(d[0],d[1],d[2],0,6.283);X.fill()}}
/* token engine: a masked block that decodes into text, or into a bar when the thumbnail is too small for text */
function token(g,lab,x,y,m,c,fz=g.fs,a=1){if(fz){const w=tw(lab,FM(fz));if(m>0)box(x-w/2,y-fz*.34,w,fz*.68,1.5,C.mask,m*a);if(m<1)txt(lab,x,y+.5,c,fz,(1-m)*a)}
  else{const w=lab.length*2.1;box(x-w/2,y-1.5,w,3,1,m>.5?C.mask:c,a*(m>.5?1:.8))}}
function flow(ws,x0,x1,lh,gap){const L=[[]],lw=[0];ws.forEach((w,i)=>{let r=L.length-1;if(lw[r]>0&&lw[r]+gap+w>x1-x0){L.push([]);lw.push(0);r++}L[r].push([i,w]);lw[r]+=(lw[r]>0?gap:0)+w});
  const o=[];L.forEach((ln,r)=>{let x=x0;ln.forEach(([i,w])=>{o[i]={x:x+w/2,y:r*lh,w};x+=w+gap})});o.rows=L.length;return o}
const wOf=(g,labs,fz=g.fs)=>labs.map(l=>fz?tw(l,FM(fz)):l.length*2.1);

const SC={
/* CaDDi · neutral tokens denoise over a few steps stacked as rows x_T … x_0; every new row reads from ALL earlier rows
   (accent arcs, right), where a Markov model would read only the row just above (one dashed arrow, left) */
caddi:{dur:4900,cap:'CaDDi ▸ each step reads every earlier state, not just the last',TOK:'GATTACAG',
  build(g){const s=g.s,p=g.p,n=8,R=6;s.n=n;s.R=R;s.lab=g.fs>=8.5;s.let=g.fs>=7.5;const side=Math.max(12,Math.round(g.W*.15)),labH=s.lab?g.fs*1.5:0;
    s.pitch=(g.H-2*p-labH)/R;s.c=Math.min((g.W-2*p-2*side)/n,s.pitch*.94);s.gw=s.c*n;s.gx=(g.W-s.gw)/2;s.gy=p+(g.H-2*p-labH-s.pitch*R)/2;s.side=Math.min(side,s.gx-p);s.labY=g.H-p-labH*.35;
    const ord=shufG(g,[...Array(n).keys()]),cum=[0,2,3,5,7,8];s.dec=[];ord.forEach((i,r)=>{s.dec[i]=cum.findIndex(c=>c>r)})},
  draw(g,t){const s=g.s,T0=450,ST=720,R=s.R,kk=cl(Math.floor((t-T0)/ST)+1,0,R-1),ry=k=>s.gy+s.pitch*(k+.5),xr=s.gx+s.gw+3,xl=s.gx-3;dust(g,1-kk/(R-1));
    for(let k=0;k<=kk;k++){const y=ry(k),ta=T0+(k-1)*ST,fa=k===0?1:cl((t-ta)/260),cs=s.c*.84;
      for(let i=0;i<s.n;i++){const x=s.gx+i*s.c+s.c/2,dec=s.dec[i]<=k,fresh=dec&&s.dec[i]===k&&t-ta<520;
        if(!dec)box(x-cs/2,y-cs/2,cs,cs,1.5,C.mask,.9*fa);
        else{box(x-cs/2,y-cs/2,cs,cs,1.5,fresh?C.signal:C.accent,(fresh?.2:.1)*fa);if(s.let)txt(this.TOK[i],x,y+.5,fresh?C.signal:C.ink,Math.min(g.fs,s.c*.72),fa);else box(x-cs/2+1.5,y-1,cs-3,2,0,fresh?C.signal:C.ink,.8*fa)}}}
    for(let k=1;k<=kk;k++){const ta=T0+(k-1)*ST,al=cl((t-ta)/320)*(k===kk?1:cl(1-(t-ta-ST)/260));if(al<=0)continue;const yk=ry(k);
      for(let j=0;j<k;j++){const yj=ry(j),bul=Math.min(s.side-3,3+(k-j)*(s.side-3)/(R-1));A(.6*al);X.strokeStyle=C.accent;X.lineWidth=1;X.beginPath();X.moveTo(xr,yj);X.quadraticCurveTo(xr+bul*2,(yj+yk)/2,xr+1,yk);X.stroke()}
      dot(xr+1,yk,1.6,C.accent,al);
      const yp=ry(k-1);lineP([[xl,yp+2],[xl,yk-3]],C.graphite,1,.6*al,[2,2]);A(.6*al);X.fillStyle=C.graphite;X.beginPath();X.moveTo(xl-2.2,yk-4.5);X.lineTo(xl+2.2,yk-4.5);X.lineTo(xl,yk-1.5);X.closePath();X.fill()}
    if(s.lab){const f=Math.max(7,g.fs-1.5);txt('Markov: last row',s.gx-s.side,s.labY,C.graphite,f,1,'left',400);txt('CaDDi: all rows',s.gx+s.gw+s.side,s.labY,C.accent,f,1,'right',500)}}},
/* Soft-Rank Diffusion · soft ranks diffuse, reflect off the edges, settle; ranks placed one position at a time */
softrank:{dur:5000,cap:'Soft-Rank ▸ soft ranks diffuse, reflect, settle',
  build(g){const s=g.s,big=g.fs>=8.5;s.big=big;s.n=big?7:5;const n=s.n,V=[42,7,19,88,3,61,25].slice(0,n);s.V=V;s.rank=[];V.map((v,i)=>[v,i]).sort((a,b)=>a[0]-b[0]).forEach(([,i],r)=>{s.rank[i]=r});
    s.lab=g.fs>0;const lw=s.lab?tw('88',FM(g.fs))+8:0;s.x0=g.p;s.x1=g.W-g.p-lw-(big?12:4);s.pitch=(g.H-2*g.p)/n;s.y0=g.p+s.pitch/2;
    const K=24,lo=-.5,hi=n-.5,ref=y=>{while(y<lo||y>hi)y=y<lo?2*lo-y:2*hi-y;return y};let far=-1;s.K=K;
    s.path=V.map((v,i)=>{const s0=g.rng()*(n-1),r=s.rank[i],Wk=[0];for(let k=1;k<=K;k++)Wk.push(Wk[k-1]+gs(g));if(Math.abs(s0-r)>far){far=Math.abs(s0-r);s.hl=i}
      return Wk.map((w,k)=>{const u=k/K;return ref(lerp(s0,r,sm(u))+1.9*(w-u*Wk[K])/Math.sqrt(K)*Math.pow(1-u,.5))})})},
  draw(g,t){const s=g.s,n=s.n,U0=200,UD=3000,tP=U0+UD+150,u=cl((t-U0)/UD),pl=cl(Math.floor((t-tP)/140)+1,0,n),yO=r=>s.y0+r*s.pitch,xO=v=>s.x0+v*(s.x1-s.x0),K=s.K;
    dust(g,1-u);const top=yO(-.5),bot=yO(n-.5);lineP([[s.x0,top],[g.W-g.p,top]],C.mask,1,1,[2,2.5]);lineP([[s.x0,bot],[g.W-g.p,bot]],C.mask,1,1,[2,2.5]);
    if(u>0&&u<1)lineP([[xO(u),top+2],[xO(u),bot-2]],C.rule);
    const at=(i,v)=>{const f=v*K,k=Math.min(K-1,f|0);return lerp(s.path[i][k],s.path[i][k+1],f-k)};
    for(const i of[...Array(n).keys()].filter(i=>i!==s.hl).concat(s.hl)){const pts=[];for(let k=0;k<=Math.min(K,Math.floor(u*K));k++)pts.push([xO(k/K),yO(s.path[i][k])]);const e=[xO(u),yO(at(i,u))];pts.push(e);
      const h=i===s.hl;strand(pts,h?C.signal:C.accent,h?1.6:1,h?1:.7);dot(e[0],e[1],h?2:1.6,h?C.signal:C.accent);dot(pts[0][0],pts[0][1],1.3,C.mask,.9);
      if(s.lab){const r=s.rank[i],l=String(s.V[i]);txt(l,e[0]+4+tw(l,FM(g.fs))/2,e[1]+.5,pl>r&&t-(tP+r*140)<450?C.signal:C.ink,g.fs)}}
    for(let r=0;r<n;r++){if(s.big)txt(String(r+1),g.W-g.p,yO(r)+.5,r<pl?C.accent:C.mask,g.fs-1.5,1,'right',400);else if(r<pl)box(g.W-g.p-2,yO(r)-1,2,2,0,C.accent)}}},
/* C2S-Scale · an expression profile is ranked into a cell sentence, read, and labelled */
c2s:{dur:5400,cap:'C2S ▸ a cell, read as a sentence of genes',
  GN:['MALAT1','TMSB4X','B2M','FTL','LYZ','S100A9','ACTB','EEF1A1','S100A8','FTH1','TYROBP','CST3'],GV:[1,.93,.9,.86,.82,.78,.74,.7,.66,.63,.58,.55],
  build(g){const s=g.s,fs=g.fs,p=g.p;s.n=fs>=8.5?12:8;const n=s.n,GN=this.GN;
    if(fs){const al=[...Array(n).keys()].sort((a,b)=>GN[a]<GN[b]?-1:1),cols=4,rows=Math.ceil(n/cols),cw=(g.W-2*p)/cols,ch=(g.H-2*p)/rows;
      s.A=[];al.forEach((i,k)=>{s.A[i]={x:p+cw*(k%cols)+cw/2,y:p+ch*(k/cols|0)+ch*.36,bw:cw-8}});
      const lh=Math.round(fs*1.7),lay=flow(wOf(g,GN.slice(0,n)),p,g.W-p,lh,tw(' ',FM(fs))),ph=fs*1.9,bh=(lay.rows-1)*lh+ph,y0=p+fs*.5+Math.max(0,(g.H-2*p-fs-bh)/2);
      s.B=lay.map(q=>({x:q.x,y:y0+q.y}));s.py=y0+(lay.rows-1)*lh+ph}
    else{const bw=(g.W-2*p)/n;s.ord=shufG(g,[...Array(n).keys()]);s.bx=k=>p+bw*k+bw/2;s.bw=bw*.62}},
  draw(g,t){const s=g.s,n=s.n,TB=1500,TC=2600,RS=110,TP=TC+n*RS+120,k=Math.floor((t-TC)/RS),GV=this.GV,gr=eo((t-150)/650);dust(g,t<TB?.5:t<TC?.25:.05);
    if(g.fs){const fa=cl(1-(t-TB)/350);for(let i=0;i<n;i++){const a=s.A[i],b=s.B[i],u=eo((t-TB-i*40)/550),x=lerp(a.x,b.x,u),y=lerp(a.y,b.y,u);
        if(fa>0){box(a.x-a.bw/2,a.y+g.fs*.85,a.bw,2,0,C.mask,fa);box(a.x-a.bw/2,a.y+g.fs*.85,a.bw*GV[i]*gr,2,0,C.accent,.85*fa)}
        token(g,this.GN[i],x,y,t<120?1:0,t<TB?C.ink:k===i?C.signal:k>i?C.ink:C.graphite);
        if(k===i){const w=tw(this.GN[i],FM(g.fs));box(x-w/2,y+g.fs*.65,w,1.2,0,C.signal)}}
      if(t>TP){const pr='→ CD14⁺ monocyte',m=Math.min(pr.length,2+Math.floor((t-TP)/40));A(1);X.font=FSI(g.fs*1.45);X.textAlign='left';X.fillStyle=C.accent;X.fillText(pr.slice(0,m),g.p,s.py)}}
    else{const base=g.H-g.p-4,mh=g.H-2*g.p-8;for(let i=0;i<n;i++){const u=eo((t-TB-i*40)/550),x=lerp(s.bx(s.ord.indexOf(i)),s.bx(i),u),h=mh*GV[i]*gr;
        box(x-s.bw/2,base-h,s.bw,h,.5,k===i?C.signal:t>TC&&k>i?C.accent:C.graphite,t<TB?.55:.85)}
      if(t>TP)box(g.p,base+2,(g.W-2*g.p)*cl((t-TP)/500),2,0,C.accent)}}},
/* STRIDE · refinement written as a chain of atomic edits, each applied to the sequence */
stride:{dur:5200,cap:'STRIDE ▸ refinement as a chain of atomic edits',
  SEQ:'MQYKLILNGKTL',E:[{op:'SUB',id:3,to:'E'},{op:'INS',after:8,id:12,to:'D'},{op:'DEL',id:10}],
  build(g){const s=g.s;let ids=[...Array(12).keys()];const lab=[...this.SEQ,'D'];
    s.txt=this.E.map(e=>{let r;if(e.op==='SUB')r=`SUB ${lab[e.id]}${ids.indexOf(e.id)+1}→${e.to}`;else if(e.op==='INS'){const q=ids.indexOf(e.after);r=`INS ${e.to}@${q+2}`;ids.splice(q+1,0,e.id)}else{const q=ids.indexOf(e.id);r=`DEL ${lab[e.id]}${q+1}`;ids.splice(q,1)}return r});
    const f=g.fs;s.pitch=Math.min(f?f*1.45:7,(g.W-2*g.p)/13);s.lh=f?f*1.5:5;s.ly=g.p+(f?f*.55:2);s.sy=g.H-g.p-s.pitch/2-1},
  ta(k){return 1100+k*1300},
  state(t){let ids=[...Array(12).keys()];const lab=[...this.SEQ,'D'],ed={};this.E.forEach((e,k)=>{const ta=this.ta(k);if(t<ta-(e.op==='INS'?180:e.op==='SUB'?150:0))return;
      if(e.op==='SUB'){if(t>=ta)lab[e.id]=e.to;ed[e.id]=k}else if(e.op==='INS'){ids.splice(ids.indexOf(e.after)+1,0,e.id);ed[e.id]=k}else if(t>=ta+260)ids.splice(ids.indexOf(e.id),1);else ed[e.id]=k});return{ids,lab,ed}},
  draw(g,t){const s=g.s,{ids,lab,ed}=this.state(t),n=ids.length,f=g.fs;dust(g,.4*(1-cl((t-700)/3900)));
    this.E.forEach((e,k)=>{const t0=this.ta(k)-400;if(t<t0)return;const y=s.ly+k*s.lh,str=s.txt[k];
      if(f){txt(str.slice(0,Math.min(str.length,Math.floor((t-t0)/(300/str.length)))),g.p,y,C.ink,f*.95,1,'left',400);if(t>t0+700)txt('✓',g.p+tw('SUB K4→E ',FM(f*.95,400)),y,C.accent,f*.95,1,'left',400)}
      else{box(g.p,y-1,g.W*.45*cl((t-t0)/300),2,0,C.ink,.6);if(t>t0+700)box(g.p+g.W*.45+4,y-1,4,2,0,C.accent)}});
    ids.forEach((id,q)=>{const x=g.W/2+(q-(n-1)/2)*s.pitch,k=ed[id],e=k!=null?this.E[k]:null,ta=k!=null?this.ta(k):0,cs=s.pitch-1.5;let y=s.sy,al=1,m=0;
      if(e&&e.op==='SUB'&&t>ta-150&&t<ta+60)m=1;if(e&&e.op==='INS'&&t<ta+60)m=1;if(e&&e.op==='DEL'){m=1;y-=6*cl((t-ta)/260);al=1-cl((t-ta)/260)}
      const c=k==null?C.ink:t-ta<600?C.signal:C.accent;A(.9*al);X.strokeStyle=C.rule;X.lineWidth=1;X.strokeRect(x-cs/2+.5,y-cs/2+.5,cs-1,cs-1);
      if(f)token(g,lab[id],x,y,m,c,f*.95,al);else box(x-cs/2+1.5,y-cs/2+1.5,cs-3,cs-3,0,m?C.mask:c,al*(k==null?.35:.9))})}},
/* MoRSE · a task becomes a DAG of (role, subtask) agents, routed to LoRA experts; one sparse reward credits experts and router separately */
morse:{dur:5600,cap:'MoRSE ▸ subtasks routed to LoRA experts',
  N:[[0,[]],[1,[0]],[1,[0]],[2,[1,2]],[3,[3]]],EX:[0,1,2,1,3],NE:4,
  build(g){const s=g.s,p=g.p,x0=p+6,x1=g.W-p-14,dy0=p+4,dy1=g.H*.58;
    s.np=this.N.map(([L],i)=>{const same=this.N.map((q,j)=>j).filter(j=>this.N[j][0]===L),j=same.indexOf(i);return{x:lerp(x0,x1,L/3),y:same.length>1?lerp(dy0+3,dy1-2,j/(same.length-1)):(dy0+dy1)/2}});
    s.r=Math.max(2.2,g.W/60);s.by=g.H-p-s.r-3;s.rx=p+s.r;s.ep=[...Array(this.NE).keys()].map(k=>({x:lerp(p+s.r*6,g.W-p-s.r,k/(this.NE-1)),y:s.by}))},
  draw(g,t){const s=g.s,N=this.N,EX=this.EX,TE=1100,ES=420,TR=TE+N.length*ES+150,TC=TR+350,ed=cl((t-600)/400),r=s.r,ly=s.by+r+2.5;dust(g,t<TE?.4:.05);
    lineP([[s.rx+r+3,ly],[g.W-g.p,ly]],C.rule);
    N.forEach(([L,deps],i)=>{const b=s.np[i];deps.forEach(d=>{const a=s.np[d],mx=(a.x+b.x)/2;A(ed);X.strokeStyle=C.mask;X.lineWidth=1;X.beginPath();X.moveTo(a.x,a.y);X.bezierCurveTo(mx,a.y,mx,b.y,b.x,b.y);X.stroke();
      const u=(t-(TE+d*ES+200))/350;if(u>0&&u<1){const q=sm(u);dot(bz(a.x,mx,mx,b.x,q),bz(a.y,a.y,b.y,b.y,q),1.6,C.signal)}})});
    N.forEach((q,i)=>{const te=TE+i*ES;if(t<te)return;const e=s.ep[EX[i]],o=s.np[i],u=cl((t-te)/220);lineP([[o.x,o.y+r],[lerp(o.x,e.x,u),lerp(o.y+r,e.y-r-1,u)]],C.accent,1,t<te+700?.8:.25,[1.5,2])});
    N.forEach((q,i)=>{const te=TE+i*ES,o=s.np[i],u=eo((t-150)/550),x=lerp(s.np[0].x,o.x,u),y=lerp(s.np[0].y,o.y,u),c=t>=te&&t<te+420?C.signal:t>=te?C.ink:C.graphite;
      dot(x,y,r,C.paper);A(1);X.strokeStyle=c;X.lineWidth=1.2;X.beginPath();X.arc(x,y,r,0,6.283);X.stroke();if(t>=te)dot(x,y,r*.5,c)});
    s.ep.forEach((e,k)=>{const hit=N.some((q,i)=>EX[i]===k&&t>=TE+i*ES+150&&t<TE+i*ES+550),used=N.some((q,i)=>EX[i]===k&&t>=TE+i*ES+150);box(e.x-r,e.y-r,2*r,2*r,1,hit?C.signal:used?C.accent:C.mask)});
    A(1);X.fillStyle=t>=TC+250?C.signal:C.graphite;X.beginPath();X.moveTo(s.rx,s.by-r);X.lineTo(s.rx+r,s.by);X.lineTo(s.rx,s.by+r);X.lineTo(s.rx-r,s.by);X.closePath();X.fill();
    if(t>=TR){const v=s.np[4],rx=v.x+r*2.6;dot(rx,v.y,r*.8,C.signal,cl((t-TR)/300));
      if(t>=TC){const f=cl((t-TC)/500);[...new Set(EX)].forEach(k=>{const e=s.ep[k];A(.5*f);X.strokeStyle=C.accent;X.lineWidth=1;X.beginPath();X.moveTo(rx,v.y+r);X.quadraticCurveTo(rx,e.y-r*3,e.x,e.y-r-1);X.stroke()});
        lineP([[rx,v.y+r],[rx,ly],[s.rx+r+2,ly]],C.signal,1.2,.8*cl((t-TC-250)/500),[2,2])}}}},
/* FLUX · unpaired snapshots on a curved manifold; transport follows the curve, and the expert switches with the regime */
flux:{dur:5400,cap:'FLUX ▸ curved transport; experts switch with the regime',
  build(g){const s=g.s,p=g.p,W=g.W,H=g.H;s.arc=u=>[lerp(p+6,W-p-6,u),H-p-7-(H-2*p-16)*Math.sin(Math.PI*u)*.85];s.st=[.08,.5,.92];
    const R=Math.max(3,Math.min(W,H)*.08);s.cl=s.st.map(u=>{const[a,b]=s.arc(u);return[...Array(12)].map(()=>[a+gs(g)*R,b+gs(g)*R*.7])});
    s.np=Math.max(5,Math.round(W/22));s.lane=[...Array(s.np)].map(()=>[gs(g)*R*.7,g.rng()*6.28])},
  pos(s,i,u){const a=lerp(s.st[0],s.st[2],u),[x,y]=s.arc(a),[x2,y2]=s.arc(a+1e-3),dx=x2-x,dy=y2-y,L=Math.hypot(dx,dy)||1,[o,ph]=s.lane[i],off=o*(.6+.4*Math.sin(u*6+ph));return[x-dy/L*off,y+dx/L*off]},
  draw(g,t){const s=g.s,u=cl((t-900)/3400),K=40;dust(g,.35*(1-u));
    lineP(s.st.map(v=>s.arc(v)),C.mask,1,1,[2,2.5]);
    s.cl.forEach((c,k)=>{const f=cl((t-k*220)/400);c.forEach(q=>dot(q[0],q[1],1.1,C.ink,.45*f))});
    for(let i=0;i<s.np;i++){const pts=[];for(let k=0;k<=K*u;k++)pts.push(this.pos(s,i,k/K));pts.push(this.pos(s,i,u));const cut=Math.min(pts.length,K/2+1);
      lineP(pts.slice(0,cut),C.accent,1,.55);if(u>.5)lineP(pts.slice(cut-1),C.signal,1,.6);const e=pts[pts.length-1];if(u>0)dot(e[0],e[1],1.5,u>.5?C.signal:C.accent)}
    const y=g.H-g.p+1,x0=s.arc(s.st[0])[0],xm=s.arc(s.st[1])[0],x2=s.arc(s.st[2])[0];if(u>0){box(x0,y,Math.min(u,.5)/.5*(xm-x0),2,0,C.accent,.9);if(u>.5)box(xm,y,(u-.5)/.5*(x2-xm),2,0,C.signal,.9)}}},
/* TANTE · rollout by local Taylor expansions; the step shrinks where the solution curves sharply */
tante:{dur:5600,cap:'TANTE ▸ Taylor steps sized to the dynamics',
  uf:x=>.5+.22*Math.sin(2*Math.PI*1.1*x)+.28*Math.exp(-(((x-.58)/.07)**2)),
  build(g){const s=g.s,uf=this.uf;s.d1=x=>(uf(x+1e-3)-uf(x-1e-3))/2e-3;s.d2=x=>(uf(x+1e-3)-2*uf(x)+uf(x-1e-3))/1e-6;
    const st=[0];let x=0;while(x<1){const c=Math.abs(s.d2(x))+Math.abs(s.d2(Math.min(1,x+.03)));x=Math.min(1,x+cl(.14/(1+c/18),.025,.14));st.push(x)}s.st=st;s.x0=g.p;s.x1=g.W-g.p;s.y0=g.p;s.y1=g.H-g.p-7},
  draw(g,t){const s=g.s,uf=this.uf,Wd=s.x1-s.x0,Y=v=>s.y1-(v-.1)/.95*(s.y1-s.y0),Xp=v=>s.x0+v*Wd,n=s.st.length,SD=Math.max(150,3800/n),k=cl(Math.floor((t-400)/SD)+1,0,n-1);dust(g,.3*(1-k/(n-1)));
    const pts=[];for(let i=0;i<=80;i++)pts.push([Xp(i/80),Y(uf(i/80))]);lineP(pts,C.mask,1,1,[2,2]);
    for(let j=0;j<k;j++){const a=s.st[j],b=s.st[j+1],u0=uf(a),d1=s.d1(a),d2=s.d2(a),q=[];for(let m=0;m<=12;m++){const tau=(b-a)*m/12;q.push([Xp(a+tau),Y(u0+d1*tau+.5*d2*tau*tau)])}
      const fresh=j===k-1&&k<n-1;lineP(q,fresh?C.signal:C.accent,1.2,fresh?1:.85);dot(Xp(a),Y(u0),1.5,C.ink)}
    if(k===n-1)dot(Xp(1),Y(uf(1)),1.5,C.ink);const yb=g.H-g.p-1;lineP([[s.x0,yb],[s.x1,yb]],C.rule);for(let j=0;j<=k;j++)box(Xp(s.st[j])-.5,yb-3,1,6,0,j===k&&k<n-1?C.signal:C.graphite)}},
/* COAST · a causal model emits each next state together with its own time step: fine steps near the steep front */
coast:{dur:5600,cap:'COAST ▸ predicts the next state and its own Δt',
  wv:t=>.13-.09*Math.exp(-(((t-.5)/.16)**2)),
  build(g){const s=g.s,rows=[0];let tt=0;while(tt<1){tt=Math.min(1,tt+cl(this.wv(tt)*.55,.02,.08));rows.push(tt)}s.rows=rows;
    s.x0=g.p+12;s.x1=g.W-g.p;s.nx=Math.max(24,Math.floor((s.x1-s.x0)/2.2));s.y0=g.p+1;s.y1=g.H-g.p-1;s.rh=Math.max(1.1,(s.y1-s.y0)*.019)},
  draw(g,t){const s=g.s,n=s.rows.length,SD=Math.max(130,3900/n),k=cl(Math.floor((t-300)/SD)+1,0,n),cw=(s.x1-s.x0)/s.nx,Yt=v=>s.y0+v*(s.y1-s.y0);dust(g,.3*(1-k/n));
    lineP([[s.x0-3,s.y0],[s.x0-3,s.y1]],C.rule);
    for(let j=0;j<k;j++){const tt=s.rows[j],y=Yt(tt),w=this.wv(tt),c=.2+.6*tt,fresh=j===k-1&&k<n;
      for(let i=0;i<s.nx;i++){const v=Math.exp(-(((i/(s.nx-1)-c)/w)**2));if(v>.05)box(s.x0+i*cw,y-s.rh/2,cw+.3,s.rh,0,fresh?C.signal:C.accent,.12+.85*v)}
      const h=j<n-1?s.rows[j+1]-tt:0;box(g.p,y-s.rh/2,Math.max(1.5,cl(h/.08)*8),s.rh,0,fresh?C.signal:C.graphite,.8)}}},
/* CaLMFlow · noise flows to data along discretised paths; each new step attends to its whole history (Volterra, not a local ODE) */
calmflow:{dur:5600,cap:'CaLMFlow ▸ each step attends to its whole path',
  build(g){const s=g.s,p=g.p,W=g.W,H=g.H,cy=H/2,cx0=p+W*.13,R0=Math.min(H*.16,W*.08),R1=(H-2*p)*.42,cx1=W-p-R1-2;s.K=8;s.n=Math.max(6,Math.round(W/16));s.tg={x:cx1,y:cy,r:R1};
    s.tr=[...Array(s.n)].map((_,i)=>{const a=i/s.n*6.283+g.rng()*.3,sx=cx0+gs(g)*R0,sy=cy+gs(g)*R0,ex=cx1+Math.cos(a)*R1,ey=cy+Math.sin(a)*R1,bend=gs(g)*H*.1;
      return[...Array(s.K+1)].map((_,k)=>{const u=k/s.K;return[lerp(sx,ex,sm(u)),lerp(sy,ey,sm(u))+Math.sin(Math.PI*u)*bend]})});s.hl=0},
  draw(g,t){const s=g.s,SD=380,k=cl(Math.floor((t-400)/SD)+1,0,s.K),fr=cl((t-400-(k-1)*SD)/SD);dust(g,.4*(1-k/s.K));
    A(1);X.strokeStyle=C.mask;X.lineWidth=1;X.setLineDash([2,2.5]);X.beginPath();X.arc(s.tg.x,s.tg.y,s.tg.r,0,6.283);X.stroke();X.setLineDash([]);
    s.tr.forEach((pts,i)=>{const h=i===s.hl,q=pts.slice(0,k+1);lineP(q,h?C.signal:C.accent,h?1.3:1,h?1:.45);q.forEach((pt,j)=>dot(pt[0],pt[1],j===0?1.2:h?1.8:1.2,j===0?C.graphite:h?C.signal:C.accent,j===0?.6:h?1:.7))});
    if(k>1){const q=s.tr[s.hl],e=q[k],f=k<s.K?1-fr*.5:.5;for(let j=0;j<k-1;j++)lineP([e,q[j]],C.signal,.8,.35*f)}}},
/* Edge of Chaos · three elementary cellular automata; the complex one (Rule 110) sits at the sweet spot */
eoc:{dur:5200,cap:'Edge of Chaos ▸ a sweet spot of data complexity',
  build(g){const s=g.s,p=g.p;s.lab=g.fs>=8.5;s.gap=Math.max(4,g.W*.04);s.pw=(g.W-2*p-2*s.gap)/3;s.cs=g.W>=170?2.4:g.W>=120?2:1.6;s.nc=Math.floor(s.pw/s.cs);
    s.top=p;s.ya=g.H-p-(s.lab?g.fs*1.5:4);s.nr=Math.floor((s.ya-3-s.top)/s.cs);
    s.G=[108,110,30].map(R=>{let row=[...Array(s.nc)].map(()=>g.rng()<.5?1:0);const out=[row];for(let r=1;r<s.nr;r++){const nx=row.map((c,i)=>R>>(row[(i-1+s.nc)%s.nc]<<2|c<<1|row[(i+1)%s.nc])&1);out.push(nx);row=nx}return out})},
  draw(g,t){const s=g.s,rows=cl(Math.floor((t-200)/(3600/s.nr)),0,s.nr);dust(g,.2*(1-rows/s.nr));
    s.G.forEach((grid,k)=>{const x0=g.p+k*(s.pw+s.gap),mid=k===1;for(let r=0;r<rows;r++){const row=grid[r],y=s.top+r*s.cs;A(mid?.9:.42);X.fillStyle=mid?(r===rows-1&&rows<s.nr?C.signal:C.accent):C.graphite;for(let i=0;i<s.nc;i++)if(row[i])X.fillRect(x0+i*s.cs,y,s.cs*.88,s.cs*.88)}});
    lineP([[g.p,s.ya],[g.W-g.p,s.ya]],C.rule);box(g.p+s.pw+s.gap,s.ya-1,s.pw*cl((t-3800)/500),2,0,C.accent);
    if(s.lab)['periodic','complex','chaotic'].forEach((l,k)=>txt(l,g.p+k*(s.pw+s.gap)+s.pw/2,s.ya+g.fs*.85,k===1?C.accent:C.graphite,g.fs-1,1,'center',k===1?500:400))}},
/* Operator learning meets numerical analysis · the network as an operator; iterating it converges to a fixed point */
iter:{dur:5400,cap:'Iterative methods ▸ iterate the operator to its fixed point',
  G:x=>.35+.35*Math.cos(2.2*x),
  build(g){const s=g.s;s.S=g.H-2*g.p;s.x0=g.p;s.y0=g.p;s.it=[.06];for(let k=0;k<9;k++)s.it.push(this.G(s.it[k]));let f=.5;for(let k=0;k<300;k++)f=this.G(f);s.fx=f;
    s.bx=g.p+s.S+Math.max(6,g.W*.06);s.bw=g.W-g.p-s.bx},
  draw(g,t){const s=g.s,Sx=v=>s.x0+v*s.S,Sy=v=>s.y0+(1-v)*s.S,n=s.it.length-1,SD=380,k=cl(Math.floor((t-300)/SD)+1,0,n);dust(g,.25*(1-k/n));
    A(1);X.strokeStyle=C.rule;X.lineWidth=1;X.strokeRect(Sx(0)+.5,Sy(1)+.5,s.S-1,s.S-1);lineP([[Sx(0),Sy(0)],[Sx(1),Sy(1)]],C.mask,1,1,[2,2]);
    const cv=[];for(let i=0;i<=40;i++)cv.push([Sx(i/40),Sy(this.G(i/40))]);lineP(cv,C.accent,1.2,.85);
    for(let j=0;j<k;j++){const a=s.it[j],b=s.it[j+1],fresh=j===k-1&&k<n;lineP([[Sx(a),Sy(j?a:0)],[Sx(a),Sy(b)],[Sx(b),Sy(b)]],fresh?C.signal:C.ink,1,fresh?1:.5)}
    if(k>=n){A(1);X.strokeStyle=C.accent;X.lineWidth=1.2;X.beginPath();X.arc(Sx(s.fx),Sy(s.fx),3,0,6.283);X.stroke()}
    const bw=s.bw/n;for(let j=0;j<=Math.min(k,n-1);j++){const h=cl(Math.log10(Math.abs(s.it[j]-s.fx)*1000+1)/3)*(s.S-2);box(s.bx+j*bw+bw*.2,Sy(0)-h,bw*.6,h,0,j===k&&k<n?C.signal:C.graphite,.75)}
    lineP([[s.bx,Sy(0)+.5],[g.W-g.p,Sy(0)+.5]],C.rule)}}
};

/* ---------- engine ---------- */
const TH=[];let lp=0;
class Thumb{constructor(el){this.el=el;this.cv=$('canvas',el);this.X=this.cv.getContext('2d');this.sc=SC[el.dataset.m];this.t=RM?this.sc.dur:0;this.run=false;this.vis=false;this.played=false;this.last=0;
    let h=7;for(const ch of el.dataset.m+(el.closest('.pubs')?'L':'S'))h=Math.imul(h^ch.charCodeAt(0),16777619);this.seed=h;el._th=this}
  size(){const r=this.cv.getBoundingClientRect();if(!r.width||!r.height)return false;this.W=r.width;this.H=r.height;this.d=Math.min(2,devicePixelRatio||1);
    this.cv.width=Math.round(this.W*this.d);this.cv.height=Math.round(this.H*this.d);const W=this.W;this.fs=W>=260?11:W>=200?9.5:W>=165?8.5:W>=130?7.5:0;this.p=Math.max(5,Math.round(W*.045));
    this.rng=mk(this.seed);this.du=[...Array(Math.round(W*this.H/900))].map(()=>[this.rng()*W,this.rng()*this.H,.5+this.rng()*.6]);this.s={};this.sc.build(this);return true}
  draw(){if(!this.W&&!this.size())return;X=this.X;X.setTransform(this.d,0,0,this.d,0,0);X.clearRect(0,0,this.W,this.H);X.textBaseline='middle';X.setLineDash([]);this.sc.draw(this,Math.min(this.t,this.sc.dur));X.globalAlpha=1}
  play(){this.played=true;this.t=0;if(RM){this.t=this.sc.dur;this.draw();return}this.run=true;this.last=0;kickT()}}
function loopT(now){lp=0;let any=0;for(const b of TH){if(!b.run||!b.vis)continue;b.t+=b.last?Math.min(64,now-b.last):16;b.last=now;if(b.t>=b.sc.dur){b.t=b.sc.dur;b.run=false}b.draw();any=1}if(any)lp=raf(loopT)}
function kickT(){if(!lp)lp=raf(loopT)}
function capOn(b,ms){b.el.classList.add('cap');clearTimeout(b.ct);if(ms)b.ct=setTimeout(()=>b.el.classList.remove('cap'),ms)}
colors();
$$('.tb[data-m]').forEach(el=>{if(!SC[el.dataset.m])return;const b=new Thumb(el);TH.push(b);
  el.addEventListener('pointerenter',e=>{if(e.pointerType!=='mouse')return;capOn(b);if(!b.run)b.play()});
  el.addEventListener('pointerleave',e=>{if(e.pointerType==='mouse')el.classList.remove('cap')});
  el.addEventListener('click',()=>{b.play();capOn(b,4000)});
  el.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();b.play();capOn(b,4000)}})});
const tio=new IntersectionObserver(es=>es.forEach(e=>{const b=e.target._th;b.vis=e.isIntersecting;if(!b.vis)return;b.last=0;
  if(!b.played&&e.intersectionRatio>=.45)b.play();else if(b.run)kickT()}),{threshold:[0,.45]});
const tro=new ResizeObserver(es=>es.forEach(e=>{const b=e.target._th;if(b.size())b.draw()}));
TH.forEach(b=>{tio.observe(b.el);tro.observe(b.el)});
const redrawAll=()=>{colors();TH.forEach(b=>b.W&&b.draw())};
if(D.fonts&&D.fonts.ready)D.fonts.ready.then(()=>{TWc.clear();TH.forEach(b=>{if(b.size())b.draw()})});

/* ---- hero sentence, generated on every load: CaDDi, Soft-Rank, or STRIDE style ----
   The sentence is data: it is read from #thesis, whatever it says. The real text stays in the DOM
   (screen readers, copy, crawlers) and is only made transparent while an aria-hidden clone animates
   on top of it. Clone words are inline-blocks laid out exactly like the real text; every frame they
   are moved by transform relative to their own natural slot, so the page never reflows. */
const TS=$('#thesis'),TCB=$('#tcap'),TV=$('.tv',TCB),TVB=$('.tverb',TCB),TM=$('.tmeth',TCB);/* readout: t counts down; the method name shows from the first frame */
(function wrap(node){for(const ch of[...node.childNodes]){if(ch.nodeType===1){wrap(ch);continue}if(ch.nodeType!==3||!ch.textContent.trim())continue;
  const fr=D.createDocumentFragment();ch.textContent.split(/(\s+)/).forEach(p=>{if(!p)return;if(/^\s+$/.test(p))fr.appendChild(D.createTextNode(p));else{const s=D.createElement('span');s.className='w';s.textContent=p;fr.appendChild(s)}});ch.replaceWith(fr)}})(TS);
/* plausible wrong first guesses; any word not listed borrows a similar-length word from the sentence */
const SUB={discrete:'continuous',continuous:'discrete',generative:'predictive',tokens:'pixels',permutations:'rankings',sequences:'graphs',graphs:'sequences',
  models:'agents',agents:'models',study:'build',build:'train',structures:'objects',systems:'pipelines',automating:'accelerating',scientific:'biomedical',
  curation:'annotation',data:'text',scale:'speed','multi-agent':'single-agent','llm-based':'rule-based',language:'vision'};
/* STRIDE's playful drafts: only interests the user already put on the site (denoise.html Off-duty § football, from personal.md).
   Trains / railways and the cities list are excluded at the user's request. */
const PERS=['Go Blue!','Michigan Wolverines'];
const STY=['caddi','softrank','stride'],GN={caddi:'CaDDi',softrank:'Soft-Rank',stride:'STRIDE'};
let gStyle=/[?&]gen=(caddi|softrank|stride)/.exec(location.search)?.[1]||STY[rnd(3)],gRaf=0;
const nextStyle=()=>STY[(STY.indexOf(gStyle)+1)%STY.length],io3=u=>u<.5?4*u*u*u:1-Math.pow(-2*u+2,3)/2,cl1=v=>v<0?0:v>1?1:v;
const okW=w=>/^[A-Za-z][A-Za-z-]{3,}[,.;:]?$/.test(w);
function wrongFor(words,i,pool){const m=/^([A-Za-z-]+)([,.;:]?)$/.exec(words[i]);if(!m)return null;const core=m[1],lc=core.toLowerCase();
  let sub=SUB[lc];if(!sub){const nb=pool.filter(j=>j!==i).map(j=>words[j].replace(/[,.;:]$/,'')).find(x=>Math.abs(x.length-core.length)<=3&&x.toLowerCase()!==lc);sub=nb&&nb.toLowerCase()}
  if(!sub)return null;if(core[0]!==core[0].toLowerCase())sub=sub[0].toUpperCase()+sub.slice(1);return sub+m[2]}
function gen(style){gStyle=style;cancelAnimationFrame(gRaf);const old=$('.gov',TS);if(old)old.remove();TS.classList.remove('gen');
  const fin=()=>{TV.textContent='0.00';TVB.textContent='sampled';TM.textContent=GN[style]};TM.textContent=GN[style];if(RM){fin();return}TV.textContent='1.00';TVB.textContent='sampling';
  const ov=D.createElement('div');ov.className='gov';ov.setAttribute('aria-hidden','true');ov.append(...[...TS.childNodes].map(c=>c.cloneNode(true)));TS.appendChild(ov);TS.classList.add('gen');
  const OW=$$('.w',ov),n=OW.length,words=OW.map(o=>o.textContent),t0=performance.now(),cls=OW.map(()=>''),set=(i,c)=>{if(cls[i]!==c){cls[i]=c;OW[i].className='w ow'+c}};
  const done=()=>{ov.remove();TS.classList.remove('gen');fin()};
  if(style==='caddi'){const NS=Math.min(16,Math.max(12,n)),SM=1800/NS,dec=[],rev=[],wrong=[];shuffle([...Array(n).keys()]).forEach((w,r)=>{dec[w]=1+Math.floor(r*NS/n)});
    const cand=shuffle([...Array(n).keys()].filter(i=>okW(words[i])));let picked=0;
    for(const i of cand){if(picked>=(n>=10?2:1))break;const w=wrongFor(words,i,cand);if(!w)continue;wrong[i]=w;dec[i]=2+rnd(3);rev[i]=Math.min(NS,dec[i]+3+rnd(3));picked++}
    const at=k=>(k-1)*SM;
    const step=now=>{const el=now-t0,cs=Math.min(NS,Math.max(0,Math.floor(el/SM)+1));
      for(let i=0;i<n;i++){const o=OW[i];if(cs<dec[i]){set(i,' m');continue}
        if(wrong[i]&&cs<rev[i]){if(o.textContent!==wrong[i]){o.style.width=o.offsetWidth+'px';o.textContent=wrong[i]}set(i,' wr');continue}
        if(o.textContent!==words[i]){o.textContent=words[i];o.style.width=''}const tk=at(wrong[i]?rev[i]:dec[i]);set(i,wrong[i]&&el-tk<90?' m':el-tk<380?' hot':'')}
      TV.textContent=(1-cs/NS).toFixed(2);if(el<NS*SM+380)gRaf=raf(step);else done()};
    step(t0);return}

  /* ---- track engine (Soft-Rank, STRIDE): the sentence is one 1-D track wrapped into lines.
     A tile's position is a single number s. Line L covers s ∈ [L·T, L·T + width); the stretch between
     lines is a short tunnel, so a tile crossing a line break slides out past the right edge and comes
     back in from the left of the next line — it never cuts diagonally through the paragraph. ---- */
  const GAP=90,st={},last={t:t0};
  const geo=()=>{const P=OW.map(o=>[o.offsetLeft,o.offsetTop,o.offsetWidth]),y0=Math.min(...P.map(p=>p[1])),lh=OW[0].offsetHeight,W=ov.clientWidth,T=W+GAP,Lmax=new Set(P.map(p=>Math.round((p[1]-y0)/lh))).size;return{P,y0,lh,W,T,Lmax}};
  const layout=(g,ids,wOf)=>{const sp=g.lh*.19,out={};let x=0,L=0;for(const id of ids){const w=wOf(id);if(x>0&&x+w>g.W+.5&&L<g.Lmax-1){x=0;L++}out[id]=L*g.T+x;x+=w+sp}return out};
  const natS=(g,i)=>Math.round((g.P[i][1]-g.y0)/g.lh)*g.T+g.P[i][0];
  /* the last line never wraps (it may run past the right edge) so the paragraph never grows a line */
  const where=(g,s,w)=>{let L=Math.min(g.Lmax-1,Math.floor(s/g.T)),x=s-L*g.T;if(L<g.Lmax-1&&x>g.W-w+GAP/2){L++;x-=g.T}const out=L<g.Lmax-1?Math.max(0,x-(g.W-w),-x):Math.max(0,-x);return[x,g.y0+L*g.lh,1-cl1(out/(GAP*.5))]};
  const put=(g,i,s,dy=0,a=1)=>{const[x,y,al]=where(g,s,g.P[i][2]);OW[i].style.transform=`translate(${(x-g.P[i][0]).toFixed(1)}px,${(y+dy-g.P[i][1]).toFixed(1)}px)`;OW[i].style.opacity=String(al*a)};
  const follow=(id,target,dt,tau=150)=>{const k=1-Math.exp(-dt/tau);if(st[id]==null)st[id]=target;else st[id]+=(target-st[id])*k;return st[id]};

  if(style==='softrank'){
    /* Soft-Rank: scramble by a few rank moves, then undo them one at a time: the moving tile travels along
       the text track to its rank while the words in between shift over to make room. */
    /* strong scramble: a random permutation with at most two words left in their own slot; then sort it left to
       right, one move per out-of-place word (move word r to rank r), with 2–3 moves overlapping in a stagger */
    let scr;do{scr=shuffle([...Array(n).keys()])}while(n>3&&scr.filter((v,i)=>v===i).length>2);
    const un=[],o2=scr.slice();for(let r=0;r<n;r++){if(o2[r]===r)continue;const i=o2.indexOf(r);o2.splice(i,1);o2.splice(r,0,r);un.push({id:r,back:r})}
    const K=Math.max(1,un.length),T0=450,GP=280,DUR=700,Tm=T0+(K-1)*GP+DUR,mvS={};
    const step=now=>{const el=now-t0,dt=Math.min(64,now-last.t);last.t=now;const g=geo(),ord=scr.slice();let doneN=0;const act={};
      un.forEach((m,j)=>{const ts=T0+j*GP;if(el<ts)return;const i=ord.indexOf(m.id);ord.splice(i,1);ord.splice(m.back,0,m.id);if(el<ts+DUR)act[m.id]=[ts,j];else doneN++});
      const tgt=el>=Tm?Object.fromEntries(ord.map(i=>[i,natS(g,i)])):layout(g,ord,i=>g.P[i][2]);
      for(const i of ord){let s;const a=act[i];
        if(a){const u=cl1((el-a[0])/DUR);if(!mvS[i]||mvS[i].j!==a[1])mvS[i]={j:a[1],from:st[i]??tgt[i]};s=st[i]=mvS[i].from+(tgt[i]-mvS[i].from)*io3(u);set(i,' tile mv2');put(g,i,s,-Math.min(1,Math.sin(Math.PI*u)*2.2)*.5*g.lh);continue}
        else{s=follow(i,tgt[i],dt,el>=Tm?90:170);const fin=un.findIndex(m=>m.id===i);set(i,fin>=0&&el>=T0+fin*GP+DUR&&el<T0+fin*GP+DUR+420?' tile hot':' tile')}
        put(g,i,s)}
      TV.textContent=(1-doneN/K).toFixed(2);if(el>Tm+150)ov.classList.add('cfade');if(el<Tm+700)gRaf=raf(step);else done()};
    step(t0);return}

  /* STRIDE: start from a short draft (a few of the sentence's words, one of them wrong) and apply an edit script
     one atomic edit at a time, as the model writes it out. Insertions make room along the line (overflow wraps to
     the next line) and the new word drops in; one substitution fixes the wrong word. Partway through, the draft
     briefly "drafts" one or two personal interests, which are struck through and deleted again. */
  const pool=[...Array(n).keys()].filter(j=>okW(words[j])),keepN=Math.max(2,Math.round(n*.22)),keep=shuffle([...Array(n).keys()]).slice(0,Math.min(n,keepN)).sort((a,b)=>a-b),inK=new Set(keep);
  const subI=shuffle(keep.filter(i=>okW(words[i]))).find(i=>wrongFor(words,i,pool)),wrongW=subI!=null?wrongFor(words,subI,pool):null;
  /* schedule: normal edits (insertions + the one substitution) on a calm step; each personal phrase is inserted early,
     sits settled through at least four other edits (≥ 1.5 s), and is deleted in its own quiet beat — the strike starts
     only after the previous edit has settled, and the next edit waits until the collapse is done */
  const E=shuffle([...Array(n).keys()].filter(i=>!inK.has(i)).map(i=>({op:'ins',i})));if(wrongW)E.splice(Math.min(E.length,(E.length>>1)+rnd(3)),0,{op:'sub',i:subI});
  const m=E.length,nX=m>=6?1:0,XS=shuffle(PERS.slice()).slice(0,nX).map((txt,k)=>{const el=D.createElement('span');el.className='ow xw tile';el.textContent=txt;ov.appendChild(el);return{el,txt,after:keep[rnd(keep.length)],k}});
  const T0=400,STEP=Math.min(260,Math.max(nX>1?130:150,(2600-(nX>1?600:0))/Math.max(1,m))),tOf={},hold=Math.max(3,Math.floor(1050/STEP));
  const seq=[];let c=0;const take=q=>{for(let j=0;j<q&&c<m;j++)seq.push(E[c++])};take(1+rnd(2));XS.forEach(x=>{seq.push({op:'pins',k:x.k});take(hold);seq.push({op:'pdel',k:x.k});take(2)});take(m);
let tt=T0-STEP,prevDel=false;
  for(const e of seq){if(e.op==='pdel'){tt=Math.max(tt+900,tOf['pins'+e.k]+1950);prevDel=true}else{tt=prevDel?tt+400:tt+STEP;prevDel=false}tOf[e.op+(e.i??e.k??'')]=tt}
  const NE=seq.length,Tend=tt+450,tags=[],seen={};
  const tag=(txt,x,y)=>{const s=D.createElement('span');s.className='etag'+(txt[0]==='−'?' del':'');s.textContent=txt;ov.appendChild(s);tags.push([s,performance.now(),x,y])};
  const step=now=>{const el=now-t0,dt=Math.min(64,now-last.t);last.t=now;
    if(subI!=null){const want=el<tOf['sub'+subI]?wrongW:words[subI];if(OW[subI].textContent!==want)OW[subI].textContent=want}
    const g=geo(),present=[...Array(n).keys()].filter(i=>inK.has(i)||el>=tOf['ins'+i]),ids=present.slice();
    XS.forEach(x=>{if(el>=tOf['pins'+x.k]&&el<tOf['pdel'+x.k])ids.splice(ids.indexOf(x.after)+1,0,'x'+x.k)});
    const tgt=el>=Tend?Object.fromEntries(present.map(i=>[i,natS(g,i)])):layout(g,ids,id=>typeof id==='string'?XS[+id.slice(1)].el.offsetWidth:g.P[id][2]);let applied=0;
    for(let i=0;i<n;i++){if(!present.includes(i)){OW[i].style.opacity='0';continue}const ti=inK.has(i)?-1:tOf['ins'+i],ts=i===subI?tOf['sub'+i]:-1;
      if(ti>=0){applied++;if(st[i]==null)st[i]=tgt[i]}const s=follow(i,tgt[i],dt,el>=Tend?90:110),d=ti>=0?cl1((el-ti-260)/260):1;
      if(ti>=0&&!seen[i]){seen[i]=1;const[x,y]=where(g,s,g.P[i][2]);tag('+ins',x+g.P[i][2]/2,y)}
      if(ts>=0&&el>=ts&&!seen.s){seen.s=1;const[x,y]=where(g,s,g.P[i][2]);tag('~sub',x+g.P[i][2]/2,y)}
      put(g,i,s,-(1-io3(d))*.45*g.lh,d);set(i,(ti>=0&&el-ti<560)||(ts>=0&&el>=ts&&el-ts<560)?' tile hot':i===subI&&el<ts?' tile wr':' tile')}
    if(subI!=null&&el>=tOf['sub'+subI])applied++;
    XS.forEach(x=>{const id='x'+x.k,ti=tOf['pins'+x.k],td=tOf['pdel'+x.k],w=x.el.offsetWidth;
      if(el<ti){x.el.style.opacity='0';return}applied++;
      if(el<td){if(st[id]==null)st[id]=tgt[id];const s=follow(id,tgt[id],dt,110),[X0,Y0,a]=where(g,s,w),d=cl1((el-ti-260)/260);
        if(!seen[id]){seen[id]=1;tag('+ins',X0+w/2,Y0)}x.el.style.opacity=String(a*d);x.el.style.transform=`translate(${X0.toFixed(1)}px,${(Y0-(1-io3(d))*.45*g.lh).toFixed(1)}px)`;
        x.el.className='ow xw tile'+(el>=td-300?' strike':el-ti<560?' hot':'')}
      else{applied++;const[X0,Y0]=where(g,st[id],w);if(!seen[id+'d']){seen[id+'d']=1;tag('−del',X0+w/2,Y0)}const f=cl1((el-td)/300);
        x.el.className='ow xw tile strike';x.el.style.opacity=String(1-f);x.el.style.transform=`translate(${X0.toFixed(1)}px,${(Y0-f*.3*g.lh).toFixed(1)}px) scaleX(${(1-.4*f).toFixed(3)})`}});
    for(const[s,t1,x,y]of tags){const a=(now-t1)/750;s.style.opacity=String(Math.max(0,.9*(1-a)));s.style.transform=`translate(${x.toFixed(1)}px,${(y-.3*g.lh-a*4).toFixed(1)}px) translateX(-50%)`}
    TV.textContent=(1-applied/NE).toFixed(2);if(el>Tend+500)ov.classList.add('cfade');if(el<Tend+1050)gRaf=raf(step);else done()};
  step(t0)}
TCB.addEventListener('click',()=>gen(nextStyle()));
gen(gStyle);

/* ---- theme (thumbnails re-read their colours) ---- */
const tb=$('#theme'),THM=['auto','light','dark'];let th=H.dataset.theme||'auto';
const setTh=()=>{if(th==='auto')H.removeAttribute('data-theme');else H.dataset.theme=th;tb.textContent='theme · '+th;LS('dn-theme',th==='auto'?'':th);redrawAll()};
tb.addEventListener('click',()=>{th=THM[(THM.indexOf(th)+1)%3];setTh()});setTh();
matchMedia('(prefers-color-scheme: dark)').addEventListener('change',redrawAll);

/* ---- A9 · r = resample: name, sentence (other style), and every visible thumbnail ---- */
D.addEventListener('keydown',e=>{if(e.metaKey||e.ctrlKey||e.altKey||(e.target.closest&&e.target.closest('input,textarea,select,[contenteditable]')))return;
  if((e.key||'').toLowerCase()==='r'){denoise();gen(nextStyle());TH.forEach(b=>{if(b.vis)b.play()})}});

let seen=null;try{seen=sessionStorage.getItem('dn-sampled');sessionStorage.setItem('dn-sampled','1')}catch(e){}if(!seen)denoise();
})();
