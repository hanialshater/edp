// Dependency-free smoke test for the component workshop.
//   node components/test.mjs
// For each component .html: extract <script>, run it against a DOM/canvas
// stub, assert no throw and that window.__component.mount exists. Plus a pure
// invariant: Bradley-Terry recovers the true order from clean match results.

import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';
import { bradleyTerry, kendallTau, ranksFromScores, rng, sigmoid } from './shared/lib.js';

const DIR = path.dirname(fileURLToPath(import.meta.url));
let fail = 0, pass = 0;
const ok = (m)=>{ pass++; console.log('  \x1b[32m✓\x1b[0m ' + m); };
const bad = (m)=>{ fail++; console.log('  \x1b[31m✗\x1b[0m ' + m); };

// ---------- 1. pure invariant: BT recovers order ----------
(function btInvariant(){
  const N=8, beta=1.15, R=rng(99);
  const skill=[]; for(let i=0;i<N;i++) skill.push(1.8-3.6*i/(N-1));
  const trueRank=ranksFromScores(skill);
  const wins=Array.from({length:N},()=>new Array(N).fill(0));
  for(let m=0;m<600;m++){ // round-robin-ish: least played pair
    let bi=0,bj=1,bn=Infinity;
    for(let i=0;i<N;i++)for(let j=i+1;j<N;j++){const g=wins[i][j]+wins[j][i];if(g<bn){bn=g;bi=i;bj=j;}}
    const w=R()<sigmoid(beta*(skill[bi]-skill[bj]))?bi:bj, l=w===bi?bj:bi;
    wins[w][l]++;
  }
  const est=bradleyTerry(wins), tau=kendallTau(ranksFromScores(est),trueRank);
  (tau>=0.78?ok:bad)(`BT recovers order after 600 matches (τ=${tau.toFixed(2)} ≥ 0.78)`);
})();

// ---------- 2. DOM/canvas stub ----------
function makeCtx(){ const o={}; return new Proxy(o,{get:(t,k)=>k in t?t[k]:(typeof k==='symbol'?undefined:()=>{}),set:(t,k,v)=>{t[k]=v;return true;}}); }
function makeEl(tag){
  const ctx=makeCtx();
  const o={tagName:tag||'div',style:{},value:'',textContent:'',innerHTML:'',width:0,height:0,
    clientWidth:520,clientHeight:300,
    classList:{add(){},remove(){},toggle(){},contains(){return false;}},
    addEventListener(){},removeEventListener(){},appendChild(){},setAttribute(){},removeAttribute(){},
    getContext(){return ctx;},querySelector(){return makeEl();},querySelectorAll(){return [];},
    getBoundingClientRect(){return{width:520,height:300,left:0,top:0,right:520,bottom:300};},
    focus(){},remove(){},closest(){return makeEl();},
  };
  return new Proxy(o,{get:(t,k)=>k in t?t[k]:(typeof k==='symbol'?undefined:()=>{}),set:(t,k,v)=>{t[k]=v;return true;}});
}
function sandboxFor(stage){
  let rafN=0;
  const sb={
    console, Math, Date, JSON, parseFloat, parseInt, isNaN, Object, Array, String, Number,
    performance:{now:()=>0},
    setTimeout:()=>0, clearTimeout:()=>{},
    requestAnimationFrame:(cb)=>{ if(rafN++<3) cb(0); return rafN; },
    cancelAnimationFrame:()=>{},
  };
  sb.window={devicePixelRatio:1,addEventListener(){},requestAnimationFrame:sb.requestAnimationFrame};
  sb.document={getElementById:(id)=> id==='stage'?stage:makeEl(),
    createElement:(t)=>makeEl(t),querySelector:()=>makeEl(),querySelectorAll:()=>[],addEventListener(){}};
  sb.globalThis=sb;
  return sb;
}

function extractScript(html){
  const m=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)];
  if(!m.length) throw new Error('no <script> block');
  return m.map(x=>x[1]).join('\n');
}

function listComponents(){
  const out=[];
  for(const sub of ['sort','path','tsp']){
    const d=path.join(DIR,sub); if(!fs.existsSync(d)) continue;
    for(const f of fs.readdirSync(d)) if(f.endsWith('.html')) out.push(path.join(sub,f));
  }
  return out;
}

// Optional argv: restrict to one component (e.g. `node test.mjs path/city.html`
// or just `city.html`). Lets parallel builds validate in isolation.
const only = process.argv[2];
let comps = listComponents();
if(only) comps = comps.filter(r => r===only || r.endsWith('/'+only) || path.basename(r)===path.basename(only));

console.log('component smoke test\n');
for(const rel of comps){
  const html=fs.readFileSync(path.join(DIR,rel),'utf8');
  console.log(rel);
  let sb;
  try{
    const code=extractScript(html);
    const stage=makeEl();
    sb=sandboxFor(stage);
    vm.runInNewContext(code,sb,{timeout:4000});
    ok('script runs against DOM stub without throwing');
  }catch(e){ bad('script threw: '+(e&&e.message)); continue; }
  const comp=sb.window.__component;
  if(comp&&typeof comp.mount==='function') ok(`exposes window.__component.mount (${comp.name})`);
  else { bad('missing window.__component.mount'); continue; }
  // exercise mount + instant — metric-agnostic (tau / regret / gap / cost ...)
  try{
    const stage2=makeEl();
    const inst=comp.mount(stage2,{seed:7});
    if(inst&&inst.api&&typeof inst.api.instant==='function'){
      inst.api.instant(80);
      const s=(inst.api.state&&inst.api.state())||{};
      const nums=Object.entries(s).filter(([k,v])=>typeof v==='number'&&isFinite(v));
      (nums.length?ok:bad)(`mount + 80 steps ok (${nums.map(([k,v])=>`${k}=${v.toFixed(2)}`).join(', ')||'no numeric metric in state()'})`);
    } else ok('mount ran (no api.instant to exercise)');
  }catch(e){ bad('mount/instant threw: '+(e&&e.message)); }
}

console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail?1:0);
