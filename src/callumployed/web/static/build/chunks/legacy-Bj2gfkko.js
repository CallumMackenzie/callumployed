import{t as e}from"./preload-helper-Czpn1I53.js";var{sankey:t,sankeyLinkHorizontal:n}=await e(async()=>{let{sankey:e,sankeyLinkHorizontal:t}=await import(`/assets/d3-sankey.js`);return{sankey:e,sankeyLinkHorizontal:t}},[]),r=document.querySelector(`#stats`),i=document.querySelector(`#status-list`),a=document.querySelector(`#search-toggle`),o=document.querySelector(`#search-dialog`),s=document.querySelector(`#search-backdrop`),c=document.querySelector(`#search-form`),l=document.querySelector(`#search-input`),u=document.querySelector(`#close-search`),d=document.querySelector(`#materials-panel`),ee=document.querySelector(`#materials-toggle`),te=document.querySelector(`#materials-body`),ne=document.querySelector(`#materials-summary`),re=document.querySelector(`#materials-required-warning`),f=document.querySelector(`#resume-meta`),p=document.querySelector(`#resume-upload`),ie=document.querySelector(`#resume-upload-button`),ae=document.querySelector(`#resume-resource-meta`),oe=document.querySelector(`#resume-resource-upload`),se=document.querySelector(`#resume-resource-upload-button`),ce=document.querySelector(`#resume-resource-list`),le=document.querySelector(`#cover-letter-meta`),ue=document.querySelector(`#cover-letter-upload`),de=document.querySelector(`#cover-letter-upload-button`),fe=document.querySelector(`#cover-letter-list`),pe=document.querySelector(`#experience-note-meta`),me=document.querySelector(`#experience-note-upload`),he=document.querySelector(`#experience-note-upload-button`),ge=document.querySelector(`#experience-note-list`),m=document.querySelector(`#material-index-button`),h=document.querySelector(`#material-index-warning`),_e=document.querySelector(`#material-index-status`),ve=document.querySelector(`#review-discovered`),ye=document.querySelector(`#prep-interested`),g=document.querySelector(`#review-view`),be=document.querySelector(`#review-heading`),xe=document.querySelector(`#review-progress`),Se=document.querySelector(`#review-card`),Ce=document.querySelector(`#close-review`),_=document.querySelector(`#prep-view`),we=document.querySelector(`#prep-heading`),Te=document.querySelector(`#prep-progress`),v=document.querySelector(`#prep-card`),Ee=document.querySelector(`#close-prep`),y=document.querySelector(`#scan-all-button`),De=document.querySelector(`#manage-companies-button`),b=document.querySelector(`#scan-status-bar`),x=document.querySelector(`#scan-status-text`),Oe=document.querySelector(`#scan-last-time`),ke=document.querySelector(`#scan-failures-open`),Ae=document.querySelector(`#scan-failures-dialog`),je=document.querySelector(`#scan-failures-backdrop`),Me=document.querySelector(`#scan-failures-close`),Ne=document.querySelector(`#scan-failures-list`),Pe=document.querySelector(`#toggle-all`),Fe=document.querySelector(`#collapse-empty`),Ie=document.querySelector(`#toolbar-summary`),Le=document.querySelector(`#settings-open`),Re=document.querySelector(`#settings-view`),ze=document.querySelector(`#settings-close`),S=document.querySelector(`#settings-status`),Be=document.querySelector(`#settings-form`),Ve=document.querySelector(`#settings-profile-options`),He=document.querySelector(`#settings-options`),Ue=document.querySelector(`#central-store-summary`),We=document.querySelector(`#central-store-sync-summary`),Ge=document.querySelector(`#central-api-url-input`),Ke=document.querySelector(`#central-passkey-input`),qe=document.querySelector(`#central-save-button`),C=document.querySelector(`#central-sync-button`),Je=document.querySelector(`#recommendation-history-summary`),Ye=document.querySelector(`#clear-recommendation-history`),Xe=document.querySelector(`#metrics-open-button`),Ze=document.querySelector(`#metrics-view`),Qe=document.querySelector(`#metrics-close`),$e=document.querySelector(`#metrics-status`),et=document.querySelector(`#metrics-overview`),tt=document.querySelector(`#metrics-sections`),nt=document.querySelector(`#metrics-scan-list`),rt=document.querySelector(`#sankey-open-button`),it=document.querySelector(`#sankey-view`),at=document.querySelector(`#sankey-close`),w=document.querySelector(`#sankey-status`),ot=document.querySelector(`#sankey-canvas`),st=document.querySelector(`#sankey-path-list`),ct=document.querySelector(`#app-update-button`),lt=document.querySelector(`#companies-view`),ut=document.querySelector(`#companies-close`),T=document.querySelector(`#companies-status`),dt=document.querySelector(`#company-create-form`),E=document.querySelector(`#companies-list`),ft=document.querySelector(`#role-add-form`),pt=document.querySelector(`#role-url-input`),mt=document.querySelector(`#role-company-input`),ht=document.querySelector(`#role-company-options`),gt=document.querySelector(`#role-add-status`),_t=3,vt=1200,yt=new Set([`applied`,`OA`,`interview`,`rejected`,`offer`]),bt=new Map([[`discovered`,`#4f6472`],[`interested`,`#00897b`],[`disinterested`,`#626970`],[`applied`,`#2257ad`],[`oa`,`#b36b00`],[`interview`,`#5f2bd8`],[`rejected`,`#b93d2d`],[`offer`,`#137347`],[`closed`,`#53606b`],[`archived`,`#765b4a`]]),xt=/^(?:about (?:the )?(?:role|team|job)|about this role|job description|job responsibilities|minimum qualifications|preferred qualifications|qualifications|requirements|responsibilities|what to expect|what (?:you'll|you’ll|you will) (?:bring|do)|what'?s in it for you|who you are|your objectives|your skills & talents):?$/i,St=!0,D=null,O=null,k=[],A=[],j=[],M=null,N=[],P=[],F=new Map,Ct=new Map,I=new Map,wt=new Map,L=new Map,Tt=new Map,Et=new Map,Dt=new Map,Ot=!1,kt=null,At=!1,jt=null,Mt=null,Nt=null,Pt=null,R=null,Ft=[],It=new Map;function z(){return D?.query?.trim()??``}function Lt(){let e=!!z();a.classList.toggle(`search-active`,e),a.setAttribute(`aria-label`,e?`clear search`:`search jobs`)}function Rt(){l.value=z(),o.hidden=!1,c.hidden=!1,l.focus(),l.select()}function zt(){o.hidden=!0,c.hidden=!0,a.focus()}function Bt(e){return e?new Intl.DateTimeFormat(void 0,{month:`short`,day:`numeric`,hour:`numeric`,minute:`2-digit`}).format(new Date(e)).toLocaleLowerCase():``}function B(e){return e?new Intl.DateTimeFormat(void 0,{month:`short`,day:`numeric`,hour:`numeric`,minute:`2-digit`}).format(new Date(e)).replace(`, `,` `).toLocaleLowerCase():``}function V(e){return String(e??``).replaceAll(`&`,`&amp;`).replaceAll(`<`,`&lt;`).replaceAll(`>`,`&gt;`).replaceAll(`"`,`&quot;`).replaceAll(`'`,`&#039;`)}function H(e){return String(e??``).toLocaleLowerCase()}function U(e){return V(H(e))}function Vt(e){return e}function W(e=v){e.querySelectorAll(`[data-prep-resume-latex], [data-prep-cover-letter-latex]`).forEach(Vt)}function Ht(){return`
    <svg class="role-link-icon" viewBox="0 0 24 24" aria-hidden="true">
      <path d="M7 17 17 7"></path>
      <path d="M8 7h9v9"></path>
    </svg>
  `}function Ut(){return`
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M12 5v14"></path>
      <path d="M5 12h14"></path>
    </svg>
  `}function Wt(){return`
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M3 6h18"></path>
      <path d="M8 6V4h8v2"></path>
      <path d="m19 6-1 14H6L5 6"></path>
      <path d="M10 11v5"></path>
      <path d="M14 11v5"></path>
    </svg>
  `}function Gt(e,t,n){let r=`<span class="role-title-text">${U(e)}</span>`;return t?`<a class="${n}" href="${V(t)}" target="_blank" rel="noreferrer">${r}${Ht()}</a>`:`<span class="${n}">${r}</span>`}function Kt(e){r.innerHTML=[[`companies`,e.companies_total],[`jobs`,e.jobs_total],[`applications`,e.applications_total]].map(([e,t])=>`<dl class="stat"><dt>${U(e)}</dt><dd>${t}</dd></dl>`).join(``)}function qt(e=D){if(!e){Ie.innerHTML=``;return}let t=t=>e.statuses.find(e=>e.key===t)?.count??0;Ie.innerHTML=[[`discovered`,t(`discovered`)],[`interested`,t(`interested`)],[`applied`,e.stats?.applications_total??0],[`total`,e.stats?.jobs_total??0]].map(([e,t])=>`
        <dl>
          <dt>${U(e)}</dt>
          <dd>${t}</dd>
        </dl>
      `).join(``)}function Jt(e,t=``){if(O=e,ie.textContent=e?`replace`:`upload`,t){f.textContent=t;return}if(!e){f.textContent=`no resume uploaded`;return}let n=B(e.updated_at),r=tn(e.content_bytes);f.textContent=[H(e.filename),r,n].filter(Boolean).join(` | `)}function Yt(e,t=``){A=Array.isArray(e)?e:[],de.textContent=A.length>0?`add`:`upload`,le.textContent=t||(A.length===0?`no examples uploaded`:`${A.length} ${A.length===1?`example`:`examples`} stored`);let n=A.slice(0,3),r=Math.max(A.length-n.length,0);fe.innerHTML=n.map(e=>{let t=tn(e.content_bytes);return`
        <li title="${U(e.filename)}">
          <span>${U(e.filename)}</span>
          <small>${V(t)}</small>
        </li>
      `}).join(``),r>0&&fe.insertAdjacentHTML(`beforeend`,`<li class="examples-more"><span>+${r} more</span></li>`)}function Xt(e,t=``){j=Array.isArray(e)?e:[],he.textContent=j.length>0?`add`:`upload`,pe.textContent=t||(j.length===0?`no notes uploaded`:`${j.length} ${j.length===1?`note`:`notes`} stored`);let n=j.slice(0,3),r=Math.max(j.length-n.length,0);ge.innerHTML=n.map(e=>{let t=tn(e.content_bytes);return`
        <li title="${U(e.filename)}">
          <span>${U(e.filename)}</span>
          <small>${V(t)}</small>
        </li>
      `}).join(``),r>0&&ge.insertAdjacentHTML(`beforeend`,`<li class="examples-more"><span>+${r} more</span></li>`)}function Zt(e,t=``){M=e??null;let n=M?.status??`missing`,r=n!==`ready`,i=j.length>0;if(h.hidden=!r,h.textContent=t||M?.warning||``,m.disabled=!i,m.textContent=n===`ready`?`reindex materials`:`index materials`,t)_e.textContent=t;else if(n===`ready`){let e=Number(M?.document_count??0),t=Number(M?.skipped_source_count??0),n=B(M?.generated_at);_e.textContent=[`${e} indexed ${e===1?`page`:`pages`}`,t?`${t} unreadable upload skipped`:``,n].filter(Boolean).join(` | `)}else _e.textContent=n===`stale`?`index out of date`:`not indexed`}function Qt(e,t=``){k=Array.isArray(e)?e:[],se.textContent=k.length>0?`add`:`upload`,ae.textContent=t||(k.length===0?`no resources uploaded`:`${k.length} ${k.length===1?`resource`:`resources`} stored`);let n=k.slice(0,3),r=Math.max(k.length-n.length,0);ce.innerHTML=n.map(e=>{let t=tn(e.bytes);return`
        <li title="${U(e.filename)}">
          <span>${U(e.filename)}</span>
          <small>${V(t)}</small>
        </li>
      `}).join(``),r>0&&ce.insertAdjacentHTML(`beforeend`,`<li class="examples-more"><span>+${r} more</span></li>`)}function $t(e,t={}){Jt(e?.master_resume??null),Qt(e?.resume_resources??[]),Yt(e?.cover_letter_examples??[]),Xt(e?.experience_notes??[]),Zt(e?.material_index??null),G(e?.ui),(!Ot||t.applyDefaultCollapsed)&&(en(!!e?.ui?.default_collapsed),Ot=!0)}function G(e=null){let t=O?`resume ready`:`no resume`,n=k.length===0?`no resources`:`${k.length} ${k.length===1?`resource`:`resources`}`,r=A.length,i=r===0?`no cover letters`:`${r} cover ${r===1?`letter`:`letters`}`,a=j.length,o=a===0?`no notes`:`${a} experience ${a===1?`note`:`notes`}`;re.hidden=!(typeof e?.has_missing_required_materials==`boolean`?e.has_missing_required_materials:!O||r===0||a===0),ne.textContent=`${t} | ${n} | ${i} | ${o}`}function en(e){d.classList.toggle(`collapsed`,e),ee.setAttribute(`aria-expanded`,String(!e)),ee.querySelector(`.materials-chevron`).textContent=e?`>`:`v`,te.hidden=e}function tn(e){return Number.isFinite(e)?e<1024?`${e} b`:`${Math.round(e/1024)} kb`:``}function nn(e){i.innerHTML=e.map(e=>{let t=e.jobs.map(t=>rn(t,e.key)).join(``);return`
        <section class="status-pane ${e.count===0?`empty`:``} ${St?`hidden-empty`:``}" id="status-${V(e.key)}" data-bucket="${V(e.key)}">
          <button class="pane-toggle" type="button" aria-expanded="false">
            <span class="chevron">></span>
            <span class="pane-title">${U(e.label)}</span>
            <span class="count">${e.count}</span>
          </button>
          <div class="pane-body" hidden>
            ${t?`<div class="jobs">${t}</div>`:`<p class="empty-copy">no jobs in this status.</p>`}
          </div>
        </section>
      `}).join(``)}function rn(e,t){return`
    <details class="job" data-role-id="${V(e.id)}">
      <summary class="job-summary">
        <span class="job-chevron">></span>
        <span class="job-identity">
          <span class="job-company">[${U(e.company_name)}]</span>
          ${Gt(e.title,e.role_url,`job-title`)}
          ${t===`interested`&&e.prep_started?sn():``}
          ${t===`closed`&&e.updated_in_latest_scan?an():``}
          ${[`discovered`,`interested`].includes(t)&&e.missing_from_latest_scan?on():``}
        </span>
      </summary>
      <div class="job-detail">
        ${t===`discovered`?cn(e):``}
        ${t===`interested`?ln(e):``}
        ${t===`disinterested`?un(e):``}
        ${t===`applied`?dn(e):``}
        ${t===`OA`?fn(e):``}
        ${t===`interview`?pn(e):``}
        ${t===`closed`?mn(e):``}
        <dl>
          ${e.location?`<div>
                  <dt>location</dt>
                  <dd>${U(e.location)}</dd>
                </div>`:``}
          <div>
            <dt>updated</dt>
            <dd>${Bt(e.updated_at)}</dd>
          </div>
        </dl>
      </div>
    </details>
  `}function an(){return`<span class="latest-scan-dot" title="updated in latest scan" aria-label="updated in latest scan"></span>`}function on(){return`<span class="missing-latest-scan-dot" title="not seen in latest scan" aria-label="not seen in latest scan"></span>`}function sn(){return`<span class="prep-started-dot" title="application materials started" aria-label="application materials started"></span>`}function cn(e){return`
    <div class="job-actions job-actions-nowrap" aria-label="discovered role actions">
      <button class="job-action success" type="button" data-review-role-id="${e.id}">view</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="interested">interested</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="disinterested">disinterested</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="closed">closed</button>
    </div>
  `}function ln(e){return`
    <div class="job-actions" aria-label="interested role actions">
      <button class="job-action success" type="button" data-prep-role-id="${e.id}">prep</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="applied">applied</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="disinterested">disinterested</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="closed">closed</button>
    </div>
  `}function un(e){return`
    <div class="job-actions" aria-label="disinterested role actions">
      <button class="job-action success" type="button" data-role-id="${e.id}" data-status="interested">interested</button>
    </div>
  `}function dn(e){return`
    <div class="job-actions job-actions-nowrap" aria-label="applied role actions">
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="OA">oa</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="interview">interview</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="rejected">rejected</button>
    </div>
  `}function fn(e){return`
    <div class="job-actions job-actions-nowrap" aria-label="oa role actions">
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="interview">interview</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="disinterested">disinterested</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="rejected">rejected</button>
    </div>
  `}function pn(e){return`
    <div class="job-actions" aria-label="interview role actions">
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="rejected">rejected</button>
      <button class="job-action success" type="button" data-role-id="${e.id}" data-status="offer">offer</button>
    </div>
  `}function mn(e){return`
    <div class="job-actions" aria-label="closed role actions">
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="interested">interested</button>
    </div>
  `}function hn(e){D=e,l.value=e.query,Lt(),Kt(e.stats),qt(e),nn(e.statuses),Fi(),Lr(e.statuses),zr(e.statuses)}function gn(e){jt=e??null;let t=!!e?.scanning,n=t&&!!e?.cancel_requested,r=Number(e?.completed_companies??0),i=Number(e?.total_companies??0),a=Number(e?.failed_companies??0),o=typeof e?.error==`string`?e.error.trim():``,s=Array.isArray(e?.failures)?e.failures:[];y.disabled=n,y.textContent=t?n?`cancelling...`:`cancel scan`:`scan roles`,y.classList.toggle(`danger`,t&&!n),b.hidden=!t&&!o&&s.length===0,b.classList.toggle(`scanning`,t),b.classList.toggle(`scan-error`,!t&&!!o||s.length>0),x.textContent=n?`cancelling scan...`:t?`scanning roles${i>0?` ${r}/${i}`:``}${a>0?`, ${a} failed`:``}`:s.length>0?`${s.length} recent scan ${s.length===1?`failure`:`failures`}`:o?`last scan error: ${o}`:`scan idle`,ke&&Ne&&(ke.hidden=s.length===0,Ne.innerHTML=s.slice(0,5).map(e=>{let t=e?.company_name||`unknown company`,n=e?.error||`scan failed`;return`
          <p>
            <span>${U(t)}</span>
            <span>${V(n)}</span>
          </p>
        `}).join(``),s.length===0&&vn());let c=e?.last_scan_at;Oe.textContent=c?`last scan: ${B(c)}`:`last scan: never`,At&&!t&&Y(z()).catch(()=>{}),At=t}function _n(){ke.hidden||(Ae.hidden=!1,Me.focus())}function vn(){Ae.hidden=!0}function K(e,t=``){Mt=e;let n=Array.isArray(e?.settings)?e.settings:[],r=n.filter(e=>e.key?.startsWith(`applicant_`)),i=n.filter(e=>!e.key?.startsWith(`applicant_`)),a=e?.central??{};S.textContent=t,S.classList.toggle(`is-empty`,!t);let o=Number(e?.recommendation_history_count??0);Je.textContent=o>0?`${o} saved ${o===1?`feedback decision`:`feedback decisions`}`:`no saved resume feedback decisions`,Ye.disabled=o===0,yn(a),Ve.innerHTML=r.map(e=>bn(e)).join(``),He.innerHTML=i.map(e=>bn(e)).join(``),q(!1)}function yn(e){let t=e?.api_url??``;Ge.value=t,Ke.value=``;let n=e?.passkey_configured?`passkey saved`:`no passkey saved`;Ue.textContent=t?`${H(t)} | ${n}`:`no api url | ${n}`,We.textContent=`${Number(e?.companies_linked??0)} linked | ${Number(e?.companies_unlinked??0)} unlinked | ${Number(e?.companies_needs_review??0)} review | ${Number(e?.companies_failed??0)} failed`,C.disabled=!t}function bn(e){if(e.control===`text`&&e.editable!==!1)return xn(e);if(e.control===`select`&&e.editable!==!1)return Sn(e);if(e.control!==`toggle`||e.editable===!1)return Cn(e);let t=e.value?`checked`:``,n=e.default?`on by default`:`off by default`;return`
    <label class="setting-option">
      <span class="setting-copy">
        <span class="setting-label">${U(e.label)}</span>
        <span class="setting-description">${U(e.description)}</span>
        <span class="setting-default">${U(n)}</span>
      </span>
      <span class="setting-switch">
        <input type="checkbox" name="${V(e.key)}" ${t} />
        <span aria-hidden="true"></span>
      </span>
    </label>
  `}function xn(e){let t=e.default?`default: ${H(e.default)}`:`optional`,n=e.input_type??`text`,r=e.autocomplete??`name`;return`
    <label class="setting-option">
      <span class="setting-copy">
        <span class="setting-label">${U(e.label)}</span>
        <span class="setting-description">${U(e.description)}</span>
        <span class="setting-default">${U(t)}</span>
      </span>
      <input
        class="setting-text-input"
        data-setting-text
        name="${V(e.key)}"
        type="${V(n)}"
        value="${V(e.value??``)}"
        autocomplete="${V(r)}"
      />
    </label>
  `}function Sn(e){let t=Array.isArray(e.options)?e.options:[],n=`default: ${H(e.default)}`;return`
    <label class="setting-option">
      <span class="setting-copy">
        <span class="setting-label">${U(e.label)}</span>
        <span class="setting-description">${U(e.description)}</span>
        <span class="setting-default">${U(n)}</span>
      </span>
      <select class="setting-select" name="${V(e.key)}">
        ${t.map(t=>{let n=t.value===e.value?`selected`:``;return`<option value="${V(t.value)}" ${n}>${U(t.label)}</option>`}).join(``)}
      </select>
    </label>
  `}function Cn(e){let t=e.default?`on by default`:`off by default`,n=e.value?`automatic`:`off`;return`
    <div class="setting-option setting-option-readonly">
      <span class="setting-copy">
        <span class="setting-label">${U(e.label)}</span>
        <span class="setting-description">${U(e.description)}</span>
        <span class="setting-default">${U(t)}</span>
      </span>
      <span class="setting-badge">${U(n)}</span>
    </div>
  `}function q(e){Be.querySelectorAll(`input, select`).forEach(t=>{t.disabled=e}),qe.disabled=e,C.disabled=e||!Ge.value.trim(),ct.disabled=e}async function wn(){Re.hidden=!1,document.body.classList.add(`settings-open`),ze.focus(),Mt?K(Mt):(S.textContent=`loading settings...`,S.classList.remove(`is-empty`),He.innerHTML=``);try{await En()}catch{S.textContent=`could not load settings.`}}function Tn(){Re.hidden=!0,document.body.classList.remove(`settings-open`),Le.focus()}async function En(){let e=await fetch(`/api/config`);if(!e.ok)throw Error(`Config request failed`);K(await e.json())}function Dn(e){let t=e?.value;return t==null?`n/a`:e?.kind===`ratio`?Number(t).toLocaleString(void 0,{maximumFractionDigits:2,minimumFractionDigits:0}):typeof t==`number`?t.toLocaleString():H(t)}function On(e,t=`metric-card`){return`
    <article class="${t}">
      <span>${U(e?.label)}</span>
      <strong>${V(Dn(e))}</strong>
    </article>
  `}function kn(e,t=``){Nt=e,$e.textContent=t||(e?.updated_at?`updated ${B(e.updated_at)}`:``),$e.classList.toggle(`is-empty`,!$e.textContent);let n=Array.isArray(e?.overview)?e.overview:[],r=Array.isArray(e?.sections)?e.sections:[],i=Array.isArray(e?.recent_scans)?e.recent_scans:[];et.innerHTML=n.map(e=>On(e)).join(``),tt.innerHTML=r.map(An).join(``),nt.innerHTML=i.length?i.map(jn).join(``):`<p class="empty-copy">no scan runs recorded.</p>`}function An(e){let t=Array.isArray(e?.metrics)?e.metrics:[];return`
    <section class="metrics-section">
      <div class="metrics-section-heading">
        <h3>${U(e?.title)}</h3>
      </div>
      <div class="metrics-section-grid">
        ${t.map(e=>On(e,`metric-card metric-card-compact`)).join(``)}
      </div>
    </section>
  `}function jn(e){let t=e?.scan_status??`unknown`,n=e?.started_at?B(e.started_at):`not started`,r=e?.finished_at?B(e.finished_at):`not finished`,i=e?.error?`<span>${U(e.error)}</span>`:``;return`
    <article class="metrics-scan-row">
      <div>
        <strong>${U(e?.company_name??`unknown company`)}</strong>
        <span>${U(n)} -> ${U(r)}</span>
        ${i}
      </div>
      <span class="metrics-status-pill">${U(t)}</span>
    </article>
  `}async function Mn(){Ze.hidden=!1,document.body.classList.add(`metrics-open`),Qe.focus(),Nt?kn(Nt):($e.textContent=`loading metrics...`,$e.classList.remove(`is-empty`),et.innerHTML=``,tt.innerHTML=``,nt.innerHTML=``);try{await Pn()}catch{$e.textContent=`could not load metrics.`}}function Nn(){Ze.hidden=!0,document.body.classList.remove(`metrics-open`),Xe.focus()}async function Pn(){let e=await fetch(`/api/metrics`);if(!e.ok)throw Error(`Metrics request failed`);kn(await e.json())}function Fn(e,t=``){Pt=e;let n=Number(e?.role_count??0),r=Array.isArray(e?.links)?e.links:[],i=Array.isArray(e?.paths)?e.paths:[];w.textContent=t||(e?.updated_at?`${n.toLocaleString()} roles | updated ${B(e.updated_at)}`:``),w.classList.toggle(`is-empty`,!w.textContent),ot.innerHTML=r.length?In(e):`<p class="empty-copy">no role transitions recorded yet.</p>`,st.innerHTML=i.length?i.map(Bn).join(``):`<p class="empty-copy">no role paths recorded yet.</p>`}function In(e){let t=Array.isArray(e?.nodes)?e.nodes:[],n=Array.isArray(e?.links)?e.links:[],r=zn(t,n),i=r.nodes,a=r.links,o=(r.flowLinks??n).map(e=>{let t=i.get(e.source),n=i.get(e.target),r=a.get(e);if(!t||!n||!r)return``;let o=r.width,s=n.x<t.x,c=Ln(e.target),l=r.priority?`0.42`:s?`0.28`:`0.34`,u=r.path??Rn({isBacktrack:s,sourceX:t.x+t.width,sourceY:r.sourceY,targetX:n.x,targetY:r.targetY,width:o});return`
        <path class="${[`sankey-link`,s?`sankey-link-backtrack`:``,r.priority?`sankey-link-priority`:``].filter(Boolean).join(` `)}" d="${u}" fill="${r.path?`none`:c}" fill-opacity="${l}" stroke="${c}" style="stroke-width: ${r.path?o:1}px">
          <title>${U(t.label)} to ${U(n.label)}: ${Number(e.value??0).toLocaleString()}</title>
        </path>
      `}).join(``),s=Array.from(i.values()).map(e=>{let t=Number(e.history_count??e.current_count??0),n=Number(e.value??t),i=n>0?n.toLocaleString():`0`,a=e.x>r.width-180,o=a?e.x-8:e.x+e.width+8,s=Math.max(24,e.y-e.height/2-16),c=a?`end`:`start`,l=Ln(e.id);return`
        <g class="sankey-node" transform="translate(${e.x}, ${e.y-e.height/2})">
          <rect width="${e.width}" height="${e.height}" rx="7" fill="${l}" stroke="${l}"></rect>
        </g>
        <g class="sankey-node-label" transform="translate(${o}, ${s})">
          <text text-anchor="${c}">${U(e.label)}</text>
          <text class="sankey-node-count" y="16" text-anchor="${c}">${U(i)} roles</text>
        </g>
      `}).join(``);return`
    <svg class="sankey-svg" viewBox="0 0 ${r.width} ${r.height}" role="img" aria-label="role state transition sankey diagram">
      <g>${o}</g>
      <g>${s}</g>
    </svg>
  `}function Ln(e){return bt.get(String(e).toLowerCase())??`#4f6472`}function Rn({isBacktrack:e,sourceX:t,sourceY:n,targetX:r,targetY:i,width:a}){let o=a/2,s=n-o,c=n+o,l=i-o,u=i+o;if(e){let e=Math.max(80,Math.abs(t-r)*.42);return[`M ${t} ${s}`,`C ${t-e} ${s}, ${r+e} ${l}, ${r} ${l}`,`L ${r} ${u}`,`C ${r+e} ${u}, ${t-e} ${c}, ${t} ${c}`,`Z`].join(` `)}let d=Math.max(46,(r-t)*.48);return[`M ${t} ${s}`,`C ${t+d} ${s}, ${r-d} ${l}, ${r} ${l}`,`L ${r} ${u}`,`C ${r-d} ${u}, ${t+d} ${c}, ${t} ${c}`,`Z`].join(` `)}function zn(e,r){let i=new Map([[`discovered`,0],[`interested`,1],[`disinterested`,2],[`applied`,2],[`oa`,3],[`interview`,3],[`rejected`,4],[`closed`,4],[`archived`,4]]),a=new Map,o=new Map;r.forEach(e=>{a.set(e.target,(a.get(e.target)??0)+Number(e.value??0)),o.set(e.source,(o.get(e.source)??0)+Number(e.value??0))});let s=e.filter(e=>Number(e?.history_count??e?.current_count??0)>0||a.has(e.id)||o.has(e.id)),c=new Set(s.map(e=>e.id)),l=r.filter(e=>c.has(e.source)&&c.has(e.target)&&Number(e.value??0)>0),u=e=>i.get(String(e).toLowerCase())??0,d=l.filter(e=>u(e.target)>=u(e.source)),ee=l.filter(e=>u(e.target)<u(e.source)),te={nodes:s.map(e=>({...e,fixedValue:Math.max(0,Number(e?.history_count??e?.current_count??0))})),links:d.map(e=>({...e}))},ne=t().nodeId(e=>e.id).nodeWidth(26).nodePadding(44).nodeAlign((e,t)=>Math.min(t-1,u(e.id))).extent([[92,88],[1014,634]]).iterations(32)(te),re=new Map;ne.nodes.forEach(e=>{re.set(e.id,{...e,x:e.x0,y:e.y0+(e.y1-e.y0)/2,width:e.x1-e.x0,height:Math.max(1.5,e.y1-e.y0),value:Number(e.fixedValue??e.value??0)})});let f=new Map,p=[],ie=n();ne.links.forEach(e=>{let t={source:e.source.id,target:e.target.id,value:e.value};p.push(t),f.set(t,{path:ie(e),width:Math.max(1.5,e.width),sourceY:e.y0,targetY:e.y1,priority:Number(e.value??0)>=20})});let ae=Math.max(.6,...ne.links.map(e=>Number(e.width??0)/Math.max(1,Number(e.value??0))));return ee.forEach(e=>{let t=re.get(e.source),n=re.get(e.target);if(!t||!n)return;let r=Math.max(1.5,Number(e.value??0)*ae),i={...e};p.push(i),f.set(i,{width:r,sourceY:t.y+t.height/2-r/2,targetY:n.y+n.height/2-r/2,priority:!1})}),p.sort((e,t)=>Number(e.value??0)-Number(t.value??0)),{flowLinks:p,height:720,links:f,nodes:re,width:1120}}function Bn(e){let t=Array.isArray(e?.path)?e.path:[];return`
    <article class="sankey-path-row">
      <div>
        <strong>${U(e?.company_name??`unknown company`)} / ${U(e?.title??`untitled role`)}</strong>
        <span>${t.map(e=>U(e)).join(` -> `)}</span>
      </div>
      <span class="metrics-status-pill">${Number(e?.loops_collapsed??0).toLocaleString()} loops</span>
    </article>
  `}async function Vn(){Re.hidden=!0,document.body.classList.remove(`settings-open`),it.hidden=!1,document.body.classList.add(`sankey-open`),at.focus(),Pt?Fn(Pt):(w.textContent=`loading role flow...`,w.classList.remove(`is-empty`),ot.innerHTML=``,st.innerHTML=``);try{await Un()}catch{w.textContent=`could not load role flow.`}}function Hn(){it.hidden=!0,document.body.classList.remove(`sankey-open`),Le.focus()}async function Un(){let e=await fetch(`/api/role-sankey`);if(!e.ok)throw Error(`Role sankey request failed`);Fn(await e.json())}async function Wn(e){let t=e.name;if(!t)return;let n=e.type===`checkbox`?!e.checked:Mt?.settings?.find(e=>e.key===t)?.value,r=e.type===`checkbox`?e.checked:e.value;q(!0),S.textContent=`saving settings...`,S.classList.remove(`is-empty`);try{let e=await fetch(`/api/config`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({[t]:r})});if(!e.ok)throw Error(`Config update failed`);K(await e.json(),`settings saved.`)}catch{e.type===`checkbox`?e.checked=n:n!==void 0&&(e.value=n),S.textContent=`could not save settings.`,q(!1)}}async function Gn(){Ye.disabled=!0,S.textContent=`clearing recommendation history...`,S.classList.remove(`is-empty`);try{let e=await fetch(`/api/recommendation-history/clear`,{method:`POST`});if(!e.ok)throw Error(`Recommendation history clear failed`);let t=await e.json();K(t.config,`cleared ${t.deleted_count} saved decisions.`)}catch{S.textContent=`could not clear recommendation history.`,Ye.disabled=!1}}async function Kn(){let e=Ge.value.trim();if(!e){S.textContent=`central api url is required.`,S.classList.remove(`is-empty`);return}let t={central_api_url:e},n=Ke.value.trim();n&&(t.central_passkey=n),q(!0),S.textContent=`saving central settings...`,S.classList.remove(`is-empty`);try{let e=await fetch(`/api/config`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(t)});if(!e.ok)throw Error(`Central settings update failed`);K(await e.json(),`central settings saved.`)}catch{S.textContent=`could not save central settings.`,q(!1)}}async function qn(){C.disabled=!0,S.textContent=`syncing remote company ids...`,S.classList.remove(`is-empty`);try{let e=await fetch(`/api/central/resolve-companies`,{method:`POST`});if(!e.ok)throw Error(`Central company sync failed`);let t=await e.json(),n=t.result??{},r=t.pulled_companies,i=r?` remote: ${Number(r.created??0)} created, ${Number(r.linked??0)} linked, ${Number(r.existing??0)} existing.`:``;K(t.config,`company sync: ${Number(n.linked??0)} matched, ${Number(n.created??0)} created, ${Number(n.needs_review??0)} review, ${Number(n.failed??0)} failed.${i}`),t.companies&&(R=t.companies,Zn(t.companies.companies))}catch{S.textContent=`could not sync companies.`,C.disabled=!Ge.value.trim()}}async function Jn(){let e=await fetch(`/api/central/resolve-companies`,{method:`POST`});if(!e.ok)throw Error(`Central company sync failed`);let t=await e.json();t.companies&&(R=t.companies,Zn(t.companies.companies))}async function Yn(){let e=Jn().catch(()=>{});await Promise.all([Y().catch(()=>{i.innerHTML=`<p class="empty-copy">could not load jobs.</p>`}),ar().catch(()=>{gt.textContent=`could not load companies.`})]),await e}async function Xn(){if(window.confirm(`Update callumployed and restart the tracker?`)){q(!0),ct.disabled=!0,S.textContent=`updating callumployed; tracker will restart shortly...`,S.classList.remove(`is-empty`);try{if(!(await fetch(`/api/app/update`,{method:`POST`})).ok)throw Error(`App update failed`);S.textContent=`update started. reconnect in a moment.`}catch{S.textContent=`could not start update.`,q(!1)}}}function J(e,t=``){R=e;let n=Array.isArray(e?.companies)?e.companies:[];if(Zn(n),T.textContent=t||`${n.length} ${n.length===1?`company`:`companies`} stored`,T.classList.toggle(`is-empty`,n.length===0&&!t),n.length===0){E.innerHTML=`<p class="empty-copy">no companies yet.</p>`;return}E.innerHTML=n.map(e=>Qn(e)).join(``)}function Zn(e){Ft=Array.isArray(e)?e:[],ht.innerHTML=Ft.map(e=>`<option value="${V(e.name)}"></option>`).join(``)}function Qn(e){let t=Array.isArray(e.career_pages)?e.career_pages:[],n=B(e.updated_at),r=$n(e.prestige_tier),i=Number(e.scan_count??0),a=Number(e.discovered_role_count??0),o=i>0&&a===0?`<span class="company-discovery-status">Discovered 0 potential roles</span>`:``;return`
    <details class="company-panel ${r}" data-company-id="${e.id}">
      <summary class="company-summary">
        <span class="company-chevron">></span>
        <span class="company-summary-main">
          <span class="company-name">${U(e.name)}</span>
          <span class="company-summary-meta">${t.length} ${t.length===1?`link`:`links`}${n?` | updated ${U(n)}`:``}</span>
          ${o}
        </span>
      </summary>
      <div class="company-body">
        <div class="company-info">
          <label class="company-notes-field">
            <span>notes</span>
            <textarea data-company-notes="${e.id}" rows="3">${V(e.notes??``)}</textarea>
          </label>
          <label>
            <span>tier</span>
            <select data-company-tier="${e.id}">
              ${er(e.prestige_tier)}
            </select>
          </label>
          <div>
            <span>browser wait</span>
            <strong>${Number(e.browser_extra_wait_ms??0)}ms</strong>
          </div>
        </div>
        <div class="company-links">
          ${t.length>0?t.map(e=>tr(e)).join(``):`<p class="company-empty-links">no career links yet.</p>`}
        </div>
        <section class="company-link-panel" aria-label="add career link">
          <form class="company-link-form" data-company-link-form="${e.id}">
            <input name="label" type="text" placeholder="label" aria-label="career link label" />
            <input name="url" type="url" placeholder="https://..." aria-label="career link url" required />
            <button class="company-link-add" type="submit" aria-label="add career link" title="add career link">
              ${Ut()}
            </button>
          </form>
        </section>
        <div class="company-danger-row">
          <button class="company-delete-button" type="button" data-delete-company="${e.id}">
            ${Wt()}
            <span>deactivate company</span>
          </button>
        </div>
      </div>
    </details>
  `}function $n(e){let t=String(e??``);return[`0`,`1`,`2`,`3`,`4`].includes(t)?`company-tier-${t}`:`company-tier-unset`}function er(e){let t=String(e??``);return[``,`0`,`1`,`2`,`3`,`4`].map(e=>{let n=e?`tier ${e}`:`not set`,r=e===t?` selected`:``;return`<option value="${V(e)}"${r}>${U(n)}</option>`}).join(``)}function tr(e){let t=e.label?U(e.label):`career page`,n=V(e.url);return`
    <div class="company-link-row" data-career-page-id="${e.id}">
      <a class="company-link-url" href="${n}" target="_blank" rel="noreferrer">
        <span class="company-link-label">${t}</span>
        <span class="company-link-text">${V(e.url)}</span>
      </a>
      <button class="company-link-delete" type="button" data-delete-career-page="${e.id}" aria-label="delete ${t} link" title="delete link">
        ${Wt()}
      </button>
    </div>
  `}async function nr(){lt.hidden=!1,document.body.classList.add(`companies-open`),ut.focus(),R?J(R):(T.textContent=`loading companies...`,T.classList.remove(`is-empty`),E.innerHTML=``);try{await ir()}catch{T.textContent=`could not load companies.`}}function rr(){lt.hidden=!0,document.body.classList.remove(`companies-open`),De.focus()}async function ir(e=``){let t=await fetch(`/api/companies`);if(!t.ok)throw Error(`Companies request failed`);J(await t.json(),e)}async function ar(){let e=await fetch(`/api/companies`);if(!e.ok)throw Error(`Companies request failed`);Zn((await e.json()).companies)}async function or(e){let t=new FormData(e),n={name:String(t.get(`name`)??``),career_url:String(t.get(`career_url`)??``),notes:String(t.get(`notes`)??``)};T.textContent=`adding company...`;let r=await fetch(`/api/companies`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(n)});if(!r.ok)throw Error(`Company create failed`);e.reset(),J(await r.json(),`company added.`),Y(z()).catch(()=>{})}async function sr(e){let t=e.dataset.companyLinkForm;if(!t)return;let n=new FormData(e),r={label:String(n.get(`label`)??``),url:String(n.get(`url`)??``)};T.textContent=`adding link...`;let i=await fetch(`/api/companies/${encodeURIComponent(t)}/career-pages`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(r)});if(!i.ok)throw Error(`Career page create failed`);e.reset(),J(await i.json(),`link added.`)}async function cr(e){T.textContent=`deleting link...`;let t=await fetch(`/api/company-career-pages/${encodeURIComponent(e)}`,{method:`DELETE`});if(!t.ok)throw Error(`Career page delete failed`);J(await t.json(),`link deleted.`)}async function lr(e){T.textContent=`deactivating company...`;let t=await fetch(`/api/companies/${encodeURIComponent(e)}`,{method:`DELETE`});if(!t.ok)throw Error(`Company deactivate failed`);J(await t.json(),`company deactivated.`),Y(z()).catch(()=>{})}function ur(){let e=mt.value.trim().toLocaleLowerCase();return Ft.find(t=>t.name.toLocaleLowerCase()===e)}async function dr(e){let t=ur();if(!t?.id){gt.textContent=`pick a saved company.`;return}let n=new FormData(e),r={company_id:t.id,role_url:String(n.get(`role_url`)??``)};gt.textContent=`adding role...`;let i=await fetch(`/api/roles`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(r)});if(!i.ok)throw Error(`Role create failed`);let a=await i.json();a.tracker?hn(a.tracker):await Y(z()),pt.value=``;let o=a.role?.title?H(a.role.title):`role`;gt.textContent=a.scan_error?`${o} added; scan could not finish.`:`${o} added.`}function fr(e){return(Array.isArray(R?.companies)?R.companies:[]).find(t=>String(t.id)===String(e))}function pr(e){T.textContent=e,T.classList.remove(`is-empty`)}function mr(e){window.clearTimeout(It.get(e)),It.set(e,window.setTimeout(()=>{hr(e).catch(()=>{pr(`could not save company.`)})},700))}async function hr(e){let t=E.querySelector(`[data-company-id="${CSS.escape(String(e))}"]`);if(!t)return;let n=t.querySelector(`[data-company-notes="${CSS.escape(String(e))}"]`),r=t.querySelector(`[data-company-tier="${CSS.escape(String(e))}"]`),i=fr(e),a={notes:n?.value??i?.notes??``,prestige_tier:r?.value??i?.prestige_tier??``};i&&(i.notes=a.notes,i.prestige_tier=a.prestige_tier),gr(t,a.prestige_tier),pr(`saving company...`);let o=await fetch(`/api/companies/${encodeURIComponent(e)}`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(a)});if(!o.ok)throw Error(`Company update failed`);R=await o.json(),pr(`company saved.`),_r(e)}function gr(e,t){e.classList.remove(`company-tier-unset`,`company-tier-0`,`company-tier-1`,`company-tier-2`,`company-tier-3`,`company-tier-4`),e.classList.add($n(t))}function _r(e){let t=E.querySelector(`[data-company-id="${CSS.escape(String(e))}"]`),n=fr(e);if(!t||!n)return;let r=Array.isArray(n.career_pages)?n.career_pages:[],i=B(n.updated_at),a=t.querySelector(`.company-summary-meta`);a&&(a.textContent=`${r.length} ${r.length===1?`link`:`links`}${i?` | updated ${i}`:``}`)}async function vr(){let e=await fetch(`/api/scan/status`);if(e.status===404){y.disabled=!0,b.hidden=!0,b.classList.add(`scan-error`),x.textContent=`restart server to enable scanning`;return}if(!e.ok)throw Error(`Scan status request failed`);gn(await e.json())}function yr(){kt===null&&(kt=window.setInterval(()=>{vr().catch(()=>{})},3e3))}async function br(){y.disabled=!0,y.textContent=`starting...`;try{let e=await fetch(`/api/scan/all`,{method:`POST`});if(e.status===404){y.disabled=!0,y.textContent=`scan roles`,b.hidden=!0,b.classList.add(`scan-error`),x.textContent=`restart server to enable scanning`;return}if(!e.ok&&e.status!==409)throw Error(`Scan start failed`);gn(await e.json()),yr()}catch{y.disabled=!1,y.textContent=`scan roles`,b.hidden=!0,b.classList.add(`scan-error`),x.textContent=`could not start scan`}}async function xr(){y.disabled=!0,y.textContent=`cancelling...`;try{let e=await fetch(`/api/scan/cancel`,{method:`POST`});if(e.status===404){y.disabled=!0,y.textContent=`scan roles`,b.hidden=!0,b.classList.add(`scan-error`),x.textContent=`restart server to enable scanning`;return}if(!e.ok&&e.status!==409)throw Error(`Scan cancel failed`);gn(await e.json()),yr()}catch{y.disabled=!1,y.textContent=`cancel scan`,b.hidden=!1,b.classList.add(`scan-error`),x.textContent=`could not cancel scan`}}async function Y(e=``){i.innerHTML=`<p class="empty-copy">loading jobs...</p>`;let t=new URLSearchParams;e&&t.set(`q`,e);let n=await fetch(`/api/tracker?${t.toString()}`);if(!n.ok)throw Error(`Tracker request failed`);hn(await n.json())}async function Sr(e={}){let t=await fetch(`/api/application-materials`);if(!t.ok)throw Error(`Application materials request failed`);$t(await t.json(),e)}async function Cr(e){if(e){if(!e.name.toLowerCase().endsWith(`.tex`)){Jt(O,`resume must be a .tex file.`);return}ie.disabled=!0,Jt(O,`uploading...`);try{let t=await e.text();if(!(await fetch(`/api/master-resume`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({filename:e.name,content:t})})).ok)throw Error(`Master resume upload failed`);await Sr()}catch{Jt(O,`could not save resume.`),G()}finally{p.value=``,ie.disabled=!1}}}async function wr(e){let t=Array.from(e??[]);if(t.length!==0){se.disabled=!0,Qt(k,`uploading ${t.length} ${t.length===1?`resource`:`resources`}...`);try{for(let e of t)if(!(await fetch(`/api/resume-resources`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({filename:e.name,content_base64:await Or(e)})})).ok)throw Error(`Resume resource upload failed`);await Sr()}catch{Qt(k,`could not save every resource.`),G()}finally{oe.value=``,se.disabled=!1}}}async function Tr(e){let t=Array.from(e??[]);if(t.length!==0){de.disabled=!0,Yt(A,`uploading ${t.length} ${t.length===1?`example`:`examples`}...`);try{for(let e of t){let t={filename:e.name};if(e.name.toLowerCase().endsWith(`.docx`)?t.content_base64=await Or(e):t.content=await e.text(),!(await fetch(`/api/cover-letter-examples`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(t)})).ok)throw Error(`Cover letter example upload failed`)}await Sr()}catch{Yt(A,`could not save every example.`),G()}finally{ue.value=``,de.disabled=!1}}}async function Er(e){let t=Array.from(e??[]);if(t.length!==0){he.disabled=!0,Xt(j,`uploading ${t.length} ${t.length===1?`note`:`notes`}...`);try{for(let e of t){let t=e.name.toLowerCase(),n={filename:e.name};if(t.endsWith(`.pdf`)||t.endsWith(`.docx`)?n.content_base64=await Or(e):n.content=await e.text(),!(await fetch(`/api/experience-notes`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(n)})).ok)throw Error(`Experience note upload failed`)}F.clear(),await Sr()}catch{Xt(j,`could not save every note.`),G()}finally{me.value=``,he.disabled=!1}}}async function Dr(){if(!(m.disabled||j.length===0)){m.disabled=!0,m.textContent=`indexing...`,h.hidden=!1,h.textContent=`Building section pages and a targeted retrieval index...`,_e.textContent=`indexing...`;try{if(!(await fetch(`/api/application-materials/index`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({})})).ok)throw Error(`Application material indexing failed`);await Sr()}catch{h.hidden=!1,h.textContent=`Could not index application materials. Try again.`,_e.textContent=`index failed`}finally{m.disabled=j.length===0,m.textContent=M?.status===`ready`?`reindex materials`:`index materials`}}}function Or(e){return new Promise((t,n)=>{let r=new FileReader;r.addEventListener(`load`,()=>{let e=String(r.result??``);t(e.includes(`,`)?e.split(`,`,2)[1]:e)}),r.addEventListener(`error`,()=>n(r.error)),r.readAsDataURL(e)})}c.addEventListener(`submit`,e=>{e.preventDefault(),Y(l.value.trim()),zt()}),a.addEventListener(`click`,()=>{if(z()){Y();return}Rt()}),l.addEventListener(`keydown`,e=>{e.key===`Escape`&&(e.stopPropagation(),zt())}),u.addEventListener(`click`,zt),s.addEventListener(`click`,zt),ie.addEventListener(`click`,()=>{p.click()}),p.addEventListener(`change`,()=>{Cr(p.files?.[0])}),se.addEventListener(`click`,()=>{oe.click()}),oe.addEventListener(`change`,()=>{wr(oe.files)}),de.addEventListener(`click`,()=>{ue.click()}),ue.addEventListener(`change`,()=>{Tr(ue.files)}),he.addEventListener(`click`,()=>{me.click()}),me.addEventListener(`change`,()=>{Er(me.files)}),m.addEventListener(`click`,()=>{Dr()}),ee.addEventListener(`click`,()=>{en(ee.getAttribute(`aria-expanded`)===`true`)}),y.addEventListener(`click`,()=>{if(jt?.scanning){xr();return}br()}),i.addEventListener(`click`,e=>{let t=e.target.closest(`[data-review-role-id]`);if(t){Vr(t.dataset.reviewRoleId);return}let n=e.target.closest(`[data-prep-role-id]`);if(n){Ur(n.dataset.prepRoleId);return}let r=e.target.closest(`.job-action`);if(r){kr(r);return}let i=e.target.closest(`.pane-toggle`);if(!i)return;let a=i.parentElement.querySelector(`.pane-body`),o=i.getAttribute(`aria-expanded`)===`true`;i.setAttribute(`aria-expanded`,String(!o)),i.querySelector(`.chevron`).textContent=o?`>`:`v`,a.hidden=o,Fi()});async function kr(e){let{roleId:t,status:n}=e.dataset;if(!t||!n)return;let r=e.closest(`.job-actions`),i=e.closest(`.job`);r.querySelectorAll(`button`).forEach(e=>{e.disabled=!0}),e.textContent=`updating...`;try{let e=await fetch(`/api/roles/${encodeURIComponent(t)}/status`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({status:n})});if(!e.ok)throw Error(`Status update failed`);Ar((await e.json()).role,i)}catch{r.querySelectorAll(`button`).forEach(e=>{e.disabled=!1}),e.textContent=n===`disinterested`?`disinterested`:n.toLowerCase()}}function Ar(e,t){if(!e||!D)return;let n=t?.closest(`.status-pane`)?.dataset.bucket??e.role_status,r=e.role_status,i=Mr(e,n,r);Nr(n,r),Pr(n,r),qt(),Lr(D.statuses),zr(D.statuses),Fr(t,i,n,r),Fi()}function jr(e){if(!e||!D)return null;let t=null;return D.statuses.forEach(n=>{let r=n.jobs.findIndex(t=>String(t.id)===String(e.id));r!==-1&&(t={...n.jobs[r],...e},n.jobs[r]=t)}),Lr(D.statuses),zr(D.statuses),t}function Mr(e,t,n){let r=e;D.statuses.forEach(t=>{let n=t.jobs.findIndex(t=>String(t.id)===String(e.id));n!==-1&&(r={...t.jobs[n],...e},t.jobs.splice(n,1),t.count=t.jobs.length)});let i=D.statuses.find(e=>e.key===n);return i&&(i.jobs.unshift(r),i.count=i.jobs.length),r}function Nr(e,t){D.statuses.forEach(e=>{let t=document.querySelector(`#status-${CSS.escape(e.key)}`);t?.classList.toggle(`empty`,e.count===0);let n=t?.querySelector(`.count`);n&&(n.textContent=e.count)}),[e,t].forEach(e=>{Ir(document.querySelector(`#status-${CSS.escape(e)}`))})}function Pr(e,t){if(!D.stats)return;let n=yt.has(e),r=yt.has(t);if(n===r){Kt(D.stats);return}D.stats.applications_total=Number(D.stats.applications_total??0)+(r?1:-1),Kt(D.stats)}function Fr(e,t,n,r){let i=document.querySelector(`#status-${CSS.escape(r)}`),a=i?.querySelector(`.pane-body`);if(!e||!i||!a)return;e.remove(),Ir(document.querySelector(`#status-${CSS.escape(n)}`)),a.hidden=!1;let o=i.querySelector(`.pane-toggle`);o?.setAttribute(`aria-expanded`,`true`);let s=o?.querySelector(`.chevron`);s&&(s.textContent=`v`);let c=a.querySelector(`.jobs`);c||=(a.innerHTML=`<div class="jobs"></div>`,a.querySelector(`.jobs`)),c.insertAdjacentHTML(`afterbegin`,rn(t,r)),Ir(i)}function Ir(e){if(!e)return;let t=e.querySelector(`.pane-body`);if(!t)return;let n=t.querySelector(`.jobs`),r=!!n?.querySelector(`.job`),i=t.querySelector(`.empty-copy`);if(r){i?.remove();return}n?.remove(),i||t.insertAdjacentHTML(`beforeend`,`<p class="empty-copy">no jobs in this status.</p>`)}function Lr(e){ve.disabled=Rr(e).length===0,ve.setAttribute(`aria-label`,`review discovered`),ve.innerHTML=`<span class="review-discovered-label">review discovered</span>`}function Rr(e=D?.statuses??[]){return e.find(e=>e.key===`discovered`)?.jobs??[]}function zr(e){ye.disabled=Br(e).length===0,ye.setAttribute(`aria-label`,`prep interested`),ye.innerHTML=`<span class="review-discovered-label">prep interested</span>`}function Br(e=D?.statuses??[]){return e.find(e=>e.key===`interested`)?.jobs??[]}function Vr(e=null){let t=[...Rr()],n=e==null?null:String(e);if(n){let e=t.findIndex(e=>String(e.id)===n);if(e>0){let[n]=t.splice(e,1);t.unshift(n)}}N=t,g.hidden=!1,document.body.classList.add(`review-open`),Gr()}function Hr(){g.hidden=!0,document.body.classList.remove(`review-open`),N=[]}function Ur(e=null){let t=[...Br()].sort((e,t)=>Number(!!t.prep_started)-Number(!!e.prep_started)),n=e==null?null:String(e);if(n){let e=t.findIndex(e=>String(e.id)===n);if(e>0){let[n]=t.splice(e,1);t.unshift(n)}}P=t,_.hidden=!1,document.body.classList.add(`prep-open`),oi()}function Wr(){_.hidden=!0,document.body.classList.remove(`prep-open`),P=[]}function Gr(e=``){let t=N[0],n=N.length,r=t?Kr(t):``;if(be.textContent=n>0?`review queue`:`review complete`,xe.textContent=n>0?`${n} discovered ${n===1?`role`:`roles`} in queue`:``,g.querySelectorAll(`.review-action`).forEach(e=>{e.disabled=n===0}),!t){Se.innerHTML=`
      <div class="review-empty">
        <h3>no discovered jobs left.</h3>
        <p>everything in this queue has been handled or moved out of discovered.</p>
      </div>
    `;return}Se.innerHTML=`
    ${e?`<p class="review-message">${V(e)}</p>`:``}
    ${r?`<p class="review-message review-message-warning">${V(r)}</p>`:``}
    <div class="review-title-row">
      <p class="review-company">${U(t.company_name)}</p>
      ${Gt(t.title,t.role_url,`review-role-title`)}
    </div>
    <dl class="review-details review-primary-details">
      ${X(`location`,t.location,!1,`review-location-detail`)}
      ${X(`first`,B(t.first_seen_at))}
      ${X(`last`,B(t.last_seen_at))}
    </dl>
    ${qr(t.description)}
    <dl class="review-details review-technical-details">
      ${X(`notes`,t.notes,!1,`review-wide-detail`)}
      ${X(`company id`,t.company_id)}
      ${X(`role id`,t.id)}
      ${X(`status`,t.role_status)}
      ${X(`posting id`,t.posting_id)}
      ${X(`created`,B(t.created_at))}
      ${X(`updated`,B(t.updated_at))}
      ${X(`url`,t.role_url,!0,`review-wide-detail`)}
    </dl>
  `}function Kr(e){let t=Number(e.review_later_count??0);return t<=_t?``:`role review has been postponed ${t} times. it is recommended to set it to disinterested.`}function X(e,t,n=!1,r=``){if(!t)return``;let i=n?`<a href="${V(t)}" target="_blank" rel="noreferrer">${U(t)}</a>`:U(t);return`
    <div class="review-detail ${V(r)}">
      <dt>${U(e)}</dt>
      <dd>${i}</dd>
    </div>
  `}function qr(e){return e?`
    <div class="review-detail review-description">
      <dt>description</dt>
      <dd>${Jr(e)}</dd>
    </div>
  `:``}function Jr(e){let t=Yr(String(e)).replace(/\u00a0/g,` `);if(Xr(t))return Zr(t);let n=t.split(/\r?\n/).map(e=>e.trim()).filter(Boolean),r=[],i=[],a=()=>{i.length!==0&&(r.push(`<ul>${i.map(e=>`<li>${e}</li>`).join(``)}</ul>`),i=[])};return n.forEach(e=>{let t=e.match(/^#{2,3}\s+(.+)$/);if(t){a(),r.push(`<h3>${U(t[1])}</h3>`);return}if(ii(e)){a(),r.push(`<h3>${U(e.replace(/:$/,``))}</h3>`);return}let n=e.match(/^[-*]\s+(.+)$/);if(n){i.push(U(n[1]));return}a(),r.push(`<p>${U(e)}</p>`)}),a(),r.join(``)}function Yr(e){let t=document.createElement(`textarea`);return t.innerHTML=e,t.value}function Xr(e){return/<\/?(?:a|br|div|em|h[1-6]|li|ol|p|span|strong|ul)\b/i.test(e)}function Zr(e){let t=document.createElement(`template`);t.innerHTML=e;let n=[];return Qr(t.content.childNodes,n),n.join(``)}function Qr(e,t){e.forEach(e=>{if(e.nodeType===Node.TEXT_NODE){let n=Z(e.textContent);n&&t.push(`<p>${U(n)}</p>`);return}if(e.nodeType!==Node.ELEMENT_NODE)return;let n=e,r=n.tagName.toLowerCase();if(r===`script`||r===`style`||r===`br`)return;if(/^h[1-6]$/.test(r)){ei(t,n.textContent);return}if(r===`ul`||r===`ol`){let e=ti(n);e&&t.push(e);return}if(r===`p`){$r(n,t);return}let i=Array.from(n.children).some(e=>[`DIV`,`H1`,`H2`,`H3`,`H4`,`H5`,`H6`,`OL`,`P`,`UL`].includes(e.tagName));if([`article`,`div`,`section`].includes(r)&&i){Qr(n.childNodes,t);return}let a=Array.from(n.children).filter(e=>[`UL`,`OL`].includes(e.tagName)),o=Z(ni(n));if(o&&(ri(o,n)?ei(t,o):t.push(`<p>${U(o)}</p>`)),a.length>0){a.forEach(e=>{let n=ti(e);n&&t.push(n)});return}!o&&i&&Qr(n.childNodes,t)})}function $r(e,t){if(!e.querySelector(`br`)){let n=Z(ni(e));if(!n)return;ri(n,e)?ei(t,n):t.push(`<p>${U(n)}</p>`);return}let n=``,r=()=>{let r=Z(n);n=``,r&&(ri(r,e)?ei(t,r):t.push(`<p>${U(r)}</p>`))};e.childNodes.forEach(e=>{if(e.nodeType===Node.ELEMENT_NODE&&e.tagName.toLowerCase()===`br`){r();return}n+=` ${e.textContent??``}`}),r()}function ei(e,t){let n=Z(t).replace(/:$/,``);n&&e.push(`<h3>${U(n)}</h3>`)}function ti(e){let t=Array.from(e.children).filter(e=>e.tagName===`LI`).map(e=>{let t=Z(ni(e)),n=Array.from(e.children).filter(e=>[`UL`,`OL`].includes(e.tagName)).map(e=>ti(e)).filter(Boolean).join(``);return t||n?`<li>${U(t)}${n}</li>`:``}).filter(Boolean);return t.length>0?`<ul>${t.join(``)}</ul>`:``}function ni(e){let t=e.cloneNode(!0);return t.querySelectorAll(`ul, ol`).forEach(e=>{e.remove()}),t.textContent}function Z(e){return String(e??``).replace(/\s+/g,` `).trim()}function ri(e,t){let n=e.replace(/:$/,``).trim();return!n||n.length>90?!1:ii(n)||/:$/.test(e)?!0:/[.!?]$/.test(n)||n.split(/\s+/).length>10?!1:t.querySelector(`strong, b, u`)?!0:ii(n)}function ii(e){return xt.test(String(e).trim())}async function ai(e){let t=N[0];if(!t)return;if(e===`later`){g.querySelectorAll(`.review-action`).forEach(e=>{e.disabled=!0});try{let e=await ki(t.id);N.shift(),jr(e),Gr(`moved out of this review pass.`)}catch{Gr(`could not postpone that role. try again.`)}finally{g.querySelectorAll(`.review-action`).forEach(e=>{e.disabled=N.length===0})}return}if(![`interested`,`disinterested`].includes(e))return;let n=g.querySelectorAll(`.review-action`);n.forEach(e=>{e.disabled=!0});try{let n=await Ai(t.id,e);N.shift(),Gr(e===`interested`?`marked interested.`:`marked disinterested.`),Ar(n,document.querySelector(`.job[data-role-id="${CSS.escape(String(t.id))}"]`))}catch{n.forEach(e=>{e.disabled=!1}),Gr(`could not update that role. try again.`)}}async function oi(e=``){let t=P[0],n=P.length;if(we.textContent=n>0?`prep queue`:`prep complete`,Te.textContent=n>0?`${n} interested ${n===1?`role`:`roles`} in queue`:``,_.querySelectorAll(`.review-action`).forEach(e=>{e.disabled=n===0}),!t){v.innerHTML=`
      <div class="review-empty">
        <h3>no interested jobs left.</h3>
        <p>everything in this queue has been prepped, moved, or postponed.</p>
      </div>
    `;return}v.innerHTML=`
    ${e?`<p class="review-message">${V(e)}</p>`:``}
    <section class="prep-role-hero" aria-label="role overview">
      <div class="review-title-row">
        <div class="prep-role-eyebrow">
          <p class="review-company">${U(t.company_name)}</p>
          <span>application workspace</span>
        </div>
        ${Gt(t.title,t.role_url,`review-role-title`)}
      </div>
      <dl class="review-details review-primary-details">
        ${X(`location`,t.location,!1,`review-location-detail`)}
        ${X(`last`,B(t.last_seen_at))}
        ${X(`updated`,B(t.updated_at))}
      </dl>
      <nav class="prep-workspace-nav" aria-label="prep sections">
        <button type="button" data-prep-section-target="prep-resume-${t.id}">
          <span>01</span> résumé
        </button>
        <button type="button" data-prep-section-target="prep-cover-letter-${t.id}">
          <span>02</span> cover letter
        </button>
        <button type="button" data-prep-section-target="prep-description-${t.id}">
          <span>03</span> role details
        </button>
        <button type="button" data-prep-section-target="prep-chat-${t.id}">
          <span>04</span> role chat
        </button>
      </nav>
    </section>
    <div class="prep-workspace">
      ${si(t)}
      ${di(t)}
      ${ci(t.id,t.description)}
      ${li(t)}
    </div>
  `,W(),_i(t.id).then(e=>{!e||P[0]?.id!==t.id||(I.set(t.id,e),v.querySelector(`.prep-resume`)?.replaceWith($(si(t,{resume:e}))),W())}).catch(()=>{}),Oi(t.id).then(e=>{!e||P[0]?.id!==t.id||(L.set(t.id,e),v.querySelector(`.prep-cover-letter`)?.replaceWith($(di(t,{coverLetter:e}))),W())}).catch(()=>{})}function si(e,t={}){let n=I.get(e.id),r=t.resume??n,i=t.tweaks??wt.get(e.id)??``,a=`/api/roles/${encodeURIComponent(e.id)}/resume.pdf`;return t.loading?`
      <details class="prep-panel prep-resume" id="prep-resume-${e.id}" open>
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
    <details class="prep-panel prep-resume" id="prep-resume-${e.id}" open>
      <summary class="prep-analysis-header">
        <span class="prep-accordion-icon" aria-hidden="true"></span>
        <h3>resume</h3>
        <div class="prep-summary-actions">
          <span>${r.pdf_base64?`preview ready`:`latex ready`}</span>
          ${r.pdf_base64?`<a class="prep-summary-action prep-cover-pdf-link" href="${V(a)}" target="_blank" rel="noreferrer">view</a>`:``}
        </div>
      </summary>
      <p class="prep-overview">${U(r.summary??`Saved resume for this role.`)}</p>
      ${Q(e)}
      <section class="prep-generation-controls" aria-label="résumé refinement">
        <div class="prep-control-heading">
          <span>refine this version</span>
          <p>Describe a focused change, then regenerate without losing the saved source.</p>
        </div>
        <label class="prep-cover-tweaks prep-resume-tweaks">
          <span>tweak instructions</span>
          <textarea
            data-prep-resume-tweaks="${e.id}"
            rows="4"
            placeholder="paste or write a resume tweak prompt..."
          >${V(i)}</textarea>
        </label>
        <div class="prep-cover-actions">
          <button type="button" data-prep-resume-regenerate="${e.id}">
            regenerate with tweaks
          </button>
        </div>
      </section>
      <div class="prep-document-workspace">
        <label class="prep-cover-latex prep-document-source">
          <span>LaTeX source</span>
          <textarea
            data-prep-resume-latex="${e.id}"
            spellcheck="false"
          >${V(r.latex??``)}</textarea>
        </label>
        <section class="prep-document-preview" aria-label="résumé preview">
          <div class="prep-preview-heading">
            <span>document preview</span>
            <p>Updates automatically after the source is saved.</p>
          </div>
          ${r.pdf_base64?`
                <iframe class="prep-cover-pdf" title="resume PDF preview" src="${V(a)}"></iframe>
              `:`<p class="prep-cover-path">PDF preview unavailable.</p>`}
        </section>
      </div>
    </details>
  `:`
      <details class="prep-panel prep-resume" id="prep-resume-${e.id}" open>
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
    `}function ci(e,t){return`
    <details class="prep-panel prep-description-panel" id="prep-description-${e}">
      <summary class="prep-analysis-header">
        <span class="prep-accordion-icon" aria-hidden="true"></span>
        <h3>description</h3>
      </summary>
      ${qr(t)}
    </details>
  `}function li(e,t={}){let n=t.messages??Tt.get(e.id)??[],r=!!t.loading;return`
    <details class="prep-panel prep-role-chat" id="prep-chat-${e.id}">
      <summary class="prep-analysis-header">
        <span class="prep-accordion-icon" aria-hidden="true"></span>
        <h3>chat about this role</h3>
        <span>${n.length?`${n.length} messages`:`ready`}</span>
      </summary>
      <div class="prep-role-chat-log" aria-live="polite">
        ${n.length?n.map(ui).join(``):`<p class="prep-role-chat-empty">ask about fit, risks, resume emphasis, or cover letter angle.</p>`}
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
  `}function ui(e){let t=e?.role===`assistant`?`assistant`:`user`;return`
    <article class="prep-role-chat-message prep-role-chat-message-${t}">
      <span>${t}</span>
      <p>${U(e?.content??``)}</p>
    </article>
  `}function di(e,t={}){let n=L.get(e.id),r=t.coverLetter??n,i=t.tweaks??r?.tweaks??``,a=`/api/roles/${encodeURIComponent(e.id)}/cover-letter.pdf`;return t.loading?`
      <details class="prep-panel prep-cover-letter" id="prep-cover-letter-${e.id}" open>
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
    <details class="prep-panel prep-cover-letter" id="prep-cover-letter-${e.id}" open>
      <summary class="prep-analysis-header">
        <span class="prep-accordion-icon" aria-hidden="true"></span>
        <h3>cover letter</h3>
        <div class="prep-summary-actions">
          <span>${r?.pdf_base64?`preview ready`:r?`latex ready`:`not generated`}</span>
          ${r?.pdf_base64?`<a class="prep-summary-action prep-cover-pdf-link" href="${V(a)}" target="_blank" rel="noreferrer">view</a>`:``}
        </div>
      </summary>
      ${r?`<p class="prep-overview">${U(r.summary??`cover letter generated`)}</p>`:`<p class="prep-overview">generate a LaTeX cover letter from the resume, posting, and stored examples.</p>`}
      <section class="prep-generation-controls" aria-label="cover letter generation">
        <div class="prep-control-heading">
          <span>${r?`refine this version`:`create a tailored draft`}</span>
          <p>Use the role, résumé, and saved examples to shape the letter.</p>
        </div>
        ${r?`
              <label class="prep-cover-tweaks">
                <span>tweak instructions</span>
                <textarea
                  data-prep-cover-letter-tweaks="${e.id}"
                  rows="3"
                  placeholder="make it warmer, cut a paragraph, emphasize systems work..."
                >${V(i)}</textarea>
              </label>
            `:``}
        <div class="prep-cover-actions">
          <button type="button" data-prep-cover-letter="${e.id}">
            ${r?`regenerate`:`generate cover letter`}
          </button>
        </div>
      </section>
      ${r?`
            <div class="prep-document-workspace">
              <label class="prep-cover-latex prep-document-source">
                <span>LaTeX source</span>
                <textarea
                  data-prep-cover-letter-latex="${e.id}"
                  spellcheck="false"
                >${V(r.latex??``)}</textarea>
              </label>
              <section class="prep-document-preview" aria-label="cover letter preview">
                <div class="prep-preview-heading">
                  <span>document preview</span>
                  <p>Updates automatically after the source is saved.</p>
                </div>
                ${r.pdf_base64?`
                      <iframe class="prep-cover-pdf" title="cover letter PDF preview" src="${V(a)}"></iframe>
                    `:`<p class="prep-cover-path">PDF preview unavailable.</p>`}
              </section>
            </div>
          `:``}
    </details>
  `}function Q(e,t={}){let n=F.get(e.id);if(!t.loading&&!t.error&&!t.analysis&&n)return Q(e,{analysis:n});if(!t.loading&&!t.error&&!t.analysis)return`
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
    `;let r=t.analysis,i=Array.isArray(r?.feedback_items)?r.feedback_items:[],a=r?.verdict===`ready_to_apply`?`ready to apply`:`tweak`,o=Math.min(Ct.get(e.id)??0,Math.max(i.length-1,0)),s=i[o];return`
    <section class="prep-analysis" aria-label="ai analysis">
      <div class="prep-analysis-header">
        <h3>ai analysis</h3>
        <span>${i.length} ${i.length===1?`item`:`items`}</span>
      </div>
      <p class="prep-verdict">${U(a)}</p>
      <p class="prep-overview">${U(r?.overview??`analysis unavailable`)}</p>
      ${s?`
            <article class="prep-feedback" data-feedback-index="${o}">
              <p class="prep-feedback-label">${U(s.label)}</p>
              <h4>${U(s.title)}</h4>
              <p>${U(s.detail)}</p>
              ${fi(s)}
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
  `}function fi(e){return e?.tweak_prompt?`
    <div class="prep-proposed-edit">
      <p class="prep-proposed-label">tweak prompt</p>
      <p>${U(e.tweak_prompt)}</p>
    </div>
  `:`
      <div class="prep-proposed-edit">
        <p class="prep-proposed-label">feedback only</p>
        <p>not enough information to turn this into a safe resume tweak.</p>
      </div>
    `}async function pi(e,t={}){if(!t.force&&F.has(e))return F.get(e);let n=await fetch(`/api/roles/${encodeURIComponent(e)}/prep-analysis`);if(!n.ok)throw Error(`Prep analysis request failed`);let r=await n.json();return r.analysis.resources=r.resources??[],F.set(e,r.analysis),r.analysis}function $(e){let t=document.createElement(`template`);return t.innerHTML=e.trim(),t.content.firstElementChild}async function mi(e){let t=P[0];if(!t)return;let n=_.querySelectorAll(`.review-action`);if(n.forEach(e=>{e.disabled=!0}),e===`later`){try{await ki(t.id),t.review_later_count=Number(t.review_later_count??0)+1,P.length>1?(P.push(P.shift()),oi(`moved to the back of the prep queue.`)):oi(`only one role is in the prep queue.`)}catch{oi(`could not postpone prep. try again.`)}return}if(e===`applied`)try{let e=await Ai(t.id,`applied`);P.shift(),oi(`moved to applied.`),Ar(e,document.querySelector(`.job[data-role-id="${CSS.escape(String(t.id))}"]`))}catch{n.forEach(e=>{e.disabled=!1}),oi(`could not move that role. try again.`)}}async function hi(e,t,n,r){let i=await fetch(`/api/roles/${encodeURIComponent(e)}/prep-feedback`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({feedback_index:t,feedback_item:n,comment:r})});if(!i.ok)throw Error(`Prep feedback update failed`);return i.json()}async function gi(e,t,n,r){let i=await fetch(`/api/roles/${encodeURIComponent(e)}/prep-feedback-ignore`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({feedback_index:t,feedback_item:n,comment:r})});if(!i.ok)throw Error(`Prep feedback ignore failed`);return i.json()}async function _i(e,{force:t=!1}={}){if(!t&&I.has(e))return I.get(e);let n=await fetch(`/api/roles/${encodeURIComponent(e)}/resume`);if(!n.ok)throw Error(`Resume request failed`);let r=await n.json();return r.resume&&I.set(e,r.resume),r.resume}async function vi(e,t){let n=await fetch(`/api/roles/${encodeURIComponent(e)}/resume/save`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({latex:t})});if(!n.ok)throw Error(`Resume save failed`);return n.json()}async function yi(e,t,n){let r=await fetch(`/api/roles/${encodeURIComponent(e)}/resume`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({tweaks:t,previous_latex:n})});if(!r.ok)throw Error(`Resume generation failed`);return r.json()}async function bi(e,t){let n=await fetch(`/api/roles/${encodeURIComponent(e)}/chat`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({messages:t})});if(!n.ok)throw Error(`Role chat failed`);return n.json()}function xi(e,t,n=vt){let r=Et.get(e)??{timer:null,saving:!1,version:0,latex:``};r.version+=1,r.latex=t,r.timer&&clearTimeout(r.timer),r.timer=setTimeout(()=>{r.timer=null,Si(e)},n),Et.set(e,r)}async function Si(e){let t=Et.get(e);if(!t||t.saving)return;t.saving=!0;let n=t.version,r=t.latex;try{let i=await vi(e,r);t.version===n&&(I.set(e,i.resume),Ci(`resume`,e,i.resume))}catch{}finally{t.saving=!1,t.version!==n&&xi(e,t.latex,0)}}function Ci(e,t,n){if(!n?.pdf_base64)return;let r=e===`resume`?`[data-prep-resume-latex="${t}"]`:`[data-prep-cover-letter-latex="${t}"]`,i=v.querySelector(r)?.closest(`.prep-panel`),a=i?.querySelector(`.prep-cover-pdf`),o=i?.querySelector(`.prep-cover-pdf-link`),s=e===`resume`?`/api/roles/${encodeURIComponent(t)}/resume.pdf`:`/api/roles/${encodeURIComponent(t)}/cover-letter.pdf`;a&&(a.src=`${s}?v=${Date.now()}`),o&&(o.href=s)}async function wi(e,t=``,n=``){let r=await fetch(`/api/roles/${encodeURIComponent(e)}/cover-letter`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({tweaks:t,previous_latex:n})});if(!r.ok)throw Error(`Cover letter generation failed`);return r.json()}async function Ti(e,t){let n=await fetch(`/api/roles/${encodeURIComponent(e)}/cover-letter/save`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({latex:t})});if(!n.ok)throw Error(`Cover letter save failed`);return n.json()}function Ei(e,t,n=``,r=vt){let i=Dt.get(e)??{timer:null,saving:!1,version:0,latex:``,tweaks:``};i.version+=1,i.latex=t,i.tweaks=n,i.timer&&clearTimeout(i.timer),i.timer=setTimeout(()=>{i.timer=null,Di(e)},r),Dt.set(e,i)}async function Di(e){let t=Dt.get(e);if(!t||t.saving)return;t.saving=!0;let n=t.version,r=t.latex,i=t.tweaks;try{let a=await Ti(e,r);t.version===n&&(L.set(e,{...a.cover_letter,tweaks:i}),Ci(`coverLetter`,e,a.cover_letter))}catch{}finally{t.saving=!1,t.version!==n&&Ei(e,t.latex,t.tweaks,0)}}async function Oi(e){if(L.has(e))return L.get(e);let t=await fetch(`/api/roles/${encodeURIComponent(e)}/cover-letter`);if(!t.ok)throw Error(`Cover letter request failed`);let n=await t.json();return n.cover_letter&&L.set(e,n.cover_letter),n.cover_letter}async function ki(e){let t=await fetch(`/api/roles/${encodeURIComponent(e)}/review-later`,{method:`POST`});if(!t.ok)throw Error(`Review later update failed`);return(await t.json()).role}async function Ai(e,t){let n=await fetch(`/api/roles/${encodeURIComponent(e)}/status`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({status:t})});if(!n.ok)throw Error(`Status update failed`);return(await n.json()).role}ve.addEventListener(`click`,Vr),Ce.addEventListener(`click`,Hr),ye.addEventListener(`click`,Ur),Ee.addEventListener(`click`,Wr),g.addEventListener(`click`,e=>{let t=e.target.closest(`[data-review-action]`);t&&ai(t.dataset.reviewAction)}),_.addEventListener(`click`,e=>{e.target.closest(`.prep-summary-action`)&&e.stopPropagation()}),_.addEventListener(`input`,e=>{let t=e.target.closest(`[data-prep-resume-tweaks]`);if(t){let e=Number(t.dataset.prepResumeTweaks);Number.isFinite(e)&&wt.set(e,t.value);return}let n=e.target.closest(`[data-prep-resume-latex]`);if(n){let e=Number(n.dataset.prepResumeLatex);if(!Number.isFinite(e))return;xi(e,n.value);return}let r=e.target.closest(`[data-prep-cover-letter-latex]`);if(!r)return;let i=Number(r.dataset.prepCoverLetterLatex);if(!Number.isFinite(i))return;let a=r.closest(`.prep-cover-letter`)?.querySelector(`[data-prep-cover-letter-tweaks="${i}"]`)?.value??``;Ei(i,r.value,a)}),_.addEventListener(`scroll`,e=>{e.target.closest(`[data-prep-resume-latex], [data-prep-cover-letter-latex]`)},!0),_.addEventListener(`focusout`,e=>{let t=e.target.closest(`[data-prep-resume-latex]`);if(t){let e=Number(t.dataset.prepResumeLatex);if(!Number.isFinite(e))return;xi(e,t.value,0);return}let n=e.target.closest(`[data-prep-cover-letter-latex]`);if(!n)return;let r=Number(n.dataset.prepCoverLetterLatex);if(!Number.isFinite(r))return;let i=n.closest(`.prep-cover-letter`)?.querySelector(`[data-prep-cover-letter-tweaks="${r}"]`)?.value??``;Ei(r,n.value,i,0)}),_.addEventListener(`submit`,async e=>{let t=e.target.closest(`[data-prep-role-chat-form]`);if(!t||!P[0])return;e.preventDefault();let n=Number(t.dataset.prepRoleChatForm);if(!Number.isFinite(n))return;let r=t.querySelector(`[data-prep-role-chat-input="${n}"]`),i=r?.value?.trim()??``;if(!i){r?.focus();return}let a=[...Tt.get(n)??[],{role:`user`,content:i}];Tt.set(n,a),v.querySelector(`.prep-role-chat`)?.replaceWith($(li(P[0],{messages:a,loading:!0})));try{let e=await bi(n,a),t=[...a,e.message];Tt.set(n,t),v.querySelector(`.prep-role-chat`)?.replaceWith($(li(P[0],{messages:t})))}catch{let e=[...a,{role:`assistant`,content:`could not answer right now.`}];Tt.set(n,e),v.querySelector(`.prep-role-chat`)?.replaceWith($(li(P[0],{messages:e})))}}),_.addEventListener(`click`,async e=>{let t=e.target.closest(`[data-prep-section-target]`);if(t){let e=t.dataset.prepSectionTarget,n=e?document.getElementById(e):null;if(n instanceof HTMLDetailsElement){n.open=!0,n.scrollIntoView({behavior:`smooth`,block:`start`});let e=n.querySelector(`summary`);e?.setAttribute(`tabindex`,`-1`),e?.focus({preventScroll:!0})}return}if(e.target.closest(`[data-prep-analysis]`)&&P[0]){let e=P[0].id;v.querySelector(`.prep-analysis`)?.replaceWith($(Q(P[0],{loading:!0})));try{let t=await pi(e,{force:!0});if(P[0]?.id!==e)return;v.querySelector(`.prep-analysis`)?.replaceWith($(Q(P[0],{analysis:t})))}catch{v.querySelector(`.prep-analysis`)?.replaceWith($(Q(P[0],{error:!0})))}return}if(e.target.closest(`[data-prep-resume-regenerate]`)&&P[0]){let e=P[0].id,t=v.querySelector(`.prep-resume`),n=t?.querySelector(`[data-prep-resume-tweaks="${e}"]`)?.value??``,r=t?.querySelector(`[data-prep-resume-latex="${e}"]`)?.value??``;if(!n.trim()){t?.querySelector(`[data-prep-resume-tweaks="${e}"]`)?.focus();return}wt.set(e,n),t?.replaceWith($(si(P[0],{loading:!0})));try{let t=await yi(e,n,r);I.set(e,t.resume),v.querySelector(`.prep-resume`)?.replaceWith($(si(P[0],{resume:t.resume}))),W()}catch{v.querySelector(`.prep-resume`)?.replaceWith($(si(P[0],{resume:I.get(e),tweaks:n}))),W()}return}if(e.target.closest(`[data-prep-cover-letter]`)&&P[0]){let e=P[0].id,t=v.querySelector(`.prep-cover-letter`),n=t?.querySelector(`[data-prep-cover-letter-tweaks="${e}"]`)?.value??``,r=n.trim()?t?.querySelector(`[data-prep-cover-letter-latex="${e}"]`)?.value??``:``;t?.replaceWith($(di(P[0],{loading:!0})));try{let t=await wi(e,n,r);L.set(e,t.cover_letter),v.querySelector(`.prep-cover-letter`)?.replaceWith($(di(P[0],{coverLetter:t.cover_letter}))),W()}catch{v.querySelector(`.prep-cover-letter`)?.replaceWith($(di(P[0],{coverLetter:L.get(e),tweaks:n}))),W()}return}let n=e.target.closest(`[data-prep-action]`);if(n){mi(n.dataset.prepAction);return}let r=e.target.closest(`[data-prep-feedback]`);if(!r||!P[0])return;let i=P[0].id,a=F.get(i),o=Array.isArray(a?.feedback_items)?a.feedback_items.length:0,s=Ct.get(i)??0;if(r.dataset.prepFeedback===`accept`||r.dataset.prepFeedback===`ignore`){let e=a?.feedback_items?.[s];if(!e)return;let t=v.querySelector(`[data-prep-feedback-comment]`)?.value??``,n=r.dataset.prepFeedback,o=n;r.disabled=!0,r.textContent=n===`accept`?`adding...`:`ignoring...`;try{if(n===`accept`){let n=await hi(i,s,e,t),r=document.querySelector(`.job[data-role-id="${CSS.escape(String(i))}"]`);n.role&&(P[0]=n.role,Ar(n.role,r)),Mi(i,n.tweak_prompt??e.tweak_prompt??``),ji(i,s,a)}else await gi(i,s,e,t),ji(i,s,a)}catch{r.disabled=!1,r.textContent=o}return}let c=r.dataset.prepFeedback===`next`?1:-1;Ct.set(i,Math.max(0,Math.min(s+c,o-1))),v.querySelector(`.prep-analysis`)?.replaceWith($(Q(P[0],{analysis:a})))});function ji(e,t,n){let r=n.feedback_items.filter((e,n)=>n!==t),i=Math.min(t,Math.max(r.length-1,0)),a={...n,feedback_items:r,verdict:r.length===0?`ready_to_apply`:n.verdict};Ct.set(e,i),F.set(e,a),v.querySelector(`.prep-analysis`)?.replaceWith($(Q(P[0],{analysis:a})))}function Mi(e,t){let n=String(t||``).trim();if(!n)return;let r=wt.get(e)?.trim()??``,i=r?`${r}\n\n${n}`:n;wt.set(e,i);let a=v.querySelector(`[data-prep-resume-tweaks="${e}"]`);a&&(a.value=i,a.focus())}document.addEventListener(`keydown`,e=>{e.key===`Escape`&&!Ae.hidden&&vn(),e.key===`Escape`&&!o.hidden&&zt(),e.key===`Escape`&&!g.hidden&&Hr(),e.key===`Escape`&&!_.hidden&&Wr(),e.key===`Escape`&&!Re.hidden&&Tn(),e.key===`Escape`&&!Ze.hidden&&Nn(),e.key===`Escape`&&!it.hidden&&Hn(),e.key===`Escape`&&!lt.hidden&&rr()}),ke.addEventListener(`click`,_n),Me.addEventListener(`click`,vn),je.addEventListener(`click`,vn);function Ni(){return Array.from(document.querySelectorAll(`.pane-toggle`))}function Pi(){return Ni().some(e=>e.getAttribute(`aria-expanded`)===`true`)}function Fi(){Pe.textContent=Pi()?`collapse all`:`expand all`}function Ii(){document.querySelectorAll(`.pane-toggle`).forEach(e=>{e.setAttribute(`aria-expanded`,`true`),e.querySelector(`.chevron`).textContent=`v`,e.parentElement.querySelector(`.pane-body`).hidden=!1})}function Li(){document.querySelectorAll(`.job[open]`).forEach(e=>{e.open=!1}),document.querySelectorAll(`.pane-toggle`).forEach(e=>{e.setAttribute(`aria-expanded`,`false`),e.querySelector(`.chevron`).textContent=`>`,e.parentElement.querySelector(`.pane-body`).hidden=!0})}Pe.addEventListener(`click`,()=>{Pi()?Li():Ii(),Fi()}),Fe.addEventListener(`click`,()=>{St=!St,Fe.textContent=St?`show empty`:`hide empty`,D&&nn(D.statuses)}),Le.addEventListener(`click`,wn),ze.addEventListener(`click`,Tn),Xe.addEventListener(`click`,Mn),Qe.addEventListener(`click`,Nn),rt.addEventListener(`click`,Vn),at.addEventListener(`click`,Hn),De.addEventListener(`click`,nr),ut.addEventListener(`click`,rr),dt.addEventListener(`submit`,e=>{e.preventDefault(),or(dt).catch(()=>{T.textContent=`could not add company.`})}),ft.addEventListener(`submit`,e=>{e.preventDefault(),dr(ft).catch(()=>{gt.textContent=`could not add role.`})}),E.addEventListener(`submit`,e=>{let t=e.target.closest(`[data-company-link-form]`);t&&(e.preventDefault(),sr(t).catch(()=>{T.textContent=`could not add link.`}))}),E.addEventListener(`input`,e=>{let t=e.target.closest(`[data-company-notes]`);t&&mr(t.dataset.companyNotes)}),E.addEventListener(`change`,e=>{let t=e.target.closest(`[data-company-tier]`);if(!t)return;let n=t.closest(`.company-panel`);n&&gr(n,t.value),window.clearTimeout(It.get(t.dataset.companyTier)),hr(t.dataset.companyTier).catch(()=>{pr(`could not save company.`)})}),E.addEventListener(`click`,e=>{let t=e.target.closest(`[data-delete-company]`);if(t){let e=fr(t.dataset.deleteCompany),n=e?.name?H(e.name):`this company`;if(!window.confirm(`Deactivate ${n}? It will be hidden from company counts and skipped during scans.`))return;t.disabled=!0,lr(t.dataset.deleteCompany).catch(()=>{T.textContent=`could not deactivate company.`,t.disabled=!1});return}let n=e.target.closest(`[data-delete-career-page]`);if(!n)return;let r=n.closest(`.company-link-row`)?.querySelector(`.company-link-text`)?.textContent?.trim();window.confirm(`Delete ${r||`this career link`}?`)&&(n.disabled=!0,cr(n.dataset.deleteCareerPage).catch(()=>{T.textContent=`could not delete link.`,n.disabled=!1}))}),Be.addEventListener(`change`,e=>{let t=e.target.closest(`input[type="checkbox"], select, input[data-setting-text]`);t&&Wn(t)}),Be.addEventListener(`submit`,async e=>{e.preventDefault();let t=Be.querySelector(`button[type="submit"]`),n=Be.querySelectorAll(`input[type="checkbox"][name], select[name], input[data-setting-text][name]`),r={};n.forEach(e=>{let t=e.name;t&&(r[t]=e.type===`checkbox`?e.checked:e.value)}),t.disabled=!0,t.textContent=`saving...`;try{S.textContent=`saving settings...`;let e=await fetch(`/api/config`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(r)});if(!e.ok)throw Error(`Config update failed`);K(await e.json(),`settings saved.`)}catch{S.textContent=`could not save settings.`,S.classList.remove(`is-empty`)}finally{t.disabled=!1,t.textContent=`save settings`}}),Ge.addEventListener(`input`,()=>{C.disabled=!Ge.value.trim()}),qe.addEventListener(`click`,Kn),C.addEventListener(`click`,qn),Ye.addEventListener(`click`,Gn),ct.addEventListener(`click`,Xn),Yn(),Sr({applyDefaultCollapsed:!0}).catch(()=>{Jt(null,`could not load resume.`),Yt([],`could not load cover letter examples.`),G()}),vr().then(()=>{yr()}).catch(()=>{x.textContent=`could not load scan status`});