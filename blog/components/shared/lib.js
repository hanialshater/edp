// Canonical helpers for the component workshop.
// Components INLINE a copy of what they need (single-file portability);
// this file is the source of truth and is imported by test.mjs for
// invariant checks. Keep these pure (no DOM).

export const COLORS = {
  blue:'#4c8df6', green:'#5fd2a3', orange:'#f0a058', purple:'#c879f0',
  red:'#e16c6c', pink:'#ff7eb6', gold:'#f5c451', dim:'#8b95a8',
  faint:'#3a4358', fg:'#e6edf3', bg:'#0e1626',
  grass:'#1f6b3a', grassDark:'#185730', line:'#cfe8d6',
  cycle:['#4c8df6','#5fd2a3','#f0a058','#c879f0','#e16c6c','#ff7eb6','#f5c451','#7ee0d0'],
};

// Deterministic seeded RNG (mulberry32). rng(seed) -> ()=>[0,1).
export function rng(seed){
  let s = seed|0 || 1;
  return function(){ s=(s+0x6D2B79F5)|0; let t=s;
    t=Math.imul(t^(t>>>15), t|1); t^=t+Math.imul(t^(t>>>7), t|61);
    return ((t^(t>>>14))>>>0)/4294967296; };
}
export function gauss(rand){ const u=rand()||1e-12, v=rand();
  return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v); }
export function clamp(x,lo,hi){ return Math.max(lo, Math.min(hi, x)); }
export function sigmoid(x){ return 1/(1+Math.exp(-x)); }
export function argmax(a){ let i=0; for(let j=1;j<a.length;j++) if(a[j]>a[i]) i=j; return i; }

// Kendall tau between two rank vectors (rank[i] = position of item i, 0=top).
export function kendallTau(rA, rB){
  const n=rA.length; let c=0,d=0;
  for(let i=0;i<n;i++) for(let j=i+1;j<n;j++){
    const a=Math.sign(rA[i]-rA[j]), b=Math.sign(rB[i]-rB[j]);
    if(a*b>0) c++; else if(a*b<0) d++;
  }
  const tot=n*(n-1)/2; return tot? (c-d)/tot : 1;
}

// Bradley-Terry skill fit by MM (minorization-maximization) on a win matrix.
// wins[i][j] = times i beat j. Returns skills s[i] (log-scale, centered),
// from p_i = exp(s_i) with sum p = N. A handful of iters converges for small N.
export function bradleyTerry(wins, iters=60){
  const n=wins.length;
  const W=new Array(n).fill(0);                 // total wins per player
  const G=Array.from({length:n},()=>new Array(n).fill(0)); // games i vs j
  for(let i=0;i<n;i++) for(let j=0;j<n;j++){
    W[i]+=wins[i][j];
    const g=wins[i][j]+wins[j][i]; G[i][j]=g; G[j][i]=g;
  }
  let p=new Array(n).fill(1);                    // strengths (>0)
  for(let it=0; it<iters; it++){
    const np=new Array(n);
    for(let i=0;i<n;i++){
      let denom=0;
      for(let j=0;j<n;j++){ if(j===i) continue;
        if(G[i][j]>0) denom += G[i][j]/(p[i]+p[j]); }
      np[i] = denom>0 ? (W[i]+0.5)/denom : p[i];  // +0.5 smoothing, keeps unbeaten finite
    }
    // normalize so geometric mean = 1 (keeps numbers tame)
    let logsum=0; for(let i=0;i<n;i++) logsum+=Math.log(np[i]);
    const g=Math.exp(logsum/n);
    for(let i=0;i<n;i++) p[i]=np[i]/g;
    p=p;
  }
  return p.map(v=>Math.log(v));   // skills on log scale, centered ~0
}

// Rank vector from a score array (higher score = better = rank 0).
export function ranksFromScores(scores){
  const idx=[...scores.keys()].sort((a,b)=>scores[b]-scores[a]);
  const r=new Array(scores.length); idx.forEach((v,k)=>r[v]=k); return r;
}
