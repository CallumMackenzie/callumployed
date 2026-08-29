export function dashboardLoginPage(invalid = false): string {
  return page("Callumployed Central", `
    <main class="login-shell">
      <section class="login-card">
        <p class="eyebrow">Callumployed Central</p>
        <h1>Cloud metrics</h1>
        <p class="muted">Enter the Central passkey to view private aggregate scan metrics.</p>
        ${invalid ? '<p class="error" role="alert">That passkey was not accepted.</p>' : ""}
        <form method="post" action="dashboard/login">
          <label for="passkey">Central passkey</label>
          <input id="passkey" name="passkey" type="password" autocomplete="current-password" required autofocus>
          <button type="submit">Open dashboard</button>
        </form>
      </section>
    </main>`, "login");
}

export function dashboardPage(): string {
  return page("Callumployed metrics", `
    <header class="topbar">
      <div><p class="eyebrow">Callumployed Central</p><h1>Scan intelligence</h1></div>
      <div class="actions">
        <label>Range <select id="range"><option value="7">7 days</option><option value="30" selected>30 days</option><option value="90">90 days</option><option value="all">All time</option></select></label>
        <form method="post" action="dashboard/logout"><button class="secondary" type="submit">Log out</button></form>
      </div>
    </header>
    <main class="dashboard">
      <p id="status" class="status">Loading cloud metrics…</p>
      <section id="cards" class="cards" aria-label="metric overview"></section>
      <section class="grid">
        <article class="panel wide"><div class="panel-head"><div><p class="eyebrow">Activity</p><h2>Scans and discoveries</h2></div></div><div id="timeline" class="chart"></div></article>
        <article class="panel"><p class="eyebrow">Conversion</p><h2>Scan funnel</h2><div id="funnel" class="funnel"></div></article>
        <article class="panel"><p class="eyebrow">Reliability</p><h2>Failure types</h2><div id="failures" class="bars"></div></article>
        <article class="panel"><p class="eyebrow">Discovery</p><h2>Candidate selection</h2><div id="candidate-selection" class="bars"></div></article>
        <article class="panel"><p class="eyebrow">Discovery</p><h2>Selection methods</h2><div id="discovery-methods" class="bars"></div></article>
        <article class="panel"><p class="eyebrow">Quality</p><h2>Candidate confidence</h2><div id="candidate-confidence" class="bars"></div></article>
        <article class="panel"><p class="eyebrow">Quality</p><h2>Page confidence</h2><div id="page-confidence" class="bars"></div></article>
        <article class="panel"><p class="eyebrow">Verification</p><h2>Outcomes</h2><div id="verification-outcomes" class="bars"></div></article>
        <article class="panel"><p class="eyebrow">Verification</p><h2>Extraction methods</h2><div id="extraction-methods" class="bars"></div></article>
        <article class="panel wide"><p class="eyebrow">Verification</p><h2>Rejection reasons</h2><div id="rejection-reasons" class="bars"></div></article>
        <article class="panel wide"><p class="eyebrow">Companies</p><h2>Performance</h2><div class="table-wrap"><table><thead><tr><th>Company</th><th>Scans</th><th>Success</th><th>Avg duration</th><th>Candidates</th><th>Discovered</th><th>Saved</th><th>Failed visits</th></tr></thead><tbody id="companies"></tbody></table></div></article>
        <article class="panel"><p class="eyebrow">Clients</p><h2>App versions</h2><div id="versions" class="bars"></div></article>
      </section>
    </main>
    <script>
      const statusNode = document.querySelector('#status');
      const rangeNode = document.querySelector('#range');
      const number = value => Number(value || 0).toLocaleString();
      const percent = value => new Intl.NumberFormat(undefined, {style:'percent', maximumFractionDigits:1}).format(value || 0);
      const duration = value => value >= 60000 ? (value / 60000).toFixed(1) + 'm' : (value / 1000).toFixed(1) + 's';
      const text = (tag, value, className = '') => { const node = document.createElement(tag); node.textContent = value; node.className = className; return node; };
      async function loadMetrics() {
        statusNode.textContent = 'Loading cloud metrics…';
        try {
          const response = await fetch('v1/dashboard/metrics?days=' + encodeURIComponent(rangeNode.value));
          if (response.status === 401) { location.href = 'dashboard'; return; }
          if (!response.ok) throw new Error('request failed');
          const data = await response.json(); render(data);
          statusNode.textContent = data.record_count ? 'Updated ' + new Date(data.generated_at).toLocaleString() + (data.truncated ? ' · showing first 5,000 records' : '') : 'No metrics recorded in this range yet.';
        } catch { statusNode.textContent = 'Could not load Central metrics.'; }
      }
      function render(data) {
        const s = data.summary;
        const cards = [
          ['Total scans', number(s.total_scans), number(s.succeeded_scans) + ' succeeded'],
          ['Success rate', percent(s.success_rate), number(s.failed_scans) + ' failed'],
          ['Roles discovered', number(s.potential_roles_discovered), number(s.roles_saved) + ' saved'],
          ['Median duration', duration(s.median_duration_ms), 'p95 ' + duration(s.p95_duration_ms)],
          ['Candidates scanned', number(s.candidates_scanned), number(s.pages_scanned) + ' pages'],
          ['Career pages', number(s.career_pages_total), number(s.pages_scanned) + ' page scans'],
          ['Verified roles', number(s.verified_open_roles), number(s.role_verification_attempts) + ' attempts'],
          ['Agent-assisted scans', number(s.agent_trace_scans), percent(s.total_scans ? s.agent_trace_scans / s.total_scans : 0)],
        ];
        const cardsNode = document.querySelector('#cards'); cardsNode.replaceChildren();
        cards.forEach(([label, value, note]) => { const card = document.createElement('article'); card.className='metric-card'; card.append(text('p',label,'metric-label'),text('strong',value),text('span',note)); cardsNode.append(card); });
        renderTimeline(data.timeseries); renderFunnel(s); renderBars('#failures', data.failures, 'No failed scans'); renderBars('#versions', data.versions, 'No version data'); renderCompanies(data.companies);
        const b=data.breakdowns; renderBars('#candidate-selection',b.candidate_selection,'No v2 selection data'); renderBars('#discovery-methods',b.candidate_discovery_method,'No v2 discovery data'); renderBars('#candidate-confidence',b.candidate_confidence,'No v2 confidence data'); renderBars('#page-confidence',b.page_confidence,'No v2 page data'); renderBars('#verification-outcomes',b.verification_outcome,'No v2 outcome data'); renderBars('#extraction-methods',b.extraction_method,'No v2 extraction data'); renderBars('#rejection-reasons',b.rejection_reason,'No v2 rejection data');
      }
      function renderTimeline(rows) {
        const root = document.querySelector('#timeline'); root.replaceChildren();
        if (!rows.length) { root.append(text('p','No activity in this range.','empty')); return; }
        const width=900,height=260,pad=34,max=Math.max(1,...rows.flatMap(row=>[row.scans,row.roles_discovered]));
        const svg=document.createElementNS('http://www.w3.org/2000/svg','svg'); svg.setAttribute('viewBox','0 0 '+width+' '+height); svg.setAttribute('role','img'); svg.setAttribute('aria-label','Scans and discovered roles over time');
        const points = key => rows.map((row,index)=>(pad+(index*(width-pad*2)/Math.max(1,rows.length-1)))+','+(height-pad-(row[key]*(height-pad*2)/max))).join(' ');
        [['scans','#16a085'],['roles_discovered','#82d173']].forEach(([key,color])=>{const line=document.createElementNS(svg.namespaceURI,'polyline'); line.setAttribute('points',points(key)); line.setAttribute('fill','none');line.setAttribute('stroke',color);line.setAttribute('stroke-width','4');line.setAttribute('stroke-linejoin','round');svg.append(line);}); root.append(svg);
        const legend=document.createElement('div');legend.className='legend';legend.append(text('span','● Scans'),text('span','● Roles discovered'));root.append(legend);
      }
      function renderFunnel(s) {
        const rows=[['Candidates',s.candidates_scanned],['Potential roles',s.potential_roles_discovered],['Verified open',s.verified_open_roles],['Saved',s.roles_saved]]; const max=Math.max(1,...rows.map(row=>row[1])); const root=document.querySelector('#funnel');root.replaceChildren();
        rows.forEach(([label,value])=>{const row=document.createElement('div');row.className='funnel-row';const bar=document.createElement('div');bar.className='funnel-bar';bar.style.width=Math.max(3,value/max*100)+'%';bar.textContent=number(value);row.append(text('span',label),bar);root.append(row);});
      }
      function renderBars(selector, rows, empty) { const root=document.querySelector(selector);root.replaceChildren(); if(!rows.length){root.append(text('p',empty,'empty'));return;} const max=Math.max(...rows.map(row=>row.count)); rows.slice(0,10).forEach(row=>{const wrap=document.createElement('div');wrap.className='bar-row';const label=text('span',row.label);const track=document.createElement('div');track.className='bar-track';const fill=document.createElement('div');fill.className='bar-fill';fill.style.width=(row.count/max*100)+'%';track.append(fill);wrap.append(label,track,text('strong',number(row.count)));root.append(wrap);}); }
      function renderCompanies(rows) { const body=document.querySelector('#companies');body.replaceChildren(); rows.forEach(row=>{const tr=document.createElement('tr');[row.company_name,number(row.scans),percent(row.success_rate),duration(row.average_duration_ms),number(row.candidates_scanned),number(row.roles_discovered),number(row.roles_saved),number(row.failed_role_visits)].forEach(value=>tr.append(text('td',value)));body.append(tr);}); }
      rangeNode.addEventListener('change', loadMetrics); loadMetrics();
    </script>`);
}

