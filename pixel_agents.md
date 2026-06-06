\<\!DOCTYPE html\>  
\<html lang="tr"\>  
\<head\>  
\<meta charset="UTF-8"\>  
\<meta name="viewport" content="width=device-width,initial-scale=1"\>  
\<title\>🎮 Pixel Agents HQ\</title\>  
\<link rel="preconnect" href="https://fonts.googleapis.com"\>  
\<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P\&display=swap" rel="stylesheet"\>  
\<style\>  
\*{box-sizing:border-box;margin:0;padding:0}  
:root{  
  \--bg:\#0a0810;--surface:\#13101e;--border:\#241d36;--line:\#1a1528;  
  \--accent:\#00e87a;--blue:\#5b9bff;--purple:\#b06bff;--orange:\#ff9944;  
  \--pink:\#ff5b8a;--gold:\#ffc24d;--red:\#ff4060;--teal:\#00d4aa;  
  \--text:\#cbc4e0;--dim:\#6a6088;--pf:'Press Start 2P','Courier New',monospace;  
}  
html,body{width:100%;height:100%;background:var(--bg);overflow:hidden}  
\#app{  
  width:100%;height:100vh;display:flex;flex-direction:column;  
  background:var(--bg);color:var(--text);font-family:var(--pf);font-size:8px;  
}

/\* ── HEADER ── \*/  
\#hd{  
  height:40px;display:flex;align-items:center;gap:10px;padding:0 12px;  
  background:var(--surface);border-bottom:2px solid var(--accent);  
  flex-shrink:0;position:relative;overflow:hidden;  
}  
\#hd::after{  
  content:'';position:absolute;inset:0;  
  background:repeating-linear-gradient(0deg,transparent,transparent 3px,rgba(0,232,122,.03) 3px,rgba(0,232,122,.03) 4px);  
  pointer-events:none;  
}  
.logo{font-size:11px;color:var(--accent);text-shadow:0 0 8px rgba(0,232,122,.6);letter-spacing:1px;white-space:nowrap}  
.hinfo{display:flex;align-items:center;gap:8px;flex:1;font-size:7px;color:var(--dim)}  
.pulse{width:6px;height:6px;border-radius:50%;background:var(--accent);box-shadow:0 0 6px var(--accent);animation:bl 1.5s infinite;flex-shrink:0}  
@keyframes bl{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.3;transform:scale(.7)}}  
.hbadges{display:flex;gap:3px;flex-wrap:wrap}  
.hb{  
  padding:2px 6px;border:1px solid var(--border);border-radius:2px;  
  font-size:6px;color:var(--dim);cursor:pointer;transition:all .2s;white-space:nowrap;  
}  
.hb.on{border-color:var(--accent);color:var(--accent);box-shadow:0 0 4px rgba(0,232,122,.25)}  
.hb.active{border-color:var(--blue);color:var(--blue);box-shadow:0 0 4px rgba(91,155,255,.3);animation:hbpulse 2s infinite}  
@keyframes hbpulse{0%,100%{box-shadow:0 0 4px rgba(91,155,255,.3)}50%{box-shadow:0 0 8px rgba(91,155,255,.6)}}  
.hclock{font-size:9px;color:var(--gold);font-family:var(--pf)}

/\* ── MAIN LAYOUT ── \*/  
\#main{flex:1;display:flex;overflow:hidden;min-height:0}

/\* ── CANVAS SIDE ── \*/  
\#canvaswrap{  
  width:420px;flex-shrink:0;border-right:1px solid var(--border);  
  position:relative;background:\#0c0918;overflow:hidden;  
}  
\#cv{display:block;image-rendering:pixelated}  
\#speedctrl{  
  position:absolute;bottom:6px;left:6px;display:flex;gap:4px;  
}  
.spbtn{  
  background:rgba(10,8,16,.7);border:1px solid var(--border);  
  color:var(--dim);font-family:var(--pf);font-size:6px;  
  padding:3px 5px;border-radius:2px;cursor:pointer;transition:all .15s;  
}  
.spbtn:hover,.spbtn.on{border-color:var(--accent);color:var(--accent)}

/\* ── RIGHT PANEL ── \*/  
\#panel{flex:1;display:flex;flex-direction:column;overflow:hidden;min-width:0}  
.tabs{display:flex;border-bottom:1px solid var(--border);flex-shrink:0;background:var(--surface)}  
.tab{  
  flex:1;padding:9px 4px;background:none;border:none;  
  border-bottom:2px solid transparent;color:var(--dim);  
  font-family:var(--pf);font-size:7px;cursor:pointer;transition:all .15s;  
}  
.tab:hover{color:var(--text)}.tab.on{color:var(--accent);border-bottom-color:var(--accent)}  
.pane{display:none;flex:1;overflow-y:auto;padding:8px;flex-direction:column;gap:5px}  
.pane.on{display:flex}  
.pane::-webkit-scrollbar{width:3px}.pane::-webkit-scrollbar-thumb{background:var(--border)}

/\* ── AGENT CARDS ── \*/  
.ac{  
  background:var(--surface);border:1px solid var(--border);  
  border-radius:3px;padding:8px;transition:border-color .3s,box-shadow .3s;  
  position:relative;overflow:hidden;  
}  
.ac::before{  
  content:'';position:absolute;top:0;left:0;width:2px;height:100%;  
  background:var(--dim);transition:background .3s;  
}  
.ac.run::before{background:var(--blue)}.ac.done::before{background:var(--accent)}.ac.err::before{background:var(--red)}  
.ac.run{border-color:rgba(91,155,255,.4);box-shadow:0 0 10px rgba(91,155,255,.1)}  
.ac.done{border-color:rgba(0,232,122,.4);box-shadow:0 0 10px rgba(0,232,122,.1)}  
.ac.err{border-color:rgba(255,64,96,.4)}  
.actop{display:flex;align-items:center;gap:6px;margin-bottom:6px}  
.acem{font-size:14px;line-height:1;flex-shrink:0}  
.acinf{flex:1;min-width:0}  
.acnm{font-size:8px;font-weight:bold;color:var(--text)}  
.acst{font-size:6px;color:var(--dim);margin-top:2px;text-transform:uppercase;letter-spacing:.5px}  
.acst.run{color:var(--blue)}.acst.done{color:var(--accent)}.acst.err{color:var(--red)}  
.acpct{font-size:9px;color:var(--dim);font-weight:bold;min-width:28px;text-align:right}  
.pbar{width:100%;height:4px;background:var(--line);border-radius:2px;overflow:hidden;margin-bottom:5px}  
.pfill{height:100%;width:0%;background:var(--blue);border-radius:2px;transition:width .5s ease}  
.pfill.done{background:var(--accent)}.pfill.err{background:var(--red)}  
.actk{font-size:6px;color:var(--dim);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}  
/\* small integration pills on each card \*/  
.agtags{display:flex;gap:2px;margin-top:4px;flex-wrap:wrap}  
.agtag{font-size:5px;padding:1px 4px;border:1px solid var(--border);border-radius:1px;color:var(--dim)}  
.agtag.live{border-color:var(--accent);color:var(--accent)}

/\* ── INTEGRATION CARDS ── \*/  
.ic{background:var(--surface);border:1px solid var(--border);border-radius:3px;padding:8px}  
.ichd{display:flex;align-items:center;gap:6px;margin-bottom:6px}  
.icic{font-size:12px}.icnm{font-size:8px;font-weight:bold;flex:1}  
.icst{font-size:6px}.icst.ok{color:var(--accent)}.icst.ld{color:var(--gold)}.icst.er{color:var(--red)}  
.iitems{display:flex;flex-direction:column;gap:2px;max-height:100px;overflow-y:auto}  
.iitems::-webkit-scrollbar{width:3px}.iitems::-webkit-scrollbar-thumb{background:var(--border)}  
.iitem{  
  font-size:6px;color:var(--dim);padding:4px 5px;background:var(--bg);  
  border-radius:1px;cursor:pointer;transition:all .15s;  
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;  
  border-left:2px solid var(--border);  
}  
.iitem:hover{color:var(--accent);border-left-color:var(--accent)}  
.iemp{font-size:6px;color:var(--dim);text-align:center;padding:10px}  
.futg{display:grid;grid-template-columns:1fr 1fr;gap:3px}  
.fut{  
  background:var(--bg);border:1px solid var(--border);border-radius:2px;  
  padding:6px;display:flex;align-items:center;gap:4px;  
  font-size:6px;color:var(--dim);cursor:pointer;transition:all .15s;  
}  
.fut:hover{border-color:var(--blue);color:var(--blue)}.futic{font-size:10px}

/\* ── LOG ── \*/  
\#loglist{display:flex;flex-direction:column;gap:2px}  
.le{  
  display:flex;gap:5px;font-size:6px;padding:3px 5px;  
  border-left:2px solid var(--border);line-height:1.6;  
}  
.le.info{border-left-color:var(--blue)}.le.ok{border-left-color:var(--accent)}  
.le.warn{border-left-color:var(--gold)}.le.error{border-left-color:var(--red)}  
.le.sys{border-left-color:var(--purple)}  
.lt{color:var(--dim);white-space:nowrap;flex-shrink:0}  
.lag{white-space:nowrap;flex-shrink:0;font-weight:bold}  
.lm{color:var(--text);word-break:break-word}

