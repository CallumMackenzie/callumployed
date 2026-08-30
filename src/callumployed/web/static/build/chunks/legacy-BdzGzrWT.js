import{t as e}from"./preload-helper-Czpn1I53.js";var{sankey:t,sankeyLinkHorizontal:n}=await e(async()=>{let{sankey:e,sankeyLinkHorizontal:t}=await import(`/assets/d3-sankey.js`);return{sankey:e,sankeyLinkHorizontal:t}},[]),r=document.querySelector(`#stats`),i=document.querySelector(`#status-list`),a=document.querySelector(`#search-toggle`),o=document.querySelector(`#search-dialog`),s=document.querySelector(`#search-backdrop`),c=document.querySelector(`#search-form`),l=document.querySelector(`#search-input`),u=document.querySelector(`#close-search`),d=document.querySelector(`#materials-panel`),ee=document.querySelector(`#materials-toggle`),te=document.querySelector(`#materials-body`),f=document.querySelector(`#materials-summary`),ne=document.querySelector(`#materials-required-warning`),p=document.querySelector(`#resume-meta`),m=document.querySelector(`#resume-upload`),h=document.querySelector(`#resume-upload-button`),re=document.querySelector(`#resume-resource-meta`),ie=document.querySelector(`#resume-resource-upload`),ae=document.querySelector(`#resume-resource-upload-button`),oe=document.querySelector(`#resume-resource-list`),se=document.querySelector(`#cover-letter-meta`),ce=document.querySelector(`#cover-letter-upload`),le=document.querySelector(`#cover-letter-upload-button`),ue=document.querySelector(`#cover-letter-list`),de=document.querySelector(`#experience-note-meta`),fe=document.querySelector(`#experience-note-upload`),pe=document.querySelector(`#experience-note-upload-button`),me=document.querySelector(`#experience-note-list`);document.querySelector(`#material-index-button`);var he=document.querySelector(`#material-index-warning`),ge=document.querySelector(`#material-index-status`),_e=document.querySelector(`#review-discovered`),ve=document.querySelector(`#prep-interested`),g=document.querySelector(`#review-view`),ye=document.querySelector(`#review-heading`),be=document.querySelector(`#review-progress`),xe=document.querySelector(`#review-card`),Se=document.querySelector(`#close-review`),_=document.querySelector(`#prep-view`),Ce=document.querySelector(`#prep-heading`),we=document.querySelector(`#prep-progress`),v=document.querySelector(`#prep-card`),Te=document.querySelector(`#close-prep`),Ee=document.querySelector(`#prepped-roles`),De=document.querySelector(`#prepped-view`),Oe=document.querySelector(`#close-prepped`),ke=document.querySelector(`#prepped-summary`),Ae=document.querySelector(`#regenerate-all-cover-letters`),je=document.querySelector(`#prepped-bulk-status`),Me=document.querySelector(`#prepped-list`),y=document.querySelector(`#prepped-detail`),b=document.querySelector(`#scan-all-button`),Ne=document.querySelector(`#manage-companies-button`),x=document.querySelector(`#scan-status-bar`),S=document.querySelector(`#scan-status-text`),Pe=document.querySelector(`#scan-last-time`),Fe=document.querySelector(`#scan-failures-open`),Ie=document.querySelector(`#scan-failures-dialog`),Le=document.querySelector(`#scan-failures-backdrop`),Re=document.querySelector(`#scan-failures-close`),ze=document.querySelector(`#scan-failures-list`),Be=document.querySelector(`#toggle-all`),Ve=document.querySelector(`#collapse-empty`),He=document.querySelector(`#toolbar-summary`),Ue=document.querySelector(`#settings-open`),We=document.querySelector(`#settings-view`),Ge=document.querySelector(`#settings-close`),C=document.querySelector(`#settings-status`),Ke=document.querySelector(`#settings-form`),qe=document.querySelector(`#settings-profile-options`),Je=document.querySelector(`#settings-autoprep-options`),Ye=document.querySelector(`#settings-options`),Xe=document.querySelector(`#central-store-summary`),Ze=document.querySelector(`#central-store-sync-summary`),Qe=document.querySelector(`#central-api-url-input`),$e=document.querySelector(`#central-passkey-input`),et=document.querySelector(`#central-save-button`),tt=document.querySelector(`#central-sync-button`),nt=document.querySelector(`#recommendation-history-summary`),rt=document.querySelector(`#clear-recommendation-history`),it=document.querySelector(`#metrics-open-button`),at=document.querySelector(`#metrics-view`),ot=document.querySelector(`#metrics-close`),st=document.querySelector(`#metrics-status`),ct=document.querySelector(`#metrics-overview`),lt=document.querySelector(`#metrics-sections`),ut=document.querySelector(`#metrics-scan-list`),dt=document.querySelector(`#sankey-open-button`),ft=document.querySelector(`#sankey-view`),pt=document.querySelector(`#sankey-close`),mt=document.querySelector(`#sankey-status`),ht=document.querySelector(`#sankey-canvas`),gt=document.querySelector(`#sankey-path-list`),_t=document.querySelector(`#app-update-button`),vt=document.querySelector(`#companies-view`),yt=document.querySelector(`#companies-close`),w=document.querySelector(`#companies-status`),bt=document.querySelector(`#company-create-form`),T=document.querySelector(`#companies-list`),xt=document.querySelector(`#role-add-form`),St=document.querySelector(`#role-url-input`),Ct=document.querySelector(`#role-company-input`),wt=document.querySelector(`#role-company-options`),Tt=document.querySelector(`#role-add-status`),Et=3,Dt=1200,Ot=new Set([`applied`,`OA`,`interview`,`rejected`,`offer`]),kt=new Map([[`discovered`,`#4f6472`],[`interested`,`#00897b`],[`disinterested`,`#626970`],[`applied`,`#2257ad`],[`oa`,`#b36b00`],[`interview`,`#5f2bd8`],[`rejected`,`#b93d2d`],[`offer`,`#137347`],[`closed`,`#53606b`],[`archived`,`#765b4a`]]),At=/^(?:about (?:the )?(?:role|team|job)|about this role|job description|job responsibilities|minimum qualifications|preferred qualifications|qualifications|requirements|responsibilities|what to expect|what (?:you'll|you’ll|you will) (?:bring|do)|what'?s in it for you|who you are|your objectives|your skills & talents):?$/i,jt=!0,E=null,Mt=null,D=[],O=[],k=[],Nt=null,A=[],j=[],M=new Map,Pt=new Map,N=new Map,Ft=new Map,P=new Map,It=new Map,Lt=new Map,Rt=new Map,F=[],I=null,zt=null,Bt=!1,L=``,R=null,Vt=new Set,Ht=new Set,Ut=new Map,z=new Set,Wt=new Set,B=new Map,Gt=new Map,Kt=new Set,qt=new Set,V=new Set,Jt=new Set,Yt=new Set,Xt=new Set,H=new Map,U=new Map,Zt=new Map,Qt=new Map,$t=new Set,en=!1,tn=0,nn=null,rn=!1,an=null,on=null,sn=null,cn=null,W=null,ln=[],un=new Map;function dn(){return E?.query?.trim()??``}function fn(){let e=!!dn();a.classList.toggle(`search-active`,e),a.setAttribute(`aria-label`,e?`clear search`:`search jobs`)}function pn(){l.value=dn(),o.hidden=!1,c.hidden=!1,l.focus(),l.select()}function mn(){o.hidden=!0,c.hidden=!0,a.focus()}function hn(e){return e?new Intl.DateTimeFormat(void 0,{month:`short`,day:`numeric`,hour:`numeric`,minute:`2-digit`}).format(new Date(e)).toLocaleLowerCase():``}function G(e){return e?new Intl.DateTimeFormat(void 0,{month:`short`,day:`numeric`,hour:`numeric`,minute:`2-digit`}).format(new Date(e)).replace(`, `,` `).toLocaleLowerCase():``}function K(e){return String(e??``).replaceAll(`&`,`&amp;`).replaceAll(`<`,`&lt;`).replaceAll(`>`,`&gt;`).replaceAll(`"`,`&quot;`).replaceAll(`'`,`&#039;`)}function q(e){return String(e??``).toLocaleLowerCase()}function J(e){return K(q(e))}function gn(e){try{let t=new URL(String(e||``));return[`http:`,`https:`].includes(t.protocol)?t.href:``}catch{return``}}function _n(e){return e}function vn(e=v){e.querySelectorAll(`[data-prep-resume-latex], [data-prep-cover-letter-latex]`).forEach(_n)}function yn(){return`
    <svg class="role-link-icon" viewBox="0 0 24 24" aria-hidden="true">
      <path d="M7 17 17 7"></path>
      <path d="M8 7h9v9"></path>
    </svg>
  `}function bn(){return`
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M12 5v14"></path>
      <path d="M5 12h14"></path>
    </svg>
  `}function xn(){return`
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M3 6h18"></path>
      <path d="M8 6V4h8v2"></path>
      <path d="m19 6-1 14H6L5 6"></path>
      <path d="M10 11v5"></path>
      <path d="M14 11v5"></path>
    </svg>
  `}function Sn(e,t,n){let r=`<span class="role-title-text">${J(e)}</span>`;return t?`<a class="${n}" href="${K(t)}" target="_blank" rel="noreferrer">${r}${yn()}</a>`:`<span class="${n}">${r}</span>`}function Cn(e){r.innerHTML=[[`companies`,e.companies_total],[`jobs`,e.jobs_total],[`applications`,e.applications_total]].map(([e,t])=>`<dl class="stat"><dt>${J(e)}</dt><dd>${t}</dd></dl>`).join(``)}function wn(e=E){if(!e){He.innerHTML=``;return}let t=t=>e.statuses.find(e=>e.key===t)?.count??0;He.innerHTML=[[`discovered`,t(`discovered`)],[`interested`,t(`interested`)],[`applied`,e.stats?.applications_total??0],[`total`,e.stats?.jobs_total??0]].map(([e,t])=>`
        <dl>
          <dt>${J(e)}</dt>
          <dd>${t}</dd>
        </dl>
      `).join(``)}function Tn(e,t=``){if(Mt=e,h.textContent=e?`replace`:`upload`,t){p.textContent=t;return}if(!e){p.textContent=`no resume uploaded`;return}let n=G(e.updated_at),r=Pn(e.content_bytes);p.textContent=[q(e.filename),r,n].filter(Boolean).join(` | `)}function En(e,t,n,{binary:r=!1}={}){let i=r?e.filename:e.id;return`
    <li class="material-source-item" title="${J(e.filename)}">
      <div class="material-source-copy">
        <span>${J(e.filename)}</span>
        <small>${K(n)}</small>
      </div>
      <div class="material-source-actions">
        <button type="button" class="material-source-view" data-material-view="${K(t)}" data-material-id="${K(i)}" data-material-binary="${r}">preview</button>
        <button type="button" class="material-source-remove" data-material-remove="${K(t)}" data-material-id="${K(i)}" data-material-name="${J(e.filename)}">remove</button>
      </div>
      <div class="material-source-preview" data-material-preview-body hidden></div>
    </li>`}function Dn(e,t=``){O=Array.isArray(e)?e:[],le.textContent=O.length>0?`add`:`upload`,se.textContent=t||(O.length===0?`no examples uploaded`:`${O.length} ${O.length===1?`example`:`examples`} stored`),ue.innerHTML=O.map(e=>En(e,`cover-letter-examples`,Pn(e.content_bytes))).join(``)}function On(e,t=``){k=Array.isArray(e)?e:[],pe.textContent=k.length>0?`add`:`upload`,de.textContent=t||(k.length===0?`no notes uploaded`:`${k.length} ${k.length===1?`note`:`notes`} stored`),me.innerHTML=k.map(e=>En(e,`experience-notes`,Pn(e.content_bytes))).join(``)}function kn(e,t=``){Nt=e??null;let n=Nt?.status??`missing`,r=n!==`ready`;if(k.length,he.hidden=!r,he.textContent=t||Nt?.warning||``,t)ge.textContent=t;else if(n===`ready`){let e=Number(Nt?.document_count??0),t=Number(Nt?.skipped_source_count??0),n=G(Nt?.generated_at);ge.innerHTML=[`${e} indexed ${e===1?`page`:`pages`}`,t?`${t} unreadable upload skipped`:``,n].filter(Boolean).map(e=>`<button type="button" class="material-index-link" data-open-material-index title="Reveal the application material index in Finder">${J(e)}</button>`).join(`<span aria-hidden="true"> | </span>`)}else ge.textContent=n===`stale`?`index out of date`:`not indexed`}function An(e,t=``){D=Array.isArray(e)?e:[],ae.textContent=D.length>0?`add`:`upload`,re.textContent=t||(D.length===0?`no resources uploaded`:`${D.length} ${D.length===1?`resource`:`resources`} stored`),oe.innerHTML=D.map(e=>En(e,`resume-resources`,Pn(e.bytes),{binary:!0})).join(``)}function jn(e,t={}){tn+=1,document.querySelectorAll(`[data-preview-blob-url]`).forEach(e=>{URL.revokeObjectURL(e.dataset.previewBlobUrl)}),Tn(e?.master_resume??null),An(e?.resume_resources??[]),Dn(e?.cover_letter_examples??[]),On(e?.experience_notes??[]),kn(e?.material_index??null),Mn(e?.ui),(!en||t.applyDefaultCollapsed)&&(Nn(!!e?.ui?.default_collapsed),en=!0)}function Mn(e=null){let t=Mt?`resume ready`:`no resume`,n=D.length===0?`no resources`:`${D.length} ${D.length===1?`resource`:`resources`}`,r=O.length,i=r===0?`no cover letters`:`${r} cover ${r===1?`letter`:`letters`}`,a=k.length,o=a===0?`no notes`:`${a} experience ${a===1?`note`:`notes`}`;ne.hidden=!(typeof e?.has_missing_required_materials==`boolean`?e.has_missing_required_materials:!Mt||r===0||a===0),f.textContent=`${t} | ${n} | ${i} | ${o}`}function Nn(e){d.classList.toggle(`collapsed`,e),ee.setAttribute(`aria-expanded`,String(!e)),ee.querySelector(`.materials-chevron`).textContent=e?`>`:`v`,te.hidden=e}function Pn(e){return Number.isFinite(e)?e<1024?`${e} b`:`${Math.round(e/1024)} kb`:``}async function Fn(e){let t=await fetch(e,{cache:`no-store`});if(!t.ok)throw Error(`Preview unavailable`);let n=await t.arrayBuffer();if(new TextDecoder(`ascii`).decode(n.slice(0,5))!==`%PDF-`)throw Error(`The selected file is not a readable PDF.`);return URL.createObjectURL(new Blob([n],{type:`application/pdf`}))}async function In(e){let t=e.closest(`.material-source-item`)?.querySelector(`[data-material-preview-body]`);if(!t)return;if(t.dataset.loaded===`true`){t.hidden=!t.hidden,e.textContent=t.hidden?`preview`:`hide`;return}e.disabled=!0,e.textContent=`loading...`;let n=e.dataset.materialView,r=e.dataset.materialId,i=tn,a=`/api/${encodeURIComponent(n)}/${encodeURIComponent(r)}`;try{if(e.dataset.materialBinary===`true`){let e=await Fn(a);if(!t.isConnected||tn!==i){URL.revokeObjectURL(e);return}t.dataset.previewBlobUrl=e,t.innerHTML=`<iframe title="${J(r)} preview"></iframe>`,t.querySelector(`iframe`).src=e}else{let e=await fetch(a);if(!e.ok)throw Error(`Preview unavailable`);let n=await e.json(),r=document.createElement(`pre`);r.textContent=n.content||`This source is empty.`,t.replaceChildren(r)}t.dataset.loaded=`true`,t.hidden=!1,e.textContent=`hide`}catch(n){t.textContent=n instanceof Error?n.message:`Preview unavailable`,t.hidden=!1,e.textContent=`preview`}finally{e.disabled=!1}}async function Ln(e){let t=e.dataset.materialRemove,n=e.dataset.materialId;if(e.dataset.confirmRemove!==`true`){e.dataset.confirmRemove=`true`,e.textContent=`confirm remove`,e.classList.add(`danger`),window.setTimeout(()=>{!e.isConnected||e.disabled||(delete e.dataset.confirmRemove,e.textContent=`remove`,e.classList.remove(`danger`))},6e3);return}e.disabled=!0,e.textContent=`removing...`;try{let e=await fetch(`/api/${encodeURIComponent(t)}/${encodeURIComponent(n)}`,{method:`DELETE`}),r=await e.json();if(!e.ok)throw Error(r.error||`Remove failed`);jn(r)}catch(t){e.disabled=!1,delete e.dataset.confirmRemove,e.classList.remove(`danger`),e.textContent=`remove`,window.alert(t instanceof Error?t.message:`Remove failed`)}}function Rn(e){i.innerHTML=e.map(e=>{let t=e.jobs.map(t=>zn(t,e.key)).join(``);return`
        <section class="status-pane ${e.count===0?`empty`:``} ${jt?`hidden-empty`:``}" id="status-${K(e.key)}" data-bucket="${K(e.key)}">
          <button class="pane-toggle" type="button" aria-expanded="false">
            <span class="chevron">></span>
            <span class="pane-title">${J(e.label)}</span>
            <span class="count">${e.count}</span>
          </button>
          <div class="pane-body" hidden>
            ${t?`<div class="jobs">${t}</div>`:`<p class="empty-copy">no jobs in this status.</p>`}
          </div>
        </section>
      `}).join(``)}function zn(e,t){return`
    <details class="job" data-role-id="${K(e.id)}">
      <summary class="job-summary">
        <span class="job-chevron">></span>
        <span class="job-identity">
          <span class="job-company">[${J(e.company_name)}]</span>
          ${Sn(e.title,e.role_url,`job-title`)}
          ${t===`interested`&&e.prep_started?Hn():``}
          ${t===`closed`&&e.updated_in_latest_scan?Bn():``}
          ${[`discovered`,`interested`].includes(t)&&e.missing_from_latest_scan?Vn():``}
        </span>
      </summary>
      <div class="job-detail">
        ${t===`discovered`?Un(e):``}
        ${t===`interested`?Wn(e):``}
        ${t===`disinterested`?Gn(e):``}
        ${t===`applied`?Kn(e):``}
        ${t===`OA`?qn(e):``}
        ${t===`interview`?Jn(e):``}
        ${t===`closed`?Yn(e):``}
        <dl>
          ${e.location?`<div>
                  <dt>location</dt>
                  <dd>${J(e.location)}</dd>
                </div>`:``}
          <div>
            <dt>updated</dt>
            <dd>${hn(e.updated_at)}</dd>
          </div>
        </dl>
      </div>
    </details>
  `}function Bn(){return`<span class="latest-scan-dot" title="updated in latest scan" aria-label="updated in latest scan"></span>`}function Vn(){return`<span class="missing-latest-scan-dot" title="not seen in latest scan" aria-label="not seen in latest scan"></span>`}function Hn(){return`<span class="prep-started-dot" title="application materials started" aria-label="application materials started"></span>`}function Un(e){return`
    <div class="job-actions job-actions-nowrap" aria-label="discovered role actions">
      <button class="job-action success" type="button" data-review-role-id="${e.id}">view</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="interested">interested</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="disinterested">disinterested</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="closed">closed</button>
    </div>
  `}function Wn(e){return`
    <div class="job-actions" aria-label="interested role actions">
      <button class="job-action success" type="button" data-prep-role-id="${e.id}">prep</button>
      <button class="job-action success" type="button" data-autoprep-role-id="${e.id}">autoprep</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="applied">applied</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="disinterested">disinterested</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="closed">closed</button>
    </div>
  `}function Gn(e){return`
    <div class="job-actions" aria-label="disinterested role actions">
      <button class="job-action success" type="button" data-role-id="${e.id}" data-status="interested">interested</button>
    </div>
  `}function Kn(e){return`
    <div class="job-actions job-actions-nowrap" aria-label="applied role actions">
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="OA">oa</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="interview">interview</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="rejected">rejected</button>
    </div>
  `}function qn(e){return`
    <div class="job-actions job-actions-nowrap" aria-label="oa role actions">
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="interview">interview</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="disinterested">disinterested</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="rejected">rejected</button>
    </div>
  `}function Jn(e){return`
    <div class="job-actions" aria-label="interview role actions">
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="rejected">rejected</button>
      <button class="job-action success" type="button" data-role-id="${e.id}" data-status="offer">offer</button>
    </div>
  `}function Yn(e){return`
    <div class="job-actions" aria-label="closed role actions">
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="interested">interested</button>
    </div>
  `}function Xn(e){E=e,l.value=e.query,fn(),Cn(e.stats),wn(e),Rn(e.statuses),ro(),Ti(e.statuses),Di(e.statuses)}function Zn(e){an=e??null;let t=!!e?.scanning,n=t&&!!e?.cancel_requested,r=Number(e?.completed_companies??0),i=Number(e?.total_companies??0),a=Number(e?.failed_companies??0),o=typeof e?.error==`string`?e.error.trim():``,s=Array.isArray(e?.failures)?e.failures:[];b.disabled=n,b.textContent=t?n?`cancelling...`:`cancel scan`:`scan roles`,b.classList.toggle(`danger`,t&&!n),x.hidden=!t&&!o&&s.length===0,x.classList.toggle(`scanning`,t),x.classList.toggle(`scan-error`,!t&&!!o||s.length>0),S.textContent=n?`cancelling scan...`:t?`scanning roles${i>0?` ${r}/${i}`:``}${a>0?`, ${a} failed`:``}`:s.length>0?`${s.length} recent scan ${s.length===1?`failure`:`failures`}`:o?`last scan error: ${o}`:`scan idle`,Fe&&ze&&(Fe.hidden=s.length===0,ze.innerHTML=s.slice(0,5).map(e=>{let t=e?.company_name||`unknown company`,n=e?.error||`scan failed`;return`
          <p>
            <span>${J(t)}</span>
            <span>${K(n)}</span>
          </p>
        `}).join(``),s.length===0&&$n());let c=e?.last_scan_at;Pe.textContent=c?`last scan: ${G(c)}`:`last scan: never`,rn&&!t&&li(dn()).catch(()=>{}),rn=t}function Qn(){Fe.hidden||(Ie.hidden=!1,Re.focus())}function $n(){Ie.hidden=!0}function er(e,t=``){on=e;let n=Array.isArray(e?.settings)?e.settings:[],r=n.filter(e=>e.key?.startsWith(`applicant_`)),i=n.filter(e=>e.key?.startsWith(`autoprep_`)||e.key===`application_generation_backend`),a=n.filter(e=>!e.key?.startsWith(`applicant_`)&&!e.key?.startsWith(`autoprep_`)&&e.key!==`application_generation_backend`),o=e?.central??{};C.textContent=t,C.classList.toggle(`is-empty`,!t);let s=Number(e?.recommendation_history_count??0);nt.textContent=s>0?`${s} saved ${s===1?`feedback decision`:`feedback decisions`}`:`no saved resume feedback decisions`,rt.disabled=s===0,rr(o),qe.innerHTML=r.map(e=>ir(e)).join(``),Je.innerHTML=i.map(t=>ir(tr(t,e))).join(``)+nr(e),Ye.innerHTML=a.map(e=>ir(e)).join(``),lr(!1)}function tr(e,t){if(e.key!==`application_generation_backend`||!Array.isArray(e.options))return e;let n=t?.application_generation_runtimes??{};return{...e,options:e.options.map(e=>{let t=n?.[e.value];return!t||e.available===!1||e.disabled===!0?e:{...e,available:t.available??t.detected??!0,reason:t.reason}})}}function nr(e){let t=e?.application_generation_runtimes??e?.runtime_availability??e?.runtimes??{},n=[[`hermes`,t?.hermes??t?.Hermes],[`openclaw`,t?.openclaw??t?.OpenClaw]];return n.some(([,e])=>e&&typeof e==`object`)?`<div class="application-runtime-statuses" aria-label="application generation runtime detection">
    ${n.map(([e,t])=>{let n=t?.available??t?.detected??!1,r=t?.reason??t?.message??(n?`Runtime detected`:`Runtime unavailable`);return`<div class="application-runtime-status" data-application-runtime="${K(e)}">
        <span><strong>${J(e===`openclaw`?`OpenClaw`:`Hermes`)}</strong> ${n?`available`:`unavailable`}</span>
        <small>${J(r)}</small>
        <button type="button" data-application-runtime-test="${K(e)}" ${n?``:`disabled`}>Test connection</button>
        <small data-application-runtime-test-status="${K(e)}" aria-live="polite"></small>
      </div>`}).join(``)}
  </div>`:``}function rr(e){let t=e?.api_url??``;Qe.value=t,$e.value=``;let n=e?.passkey_configured?`passkey saved`:`no passkey saved`;Xe.textContent=t?`${q(t)} | ${n}`:`no api url | ${n}`,Ze.textContent=`${Number(e?.companies_linked??0)} linked | ${Number(e?.companies_unlinked??0)} unlinked | ${Number(e?.companies_needs_review??0)} review | ${Number(e?.companies_failed??0)} failed`,tt.disabled=!t}function ir(e){if(e.control===`textarea`&&e.editable!==!1)return or(e);if(e.control===`text`&&e.editable!==!1)return ar(e);if(e.control===`select`&&e.editable!==!1)return sr(e);if(e.control!==`toggle`||e.editable===!1)return cr(e);let t=e.value?`checked`:``,n=e.default?`on by default`:`off by default`;return`
    <label class="setting-option">
      <span class="setting-copy">
        <span class="setting-label">${J(e.label)}</span>
        <span class="setting-description">${J(e.description)}</span>
        <span class="setting-default">${J(n)}</span>
      </span>
      <span class="setting-switch">
        <input type="checkbox" name="${K(e.key)}" ${t} />
        <span aria-hidden="true"></span>
      </span>
    </label>
  `}function ar(e){let t=e.default?`default: ${q(e.default)}`:`optional`,n=e.input_type??`text`,r=e.autocomplete??`name`;return`
    <label class="setting-option">
      <span class="setting-copy">
        <span class="setting-label">${J(e.label)}</span>
        <span class="setting-description">${J(e.description)}</span>
        <span class="setting-default">${J(t)}</span>
      </span>
      <input
        class="setting-text-input"
        data-setting-text
        name="${K(e.key)}"
        type="${K(n)}"
        value="${K(e.value??``)}"
        autocomplete="${K(r)}"
      />
    </label>
  `}function or(e){return`
    <label class="setting-option setting-option-prompt">
      <span class="setting-copy">
        <span class="setting-label">${J(e.label)}</span>
        <span class="setting-description">${J(e.description)}</span>
      </span>
      <textarea
        class="setting-prompt-input"
        data-setting-textarea
        name="${K(e.key)}"
        rows="7"
        maxlength="8000"
      >${J(e.value??``)}</textarea>
    </label>
  `}function sr(e){let t=Array.isArray(e.options)?e.options:[],n=`default: ${q(e.default)}`,r=e.key===`application_generation_backend`,i=r?`setting-select setting-select-application-backend`:`setting-select`;return`
    <label class="setting-option">
      <span class="setting-copy">
        <span class="setting-label">${J(e.label)}</span>
        <span class="setting-description">${J(e.description)}</span>
        <span class="setting-default">${J(n)}</span>
      </span>
      <select class="${i}" name="${K(e.key)}">
        ${t.map(t=>{let n=t.value===e.value?`selected`:``,i=t.available===!1||t.disabled===!0,a=r&&i?` — unavailable`:``;return`<option value="${K(t.value)}" ${n} ${i?`disabled`:``}>${J(t.label)}${J(a)}</option>`}).join(``)}
      </select>
    </label>
  `}function cr(e){let t=e.default?`on by default`:`off by default`,n=e.value?`automatic`:`off`;return`
    <div class="setting-option setting-option-readonly">
      <span class="setting-copy">
        <span class="setting-label">${J(e.label)}</span>
        <span class="setting-description">${J(e.description)}</span>
        <span class="setting-default">${J(t)}</span>
      </span>
      <span class="setting-badge">${J(n)}</span>
    </div>
  `}function lr(e){Ke.querySelectorAll(`input, select, textarea`).forEach(t=>{t.disabled=e}),et.disabled=e,tt.disabled=e||!Qe.value.trim(),_t.disabled=e}async function ur(){We.hidden=!1,document.body.classList.add(`settings-open`),Ge.focus(),on?er(on):(C.textContent=`loading settings...`,C.classList.remove(`is-empty`),Ye.innerHTML=``);try{await fr()}catch{C.textContent=`could not load settings.`}}function dr(){We.hidden=!0,document.body.classList.remove(`settings-open`),Ue.focus()}async function fr(){let e=await fetch(`/api/config`);if(!e.ok)throw Error(`Config request failed`);er(await e.json())}function pr(e){let t=e?.value;return t==null?`n/a`:e?.kind===`ratio`?Number(t).toLocaleString(void 0,{maximumFractionDigits:2,minimumFractionDigits:0}):typeof t==`number`?t.toLocaleString():q(t)}function mr(e,t=`metric-card`){return`
    <article class="${t}">
      <span>${J(e?.label)}</span>
      <strong>${K(pr(e))}</strong>
    </article>
  `}function hr(e,t=``){sn=e,st.textContent=t||(e?.updated_at?`updated ${G(e.updated_at)}`:``),st.classList.toggle(`is-empty`,!st.textContent);let n=Array.isArray(e?.overview)?e.overview:[],r=Array.isArray(e?.sections)?e.sections:[],i=Array.isArray(e?.recent_scans)?e.recent_scans:[];ct.innerHTML=n.map(e=>mr(e)).join(``),lt.innerHTML=r.map(gr).join(``),ut.innerHTML=i.length?i.map(_r).join(``):`<p class="empty-copy">no scan runs recorded.</p>`}function gr(e){let t=Array.isArray(e?.metrics)?e.metrics:[];return`
    <section class="metrics-section">
      <div class="metrics-section-heading">
        <h3>${J(e?.title)}</h3>
      </div>
      <div class="metrics-section-grid">
        ${t.map(e=>mr(e,`metric-card metric-card-compact`)).join(``)}
      </div>
    </section>
  `}function _r(e){let t=e?.scan_status??`unknown`,n=e?.started_at?G(e.started_at):`not started`,r=e?.finished_at?G(e.finished_at):`not finished`,i=e?.error?`<span>${J(e.error)}</span>`:``;return`
    <article class="metrics-scan-row">
      <div>
        <strong>${J(e?.company_name??`unknown company`)}</strong>
        <span>${J(n)} -> ${J(r)}</span>
        ${i}
      </div>
      <span class="metrics-status-pill">${J(t)}</span>
    </article>
  `}async function vr(){at.hidden=!1,document.body.classList.add(`metrics-open`),ot.focus(),sn?hr(sn):(st.textContent=`loading metrics...`,st.classList.remove(`is-empty`),ct.innerHTML=``,lt.innerHTML=``,ut.innerHTML=``);try{await br()}catch{st.textContent=`could not load metrics.`}}function yr(){at.hidden=!0,document.body.classList.remove(`metrics-open`),it.focus()}async function br(){let e=await fetch(`/api/metrics`);if(!e.ok)throw Error(`Metrics request failed`);hr(await e.json())}function xr(e,t=``){cn=e;let n=Number(e?.role_count??0),r=Array.isArray(e?.links)?e.links:[],i=Array.isArray(e?.paths)?e.paths:[];mt.textContent=t||(e?.updated_at?`${n.toLocaleString()} roles | updated ${G(e.updated_at)}`:``),mt.classList.toggle(`is-empty`,!mt.textContent),ht.innerHTML=r.length?Sr(e):`<p class="empty-copy">no role transitions recorded yet.</p>`,gt.innerHTML=i.length?i.map(Er).join(``):`<p class="empty-copy">no role paths recorded yet.</p>`}function Sr(e){let t=Array.isArray(e?.nodes)?e.nodes:[],n=Array.isArray(e?.links)?e.links:[],r=Tr(t,n),i=r.nodes,a=r.links,o=(r.flowLinks??n).map(e=>{let t=i.get(e.source),n=i.get(e.target),r=a.get(e);if(!t||!n||!r)return``;let o=r.width,s=n.x<t.x,c=Cr(e.target),l=r.priority?`0.42`:s?`0.28`:`0.34`,u=r.path??wr({isBacktrack:s,sourceX:t.x+t.width,sourceY:r.sourceY,targetX:n.x,targetY:r.targetY,width:o});return`
        <path class="${[`sankey-link`,s?`sankey-link-backtrack`:``,r.priority?`sankey-link-priority`:``].filter(Boolean).join(` `)}" d="${u}" fill="${r.path?`none`:c}" fill-opacity="${l}" stroke="${c}" style="stroke-width: ${r.path?o:1}px">
          <title>${J(t.label)} to ${J(n.label)}: ${Number(e.value??0).toLocaleString()}</title>
        </path>
      `}).join(``),s=Array.from(i.values()).map(e=>{let t=Number(e.history_count??e.current_count??0),n=Number(e.value??t),i=n>0?n.toLocaleString():`0`,a=e.x>r.width-180,o=a?e.x-8:e.x+e.width+8,s=Math.max(24,e.y-e.height/2-16),c=a?`end`:`start`,l=Cr(e.id);return`
        <g class="sankey-node" transform="translate(${e.x}, ${e.y-e.height/2})">
          <rect width="${e.width}" height="${e.height}" rx="7" fill="${l}" stroke="${l}"></rect>
        </g>
        <g class="sankey-node-label" transform="translate(${o}, ${s})">
          <text text-anchor="${c}">${J(e.label)}</text>
          <text class="sankey-node-count" y="16" text-anchor="${c}">${J(i)} roles</text>
        </g>
      `}).join(``);return`
    <svg class="sankey-svg" viewBox="0 0 ${r.width} ${r.height}" role="img" aria-label="role state transition sankey diagram">
      <g>${o}</g>
      <g>${s}</g>
    </svg>
  `}function Cr(e){return kt.get(String(e).toLowerCase())??`#4f6472`}function wr({isBacktrack:e,sourceX:t,sourceY:n,targetX:r,targetY:i,width:a}){let o=a/2,s=n-o,c=n+o,l=i-o,u=i+o;if(e){let e=Math.max(80,Math.abs(t-r)*.42);return[`M ${t} ${s}`,`C ${t-e} ${s}, ${r+e} ${l}, ${r} ${l}`,`L ${r} ${u}`,`C ${r+e} ${u}, ${t-e} ${c}, ${t} ${c}`,`Z`].join(` `)}let d=Math.max(46,(r-t)*.48);return[`M ${t} ${s}`,`C ${t+d} ${s}, ${r-d} ${l}, ${r} ${l}`,`L ${r} ${u}`,`C ${r-d} ${u}, ${t+d} ${c}, ${t} ${c}`,`Z`].join(` `)}function Tr(e,r){let i=new Map([[`discovered`,0],[`interested`,1],[`disinterested`,2],[`applied`,2],[`oa`,3],[`interview`,3],[`rejected`,4],[`closed`,4],[`archived`,4]]),a=new Map,o=new Map;r.forEach(e=>{a.set(e.target,(a.get(e.target)??0)+Number(e.value??0)),o.set(e.source,(o.get(e.source)??0)+Number(e.value??0))});let s=e.filter(e=>Number(e?.history_count??e?.current_count??0)>0||a.has(e.id)||o.has(e.id)),c=new Set(s.map(e=>e.id)),l=r.filter(e=>c.has(e.source)&&c.has(e.target)&&Number(e.value??0)>0),u=e=>i.get(String(e).toLowerCase())??0,d=l.filter(e=>u(e.target)>=u(e.source)),ee=l.filter(e=>u(e.target)<u(e.source)),te={nodes:s.map(e=>({...e,fixedValue:Math.max(0,Number(e?.history_count??e?.current_count??0))})),links:d.map(e=>({...e}))},f=t().nodeId(e=>e.id).nodeWidth(26).nodePadding(44).nodeAlign((e,t)=>Math.min(t-1,u(e.id))).extent([[92,88],[1014,634]]).iterations(32)(te),ne=new Map;f.nodes.forEach(e=>{ne.set(e.id,{...e,x:e.x0,y:e.y0+(e.y1-e.y0)/2,width:e.x1-e.x0,height:Math.max(1.5,e.y1-e.y0),value:Number(e.fixedValue??e.value??0)})});let p=new Map,m=[],h=n();f.links.forEach(e=>{let t={source:e.source.id,target:e.target.id,value:e.value};m.push(t),p.set(t,{path:h(e),width:Math.max(1.5,e.width),sourceY:e.y0,targetY:e.y1,priority:Number(e.value??0)>=20})});let re=Math.max(.6,...f.links.map(e=>Number(e.width??0)/Math.max(1,Number(e.value??0))));return ee.forEach(e=>{let t=ne.get(e.source),n=ne.get(e.target);if(!t||!n)return;let r=Math.max(1.5,Number(e.value??0)*re),i={...e};m.push(i),p.set(i,{width:r,sourceY:t.y+t.height/2-r/2,targetY:n.y+n.height/2-r/2,priority:!1})}),m.sort((e,t)=>Number(e.value??0)-Number(t.value??0)),{flowLinks:m,height:720,links:p,nodes:ne,width:1120}}function Er(e){let t=Array.isArray(e?.path)?e.path:[];return`
    <article class="sankey-path-row">
      <div>
        <strong>${J(e?.company_name??`unknown company`)} / ${J(e?.title??`untitled role`)}</strong>
        <span>${t.map(e=>J(e)).join(` -> `)}</span>
      </div>
      <span class="metrics-status-pill">${Number(e?.loops_collapsed??0).toLocaleString()} loops</span>
    </article>
  `}async function Dr(){We.hidden=!0,document.body.classList.remove(`settings-open`),ft.hidden=!1,document.body.classList.add(`sankey-open`),pt.focus(),cn?xr(cn):(mt.textContent=`loading role flow...`,mt.classList.remove(`is-empty`),ht.innerHTML=``,gt.innerHTML=``);try{await kr()}catch{mt.textContent=`could not load role flow.`}}function Or(){ft.hidden=!0,document.body.classList.remove(`sankey-open`),Ue.focus()}async function kr(){let e=await fetch(`/api/role-sankey`);if(!e.ok)throw Error(`Role sankey request failed`);xr(await e.json())}async function Ar(e){let t=e.name;if(!t)return;let n=e.type===`checkbox`?!e.checked:on?.settings?.find(e=>e.key===t)?.value,r=e.type===`checkbox`?e.checked:e.value;lr(!0),C.textContent=`saving settings...`,C.classList.remove(`is-empty`);try{let e=await fetch(`/api/config`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({[t]:r})});if(!e.ok)throw Error(`Config update failed`);er(await e.json(),`settings saved.`)}catch{e.type===`checkbox`?e.checked=n:n!==void 0&&(e.value=n),C.textContent=`could not save settings.`,lr(!1)}}async function jr(){rt.disabled=!0,C.textContent=`clearing recommendation history...`,C.classList.remove(`is-empty`);try{let e=await fetch(`/api/recommendation-history/clear`,{method:`POST`});if(!e.ok)throw Error(`Recommendation history clear failed`);let t=await e.json();er(t.config,`cleared ${t.deleted_count} saved decisions.`)}catch{C.textContent=`could not clear recommendation history.`,rt.disabled=!1}}async function Mr(){let e=Qe.value.trim();if(!e){C.textContent=`central api url is required.`,C.classList.remove(`is-empty`);return}let t={central_api_url:e},n=$e.value.trim();n&&(t.central_passkey=n),lr(!0),C.textContent=`saving central settings...`,C.classList.remove(`is-empty`);try{let e=await fetch(`/api/config`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(t)});if(!e.ok)throw Error(`Central settings update failed`);er(await e.json(),`central settings saved.`)}catch{C.textContent=`could not save central settings.`,lr(!1)}}async function Nr(){tt.disabled=!0,C.textContent=`syncing remote company ids...`,C.classList.remove(`is-empty`);try{let e=await fetch(`/api/central/resolve-companies`,{method:`POST`});if(!e.ok)throw Error(`Central company sync failed`);let t=await e.json(),n=t.result??{},r=t.pulled_companies,i=r?` remote: ${Number(r.created??0)} created, ${Number(r.linked??0)} linked, ${Number(r.existing??0)} existing.`:``;er(t.config,`company sync: ${Number(n.linked??0)} matched, ${Number(n.created??0)} created, ${Number(n.needs_review??0)} review, ${Number(n.failed??0)} failed.${i}`),t.companies&&(W=t.companies,Rr(t.companies.companies))}catch{C.textContent=`could not sync companies.`,tt.disabled=!Qe.value.trim()}}async function Pr(){let e=await fetch(`/api/central/resolve-companies`,{method:`POST`});if(!e.ok)throw Error(`Central company sync failed`);let t=await e.json();t.companies&&(W=t.companies,Rr(t.companies.companies))}async function Fr(){let e=Pr().catch(()=>{});await Promise.all([li().catch(()=>{i.innerHTML=`<p class="empty-copy">could not load jobs.</p>`}),Kr().catch(()=>{Tt.textContent=`could not load companies.`})]),await e}async function Ir(){if(window.confirm(`Update callumployed and restart the tracker?`)){lr(!0),_t.disabled=!0,C.textContent=`updating callumployed; tracker will restart shortly...`,C.classList.remove(`is-empty`);try{if(!(await fetch(`/api/app/update`,{method:`POST`})).ok)throw Error(`App update failed`);C.textContent=`update started. reconnect in a moment.`}catch{C.textContent=`could not start update.`,lr(!1)}}}function Lr(e,t=``){W=e;let n=Array.isArray(e?.companies)?e.companies:[];if(Rr(n),w.textContent=t||`${n.length} ${n.length===1?`company`:`companies`} stored`,w.classList.toggle(`is-empty`,n.length===0&&!t),n.length===0){T.innerHTML=`<p class="empty-copy">no companies yet.</p>`;return}T.innerHTML=n.map(e=>zr(e)).join(``)}function Rr(e){ln=Array.isArray(e)?e:[],wt.innerHTML=ln.map(e=>`<option value="${K(e.name)}"></option>`).join(``)}function zr(e){let t=Array.isArray(e.career_pages)?e.career_pages:[],n=G(e.updated_at),r=Br(e.prestige_tier),i=Number(e.scan_count??0),a=Number(e.discovered_role_count??0),o=i>0&&a===0?`<span class="company-discovery-status">Discovered 0 potential roles</span>`:``;return`
    <details class="company-panel ${r}" data-company-id="${e.id}">
      <summary class="company-summary">
        <span class="company-chevron">></span>
        <span class="company-summary-main">
          <span class="company-name">${J(e.name)}</span>
          <span class="company-summary-meta">${t.length} ${t.length===1?`link`:`links`}${n?` | updated ${J(n)}`:``}</span>
          ${o}
        </span>
      </summary>
      <div class="company-body">
        <div class="company-info">
          <label class="company-notes-field">
            <span>notes</span>
            <textarea data-company-notes="${e.id}" rows="3">${K(e.notes??``)}</textarea>
          </label>
          <label>
            <span>tier</span>
            <select data-company-tier="${e.id}">
              ${Vr(e.prestige_tier)}
            </select>
          </label>
          <div>
            <span>browser wait</span>
            <strong>${Number(e.browser_extra_wait_ms??0)}ms</strong>
          </div>
        </div>
        <div class="company-links">
          ${t.length>0?t.map(e=>Hr(e)).join(``):`<p class="company-empty-links">no career links yet.</p>`}
        </div>
        <section class="company-link-panel" aria-label="add career link">
          <form class="company-link-form" data-company-link-form="${e.id}">
            <input name="label" type="text" placeholder="label" aria-label="career link label" />
            <input name="url" type="url" placeholder="https://..." aria-label="career link url" required />
            <button class="company-link-add" type="submit" aria-label="add career link" title="add career link">
              ${bn()}
            </button>
          </form>
        </section>
        <div class="company-danger-row">
          <button class="company-delete-button" type="button" data-delete-company="${e.id}">
            ${xn()}
            <span>deactivate company</span>
          </button>
        </div>
      </div>
    </details>
  `}function Br(e){let t=String(e??``);return[`0`,`1`,`2`,`3`,`4`].includes(t)?`company-tier-${t}`:`company-tier-unset`}function Vr(e){let t=String(e??``);return[``,`0`,`1`,`2`,`3`,`4`].map(e=>{let n=e?`tier ${e}`:`not set`,r=e===t?` selected`:``;return`<option value="${K(e)}"${r}>${J(n)}</option>`}).join(``)}function Hr(e){let t=e.label?J(e.label):`career page`,n=K(e.url);return`
    <div class="company-link-row" data-career-page-id="${e.id}">
      <a class="company-link-url" href="${n}" target="_blank" rel="noreferrer">
        <span class="company-link-label">${t}</span>
        <span class="company-link-text">${K(e.url)}</span>
      </a>
      <button class="company-link-delete" type="button" data-delete-career-page="${e.id}" aria-label="delete ${t} link" title="delete link">
        ${xn()}
      </button>
    </div>
  `}async function Ur(){vt.hidden=!1,document.body.classList.add(`companies-open`),yt.focus(),W?Lr(W):(w.textContent=`loading companies...`,w.classList.remove(`is-empty`),T.innerHTML=``);try{await Gr()}catch{w.textContent=`could not load companies.`}}function Wr(){vt.hidden=!0,document.body.classList.remove(`companies-open`),Ne.focus()}async function Gr(e=``){let t=await fetch(`/api/companies`);if(!t.ok)throw Error(`Companies request failed`);Lr(await t.json(),e)}async function Kr(){let e=await fetch(`/api/companies`);if(!e.ok)throw Error(`Companies request failed`);Rr((await e.json()).companies)}async function qr(e){let t=new FormData(e),n={name:String(t.get(`name`)??``),career_url:String(t.get(`career_url`)??``),notes:String(t.get(`notes`)??``)};w.textContent=`adding company...`;let r=await fetch(`/api/companies`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(n)});if(!r.ok)throw Error(`Company create failed`);e.reset(),Lr(await r.json(),`company added.`),li(dn()).catch(()=>{})}async function Jr(e){let t=e.dataset.companyLinkForm;if(!t)return;let n=new FormData(e),r={label:String(n.get(`label`)??``),url:String(n.get(`url`)??``)};w.textContent=`adding link...`;let i=await fetch(`/api/companies/${encodeURIComponent(t)}/career-pages`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(r)});if(!i.ok)throw Error(`Career page create failed`);e.reset(),Lr(await i.json(),`link added.`)}async function Yr(e){w.textContent=`deleting link...`;let t=await fetch(`/api/company-career-pages/${encodeURIComponent(e)}`,{method:`DELETE`});if(!t.ok)throw Error(`Career page delete failed`);Lr(await t.json(),`link deleted.`)}async function Xr(e){w.textContent=`deactivating company...`;let t=await fetch(`/api/companies/${encodeURIComponent(e)}`,{method:`DELETE`});if(!t.ok)throw Error(`Company deactivate failed`);Lr(await t.json(),`company deactivated.`),li(dn()).catch(()=>{})}function Zr(){let e=Ct.value.trim().toLocaleLowerCase();return ln.find(t=>t.name.toLocaleLowerCase()===e)}async function Qr(e){let t=Zr();if(!t?.id){Tt.textContent=`pick a saved company.`;return}let n=new FormData(e),r={company_id:t.id,role_url:String(n.get(`role_url`)??``)};Tt.textContent=`adding role...`;let i=await fetch(`/api/roles`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(r)});if(!i.ok)throw Error(`Role create failed`);let a=await i.json();a.tracker?Xn(a.tracker):await li(dn()),St.value=``;let o=a.role?.title?q(a.role.title):`role`;Tt.textContent=a.scan_error?`${o} added; scan could not finish.`:`${o} added.`}function $r(e){return(Array.isArray(W?.companies)?W.companies:[]).find(t=>String(t.id)===String(e))}function ei(e){w.textContent=e,w.classList.remove(`is-empty`)}function ti(e){window.clearTimeout(un.get(e)),un.set(e,window.setTimeout(()=>{ni(e).catch(()=>{ei(`could not save company.`)})},700))}async function ni(e){let t=T.querySelector(`[data-company-id="${CSS.escape(String(e))}"]`);if(!t)return;let n=t.querySelector(`[data-company-notes="${CSS.escape(String(e))}"]`),r=t.querySelector(`[data-company-tier="${CSS.escape(String(e))}"]`),i=$r(e),a={notes:n?.value??i?.notes??``,prestige_tier:r?.value??i?.prestige_tier??``};i&&(i.notes=a.notes,i.prestige_tier=a.prestige_tier),ri(t,a.prestige_tier),ei(`saving company...`);let o=await fetch(`/api/companies/${encodeURIComponent(e)}`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(a)});if(!o.ok)throw Error(`Company update failed`);W=await o.json(),ei(`company saved.`),ii(e)}function ri(e,t){e.classList.remove(`company-tier-unset`,`company-tier-0`,`company-tier-1`,`company-tier-2`,`company-tier-3`,`company-tier-4`),e.classList.add(Br(t))}function ii(e){let t=T.querySelector(`[data-company-id="${CSS.escape(String(e))}"]`),n=$r(e);if(!t||!n)return;let r=Array.isArray(n.career_pages)?n.career_pages:[],i=G(n.updated_at),a=t.querySelector(`.company-summary-meta`);a&&(a.textContent=`${r.length} ${r.length===1?`link`:`links`}${i?` | updated ${i}`:``}`)}async function ai(){let e=await fetch(`/api/scan/status`);if(e.status===404){b.disabled=!0,x.hidden=!0,x.classList.add(`scan-error`),S.textContent=`restart server to enable scanning`;return}if(!e.ok)throw Error(`Scan status request failed`);Zn(await e.json())}function oi(){nn===null&&(nn=window.setInterval(()=>{ai().catch(()=>{})},3e3))}async function si(){b.disabled=!0,b.textContent=`starting...`;try{let e=await fetch(`/api/scan/all`,{method:`POST`});if(e.status===404){b.disabled=!0,b.textContent=`scan roles`,x.hidden=!0,x.classList.add(`scan-error`),S.textContent=`restart server to enable scanning`;return}if(!e.ok&&e.status!==409)throw Error(`Scan start failed`);Zn(await e.json()),oi()}catch{b.disabled=!1,b.textContent=`scan roles`,x.hidden=!0,x.classList.add(`scan-error`),S.textContent=`could not start scan`}}async function ci(){b.disabled=!0,b.textContent=`cancelling...`;try{let e=await fetch(`/api/scan/cancel`,{method:`POST`});if(e.status===404){b.disabled=!0,b.textContent=`scan roles`,x.hidden=!0,x.classList.add(`scan-error`),S.textContent=`restart server to enable scanning`;return}if(!e.ok&&e.status!==409)throw Error(`Scan cancel failed`);Zn(await e.json()),oi()}catch{b.disabled=!1,b.textContent=`cancel scan`,x.hidden=!1,x.classList.add(`scan-error`),S.textContent=`could not cancel scan`}}async function li(e=``){i.innerHTML=`<p class="empty-copy">loading jobs...</p>`;let t=new URLSearchParams;e&&t.set(`q`,e);let n=await fetch(`/api/tracker?${t.toString()}`);if(!n.ok)throw Error(`Tracker request failed`);Xn(await n.json())}async function ui(e={}){let t=await fetch(`/api/application-materials`);if(!t.ok)throw Error(`Application materials request failed`);jn(await t.json(),e)}async function di(e){if(e){if(!e.name.toLowerCase().endsWith(`.tex`)){Tn(Mt,`resume must be a .tex file.`);return}h.disabled=!0,Tn(Mt,`uploading...`);try{let t=await e.text();if(!(await fetch(`/api/master-resume`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({filename:e.name,content:t})})).ok)throw Error(`Master resume upload failed`);await ui()}catch{Tn(Mt,`could not save resume.`),Mn()}finally{m.value=``,h.disabled=!1}}}async function fi(e){let t=Array.from(e??[]);if(t.length!==0){ae.disabled=!0,An(D,`uploading ${t.length} ${t.length===1?`resource`:`resources`}...`);try{for(let e of t)if(!(await fetch(`/api/resume-resources`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({filename:e.name,content_base64:await hi(e)})})).ok)throw Error(`Resume resource upload failed`);await ui()}catch{An(D,`could not save every resource.`),Mn()}finally{ie.value=``,ae.disabled=!1}}}async function pi(e){let t=Array.from(e??[]);if(t.length!==0){le.disabled=!0,Dn(O,`uploading ${t.length} ${t.length===1?`example`:`examples`}...`);try{for(let e of t){let t={filename:e.name};if([`.pdf`,`.docx`].some(t=>e.name.toLowerCase().endsWith(t))?t.content_base64=await hi(e):t.content=await e.text(),!(await fetch(`/api/cover-letter-examples`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(t)})).ok)throw Error(`Cover letter example upload failed`)}await ui()}catch{Dn(O,`could not save every example.`),Mn()}finally{ce.value=``,le.disabled=!1}}}async function mi(e){let t=Array.from(e??[]);if(t.length!==0){pe.disabled=!0,On(k,`uploading ${t.length} ${t.length===1?`note`:`notes`}...`);try{for(let e of t){let t=e.name.toLowerCase(),n={filename:e.name};if(t.endsWith(`.pdf`)||t.endsWith(`.docx`)?n.content_base64=await hi(e):n.content=await e.text(),!(await fetch(`/api/experience-notes`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(n)})).ok)throw Error(`Experience note upload failed`)}M.clear(),await ui()}catch{On(k,`could not save every note.`),Mn()}finally{fe.value=``,pe.disabled=!1}}}function hi(e){return new Promise((t,n)=>{let r=new FileReader;r.addEventListener(`load`,()=>{let e=String(r.result??``);t(e.includes(`,`)?e.split(`,`,2)[1]:e)}),r.addEventListener(`error`,()=>n(r.error)),r.readAsDataURL(e)})}c.addEventListener(`submit`,e=>{e.preventDefault(),li(l.value.trim()),mn()}),a.addEventListener(`click`,()=>{if(dn()){li();return}pn()}),l.addEventListener(`keydown`,e=>{e.key===`Escape`&&(e.stopPropagation(),mn())}),u.addEventListener(`click`,mn),s.addEventListener(`click`,mn),h.addEventListener(`click`,()=>{m.click()}),m.addEventListener(`change`,()=>{di(m.files?.[0])}),ae.addEventListener(`click`,()=>{ie.click()}),ie.addEventListener(`change`,()=>{fi(ie.files)}),le.addEventListener(`click`,()=>{ce.click()}),ce.addEventListener(`change`,()=>{pi(ce.files)}),pe.addEventListener(`click`,()=>{fe.click()}),fe.addEventListener(`change`,()=>{mi(fe.files)}),ee.addEventListener(`click`,()=>{Nn(ee.getAttribute(`aria-expanded`)===`true`)});async function gi(e){e.disabled=!0;let t=e.textContent;e.textContent=`opening...`;try{if(!(await fetch(`/api/application-materials/index/open`,{method:`POST`})).ok)throw Error(`Could not open the application material index.`)}catch(e){he.hidden=!1,he.textContent=e instanceof Error?e.message:`Could not open the application material index.`}finally{e.disabled=!1,e.textContent=t}}te.addEventListener(`click`,e=>{let t=e.target.closest(`[data-open-material-index]`);if(t){gi(t);return}let n=e.target.closest(`[data-material-view]`);if(n){In(n);return}let r=e.target.closest(`[data-material-remove]`);r&&Ln(r)}),b.addEventListener(`click`,()=>{if(an?.scanning){ci();return}si()}),i.addEventListener(`click`,e=>{let t=e.target.closest(`[data-review-role-id]`);if(t){ki(t.dataset.reviewRoleId);return}let n=e.target.closest(`[data-prep-role-id]`);if(n){ji(n.dataset.prepRoleId);return}let r=e.target.closest(`[data-autoprep-role-id]`);if(r){Sa(r.dataset.autoprepRoleId).catch(()=>{He.textContent=`could not add that role to Autoprep. try again.`});return}let i=e.target.closest(`.job-action`);if(i){_i(i);return}let a=e.target.closest(`.pane-toggle`);if(!a)return;let o=a.parentElement.querySelector(`.pane-body`),s=a.getAttribute(`aria-expanded`)===`true`;a.setAttribute(`aria-expanded`,String(!s)),a.querySelector(`.chevron`).textContent=s?`>`:`v`,o.hidden=s,ro()});async function _i(e){let{roleId:t,status:n}=e.dataset;if(!t||!n)return;let r=e.closest(`.job-actions`),i=e.closest(`.job`);r.querySelectorAll(`button`).forEach(e=>{e.disabled=!0}),e.textContent=`updating...`;try{let e=await fetch(`/api/roles/${encodeURIComponent(t)}/status`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({status:n})});if(!e.ok)throw Error(`Status update failed`);vi((await e.json()).role,i)}catch{r.querySelectorAll(`button`).forEach(e=>{e.disabled=!1}),e.textContent=n===`disinterested`?`disinterested`:n.toLowerCase()}}function vi(e,t){if(!e||!E)return;let n=t?.closest(`.status-pane`)?.dataset.bucket??e.role_status,r=e.role_status,i=bi(e,n,r);xi(n,r),Si(n,r),wn(),Ti(E.statuses),Di(E.statuses),Ci(t,i,n,r),ro()}function yi(e){if(!e||!E)return null;let t=null;return E.statuses.forEach(n=>{let r=n.jobs.findIndex(t=>String(t.id)===String(e.id));r!==-1&&(t={...n.jobs[r],...e},n.jobs[r]=t)}),Ti(E.statuses),Di(E.statuses),t}function bi(e,t,n){let r=e;E.statuses.forEach(t=>{let n=t.jobs.findIndex(t=>String(t.id)===String(e.id));n!==-1&&(r={...t.jobs[n],...e},t.jobs.splice(n,1),t.count=t.jobs.length)});let i=E.statuses.find(e=>e.key===n);return i&&(i.jobs.unshift(r),i.count=i.jobs.length),r}function xi(e,t){E.statuses.forEach(e=>{let t=document.querySelector(`#status-${CSS.escape(e.key)}`);t?.classList.toggle(`empty`,e.count===0);let n=t?.querySelector(`.count`);n&&(n.textContent=e.count)}),[e,t].forEach(e=>{wi(document.querySelector(`#status-${CSS.escape(e)}`))})}function Si(e,t){if(!E.stats)return;let n=Ot.has(e),r=Ot.has(t);if(n===r){Cn(E.stats);return}E.stats.applications_total=Number(E.stats.applications_total??0)+(r?1:-1),Cn(E.stats)}function Ci(e,t,n,r){let i=document.querySelector(`#status-${CSS.escape(r)}`),a=i?.querySelector(`.pane-body`);if(!e||!i||!a)return;e.remove(),wi(document.querySelector(`#status-${CSS.escape(n)}`)),a.hidden=!1;let o=i.querySelector(`.pane-toggle`);o?.setAttribute(`aria-expanded`,`true`);let s=o?.querySelector(`.chevron`);s&&(s.textContent=`v`);let c=a.querySelector(`.jobs`);c||=(a.innerHTML=`<div class="jobs"></div>`,a.querySelector(`.jobs`)),c.insertAdjacentHTML(`afterbegin`,zn(t,r)),wi(i)}function wi(e){if(!e)return;let t=e.querySelector(`.pane-body`);if(!t)return;let n=t.querySelector(`.jobs`),r=!!n?.querySelector(`.job`),i=t.querySelector(`.empty-copy`);if(r){i?.remove();return}n?.remove(),i||t.insertAdjacentHTML(`beforeend`,`<p class="empty-copy">no jobs in this status.</p>`)}function Ti(e){_e.disabled=Ei(e).length===0,_e.setAttribute(`aria-label`,`review discovered`),_e.innerHTML=`<span class="review-discovered-label">review discovered</span>`}function Ei(e=E?.statuses??[]){return e.find(e=>e.key===`discovered`)?.jobs??[]}function Di(e){ve.disabled=Oi(e).length===0,ve.setAttribute(`aria-label`,`prep interested`),ve.innerHTML=`<span class="review-discovered-label">prep interested</span>`}function Oi(e=E?.statuses??[]){return e.find(e=>e.key===`interested`)?.jobs??[]}function ki(e=null){let t=[...Ei()],n=e==null?null:String(e);if(n){let e=t.findIndex(e=>String(e.id)===n);if(e>0){let[n]=t.splice(e,1);t.unshift(n)}}A=t,g.hidden=!1,document.body.classList.add(`review-open`),Ni()}function Ai(){g.hidden=!0,document.body.classList.remove(`review-open`),A=[]}function ji(e=null){let t=[...Oi()].sort((e,t)=>Number(!!t.prep_started)-Number(!!e.prep_started)),n=e==null?null:String(e);if(n){let e=t.findIndex(e=>String(e.id)===n);if(e>0){let[n]=t.splice(e,1);t.unshift(n)}}j=t,_.hidden=!1,document.body.classList.add(`prep-open`),Yi()}function Mi(){_.hidden=!0,document.body.classList.remove(`prep-open`),j=[]}function Ni(e=``){let t=A[0],n=A.length,r=t?Pi(t):``;if(ye.textContent=n>0?`review queue`:`review complete`,be.textContent=n>0?`${n} discovered ${n===1?`role`:`roles`} in queue`:``,g.querySelectorAll(`.review-action`).forEach(e=>{e.disabled=n===0}),!t){xe.innerHTML=`
      <div class="review-empty">
        <h3>no discovered jobs left.</h3>
        <p>everything in this queue has been handled or moved out of discovered.</p>
      </div>
    `;return}xe.innerHTML=`
    ${e?`<p class="review-message">${K(e)}</p>`:``}
    ${r?`<p class="review-message review-message-warning">${K(r)}</p>`:``}
    <div class="review-title-row">
      <p class="review-company">${J(t.company_name)}</p>
      ${Sn(t.title,t.role_url,`review-role-title`)}
    </div>
    <dl class="review-details review-primary-details">
      ${Y(`location`,t.location,!1,`review-location-detail`)}
      ${Y(`first`,G(t.first_seen_at))}
      ${Y(`last`,G(t.last_seen_at))}
    </dl>
    ${Fi(t.description)}
    <dl class="review-details review-technical-details">
      ${Y(`notes`,t.notes,!1,`review-wide-detail`)}
      ${Y(`company id`,t.company_id)}
      ${Y(`role id`,t.id)}
      ${Y(`status`,t.role_status)}
      ${Y(`posting id`,t.posting_id)}
      ${Y(`created`,G(t.created_at))}
      ${Y(`updated`,G(t.updated_at))}
      ${Y(`url`,t.role_url,!0,`review-wide-detail`)}
    </dl>
  `}function Pi(e){let t=Number(e.review_later_count??0);return t<=Et?``:`role review has been postponed ${t} times. it is recommended to set it to disinterested.`}function Y(e,t,n=!1,r=``){if(!t)return``;let i=n?`<a href="${K(t)}" target="_blank" rel="noreferrer">${J(t)}</a>`:J(t);return`
    <div class="review-detail ${K(r)}">
      <dt>${J(e)}</dt>
      <dd>${i}</dd>
    </div>
  `}function Fi(e){return e?`
    <div class="review-detail review-description">
      <dt>description</dt>
      <dd>${Ii(e)}</dd>
    </div>
  `:``}function Ii(e){let t=Li(String(e)).replace(/\u00a0/g,` `);if(Ri(t))return zi(t);let n=t.split(/\r?\n/).map(e=>e.trim()).filter(Boolean),r=[],i=[],a=()=>{i.length!==0&&(r.push(`<ul>${i.map(e=>`<li>${e}</li>`).join(``)}</ul>`),i=[])};return n.forEach(e=>{let t=e.match(/^#{2,3}\s+(.+)$/);if(t){a(),r.push(`<h3>${J(t[1])}</h3>`);return}if(qi(e)){a(),r.push(`<h3>${J(e.replace(/:$/,``))}</h3>`);return}let n=e.match(/^[-*]\s+(.+)$/);if(n){i.push(J(n[1]));return}a(),r.push(`<p>${J(e)}</p>`)}),a(),r.join(``)}function Li(e){let t=document.createElement(`textarea`);return t.innerHTML=e,t.value}function Ri(e){return/<\/?(?:a|br|div|em|h[1-6]|li|ol|p|span|strong|ul)\b/i.test(e)}function zi(e){let t=document.createElement(`template`);t.innerHTML=e;let n=[];return Bi(t.content.childNodes,n),n.join(``)}function Bi(e,t){e.forEach(e=>{if(e.nodeType===Node.TEXT_NODE){let n=Gi(e.textContent);n&&t.push(`<p>${J(n)}</p>`);return}if(e.nodeType!==Node.ELEMENT_NODE)return;let n=e,r=n.tagName.toLowerCase();if(r===`script`||r===`style`||r===`br`)return;if(/^h[1-6]$/.test(r)){Hi(t,n.textContent);return}if(r===`ul`||r===`ol`){let e=Ui(n);e&&t.push(e);return}if(r===`p`){Vi(n,t);return}let i=Array.from(n.children).some(e=>[`DIV`,`H1`,`H2`,`H3`,`H4`,`H5`,`H6`,`OL`,`P`,`UL`].includes(e.tagName));if([`article`,`div`,`section`].includes(r)&&i){Bi(n.childNodes,t);return}let a=Array.from(n.children).filter(e=>[`UL`,`OL`].includes(e.tagName)),o=Gi(Wi(n));if(o&&(Ki(o,n)?Hi(t,o):t.push(`<p>${J(o)}</p>`)),a.length>0){a.forEach(e=>{let n=Ui(e);n&&t.push(n)});return}!o&&i&&Bi(n.childNodes,t)})}function Vi(e,t){if(!e.querySelector(`br`)){let n=Gi(Wi(e));if(!n)return;Ki(n,e)?Hi(t,n):t.push(`<p>${J(n)}</p>`);return}let n=``,r=()=>{let r=Gi(n);n=``,r&&(Ki(r,e)?Hi(t,r):t.push(`<p>${J(r)}</p>`))};e.childNodes.forEach(e=>{if(e.nodeType===Node.ELEMENT_NODE&&e.tagName.toLowerCase()===`br`){r();return}n+=` ${e.textContent??``}`}),r()}function Hi(e,t){let n=Gi(t).replace(/:$/,``);n&&e.push(`<h3>${J(n)}</h3>`)}function Ui(e){let t=Array.from(e.children).filter(e=>e.tagName===`LI`).map(e=>{let t=Gi(Wi(e)),n=Array.from(e.children).filter(e=>[`UL`,`OL`].includes(e.tagName)).map(e=>Ui(e)).filter(Boolean).join(``);return t||n?`<li>${J(t)}${n}</li>`:``}).filter(Boolean);return t.length>0?`<ul>${t.join(``)}</ul>`:``}function Wi(e){let t=e.cloneNode(!0);return t.querySelectorAll(`ul, ol`).forEach(e=>{e.remove()}),t.textContent}function Gi(e){return String(e??``).replace(/\s+/g,` `).trim()}function Ki(e,t){let n=e.replace(/:$/,``).trim();return!n||n.length>90?!1:qi(n)||/:$/.test(e)?!0:/[.!?]$/.test(n)||n.split(/\s+/).length>10?!1:t.querySelector(`strong, b, u`)?!0:qi(n)}function qi(e){return At.test(String(e).trim())}async function Ji(e){let t=A[0];if(!t)return;if(e===`later`){g.querySelectorAll(`.review-action`).forEach(e=>{e.disabled=!0});try{let e=await ya(t.id);A.shift(),yi(e),Ni(`moved out of this review pass.`)}catch{Ni(`could not postpone that role. try again.`)}finally{g.querySelectorAll(`.review-action`).forEach(e=>{e.disabled=A.length===0})}return}if(![`interested`,`disinterested`].includes(e))return;let n=g.querySelectorAll(`.review-action`);n.forEach(e=>{e.disabled=!0});try{let n=await ba(t.id,e);A.shift(),Ni(e===`interested`?`marked interested.`:`marked disinterested.`),vi(n,document.querySelector(`.job[data-role-id="${CSS.escape(String(t.id))}"]`))}catch{n.forEach(e=>{e.disabled=!1}),Ni(`could not update that role. try again.`)}}async function Yi(e=``){let t=j[0],n=j.length;if(Ce.textContent=n>0?`prep queue`:`prep complete`,we.textContent=n>0?`${n} interested ${n===1?`role`:`roles`} in queue`:``,_.querySelectorAll(`.review-action`).forEach(e=>{e.disabled=n===0}),!t){v.innerHTML=`
      <div class="review-empty">
        <h3>no interested jobs left.</h3>
        <p>everything in this queue has been prepped, moved, or postponed.</p>
      </div>
    `;return}v.innerHTML=`
    ${e?`<p class="review-message">${K(e)}</p>`:``}
    <section class="prep-role-hero" aria-label="role overview">
      <div class="review-title-row">
        <div class="prep-role-eyebrow">
          <p class="review-company">${J(t.company_name)}</p>
          <span>application workspace</span>
        </div>
        ${Sn(t.title,t.role_url,`review-role-title`)}
      </div>
      <dl class="review-details review-primary-details">
        ${Y(`location`,t.location,!1,`review-location-detail`)}
        ${Y(`last`,G(t.last_seen_at))}
        ${Y(`updated`,G(t.updated_at))}
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
      ${Xi(t)}
      ${ea(t)}
      ${Zi(t.id,t.description)}
      ${Qi(t)}
    </div>
  `,vn(),sa(t.id).then(e=>{!e||j[0]?.id!==t.id||(N.set(t.id,e),v.querySelector(`.prep-resume`)?.replaceWith(X(Xi(t,{resume:e}))),vn())}).catch(()=>{}),va(t.id).then(e=>{!e||j[0]?.id!==t.id||(P.set(t.id,e),v.querySelector(`.prep-cover-letter`)?.replaceWith(X(ea(t,{coverLetter:e}))),vn())}).catch(()=>{})}function Xi(e,t={}){let n=N.get(e.id),r=t.resume??n,i=t.tweaks??Ft.get(e.id)??``,a=`/api/roles/${encodeURIComponent(e.id)}/resume.pdf`;return t.loading?`
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
          ${r.pdf_base64?`<a class="prep-summary-action prep-cover-pdf-link" href="${K(a)}" target="_blank" rel="noreferrer">view</a>`:``}
        </div>
      </summary>
      <p class="prep-overview">${J(r.summary??`Saved resume for this role.`)}</p>
      ${ta(e)}
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
          >${K(i)}</textarea>
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
          >${K(r.latex??``)}</textarea>
        </label>
        <section class="prep-document-preview" aria-label="resume preview">
          <div class="prep-preview-heading">
            <span>document preview</span>
            <p>Updates automatically after the source is saved.</p>
          </div>
          ${r.pdf_base64?`
                <iframe class="prep-cover-pdf" title="resume PDF preview" src="${K(a)}"></iframe>
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
    `}function Zi(e,t){return`
    <details class="prep-panel prep-description-panel" id="prep-description-${e}">
      <summary class="prep-analysis-header">
        <span class="prep-accordion-icon" aria-hidden="true"></span>
        <h3>description</h3>
      </summary>
      ${Fi(t)}
    </details>
  `}function Qi(e,t={}){let n=t.messages??It.get(e.id)??[],r=!!t.loading;return`
    <details class="prep-panel prep-role-chat" id="prep-chat-${e.id}">
      <summary class="prep-analysis-header">
        <span class="prep-accordion-icon" aria-hidden="true"></span>
        <h3>chat about this role</h3>
        <span>${n.length?`${n.length} messages`:`ready`}</span>
      </summary>
      <div class="prep-role-chat-log" aria-live="polite">
        ${n.length?n.map($i).join(``):`<p class="prep-role-chat-empty">ask about fit, risks, resume emphasis, or cover letter angle.</p>`}
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
  `}function $i(e){let t=e?.role===`assistant`?`assistant`:`user`;return`
    <article class="prep-role-chat-message prep-role-chat-message-${t}">
      <span>${t}</span>
      <p>${J(e?.content??``)}</p>
    </article>
  `}function ea(e,t={}){let n=P.get(e.id),r=t.coverLetter??n,i=t.tweaks??r?.tweaks??``,a=`/api/roles/${encodeURIComponent(e.id)}/cover-letter.pdf`;return t.loading?`
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
          ${r?.pdf_base64?`<a class="prep-summary-action prep-cover-pdf-link" href="${K(a)}" target="_blank" rel="noreferrer">view</a>`:``}
        </div>
      </summary>
      ${r?`<p class="prep-overview">${J(r.summary??`cover letter generated`)}</p>`:`<p class="prep-overview">generate a LaTeX cover letter from the resume, posting, and stored examples.</p>`}
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
                >${K(i)}</textarea>
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
                >${K(r.latex??``)}</textarea>
              </label>
              <section class="prep-document-preview" aria-label="cover letter preview">
                <div class="prep-preview-heading">
                  <span>document preview</span>
                  <p>Updates automatically after the source is saved.</p>
                </div>
                ${r.pdf_base64?`
                      <iframe class="prep-cover-pdf" title="cover letter PDF preview" src="${K(a)}"></iframe>
                    `:`<p class="prep-cover-path">PDF preview unavailable.</p>`}
              </section>
            </div>
          `:``}
    </details>
  `}function ta(e,t={}){let n=M.get(e.id);if(!t.loading&&!t.error&&!t.analysis&&n)return ta(e,{analysis:n});if(!t.loading&&!t.error&&!t.analysis)return`
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
    `;let r=t.analysis,i=Array.isArray(r?.feedback_items)?r.feedback_items:[],a=r?.verdict===`ready_to_apply`?`ready to apply`:`tweak`,o=Math.min(Pt.get(e.id)??0,Math.max(i.length-1,0)),s=i[o];return`
    <section class="prep-analysis" aria-label="ai analysis">
      <div class="prep-analysis-header">
        <h3>ai analysis</h3>
        <span>${i.length} ${i.length===1?`item`:`items`}</span>
      </div>
      <p class="prep-verdict">${J(a)}</p>
      <p class="prep-overview">${J(r?.overview??`analysis unavailable`)}</p>
      ${s?`
            <article class="prep-feedback" data-feedback-index="${o}">
              <p class="prep-feedback-label">${J(s.label)}</p>
              <h4>${J(s.title)}</h4>
              <p>${J(s.detail)}</p>
              ${na(s)}
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
  `}function na(e){return e?.tweak_prompt?`
    <div class="prep-proposed-edit">
      <p class="prep-proposed-label">tweak prompt</p>
      <p>${J(e.tweak_prompt)}</p>
    </div>
  `:`
      <div class="prep-proposed-edit">
        <p class="prep-proposed-label">feedback only</p>
        <p>not enough information to turn this into a safe resume tweak.</p>
      </div>
    `}async function ra(e,t={}){if(!t.force&&M.has(e))return M.get(e);let n=await fetch(`/api/roles/${encodeURIComponent(e)}/prep-analysis`);if(!n.ok)throw Error(`Prep analysis request failed`);let r=await n.json();return r.analysis.resources=r.resources??[],M.set(e,r.analysis),r.analysis}function X(e){let t=document.createElement(`template`);return t.innerHTML=e.trim(),t.content.firstElementChild}async function ia(e){let t=j[0];if(!t)return;let n=_.querySelectorAll(`.review-action`);if(n.forEach(e=>{e.disabled=!0}),e===`later`){try{await ya(t.id),t.review_later_count=Number(t.review_later_count??0)+1,j.length>1?(j.push(j.shift()),Yi(`moved to the back of the prep queue.`)):Yi(`only one role is in the prep queue.`)}catch{Yi(`could not postpone prep. try again.`)}return}if(e===`autoprep`){try{await Sa(t.id)}catch{Yi(`could not add that role to Autoprep. try again.`)}return}if(e===`applied`)try{let e=await ba(t.id,`applied`);j.shift(),Yi(`moved to applied.`),vi(e,document.querySelector(`.job[data-role-id="${CSS.escape(String(t.id))}"]`))}catch{n.forEach(e=>{e.disabled=!1}),Yi(`could not move that role. try again.`)}}async function aa(e,t,n,r){let i=await fetch(`/api/roles/${encodeURIComponent(e)}/prep-feedback`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({feedback_index:t,feedback_item:n,comment:r})});if(!i.ok)throw Error(`Prep feedback update failed`);return i.json()}async function oa(e,t,n,r){let i=await fetch(`/api/roles/${encodeURIComponent(e)}/prep-feedback-ignore`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({feedback_index:t,feedback_item:n,comment:r})});if(!i.ok)throw Error(`Prep feedback ignore failed`);return i.json()}async function sa(e,{force:t=!1}={}){if(!t&&N.has(e))return N.get(e);let n=await fetch(`/api/roles/${encodeURIComponent(e)}/resume`);if(!n.ok)throw Error(`Resume request failed`);let r=await n.json();return r.resume&&N.set(e,r.resume),r.resume}async function ca(e,t){let n=await fetch(`/api/roles/${encodeURIComponent(e)}/resume/save`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({latex:t})});if(!n.ok)throw Error(`Resume save failed`);return n.json()}async function la(e,t,n){let r=await fetch(`/api/roles/${encodeURIComponent(e)}/resume`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({tweaks:t,previous_latex:n})});if(!r.ok)throw Error(`Resume generation failed`);return r.json()}async function ua(e,t){let n=await fetch(`/api/roles/${encodeURIComponent(e)}/chat`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({messages:t})});if(!n.ok)throw Error(`Role chat failed`);return n.json()}function da(e,t,n=Dt){let r=Lt.get(e)??{timer:null,saving:!1,version:0,latex:``};r.version+=1,r.latex=t,r.timer&&clearTimeout(r.timer),r.timer=setTimeout(()=>{r.timer=null,fa(e)},n),Lt.set(e,r)}async function fa(e){let t=Lt.get(e);if(!t||t.saving)return;t.saving=!0;let n=t.version,r=t.latex;try{let i=await ca(e,r);t.version===n&&(N.set(e,i.resume),pa(`resume`,e,i.resume))}catch{}finally{t.saving=!1,t.version!==n&&da(e,t.latex,0)}}function pa(e,t,n){if(!n?.pdf_base64)return;let r=e===`resume`?`[data-prep-resume-latex="${t}"]`:`[data-prep-cover-letter-latex="${t}"]`,i=v.querySelector(r)?.closest(`.prep-panel`),a=i?.querySelector(`.prep-cover-pdf`),o=i?.querySelector(`.prep-cover-pdf-link`),s=e===`resume`?`/api/roles/${encodeURIComponent(t)}/resume.pdf`:`/api/roles/${encodeURIComponent(t)}/cover-letter.pdf`;a&&(a.src=`${s}?v=${Date.now()}`),o&&(o.href=s)}async function ma(e,t=``,n=``){let r=await fetch(`/api/roles/${encodeURIComponent(e)}/cover-letter`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({tweaks:t,previous_latex:n})});if(!r.ok)throw Error(`Cover letter generation failed`);return r.json()}async function ha(e,t){let n=await fetch(`/api/roles/${encodeURIComponent(e)}/cover-letter/save`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({latex:t})});if(!n.ok)throw Error(`Cover letter save failed`);return n.json()}function ga(e,t,n=``,r=Dt){let i=Rt.get(e)??{timer:null,saving:!1,version:0,latex:``,tweaks:``};i.version+=1,i.latex=t,i.tweaks=n,i.timer&&clearTimeout(i.timer),i.timer=setTimeout(()=>{i.timer=null,_a(e)},r),Rt.set(e,i)}async function _a(e){let t=Rt.get(e);if(!t||t.saving)return;t.saving=!0;let n=t.version,r=t.latex,i=t.tweaks;try{let a=await ha(e,r);t.version===n&&(P.set(e,{...a.cover_letter,tweaks:i}),pa(`coverLetter`,e,a.cover_letter))}catch{}finally{t.saving=!1,t.version!==n&&ga(e,t.latex,t.tweaks,0)}}async function va(e){if(P.has(e))return P.get(e);let t=await fetch(`/api/roles/${encodeURIComponent(e)}/cover-letter`);if(!t.ok)throw Error(`Cover letter request failed`);let n=await t.json();return n.cover_letter&&P.set(e,n.cover_letter),n.cover_letter}async function ya(e){let t=await fetch(`/api/roles/${encodeURIComponent(e)}/review-later`,{method:`POST`});if(!t.ok)throw Error(`Review later update failed`);return(await t.json()).role}async function ba(e,t){let n=await fetch(`/api/roles/${encodeURIComponent(e)}/status`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({status:t})});if(!n.ok)throw Error(`Status update failed`);return(await n.json()).role}function xa(e){return`${e}-${globalThis.crypto?.randomUUID?.()??`${Date.now()}-${Math.random()}`}`}async function Sa(e){let t=Number(e);if(!Number.isInteger(t)||t<=0||Vt.has(t))return null;Vt.add(t);let n=document.querySelectorAll(`[data-autoprep-role-id="${CSS.escape(String(t))}"]`);n.forEach(e=>{e.disabled=!0,e.setAttribute(`aria-busy`,`true`),e.textContent=`queuing...`});try{let e=await fetch(`/api/autoprep/jobs`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({role_ids:[t],idempotency_key:xa(`autoprep-role-${t}`)})}),n=await e.json();if(!e.ok)throw Error(n.error||`Autoprep request failed`);let r=Array.isArray(n.jobs)?n.jobs:[],i=new Map(F.map(e=>[Number(e.role_id),e]));return r.forEach(e=>i.set(Number(e.role_id),e)),I=t,_.hidden||Mi(),await wa({seedJobs:[...i.values()]}),r}finally{Vt.delete(t),n.forEach(e=>{e.disabled=!1,e.removeAttribute(`aria-busy`),e.textContent=`autoprep`})}}function Ca(e){window.location.hash!==e&&window.history.pushState({},``,e||`${window.location.pathname}${window.location.search}`)}async function wa({seedJobs:e=null}={}){De.hidden=!1,document.body.classList.add(`prepped-open`),Ca(`#prepped-roles`),e?(F=e,I=I??F[0]?.role_id??null,Q()):F.length===0&&(ke.textContent=`loading prepared roles...`),await Ea(),Da()}function Ta({clearHash:e=!0}={}){De.hidden=!0,document.body.classList.remove(`prepped-open`),Oa(),z.clear(),Wt.clear(),U.forEach(e=>URL.revokeObjectURL(e)),U.clear(),Zt.clear(),Qt.clear(),e&&window.location.hash===`#prepped-roles`&&Ca(``)}window.addEventListener(`pagehide`,()=>{document.querySelectorAll(`[data-preview-blob-url]`).forEach(e=>{URL.revokeObjectURL(e.dataset.previewBlobUrl)}),U.forEach(e=>URL.revokeObjectURL(e)),U.clear(),Zt.clear()});async function Ea(){try{let e=await fetch(`/api/autoprep/jobs`);if(!e.ok)throw Error(`Prepped roles request failed`);let t=await e.json();F=t.jobs??[];let n=t.bulk_cover_letter_regeneration;if(n){let e=Array.isArray(n.jobs)?n.jobs:[];R={idempotencyKey:n.idempotency_key,roleIds:e.map(e=>Number(e.role_id)),jobs:e,skipped:Array.isArray(n.skipped)?n.skipped:[]}}F.some(e=>Number(e.role_id)===Number(I))||(I=F[0]?.role_id??null),Q()}catch{ke.textContent=`could not refresh preparation progress.`}}function Da(){Oa(),F.some(ka)&&(zt=window.setInterval(Ea,2e3))}function Oa(){zt!==null&&window.clearInterval(zt),zt=null}function ka(e){return[`queued`,`generating_resume_tweaks`,`regenerating_resume`,`generating_cover_letter`].includes(e.overall_status)}function Aa(e){return[e.resume_status,e.cover_letter_status].some(e=>[`failed`,`interrupted`].includes(e))}function ja(e){return e.cover_letter_status===`generating`||e.overall_status===`generating_cover_letter`}function Ma(e){return ja(e)||e.resume_status===`generating_tweaks`||e.resume_status===`regenerating`||e.overall_status===`generating_resume_tweaks`||e.overall_status===`regenerating_resume`}function Na(e){return e.worker_state===`queued`||e.overall_status===`queued`}function Pa(e){return{queued:`Queued`,generating_resume_tweaks:`Generating resume tweaks`,regenerating_resume:`Regenerating resume`,generating_cover_letter:`Generating cover letter`,partially_complete:`Partially complete`,ready:`Ready`,failed:`Failed`,interrupted:`Interrupted`,generating_tweaks:`Generating tweaks`,regenerating:`Regenerating`,generating:`Generating`}[e]??q(e)}function Fa(e,t){let n=t===`cover-letter`?`cover_letter`:`resume`;return`${e.updated_at||``}:${e[`${n}_artifact_path`]||``}`}function Z(e,{close:t=!1}={}){let n=U.get(e);n&&URL.revokeObjectURL(n),U.delete(e),Zt.delete(e),Qt.delete(e),t&&z.delete(e)}function Ia(){Zt.forEach((e,t)=>{let[n,r]=t.split(`:`),i=F.find(e=>Number(e.role_id)===Number(n));(!i||Fa(i,r)!==e)&&Z(t,{close:!0})})}function La(){if(!R)return;let e=R.jobs||F,t=new Map(e.map(e=>[Number(e.role_id),e])),n=R.roleIds.map(e=>t.get(Number(e))),r=n.filter(e=>e?.worker_state===`idle`&&e.cover_letter_status===`ready`).length,i=n.filter(e=>!e||e.worker_state===`idle`&&[`failed`,`interrupted`].includes(e.cover_letter_status)),a=n.length-r-i.length,o=R.skipped.length?` Skipped before queueing: ${R.skipped.map(e=>`${e.company_name} — ${e.title}: ${e.reason}`).join(` · `)}`:``,s=i.length?` Queued regeneration failures: ${i.map(e=>e?`${e.company_name} — ${e.title}: ${e.cover_letter_error||`generation failed`}`:`A role left the Prepped queue before regeneration completed`).join(` · `)}`:``;L=n.length?a>0?`Cover-letter regeneration in progress: ${r} of ${n.length} complete · ${a} remaining.${o}${s}`:`Cover-letter regeneration complete: ${r} succeeded, ${i.length} failed.${o}${s}`:`No cover letters were queued.${o}`}function Q(){Ia(),La();let e=F.filter(ka).length,t=F.filter(e=>e.worker_state===`idle`&&e.cover_letter_status===`ready`).length;ke.textContent=F.length?`${F.length} prepped ${F.length===1?`role`:`roles`}${e?` · ${e} in progress`:``}`:`No queued or prepared roles.`,Ae.disabled=Bt||t===0,Ae.setAttribute(`aria-busy`,Bt?`true`:`false`),Ae.textContent=Bt?`queuing cover letters...`:`regenerate all cover letters`,je.textContent=L,Me.innerHTML=F.map(e=>{let t=Aa(e),n=!t&&Ma(e),r=!t&&!n&&Na(e),i=Number(e.role_id)===Number(I)?` is-active`:``;return`
      <button type="button" class="prepped-list-item${r?` is-generation-queued`:``}${n?` is-document-generating`:``}${t?` has-generation-failure`:``}${i}" data-prepped-role="${e.role_id}">
        <strong>${J(e.company_name)}</strong><span>${J(e.title)}</span>
        <small class="status-${K(e.overall_status)}">${K(Pa(e.overall_status))}</small>
      </button>`}).join(``),$(),Da()}function $(){let e=F.findIndex(e=>Number(e.role_id)===Number(I)),t=F[e];if(!t){y.innerHTML=`<div class="prepped-empty"><h3>nothing prepped yet.</h3><p>Queue Interested roles from Autoprep Interested.</p></div>`;return}let n=J(t.title),r=gn(t.role_url),i=r?`<a class="prepped-role-link" href="${K(r)}" target="_blank" rel="noopener noreferrer">${n}<span aria-hidden="true">↗</span></a>`:n,a=[[`Location`,t.location||`Unavailable`],[`Added`,G(t.date_added||t.created_at)||`Unavailable`],[`Last seen`,G(t.last_seen_at)||`Unavailable`],[`Posting ID`,t.posting_id||`Unavailable`]],o=Ht.has(Number(t.role_id)),s=o||ka(t),c=`${t.role_id}:description`,l=`${t.role_id}:notes`;y.innerHTML=`
    <header class="prepped-detail-heading">
      <div><p class="eyebrow">${J(t.company_name)}</p><h3>${i}</h3></div>
      <span class="prepped-status status-${K(t.overall_status)}">${K(Pa(t.overall_status))}</span>
    </header>
    <dl class="prepped-role-facts">${a.map(([e,t])=>`<div><dt>${K(e)}</dt><dd>${J(t)}</dd></div>`).join(``)}</dl>
    <details class="prepped-role-description" data-prepped-detail-section="description" ${Wt.has(c)?`open`:``}>
      <summary>Job description</summary>
      <div class="prepped-description-copy">${J(t.description||`No job description was saved.`).replaceAll(`
`,`<br>`)}</div>
    </details>
    ${t.notes?`<details class="prepped-role-description" data-prepped-detail-section="notes" ${Wt.has(l)?`open`:``}><summary>Role notes</summary><div class="prepped-description-copy">${J(t.notes).replaceAll(`
`,`<br>`)}</div></details>`:``}
    <div class="prepped-document-grid">
      ${Ja(t,`resume`,`Resume`)}
      ${Ja(t,`cover-letter`,`Cover letter`)}
    </div>
    ${za(t)}
    <div class="prepped-detail-actions">
      <button type="button" data-prepped-nav="previous" ${e<=0?`disabled`:``}>Previous</button>
      <button type="button" data-prepped-nav="next" ${e>=F.length-1?`disabled`:``}>Next</button>
      <button type="button" data-autoprep-open-folder ${t.artifact_directory?``:`disabled`}>Open Documents Folder</button>
      <button class="prepped-disinterested" type="button" data-autoprep-disinterested aria-busy="${o?`true`:`false`}" ${s?`disabled`:``} title="${ka(t)?`Wait for preparation to finish before moving this role`:`Move this role out of Prepped`}">${o?`Moving to Disinterested...`:`Move to Disinterested`}</button>
      <button class="success" type="button" data-autoprep-applied ${t.overall_status===`ready`?``:`disabled`}>Applied</button>
    </div>
    <p class="prepped-safety-note">Autoprep prepares files only. It never submits an application.</p>`,Kt.has(Number(t.role_id))||Va(t.role_id)}function Ra(e){return Array.isArray(e)?e:Array.isArray(e?.answers)?e.answers:e?.answer&&typeof e.answer==`object`?[e.answer]:e?.record&&typeof e.record==`object`?[e.record]:e&&typeof e==`object`&&(`question`in e||`answer`in e||`status`in e||`error`in e)?[e]:[]}function za(e){let t=Number(e.role_id),n=B.get(t)??[],r=Gt.get(t)??``,i=V.has(t),a=qt.has(t),o=H.get(t);return`<section class="application-questions-workspace" aria-labelledby="application-questions-heading-${t}">
    <div class="application-questions-heading"><div><p class="eyebrow">Application helper</p><h4 id="application-questions-heading-${t}">Application questions</h4></div><span>${n.length} saved</span></div>
    <p class="application-questions-intro">Paste a question from an application form to generate and keep a role-specific answer.</p>
    <div class="application-answer-history" aria-live="polite">
      ${a&&!n.length?`<p class="application-answer-empty">Loading saved answers…</p>`:``}
      ${o?`<p class="prepped-error">${J(o)}</p>`:``}
      ${!a&&!o&&!n.length?`<p class="application-answer-empty">No application questions saved yet.</p>`:``}
      ${n.map((e,t)=>Ba(e,t,i)).join(``)}
    </div>
    <div class="application-question-composer">
      <label for="application-question-${t}">Question</label>
      <textarea id="application-question-${t}" data-application-question-draft rows="4" placeholder="Paste an application question…" ${i?`disabled`:``}>${K(r)}</textarea>
      <div><small>Answers are saved to this role. Asking never changes its status.</small><button type="button" data-application-question-submit aria-busy="${i?`true`:`false`}" ${i||!r.trim()?`disabled`:``}>${i?`Generating…`:`Generate answer`}</button></div>
    </div>
  </section>`}function Ba(e,t,n){let r=e?.status??`saved`,i=e?.created_at??e?.updated_at??e?.timestamp,a=e?.backend??e?.generation_backend,o=Number(e?.id),s=Number.isFinite(o)&&r!==`pending`&&!n,c=Jt.has(o),l=Yt.has(o),u=Xt.has(o);return`<article class="application-answer-record status-${K(r)}">
    <div class="application-answer-meta"><span>${J(r)}</span>${a?`<span>${J(a)}</span>`:``}${i?`<time datetime="${K(i)}">${J(G(i)||i)}</time>`:``}</div>
    <h5>${K(e.question??`Question unavailable`)}</h5>
    ${e.answer?`<p class="application-answer-copy">${K(e.answer).replaceAll(`
`,`<br>`)}</p>`:``}
    ${e.error?`<p class="prepped-error">${J(e.error)}</p>`:``}
    <div class="application-answer-actions">
      ${e.answer?`<button type="button" data-application-answer-copy="${t}">Copy answer</button>`:``}
      ${Number.isFinite(o)?`<button type="button" data-application-answer-regenerate="${o}" ${s?``:`disabled`}>${l||r===`pending`?`Regenerating…`:`Regenerate`}</button><button class="danger" type="button" data-application-answer-delete="${o}" ${s?``:`disabled`}>${u?`Deleting…`:c?`Confirm delete`:`Delete question`}</button>`:``}
    </div>
  </article>`}async function Va(e){let t=Number(e);if(!qt.has(t)){qt.add(t),H.delete(t);try{let n=await fetch(`/api/autoprep/roles/${encodeURIComponent(e)}/application-answers`),r=await n.json();if(!n.ok)throw Error(r?.error||`Could not load saved answers.`);B.set(t,Ra(r)),Kt.add(t)}catch(e){H.set(t,e instanceof Error?e.message:`Could not load saved answers.`)}finally{qt.delete(t),Number(I)===t&&$()}}}async function Ha(e){if(navigator.clipboard?.writeText)try{await navigator.clipboard.writeText(e);return}catch{}let t=document.createElement(`textarea`);t.value=e,t.readOnly=!0,t.style.position=`fixed`,t.style.opacity=`0`,document.body.append(t),t.select();let n=document.execCommand(`copy`);if(t.remove(),!n)throw Error(`Clipboard copy is unavailable`)}async function Ua(e){let t=Number(e),n=String(Gt.get(t)??``).trim();if(!(!n||V.has(t))){V.add(t),$();try{let r=await fetch(`/api/autoprep/roles/${encodeURIComponent(e)}/application-answers`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({question:n})}),i=await r.json(),a=Ra(i),o=B.get(t)??[];if(Array.isArray(i?.answers)?B.set(t,a):a.length&&B.set(t,[...o,...a]),!r.ok)throw Error(i?.error||a[0]?.error||`Could not generate an answer.`);Gt.delete(t),Kt.add(t),H.delete(t)}catch(e){H.set(t,e instanceof Error?e.message:`Could not generate an answer.`)}finally{V.delete(t),Number(I)===t&&$()}}}function Wa(e,t){let n=Number(e),r=B.get(n)??[],i=Number(t?.id),a=r.findIndex(e=>Number(e?.id)===i);if(a<0){B.set(n,[t,...r]);return}let o=[...r];o[a]=t,B.set(n,o)}async function Ga(e,t){let n=Number(e);if(!V.has(n)){V.add(n),Yt.add(Number(t)),Jt.delete(Number(t)),H.delete(n),$();try{let r=await fetch(`/api/autoprep/roles/${encodeURIComponent(e)}/application-answers/${encodeURIComponent(t)}/regenerate`,{method:`POST`}),i=await r.json(),[a]=Ra(i);if(a&&Wa(n,a),!r.ok)throw Error(i?.error||a?.error||`Could not regenerate the answer.`)}catch(e){H.set(n,e instanceof Error?e.message:`Could not regenerate the answer.`)}finally{Yt.delete(Number(t)),V.delete(n),Number(I)===n&&$()}}}async function Ka(e,t){let n=Number(e),r=Number(t);if(!Jt.has(r)){Jt.add(r),$();return}if(!V.has(n)){V.add(n),Xt.add(r),Jt.delete(r),H.delete(n),$();try{let i=await fetch(`/api/autoprep/roles/${encodeURIComponent(e)}/application-answers/${encodeURIComponent(t)}`,{method:`DELETE`}),a=await i.json();if(!i.ok)throw Error(a?.error||`Could not delete the question.`);let o=B.get(n)??[];B.set(n,o.filter(e=>Number(e?.id)!==r))}catch(e){H.set(n,e instanceof Error?e.message:`Could not delete the question.`)}finally{Xt.delete(r),V.delete(n),Number(I)===n&&$()}}}async function qa(e,t){let n=`${e.role_id}:${t}`,r=Fa(e,t);if(!(Zt.get(n)===r||$t.has(n))){Z(n),$t.add(n),Qt.delete(n),$();try{let i=await Fn(`/api/autoprep/roles/${encodeURIComponent(e.role_id)}/documents/${t}.pdf?v=${encodeURIComponent(e.updated_at||``)}`),a=F.find(t=>Number(t.role_id)===Number(e.role_id));if(!z.has(n)||!a||Fa(a,t)!==r){URL.revokeObjectURL(i),z.delete(n);return}U.set(n,i),Zt.set(n,r)}catch(e){Qt.set(n,e instanceof Error?e.message:`PDF preview unavailable`)}finally{$t.delete(n),Number(I)===Number(e.role_id)&&$()}}}function Ja(e,t,n){let r=t===`cover-letter`?`cover_letter`:`resume`,i=e[`${r}_status`],a=e[`${r}_artifact_path`],o=a?.split(`/`).pop()??`Not available`,s=e[`${r}_error`],c=e[`${r}_instruction`]||``,l=`${e.role_id}:${t}`,u=Ut.get(l)??c,d=t===`cover-letter`?`Optional comments for the next version`:`Comments for the next version`,ee=t===`cover-letter`?`Optionally describe specific, truthful changes...`:`Describe specific, truthful changes...`,te=[`failed`,`interrupted`].includes(i),f=e.worker_state!==`idle`||[`queued`,`generating`,`generating_tweaks`,`regenerating`].includes(i),ne=!f&&(i===`ready`||te)&&(te||t===`cover-letter`||String(u).trim()),p=z.has(l),m=`/api/autoprep/roles/${encodeURIComponent(e.role_id)}/documents/${t}.pdf?v=${encodeURIComponent(e.updated_at||``)}`,h=U.get(l),re=Qt.get(l),ie=$t.has(l),ae=a?`<a class="prep-cover-pdf-link" data-autoprep-view="${t}" href="${K(m)}" target="_blank" rel="noreferrer" aria-label="View ${K(n.toLowerCase())} PDF in browser">View PDF</a>`:``;return`
    <section class="prepped-document${p?` has-open-preview`:``} status-${K(i)}">
      <div class="prepped-document-heading"><h4>${K(n)}</h4><span>${K(Pa(i))}</span></div>
      <p class="prepped-filename">${K(o)}</p>
      ${s?`<p class="prepped-error">${K(s)}</p>`:``}
      <div class="prepped-document-actions">
        <button type="button" data-autoprep-preview="${t}" ${a?``:`disabled`}>${p?`Hide preview`:`Preview PDF`}</button>
        ${ae}
      </div>
      <div class="prepped-pdf-preview" data-autoprep-preview-panel="${t}" ${p&&a?``:`hidden`}>
        ${p&&h?`<iframe title="${K(n)} PDF preview" src="${K(h)}"></iframe>`:``}
        ${p&&ie?`<p>Loading PDF preview...</p>`:``}
        ${p&&re?`<p class="prepped-error">${J(re)}</p>`:``}
      </div>
      <label class="prepped-comments-label" for="prepped-comments-${K(l)}">${d}</label>
      <textarea id="prepped-comments-${K(l)}" data-autoprep-comments="${t}" rows="4" placeholder="${ee}" ${f?`disabled`:``}>${J(u)}</textarea>
      <button class="prepped-regenerate" type="button" data-autoprep-regenerate="${t}" ${ne?``:`disabled`}>${f?`Regenerating...`:`Regenerate ${K(n)}`}</button>
    </section>`}async function Ya(e,t,n){if(n.disabled)return;let r=`${e.role_id}:${t}`,i=e[`${t===`cover-letter`?`cover_letter`:`resume`}_status`],a=[`failed`,`interrupted`].includes(i),o=y.querySelector(`[data-autoprep-comments="${t}"]`),s=String(o?.value||Ut.get(r)||``).trim();if(!s&&t!==`cover-letter`&&!a){o?.focus();return}n.disabled=!0,n.textContent=`Queuing regeneration...`;try{let n=await fetch(`/api/autoprep/roles/${encodeURIComponent(e.role_id)}/${a?`retry`:`regenerate`}/${t}`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(a?{idempotency_key:xa(`retry-${t}`)}:{comments:s,idempotency_key:xa(`regenerate-${t}`)})}),i=await n.json();if(!n.ok)throw Error(i.error||`Regeneration request failed`);Ut.delete(r),Z(r,{close:!0});let o=F.findIndex(t=>Number(t.role_id)===Number(e.role_id));o>=0&&(F[o]=i.job),Q()}catch(e){window.alert(e instanceof Error?e.message:`Regeneration request failed`),await Ea()}}async function Xa(){if(!Bt){Bt=!0,R=null,L=`Queuing eligible cover letters...`,Q();try{let e=await fetch(`/api/autoprep/cover-letters/regenerate`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({idempotency_key:xa(`regenerate-all-cover-letters`)})}),t=await e.json();if(!e.ok)throw Error(t.error||`Bulk regeneration request failed`);let n=Number(t.queued_count||0),r=Array.isArray(t.skipped)?t.skipped:[];R={roleIds:(t.jobs||[]).map(e=>Number(e.role_id)),jobs:t.jobs||[],skipped:r},!n&&!r.length&&(R=null,L=`No prepped roles are available to regenerate.`),(t.jobs||[]).forEach(e=>{let t=F.findIndex(t=>Number(t.role_id)===Number(e.role_id));t>=0&&(F[t]=e),Z(`${e.role_id}:cover-letter`,{close:!0})}),await Ea(),Da()}catch(e){R=null,L=e instanceof Error?e.message:`Bulk regeneration request failed`}finally{Bt=!1,Q()}}}async function Za(e,t){let n=Number(e);if(Ht.has(n))return;Ht.add(n),t.disabled=!0,t.setAttribute(`aria-busy`,`true`),t.textContent=`Moving to Disinterested...`;let r=F.findIndex(e=>Number(e.role_id)===n);try{await ba(e,`disinterested`),Z(`${e}:resume`,{close:!0}),Z(`${e}:cover-letter`,{close:!0}),r>=0&&F.splice(r,1),I=F[Math.min(r,F.length-1)]?.role_id??null,L=`Role moved to Disinterested.`,Q(),Fr()}catch(e){L=e instanceof Error?e.message:`Could not move this role to Disinterested.`,await Ea()}finally{Ht.delete(n),F.some(e=>Number(e.role_id)===n)&&Q()}}async function Qa(e,t){if(t.disabled)return;t.disabled=!0,t.textContent=`Moving to Applied...`;let n=F.findIndex(t=>Number(t.role_id)===Number(e));try{if(!(await fetch(`/api/autoprep/roles/${encodeURIComponent(e)}/applied`,{method:`POST`})).ok)throw Error(`Applied update failed`);Z(`${e}:resume`,{close:!0}),Z(`${e}:cover-letter`,{close:!0}),F.splice(n,1),I=F[Math.min(n,F.length-1)]?.role_id??null,Q(),Fr()}catch{await Ea()}}_e.addEventListener(`click`,ki),Se.addEventListener(`click`,Ai),ve.addEventListener(`click`,ji),Ee.addEventListener(`click`,()=>wa()),Oe.addEventListener(`click`,Ta),Ae.addEventListener(`click`,Xa),Me.addEventListener(`click`,e=>{let t=e.target.closest(`[data-prepped-role]`);t&&(I=Number(t.dataset.preppedRole),Q())}),y.addEventListener(`input`,e=>{let t=e.target.closest(`[data-application-question-draft]`);if(t){let e=Number(I);Gt.set(e,t.value);let n=y.querySelector(`[data-application-question-submit]`);n&&(n.disabled=!t.value.trim()||V.has(e));return}let n=e.target.closest(`[data-autoprep-comments]`);if(!n)return;let r=`${I}:${n.dataset.autoprepComments}`;Ut.set(r,n.value);let i=y.querySelector(`[data-autoprep-regenerate="${n.dataset.autoprepComments}"]`),a=F.find(e=>Number(e.role_id)===Number(I)),o=n.dataset.autoprepComments===`cover-letter`?`cover_letter`:`resume`,s=a?.[`${o}_status`],c=[`failed`,`interrupted`].includes(s);i&&(i.disabled=a?.worker_state!==`idle`||![`ready`,`failed`,`interrupted`].includes(s)||!c&&n.dataset.autoprepComments!==`cover-letter`&&!n.value.trim())}),y.addEventListener(`toggle`,e=>{let t=e.target.closest(`[data-prepped-detail-section]`);if(!t)return;let n=`${I}:${t.dataset.preppedDetailSection}`;t.open?Wt.add(n):Wt.delete(n)},!0),y.addEventListener(`click`,async e=>{let t=F.find(e=>Number(e.role_id)===Number(I));if(!t)return;if(e.target.closest(`[data-application-question-submit]`)){Ua(t.role_id);return}let n=e.target.closest(`[data-application-answer-regenerate]`);if(n){Ga(t.role_id,n.dataset.applicationAnswerRegenerate);return}let r=e.target.closest(`[data-application-answer-delete]`);if(r){Ka(t.role_id,r.dataset.applicationAnswerDelete);return}let i=e.target.closest(`[data-application-answer-copy]`);if(i){let e=(B.get(Number(t.role_id))??[])[Number(i.dataset.applicationAnswerCopy)]?.answer;if(!e)return;try{await Ha(String(e)),i.textContent=`Copied`}catch{i.textContent=`Copy unavailable`}return}let a=e.target.closest(`[data-prepped-nav]`);if(a){let e=F.indexOf(t),n=a.dataset.preppedNav===`next`?1:-1;I=F[e+n]?.role_id??t.role_id,Q();return}let o=e.target.closest(`[data-autoprep-preview]`);if(o){let e=o.dataset.autoprepPreview,n=`${t.role_id}:${e}`;z.has(n)?(z.delete(n),$()):(z.add(n),$(),qa(t,e));return}let s=e.target.closest(`[data-autoprep-regenerate]`);if(s){Ya(t,s.dataset.autoprepRegenerate,s);return}let c=e.target.closest(`[data-autoprep-open-folder]`);if(c&&!c.disabled){c.disabled=!0,c.textContent=`Opening...`;try{if(!(await fetch(`/api/autoprep/roles/${encodeURIComponent(t.role_id)}/open-folder`,{method:`POST`})).ok)throw Error(`Could not open the documents folder.`);c.textContent=`Opened in Finder`,window.setTimeout(()=>{c.isConnected&&(c.textContent=`Open Documents Folder`,c.disabled=!1)},1500)}catch(e){c.textContent=e instanceof Error?e.message:`Could not open folder`,c.disabled=!1}return}let l=e.target.closest(`[data-autoprep-disinterested]`);if(l){Za(t.role_id,l);return}let u=e.target.closest(`[data-autoprep-applied]`);u&&Qa(t.role_id,u)}),Te.addEventListener(`click`,Mi),g.addEventListener(`click`,e=>{let t=e.target.closest(`[data-review-action]`);t&&Ji(t.dataset.reviewAction)}),_.addEventListener(`click`,e=>{e.target.closest(`.prep-summary-action`)&&e.stopPropagation()}),_.addEventListener(`input`,e=>{let t=e.target.closest(`[data-prep-resume-tweaks]`);if(t){let e=Number(t.dataset.prepResumeTweaks);Number.isFinite(e)&&Ft.set(e,t.value);return}let n=e.target.closest(`[data-prep-resume-latex]`);if(n){let e=Number(n.dataset.prepResumeLatex);if(!Number.isFinite(e))return;da(e,n.value);return}let r=e.target.closest(`[data-prep-cover-letter-latex]`);if(!r)return;let i=Number(r.dataset.prepCoverLetterLatex);if(!Number.isFinite(i))return;let a=r.closest(`.prep-cover-letter`)?.querySelector(`[data-prep-cover-letter-tweaks="${i}"]`)?.value??``;ga(i,r.value,a)}),_.addEventListener(`scroll`,e=>{e.target.closest(`[data-prep-resume-latex], [data-prep-cover-letter-latex]`)},!0),_.addEventListener(`focusout`,e=>{let t=e.target.closest(`[data-prep-resume-latex]`);if(t){let e=Number(t.dataset.prepResumeLatex);if(!Number.isFinite(e))return;da(e,t.value,0);return}let n=e.target.closest(`[data-prep-cover-letter-latex]`);if(!n)return;let r=Number(n.dataset.prepCoverLetterLatex);if(!Number.isFinite(r))return;let i=n.closest(`.prep-cover-letter`)?.querySelector(`[data-prep-cover-letter-tweaks="${r}"]`)?.value??``;ga(r,n.value,i,0)}),_.addEventListener(`submit`,async e=>{let t=e.target.closest(`[data-prep-role-chat-form]`);if(!t||!j[0])return;e.preventDefault();let n=Number(t.dataset.prepRoleChatForm);if(!Number.isFinite(n))return;let r=t.querySelector(`[data-prep-role-chat-input="${n}"]`),i=r?.value?.trim()??``;if(!i){r?.focus();return}let a=[...It.get(n)??[],{role:`user`,content:i}];It.set(n,a),v.querySelector(`.prep-role-chat`)?.replaceWith(X(Qi(j[0],{messages:a,loading:!0})));try{let e=await ua(n,a),t=[...a,e.message];It.set(n,t),v.querySelector(`.prep-role-chat`)?.replaceWith(X(Qi(j[0],{messages:t})))}catch{let e=[...a,{role:`assistant`,content:`could not answer right now.`}];It.set(n,e),v.querySelector(`.prep-role-chat`)?.replaceWith(X(Qi(j[0],{messages:e})))}}),_.addEventListener(`click`,async e=>{let t=e.target.closest(`[data-prep-section-target]`);if(t){let e=t.dataset.prepSectionTarget,n=e?document.getElementById(e):null;if(n instanceof HTMLDetailsElement){n.open=!0,n.scrollIntoView({behavior:`smooth`,block:`start`});let e=n.querySelector(`summary`);e?.setAttribute(`tabindex`,`-1`),e?.focus({preventScroll:!0})}return}if(e.target.closest(`[data-prep-analysis]`)&&j[0]){let e=j[0].id;v.querySelector(`.prep-analysis`)?.replaceWith(X(ta(j[0],{loading:!0})));try{let t=await ra(e,{force:!0});if(j[0]?.id!==e)return;v.querySelector(`.prep-analysis`)?.replaceWith(X(ta(j[0],{analysis:t})))}catch{v.querySelector(`.prep-analysis`)?.replaceWith(X(ta(j[0],{error:!0})))}return}if(e.target.closest(`[data-prep-resume-regenerate]`)&&j[0]){let e=j[0].id,t=v.querySelector(`.prep-resume`),n=t?.querySelector(`[data-prep-resume-tweaks="${e}"]`)?.value??``,r=t?.querySelector(`[data-prep-resume-latex="${e}"]`)?.value??``;if(!n.trim()){t?.querySelector(`[data-prep-resume-tweaks="${e}"]`)?.focus();return}Ft.set(e,n),t?.replaceWith(X(Xi(j[0],{loading:!0})));try{let t=await la(e,n,r);N.set(e,t.resume),v.querySelector(`.prep-resume`)?.replaceWith(X(Xi(j[0],{resume:t.resume}))),vn()}catch{v.querySelector(`.prep-resume`)?.replaceWith(X(Xi(j[0],{resume:N.get(e),tweaks:n}))),vn()}return}if(e.target.closest(`[data-prep-cover-letter]`)&&j[0]){let e=j[0].id,t=v.querySelector(`.prep-cover-letter`),n=t?.querySelector(`[data-prep-cover-letter-tweaks="${e}"]`)?.value??``,r=n.trim()?t?.querySelector(`[data-prep-cover-letter-latex="${e}"]`)?.value??``:``;t?.replaceWith(X(ea(j[0],{loading:!0})));try{let t=await ma(e,n,r);P.set(e,t.cover_letter),v.querySelector(`.prep-cover-letter`)?.replaceWith(X(ea(j[0],{coverLetter:t.cover_letter}))),vn()}catch{v.querySelector(`.prep-cover-letter`)?.replaceWith(X(ea(j[0],{coverLetter:P.get(e),tweaks:n}))),vn()}return}let n=e.target.closest(`[data-prep-action]`);if(n){ia(n.dataset.prepAction);return}let r=e.target.closest(`[data-prep-feedback]`);if(!r||!j[0])return;let i=j[0].id,a=M.get(i),o=Array.isArray(a?.feedback_items)?a.feedback_items.length:0,s=Pt.get(i)??0;if(r.dataset.prepFeedback===`accept`||r.dataset.prepFeedback===`ignore`){let e=a?.feedback_items?.[s];if(!e)return;let t=v.querySelector(`[data-prep-feedback-comment]`)?.value??``,n=r.dataset.prepFeedback,o=n;r.disabled=!0,r.textContent=n===`accept`?`adding...`:`ignoring...`;try{if(n===`accept`){let n=await aa(i,s,e,t),r=document.querySelector(`.job[data-role-id="${CSS.escape(String(i))}"]`);n.role&&(j[0]=n.role,vi(n.role,r)),eo(i,n.tweak_prompt??e.tweak_prompt??``),$a(i,s,a)}else await oa(i,s,e,t),$a(i,s,a)}catch{r.disabled=!1,r.textContent=o}return}let c=r.dataset.prepFeedback===`next`?1:-1;Pt.set(i,Math.max(0,Math.min(s+c,o-1))),v.querySelector(`.prep-analysis`)?.replaceWith(X(ta(j[0],{analysis:a})))});function $a(e,t,n){let r=n.feedback_items.filter((e,n)=>n!==t),i=Math.min(t,Math.max(r.length-1,0)),a={...n,feedback_items:r,verdict:r.length===0?`ready_to_apply`:n.verdict};Pt.set(e,i),M.set(e,a),v.querySelector(`.prep-analysis`)?.replaceWith(X(ta(j[0],{analysis:a})))}function eo(e,t){let n=String(t||``).trim();if(!n)return;let r=Ft.get(e)?.trim()??``,i=r?`${r}\n\n${n}`:n;Ft.set(e,i);let a=v.querySelector(`[data-prep-resume-tweaks="${e}"]`);a&&(a.value=i,a.focus())}document.addEventListener(`keydown`,e=>{e.key===`Escape`&&!Ie.hidden&&$n(),e.key===`Escape`&&!o.hidden&&mn(),e.key===`Escape`&&!g.hidden&&Ai(),e.key===`Escape`&&!_.hidden&&Mi(),e.key===`Escape`&&!De.hidden&&Ta(),e.key===`Escape`&&!We.hidden&&dr(),e.key===`Escape`&&!at.hidden&&yr(),e.key===`Escape`&&!ft.hidden&&Or(),e.key===`Escape`&&!vt.hidden&&Wr()}),Fe.addEventListener(`click`,Qn),Re.addEventListener(`click`,$n),Le.addEventListener(`click`,$n);function to(){return Array.from(document.querySelectorAll(`.pane-toggle`))}function no(){return to().some(e=>e.getAttribute(`aria-expanded`)===`true`)}function ro(){Be.textContent=no()?`collapse all`:`expand all`}function io(){document.querySelectorAll(`.pane-toggle`).forEach(e=>{e.setAttribute(`aria-expanded`,`true`),e.querySelector(`.chevron`).textContent=`v`,e.parentElement.querySelector(`.pane-body`).hidden=!1})}function ao(){document.querySelectorAll(`.job[open]`).forEach(e=>{e.open=!1}),document.querySelectorAll(`.pane-toggle`).forEach(e=>{e.setAttribute(`aria-expanded`,`false`),e.querySelector(`.chevron`).textContent=`>`,e.parentElement.querySelector(`.pane-body`).hidden=!0})}Be.addEventListener(`click`,()=>{no()?ao():io(),ro()}),Ve.addEventListener(`click`,()=>{jt=!jt,Ve.textContent=jt?`show empty`:`hide empty`,E&&Rn(E.statuses)}),Ue.addEventListener(`click`,ur),Ge.addEventListener(`click`,dr),it.addEventListener(`click`,vr),ot.addEventListener(`click`,yr),dt.addEventListener(`click`,Dr),pt.addEventListener(`click`,Or),Ne.addEventListener(`click`,Ur),yt.addEventListener(`click`,Wr),bt.addEventListener(`submit`,e=>{e.preventDefault(),qr(bt).catch(()=>{w.textContent=`could not add company.`})}),xt.addEventListener(`submit`,e=>{e.preventDefault(),Qr(xt).catch(()=>{Tt.textContent=`could not add role.`})}),T.addEventListener(`submit`,e=>{let t=e.target.closest(`[data-company-link-form]`);t&&(e.preventDefault(),Jr(t).catch(()=>{w.textContent=`could not add link.`}))}),T.addEventListener(`input`,e=>{let t=e.target.closest(`[data-company-notes]`);t&&ti(t.dataset.companyNotes)}),T.addEventListener(`change`,e=>{let t=e.target.closest(`[data-company-tier]`);if(!t)return;let n=t.closest(`.company-panel`);n&&ri(n,t.value),window.clearTimeout(un.get(t.dataset.companyTier)),ni(t.dataset.companyTier).catch(()=>{ei(`could not save company.`)})}),T.addEventListener(`click`,e=>{let t=e.target.closest(`[data-delete-company]`);if(t){let e=$r(t.dataset.deleteCompany),n=e?.name?q(e.name):`this company`;if(!window.confirm(`Deactivate ${n}? It will be hidden from company counts and skipped during scans.`))return;t.disabled=!0,Xr(t.dataset.deleteCompany).catch(()=>{w.textContent=`could not deactivate company.`,t.disabled=!1});return}let n=e.target.closest(`[data-delete-career-page]`);if(!n)return;let r=n.closest(`.company-link-row`)?.querySelector(`.company-link-text`)?.textContent?.trim();window.confirm(`Delete ${r||`this career link`}?`)&&(n.disabled=!0,Yr(n.dataset.deleteCareerPage).catch(()=>{w.textContent=`could not delete link.`,n.disabled=!1}))}),Ke.addEventListener(`change`,e=>{let t=e.target.closest(`input[type="checkbox"], select, input[data-setting-text], textarea[data-setting-textarea]`);t&&Ar(t)}),Ke.addEventListener(`click`,async e=>{let t=e.target.closest(`[data-application-runtime-test]`);if(!t||t.disabled)return;let n=t.dataset.applicationRuntimeTest,r=Ke.querySelector(`[data-application-runtime-test-status="${CSS.escape(n)}"]`);t.disabled=!0,t.textContent=`Testing…`,r&&(r.textContent=`Creating a bounded Callumployed session…`);try{let e=await fetch(`/api/application-generation/backends/${encodeURIComponent(n)}/test`,{method:`POST`}),t=await e.json();if(!e.ok||t?.ok!==!0)throw Error(t?.error||`Connection test failed.`);r&&(r.textContent=t.message||`Connection succeeded.`)}catch(e){r&&(r.textContent=e instanceof Error?e.message:`Connection test failed.`)}finally{t.disabled=!1,t.textContent=`Test connection`}}),Ke.addEventListener(`submit`,async e=>{e.preventDefault();let t=Ke.querySelector(`button[type="submit"]`),n=Ke.querySelectorAll(`input[type="checkbox"][name], select[name], input[data-setting-text][name], textarea[data-setting-textarea][name]`),r={};n.forEach(e=>{let t=e.name;t&&(r[t]=e.type===`checkbox`?e.checked:e.value)}),t.disabled=!0,t.textContent=`saving...`;try{C.textContent=`saving settings...`;let e=await fetch(`/api/config`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(r)});if(!e.ok)throw Error(`Config update failed`);er(await e.json(),`settings saved.`)}catch{C.textContent=`could not save settings.`,C.classList.remove(`is-empty`)}finally{t.disabled=!1,t.textContent=`save settings`}}),Qe.addEventListener(`input`,()=>{tt.disabled=!Qe.value.trim()}),et.addEventListener(`click`,Mr),tt.addEventListener(`click`,Nr),rt.addEventListener(`click`,jr),_t.addEventListener(`click`,Ir);function oo(){if(window.location.hash===`#prepped-roles`){wa();return}Ta({clearHash:!1})}window.addEventListener(`popstate`,oo),Fr(),window.location.hash===`#prepped-roles`&&oo(),ui({applyDefaultCollapsed:!0}).catch(()=>{Tn(null,`could not load resume.`),Dn([],`could not load cover letter examples.`),Mn()}),ai().then(()=>{oi()}).catch(()=>{S.textContent=`could not load scan status`});