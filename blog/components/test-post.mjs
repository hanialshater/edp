// Post-level smoke test: validate a composed post embeds its component(s)
// without throwing and pulls in NO external network assets (offline rule).
//   node components/test-post.mjs 02-sort/index.html [03-shortest-path/index.html ...]
// Reuses the same DOM/canvas stub philosophy as test.mjs.

import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const DIR = path.dirname(fileURLToPath(import.meta.url));      // .../blog/components
const BLOG = path.dirname(DIR);                                // .../blog
let fail=0, pass=0;
const ok=(m)=>{pass++;console.log('  \x1b[32m✓\x1b[0m '+m);};
const bad=(m)=>{fail++;console.log('  \x1b[31m✗\x1b[0m '+m);};

function makeCtx(){const o={};return new Proxy(o,{get:(t,k)=>k in t?t[k]:(typeof k==='symbol'?undefined:()=>{}),set:(t,k,v)=>{t[k]=v;return true;}});}
function makeEl(tag){const ctx=makeCtx();const o={tagName:tag||'div',style:{},value:'',textContent:'',innerHTML:'',width:0,height:0,clientWidth:760,clientHeight:300,
  classList:{add(){},remove(){},toggle(){},contains(){return false;}},
  addEventListener(){},removeEventListener(){},appendChild(){},insertBefore(){},setAttribute(){},removeAttribute(){},
  getContext(){return ctx;},querySelector(){return makeEl();},querySelectorAll(){return [];},
  getBoundingClientRect(){return{width:760,height:300,left:0,top:0,right:760,bottom:300};},focus(){},remove(){},closest(){return makeEl();}};
  return new Proxy(o,{get:(t,k)=>k in t?t[k]:(typeof k==='symbol'?undefined:()=>{}),set:(t,k,v)=>{t[k]=v;return true;}});}
function sandbox(){let raf=0;const sb={console,Math,Date,JSON,parseFloat,parseInt,isNaN,Object,Array,String,Number,
  performance:{now:()=>0},setTimeout:()=>0,clearTimeout:()=>{},
  requestAnimationFrame:(cb)=>{if(raf++<3)cb(0);return raf;},cancelAnimationFrame:()=>{}};
  sb.window={devicePixelRatio:1,addEventListener(){},requestAnimationFrame:sb.requestAnimationFrame};
  sb.document={getElementById:()=>makeEl(),createElement:(t)=>makeEl(t),querySelector:()=>makeEl(),querySelectorAll:()=>[],addEventListener(){},body:makeEl()};
  // browser globals some posts use at top level (OPRO provider panel)
  const store={}; sb.localStorage={getItem:k=>k in store?store[k]:null,setItem:(k,v)=>{store[k]=''+v;},removeItem:k=>{delete store[k];}};
  sb.fetch=()=>Promise.reject(new Error('network disabled in test')); sb.AbortController=class{constructor(){this.signal={};}abort(){}};
  sb.globalThis=sb;return sb;}

const targets = process.argv.slice(2);
if(!targets.length){console.error('usage: node test-post.mjs <post/index.html> [...]');process.exit(2);}

for(const rel of targets){
  const file=path.isAbsolute(rel)?rel:path.join(BLOG,rel);
  console.log(rel);
  if(!fs.existsSync(file)){bad('file not found: '+file);continue;}
  const html=fs.readFileSync(file,'utf8');
  // 1. no external loaded ASSETS at page load (script/link/img from the network).
  // A user-initiated fetch() to a user-supplied provider (e.g. the OPRO live-LLM
  // panel) is allowed and noted, since it only runs on an explicit click.
  const ext=[];
  for(const m of html.matchAll(/<script[^>]*\ssrc\s*=\s*["']([^"']+)["']/gi)) ext.push('script src '+m[1]);
  for(const m of html.matchAll(/<link[^>]*\shref\s*=\s*["']([^"']+)["']/gi)) ext.push('link '+m[1]);
  for(const m of html.matchAll(/<img[^>]*\ssrc\s*=\s*["'](https?:[^"']+)["']/gi)) ext.push('img '+m[1]);
  (ext.length?bad:ok)(ext.length?('external/network assets at load: '+ext.join(', ')):'no external assets loaded at page load');
  if(/\bfetch\s*\(/.test(html)) console.log('    (note: contains a user-initiated fetch — provider panel; runs only on click)');
  // 2. all <script> blocks run against DOM stub without throwing
  const scripts=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m=>m[1]);
  if(!scripts.length){bad('no inline <script> blocks');continue;}
  try{ vm.runInNewContext(scripts.join('\n'),sandbox(),{timeout:6000}); ok(`${scripts.length} script block(s) run without throwing`); }
  catch(e){ bad('script threw: '+(e&&e.message)); }
  // 3. has a forward/next link and the series nav
  (/class=["']nav["']/.test(html)?ok:bad)('has series nav');
}
console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail?1:0);