/\* ── BOTTOM BAR ── \*/  
\#ab{  
  height:46px;display:flex;align-items:center;gap:5px;padding:0 10px;  
  background:var(--surface);border-top:1px solid var(--border);flex-shrink:0;  
}  
\#topic{  
  flex:1;background:var(--bg);border:1px solid var(--border);  
  color:var(--text);font-family:var(--pf);font-size:7px;  
  padding:7px 9px;border-radius:2px;outline:none;min-width:0;  
  transition:border-color .2s;  
}  
\#topic:focus{border-color:var(--blue);box-shadow:0 0 0 1px rgba(91,155,255,.2)}  
.abtn{  
  background:none;border:1px solid var(--border);color:var(--dim);  
  font-family:var(--pf);font-size:7px;padding:7px 9px;border-radius:2px;  
  cursor:pointer;white-space:nowrap;transition:all .15s;flex-shrink:0;  
}  
.abtn:hover:not(:disabled){border-color:var(--text);color:var(--text)}  
.abtn.pri{border-color:var(--accent);color:var(--accent)}  
.abtn.pri:hover:not(:disabled){background:var(--accent);color:var(--bg)}  
.abtn:disabled{opacity:.3;cursor:not-allowed}  
\#runst{font-size:6px;color:var(--dim);white-space:nowrap;min-width:56px;text-align:right}

/\* ── REPORT MODAL ── \*/  
\#modal{  
  display:none;position:fixed;inset:0;background:rgba(0,0,0,.8);  
  z-index:100;align-items:center;justify-content:center;  
}  
\#modal.on{display:flex}  
\#modalbox{  
  background:var(--surface);border:1px solid var(--accent);border-radius:4px;  
  padding:16px;max-width:560px;width:90%;max-height:80vh;overflow-y:auto;  
  font-size:7px;color:var(--text);line-height:1.8;  
}  
\#modalbox h2{font-size:9px;color:var(--accent);margin-bottom:10px}  
\#modalbox pre{font-family:var(--pf);white-space:pre-wrap;word-break:break-word}  
\#modalclose{  
  float:right;background:none;border:1px solid var(--red);color:var(--red);  
  font-family:var(--pf);font-size:7px;padding:4px 8px;cursor:pointer;border-radius:2px;  
}

/\* ── SCANNING OVERLAY ── \*/  
\#scan{  
  position:fixed;inset:0;pointer-events:none;z-index:50;  
  background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,.04) 2px,rgba(0,0,0,.04) 4px);  
}  
\</style\>  
\</head\>  
\<body\>  
\<div id="scan"\>\</div\>  
\<div id="app"\>

\<\!-- HEADER \--\>  
\<header id="hd"\>  
  \<div class="logo"\>🎮 PIXEL AGENTS HQ\</div\>  
  \<div class="hinfo"\>  
    \<span class="pulse"\>\</span\>  
    \<span id="hstatus"\>ONLINE\</span\>  
    \<span id="hruns"\>RUNS: 0\</span\>  
    \<span class="hclock" id="hclock"\>00:00:00\</span\>  
  \</div\>  
  \<div class="hbadges"\>  
    \<span class="hb on" id="b-gcal"\>📅 GCAL\</span\>  
    \<span class="hb on" id="b-drive"\>📁 DRIVE\</span\>  
    \<span class="hb" id="b-slack"\>💬 SLACK\</span\>  
    \<span class="hb" id="b-notion"\>📝 NOTION\</span\>  
    \<span class="hb" id="b-github"\>🐙 GH\</span\>  
    \<span class="hb" id="b-linear"\>🔷 LINEAR\</span\>  
    \<span class="hb" id="b-tg"\>✈️ TG\</span\>  
  \</div\>  
\</header\>

\<main id="main"\>  
  \<\!-- ISOMETRIC CANVAS \--\>  
  \<div id="canvaswrap"\>  
    \<canvas id="cv"\>\</canvas\>  
    \<div id="speedctrl"\>  
      \<button class="spbtn on" id="sp1" onclick="setSpeed(1)"\>1x\</button\>  
      \<button class="spbtn" id="sp2" onclick="setSpeed(2)"\>2x\</button\>  
      \<button class="spbtn" id="sp3" onclick="setSpeed(4)"\>4x\</button\>  
    \</div\>  
  \</div\>

  \<\!-- RIGHT PANEL \--\>  
  \<div id="panel"\>  
    \<nav class="tabs"\>  
      \<button class="tab on" data-pane="agents"\>AGENTS\</button\>  
      \<button class="tab" data-pane="connect"\>CONNECT\</button\>  
      \<button class="tab" data-pane="log"\>LOG\</button\>  
    \</nav\>

    \<div class="pane on" id="pane-agents"\>\</div\>

    \<div class="pane" id="pane-connect"\>  
      \<\!-- Google Calendar \--\>  
      \<div class="ic"\>  
        \<div class="ichd"\>\<span class="icic"\>📅\</span\>\<span class="icnm"\>Google Calendar\</span\>\<span class="icst ok" id="gcal-st"\>READY\</span\>\</div\>  
        \<div class="iitems" id="gcal-items"\>\<div class="iemp"\>📅 butonuna bas → etkinlikleri yükle\</div\>\</div\>  
      \</div\>  
      \<\!-- Google Drive \--\>  
      \<div class="ic"\>  
        \<div class="ichd"\>\<span class="icic"\>📁\</span\>\<span class="icnm"\>Google Drive\</span\>\<span class="icst ok" id="drive-st"\>READY\</span\>\</div\>  
        \<div class="iitems" id="drive-items"\>\<div class="iemp"\>📁 butonuna bas → dosyaları tara\</div\>\</div\>  
      \</div\>  
      \<\!-- Coming soon \--\>  
      \<div class="ic"\>  
        \<div class="ichd"\>\<span class="icic"\>🔌\</span\>\<span class="icnm"\>Entegrasyonlar\</span\>\</div\>  
        \<div class="futg"\>  
          \<div class="fut" onclick="showComingSoon('Slack')"\>\<span class="futic"\>💬\</span\>Slack\</div\>  
          \<div class="fut" onclick="showComingSoon('Notion')"\>\<span class="futic"\>📝\</span\>Notion\</div\>  
          \<div class="fut" onclick="showComingSoon('Linear')"\>\<span class="futic"\>🔷\</span\>Linear\</div\>  
          \<div class="fut" onclick="showComingSoon('GitHub')"\>\<span class="futic"\>🐙\</span\>GitHub\</div\>  
          \<div class="fut" onclick="showComingSoon('GitLab')"\>\<span class="futic"\>🦊\</span\>GitLab\</div\>  
          \<div class="fut" onclick="showComingSoon('Monday')"\>\<span class="futic"\>📋\</span\>Monday\</div\>  
          \<div class="fut" onclick="showComingSoon('Jira')"\>\<span class="futic"\>🎯\</span\>Jira\</div\>  
          \<div class="fut" onclick="showComingSoon('Telegram')"\>\<span class="futic"\>✈️\</span\>Telegram\</div\>  
          \<div class="fut" onclick="showComingSoon('n8n')"\>\<span class="futic"\>🔄\</span\>n8n\</div\>  
          \<div class="fut" onclick="showComingSoon('Webhook')"\>\<span class="futic"\>🔔\</span\>Webhook\</div\>  
        \</div\>  
      \</div\>  
    \</div\>

    \<div class="pane" id="pane-log"\>\<div id="loglist"\>\</div\>\</div\>  
  \</div\>  
\</main\>

\<\!-- BOTTOM BAR \--\>  
\<div id="ab"\>  
  \<input id="topic" type="text" placeholder="Araştırma konusu gir..." value="BIST100 günlük piyasa analizi"\>  
  \<button class="abtn pri" id="run-btn"\>▶ RUN\</button\>  
  \<button class="abtn" id="cal-btn" title="Google Calendar Yükle"\>📅\</button\>  
  \<button class="abtn" id="drv-btn" title="Google Drive Tara"\>📁\</button\>  
  \<button class="abtn" id="rpt-btn" title="Son Raporu Göster"\>📄\</button\>  
  \<span id="runst"\>READY\</span\>  
\</div\>

\</div\>

\<\!-- REPORT MODAL \--\>  
\<div id="modal"\>  
  \<div id="modalbox"\>  
    \<button id="modalclose" onclick="document.getElementById('modal').classList.remove('on')"\>✕ KAPAT\</button\>  
    \<h2\>📄 SON RAPOR\</h2\>  
    \<pre id="modalcontent"\>\</pre\>  
  \</div\>  
\</div\>

\<script\>  
'use strict';  
// ═══════════════════════════════════════════════════  
// STATE  
// ═══════════════════════════════════════════════════  
const ALIST \= \[  
  {id:'scout',    name:'Scout',     em:'🕵️', col:'\#5b9bff', drk:'\#1e3f88', skin:'\#f0c898', hair:'\#e8c85a', hstyle:'medium', glass:false, shirt:'\#3a68c8'},  
  {id:'researcher',name:'Researcher',em:'🔬',col:'\#b06bff', drk:'\#6030a8', skin:'\#e8b080', hair:'\#1e1428', hstyle:'long',   glass:true,  shirt:'\#803ab8'},  
  {id:'analyst',  name:'Analyst',   em:'📊', col:'\#ff9944', drk:'\#a84010', skin:'\#c88850', hair:'\#583010', hstyle:'short',  glass:true,  shirt:'\#c86820'},  
  {id:'writer',   name:'Writer',    em:'✍️', col:'\#ff5b8a', drk:'\#a81848', skin:'\#f0c0a0', hair:'\#2a1810', hstyle:'long',   glass:false, shirt:'\#c83860'},  
  {id:'publisher',name:'Publisher', em:'📤', col:'\#00d4aa', drk:'\#008870', skin:'\#e8b088', hair:'\#c04828', hstyle:'short',  glass:false, shirt:'\#008878'},  
\];

// Isometric desk positions — matching the image layout  
// Back-left, back-right, center, front-left, front-right  
const DESK\_POS \= \[  
  {gx:1.5, gy:1.2},  // Scout — back left (purple person in image)  
  {gx:3.2, gy:0.8},  // Researcher — back center (orange person)  
  {gx:4.5, gy:2.0},  // Analyst — right (green person)  
  {gx:1.0, gy:3.5},  // Writer — front left (blue person)  
  {gx:3.2, gy:3.2},  // Publisher — front right (red person)  
\];

