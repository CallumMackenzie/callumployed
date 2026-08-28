import{t as e}from"./preload-helper-Czpn1I53.js";var{sankey:t,sankeyLinkHorizontal:n}=await e(async()=>{let{sankey:e,sankeyLinkHorizontal:t}=await import(`/assets/d3-sankey.js`);return{sankey:e,sankeyLinkHorizontal:t}},[]),r=document.querySelector(`#stats`),i=document.querySelector(`#status-list`),a=document.querySelector(`#search-toggle`),o=document.querySelector(`#search-dialog`),s=document.querySelector(`#search-backdrop`),c=document.querySelector(`#search-form`),l=document.querySelector(`#search-input`),u=document.querySelector(`#close-search`),d=document.querySelector(`#materials-panel`),f=document.querySelector(`#materials-toggle`),ee=document.querySelector(`#materials-body`),te=document.querySelector(`#materials-summary`),ne=document.querySelector(`#materials-required-warning`),re=document.querySelector(`#resume-meta`),p=document.querySelector(`#resume-upload`),ie=document.querySelector(`#resume-upload-button`),ae=document.querySelector(`#resume-resource-meta`),oe=document.querySelector(`#resume-resource-upload`),se=document.querySelector(`#resume-resource-upload-button`),ce=document.querySelector(`#resume-resource-list`),le=document.querySelector(`#cover-letter-meta`),ue=document.querySelector(`#cover-letter-upload`),de=document.querySelector(`#cover-letter-upload-button`),fe=document.querySelector(`#cover-letter-list`),pe=document.querySelector(`#experience-note-meta`),me=document.querySelector(`#experience-note-upload`),he=document.querySelector(`#experience-note-upload-button`),ge=document.querySelector(`#experience-note-list`);document.querySelector(`#material-index-button`);var _e=document.querySelector(`#material-index-warning`),ve=document.querySelector(`#material-index-status`),ye=document.querySelector(`#review-discovered`),be=document.querySelector(`#prep-interested`),m=document.querySelector(`#review-view`),xe=document.querySelector(`#review-heading`),Se=document.querySelector(`#review-progress`),Ce=document.querySelector(`#review-card`),we=document.querySelector(`#close-review`),h=document.querySelector(`#prep-view`),Te=document.querySelector(`#prep-heading`),Ee=document.querySelector(`#prep-progress`),g=document.querySelector(`#prep-card`),De=document.querySelector(`#close-prep`),Oe=document.querySelector(`#prepped-roles`),ke=document.querySelector(`#prepped-view`),Ae=document.querySelector(`#close-prepped`),je=document.querySelector(`#prepped-summary`),Me=document.querySelector(`#prepped-list`),_=document.querySelector(`#prepped-detail`),v=document.querySelector(`#scan-all-button`),Ne=document.querySelector(`#manage-companies-button`),y=document.querySelector(`#scan-status-bar`),b=document.querySelector(`#scan-status-text`),Pe=document.querySelector(`#scan-last-time`),Fe=document.querySelector(`#scan-failures-open`),Ie=document.querySelector(`#scan-failures-dialog`),Le=document.querySelector(`#scan-failures-backdrop`),Re=document.querySelector(`#scan-failures-close`),ze=document.querySelector(`#scan-failures-list`),Be=document.querySelector(`#toggle-all`),Ve=document.querySelector(`#collapse-empty`),He=document.querySelector(`#toolbar-summary`),Ue=document.querySelector(`#settings-open`),We=document.querySelector(`#settings-view`),Ge=document.querySelector(`#settings-close`),x=document.querySelector(`#settings-status`),Ke=document.querySelector(`#settings-form`),qe=document.querySelector(`#settings-profile-options`),Je=document.querySelector(`#settings-options`),Ye=document.querySelector(`#central-store-summary`),Xe=document.querySelector(`#central-store-sync-summary`),S=document.querySelector(`#central-api-url-input`),Ze=document.querySelector(`#central-passkey-input`),Qe=document.querySelector(`#central-save-button`),C=document.querySelector(`#central-sync-button`),$e=document.querySelector(`#recommendation-history-summary`),et=document.querySelector(`#clear-recommendation-history`),tt=document.querySelector(`#metrics-open-button`),nt=document.querySelector(`#metrics-view`),rt=document.querySelector(`#metrics-close`),w=document.querySelector(`#metrics-status`),it=document.querySelector(`#metrics-overview`),at=document.querySelector(`#metrics-sections`),ot=document.querySelector(`#metrics-scan-list`),st=document.querySelector(`#sankey-open-button`),ct=document.querySelector(`#sankey-view`),lt=document.querySelector(`#sankey-close`),T=document.querySelector(`#sankey-status`),ut=document.querySelector(`#sankey-canvas`),dt=document.querySelector(`#sankey-path-list`),ft=document.querySelector(`#app-update-button`),pt=document.querySelector(`#companies-view`),mt=document.querySelector(`#companies-close`),E=document.querySelector(`#companies-status`),ht=document.querySelector(`#company-create-form`),D=document.querySelector(`#companies-list`),gt=document.querySelector(`#role-add-form`),_t=document.querySelector(`#role-url-input`),vt=document.querySelector(`#role-company-input`),yt=document.querySelector(`#role-company-options`),bt=document.querySelector(`#role-add-status`),xt=3,St=1200,Ct=new Set([`applied`,`OA`,`interview`,`rejected`,`offer`]),wt=new Map([[`discovered`,`#4f6472`],[`interested`,`#00897b`],[`disinterested`,`#626970`],[`applied`,`#2257ad`],[`oa`,`#b36b00`],[`interview`,`#5f2bd8`],[`rejected`,`#b93d2d`],[`offer`,`#137347`],[`closed`,`#53606b`],[`archived`,`#765b4a`]]),Tt=/^(?:about (?:the )?(?:role|team|job)|about this role|job description|job responsibilities|minimum qualifications|preferred qualifications|qualifications|requirements|responsibilities|what to expect|what (?:you'll|you’ll|you will) (?:bring|do)|what'?s in it for you|who you are|your objectives|your skills & talents):?$/i,Et=!0,O=null,Dt=null,k=[],A=[],j=[],M=null,N=[],P=[],F=new Map,Ot=new Map,I=new Map,kt=new Map,L=new Map,At=new Map,jt=new Map,Mt=new Map,R=[],z=null,Nt=null,Pt=new Map,Ft=new Set,It=!1,Lt=null,Rt=!1,zt=null,Bt=null,Vt=null,Ht=null,B=null,Ut=[],Wt=new Map;function V(){return O?.query?.trim()??``}function Gt(){let e=!!V();a.classList.toggle(`search-active`,e),a.setAttribute(`aria-label`,e?`clear search`:`search jobs`)}function Kt(){l.value=V(),o.hidden=!1,c.hidden=!1,l.focus(),l.select()}function qt(){o.hidden=!0,c.hidden=!0,a.focus()}function Jt(e){return e?new Intl.DateTimeFormat(void 0,{month:`short`,day:`numeric`,hour:`numeric`,minute:`2-digit`}).format(new Date(e)).toLocaleLowerCase():``}function H(e){return e?new Intl.DateTimeFormat(void 0,{month:`short`,day:`numeric`,hour:`numeric`,minute:`2-digit`}).format(new Date(e)).replace(`, `,` `).toLocaleLowerCase():``}function U(e){return String(e??``).replaceAll(`&`,`&amp;`).replaceAll(`<`,`&lt;`).replaceAll(`>`,`&gt;`).replaceAll(`"`,`&quot;`).replaceAll(`'`,`&#039;`)}function W(e){return String(e??``).toLocaleLowerCase()}function G(e){return U(W(e))}function Yt(e){try{let t=new URL(String(e||``));return[`http:`,`https:`].includes(t.protocol)?t.href:``}catch{return``}}function Xt(e){return e}function K(e=g){e.querySelectorAll(`[data-prep-resume-latex], [data-prep-cover-letter-latex]`).forEach(Xt)}function Zt(){return`
    <svg class="role-link-icon" viewBox="0 0 24 24" aria-hidden="true">
      <path d="M7 17 17 7"></path>
      <path d="M8 7h9v9"></path>
    </svg>
  `}function Qt(){return`
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M12 5v14"></path>
      <path d="M5 12h14"></path>
    </svg>
  `}function $t(){return`
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M3 6h18"></path>
      <path d="M8 6V4h8v2"></path>
      <path d="m19 6-1 14H6L5 6"></path>
      <path d="M10 11v5"></path>
      <path d="M14 11v5"></path>
    </svg>
  `}function en(e,t,n){let r=`<span class="role-title-text">${G(e)}</span>`;return t?`<a class="${n}" href="${U(t)}" target="_blank" rel="noreferrer">${r}${Zt()}</a>`:`<span class="${n}">${r}</span>`}function tn(e){r.innerHTML=[[`companies`,e.companies_total],[`jobs`,e.jobs_total],[`applications`,e.applications_total]].map(([e,t])=>`<dl class="stat"><dt>${G(e)}</dt><dd>${t}</dd></dl>`).join(``)}function nn(e=O){if(!e){He.innerHTML=``;return}let t=t=>e.statuses.find(e=>e.key===t)?.count??0;He.innerHTML=[[`discovered`,t(`discovered`)],[`interested`,t(`interested`)],[`applied`,e.stats?.applications_total??0],[`total`,e.stats?.jobs_total??0]].map(([e,t])=>`
        <dl>
          <dt>${G(e)}</dt>
          <dd>${t}</dd>
        </dl>
      `).join(``)}function rn(e,t=``){if(Dt=e,ie.textContent=e?`replace`:`upload`,t){re.textContent=t;return}if(!e){re.textContent=`no resume uploaded`;return}let n=H(e.updated_at),r=pn(e.content_bytes);re.textContent=[W(e.filename),r,n].filter(Boolean).join(` | `)}function an(e,t,n,{binary:r=!1}={}){let i=r?e.filename:e.id;return`
    <li class="material-source-item" title="${G(e.filename)}">
      <div class="material-source-copy">
        <span>${G(e.filename)}</span>
        <small>${U(n)}</small>
      </div>
      <div class="material-source-actions">
        <button type="button" class="material-source-view" data-material-view="${U(t)}" data-material-id="${U(i)}" data-material-binary="${r}">preview</button>
        <button type="button" class="material-source-remove" data-material-remove="${U(t)}" data-material-id="${U(i)}" data-material-name="${G(e.filename)}">remove</button>
      </div>
      <div class="material-source-preview" data-material-preview-body hidden></div>
    </li>`}function on(e,t=``){A=Array.isArray(e)?e:[],de.textContent=A.length>0?`add`:`upload`,le.textContent=t||(A.length===0?`no examples uploaded`:`${A.length} ${A.length===1?`example`:`examples`} stored`),fe.innerHTML=A.map(e=>an(e,`cover-letter-examples`,pn(e.content_bytes))).join(``)}function sn(e,t=``){j=Array.isArray(e)?e:[],he.textContent=j.length>0?`add`:`upload`,pe.textContent=t||(j.length===0?`no notes uploaded`:`${j.length} ${j.length===1?`note`:`notes`} stored`),ge.innerHTML=j.map(e=>an(e,`experience-notes`,pn(e.content_bytes))).join(``)}function cn(e,t=``){M=e??null;let n=M?.status??`missing`,r=n!==`ready`;if(j.length,_e.hidden=!r,_e.textContent=t||M?.warning||``,t)ve.textContent=t;else if(n===`ready`){let e=Number(M?.document_count??0),t=Number(M?.skipped_source_count??0),n=H(M?.generated_at);ve.textContent=[`${e} indexed ${e===1?`page`:`pages`}`,t?`${t} unreadable upload skipped`:``,n].filter(Boolean).join(` | `)}else ve.textContent=n===`stale`?`index out of date`:`not indexed`}function ln(e,t=``){k=Array.isArray(e)?e:[],se.textContent=k.length>0?`add`:`upload`,ae.textContent=t||(k.length===0?`no resources uploaded`:`${k.length} ${k.length===1?`resource`:`resources`} stored`),ce.innerHTML=k.map(e=>an(e,`resume-resources`,pn(e.bytes),{binary:!0})).join(``)}function un(e,t={}){rn(e?.master_resume??null),ln(e?.resume_resources??[]),on(e?.cover_letter_examples??[]),sn(e?.experience_notes??[]),cn(e?.material_index??null),dn(e?.ui),(!It||t.applyDefaultCollapsed)&&(fn(!!e?.ui?.default_collapsed),It=!0)}function dn(e=null){let t=Dt?`resume ready`:`no resume`,n=k.length===0?`no resources`:`${k.length} ${k.length===1?`resource`:`resources`}`,r=A.length,i=r===0?`no cover letters`:`${r} cover ${r===1?`letter`:`letters`}`,a=j.length,o=a===0?`no notes`:`${a} experience ${a===1?`note`:`notes`}`;ne.hidden=!(typeof e?.has_missing_required_materials==`boolean`?e.has_missing_required_materials:!Dt||r===0||a===0),te.textContent=`${t} | ${n} | ${i} | ${o}`}function fn(e){d.classList.toggle(`collapsed`,e),f.setAttribute(`aria-expanded`,String(!e)),f.querySelector(`.materials-chevron`).textContent=e?`>`:`v`,ee.hidden=e}function pn(e){return Number.isFinite(e)?e<1024?`${e} b`:`${Math.round(e/1024)} kb`:``}async function mn(e){let t=e.closest(`.material-source-item`)?.querySelector(`[data-material-preview-body]`);if(!t)return;if(t.dataset.loaded===`true`){t.hidden=!t.hidden,e.textContent=t.hidden?`preview`:`hide`;return}e.disabled=!0,e.textContent=`loading...`;let n=e.dataset.materialView,r=e.dataset.materialId,i=`/api/${encodeURIComponent(n)}/${encodeURIComponent(r)}`;try{if(e.dataset.materialBinary===`true`)t.innerHTML=`<iframe title="${G(r)} preview" src="${U(i)}"></iframe>`;else{let e=await fetch(i);if(!e.ok)throw Error(`Preview unavailable`);let n=await e.json(),r=document.createElement(`pre`);r.textContent=n.content||`This source is empty.`,t.replaceChildren(r)}t.dataset.loaded=`true`,t.hidden=!1,e.textContent=`hide`}catch(n){t.textContent=n instanceof Error?n.message:`Preview unavailable`,t.hidden=!1,e.textContent=`preview`}finally{e.disabled=!1}}async function hn(e){let t=e.dataset.materialRemove,n=e.dataset.materialId,r=e.dataset.materialName||`this source`;if(window.confirm(`Remove ${r}? This removes it from future application preparation.`)){e.disabled=!0,e.textContent=`removing...`;try{let e=await fetch(`/api/${encodeURIComponent(t)}/${encodeURIComponent(n)}`,{method:`DELETE`}),r=await e.json();if(!e.ok)throw Error(r.error||`Remove failed`);un(r)}catch(t){e.disabled=!1,e.textContent=`remove`,window.alert(t instanceof Error?t.message:`Remove failed`)}}}function gn(e){i.innerHTML=e.map(e=>{let t=e.jobs.map(t=>_n(t,e.key)).join(``);return`
        <section class="status-pane ${e.count===0?`empty`:``} ${Et?`hidden-empty`:``}" id="status-${U(e.key)}" data-bucket="${U(e.key)}">
          <button class="pane-toggle" type="button" aria-expanded="false">
            <span class="chevron">></span>
            <span class="pane-title">${G(e.label)}</span>
            <span class="count">${e.count}</span>
          </button>
          <div class="pane-body" hidden>
            ${t?`<div class="jobs">${t}</div>`:`<p class="empty-copy">no jobs in this status.</p>`}
          </div>
        </section>
      `}).join(``)}function _n(e,t){return`
    <details class="job" data-role-id="${U(e.id)}">
      <summary class="job-summary">
        <span class="job-chevron">></span>
        <span class="job-identity">
          <span class="job-company">[${G(e.company_name)}]</span>
          ${en(e.title,e.role_url,`job-title`)}
          ${t===`interested`&&e.prep_started?bn():``}
          ${t===`closed`&&e.updated_in_latest_scan?vn():``}
          ${[`discovered`,`interested`].includes(t)&&e.missing_from_latest_scan?yn():``}
        </span>
      </summary>
      <div class="job-detail">
        ${t===`discovered`?xn(e):``}
        ${t===`interested`?Sn(e):``}
        ${t===`disinterested`?Cn(e):``}
        ${t===`applied`?wn(e):``}
        ${t===`OA`?Tn(e):``}
        ${t===`interview`?En(e):``}
        ${t===`closed`?Dn(e):``}
        <dl>
          ${e.location?`<div>
                  <dt>location</dt>
                  <dd>${G(e.location)}</dd>
                </div>`:``}
          <div>
            <dt>updated</dt>
            <dd>${Jt(e.updated_at)}</dd>
          </div>
        </dl>
      </div>
    </details>
  `}function vn(){return`<span class="latest-scan-dot" title="updated in latest scan" aria-label="updated in latest scan"></span>`}function yn(){return`<span class="missing-latest-scan-dot" title="not seen in latest scan" aria-label="not seen in latest scan"></span>`}function bn(){return`<span class="prep-started-dot" title="application materials started" aria-label="application materials started"></span>`}function xn(e){return`
    <div class="job-actions job-actions-nowrap" aria-label="discovered role actions">
      <button class="job-action success" type="button" data-review-role-id="${e.id}">view</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="interested">interested</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="disinterested">disinterested</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="closed">closed</button>
    </div>
  `}function Sn(e){return`
    <div class="job-actions" aria-label="interested role actions">
      <button class="job-action success" type="button" data-prep-role-id="${e.id}">prep</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="applied">applied</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="disinterested">disinterested</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="closed">closed</button>
    </div>
  `}function Cn(e){return`
    <div class="job-actions" aria-label="disinterested role actions">
      <button class="job-action success" type="button" data-role-id="${e.id}" data-status="interested">interested</button>
    </div>
  `}function wn(e){return`
    <div class="job-actions job-actions-nowrap" aria-label="applied role actions">
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="OA">oa</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="interview">interview</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="rejected">rejected</button>
    </div>
  `}function Tn(e){return`
    <div class="job-actions job-actions-nowrap" aria-label="oa role actions">
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="interview">interview</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="disinterested">disinterested</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="rejected">rejected</button>
    </div>
  `}function En(e){return`
    <div class="job-actions" aria-label="interview role actions">
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="rejected">rejected</button>
      <button class="job-action success" type="button" data-role-id="${e.id}" data-status="offer">offer</button>
    </div>
  `}function Dn(e){return`
    <div class="job-actions" aria-label="closed role actions">
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="interested">interested</button>
    </div>
  `}function On(e){O=e,l.value=e.query,Gt(),tn(e.stats),nn(e),gn(e.statuses),la(),Xr(e.statuses),Qr(e.statuses)}function kn(e){zt=e??null;let t=!!e?.scanning,n=t&&!!e?.cancel_requested,r=Number(e?.completed_companies??0),i=Number(e?.total_companies??0),a=Number(e?.failed_companies??0),o=typeof e?.error==`string`?e.error.trim():``,s=Array.isArray(e?.failures)?e.failures:[];v.disabled=n,v.textContent=t?n?`cancelling...`:`cancel scan`:`scan roles`,v.classList.toggle(`danger`,t&&!n),y.hidden=!t&&!o&&s.length===0,y.classList.toggle(`scanning`,t),y.classList.toggle(`scan-error`,!t&&!!o||s.length>0),b.textContent=n?`cancelling scan...`:t?`scanning roles${i>0?` ${r}/${i}`:``}${a>0?`, ${a} failed`:``}`:s.length>0?`${s.length} recent scan ${s.length===1?`failure`:`failures`}`:o?`last scan error: ${o}`:`scan idle`,Fe&&ze&&(Fe.hidden=s.length===0,ze.innerHTML=s.slice(0,5).map(e=>{let t=e?.company_name||`unknown company`,n=e?.error||`scan failed`;return`
          <p>
            <span>${G(t)}</span>
            <span>${U(n)}</span>
          </p>
        `}).join(``),s.length===0&&jn());let c=e?.last_scan_at;Pe.textContent=c?`last scan: ${H(c)}`:`last scan: never`,Rt&&!t&&Y(V()).catch(()=>{}),Rt=t}function An(){Fe.hidden||(Ie.hidden=!1,Re.focus())}function jn(){Ie.hidden=!0}function q(e,t=``){Bt=e;let n=Array.isArray(e?.settings)?e.settings:[],r=n.filter(e=>e.key?.startsWith(`applicant_`)),i=n.filter(e=>!e.key?.startsWith(`applicant_`)),a=e?.central??{};x.textContent=t,x.classList.toggle(`is-empty`,!t);let o=Number(e?.recommendation_history_count??0);$e.textContent=o>0?`${o} saved ${o===1?`feedback decision`:`feedback decisions`}`:`no saved resume feedback decisions`,et.disabled=o===0,Mn(a),qe.innerHTML=r.map(e=>Nn(e)).join(``),Je.innerHTML=i.map(e=>Nn(e)).join(``),J(!1)}function Mn(e){let t=e?.api_url??``;S.value=t,Ze.value=``;let n=e?.passkey_configured?`passkey saved`:`no passkey saved`;Ye.textContent=t?`${W(t)} | ${n}`:`no api url | ${n}`,Xe.textContent=`${Number(e?.companies_linked??0)} linked | ${Number(e?.companies_unlinked??0)} unlinked | ${Number(e?.companies_needs_review??0)} review | ${Number(e?.companies_failed??0)} failed`,C.disabled=!t}function Nn(e){if(e.control===`text`&&e.editable!==!1)return Pn(e);if(e.control===`select`&&e.editable!==!1)return Fn(e);if(e.control!==`toggle`||e.editable===!1)return In(e);let t=e.value?`checked`:``,n=e.default?`on by default`:`off by default`;return`
    <label class="setting-option">
      <span class="setting-copy">
        <span class="setting-label">${G(e.label)}</span>
        <span class="setting-description">${G(e.description)}</span>
        <span class="setting-default">${G(n)}</span>
      </span>
      <span class="setting-switch">
        <input type="checkbox" name="${U(e.key)}" ${t} />
        <span aria-hidden="true"></span>
      </span>
    </label>
  `}function Pn(e){let t=e.default?`default: ${W(e.default)}`:`optional`,n=e.input_type??`text`,r=e.autocomplete??`name`;return`
    <label class="setting-option">
      <span class="setting-copy">
        <span class="setting-label">${G(e.label)}</span>
        <span class="setting-description">${G(e.description)}</span>
        <span class="setting-default">${G(t)}</span>
      </span>
      <input
        class="setting-text-input"
        data-setting-text
        name="${U(e.key)}"
        type="${U(n)}"
        value="${U(e.value??``)}"
        autocomplete="${U(r)}"
      />
    </label>
  `}function Fn(e){let t=Array.isArray(e.options)?e.options:[],n=`default: ${W(e.default)}`;return`
    <label class="setting-option">
      <span class="setting-copy">
        <span class="setting-label">${G(e.label)}</span>
        <span class="setting-description">${G(e.description)}</span>
        <span class="setting-default">${G(n)}</span>
      </span>
      <select class="setting-select" name="${U(e.key)}">
        ${t.map(t=>{let n=t.value===e.value?`selected`:``;return`<option value="${U(t.value)}" ${n}>${G(t.label)}</option>`}).join(``)}
      </select>
    </label>
  `}function In(e){let t=e.default?`on by default`:`off by default`,n=e.value?`automatic`:`off`;return`
    <div class="setting-option setting-option-readonly">
      <span class="setting-copy">
        <span class="setting-label">${G(e.label)}</span>
        <span class="setting-description">${G(e.description)}</span>
        <span class="setting-default">${G(t)}</span>
      </span>
      <span class="setting-badge">${G(n)}</span>
    </div>
  `}function J(e){Ke.querySelectorAll(`input, select`).forEach(t=>{t.disabled=e}),Qe.disabled=e,C.disabled=e||!S.value.trim(),ft.disabled=e}async function Ln(){We.hidden=!1,document.body.classList.add(`settings-open`),Ge.focus(),Bt?q(Bt):(x.textContent=`loading settings...`,x.classList.remove(`is-empty`),Je.innerHTML=``);try{await zn()}catch{x.textContent=`could not load settings.`}}function Rn(){We.hidden=!0,document.body.classList.remove(`settings-open`),Ue.focus()}async function zn(){let e=await fetch(`/api/config`);if(!e.ok)throw Error(`Config request failed`);q(await e.json())}function Bn(e){let t=e?.value;return t==null?`n/a`:e?.kind===`ratio`?Number(t).toLocaleString(void 0,{maximumFractionDigits:2,minimumFractionDigits:0}):typeof t==`number`?t.toLocaleString():W(t)}function Vn(e,t=`metric-card`){return`
    <article class="${t}">
      <span>${G(e?.label)}</span>
      <strong>${U(Bn(e))}</strong>
    </article>
  `}function Hn(e,t=``){Vt=e,w.textContent=t||(e?.updated_at?`updated ${H(e.updated_at)}`:``),w.classList.toggle(`is-empty`,!w.textContent);let n=Array.isArray(e?.overview)?e.overview:[],r=Array.isArray(e?.sections)?e.sections:[],i=Array.isArray(e?.recent_scans)?e.recent_scans:[];it.innerHTML=n.map(e=>Vn(e)).join(``),at.innerHTML=r.map(Un).join(``),ot.innerHTML=i.length?i.map(Wn).join(``):`<p class="empty-copy">no scan runs recorded.</p>`}function Un(e){let t=Array.isArray(e?.metrics)?e.metrics:[];return`
    <section class="metrics-section">
      <div class="metrics-section-heading">
        <h3>${G(e?.title)}</h3>
      </div>
      <div class="metrics-section-grid">
        ${t.map(e=>Vn(e,`metric-card metric-card-compact`)).join(``)}
      </div>
    </section>
  `}function Wn(e){let t=e?.scan_status??`unknown`,n=e?.started_at?H(e.started_at):`not started`,r=e?.finished_at?H(e.finished_at):`not finished`,i=e?.error?`<span>${G(e.error)}</span>`:``;return`
    <article class="metrics-scan-row">
      <div>
        <strong>${G(e?.company_name??`unknown company`)}</strong>
        <span>${G(n)} -> ${G(r)}</span>
        ${i}
      </div>
      <span class="metrics-status-pill">${G(t)}</span>
    </article>
  `}async function Gn(){nt.hidden=!1,document.body.classList.add(`metrics-open`),rt.focus(),Vt?Hn(Vt):(w.textContent=`loading metrics...`,w.classList.remove(`is-empty`),it.innerHTML=``,at.innerHTML=``,ot.innerHTML=``);try{await qn()}catch{w.textContent=`could not load metrics.`}}function Kn(){nt.hidden=!0,document.body.classList.remove(`metrics-open`),tt.focus()}async function qn(){let e=await fetch(`/api/metrics`);if(!e.ok)throw Error(`Metrics request failed`);Hn(await e.json())}function Jn(e,t=``){Ht=e;let n=Number(e?.role_count??0),r=Array.isArray(e?.links)?e.links:[],i=Array.isArray(e?.paths)?e.paths:[];T.textContent=t||(e?.updated_at?`${n.toLocaleString()} roles | updated ${H(e.updated_at)}`:``),T.classList.toggle(`is-empty`,!T.textContent),ut.innerHTML=r.length?Yn(e):`<p class="empty-copy">no role transitions recorded yet.</p>`,dt.innerHTML=i.length?i.map($n).join(``):`<p class="empty-copy">no role paths recorded yet.</p>`}function Yn(e){let t=Array.isArray(e?.nodes)?e.nodes:[],n=Array.isArray(e?.links)?e.links:[],r=Qn(t,n),i=r.nodes,a=r.links,o=(r.flowLinks??n).map(e=>{let t=i.get(e.source),n=i.get(e.target),r=a.get(e);if(!t||!n||!r)return``;let o=r.width,s=n.x<t.x,c=Xn(e.target),l=r.priority?`0.42`:s?`0.28`:`0.34`,u=r.path??Zn({isBacktrack:s,sourceX:t.x+t.width,sourceY:r.sourceY,targetX:n.x,targetY:r.targetY,width:o});return`
        <path class="${[`sankey-link`,s?`sankey-link-backtrack`:``,r.priority?`sankey-link-priority`:``].filter(Boolean).join(` `)}" d="${u}" fill="${r.path?`none`:c}" fill-opacity="${l}" stroke="${c}" style="stroke-width: ${r.path?o:1}px">
          <title>${G(t.label)} to ${G(n.label)}: ${Number(e.value??0).toLocaleString()}</title>
        </path>
      `}).join(``),s=Array.from(i.values()).map(e=>{let t=Number(e.history_count??e.current_count??0),n=Number(e.value??t),i=n>0?n.toLocaleString():`0`,a=e.x>r.width-180,o=a?e.x-8:e.x+e.width+8,s=Math.max(24,e.y-e.height/2-16),c=a?`end`:`start`,l=Xn(e.id);return`
        <g class="sankey-node" transform="translate(${e.x}, ${e.y-e.height/2})">
          <rect width="${e.width}" height="${e.height}" rx="7" fill="${l}" stroke="${l}"></rect>
        </g>
        <g class="sankey-node-label" transform="translate(${o}, ${s})">
          <text text-anchor="${c}">${G(e.label)}</text>
          <text class="sankey-node-count" y="16" text-anchor="${c}">${G(i)} roles</text>
        </g>
      `}).join(``);return`
    <svg class="sankey-svg" viewBox="0 0 ${r.width} ${r.height}" role="img" aria-label="role state transition sankey diagram">
      <g>${o}</g>
      <g>${s}</g>
    </svg>
  `}function Xn(e){return wt.get(String(e).toLowerCase())??`#4f6472`}function Zn({isBacktrack:e,sourceX:t,sourceY:n,targetX:r,targetY:i,width:a}){let o=a/2,s=n-o,c=n+o,l=i-o,u=i+o;if(e){let e=Math.max(80,Math.abs(t-r)*.42);return[`M ${t} ${s}`,`C ${t-e} ${s}, ${r+e} ${l}, ${r} ${l}`,`L ${r} ${u}`,`C ${r+e} ${u}, ${t-e} ${c}, ${t} ${c}`,`Z`].join(` `)}let d=Math.max(46,(r-t)*.48);return[`M ${t} ${s}`,`C ${t+d} ${s}, ${r-d} ${l}, ${r} ${l}`,`L ${r} ${u}`,`C ${r-d} ${u}, ${t+d} ${c}, ${t} ${c}`,`Z`].join(` `)}function Qn(e,r){let i=new Map([[`discovered`,0],[`interested`,1],[`disinterested`,2],[`applied`,2],[`oa`,3],[`interview`,3],[`rejected`,4],[`closed`,4],[`archived`,4]]),a=new Map,o=new Map;r.forEach(e=>{a.set(e.target,(a.get(e.target)??0)+Number(e.value??0)),o.set(e.source,(o.get(e.source)??0)+Number(e.value??0))});let s=e.filter(e=>Number(e?.history_count??e?.current_count??0)>0||a.has(e.id)||o.has(e.id)),c=new Set(s.map(e=>e.id)),l=r.filter(e=>c.has(e.source)&&c.has(e.target)&&Number(e.value??0)>0),u=e=>i.get(String(e).toLowerCase())??0,d=l.filter(e=>u(e.target)>=u(e.source)),f=l.filter(e=>u(e.target)<u(e.source)),ee={nodes:s.map(e=>({...e,fixedValue:Math.max(0,Number(e?.history_count??e?.current_count??0))})),links:d.map(e=>({...e}))},te=t().nodeId(e=>e.id).nodeWidth(26).nodePadding(44).nodeAlign((e,t)=>Math.min(t-1,u(e.id))).extent([[92,88],[1014,634]]).iterations(32)(ee),ne=new Map;te.nodes.forEach(e=>{ne.set(e.id,{...e,x:e.x0,y:e.y0+(e.y1-e.y0)/2,width:e.x1-e.x0,height:Math.max(1.5,e.y1-e.y0),value:Number(e.fixedValue??e.value??0)})});let re=new Map,p=[],ie=n();te.links.forEach(e=>{let t={source:e.source.id,target:e.target.id,value:e.value};p.push(t),re.set(t,{path:ie(e),width:Math.max(1.5,e.width),sourceY:e.y0,targetY:e.y1,priority:Number(e.value??0)>=20})});let ae=Math.max(.6,...te.links.map(e=>Number(e.width??0)/Math.max(1,Number(e.value??0))));return f.forEach(e=>{let t=ne.get(e.source),n=ne.get(e.target);if(!t||!n)return;let r=Math.max(1.5,Number(e.value??0)*ae),i={...e};p.push(i),re.set(i,{width:r,sourceY:t.y+t.height/2-r/2,targetY:n.y+n.height/2-r/2,priority:!1})}),p.sort((e,t)=>Number(e.value??0)-Number(t.value??0)),{flowLinks:p,height:720,links:re,nodes:ne,width:1120}}function $n(e){let t=Array.isArray(e?.path)?e.path:[];return`
    <article class="sankey-path-row">
      <div>
        <strong>${G(e?.company_name??`unknown company`)} / ${G(e?.title??`untitled role`)}</strong>
        <span>${t.map(e=>G(e)).join(` -> `)}</span>
      </div>
      <span class="metrics-status-pill">${Number(e?.loops_collapsed??0).toLocaleString()} loops</span>
    </article>
  `}async function er(){We.hidden=!0,document.body.classList.remove(`settings-open`),ct.hidden=!1,document.body.classList.add(`sankey-open`),lt.focus(),Ht?Jn(Ht):(T.textContent=`loading role flow...`,T.classList.remove(`is-empty`),ut.innerHTML=``,dt.innerHTML=``);try{await nr()}catch{T.textContent=`could not load role flow.`}}function tr(){ct.hidden=!0,document.body.classList.remove(`sankey-open`),Ue.focus()}async function nr(){let e=await fetch(`/api/role-sankey`);if(!e.ok)throw Error(`Role sankey request failed`);Jn(await e.json())}async function rr(e){let t=e.name;if(!t)return;let n=e.type===`checkbox`?!e.checked:Bt?.settings?.find(e=>e.key===t)?.value,r=e.type===`checkbox`?e.checked:e.value;J(!0),x.textContent=`saving settings...`,x.classList.remove(`is-empty`);try{let e=await fetch(`/api/config`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({[t]:r})});if(!e.ok)throw Error(`Config update failed`);q(await e.json(),`settings saved.`)}catch{e.type===`checkbox`?e.checked=n:n!==void 0&&(e.value=n),x.textContent=`could not save settings.`,J(!1)}}async function ir(){et.disabled=!0,x.textContent=`clearing recommendation history...`,x.classList.remove(`is-empty`);try{let e=await fetch(`/api/recommendation-history/clear`,{method:`POST`});if(!e.ok)throw Error(`Recommendation history clear failed`);let t=await e.json();q(t.config,`cleared ${t.deleted_count} saved decisions.`)}catch{x.textContent=`could not clear recommendation history.`,et.disabled=!1}}async function ar(){let e=S.value.trim();if(!e){x.textContent=`central api url is required.`,x.classList.remove(`is-empty`);return}let t={central_api_url:e},n=Ze.value.trim();n&&(t.central_passkey=n),J(!0),x.textContent=`saving central settings...`,x.classList.remove(`is-empty`);try{let e=await fetch(`/api/config`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(t)});if(!e.ok)throw Error(`Central settings update failed`);q(await e.json(),`central settings saved.`)}catch{x.textContent=`could not save central settings.`,J(!1)}}async function or(){C.disabled=!0,x.textContent=`syncing remote company ids...`,x.classList.remove(`is-empty`);try{let e=await fetch(`/api/central/resolve-companies`,{method:`POST`});if(!e.ok)throw Error(`Central company sync failed`);let t=await e.json(),n=t.result??{},r=t.pulled_companies,i=r?` remote: ${Number(r.created??0)} created, ${Number(r.linked??0)} linked, ${Number(r.existing??0)} existing.`:``;q(t.config,`company sync: ${Number(n.linked??0)} matched, ${Number(n.created??0)} created, ${Number(n.needs_review??0)} review, ${Number(n.failed??0)} failed.${i}`),t.companies&&(B=t.companies,dr(t.companies.companies))}catch{x.textContent=`could not sync companies.`,C.disabled=!S.value.trim()}}async function sr(){let e=await fetch(`/api/central/resolve-companies`,{method:`POST`});if(!e.ok)throw Error(`Central company sync failed`);let t=await e.json();t.companies&&(B=t.companies,dr(t.companies.companies))}async function cr(){let e=sr().catch(()=>{});await Promise.all([Y().catch(()=>{i.innerHTML=`<p class="empty-copy">could not load jobs.</p>`}),yr().catch(()=>{bt.textContent=`could not load companies.`})]),await e}async function lr(){if(window.confirm(`Update callumployed and restart the tracker?`)){J(!0),ft.disabled=!0,x.textContent=`updating callumployed; tracker will restart shortly...`,x.classList.remove(`is-empty`);try{if(!(await fetch(`/api/app/update`,{method:`POST`})).ok)throw Error(`App update failed`);x.textContent=`update started. reconnect in a moment.`}catch{x.textContent=`could not start update.`,J(!1)}}}function ur(e,t=``){B=e;let n=Array.isArray(e?.companies)?e.companies:[];if(dr(n),E.textContent=t||`${n.length} ${n.length===1?`company`:`companies`} stored`,E.classList.toggle(`is-empty`,n.length===0&&!t),n.length===0){D.innerHTML=`<p class="empty-copy">no companies yet.</p>`;return}D.innerHTML=n.map(e=>fr(e)).join(``)}function dr(e){Ut=Array.isArray(e)?e:[],yt.innerHTML=Ut.map(e=>`<option value="${U(e.name)}"></option>`).join(``)}function fr(e){let t=Array.isArray(e.career_pages)?e.career_pages:[],n=H(e.updated_at),r=pr(e.prestige_tier),i=Number(e.scan_count??0),a=Number(e.discovered_role_count??0),o=i>0&&a===0?`<span class="company-discovery-status">Discovered 0 potential roles</span>`:``;return`
    <details class="company-panel ${r}" data-company-id="${e.id}">
      <summary class="company-summary">
        <span class="company-chevron">></span>
        <span class="company-summary-main">
          <span class="company-name">${G(e.name)}</span>
          <span class="company-summary-meta">${t.length} ${t.length===1?`link`:`links`}${n?` | updated ${G(n)}`:``}</span>
          ${o}
        </span>
      </summary>
      <div class="company-body">
        <div class="company-info">
          <label class="company-notes-field">
            <span>notes</span>
            <textarea data-company-notes="${e.id}" rows="3">${U(e.notes??``)}</textarea>
          </label>
          <label>
            <span>tier</span>
            <select data-company-tier="${e.id}">
              ${mr(e.prestige_tier)}
            </select>
          </label>
          <div>
            <span>browser wait</span>
            <strong>${Number(e.browser_extra_wait_ms??0)}ms</strong>
          </div>
        </div>
        <div class="company-links">
          ${t.length>0?t.map(e=>hr(e)).join(``):`<p class="company-empty-links">no career links yet.</p>`}
        </div>
        <section class="company-link-panel" aria-label="add career link">
          <form class="company-link-form" data-company-link-form="${e.id}">
            <input name="label" type="text" placeholder="label" aria-label="career link label" />
            <input name="url" type="url" placeholder="https://..." aria-label="career link url" required />
            <button class="company-link-add" type="submit" aria-label="add career link" title="add career link">
              ${Qt()}
            </button>
          </form>
        </section>
        <div class="company-danger-row">
          <button class="company-delete-button" type="button" data-delete-company="${e.id}">
            ${$t()}
            <span>deactivate company</span>
          </button>
        </div>
      </div>
    </details>
  `}function pr(e){let t=String(e??``);return[`0`,`1`,`2`,`3`,`4`].includes(t)?`company-tier-${t}`:`company-tier-unset`}function mr(e){let t=String(e??``);return[``,`0`,`1`,`2`,`3`,`4`].map(e=>{let n=e?`tier ${e}`:`not set`,r=e===t?` selected`:``;return`<option value="${U(e)}"${r}>${G(n)}</option>`}).join(``)}function hr(e){let t=e.label?G(e.label):`career page`,n=U(e.url);return`
    <div class="company-link-row" data-career-page-id="${e.id}">
      <a class="company-link-url" href="${n}" target="_blank" rel="noreferrer">
        <span class="company-link-label">${t}</span>
        <span class="company-link-text">${U(e.url)}</span>
      </a>
      <button class="company-link-delete" type="button" data-delete-career-page="${e.id}" aria-label="delete ${t} link" title="delete link">
        ${$t()}
      </button>
    </div>
  `}async function gr(){pt.hidden=!1,document.body.classList.add(`companies-open`),mt.focus(),B?ur(B):(E.textContent=`loading companies...`,E.classList.remove(`is-empty`),D.innerHTML=``);try{await vr()}catch{E.textContent=`could not load companies.`}}function _r(){pt.hidden=!0,document.body.classList.remove(`companies-open`),Ne.focus()}async function vr(e=``){let t=await fetch(`/api/companies`);if(!t.ok)throw Error(`Companies request failed`);ur(await t.json(),e)}async function yr(){let e=await fetch(`/api/companies`);if(!e.ok)throw Error(`Companies request failed`);dr((await e.json()).companies)}async function br(e){let t=new FormData(e),n={name:String(t.get(`name`)??``),career_url:String(t.get(`career_url`)??``),notes:String(t.get(`notes`)??``)};E.textContent=`adding company...`;let r=await fetch(`/api/companies`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(n)});if(!r.ok)throw Error(`Company create failed`);e.reset(),ur(await r.json(),`company added.`),Y(V()).catch(()=>{})}async function xr(e){let t=e.dataset.companyLinkForm;if(!t)return;let n=new FormData(e),r={label:String(n.get(`label`)??``),url:String(n.get(`url`)??``)};E.textContent=`adding link...`;let i=await fetch(`/api/companies/${encodeURIComponent(t)}/career-pages`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(r)});if(!i.ok)throw Error(`Career page create failed`);e.reset(),ur(await i.json(),`link added.`)}async function Sr(e){E.textContent=`deleting link...`;let t=await fetch(`/api/company-career-pages/${encodeURIComponent(e)}`,{method:`DELETE`});if(!t.ok)throw Error(`Career page delete failed`);ur(await t.json(),`link deleted.`)}async function Cr(e){E.textContent=`deactivating company...`;let t=await fetch(`/api/companies/${encodeURIComponent(e)}`,{method:`DELETE`});if(!t.ok)throw Error(`Company deactivate failed`);ur(await t.json(),`company deactivated.`),Y(V()).catch(()=>{})}function wr(){let e=vt.value.trim().toLocaleLowerCase();return Ut.find(t=>t.name.toLocaleLowerCase()===e)}async function Tr(e){let t=wr();if(!t?.id){bt.textContent=`pick a saved company.`;return}let n=new FormData(e),r={company_id:t.id,role_url:String(n.get(`role_url`)??``)};bt.textContent=`adding role...`;let i=await fetch(`/api/roles`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(r)});if(!i.ok)throw Error(`Role create failed`);let a=await i.json();a.tracker?On(a.tracker):await Y(V()),_t.value=``;let o=a.role?.title?W(a.role.title):`role`;bt.textContent=a.scan_error?`${o} added; scan could not finish.`:`${o} added.`}function Er(e){return(Array.isArray(B?.companies)?B.companies:[]).find(t=>String(t.id)===String(e))}function Dr(e){E.textContent=e,E.classList.remove(`is-empty`)}function Or(e){window.clearTimeout(Wt.get(e)),Wt.set(e,window.setTimeout(()=>{kr(e).catch(()=>{Dr(`could not save company.`)})},700))}async function kr(e){let t=D.querySelector(`[data-company-id="${CSS.escape(String(e))}"]`);if(!t)return;let n=t.querySelector(`[data-company-notes="${CSS.escape(String(e))}"]`),r=t.querySelector(`[data-company-tier="${CSS.escape(String(e))}"]`),i=Er(e),a={notes:n?.value??i?.notes??``,prestige_tier:r?.value??i?.prestige_tier??``};i&&(i.notes=a.notes,i.prestige_tier=a.prestige_tier),Ar(t,a.prestige_tier),Dr(`saving company...`);let o=await fetch(`/api/companies/${encodeURIComponent(e)}`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(a)});if(!o.ok)throw Error(`Company update failed`);B=await o.json(),Dr(`company saved.`),jr(e)}function Ar(e,t){e.classList.remove(`company-tier-unset`,`company-tier-0`,`company-tier-1`,`company-tier-2`,`company-tier-3`,`company-tier-4`),e.classList.add(pr(t))}function jr(e){let t=D.querySelector(`[data-company-id="${CSS.escape(String(e))}"]`),n=Er(e);if(!t||!n)return;let r=Array.isArray(n.career_pages)?n.career_pages:[],i=H(n.updated_at),a=t.querySelector(`.company-summary-meta`);a&&(a.textContent=`${r.length} ${r.length===1?`link`:`links`}${i?` | updated ${i}`:``}`)}async function Mr(){let e=await fetch(`/api/scan/status`);if(e.status===404){v.disabled=!0,y.hidden=!0,y.classList.add(`scan-error`),b.textContent=`restart server to enable scanning`;return}if(!e.ok)throw Error(`Scan status request failed`);kn(await e.json())}function Nr(){Lt===null&&(Lt=window.setInterval(()=>{Mr().catch(()=>{})},3e3))}async function Pr(){v.disabled=!0,v.textContent=`starting...`;try{let e=await fetch(`/api/scan/all`,{method:`POST`});if(e.status===404){v.disabled=!0,v.textContent=`scan roles`,y.hidden=!0,y.classList.add(`scan-error`),b.textContent=`restart server to enable scanning`;return}if(!e.ok&&e.status!==409)throw Error(`Scan start failed`);kn(await e.json()),Nr()}catch{v.disabled=!1,v.textContent=`scan roles`,y.hidden=!0,y.classList.add(`scan-error`),b.textContent=`could not start scan`}}async function Fr(){v.disabled=!0,v.textContent=`cancelling...`;try{let e=await fetch(`/api/scan/cancel`,{method:`POST`});if(e.status===404){v.disabled=!0,v.textContent=`scan roles`,y.hidden=!0,y.classList.add(`scan-error`),b.textContent=`restart server to enable scanning`;return}if(!e.ok&&e.status!==409)throw Error(`Scan cancel failed`);kn(await e.json()),Nr()}catch{v.disabled=!1,v.textContent=`cancel scan`,y.hidden=!1,y.classList.add(`scan-error`),b.textContent=`could not cancel scan`}}async function Y(e=``){i.innerHTML=`<p class="empty-copy">loading jobs...</p>`;let t=new URLSearchParams;e&&t.set(`q`,e);let n=await fetch(`/api/tracker?${t.toString()}`);if(!n.ok)throw Error(`Tracker request failed`);On(await n.json())}async function Ir(e={}){let t=await fetch(`/api/application-materials`);if(!t.ok)throw Error(`Application materials request failed`);un(await t.json(),e)}async function Lr(e){if(e){if(!e.name.toLowerCase().endsWith(`.tex`)){rn(Dt,`resume must be a .tex file.`);return}ie.disabled=!0,rn(Dt,`uploading...`);try{let t=await e.text();if(!(await fetch(`/api/master-resume`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({filename:e.name,content:t})})).ok)throw Error(`Master resume upload failed`);await Ir()}catch{rn(Dt,`could not save resume.`),dn()}finally{p.value=``,ie.disabled=!1}}}async function Rr(e){let t=Array.from(e??[]);if(t.length!==0){se.disabled=!0,ln(k,`uploading ${t.length} ${t.length===1?`resource`:`resources`}...`);try{for(let e of t)if(!(await fetch(`/api/resume-resources`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({filename:e.name,content_base64:await Vr(e)})})).ok)throw Error(`Resume resource upload failed`);await Ir()}catch{ln(k,`could not save every resource.`),dn()}finally{oe.value=``,se.disabled=!1}}}async function zr(e){let t=Array.from(e??[]);if(t.length!==0){de.disabled=!0,on(A,`uploading ${t.length} ${t.length===1?`example`:`examples`}...`);try{for(let e of t){let t={filename:e.name};if([`.pdf`,`.docx`].some(t=>e.name.toLowerCase().endsWith(t))?t.content_base64=await Vr(e):t.content=await e.text(),!(await fetch(`/api/cover-letter-examples`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(t)})).ok)throw Error(`Cover letter example upload failed`)}await Ir()}catch{on(A,`could not save every example.`),dn()}finally{ue.value=``,de.disabled=!1}}}async function Br(e){let t=Array.from(e??[]);if(t.length!==0){he.disabled=!0,sn(j,`uploading ${t.length} ${t.length===1?`note`:`notes`}...`);try{for(let e of t){let t=e.name.toLowerCase(),n={filename:e.name};if(t.endsWith(`.pdf`)||t.endsWith(`.docx`)?n.content_base64=await Vr(e):n.content=await e.text(),!(await fetch(`/api/experience-notes`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(n)})).ok)throw Error(`Experience note upload failed`)}F.clear(),await Ir()}catch{sn(j,`could not save every note.`),dn()}finally{me.value=``,he.disabled=!1}}}function Vr(e){return new Promise((t,n)=>{let r=new FileReader;r.addEventListener(`load`,()=>{let e=String(r.result??``);t(e.includes(`,`)?e.split(`,`,2)[1]:e)}),r.addEventListener(`error`,()=>n(r.error)),r.readAsDataURL(e)})}c.addEventListener(`submit`,e=>{e.preventDefault(),Y(l.value.trim()),qt()}),a.addEventListener(`click`,()=>{if(V()){Y();return}Kt()}),l.addEventListener(`keydown`,e=>{e.key===`Escape`&&(e.stopPropagation(),qt())}),u.addEventListener(`click`,qt),s.addEventListener(`click`,qt),ie.addEventListener(`click`,()=>{p.click()}),p.addEventListener(`change`,()=>{Lr(p.files?.[0])}),se.addEventListener(`click`,()=>{oe.click()}),oe.addEventListener(`change`,()=>{Rr(oe.files)}),de.addEventListener(`click`,()=>{ue.click()}),ue.addEventListener(`change`,()=>{zr(ue.files)}),he.addEventListener(`click`,()=>{me.click()}),me.addEventListener(`change`,()=>{Br(me.files)}),f.addEventListener(`click`,()=>{fn(f.getAttribute(`aria-expanded`)===`true`)}),ee.addEventListener(`click`,e=>{let t=e.target.closest(`[data-material-view]`);if(t){mn(t);return}let n=e.target.closest(`[data-material-remove]`);n&&hn(n)}),v.addEventListener(`click`,()=>{if(zt?.scanning){Fr();return}Pr()}),i.addEventListener(`click`,e=>{let t=e.target.closest(`[data-review-role-id]`);if(t){ei(t.dataset.reviewRoleId);return}let n=e.target.closest(`[data-prep-role-id]`);if(n){ni(n.dataset.prepRoleId);return}let r=e.target.closest(`.job-action`);if(r){Hr(r);return}let i=e.target.closest(`.pane-toggle`);if(!i)return;let a=i.parentElement.querySelector(`.pane-body`),o=i.getAttribute(`aria-expanded`)===`true`;i.setAttribute(`aria-expanded`,String(!o)),i.querySelector(`.chevron`).textContent=o?`>`:`v`,a.hidden=o,la()});async function Hr(e){let{roleId:t,status:n}=e.dataset;if(!t||!n)return;let r=e.closest(`.job-actions`),i=e.closest(`.job`);r.querySelectorAll(`button`).forEach(e=>{e.disabled=!0}),e.textContent=`updating...`;try{let e=await fetch(`/api/roles/${encodeURIComponent(t)}/status`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({status:n})});if(!e.ok)throw Error(`Status update failed`);Ur((await e.json()).role,i)}catch{r.querySelectorAll(`button`).forEach(e=>{e.disabled=!1}),e.textContent=n===`disinterested`?`disinterested`:n.toLowerCase()}}function Ur(e,t){if(!e||!O)return;let n=t?.closest(`.status-pane`)?.dataset.bucket??e.role_status,r=e.role_status,i=Gr(e,n,r);Kr(n,r),qr(n,r),nn(),Xr(O.statuses),Qr(O.statuses),Jr(t,i,n,r),la()}function Wr(e){if(!e||!O)return null;let t=null;return O.statuses.forEach(n=>{let r=n.jobs.findIndex(t=>String(t.id)===String(e.id));r!==-1&&(t={...n.jobs[r],...e},n.jobs[r]=t)}),Xr(O.statuses),Qr(O.statuses),t}function Gr(e,t,n){let r=e;O.statuses.forEach(t=>{let n=t.jobs.findIndex(t=>String(t.id)===String(e.id));n!==-1&&(r={...t.jobs[n],...e},t.jobs.splice(n,1),t.count=t.jobs.length)});let i=O.statuses.find(e=>e.key===n);return i&&(i.jobs.unshift(r),i.count=i.jobs.length),r}function Kr(e,t){O.statuses.forEach(e=>{let t=document.querySelector(`#status-${CSS.escape(e.key)}`);t?.classList.toggle(`empty`,e.count===0);let n=t?.querySelector(`.count`);n&&(n.textContent=e.count)}),[e,t].forEach(e=>{Yr(document.querySelector(`#status-${CSS.escape(e)}`))})}function qr(e,t){if(!O.stats)return;let n=Ct.has(e),r=Ct.has(t);if(n===r){tn(O.stats);return}O.stats.applications_total=Number(O.stats.applications_total??0)+(r?1:-1),tn(O.stats)}function Jr(e,t,n,r){let i=document.querySelector(`#status-${CSS.escape(r)}`),a=i?.querySelector(`.pane-body`);if(!e||!i||!a)return;e.remove(),Yr(document.querySelector(`#status-${CSS.escape(n)}`)),a.hidden=!1;let o=i.querySelector(`.pane-toggle`);o?.setAttribute(`aria-expanded`,`true`);let s=o?.querySelector(`.chevron`);s&&(s.textContent=`v`);let c=a.querySelector(`.jobs`);c||=(a.innerHTML=`<div class="jobs"></div>`,a.querySelector(`.jobs`)),c.insertAdjacentHTML(`afterbegin`,_n(t,r)),Yr(i)}function Yr(e){if(!e)return;let t=e.querySelector(`.pane-body`);if(!t)return;let n=t.querySelector(`.jobs`),r=!!n?.querySelector(`.job`),i=t.querySelector(`.empty-copy`);if(r){i?.remove();return}n?.remove(),i||t.insertAdjacentHTML(`beforeend`,`<p class="empty-copy">no jobs in this status.</p>`)}function Xr(e){ye.disabled=Zr(e).length===0,ye.setAttribute(`aria-label`,`review discovered`),ye.innerHTML=`<span class="review-discovered-label">review discovered</span>`}function Zr(e=O?.statuses??[]){return e.find(e=>e.key===`discovered`)?.jobs??[]}function Qr(e){be.disabled=$r(e).length===0,be.setAttribute(`aria-label`,`prep interested`),be.innerHTML=`<span class="review-discovered-label">prep interested</span>`}function $r(e=O?.statuses??[]){return e.find(e=>e.key===`interested`)?.jobs??[]}function ei(e=null){let t=[...Zr()],n=e==null?null:String(e);if(n){let e=t.findIndex(e=>String(e.id)===n);if(e>0){let[n]=t.splice(e,1);t.unshift(n)}}N=t,m.hidden=!1,document.body.classList.add(`review-open`),ii()}function ti(){m.hidden=!0,document.body.classList.remove(`review-open`),N=[]}function ni(e=null){let t=[...$r()].sort((e,t)=>Number(!!t.prep_started)-Number(!!e.prep_started)),n=e==null?null:String(e);if(n){let e=t.findIndex(e=>String(e.id)===n);if(e>0){let[n]=t.splice(e,1);t.unshift(n)}}P=t,h.hidden=!1,document.body.classList.add(`prep-open`),bi()}function ri(){h.hidden=!0,document.body.classList.remove(`prep-open`),P=[]}function ii(e=``){let t=N[0],n=N.length,r=t?ai(t):``;if(xe.textContent=n>0?`review queue`:`review complete`,Se.textContent=n>0?`${n} discovered ${n===1?`role`:`roles`} in queue`:``,m.querySelectorAll(`.review-action`).forEach(e=>{e.disabled=n===0}),!t){Ce.innerHTML=`
      <div class="review-empty">
        <h3>no discovered jobs left.</h3>
        <p>everything in this queue has been handled or moved out of discovered.</p>
      </div>
    `;return}Ce.innerHTML=`
    ${e?`<p class="review-message">${U(e)}</p>`:``}
    ${r?`<p class="review-message review-message-warning">${U(r)}</p>`:``}
    <div class="review-title-row">
      <p class="review-company">${G(t.company_name)}</p>
      ${en(t.title,t.role_url,`review-role-title`)}
    </div>
    <dl class="review-details review-primary-details">
      ${X(`location`,t.location,!1,`review-location-detail`)}
      ${X(`first`,H(t.first_seen_at))}
      ${X(`last`,H(t.last_seen_at))}
    </dl>
    ${oi(t.description)}
    <dl class="review-details review-technical-details">
      ${X(`notes`,t.notes,!1,`review-wide-detail`)}
      ${X(`company id`,t.company_id)}
      ${X(`role id`,t.id)}
      ${X(`status`,t.role_status)}
      ${X(`posting id`,t.posting_id)}
      ${X(`created`,H(t.created_at))}
      ${X(`updated`,H(t.updated_at))}
      ${X(`url`,t.role_url,!0,`review-wide-detail`)}
    </dl>
  `}function ai(e){let t=Number(e.review_later_count??0);return t<=xt?``:`role review has been postponed ${t} times. it is recommended to set it to disinterested.`}function X(e,t,n=!1,r=``){if(!t)return``;let i=n?`<a href="${U(t)}" target="_blank" rel="noreferrer">${G(t)}</a>`:G(t);return`
    <div class="review-detail ${U(r)}">
      <dt>${G(e)}</dt>
      <dd>${i}</dd>
    </div>
  `}function oi(e){return e?`
    <div class="review-detail review-description">
      <dt>description</dt>
      <dd>${si(e)}</dd>
    </div>
  `:``}function si(e){let t=ci(String(e)).replace(/\u00a0/g,` `);if(li(t))return ui(t);let n=t.split(/\r?\n/).map(e=>e.trim()).filter(Boolean),r=[],i=[],a=()=>{i.length!==0&&(r.push(`<ul>${i.map(e=>`<li>${e}</li>`).join(``)}</ul>`),i=[])};return n.forEach(e=>{let t=e.match(/^#{2,3}\s+(.+)$/);if(t){a(),r.push(`<h3>${G(t[1])}</h3>`);return}if(vi(e)){a(),r.push(`<h3>${G(e.replace(/:$/,``))}</h3>`);return}let n=e.match(/^[-*]\s+(.+)$/);if(n){i.push(G(n[1]));return}a(),r.push(`<p>${G(e)}</p>`)}),a(),r.join(``)}function ci(e){let t=document.createElement(`textarea`);return t.innerHTML=e,t.value}function li(e){return/<\/?(?:a|br|div|em|h[1-6]|li|ol|p|span|strong|ul)\b/i.test(e)}function ui(e){let t=document.createElement(`template`);t.innerHTML=e;let n=[];return di(t.content.childNodes,n),n.join(``)}function di(e,t){e.forEach(e=>{if(e.nodeType===Node.TEXT_NODE){let n=gi(e.textContent);n&&t.push(`<p>${G(n)}</p>`);return}if(e.nodeType!==Node.ELEMENT_NODE)return;let n=e,r=n.tagName.toLowerCase();if(r===`script`||r===`style`||r===`br`)return;if(/^h[1-6]$/.test(r)){pi(t,n.textContent);return}if(r===`ul`||r===`ol`){let e=mi(n);e&&t.push(e);return}if(r===`p`){fi(n,t);return}let i=Array.from(n.children).some(e=>[`DIV`,`H1`,`H2`,`H3`,`H4`,`H5`,`H6`,`OL`,`P`,`UL`].includes(e.tagName));if([`article`,`div`,`section`].includes(r)&&i){di(n.childNodes,t);return}let a=Array.from(n.children).filter(e=>[`UL`,`OL`].includes(e.tagName)),o=gi(hi(n));if(o&&(_i(o,n)?pi(t,o):t.push(`<p>${G(o)}</p>`)),a.length>0){a.forEach(e=>{let n=mi(e);n&&t.push(n)});return}!o&&i&&di(n.childNodes,t)})}function fi(e,t){if(!e.querySelector(`br`)){let n=gi(hi(e));if(!n)return;_i(n,e)?pi(t,n):t.push(`<p>${G(n)}</p>`);return}let n=``,r=()=>{let r=gi(n);n=``,r&&(_i(r,e)?pi(t,r):t.push(`<p>${G(r)}</p>`))};e.childNodes.forEach(e=>{if(e.nodeType===Node.ELEMENT_NODE&&e.tagName.toLowerCase()===`br`){r();return}n+=` ${e.textContent??``}`}),r()}function pi(e,t){let n=gi(t).replace(/:$/,``);n&&e.push(`<h3>${G(n)}</h3>`)}function mi(e){let t=Array.from(e.children).filter(e=>e.tagName===`LI`).map(e=>{let t=gi(hi(e)),n=Array.from(e.children).filter(e=>[`UL`,`OL`].includes(e.tagName)).map(e=>mi(e)).filter(Boolean).join(``);return t||n?`<li>${G(t)}${n}</li>`:``}).filter(Boolean);return t.length>0?`<ul>${t.join(``)}</ul>`:``}function hi(e){let t=e.cloneNode(!0);return t.querySelectorAll(`ul, ol`).forEach(e=>{e.remove()}),t.textContent}function gi(e){return String(e??``).replace(/\s+/g,` `).trim()}function _i(e,t){let n=e.replace(/:$/,``).trim();return!n||n.length>90?!1:vi(n)||/:$/.test(e)?!0:/[.!?]$/.test(n)||n.split(/\s+/).length>10?!1:t.querySelector(`strong, b, u`)?!0:vi(n)}function vi(e){return Tt.test(String(e).trim())}async function yi(e){let t=N[0];if(!t)return;if(e===`later`){m.querySelectorAll(`.review-action`).forEach(e=>{e.disabled=!0});try{let e=await Ui(t.id);N.shift(),Wr(e),ii(`moved out of this review pass.`)}catch{ii(`could not postpone that role. try again.`)}finally{m.querySelectorAll(`.review-action`).forEach(e=>{e.disabled=N.length===0})}return}if(![`interested`,`disinterested`].includes(e))return;let n=m.querySelectorAll(`.review-action`);n.forEach(e=>{e.disabled=!0});try{let n=await Wi(t.id,e);N.shift(),ii(e===`interested`?`marked interested.`:`marked disinterested.`),Ur(n,document.querySelector(`.job[data-role-id="${CSS.escape(String(t.id))}"]`))}catch{n.forEach(e=>{e.disabled=!1}),ii(`could not update that role. try again.`)}}async function bi(e=``){let t=P[0],n=P.length;if(Te.textContent=n>0?`prep queue`:`prep complete`,Ee.textContent=n>0?`${n} interested ${n===1?`role`:`roles`} in queue`:``,h.querySelectorAll(`.review-action`).forEach(e=>{e.disabled=n===0}),!t){g.innerHTML=`
      <div class="review-empty">
        <h3>no interested jobs left.</h3>
        <p>everything in this queue has been prepped, moved, or postponed.</p>
      </div>
    `;return}g.innerHTML=`
    ${e?`<p class="review-message">${U(e)}</p>`:``}
    <section class="prep-role-hero" aria-label="role overview">
      <div class="review-title-row">
        <div class="prep-role-eyebrow">
          <p class="review-company">${G(t.company_name)}</p>
          <span>application workspace</span>
        </div>
        ${en(t.title,t.role_url,`review-role-title`)}
      </div>
      <dl class="review-details review-primary-details">
        ${X(`location`,t.location,!1,`review-location-detail`)}
        ${X(`last`,H(t.last_seen_at))}
        ${X(`updated`,H(t.updated_at))}
      </dl>
      <nav class="prep-workspace-nav" aria-label="prep sections">
        <button type="button" data-prep-section-target="prep-resume-${t.id}">
          <span>01</span> resume
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
      ${xi(t)}
      ${Ti(t)}
      ${Si(t.id,t.description)}
      ${Ci(t)}
    </div>
  `,K(),ji(t.id).then(e=>{!e||P[0]?.id!==t.id||(I.set(t.id,e),g.querySelector(`.prep-resume`)?.replaceWith(Q(xi(t,{resume:e}))),K())}).catch(()=>{}),Hi(t.id).then(e=>{!e||P[0]?.id!==t.id||(L.set(t.id,e),g.querySelector(`.prep-cover-letter`)?.replaceWith(Q(Ti(t,{coverLetter:e}))),K())}).catch(()=>{})}function xi(e,t={}){let n=I.get(e.id),r=t.resume??n,i=t.tweaks??kt.get(e.id)??``,a=`/api/roles/${encodeURIComponent(e.id)}/resume.pdf`;return t.loading?`
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
          ${r.pdf_base64?`<a class="prep-summary-action prep-cover-pdf-link" href="${U(a)}" target="_blank" rel="noreferrer">view</a>`:``}
        </div>
      </summary>
      <p class="prep-overview">${G(r.summary??`Saved resume for this role.`)}</p>
      ${Z(e)}
      <section class="prep-generation-controls" aria-label="resume refinement">
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
          >${U(i)}</textarea>
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
          >${U(r.latex??``)}</textarea>
        </label>
        <section class="prep-document-preview" aria-label="resume preview">
          <div class="prep-preview-heading">
            <span>document preview</span>
            <p>Updates automatically after the source is saved.</p>
          </div>
          ${r.pdf_base64?`
                <iframe class="prep-cover-pdf" title="resume PDF preview" src="${U(a)}"></iframe>
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
    `}function Si(e,t){return`
    <details class="prep-panel prep-description-panel" id="prep-description-${e}">
      <summary class="prep-analysis-header">
        <span class="prep-accordion-icon" aria-hidden="true"></span>
        <h3>description</h3>
      </summary>
      ${oi(t)}
    </details>
  `}function Ci(e,t={}){let n=t.messages??At.get(e.id)??[],r=!!t.loading;return`
    <details class="prep-panel prep-role-chat" id="prep-chat-${e.id}">
      <summary class="prep-analysis-header">
        <span class="prep-accordion-icon" aria-hidden="true"></span>
        <h3>chat about this role</h3>
        <span>${n.length?`${n.length} messages`:`ready`}</span>
      </summary>
      <div class="prep-role-chat-log" aria-live="polite">
        ${n.length?n.map(wi).join(``):`<p class="prep-role-chat-empty">ask about fit, risks, resume emphasis, or cover letter angle.</p>`}
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
  `}function wi(e){let t=e?.role===`assistant`?`assistant`:`user`;return`
    <article class="prep-role-chat-message prep-role-chat-message-${t}">
      <span>${t}</span>
      <p>${G(e?.content??``)}</p>
    </article>
  `}function Ti(e,t={}){let n=L.get(e.id),r=t.coverLetter??n,i=t.tweaks??r?.tweaks??``,a=`/api/roles/${encodeURIComponent(e.id)}/cover-letter.pdf`;return t.loading?`
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
          ${r?.pdf_base64?`<a class="prep-summary-action prep-cover-pdf-link" href="${U(a)}" target="_blank" rel="noreferrer">view</a>`:``}
        </div>
      </summary>
      ${r?`<p class="prep-overview">${G(r.summary??`cover letter generated`)}</p>`:`<p class="prep-overview">generate a LaTeX cover letter from the resume, posting, and stored examples.</p>`}
      <section class="prep-generation-controls" aria-label="cover letter generation">
        <div class="prep-control-heading">
          <span>${r?`refine this version`:`create a tailored draft`}</span>
          <p>Use the role, resume, and saved examples to shape the letter.</p>
        </div>
        ${r?`
              <label class="prep-cover-tweaks">
                <span>tweak instructions</span>
                <textarea
                  data-prep-cover-letter-tweaks="${e.id}"
                  rows="3"
                  placeholder="make it warmer, cut a paragraph, emphasize systems work..."
                >${U(i)}</textarea>
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
                >${U(r.latex??``)}</textarea>
              </label>
              <section class="prep-document-preview" aria-label="cover letter preview">
                <div class="prep-preview-heading">
                  <span>document preview</span>
                  <p>Updates automatically after the source is saved.</p>
                </div>
                ${r.pdf_base64?`
                      <iframe class="prep-cover-pdf" title="cover letter PDF preview" src="${U(a)}"></iframe>
                    `:`<p class="prep-cover-path">PDF preview unavailable.</p>`}
              </section>
            </div>
          `:``}
    </details>
  `}function Z(e,t={}){let n=F.get(e.id);if(!t.loading&&!t.error&&!t.analysis&&n)return Z(e,{analysis:n});if(!t.loading&&!t.error&&!t.analysis)return`
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
    `;let r=t.analysis,i=Array.isArray(r?.feedback_items)?r.feedback_items:[],a=r?.verdict===`ready_to_apply`?`ready to apply`:`tweak`,o=Math.min(Ot.get(e.id)??0,Math.max(i.length-1,0)),s=i[o];return`
    <section class="prep-analysis" aria-label="ai analysis">
      <div class="prep-analysis-header">
        <h3>ai analysis</h3>
        <span>${i.length} ${i.length===1?`item`:`items`}</span>
      </div>
      <p class="prep-verdict">${G(a)}</p>
      <p class="prep-overview">${G(r?.overview??`analysis unavailable`)}</p>
      ${s?`
            <article class="prep-feedback" data-feedback-index="${o}">
              <p class="prep-feedback-label">${G(s.label)}</p>
              <h4>${G(s.title)}</h4>
              <p>${G(s.detail)}</p>
              ${Ei(s)}
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
  `}function Ei(e){return e?.tweak_prompt?`
    <div class="prep-proposed-edit">
      <p class="prep-proposed-label">tweak prompt</p>
      <p>${G(e.tweak_prompt)}</p>
    </div>
  `:`
      <div class="prep-proposed-edit">
        <p class="prep-proposed-label">feedback only</p>
        <p>not enough information to turn this into a safe resume tweak.</p>
      </div>
    `}async function Di(e,t={}){if(!t.force&&F.has(e))return F.get(e);let n=await fetch(`/api/roles/${encodeURIComponent(e)}/prep-analysis`);if(!n.ok)throw Error(`Prep analysis request failed`);let r=await n.json();return r.analysis.resources=r.resources??[],F.set(e,r.analysis),r.analysis}function Q(e){let t=document.createElement(`template`);return t.innerHTML=e.trim(),t.content.firstElementChild}async function Oi(e){let t=P[0];if(!t)return;let n=h.querySelectorAll(`.review-action`);if(n.forEach(e=>{e.disabled=!0}),e===`later`){try{await Ui(t.id),t.review_later_count=Number(t.review_later_count??0)+1,P.length>1?(P.push(P.shift()),bi(`moved to the back of the prep queue.`)):bi(`only one role is in the prep queue.`)}catch{bi(`could not postpone prep. try again.`)}return}if(e===`applied`)try{let e=await Wi(t.id,`applied`);P.shift(),bi(`moved to applied.`),Ur(e,document.querySelector(`.job[data-role-id="${CSS.escape(String(t.id))}"]`))}catch{n.forEach(e=>{e.disabled=!1}),bi(`could not move that role. try again.`)}}async function ki(e,t,n,r){let i=await fetch(`/api/roles/${encodeURIComponent(e)}/prep-feedback`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({feedback_index:t,feedback_item:n,comment:r})});if(!i.ok)throw Error(`Prep feedback update failed`);return i.json()}async function Ai(e,t,n,r){let i=await fetch(`/api/roles/${encodeURIComponent(e)}/prep-feedback-ignore`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({feedback_index:t,feedback_item:n,comment:r})});if(!i.ok)throw Error(`Prep feedback ignore failed`);return i.json()}async function ji(e,{force:t=!1}={}){if(!t&&I.has(e))return I.get(e);let n=await fetch(`/api/roles/${encodeURIComponent(e)}/resume`);if(!n.ok)throw Error(`Resume request failed`);let r=await n.json();return r.resume&&I.set(e,r.resume),r.resume}async function Mi(e,t){let n=await fetch(`/api/roles/${encodeURIComponent(e)}/resume/save`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({latex:t})});if(!n.ok)throw Error(`Resume save failed`);return n.json()}async function Ni(e,t,n){let r=await fetch(`/api/roles/${encodeURIComponent(e)}/resume`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({tweaks:t,previous_latex:n})});if(!r.ok)throw Error(`Resume generation failed`);return r.json()}async function Pi(e,t){let n=await fetch(`/api/roles/${encodeURIComponent(e)}/chat`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({messages:t})});if(!n.ok)throw Error(`Role chat failed`);return n.json()}function Fi(e,t,n=St){let r=jt.get(e)??{timer:null,saving:!1,version:0,latex:``};r.version+=1,r.latex=t,r.timer&&clearTimeout(r.timer),r.timer=setTimeout(()=>{r.timer=null,Ii(e)},n),jt.set(e,r)}async function Ii(e){let t=jt.get(e);if(!t||t.saving)return;t.saving=!0;let n=t.version,r=t.latex;try{let i=await Mi(e,r);t.version===n&&(I.set(e,i.resume),Li(`resume`,e,i.resume))}catch{}finally{t.saving=!1,t.version!==n&&Fi(e,t.latex,0)}}function Li(e,t,n){if(!n?.pdf_base64)return;let r=e===`resume`?`[data-prep-resume-latex="${t}"]`:`[data-prep-cover-letter-latex="${t}"]`,i=g.querySelector(r)?.closest(`.prep-panel`),a=i?.querySelector(`.prep-cover-pdf`),o=i?.querySelector(`.prep-cover-pdf-link`),s=e===`resume`?`/api/roles/${encodeURIComponent(t)}/resume.pdf`:`/api/roles/${encodeURIComponent(t)}/cover-letter.pdf`;a&&(a.src=`${s}?v=${Date.now()}`),o&&(o.href=s)}async function Ri(e,t=``,n=``){let r=await fetch(`/api/roles/${encodeURIComponent(e)}/cover-letter`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({tweaks:t,previous_latex:n})});if(!r.ok)throw Error(`Cover letter generation failed`);return r.json()}async function zi(e,t){let n=await fetch(`/api/roles/${encodeURIComponent(e)}/cover-letter/save`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({latex:t})});if(!n.ok)throw Error(`Cover letter save failed`);return n.json()}function Bi(e,t,n=``,r=St){let i=Mt.get(e)??{timer:null,saving:!1,version:0,latex:``,tweaks:``};i.version+=1,i.latex=t,i.tweaks=n,i.timer&&clearTimeout(i.timer),i.timer=setTimeout(()=>{i.timer=null,Vi(e)},r),Mt.set(e,i)}async function Vi(e){let t=Mt.get(e);if(!t||t.saving)return;t.saving=!0;let n=t.version,r=t.latex,i=t.tweaks;try{let a=await zi(e,r);t.version===n&&(L.set(e,{...a.cover_letter,tweaks:i}),Li(`coverLetter`,e,a.cover_letter))}catch{}finally{t.saving=!1,t.version!==n&&Bi(e,t.latex,t.tweaks,0)}}async function Hi(e){if(L.has(e))return L.get(e);let t=await fetch(`/api/roles/${encodeURIComponent(e)}/cover-letter`);if(!t.ok)throw Error(`Cover letter request failed`);let n=await t.json();return n.cover_letter&&L.set(e,n.cover_letter),n.cover_letter}async function Ui(e){let t=await fetch(`/api/roles/${encodeURIComponent(e)}/review-later`,{method:`POST`});if(!t.ok)throw Error(`Review later update failed`);return(await t.json()).role}async function Wi(e,t){let n=await fetch(`/api/roles/${encodeURIComponent(e)}/status`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({status:t})});if(!n.ok)throw Error(`Status update failed`);return(await n.json()).role}function Gi(e){return`${e}-${globalThis.crypto?.randomUUID?.()??`${Date.now()}-${Math.random()}`}`}function Ki(e){window.location.hash!==e&&window.history.pushState({},``,e||`${window.location.pathname}${window.location.search}`)}async function qi({seedJobs:e=null}={}){ke.hidden=!1,document.body.classList.add(`prepped-open`),Ki(`#prepped-roles`),e?(R=e,z=z??R[0]?.role_id??null,$()):R.length===0&&(je.textContent=`loading prepared roles...`),await Yi(),Xi()}function Ji({clearHash:e=!0}={}){ke.hidden=!0,document.body.classList.remove(`prepped-open`),Zi(),e&&window.location.hash===`#prepped-roles`&&Ki(``)}async function Yi(){try{let e=await fetch(`/api/autoprep/jobs`);if(!e.ok)throw Error(`Prepped roles request failed`);R=(await e.json()).jobs??[],R.some(e=>Number(e.role_id)===Number(z))||(z=R[0]?.role_id??null),$()}catch{je.textContent=`could not refresh preparation progress.`}}function Xi(){Zi(),R.some(Qi)&&(Nt=window.setInterval(Yi,2e3))}function Zi(){Nt!==null&&window.clearInterval(Nt),Nt=null}function Qi(e){return[`queued`,`generating_resume_tweaks`,`regenerating_resume`,`generating_cover_letter`].includes(e.overall_status)}function $i(e){return{queued:`Queued`,generating_resume_tweaks:`Generating resume tweaks`,regenerating_resume:`Regenerating resume`,generating_cover_letter:`Generating cover letter`,partially_complete:`Partially complete`,ready:`Ready`,failed:`Failed`,interrupted:`Interrupted`,generating_tweaks:`Generating tweaks`,regenerating:`Regenerating`,generating:`Generating`}[e]??W(e)}function $(){let e=R.filter(Qi).length;je.textContent=R.length?`${R.length} prepped ${R.length===1?`role`:`roles`}${e?` · ${e} in progress`:``}`:`No queued or prepared roles.`,Me.innerHTML=R.map(e=>`
    <button type="button" class="prepped-list-item${Number(e.role_id)===Number(z)?` is-active`:``}" data-prepped-role="${e.role_id}">
      <strong>${G(e.company_name)}</strong><span>${G(e.title)}</span>
      <small class="status-${U(e.overall_status)}">${U($i(e.overall_status))}</small>
    </button>`).join(``),ea(),Xi()}function ea(){let e=R.findIndex(e=>Number(e.role_id)===Number(z)),t=R[e];if(!t){_.innerHTML=`<div class="prepped-empty"><h3>nothing prepped yet.</h3><p>Queue Interested roles from Autoprep Interested.</p></div>`;return}let n=G(t.title),r=Yt(t.role_url),i=r?`<a class="prepped-role-link" href="${U(r)}" target="_blank" rel="noopener noreferrer">${n}<span aria-hidden="true">↗</span></a>`:n,a=[[`Location`,t.location||`Unavailable`],[`Added`,H(t.date_added||t.created_at)||`Unavailable`],[`Last seen`,H(t.last_seen_at)||`Unavailable`],[`Posting ID`,t.posting_id||`Unavailable`]];_.innerHTML=`
    <header class="prepped-detail-heading">
      <div><p class="eyebrow">${G(t.company_name)}</p><h3>${i}</h3></div>
      <span class="prepped-status status-${U(t.overall_status)}">${U($i(t.overall_status))}</span>
    </header>
    <dl class="prepped-role-facts">${a.map(([e,t])=>`<div><dt>${U(e)}</dt><dd>${G(t)}</dd></div>`).join(``)}</dl>
    <details class="prepped-role-description">
      <summary>Job description</summary>
      <div class="prepped-description-copy">${G(t.description||`No job description was saved.`).replaceAll(`
`,`<br>`)}</div>
    </details>
    ${t.notes?`<details class="prepped-role-description"><summary>Role notes</summary><div class="prepped-description-copy">${G(t.notes).replaceAll(`
`,`<br>`)}</div></details>`:``}
    <div class="prepped-document-grid">
      ${ta(t,`resume`,`Resume`)}
      ${ta(t,`cover-letter`,`Cover letter`)}
    </div>
    <div class="prepped-detail-actions">
      <button type="button" data-prepped-nav="previous" ${e<=0?`disabled`:``}>Previous</button>
      <button type="button" data-prepped-nav="next" ${e>=R.length-1?`disabled`:``}>Next</button>
      <button type="button" data-autoprep-open-folder ${t.artifact_directory?``:`disabled`}>Open Documents Folder</button>
      <button class="success" type="button" data-autoprep-applied ${t.overall_status===`ready`?``:`disabled`}>Applied</button>
    </div>
    <p class="prepped-safety-note">Autoprep prepares files only. It never submits an application.</p>`}function ta(e,t,n){let r=t===`cover-letter`?`cover_letter`:`resume`,i=e[`${r}_status`],a=e[`${r}_artifact_path`],o=a?.split(`/`).pop()??`Not available`,s=e[`${r}_error`],c=e[`${r}_instruction`]||``,l=`${e.role_id}:${t}`,u=Pt.get(l)??c,d=[`queued`,`generating`,`generating_tweaks`,`regenerating`].includes(i),f=[`failed`,`interrupted`].includes(i)?`<button type="button" data-autoprep-retry="${t}">Retry ${U(n.toLowerCase())}</button>`:``,ee=Ft.has(l),te=`/api/autoprep/roles/${encodeURIComponent(e.role_id)}/documents/${t}.pdf?v=${encodeURIComponent(e.updated_at||``)}`;return`
    <section class="prepped-document status-${U(i)}">
      <div class="prepped-document-heading"><h4>${U(n)}</h4><span>${U($i(i))}</span></div>
      <p class="prepped-filename">${U(o)}</p>
      ${s?`<p class="prepped-error">${U(s)}</p>`:``}
      <div class="prepped-document-actions">
        <button type="button" data-autoprep-preview="${t}" ${a?``:`disabled`}>${ee?`Hide preview`:`Preview PDF`}</button>
        ${f}
      </div>
      <div class="prepped-pdf-preview" data-autoprep-preview-panel="${t}" ${ee&&a?``:`hidden`}>
        ${ee&&a?`<iframe title="${U(n)} PDF preview" src="${U(te)}"></iframe>`:``}
      </div>
      <label class="prepped-comments-label" for="prepped-comments-${U(l)}">Comments for the next version</label>
      <textarea id="prepped-comments-${U(l)}" data-autoprep-comments="${t}" rows="4" placeholder="Describe specific, truthful changes..." ${d?`disabled`:``}>${G(u)}</textarea>
      <button class="prepped-regenerate" type="button" data-autoprep-regenerate="${t}" ${i===`ready`&&String(u).trim()?``:`disabled`}>${d?`Regenerating...`:`Regenerate ${U(n)}`}</button>
    </section>`}async function na(e,t,n){if(n.disabled)return;let r=`${e.role_id}:${t}`,i=_.querySelector(`[data-autoprep-comments="${t}"]`),a=String(i?.value||Pt.get(r)||``).trim();if(!a){i?.focus();return}n.disabled=!0,n.textContent=`Queuing regeneration...`;try{let n=await fetch(`/api/autoprep/roles/${encodeURIComponent(e.role_id)}/regenerate/${t}`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({comments:a,idempotency_key:Gi(`regenerate-${t}`)})}),i=await n.json();if(!n.ok)throw Error(i.error||`Regeneration request failed`);Pt.delete(r);let o=R.findIndex(t=>Number(t.role_id)===Number(e.role_id));o>=0&&(R[o]=i.job),$()}catch(e){window.alert(e instanceof Error?e.message:`Regeneration request failed`),await Yi()}}async function ra(e,t,n){if(!n.disabled){n.disabled=!0,n.textContent=`Queuing retry...`;try{let n=await fetch(`/api/autoprep/roles/${encodeURIComponent(e)}/retry/${t}`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({idempotency_key:Gi(`retry-${t}`)})}),r=await n.json();if(!n.ok)throw Error(r.error||`Retry request failed`);let i=R.findIndex(t=>Number(t.role_id)===Number(e));i>=0&&(R[i]=r.job),$()}catch{await Yi()}}}async function ia(e,t){if(t.disabled)return;t.disabled=!0,t.textContent=`Moving to Applied...`;let n=R.findIndex(t=>Number(t.role_id)===Number(e));try{if(!(await fetch(`/api/autoprep/roles/${encodeURIComponent(e)}/applied`,{method:`POST`})).ok)throw Error(`Applied update failed`);R.splice(n,1),z=R[Math.min(n,R.length-1)]?.role_id??null,$(),cr()}catch{await Yi()}}ye.addEventListener(`click`,ei),we.addEventListener(`click`,ti),be.addEventListener(`click`,ni),Oe.addEventListener(`click`,()=>qi()),Ae.addEventListener(`click`,Ji),Me.addEventListener(`click`,e=>{let t=e.target.closest(`[data-prepped-role]`);t&&(z=Number(t.dataset.preppedRole),$())}),_.addEventListener(`input`,e=>{let t=e.target.closest(`[data-autoprep-comments]`);if(!t)return;let n=`${z}:${t.dataset.autoprepComments}`;Pt.set(n,t.value);let r=_.querySelector(`[data-autoprep-regenerate="${t.dataset.autoprepComments}"]`),i=R.find(e=>Number(e.role_id)===Number(z)),a=t.dataset.autoprepComments===`cover-letter`?`cover_letter`:`resume`;r&&(r.disabled=i?.[`${a}_status`]!==`ready`||!t.value.trim())}),_.addEventListener(`click`,async e=>{let t=R.find(e=>Number(e.role_id)===Number(z));if(!t)return;let n=e.target.closest(`[data-prepped-nav]`);if(n){let e=R.indexOf(t),r=n.dataset.preppedNav===`next`?1:-1;z=R[e+r]?.role_id??t.role_id,$();return}let r=e.target.closest(`[data-autoprep-preview]`);if(r){let e=`${t.role_id}:${r.dataset.autoprepPreview}`;Ft.has(e)?Ft.delete(e):Ft.add(e),ea();return}let i=e.target.closest(`[data-autoprep-regenerate]`);if(i){na(t,i.dataset.autoprepRegenerate,i);return}let a=e.target.closest(`[data-autoprep-retry]`);if(a){ra(t.role_id,a.dataset.autoprepRetry,a);return}let o=e.target.closest(`[data-autoprep-open-folder]`);if(o&&!o.disabled){o.disabled=!0;try{if(!(await fetch(`/api/autoprep/roles/${encodeURIComponent(t.role_id)}/open-folder`,{method:`POST`})).ok)throw Error(`Folder open failed`)}finally{o.disabled=!1}return}let s=e.target.closest(`[data-autoprep-applied]`);s&&ia(t.role_id,s)}),De.addEventListener(`click`,ri),m.addEventListener(`click`,e=>{let t=e.target.closest(`[data-review-action]`);t&&yi(t.dataset.reviewAction)}),h.addEventListener(`click`,e=>{e.target.closest(`.prep-summary-action`)&&e.stopPropagation()}),h.addEventListener(`input`,e=>{let t=e.target.closest(`[data-prep-resume-tweaks]`);if(t){let e=Number(t.dataset.prepResumeTweaks);Number.isFinite(e)&&kt.set(e,t.value);return}let n=e.target.closest(`[data-prep-resume-latex]`);if(n){let e=Number(n.dataset.prepResumeLatex);if(!Number.isFinite(e))return;Fi(e,n.value);return}let r=e.target.closest(`[data-prep-cover-letter-latex]`);if(!r)return;let i=Number(r.dataset.prepCoverLetterLatex);if(!Number.isFinite(i))return;let a=r.closest(`.prep-cover-letter`)?.querySelector(`[data-prep-cover-letter-tweaks="${i}"]`)?.value??``;Bi(i,r.value,a)}),h.addEventListener(`scroll`,e=>{e.target.closest(`[data-prep-resume-latex], [data-prep-cover-letter-latex]`)},!0),h.addEventListener(`focusout`,e=>{let t=e.target.closest(`[data-prep-resume-latex]`);if(t){let e=Number(t.dataset.prepResumeLatex);if(!Number.isFinite(e))return;Fi(e,t.value,0);return}let n=e.target.closest(`[data-prep-cover-letter-latex]`);if(!n)return;let r=Number(n.dataset.prepCoverLetterLatex);if(!Number.isFinite(r))return;let i=n.closest(`.prep-cover-letter`)?.querySelector(`[data-prep-cover-letter-tweaks="${r}"]`)?.value??``;Bi(r,n.value,i,0)}),h.addEventListener(`submit`,async e=>{let t=e.target.closest(`[data-prep-role-chat-form]`);if(!t||!P[0])return;e.preventDefault();let n=Number(t.dataset.prepRoleChatForm);if(!Number.isFinite(n))return;let r=t.querySelector(`[data-prep-role-chat-input="${n}"]`),i=r?.value?.trim()??``;if(!i){r?.focus();return}let a=[...At.get(n)??[],{role:`user`,content:i}];At.set(n,a),g.querySelector(`.prep-role-chat`)?.replaceWith(Q(Ci(P[0],{messages:a,loading:!0})));try{let e=await Pi(n,a),t=[...a,e.message];At.set(n,t),g.querySelector(`.prep-role-chat`)?.replaceWith(Q(Ci(P[0],{messages:t})))}catch{let e=[...a,{role:`assistant`,content:`could not answer right now.`}];At.set(n,e),g.querySelector(`.prep-role-chat`)?.replaceWith(Q(Ci(P[0],{messages:e})))}}),h.addEventListener(`click`,async e=>{let t=e.target.closest(`[data-prep-section-target]`);if(t){let e=t.dataset.prepSectionTarget,n=e?document.getElementById(e):null;if(n instanceof HTMLDetailsElement){n.open=!0,n.scrollIntoView({behavior:`smooth`,block:`start`});let e=n.querySelector(`summary`);e?.setAttribute(`tabindex`,`-1`),e?.focus({preventScroll:!0})}return}if(e.target.closest(`[data-prep-analysis]`)&&P[0]){let e=P[0].id;g.querySelector(`.prep-analysis`)?.replaceWith(Q(Z(P[0],{loading:!0})));try{let t=await Di(e,{force:!0});if(P[0]?.id!==e)return;g.querySelector(`.prep-analysis`)?.replaceWith(Q(Z(P[0],{analysis:t})))}catch{g.querySelector(`.prep-analysis`)?.replaceWith(Q(Z(P[0],{error:!0})))}return}if(e.target.closest(`[data-prep-resume-regenerate]`)&&P[0]){let e=P[0].id,t=g.querySelector(`.prep-resume`),n=t?.querySelector(`[data-prep-resume-tweaks="${e}"]`)?.value??``,r=t?.querySelector(`[data-prep-resume-latex="${e}"]`)?.value??``;if(!n.trim()){t?.querySelector(`[data-prep-resume-tweaks="${e}"]`)?.focus();return}kt.set(e,n),t?.replaceWith(Q(xi(P[0],{loading:!0})));try{let t=await Ni(e,n,r);I.set(e,t.resume),g.querySelector(`.prep-resume`)?.replaceWith(Q(xi(P[0],{resume:t.resume}))),K()}catch{g.querySelector(`.prep-resume`)?.replaceWith(Q(xi(P[0],{resume:I.get(e),tweaks:n}))),K()}return}if(e.target.closest(`[data-prep-cover-letter]`)&&P[0]){let e=P[0].id,t=g.querySelector(`.prep-cover-letter`),n=t?.querySelector(`[data-prep-cover-letter-tweaks="${e}"]`)?.value??``,r=n.trim()?t?.querySelector(`[data-prep-cover-letter-latex="${e}"]`)?.value??``:``;t?.replaceWith(Q(Ti(P[0],{loading:!0})));try{let t=await Ri(e,n,r);L.set(e,t.cover_letter),g.querySelector(`.prep-cover-letter`)?.replaceWith(Q(Ti(P[0],{coverLetter:t.cover_letter}))),K()}catch{g.querySelector(`.prep-cover-letter`)?.replaceWith(Q(Ti(P[0],{coverLetter:L.get(e),tweaks:n}))),K()}return}let n=e.target.closest(`[data-prep-action]`);if(n){Oi(n.dataset.prepAction);return}let r=e.target.closest(`[data-prep-feedback]`);if(!r||!P[0])return;let i=P[0].id,a=F.get(i),o=Array.isArray(a?.feedback_items)?a.feedback_items.length:0,s=Ot.get(i)??0;if(r.dataset.prepFeedback===`accept`||r.dataset.prepFeedback===`ignore`){let e=a?.feedback_items?.[s];if(!e)return;let t=g.querySelector(`[data-prep-feedback-comment]`)?.value??``,n=r.dataset.prepFeedback,o=n;r.disabled=!0,r.textContent=n===`accept`?`adding...`:`ignoring...`;try{if(n===`accept`){let n=await ki(i,s,e,t),r=document.querySelector(`.job[data-role-id="${CSS.escape(String(i))}"]`);n.role&&(P[0]=n.role,Ur(n.role,r)),oa(i,n.tweak_prompt??e.tweak_prompt??``),aa(i,s,a)}else await Ai(i,s,e,t),aa(i,s,a)}catch{r.disabled=!1,r.textContent=o}return}let c=r.dataset.prepFeedback===`next`?1:-1;Ot.set(i,Math.max(0,Math.min(s+c,o-1))),g.querySelector(`.prep-analysis`)?.replaceWith(Q(Z(P[0],{analysis:a})))});function aa(e,t,n){let r=n.feedback_items.filter((e,n)=>n!==t),i=Math.min(t,Math.max(r.length-1,0)),a={...n,feedback_items:r,verdict:r.length===0?`ready_to_apply`:n.verdict};Ot.set(e,i),F.set(e,a),g.querySelector(`.prep-analysis`)?.replaceWith(Q(Z(P[0],{analysis:a})))}function oa(e,t){let n=String(t||``).trim();if(!n)return;let r=kt.get(e)?.trim()??``,i=r?`${r}\n\n${n}`:n;kt.set(e,i);let a=g.querySelector(`[data-prep-resume-tweaks="${e}"]`);a&&(a.value=i,a.focus())}document.addEventListener(`keydown`,e=>{e.key===`Escape`&&!Ie.hidden&&jn(),e.key===`Escape`&&!o.hidden&&qt(),e.key===`Escape`&&!m.hidden&&ti(),e.key===`Escape`&&!h.hidden&&ri(),e.key===`Escape`&&!ke.hidden&&Ji(),e.key===`Escape`&&!We.hidden&&Rn(),e.key===`Escape`&&!nt.hidden&&Kn(),e.key===`Escape`&&!ct.hidden&&tr(),e.key===`Escape`&&!pt.hidden&&_r()}),Fe.addEventListener(`click`,An),Re.addEventListener(`click`,jn),Le.addEventListener(`click`,jn);function sa(){return Array.from(document.querySelectorAll(`.pane-toggle`))}function ca(){return sa().some(e=>e.getAttribute(`aria-expanded`)===`true`)}function la(){Be.textContent=ca()?`collapse all`:`expand all`}function ua(){document.querySelectorAll(`.pane-toggle`).forEach(e=>{e.setAttribute(`aria-expanded`,`true`),e.querySelector(`.chevron`).textContent=`v`,e.parentElement.querySelector(`.pane-body`).hidden=!1})}function da(){document.querySelectorAll(`.job[open]`).forEach(e=>{e.open=!1}),document.querySelectorAll(`.pane-toggle`).forEach(e=>{e.setAttribute(`aria-expanded`,`false`),e.querySelector(`.chevron`).textContent=`>`,e.parentElement.querySelector(`.pane-body`).hidden=!0})}Be.addEventListener(`click`,()=>{ca()?da():ua(),la()}),Ve.addEventListener(`click`,()=>{Et=!Et,Ve.textContent=Et?`show empty`:`hide empty`,O&&gn(O.statuses)}),Ue.addEventListener(`click`,Ln),Ge.addEventListener(`click`,Rn),tt.addEventListener(`click`,Gn),rt.addEventListener(`click`,Kn),st.addEventListener(`click`,er),lt.addEventListener(`click`,tr),Ne.addEventListener(`click`,gr),mt.addEventListener(`click`,_r),ht.addEventListener(`submit`,e=>{e.preventDefault(),br(ht).catch(()=>{E.textContent=`could not add company.`})}),gt.addEventListener(`submit`,e=>{e.preventDefault(),Tr(gt).catch(()=>{bt.textContent=`could not add role.`})}),D.addEventListener(`submit`,e=>{let t=e.target.closest(`[data-company-link-form]`);t&&(e.preventDefault(),xr(t).catch(()=>{E.textContent=`could not add link.`}))}),D.addEventListener(`input`,e=>{let t=e.target.closest(`[data-company-notes]`);t&&Or(t.dataset.companyNotes)}),D.addEventListener(`change`,e=>{let t=e.target.closest(`[data-company-tier]`);if(!t)return;let n=t.closest(`.company-panel`);n&&Ar(n,t.value),window.clearTimeout(Wt.get(t.dataset.companyTier)),kr(t.dataset.companyTier).catch(()=>{Dr(`could not save company.`)})}),D.addEventListener(`click`,e=>{let t=e.target.closest(`[data-delete-company]`);if(t){let e=Er(t.dataset.deleteCompany),n=e?.name?W(e.name):`this company`;if(!window.confirm(`Deactivate ${n}? It will be hidden from company counts and skipped during scans.`))return;t.disabled=!0,Cr(t.dataset.deleteCompany).catch(()=>{E.textContent=`could not deactivate company.`,t.disabled=!1});return}let n=e.target.closest(`[data-delete-career-page]`);if(!n)return;let r=n.closest(`.company-link-row`)?.querySelector(`.company-link-text`)?.textContent?.trim();window.confirm(`Delete ${r||`this career link`}?`)&&(n.disabled=!0,Sr(n.dataset.deleteCareerPage).catch(()=>{E.textContent=`could not delete link.`,n.disabled=!1}))}),Ke.addEventListener(`change`,e=>{let t=e.target.closest(`input[type="checkbox"], select, input[data-setting-text]`);t&&rr(t)}),Ke.addEventListener(`submit`,async e=>{e.preventDefault();let t=Ke.querySelector(`button[type="submit"]`),n=Ke.querySelectorAll(`input[type="checkbox"][name], select[name], input[data-setting-text][name]`),r={};n.forEach(e=>{let t=e.name;t&&(r[t]=e.type===`checkbox`?e.checked:e.value)}),t.disabled=!0,t.textContent=`saving...`;try{x.textContent=`saving settings...`;let e=await fetch(`/api/config`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(r)});if(!e.ok)throw Error(`Config update failed`);q(await e.json(),`settings saved.`)}catch{x.textContent=`could not save settings.`,x.classList.remove(`is-empty`)}finally{t.disabled=!1,t.textContent=`save settings`}}),S.addEventListener(`input`,()=>{C.disabled=!S.value.trim()}),Qe.addEventListener(`click`,ar),C.addEventListener(`click`,or),et.addEventListener(`click`,ir),ft.addEventListener(`click`,lr);function fa(){if(window.location.hash===`#prepped-roles`){qi();return}Ji({clearHash:!1})}window.addEventListener(`popstate`,fa),cr(),window.location.hash===`#prepped-roles`&&fa(),Ir({applyDefaultCollapsed:!0}).catch(()=>{rn(null,`could not load resume.`),on([],`could not load cover letter examples.`),dn()}),Mr().then(()=>{Nr()}).catch(()=>{b.textContent=`could not load scan status`});