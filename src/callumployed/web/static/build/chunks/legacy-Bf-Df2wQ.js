import{t as e}from"./preload-helper-Czpn1I53.js";var{sankey:t,sankeyLinkHorizontal:n}=await e(async()=>{let{sankey:e,sankeyLinkHorizontal:t}=await import(`/assets/d3-sankey.js`);return{sankey:e,sankeyLinkHorizontal:t}},[]),r=document.querySelector(`#stats`),i=document.querySelector(`#status-list`),a=document.querySelector(`#search-toggle`),o=document.querySelector(`#search-dialog`),s=document.querySelector(`#search-backdrop`),c=document.querySelector(`#search-form`),l=document.querySelector(`#search-input`),u=document.querySelector(`#close-search`),ee=document.querySelector(`#materials-panel`),te=document.querySelector(`#materials-toggle`),ne=document.querySelector(`#materials-body`),d=document.querySelector(`#materials-summary`),re=document.querySelector(`#materials-required-warning`),f=document.querySelector(`#resume-meta`),p=document.querySelector(`#resume-upload`),ie=document.querySelector(`#resume-upload-button`),ae=document.querySelector(`#resume-resource-meta`),oe=document.querySelector(`#resume-resource-upload`),se=document.querySelector(`#resume-resource-upload-button`),ce=document.querySelector(`#resume-resource-list`),le=document.querySelector(`#cover-letter-meta`),ue=document.querySelector(`#cover-letter-upload`),de=document.querySelector(`#cover-letter-upload-button`),fe=document.querySelector(`#cover-letter-list`),pe=document.querySelector(`#experience-note-meta`),me=document.querySelector(`#experience-note-upload`),he=document.querySelector(`#experience-note-upload-button`),ge=document.querySelector(`#experience-note-list`);document.querySelector(`#material-index-button`);var _e=document.querySelector(`#material-index-warning`),ve=document.querySelector(`#material-index-status`),ye=document.querySelector(`#review-discovered`),be=document.querySelector(`#role-information-view`),xe=document.querySelector(`#role-information-card`),Se=document.querySelector(`#close-role-information`),m=document.querySelector(`#review-view`),Ce=document.querySelector(`#review-heading`),we=document.querySelector(`#review-progress`),Te=document.querySelector(`#review-card`),Ee=document.querySelector(`#close-review`),h=document.querySelector(`#prep-view`),De=document.querySelector(`#prep-heading`),Oe=document.querySelector(`#prep-progress`),g=document.querySelector(`#prep-card`),ke=document.querySelector(`#close-prep`),Ae=document.querySelector(`#prepped-roles`),je=document.querySelector(`#prepped-view`),Me=document.querySelector(`#close-prepped`),Ne=document.querySelector(`#prepped-summary`),Pe=document.querySelector(`#regenerate-all-cover-letters`),Fe=document.querySelector(`#prepped-bulk-status`),Ie=document.querySelector(`#prepped-list`),_=document.querySelector(`#prepped-detail`),v=document.querySelector(`#scan-all-button`),Le=document.querySelector(`#manage-companies-button`),y=document.querySelector(`#scan-status-bar`),Re=document.querySelector(`#scan-status-text`),ze=document.querySelector(`#scan-last-time`),Be=document.querySelector(`#scan-failures-open`),Ve=document.querySelector(`#scan-failures-dialog`),He=document.querySelector(`#scan-failures-backdrop`),Ue=document.querySelector(`#scan-failures-close`),We=document.querySelector(`#scan-failures-list`),Ge=document.querySelector(`#toggle-all`),Ke=document.querySelector(`#collapse-empty`),qe=document.querySelector(`#toolbar-summary`),Je=document.querySelector(`#settings-open`),Ye=document.querySelector(`#settings-view`),Xe=document.querySelector(`#settings-close`),b=document.querySelector(`#settings-status`),x=document.querySelector(`#settings-form`),Ze=document.querySelector(`#settings-profile-options`),Qe=document.querySelector(`#settings-profile-extract`),$e=document.querySelector(`#settings-autoprep-options`),et=document.querySelector(`#settings-options`),tt=document.querySelector(`#central-store-summary`),nt=document.querySelector(`#central-store-sync-summary`),rt=document.querySelector(`#central-api-url-input`),it=document.querySelector(`#central-passkey-input`),at=document.querySelector(`#central-save-button`),ot=document.querySelector(`#central-sync-button`),st=document.querySelector(`#recommendation-history-summary`),ct=document.querySelector(`#clear-recommendation-history`),lt=document.querySelector(`#metrics-open-button`),ut=document.querySelector(`#metrics-view`),dt=document.querySelector(`#metrics-close`),ft=document.querySelector(`#metrics-status`),pt=document.querySelector(`#metrics-overview`),mt=document.querySelector(`#metrics-sections`),ht=document.querySelector(`#metrics-scan-list`),gt=document.querySelector(`#sankey-open-button`),_t=document.querySelector(`#sankey-view`),vt=document.querySelector(`#sankey-close`),yt=document.querySelector(`#sankey-status`),bt=document.querySelector(`#sankey-canvas`),xt=document.querySelector(`#sankey-path-list`),St=document.querySelector(`#app-update-button`),Ct=document.querySelector(`#companies-view`),wt=document.querySelector(`#companies-close`),S=document.querySelector(`#companies-status`),Tt=document.querySelector(`#company-create-form`),C=document.querySelector(`#companies-list`),Et=document.querySelector(`#role-add-form`),Dt=document.querySelector(`#role-url-input`),Ot=document.querySelector(`#role-company-input`),kt=document.querySelector(`#role-company-options`),At=document.querySelector(`#role-add-status`),jt=3,Mt=1200,Nt=new Set([`applied`,`OA`,`interview`,`rejected`,`offer`]),Pt=new Map([[`discovered`,`#4f6472`],[`interested`,`#00897b`],[`disinterested`,`#626970`],[`applied`,`#2257ad`],[`oa`,`#b36b00`],[`interview`,`#5f2bd8`],[`rejected`,`#b93d2d`],[`offer`,`#137347`],[`closed`,`#53606b`],[`archived`,`#765b4a`]]),Ft=/^(?:about (?:the )?(?:role|team|job)|about this role|job description|job responsibilities|minimum qualifications|preferred qualifications|qualifications|requirements|responsibilities|what to expect|what (?:you'll|you’ll|you will) (?:bring|do)|what'?s in it for you|who you are|your objectives|your skills & talents):?$/i,It=!0,w=null,Lt=null,T=[],E=[],D=[],Rt=null,O=[],k=[],A=new Map,zt=new Map,j=new Map,Bt=new Map,M=new Map,Vt=new Map,Ht=new Map,Ut=new Map,N=[],P=null,Wt=null,Gt=!1,Kt=``,F=null,qt=new Set,Jt=new Set,Yt=new Map,I=new Set,Xt=new Set,L=new Map,Zt=new Map,Qt=new Set,$t=new Set,R=new Set,en=new Set,tn=new Set,nn=new Set,z=new Map,B=new Map,rn=new Map,an=new Map,on=new Set,sn=!1,cn=0,ln=null,un=!1,dn=null,fn=null,pn=null,mn=null,V=null,hn=[],gn=new Map;function H(){return w?.query?.trim()??``}function _n(){let e=!!H();a.classList.toggle(`search-active`,e),a.setAttribute(`aria-label`,e?`clear search`:`search jobs`)}function vn(){l.value=H(),o.hidden=!1,c.hidden=!1,l.focus(),l.select()}function yn(){o.hidden=!0,c.hidden=!0,a.focus()}function bn(e){return e?new Intl.DateTimeFormat(void 0,{month:`short`,day:`numeric`,hour:`numeric`,minute:`2-digit`}).format(new Date(e)).toLocaleLowerCase():``}function U(e){return e?new Intl.DateTimeFormat(void 0,{month:`short`,day:`numeric`,hour:`numeric`,minute:`2-digit`}).format(new Date(e)).replace(`, `,` `).toLocaleLowerCase():``}function W(e){return String(e??``).replaceAll(`&`,`&amp;`).replaceAll(`<`,`&lt;`).replaceAll(`>`,`&gt;`).replaceAll(`"`,`&quot;`).replaceAll(`'`,`&#039;`)}function G(e){return String(e??``).toLocaleLowerCase()}function K(e){return W(G(e))}function xn(e){try{let t=new URL(String(e||``));return[`http:`,`https:`].includes(t.protocol)?t.href:``}catch{return``}}function Sn(e){return e}function q(e=g){e.querySelectorAll(`[data-prep-resume-latex], [data-prep-cover-letter-latex]`).forEach(Sn)}function Cn(){return`
    <svg class="role-link-icon" viewBox="0 0 24 24" aria-hidden="true">
      <path d="M7 17 17 7"></path>
      <path d="M8 7h9v9"></path>
    </svg>
  `}function wn(){return`
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M12 5v14"></path>
      <path d="M5 12h14"></path>
    </svg>
  `}function Tn(){return`
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M3 6h18"></path>
      <path d="M8 6V4h8v2"></path>
      <path d="m19 6-1 14H6L5 6"></path>
      <path d="M10 11v5"></path>
      <path d="M14 11v5"></path>
    </svg>
  `}function En(e,t,n){let r=`<span class="role-title-text">${K(e)}</span>`;return t?`<a class="${n}" href="${W(t)}" target="_blank" rel="noreferrer">${r}${Cn()}</a>`:`<span class="${n}">${r}</span>`}function Dn(e){r.innerHTML=[[`companies`,e.companies_total],[`jobs`,e.jobs_total],[`applications`,e.applications_total]].map(([e,t])=>`<dl class="stat"><dt>${K(e)}</dt><dd>${t}</dd></dl>`).join(``)}function On(e=w){if(!e){qe.innerHTML=``;return}let t=t=>e.statuses.find(e=>e.key===t)?.count??0;qe.innerHTML=[[`discovered`,t(`discovered`)],[`interested`,t(`interested`)],[`applied`,e.stats?.applications_total??0],[`total`,e.stats?.jobs_total??0]].map(([e,t])=>`
        <dl>
          <dt>${K(e)}</dt>
          <dd>${t}</dd>
        </dl>
      `).join(``)}function kn(e,t=``){if(Lt=e,ie.textContent=e?`replace`:`upload`,t){f.textContent=t;return}if(!e){f.textContent=`no resume uploaded`;return}let n=U(e.updated_at),r=Rn(e.content_bytes);f.textContent=[G(e.filename),r,n].filter(Boolean).join(` | `)}function An(e,t,n,{binary:r=!1}={}){let i=r?e.filename:e.id;return`
    <li class="material-source-item" title="${K(e.filename)}">
      <div class="material-source-copy">
        <span>${K(e.filename)}</span>
        <small>${W(n)}</small>
      </div>
      <div class="material-source-actions">
        <button type="button" class="material-source-view" data-material-view="${W(t)}" data-material-id="${W(i)}" data-material-binary="${r}">preview</button>
        <button type="button" class="material-source-remove" data-material-remove="${W(t)}" data-material-id="${W(i)}" data-material-name="${K(e.filename)}">remove</button>
      </div>
      <div class="material-source-preview" data-material-preview-body hidden></div>
    </li>`}function jn(e,t=``){E=Array.isArray(e)?e:[],de.textContent=E.length>0?`add`:`upload`,le.textContent=t||(E.length===0?`no examples uploaded`:`${E.length} ${E.length===1?`example`:`examples`} stored`),fe.innerHTML=E.map(e=>An(e,`cover-letter-examples`,Rn(e.content_bytes))).join(``)}function Mn(e,t=``){D=Array.isArray(e)?e:[],he.textContent=D.length>0?`add`:`upload`,pe.textContent=t||(D.length===0?`no notes uploaded`:`${D.length} ${D.length===1?`note`:`notes`} stored`),ge.innerHTML=D.map(e=>An(e,`experience-notes`,Rn(e.content_bytes))).join(``)}function Nn(e,t=``){Rt=e??null;let n=Rt?.status??`missing`,r=n!==`ready`;if(D.length,_e.hidden=!r,_e.textContent=t||Rt?.warning||``,t)ve.textContent=t;else if(n===`ready`){let e=Number(Rt?.document_count??0),t=Number(Rt?.skipped_source_count??0),n=U(Rt?.generated_at);ve.innerHTML=[`${e} indexed ${e===1?`page`:`pages`}`,t?`${t} unreadable upload skipped`:``,n].filter(Boolean).map(e=>`<button type="button" class="material-index-link" data-open-material-index title="Reveal the application material index in Finder">${K(e)}</button>`).join(`<span aria-hidden="true"> | </span>`)}else ve.textContent=n===`stale`?`index out of date`:`not indexed`}function Pn(e,t=``){T=Array.isArray(e)?e:[],se.textContent=T.length>0?`add`:`upload`,ae.textContent=t||(T.length===0?`no resources uploaded`:`${T.length} ${T.length===1?`resource`:`resources`} stored`),ce.innerHTML=T.map(e=>An(e,`resume-resources`,Rn(e.bytes),{binary:!0})).join(``)}function Fn(e,t={}){cn+=1,document.querySelectorAll(`[data-preview-blob-url]`).forEach(e=>{URL.revokeObjectURL(e.dataset.previewBlobUrl)}),kn(e?.master_resume??null),Pn(e?.resume_resources??[]),jn(e?.cover_letter_examples??[]),Mn(e?.experience_notes??[]),Nn(e?.material_index??null),In(e?.ui),(!sn||t.applyDefaultCollapsed)&&(Ln(!!e?.ui?.default_collapsed),sn=!0)}function In(e=null){let t=Lt?`resume ready`:`no resume`,n=T.length===0?`no resources`:`${T.length} ${T.length===1?`resource`:`resources`}`,r=E.length,i=r===0?`no cover letters`:`${r} cover ${r===1?`letter`:`letters`}`,a=D.length,o=a===0?`no notes`:`${a} experience ${a===1?`note`:`notes`}`;re.hidden=!(typeof e?.has_missing_required_materials==`boolean`?e.has_missing_required_materials:!Lt||r===0||a===0),d.textContent=`${t} | ${n} | ${i} | ${o}`}function Ln(e){ee.classList.toggle(`collapsed`,e),te.setAttribute(`aria-expanded`,String(!e)),te.querySelector(`.materials-chevron`).textContent=e?`>`:`v`,ne.hidden=e}function Rn(e){return Number.isFinite(e)?e<1024?`${e} b`:`${Math.round(e/1024)} kb`:``}async function zn(e){let t=await fetch(e,{cache:`no-store`});if(!t.ok)throw Error(`Preview unavailable`);let n=await t.arrayBuffer();if(new TextDecoder(`ascii`).decode(n.slice(0,5))!==`%PDF-`)throw Error(`The selected file is not a readable PDF.`);return URL.createObjectURL(new Blob([n],{type:`application/pdf`}))}async function Bn(e){let t=e.closest(`.material-source-item`)?.querySelector(`[data-material-preview-body]`);if(!t)return;if(t.dataset.loaded===`true`){t.hidden=!t.hidden,e.textContent=t.hidden?`preview`:`hide`;return}e.disabled=!0,e.textContent=`loading...`;let n=e.dataset.materialView,r=e.dataset.materialId,i=cn,a=`/api/${encodeURIComponent(n)}/${encodeURIComponent(r)}`;try{if(e.dataset.materialBinary===`true`){let e=await zn(a);if(!t.isConnected||cn!==i){URL.revokeObjectURL(e);return}t.dataset.previewBlobUrl=e,t.innerHTML=`<iframe title="${K(r)} preview"></iframe>`,t.querySelector(`iframe`).src=e}else{let e=await fetch(a);if(!e.ok)throw Error(`Preview unavailable`);let n=await e.json(),r=document.createElement(`pre`);r.textContent=n.content||`This source is empty.`,t.replaceChildren(r)}t.dataset.loaded=`true`,t.hidden=!1,e.textContent=`hide`}catch(n){t.textContent=n instanceof Error?n.message:`Preview unavailable`,t.hidden=!1,e.textContent=`preview`}finally{e.disabled=!1}}async function Vn(e){let t=e.dataset.materialRemove,n=e.dataset.materialId;if(e.dataset.confirmRemove!==`true`){e.dataset.confirmRemove=`true`,e.textContent=`confirm remove`,e.classList.add(`danger`),window.setTimeout(()=>{!e.isConnected||e.disabled||(delete e.dataset.confirmRemove,e.textContent=`remove`,e.classList.remove(`danger`))},6e3);return}e.disabled=!0,e.textContent=`removing...`;try{let e=await fetch(`/api/${encodeURIComponent(t)}/${encodeURIComponent(n)}`,{method:`DELETE`}),r=await e.json();if(!e.ok)throw Error(r.error||`Remove failed`);Fn(r)}catch(t){e.disabled=!1,delete e.dataset.confirmRemove,e.classList.remove(`danger`),e.textContent=`remove`,window.alert(t instanceof Error?t.message:`Remove failed`)}}function Hn(e){i.innerHTML=e.map(e=>{let t=e.jobs.map(t=>Un(t,e.key)).join(``),n=Math.max(Number(e.count)-e.jobs.length,0),r=[`disinterested`,`rejected`,`closed`].includes(e.key)&&n>0?`<p class="empty-copy status-more-copy">... and ${n} more</p>`:``;return`
        <section class="status-pane ${e.count===0?`empty`:``} ${It?`hidden-empty`:``}" id="status-${W(e.key)}" data-bucket="${W(e.key)}">
          <button class="pane-toggle" type="button" aria-expanded="false">
            <span class="chevron">></span>
            <span class="pane-title">${K(e.label)}</span>
            <span class="count">${e.count}</span>
          </button>
          <div class="pane-body" hidden>
            ${t||r?`<div class="jobs">${t}${r}</div>`:`<p class="empty-copy">${e.key===`archived`&&e.count>0?`archived role details are hidden.`:`no jobs in this status.`}</p>`}
          </div>
        </section>
      `}).join(``)}function Un(e,t){return`
    <details class="job" data-role-id="${W(e.id)}">
      <summary class="job-summary">
        <span class="job-chevron">></span>
        <span class="job-identity">
          <span class="job-company">[${K(e.company_name)}]</span>
          ${En(e.title,e.role_url,`job-title`)}
          ${t===`interested`&&e.prep_started?Kn():``}
          ${t===`closed`&&e.updated_in_latest_scan?Wn():``}
          ${[`discovered`,`interested`].includes(t)&&e.missing_from_latest_scan?Gn():``}
        </span>
      </summary>
      <div class="job-detail">
        ${t===`discovered`?qn(e):``}
        ${t===`interested`?Jn(e):``}
        ${t===`disinterested`?Yn(e):``}
        ${t===`applied`?Xn(e):``}
        ${t===`OA`?Zn(e):``}
        ${t===`interview`?Qn(e):``}
        ${t===`closed`?$n(e):``}
        <dl>
          ${e.location?`<div>
                  <dt>location</dt>
                  <dd>${K(e.location)}</dd>
                </div>`:``}
          <div>
            <dt>updated</dt>
            <dd>${bn(e.updated_at)}</dd>
          </div>
        </dl>
      </div>
    </details>
  `}function Wn(){return`<span class="latest-scan-dot" title="updated in latest scan" aria-label="updated in latest scan"></span>`}function Gn(){return`<span class="missing-latest-scan-dot" title="not seen in latest scan" aria-label="not seen in latest scan"></span>`}function Kn(){return`<span class="prep-started-dot" title="application materials started" aria-label="application materials started"></span>`}function qn(e){return`
    <div class="job-actions job-actions-nowrap" aria-label="discovered role actions">
      <button class="job-action success" type="button" data-review-role-id="${e.id}">view</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="interested">interested</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="disinterested">disinterested</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="closed">closed</button>
    </div>
  `}function Jn(e){return`
    <div class="job-actions" aria-label="interested role actions">
      <button class="job-action success" type="button" data-prep-role-id="${e.id}">prep</button>
      <button class="job-action success" type="button" data-autoprep-role-id="${e.id}">${e.autoprep_started?`view / regenerate prep`:`autoprep`}</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="applied">applied</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="disinterested">disinterested</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="closed">closed</button>
    </div>
    ${e.autoprep_started?`<p class="job-prepped-note">already prepped</p>`:``}
  `}function Yn(e){return`
    <div class="job-actions" aria-label="disinterested role actions">
      <button class="job-action success" type="button" data-role-id="${e.id}" data-status="interested">interested</button>
    </div>
  `}function Xn(e){return`
    <div class="job-actions job-actions-nowrap" aria-label="applied role actions">
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="OA">oa</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="interview">interview</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="rejected">rejected</button>
    </div>
  `}function Zn(e){return`
    <div class="job-actions job-actions-nowrap" aria-label="oa role actions">
      <button class="job-action" type="button" data-view-role-info="${e.id}">view information</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="interview">interview</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="disinterested">disinterested</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="rejected">rejected</button>
    </div>
  `}function Qn(e){return`
    <div class="job-actions" aria-label="interview role actions">
      <button class="job-action" type="button" data-view-role-info="${e.id}">view information</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="rejected">rejected</button>
      <button class="job-action success" type="button" data-role-id="${e.id}" data-status="offer">offer</button>
    </div>
  `}function $n(e){return`
    <div class="job-actions" aria-label="closed role actions">
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="interested">interested</button>
    </div>
  `}function er(e){w=e,l.value=e.query,_n(),Dn(e.stats),On(e),Hn(e.statuses),uo(),Ai(e.statuses)}function tr(e){dn=e??null;let t=!!e?.scanning,n=t&&!!e?.cancel_requested,r=Number(e?.completed_companies??0),i=Number(e?.total_companies??0),a=Number(e?.failed_companies??0),o=typeof e?.error==`string`?e.error.trim():``,s=Array.isArray(e?.failures)?e.failures:[];v.disabled=n,v.textContent=t?n?`cancelling...`:`cancel scan`:`scan roles`,v.classList.toggle(`danger`,t&&!n),y.hidden=!t&&!o&&s.length===0,y.classList.toggle(`scanning`,t),y.classList.toggle(`scan-error`,!t&&!!o||s.length>0),Re.textContent=n?`cancelling scan...`:t?`scanning roles${i>0?` ${r}/${i}`:``}${a>0?`, ${a} failed`:``}`:s.length>0?`${s.length} recent scan ${s.length===1?`failure`:`failures`}`:o?`last scan error: ${o}`:`scan idle`,Be&&We&&(Be.hidden=s.length===0,We.innerHTML=s.slice(0,5).map(e=>{let t=e?.company_name||`unknown company`,n=e?.error||`scan failed`;return`
          <p>
            <span>${K(t)}</span>
            <span>${W(n)}</span>
          </p>
        `}).join(``),s.length===0&&rr());let c=e?.last_scan_at;ze.textContent=c?`last scan: ${U(c)}`:`last scan: never`,un&&!t&&mi(H()).catch(()=>{}),un=t}function nr(){Be.hidden||(Ve.hidden=!1,Ue.focus())}function rr(){Ve.hidden=!0}function J(e,t=``){fn=e;let n=Array.isArray(e?.settings)?e.settings:[],r=n.filter(e=>e.key?.startsWith(`applicant_`)),i=n.filter(e=>e.key?.startsWith(`autoprep_`)||e.key===`application_generation_backend`),a=n.filter(e=>!e.key?.startsWith(`applicant_`)&&!e.key?.startsWith(`autoprep_`)&&e.key!==`application_generation_backend`),o=e?.central??{};b.textContent=t,b.classList.toggle(`is-empty`,!t);let s=Number(e?.recommendation_history_count??0);st.textContent=s>0?`${s} saved ${s===1?`feedback decision`:`feedback decisions`}`:`no saved resume feedback decisions`,ct.disabled=s===0,or(o),Ze.innerHTML=r.map(e=>sr(e)).join(``),$e.innerHTML=i.map(t=>sr(ir(t,e))).join(``)+ar(e),et.innerHTML=a.map(e=>sr(e)).join(``),fr(!1)}function ir(e,t){if(e.key!==`application_generation_backend`||!Array.isArray(e.options))return e;let n=t?.application_generation_runtimes??{};return{...e,options:e.options.map(e=>{let t=n?.[e.value];return!t||e.available===!1||e.disabled===!0?e:{...e,available:t.available??t.detected??!0,reason:t.reason}})}}function ar(e){let t=e?.application_generation_runtimes??e?.runtime_availability??e?.runtimes??{},n=[[`hermes`,t?.hermes??t?.Hermes],[`openclaw`,t?.openclaw??t?.OpenClaw]];return n.some(([,e])=>e&&typeof e==`object`)?`<div class="application-runtime-statuses" aria-label="application generation runtime detection">
    ${n.map(([e,t])=>{let n=t?.available??t?.detected??!1,r=t?.reason??t?.message??(n?`Runtime detected`:`Runtime unavailable`);return`<div class="application-runtime-status" data-application-runtime="${W(e)}">
        <span><strong>${K(e===`openclaw`?`OpenClaw`:`Hermes`)}</strong> ${n?`available`:`unavailable`}</span>
        <small>${K(r)}</small>
        <button type="button" data-application-runtime-test="${W(e)}" ${n?``:`disabled`}>Test connection</button>
        <small data-application-runtime-test-status="${W(e)}" aria-live="polite"></small>
      </div>`}).join(``)}
  </div>`:``}function or(e){let t=e?.api_url??``;rt.value=t,it.value=``;let n=e?.passkey_configured?`passkey saved`:`no passkey saved`;tt.textContent=t?`${G(t)} | ${n}`:`no api url | ${n}`,nt.textContent=`${Number(e?.companies_linked??0)} linked | ${Number(e?.companies_unlinked??0)} unlinked | ${Number(e?.companies_needs_review??0)} review | ${Number(e?.companies_failed??0)} failed`,ot.disabled=!t}function sr(e){if(e.control===`textarea`&&e.editable!==!1)return lr(e);if(e.control===`text`&&e.editable!==!1)return cr(e);if(e.control===`select`&&e.editable!==!1)return ur(e);if(e.control!==`toggle`||e.editable===!1)return dr(e);let t=e.value?`checked`:``,n=e.default?`on by default`:`off by default`;return`
    <label class="setting-option">
      <span class="setting-copy">
        <span class="setting-label">${K(e.label)}</span>
        <span class="setting-description">${K(e.description)}</span>
        <span class="setting-default">${K(n)}</span>
      </span>
      <span class="setting-switch">
        <input type="checkbox" name="${W(e.key)}" ${t} />
        <span aria-hidden="true"></span>
      </span>
    </label>
  `}function cr(e){let t=e.default?`default: ${G(e.default)}`:`optional`,n=e.input_type??`text`,r=e.autocomplete??`name`;return`
    <label class="setting-option">
      <span class="setting-copy">
        <span class="setting-label">${K(e.label)}</span>
        <span class="setting-description">${K(e.description)}</span>
        <span class="setting-default">${K(t)}</span>
      </span>
      <input
        class="setting-text-input"
        data-setting-text
        name="${W(e.key)}"
        type="${W(n)}"
        value="${W(e.value??``)}"
        autocomplete="${W(r)}"
      />
    </label>
  `}function lr(e){return`
    <label class="setting-option setting-option-prompt">
      <span class="setting-copy">
        <span class="setting-label">${K(e.label)}</span>
        <span class="setting-description">${K(e.description)}</span>
      </span>
      <textarea
        class="setting-prompt-input"
        data-setting-textarea
        name="${W(e.key)}"
        rows="7"
        maxlength="8000"
      >${K(e.value??``)}</textarea>
    </label>
  `}function ur(e){let t=Array.isArray(e.options)?e.options:[],n=`default: ${G(e.default)}`,r=e.key===`application_generation_backend`,i=r?`setting-select setting-select-application-backend`:`setting-select`;return`
    <label class="setting-option">
      <span class="setting-copy">
        <span class="setting-label">${K(e.label)}</span>
        <span class="setting-description">${K(e.description)}</span>
        <span class="setting-default">${K(n)}</span>
      </span>
      <select class="${i}" name="${W(e.key)}">
        ${t.map(t=>{let n=t.value===e.value?`selected`:``,i=t.available===!1||t.disabled===!0,a=r&&i?` — unavailable`:``;return`<option value="${W(t.value)}" ${n} ${i?`disabled`:``}>${K(t.label)}${K(a)}</option>`}).join(``)}
      </select>
    </label>
  `}function dr(e){let t=e.default?`on by default`:`off by default`,n=e.value?`automatic`:`off`;return`
    <div class="setting-option setting-option-readonly">
      <span class="setting-copy">
        <span class="setting-label">${K(e.label)}</span>
        <span class="setting-description">${K(e.description)}</span>
        <span class="setting-default">${K(t)}</span>
      </span>
      <span class="setting-badge">${K(n)}</span>
    </div>
  `}function fr(e){x.querySelectorAll(`input, select, textarea`).forEach(t=>{t.disabled=e}),at.disabled=e,ot.disabled=e||!rt.value.trim(),Qe.disabled=e,St.disabled=e}async function pr(){Ye.hidden=!1,document.body.classList.add(`settings-open`),Xe.focus(),fn?J(fn):(b.textContent=`loading settings...`,b.classList.remove(`is-empty`),et.innerHTML=``);try{await hr()}catch{b.textContent=`could not load settings.`}}function mr(){Ye.hidden=!0,document.body.classList.remove(`settings-open`),Je.focus()}async function hr(){let e=await fetch(`/api/config`);if(!e.ok)throw Error(`Config request failed`);J(await e.json())}async function gr(){Qe.disabled=!0,Qe.textContent=`filling blank fields...`,b.textContent=`sending the master resume to the selected AI provider...`,b.classList.remove(`is-empty`);try{let e=await fetch(`/api/config/extract-profile`,{method:`POST`});if(!e.ok)throw Error(`Profile extraction request failed`);let t=await e.json(),n=Array.isArray(t.populated)?t.populated:[];J(t.config,n.length?`filled ${n.length} blank profile ${n.length===1?`field`:`fields`}.`:`no blank profile fields could be filled.`)}catch{b.textContent=`could not fill profile fields from the resume.`}finally{Qe.disabled=!1,Qe.textContent=`fill blank fields`}}function _r(e){let t=e?.value;return t==null?`n/a`:e?.kind===`ratio`?Number(t).toLocaleString(void 0,{maximumFractionDigits:2,minimumFractionDigits:0}):typeof t==`number`?t.toLocaleString():G(t)}function vr(e,t=`metric-card`){return`
    <article class="${t}">
      <span>${K(e?.label)}</span>
      <strong>${W(_r(e))}</strong>
    </article>
  `}function yr(e,t=``){pn=e,ft.textContent=t||(e?.updated_at?`updated ${U(e.updated_at)}`:``),ft.classList.toggle(`is-empty`,!ft.textContent);let n=Array.isArray(e?.overview)?e.overview:[],r=Array.isArray(e?.sections)?e.sections:[],i=Array.isArray(e?.recent_scans)?e.recent_scans:[];pt.innerHTML=n.map(e=>vr(e)).join(``),mt.innerHTML=r.map(br).join(``),ht.innerHTML=i.length?i.map(xr).join(``):`<p class="empty-copy">no scan runs recorded.</p>`}function br(e){let t=Array.isArray(e?.metrics)?e.metrics:[];return`
    <section class="metrics-section">
      <div class="metrics-section-heading">
        <h3>${K(e?.title)}</h3>
      </div>
      <div class="metrics-section-grid">
        ${t.map(e=>vr(e,`metric-card metric-card-compact`)).join(``)}
      </div>
    </section>
  `}function xr(e){let t=e?.scan_status??`unknown`,n=e?.started_at?U(e.started_at):`not started`,r=e?.finished_at?U(e.finished_at):`not finished`,i=e?.error?`<span>${K(e.error)}</span>`:``;return`
    <article class="metrics-scan-row">
      <div>
        <strong>${K(e?.company_name??`unknown company`)}</strong>
        <span>${K(n)} -> ${K(r)}</span>
        ${i}
      </div>
      <span class="metrics-status-pill">${K(t)}</span>
    </article>
  `}async function Sr(){ut.hidden=!1,document.body.classList.add(`metrics-open`),dt.focus(),pn?yr(pn):(ft.textContent=`loading metrics...`,ft.classList.remove(`is-empty`),pt.innerHTML=``,mt.innerHTML=``,ht.innerHTML=``);try{await wr()}catch{ft.textContent=`could not load metrics.`}}function Cr(){ut.hidden=!0,document.body.classList.remove(`metrics-open`),lt.focus()}async function wr(){let e=await fetch(`/api/metrics`);if(!e.ok)throw Error(`Metrics request failed`);yr(await e.json())}function Tr(e,t=``){mn=e;let n=Number(e?.role_count??0),r=Array.isArray(e?.links)?e.links:[],i=Array.isArray(e?.paths)?e.paths:[];yt.textContent=t||(e?.updated_at?`${n.toLocaleString()} roles | updated ${U(e.updated_at)}`:``),yt.classList.toggle(`is-empty`,!yt.textContent),bt.innerHTML=r.length?Er(e):`<p class="empty-copy">no role transitions recorded yet.</p>`,xt.innerHTML=i.length?i.map(Ar).join(``):`<p class="empty-copy">no role paths recorded yet.</p>`}function Er(e){let t=Array.isArray(e?.nodes)?e.nodes:[],n=Array.isArray(e?.links)?e.links:[],r=kr(t,n),i=r.nodes,a=r.links,o=(r.flowLinks??n).map(e=>{let t=i.get(e.source),n=i.get(e.target),r=a.get(e);if(!t||!n||!r)return``;let o=r.width,s=n.x<t.x,c=Dr(e.target),l=r.priority?`0.42`:s?`0.28`:`0.34`,u=r.path??Or({isBacktrack:s,sourceX:t.x+t.width,sourceY:r.sourceY,targetX:n.x,targetY:r.targetY,width:o});return`
        <path class="${[`sankey-link`,s?`sankey-link-backtrack`:``,r.priority?`sankey-link-priority`:``].filter(Boolean).join(` `)}" d="${u}" fill="${r.path?`none`:c}" fill-opacity="${l}" stroke="${c}" style="stroke-width: ${r.path?o:1}px">
          <title>${K(t.label)} to ${K(n.label)}: ${Number(e.value??0).toLocaleString()}</title>
        </path>
      `}).join(``),s=Array.from(i.values()).map(e=>{let t=Number(e.history_count??e.current_count??0),n=Number(e.value??t),i=n>0?n.toLocaleString():`0`,a=e.x>r.width-180,o=a?e.x-8:e.x+e.width+8,s=Math.max(24,e.y-e.height/2-16),c=a?`end`:`start`,l=Dr(e.id);return`
        <g class="sankey-node" transform="translate(${e.x}, ${e.y-e.height/2})">
          <rect width="${e.width}" height="${e.height}" rx="7" fill="${l}" stroke="${l}"></rect>
        </g>
        <g class="sankey-node-label" transform="translate(${o}, ${s})">
          <text text-anchor="${c}">${K(e.label)}</text>
          <text class="sankey-node-count" y="16" text-anchor="${c}">${K(i)} roles</text>
        </g>
      `}).join(``);return`
    <svg class="sankey-svg" viewBox="0 0 ${r.width} ${r.height}" role="img" aria-label="role state transition sankey diagram">
      <g>${o}</g>
      <g>${s}</g>
    </svg>
  `}function Dr(e){return Pt.get(String(e).toLowerCase())??`#4f6472`}function Or({isBacktrack:e,sourceX:t,sourceY:n,targetX:r,targetY:i,width:a}){let o=a/2,s=n-o,c=n+o,l=i-o,u=i+o;if(e){let e=Math.max(80,Math.abs(t-r)*.42);return[`M ${t} ${s}`,`C ${t-e} ${s}, ${r+e} ${l}, ${r} ${l}`,`L ${r} ${u}`,`C ${r+e} ${u}, ${t-e} ${c}, ${t} ${c}`,`Z`].join(` `)}let ee=Math.max(46,(r-t)*.48);return[`M ${t} ${s}`,`C ${t+ee} ${s}, ${r-ee} ${l}, ${r} ${l}`,`L ${r} ${u}`,`C ${r-ee} ${u}, ${t+ee} ${c}, ${t} ${c}`,`Z`].join(` `)}function kr(e,r){let i=new Map([[`discovered`,0],[`interested`,1],[`disinterested`,2],[`applied`,2],[`oa`,3],[`interview`,3],[`rejected`,4],[`closed`,4],[`archived`,4]]),a=new Map,o=new Map;r.forEach(e=>{a.set(e.target,(a.get(e.target)??0)+Number(e.value??0)),o.set(e.source,(o.get(e.source)??0)+Number(e.value??0))});let s=e.filter(e=>Number(e?.history_count??e?.current_count??0)>0||a.has(e.id)||o.has(e.id)),c=new Set(s.map(e=>e.id)),l=r.filter(e=>c.has(e.source)&&c.has(e.target)&&Number(e.value??0)>0),u=e=>i.get(String(e).toLowerCase())??0,ee=l.filter(e=>u(e.target)>=u(e.source)),te=l.filter(e=>u(e.target)<u(e.source)),ne={nodes:s.map(e=>({...e,fixedValue:Math.max(0,Number(e?.history_count??e?.current_count??0))})),links:ee.map(e=>({...e}))},d=t().nodeId(e=>e.id).nodeWidth(26).nodePadding(44).nodeAlign((e,t)=>Math.min(t-1,u(e.id))).extent([[92,88],[1014,634]]).iterations(32)(ne),re=new Map;d.nodes.forEach(e=>{re.set(e.id,{...e,x:e.x0,y:e.y0+(e.y1-e.y0)/2,width:e.x1-e.x0,height:Math.max(1.5,e.y1-e.y0),value:Number(e.fixedValue??e.value??0)})});let f=new Map,p=[],ie=n();d.links.forEach(e=>{let t={source:e.source.id,target:e.target.id,value:e.value};p.push(t),f.set(t,{path:ie(e),width:Math.max(1.5,e.width),sourceY:e.y0,targetY:e.y1,priority:Number(e.value??0)>=20})});let ae=Math.max(.6,...d.links.map(e=>Number(e.width??0)/Math.max(1,Number(e.value??0))));return te.forEach(e=>{let t=re.get(e.source),n=re.get(e.target);if(!t||!n)return;let r=Math.max(1.5,Number(e.value??0)*ae),i={...e};p.push(i),f.set(i,{width:r,sourceY:t.y+t.height/2-r/2,targetY:n.y+n.height/2-r/2,priority:!1})}),p.sort((e,t)=>Number(e.value??0)-Number(t.value??0)),{flowLinks:p,height:720,links:f,nodes:re,width:1120}}function Ar(e){let t=Array.isArray(e?.path)?e.path:[];return`
    <article class="sankey-path-row">
      <div>
        <strong>${K(e?.company_name??`unknown company`)} / ${K(e?.title??`untitled role`)}</strong>
        <span>${t.map(e=>K(e)).join(` -> `)}</span>
      </div>
      <span class="metrics-status-pill">${Number(e?.loops_collapsed??0).toLocaleString()} loops</span>
    </article>
  `}async function jr(){Ye.hidden=!0,document.body.classList.remove(`settings-open`),_t.hidden=!1,document.body.classList.add(`sankey-open`),vt.focus(),mn?Tr(mn):(yt.textContent=`loading role flow...`,yt.classList.remove(`is-empty`),bt.innerHTML=``,xt.innerHTML=``);try{await Nr()}catch{yt.textContent=`could not load role flow.`}}function Mr(){_t.hidden=!0,document.body.classList.remove(`sankey-open`),Je.focus()}async function Nr(){let e=await fetch(`/api/role-sankey`);if(!e.ok)throw Error(`Role sankey request failed`);Tr(await e.json())}async function Pr(e){let t=e.name;if(!t)return;let n=e.type===`checkbox`?!e.checked:fn?.settings?.find(e=>e.key===t)?.value,r=e.type===`checkbox`?e.checked:e.value;fr(!0),b.textContent=`saving settings...`,b.classList.remove(`is-empty`);try{let e=await fetch(`/api/config`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({[t]:r})});if(!e.ok)throw Error(`Config update failed`);J(await e.json(),`settings saved.`)}catch{e.type===`checkbox`?e.checked=n:n!==void 0&&(e.value=n),b.textContent=`could not save settings.`,fr(!1)}}async function Fr(){ct.disabled=!0,b.textContent=`clearing recommendation history...`,b.classList.remove(`is-empty`);try{let e=await fetch(`/api/recommendation-history/clear`,{method:`POST`});if(!e.ok)throw Error(`Recommendation history clear failed`);let t=await e.json();J(t.config,`cleared ${t.deleted_count} saved decisions.`)}catch{b.textContent=`could not clear recommendation history.`,ct.disabled=!1}}async function Ir(){let e=rt.value.trim();if(!e){b.textContent=`central api url is required.`,b.classList.remove(`is-empty`);return}let t={central_api_url:e},n=it.value.trim();n&&(t.central_passkey=n),fr(!0),b.textContent=`saving central settings...`,b.classList.remove(`is-empty`);try{let e=await fetch(`/api/config`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(t)});if(!e.ok)throw Error(`Central settings update failed`);J(await e.json(),`central settings saved.`)}catch{b.textContent=`could not save central settings.`,fr(!1)}}async function Lr(){ot.disabled=!0,b.textContent=`syncing remote company ids...`,b.classList.remove(`is-empty`);try{let e=await fetch(`/api/central/resolve-companies`,{method:`POST`});if(!e.ok)throw Error(`Central company sync failed`);let t=await e.json(),n=t.result??{},r=t.pulled_companies,i=r?` remote: ${Number(r.created??0)} created, ${Number(r.linked??0)} linked, ${Number(r.existing??0)} existing.`:``;J(t.config,`company sync: ${Number(n.linked??0)} matched, ${Number(n.created??0)} created, ${Number(n.needs_review??0)} review, ${Number(n.failed??0)} failed.${i}`),t.companies&&(V=t.companies,Ur(t.companies.companies))}catch{b.textContent=`could not sync companies.`,ot.disabled=!rt.value.trim()}}async function Rr(){let e=await fetch(`/api/central/resolve-companies`,{method:`POST`});if(!e.ok)throw Error(`Central company sync failed`);let t=await e.json();t.companies&&(V=t.companies,Ur(t.companies.companies))}async function zr(){await Promise.all([mi().catch(()=>{i.innerHTML=`<p class="empty-copy">could not load jobs.</p>`}),Zr().catch(()=>{At.textContent=`could not load companies.`})])}function Br(){window.setTimeout(()=>{Rr().catch(()=>{})},1e4)}async function Vr(){if(window.confirm(`Update callumployed and restart the tracker?`)){fr(!0),St.disabled=!0,b.textContent=`updating callumployed; tracker will restart shortly...`,b.classList.remove(`is-empty`);try{if(!(await fetch(`/api/app/update`,{method:`POST`})).ok)throw Error(`App update failed`);b.textContent=`update started. reconnect in a moment.`}catch{b.textContent=`could not start update.`,fr(!1)}}}function Hr(e,t=``){V=e;let n=Array.isArray(e?.companies)?e.companies:[];if(Ur(n),S.textContent=t||`${n.length} ${n.length===1?`company`:`companies`} stored`,S.classList.toggle(`is-empty`,n.length===0&&!t),n.length===0){C.innerHTML=`<p class="empty-copy">no companies yet.</p>`;return}C.innerHTML=n.map(e=>Wr(e)).join(``)}function Ur(e){hn=Array.isArray(e)?e:[],kt.innerHTML=hn.map(e=>`<option value="${W(e.name)}"></option>`).join(``)}function Wr(e){let t=Array.isArray(e.career_pages)?e.career_pages:[],n=U(e.updated_at),r=Gr(e.prestige_tier),i=Number(e.scan_count??0),a=Number(e.discovered_role_count??0),o=i>0&&a===0?`<span class="company-discovery-status">Discovered 0 potential roles</span>`:``;return`
    <details class="company-panel ${r}" data-company-id="${e.id}">
      <summary class="company-summary">
        <span class="company-chevron">></span>
        <span class="company-summary-main">
          <span class="company-name">${K(e.name)}</span>
          <span class="company-summary-meta">${t.length} ${t.length===1?`link`:`links`}${n?` | updated ${K(n)}`:``}</span>
          ${o}
        </span>
      </summary>
      <div class="company-body">
        <div class="company-info">
          <label class="company-notes-field">
            <span>notes</span>
            <textarea data-company-notes="${e.id}" rows="3">${W(e.notes??``)}</textarea>
          </label>
          <label>
            <span>tier</span>
            <select data-company-tier="${e.id}">
              ${Kr(e.prestige_tier)}
            </select>
          </label>
          <div>
            <span>browser wait</span>
            <strong>${Number(e.browser_extra_wait_ms??0)}ms</strong>
          </div>
        </div>
        <div class="company-links">
          ${t.length>0?t.map(e=>qr(e)).join(``):`<p class="company-empty-links">no career links yet.</p>`}
        </div>
        <section class="company-link-panel" aria-label="add career link">
          <form class="company-link-form" data-company-link-form="${e.id}">
            <input name="label" type="text" placeholder="label" aria-label="career link label" />
            <input name="url" type="url" placeholder="https://..." aria-label="career link url" required />
            <button class="company-link-add" type="submit" aria-label="add career link" title="add career link">
              ${wn()}
            </button>
          </form>
        </section>
        <div class="company-danger-row">
          <button class="company-delete-button" type="button" data-delete-company="${e.id}">
            ${Tn()}
            <span>deactivate company</span>
          </button>
        </div>
      </div>
    </details>
  `}function Gr(e){let t=String(e??``);return[`0`,`1`,`2`,`3`,`4`].includes(t)?`company-tier-${t}`:`company-tier-unset`}function Kr(e){let t=String(e??``);return[``,`0`,`1`,`2`,`3`,`4`].map(e=>{let n=e?`tier ${e}`:`not set`,r=e===t?` selected`:``;return`<option value="${W(e)}"${r}>${K(n)}</option>`}).join(``)}function qr(e){let t=e.label?K(e.label):`career page`,n=W(e.url);return`
    <div class="company-link-row" data-career-page-id="${e.id}">
      <a class="company-link-url" href="${n}" target="_blank" rel="noreferrer">
        <span class="company-link-label">${t}</span>
        <span class="company-link-text">${W(e.url)}</span>
      </a>
      <button class="company-link-delete" type="button" data-delete-career-page="${e.id}" aria-label="delete ${t} link" title="delete link">
        ${Tn()}
      </button>
    </div>
  `}async function Jr(){Ct.hidden=!1,document.body.classList.add(`companies-open`),wt.focus(),V?Hr(V):(S.textContent=`loading companies...`,S.classList.remove(`is-empty`),C.innerHTML=``);try{await Xr()}catch{S.textContent=`could not load companies.`}}function Yr(){Ct.hidden=!0,document.body.classList.remove(`companies-open`),Le.focus()}async function Xr(e=``){let t=await fetch(`/api/companies`);if(!t.ok)throw Error(`Companies request failed`);Hr(await t.json(),e)}async function Zr(){let e=await fetch(`/api/companies`);if(!e.ok)throw Error(`Companies request failed`);Ur((await e.json()).companies)}async function Qr(e){let t=new FormData(e),n={name:String(t.get(`name`)??``),career_url:String(t.get(`career_url`)??``),notes:String(t.get(`notes`)??``)};S.textContent=`adding company...`;let r=await fetch(`/api/companies`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(n)});if(!r.ok)throw Error(`Company create failed`);e.reset(),Hr(await r.json(),`company added.`),mi(H()).catch(()=>{})}async function $r(e){let t=e.dataset.companyLinkForm;if(!t)return;let n=new FormData(e),r={label:String(n.get(`label`)??``),url:String(n.get(`url`)??``)};S.textContent=`adding link...`;let i=await fetch(`/api/companies/${encodeURIComponent(t)}/career-pages`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(r)});if(!i.ok)throw Error(`Career page create failed`);e.reset(),Hr(await i.json(),`link added.`)}async function ei(e){S.textContent=`deleting link...`;let t=await fetch(`/api/company-career-pages/${encodeURIComponent(e)}`,{method:`DELETE`});if(!t.ok)throw Error(`Career page delete failed`);Hr(await t.json(),`link deleted.`)}async function ti(e){S.textContent=`deactivating company...`;let t=await fetch(`/api/companies/${encodeURIComponent(e)}`,{method:`DELETE`});if(!t.ok)throw Error(`Company deactivate failed`);Hr(await t.json(),`company deactivated.`),mi(H()).catch(()=>{})}function ni(){let e=Ot.value.trim().toLocaleLowerCase();return hn.find(t=>t.name.toLocaleLowerCase()===e)}async function ri(e){let t=ni();if(!t?.id){At.textContent=`pick a saved company.`;return}let n=new FormData(e),r={company_id:t.id,role_url:String(n.get(`role_url`)??``)};At.textContent=`adding role...`;let i=await fetch(`/api/roles`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(r)});if(!i.ok)throw Error(`Role create failed`);let a=await i.json();a.tracker?er(a.tracker):await mi(H()),Dt.value=``;let o=a.role?.title?G(a.role.title):`role`;At.textContent=a.scan_error?`${o} added; scan could not finish.`:`${o} added.`}function ii(e){return(Array.isArray(V?.companies)?V.companies:[]).find(t=>String(t.id)===String(e))}function ai(e){S.textContent=e,S.classList.remove(`is-empty`)}function oi(e){window.clearTimeout(gn.get(e)),gn.set(e,window.setTimeout(()=>{si(e).catch(()=>{ai(`could not save company.`)})},700))}async function si(e){let t=C.querySelector(`[data-company-id="${CSS.escape(String(e))}"]`);if(!t)return;let n=t.querySelector(`[data-company-notes="${CSS.escape(String(e))}"]`),r=t.querySelector(`[data-company-tier="${CSS.escape(String(e))}"]`),i=ii(e),a={notes:n?.value??i?.notes??``,prestige_tier:r?.value??i?.prestige_tier??``};i&&(i.notes=a.notes,i.prestige_tier=a.prestige_tier),ci(t,a.prestige_tier),ai(`saving company...`);let o=await fetch(`/api/companies/${encodeURIComponent(e)}`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(a)});if(!o.ok)throw Error(`Company update failed`);V=await o.json(),ai(`company saved.`),li(e)}function ci(e,t){e.classList.remove(`company-tier-unset`,`company-tier-0`,`company-tier-1`,`company-tier-2`,`company-tier-3`,`company-tier-4`),e.classList.add(Gr(t))}function li(e){let t=C.querySelector(`[data-company-id="${CSS.escape(String(e))}"]`),n=ii(e);if(!t||!n)return;let r=Array.isArray(n.career_pages)?n.career_pages:[],i=U(n.updated_at),a=t.querySelector(`.company-summary-meta`);a&&(a.textContent=`${r.length} ${r.length===1?`link`:`links`}${i?` | updated ${i}`:``}`)}async function ui(){let e=await fetch(`/api/scan/status`);if(e.status===404){v.disabled=!0,y.hidden=!0,y.classList.add(`scan-error`),Re.textContent=`restart server to enable scanning`;return}if(!e.ok)throw Error(`Scan status request failed`);tr(await e.json())}function di(){ln===null&&(ln=window.setInterval(()=>{ui().catch(()=>{})},3e3))}async function fi(){v.disabled=!0,v.textContent=`starting...`;try{let e=await fetch(`/api/scan/all`,{method:`POST`});if(e.status===404){v.disabled=!0,v.textContent=`scan roles`,y.hidden=!0,y.classList.add(`scan-error`),Re.textContent=`restart server to enable scanning`;return}if(!e.ok&&e.status!==409)throw Error(`Scan start failed`);tr(await e.json()),di()}catch{v.disabled=!1,v.textContent=`scan roles`,y.hidden=!0,y.classList.add(`scan-error`),Re.textContent=`could not start scan`}}async function pi(){v.disabled=!0,v.textContent=`cancelling...`;try{let e=await fetch(`/api/scan/cancel`,{method:`POST`});if(e.status===404){v.disabled=!0,v.textContent=`scan roles`,y.hidden=!0,y.classList.add(`scan-error`),Re.textContent=`restart server to enable scanning`;return}if(!e.ok&&e.status!==409)throw Error(`Scan cancel failed`);tr(await e.json()),di()}catch{v.disabled=!1,v.textContent=`cancel scan`,y.hidden=!1,y.classList.add(`scan-error`),Re.textContent=`could not cancel scan`}}async function mi(e=``){i.innerHTML=`<p class="empty-copy">loading jobs...</p>`;let t=new URLSearchParams;e&&t.set(`q`,e);let n=await fetch(`/api/tracker?${t.toString()}`);if(!n.ok)throw Error(`Tracker request failed`);er(await n.json())}async function hi(e={}){let t=await fetch(`/api/application-materials`);if(!t.ok)throw Error(`Application materials request failed`);Fn(await t.json(),e)}async function gi(e){if(e){if(!e.name.toLowerCase().endsWith(`.tex`)){kn(Lt,`resume must be a .tex file.`);return}ie.disabled=!0,kn(Lt,`uploading...`);try{let t=await e.text();if(!(await fetch(`/api/master-resume`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({filename:e.name,content:t})})).ok)throw Error(`Master resume upload failed`);await hi()}catch{kn(Lt,`could not save resume.`),In()}finally{p.value=``,ie.disabled=!1}}}async function _i(e){let t=Array.from(e??[]);if(t.length!==0){se.disabled=!0,Pn(T,`uploading ${t.length} ${t.length===1?`resource`:`resources`}...`);try{for(let e of t)if(!(await fetch(`/api/resume-resources`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({filename:e.name,content_base64:await bi(e)})})).ok)throw Error(`Resume resource upload failed`);await hi()}catch{Pn(T,`could not save every resource.`),In()}finally{oe.value=``,se.disabled=!1}}}async function vi(e){let t=Array.from(e??[]);if(t.length!==0){de.disabled=!0,jn(E,`uploading ${t.length} ${t.length===1?`example`:`examples`}...`);try{for(let e of t){let t={filename:e.name};if([`.pdf`,`.docx`].some(t=>e.name.toLowerCase().endsWith(t))?t.content_base64=await bi(e):t.content=await e.text(),!(await fetch(`/api/cover-letter-examples`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(t)})).ok)throw Error(`Cover letter example upload failed`)}await hi()}catch{jn(E,`could not save every example.`),In()}finally{ue.value=``,de.disabled=!1}}}async function yi(e){let t=Array.from(e??[]);if(t.length!==0){he.disabled=!0,Mn(D,`uploading ${t.length} ${t.length===1?`note`:`notes`}...`);try{for(let e of t){let t=e.name.toLowerCase(),n={filename:e.name};if(t.endsWith(`.pdf`)||t.endsWith(`.docx`)?n.content_base64=await bi(e):n.content=await e.text(),!(await fetch(`/api/experience-notes`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(n)})).ok)throw Error(`Experience note upload failed`)}A.clear(),await hi()}catch{Mn(D,`could not save every note.`),In()}finally{me.value=``,he.disabled=!1}}}function bi(e){return new Promise((t,n)=>{let r=new FileReader;r.addEventListener(`load`,()=>{let e=String(r.result??``);t(e.includes(`,`)?e.split(`,`,2)[1]:e)}),r.addEventListener(`error`,()=>n(r.error)),r.readAsDataURL(e)})}c.addEventListener(`submit`,e=>{e.preventDefault(),mi(l.value.trim()),yn()}),a.addEventListener(`click`,()=>{if(H()){mi();return}vn()}),l.addEventListener(`keydown`,e=>{e.key===`Escape`&&(e.stopPropagation(),yn())}),u.addEventListener(`click`,yn),s.addEventListener(`click`,yn),ie.addEventListener(`click`,()=>{p.click()}),p.addEventListener(`change`,()=>{gi(p.files?.[0])}),se.addEventListener(`click`,()=>{oe.click()}),oe.addEventListener(`change`,()=>{_i(oe.files)}),de.addEventListener(`click`,()=>{ue.click()}),ue.addEventListener(`change`,()=>{vi(ue.files)}),he.addEventListener(`click`,()=>{me.click()}),me.addEventListener(`change`,()=>{yi(me.files)}),te.addEventListener(`click`,()=>{Ln(te.getAttribute(`aria-expanded`)===`true`)});async function xi(e){e.disabled=!0;let t=e.textContent;e.textContent=`opening...`;try{if(!(await fetch(`/api/application-materials/index/open`,{method:`POST`})).ok)throw Error(`Could not open the application material index.`)}catch(e){_e.hidden=!1,_e.textContent=e instanceof Error?e.message:`Could not open the application material index.`}finally{e.disabled=!1,e.textContent=t}}ne.addEventListener(`click`,e=>{let t=e.target.closest(`[data-open-material-index]`);if(t){xi(t);return}let n=e.target.closest(`[data-material-view]`);if(n){Bn(n);return}let r=e.target.closest(`[data-material-remove]`);r&&Vn(r)}),v.addEventListener(`click`,()=>{if(dn?.scanning){pi();return}fi()}),i.addEventListener(`click`,e=>{let t=e.target.closest(`[data-view-role-info]`);if(t){try{Pi(t.dataset.viewRoleInfo)}catch{window.alert(`Could not load role information.`)}return}let n=e.target.closest(`[data-review-role-id]`);if(n){Ni(n.dataset.reviewRoleId);return}let r=e.target.closest(`[data-prep-role-id]`);if(r){Li(r.dataset.prepRoleId);return}let i=e.target.closest(`[data-autoprep-role-id]`);if(i){let e=Mi().find(e=>String(e.id)===String(i.dataset.autoprepRoleId));if(e?.autoprep_started){Oa(e.id).catch(()=>{qe.textContent=`could not open that prepared role. try again.`});return}ka(i.dataset.autoprepRoleId).catch(()=>{qe.textContent=`could not add that role to Autoprep. try again.`});return}let a=e.target.closest(`.job-action`);if(a){Si(a);return}let o=e.target.closest(`.pane-toggle`);if(!o)return;let s=o.parentElement.querySelector(`.pane-body`),c=o.getAttribute(`aria-expanded`)===`true`;o.setAttribute(`aria-expanded`,String(!c)),o.querySelector(`.chevron`).textContent=c?`>`:`v`,s.hidden=c,uo()});async function Si(e){let{roleId:t,status:n}=e.dataset;if(!t||!n)return;let r=e.closest(`.job-actions`),i=e.closest(`.job`);r.querySelectorAll(`button`).forEach(e=>{e.disabled=!0}),e.textContent=`updating...`;try{let e=await fetch(`/api/roles/${encodeURIComponent(t)}/status`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({status:n})});if(!e.ok)throw Error(`Status update failed`);Ci((await e.json()).role,i)}catch{r.querySelectorAll(`button`).forEach(e=>{e.disabled=!1}),e.textContent=n===`disinterested`?`disinterested`:n.toLowerCase()}}function Ci(e,t){if(!e||!w)return;let n=t?.closest(`.status-pane`)?.dataset.bucket??e.role_status,r=e.role_status,i=Ti(e,n,r);Ei(n,r),Di(n,r),On(),Ai(w.statuses),Oi(t,i,n,r),uo()}function wi(e){if(!e||!w)return null;let t=null;return w.statuses.forEach(n=>{let r=n.jobs.findIndex(t=>String(t.id)===String(e.id));r!==-1&&(t={...n.jobs[r],...e},n.jobs[r]=t)}),Ai(w.statuses),t}function Ti(e,t,n){let r=e;w.statuses.forEach(t=>{let n=t.jobs.findIndex(t=>String(t.id)===String(e.id));n!==-1&&(r={...t.jobs[n],...e},t.jobs.splice(n,1),t.count=t.jobs.length)});let i=w.statuses.find(e=>e.key===n);return i&&(i.jobs.unshift(r),i.count=i.jobs.length),r}function Ei(e,t){w.statuses.forEach(e=>{let t=document.querySelector(`#status-${CSS.escape(e.key)}`);t?.classList.toggle(`empty`,e.count===0);let n=t?.querySelector(`.count`);n&&(n.textContent=e.count)}),[e,t].forEach(e=>{ki(document.querySelector(`#status-${CSS.escape(e)}`))})}function Di(e,t){if(!w.stats)return;let n=Nt.has(e),r=Nt.has(t);if(n===r){Dn(w.stats);return}w.stats.applications_total=Number(w.stats.applications_total??0)+(r?1:-1),Dn(w.stats)}function Oi(e,t,n,r){let i=document.querySelector(`#status-${CSS.escape(r)}`),a=i?.querySelector(`.pane-body`);if(!e||!i||!a)return;e.remove(),ki(document.querySelector(`#status-${CSS.escape(n)}`)),a.hidden=!1;let o=i.querySelector(`.pane-toggle`);o?.setAttribute(`aria-expanded`,`true`);let s=o?.querySelector(`.chevron`);s&&(s.textContent=`v`);let c=a.querySelector(`.jobs`);c||=(a.innerHTML=`<div class="jobs"></div>`,a.querySelector(`.jobs`)),c.insertAdjacentHTML(`afterbegin`,Un(t,r)),ki(i)}function ki(e){if(!e)return;let t=e.querySelector(`.pane-body`);if(!t)return;let n=t.querySelector(`.jobs`),r=!!n?.querySelector(`.job`),i=t.querySelector(`.empty-copy`);if(r){i?.remove();return}n?.remove(),i||t.insertAdjacentHTML(`beforeend`,`<p class="empty-copy">no jobs in this status.</p>`)}function Ai(e){ye.disabled=ji(e).length===0,ye.setAttribute(`aria-label`,`review discovered`),ye.innerHTML=`<span class="review-discovered-label">review discovered</span>`}function ji(e=w?.statuses??[]){return e.find(e=>e.key===`discovered`)?.jobs??[]}function Mi(e=w?.statuses??[]){return e.find(e=>e.key===`interested`)?.jobs??[]}function Ni(e=null){let t=[...ji()],n=e==null?null:String(e);if(n){let e=t.findIndex(e=>String(e.id)===n);if(e>0){let[n]=t.splice(e,1);t.unshift(n)}}O=t,m.hidden=!1,document.body.classList.add(`review-open`),zi()}function Pi(e){let t=String(e),n=(w?.statuses??[]).flatMap(e=>e.jobs??[]).find(e=>String(e.id)===t);if(!n)throw Error(`Role information not found`);xe.innerHTML=`
    <div class="review-title-row">
      <p class="review-company">${K(n.company_name)}</p>
      <p class="review-role-title">${K(n.title)}</p>
    </div>
    <dl class="review-details review-primary-details">
      ${Y(`location`,n.location,!1,`review-location-detail`)}
      ${Y(`first`,U(n.first_seen_at))}
      ${Y(`last`,U(n.last_seen_at))}
    </dl>
    ${Vi(n.description)}
    <dl class="review-details review-technical-details">
      ${Y(`notes`,n.notes,!1,`review-wide-detail`)}
      ${Y(`company id`,n.company_id)}
      ${Y(`role id`,n.id)}
      ${Y(`status`,n.role_status)}
      ${Y(`posting id`,n.posting_id)}
      ${Y(`created`,U(n.created_at))}
      ${Y(`updated`,U(n.updated_at))}
      ${Y(`url`,n.role_url,!1,`review-wide-detail`)}
    </dl>
  `,be.hidden=!1,document.body.classList.add(`review-open`),Se.focus()}function Fi(){be.hidden=!0,xe.innerHTML=``,document.body.classList.remove(`review-open`)}function Ii(){m.hidden=!0,document.body.classList.remove(`review-open`),O=[]}function Li(e=null){let t=[...Mi()].sort((e,t)=>Number(!!t.prep_started)-Number(!!e.prep_started)),n=e==null?null:String(e);if(n){let e=t.findIndex(e=>String(e.id)===n);if(e>0){let[n]=t.splice(e,1);t.unshift(n)}}k=t,h.hidden=!1,document.body.classList.add(`prep-open`),ta()}function Ri(){h.hidden=!0,document.body.classList.remove(`prep-open`),k=[]}function zi(e=``){let t=O[0],n=O.length,r=t?Bi(t):``;if(Ce.textContent=n>0?`review queue`:`review complete`,we.textContent=n>0?`${n} discovered ${n===1?`role`:`roles`} in queue`:``,m.querySelectorAll(`.review-action`).forEach(e=>{e.disabled=n===0}),!t){Te.innerHTML=`
      <div class="review-empty">
        <h3>no discovered jobs left.</h3>
        <p>everything in this queue has been handled or moved out of discovered.</p>
      </div>
    `;return}Te.innerHTML=`
    ${e?`<p class="review-message">${W(e)}</p>`:``}
    ${r?`<p class="review-message review-message-warning">${W(r)}</p>`:``}
    <div class="review-title-row">
      <p class="review-company">${K(t.company_name)}</p>
      ${En(t.title,t.role_url,`review-role-title`)}
    </div>
    <dl class="review-details review-primary-details">
      ${Y(`location`,t.location,!1,`review-location-detail`)}
      ${Y(`first`,U(t.first_seen_at))}
      ${Y(`last`,U(t.last_seen_at))}
    </dl>
    ${Vi(t.description)}
    <dl class="review-details review-technical-details">
      ${Y(`notes`,t.notes,!1,`review-wide-detail`)}
      ${Y(`company id`,t.company_id)}
      ${Y(`role id`,t.id)}
      ${Y(`status`,t.role_status)}
      ${Y(`posting id`,t.posting_id)}
      ${Y(`created`,U(t.created_at))}
      ${Y(`updated`,U(t.updated_at))}
      ${Y(`url`,t.role_url,!0,`review-wide-detail`)}
    </dl>
  `}function Bi(e){let t=Number(e.review_later_count??0);return t<=jt?``:`role review has been postponed ${t} times. it is recommended to set it to disinterested.`}function Y(e,t,n=!1,r=``){if(!t)return``;let i=n?`<a href="${W(t)}" target="_blank" rel="noreferrer">${K(t)}</a>`:K(t);return`
    <div class="review-detail ${W(r)}">
      <dt>${K(e)}</dt>
      <dd>${i}</dd>
    </div>
  `}function Vi(e){return e?`
    <div class="review-detail review-description">
      <dt>description</dt>
      <dd>${Hi(e)}</dd>
    </div>
  `:``}function Hi(e){let t=Ui(String(e)).replace(/\u00a0/g,` `);if(Wi(t))return Gi(t);let n=t.split(/\r?\n/).map(e=>e.trim()).filter(Boolean),r=[],i=[],a=()=>{i.length!==0&&(r.push(`<ul>${i.map(e=>`<li>${e}</li>`).join(``)}</ul>`),i=[])};return n.forEach(e=>{let t=e.match(/^#{2,3}\s+(.+)$/);if(t){a(),r.push(`<h3>${K(t[1])}</h3>`);return}if($i(e)){a(),r.push(`<h3>${K(e.replace(/:$/,``))}</h3>`);return}let n=e.match(/^[-*]\s+(.+)$/);if(n){i.push(K(n[1]));return}a(),r.push(`<p>${K(e)}</p>`)}),a(),r.join(``)}function Ui(e){let t=document.createElement(`textarea`);return t.innerHTML=e,t.value}function Wi(e){return/<\/?(?:a|br|div|em|h[1-6]|li|ol|p|span|strong|ul)\b/i.test(e)}function Gi(e){let t=document.createElement(`template`);t.innerHTML=e;let n=[];return Ki(t.content.childNodes,n),n.join(``)}function Ki(e,t){e.forEach(e=>{if(e.nodeType===Node.TEXT_NODE){let n=Zi(e.textContent);n&&t.push(`<p>${K(n)}</p>`);return}if(e.nodeType!==Node.ELEMENT_NODE)return;let n=e,r=n.tagName.toLowerCase();if(r===`script`||r===`style`||r===`br`)return;if(/^h[1-6]$/.test(r)){Ji(t,n.textContent);return}if(r===`ul`||r===`ol`){let e=Yi(n);e&&t.push(e);return}if(r===`p`){qi(n,t);return}let i=Array.from(n.children).some(e=>[`DIV`,`H1`,`H2`,`H3`,`H4`,`H5`,`H6`,`OL`,`P`,`UL`].includes(e.tagName));if([`article`,`div`,`section`].includes(r)&&i){Ki(n.childNodes,t);return}let a=Array.from(n.children).filter(e=>[`UL`,`OL`].includes(e.tagName)),o=Zi(Xi(n));if(o&&(Qi(o,n)?Ji(t,o):t.push(`<p>${K(o)}</p>`)),a.length>0){a.forEach(e=>{let n=Yi(e);n&&t.push(n)});return}!o&&i&&Ki(n.childNodes,t)})}function qi(e,t){if(!e.querySelector(`br`)){let n=Zi(Xi(e));if(!n)return;Qi(n,e)?Ji(t,n):t.push(`<p>${K(n)}</p>`);return}let n=``,r=()=>{let r=Zi(n);n=``,r&&(Qi(r,e)?Ji(t,r):t.push(`<p>${K(r)}</p>`))};e.childNodes.forEach(e=>{if(e.nodeType===Node.ELEMENT_NODE&&e.tagName.toLowerCase()===`br`){r();return}n+=` ${e.textContent??``}`}),r()}function Ji(e,t){let n=Zi(t).replace(/:$/,``);n&&e.push(`<h3>${K(n)}</h3>`)}function Yi(e){let t=Array.from(e.children).filter(e=>e.tagName===`LI`).map(e=>{let t=Zi(Xi(e)),n=Array.from(e.children).filter(e=>[`UL`,`OL`].includes(e.tagName)).map(e=>Yi(e)).filter(Boolean).join(``);return t||n?`<li>${K(t)}${n}</li>`:``}).filter(Boolean);return t.length>0?`<ul>${t.join(``)}</ul>`:``}function Xi(e){let t=e.cloneNode(!0);return t.querySelectorAll(`ul, ol`).forEach(e=>{e.remove()}),t.textContent}function Zi(e){return String(e??``).replace(/\s+/g,` `).trim()}function Qi(e,t){let n=e.replace(/:$/,``).trim();return!n||n.length>90?!1:$i(n)||/:$/.test(e)?!0:/[.!?]$/.test(n)||n.split(/\s+/).length>10?!1:t.querySelector(`strong, b, u`)?!0:$i(n)}function $i(e){return Ft.test(String(e).trim())}async function ea(e){let t=O[0];if(!t)return;if(e===`later`){m.querySelectorAll(`.review-action`).forEach(e=>{e.disabled=!0});try{let e=await Ta(t.id);O.shift(),wi(e),zi(`moved out of this review pass.`)}catch{zi(`could not postpone that role. try again.`)}finally{m.querySelectorAll(`.review-action`).forEach(e=>{e.disabled=O.length===0})}return}if(![`interested`,`disinterested`].includes(e))return;let n=m.querySelectorAll(`.review-action`);n.forEach(e=>{e.disabled=!0});try{let n=await Ea(t.id,e);O.shift(),zi(e===`interested`?`marked interested.`:`marked disinterested.`),Ci(n,document.querySelector(`.job[data-role-id="${CSS.escape(String(t.id))}"]`))}catch{n.forEach(e=>{e.disabled=!1}),zi(`could not update that role. try again.`)}}async function ta(e=``){let t=k[0],n=k.length;De.textContent=n>0?`prep queue`:`prep complete`,Oe.textContent=n>0?`${n} interested ${n===1?`role`:`roles`} in queue`:``,h.querySelectorAll(`.review-action`).forEach(e=>{e.disabled=n===0});let r=h.querySelector(`[data-prep-action="autoprep"]`);if(r&&(r.textContent=t?.autoprep_started?`view / regenerate prep`:`autoprep`),!t){g.innerHTML=`
      <div class="review-empty">
        <h3>no interested jobs left.</h3>
        <p>everything in this queue has been prepped, moved, or postponed.</p>
      </div>
    `;return}g.innerHTML=`
    ${e?`<p class="review-message">${W(e)}</p>`:``}
    <section class="prep-role-hero" aria-label="role overview">
      <div class="review-title-row">
        <div class="prep-role-eyebrow">
          <p class="review-company">${K(t.company_name)}</p>
          <span>application workspace</span>
        </div>
        ${En(t.title,t.role_url,`review-role-title`)}
      </div>
      <dl class="review-details review-primary-details">
        ${Y(`location`,t.location,!1,`review-location-detail`)}
        ${Y(`last`,U(t.last_seen_at))}
        ${Y(`updated`,U(t.updated_at))}
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
    ${t.autoprep_started?`<p class="prep-autoprep-note">already prepped — open Prepped Roles to view or regenerate its documents.</p>`:``}
    <div class="prep-workspace">
      ${na(t)}
      ${oa(t)}
      ${ra(t.id,t.description)}
      ${ia(t)}
    </div>
  `,q(),pa(t.id).then(e=>{!e||k[0]?.id!==t.id||(j.set(t.id,e),g.querySelector(`.prep-resume`)?.replaceWith(X(na(t,{resume:e}))),q())}).catch(()=>{}),wa(t.id).then(e=>{!e||k[0]?.id!==t.id||(M.set(t.id,e),g.querySelector(`.prep-cover-letter`)?.replaceWith(X(oa(t,{coverLetter:e}))),q())}).catch(()=>{})}function na(e,t={}){let n=j.get(e.id),r=t.resume??n,i=t.tweaks??Bt.get(e.id)??``,a=`/api/roles/${encodeURIComponent(e.id)}/resume.pdf`;return t.loading?`
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
          ${r.pdf_base64?`<a class="prep-summary-action prep-cover-pdf-link" href="${W(a)}" target="_blank" rel="noreferrer">view</a>`:``}
        </div>
      </summary>
      <p class="prep-overview">${K(r.summary??`Saved resume for this role.`)}</p>
      ${sa(e)}
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
          >${W(i)}</textarea>
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
          >${W(r.latex??``)}</textarea>
        </label>
        <section class="prep-document-preview" aria-label="resume preview">
          <div class="prep-preview-heading">
            <span>document preview</span>
            <p>Updates automatically after the source is saved.</p>
          </div>
          ${r.pdf_base64?`
                <iframe class="prep-cover-pdf" title="resume PDF preview" src="${W(a)}"></iframe>
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
    `}function ra(e,t){return`
    <details class="prep-panel prep-description-panel" id="prep-description-${e}">
      <summary class="prep-analysis-header">
        <span class="prep-accordion-icon" aria-hidden="true"></span>
        <h3>description</h3>
      </summary>
      ${Vi(t)}
    </details>
  `}function ia(e,t={}){let n=t.messages??Vt.get(e.id)??[],r=!!t.loading;return`
    <details class="prep-panel prep-role-chat" id="prep-chat-${e.id}">
      <summary class="prep-analysis-header">
        <span class="prep-accordion-icon" aria-hidden="true"></span>
        <h3>chat about this role</h3>
        <span>${n.length?`${n.length} messages`:`ready`}</span>
      </summary>
      <div class="prep-role-chat-log" aria-live="polite">
        ${n.length?n.map(aa).join(``):`<p class="prep-role-chat-empty">ask about fit, risks, resume emphasis, or cover letter angle.</p>`}
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
  `}function aa(e){let t=e?.role===`assistant`?`assistant`:`user`;return`
    <article class="prep-role-chat-message prep-role-chat-message-${t}">
      <span>${t}</span>
      <p>${K(e?.content??``)}</p>
    </article>
  `}function oa(e,t={}){let n=M.get(e.id),r=t.coverLetter??n,i=t.tweaks??r?.tweaks??``,a=`/api/roles/${encodeURIComponent(e.id)}/cover-letter.pdf`;return t.loading?`
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
          ${r?.pdf_base64?`<a class="prep-summary-action prep-cover-pdf-link" href="${W(a)}" target="_blank" rel="noreferrer">view</a>`:``}
        </div>
      </summary>
      ${r?`<p class="prep-overview">${K(r.summary??`cover letter generated`)}</p>`:`<p class="prep-overview">generate a LaTeX cover letter from the resume, posting, and stored examples.</p>`}
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
                >${W(i)}</textarea>
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
                >${W(r.latex??``)}</textarea>
              </label>
              <section class="prep-document-preview" aria-label="cover letter preview">
                <div class="prep-preview-heading">
                  <span>document preview</span>
                  <p>Updates automatically after the source is saved.</p>
                </div>
                ${r.pdf_base64?`
                      <iframe class="prep-cover-pdf" title="cover letter PDF preview" src="${W(a)}"></iframe>
                    `:`<p class="prep-cover-path">PDF preview unavailable.</p>`}
              </section>
            </div>
          `:``}
    </details>
  `}function sa(e,t={}){let n=A.get(e.id);if(!t.loading&&!t.error&&!t.analysis&&n)return sa(e,{analysis:n});if(!t.loading&&!t.error&&!t.analysis)return`
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
      <p class="prep-verdict">${K(a)}</p>
      <p class="prep-overview">${K(r?.overview??`analysis unavailable`)}</p>
      ${s?`
            <article class="prep-feedback" data-feedback-index="${o}">
              <p class="prep-feedback-label">${K(s.label)}</p>
              <h4>${K(s.title)}</h4>
              <p>${K(s.detail)}</p>
              ${ca(s)}
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
  `}function ca(e){return e?.tweak_prompt?`
    <div class="prep-proposed-edit">
      <p class="prep-proposed-label">tweak prompt</p>
      <p>${K(e.tweak_prompt)}</p>
    </div>
  `:`
      <div class="prep-proposed-edit">
        <p class="prep-proposed-label">feedback only</p>
        <p>not enough information to turn this into a safe resume tweak.</p>
      </div>
    `}async function la(e,t={}){if(!t.force&&A.has(e))return A.get(e);let n=await fetch(`/api/roles/${encodeURIComponent(e)}/prep-analysis`);if(!n.ok)throw Error(`Prep analysis request failed`);let r=await n.json();return r.analysis.resources=r.resources??[],A.set(e,r.analysis),r.analysis}function X(e){let t=document.createElement(`template`);return t.innerHTML=e.trim(),t.content.firstElementChild}async function ua(e){let t=k[0];if(!t)return;let n=h.querySelectorAll(`.review-action`);if(n.forEach(e=>{e.disabled=!0}),e===`later`){try{await Ta(t.id),t.review_later_count=Number(t.review_later_count??0)+1,k.length>1?(k.push(k.shift()),ta(`moved to the back of the prep queue.`)):ta(`only one role is in the prep queue.`)}catch{ta(`could not postpone prep. try again.`)}return}if(e===`autoprep`){try{if(t.autoprep_started){await Oa(t.id);return}await ka(t.id)}catch{ta(`could not add that role to Autoprep. try again.`)}return}if(e===`applied`)try{let e=await Ea(t.id,`applied`);k.shift(),ta(`moved to applied.`),Ci(e,document.querySelector(`.job[data-role-id="${CSS.escape(String(t.id))}"]`))}catch{n.forEach(e=>{e.disabled=!1}),ta(`could not move that role. try again.`)}}async function da(e,t,n,r){let i=await fetch(`/api/roles/${encodeURIComponent(e)}/prep-feedback`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({feedback_index:t,feedback_item:n,comment:r})});if(!i.ok)throw Error(`Prep feedback update failed`);return i.json()}async function fa(e,t,n,r){let i=await fetch(`/api/roles/${encodeURIComponent(e)}/prep-feedback-ignore`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({feedback_index:t,feedback_item:n,comment:r})});if(!i.ok)throw Error(`Prep feedback ignore failed`);return i.json()}async function pa(e,{force:t=!1}={}){if(!t&&j.has(e))return j.get(e);let n=await fetch(`/api/roles/${encodeURIComponent(e)}/resume`);if(!n.ok)throw Error(`Resume request failed`);let r=await n.json();return r.resume&&j.set(e,r.resume),r.resume}async function ma(e,t){let n=await fetch(`/api/roles/${encodeURIComponent(e)}/resume/save`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({latex:t})});if(!n.ok)throw Error(`Resume save failed`);return n.json()}async function ha(e,t,n){let r=await fetch(`/api/roles/${encodeURIComponent(e)}/resume`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({tweaks:t,previous_latex:n})});if(!r.ok)throw Error(`Resume generation failed`);return r.json()}async function ga(e,t){let n=await fetch(`/api/roles/${encodeURIComponent(e)}/chat`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({messages:t})});if(!n.ok)throw Error(`Role chat failed`);return n.json()}function _a(e,t,n=Mt){let r=Ht.get(e)??{timer:null,saving:!1,version:0,latex:``};r.version+=1,r.latex=t,r.timer&&clearTimeout(r.timer),r.timer=setTimeout(()=>{r.timer=null,va(e)},n),Ht.set(e,r)}async function va(e){let t=Ht.get(e);if(!t||t.saving)return;t.saving=!0;let n=t.version,r=t.latex;try{let i=await ma(e,r);t.version===n&&(j.set(e,i.resume),ya(`resume`,e,i.resume))}catch{}finally{t.saving=!1,t.version!==n&&_a(e,t.latex,0)}}function ya(e,t,n){if(!n?.pdf_base64)return;let r=e===`resume`?`[data-prep-resume-latex="${t}"]`:`[data-prep-cover-letter-latex="${t}"]`,i=g.querySelector(r)?.closest(`.prep-panel`),a=i?.querySelector(`.prep-cover-pdf`),o=i?.querySelector(`.prep-cover-pdf-link`),s=e===`resume`?`/api/roles/${encodeURIComponent(t)}/resume.pdf`:`/api/roles/${encodeURIComponent(t)}/cover-letter.pdf`;a&&(a.src=`${s}?v=${Date.now()}`),o&&(o.href=s)}async function ba(e,t=``,n=``){let r=await fetch(`/api/roles/${encodeURIComponent(e)}/cover-letter`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({tweaks:t,previous_latex:n})});if(!r.ok)throw Error(`Cover letter generation failed`);return r.json()}async function xa(e,t){let n=await fetch(`/api/roles/${encodeURIComponent(e)}/cover-letter/save`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({latex:t})});if(!n.ok)throw Error(`Cover letter save failed`);return n.json()}function Sa(e,t,n=``,r=Mt){let i=Ut.get(e)??{timer:null,saving:!1,version:0,latex:``,tweaks:``};i.version+=1,i.latex=t,i.tweaks=n,i.timer&&clearTimeout(i.timer),i.timer=setTimeout(()=>{i.timer=null,Ca(e)},r),Ut.set(e,i)}async function Ca(e){let t=Ut.get(e);if(!t||t.saving)return;t.saving=!0;let n=t.version,r=t.latex,i=t.tweaks;try{let a=await xa(e,r);t.version===n&&(M.set(e,{...a.cover_letter,tweaks:i}),ya(`coverLetter`,e,a.cover_letter))}catch{}finally{t.saving=!1,t.version!==n&&Sa(e,t.latex,t.tweaks,0)}}async function wa(e){if(M.has(e))return M.get(e);let t=await fetch(`/api/roles/${encodeURIComponent(e)}/cover-letter`);if(!t.ok)throw Error(`Cover letter request failed`);let n=await t.json();return n.cover_letter&&M.set(e,n.cover_letter),n.cover_letter}async function Ta(e){let t=await fetch(`/api/roles/${encodeURIComponent(e)}/review-later`,{method:`POST`});if(!t.ok)throw Error(`Review later update failed`);return(await t.json()).role}async function Ea(e,t){let n=await fetch(`/api/roles/${encodeURIComponent(e)}/status`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({status:t})});if(!n.ok)throw Error(`Status update failed`);return(await n.json()).role}function Da(e){return`${e}-${globalThis.crypto?.randomUUID?.()??`${Date.now()}-${Math.random()}`}`}async function Oa(e){let t=Number(e);!Number.isInteger(t)||t<=0||(P=t,h.hidden||Ri(),await ja())}async function ka(e){let t=Number(e);if(!Number.isInteger(t)||t<=0||qt.has(t))return null;qt.add(t);let n=document.querySelectorAll(`[data-autoprep-role-id="${CSS.escape(String(t))}"]`);n.forEach(e=>{e.disabled=!0,e.setAttribute(`aria-busy`,`true`),e.textContent=`queuing...`});try{let e=await fetch(`/api/autoprep/jobs`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({role_ids:[t],idempotency_key:Da(`autoprep-role-${t}`)})}),n=await e.json();if(!e.ok)throw Error(n.error||`Autoprep request failed`);let r=Array.isArray(n.jobs)?n.jobs:[],i=new Map(N.map(e=>[Number(e.role_id),e]));r.forEach(e=>i.set(Number(e.role_id),e));let a=r.find(e=>Number(e.role_id)===t),o=Mi().find(e=>Number(e.id)===t);return a&&o&&w&&(o.autoprep_started=!0,o.autoprep_status=a.overall_status??`queued`,er(w)),P=t,h.hidden||Ri(),await ja({seedJobs:[...i.values()]}),r}finally{qt.delete(t),n.forEach(e=>{e.disabled=!1,e.removeAttribute(`aria-busy`),e.textContent=Mi().find(e=>Number(e.id)===t)?.autoprep_started?`view / regenerate prep`:`autoprep`})}}function Aa(e){window.location.hash!==e&&window.history.pushState({},``,e||`${window.location.pathname}${window.location.search}`)}async function ja({seedJobs:e=null}={}){je.hidden=!1,document.body.classList.add(`prepped-open`),Aa(`#prepped-roles`),e?(N=e,P=P??N[0]?.role_id??null,Q()):N.length===0&&(Ne.textContent=`loading prepared roles...`),await Na(),Pa()}function Ma({clearHash:e=!0}={}){je.hidden=!0,document.body.classList.remove(`prepped-open`),Fa(),I.clear(),Xt.clear(),B.forEach(e=>URL.revokeObjectURL(e)),B.clear(),rn.clear(),an.clear(),e&&window.location.hash===`#prepped-roles`&&Aa(``)}window.addEventListener(`pagehide`,()=>{document.querySelectorAll(`[data-preview-blob-url]`).forEach(e=>{URL.revokeObjectURL(e.dataset.previewBlobUrl)}),B.forEach(e=>URL.revokeObjectURL(e)),B.clear(),rn.clear()});async function Na(){try{let e=await fetch(`/api/autoprep/jobs`);if(!e.ok)throw Error(`Prepped roles request failed`);let t=await e.json();N=t.jobs??[];let n=t.bulk_cover_letter_regeneration;if(n){let e=Array.isArray(n.jobs)?n.jobs:[];F={idempotencyKey:n.idempotency_key,roleIds:e.map(e=>Number(e.role_id)),jobs:e,skipped:Array.isArray(n.skipped)?n.skipped:[]}}N.some(e=>Number(e.role_id)===Number(P))||(P=N[0]?.role_id??null),Q()}catch{Ne.textContent=`could not refresh preparation progress.`}}function Pa(){Fa(),N.some(Ia)&&(Wt=window.setInterval(Na,2e3))}function Fa(){Wt!==null&&window.clearInterval(Wt),Wt=null}function Ia(e){return[`queued`,`generating_resume_tweaks`,`regenerating_resume`,`generating_cover_letter`].includes(e.overall_status)}function La(e){return[e.resume_status,e.cover_letter_status].some(e=>[`failed`,`interrupted`].includes(e))}function Ra(e){return e.cover_letter_status===`generating`||e.overall_status===`generating_cover_letter`}function za(e){return Ra(e)||e.resume_status===`generating_tweaks`||e.resume_status===`regenerating`||e.overall_status===`generating_resume_tweaks`||e.overall_status===`regenerating_resume`}function Ba(e){return e.worker_state===`queued`||e.overall_status===`queued`}function Va(e){return{queued:`Queued`,generating_resume_tweaks:`Generating resume tweaks`,regenerating_resume:`Regenerating resume`,generating_cover_letter:`Generating cover letter`,partially_complete:`Partially complete`,ready:`Ready`,failed:`Failed`,interrupted:`Interrupted`,generating_tweaks:`Generating tweaks`,regenerating:`Regenerating`,generating:`Generating`}[e]??G(e)}function Ha(e,t){let n=t===`cover-letter`?`cover_letter`:`resume`;return`${e.updated_at||``}:${e[`${n}_artifact_path`]||``}`}function Z(e,{close:t=!1}={}){let n=B.get(e);n&&URL.revokeObjectURL(n),B.delete(e),rn.delete(e),an.delete(e),t&&I.delete(e)}function Ua(){rn.forEach((e,t)=>{let[n,r]=t.split(`:`),i=N.find(e=>Number(e.role_id)===Number(n));(!i||Ha(i,r)!==e)&&Z(t,{close:!0})})}function Wa(){if(!F)return;let e=F.jobs||N,t=new Map(e.map(e=>[Number(e.role_id),e])),n=F.roleIds.map(e=>t.get(Number(e))),r=n.filter(e=>e?.worker_state===`idle`&&e.cover_letter_status===`ready`).length,i=n.filter(e=>!e||e.worker_state===`idle`&&[`failed`,`interrupted`].includes(e.cover_letter_status)),a=n.length-r-i.length,o=F.skipped.length?` Skipped before queueing: ${F.skipped.map(e=>`${e.company_name} — ${e.title}: ${e.reason}`).join(` · `)}`:``,s=i.length?` Queued regeneration failures: ${i.map(e=>e?`${e.company_name} — ${e.title}: ${e.cover_letter_error||`generation failed`}`:`A role left the Prepped queue before regeneration completed`).join(` · `)}`:``;Kt=n.length?a>0?`Cover-letter regeneration in progress: ${r} of ${n.length} complete · ${a} remaining.${o}${s}`:`Cover-letter regeneration complete: ${r} succeeded, ${i.length} failed.${o}${s}`:`No cover letters were queued.${o}`}function Q(){Ua(),Wa();let e=N.filter(Ia).length,t=N.filter(e=>e.worker_state===`idle`&&e.cover_letter_status===`ready`).length;Ne.textContent=N.length?`${N.length} prepped ${N.length===1?`role`:`roles`}${e?` · ${e} in progress`:``}`:`No queued or prepared roles.`,Pe.disabled=Gt||t===0,Pe.setAttribute(`aria-busy`,Gt?`true`:`false`),Pe.textContent=Gt?`queuing cover letters...`:`regenerate all cover letters`,Fe.textContent=Kt,Ie.innerHTML=N.map(e=>{let t=La(e),n=!t&&za(e),r=!t&&!n&&Ba(e),i=Number(e.role_id)===Number(P)?` is-active`:``;return`
      <button type="button" class="prepped-list-item${r?` is-generation-queued`:``}${n?` is-document-generating`:``}${t?` has-generation-failure`:``}${i}" data-prepped-role="${e.role_id}">
        <strong>${K(e.company_name)}</strong><span>${K(e.title)}</span>
        <small class="status-${W(e.overall_status)}">${W(Va(e.overall_status))}</small>
      </button>`}).join(``),$(),Pa()}function $(){let e=N.findIndex(e=>Number(e.role_id)===Number(P)),t=N[e];if(!t){_.innerHTML=`<div class="prepped-empty"><h3>nothing prepped yet.</h3><p>Queue Interested roles from Autoprep Interested.</p></div>`;return}let n=K(t.title),r=xn(t.role_url),i=r?`<a class="prepped-role-link" href="${W(r)}" target="_blank" rel="noopener noreferrer">${n}<span aria-hidden="true">↗</span></a>`:n,a=[[`Location`,t.location||`Unavailable`],[`Added`,U(t.date_added||t.created_at)||`Unavailable`],[`Last seen`,U(t.last_seen_at)||`Unavailable`],[`Posting ID`,t.posting_id||`Unavailable`]],o=Jt.has(Number(t.role_id)),s=o||Ia(t),c=`${t.role_id}:description`,l=`${t.role_id}:notes`;_.innerHTML=`
    <header class="prepped-detail-heading">
      <div><p class="eyebrow">${K(t.company_name)}</p><h3>${i}</h3></div>
      <span class="prepped-status status-${W(t.overall_status)}">${W(Va(t.overall_status))}</span>
    </header>
    <dl class="prepped-role-facts">${a.map(([e,t])=>`<div><dt>${W(e)}</dt><dd>${K(t)}</dd></div>`).join(``)}</dl>
    <details class="prepped-role-description" data-prepped-detail-section="description" ${Xt.has(c)?`open`:``}>
      <summary>Job description</summary>
      <div class="prepped-description-copy">${K(t.description||`No job description was saved.`).replaceAll(`
`,`<br>`)}</div>
    </details>
    ${t.notes?`<details class="prepped-role-description" data-prepped-detail-section="notes" ${Xt.has(l)?`open`:``}><summary>Role notes</summary><div class="prepped-description-copy">${K(t.notes).replaceAll(`
`,`<br>`)}</div></details>`:``}
    <div class="prepped-document-grid">
      ${to(t,`resume`,`Resume`)}
      ${to(t,`cover-letter`,`Cover letter`)}
    </div>
    ${Ka(t)}
    <div class="prepped-detail-actions">
      <button class="prepped-nav-action" type="button" data-prepped-nav="previous" ${e<=0?`disabled`:``}>Previous</button>
      <button class="prepped-nav-action" type="button" data-prepped-nav="next" ${e>=N.length-1?`disabled`:``}>Next</button>
      <button class="prepped-folder-action" type="button" data-autoprep-open-folder ${t.artifact_directory?``:`disabled`}>Open Documents Folder</button>
      <button class="prepped-disinterested" type="button" data-autoprep-disinterested aria-busy="${o?`true`:`false`}" ${s?`disabled`:``} title="${Ia(t)?`Wait for preparation to finish before moving this role`:`Move this role out of Prepped`}">${o?`Moving to Disinterested...`:`Move to Disinterested`}</button>
      <button class="success" type="button" data-autoprep-applied ${t.overall_status===`ready`?``:`disabled`}>Applied</button>
    </div>
    <p class="prepped-safety-note">Autoprep prepares files only. It never submits an application.</p>`,Qt.has(Number(t.role_id))||Ja(t.role_id)}function Ga(e){return Array.isArray(e)?e:Array.isArray(e?.answers)?e.answers:e?.answer&&typeof e.answer==`object`?[e.answer]:e?.record&&typeof e.record==`object`?[e.record]:e&&typeof e==`object`&&(`question`in e||`answer`in e||`status`in e||`error`in e)?[e]:[]}function Ka(e){let t=Number(e.role_id),n=L.get(t)??[],r=Zt.get(t)??``,i=R.has(t),a=$t.has(t),o=z.get(t);return`<section class="application-questions-workspace" aria-labelledby="application-questions-heading-${t}">
    <div class="application-questions-heading"><div><p class="eyebrow">Application helper</p><h4 id="application-questions-heading-${t}">Application questions</h4></div><span>${n.length} saved</span></div>
    <p class="application-questions-intro">Paste a question from an application form to generate and keep a role-specific answer.</p>
    <div class="application-answer-history" aria-live="polite">
      ${a&&!n.length?`<p class="application-answer-empty">Loading saved answers…</p>`:``}
      ${o?`<p class="prepped-error">${K(o)}</p>`:``}
      ${!a&&!o&&!n.length?`<p class="application-answer-empty">No application questions saved yet.</p>`:``}
      ${n.map((e,t)=>qa(e,t,i)).join(``)}
    </div>
    <div class="application-question-composer">
      <label for="application-question-${t}">Question</label>
      <textarea id="application-question-${t}" data-application-question-draft rows="4" placeholder="Paste an application question…" ${i?`disabled`:``}>${W(r)}</textarea>
      <div><small>Answers are saved to this role. Asking never changes its status.</small><button class="application-question-submit" type="button" data-application-question-submit aria-busy="${i?`true`:`false`}" ${i||!r.trim()?`disabled`:``}>${i?`Generating…`:`Generate answer`}</button></div>
    </div>
  </section>`}function qa(e,t,n){let r=e?.status??`saved`,i=e?.created_at??e?.updated_at??e?.timestamp,a=e?.backend??e?.generation_backend,o=Number(e?.id),s=Number.isFinite(o)&&r!==`pending`&&!n,c=en.has(o),l=tn.has(o),u=nn.has(o);return`<article class="application-answer-record status-${W(r)}">
    <div class="application-answer-meta"><span>${K(r)}</span>${a?`<span>${K(a)}</span>`:``}${i?`<time datetime="${W(i)}">${K(U(i)||i)}</time>`:``}</div>
    <h5>${W(e.question??`Question unavailable`)}</h5>
    ${e.answer?`<p class="application-answer-copy">${W(e.answer).replaceAll(`
`,`<br>`)}</p>`:``}
    ${e.error?`<p class="prepped-error">${K(e.error)}</p>`:``}
    <div class="application-answer-actions">
      ${e.answer?`<button type="button" data-application-answer-copy="${t}">Copy answer</button>`:``}
      ${Number.isFinite(o)?`<button type="button" data-application-answer-regenerate="${o}" ${s?``:`disabled`}>${l||r===`pending`?`Regenerating…`:`Regenerate`}</button><button class="danger" type="button" data-application-answer-delete="${o}" ${s?``:`disabled`}>${u?`Deleting…`:c?`Confirm delete`:`Delete question`}</button>`:``}
    </div>
  </article>`}async function Ja(e){let t=Number(e);if(!$t.has(t)){$t.add(t),z.delete(t);try{let n=await fetch(`/api/autoprep/roles/${encodeURIComponent(e)}/application-answers`),r=await n.json();if(!n.ok)throw Error(r?.error||`Could not load saved answers.`);L.set(t,Ga(r)),Qt.add(t)}catch(e){z.set(t,e instanceof Error?e.message:`Could not load saved answers.`)}finally{$t.delete(t),Number(P)===t&&$()}}}async function Ya(e){if(navigator.clipboard?.writeText)try{await navigator.clipboard.writeText(e);return}catch{}let t=document.createElement(`textarea`);t.value=e,t.readOnly=!0,t.style.position=`fixed`,t.style.opacity=`0`,document.body.append(t),t.select();let n=document.execCommand(`copy`);if(t.remove(),!n)throw Error(`Clipboard copy is unavailable`)}async function Xa(e){let t=Number(e),n=String(Zt.get(t)??``).trim();if(!(!n||R.has(t))){R.add(t),$();try{let r=await fetch(`/api/autoprep/roles/${encodeURIComponent(e)}/application-answers`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({question:n})}),i=await r.json(),a=Ga(i),o=L.get(t)??[];if(Array.isArray(i?.answers)?L.set(t,a):a.length&&L.set(t,[...o,...a]),!r.ok)throw Error(i?.error||a[0]?.error||`Could not generate an answer.`);Zt.delete(t),Qt.add(t),z.delete(t)}catch(e){z.set(t,e instanceof Error?e.message:`Could not generate an answer.`)}finally{R.delete(t),Number(P)===t&&$()}}}function Za(e,t){let n=Number(e),r=L.get(n)??[],i=Number(t?.id),a=r.findIndex(e=>Number(e?.id)===i);if(a<0){L.set(n,[t,...r]);return}let o=[...r];o[a]=t,L.set(n,o)}async function Qa(e,t){let n=Number(e);if(!R.has(n)){R.add(n),tn.add(Number(t)),en.delete(Number(t)),z.delete(n),$();try{let r=await fetch(`/api/autoprep/roles/${encodeURIComponent(e)}/application-answers/${encodeURIComponent(t)}/regenerate`,{method:`POST`}),i=await r.json(),[a]=Ga(i);if(a&&Za(n,a),!r.ok)throw Error(i?.error||a?.error||`Could not regenerate the answer.`)}catch(e){z.set(n,e instanceof Error?e.message:`Could not regenerate the answer.`)}finally{tn.delete(Number(t)),R.delete(n),Number(P)===n&&$()}}}async function $a(e,t){let n=Number(e),r=Number(t);if(!en.has(r)){en.add(r),$();return}if(!R.has(n)){R.add(n),nn.add(r),en.delete(r),z.delete(n),$();try{let i=await fetch(`/api/autoprep/roles/${encodeURIComponent(e)}/application-answers/${encodeURIComponent(t)}`,{method:`DELETE`}),a=await i.json();if(!i.ok)throw Error(a?.error||`Could not delete the question.`);let o=L.get(n)??[];L.set(n,o.filter(e=>Number(e?.id)!==r))}catch(e){z.set(n,e instanceof Error?e.message:`Could not delete the question.`)}finally{nn.delete(r),R.delete(n),Number(P)===n&&$()}}}async function eo(e,t){let n=`${e.role_id}:${t}`,r=Ha(e,t);if(!(rn.get(n)===r||on.has(n))){Z(n),on.add(n),an.delete(n),$();try{let i=await zn(`/api/autoprep/roles/${encodeURIComponent(e.role_id)}/documents/${t}.pdf?v=${encodeURIComponent(e.updated_at||``)}`),a=N.find(t=>Number(t.role_id)===Number(e.role_id));if(!I.has(n)||!a||Ha(a,t)!==r){URL.revokeObjectURL(i),I.delete(n);return}B.set(n,i),rn.set(n,r)}catch(e){an.set(n,e instanceof Error?e.message:`PDF preview unavailable`)}finally{on.delete(n),Number(P)===Number(e.role_id)&&$()}}}function to(e,t,n){let r=t===`cover-letter`?`cover_letter`:`resume`,i=e[`${r}_status`],a=e[`${r}_artifact_path`],o=a?.split(`/`).pop()??`Not available`,s=e[`${r}_error`],c=e[`${r}_instruction`]||``,l=`${e.role_id}:${t}`,u=Yt.get(l)??c,ee=t===`cover-letter`?`Optional comments for the next version`:`Comments for the next version`,te=t===`cover-letter`?`Optionally describe specific, truthful changes...`:`Describe specific, truthful changes...`,ne=[`failed`,`interrupted`].includes(i),d=e.worker_state!==`idle`||[`queued`,`generating`,`generating_tweaks`,`regenerating`].includes(i),re=!d&&(i===`ready`||ne)&&(ne||t===`cover-letter`||String(u).trim()),f=I.has(l),p=`/api/autoprep/roles/${encodeURIComponent(e.role_id)}/documents/${t}.pdf?v=${encodeURIComponent(e.updated_at||``)}`,ie=B.get(l),ae=an.get(l),oe=on.has(l),se=a?`<a class="prep-cover-pdf-link" data-autoprep-view="${t}" href="${W(p)}" target="_blank" rel="noreferrer" aria-label="View ${W(n.toLowerCase())} PDF in browser">View PDF</a>`:``;return`
    <section class="prepped-document${f?` has-open-preview`:``} status-${W(i)}">
      <div class="prepped-document-heading"><h4>${W(n)}</h4><span>${W(Va(i))}</span></div>
      <p class="prepped-filename">${W(o)}</p>
      ${s?`<p class="prepped-error">${W(s)}</p>`:``}
      <div class="prepped-document-actions">
        <button type="button" data-autoprep-preview="${t}" ${a?``:`disabled`}>${f?`Hide preview`:`Preview PDF`}</button>
        ${se}
      </div>
      <div class="prepped-pdf-preview" data-autoprep-preview-panel="${t}" ${f&&a?``:`hidden`}>
        ${f&&ie?`<iframe title="${W(n)} PDF preview" src="${W(ie)}"></iframe>`:``}
        ${f&&oe?`<p>Loading PDF preview...</p>`:``}
        ${f&&ae?`<p class="prepped-error">${K(ae)}</p>`:``}
      </div>
      <label class="prepped-comments-label" for="prepped-comments-${W(l)}">${ee}</label>
      <textarea id="prepped-comments-${W(l)}" data-autoprep-comments="${t}" rows="4" placeholder="${te}" ${d?`disabled`:``}>${K(u)}</textarea>
      <button class="prepped-regenerate" type="button" data-autoprep-regenerate="${t}" ${re?``:`disabled`}>${d?`Regenerating...`:`Regenerate ${W(n)}`}</button>
    </section>`}async function no(e,t,n){if(n.disabled)return;let r=`${e.role_id}:${t}`,i=e[`${t===`cover-letter`?`cover_letter`:`resume`}_status`],a=[`failed`,`interrupted`].includes(i),o=_.querySelector(`[data-autoprep-comments="${t}"]`),s=String(o?.value||Yt.get(r)||``).trim();if(!s&&t!==`cover-letter`&&!a){o?.focus();return}n.disabled=!0,n.textContent=`Queuing regeneration...`;try{let n=await fetch(`/api/autoprep/roles/${encodeURIComponent(e.role_id)}/${a?`retry`:`regenerate`}/${t}`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(a?{idempotency_key:Da(`retry-${t}`)}:{comments:s,idempotency_key:Da(`regenerate-${t}`)})}),i=await n.json();if(!n.ok)throw Error(i.error||`Regeneration request failed`);Yt.delete(r),Z(r,{close:!0});let o=N.findIndex(t=>Number(t.role_id)===Number(e.role_id));o>=0&&(N[o]=i.job),Q()}catch(e){window.alert(e instanceof Error?e.message:`Regeneration request failed`),await Na()}}async function ro(){if(!Gt){Gt=!0,F=null,Kt=`Queuing eligible cover letters...`,Q();try{let e=await fetch(`/api/autoprep/cover-letters/regenerate`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({idempotency_key:Da(`regenerate-all-cover-letters`)})}),t=await e.json();if(!e.ok)throw Error(t.error||`Bulk regeneration request failed`);let n=Number(t.queued_count||0),r=Array.isArray(t.skipped)?t.skipped:[];F={roleIds:(t.jobs||[]).map(e=>Number(e.role_id)),jobs:t.jobs||[],skipped:r},!n&&!r.length&&(F=null,Kt=`No prepped roles are available to regenerate.`),(t.jobs||[]).forEach(e=>{let t=N.findIndex(t=>Number(t.role_id)===Number(e.role_id));t>=0&&(N[t]=e),Z(`${e.role_id}:cover-letter`,{close:!0})}),await Na(),Pa()}catch(e){F=null,Kt=e instanceof Error?e.message:`Bulk regeneration request failed`}finally{Gt=!1,Q()}}}async function io(e,t){let n=Number(e);if(Jt.has(n))return;Jt.add(n),t.disabled=!0,t.setAttribute(`aria-busy`,`true`),t.textContent=`Moving to Disinterested...`;let r=N.findIndex(e=>Number(e.role_id)===n);try{await Ea(e,`disinterested`),Z(`${e}:resume`,{close:!0}),Z(`${e}:cover-letter`,{close:!0}),r>=0&&N.splice(r,1),P=N[Math.min(r,N.length-1)]?.role_id??null,Kt=`Role moved to Disinterested.`,Q(),zr()}catch(e){Kt=e instanceof Error?e.message:`Could not move this role to Disinterested.`,await Na()}finally{Jt.delete(n),N.some(e=>Number(e.role_id)===n)&&Q()}}async function ao(e,t){if(t.disabled)return;t.disabled=!0,t.textContent=`Moving to Applied...`;let n=N.findIndex(t=>Number(t.role_id)===Number(e));try{if(!(await fetch(`/api/autoprep/roles/${encodeURIComponent(e)}/applied`,{method:`POST`})).ok)throw Error(`Applied update failed`);Z(`${e}:resume`,{close:!0}),Z(`${e}:cover-letter`,{close:!0}),N.splice(n,1),P=N[Math.min(n,N.length-1)]?.role_id??null,Q(),zr()}catch{await Na()}}ye.addEventListener(`click`,Ni),Ee.addEventListener(`click`,Ii),Se.addEventListener(`click`,Fi),Ae.addEventListener(`click`,()=>ja()),Me.addEventListener(`click`,Ma),Pe.addEventListener(`click`,ro),Ie.addEventListener(`click`,e=>{let t=e.target.closest(`[data-prepped-role]`);t&&(P=Number(t.dataset.preppedRole),Q())}),_.addEventListener(`input`,e=>{let t=e.target.closest(`[data-application-question-draft]`);if(t){let e=Number(P);Zt.set(e,t.value);let n=_.querySelector(`[data-application-question-submit]`);n&&(n.disabled=!t.value.trim()||R.has(e));return}let n=e.target.closest(`[data-autoprep-comments]`);if(!n)return;let r=`${P}:${n.dataset.autoprepComments}`;Yt.set(r,n.value);let i=_.querySelector(`[data-autoprep-regenerate="${n.dataset.autoprepComments}"]`),a=N.find(e=>Number(e.role_id)===Number(P)),o=n.dataset.autoprepComments===`cover-letter`?`cover_letter`:`resume`,s=a?.[`${o}_status`],c=[`failed`,`interrupted`].includes(s);i&&(i.disabled=a?.worker_state!==`idle`||![`ready`,`failed`,`interrupted`].includes(s)||!c&&n.dataset.autoprepComments!==`cover-letter`&&!n.value.trim())}),_.addEventListener(`toggle`,e=>{let t=e.target.closest(`[data-prepped-detail-section]`);if(!t)return;let n=`${P}:${t.dataset.preppedDetailSection}`;t.open?Xt.add(n):Xt.delete(n)},!0),_.addEventListener(`click`,async e=>{let t=N.find(e=>Number(e.role_id)===Number(P));if(!t)return;if(e.target.closest(`[data-application-question-submit]`)){Xa(t.role_id);return}let n=e.target.closest(`[data-application-answer-regenerate]`);if(n){Qa(t.role_id,n.dataset.applicationAnswerRegenerate);return}let r=e.target.closest(`[data-application-answer-delete]`);if(r){$a(t.role_id,r.dataset.applicationAnswerDelete);return}let i=e.target.closest(`[data-application-answer-copy]`);if(i){let e=(L.get(Number(t.role_id))??[])[Number(i.dataset.applicationAnswerCopy)]?.answer;if(!e)return;try{await Ya(String(e)),i.textContent=`Copied`}catch{i.textContent=`Copy unavailable`}return}let a=e.target.closest(`[data-prepped-nav]`);if(a){let e=N.indexOf(t),n=a.dataset.preppedNav===`next`?1:-1;P=N[e+n]?.role_id??t.role_id,Q();return}let o=e.target.closest(`[data-autoprep-preview]`);if(o){let e=o.dataset.autoprepPreview,n=`${t.role_id}:${e}`;I.has(n)?(I.delete(n),$()):(I.add(n),$(),eo(t,e));return}let s=e.target.closest(`[data-autoprep-regenerate]`);if(s){no(t,s.dataset.autoprepRegenerate,s);return}let c=e.target.closest(`[data-autoprep-open-folder]`);if(c&&!c.disabled){c.disabled=!0,c.textContent=`Opening...`;try{if(!(await fetch(`/api/autoprep/roles/${encodeURIComponent(t.role_id)}/open-folder`,{method:`POST`})).ok)throw Error(`Could not open the documents folder.`);c.textContent=`Opened in Finder`,window.setTimeout(()=>{c.isConnected&&(c.textContent=`Open Documents Folder`,c.disabled=!1)},1500)}catch(e){c.textContent=e instanceof Error?e.message:`Could not open folder`,c.disabled=!1}return}let l=e.target.closest(`[data-autoprep-disinterested]`);if(l){io(t.role_id,l);return}let u=e.target.closest(`[data-autoprep-applied]`);u&&ao(t.role_id,u)}),ke.addEventListener(`click`,Ri),m.addEventListener(`click`,e=>{let t=e.target.closest(`[data-review-action]`);t&&ea(t.dataset.reviewAction)}),h.addEventListener(`click`,e=>{e.target.closest(`.prep-summary-action`)&&e.stopPropagation()}),h.addEventListener(`input`,e=>{let t=e.target.closest(`[data-prep-resume-tweaks]`);if(t){let e=Number(t.dataset.prepResumeTweaks);Number.isFinite(e)&&Bt.set(e,t.value);return}let n=e.target.closest(`[data-prep-resume-latex]`);if(n){let e=Number(n.dataset.prepResumeLatex);if(!Number.isFinite(e))return;_a(e,n.value);return}let r=e.target.closest(`[data-prep-cover-letter-latex]`);if(!r)return;let i=Number(r.dataset.prepCoverLetterLatex);if(!Number.isFinite(i))return;let a=r.closest(`.prep-cover-letter`)?.querySelector(`[data-prep-cover-letter-tweaks="${i}"]`)?.value??``;Sa(i,r.value,a)}),h.addEventListener(`scroll`,e=>{e.target.closest(`[data-prep-resume-latex], [data-prep-cover-letter-latex]`)},!0),h.addEventListener(`focusout`,e=>{let t=e.target.closest(`[data-prep-resume-latex]`);if(t){let e=Number(t.dataset.prepResumeLatex);if(!Number.isFinite(e))return;_a(e,t.value,0);return}let n=e.target.closest(`[data-prep-cover-letter-latex]`);if(!n)return;let r=Number(n.dataset.prepCoverLetterLatex);if(!Number.isFinite(r))return;let i=n.closest(`.prep-cover-letter`)?.querySelector(`[data-prep-cover-letter-tweaks="${r}"]`)?.value??``;Sa(r,n.value,i,0)}),h.addEventListener(`submit`,async e=>{let t=e.target.closest(`[data-prep-role-chat-form]`);if(!t||!k[0])return;e.preventDefault();let n=Number(t.dataset.prepRoleChatForm);if(!Number.isFinite(n))return;let r=t.querySelector(`[data-prep-role-chat-input="${n}"]`),i=r?.value?.trim()??``;if(!i){r?.focus();return}let a=[...Vt.get(n)??[],{role:`user`,content:i}];Vt.set(n,a),g.querySelector(`.prep-role-chat`)?.replaceWith(X(ia(k[0],{messages:a,loading:!0})));try{let e=await ga(n,a),t=[...a,e.message];Vt.set(n,t),g.querySelector(`.prep-role-chat`)?.replaceWith(X(ia(k[0],{messages:t})))}catch{let e=[...a,{role:`assistant`,content:`could not answer right now.`}];Vt.set(n,e),g.querySelector(`.prep-role-chat`)?.replaceWith(X(ia(k[0],{messages:e})))}}),h.addEventListener(`click`,async e=>{let t=e.target.closest(`[data-prep-section-target]`);if(t){let e=t.dataset.prepSectionTarget,n=e?document.getElementById(e):null;if(n instanceof HTMLDetailsElement){n.open=!0,n.scrollIntoView({behavior:`smooth`,block:`start`});let e=n.querySelector(`summary`);e?.setAttribute(`tabindex`,`-1`),e?.focus({preventScroll:!0})}return}if(e.target.closest(`[data-prep-analysis]`)&&k[0]){let e=k[0].id;g.querySelector(`.prep-analysis`)?.replaceWith(X(sa(k[0],{loading:!0})));try{let t=await la(e,{force:!0});if(k[0]?.id!==e)return;g.querySelector(`.prep-analysis`)?.replaceWith(X(sa(k[0],{analysis:t})))}catch{g.querySelector(`.prep-analysis`)?.replaceWith(X(sa(k[0],{error:!0})))}return}if(e.target.closest(`[data-prep-resume-regenerate]`)&&k[0]){let e=k[0].id,t=g.querySelector(`.prep-resume`),n=t?.querySelector(`[data-prep-resume-tweaks="${e}"]`)?.value??``,r=t?.querySelector(`[data-prep-resume-latex="${e}"]`)?.value??``;if(!n.trim()){t?.querySelector(`[data-prep-resume-tweaks="${e}"]`)?.focus();return}Bt.set(e,n),t?.replaceWith(X(na(k[0],{loading:!0})));try{let t=await ha(e,n,r);j.set(e,t.resume),g.querySelector(`.prep-resume`)?.replaceWith(X(na(k[0],{resume:t.resume}))),q()}catch{g.querySelector(`.prep-resume`)?.replaceWith(X(na(k[0],{resume:j.get(e),tweaks:n}))),q()}return}if(e.target.closest(`[data-prep-cover-letter]`)&&k[0]){let e=k[0].id,t=g.querySelector(`.prep-cover-letter`),n=t?.querySelector(`[data-prep-cover-letter-tweaks="${e}"]`)?.value??``,r=n.trim()?t?.querySelector(`[data-prep-cover-letter-latex="${e}"]`)?.value??``:``;t?.replaceWith(X(oa(k[0],{loading:!0})));try{let t=await ba(e,n,r);M.set(e,t.cover_letter),g.querySelector(`.prep-cover-letter`)?.replaceWith(X(oa(k[0],{coverLetter:t.cover_letter}))),q()}catch{g.querySelector(`.prep-cover-letter`)?.replaceWith(X(oa(k[0],{coverLetter:M.get(e),tweaks:n}))),q()}return}let n=e.target.closest(`[data-prep-action]`);if(n){ua(n.dataset.prepAction);return}let r=e.target.closest(`[data-prep-feedback]`);if(!r||!k[0])return;let i=k[0].id,a=A.get(i),o=Array.isArray(a?.feedback_items)?a.feedback_items.length:0,s=zt.get(i)??0;if(r.dataset.prepFeedback===`accept`||r.dataset.prepFeedback===`ignore`){let e=a?.feedback_items?.[s];if(!e)return;let t=g.querySelector(`[data-prep-feedback-comment]`)?.value??``,n=r.dataset.prepFeedback,o=n;r.disabled=!0,r.textContent=n===`accept`?`adding...`:`ignoring...`;try{if(n===`accept`){let n=await da(i,s,e,t),r=document.querySelector(`.job[data-role-id="${CSS.escape(String(i))}"]`);n.role&&(k[0]=n.role,Ci(n.role,r)),so(i,n.tweak_prompt??e.tweak_prompt??``),oo(i,s,a)}else await fa(i,s,e,t),oo(i,s,a)}catch{r.disabled=!1,r.textContent=o}return}let c=r.dataset.prepFeedback===`next`?1:-1;zt.set(i,Math.max(0,Math.min(s+c,o-1))),g.querySelector(`.prep-analysis`)?.replaceWith(X(sa(k[0],{analysis:a})))});function oo(e,t,n){let r=n.feedback_items.filter((e,n)=>n!==t),i=Math.min(t,Math.max(r.length-1,0)),a={...n,feedback_items:r,verdict:r.length===0?`ready_to_apply`:n.verdict};zt.set(e,i),A.set(e,a),g.querySelector(`.prep-analysis`)?.replaceWith(X(sa(k[0],{analysis:a})))}function so(e,t){let n=String(t||``).trim();if(!n)return;let r=Bt.get(e)?.trim()??``,i=r?`${r}\n\n${n}`:n;Bt.set(e,i);let a=g.querySelector(`[data-prep-resume-tweaks="${e}"]`);a&&(a.value=i,a.focus())}document.addEventListener(`keydown`,e=>{e.key===`Escape`&&!be.hidden&&Fi(),e.key===`Escape`&&!Ve.hidden&&rr(),e.key===`Escape`&&!o.hidden&&yn(),e.key===`Escape`&&!m.hidden&&Ii(),e.key===`Escape`&&!h.hidden&&Ri(),e.key===`Escape`&&!je.hidden&&Ma(),e.key===`Escape`&&!Ye.hidden&&mr(),e.key===`Escape`&&!ut.hidden&&Cr(),e.key===`Escape`&&!_t.hidden&&Mr(),e.key===`Escape`&&!Ct.hidden&&Yr()}),Be.addEventListener(`click`,nr),Ue.addEventListener(`click`,rr),He.addEventListener(`click`,rr);function co(){return Array.from(document.querySelectorAll(`.pane-toggle`))}function lo(){return co().some(e=>e.getAttribute(`aria-expanded`)===`true`)}function uo(){Ge.textContent=lo()?`collapse all`:`expand all`}function fo(){document.querySelectorAll(`.pane-toggle`).forEach(e=>{e.setAttribute(`aria-expanded`,`true`),e.querySelector(`.chevron`).textContent=`v`,e.parentElement.querySelector(`.pane-body`).hidden=!1})}function po(){document.querySelectorAll(`.job[open]`).forEach(e=>{e.open=!1}),document.querySelectorAll(`.pane-toggle`).forEach(e=>{e.setAttribute(`aria-expanded`,`false`),e.querySelector(`.chevron`).textContent=`>`,e.parentElement.querySelector(`.pane-body`).hidden=!0})}Ge.addEventListener(`click`,()=>{lo()?po():fo(),uo()}),Ke.addEventListener(`click`,()=>{It=!It,Ke.textContent=It?`show empty`:`hide empty`,w&&Hn(w.statuses)}),Je.addEventListener(`click`,pr),Qe.addEventListener(`click`,gr),Xe.addEventListener(`click`,mr),lt.addEventListener(`click`,Sr),dt.addEventListener(`click`,Cr),gt.addEventListener(`click`,jr),vt.addEventListener(`click`,Mr),Le.addEventListener(`click`,Jr),wt.addEventListener(`click`,Yr),Tt.addEventListener(`submit`,e=>{e.preventDefault(),Qr(Tt).catch(()=>{S.textContent=`could not add company.`})}),Et.addEventListener(`submit`,e=>{e.preventDefault(),ri(Et).catch(()=>{At.textContent=`could not add role.`})}),C.addEventListener(`submit`,e=>{let t=e.target.closest(`[data-company-link-form]`);t&&(e.preventDefault(),$r(t).catch(()=>{S.textContent=`could not add link.`}))}),C.addEventListener(`input`,e=>{let t=e.target.closest(`[data-company-notes]`);t&&oi(t.dataset.companyNotes)}),C.addEventListener(`change`,e=>{let t=e.target.closest(`[data-company-tier]`);if(!t)return;let n=t.closest(`.company-panel`);n&&ci(n,t.value),window.clearTimeout(gn.get(t.dataset.companyTier)),si(t.dataset.companyTier).catch(()=>{ai(`could not save company.`)})}),C.addEventListener(`click`,e=>{let t=e.target.closest(`[data-delete-company]`);if(t){let e=ii(t.dataset.deleteCompany),n=e?.name?G(e.name):`this company`;if(!window.confirm(`Deactivate ${n}? It will be hidden from company counts and skipped during scans.`))return;t.disabled=!0,ti(t.dataset.deleteCompany).catch(()=>{S.textContent=`could not deactivate company.`,t.disabled=!1});return}let n=e.target.closest(`[data-delete-career-page]`);if(!n)return;let r=n.closest(`.company-link-row`)?.querySelector(`.company-link-text`)?.textContent?.trim();window.confirm(`Delete ${r||`this career link`}?`)&&(n.disabled=!0,ei(n.dataset.deleteCareerPage).catch(()=>{S.textContent=`could not delete link.`,n.disabled=!1}))}),x.addEventListener(`change`,e=>{let t=e.target.closest(`input[type="checkbox"], select, input[data-setting-text], textarea[data-setting-textarea]`);t&&Pr(t)}),x.addEventListener(`click`,async e=>{let t=e.target.closest(`[data-application-runtime-test]`);if(!t||t.disabled)return;let n=t.dataset.applicationRuntimeTest,r=x.querySelector(`[data-application-runtime-test-status="${CSS.escape(n)}"]`);t.disabled=!0,t.textContent=`Testing…`,r&&(r.textContent=`Creating a bounded Callumployed session…`);try{let e=await fetch(`/api/application-generation/backends/${encodeURIComponent(n)}/test`,{method:`POST`}),t=await e.json();if(!e.ok||t?.ok!==!0)throw Error(t?.error||`Connection test failed.`);r&&(r.textContent=t.message||`Connection succeeded.`)}catch(e){r&&(r.textContent=e instanceof Error?e.message:`Connection test failed.`)}finally{t.disabled=!1,t.textContent=`Test connection`}}),x.addEventListener(`submit`,async e=>{e.preventDefault();let t=x.querySelector(`button[type="submit"]`),n=x.querySelectorAll(`input[type="checkbox"][name], select[name], input[data-setting-text][name], textarea[data-setting-textarea][name]`),r={};n.forEach(e=>{let t=e.name;t&&(r[t]=e.type===`checkbox`?e.checked:e.value)}),t.disabled=!0,t.textContent=`saving...`;try{b.textContent=`saving settings...`;let e=await fetch(`/api/config`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(r)});if(!e.ok)throw Error(`Config update failed`);J(await e.json(),`settings saved.`)}catch{b.textContent=`could not save settings.`,b.classList.remove(`is-empty`)}finally{t.disabled=!1,t.textContent=`save settings`}}),rt.addEventListener(`input`,()=>{ot.disabled=!rt.value.trim()}),at.addEventListener(`click`,Ir),ot.addEventListener(`click`,Lr),ct.addEventListener(`click`,Fr),St.addEventListener(`click`,Vr);function mo(){if(window.location.hash===`#prepped-roles`){ja();return}Ma({clearHash:!1})}window.addEventListener(`popstate`,mo),zr().finally(Br),window.location.hash===`#prepped-roles`&&mo(),hi({applyDefaultCollapsed:!0}).catch(()=>{kn(null,`could not load resume.`),jn([],`could not load cover letter examples.`),In()}),ui().then(()=>{di()}).catch(()=>{Re.textContent=`could not load scan status`});