const S \= {  
  agents:{}, running:false, runs:0, t:0, speed:1,  
  lastReport:'', lastTopic:'',  
};  
ALIST.forEach((a,i)=\>{  
  a.gx \= DESK\_POS\[i\].gx;  
  a.gy \= DESK\_POS\[i\].gy;  
  S.agents\[a.id\] \= {status:'idle', task:'Bekliyor...', pct:0, ph:Math.random()\*Math.PI\*2};  
});

// ═══════════════════════════════════════════════════  
// CANVAS SETUP  
// ═══════════════════════════════════════════════════  
const cv \= document.getElementById('cv');  
const cx \= cv.getContext('2d');  
const WRAP \= document.getElementById('canvaswrap');  
const GN \= 6;     // grid cells  
const TW \= 38;    // tile half-width (isometric)  
const TH \= 19;    // tile half-height  
const WH \= 96;    // wall height px  
const DH \= 22;    // desk height px

let OX \= 210, OY \= 90;

function resize(){  
  cv.width  \= WRAP.clientWidth  || 420;  
  cv.height \= WRAP.clientHeight || 480;  
  OX \= cv.width / 2;  
  OY \= Math.round(cv.height \* 0.26);  
}  
resize();  
new ResizeObserver(resize).observe(WRAP);

function iso(gx, gy, gz){  
  gz \= gz || 0;  
  return {  
    x: OX \+ (gx \- gy) \* TW,  
    y: OY \+ (gx \+ gy) \* TH \- gz  
  };  
}

// Rounded rect helper  
function rr(x, y, w, h, r){  
  r \= Math.min(r, w/2, h/2);  
  cx.beginPath();  
  cx.moveTo(x+r, y);  
  cx.arcTo(x+w, y, x+w, y+h, r);  
  cx.arcTo(x+w, y+h, x, y+h, r);  
  cx.arcTo(x, y+h, x, y, r);  
  cx.arcTo(x, y, x+w, y, r);  
  cx.closePath();  
}

// ═══════════════════════════════════════════════════  
// ROOM DRAWING — matching the warm wood office in images  
// ═══════════════════════════════════════════════════  
function drawRoom(){  
  // Sky/background  
  cx.fillStyle \= '\#0c0918';  
  cx.fillRect(0, 0, cv.width, cv.height);

  // ── WALLS ──────────────────────────────────────────

  // LEFT WALL (along gx=0, gy 0→GN)  
  const lw\_a \= iso(0,0), lw\_b \= iso(0,GN);  
  // Base wall  
  const lw\_grad \= cx.createLinearGradient(lw\_a.x, lw\_a.y-WH, lw\_b.x, lw\_b.y-WH);  
  lw\_grad.addColorStop(0, '\#3d3358');  
  lw\_grad.addColorStop(1, '\#2e2845');  
  cx.fillStyle \= lw\_grad;  
  cx.beginPath();  
  cx.moveTo(lw\_a.x, lw\_a.y);  
  cx.lineTo(lw\_b.x, lw\_b.y);  
  cx.lineTo(lw\_b.x, lw\_b.y \- WH);  
  cx.lineTo(lw\_a.x, lw\_a.y \- WH);  
  cx.closePath(); cx.fill();

  // Window light on left wall (warm golden glow like in image)  
  for(let wy of \[1.0, 2.9\]){  
    const w0 \= iso(0, wy+0.1);  
    const w1 \= iso(0, wy+0.85);  
    const wtop \= WH \- 20, wbot \= 24;  
    // Window pane glow  
    const wg \= cx.createLinearGradient(w0.x, w0.y-wbot-wtop, w1.x, w1.y-wbot);  
    wg.addColorStop(0, 'rgba(255,220,140,.18)');  
    wg.addColorStop(.5,'rgba(255,200,80,.32)');  
    wg.addColorStop(1, 'rgba(255,180,60,.08)');  
    cx.fillStyle \= wg;  
    cx.beginPath();  
    cx.moveTo(w0.x, w0.y-wbot);  
    cx.lineTo(w1.x, w1.y-wbot);  
    cx.lineTo(w1.x, w1.y-wbot-wtop);  
    cx.lineTo(w0.x, w0.y-wbot-wtop);  
    cx.closePath(); cx.fill();  
    // Frame  
    cx.strokeStyle \= '\#7a6840'; cx.lineWidth \= 2;  
    cx.beginPath();  
    cx.moveTo(w0.x, w0.y-wbot);  
    cx.lineTo(w1.x, w1.y-wbot);  
    cx.lineTo(w1.x, w1.y-wbot-wtop);  
    cx.lineTo(w0.x, w0.y-wbot-wtop);  
    cx.closePath(); cx.stroke();  
    // Cross divider  
    const wm \= iso(0, wy+0.475);  
    cx.beginPath(); cx.moveTo(wm.x, wm.y-wbot); cx.lineTo(wm.x, wm.y-wbot-wtop); cx.stroke();  
    cx.lineWidth \= 1;  
    // Floor glow from window  
    const fg \= cx.createRadialGradient(w0.x+TW\*2, w0.y+TH\*2, 0, w0.x+TW\*2, w0.y+TH\*2, TW\*3.5);  
    fg.addColorStop(0, 'rgba(255,200,100,.12)');  
    fg.addColorStop(1, 'transparent');  
    cx.fillStyle \= fg; cx.fillRect(0, 0, cv.width, cv.height);  
  }

  // RIGHT WALL (along gy=0, gx 0→GN)  
  const rw\_a \= iso(0,0), rw\_b \= iso(GN,0);  
  const rw\_grad \= cx.createLinearGradient(rw\_a.x, 0, rw\_b.x, 0);  
  rw\_grad.addColorStop(0, '\#272238');  
  rw\_grad.addColorStop(1, '\#1e1b30');  
  cx.fillStyle \= rw\_grad;  
  cx.beginPath();  
  cx.moveTo(rw\_a.x, rw\_a.y);  
  cx.lineTo(rw\_b.x, rw\_b.y);  
  cx.lineTo(rw\_b.x, rw\_b.y \- WH);  
  cx.lineTo(rw\_a.x, rw\_a.y \- WH);  
  cx.closePath(); cx.fill();

  // Analytics board on right wall (matches image)  
  const bd0 \= iso(1.5, 0), bd1 \= iso(4.0, 0);  
  const bdtop \= WH \- 18, bdbot \= 28;  
  cx.fillStyle \= '\#0d1c35';  
  cx.strokeStyle \= '\#2a4870'; cx.lineWidth \= 2;  
  cx.beginPath();  
  cx.moveTo(bd0.x+2, bd0.y-bdbot);  
  cx.lineTo(bd1.x-2, bd1.y-bdbot);  
  cx.lineTo(bd1.x-2, bd1.y-bdbot-bdbot\*2.2);  
  cx.lineTo(bd0.x+2, bd0.y-bdbot-bdbot\*2.2);  
  cx.closePath(); cx.fill(); cx.stroke();  
  // Charts on board  
  drawBoard(bd0, bd1, bdbot);

  // Corner edge  
  cx.strokeStyle \= '\#160f28'; cx.lineWidth \= 2;  
  cx.beginPath(); cx.moveTo(rw\_a.x, rw\_a.y); cx.lineTo(rw\_a.x, rw\_a.y-WH); cx.stroke();

  // ── FLOOR ───────────────────────────────────────────  
  // Wood floor — warm tones like image  
  for(let gx=0; gx\<GN; gx++){  
    for(let gy=0; gy\<GN; gy++){  
      const a=iso(gx,gy), b=iso(gx+1,gy), c=iso(gx+1,gy+1), d=iso(gx,gy+1);  
      // Alternating warm wood shades  
      const shade \= (gx+gy)%2===0;  
      cx.fillStyle \= shade ? '\#7a5c38' : '\#6b5030';  
      cx.beginPath(); cx.moveTo(a.x,a.y); cx.lineTo(b.x,b.y); cx.lineTo(c.x,c.y); cx.lineTo(d.x,d.y); cx.closePath(); cx.fill();  
      // Subtle grout lines  
      cx.strokeStyle \= '\#4e3820'; cx.lineWidth \= .5;  
      cx.beginPath(); cx.moveTo(a.x,a.y); cx.lineTo(b.x,b.y); cx.lineTo(c.x,c.y); cx.lineTo(d.x,d.y); cx.closePath(); cx.stroke();  
    }  
  }

  // Center carpet/rug (light tile area like in image)  
  for(let gx=1.5; gx\<3.5; gx++) for(let gy=1.5; gy\<3.5; gy++){  
    const a=iso(gx,gy), b=iso(gx+1,gy), c=iso(gx+1,gy+1), d=iso(gx,gy+1);  
    cx.fillStyle \= 'rgba(220,190,140,.08)';  
    cx.beginPath(); cx.moveTo(a.x,a.y); cx.lineTo(b.x,b.y); cx.lineTo(c.x,c.y); cx.lineTo(d.x,d.y); cx.closePath(); cx.fill();  
  }

  // ── BOOKSHELVES ─────────────────────────────────────  
  drawShelf(0.05, 0.2, 'L');  
  drawShelf(0.05, 2.5, 'L');  
  drawShelf(0.05, 4.5, 'L');  
  drawShelf(0.5,  0.05,'R');  
  drawShelf(2.5,  0.05,'R');  
  drawShelf(4.5,  0.05,'R');

  // ── PLANTS ──────────────────────────────────────────  
  drawPlant(iso(GN-0.3, 0.3));  
  drawPlant(iso(GN-0.3, 2.3));  
  drawPlant(iso(0.4, GN-0.3));  
  drawPlant(iso(2.4, GN-0.4));  
}

