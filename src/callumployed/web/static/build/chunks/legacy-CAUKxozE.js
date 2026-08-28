import{t as e}from"./preload-helper-Czpn1I53.js";var{sankey:t,sankeyLinkHorizontal:n}=await e(async()=>{let{sankey:e,sankeyLinkHorizontal:t}=await import(`/assets/d3-sankey.js`);return{sankey:e,sankeyLinkHorizontal:t}},[]),r=document.querySelector(`#stats`),i=document.querySelector(`#status-list`),a=document.querySelector(`#search-toggle`),o=document.querySelector(`#search-dialog`),s=document.querySelector(`#search-backdrop`),c=document.querySelector(`#search-form`),l=document.querySelector(`#search-input`),u=document.querySelector(`#close-search`),d=document.querySelector(`#materials-panel`),f=document.querySelector(`#materials-toggle`),p=document.querySelector(`#materials-body`),ee=document.querySelector(`#materials-summary`),te=document.querySelector(`#materials-required-warning`),ne=document.querySelector(`#resume-meta`),m=document.querySelector(`#resume-upload`),re=document.querySelector(`#resume-upload-button`),ie=document.querySelector(`#resume-resource-meta`),ae=document.querySelector(`#resume-resource-upload`),oe=document.querySelector(`#resume-resource-upload-button`),se=document.querySelector(`#resume-resource-list`),ce=document.querySelector(`#cover-letter-meta`),le=document.querySelector(`#cover-letter-upload`),ue=document.querySelector(`#cover-letter-upload-button`),de=document.querySelector(`#cover-letter-list`),fe=document.querySelector(`#experience-note-meta`),pe=document.querySelector(`#experience-note-upload`),me=document.querySelector(`#experience-note-upload-button`),he=document.querySelector(`#experience-note-list`);document.querySelector(`#material-index-button`);var ge=document.querySelector(`#material-index-warning`),_e=document.querySelector(`#material-index-status`),ve=document.querySelector(`#review-discovered`),ye=document.querySelector(`#prep-interested`),h=document.querySelector(`#review-view`),be=document.querySelector(`#review-heading`),xe=document.querySelector(`#review-progress`),Se=document.querySelector(`#review-card`),Ce=document.querySelector(`#close-review`),g=document.querySelector(`#prep-view`),we=document.querySelector(`#prep-heading`),Te=document.querySelector(`#prep-progress`),_=document.querySelector(`#prep-card`),Ee=document.querySelector(`#close-prep`),De=document.querySelector(`#autoprep-interested`),Oe=document.querySelector(`#prepped-roles`),ke=document.querySelector(`#autoprep-view`),Ae=document.querySelector(`#close-autoprep`),je=document.querySelector(`#autoprep-select-all`),Me=document.querySelector(`#autoprep-deselect-all`),Ne=document.querySelector(`#autoprep-selection-count`),Pe=document.querySelector(`#autoprep-status`),Fe=document.querySelector(`#autoprep-list`),Ie=document.querySelector(`#autoprep-selected`),Le=document.querySelector(`#prepped-view`),Re=document.querySelector(`#close-prepped`),ze=document.querySelector(`#prepped-summary`),Be=document.querySelector(`#prepped-list`),v=document.querySelector(`#prepped-detail`),y=document.querySelector(`#scan-all-button`),Ve=document.querySelector(`#manage-companies-button`),b=document.querySelector(`#scan-status-bar`),x=document.querySelector(`#scan-status-text`),He=document.querySelector(`#scan-last-time`),Ue=document.querySelector(`#scan-failures-open`),We=document.querySelector(`#scan-failures-dialog`),Ge=document.querySelector(`#scan-failures-backdrop`),Ke=document.querySelector(`#scan-failures-close`),qe=document.querySelector(`#scan-failures-list`),Je=document.querySelector(`#toggle-all`),Ye=document.querySelector(`#collapse-empty`),Xe=document.querySelector(`#toolbar-summary`),Ze=document.querySelector(`#settings-open`),Qe=document.querySelector(`#settings-view`),$e=document.querySelector(`#settings-close`),S=document.querySelector(`#settings-status`),et=document.querySelector(`#settings-form`),tt=document.querySelector(`#settings-profile-options`),nt=document.querySelector(`#settings-options`),rt=document.querySelector(`#central-store-summary`),it=document.querySelector(`#central-store-sync-summary`),at=document.querySelector(`#central-api-url-input`),ot=document.querySelector(`#central-passkey-input`),st=document.querySelector(`#central-save-button`),C=document.querySelector(`#central-sync-button`),ct=document.querySelector(`#recommendation-history-summary`),lt=document.querySelector(`#clear-recommendation-history`),ut=document.querySelector(`#metrics-open-button`),dt=document.querySelector(`#metrics-view`),ft=document.querySelector(`#metrics-close`),pt=document.querySelector(`#metrics-status`),mt=document.querySelector(`#metrics-overview`),ht=document.querySelector(`#metrics-sections`),gt=document.querySelector(`#metrics-scan-list`),_t=document.querySelector(`#sankey-open-button`),vt=document.querySelector(`#sankey-view`),yt=document.querySelector(`#sankey-close`),bt=document.querySelector(`#sankey-status`),xt=document.querySelector(`#sankey-canvas`),St=document.querySelector(`#sankey-path-list`),Ct=document.querySelector(`#app-update-button`),wt=document.querySelector(`#companies-view`),Tt=document.querySelector(`#companies-close`),w=document.querySelector(`#companies-status`),Et=document.querySelector(`#company-create-form`),T=document.querySelector(`#companies-list`),Dt=document.querySelector(`#role-add-form`),Ot=document.querySelector(`#role-url-input`),kt=document.querySelector(`#role-company-input`),At=document.querySelector(`#role-company-options`),jt=document.querySelector(`#role-add-status`),Mt=3,Nt=1200,Pt=new Set([`applied`,`OA`,`interview`,`rejected`,`offer`]),Ft=new Map([[`discovered`,`#4f6472`],[`interested`,`#00897b`],[`disinterested`,`#626970`],[`applied`,`#2257ad`],[`oa`,`#b36b00`],[`interview`,`#5f2bd8`],[`rejected`,`#b93d2d`],[`offer`,`#137347`],[`closed`,`#53606b`],[`archived`,`#765b4a`]]),It=/^(?:about (?:the )?(?:role|team|job)|about this role|job description|job responsibilities|minimum qualifications|preferred qualifications|qualifications|requirements|responsibilities|what to expect|what (?:you'll|you’ll|you will) (?:bring|do)|what'?s in it for you|who you are|your objectives|your skills & talents):?$/i,Lt=!0,E=null,D=null,O=[],k=[],A=[],Rt=null,j=[],M=[],N=new Map,zt=new Map,P=new Map,Bt=new Map,F=new Map,Vt=new Map,Ht=new Map,Ut=new Map,Wt=[],I=new Set,L=!1,R=[],z=null,Gt=null,Kt=new Map,qt=new Set,Jt=!1,Yt=null,Xt=!1,Zt=null,Qt=null,$t=null,en=null,B=null,tn=[],nn=new Map;function V(){return E?.query?.trim()??``}function rn(){let e=!!V();a.classList.toggle(`search-active`,e),a.setAttribute(`aria-label`,e?`clear search`:`search jobs`)}function an(){l.value=V(),o.hidden=!1,c.hidden=!1,l.focus(),l.select()}function on(){o.hidden=!0,c.hidden=!0,a.focus()}function sn(e){return e?new Intl.DateTimeFormat(void 0,{month:`short`,day:`numeric`,hour:`numeric`,minute:`2-digit`}).format(new Date(e)).toLocaleLowerCase():``}function H(e){return e?new Intl.DateTimeFormat(void 0,{month:`short`,day:`numeric`,hour:`numeric`,minute:`2-digit`}).format(new Date(e)).replace(`, `,` `).toLocaleLowerCase():``}function U(e){return String(e??``).replaceAll(`&`,`&amp;`).replaceAll(`<`,`&lt;`).replaceAll(`>`,`&gt;`).replaceAll(`"`,`&quot;`).replaceAll(`'`,`&#039;`)}function W(e){return String(e??``).toLocaleLowerCase()}function G(e){return U(W(e))}function cn(e){try{let t=new URL(String(e||``));return[`http:`,`https:`].includes(t.protocol)?t.href:``}catch{return``}}function ln(e){return e}function K(e=_){e.querySelectorAll(`[data-prep-resume-latex], [data-prep-cover-letter-latex]`).forEach(ln)}function un(){return`
    <svg class="role-link-icon" viewBox="0 0 24 24" aria-hidden="true">
      <path d="M7 17 17 7"></path>
      <path d="M8 7h9v9"></path>
    </svg>
  `}function dn(){return`
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M12 5v14"></path>
      <path d="M5 12h14"></path>
    </svg>
  `}function fn(){return`
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M3 6h18"></path>
      <path d="M8 6V4h8v2"></path>
      <path d="m19 6-1 14H6L5 6"></path>
      <path d="M10 11v5"></path>
      <path d="M14 11v5"></path>
    </svg>
  `}function pn(e,t,n){let r=`<span class="role-title-text">${G(e)}</span>`;return t?`<a class="${n}" href="${U(t)}" target="_blank" rel="noreferrer">${r}${un()}</a>`:`<span class="${n}">${r}</span>`}function mn(e){r.innerHTML=[[`companies`,e.companies_total],[`jobs`,e.jobs_total],[`applications`,e.applications_total]].map(([e,t])=>`<dl class="stat"><dt>${G(e)}</dt><dd>${t}</dd></dl>`).join(``)}function hn(e=E){if(!e){Xe.innerHTML=``;return}let t=t=>e.statuses.find(e=>e.key===t)?.count??0;Xe.innerHTML=[[`discovered`,t(`discovered`)],[`interested`,t(`interested`)],[`applied`,e.stats?.applications_total??0],[`total`,e.stats?.jobs_total??0]].map(([e,t])=>`
        <dl>
          <dt>${G(e)}</dt>
          <dd>${t}</dd>
        </dl>
      `).join(``)}function gn(e,t=``){if(D=e,re.textContent=e?`replace`:`upload`,t){ne.textContent=t;return}if(!e){ne.textContent=`no resume uploaded`;return}let n=H(e.updated_at),r=Tn(e.content_bytes);ne.textContent=[W(e.filename),r,n].filter(Boolean).join(` | `)}function _n(e,t,n,{binary:r=!1}={}){let i=r?e.filename:e.id;return`
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
    </li>`}function vn(e,t=``){k=Array.isArray(e)?e:[],ue.textContent=k.length>0?`add`:`upload`,ce.textContent=t||(k.length===0?`no examples uploaded`:`${k.length} ${k.length===1?`example`:`examples`} stored`),de.innerHTML=k.map(e=>_n(e,`cover-letter-examples`,Tn(e.content_bytes))).join(``)}function yn(e,t=``){A=Array.isArray(e)?e:[],me.textContent=A.length>0?`add`:`upload`,fe.textContent=t||(A.length===0?`no notes uploaded`:`${A.length} ${A.length===1?`note`:`notes`} stored`),he.innerHTML=A.map(e=>_n(e,`experience-notes`,Tn(e.content_bytes))).join(``)}function bn(e,t=``){Rt=e??null;let n=Rt?.status??`missing`,r=n!==`ready`;if(A.length,ge.hidden=!r,ge.textContent=t||Rt?.warning||``,t)_e.textContent=t;else if(n===`ready`){let e=Number(Rt?.document_count??0),t=Number(Rt?.skipped_source_count??0),n=H(Rt?.generated_at);_e.textContent=[`${e} indexed ${e===1?`page`:`pages`}`,t?`${t} unreadable upload skipped`:``,n].filter(Boolean).join(` | `)}else _e.textContent=n===`stale`?`index out of date`:`not indexed`}function xn(e,t=``){O=Array.isArray(e)?e:[],oe.textContent=O.length>0?`add`:`upload`,ie.textContent=t||(O.length===0?`no resources uploaded`:`${O.length} ${O.length===1?`resource`:`resources`} stored`),se.innerHTML=O.map(e=>_n(e,`resume-resources`,Tn(e.bytes),{binary:!0})).join(``)}function Sn(e,t={}){gn(e?.master_resume??null),xn(e?.resume_resources??[]),vn(e?.cover_letter_examples??[]),yn(e?.experience_notes??[]),bn(e?.material_index??null),Cn(e?.ui),(!Jt||t.applyDefaultCollapsed)&&(wn(!!e?.ui?.default_collapsed),Jt=!0)}function Cn(e=null){let t=D?`resume ready`:`no resume`,n=O.length===0?`no resources`:`${O.length} ${O.length===1?`resource`:`resources`}`,r=k.length,i=r===0?`no cover letters`:`${r} cover ${r===1?`letter`:`letters`}`,a=A.length,o=a===0?`no notes`:`${a} experience ${a===1?`note`:`notes`}`;te.hidden=!(typeof e?.has_missing_required_materials==`boolean`?e.has_missing_required_materials:!D||r===0||a===0),ee.textContent=`${t} | ${n} | ${i} | ${o}`}function wn(e){d.classList.toggle(`collapsed`,e),f.setAttribute(`aria-expanded`,String(!e)),f.querySelector(`.materials-chevron`).textContent=e?`>`:`v`,p.hidden=e}function Tn(e){return Number.isFinite(e)?e<1024?`${e} b`:`${Math.round(e/1024)} kb`:``}async function En(e){let t=e.closest(`.material-source-item`)?.querySelector(`[data-material-preview-body]`);if(!t)return;if(t.dataset.loaded===`true`){t.hidden=!t.hidden,e.textContent=t.hidden?`preview`:`hide`;return}e.disabled=!0,e.textContent=`loading...`;let n=e.dataset.materialView,r=e.dataset.materialId,i=`/api/${encodeURIComponent(n)}/${encodeURIComponent(r)}`;try{if(e.dataset.materialBinary===`true`)t.innerHTML=`<iframe title="${G(r)} preview" src="${U(i)}"></iframe>`;else{let e=await fetch(i);if(!e.ok)throw Error(`Preview unavailable`);let n=await e.json(),r=document.createElement(`pre`);r.textContent=n.content||`This source is empty.`,t.replaceChildren(r)}t.dataset.loaded=`true`,t.hidden=!1,e.textContent=`hide`}catch(n){t.textContent=n instanceof Error?n.message:`Preview unavailable`,t.hidden=!1,e.textContent=`preview`}finally{e.disabled=!1}}async function Dn(e){let t=e.dataset.materialRemove,n=e.dataset.materialId,r=e.dataset.materialName||`this source`;if(window.confirm(`Remove ${r}? This removes it from future application preparation.`)){e.disabled=!0,e.textContent=`removing...`;try{let e=await fetch(`/api/${encodeURIComponent(t)}/${encodeURIComponent(n)}`,{method:`DELETE`}),r=await e.json();if(!e.ok)throw Error(r.error||`Remove failed`);Sn(r)}catch(t){e.disabled=!1,e.textContent=`remove`,window.alert(t instanceof Error?t.message:`Remove failed`)}}}function On(e){i.innerHTML=e.map(e=>{let t=e.jobs.map(t=>kn(t,e.key)).join(``);return`
        <section class="status-pane ${e.count===0?`empty`:``} ${Lt?`hidden-empty`:``}" id="status-${U(e.key)}" data-bucket="${U(e.key)}">
          <button class="pane-toggle" type="button" aria-expanded="false">
            <span class="chevron">></span>
            <span class="pane-title">${G(e.label)}</span>
            <span class="count">${e.count}</span>
          </button>
          <div class="pane-body" hidden>
            ${t?`<div class="jobs">${t}</div>`:`<p class="empty-copy">no jobs in this status.</p>`}
          </div>
        </section>
      `}).join(``)}function kn(e,t){return`
    <details class="job" data-role-id="${U(e.id)}">
      <summary class="job-summary">
        <span class="job-chevron">></span>
        <span class="job-identity">
          <span class="job-company">[${G(e.company_name)}]</span>
          ${pn(e.title,e.role_url,`job-title`)}
          ${t===`interested`&&e.prep_started?Mn():``}
          ${t===`closed`&&e.updated_in_latest_scan?An():``}
          ${[`discovered`,`interested`].includes(t)&&e.missing_from_latest_scan?jn():``}
        </span>
      </summary>
      <div class="job-detail">
        ${t===`discovered`?Nn(e):``}
        ${t===`interested`?Pn(e):``}
        ${t===`disinterested`?Fn(e):``}
        ${t===`applied`?In(e):``}
        ${t===`OA`?Ln(e):``}
        ${t===`interview`?Rn(e):``}
        ${t===`closed`?zn(e):``}
        <dl>
          ${e.location?`<div>
                  <dt>location</dt>
                  <dd>${G(e.location)}</dd>
                </div>`:``}
          <div>
            <dt>updated</dt>
            <dd>${sn(e.updated_at)}</dd>
          </div>
        </dl>
      </div>
    </details>
  `}function An(){return`<span class="latest-scan-dot" title="updated in latest scan" aria-label="updated in latest scan"></span>`}function jn(){return`<span class="missing-latest-scan-dot" title="not seen in latest scan" aria-label="not seen in latest scan"></span>`}function Mn(){return`<span class="prep-started-dot" title="application materials started" aria-label="application materials started"></span>`}function Nn(e){return`
    <div class="job-actions job-actions-nowrap" aria-label="discovered role actions">
      <button class="job-action success" type="button" data-review-role-id="${e.id}">view</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="interested">interested</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="disinterested">disinterested</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="closed">closed</button>
    </div>
  `}function Pn(e){return`
    <div class="job-actions" aria-label="interested role actions">
      <button class="job-action success" type="button" data-prep-role-id="${e.id}">prep</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="applied">applied</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="disinterested">disinterested</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="closed">closed</button>
    </div>
  `}function Fn(e){return`
    <div class="job-actions" aria-label="disinterested role actions">
      <button class="job-action success" type="button" data-role-id="${e.id}" data-status="interested">interested</button>
    </div>
  `}function In(e){return`
    <div class="job-actions job-actions-nowrap" aria-label="applied role actions">
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="OA">oa</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="interview">interview</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="rejected">rejected</button>
    </div>
  `}function Ln(e){return`
    <div class="job-actions job-actions-nowrap" aria-label="oa role actions">
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="interview">interview</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="disinterested">disinterested</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="rejected">rejected</button>
    </div>
  `}function Rn(e){return`
    <div class="job-actions" aria-label="interview role actions">
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="rejected">rejected</button>
      <button class="job-action success" type="button" data-role-id="${e.id}" data-status="offer">offer</button>
    </div>
  `}function zn(e){return`
    <div class="job-actions" aria-label="closed role actions">
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="interested">interested</button>
    </div>
  `}function Bn(e){E=e,l.value=e.query,rn(),mn(e.stats),hn(e),On(e.statuses),Ea(),ci(e.statuses),ui(e.statuses)}function Vn(e){Zt=e??null;let t=!!e?.scanning,n=t&&!!e?.cancel_requested,r=Number(e?.completed_companies??0),i=Number(e?.total_companies??0),a=Number(e?.failed_companies??0),o=typeof e?.error==`string`?e.error.trim():``,s=Array.isArray(e?.failures)?e.failures:[];y.disabled=n,y.textContent=t?n?`cancelling...`:`cancel scan`:`scan roles`,y.classList.toggle(`danger`,t&&!n),b.hidden=!t&&!o&&s.length===0,b.classList.toggle(`scanning`,t),b.classList.toggle(`scan-error`,!t&&!!o||s.length>0),x.textContent=n?`cancelling scan...`:t?`scanning roles${i>0?` ${r}/${i}`:``}${a>0?`, ${a} failed`:``}`:s.length>0?`${s.length} recent scan ${s.length===1?`failure`:`failures`}`:o?`last scan error: ${o}`:`scan idle`,Ue&&qe&&(Ue.hidden=s.length===0,qe.innerHTML=s.slice(0,5).map(e=>{let t=e?.company_name||`unknown company`,n=e?.error||`scan failed`;return`
          <p>
            <span>${G(t)}</span>
            <span>${U(n)}</span>
          </p>
        `}).join(``),s.length===0&&Un());let c=e?.last_scan_at;He.textContent=c?`last scan: ${H(c)}`:`last scan: never`,Xt&&!t&&Y(V()).catch(()=>{}),Xt=t}function Hn(){Ue.hidden||(We.hidden=!1,Ke.focus())}function Un(){We.hidden=!0}function q(e,t=``){Qt=e;let n=Array.isArray(e?.settings)?e.settings:[],r=n.filter(e=>e.key?.startsWith(`applicant_`)),i=n.filter(e=>!e.key?.startsWith(`applicant_`)),a=e?.central??{};S.textContent=t,S.classList.toggle(`is-empty`,!t);let o=Number(e?.recommendation_history_count??0);ct.textContent=o>0?`${o} saved ${o===1?`feedback decision`:`feedback decisions`}`:`no saved resume feedback decisions`,lt.disabled=o===0,Wn(a),tt.innerHTML=r.map(e=>Gn(e)).join(``),nt.innerHTML=i.map(e=>Gn(e)).join(``),J(!1)}function Wn(e){let t=e?.api_url??``;at.value=t,ot.value=``;let n=e?.passkey_configured?`passkey saved`:`no passkey saved`;rt.textContent=t?`${W(t)} | ${n}`:`no api url | ${n}`,it.textContent=`${Number(e?.companies_linked??0)} linked | ${Number(e?.companies_unlinked??0)} unlinked | ${Number(e?.companies_needs_review??0)} review | ${Number(e?.companies_failed??0)} failed`,C.disabled=!t}function Gn(e){if(e.control===`text`&&e.editable!==!1)return Kn(e);if(e.control===`select`&&e.editable!==!1)return qn(e);if(e.control!==`toggle`||e.editable===!1)return Jn(e);let t=e.value?`checked`:``,n=e.default?`on by default`:`off by default`;return`
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
  `}function Kn(e){let t=e.default?`default: ${W(e.default)}`:`optional`,n=e.input_type??`text`,r=e.autocomplete??`name`;return`
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
  `}function qn(e){let t=Array.isArray(e.options)?e.options:[],n=`default: ${W(e.default)}`;return`
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
  `}function Jn(e){let t=e.default?`on by default`:`off by default`,n=e.value?`automatic`:`off`;return`
    <div class="setting-option setting-option-readonly">
      <span class="setting-copy">
        <span class="setting-label">${G(e.label)}</span>
        <span class="setting-description">${G(e.description)}</span>
        <span class="setting-default">${G(t)}</span>
      </span>
      <span class="setting-badge">${G(n)}</span>
    </div>
  `}function J(e){et.querySelectorAll(`input, select`).forEach(t=>{t.disabled=e}),st.disabled=e,C.disabled=e||!at.value.trim(),Ct.disabled=e}async function Yn(){Qe.hidden=!1,document.body.classList.add(`settings-open`),$e.focus(),Qt?q(Qt):(S.textContent=`loading settings...`,S.classList.remove(`is-empty`),nt.innerHTML=``);try{await Zn()}catch{S.textContent=`could not load settings.`}}function Xn(){Qe.hidden=!0,document.body.classList.remove(`settings-open`),Ze.focus()}async function Zn(){let e=await fetch(`/api/config`);if(!e.ok)throw Error(`Config request failed`);q(await e.json())}function Qn(e){let t=e?.value;return t==null?`n/a`:e?.kind===`ratio`?Number(t).toLocaleString(void 0,{maximumFractionDigits:2,minimumFractionDigits:0}):typeof t==`number`?t.toLocaleString():W(t)}function $n(e,t=`metric-card`){return`
    <article class="${t}">
      <span>${G(e?.label)}</span>
      <strong>${U(Qn(e))}</strong>
    </article>
  `}function er(e,t=``){$t=e,pt.textContent=t||(e?.updated_at?`updated ${H(e.updated_at)}`:``),pt.classList.toggle(`is-empty`,!pt.textContent);let n=Array.isArray(e?.overview)?e.overview:[],r=Array.isArray(e?.sections)?e.sections:[],i=Array.isArray(e?.recent_scans)?e.recent_scans:[];mt.innerHTML=n.map(e=>$n(e)).join(``),ht.innerHTML=r.map(tr).join(``),gt.innerHTML=i.length?i.map(nr).join(``):`<p class="empty-copy">no scan runs recorded.</p>`}function tr(e){let t=Array.isArray(e?.metrics)?e.metrics:[];return`
    <section class="metrics-section">
      <div class="metrics-section-heading">
        <h3>${G(e?.title)}</h3>
      </div>
      <div class="metrics-section-grid">
        ${t.map(e=>$n(e,`metric-card metric-card-compact`)).join(``)}
      </div>
    </section>
  `}function nr(e){let t=e?.scan_status??`unknown`,n=e?.started_at?H(e.started_at):`not started`,r=e?.finished_at?H(e.finished_at):`not finished`,i=e?.error?`<span>${G(e.error)}</span>`:``;return`
    <article class="metrics-scan-row">
      <div>
        <strong>${G(e?.company_name??`unknown company`)}</strong>
        <span>${G(n)} -> ${G(r)}</span>
        ${i}
      </div>
      <span class="metrics-status-pill">${G(t)}</span>
    </article>
  `}async function rr(){dt.hidden=!1,document.body.classList.add(`metrics-open`),ft.focus(),$t?er($t):(pt.textContent=`loading metrics...`,pt.classList.remove(`is-empty`),mt.innerHTML=``,ht.innerHTML=``,gt.innerHTML=``);try{await ar()}catch{pt.textContent=`could not load metrics.`}}function ir(){dt.hidden=!0,document.body.classList.remove(`metrics-open`),ut.focus()}async function ar(){let e=await fetch(`/api/metrics`);if(!e.ok)throw Error(`Metrics request failed`);er(await e.json())}function or(e,t=``){en=e;let n=Number(e?.role_count??0),r=Array.isArray(e?.links)?e.links:[],i=Array.isArray(e?.paths)?e.paths:[];bt.textContent=t||(e?.updated_at?`${n.toLocaleString()} roles | updated ${H(e.updated_at)}`:``),bt.classList.toggle(`is-empty`,!bt.textContent),xt.innerHTML=r.length?sr(e):`<p class="empty-copy">no role transitions recorded yet.</p>`,St.innerHTML=i.length?i.map(dr).join(``):`<p class="empty-copy">no role paths recorded yet.</p>`}function sr(e){let t=Array.isArray(e?.nodes)?e.nodes:[],n=Array.isArray(e?.links)?e.links:[],r=ur(t,n),i=r.nodes,a=r.links,o=(r.flowLinks??n).map(e=>{let t=i.get(e.source),n=i.get(e.target),r=a.get(e);if(!t||!n||!r)return``;let o=r.width,s=n.x<t.x,c=cr(e.target),l=r.priority?`0.42`:s?`0.28`:`0.34`,u=r.path??lr({isBacktrack:s,sourceX:t.x+t.width,sourceY:r.sourceY,targetX:n.x,targetY:r.targetY,width:o});return`
        <path class="${[`sankey-link`,s?`sankey-link-backtrack`:``,r.priority?`sankey-link-priority`:``].filter(Boolean).join(` `)}" d="${u}" fill="${r.path?`none`:c}" fill-opacity="${l}" stroke="${c}" style="stroke-width: ${r.path?o:1}px">
          <title>${G(t.label)} to ${G(n.label)}: ${Number(e.value??0).toLocaleString()}</title>
        </path>
      `}).join(``),s=Array.from(i.values()).map(e=>{let t=Number(e.history_count??e.current_count??0),n=Number(e.value??t),i=n>0?n.toLocaleString():`0`,a=e.x>r.width-180,o=a?e.x-8:e.x+e.width+8,s=Math.max(24,e.y-e.height/2-16),c=a?`end`:`start`,l=cr(e.id);return`
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
  `}function cr(e){return Ft.get(String(e).toLowerCase())??`#4f6472`}function lr({isBacktrack:e,sourceX:t,sourceY:n,targetX:r,targetY:i,width:a}){let o=a/2,s=n-o,c=n+o,l=i-o,u=i+o;if(e){let e=Math.max(80,Math.abs(t-r)*.42);return[`M ${t} ${s}`,`C ${t-e} ${s}, ${r+e} ${l}, ${r} ${l}`,`L ${r} ${u}`,`C ${r+e} ${u}, ${t-e} ${c}, ${t} ${c}`,`Z`].join(` `)}let d=Math.max(46,(r-t)*.48);return[`M ${t} ${s}`,`C ${t+d} ${s}, ${r-d} ${l}, ${r} ${l}`,`L ${r} ${u}`,`C ${r-d} ${u}, ${t+d} ${c}, ${t} ${c}`,`Z`].join(` `)}function ur(e,r){let i=new Map([[`discovered`,0],[`interested`,1],[`disinterested`,2],[`applied`,2],[`oa`,3],[`interview`,3],[`rejected`,4],[`closed`,4],[`archived`,4]]),a=new Map,o=new Map;r.forEach(e=>{a.set(e.target,(a.get(e.target)??0)+Number(e.value??0)),o.set(e.source,(o.get(e.source)??0)+Number(e.value??0))});let s=e.filter(e=>Number(e?.history_count??e?.current_count??0)>0||a.has(e.id)||o.has(e.id)),c=new Set(s.map(e=>e.id)),l=r.filter(e=>c.has(e.source)&&c.has(e.target)&&Number(e.value??0)>0),u=e=>i.get(String(e).toLowerCase())??0,d=l.filter(e=>u(e.target)>=u(e.source)),f=l.filter(e=>u(e.target)<u(e.source)),p={nodes:s.map(e=>({...e,fixedValue:Math.max(0,Number(e?.history_count??e?.current_count??0))})),links:d.map(e=>({...e}))},ee=t().nodeId(e=>e.id).nodeWidth(26).nodePadding(44).nodeAlign((e,t)=>Math.min(t-1,u(e.id))).extent([[92,88],[1014,634]]).iterations(32)(p),te=new Map;ee.nodes.forEach(e=>{te.set(e.id,{...e,x:e.x0,y:e.y0+(e.y1-e.y0)/2,width:e.x1-e.x0,height:Math.max(1.5,e.y1-e.y0),value:Number(e.fixedValue??e.value??0)})});let ne=new Map,m=[],re=n();ee.links.forEach(e=>{let t={source:e.source.id,target:e.target.id,value:e.value};m.push(t),ne.set(t,{path:re(e),width:Math.max(1.5,e.width),sourceY:e.y0,targetY:e.y1,priority:Number(e.value??0)>=20})});let ie=Math.max(.6,...ee.links.map(e=>Number(e.width??0)/Math.max(1,Number(e.value??0))));return f.forEach(e=>{let t=te.get(e.source),n=te.get(e.target);if(!t||!n)return;let r=Math.max(1.5,Number(e.value??0)*ie),i={...e};m.push(i),ne.set(i,{width:r,sourceY:t.y+t.height/2-r/2,targetY:n.y+n.height/2-r/2,priority:!1})}),m.sort((e,t)=>Number(e.value??0)-Number(t.value??0)),{flowLinks:m,height:720,links:ne,nodes:te,width:1120}}function dr(e){let t=Array.isArray(e?.path)?e.path:[];return`
    <article class="sankey-path-row">
      <div>
        <strong>${G(e?.company_name??`unknown company`)} / ${G(e?.title??`untitled role`)}</strong>
        <span>${t.map(e=>G(e)).join(` -> `)}</span>
      </div>
      <span class="metrics-status-pill">${Number(e?.loops_collapsed??0).toLocaleString()} loops</span>
    </article>
  `}async function fr(){Qe.hidden=!0,document.body.classList.remove(`settings-open`),vt.hidden=!1,document.body.classList.add(`sankey-open`),yt.focus(),en?or(en):(bt.textContent=`loading role flow...`,bt.classList.remove(`is-empty`),xt.innerHTML=``,St.innerHTML=``);try{await mr()}catch{bt.textContent=`could not load role flow.`}}function pr(){vt.hidden=!0,document.body.classList.remove(`sankey-open`),Ze.focus()}async function mr(){let e=await fetch(`/api/role-sankey`);if(!e.ok)throw Error(`Role sankey request failed`);or(await e.json())}async function hr(e){let t=e.name;if(!t)return;let n=e.type===`checkbox`?!e.checked:Qt?.settings?.find(e=>e.key===t)?.value,r=e.type===`checkbox`?e.checked:e.value;J(!0),S.textContent=`saving settings...`,S.classList.remove(`is-empty`);try{let e=await fetch(`/api/config`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({[t]:r})});if(!e.ok)throw Error(`Config update failed`);q(await e.json(),`settings saved.`)}catch{e.type===`checkbox`?e.checked=n:n!==void 0&&(e.value=n),S.textContent=`could not save settings.`,J(!1)}}async function gr(){lt.disabled=!0,S.textContent=`clearing recommendation history...`,S.classList.remove(`is-empty`);try{let e=await fetch(`/api/recommendation-history/clear`,{method:`POST`});if(!e.ok)throw Error(`Recommendation history clear failed`);let t=await e.json();q(t.config,`cleared ${t.deleted_count} saved decisions.`)}catch{S.textContent=`could not clear recommendation history.`,lt.disabled=!1}}async function _r(){let e=at.value.trim();if(!e){S.textContent=`central api url is required.`,S.classList.remove(`is-empty`);return}let t={central_api_url:e},n=ot.value.trim();n&&(t.central_passkey=n),J(!0),S.textContent=`saving central settings...`,S.classList.remove(`is-empty`);try{let e=await fetch(`/api/config`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(t)});if(!e.ok)throw Error(`Central settings update failed`);q(await e.json(),`central settings saved.`)}catch{S.textContent=`could not save central settings.`,J(!1)}}async function vr(){C.disabled=!0,S.textContent=`syncing remote company ids...`,S.classList.remove(`is-empty`);try{let e=await fetch(`/api/central/resolve-companies`,{method:`POST`});if(!e.ok)throw Error(`Central company sync failed`);let t=await e.json(),n=t.result??{},r=t.pulled_companies,i=r?` remote: ${Number(r.created??0)} created, ${Number(r.linked??0)} linked, ${Number(r.existing??0)} existing.`:``;q(t.config,`company sync: ${Number(n.linked??0)} matched, ${Number(n.created??0)} created, ${Number(n.needs_review??0)} review, ${Number(n.failed??0)} failed.${i}`),t.companies&&(B=t.companies,Cr(t.companies.companies))}catch{S.textContent=`could not sync companies.`,C.disabled=!at.value.trim()}}async function yr(){let e=await fetch(`/api/central/resolve-companies`,{method:`POST`});if(!e.ok)throw Error(`Central company sync failed`);let t=await e.json();t.companies&&(B=t.companies,Cr(t.companies.companies))}async function br(){let e=yr().catch(()=>{});await Promise.all([Y().catch(()=>{i.innerHTML=`<p class="empty-copy">could not load jobs.</p>`}),jr().catch(()=>{jt.textContent=`could not load companies.`})]),await e}async function xr(){if(window.confirm(`Update callumployed and restart the tracker?`)){J(!0),Ct.disabled=!0,S.textContent=`updating callumployed; tracker will restart shortly...`,S.classList.remove(`is-empty`);try{if(!(await fetch(`/api/app/update`,{method:`POST`})).ok)throw Error(`App update failed`);S.textContent=`update started. reconnect in a moment.`}catch{S.textContent=`could not start update.`,J(!1)}}}function Sr(e,t=``){B=e;let n=Array.isArray(e?.companies)?e.companies:[];if(Cr(n),w.textContent=t||`${n.length} ${n.length===1?`company`:`companies`} stored`,w.classList.toggle(`is-empty`,n.length===0&&!t),n.length===0){T.innerHTML=`<p class="empty-copy">no companies yet.</p>`;return}T.innerHTML=n.map(e=>wr(e)).join(``)}function Cr(e){tn=Array.isArray(e)?e:[],At.innerHTML=tn.map(e=>`<option value="${U(e.name)}"></option>`).join(``)}function wr(e){let t=Array.isArray(e.career_pages)?e.career_pages:[],n=H(e.updated_at),r=Tr(e.prestige_tier),i=Number(e.scan_count??0),a=Number(e.discovered_role_count??0),o=i>0&&a===0?`<span class="company-discovery-status">Discovered 0 potential roles</span>`:``;return`
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
              ${Er(e.prestige_tier)}
            </select>
          </label>
          <div>
            <span>browser wait</span>
            <strong>${Number(e.browser_extra_wait_ms??0)}ms</strong>
          </div>
        </div>
        <div class="company-links">
          ${t.length>0?t.map(e=>Dr(e)).join(``):`<p class="company-empty-links">no career links yet.</p>`}
        </div>
        <section class="company-link-panel" aria-label="add career link">
          <form class="company-link-form" data-company-link-form="${e.id}">
            <input name="label" type="text" placeholder="label" aria-label="career link label" />
            <input name="url" type="url" placeholder="https://..." aria-label="career link url" required />
            <button class="company-link-add" type="submit" aria-label="add career link" title="add career link">
              ${dn()}
            </button>
          </form>
        </section>
        <div class="company-danger-row">
          <button class="company-delete-button" type="button" data-delete-company="${e.id}">
            ${fn()}
            <span>deactivate company</span>
          </button>
        </div>
      </div>
    </details>
  `}function Tr(e){let t=String(e??``);return[`0`,`1`,`2`,`3`,`4`].includes(t)?`company-tier-${t}`:`company-tier-unset`}function Er(e){let t=String(e??``);return[``,`0`,`1`,`2`,`3`,`4`].map(e=>{let n=e?`tier ${e}`:`not set`,r=e===t?` selected`:``;return`<option value="${U(e)}"${r}>${G(n)}</option>`}).join(``)}function Dr(e){let t=e.label?G(e.label):`career page`,n=U(e.url);return`
    <div class="company-link-row" data-career-page-id="${e.id}">
      <a class="company-link-url" href="${n}" target="_blank" rel="noreferrer">
        <span class="company-link-label">${t}</span>
        <span class="company-link-text">${U(e.url)}</span>
      </a>
      <button class="company-link-delete" type="button" data-delete-career-page="${e.id}" aria-label="delete ${t} link" title="delete link">
        ${fn()}
      </button>
    </div>
  `}async function Or(){wt.hidden=!1,document.body.classList.add(`companies-open`),Tt.focus(),B?Sr(B):(w.textContent=`loading companies...`,w.classList.remove(`is-empty`),T.innerHTML=``);try{await Ar()}catch{w.textContent=`could not load companies.`}}function kr(){wt.hidden=!0,document.body.classList.remove(`companies-open`),Ve.focus()}async function Ar(e=``){let t=await fetch(`/api/companies`);if(!t.ok)throw Error(`Companies request failed`);Sr(await t.json(),e)}async function jr(){let e=await fetch(`/api/companies`);if(!e.ok)throw Error(`Companies request failed`);Cr((await e.json()).companies)}async function Mr(e){let t=new FormData(e),n={name:String(t.get(`name`)??``),career_url:String(t.get(`career_url`)??``),notes:String(t.get(`notes`)??``)};w.textContent=`adding company...`;let r=await fetch(`/api/companies`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(n)});if(!r.ok)throw Error(`Company create failed`);e.reset(),Sr(await r.json(),`company added.`),Y(V()).catch(()=>{})}async function Nr(e){let t=e.dataset.companyLinkForm;if(!t)return;let n=new FormData(e),r={label:String(n.get(`label`)??``),url:String(n.get(`url`)??``)};w.textContent=`adding link...`;let i=await fetch(`/api/companies/${encodeURIComponent(t)}/career-pages`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(r)});if(!i.ok)throw Error(`Career page create failed`);e.reset(),Sr(await i.json(),`link added.`)}async function Pr(e){w.textContent=`deleting link...`;let t=await fetch(`/api/company-career-pages/${encodeURIComponent(e)}`,{method:`DELETE`});if(!t.ok)throw Error(`Career page delete failed`);Sr(await t.json(),`link deleted.`)}async function Fr(e){w.textContent=`deactivating company...`;let t=await fetch(`/api/companies/${encodeURIComponent(e)}`,{method:`DELETE`});if(!t.ok)throw Error(`Company deactivate failed`);Sr(await t.json(),`company deactivated.`),Y(V()).catch(()=>{})}function Ir(){let e=kt.value.trim().toLocaleLowerCase();return tn.find(t=>t.name.toLocaleLowerCase()===e)}async function Lr(e){let t=Ir();if(!t?.id){jt.textContent=`pick a saved company.`;return}let n=new FormData(e),r={company_id:t.id,role_url:String(n.get(`role_url`)??``)};jt.textContent=`adding role...`;let i=await fetch(`/api/roles`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(r)});if(!i.ok)throw Error(`Role create failed`);let a=await i.json();a.tracker?Bn(a.tracker):await Y(V()),Ot.value=``;let o=a.role?.title?W(a.role.title):`role`;jt.textContent=a.scan_error?`${o} added; scan could not finish.`:`${o} added.`}function Rr(e){return(Array.isArray(B?.companies)?B.companies:[]).find(t=>String(t.id)===String(e))}function zr(e){w.textContent=e,w.classList.remove(`is-empty`)}function Br(e){window.clearTimeout(nn.get(e)),nn.set(e,window.setTimeout(()=>{Vr(e).catch(()=>{zr(`could not save company.`)})},700))}async function Vr(e){let t=T.querySelector(`[data-company-id="${CSS.escape(String(e))}"]`);if(!t)return;let n=t.querySelector(`[data-company-notes="${CSS.escape(String(e))}"]`),r=t.querySelector(`[data-company-tier="${CSS.escape(String(e))}"]`),i=Rr(e),a={notes:n?.value??i?.notes??``,prestige_tier:r?.value??i?.prestige_tier??``};i&&(i.notes=a.notes,i.prestige_tier=a.prestige_tier),Hr(t,a.prestige_tier),zr(`saving company...`);let o=await fetch(`/api/companies/${encodeURIComponent(e)}`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(a)});if(!o.ok)throw Error(`Company update failed`);B=await o.json(),zr(`company saved.`),Ur(e)}function Hr(e,t){e.classList.remove(`company-tier-unset`,`company-tier-0`,`company-tier-1`,`company-tier-2`,`company-tier-3`,`company-tier-4`),e.classList.add(Tr(t))}function Ur(e){let t=T.querySelector(`[data-company-id="${CSS.escape(String(e))}"]`),n=Rr(e);if(!t||!n)return;let r=Array.isArray(n.career_pages)?n.career_pages:[],i=H(n.updated_at),a=t.querySelector(`.company-summary-meta`);a&&(a.textContent=`${r.length} ${r.length===1?`link`:`links`}${i?` | updated ${i}`:``}`)}async function Wr(){let e=await fetch(`/api/scan/status`);if(e.status===404){y.disabled=!0,b.hidden=!0,b.classList.add(`scan-error`),x.textContent=`restart server to enable scanning`;return}if(!e.ok)throw Error(`Scan status request failed`);Vn(await e.json())}function Gr(){Yt===null&&(Yt=window.setInterval(()=>{Wr().catch(()=>{})},3e3))}async function Kr(){y.disabled=!0,y.textContent=`starting...`;try{let e=await fetch(`/api/scan/all`,{method:`POST`});if(e.status===404){y.disabled=!0,y.textContent=`scan roles`,b.hidden=!0,b.classList.add(`scan-error`),x.textContent=`restart server to enable scanning`;return}if(!e.ok&&e.status!==409)throw Error(`Scan start failed`);Vn(await e.json()),Gr()}catch{y.disabled=!1,y.textContent=`scan roles`,b.hidden=!0,b.classList.add(`scan-error`),x.textContent=`could not start scan`}}async function qr(){y.disabled=!0,y.textContent=`cancelling...`;try{let e=await fetch(`/api/scan/cancel`,{method:`POST`});if(e.status===404){y.disabled=!0,y.textContent=`scan roles`,b.hidden=!0,b.classList.add(`scan-error`),x.textContent=`restart server to enable scanning`;return}if(!e.ok&&e.status!==409)throw Error(`Scan cancel failed`);Vn(await e.json()),Gr()}catch{y.disabled=!1,y.textContent=`cancel scan`,b.hidden=!1,b.classList.add(`scan-error`),x.textContent=`could not cancel scan`}}async function Y(e=``){i.innerHTML=`<p class="empty-copy">loading jobs...</p>`;let t=new URLSearchParams;e&&t.set(`q`,e);let n=await fetch(`/api/tracker?${t.toString()}`);if(!n.ok)throw Error(`Tracker request failed`);Bn(await n.json())}async function Jr(e={}){let t=await fetch(`/api/application-materials`);if(!t.ok)throw Error(`Application materials request failed`);Sn(await t.json(),e)}async function Yr(e){if(e){if(!e.name.toLowerCase().endsWith(`.tex`)){gn(D,`resume must be a .tex file.`);return}re.disabled=!0,gn(D,`uploading...`);try{let t=await e.text();if(!(await fetch(`/api/master-resume`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({filename:e.name,content:t})})).ok)throw Error(`Master resume upload failed`);await Jr()}catch{gn(D,`could not save resume.`),Cn()}finally{m.value=``,re.disabled=!1}}}async function Xr(e){let t=Array.from(e??[]);if(t.length!==0){oe.disabled=!0,xn(O,`uploading ${t.length} ${t.length===1?`resource`:`resources`}...`);try{for(let e of t)if(!(await fetch(`/api/resume-resources`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({filename:e.name,content_base64:await $r(e)})})).ok)throw Error(`Resume resource upload failed`);await Jr()}catch{xn(O,`could not save every resource.`),Cn()}finally{ae.value=``,oe.disabled=!1}}}async function Zr(e){let t=Array.from(e??[]);if(t.length!==0){ue.disabled=!0,vn(k,`uploading ${t.length} ${t.length===1?`example`:`examples`}...`);try{for(let e of t){let t={filename:e.name};if([`.pdf`,`.docx`].some(t=>e.name.toLowerCase().endsWith(t))?t.content_base64=await $r(e):t.content=await e.text(),!(await fetch(`/api/cover-letter-examples`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(t)})).ok)throw Error(`Cover letter example upload failed`)}await Jr()}catch{vn(k,`could not save every example.`),Cn()}finally{le.value=``,ue.disabled=!1}}}async function Qr(e){let t=Array.from(e??[]);if(t.length!==0){me.disabled=!0,yn(A,`uploading ${t.length} ${t.length===1?`note`:`notes`}...`);try{for(let e of t){let t=e.name.toLowerCase(),n={filename:e.name};if(t.endsWith(`.pdf`)||t.endsWith(`.docx`)?n.content_base64=await $r(e):n.content=await e.text(),!(await fetch(`/api/experience-notes`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(n)})).ok)throw Error(`Experience note upload failed`)}N.clear(),await Jr()}catch{yn(A,`could not save every note.`),Cn()}finally{pe.value=``,me.disabled=!1}}}function $r(e){return new Promise((t,n)=>{let r=new FileReader;r.addEventListener(`load`,()=>{let e=String(r.result??``);t(e.includes(`,`)?e.split(`,`,2)[1]:e)}),r.addEventListener(`error`,()=>n(r.error)),r.readAsDataURL(e)})}c.addEventListener(`submit`,e=>{e.preventDefault(),Y(l.value.trim()),on()}),a.addEventListener(`click`,()=>{if(V()){Y();return}an()}),l.addEventListener(`keydown`,e=>{e.key===`Escape`&&(e.stopPropagation(),on())}),u.addEventListener(`click`,on),s.addEventListener(`click`,on),re.addEventListener(`click`,()=>{m.click()}),m.addEventListener(`change`,()=>{Yr(m.files?.[0])}),oe.addEventListener(`click`,()=>{ae.click()}),ae.addEventListener(`change`,()=>{Xr(ae.files)}),ue.addEventListener(`click`,()=>{le.click()}),le.addEventListener(`change`,()=>{Zr(le.files)}),me.addEventListener(`click`,()=>{pe.click()}),pe.addEventListener(`change`,()=>{Qr(pe.files)}),f.addEventListener(`click`,()=>{wn(f.getAttribute(`aria-expanded`)===`true`)}),p.addEventListener(`click`,e=>{let t=e.target.closest(`[data-material-view]`);if(t){En(t);return}let n=e.target.closest(`[data-material-remove]`);n&&Dn(n)}),y.addEventListener(`click`,()=>{if(Zt?.scanning){qr();return}Kr()}),i.addEventListener(`click`,e=>{let t=e.target.closest(`[data-review-role-id]`);if(t){fi(t.dataset.reviewRoleId);return}let n=e.target.closest(`[data-prep-role-id]`);if(n){mi(n.dataset.prepRoleId);return}let r=e.target.closest(`.job-action`);if(r){ei(r);return}let i=e.target.closest(`.pane-toggle`);if(!i)return;let a=i.parentElement.querySelector(`.pane-body`),o=i.getAttribute(`aria-expanded`)===`true`;i.setAttribute(`aria-expanded`,String(!o)),i.querySelector(`.chevron`).textContent=o?`>`:`v`,a.hidden=o,Ea()});async function ei(e){let{roleId:t,status:n}=e.dataset;if(!t||!n)return;let r=e.closest(`.job-actions`),i=e.closest(`.job`);r.querySelectorAll(`button`).forEach(e=>{e.disabled=!0}),e.textContent=`updating...`;try{let e=await fetch(`/api/roles/${encodeURIComponent(t)}/status`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({status:n})});if(!e.ok)throw Error(`Status update failed`);ti((await e.json()).role,i)}catch{r.querySelectorAll(`button`).forEach(e=>{e.disabled=!1}),e.textContent=n===`disinterested`?`disinterested`:n.toLowerCase()}}function ti(e,t){if(!e||!E)return;let n=t?.closest(`.status-pane`)?.dataset.bucket??e.role_status,r=e.role_status,i=ri(e,n,r);ii(n,r),ai(n,r),hn(),ci(E.statuses),ui(E.statuses),oi(t,i,n,r),Ea()}function ni(e){if(!e||!E)return null;let t=null;return E.statuses.forEach(n=>{let r=n.jobs.findIndex(t=>String(t.id)===String(e.id));r!==-1&&(t={...n.jobs[r],...e},n.jobs[r]=t)}),ci(E.statuses),ui(E.statuses),t}function ri(e,t,n){let r=e;E.statuses.forEach(t=>{let n=t.jobs.findIndex(t=>String(t.id)===String(e.id));n!==-1&&(r={...t.jobs[n],...e},t.jobs.splice(n,1),t.count=t.jobs.length)});let i=E.statuses.find(e=>e.key===n);return i&&(i.jobs.unshift(r),i.count=i.jobs.length),r}function ii(e,t){E.statuses.forEach(e=>{let t=document.querySelector(`#status-${CSS.escape(e.key)}`);t?.classList.toggle(`empty`,e.count===0);let n=t?.querySelector(`.count`);n&&(n.textContent=e.count)}),[e,t].forEach(e=>{si(document.querySelector(`#status-${CSS.escape(e)}`))})}function ai(e,t){if(!E.stats)return;let n=Pt.has(e),r=Pt.has(t);if(n===r){mn(E.stats);return}E.stats.applications_total=Number(E.stats.applications_total??0)+(r?1:-1),mn(E.stats)}function oi(e,t,n,r){let i=document.querySelector(`#status-${CSS.escape(r)}`),a=i?.querySelector(`.pane-body`);if(!e||!i||!a)return;e.remove(),si(document.querySelector(`#status-${CSS.escape(n)}`)),a.hidden=!1;let o=i.querySelector(`.pane-toggle`);o?.setAttribute(`aria-expanded`,`true`);let s=o?.querySelector(`.chevron`);s&&(s.textContent=`v`);let c=a.querySelector(`.jobs`);c||=(a.innerHTML=`<div class="jobs"></div>`,a.querySelector(`.jobs`)),c.insertAdjacentHTML(`afterbegin`,kn(t,r)),si(i)}function si(e){if(!e)return;let t=e.querySelector(`.pane-body`);if(!t)return;let n=t.querySelector(`.jobs`),r=!!n?.querySelector(`.job`),i=t.querySelector(`.empty-copy`);if(r){i?.remove();return}n?.remove(),i||t.insertAdjacentHTML(`beforeend`,`<p class="empty-copy">no jobs in this status.</p>`)}function ci(e){ve.disabled=li(e).length===0,ve.setAttribute(`aria-label`,`review discovered`),ve.innerHTML=`<span class="review-discovered-label">review discovered</span>`}function li(e=E?.statuses??[]){return e.find(e=>e.key===`discovered`)?.jobs??[]}function ui(e){ye.disabled=di(e).length===0,ye.setAttribute(`aria-label`,`prep interested`),ye.innerHTML=`<span class="review-discovered-label">prep interested</span>`}function di(e=E?.statuses??[]){return e.find(e=>e.key===`interested`)?.jobs??[]}function fi(e=null){let t=[...li()],n=e==null?null:String(e);if(n){let e=t.findIndex(e=>String(e.id)===n);if(e>0){let[n]=t.splice(e,1);t.unshift(n)}}j=t,h.hidden=!1,document.body.classList.add(`review-open`),gi()}function pi(){h.hidden=!0,document.body.classList.remove(`review-open`),j=[]}function mi(e=null){let t=[...di()].sort((e,t)=>Number(!!t.prep_started)-Number(!!e.prep_started)),n=e==null?null:String(e);if(n){let e=t.findIndex(e=>String(e.id)===n);if(e>0){let[n]=t.splice(e,1);t.unshift(n)}}M=t,g.hidden=!1,document.body.classList.add(`prep-open`),Mi()}function hi(){g.hidden=!0,document.body.classList.remove(`prep-open`),M=[]}function gi(e=``){let t=j[0],n=j.length,r=t?_i(t):``;if(be.textContent=n>0?`review queue`:`review complete`,xe.textContent=n>0?`${n} discovered ${n===1?`role`:`roles`} in queue`:``,h.querySelectorAll(`.review-action`).forEach(e=>{e.disabled=n===0}),!t){Se.innerHTML=`
      <div class="review-empty">
        <h3>no discovered jobs left.</h3>
        <p>everything in this queue has been handled or moved out of discovered.</p>
      </div>
    `;return}Se.innerHTML=`
    ${e?`<p class="review-message">${U(e)}</p>`:``}
    ${r?`<p class="review-message review-message-warning">${U(r)}</p>`:``}
    <div class="review-title-row">
      <p class="review-company">${G(t.company_name)}</p>
      ${pn(t.title,t.role_url,`review-role-title`)}
    </div>
    <dl class="review-details review-primary-details">
      ${X(`location`,t.location,!1,`review-location-detail`)}
      ${X(`first`,H(t.first_seen_at))}
      ${X(`last`,H(t.last_seen_at))}
    </dl>
    ${vi(t.description)}
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
  `}function _i(e){let t=Number(e.review_later_count??0);return t<=Mt?``:`role review has been postponed ${t} times. it is recommended to set it to disinterested.`}function X(e,t,n=!1,r=``){if(!t)return``;let i=n?`<a href="${U(t)}" target="_blank" rel="noreferrer">${G(t)}</a>`:G(t);return`
    <div class="review-detail ${U(r)}">
      <dt>${G(e)}</dt>
      <dd>${i}</dd>
    </div>
  `}function vi(e){return e?`
    <div class="review-detail review-description">
      <dt>description</dt>
      <dd>${yi(e)}</dd>
    </div>
  `:``}function yi(e){let t=bi(String(e)).replace(/\u00a0/g,` `);if(xi(t))return Si(t);let n=t.split(/\r?\n/).map(e=>e.trim()).filter(Boolean),r=[],i=[],a=()=>{i.length!==0&&(r.push(`<ul>${i.map(e=>`<li>${e}</li>`).join(``)}</ul>`),i=[])};return n.forEach(e=>{let t=e.match(/^#{2,3}\s+(.+)$/);if(t){a(),r.push(`<h3>${G(t[1])}</h3>`);return}if(Ai(e)){a(),r.push(`<h3>${G(e.replace(/:$/,``))}</h3>`);return}let n=e.match(/^[-*]\s+(.+)$/);if(n){i.push(G(n[1]));return}a(),r.push(`<p>${G(e)}</p>`)}),a(),r.join(``)}function bi(e){let t=document.createElement(`textarea`);return t.innerHTML=e,t.value}function xi(e){return/<\/?(?:a|br|div|em|h[1-6]|li|ol|p|span|strong|ul)\b/i.test(e)}function Si(e){let t=document.createElement(`template`);t.innerHTML=e;let n=[];return Ci(t.content.childNodes,n),n.join(``)}function Ci(e,t){e.forEach(e=>{if(e.nodeType===Node.TEXT_NODE){let n=Oi(e.textContent);n&&t.push(`<p>${G(n)}</p>`);return}if(e.nodeType!==Node.ELEMENT_NODE)return;let n=e,r=n.tagName.toLowerCase();if(r===`script`||r===`style`||r===`br`)return;if(/^h[1-6]$/.test(r)){Ti(t,n.textContent);return}if(r===`ul`||r===`ol`){let e=Ei(n);e&&t.push(e);return}if(r===`p`){wi(n,t);return}let i=Array.from(n.children).some(e=>[`DIV`,`H1`,`H2`,`H3`,`H4`,`H5`,`H6`,`OL`,`P`,`UL`].includes(e.tagName));if([`article`,`div`,`section`].includes(r)&&i){Ci(n.childNodes,t);return}let a=Array.from(n.children).filter(e=>[`UL`,`OL`].includes(e.tagName)),o=Oi(Di(n));if(o&&(ki(o,n)?Ti(t,o):t.push(`<p>${G(o)}</p>`)),a.length>0){a.forEach(e=>{let n=Ei(e);n&&t.push(n)});return}!o&&i&&Ci(n.childNodes,t)})}function wi(e,t){if(!e.querySelector(`br`)){let n=Oi(Di(e));if(!n)return;ki(n,e)?Ti(t,n):t.push(`<p>${G(n)}</p>`);return}let n=``,r=()=>{let r=Oi(n);n=``,r&&(ki(r,e)?Ti(t,r):t.push(`<p>${G(r)}</p>`))};e.childNodes.forEach(e=>{if(e.nodeType===Node.ELEMENT_NODE&&e.tagName.toLowerCase()===`br`){r();return}n+=` ${e.textContent??``}`}),r()}function Ti(e,t){let n=Oi(t).replace(/:$/,``);n&&e.push(`<h3>${G(n)}</h3>`)}function Ei(e){let t=Array.from(e.children).filter(e=>e.tagName===`LI`).map(e=>{let t=Oi(Di(e)),n=Array.from(e.children).filter(e=>[`UL`,`OL`].includes(e.tagName)).map(e=>Ei(e)).filter(Boolean).join(``);return t||n?`<li>${G(t)}${n}</li>`:``}).filter(Boolean);return t.length>0?`<ul>${t.join(``)}</ul>`:``}function Di(e){let t=e.cloneNode(!0);return t.querySelectorAll(`ul, ol`).forEach(e=>{e.remove()}),t.textContent}function Oi(e){return String(e??``).replace(/\s+/g,` `).trim()}function ki(e,t){let n=e.replace(/:$/,``).trim();return!n||n.length>90?!1:Ai(n)||/:$/.test(e)?!0:/[.!?]$/.test(n)||n.split(/\s+/).length>10?!1:t.querySelector(`strong, b, u`)?!0:Ai(n)}function Ai(e){return It.test(String(e).trim())}async function ji(e){let t=j[0];if(!t)return;if(e===`later`){h.querySelectorAll(`.review-action`).forEach(e=>{e.disabled=!0});try{let e=await ta(t.id);j.shift(),ni(e),gi(`moved out of this review pass.`)}catch{gi(`could not postpone that role. try again.`)}finally{h.querySelectorAll(`.review-action`).forEach(e=>{e.disabled=j.length===0})}return}if(![`interested`,`disinterested`].includes(e))return;let n=h.querySelectorAll(`.review-action`);n.forEach(e=>{e.disabled=!0});try{let n=await na(t.id,e);j.shift(),gi(e===`interested`?`marked interested.`:`marked disinterested.`),ti(n,document.querySelector(`.job[data-role-id="${CSS.escape(String(t.id))}"]`))}catch{n.forEach(e=>{e.disabled=!1}),gi(`could not update that role. try again.`)}}async function Mi(e=``){let t=M[0],n=M.length;if(we.textContent=n>0?`prep queue`:`prep complete`,Te.textContent=n>0?`${n} interested ${n===1?`role`:`roles`} in queue`:``,g.querySelectorAll(`.review-action`).forEach(e=>{e.disabled=n===0}),!t){_.innerHTML=`
      <div class="review-empty">
        <h3>no interested jobs left.</h3>
        <p>everything in this queue has been prepped, moved, or postponed.</p>
      </div>
    `;return}_.innerHTML=`
    ${e?`<p class="review-message">${U(e)}</p>`:``}
    <section class="prep-role-hero" aria-label="role overview">
      <div class="review-title-row">
        <div class="prep-role-eyebrow">
          <p class="review-company">${G(t.company_name)}</p>
          <span>application workspace</span>
        </div>
        ${pn(t.title,t.role_url,`review-role-title`)}
      </div>
      <dl class="review-details review-primary-details">
        ${X(`location`,t.location,!1,`review-location-detail`)}
        ${X(`last`,H(t.last_seen_at))}
        ${X(`updated`,H(t.updated_at))}
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
      ${Ni(t)}
      ${Li(t)}
      ${Pi(t.id,t.description)}
      ${Fi(t)}
    </div>
  `,K(),Ui(t.id).then(e=>{!e||M[0]?.id!==t.id||(P.set(t.id,e),_.querySelector(`.prep-resume`)?.replaceWith(Q(Ni(t,{resume:e}))),K())}).catch(()=>{}),ea(t.id).then(e=>{!e||M[0]?.id!==t.id||(F.set(t.id,e),_.querySelector(`.prep-cover-letter`)?.replaceWith(Q(Li(t,{coverLetter:e}))),K())}).catch(()=>{})}function Ni(e,t={}){let n=P.get(e.id),r=t.resume??n,i=t.tweaks??Bt.get(e.id)??``,a=`/api/roles/${encodeURIComponent(e.id)}/resume.pdf`;return t.loading?`
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
        <section class="prep-document-preview" aria-label="résumé preview">
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
    `}function Pi(e,t){return`
    <details class="prep-panel prep-description-panel" id="prep-description-${e}">
      <summary class="prep-analysis-header">
        <span class="prep-accordion-icon" aria-hidden="true"></span>
        <h3>description</h3>
      </summary>
      ${vi(t)}
    </details>
  `}function Fi(e,t={}){let n=t.messages??Vt.get(e.id)??[],r=!!t.loading;return`
    <details class="prep-panel prep-role-chat" id="prep-chat-${e.id}">
      <summary class="prep-analysis-header">
        <span class="prep-accordion-icon" aria-hidden="true"></span>
        <h3>chat about this role</h3>
        <span>${n.length?`${n.length} messages`:`ready`}</span>
      </summary>
      <div class="prep-role-chat-log" aria-live="polite">
        ${n.length?n.map(Ii).join(``):`<p class="prep-role-chat-empty">ask about fit, risks, resume emphasis, or cover letter angle.</p>`}
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
  `}function Ii(e){let t=e?.role===`assistant`?`assistant`:`user`;return`
    <article class="prep-role-chat-message prep-role-chat-message-${t}">
      <span>${t}</span>
      <p>${G(e?.content??``)}</p>
    </article>
  `}function Li(e,t={}){let n=F.get(e.id),r=t.coverLetter??n,i=t.tweaks??r?.tweaks??``,a=`/api/roles/${encodeURIComponent(e.id)}/cover-letter.pdf`;return t.loading?`
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
          <p>Use the role, résumé, and saved examples to shape the letter.</p>
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
  `}function Z(e,t={}){let n=N.get(e.id);if(!t.loading&&!t.error&&!t.analysis&&n)return Z(e,{analysis:n});if(!t.loading&&!t.error&&!t.analysis)return`
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
    `;let r=t.analysis,i=Array.isArray(r?.feedback_items)?r.feedback_items:[],a=r?.verdict===`ready_to_apply`?`ready to apply`:`tweak`,o=Math.min(zt.get(e.id)??0,Math.max(i.length-1,0)),s=i[o];return`
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
              ${Ri(s)}
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
  `}function Ri(e){return e?.tweak_prompt?`
    <div class="prep-proposed-edit">
      <p class="prep-proposed-label">tweak prompt</p>
      <p>${G(e.tweak_prompt)}</p>
    </div>
  `:`
      <div class="prep-proposed-edit">
        <p class="prep-proposed-label">feedback only</p>
        <p>not enough information to turn this into a safe resume tweak.</p>
      </div>
    `}async function zi(e,t={}){if(!t.force&&N.has(e))return N.get(e);let n=await fetch(`/api/roles/${encodeURIComponent(e)}/prep-analysis`);if(!n.ok)throw Error(`Prep analysis request failed`);let r=await n.json();return r.analysis.resources=r.resources??[],N.set(e,r.analysis),r.analysis}function Q(e){let t=document.createElement(`template`);return t.innerHTML=e.trim(),t.content.firstElementChild}async function Bi(e){let t=M[0];if(!t)return;let n=g.querySelectorAll(`.review-action`);if(n.forEach(e=>{e.disabled=!0}),e===`later`){try{await ta(t.id),t.review_later_count=Number(t.review_later_count??0)+1,M.length>1?(M.push(M.shift()),Mi(`moved to the back of the prep queue.`)):Mi(`only one role is in the prep queue.`)}catch{Mi(`could not postpone prep. try again.`)}return}if(e===`applied`)try{let e=await na(t.id,`applied`);M.shift(),Mi(`moved to applied.`),ti(e,document.querySelector(`.job[data-role-id="${CSS.escape(String(t.id))}"]`))}catch{n.forEach(e=>{e.disabled=!1}),Mi(`could not move that role. try again.`)}}async function Vi(e,t,n,r){let i=await fetch(`/api/roles/${encodeURIComponent(e)}/prep-feedback`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({feedback_index:t,feedback_item:n,comment:r})});if(!i.ok)throw Error(`Prep feedback update failed`);return i.json()}async function Hi(e,t,n,r){let i=await fetch(`/api/roles/${encodeURIComponent(e)}/prep-feedback-ignore`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({feedback_index:t,feedback_item:n,comment:r})});if(!i.ok)throw Error(`Prep feedback ignore failed`);return i.json()}async function Ui(e,{force:t=!1}={}){if(!t&&P.has(e))return P.get(e);let n=await fetch(`/api/roles/${encodeURIComponent(e)}/resume`);if(!n.ok)throw Error(`Resume request failed`);let r=await n.json();return r.resume&&P.set(e,r.resume),r.resume}async function Wi(e,t){let n=await fetch(`/api/roles/${encodeURIComponent(e)}/resume/save`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({latex:t})});if(!n.ok)throw Error(`Resume save failed`);return n.json()}async function Gi(e,t,n){let r=await fetch(`/api/roles/${encodeURIComponent(e)}/resume`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({tweaks:t,previous_latex:n})});if(!r.ok)throw Error(`Resume generation failed`);return r.json()}async function Ki(e,t){let n=await fetch(`/api/roles/${encodeURIComponent(e)}/chat`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({messages:t})});if(!n.ok)throw Error(`Role chat failed`);return n.json()}function qi(e,t,n=Nt){let r=Ht.get(e)??{timer:null,saving:!1,version:0,latex:``};r.version+=1,r.latex=t,r.timer&&clearTimeout(r.timer),r.timer=setTimeout(()=>{r.timer=null,Ji(e)},n),Ht.set(e,r)}async function Ji(e){let t=Ht.get(e);if(!t||t.saving)return;t.saving=!0;let n=t.version,r=t.latex;try{let i=await Wi(e,r);t.version===n&&(P.set(e,i.resume),Yi(`resume`,e,i.resume))}catch{}finally{t.saving=!1,t.version!==n&&qi(e,t.latex,0)}}function Yi(e,t,n){if(!n?.pdf_base64)return;let r=e===`resume`?`[data-prep-resume-latex="${t}"]`:`[data-prep-cover-letter-latex="${t}"]`,i=_.querySelector(r)?.closest(`.prep-panel`),a=i?.querySelector(`.prep-cover-pdf`),o=i?.querySelector(`.prep-cover-pdf-link`),s=e===`resume`?`/api/roles/${encodeURIComponent(t)}/resume.pdf`:`/api/roles/${encodeURIComponent(t)}/cover-letter.pdf`;a&&(a.src=`${s}?v=${Date.now()}`),o&&(o.href=s)}async function Xi(e,t=``,n=``){let r=await fetch(`/api/roles/${encodeURIComponent(e)}/cover-letter`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({tweaks:t,previous_latex:n})});if(!r.ok)throw Error(`Cover letter generation failed`);return r.json()}async function Zi(e,t){let n=await fetch(`/api/roles/${encodeURIComponent(e)}/cover-letter/save`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({latex:t})});if(!n.ok)throw Error(`Cover letter save failed`);return n.json()}function Qi(e,t,n=``,r=Nt){let i=Ut.get(e)??{timer:null,saving:!1,version:0,latex:``,tweaks:``};i.version+=1,i.latex=t,i.tweaks=n,i.timer&&clearTimeout(i.timer),i.timer=setTimeout(()=>{i.timer=null,$i(e)},r),Ut.set(e,i)}async function $i(e){let t=Ut.get(e);if(!t||t.saving)return;t.saving=!0;let n=t.version,r=t.latex,i=t.tweaks;try{let a=await Zi(e,r);t.version===n&&(F.set(e,{...a.cover_letter,tweaks:i}),Yi(`coverLetter`,e,a.cover_letter))}catch{}finally{t.saving=!1,t.version!==n&&Qi(e,t.latex,t.tweaks,0)}}async function ea(e){if(F.has(e))return F.get(e);let t=await fetch(`/api/roles/${encodeURIComponent(e)}/cover-letter`);if(!t.ok)throw Error(`Cover letter request failed`);let n=await t.json();return n.cover_letter&&F.set(e,n.cover_letter),n.cover_letter}async function ta(e){let t=await fetch(`/api/roles/${encodeURIComponent(e)}/review-later`,{method:`POST`});if(!t.ok)throw Error(`Review later update failed`);return(await t.json()).role}async function na(e,t){let n=await fetch(`/api/roles/${encodeURIComponent(e)}/status`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({status:t})});if(!n.ok)throw Error(`Status update failed`);return(await n.json()).role}function ra(e){return`${e}-${globalThis.crypto?.randomUUID?.()??`${Date.now()}-${Math.random()}`}`}function ia(e){window.location.hash!==e&&window.history.pushState({},``,e||`${window.location.pathname}${window.location.search}`)}async function aa(){if(De){Ie.textContent=`Autoprep Selected`,ke.hidden=!1,document.body.classList.add(`autoprep-open`),ia(`#autoprep-interested`),Pe.textContent=`loading Interested roles...`;try{let e=await fetch(`/api/autoprep/interested`);if(!e.ok)throw Error(`Interested roles request failed`);Wt=(await e.json()).roles??[];let t=new Set(Wt.filter(e=>e.selectable).map(e=>Number(e.id)));I=new Set([...I].filter(e=>t.has(e))),Pe.textContent=``,sa()}catch{Pe.textContent=`could not load Interested roles.`,Fe.innerHTML=``}}}function oa({clearHash:e=!0}={}){ke.hidden=!0,document.body.classList.remove(`autoprep-open`),e&&window.location.hash===`#autoprep-interested`&&ia(``)}function sa(){if(Wt.length===0){Fe.innerHTML=`<div class="autoprep-empty"><h3>no Interested roles.</h3><p>Mark roles Interested on the homepage before using Autoprep.</p></div>`,ca();return}Fe.innerHTML=Wt.map(e=>{let t=Number(e.id),n=e.preparation_status?ga(e.preparation_status):e.manual_prep_started?`Manual preparation started`:`Not started`,r=[e.location,e.date_added?`added ${H(e.date_added)}`:``].filter(Boolean).map(G).join(` · `);return`
      <label class="autoprep-role${e.selectable?``:` is-unavailable`}">
        <input type="checkbox" data-autoprep-role="${t}" ${I.has(t)?`checked`:``} ${e.selectable?``:`disabled`} />
        <span class="autoprep-role-copy"><strong>${G(e.company_name)}</strong><span>${G(e.title)}</span><small>${r}</small></span>
        <span class="autoprep-role-status">${U(n)}</span>
      </label>`}).join(``),ca()}function ca(){let e=I.size;Ne.textContent=`${e} selected`,Ie.disabled=e===0||L,je.disabled=L||!Wt.some(e=>e.selectable),Me.disabled=L||e===0}async function la(){if(!(L||I.size===0)){L=!0,Ie.disabled=!0,Ie.textContent=`Queuing selected roles...`,Pe.textContent=`creating durable preparation jobs...`,Fe.querySelectorAll(`input`).forEach(e=>{e.disabled=!0});try{let e=await fetch(`/api/autoprep/jobs`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({role_ids:[...I],idempotency_key:ra(`autoprep`)})}),t=await e.json();if(!e.ok)throw Error(t.error||`Autoprep queue request failed`);R=t.jobs??[],z=R[0]?.role_id??null,oa({clearHash:!1}),ua({seedJobs:R})}catch(e){Pe.textContent=e.message||`could not queue selected roles.`,L=!1,Ie.textContent=`Autoprep Selected`,sa()}}}async function ua({seedJobs:e=null}={}){Le.hidden=!1,document.body.classList.add(`prepped-open`),ia(`#prepped-roles`),e?(R=e,z=z??R[0]?.role_id??null,$()):R.length===0&&(ze.textContent=`loading prepared roles...`),await fa(),pa()}function da({clearHash:e=!0}={}){Le.hidden=!0,document.body.classList.remove(`prepped-open`),ma(),e&&window.location.hash===`#prepped-roles`&&ia(``)}async function fa(){try{let e=await fetch(`/api/autoprep/jobs`);if(!e.ok)throw Error(`Prepped roles request failed`);R=(await e.json()).jobs??[],R.some(e=>Number(e.role_id)===Number(z))||(z=R[0]?.role_id??null),$()}catch{ze.textContent=`could not refresh preparation progress.`}}function pa(){ma(),R.some(ha)&&(Gt=window.setInterval(fa,2e3))}function ma(){Gt!==null&&window.clearInterval(Gt),Gt=null}function ha(e){return[`queued`,`generating_resume_tweaks`,`regenerating_resume`,`generating_cover_letter`].includes(e.overall_status)}function ga(e){return{queued:`Queued`,generating_resume_tweaks:`Generating résumé tweaks`,regenerating_resume:`Regenerating résumé`,generating_cover_letter:`Generating cover letter`,partially_complete:`Partially complete`,ready:`Ready`,failed:`Failed`,interrupted:`Interrupted`,generating_tweaks:`Generating tweaks`,regenerating:`Regenerating`,generating:`Generating`}[e]??W(e)}function $(){let e=R.filter(ha).length;ze.textContent=R.length?`${R.length} prepped ${R.length===1?`role`:`roles`}${e?` · ${e} in progress`:``}`:`No queued or prepared roles.`,Be.innerHTML=R.map(e=>`
    <button type="button" class="prepped-list-item${Number(e.role_id)===Number(z)?` is-active`:``}" data-prepped-role="${e.role_id}">
      <strong>${G(e.company_name)}</strong><span>${G(e.title)}</span>
      <small class="status-${U(e.overall_status)}">${U(ga(e.overall_status))}</small>
    </button>`).join(``),_a(),pa()}function _a(){let e=R.findIndex(e=>Number(e.role_id)===Number(z)),t=R[e];if(!t){v.innerHTML=`<div class="prepped-empty"><h3>nothing prepped yet.</h3><p>Queue Interested roles from Autoprep Interested.</p></div>`;return}let n=G(t.title),r=cn(t.role_url),i=r?`<a class="prepped-role-link" href="${U(r)}" target="_blank" rel="noopener noreferrer">${n}<span aria-hidden="true">↗</span></a>`:n,a=[[`Location`,t.location||`Unavailable`],[`Added`,H(t.date_added||t.created_at)||`Unavailable`],[`Last seen`,H(t.last_seen_at)||`Unavailable`],[`Posting ID`,t.posting_id||`Unavailable`]];v.innerHTML=`
    <header class="prepped-detail-heading">
      <div><p class="eyebrow">${G(t.company_name)}</p><h3>${i}</h3></div>
      <span class="prepped-status status-${U(t.overall_status)}">${U(ga(t.overall_status))}</span>
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
      ${va(t,`resume`,`Résumé`)}
      ${va(t,`cover-letter`,`Cover letter`)}
    </div>
    <div class="prepped-detail-actions">
      <button type="button" data-prepped-nav="previous" ${e<=0?`disabled`:``}>Previous</button>
      <button type="button" data-prepped-nav="next" ${e>=R.length-1?`disabled`:``}>Next</button>
      <button type="button" data-autoprep-open-folder ${t.artifact_directory?``:`disabled`}>Open Documents Folder</button>
      <button class="success" type="button" data-autoprep-applied ${t.overall_status===`ready`?``:`disabled`}>Applied</button>
    </div>
    <p class="prepped-safety-note">Autoprep prepares files only. It never submits an application.</p>`}function va(e,t,n){let r=t===`cover-letter`?`cover_letter`:`resume`,i=e[`${r}_status`],a=e[`${r}_artifact_path`],o=a?.split(`/`).pop()??`Not available`,s=e[`${r}_error`],c=e[`${r}_instruction`]||``,l=`${e.role_id}:${t}`,u=Kt.get(l)??c,d=[`queued`,`generating`,`generating_tweaks`,`regenerating`].includes(i),f=[`failed`,`interrupted`].includes(i)?`<button type="button" data-autoprep-retry="${t}">Retry ${U(n.toLowerCase())}</button>`:``,p=qt.has(l),ee=`/api/autoprep/roles/${encodeURIComponent(e.role_id)}/documents/${t}.pdf?v=${encodeURIComponent(e.updated_at||``)}`;return`
    <section class="prepped-document status-${U(i)}">
      <div class="prepped-document-heading"><h4>${U(n)}</h4><span>${U(ga(i))}</span></div>
      <p class="prepped-filename">${U(o)}</p>
      ${s?`<p class="prepped-error">${U(s)}</p>`:``}
      <div class="prepped-document-actions">
        <button type="button" data-autoprep-preview="${t}" ${a?``:`disabled`}>${p?`Hide preview`:`Preview PDF`}</button>
        ${f}
      </div>
      <div class="prepped-pdf-preview" data-autoprep-preview-panel="${t}" ${p&&a?``:`hidden`}>
        ${p&&a?`<iframe title="${U(n)} PDF preview" src="${U(ee)}"></iframe>`:``}
      </div>
      <label class="prepped-comments-label" for="prepped-comments-${U(l)}">Comments for the next version</label>
      <textarea id="prepped-comments-${U(l)}" data-autoprep-comments="${t}" rows="4" placeholder="Describe specific, truthful changes..." ${d?`disabled`:``}>${G(u)}</textarea>
      <button class="prepped-regenerate" type="button" data-autoprep-regenerate="${t}" ${i===`ready`&&String(u).trim()?``:`disabled`}>${d?`Regenerating...`:`Regenerate ${U(n)}`}</button>
    </section>`}async function ya(e,t,n){if(n.disabled)return;let r=`${e.role_id}:${t}`,i=v.querySelector(`[data-autoprep-comments="${t}"]`),a=String(i?.value||Kt.get(r)||``).trim();if(!a){i?.focus();return}n.disabled=!0,n.textContent=`Queuing regeneration...`;try{let n=await fetch(`/api/autoprep/roles/${encodeURIComponent(e.role_id)}/regenerate/${t}`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({comments:a,idempotency_key:ra(`regenerate-${t}`)})}),i=await n.json();if(!n.ok)throw Error(i.error||`Regeneration request failed`);Kt.delete(r);let o=R.findIndex(t=>Number(t.role_id)===Number(e.role_id));o>=0&&(R[o]=i.job),$()}catch(e){window.alert(e instanceof Error?e.message:`Regeneration request failed`),await fa()}}async function ba(e,t,n){if(!n.disabled){n.disabled=!0,n.textContent=`Queuing retry...`;try{let n=await fetch(`/api/autoprep/roles/${encodeURIComponent(e)}/retry/${t}`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({idempotency_key:ra(`retry-${t}`)})}),r=await n.json();if(!n.ok)throw Error(r.error||`Retry request failed`);let i=R.findIndex(t=>Number(t.role_id)===Number(e));i>=0&&(R[i]=r.job),$()}catch{await fa()}}}async function xa(e,t){if(t.disabled)return;t.disabled=!0,t.textContent=`Moving to Applied...`;let n=R.findIndex(t=>Number(t.role_id)===Number(e));try{if(!(await fetch(`/api/autoprep/roles/${encodeURIComponent(e)}/applied`,{method:`POST`})).ok)throw Error(`Applied update failed`);R.splice(n,1),z=R[Math.min(n,R.length-1)]?.role_id??null,$(),br()}catch{await fa()}}ve.addEventListener(`click`,fi),Ce.addEventListener(`click`,pi),ye.addEventListener(`click`,mi),De?.addEventListener(`click`,aa),Oe.addEventListener(`click`,()=>ua()),Ae.addEventListener(`click`,oa),Re.addEventListener(`click`,da),je.addEventListener(`click`,()=>{L||(I=new Set(Wt.filter(e=>e.selectable).map(e=>Number(e.id))),sa())}),Me.addEventListener(`click`,()=>{L||(I.clear(),sa())}),Fe.addEventListener(`change`,e=>{let t=e.target.closest(`[data-autoprep-role]`);if(!t||L)return;let n=Number(t.dataset.autoprepRole);t.checked?I.add(n):I.delete(n),ca()}),Ie.addEventListener(`click`,la),Be.addEventListener(`click`,e=>{let t=e.target.closest(`[data-prepped-role]`);t&&(z=Number(t.dataset.preppedRole),$())}),v.addEventListener(`input`,e=>{let t=e.target.closest(`[data-autoprep-comments]`);if(!t)return;let n=`${z}:${t.dataset.autoprepComments}`;Kt.set(n,t.value);let r=v.querySelector(`[data-autoprep-regenerate="${t.dataset.autoprepComments}"]`),i=R.find(e=>Number(e.role_id)===Number(z)),a=t.dataset.autoprepComments===`cover-letter`?`cover_letter`:`resume`;r&&(r.disabled=i?.[`${a}_status`]!==`ready`||!t.value.trim())}),v.addEventListener(`click`,async e=>{let t=R.find(e=>Number(e.role_id)===Number(z));if(!t)return;let n=e.target.closest(`[data-prepped-nav]`);if(n){let e=R.indexOf(t),r=n.dataset.preppedNav===`next`?1:-1;z=R[e+r]?.role_id??t.role_id,$();return}let r=e.target.closest(`[data-autoprep-preview]`);if(r){let e=`${t.role_id}:${r.dataset.autoprepPreview}`;qt.has(e)?qt.delete(e):qt.add(e),_a();return}let i=e.target.closest(`[data-autoprep-regenerate]`);if(i){ya(t,i.dataset.autoprepRegenerate,i);return}let a=e.target.closest(`[data-autoprep-retry]`);if(a){ba(t.role_id,a.dataset.autoprepRetry,a);return}let o=e.target.closest(`[data-autoprep-open-folder]`);if(o&&!o.disabled){o.disabled=!0;try{if(!(await fetch(`/api/autoprep/roles/${encodeURIComponent(t.role_id)}/open-folder`,{method:`POST`})).ok)throw Error(`Folder open failed`)}finally{o.disabled=!1}return}let s=e.target.closest(`[data-autoprep-applied]`);s&&xa(t.role_id,s)}),Ee.addEventListener(`click`,hi),h.addEventListener(`click`,e=>{let t=e.target.closest(`[data-review-action]`);t&&ji(t.dataset.reviewAction)}),g.addEventListener(`click`,e=>{e.target.closest(`.prep-summary-action`)&&e.stopPropagation()}),g.addEventListener(`input`,e=>{let t=e.target.closest(`[data-prep-resume-tweaks]`);if(t){let e=Number(t.dataset.prepResumeTweaks);Number.isFinite(e)&&Bt.set(e,t.value);return}let n=e.target.closest(`[data-prep-resume-latex]`);if(n){let e=Number(n.dataset.prepResumeLatex);if(!Number.isFinite(e))return;qi(e,n.value);return}let r=e.target.closest(`[data-prep-cover-letter-latex]`);if(!r)return;let i=Number(r.dataset.prepCoverLetterLatex);if(!Number.isFinite(i))return;let a=r.closest(`.prep-cover-letter`)?.querySelector(`[data-prep-cover-letter-tweaks="${i}"]`)?.value??``;Qi(i,r.value,a)}),g.addEventListener(`scroll`,e=>{e.target.closest(`[data-prep-resume-latex], [data-prep-cover-letter-latex]`)},!0),g.addEventListener(`focusout`,e=>{let t=e.target.closest(`[data-prep-resume-latex]`);if(t){let e=Number(t.dataset.prepResumeLatex);if(!Number.isFinite(e))return;qi(e,t.value,0);return}let n=e.target.closest(`[data-prep-cover-letter-latex]`);if(!n)return;let r=Number(n.dataset.prepCoverLetterLatex);if(!Number.isFinite(r))return;let i=n.closest(`.prep-cover-letter`)?.querySelector(`[data-prep-cover-letter-tweaks="${r}"]`)?.value??``;Qi(r,n.value,i,0)}),g.addEventListener(`submit`,async e=>{let t=e.target.closest(`[data-prep-role-chat-form]`);if(!t||!M[0])return;e.preventDefault();let n=Number(t.dataset.prepRoleChatForm);if(!Number.isFinite(n))return;let r=t.querySelector(`[data-prep-role-chat-input="${n}"]`),i=r?.value?.trim()??``;if(!i){r?.focus();return}let a=[...Vt.get(n)??[],{role:`user`,content:i}];Vt.set(n,a),_.querySelector(`.prep-role-chat`)?.replaceWith(Q(Fi(M[0],{messages:a,loading:!0})));try{let e=await Ki(n,a),t=[...a,e.message];Vt.set(n,t),_.querySelector(`.prep-role-chat`)?.replaceWith(Q(Fi(M[0],{messages:t})))}catch{let e=[...a,{role:`assistant`,content:`could not answer right now.`}];Vt.set(n,e),_.querySelector(`.prep-role-chat`)?.replaceWith(Q(Fi(M[0],{messages:e})))}}),g.addEventListener(`click`,async e=>{let t=e.target.closest(`[data-prep-section-target]`);if(t){let e=t.dataset.prepSectionTarget,n=e?document.getElementById(e):null;if(n instanceof HTMLDetailsElement){n.open=!0,n.scrollIntoView({behavior:`smooth`,block:`start`});let e=n.querySelector(`summary`);e?.setAttribute(`tabindex`,`-1`),e?.focus({preventScroll:!0})}return}if(e.target.closest(`[data-prep-analysis]`)&&M[0]){let e=M[0].id;_.querySelector(`.prep-analysis`)?.replaceWith(Q(Z(M[0],{loading:!0})));try{let t=await zi(e,{force:!0});if(M[0]?.id!==e)return;_.querySelector(`.prep-analysis`)?.replaceWith(Q(Z(M[0],{analysis:t})))}catch{_.querySelector(`.prep-analysis`)?.replaceWith(Q(Z(M[0],{error:!0})))}return}if(e.target.closest(`[data-prep-resume-regenerate]`)&&M[0]){let e=M[0].id,t=_.querySelector(`.prep-resume`),n=t?.querySelector(`[data-prep-resume-tweaks="${e}"]`)?.value??``,r=t?.querySelector(`[data-prep-resume-latex="${e}"]`)?.value??``;if(!n.trim()){t?.querySelector(`[data-prep-resume-tweaks="${e}"]`)?.focus();return}Bt.set(e,n),t?.replaceWith(Q(Ni(M[0],{loading:!0})));try{let t=await Gi(e,n,r);P.set(e,t.resume),_.querySelector(`.prep-resume`)?.replaceWith(Q(Ni(M[0],{resume:t.resume}))),K()}catch{_.querySelector(`.prep-resume`)?.replaceWith(Q(Ni(M[0],{resume:P.get(e),tweaks:n}))),K()}return}if(e.target.closest(`[data-prep-cover-letter]`)&&M[0]){let e=M[0].id,t=_.querySelector(`.prep-cover-letter`),n=t?.querySelector(`[data-prep-cover-letter-tweaks="${e}"]`)?.value??``,r=n.trim()?t?.querySelector(`[data-prep-cover-letter-latex="${e}"]`)?.value??``:``;t?.replaceWith(Q(Li(M[0],{loading:!0})));try{let t=await Xi(e,n,r);F.set(e,t.cover_letter),_.querySelector(`.prep-cover-letter`)?.replaceWith(Q(Li(M[0],{coverLetter:t.cover_letter}))),K()}catch{_.querySelector(`.prep-cover-letter`)?.replaceWith(Q(Li(M[0],{coverLetter:F.get(e),tweaks:n}))),K()}return}let n=e.target.closest(`[data-prep-action]`);if(n){Bi(n.dataset.prepAction);return}let r=e.target.closest(`[data-prep-feedback]`);if(!r||!M[0])return;let i=M[0].id,a=N.get(i),o=Array.isArray(a?.feedback_items)?a.feedback_items.length:0,s=zt.get(i)??0;if(r.dataset.prepFeedback===`accept`||r.dataset.prepFeedback===`ignore`){let e=a?.feedback_items?.[s];if(!e)return;let t=_.querySelector(`[data-prep-feedback-comment]`)?.value??``,n=r.dataset.prepFeedback,o=n;r.disabled=!0,r.textContent=n===`accept`?`adding...`:`ignoring...`;try{if(n===`accept`){let n=await Vi(i,s,e,t),r=document.querySelector(`.job[data-role-id="${CSS.escape(String(i))}"]`);n.role&&(M[0]=n.role,ti(n.role,r)),Ca(i,n.tweak_prompt??e.tweak_prompt??``),Sa(i,s,a)}else await Hi(i,s,e,t),Sa(i,s,a)}catch{r.disabled=!1,r.textContent=o}return}let c=r.dataset.prepFeedback===`next`?1:-1;zt.set(i,Math.max(0,Math.min(s+c,o-1))),_.querySelector(`.prep-analysis`)?.replaceWith(Q(Z(M[0],{analysis:a})))});function Sa(e,t,n){let r=n.feedback_items.filter((e,n)=>n!==t),i=Math.min(t,Math.max(r.length-1,0)),a={...n,feedback_items:r,verdict:r.length===0?`ready_to_apply`:n.verdict};zt.set(e,i),N.set(e,a),_.querySelector(`.prep-analysis`)?.replaceWith(Q(Z(M[0],{analysis:a})))}function Ca(e,t){let n=String(t||``).trim();if(!n)return;let r=Bt.get(e)?.trim()??``,i=r?`${r}\n\n${n}`:n;Bt.set(e,i);let a=_.querySelector(`[data-prep-resume-tweaks="${e}"]`);a&&(a.value=i,a.focus())}document.addEventListener(`keydown`,e=>{e.key===`Escape`&&!We.hidden&&Un(),e.key===`Escape`&&!o.hidden&&on(),e.key===`Escape`&&!h.hidden&&pi(),e.key===`Escape`&&!g.hidden&&hi(),e.key===`Escape`&&!ke.hidden&&oa(),e.key===`Escape`&&!Le.hidden&&da(),e.key===`Escape`&&!Qe.hidden&&Xn(),e.key===`Escape`&&!dt.hidden&&ir(),e.key===`Escape`&&!vt.hidden&&pr(),e.key===`Escape`&&!wt.hidden&&kr()}),Ue.addEventListener(`click`,Hn),Ke.addEventListener(`click`,Un),Ge.addEventListener(`click`,Un);function wa(){return Array.from(document.querySelectorAll(`.pane-toggle`))}function Ta(){return wa().some(e=>e.getAttribute(`aria-expanded`)===`true`)}function Ea(){Je.textContent=Ta()?`collapse all`:`expand all`}function Da(){document.querySelectorAll(`.pane-toggle`).forEach(e=>{e.setAttribute(`aria-expanded`,`true`),e.querySelector(`.chevron`).textContent=`v`,e.parentElement.querySelector(`.pane-body`).hidden=!1})}function Oa(){document.querySelectorAll(`.job[open]`).forEach(e=>{e.open=!1}),document.querySelectorAll(`.pane-toggle`).forEach(e=>{e.setAttribute(`aria-expanded`,`false`),e.querySelector(`.chevron`).textContent=`>`,e.parentElement.querySelector(`.pane-body`).hidden=!0})}Je.addEventListener(`click`,()=>{Ta()?Oa():Da(),Ea()}),Ye.addEventListener(`click`,()=>{Lt=!Lt,Ye.textContent=Lt?`show empty`:`hide empty`,E&&On(E.statuses)}),Ze.addEventListener(`click`,Yn),$e.addEventListener(`click`,Xn),ut.addEventListener(`click`,rr),ft.addEventListener(`click`,ir),_t.addEventListener(`click`,fr),yt.addEventListener(`click`,pr),Ve.addEventListener(`click`,Or),Tt.addEventListener(`click`,kr),Et.addEventListener(`submit`,e=>{e.preventDefault(),Mr(Et).catch(()=>{w.textContent=`could not add company.`})}),Dt.addEventListener(`submit`,e=>{e.preventDefault(),Lr(Dt).catch(()=>{jt.textContent=`could not add role.`})}),T.addEventListener(`submit`,e=>{let t=e.target.closest(`[data-company-link-form]`);t&&(e.preventDefault(),Nr(t).catch(()=>{w.textContent=`could not add link.`}))}),T.addEventListener(`input`,e=>{let t=e.target.closest(`[data-company-notes]`);t&&Br(t.dataset.companyNotes)}),T.addEventListener(`change`,e=>{let t=e.target.closest(`[data-company-tier]`);if(!t)return;let n=t.closest(`.company-panel`);n&&Hr(n,t.value),window.clearTimeout(nn.get(t.dataset.companyTier)),Vr(t.dataset.companyTier).catch(()=>{zr(`could not save company.`)})}),T.addEventListener(`click`,e=>{let t=e.target.closest(`[data-delete-company]`);if(t){let e=Rr(t.dataset.deleteCompany),n=e?.name?W(e.name):`this company`;if(!window.confirm(`Deactivate ${n}? It will be hidden from company counts and skipped during scans.`))return;t.disabled=!0,Fr(t.dataset.deleteCompany).catch(()=>{w.textContent=`could not deactivate company.`,t.disabled=!1});return}let n=e.target.closest(`[data-delete-career-page]`);if(!n)return;let r=n.closest(`.company-link-row`)?.querySelector(`.company-link-text`)?.textContent?.trim();window.confirm(`Delete ${r||`this career link`}?`)&&(n.disabled=!0,Pr(n.dataset.deleteCareerPage).catch(()=>{w.textContent=`could not delete link.`,n.disabled=!1}))}),et.addEventListener(`change`,e=>{let t=e.target.closest(`input[type="checkbox"], select, input[data-setting-text]`);t&&hr(t)}),et.addEventListener(`submit`,async e=>{e.preventDefault();let t=et.querySelector(`button[type="submit"]`),n=et.querySelectorAll(`input[type="checkbox"][name], select[name], input[data-setting-text][name]`),r={};n.forEach(e=>{let t=e.name;t&&(r[t]=e.type===`checkbox`?e.checked:e.value)}),t.disabled=!0,t.textContent=`saving...`;try{S.textContent=`saving settings...`;let e=await fetch(`/api/config`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(r)});if(!e.ok)throw Error(`Config update failed`);q(await e.json(),`settings saved.`)}catch{S.textContent=`could not save settings.`,S.classList.remove(`is-empty`)}finally{t.disabled=!1,t.textContent=`save settings`}}),at.addEventListener(`input`,()=>{C.disabled=!at.value.trim()}),st.addEventListener(`click`,_r),C.addEventListener(`click`,vr),lt.addEventListener(`click`,gr),Ct.addEventListener(`click`,xr);function ka(){if(window.location.hash===`#autoprep-interested`){da({clearHash:!1}),aa();return}if(window.location.hash===`#prepped-roles`){oa({clearHash:!1}),ua();return}oa({clearHash:!1}),da({clearHash:!1})}window.addEventListener(`popstate`,ka),br(),[`#autoprep-interested`,`#prepped-roles`].includes(window.location.hash)&&ka(),Jr({applyDefaultCollapsed:!0}).catch(()=>{gn(null,`could not load resume.`),vn([],`could not load cover letter examples.`),Cn()}),Wr().then(()=>{Gr()}).catch(()=>{x.textContent=`could not load scan status`});