function page(title: string, body: string, bodyClass = ""): string {
  return `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${title}</title><style>
  :root{color-scheme:dark;--bg:#07110f;--panel:#101d1a;--line:#29423b;--text:#eff9f4;--muted:#91aaa2;--accent:#4ed2a6;--accent2:#82d173;--danger:#ff8e86}*{box-sizing:border-box}body{margin:0;background:radial-gradient(circle at 10% 0,#113329 0,transparent 34%),var(--bg);color:var(--text);font:15px/1.45 ui-sans-serif,system-ui,-apple-system,sans-serif;min-height:100vh}button,input,select{font:inherit}.topbar{display:flex;justify-content:space-between;gap:24px;align-items:center;padding:28px clamp(20px,5vw,72px);border-bottom:1px solid var(--line);background:#07110fcc;backdrop-filter:blur(14px);position:sticky;top:0;z-index:4}h1,h2,p{margin-top:0}h1{font-size:clamp(28px,4vw,44px);margin-bottom:0;letter-spacing:-.04em}h2{font-size:20px}.eyebrow{text-transform:uppercase;letter-spacing:.14em;color:var(--accent);font-size:11px;font-weight:800;margin-bottom:5px}.muted,.status,.empty{color:var(--muted)}.actions{display:flex;align-items:end;gap:12px}.actions label{color:var(--muted);font-size:12px}.actions select{display:block;margin-top:4px}.dashboard{padding:28px clamp(20px,5vw,72px) 72px}.status{min-height:22px}.cards{display:grid;grid-template-columns:repeat(6,minmax(150px,1fr));gap:12px}.metric-card,.panel,.login-card{background:linear-gradient(145deg,#13221e,#0d1815);border:1px solid var(--line);border-radius:16px;box-shadow:0 14px 40px #0003}.metric-card{padding:18px}.metric-card strong{display:block;font-size:28px;letter-spacing:-.04em}.metric-card span,.metric-label{color:var(--muted);font-size:12px}.grid{display:grid;grid-template-columns:2fr 1fr;gap:16px;margin-top:16px}.panel{padding:22px;min-width:0}.panel.wide{grid-column:span 2}.chart svg{width:100%;height:260px;background:linear-gradient(#ffffff05 1px,transparent 1px);background-size:100% 52px}.legend{display:flex;gap:20px;color:var(--muted)}.legend span:first-child{color:#16a085}.legend span:last-child{color:#82d173}.funnel-row{margin:16px 0}.funnel-row>span{display:block;color:var(--muted);font-size:12px;margin-bottom:5px}.funnel-bar{background:linear-gradient(90deg,#168d72,var(--accent2));color:#04110d;border-radius:7px;padding:7px 10px;min-width:max-content;font-weight:800}.bar-row{display:grid;grid-template-columns:minmax(90px,1fr) 2fr 40px;gap:10px;align-items:center;margin:14px 0}.bar-row>span{overflow:hidden;text-overflow:ellipsis}.bar-track{height:9px;border-radius:9px;background:#233630;overflow:hidden}.bar-fill{height:100%;background:var(--accent);border-radius:inherit}.table-wrap{overflow:auto}table{width:100%;border-collapse:collapse;white-space:nowrap}th,td{text-align:right;padding:12px;border-bottom:1px solid var(--line)}th:first-child,td:first-child{text-align:left}th{color:var(--muted);font-size:11px;text-transform:uppercase;letter-spacing:.08em}button,select,input{border:1px solid var(--line);border-radius:9px;background:#152722;color:var(--text);padding:10px 13px}button{background:var(--accent);color:#06130f;border:0;font-weight:800;cursor:pointer}.secondary{background:#172823;color:var(--text);border:1px solid var(--line)}.login-shell{min-height:100vh;display:grid;place-items:center;padding:20px}.login-card{width:min(440px,100%);padding:32px}.login-card form{display:grid;gap:12px;margin-top:24px}.login-card label{color:var(--muted)}.login-card input{width:100%;font-size:18px}.error{color:var(--danger);padding:10px 12px;background:#441d1a;border-radius:8px}@media(max-width:1100px){.cards{grid-template-columns:repeat(3,1fr)}}@media(max-width:720px){.topbar{position:static;align-items:flex-start;flex-direction:column}.cards{grid-template-columns:repeat(2,1fr)}.grid{display:block}.panel{margin-top:14px}.actions{width:100%;justify-content:space-between}.metric-card strong{font-size:23px}}
  </style></head><body class="${bodyClass}">${body}</body></html>`;
}