function drawBoard(p0, p1, bdbot){  
  // Multi-chart analytics board like in image  
  const bx0 \= p0.x+6, bx1 \= p1.x-6;  
  const by0 \= p0.y-bdbot-2;  
  const bw \= bx1-bx0, bh \= bdbot\*2.0;

  // Bar chart (left half)  
  const colors \= \['\#5b9bff','\#ff9944','\#00e87a','\#b06bff'\];  
  for(let i=0;i\<4;i++){  
    cx.fillStyle \= colors\[i\];  
    const bh2 \= 8 \+ (i%3)\*8;  
    cx.fillRect(bx0+6+i\*9, by0-bh+bh2+4, 7, bh-bh2-4);  
  }  
  // Axis  
  cx.strokeStyle \= '\#3a5070'; cx.lineWidth \= 1;  
  cx.beginPath(); cx.moveTo(bx0+4, by0-bh+2); cx.lineTo(bx0+4, by0-2); cx.lineTo(bx0+42, by0-2); cx.stroke();

  // Line chart (right half)  
  const pts \= \[\[0,14\],\[1,8\],\[2,12\],\[3,5\],\[4,10\],\[5,4\]\];  
  cx.strokeStyle \= '\#00e87a'; cx.lineWidth \= 1.5;  
  cx.beginPath();  
  pts.forEach((p,i)=\>{  
    const px2 \= bx0+48+p\[0\]\*8;  
    const py2 \= by0-4-p\[1\];  
    i===0 ? cx.moveTo(px2,py2) : cx.lineTo(px2,py2);  
  });  
  cx.stroke();  
  // Line chart dots  
  cx.fillStyle \= '\#00e87a';  
  pts.forEach(p=\>{cx.beginPath();cx.arc(bx0+48+p\[0\]\*8, by0-4-p\[1\], 1.5,0,Math.PI\*2);cx.fill()});

  // Pie chart (far right)  
  const pc \= bx0+bw-16, py2 \= by0-bh/2-4;  
  const slices \= \[\[0, 2.3,'\#b06bff'\],\[2.3,4.2,'\#00e87a'\],\[4.2,6.28,'\#ff9944'\]\];  
  slices.forEach((\[s,e,c\])=\>{  
    cx.fillStyle=c; cx.beginPath();  
    cx.moveTo(pc,py2); cx.arc(pc,py2,12,s,e); cx.closePath(); cx.fill();  
  });  
}

function drawShelf(gx, gy, side){  
  const p \= iso(gx, gy);  
  const w=24, h=62;  
  // Shelf body  
  cx.fillStyle \= '\#2a1a0c';  
  cx.fillRect(p.x-w/2, p.y-h, w, h);  
  cx.fillStyle \= '\#3a2614';  
  cx.fillRect(p.x-w/2+2, p.y-h+2, w-4, h-4);  
  // Books — colorful like in image  
  const bkColors \= \['\#5b9bff','\#ff5b8a','\#ff9944','\#b06bff','\#00e87a','\#ffc24d','\#ff4060','\#00d4aa'\];  
  for(let row=0; row\<4; row++){  
    for(let b=0; b\<4; b++){  
      cx.fillStyle \= bkColors\[(row\*3+b)%8\];  
      cx.globalAlpha \= .85;  
      cx.fillRect(p.x-w/2+3+b\*4.8, p.y-h+4+row\*15, 4, 12);  
    }  
    cx.globalAlpha \= 1;  
    cx.fillStyle \= '\#1a1006';  
    cx.fillRect(p.x-w/2+2, p.y-h+16+row\*15, w-4, 1.5);  
  }  
  // Shelf edge glow  
  cx.strokeStyle \= '\#4a3020'; cx.lineWidth \= 1;  
  cx.strokeRect(p.x-w/2, p.y-h, w, h);  
}

function drawPlant(p){  
  // Pot  
  cx.fillStyle \= '\#4a2808';  
  rr(p.x-7, p.y-10, 14, 12, 2); cx.fill();  
  cx.fillStyle \= '\#5a3010';  
  rr(p.x-7, p.y-10, 14, 4, 1); cx.fill();  
  // Soil  
  cx.fillStyle \= '\#2a1808';  
  cx.fillRect(p.x-5, p.y-11, 10, 3);  
  // Leaves — multiple overlapping like in image  
  const leafColors \= \['\#0a7a3a','\#0d9a48','\#10b855','\#0c8840'\];  
  leafColors.forEach((c,i)=\>{  
    const ox \= (i%2===0?1:-1)\*3, oy \= i\*2;  
    cx.fillStyle \= c;  
    cx.globalAlpha \= .9;  
    cx.beginPath();  
    cx.ellipse(p.x+ox, p.y-18-oy, 7+i%2\*2, 14+i\*2, (i\*.3)-.2, 0, Math.PI\*2);  
    cx.fill();  
  });  
  cx.globalAlpha \= 1;  
}

// ═══════════════════════════════════════════════════  
// DESK STATION — detailed like image (CRT monitor, lamp, keyboard)  
// ═══════════════════════════════════════════════════  
function drawStation(a){  
  const ag \= S.agents\[a.id\];  
  const s \= ag.status;  
  const ts \= S.t / 1000;  
  const ph \= ag.ph;  
  const active \= \['fetching','processing','analyzing','writing','thinking'\].includes(s);

  // Desk (isometric box)  
  drawDesk(a.gx, a.gy, s, a.col, active, ts);

  const top \= iso(a.gx, a.gy, DH);

  // Lamp (to the right of monitor like in image)  
  drawLamp(top.x \+ 26, top.y \- 4, active, s, ts, ph, a.col);

  // CRT Monitor (center-back of desk — facing viewer)  
  drawCRT(top.x \- 12, top.y \- 8, s, a.col, active, ts, ph);

  // Coffee mug  
  drawMug(top.x \+ 36, top.y \+ 2, a.col);

  // Keyboard  
  cx.fillStyle \= '\#d8d0b0';  
  rr(top.x-14, top.y+2, 26, 8, 2); cx.fill();  
  cx.fillStyle \= '\#c0b898'; cx.fillRect(top.x-12, top.y+3, 22, 6);  
  // Key rows  
  cx.fillStyle \= '\#a09878'; cx.lineWidth \= .5;  
  for(let ki=0; ki\<3; ki++){  
    for(let kj=0; kj\<7; kj++){  
      rr(top.x-11+kj\*3, top.y+4+ki\*1.8, 2, 1.3, .3); cx.fill();  
    }  
  }

  // Small plant on desk (some agents have it)  
  if(a.id \=== 'researcher' || a.id \=== 'writer'){  
    const pp \= {x: top.x-28, y: top.y+2};  
    cx.fillStyle \= '\#3a2008'; cx.fillRect(pp.x-3,pp.y-4,6,6);  
    cx.fillStyle \= '\#0a8a38'; cx.globalAlpha=.9;  
    cx.beginPath(); cx.ellipse(pp.x, pp.y-9, 4, 7, 0, 0, Math.PI\*2); cx.fill();  
    cx.globalAlpha=1;  
  }

  // Papers / documents  
  cx.fillStyle \= '\#f0e8d0';  
  cx.save(); cx.translate(top.x+18, top.y-1); cx.rotate(.05);  
  cx.fillRect(-8,-5,16,10); cx.restore();  
  cx.fillStyle \= '\#e8d8b8';  
  cx.save(); cx.translate(top.x+18, top.y-1); cx.rotate(-.04);  
  cx.fillRect(-8,-5,16,10); cx.restore();  
  // Text lines on paper  
  cx.fillStyle \= '\#6a5830'; cx.globalAlpha=.5;  
  for(let li=0;li\<3;li++) cx.fillRect(top.x+12, top.y-3+li\*3, 10, 1);  
  cx.globalAlpha=1;

  // Character  
  drawCharacter(top.x, top.y, a, s, ts, ph, active);

  // Speech bubble  
  const bubble \= getBubbleText(s, a.id);  
  if(bubble.text){  
    drawBubble(top.x, top.y \- 62, bubble.text, bubble.color);  
  }  
}

function drawDesk(gx, gy, s, col, active, ts){  
  const x1=gx-.75, x2=gx+.75, y1=gy-.55, y2=gy+.55;  
  const h \= DH;

  // Desk shadow  
  const sh \= iso(gx, gy, 0);  
  cx.fillStyle \= 'rgba(0,0,0,.25)';  
  cx.beginPath(); cx.ellipse(sh.x, sh.y+4, TW\*.8, TH\*.6, 0, 0, Math.PI\*2); cx.fill();

  // Desk surfaces — warm wood  
  const A=iso(x1,y1,h), B=iso(x2,y1,h), C=iso(x2,y2,h), D=iso(x1,y2,h);  
  const A0=iso(x1,y1,0), B0=iso(x2,y1,0), C0=iso(x2,y2,0), D0=iso(x1,y2,0);

  // Left face (darker)  
  cx.fillStyle \= '\#7a5228';  
  cx.beginPath(); cx.moveTo(D0.x,D0.y); cx.lineTo(C0.x,C0.y); cx.lineTo(C.x,C.y); cx.lineTo(D.x,D.y); cx.closePath(); cx.fill();  
  // Right face  
  cx.fillStyle \= '\#9a6838';  
  cx.beginPath(); cx.moveTo(C0.x,C0.y); cx.lineTo(B0.x,B0.y); cx.lineTo(B.x,B.y); cx.lineTo(C.x,C.y); cx.closePath(); cx.fill();  
  // Top surface  
  const tg \= cx.createLinearGradient(A.x,A.y,C.x,C.y);  
  tg.addColorStop(0, '\#c8924a');  
  tg.addColorStop(.5,'\#b87838');  
  tg.addColorStop(1, '\#a06830');  
  cx.fillStyle \= tg;  
  cx.beginPath(); cx.moveTo(A.x,A.y); cx.lineTo(B.x,B.y); cx.lineTo(C.x,C.y); cx.lineTo(D.x,D.y); cx.closePath(); cx.fill();

  // Active glow on desk top  
  if(active){  
    cx.fillStyle \= col; cx.globalAlpha \= .06 \+ Math.sin(ts\*2)\*.03;  
    cx.beginPath(); cx.moveTo(A.x,A.y); cx.lineTo(B.x,B.y); cx.lineTo(C.x,C.y); cx.lineTo(D.x,D.y); cx.closePath(); cx.fill();  
    cx.globalAlpha \= 1;  
  }

  // Desk drawer details on right face  
  cx.fillStyle \= '\#7a5028'; cx.strokeStyle='\#6a4020'; cx.lineWidth=.5;  
  const dfx \= (C0.x+B0.x)/2, dfy \= (C0.y+B0.y)/2;  
  cx.fillRect(dfx-6, dfy-8, 12, 6);  cx.strokeRect(dfx-6, dfy-8, 12, 6);  
  cx.fillRect(dfx-6, dfy-1, 12, 6);  cx.strokeRect(dfx-6, dfy-1, 12, 6);  
  // Handles  
  cx.fillStyle='\#c8a060'; cx.fillRect(dfx-1,dfy-6,2,2); cx.fillRect(dfx-1,dfy+0,2,2);  
}

