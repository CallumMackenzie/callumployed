import{t as e}from"./preload-helper-Czpn1I53.js";var{sankey:t,sankeyLinkHorizontal:n}=await e(async()=>{let{sankey:e,sankeyLinkHorizontal:t}=await import(`/assets/d3-sankey.js`);return{sankey:e,sankeyLinkHorizontal:t}},[]),r=document.querySelector(`#stats`),i=document.querySelector(`#status-list`),a=document.querySelector(`#search-toggle`),o=document.querySelector(`#search-dialog`),s=document.querySelector(`#search-backdrop`),c=document.querySelector(`#search-form`),l=document.querySelector(`#search-input`),u=document.querySelector(`#close-search`),d=document.querySelector(`#materials-panel`),ee=document.querySelector(`#materials-toggle`),te=document.querySelector(`#materials-body`),ne=document.querySelector(`#materials-summary`),re=document.querySelector(`#materials-required-warning`),f=document.querySelector(`#resume-meta`),p=document.querySelector(`#resume-upload`),ie=document.querySelector(`#resume-upload-button`),ae=document.querySelector(`#resume-resource-meta`),oe=document.querySelector(`#resume-resource-upload`),se=document.querySelector(`#resume-resource-upload-button`),ce=document.querySelector(`#resume-resource-list`),le=document.querySelector(`#cover-letter-meta`),ue=document.querySelector(`#cover-letter-upload`),de=document.querySelector(`#cover-letter-upload-button`),fe=document.querySelector(`#cover-letter-list`),pe=document.querySelector(`#experience-note-meta`),me=document.querySelector(`#experience-note-upload`),he=document.querySelector(`#experience-note-upload-button`),ge=document.querySelector(`#experience-note-list`),_e=document.querySelector(`#review-discovered`),ve=document.querySelector(`#prep-interested`),m=document.querySelector(`#review-view`),ye=document.querySelector(`#review-heading`),be=document.querySelector(`#review-progress`),xe=document.querySelector(`#review-card`),Se=document.querySelector(`#close-review`),h=document.querySelector(`#prep-view`),Ce=document.querySelector(`#prep-heading`),we=document.querySelector(`#prep-progress`),g=document.querySelector(`#prep-card`),Te=document.querySelector(`#close-prep`),_=document.querySelector(`#scan-all-button`),Ee=document.querySelector(`#manage-companies-button`),v=document.querySelector(`#scan-status-bar`),y=document.querySelector(`#scan-status-text`),De=document.querySelector(`#scan-last-time`),Oe=document.querySelector(`#scan-errors`),ke=document.querySelector(`#toggle-all`),Ae=document.querySelector(`#collapse-empty`),je=document.querySelector(`#toolbar-summary`),Me=document.querySelector(`#settings-open`),Ne=document.querySelector(`#settings-view`),Pe=document.querySelector(`#settings-close`),b=document.querySelector(`#settings-status`),Fe=document.querySelector(`#settings-form`),Ie=document.querySelector(`#settings-profile-options`),Le=document.querySelector(`#settings-options`),Re=document.querySelector(`#central-store-summary`),ze=document.querySelector(`#central-store-sync-summary`),x=document.querySelector(`#central-api-url-input`),Be=document.querySelector(`#central-passkey-input`),Ve=document.querySelector(`#central-save-button`),S=document.querySelector(`#central-sync-button`),He=document.querySelector(`#recommendation-history-summary`),Ue=document.querySelector(`#clear-recommendation-history`),We=document.querySelector(`#metrics-open-button`),Ge=document.querySelector(`#metrics-view`),Ke=document.querySelector(`#metrics-close`),C=document.querySelector(`#metrics-status`),qe=document.querySelector(`#metrics-overview`),Je=document.querySelector(`#metrics-sections`),Ye=document.querySelector(`#metrics-scan-list`),Xe=document.querySelector(`#sankey-open-button`),Ze=document.querySelector(`#sankey-view`),Qe=document.querySelector(`#sankey-close`),w=document.querySelector(`#sankey-status`),$e=document.querySelector(`#sankey-canvas`),et=document.querySelector(`#sankey-path-list`),tt=document.querySelector(`#app-update-button`),nt=document.querySelector(`#companies-view`),rt=document.querySelector(`#companies-close`),T=document.querySelector(`#companies-status`),it=document.querySelector(`#company-create-form`),E=document.querySelector(`#companies-list`),at=document.querySelector(`#role-add-form`),ot=document.querySelector(`#role-url-input`),st=document.querySelector(`#role-company-input`),ct=document.querySelector(`#role-company-options`),lt=document.querySelector(`#role-add-status`),ut=3,dt=1200,ft=new Set([`applied`,`OA`,`interview`,`rejected`,`offer`]),pt=new Map([[`discovered`,`#4f6472`],[`interested`,`#00897b`],[`disinterested`,`#626970`],[`applied`,`#2257ad`],[`oa`,`#b36b00`],[`interview`,`#5f2bd8`],[`rejected`,`#b93d2d`],[`offer`,`#137347`],[`closed`,`#53606b`],[`archived`,`#765b4a`]]),mt=/^(?:about (?:the )?(?:role|team|job)|about this role|job description|job responsibilities|minimum qualifications|preferred qualifications|qualifications|requirements|responsibilities|what to expect|what (?:you'll|you’ll|you will) (?:bring|do)|what'?s in it for you|who you are|your objectives|your skills & talents):?$/i,ht=!0,D=null,O=null,k=[],A=[],j=[],M=[],N=[],P=new Map,gt=new Map,F=new Map,_t=new Map,I=new Map,vt=new Map,yt=new Map,bt=new Map,xt=!1,St=null,Ct=!1,wt=null,Tt=null,Et=null,Dt=null,L=null,Ot=[],kt=new Map;function R(){return D?.query?.trim()??``}function At(){let e=!!R();a.classList.toggle(`search-active`,e),a.setAttribute(`aria-label`,e?`clear search`:`search jobs`)}function jt(){l.value=R(),o.hidden=!1,c.hidden=!1,l.focus(),l.select()}function Mt(){o.hidden=!0,c.hidden=!0,a.focus()}function Nt(e){return e?new Intl.DateTimeFormat(void 0,{month:`short`,day:`numeric`,hour:`numeric`,minute:`2-digit`}).format(new Date(e)).toLocaleLowerCase():``}function z(e){return e?new Intl.DateTimeFormat(void 0,{month:`short`,day:`numeric`,hour:`numeric`,minute:`2-digit`}).format(new Date(e)).replace(`, `,` `).toLocaleLowerCase():``}function B(e){return String(e??``).replaceAll(`&`,`&amp;`).replaceAll(`<`,`&lt;`).replaceAll(`>`,`&gt;`).replaceAll(`"`,`&quot;`).replaceAll(`'`,`&#039;`)}function V(e){return String(e??``).toLocaleLowerCase()}function H(e){return B(V(e))}function Pt(e){return e}function U(e=g){e.querySelectorAll(`[data-prep-resume-latex], [data-prep-cover-letter-latex]`).forEach(Pt)}function Ft(){return`
    <svg class="role-link-icon" viewBox="0 0 24 24" aria-hidden="true">
      <path d="M7 17 17 7"></path>
      <path d="M8 7h9v9"></path>
    </svg>
  `}function It(){return`
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M12 5v14"></path>
      <path d="M5 12h14"></path>
    </svg>
  `}function Lt(){return`
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M3 6h18"></path>
      <path d="M8 6V4h8v2"></path>
      <path d="m19 6-1 14H6L5 6"></path>
      <path d="M10 11v5"></path>
      <path d="M14 11v5"></path>
    </svg>
  `}function Rt(e,t,n){let r=`<span class="role-title-text">${H(e)}</span>`;return t?`<a class="${n}" href="${B(t)}" target="_blank" rel="noreferrer">${r}${Ft()}</a>`:`<span class="${n}">${r}</span>`}function zt(e){r.innerHTML=[[`companies`,e.companies_total],[`jobs`,e.jobs_total],[`applications`,e.applications_total]].map(([e,t])=>`<dl class="stat"><dt>${H(e)}</dt><dd>${t}</dd></dl>`).join(``)}function Bt(e=D){if(!e){je.innerHTML=``;return}let t=t=>e.statuses.find(e=>e.key===t)?.count??0;je.innerHTML=[[`discovered`,t(`discovered`)],[`interested`,t(`interested`)],[`applied`,e.stats?.applications_total??0],[`total`,e.stats?.jobs_total??0]].map(([e,t])=>`
        <dl>
          <dt>${H(e)}</dt>
          <dd>${t}</dd>
        </dl>
      `).join(``)}function Vt(e,t=``){if(O=e,ie.textContent=e?`replace`:`upload`,t){f.textContent=t;return}if(!e){f.textContent=`no resume uploaded`;return}let n=z(e.updated_at),r=qt(e.content_bytes);f.textContent=[V(e.filename),r,n].filter(Boolean).join(` | `)}function Ht(e,t=``){A=Array.isArray(e)?e:[],de.textContent=A.length>0?`add`:`upload`,le.textContent=t||(A.length===0?`no examples uploaded`:`${A.length} ${A.length===1?`example`:`examples`} stored`);let n=A.slice(0,3),r=Math.max(A.length-n.length,0);fe.innerHTML=n.map(e=>{let t=qt(e.content_bytes);return`
        <li title="${H(e.filename)}">
          <span>${H(e.filename)}</span>
          <small>${B(t)}</small>
        </li>
      `}).join(``),r>0&&fe.insertAdjacentHTML(`beforeend`,`<li class="examples-more"><span>+${r} more</span></li>`)}function Ut(e,t=``){j=Array.isArray(e)?e:[],he.textContent=j.length>0?`add`:`upload`,pe.textContent=t||(j.length===0?`no notes uploaded`:`${j.length} ${j.length===1?`note`:`notes`} stored`);let n=j.slice(0,3),r=Math.max(j.length-n.length,0);ge.innerHTML=n.map(e=>{let t=qt(e.content_bytes);return`
        <li title="${H(e.filename)}">
          <span>${H(e.filename)}</span>
          <small>${B(t)}</small>
        </li>
      `}).join(``),r>0&&ge.insertAdjacentHTML(`beforeend`,`<li class="examples-more"><span>+${r} more</span></li>`)}function Wt(e,t=``){k=Array.isArray(e)?e:[],se.textContent=k.length>0?`add`:`upload`,ae.textContent=t||(k.length===0?`no resources uploaded`:`${k.length} ${k.length===1?`resource`:`resources`} stored`);let n=k.slice(0,3),r=Math.max(k.length-n.length,0);ce.innerHTML=n.map(e=>{let t=qt(e.bytes);return`
        <li title="${H(e.filename)}">
          <span>${H(e.filename)}</span>
          <small>${B(t)}</small>
        </li>
      `}).join(``),r>0&&ce.insertAdjacentHTML(`beforeend`,`<li class="examples-more"><span>+${r} more</span></li>`)}function Gt(e,t={}){Vt(e?.master_resume??null),Wt(e?.resume_resources??[]),Ht(e?.cover_letter_examples??[]),Ut(e?.experience_notes??[]),W(e?.ui),(!xt||t.applyDefaultCollapsed)&&(Kt(!!e?.ui?.default_collapsed),xt=!0)}function W(e=null){let t=O?`resume ready`:`no resume`,n=k.length===0?`no resources`:`${k.length} ${k.length===1?`resource`:`resources`}`,r=A.length,i=r===0?`no cover letters`:`${r} cover ${r===1?`letter`:`letters`}`,a=j.length,o=a===0?`no notes`:`${a} experience ${a===1?`note`:`notes`}`;re.hidden=!(typeof e?.has_missing_required_materials==`boolean`?e.has_missing_required_materials:!O||r===0||a===0),ne.textContent=`${t} | ${n} | ${i} | ${o}`}function Kt(e){d.classList.toggle(`collapsed`,e),ee.setAttribute(`aria-expanded`,String(!e)),ee.querySelector(`.materials-chevron`).textContent=e?`>`:`v`,te.hidden=e}function qt(e){return Number.isFinite(e)?e<1024?`${e} b`:`${Math.round(e/1024)} kb`:``}function Jt(e){i.innerHTML=e.map(e=>{let t=e.jobs.map(t=>Yt(t,e.key)).join(``);return`
        <section class="status-pane ${e.count===0?`empty`:``} ${ht?`hidden-empty`:``}" id="status-${B(e.key)}" data-bucket="${B(e.key)}">
          <button class="pane-toggle" type="button" aria-expanded="false">
            <span class="chevron">></span>
            <span class="pane-title">${H(e.label)}</span>
            <span class="count">${e.count}</span>
          </button>
          <div class="pane-body" hidden>
            ${t?`<div class="jobs">${t}</div>`:`<p class="empty-copy">no jobs in this status.</p>`}
          </div>
        </section>
      `}).join(``)}function Yt(e,t){return`
    <details class="job" data-role-id="${B(e.id)}">
      <summary class="job-summary">
        <span class="job-chevron">></span>
        <span class="job-identity">
          <span class="job-company">[${H(e.company_name)}]</span>
          ${Rt(e.title,e.role_url,`job-title`)}
          ${t===`interested`&&e.prep_started?Qt():``}
          ${t===`closed`&&e.updated_in_latest_scan?Xt():``}
          ${[`discovered`,`interested`].includes(t)&&e.missing_from_latest_scan?Zt():``}
        </span>
      </summary>
      <div class="job-detail">
        ${t===`discovered`?$t(e):``}
        ${t===`interested`?en(e):``}
        ${t===`disinterested`?tn(e):``}
        ${t===`applied`?nn(e):``}
        ${t===`OA`?rn(e):``}
        ${t===`interview`?an(e):``}
        ${t===`closed`?on(e):``}
        <dl>
          ${e.location?`<div>
                  <dt>location</dt>
                  <dd>${H(e.location)}</dd>
                </div>`:``}
          <div>
            <dt>updated</dt>
            <dd>${Nt(e.updated_at)}</dd>
          </div>
        </dl>
      </div>
    </details>
  `}function Xt(){return`<span class="latest-scan-dot" title="updated in latest scan" aria-label="updated in latest scan"></span>`}function Zt(){return`<span class="missing-latest-scan-dot" title="not seen in latest scan" aria-label="not seen in latest scan"></span>`}function Qt(){return`<span class="prep-started-dot" title="application materials started" aria-label="application materials started"></span>`}function $t(e){return`
    <div class="job-actions job-actions-nowrap" aria-label="discovered role actions">
      <button class="job-action success" type="button" data-review-role-id="${e.id}">view</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="interested">interested</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="disinterested">disinterested</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="closed">closed</button>
    </div>
  `}function en(e){return`
    <div class="job-actions" aria-label="interested role actions">
      <button class="job-action success" type="button" data-prep-role-id="${e.id}">prep</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="applied">applied</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="disinterested">disinterested</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="closed">closed</button>
    </div>
  `}function tn(e){return`
    <div class="job-actions" aria-label="disinterested role actions">
      <button class="job-action success" type="button" data-role-id="${e.id}" data-status="interested">interested</button>
    </div>
  `}function nn(e){return`
    <div class="job-actions job-actions-nowrap" aria-label="applied role actions">
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="OA">oa</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="interview">interview</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="rejected">rejected</button>
    </div>
  `}function rn(e){return`
    <div class="job-actions job-actions-nowrap" aria-label="oa role actions">
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="interview">interview</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="disinterested">disinterested</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="rejected">rejected</button>
    </div>
  `}function an(e){return`
    <div class="job-actions" aria-label="interview role actions">
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="rejected">rejected</button>
      <button class="job-action success" type="button" data-role-id="${e.id}" data-status="offer">offer</button>
    </div>
  `}function on(e){return`
    <div class="job-actions" aria-label="closed role actions">
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="interested">interested</button>
    </div>
  `}function sn(e){D=e,l.value=e.query,At(),zt(e.stats),Bt(e),Jt(e.statuses),Ci(),Er(e.statuses),Or(e.statuses)}function cn(e){wt=e??null;let t=!!e?.scanning,n=t&&!!e?.cancel_requested,r=Number(e?.completed_companies??0),i=Number(e?.total_companies??0),a=Number(e?.failed_companies??0),o=typeof e?.error==`string`?e.error.trim():``,s=Array.isArray(e?.failures)?e.failures:[];_.disabled=n,_.textContent=t?n?`cancelling...`:`cancel scan`:`scan roles`,_.classList.toggle(`danger`,t&&!n),v.hidden=!t&&!o&&s.length===0,v.classList.toggle(`scanning`,t),v.classList.toggle(`scan-error`,!t&&!!o||s.length>0),y.textContent=n?`cancelling scan...`:t?`scanning roles${i>0?` ${r}/${i}`:``}${a>0?`, ${a} failed`:``}`:s.length>0?`${s.length} recent scan ${s.length===1?`failure`:`failures`}`:o?`last scan error: ${o}`:`scan idle`,Oe&&(Oe.hidden=s.length===0,Oe.innerHTML=s.slice(0,5).map(e=>{let t=e?.company_name||`unknown company`,n=e?.error||`scan failed`;return`
          <p>
            <span>${H(t)}</span>
            <span>${B(n)}</span>
          </p>
        `}).join(``));let c=e?.last_scan_at;De.textContent=c?`last scan: ${z(c)}`:`last scan: never`,Ct&&!t&&J(R()).catch(()=>{}),Ct=t}function G(e,t=``){Tt=e;let n=Array.isArray(e?.settings)?e.settings:[],r=n.filter(e=>e.key?.startsWith(`applicant_`)),i=n.filter(e=>!e.key?.startsWith(`applicant_`)),a=e?.central??{};b.textContent=t,b.classList.toggle(`is-empty`,!t);let o=Number(e?.recommendation_history_count??0);He.textContent=o>0?`${o} saved ${o===1?`feedback decision`:`feedback decisions`}`:`no saved resume feedback decisions`,Ue.disabled=o===0,ln(a),Ie.innerHTML=r.map(e=>un(e)).join(``),Le.innerHTML=i.map(e=>un(e)).join(``),K(!1)}function ln(e){let t=e?.api_url??``;x.value=t,Be.value=``;let n=e?.passkey_configured?`passkey saved`:`no passkey saved`;Re.textContent=t?`${V(t)} | ${n}`:`no api url | ${n}`,ze.textContent=`${Number(e?.companies_linked??0)} linked | ${Number(e?.companies_unlinked??0)} unlinked | ${Number(e?.companies_needs_review??0)} review | ${Number(e?.companies_failed??0)} failed`,S.disabled=!t}function un(e){if(e.control===`text`&&e.editable!==!1)return dn(e);if(e.control===`select`&&e.editable!==!1)return fn(e);if(e.control!==`toggle`||e.editable===!1)return pn(e);let t=e.value?`checked`:``,n=e.default?`on by default`:`off by default`;return`
    <label class="setting-option">
      <span class="setting-copy">
        <span class="setting-label">${H(e.label)}</span>
        <span class="setting-description">${H(e.description)}</span>
        <span class="setting-default">${H(n)}</span>
      </span>
      <span class="setting-switch">
        <input type="checkbox" name="${B(e.key)}" ${t} />
        <span aria-hidden="true"></span>
      </span>
    </label>
  `}function dn(e){let t=e.default?`default: ${V(e.default)}`:`optional`,n=e.input_type??`text`,r=e.autocomplete??`name`;return`
    <label class="setting-option">
      <span class="setting-copy">
        <span class="setting-label">${H(e.label)}</span>
        <span class="setting-description">${H(e.description)}</span>
        <span class="setting-default">${H(t)}</span>
      </span>
      <input
        class="setting-text-input"
        data-setting-text
        name="${B(e.key)}"
        type="${B(n)}"
        value="${B(e.value??``)}"
        autocomplete="${B(r)}"
      />
    </label>
  `}function fn(e){let t=Array.isArray(e.options)?e.options:[],n=`default: ${V(e.default)}`;return`
    <label class="setting-option">
      <span class="setting-copy">
        <span class="setting-label">${H(e.label)}</span>
        <span class="setting-description">${H(e.description)}</span>
        <span class="setting-default">${H(n)}</span>
      </span>
      <select class="setting-select" name="${B(e.key)}">
        ${t.map(t=>{let n=t.value===e.value?`selected`:``;return`<option value="${B(t.value)}" ${n}>${H(t.label)}</option>`}).join(``)}
      </select>
    </label>
  `}function pn(e){let t=e.default?`on by default`:`off by default`,n=e.value?`automatic`:`off`;return`
    <div class="setting-option setting-option-readonly">
      <span class="setting-copy">
        <span class="setting-label">${H(e.label)}</span>
        <span class="setting-description">${H(e.description)}</span>
        <span class="setting-default">${H(t)}</span>
      </span>
      <span class="setting-badge">${H(n)}</span>
    </div>
  `}function K(e){Fe.querySelectorAll(`input, select`).forEach(t=>{t.disabled=e}),Ve.disabled=e,S.disabled=e||!x.value.trim(),tt.disabled=e}async function mn(){Ne.hidden=!1,document.body.classList.add(`settings-open`),Pe.focus(),Tt?G(Tt):(b.textContent=`loading settings...`,b.classList.remove(`is-empty`),Le.innerHTML=``);try{await gn()}catch{b.textContent=`could not load settings.`}}function hn(){Ne.hidden=!0,document.body.classList.remove(`settings-open`),Me.focus()}async function gn(){let e=await fetch(`/api/config`);if(!e.ok)throw Error(`Config request failed`);G(await e.json())}function _n(e){let t=e?.value;return t==null?`n/a`:e?.kind===`ratio`?Number(t).toLocaleString(void 0,{maximumFractionDigits:2,minimumFractionDigits:0}):typeof t==`number`?t.toLocaleString():V(t)}function vn(e,t=`metric-card`){return`
    <article class="${t}">
      <span>${H(e?.label)}</span>
      <strong>${B(_n(e))}</strong>
    </article>
  `}function yn(e,t=``){Et=e,C.textContent=t||(e?.updated_at?`updated ${z(e.updated_at)}`:``),C.classList.toggle(`is-empty`,!C.textContent);let n=Array.isArray(e?.overview)?e.overview:[],r=Array.isArray(e?.sections)?e.sections:[],i=Array.isArray(e?.recent_scans)?e.recent_scans:[];qe.innerHTML=n.map(e=>vn(e)).join(``),Je.innerHTML=r.map(bn).join(``),Ye.innerHTML=i.length?i.map(xn).join(``):`<p class="empty-copy">no scan runs recorded.</p>`}function bn(e){let t=Array.isArray(e?.metrics)?e.metrics:[];return`
    <section class="metrics-section">
      <div class="metrics-section-heading">
        <h3>${H(e?.title)}</h3>
      </div>
      <div class="metrics-section-grid">
        ${t.map(e=>vn(e,`metric-card metric-card-compact`)).join(``)}
      </div>
    </section>
  `}function xn(e){let t=e?.scan_status??`unknown`,n=e?.started_at?z(e.started_at):`not started`,r=e?.finished_at?z(e.finished_at):`not finished`,i=e?.error?`<span>${H(e.error)}</span>`:``;return`
    <article class="metrics-scan-row">
      <div>
        <strong>${H(e?.company_name??`unknown company`)}</strong>
        <span>${H(n)} -> ${H(r)}</span>
        ${i}
      </div>
      <span class="metrics-status-pill">${H(t)}</span>
    </article>
  `}async function Sn(){Ge.hidden=!1,document.body.classList.add(`metrics-open`),Ke.focus(),Et?yn(Et):(C.textContent=`loading metrics...`,C.classList.remove(`is-empty`),qe.innerHTML=``,Je.innerHTML=``,Ye.innerHTML=``);try{await wn()}catch{C.textContent=`could not load metrics.`}}function Cn(){Ge.hidden=!0,document.body.classList.remove(`metrics-open`),We.focus()}async function wn(){let e=await fetch(`/api/metrics`);if(!e.ok)throw Error(`Metrics request failed`);yn(await e.json())}function Tn(e,t=``){Dt=e;let n=Number(e?.role_count??0),r=Array.isArray(e?.links)?e.links:[],i=Array.isArray(e?.paths)?e.paths:[];w.textContent=t||(e?.updated_at?`${n.toLocaleString()} roles | updated ${z(e.updated_at)}`:``),w.classList.toggle(`is-empty`,!w.textContent),$e.innerHTML=r.length?En(e):`<p class="empty-copy">no role transitions recorded yet.</p>`,et.innerHTML=i.length?i.map(An).join(``):`<p class="empty-copy">no role paths recorded yet.</p>`}function En(e){let t=Array.isArray(e?.nodes)?e.nodes:[],n=Array.isArray(e?.links)?e.links:[],r=kn(t,n),i=r.nodes,a=r.links,o=(r.flowLinks??n).map(e=>{let t=i.get(e.source),n=i.get(e.target),r=a.get(e);if(!t||!n||!r)return``;let o=r.width,s=n.x<t.x,c=Dn(e.target),l=r.priority?`0.42`:s?`0.28`:`0.34`,u=r.path??On({isBacktrack:s,sourceX:t.x+t.width,sourceY:r.sourceY,targetX:n.x,targetY:r.targetY,width:o});return`
        <path class="${[`sankey-link`,s?`sankey-link-backtrack`:``,r.priority?`sankey-link-priority`:``].filter(Boolean).join(` `)}" d="${u}" fill="${r.path?`none`:c}" fill-opacity="${l}" stroke="${c}" style="stroke-width: ${r.path?o:1}px">
          <title>${H(t.label)} to ${H(n.label)}: ${Number(e.value??0).toLocaleString()}</title>
        </path>
      `}).join(``),s=Array.from(i.values()).map(e=>{let t=Number(e.history_count??e.current_count??0),n=Number(e.value??t),i=n>0?n.toLocaleString():`0`,a=e.x>r.width-180,o=a?e.x-8:e.x+e.width+8,s=Math.max(24,e.y-e.height/2-16),c=a?`end`:`start`,l=Dn(e.id);return`
        <g class="sankey-node" transform="translate(${e.x}, ${e.y-e.height/2})">
          <rect width="${e.width}" height="${e.height}" rx="7" fill="${l}" stroke="${l}"></rect>
        </g>
        <g class="sankey-node-label" transform="translate(${o}, ${s})">
          <text text-anchor="${c}">${H(e.label)}</text>
          <text class="sankey-node-count" y="16" text-anchor="${c}">${H(i)} roles</text>
        </g>
      `}).join(``);return`
    <svg class="sankey-svg" viewBox="0 0 ${r.width} ${r.height}" role="img" aria-label="role state transition sankey diagram">
      <g>${o}</g>
      <g>${s}</g>
    </svg>
  `}function Dn(e){return pt.get(String(e).toLowerCase())??`#4f6472`}function On({isBacktrack:e,sourceX:t,sourceY:n,targetX:r,targetY:i,width:a}){let o=a/2,s=n-o,c=n+o,l=i-o,u=i+o;if(e){let e=Math.max(80,Math.abs(t-r)*.42);return[`M ${t} ${s}`,`C ${t-e} ${s}, ${r+e} ${l}, ${r} ${l}`,`L ${r} ${u}`,`C ${r+e} ${u}, ${t-e} ${c}, ${t} ${c}`,`Z`].join(` `)}let d=Math.max(46,(r-t)*.48);return[`M ${t} ${s}`,`C ${t+d} ${s}, ${r-d} ${l}, ${r} ${l}`,`L ${r} ${u}`,`C ${r-d} ${u}, ${t+d} ${c}, ${t} ${c}`,`Z`].join(` `)}function kn(e,r){let i=new Map([[`discovered`,0],[`interested`,1],[`disinterested`,2],[`applied`,2],[`oa`,3],[`interview`,3],[`rejected`,4],[`closed`,4],[`archived`,4]]),a=new Map,o=new Map;r.forEach(e=>{a.set(e.target,(a.get(e.target)??0)+Number(e.value??0)),o.set(e.source,(o.get(e.source)??0)+Number(e.value??0))});let s=e.filter(e=>Number(e?.history_count??e?.current_count??0)>0||a.has(e.id)||o.has(e.id)),c=new Set(s.map(e=>e.id)),l=r.filter(e=>c.has(e.source)&&c.has(e.target)&&Number(e.value??0)>0),u=e=>i.get(String(e).toLowerCase())??0,d=l.filter(e=>u(e.target)>=u(e.source)),ee=l.filter(e=>u(e.target)<u(e.source)),te={nodes:s.map(e=>({...e,fixedValue:Math.max(0,Number(e?.history_count??e?.current_count??0))})),links:d.map(e=>({...e}))},ne=t().nodeId(e=>e.id).nodeWidth(26).nodePadding(44).nodeAlign((e,t)=>Math.min(t-1,u(e.id))).extent([[92,88],[1014,634]]).iterations(32)(te),re=new Map;ne.nodes.forEach(e=>{re.set(e.id,{...e,x:e.x0,y:e.y0+(e.y1-e.y0)/2,width:e.x1-e.x0,height:Math.max(1.5,e.y1-e.y0),value:Number(e.fixedValue??e.value??0)})});let f=new Map,p=[],ie=n();ne.links.forEach(e=>{let t={source:e.source.id,target:e.target.id,value:e.value};p.push(t),f.set(t,{path:ie(e),width:Math.max(1.5,e.width),sourceY:e.y0,targetY:e.y1,priority:Number(e.value??0)>=20})});let ae=Math.max(.6,...ne.links.map(e=>Number(e.width??0)/Math.max(1,Number(e.value??0))));return ee.forEach(e=>{let t=re.get(e.source),n=re.get(e.target);if(!t||!n)return;let r=Math.max(1.5,Number(e.value??0)*ae),i={...e};p.push(i),f.set(i,{width:r,sourceY:t.y+t.height/2-r/2,targetY:n.y+n.height/2-r/2,priority:!1})}),p.sort((e,t)=>Number(e.value??0)-Number(t.value??0)),{flowLinks:p,height:720,links:f,nodes:re,width:1120}}function An(e){let t=Array.isArray(e?.path)?e.path:[];return`
    <article class="sankey-path-row">
      <div>
        <strong>${H(e?.company_name??`unknown company`)} / ${H(e?.title??`untitled role`)}</strong>
        <span>${t.map(e=>H(e)).join(` -> `)}</span>
      </div>
      <span class="metrics-status-pill">${Number(e?.loops_collapsed??0).toLocaleString()} loops</span>
    </article>
  `}async function jn(){Ne.hidden=!0,document.body.classList.remove(`settings-open`),Ze.hidden=!1,document.body.classList.add(`sankey-open`),Qe.focus(),Dt?Tn(Dt):(w.textContent=`loading role flow...`,w.classList.remove(`is-empty`),$e.innerHTML=``,et.innerHTML=``);try{await Nn()}catch{w.textContent=`could not load role flow.`}}function Mn(){Ze.hidden=!0,document.body.classList.remove(`sankey-open`),Me.focus()}async function Nn(){let e=await fetch(`/api/role-sankey`);if(!e.ok)throw Error(`Role sankey request failed`);Tn(await e.json())}async function Pn(e){let t=e.name;if(!t)return;let n=e.type===`checkbox`?!e.checked:Tt?.settings?.find(e=>e.key===t)?.value,r=e.type===`checkbox`?e.checked:e.value;K(!0),b.textContent=`saving settings...`,b.classList.remove(`is-empty`);try{let e=await fetch(`/api/config`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({[t]:r})});if(!e.ok)throw Error(`Config update failed`);G(await e.json(),`settings saved.`)}catch{e.type===`checkbox`?e.checked=n:n!==void 0&&(e.value=n),b.textContent=`could not save settings.`,K(!1)}}async function Fn(){Ue.disabled=!0,b.textContent=`clearing recommendation history...`,b.classList.remove(`is-empty`);try{let e=await fetch(`/api/recommendation-history/clear`,{method:`POST`});if(!e.ok)throw Error(`Recommendation history clear failed`);let t=await e.json();G(t.config,`cleared ${t.deleted_count} saved decisions.`)}catch{b.textContent=`could not clear recommendation history.`,Ue.disabled=!1}}async function In(){let e=x.value.trim();if(!e){b.textContent=`central api url is required.`,b.classList.remove(`is-empty`);return}let t={central_api_url:e},n=Be.value.trim();n&&(t.central_passkey=n),K(!0),b.textContent=`saving central settings...`,b.classList.remove(`is-empty`);try{let e=await fetch(`/api/config`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(t)});if(!e.ok)throw Error(`Central settings update failed`);G(await e.json(),`central settings saved.`)}catch{b.textContent=`could not save central settings.`,K(!1)}}async function Ln(){S.disabled=!0,b.textContent=`syncing remote company ids...`,b.classList.remove(`is-empty`);try{let e=await fetch(`/api/central/resolve-companies`,{method:`POST`});if(!e.ok)throw Error(`Central company sync failed`);let t=await e.json(),n=t.result??{},r=t.pulled_companies,i=r?` remote: ${Number(r.created??0)} created, ${Number(r.linked??0)} linked, ${Number(r.existing??0)} existing.`:``;G(t.config,`company sync: ${Number(n.linked??0)} matched, ${Number(n.created??0)} created, ${Number(n.needs_review??0)} review, ${Number(n.failed??0)} failed.${i}`),t.companies&&(L=t.companies,Vn(t.companies.companies))}catch{b.textContent=`could not sync companies.`,S.disabled=!x.value.trim()}}async function Rn(){let e=await fetch(`/api/central/resolve-companies`,{method:`POST`});if(!e.ok)throw Error(`Central company sync failed`);let t=await e.json();t.companies&&(L=t.companies,Vn(t.companies.companies))}async function zn(){await Rn().catch(()=>{}),await Promise.all([J().catch(()=>{i.innerHTML=`<p class="empty-copy">could not load jobs.</p>`}),Yn().catch(()=>{lt.textContent=`could not load companies.`})])}async function Bn(){if(window.confirm(`Update callumployed and restart the tracker?`)){K(!0),tt.disabled=!0,b.textContent=`updating callumployed; tracker will restart shortly...`,b.classList.remove(`is-empty`);try{if(!(await fetch(`/api/app/update`,{method:`POST`})).ok)throw Error(`App update failed`);b.textContent=`update started. reconnect in a moment.`}catch{b.textContent=`could not start update.`,K(!1)}}}function q(e,t=``){L=e;let n=Array.isArray(e?.companies)?e.companies:[];if(Vn(n),T.textContent=t||`${n.length} ${n.length===1?`company`:`companies`} stored`,T.classList.toggle(`is-empty`,n.length===0&&!t),n.length===0){E.innerHTML=`<p class="empty-copy">no companies yet.</p>`;return}E.innerHTML=n.map(e=>Hn(e)).join(``)}function Vn(e){Ot=Array.isArray(e)?e:[],ct.innerHTML=Ot.map(e=>`<option value="${B(e.name)}"></option>`).join(``)}function Hn(e){let t=Array.isArray(e.career_pages)?e.career_pages:[],n=z(e.updated_at),r=Un(e.prestige_tier),i=Number(e.scan_count??0),a=Number(e.discovered_role_count??0),o=i>0&&a===0?`<span class="company-discovery-status">Discovered 0 potential roles</span>`:``;return`
    <details class="company-panel ${r}" data-company-id="${e.id}">
      <summary class="company-summary">
        <span class="company-chevron">></span>
        <span class="company-summary-main">
          <span class="company-name">${H(e.name)}</span>
          <span class="company-summary-meta">${t.length} ${t.length===1?`link`:`links`}${n?` | updated ${H(n)}`:``}</span>
          ${o}
        </span>
      </summary>
      <div class="company-body">
        <div class="company-info">
          <label class="company-notes-field">
            <span>notes</span>
            <textarea data-company-notes="${e.id}" rows="3">${B(e.notes??``)}</textarea>
          </label>
          <label>
            <span>tier</span>
            <select data-company-tier="${e.id}">
              ${Wn(e.prestige_tier)}
            </select>
          </label>
          <div>
            <span>browser wait</span>
            <strong>${Number(e.browser_extra_wait_ms??0)}ms</strong>
          </div>
        </div>
        <div class="company-links">
          ${t.length>0?t.map(e=>Gn(e)).join(``):`<p class="company-empty-links">no career links yet.</p>`}
        </div>
        <section class="company-link-panel" aria-label="add career link">
          <form class="company-link-form" data-company-link-form="${e.id}">
            <input name="label" type="text" placeholder="label" aria-label="career link label" />
            <input name="url" type="url" placeholder="https://..." aria-label="career link url" required />
            <button class="company-link-add" type="submit" aria-label="add career link" title="add career link">
              ${It()}
            </button>
          </form>
        </section>
        <div class="company-danger-row">
          <button class="company-delete-button" type="button" data-delete-company="${e.id}">
            ${Lt()}
            <span>deactivate company</span>
          </button>
        </div>
      </div>
    </details>
  `}function Un(e){let t=String(e??``);return[`0`,`1`,`2`,`3`,`4`].includes(t)?`company-tier-${t}`:`company-tier-unset`}function Wn(e){let t=String(e??``);return[``,`0`,`1`,`2`,`3`,`4`].map(e=>{let n=e?`tier ${e}`:`not set`,r=e===t?` selected`:``;return`<option value="${B(e)}"${r}>${H(n)}</option>`}).join(``)}function Gn(e){let t=e.label?H(e.label):`career page`,n=B(e.url);return`
    <div class="company-link-row" data-career-page-id="${e.id}">
      <a class="company-link-url" href="${n}" target="_blank" rel="noreferrer">
        <span class="company-link-label">${t}</span>
        <span class="company-link-text">${B(e.url)}</span>
      </a>
      <button class="company-link-delete" type="button" data-delete-career-page="${e.id}" aria-label="delete ${t} link" title="delete link">
        ${Lt()}
      </button>
    </div>
  `}async function Kn(){nt.hidden=!1,document.body.classList.add(`companies-open`),rt.focus(),L?q(L):(T.textContent=`loading companies...`,T.classList.remove(`is-empty`),E.innerHTML=``);try{await Jn()}catch{T.textContent=`could not load companies.`}}function qn(){nt.hidden=!0,document.body.classList.remove(`companies-open`),Ee.focus()}async function Jn(e=``){let t=await fetch(`/api/companies`);if(!t.ok)throw Error(`Companies request failed`);q(await t.json(),e)}async function Yn(){let e=await fetch(`/api/companies`);if(!e.ok)throw Error(`Companies request failed`);Vn((await e.json()).companies)}async function Xn(e){let t=new FormData(e),n={name:String(t.get(`name`)??``),career_url:String(t.get(`career_url`)??``),notes:String(t.get(`notes`)??``)};T.textContent=`adding company...`;let r=await fetch(`/api/companies`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(n)});if(!r.ok)throw Error(`Company create failed`);e.reset(),q(await r.json(),`company added.`),J(R()).catch(()=>{})}async function Zn(e){let t=e.dataset.companyLinkForm;if(!t)return;let n=new FormData(e),r={label:String(n.get(`label`)??``),url:String(n.get(`url`)??``)};T.textContent=`adding link...`;let i=await fetch(`/api/companies/${encodeURIComponent(t)}/career-pages`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(r)});if(!i.ok)throw Error(`Career page create failed`);e.reset(),q(await i.json(),`link added.`)}async function Qn(e){T.textContent=`deleting link...`;let t=await fetch(`/api/company-career-pages/${encodeURIComponent(e)}`,{method:`DELETE`});if(!t.ok)throw Error(`Career page delete failed`);q(await t.json(),`link deleted.`)}async function $n(e){T.textContent=`deactivating company...`;let t=await fetch(`/api/companies/${encodeURIComponent(e)}`,{method:`DELETE`});if(!t.ok)throw Error(`Company deactivate failed`);q(await t.json(),`company deactivated.`),J(R()).catch(()=>{})}function er(){let e=st.value.trim().toLocaleLowerCase();return Ot.find(t=>t.name.toLocaleLowerCase()===e)}async function tr(e){let t=er();if(!t?.id){lt.textContent=`pick a saved company.`;return}let n=new FormData(e),r={company_id:t.id,role_url:String(n.get(`role_url`)??``)};lt.textContent=`adding role...`;let i=await fetch(`/api/roles`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(r)});if(!i.ok)throw Error(`Role create failed`);let a=await i.json();a.tracker?sn(a.tracker):await J(R()),ot.value=``;let o=a.role?.title?V(a.role.title):`role`;lt.textContent=a.scan_error?`${o} added; scan could not finish.`:`${o} added.`}function nr(e){return(Array.isArray(L?.companies)?L.companies:[]).find(t=>String(t.id)===String(e))}function rr(e){T.textContent=e,T.classList.remove(`is-empty`)}function ir(e){window.clearTimeout(kt.get(e)),kt.set(e,window.setTimeout(()=>{ar(e).catch(()=>{rr(`could not save company.`)})},700))}async function ar(e){let t=E.querySelector(`[data-company-id="${CSS.escape(String(e))}"]`);if(!t)return;let n=t.querySelector(`[data-company-notes="${CSS.escape(String(e))}"]`),r=t.querySelector(`[data-company-tier="${CSS.escape(String(e))}"]`),i=nr(e),a={notes:n?.value??i?.notes??``,prestige_tier:r?.value??i?.prestige_tier??``};i&&(i.notes=a.notes,i.prestige_tier=a.prestige_tier),or(t,a.prestige_tier),rr(`saving company...`);let o=await fetch(`/api/companies/${encodeURIComponent(e)}`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(a)});if(!o.ok)throw Error(`Company update failed`);L=await o.json(),rr(`company saved.`),sr(e)}function or(e,t){e.classList.remove(`company-tier-unset`,`company-tier-0`,`company-tier-1`,`company-tier-2`,`company-tier-3`,`company-tier-4`),e.classList.add(Un(t))}function sr(e){let t=E.querySelector(`[data-company-id="${CSS.escape(String(e))}"]`),n=nr(e);if(!t||!n)return;let r=Array.isArray(n.career_pages)?n.career_pages:[],i=z(n.updated_at),a=t.querySelector(`.company-summary-meta`);a&&(a.textContent=`${r.length} ${r.length===1?`link`:`links`}${i?` | updated ${i}`:``}`)}async function cr(){let e=await fetch(`/api/scan/status`);if(e.status===404){_.disabled=!0,v.hidden=!0,v.classList.add(`scan-error`),y.textContent=`restart server to enable scanning`;return}if(!e.ok)throw Error(`Scan status request failed`);cn(await e.json())}function lr(){St===null&&(St=window.setInterval(()=>{cr().catch(()=>{})},3e3))}async function ur(){_.disabled=!0,_.textContent=`starting...`;try{let e=await fetch(`/api/scan/all`,{method:`POST`});if(e.status===404){_.disabled=!0,_.textContent=`scan roles`,v.hidden=!0,v.classList.add(`scan-error`),y.textContent=`restart server to enable scanning`;return}if(!e.ok&&e.status!==409)throw Error(`Scan start failed`);cn(await e.json()),lr()}catch{_.disabled=!1,_.textContent=`scan roles`,v.hidden=!0,v.classList.add(`scan-error`),y.textContent=`could not start scan`}}async function dr(){_.disabled=!0,_.textContent=`cancelling...`;try{let e=await fetch(`/api/scan/cancel`,{method:`POST`});if(e.status===404){_.disabled=!0,_.textContent=`scan roles`,v.hidden=!0,v.classList.add(`scan-error`),y.textContent=`restart server to enable scanning`;return}if(!e.ok&&e.status!==409)throw Error(`Scan cancel failed`);cn(await e.json()),lr()}catch{_.disabled=!1,_.textContent=`cancel scan`,v.hidden=!1,v.classList.add(`scan-error`),y.textContent=`could not cancel scan`}}async function J(e=``){i.innerHTML=`<p class="empty-copy">loading jobs...</p>`;let t=new URLSearchParams;e&&t.set(`q`,e);let n=await fetch(`/api/tracker?${t.toString()}`);if(!n.ok)throw Error(`Tracker request failed`);sn(await n.json())}async function fr(e={}){let t=await fetch(`/api/application-materials`);if(!t.ok)throw Error(`Application materials request failed`);Gt(await t.json(),e)}async function pr(e){if(e){if(!e.name.toLowerCase().endsWith(`.tex`)){Vt(O,`resume must be a .tex file.`);return}ie.disabled=!0,Vt(O,`uploading...`);try{let t=await e.text();if(!(await fetch(`/api/master-resume`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({filename:e.name,content:t})})).ok)throw Error(`Master resume upload failed`);await fr()}catch{Vt(O,`could not save resume.`),W()}finally{p.value=``,ie.disabled=!1}}}async function mr(e){let t=Array.from(e??[]);if(t.length!==0){se.disabled=!0,Wt(k,`uploading ${t.length} ${t.length===1?`resource`:`resources`}...`);try{for(let e of t)if(!(await fetch(`/api/resume-resources`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({filename:e.name,content_base64:await _r(e)})})).ok)throw Error(`Resume resource upload failed`);await fr()}catch{Wt(k,`could not save every resource.`),W()}finally{oe.value=``,se.disabled=!1}}}async function hr(e){let t=Array.from(e??[]);if(t.length!==0){de.disabled=!0,Ht(A,`uploading ${t.length} ${t.length===1?`example`:`examples`}...`);try{for(let e of t){let t={filename:e.name};if(e.name.toLowerCase().endsWith(`.docx`)?t.content_base64=await _r(e):t.content=await e.text(),!(await fetch(`/api/cover-letter-examples`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(t)})).ok)throw Error(`Cover letter example upload failed`)}await fr()}catch{Ht(A,`could not save every example.`),W()}finally{ue.value=``,de.disabled=!1}}}async function gr(e){let t=Array.from(e??[]);if(t.length!==0){he.disabled=!0,Ut(j,`uploading ${t.length} ${t.length===1?`note`:`notes`}...`);try{for(let e of t)if(!(await fetch(`/api/experience-notes`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({filename:e.name,content:await e.text()})})).ok)throw Error(`Experience note upload failed`);P.clear(),await fr()}catch{Ut(j,`could not save every note.`),W()}finally{me.value=``,he.disabled=!1}}}function _r(e){return new Promise((t,n)=>{let r=new FileReader;r.addEventListener(`load`,()=>{let e=String(r.result??``);t(e.includes(`,`)?e.split(`,`,2)[1]:e)}),r.addEventListener(`error`,()=>n(r.error)),r.readAsDataURL(e)})}c.addEventListener(`submit`,e=>{e.preventDefault(),J(l.value.trim()),Mt()}),a.addEventListener(`click`,()=>{if(R()){J();return}jt()}),l.addEventListener(`keydown`,e=>{e.key===`Escape`&&(e.stopPropagation(),Mt())}),u.addEventListener(`click`,Mt),s.addEventListener(`click`,Mt),ie.addEventListener(`click`,()=>{p.click()}),p.addEventListener(`change`,()=>{pr(p.files?.[0])}),se.addEventListener(`click`,()=>{oe.click()}),oe.addEventListener(`change`,()=>{mr(oe.files)}),de.addEventListener(`click`,()=>{ue.click()}),ue.addEventListener(`change`,()=>{hr(ue.files)}),he.addEventListener(`click`,()=>{me.click()}),me.addEventListener(`change`,()=>{gr(me.files)}),ee.addEventListener(`click`,()=>{Kt(ee.getAttribute(`aria-expanded`)===`true`)}),_.addEventListener(`click`,()=>{if(wt?.scanning){if(!window.confirm(`Cancel the running scan?`))return;dr();return}ur()}),i.addEventListener(`click`,e=>{let t=e.target.closest(`[data-review-role-id]`);if(t){Ar(t.dataset.reviewRoleId);return}let n=e.target.closest(`[data-prep-role-id]`);if(n){Mr(n.dataset.prepRoleId);return}let r=e.target.closest(`.job-action`);if(r){vr(r);return}let i=e.target.closest(`.pane-toggle`);if(!i)return;let a=i.parentElement.querySelector(`.pane-body`),o=i.getAttribute(`aria-expanded`)===`true`;i.setAttribute(`aria-expanded`,String(!o)),i.querySelector(`.chevron`).textContent=o?`>`:`v`,a.hidden=o,Ci()});async function vr(e){let{roleId:t,status:n}=e.dataset;if(!t||!n)return;let r=e.closest(`.job-actions`),i=e.closest(`.job`);r.querySelectorAll(`button`).forEach(e=>{e.disabled=!0}),e.textContent=`updating...`;try{let e=await fetch(`/api/roles/${encodeURIComponent(t)}/status`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({status:n})});if(!e.ok)throw Error(`Status update failed`);yr((await e.json()).role,i)}catch{r.querySelectorAll(`button`).forEach(e=>{e.disabled=!1}),e.textContent=n===`disinterested`?`disinterested`:n.toLowerCase()}}function yr(e,t){if(!e||!D)return;let n=t?.closest(`.status-pane`)?.dataset.bucket??e.role_status,r=e.role_status,i=xr(e,n,r);Sr(n,r),Cr(n,r),Bt(),Er(D.statuses),Or(D.statuses),wr(t,i,n,r),Ci()}function br(e){if(!e||!D)return null;let t=null;return D.statuses.forEach(n=>{let r=n.jobs.findIndex(t=>String(t.id)===String(e.id));r!==-1&&(t={...n.jobs[r],...e},n.jobs[r]=t)}),Er(D.statuses),Or(D.statuses),t}function xr(e,t,n){let r=e;D.statuses.forEach(t=>{let n=t.jobs.findIndex(t=>String(t.id)===String(e.id));n!==-1&&(r={...t.jobs[n],...e},t.jobs.splice(n,1),t.count=t.jobs.length)});let i=D.statuses.find(e=>e.key===n);return i&&(i.jobs.unshift(r),i.count=i.jobs.length),r}function Sr(e,t){D.statuses.forEach(e=>{let t=document.querySelector(`#status-${CSS.escape(e.key)}`);t?.classList.toggle(`empty`,e.count===0);let n=t?.querySelector(`.count`);n&&(n.textContent=e.count)}),[e,t].forEach(e=>{Tr(document.querySelector(`#status-${CSS.escape(e)}`))})}function Cr(e,t){if(!D.stats)return;let n=ft.has(e),r=ft.has(t);if(n===r){zt(D.stats);return}D.stats.applications_total=Number(D.stats.applications_total??0)+(r?1:-1),zt(D.stats)}function wr(e,t,n,r){let i=document.querySelector(`#status-${CSS.escape(r)}`),a=i?.querySelector(`.pane-body`);if(!e||!i||!a)return;e.remove(),Tr(document.querySelector(`#status-${CSS.escape(n)}`)),a.hidden=!1;let o=i.querySelector(`.pane-toggle`);o?.setAttribute(`aria-expanded`,`true`);let s=o?.querySelector(`.chevron`);s&&(s.textContent=`v`);let c=a.querySelector(`.jobs`);c||=(a.innerHTML=`<div class="jobs"></div>`,a.querySelector(`.jobs`)),c.insertAdjacentHTML(`afterbegin`,Yt(t,r)),Tr(i)}function Tr(e){if(!e)return;let t=e.querySelector(`.pane-body`);if(!t)return;let n=t.querySelector(`.jobs`),r=!!n?.querySelector(`.job`),i=t.querySelector(`.empty-copy`);if(r){i?.remove();return}n?.remove(),i||t.insertAdjacentHTML(`beforeend`,`<p class="empty-copy">no jobs in this status.</p>`)}function Er(e){_e.disabled=Dr(e).length===0,_e.setAttribute(`aria-label`,`review discovered`),_e.innerHTML=`<span class="review-discovered-label">review discovered</span>`}function Dr(e=D?.statuses??[]){return e.find(e=>e.key===`discovered`)?.jobs??[]}function Or(e){ve.disabled=kr(e).length===0,ve.setAttribute(`aria-label`,`prep interested`),ve.innerHTML=`<span class="review-discovered-label">prep interested</span>`}function kr(e=D?.statuses??[]){return e.find(e=>e.key===`interested`)?.jobs??[]}function Ar(e=null){let t=[...Dr()],n=e==null?null:String(e);if(n){let e=t.findIndex(e=>String(e.id)===n);if(e>0){let[n]=t.splice(e,1);t.unshift(n)}}M=t,m.hidden=!1,document.body.classList.add(`review-open`),Pr()}function jr(){m.hidden=!0,document.body.classList.remove(`review-open`),M=[]}function Mr(e=null){let t=[...kr()].sort((e,t)=>Number(!!t.prep_started)-Number(!!e.prep_started)),n=e==null?null:String(e);if(n){let e=t.findIndex(e=>String(e.id)===n);if(e>0){let[n]=t.splice(e,1);t.unshift(n)}}N=t,h.hidden=!1,document.body.classList.add(`prep-open`),Z()}function Nr(){h.hidden=!0,document.body.classList.remove(`prep-open`),N=[]}function Pr(e=``){let t=M[0],n=M.length,r=t?Fr(t):``;if(ye.textContent=n>0?`review queue`:`review complete`,be.textContent=n>0?`${n} discovered ${n===1?`role`:`roles`} in queue`:``,m.querySelectorAll(`.review-action`).forEach(e=>{e.disabled=n===0}),!t){xe.innerHTML=`
      <div class="review-empty">
        <h3>no discovered jobs left.</h3>
        <p>everything in this queue has been handled or moved out of discovered.</p>
      </div>
    `;return}xe.innerHTML=`
    ${e?`<p class="review-message">${B(e)}</p>`:``}
    ${r?`<p class="review-message review-message-warning">${B(r)}</p>`:``}
    <div class="review-title-row">
      <p class="review-company">${H(t.company_name)}</p>
      ${Rt(t.title,t.role_url,`review-role-title`)}
    </div>
    <dl class="review-details review-primary-details">
      ${Y(`location`,t.location,!1,`review-location-detail`)}
      ${Y(`first`,z(t.first_seen_at))}
      ${Y(`last`,z(t.last_seen_at))}
    </dl>
    ${Ir(t.description)}
    <dl class="review-details review-technical-details">
      ${Y(`notes`,t.notes,!1,`review-wide-detail`)}
      ${Y(`company id`,t.company_id)}
      ${Y(`role id`,t.id)}
      ${Y(`status`,t.role_status)}
      ${Y(`posting id`,t.posting_id)}
      ${Y(`created`,z(t.created_at))}
      ${Y(`updated`,z(t.updated_at))}
      ${Y(`url`,t.role_url,!0,`review-wide-detail`)}
    </dl>
  `}function Fr(e){let t=Number(e.review_later_count??0);return t<=ut?``:`role review has been postponed ${t} times. it is recommended to set it to disinterested.`}function Y(e,t,n=!1,r=``){if(!t)return``;let i=n?`<a href="${B(t)}" target="_blank" rel="noreferrer">${H(t)}</a>`:H(t);return`
    <div class="review-detail ${B(r)}">
      <dt>${H(e)}</dt>
      <dd>${i}</dd>
    </div>
  `}function Ir(e){return e?`
    <div class="review-detail review-description">
      <dt>description</dt>
      <dd>${Lr(e)}</dd>
    </div>
  `:``}function Lr(e){let t=Rr(String(e)).replace(/\u00a0/g,` `);if(zr(t))return Br(t);let n=t.split(/\r?\n/).map(e=>e.trim()).filter(Boolean),r=[],i=[],a=()=>{i.length!==0&&(r.push(`<ul>${i.map(e=>`<li>${e}</li>`).join(``)}</ul>`),i=[])};return n.forEach(e=>{let t=e.match(/^#{2,3}\s+(.+)$/);if(t){a(),r.push(`<h3>${H(t[1])}</h3>`);return}if(qr(e)){a(),r.push(`<h3>${H(e.replace(/:$/,``))}</h3>`);return}let n=e.match(/^[-*]\s+(.+)$/);if(n){i.push(H(n[1]));return}a(),r.push(`<p>${H(e)}</p>`)}),a(),r.join(``)}function Rr(e){let t=document.createElement(`textarea`);return t.innerHTML=e,t.value}function zr(e){return/<\/?(?:a|br|div|em|h[1-6]|li|ol|p|span|strong|ul)\b/i.test(e)}function Br(e){let t=document.createElement(`template`);t.innerHTML=e;let n=[];return Vr(t.content.childNodes,n),n.join(``)}function Vr(e,t){e.forEach(e=>{if(e.nodeType===Node.TEXT_NODE){let n=X(e.textContent);n&&t.push(`<p>${H(n)}</p>`);return}if(e.nodeType!==Node.ELEMENT_NODE)return;let n=e,r=n.tagName.toLowerCase();if(r===`script`||r===`style`||r===`br`)return;if(/^h[1-6]$/.test(r)){Ur(t,n.textContent);return}if(r===`ul`||r===`ol`){let e=Wr(n);e&&t.push(e);return}if(r===`p`){Hr(n,t);return}let i=Array.from(n.children).some(e=>[`DIV`,`H1`,`H2`,`H3`,`H4`,`H5`,`H6`,`OL`,`P`,`UL`].includes(e.tagName));if([`article`,`div`,`section`].includes(r)&&i){Vr(n.childNodes,t);return}let a=Array.from(n.children).filter(e=>[`UL`,`OL`].includes(e.tagName)),o=X(Gr(n));if(o&&(Kr(o,n)?Ur(t,o):t.push(`<p>${H(o)}</p>`)),a.length>0){a.forEach(e=>{let n=Wr(e);n&&t.push(n)});return}!o&&i&&Vr(n.childNodes,t)})}function Hr(e,t){if(!e.querySelector(`br`)){let n=X(Gr(e));if(!n)return;Kr(n,e)?Ur(t,n):t.push(`<p>${H(n)}</p>`);return}let n=``,r=()=>{let r=X(n);n=``,r&&(Kr(r,e)?Ur(t,r):t.push(`<p>${H(r)}</p>`))};e.childNodes.forEach(e=>{if(e.nodeType===Node.ELEMENT_NODE&&e.tagName.toLowerCase()===`br`){r();return}n+=` ${e.textContent??``}`}),r()}function Ur(e,t){let n=X(t).replace(/:$/,``);n&&e.push(`<h3>${H(n)}</h3>`)}function Wr(e){let t=Array.from(e.children).filter(e=>e.tagName===`LI`).map(e=>{let t=X(Gr(e)),n=Array.from(e.children).filter(e=>[`UL`,`OL`].includes(e.tagName)).map(e=>Wr(e)).filter(Boolean).join(``);return t||n?`<li>${H(t)}${n}</li>`:``}).filter(Boolean);return t.length>0?`<ul>${t.join(``)}</ul>`:``}function Gr(e){let t=e.cloneNode(!0);return t.querySelectorAll(`ul, ol`).forEach(e=>{e.remove()}),t.textContent}function X(e){return String(e??``).replace(/\s+/g,` `).trim()}function Kr(e,t){let n=e.replace(/:$/,``).trim();return!n||n.length>90?!1:qr(n)||/:$/.test(e)?!0:/[.!?]$/.test(n)||n.split(/\s+/).length>10?!1:t.querySelector(`strong, b, u`)?!0:qr(n)}function qr(e){return mt.test(String(e).trim())}async function Jr(e){let t=M[0];if(!t)return;if(e===`later`){m.querySelectorAll(`.review-action`).forEach(e=>{e.disabled=!0});try{let e=await _i(t.id);M.shift(),br(e),Pr(`moved out of this review pass.`)}catch{Pr(`could not postpone that role. try again.`)}finally{m.querySelectorAll(`.review-action`).forEach(e=>{e.disabled=M.length===0})}return}if(![`interested`,`disinterested`].includes(e))return;let n=m.querySelectorAll(`.review-action`);n.forEach(e=>{e.disabled=!0});try{let n=await vi(t.id,e);M.shift(),Pr(e===`interested`?`marked interested.`:`marked disinterested.`),yr(n,document.querySelector(`.job[data-role-id="${CSS.escape(String(t.id))}"]`))}catch{n.forEach(e=>{e.disabled=!1}),Pr(`could not update that role. try again.`)}}async function Z(e=``){let t=N[0],n=N.length;if(Ce.textContent=n>0?`prep queue`:`prep complete`,we.textContent=n>0?`${n} interested ${n===1?`role`:`roles`} in queue`:``,h.querySelectorAll(`.review-action`).forEach(e=>{e.disabled=n===0}),!t){g.innerHTML=`
      <div class="review-empty">
        <h3>no interested jobs left.</h3>
        <p>everything in this queue has been prepped, moved, or postponed.</p>
      </div>
    `;return}g.innerHTML=`
    ${e?`<p class="review-message">${B(e)}</p>`:``}
    <div class="review-title-row">
      <p class="review-company">${H(t.company_name)}</p>
      ${Rt(t.title,t.role_url,`review-role-title`)}
    </div>
    <dl class="review-details review-primary-details">
      ${Y(`location`,t.location,!1,`review-location-detail`)}
      ${Y(`last`,z(t.last_seen_at))}
      ${Y(`updated`,z(t.updated_at))}
    </dl>
    ${Yr(t)}
    ${$r(t)}
    ${Xr(t.description)}
    ${Zr(t)}
  `,U(),ai(t.id).then(e=>{!e||N[0]?.id!==t.id||(F.set(t.id,e),g.querySelector(`.prep-resume`)?.replaceWith($(Yr(t,{resume:e}))),U())}).catch(()=>{}),gi(t.id).then(e=>{!e||N[0]?.id!==t.id||(I.set(t.id,e),g.querySelector(`.prep-cover-letter`)?.replaceWith($($r(t,{coverLetter:e}))),U())}).catch(()=>{})}function Yr(e,t={}){let n=F.get(e.id),r=t.resume??n,i=t.tweaks??_t.get(e.id)??``,a=`/api/roles/${encodeURIComponent(e.id)}/resume.pdf`;return t.loading?`
      <details class="prep-panel prep-resume" open>
        <summary class="prep-analysis-header">
          <span class="prep-accordion-icon" aria-hidden="true"></span>
          <h3>resume</h3>
          <span>regenerating</span>
        </summary>
        <div class="prep-fit-loading" aria-label="regenerating resume">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <p>regenerating resume with tweaks...</p>
        </div>
      </details>
    `:r?`
    <details class="prep-panel prep-resume" open>
      <summary class="prep-analysis-header">
        <span class="prep-accordion-icon" aria-hidden="true"></span>
        <h3>resume</h3>
        <div class="prep-summary-actions">
          <span>${r.pdf_base64?`preview ready`:`latex ready`}</span>
          ${r.pdf_base64?`<a class="prep-summary-action prep-cover-pdf-link" href="${B(a)}" target="_blank" rel="noreferrer">view</a>`:``}
        </div>
      </summary>
      <p class="prep-overview">${H(r.summary??`Saved resume for this role.`)}</p>
      ${Q(e)}
      <label class="prep-cover-tweaks prep-resume-tweaks">
        <span>tweaks</span>
        <textarea
          data-prep-resume-tweaks="${e.id}"
          rows="4"
          placeholder="paste or write a resume tweak prompt..."
        >${B(i)}</textarea>
      </label>
      <div class="prep-cover-actions">
        <button type="button" data-prep-resume-regenerate="${e.id}">
          regenerate with tweaks
        </button>
      </div>
      <label class="prep-cover-latex">
        <span>latex</span>
        <textarea
          data-prep-resume-latex="${e.id}"
          spellcheck="false"
        >${B(r.latex??``)}</textarea>
      </label>
      ${r.pdf_base64?`
            <iframe class="prep-cover-pdf" title="resume PDF preview" src="data:application/pdf;base64,${B(r.pdf_base64)}"></iframe>
          `:`<p class="prep-cover-path">PDF preview unavailable.</p>`}
    </details>
  `:`
      <details class="prep-panel prep-resume" open>
        <summary class="prep-analysis-header">
          <span class="prep-accordion-icon" aria-hidden="true"></span>
          <h3>resume</h3>
          <span>loading</span>
        </summary>
        <div class="prep-fit-loading" aria-label="loading resume">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <p>loading role resume...</p>
        </div>
      </details>
    `}function Xr(e){return`
    <details class="prep-panel prep-description-panel">
      <summary class="prep-analysis-header">
        <span class="prep-accordion-icon" aria-hidden="true"></span>
        <h3>description</h3>
      </summary>
      ${Ir(e)}
    </details>
  `}function Zr(e,t={}){let n=t.messages??vt.get(e.id)??[],r=!!t.loading;return`
    <details class="prep-panel prep-role-chat">
      <summary class="prep-analysis-header">
        <span class="prep-accordion-icon" aria-hidden="true"></span>
        <h3>chat about this role</h3>
        <span>${n.length?`${n.length} messages`:`ready`}</span>
      </summary>
      <div class="prep-role-chat-log" aria-live="polite">
        ${n.length?n.map(Qr).join(``):`<p class="prep-role-chat-empty">ask about fit, risks, resume emphasis, or cover letter angle.</p>`}
        ${r?`<p class="prep-role-chat-loading">thinking...</p>`:``}
      </div>
      <form class="prep-role-chat-form" data-prep-role-chat-form="${e.id}">
        <textarea
          data-prep-role-chat-input="${e.id}"
          rows="3"
          placeholder="ask about this role..."
        ></textarea>
        <button type="submit" ${r?`disabled`:``}>send</button>
      </form>
    </details>
  `}function Qr(e){let t=e?.role===`assistant`?`assistant`:`user`;return`
    <article class="prep-role-chat-message prep-role-chat-message-${t}">
      <span>${t}</span>
      <p>${H(e?.content??``)}</p>
    </article>
  `}function $r(e,t={}){let n=I.get(e.id),r=t.coverLetter??n,i=t.tweaks??r?.tweaks??``,a=`/api/roles/${encodeURIComponent(e.id)}/cover-letter.pdf`;return t.loading?`
      <details class="prep-panel prep-cover-letter" open>
        <summary class="prep-analysis-header">
          <span class="prep-accordion-icon" aria-hidden="true"></span>
          <h3>cover letter</h3>
          <span>generating</span>
        </summary>
        <div class="prep-fit-loading" aria-label="generating cover letter">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <p>generating latex cover letter...</p>
        </div>
      </details>
    `:`
    <details class="prep-panel prep-cover-letter" open>
      <summary class="prep-analysis-header">
        <span class="prep-accordion-icon" aria-hidden="true"></span>
        <h3>cover letter</h3>
        <div class="prep-summary-actions">
          <span>${r?.pdf_base64?`preview ready`:r?`latex ready`:`not generated`}</span>
          ${r?.pdf_base64?`<a class="prep-summary-action prep-cover-pdf-link" href="${B(a)}" target="_blank" rel="noreferrer">view</a>`:``}
        </div>
      </summary>
      ${r?`<p class="prep-overview">${H(r.summary??`cover letter generated`)}</p>`:`<p class="prep-overview">generate a LaTeX cover letter from the resume, posting, and stored examples.</p>`}
      <div class="prep-cover-actions">
        <button type="button" data-prep-cover-letter="${e.id}">
          ${r?`regenerate`:`generate`}
        </button>
      </div>
      ${r?`
            <label class="prep-cover-tweaks">
              <span>tweaks</span>
              <textarea
                data-prep-cover-letter-tweaks="${e.id}"
                rows="3"
                placeholder="make it warmer, cut a paragraph, emphasize systems work..."
              >${B(i)}</textarea>
            </label>
            <label class="prep-cover-latex">
              <span>latex</span>
              <textarea
                data-prep-cover-letter-latex="${e.id}"
                spellcheck="false"
              >${B(r.latex??``)}</textarea>
            </label>
            ${r.pdf_base64?`
                  <iframe class="prep-cover-pdf" title="cover letter PDF preview" src="data:application/pdf;base64,${B(r.pdf_base64)}"></iframe>
                `:`<p class="prep-cover-path">PDF preview unavailable.</p>`}
          `:``}
    </details>
  `}function Q(e,t={}){let n=P.get(e.id);if(!t.loading&&!t.error&&!t.analysis&&n)return Q(e,{analysis:n});if(!t.loading&&!t.error&&!t.analysis)return`
      <section class="prep-analysis" aria-label="ai analysis">
        <div class="prep-analysis-header">
          <h3>ai analysis</h3>
          <button type="button" data-prep-analysis="${e.id}">check fit</button>
        </div>
        <p class="prep-overview">check resume fit when you are ready to review AI feedback.</p>
      </section>
    `;if(t.loading)return`
      <section class="prep-analysis" aria-label="ai analysis">
        <div class="prep-analysis-header">
          <h3>ai analysis</h3>
          <span>loading</span>
        </div>
        <div class="prep-fit-loading" aria-label="checking resume fit">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <p>checking resume fit...</p>
        </div>
      </section>
    `;if(t.error)return`
      <section class="prep-analysis" aria-label="ai analysis">
        <div class="prep-analysis-header">
          <h3>ai analysis</h3>
          <span>unavailable</span>
        </div>
        <p class="prep-overview">could not generate analysis for this role.</p>
      </section>
    `;let r=t.analysis,i=Array.isArray(r?.feedback_items)?r.feedback_items:[],a=r?.verdict===`ready_to_apply`?`ready to apply`:`tweak`,o=Math.min(gt.get(e.id)??0,Math.max(i.length-1,0)),s=i[o];return`
    <section class="prep-analysis" aria-label="ai analysis">
      <div class="prep-analysis-header">
        <h3>ai analysis</h3>
        <span>${i.length} ${i.length===1?`item`:`items`}</span>
      </div>
      <p class="prep-verdict">${H(a)}</p>
      <p class="prep-overview">${H(r?.overview??`analysis unavailable`)}</p>
      ${s?`
            <article class="prep-feedback" data-feedback-index="${o}">
              <p class="prep-feedback-label">${H(s.label)}</p>
              <h4>${H(s.title)}</h4>
              <p>${H(s.detail)}</p>
              ${ei(s)}
              <label class="prep-feedback-comment">
                <span>response comment</span>
                <textarea
                  data-prep-feedback-comment
                  rows="2"
                  placeholder="why accept or ignore this?"
                ></textarea>
              </label>
            </article>
            <div class="prep-feedback-controls">
              <div class="prep-feedback-nav">
                <button type="button" data-prep-feedback="previous" ${o===0?`disabled`:``}>previous</button>
                <span>${o+1}/${i.length}</span>
                <button type="button" data-prep-feedback="next" ${o>=i.length-1?`disabled`:``}>next</button>
              </div>
              <div class="prep-feedback-decisions">
                <button type="button" data-prep-feedback="ignore">ignore</button>
                <button type="button" data-prep-feedback="accept" ${s.tweak_prompt?``:`disabled`}>
                  add tweak
                </button>
              </div>
            </div>
          `:`<p class="prep-overview">ready to apply with the current resume.</p>`}
    </section>
  `}function ei(e){return e?.tweak_prompt?`
    <div class="prep-proposed-edit">
      <p class="prep-proposed-label">tweak prompt</p>
      <p>${H(e.tweak_prompt)}</p>
    </div>
  `:`
      <div class="prep-proposed-edit">
        <p class="prep-proposed-label">feedback only</p>
        <p>not enough information to turn this into a safe resume tweak.</p>
      </div>
    `}async function ti(e,t={}){if(!t.force&&P.has(e))return P.get(e);let n=await fetch(`/api/roles/${encodeURIComponent(e)}/prep-analysis`);if(!n.ok)throw Error(`Prep analysis request failed`);let r=await n.json();return r.analysis.resources=r.resources??[],P.set(e,r.analysis),r.analysis}function $(e){let t=document.createElement(`template`);return t.innerHTML=e.trim(),t.content.firstElementChild}async function ni(e){let t=N[0];if(!t)return;let n=h.querySelectorAll(`.review-action`);if(n.forEach(e=>{e.disabled=!0}),e===`later`){try{await _i(t.id),t.review_later_count=Number(t.review_later_count??0)+1,N.length>1?(N.push(N.shift()),Z(`moved to the back of the prep queue.`)):Z(`only one role is in the prep queue.`)}catch{Z(`could not postpone prep. try again.`)}return}if(e===`applied`)try{let e=await vi(t.id,`applied`);N.shift(),Z(`moved to applied.`),yr(e,document.querySelector(`.job[data-role-id="${CSS.escape(String(t.id))}"]`))}catch{n.forEach(e=>{e.disabled=!1}),Z(`could not move that role. try again.`)}}async function ri(e,t,n,r){let i=await fetch(`/api/roles/${encodeURIComponent(e)}/prep-feedback`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({feedback_index:t,feedback_item:n,comment:r})});if(!i.ok)throw Error(`Prep feedback update failed`);return i.json()}async function ii(e,t,n,r){let i=await fetch(`/api/roles/${encodeURIComponent(e)}/prep-feedback-ignore`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({feedback_index:t,feedback_item:n,comment:r})});if(!i.ok)throw Error(`Prep feedback ignore failed`);return i.json()}async function ai(e,{force:t=!1}={}){if(!t&&F.has(e))return F.get(e);let n=await fetch(`/api/roles/${encodeURIComponent(e)}/resume`);if(!n.ok)throw Error(`Resume request failed`);let r=await n.json();return r.resume&&F.set(e,r.resume),r.resume}async function oi(e,t){let n=await fetch(`/api/roles/${encodeURIComponent(e)}/resume/save`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({latex:t})});if(!n.ok)throw Error(`Resume save failed`);return n.json()}async function si(e,t,n){let r=await fetch(`/api/roles/${encodeURIComponent(e)}/resume`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({tweaks:t,previous_latex:n})});if(!r.ok)throw Error(`Resume generation failed`);return r.json()}async function ci(e,t){let n=await fetch(`/api/roles/${encodeURIComponent(e)}/chat`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({messages:t})});if(!n.ok)throw Error(`Role chat failed`);return n.json()}function li(e,t,n=dt){let r=yt.get(e)??{timer:null,saving:!1,version:0,latex:``};r.version+=1,r.latex=t,r.timer&&clearTimeout(r.timer),r.timer=setTimeout(()=>{r.timer=null,ui(e)},n),yt.set(e,r)}async function ui(e){let t=yt.get(e);if(!t||t.saving)return;t.saving=!0;let n=t.version,r=t.latex;try{let i=await oi(e,r);t.version===n&&(F.set(e,i.resume),di(`resume`,e,i.resume))}catch{}finally{t.saving=!1,t.version!==n&&li(e,t.latex,0)}}function di(e,t,n){if(!n?.pdf_base64)return;let r=e===`resume`?`[data-prep-resume-latex="${t}"]`:`[data-prep-cover-letter-latex="${t}"]`,i=g.querySelector(r)?.closest(`.prep-panel`),a=i?.querySelector(`.prep-cover-pdf`),o=i?.querySelector(`.prep-cover-pdf-link`);a&&(a.src=`data:application/pdf;base64,${n.pdf_base64}`),o&&(o.href=e===`resume`?`/api/roles/${encodeURIComponent(t)}/resume.pdf`:`/api/roles/${encodeURIComponent(t)}/cover-letter.pdf`)}async function fi(e,t=``,n=``){let r=await fetch(`/api/roles/${encodeURIComponent(e)}/cover-letter`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({tweaks:t,previous_latex:n})});if(!r.ok)throw Error(`Cover letter generation failed`);return r.json()}async function pi(e,t){let n=await fetch(`/api/roles/${encodeURIComponent(e)}/cover-letter/save`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({latex:t})});if(!n.ok)throw Error(`Cover letter save failed`);return n.json()}function mi(e,t,n=``,r=dt){let i=bt.get(e)??{timer:null,saving:!1,version:0,latex:``,tweaks:``};i.version+=1,i.latex=t,i.tweaks=n,i.timer&&clearTimeout(i.timer),i.timer=setTimeout(()=>{i.timer=null,hi(e)},r),bt.set(e,i)}async function hi(e){let t=bt.get(e);if(!t||t.saving)return;t.saving=!0;let n=t.version,r=t.latex,i=t.tweaks;try{let a=await pi(e,r);t.version===n&&(I.set(e,{...a.cover_letter,tweaks:i}),di(`coverLetter`,e,a.cover_letter))}catch{}finally{t.saving=!1,t.version!==n&&mi(e,t.latex,t.tweaks,0)}}async function gi(e){if(I.has(e))return I.get(e);let t=await fetch(`/api/roles/${encodeURIComponent(e)}/cover-letter`);if(!t.ok)throw Error(`Cover letter request failed`);let n=await t.json();return n.cover_letter&&I.set(e,n.cover_letter),n.cover_letter}async function _i(e){let t=await fetch(`/api/roles/${encodeURIComponent(e)}/review-later`,{method:`POST`});if(!t.ok)throw Error(`Review later update failed`);return(await t.json()).role}async function vi(e,t){let n=await fetch(`/api/roles/${encodeURIComponent(e)}/status`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({status:t})});if(!n.ok)throw Error(`Status update failed`);return(await n.json()).role}_e.addEventListener(`click`,Ar),Se.addEventListener(`click`,jr),ve.addEventListener(`click`,Mr),Te.addEventListener(`click`,Nr),m.addEventListener(`click`,e=>{let t=e.target.closest(`[data-review-action]`);t&&Jr(t.dataset.reviewAction)}),h.addEventListener(`click`,e=>{e.target.closest(`.prep-summary-action`)&&e.stopPropagation()}),h.addEventListener(`input`,e=>{let t=e.target.closest(`[data-prep-resume-tweaks]`);if(t){let e=Number(t.dataset.prepResumeTweaks);Number.isFinite(e)&&_t.set(e,t.value);return}let n=e.target.closest(`[data-prep-resume-latex]`);if(n){let e=Number(n.dataset.prepResumeLatex);if(!Number.isFinite(e))return;li(e,n.value);return}let r=e.target.closest(`[data-prep-cover-letter-latex]`);if(!r)return;let i=Number(r.dataset.prepCoverLetterLatex);if(!Number.isFinite(i))return;let a=r.closest(`.prep-cover-letter`)?.querySelector(`[data-prep-cover-letter-tweaks="${i}"]`)?.value??``;mi(i,r.value,a)}),h.addEventListener(`scroll`,e=>{e.target.closest(`[data-prep-resume-latex], [data-prep-cover-letter-latex]`)},!0),h.addEventListener(`focusout`,e=>{let t=e.target.closest(`[data-prep-resume-latex]`);if(t){let e=Number(t.dataset.prepResumeLatex);if(!Number.isFinite(e))return;li(e,t.value,0);return}let n=e.target.closest(`[data-prep-cover-letter-latex]`);if(!n)return;let r=Number(n.dataset.prepCoverLetterLatex);if(!Number.isFinite(r))return;let i=n.closest(`.prep-cover-letter`)?.querySelector(`[data-prep-cover-letter-tweaks="${r}"]`)?.value??``;mi(r,n.value,i,0)}),h.addEventListener(`submit`,async e=>{let t=e.target.closest(`[data-prep-role-chat-form]`);if(!t||!N[0])return;e.preventDefault();let n=Number(t.dataset.prepRoleChatForm);if(!Number.isFinite(n))return;let r=t.querySelector(`[data-prep-role-chat-input="${n}"]`),i=r?.value?.trim()??``;if(!i){r?.focus();return}let a=[...vt.get(n)??[],{role:`user`,content:i}];vt.set(n,a),g.querySelector(`.prep-role-chat`)?.replaceWith($(Zr(N[0],{messages:a,loading:!0})));try{let e=await ci(n,a),t=[...a,e.message];vt.set(n,t),g.querySelector(`.prep-role-chat`)?.replaceWith($(Zr(N[0],{messages:t})))}catch{let e=[...a,{role:`assistant`,content:`could not answer right now.`}];vt.set(n,e),g.querySelector(`.prep-role-chat`)?.replaceWith($(Zr(N[0],{messages:e})))}}),h.addEventListener(`click`,async e=>{if(e.target.closest(`[data-prep-analysis]`)&&N[0]){let e=N[0].id;g.querySelector(`.prep-analysis`)?.replaceWith($(Q(N[0],{loading:!0})));try{let t=await ti(e,{force:!0});if(N[0]?.id!==e)return;g.querySelector(`.prep-analysis`)?.replaceWith($(Q(N[0],{analysis:t})))}catch{g.querySelector(`.prep-analysis`)?.replaceWith($(Q(N[0],{error:!0})))}return}if(e.target.closest(`[data-prep-resume-regenerate]`)&&N[0]){let e=N[0].id,t=g.querySelector(`.prep-resume`),n=t?.querySelector(`[data-prep-resume-tweaks="${e}"]`)?.value??``,r=t?.querySelector(`[data-prep-resume-latex="${e}"]`)?.value??``;if(!n.trim()){t?.querySelector(`[data-prep-resume-tweaks="${e}"]`)?.focus();return}_t.set(e,n),t?.replaceWith($(Yr(N[0],{loading:!0})));try{let t=await si(e,n,r);F.set(e,t.resume),g.querySelector(`.prep-resume`)?.replaceWith($(Yr(N[0],{resume:t.resume}))),U()}catch{g.querySelector(`.prep-resume`)?.replaceWith($(Yr(N[0],{resume:F.get(e),tweaks:n}))),U()}return}if(e.target.closest(`[data-prep-cover-letter]`)&&N[0]){let e=N[0].id,t=g.querySelector(`.prep-cover-letter`),n=t?.querySelector(`[data-prep-cover-letter-tweaks="${e}"]`)?.value??``,r=n.trim()?t?.querySelector(`[data-prep-cover-letter-latex="${e}"]`)?.value??``:``;t?.replaceWith($($r(N[0],{loading:!0})));try{let t=await fi(e,n,r);I.set(e,t.cover_letter),g.querySelector(`.prep-cover-letter`)?.replaceWith($($r(N[0],{coverLetter:t.cover_letter}))),U()}catch{g.querySelector(`.prep-cover-letter`)?.replaceWith($($r(N[0],{coverLetter:I.get(e),tweaks:n}))),U()}return}let t=e.target.closest(`[data-prep-action]`);if(t){ni(t.dataset.prepAction);return}let n=e.target.closest(`[data-prep-feedback]`);if(!n||!N[0])return;let r=N[0].id,i=P.get(r),a=Array.isArray(i?.feedback_items)?i.feedback_items.length:0,o=gt.get(r)??0;if(n.dataset.prepFeedback===`accept`||n.dataset.prepFeedback===`ignore`){let e=i?.feedback_items?.[o];if(!e)return;let t=g.querySelector(`[data-prep-feedback-comment]`)?.value??``,a=n.dataset.prepFeedback,s=a;n.disabled=!0,n.textContent=a===`accept`?`adding...`:`ignoring...`;try{if(a===`accept`){let n=await ri(r,o,e,t),a=document.querySelector(`.job[data-role-id="${CSS.escape(String(r))}"]`);n.role&&(N[0]=n.role,yr(n.role,a)),bi(r,n.tweak_prompt??e.tweak_prompt??``),yi(r,o,i)}else await ii(r,o,e,t),yi(r,o,i)}catch{n.disabled=!1,n.textContent=s}return}let s=n.dataset.prepFeedback===`next`?1:-1;gt.set(r,Math.max(0,Math.min(o+s,a-1))),g.querySelector(`.prep-analysis`)?.replaceWith($(Q(N[0],{analysis:i})))});function yi(e,t,n){let r=n.feedback_items.filter((e,n)=>n!==t),i=Math.min(t,Math.max(r.length-1,0)),a={...n,feedback_items:r,verdict:r.length===0?`ready_to_apply`:n.verdict};gt.set(e,i),P.set(e,a),g.querySelector(`.prep-analysis`)?.replaceWith($(Q(N[0],{analysis:a})))}function bi(e,t){let n=String(t||``).trim();if(!n)return;let r=_t.get(e)?.trim()??``,i=r?`${r}\n\n${n}`:n;_t.set(e,i);let a=g.querySelector(`[data-prep-resume-tweaks="${e}"]`);a&&(a.value=i,a.focus())}document.addEventListener(`keydown`,e=>{e.key===`Escape`&&!o.hidden&&Mt(),e.key===`Escape`&&!m.hidden&&jr(),e.key===`Escape`&&!h.hidden&&Nr(),e.key===`Escape`&&!Ne.hidden&&hn(),e.key===`Escape`&&!Ge.hidden&&Cn(),e.key===`Escape`&&!Ze.hidden&&Mn(),e.key===`Escape`&&!nt.hidden&&qn()});function xi(){return Array.from(document.querySelectorAll(`.pane-toggle`))}function Si(){return xi().some(e=>e.getAttribute(`aria-expanded`)===`true`)}function Ci(){ke.textContent=Si()?`collapse all`:`expand all`}function wi(){document.querySelectorAll(`.pane-toggle`).forEach(e=>{e.setAttribute(`aria-expanded`,`true`),e.querySelector(`.chevron`).textContent=`v`,e.parentElement.querySelector(`.pane-body`).hidden=!1})}function Ti(){document.querySelectorAll(`.job[open]`).forEach(e=>{e.open=!1}),document.querySelectorAll(`.pane-toggle`).forEach(e=>{e.setAttribute(`aria-expanded`,`false`),e.querySelector(`.chevron`).textContent=`>`,e.parentElement.querySelector(`.pane-body`).hidden=!0})}ke.addEventListener(`click`,()=>{Si()?Ti():wi(),Ci()}),Ae.addEventListener(`click`,()=>{ht=!ht,Ae.textContent=ht?`show empty`:`hide empty`,D&&Jt(D.statuses)}),Me.addEventListener(`click`,mn),Pe.addEventListener(`click`,hn),We.addEventListener(`click`,Sn),Ke.addEventListener(`click`,Cn),Xe.addEventListener(`click`,jn),Qe.addEventListener(`click`,Mn),Ee.addEventListener(`click`,Kn),rt.addEventListener(`click`,qn),it.addEventListener(`submit`,e=>{e.preventDefault(),Xn(it).catch(()=>{T.textContent=`could not add company.`})}),at.addEventListener(`submit`,e=>{e.preventDefault(),tr(at).catch(()=>{lt.textContent=`could not add role.`})}),E.addEventListener(`submit`,e=>{let t=e.target.closest(`[data-company-link-form]`);t&&(e.preventDefault(),Zn(t).catch(()=>{T.textContent=`could not add link.`}))}),E.addEventListener(`input`,e=>{let t=e.target.closest(`[data-company-notes]`);t&&ir(t.dataset.companyNotes)}),E.addEventListener(`change`,e=>{let t=e.target.closest(`[data-company-tier]`);if(!t)return;let n=t.closest(`.company-panel`);n&&or(n,t.value),window.clearTimeout(kt.get(t.dataset.companyTier)),ar(t.dataset.companyTier).catch(()=>{rr(`could not save company.`)})}),E.addEventListener(`click`,e=>{let t=e.target.closest(`[data-delete-company]`);if(t){let e=nr(t.dataset.deleteCompany),n=e?.name?V(e.name):`this company`;if(!window.confirm(`Deactivate ${n}? It will be hidden from company counts and skipped during scans.`))return;t.disabled=!0,$n(t.dataset.deleteCompany).catch(()=>{T.textContent=`could not deactivate company.`,t.disabled=!1});return}let n=e.target.closest(`[data-delete-career-page]`);if(!n)return;let r=n.closest(`.company-link-row`)?.querySelector(`.company-link-text`)?.textContent?.trim();window.confirm(`Delete ${r||`this career link`}?`)&&(n.disabled=!0,Qn(n.dataset.deleteCareerPage).catch(()=>{T.textContent=`could not delete link.`,n.disabled=!1}))}),Fe.addEventListener(`change`,e=>{let t=e.target.closest(`input[type="checkbox"], select, input[data-setting-text]`);t&&Pn(t)}),Fe.addEventListener(`submit`,e=>{e.preventDefault()}),x.addEventListener(`input`,()=>{S.disabled=!x.value.trim()}),Ve.addEventListener(`click`,In),S.addEventListener(`click`,Ln),Ue.addEventListener(`click`,Fn),tt.addEventListener(`click`,Bn),zn(),fr({applyDefaultCollapsed:!0}).catch(()=>{Vt(null,`could not load resume.`),Ht([],`could not load cover letter examples.`),W()}),cr().then(()=>{lr()}).catch(()=>{y.textContent=`could not load scan status`});