function drawLamp(lx, ly, active, s, ts, ph, col){  
  // Base  
  cx.fillStyle \= '\#3a2c18';  
  cx.fillRect(lx-2, ly, 4, 10);  
  cx.fillRect(lx-5, ly+9, 10, 3);  
  // Neck  
  cx.fillStyle \= '\#4a3c28';  
  cx.fillRect(lx-1.5, ly-8, 3, 10);  
  // Shade — warm conical shape  
  cx.fillStyle \= active ? '\#c89040' : '\#a07830';  
  cx.beginPath();  
  cx.moveTo(lx-9, ly-8);  
  cx.lineTo(lx+9, ly-8);  
  cx.lineTo(lx+5, ly-18);  
  cx.lineTo(lx-5, ly-18);  
  cx.closePath(); cx.fill();  
  // Inner lamp glow  
  if(active){  
    const lampGrad \= cx.createRadialGradient(lx, ly-12, 0, lx, ly-12, 14);  
    lampGrad.addColorStop(0, 'rgba(255,220,120,.95)');  
    lampGrad.addColorStop(.4,'rgba(255,200,80,.4)');  
    lampGrad.addColorStop(1, 'transparent');  
    cx.fillStyle \= lampGrad; cx.globalAlpha \= .8 \+ Math.sin(ts\*3+ph)\*.1;  
    cx.beginPath(); cx.arc(lx, ly-10, 14, 0, Math.PI\*2); cx.fill();  
    cx.globalAlpha \= 1;  
    // Cast floor light  
    const floorGlow \= cx.createRadialGradient(lx+TW\*.5, ly+TH\*3, 0, lx+TW\*.5, ly+TH\*3, TW\*2);  
    floorGlow.addColorStop(0, 'rgba(255,200,100,.12)');  
    floorGlow.addColorStop(1,'transparent');  
    cx.fillStyle \= floorGlow; cx.globalAlpha=1;  
    cx.fillRect(0,0,cv.width,cv.height);  
  } else {  
    // Off lamp still has slight warmth  
    cx.fillStyle \= 'rgba(255,200,80,.15)';  
    cx.beginPath(); cx.arc(lx, ly-13, 5, 0, Math.PI\*2); cx.fill();  
  }  
}

function drawCRT(mx, my, s, col, active, ts, ph){  
  // CRT Body — cream/beige like in image  
  cx.fillStyle \= '\#c8bea0';  
  rr(mx-18, my-38, 36, 32, 3); cx.fill();  
  cx.fillStyle \= '\#d8ceb0';  
  rr(mx-18, my-38, 36, 8, 3); cx.fill();  
  // Sides darker  
  cx.fillStyle \= '\#a89880';  
  cx.fillRect(mx+15, my-38, 3, 32);  
  // Monitor border  
  cx.strokeStyle \= '\#888070'; cx.lineWidth=1;  
  cx.strokeRect(mx-18, my-38, 36, 32);  
  // Screen area  
  const scr\_col \= s==='idle' ? '\#0a2818' : s==='complete' ? '\#082a1a' : s==='error' ? '\#2a0808' : '\#082218';  
  rr(mx-14, my-35, 28, 24, 1); cx.fill();  
  cx.fillStyle \= scr\_col; rr(mx-14,my-35,28,24,1); cx.fill();

  // Screen content — green phosphor glow (like CRT in image)  
  if(s \=== 'idle'){  
    cx.fillStyle \= 'rgba(0,180,80,.35)';  
    cx.fillRect(mx-12, my-33, 24, 2);  
    cx.fillRect(mx-12, my-28, 18, 2);  
    cx.fillRect(mx-12, my-23, 20, 2);  
    cx.fillRect(mx-12, my-18, 15, 2);  
    cx.fillRect(mx-12, my-13, 22, 2);  
  } else {  
    // Active — scrolling code lines  
    cx.fillStyle \= 'rgba(0,220,100,.7)';  
    cx.globalAlpha \= .8 \+ Math.sin(ts\*2+ph)\*.1;  
    const lineCount \= active ? 5 : 3;  
    for(let li=0; li\<lineCount; li++){  
      const scrollOff \= active ? (ts \* 20 \* S.speed \+ li\*8) % 28 : 0;  
      const lw \= active ? 8 \+ Math.abs(Math.sin(ts\*3+ph+li))\*(24-8) : 14+li\*2;  
      cx.fillRect(mx-12, my-33+li\*5-scrollOff%5, Math.min(lw,24), 1.5);  
    }  
    cx.globalAlpha=1;  
    // Scanline overlay on screen  
    cx.fillStyle \= 'rgba(0,0,0,.15)';  
    for(let sl=my-35; sl\<my-11; sl+=3) cx.fillRect(mx-14, sl, 28, 1);  
  }

  // Screen glow  
  if(active){  
    const sg \= cx.createRadialGradient(mx, my-23, 2, mx, my-23, 18);  
    sg.addColorStop(0, 'rgba(0,200,100,.2)');  
    sg.addColorStop(1, 'transparent');  
    cx.fillStyle=sg; cx.globalAlpha=.6+Math.sin(ts\*4+ph)\*.2;  
    cx.beginPath(); cx.arc(mx, my-23, 18, 0, Math.PI\*2); cx.fill();  
    cx.globalAlpha=1;  
  }  
  // Status indicator dot on CRT  
  cx.fillStyle \= s==='complete' ? '\#00e87a' : s==='error' ? '\#ff4060' : active ? '\#ffcc00' : '\#3a3828';  
  cx.beginPath(); cx.arc(mx+14, my-2, 2, 0, Math.PI\*2); cx.fill();

  // CRT stand/neck  
  cx.fillStyle \= '\#9a9080';  
  cx.fillRect(mx-3, my-6, 6, 4);  
  cx.fillStyle \= '\#888070';  
  cx.fillRect(mx-7, my-2, 14, 3);  
}

// ═══════════════════════════════════════════════════  
// CHARACTER — detailed pixel person facing 3/4 view toward viewer  
// Matches image: colored shirts, hair, faces looking at screen  
// ═══════════════════════════════════════════════════  
function drawCharacter(px, py, a, s, ts, ph, active){  
  // Bob offset  
  let bob \= 0;  
  if(s==='idle')       bob \= Math.sin(ts\*.6+ph)\*.8;  
  else if(active)      bob \= Math.sin(ts\*4+ph)\*1.2;  
  else if(s==='thinking') bob \= Math.sin(ts\*1.5+ph)\*1.8;  
  else if(s==='complete') bob \= \-Math.abs(Math.sin(ts\*3+ph))\*3;  
  else if(s==='error')    bob \= Math.sin(ts\*8+ph)\*1.5;

  const base\_y \= py \- 4 \+ bob;  
  const head\_y \= base\_y \- 36;

  // Chair (behind character, lower z-order)  
  drawChair(px, base\_y, a.col);

  // BODY — shirt  
  cx.fillStyle \= a.shirt;  
  rr(px-11, base\_y-24, 22, 20, 5); cx.fill();  
  // Shirt collar/neck  
  cx.fillStyle \= a.skin;  
  cx.fillRect(px-3, base\_y-25, 6, 6);  
  // Shirt detail (button line or pocket)  
  cx.fillStyle \= a.drk; cx.globalAlpha=.4;  
  cx.fillRect(px-1, base\_y-22, 2, 10);  
  cx.globalAlpha=1;  
  // Belt/waist  
  cx.fillStyle \= '\#2a1808';  
  cx.fillRect(px-11, base\_y-5, 22, 3);

  // ARMS — animated when typing  
  const lt \= active ? Math.sin(ts\*12+ph)\*2.8 : 0;  
  const rt \= active ? \-Math.sin(ts\*12+ph)\*2.8 : 0;  
  // Upper arms  
  cx.fillStyle \= a.shirt;  
  cx.fillRect(px-16, base\_y-22, 6, 14+lt);  
  cx.fillRect(px+10, base\_y-22, 6, 14+rt);  
  // Forearms / hands on keyboard  
  cx.fillStyle \= a.skin;  
  cx.fillRect(px-15, base\_y-9+lt, 5, 5);  
  cx.fillRect(px+10, base\_y-9+rt, 5, 5);  
  // Fingers suggestion  
  cx.fillStyle \= a.skin; cx.globalAlpha=.7;  
  cx.fillRect(px-16, base\_y-5+lt, 7, 2);  
  cx.fillRect(px+9, base\_y-5+rt, 7, 2);  
  cx.globalAlpha=1;

  // HEAD  
  cx.fillStyle \= a.skin;  
  rr(px-10, head\_y-10, 20, 21, 5); cx.fill();  
  // Ears  
  cx.fillStyle \= a.skin;  
  cx.fillRect(px-12, head\_y-2, 3, 5);  
  cx.fillRect(px+9, head\_y-2, 3, 5);  
  // Ear detail  
  cx.fillStyle \= a.drk; cx.globalAlpha=.2;  
  cx.fillRect(px-11, head\_y-1, 2, 3);  
  cx.fillRect(px+10, head\_y-1, 2, 3);  
  cx.globalAlpha=1;

  // HAIR  
  cx.fillStyle \= a.hair;  
  if(a.hstyle==='long'){  
    rr(px-11, head\_y-12, 22, 13, 5); cx.fill();  
    cx.fillRect(px-11, head\_y-6, 3, 16);  
    cx.fillRect(px+8, head\_y-6, 3, 16);  
    cx.fillRect(px-11, head\_y+6, 22, 4);  
  } else if(a.hstyle==='medium'){  
    rr(px-11, head\_y-12, 22, 11, 5); cx.fill();  
    cx.fillRect(px-11, head\_y-6, 3, 8);  
    cx.fillRect(px+8, head\_y-6, 3, 8);  
  } else {  
    rr(px-11, head\_y-12, 22, 9, 5); cx.fill();  
    cx.fillRect(px-11, head\_y-8, 2, 4);  
    cx.fillRect(px+9, head\_y-8, 2, 4);  
  }

  // NECK SHADOW  
  cx.fillStyle \= a.drk; cx.globalAlpha=.2;  
  cx.fillRect(px-2, base\_y-26, 4, 3);  
  cx.globalAlpha=1;

  // FACE  
  const ey \= head\_y \+ 1;  
  // Eyes  
  cx.fillStyle \= '\#1a1418';  
  if(s==='complete'){  
    // Happy eyes (curved)  
    cx.beginPath(); cx.arc(px-4,ey+1,2,Math.PI,0); cx.stroke();  
    cx.beginPath(); cx.arc(px+4,ey+1,2,Math.PI,0); cx.stroke();  
    cx.fillRect(px-6,ey-1,4,2); cx.fillRect(px+2,ey-1,4,2);  
  } else if(s==='error'){  
    // Worried eyes  
    cx.fillRect(px-6,ey-2,4,4); cx.fillRect(px+2,ey-2,4,4);  
    // Worry lines  
    cx.fillStyle='\#a05040'; cx.globalAlpha=.5;  
    cx.fillRect(px-5,ey-4,2,2); cx.fillRect(px+3,ey-4,2,2);  
    cx.globalAlpha=1;  
  } else if(s==='thinking'||s==='analyzing'){  
    // Looking up/sideways  
    cx.fillRect(px-5,ey-2,3,3); cx.fillRect(px+2,ey-2,3,3);  
  } else {  
    // Normal eyes looking at screen  
    cx.fillRect(px-5,ey,3,3); cx.fillRect(px+2,ey,3,3);  
    // Pupils looking toward screen  
    cx.fillStyle='\#3a3060'; cx.globalAlpha=.5;  
    cx.fillRect(px-4,ey+1,2,2); cx.fillRect(px+3,ey+1,2,2);  
    cx.globalAlpha=1;  
  }

  // Glasses  
  if(a.glass){  
    cx.strokeStyle='\#2a2838'; cx.lineWidth=1.5;  
    cx.strokeRect(px-7,ey-1,6,5);  
    cx.strokeRect(px+1,ey-1,6,5);  
    cx.beginPath(); cx.moveTo(px-1,ey+1); cx.lineTo(px+1,ey+1); cx.stroke();  
    // Temple arms  
    cx.beginPath(); cx.moveTo(px-7,ey+1); cx.lineTo(px-11,ey+2); cx.stroke();  
    cx.beginPath(); cx.moveTo(px+7,ey+1); cx.lineTo(px+11,ey+2); cx.stroke();  
  }

  // Nose  
  cx.fillStyle \= a.drk; cx.globalAlpha=.25;  
  cx.fillRect(px-1, ey+4, 2, 2);  
  cx.globalAlpha=1;

  // Mouth  
  cx.fillStyle \= '\#b06060';  
  if(s==='complete'){  
    cx.beginPath(); cx.arc(px,head\_y+9,3,0,Math.PI); cx.fill(); // smile  
  } else if(s==='error'){  
    cx.beginPath(); cx.arc(px,head\_y+11,3,Math.PI,0); cx.fill(); // frown  
  } else {  
    cx.fillRect(px-2, head\_y+9, 4, 1.5);  
  }

  // Completion sparkles  
  if(s==='complete'){  
    const t2 \= Math.floor(ts\*5)%4;  
    const sparkles \= \[\[14,-10\],\[−14,-8\],\[10,-16\],\[−10,-14\]\];  
    sparkles.forEach((sp,i)=\>{  
      if(i===t2){  
        cx.fillStyle \= a.col; cx.globalAlpha=.9;  
        cx.fillRect(px+sp\[0\], head\_y+sp\[1\], 3, 3);  
        cx.fillRect(px+sp\[0\]+1, head\_y+sp\[1\]-2, 2, 2);  
        cx.globalAlpha=1;  
      }  
    });  
  }

  // Thinking dots above head  
  if(s==='thinking'){  
    const dotT \= Math.floor(ts\*3)%3+1;  
    for(let di=0;di\<dotT;di++){  
      cx.fillStyle=a.col; cx.globalAlpha=.7+di\*.1;  
      cx.beginPath(); cx.arc(px-4+di\*4, head\_y-16-di\*2, 2, 0, Math.PI\*2); cx.fill();  
    }  
    cx.globalAlpha=1;  
  }  
}

function drawChair(px, py, col){  
  // Chair back  
  cx.fillStyle \= '\#252038';  
  rr(px-13, py-30, 26, 26, 4); cx.fill();  
  // Chair back top highlight  
  cx.fillStyle \= '\#302a48';  
  rr(px-13, py-30, 26, 6, 4); cx.fill();  
  // Chair seat (not visible, just shadow)  
  cx.fillStyle \= '\#1e1a30';  
  rr(px-12, py-5, 24, 8, 3); cx.fill();  
  // Armrests  
  cx.fillStyle \= '\#2a2540';  
  cx.fillRect(px-14, py-15, 3, 8);  
  cx.fillRect(px+11, py-15, 3, 8);  
  // Chair base/wheels (minimal)  
  cx.fillStyle \= '\#1a1828'; cx.globalAlpha=.6;  
  cx.fillRect(px-4, py+2, 8, 4);  
  cx.globalAlpha=1;  
}

function drawMug(mx, my, col){  
  // Mug body  
  cx.fillStyle \= '\#e8e0c8';  
  rr(mx-4, my-6, 9, 10, 2); cx.fill();  
  // Mug handle  
  cx.strokeStyle='\#c8c0a8'; cx.lineWidth=1.5;  
  cx.beginPath(); cx.arc(mx+6, my-2, 3, \-Math.PI\*.6, Math.PI\*.6); cx.stroke();  
  // Coffee inside  
  cx.fillStyle \= '\#3a1808'; cx.globalAlpha=.7;  
  cx.fillRect(mx-3, my-6, 7, 3);  
  cx.globalAlpha=1;  
  // Mug color stripe  
  cx.fillStyle \= col; cx.globalAlpha=.4;  
  cx.fillRect(mx-4, my-3, 9, 2);  
  cx.globalAlpha=1;  
}

function getBubbleText(s, id){  
  const statusMap \= {  
    'fetching':   {text:'Fetching web content', color:'\#1a3a60'},  
    'processing': {text:'Processing data',       color:'\#1a3a60'},  
    'analyzing':  {text:'Analyzing results',     color:'\#1a3a60'},  
    'writing':    {text:'Writing report',        color:'\#1a2840'},  
    'thinking':   {text:'Thinking...',           color:'\#2a1a40'},  
    'complete':   {text:'Done\! ✓',              color:'\#0a2a18'},  
    'error':      {text:'Error\!',               color:'\#3a0808'},  
  };  
  return statusMap\[s\] || {text:null};  
}

function drawBubble(x, y, text, bgColor){  
  cx.font \= '7px "Press Start 2P",monospace';  
  const tw \= cx.measureText(text).width;  
  const bw \= Math.max(tw \+ 16, 60), bh \= 18;  
  const bx \= x \- bw/2, by \= y \- bh;

  // Shadow  
  cx.fillStyle \= 'rgba(0,0,0,.3)';  
  rr(bx+2, by+2, bw, bh, 4); cx.fill();

  // Bubble body  
  cx.fillStyle \= '\#f4f0fc';  
  cx.strokeStyle \= '\#c0b8d8'; cx.lineWidth=1.5;  
  rr(bx, by, bw, bh, 4); cx.fill(); cx.stroke();

  // Tail  
  cx.fillStyle='\#f4f0fc'; cx.strokeStyle='\#c0b8d8'; cx.lineWidth=1;  
  cx.beginPath(); cx.moveTo(x-5,y); cx.lineTo(x+5,y); cx.lineTo(x,y+6); cx.closePath();  
  cx.fill(); cx.stroke();

  // Text  
  cx.fillStyle \= bgColor || '\#2a2050';  
  cx.fillText(text, bx+8, by+bh-6);  
}

// ═══════════════════════════════════════════════════  
// ANIMATION LOOP  
// ═══════════════════════════════════════════════════  
let lastT \= 0;  
function loop(t){  
  const dt \= t \- lastT; lastT \= t;  
  S.t \+= dt \* S.speed;  
  cx.clearRect(0, 0, cv.width, cv.height);  
  drawRoom();  
  // Sort desks by iso depth (painter's algorithm)  
  \[...ALIST\]  
    .sort((a,b) \=\> (a.gx+a.gy) \- (b.gx+b.gy))  
    .forEach(a \=\> drawStation(a));  
  requestAnimationFrame(loop);  
}  
requestAnimationFrame(loop);

// ═══════════════════════════════════════════════════  
// UI — CARDS, TABS, CLOCK  
// ═══════════════════════════════════════════════════  
function buildCards(){  
  const p \= document.getElementById('pane-agents');  
  p.innerHTML \= '';  
  ALIST.forEach(a=\>{  
    const d \= document.createElement('div');  
    d.className='ac'; d.id='ac-'+a.id;  
    d.innerHTML=\`  
      \<div class="actop"\>  
        \<span class="acem"\>${a.em}\</span\>  
        \<div class="acinf"\>  
          \<div class="acnm"\>${a.name.toUpperCase()}\</div\>  
          \<div class="acst" id="ast-${a.id}"\>IDLE\</div\>  
        \</div\>  
        \<span class="acpct" id="apct-${a.id}"\>0%\</span\>  
      \</div\>  
      \<div class="pbar"\>\<div class="pfill" id="apf-${a.id}"\>\</div\>\</div\>  
      \<div class="actk" id="atk-${a.id}"\>Bekliyor...\</div\>  
      \<div class="agtags" id="atags-${a.id}"\>\</div\>\`;  
    p.appendChild(d);  
  });  
}  
buildCards();

function setAgent(id, status, task, pct, tags){  
  S.agents\[id\] \= {...S.agents\[id\], status, task, pct};  
  const c \= document.getElementById('ac-'+id); if(\!c) return;  
  const run \= \!\['idle','complete','error'\].includes(status);  
  const done \= status==='complete', err \= status==='error';  
  c.className \= 'ac'+(run?' run':done?' done':err?' err':'');  
  const st \= document.getElementById('ast-'+id);  
  st.className='acst'+(run?' run':done?' done':err?' err':'');  
  st.textContent \= status.toUpperCase();  
  document.getElementById('apf-'+id).style.width \= pct+'%';  
  document.getElementById('apf-'+id).className \= 'pfill'+(done?' done':err?' err':'');  
  document.getElementById('atk-'+id).textContent \= task;  
  document.getElementById('apct-'+id).textContent \= pct+'%';  
  if(tags){  
    const tg \= document.getElementById('atags-'+id);  
    tg.innerHTML \= tags.map(t=\>\`\<span class="agtag ${t.live?'live':''}"\>${t.label}\</span\>\`).join('');  
  }  
}

function addLog(type, agent, msg){  
  const el \= document.getElementById('loglist');  
  const d \= document.createElement('div');  
  d.className='le '+type;  
  const t \= new Date().toLocaleTimeString('tr-TR',{hour12:false});  
  const ag \= ALIST.find(a=\>a.id===agent);  
  d.innerHTML=\`\<span class="lt"\>${t}\</span\>\<span class="lag" style="color:${ag?.col||'\#a080ff'}"\>${(agent||'sys').toUpperCase()}\</span\>\<span class="lm"\>${msg}\</span\>\`;  
  el.prepend(d);  
  while(el.children.length\>120) el.removeChild(el.lastChild);  
}

// Tabs  
document.querySelectorAll('.tab').forEach(b=\>{  
  b.addEventListener('click',()=\>{  
    document.querySelectorAll('.tab').forEach(x=\>x.classList.remove('on'));  
    document.querySelectorAll('.pane').forEach(p=\>p.classList.remove('on'));  
    b.classList.add('on');  
    document.getElementById('pane-'+b.dataset.pane).classList.add('on');  
  });  
});

// Clock  
setInterval(()=\>{  
  document.getElementById('hclock').textContent \=  
    new Date().toLocaleTimeString('tr-TR',{hour12:false});  
},1000);  
document.getElementById('hclock').textContent=new Date().toLocaleTimeString('tr-TR',{hour12:false});

// Speed control  
function setSpeed(s){  
  S.speed \= s;  
  document.querySelectorAll('.spbtn').forEach(b=\>b.classList.remove('on'));  
  document.getElementById('sp'+s)?.classList.add('on');  
  if(s===2) document.getElementById('sp2').classList.add('on');  
  if(s===4) document.getElementById('sp3').classList.add('on');  
}

// ═══════════════════════════════════════════════════  
// PIPELINE  
// ═══════════════════════════════════════════════════  
const sleep \= ms \=\> new Promise(r=\>setTimeout(r,ms));

async function callOpenAI(systemMsg, userMsg){  
  // Uses OpenAI gpt-4o — no API key needed in browser (add yours here)  
  const key \= localStorage.getItem('oai\_key') || '';  
  if(\!key){  
    // Demo mode — return simulated response  
    await sleep(1200 \+ Math.random()\*800);  
    return demoResponse(userMsg);  
  }  
  const res \= await fetch('https://api.openai.com/v1/chat/completions',{  
    method:'POST',  
    headers:{'Content-Type':'application/json','Authorization':'Bearer '+key},  
    body:JSON.stringify({  
      model:'gpt-4o',  
      temperature:.3,  
      max\_tokens:800,  
      messages:\[{role:'system',content:systemMsg},{role:'user',content:userMsg}\]  
    })  
  });  
  const d \= await res.json();  
  if(d.error) throw new Error(d.error.message);  
  return d.choices?.\[0\]?.message?.content || '';  
}

function demoResponse(topic){  
  return \`\#\# ${topic} Analizi\\n\\n\*\*Bulgular:\*\*\\n• Güçlü momentum sinyalleri tespit edildi\\n• Hacim ortalamanın %23 üzerinde\\n• Teknik göstergeler pozitif ayrışma gösteriyor\\n\\n\*\*Risk:\*\* Orta (65/100)\\n\*\*Fırsat Skoru:\*\* 72/100\\n\*\*Güven:\*\* %78\\n\\n\*\*Öneri:\*\* Kademeli pozisyon artırımı değerlendirilebilir. Stop-loss seviyeleri kritik.\`;  
}

async function runPipeline(topic){  
  if(S.running) return;  
  S.running \= true; S.runs++;  
  S.lastTopic \= topic;  
  document.getElementById('hruns').textContent='RUNS: '+S.runs;  
  document.getElementById('run-btn').disabled=true;  
  document.getElementById('runst').textContent='● RUNNING';  
  document.getElementById('hstatus').textContent='RUNNING';

  ALIST.forEach(a=\>setAgent(a.id,'idle','Bekliyor...',0));  
  addLog('sys','sys',\`━━ Run \#${S.runs} başladı: "${topic}" ━━\`);

  let scoutData='', resData='', anaData='', repData='';  
  try{  
    // ── SCOUT ──  
    setAgent('scout','fetching','Kaynaklar taranıyor...',20,\[  
      {label:'WEB',live:true},{label:'GCAL',live:S.agents.scout?.calLive}  
    \]);  
    addLog('info','scout','Web içeriği çekiliyor...');  
    scoutData \= await callOpenAI(  
      'Sen Scout, hızlı bir AI araştırma ajanısın. Kısa, madde madde, Türkçe yanıtla. Önsöz yok.',  
      \`Konu: "${topic}"\\n1) Bu konuda 5 kritik veri kaynağı türü\\n2) 5 anahtar terim\\n3) 3 acil izleme noktası\`  
    );  
    setAgent('scout','complete','Kaynaklar bulundu ✓',100,\[{label:'WEB',live:true},{label:'6 KAYNAK',live:true}\]);  
    addLog('ok','scout','Tarama tamamlandı → '+scoutData.substring(0,60)+'...');  
    await sleep(400/S.speed);

    // ── RESEARCHER ──  
    setAgent('researcher','processing','Veri çıkarılıyor...',35,\[{label:'PROCESS',live:true}\]);  
    addLog('info','researcher','Scout verileri işleniyor...');  
    resData \= await callOpenAI(  
      'Sen Researcher, yapılandırılmış veri çıkaran bir AI ajanısın. Türkçe, madde madde, kısa.',  
      \`Konu: "${topic}"\\nScout bulguları:\\n${scoutData}\\n\\nÇıkar: 1\) Sayısal veriler ve trendler 2\) Kritik faktörler 3\) Karşılaştırmalı analiz noktaları\`  
    );  
    setAgent('researcher','complete','Veri yapılandırıldı ✓',100,\[{label:'STRUCTURED',live:true}\]);  
    addLog('ok','researcher','Araştırma tamamlandı');  
    await sleep(350/S.speed);

    // ── ANALYST ──  
    setAgent('analyst','analyzing','Örüntü analizi...',55,\[{label:'PATTERNS',live:true},{label:'RISK',live:true}\]);  
    addLog('info','analyst','Analiz modelleri çalışıyor...');  
    anaData \= await callOpenAI(  
      'Sen Analyst, uzman bir piyasa/veri analistisisin. Türkçe, yapılandırılmış, sayısal.',  
      \`Konu: "${topic}"\\nAraştırma:\\n${resData}\\n\\nÜret: 1\) 3 temel içgörü 2\) Risk skoru (0-100+neden) 3\) Fırsat matrisi 4\) Güven yüzdesi 5\) Eylem önerileri\`  
    );  
    setAgent('analyst','complete','Analiz tamam ✓',100,\[{label:'RISK SCORED',live:true}\]);  
    addLog('ok','analyst','Risk & fırsat haritası hazır');  
    await sleep(300/S.speed);

    // ── WRITER ──  
    setAgent('writer','writing','Rapor yazılıyor...',72,\[{label:'MARKDOWN',live:true}\]);  
    addLog('info','writer','Yönetici raporu hazırlanıyor...');  
    repData \= await callOpenAI(  
      'Sen Writer, özlü ve etkili yönetici raporları üretirsin. Markdown formatı, Türkçe, profesyonel.',  
      \`Konu: "${topic}"\\nAnaliz: ${anaData}\\n\\n\#\# RAPOR FORMATI:\\n\# Yönetici Özeti (2 satır)\\n\#\# Temel Bulgular (3 madde, bullet)\\n\#\# Risk Değerlendirmesi\\n\#\# Fırsatlar\\n\#\# Öneri ve Sonraki Adımlar\`  
    );  
    S.lastReport \= repData;  
    setAgent('writer','complete','Rapor hazır ✓',100,\[{label:'REPORT',live:true}\]);  
    addLog('ok','writer','Rapor tamamlandı');  
    await sleep(300/S.speed);

    // ── PUBLISHER ──  
    setAgent('publisher','processing','Platformlara dağıtılıyor...',85,\[  
      {label:'NOTION',live:true},{label:'SLACK',live:true},{label:'GH',live:true}  
    \]);  
    addLog('info','publisher','Entegrasyonlara gönderiliyor...');  
    await sleep(800/S.speed);  
    setAgent('publisher','complete','Yayınlandı ✓',100,\[  
      {label:'NOTION ✓',live:true},{label:'SLACK ✓',live:true},{label:'GH ✓',live:true}  
    \]);  
    addLog('ok','publisher','Tüm platformlara dağıtıldı');

    // Success  
    addLog('ok','sys','━━ Run \#'+S.runs+' TAMAMLANDI ━━');  
    document.getElementById('runst').textContent='✓ DONE \#'+S.runs;  
    document.getElementById('hstatus').textContent='ONLINE';

    // Show log tab with report  
    setTimeout(()=\>{  
      repData.split('\\n').filter(l=\>l.trim()).forEach(l=\>addLog('info','writer',l));  
      document.querySelector('\[data-pane="log"\]').click();  
    }, 500);

  }catch(err){  
    const actAgent \= ALIST.find(a=\>\!\['idle','complete','error'\].includes(S.agents\[a.id\]?.status));  
    if(actAgent) setAgent(actAgent.id,'error','Hata: '+String(err).substring(0,40),0);  
    addLog('error','sys','Pipeline hatası: '+err.message);  
    document.getElementById('runst').textContent='✕ ERROR';  
    document.getElementById('hstatus').textContent='ERROR';  
  }finally{  
    S.running=false;  
    document.getElementById('run-btn').disabled=false;  
  }  
}

// ═══════════════════════════════════════════════════  
// GOOGLE CALENDAR (MCP / Demo)  
// ═══════════════════════════════════════════════════  
async function loadCalendar(){  
  const btn \= document.getElementById('cal-btn');  
  const stEl \= document.getElementById('gcal-st');  
  btn.disabled=true; btn.textContent='⏳';  
  stEl.textContent='LOADING'; stEl.className='icst ld';  
  document.getElementById('gcal-items').innerHTML='\<div class="iemp"\>Yükleniyor...\</div\>';  
  document.querySelector('\[data-pane="connect"\]').click();  
  addLog('info','sys','Google Calendar verisi çekiliyor...');

  try{  
    // Demo calendar events (replace with real MCP call)  
    await sleep(1200);  
    const events \= \[  
      '\[Pzt 26 May\] 09:00 — Haftalık Takım Toplantısı',  
      '\[Pzt 26 May\] 14:00 — BIST100 Değerlendirme Oturumu',  
      '\[Sal 27 May\] 10:30 — Q2 Bütçe Gözden Geçirme',  
      '\[Sal 27 May\] 15:00 — Ürün Yol Haritası Sunumu',  
      '\[Çar 28 May\] 11:00 — Yatırımcı Brifing',  
      '\[Per 29 May\] 09:00 — Sprint Planlama',  
      '\[Per 29 May\] 16:00 — Teknik Borç Değerlendirmesi',  
      '\[Cum 30 May\] 10:00 — Haftalık OKR Gözden Geçirme',  
    \];  
    const box \= document.getElementById('gcal-items');  
    box.innerHTML='';  
    events.forEach(ev=\>{  
      const d=document.createElement('div'); d.className='iitem';  
      d.textContent=ev;  
      d.title='Tıkla → bu etkinlik için ajan çalıştır';  
      d.onclick=()=\>{  
        document.getElementById('topic').value='Hazırlık: '+ev;  
        document.querySelector('\[data-pane="agents"\]').click();  
        addLog('info','sys','Takvim etkinliği seçildi: '+ev);  
      };  
      box.appendChild(d);  
    });  
    stEl.textContent='LIVE'; stEl.className='icst ok';  
    document.getElementById('b-gcal').className='hb active';  
    addLog('ok','sys','Calendar: '+events.length+' etkinlik yüklendi');  
  }catch(e){  
    document.getElementById('gcal-items').innerHTML='\<div class="iemp"\>Hata: '+e.message+'\</div\>';  
    stEl.textContent='ERROR'; stEl.className='icst er';  
    addLog('error','sys','Calendar hatası: '+e.message);  
  }finally{  
    btn.disabled=false; btn.textContent='📅';  
  }  
}

// ═══════════════════════════════════════════════════  
// GOOGLE DRIVE (Demo / MCP)  
// ═══════════════════════════════════════════════════  
async function loadDrive(){  
  const btn \= document.getElementById('drv-btn');  
  const stEl \= document.getElementById('drive-st');  
  btn.disabled=true; btn.textContent='⏳';  
  stEl.textContent='SCANNING'; stEl.className='icst ld';  
  document.getElementById('drive-items').innerHTML='\<div class="iemp"\>Drive taranıyor...\</div\>';  
  document.querySelector('\[data-pane="connect"\]').click();  
  addLog('info','sys','Google Drive taranıyor...');

  try{  
    await sleep(1000);  
    const files \= \[  
      'Q2\_2025\_Raporu.xlsx — 24 May 2025',  
      'BIST100\_Teknik\_Analiz.pdf — 23 May 2025',  
      'Piyasa\_Stratejisi\_v3.docx — 22 May 2025',  
      'Yatirimci\_Sunumu\_Q2.pptx — 21 May 2025',  
      'Risk\_Degerlendirme\_2025.pdf — 20 May 2025',  
      'OKR\_Takip\_Mayis.sheets — 19 May 2025',  
      'Musteri\_Analizi\_Final.csv — 18 May 2025',  
      'Proje\_Roadmap\_2025H2.docx — 17 May 2025',  
    \];  
    const box \= document.getElementById('drive-items');  
    box.innerHTML='';  
    files.forEach(f=\>{  
      const d=document.createElement('div'); d.className='iitem';  
      d.textContent=f;  
      d.title='Tıkla → bu dosyayı ajanlarla analiz et';  
      d.onclick=()=\>{  
        document.getElementById('topic').value='Analiz: '+f.split('—')\[0\].trim();  
        document.querySelector('\[data-pane="agents"\]').click();  
        addLog('info','sys','Drive dosyası seçildi: '+f);  
      };  
      box.appendChild(d);  
    });  
    stEl.textContent='LIVE'; stEl.className='icst ok';  
    document.getElementById('b-drive').className='hb active';  
    addLog('ok','sys','Drive: '+files.length+' dosya listelendi');  
  }catch(e){  
    document.getElementById('drive-items').innerHTML='\<div class="iemp"\>Hata: '+e.message+'\</div\>';  
    stEl.textContent='ERROR'; stEl.className='icst er';  
    addLog('error','sys','Drive hatası: '+e.message);  
  }finally{  
    btn.disabled=false; btn.textContent='📁';  
  }  
}

// ═══════════════════════════════════════════════════  
// UTILITY  
// ═══════════════════════════════════════════════════  
function showComingSoon(name){  
  addLog('warn','sys',\`${name} entegrasyonu yakında eklenecek. API key ayarla → hazır\!\`);  
  document.querySelector('\[data-pane="log"\]').click();  
}

// Report modal  
document.getElementById('rpt-btn').onclick=()=\>{  
  if(\!S.lastReport){ addLog('warn','sys','Henüz rapor yok. Önce RUN çalıştır.'); return; }  
  document.getElementById('modalcontent').textContent \= S.lastReport;  
  document.getElementById('modal').classList.add('on');  
};  
document.getElementById('modal').onclick=(e)=\>{  
  if(e.target===document.getElementById('modal')) document.getElementById('modal').classList.remove('on');  
};

// OpenAI key setup  
function checkAPIKey(){  
  const k \= localStorage.getItem('oai\_key');  
  if(\!k){  
    addLog('warn','sys','OpenAI API key yok → demo modu aktif');  
    addLog('info','sys','API key için: localStorage.setItem("oai\_key","sk-...")');  
  } else {  
    addLog('ok','sys','OpenAI API key bulundu → gerçek mod aktif');  
  }  
}

// ═══════════════════════════════════════════════════  
// EVENTS  
// ═══════════════════════════════════════════════════  
document.getElementById('run-btn').onclick=()=\>{  
  runPipeline(document.getElementById('topic').value.trim() || 'BIST100 günlük piyasa analizi');  
};  
document.getElementById('cal-btn').onclick=loadCalendar;  
document.getElementById('drv-btn').onclick=loadDrive;  
document.getElementById('topic').addEventListener('keydown', e=\>{  
  if(e.key==='Enter') document.getElementById('run-btn').click();  
});

// ═══════════════════════════════════════════════════  
// INIT  
// ═══════════════════════════════════════════════════  
addLog('ok','sys','🎮 Pixel Agents HQ v2.0 başlatıldı');  
addLog('ok','sys','5 ajan hazır: Scout • Researcher • Analyst • Writer • Publisher');  
addLog('info','sys','📅 Takvim  📁 Drive  ▶ RUN — alt çubuktaki butonları kullan');  
addLog('info','sys','API key: localStorage.setItem("oai\_key","sk-...")');  
checkAPIKey();  
\</script\>  
\</body\>  
\</html\>  
