import{t as e}from"./preload-helper-Czpn1I53.js";var{sankey:t,sankeyLinkHorizontal:n}=await e(async()=>{let{sankey:e,sankeyLinkHorizontal:t}=await import(`/assets/d3-sankey.js`);return{sankey:e,sankeyLinkHorizontal:t}},[]),r=document.querySelector(`#stats`),i=document.querySelector(`#status-list`),a=document.querySelector(`#search-toggle`),o=document.querySelector(`#search-dialog`),s=document.querySelector(`#search-backdrop`),c=document.querySelector(`#search-form`),l=document.querySelector(`#search-input`),u=document.querySelector(`#close-search`),ee=document.querySelector(`#materials-panel`),te=document.querySelector(`#materials-toggle`),ne=document.querySelector(`#materials-body`),d=document.querySelector(`#materials-summary`),re=document.querySelector(`#materials-required-warning`),f=document.querySelector(`#resume-meta`),p=document.querySelector(`#resume-upload`),m=document.querySelector(`#resume-upload-button`),ie=document.querySelector(`#resume-resource-meta`),ae=document.querySelector(`#resume-resource-upload`),oe=document.querySelector(`#resume-resource-upload-button`),se=document.querySelector(`#resume-resource-list`),ce=document.querySelector(`#cover-letter-meta`),le=document.querySelector(`#cover-letter-upload`),ue=document.querySelector(`#cover-letter-upload-button`),de=document.querySelector(`#cover-letter-list`),fe=document.querySelector(`#experience-note-meta`),pe=document.querySelector(`#experience-note-upload`),me=document.querySelector(`#experience-note-upload-button`),he=document.querySelector(`#experience-note-list`);document.querySelector(`#material-index-button`);var ge=document.querySelector(`#material-index-warning`),_e=document.querySelector(`#material-index-status`),ve=document.querySelector(`#review-discovered`),ye=document.querySelector(`#role-information-view`),be=document.querySelector(`#role-information-card`),xe=document.querySelector(`#close-role-information`),h=document.querySelector(`#review-view`),Se=document.querySelector(`#review-heading`),Ce=document.querySelector(`#review-progress`),we=document.querySelector(`#review-card`),Te=document.querySelector(`#close-review`),g=document.querySelector(`#prep-view`),Ee=document.querySelector(`#prep-heading`),De=document.querySelector(`#prep-progress`),_=document.querySelector(`#prep-card`),Oe=document.querySelector(`#close-prep`),ke=document.querySelector(`#prepped-roles`),Ae=document.querySelector(`#prepped-view`),je=document.querySelector(`#close-prepped`),Me=document.querySelector(`#prepped-summary`),Ne=document.querySelector(`#regenerate-all-cover-letters`),Pe=document.querySelector(`#prepped-bulk-status`),Fe=document.querySelector(`#prepped-list`),v=document.querySelector(`#prepped-detail`),y=document.querySelector(`#scan-all-button`),Ie=document.querySelector(`#manage-companies-button`),b=document.querySelector(`#scan-status-bar`),Le=document.querySelector(`#scan-status-text`),Re=document.querySelector(`#scan-last-time`),ze=document.querySelector(`#scan-failures-open`),Be=document.querySelector(`#scan-failures-dialog`),Ve=document.querySelector(`#scan-failures-backdrop`),He=document.querySelector(`#scan-failures-close`),Ue=document.querySelector(`#scan-failures-list`),We=document.querySelector(`#toggle-all`),Ge=document.querySelector(`#collapse-empty`),Ke=document.querySelector(`#toolbar-summary`),qe=document.querySelector(`#settings-open`),Je=document.querySelector(`#settings-view`),Ye=document.querySelector(`#settings-close`),x=document.querySelector(`#settings-status`),S=document.querySelector(`#settings-form`),Xe=document.querySelector(`#settings-profile-options`),Ze=document.querySelector(`#settings-profile-extract`),Qe=document.querySelector(`#settings-autoprep-options`),$e=document.querySelector(`#settings-options`),et=document.querySelector(`#central-store-summary`),tt=document.querySelector(`#central-store-sync-summary`),nt=document.querySelector(`#central-api-url-input`),rt=document.querySelector(`#central-passkey-input`),it=document.querySelector(`#central-save-button`),at=document.querySelector(`#central-sync-button`),ot=document.querySelector(`#recommendation-history-summary`),st=document.querySelector(`#clear-recommendation-history`),ct=document.querySelector(`#metrics-open-button`),lt=document.querySelector(`#metrics-view`),ut=document.querySelector(`#metrics-close`),dt=document.querySelector(`#metrics-status`),ft=document.querySelector(`#metrics-overview`),pt=document.querySelector(`#metrics-sections`),mt=document.querySelector(`#metrics-scan-list`),ht=document.querySelector(`#sankey-open-button`),gt=document.querySelector(`#sankey-view`),_t=document.querySelector(`#sankey-close`),vt=document.querySelector(`#sankey-status`),yt=document.querySelector(`#sankey-canvas`),bt=document.querySelector(`#sankey-path-list`),xt=document.querySelector(`#app-update-button`),St=document.querySelector(`#companies-view`),Ct=document.querySelector(`#companies-close`),C=document.querySelector(`#companies-status`),wt=document.querySelector(`#company-create-form`),w=document.querySelector(`#companies-list`),Tt=document.querySelector(`#role-add-form`),Et=document.querySelector(`#role-url-input`),Dt=document.querySelector(`#role-company-input`),Ot=document.querySelector(`#role-company-options`),kt=document.querySelector(`#role-add-status`),At=3,jt=1200,Mt=new Set([`applied`,`OA`,`interview`,`rejected`,`offer`]),Nt=new Map([[`discovered`,`#4f6472`],[`interested`,`#00897b`],[`disinterested`,`#626970`],[`applied`,`#2257ad`],[`oa`,`#b36b00`],[`interview`,`#5f2bd8`],[`rejected`,`#b93d2d`],[`offer`,`#137347`],[`closed`,`#53606b`],[`archived`,`#765b4a`]]),Pt=/^(?:about (?:the )?(?:role|team|job)|about this role|job description|job responsibilities|minimum qualifications|preferred qualifications|qualifications|requirements|responsibilities|what to expect|what (?:you'll|you’ll|you will) (?:bring|do)|what'?s in it for you|who you are|your objectives|your skills & talents):?$/i,Ft=!0,T=null,It=null,E=[],D=[],O=[],Lt=null,k=[],A=[],j=new Map,Rt=new Map,M=new Map,zt=new Map,N=new Map,Bt=new Map,Vt=new Map,Ht=new Map,P=[],F=null,Ut=null,Wt=!1,I=``,L=null,Gt=new Set,Kt=new Set,qt=new Map,R=new Set,Jt=new Set,z=new Map,Yt=new Map,Xt=new Set,Zt=new Set,B=new Set,Qt=new Set,$t=new Set,en=new Set,V=new Map,H=new Map,tn=new Map,nn=new Map,rn=new Set,an=!1,on=0,sn=null,cn=!1,ln=null,un=null,dn=null,fn=null,U=null,pn=[],mn=new Map;function hn(){return T?.query?.trim()??``}function gn(){let e=!!hn();a.classList.toggle(`search-active`,e),a.setAttribute(`aria-label`,e?`clear search`:`search jobs`)}function _n(){l.value=hn(),o.hidden=!1,c.hidden=!1,l.focus(),l.select()}function vn(){o.hidden=!0,c.hidden=!0,a.focus()}function yn(e){return e?new Intl.DateTimeFormat(void 0,{month:`short`,day:`numeric`,hour:`numeric`,minute:`2-digit`}).format(new Date(e)).toLocaleLowerCase():``}function W(e){return e?new Intl.DateTimeFormat(void 0,{month:`short`,day:`numeric`,hour:`numeric`,minute:`2-digit`}).format(new Date(e)).replace(`, `,` `).toLocaleLowerCase():``}function G(e){return String(e??``).replaceAll(`&`,`&amp;`).replaceAll(`<`,`&lt;`).replaceAll(`>`,`&gt;`).replaceAll(`"`,`&quot;`).replaceAll(`'`,`&#039;`)}function K(e){return String(e??``).toLocaleLowerCase()}function q(e){return G(K(e))}function bn(e){try{let t=new URL(String(e||``));return[`http:`,`https:`].includes(t.protocol)?t.href:``}catch{return``}}function xn(e){return e}function Sn(e=_){e.querySelectorAll(`[data-prep-resume-latex], [data-prep-cover-letter-latex]`).forEach(xn)}function Cn(){return`
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
  `}function En(e,t,n){let r=`<span class="role-title-text">${q(e)}</span>`;return t?`<a class="${n}" href="${G(t)}" target="_blank" rel="noreferrer">${r}${Cn()}</a>`:`<span class="${n}">${r}</span>`}function Dn(e){r.innerHTML=[[`companies`,e.companies_total],[`jobs`,e.jobs_total],[`applications`,e.applications_total]].map(([e,t])=>`<dl class="stat"><dt>${q(e)}</dt><dd>${t}</dd></dl>`).join(``)}function On(e=T){if(!e){Ke.innerHTML=``;return}let t=t=>e.statuses.find(e=>e.key===t)?.count??0;Ke.innerHTML=[[`discovered`,t(`discovered`)],[`interested`,t(`interested`)],[`applied`,e.stats?.applications_total??0],[`total`,e.stats?.jobs_total??0]].map(([e,t])=>`
        <dl>
          <dt>${q(e)}</dt>
          <dd>${t}</dd>
        </dl>
      `).join(``)}function kn(e,t=``){if(It=e,m.textContent=e?`replace`:`upload`,t){f.textContent=t;return}if(!e){f.textContent=`no resume uploaded`;return}let n=W(e.updated_at),r=zn(e.content_bytes);f.textContent=[K(e.filename),r,n].filter(Boolean).join(` | `)}function An(e,t,n,{binary:r=!1}={}){let i=r?e.filename:e.id;return`
    <li class="material-source-item" title="${q(e.filename)}">
      <div class="material-source-copy">
        <span>${q(e.filename)}</span>
        <small>${G(n)}</small>
      </div>
      <div class="material-source-actions">
        <button type="button" class="material-source-view" data-material-view="${G(t)}" data-material-id="${G(i)}" data-material-binary="${r}">preview</button>
        <button type="button" class="material-source-remove" data-material-remove="${G(t)}" data-material-id="${G(i)}" data-material-name="${q(e.filename)}">remove</button>
      </div>
      <div class="material-source-preview" data-material-preview-body hidden></div>
    </li>`}function jn(e,t=``){D=Array.isArray(e)?e:[],ue.textContent=D.length>0?`add`:`upload`,ce.textContent=t||(D.length===0?`no examples uploaded`:`${D.length} ${D.length===1?`example`:`examples`} stored`),de.innerHTML=D.map(e=>An(e,`cover-letter-examples`,zn(e.content_bytes))).join(``)}function Mn(e,t=``){O=Array.isArray(e)?e:[],me.textContent=O.length>0?`add`:`upload`,fe.textContent=t||(O.length===0?`no notes uploaded`:`${O.length} ${O.length===1?`note`:`notes`} stored`),he.innerHTML=O.map(e=>An(e,`experience-notes`,zn(e.content_bytes))).join(``)}function Nn(e,t=``){Lt=e??null;let n=Lt?.status??`missing`,r=n!==`ready`;if(O.length,ge.hidden=!r,ge.textContent=t||Lt?.warning||``,t)_e.textContent=t;else if(n===`ready`){let e=Number(Lt?.document_count??0),t=Number(Lt?.skipped_source_count??0),n=W(Lt?.generated_at);_e.innerHTML=[`${e} indexed ${e===1?`page`:`pages`}`,t?`${t} unreadable upload skipped`:``,n].filter(Boolean).map(e=>`<button type="button" class="material-index-link" data-open-material-index title="Reveal the application material index in Finder">${q(e)}</button>`).join(`<span aria-hidden="true"> | </span>`)}else _e.textContent=n===`stale`?`index out of date`:`not indexed`}function Pn(e,t=``){E=Array.isArray(e)?e:[],oe.textContent=E.length>0?`add`:`upload`,ie.textContent=t||(E.length===0?`no resources uploaded`:`${E.length} ${E.length===1?`resource`:`resources`} stored`),se.innerHTML=E.map(e=>An(e,`resume-resources`,zn(e.bytes),{binary:!0})).join(``)}function Fn(e,t={}){on+=1,document.querySelectorAll(`[data-preview-blob-url]`).forEach(e=>{URL.revokeObjectURL(e.dataset.previewBlobUrl)}),kn(e?.master_resume??null),Pn(e?.resume_resources??[]),jn(e?.cover_letter_examples??[]),Mn(e?.experience_notes??[]),Nn(e?.material_index??null),Ln(e?.ui),(!an||t.applyDefaultCollapsed)&&(Rn(!In(e?.ui)),an=!0)}function In(e=null){return typeof e?.has_missing_required_materials==`boolean`?e.has_missing_required_materials:!It||D.length===0||O.length===0}function Ln(e=null){let t=It?`resume ready`:`no resume`,n=E.length===0?`no resources`:`${E.length} ${E.length===1?`resource`:`resources`}`,r=D.length,i=r===0?`no cover letters`:`${r} cover ${r===1?`letter`:`letters`}`,a=O.length,o=a===0?`no notes`:`${a} experience ${a===1?`note`:`notes`}`;re.hidden=!In(e),d.textContent=`${t} | ${n} | ${i} | ${o}`}function Rn(e){ee.classList.toggle(`collapsed`,e),te.setAttribute(`aria-expanded`,String(!e)),te.querySelector(`.materials-chevron`).textContent=e?`>`:`v`,ne.hidden=e}function zn(e){return Number.isFinite(e)?e<1024?`${e} b`:`${Math.round(e/1024)} kb`:``}async function Bn(e){let t=await fetch(e,{cache:`no-store`});if(!t.ok)throw Error(`Preview unavailable`);let n=await t.arrayBuffer();if(new TextDecoder(`ascii`).decode(n.slice(0,5))!==`%PDF-`)throw Error(`The selected file is not a readable PDF.`);return URL.createObjectURL(new Blob([n],{type:`application/pdf`}))}async function Vn(e){let t=e.closest(`.material-source-item`)?.querySelector(`[data-material-preview-body]`);if(!t)return;if(t.dataset.loaded===`true`){t.hidden=!t.hidden,e.textContent=t.hidden?`preview`:`hide`;return}e.disabled=!0,e.textContent=`loading...`;let n=e.dataset.materialView,r=e.dataset.materialId,i=on,a=`/api/${encodeURIComponent(n)}/${encodeURIComponent(r)}`;try{if(e.dataset.materialBinary===`true`){let e=await Bn(a);if(!t.isConnected||on!==i){URL.revokeObjectURL(e);return}t.dataset.previewBlobUrl=e,t.innerHTML=`<iframe title="${q(r)} preview"></iframe>`,t.querySelector(`iframe`).src=e}else{let e=await fetch(a);if(!e.ok)throw Error(`Preview unavailable`);let n=await e.json(),r=document.createElement(`pre`);r.textContent=n.content||`This source is empty.`,t.replaceChildren(r)}t.dataset.loaded=`true`,t.hidden=!1,e.textContent=`hide`}catch(n){t.textContent=n instanceof Error?n.message:`Preview unavailable`,t.hidden=!1,e.textContent=`preview`}finally{e.disabled=!1}}async function Hn(e){let t=e.dataset.materialRemove,n=e.dataset.materialId;if(e.dataset.confirmRemove!==`true`){e.dataset.confirmRemove=`true`,e.textContent=`confirm remove`,e.classList.add(`danger`),window.setTimeout(()=>{!e.isConnected||e.disabled||(delete e.dataset.confirmRemove,e.textContent=`remove`,e.classList.remove(`danger`))},6e3);return}e.disabled=!0,e.textContent=`removing...`;try{let e=await fetch(`/api/${encodeURIComponent(t)}/${encodeURIComponent(n)}`,{method:`DELETE`}),r=await e.json();if(!e.ok)throw Error(r.error||`Remove failed`);Fn(r)}catch(t){e.disabled=!1,delete e.dataset.confirmRemove,e.classList.remove(`danger`),e.textContent=`remove`,window.alert(t instanceof Error?t.message:`Remove failed`)}}function Un(e){i.innerHTML=e.map(e=>{let t=e.jobs.map(t=>Wn(t,e.key)).join(``),n=Math.max(Number(e.count)-e.jobs.length,0),r=[`disinterested`,`rejected`,`closed`].includes(e.key)&&n>0?`<p class="empty-copy status-more-copy">... and ${n} more</p>`:``;return`
        <section class="status-pane ${e.count===0?`empty`:``} ${Ft?`hidden-empty`:``}" id="status-${G(e.key)}" data-bucket="${G(e.key)}">
          <button class="pane-toggle" type="button" aria-expanded="false">
            <span class="chevron">></span>
            <span class="pane-title">${q(e.label)}</span>
            <span class="count">${e.count}</span>
          </button>
          <div class="pane-body" hidden>
            ${t||r?`<div class="jobs">${t}${r}</div>`:`<p class="empty-copy">${e.key===`archived`&&e.count>0?`archived role details are hidden.`:`no jobs in this status.`}</p>`}
          </div>
        </section>
      `}).join(``)}function Wn(e,t){return`
    <details class="job" data-role-id="${G(e.id)}">
      <summary class="job-summary">
        <span class="job-chevron">></span>
        <span class="job-identity">
          <span class="job-company">[${q(e.company_name)}]</span>
          ${En(e.title,e.role_url,`job-title`)}
          ${t===`interested`&&e.prep_started?qn():``}
          ${t===`closed`&&e.updated_in_latest_scan?Gn():``}
          ${[`discovered`,`interested`].includes(t)&&e.missing_from_latest_scan?Kn():``}
        </span>
      </summary>
      <div class="job-detail">
        ${t===`discovered`?Jn(e):``}
        ${t===`interested`?Yn(e):``}
        ${t===`disinterested`?Xn(e):``}
        ${t===`applied`?Zn(e):``}
        ${t===`OA`?Qn(e):``}
        ${t===`interview`?$n(e):``}
        ${t===`closed`?er(e):``}
        <dl>
          ${e.location?`<div>
                  <dt>location</dt>
                  <dd>${q(e.location)}</dd>
                </div>`:``}
          <div>
            <dt>updated</dt>
            <dd>${yn(e.updated_at)}</dd>
          </div>
        </dl>
      </div>
    </details>
  `}function Gn(){return`<span class="latest-scan-dot" title="updated in latest scan" aria-label="updated in latest scan"></span>`}function Kn(){return`<span class="missing-latest-scan-dot" title="not seen in latest scan" aria-label="not seen in latest scan"></span>`}function qn(){return`<span class="prep-started-dot" title="application materials started" aria-label="application materials started"></span>`}function Jn(e){return`
    <div class="job-actions job-actions-nowrap" aria-label="discovered role actions">
      <button class="job-action success" type="button" data-review-role-id="${e.id}">view</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="interested">interested</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="disinterested">disinterested</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="closed">closed</button>
    </div>
  `}function Yn(e){return`
    <div class="job-actions" aria-label="interested role actions">
      <button class="job-action success" type="button" data-prep-role-id="${e.id}">prep</button>
      <button class="job-action success" type="button" data-autoprep-role-id="${e.id}">${e.autoprep_started?`view / regenerate prep`:`autoprep`}</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="applied">applied</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="disinterested">disinterested</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="closed">closed</button>
    </div>
    ${e.autoprep_started?`<p class="job-prepped-note">already prepped</p>`:``}
  `}function Xn(e){return`
    <div class="job-actions" aria-label="disinterested role actions">
      <button class="job-action success" type="button" data-role-id="${e.id}" data-status="interested">interested</button>
    </div>
  `}function Zn(e){return`
    <div class="job-actions job-actions-nowrap" aria-label="applied role actions">
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="OA">oa</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="interview">interview</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="rejected">rejected</button>
    </div>
  `}function Qn(e){return`
    <div class="job-actions job-actions-nowrap" aria-label="oa role actions">
      <button class="job-action" type="button" data-view-role-info="${e.id}">view information</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="interview">interview</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="disinterested">disinterested</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="rejected">rejected</button>
    </div>
  `}function $n(e){return`
    <div class="job-actions" aria-label="interview role actions">
      <button class="job-action" type="button" data-view-role-info="${e.id}">view information</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="rejected">rejected</button>
      <button class="job-action success" type="button" data-role-id="${e.id}" data-status="offer">offer</button>
    </div>
  `}function er(e){return`
    <div class="job-actions" aria-label="closed role actions">
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="interested">interested</button>
    </div>
  `}function tr(e){T=e,l.value=e.query,gn(),Dn(e.stats),On(e),Un(e.statuses),fo(),ji(e.statuses)}function nr(e){ln=e??null;let t=!!e?.scanning,n=t&&!!e?.cancel_requested,r=Number(e?.completed_companies??0),i=Number(e?.total_companies??0),a=Number(e?.failed_companies??0),o=typeof e?.error==`string`?e.error.trim():``,s=Array.isArray(e?.failures)?e.failures:[];y.disabled=n,y.textContent=t?n?`cancelling...`:`cancel scan`:`scan roles`,y.classList.toggle(`danger`,t&&!n),b.hidden=!t&&!o&&s.length===0,b.classList.toggle(`scanning`,t),b.classList.toggle(`scan-error`,!t&&!!o||s.length>0),Le.textContent=n?`cancelling scan...`:t?`scanning roles${i>0?` ${r}/${i}`:``}${a>0?`, ${a} failed`:``}`:s.length>0?`${s.length} recent scan ${s.length===1?`failure`:`failures`}`:o?`last scan error: ${o}`:`scan idle`,ze&&Ue&&(ze.hidden=s.length===0,Ue.innerHTML=s.slice(0,5).map(e=>{let t=e?.company_name||`unknown company`,n=e?.error||`scan failed`;return`
          <p>
            <span>${q(t)}</span>
            <span>${G(n)}</span>
          </p>
        `}).join(``),s.length===0&&ir());let c=e?.last_scan_at;Re.textContent=c?`last scan: ${W(c)}`:`last scan: never`,cn&&!t&&hi(hn()).catch(()=>{}),cn=t}function rr(){ze.hidden||(Be.hidden=!1,He.focus())}function ir(){Be.hidden=!0}function J(e,t=``){un=e;let n=Array.isArray(e?.settings)?e.settings:[],r=n.filter(e=>e.key?.startsWith(`applicant_`)),i=n.filter(e=>e.key?.startsWith(`autoprep_`)||e.key===`application_generation_backend`),a=n.filter(e=>!e.key?.startsWith(`applicant_`)&&!e.key?.startsWith(`autoprep_`)&&e.key!==`application_generation_backend`),o=e?.central??{};x.textContent=t,x.classList.toggle(`is-empty`,!t);let s=Number(e?.recommendation_history_count??0);ot.textContent=s>0?`${s} saved ${s===1?`feedback decision`:`feedback decisions`}`:`no saved resume feedback decisions`,st.disabled=s===0,sr(o),Xe.innerHTML=r.map(e=>cr(e)).join(``),Qe.innerHTML=i.map(t=>cr(ar(t,e))).join(``)+or(e),$e.innerHTML=a.map(e=>cr(e)).join(``),pr(!1)}function ar(e,t){if(e.key!==`application_generation_backend`||!Array.isArray(e.options))return e;let n=t?.application_generation_runtimes??{};return{...e,options:e.options.map(e=>{let t=n?.[e.value];return!t||e.available===!1||e.disabled===!0?e:{...e,available:t.available??t.detected??!0,reason:t.reason}})}}function or(e){let t=e?.application_generation_runtimes??e?.runtime_availability??e?.runtimes??{},n=[[`hermes`,t?.hermes??t?.Hermes],[`openclaw`,t?.openclaw??t?.OpenClaw]];return n.some(([,e])=>e&&typeof e==`object`)?`<div class="application-runtime-statuses" aria-label="application generation runtime detection">
    ${n.map(([e,t])=>{let n=t?.available??t?.detected??!1,r=t?.reason??t?.message??(n?`Runtime detected`:`Runtime unavailable`);return`<div class="application-runtime-status" data-application-runtime="${G(e)}">
        <span><strong>${q(e===`openclaw`?`OpenClaw`:`Hermes`)}</strong> ${n?`available`:`unavailable`}</span>
        <small>${q(r)}</small>
        <button type="button" data-application-runtime-test="${G(e)}" ${n?``:`disabled`}>Test connection</button>
        <small data-application-runtime-test-status="${G(e)}" aria-live="polite"></small>
      </div>`}).join(``)}
  </div>`:``}function sr(e){let t=e?.api_url??``;nt.value=t,rt.value=``;let n=e?.passkey_configured?`passkey saved`:`no passkey saved`;et.textContent=t?`${K(t)} | ${n}`:`no api url | ${n}`,tt.textContent=`${Number(e?.companies_linked??0)} linked | ${Number(e?.companies_unlinked??0)} unlinked | ${Number(e?.companies_needs_review??0)} review | ${Number(e?.companies_failed??0)} failed`,at.disabled=!t}function cr(e){if(e.control===`textarea`&&e.editable!==!1)return ur(e);if(e.control===`text`&&e.editable!==!1)return lr(e);if(e.control===`select`&&e.editable!==!1)return dr(e);if(e.control!==`toggle`||e.editable===!1)return fr(e);let t=e.value?`checked`:``,n=e.default?`on by default`:`off by default`;return`
    <label class="setting-option">
      <span class="setting-copy">
        <span class="setting-label">${q(e.label)}</span>
        <span class="setting-description">${q(e.description)}</span>
        <span class="setting-default">${q(n)}</span>
      </span>
      <span class="setting-switch">
        <input type="checkbox" name="${G(e.key)}" ${t} />
        <span aria-hidden="true"></span>
      </span>
    </label>
  `}function lr(e){let t=e.default?`default: ${K(e.default)}`:`optional`,n=e.input_type??`text`,r=e.autocomplete??`name`;return`
    <label class="setting-option">
      <span class="setting-copy">
        <span class="setting-label">${q(e.label)}</span>
        <span class="setting-description">${q(e.description)}</span>
        <span class="setting-default">${q(t)}</span>
      </span>
      <input
        class="setting-text-input"
        data-setting-text
        name="${G(e.key)}"
        type="${G(n)}"
        value="${G(e.value??``)}"
        autocomplete="${G(r)}"
      />
    </label>
  `}function ur(e){return`
    <label class="setting-option setting-option-prompt">
      <span class="setting-copy">
        <span class="setting-label">${q(e.label)}</span>
        <span class="setting-description">${q(e.description)}</span>
      </span>
      <textarea
        class="setting-prompt-input"
        data-setting-textarea
        name="${G(e.key)}"
        rows="7"
        maxlength="8000"
      >${q(e.value??``)}</textarea>
    </label>
  `}function dr(e){let t=Array.isArray(e.options)?e.options:[],n=`default: ${K(e.default)}`,r=e.key===`application_generation_backend`,i=r?`setting-select setting-select-application-backend`:`setting-select`;return`
    <label class="setting-option">
      <span class="setting-copy">
        <span class="setting-label">${q(e.label)}</span>
        <span class="setting-description">${q(e.description)}</span>
        <span class="setting-default">${q(n)}</span>
      </span>
      <select class="${i}" name="${G(e.key)}">
        ${t.map(t=>{let n=t.value===e.value?`selected`:``,i=t.available===!1||t.disabled===!0,a=r&&i?` — unavailable`:``;return`<option value="${G(t.value)}" ${n} ${i?`disabled`:``}>${q(t.label)}${q(a)}</option>`}).join(``)}
      </select>
    </label>
  `}function fr(e){let t=e.default?`on by default`:`off by default`,n=e.value?`automatic`:`off`;return`
    <div class="setting-option setting-option-readonly">
      <span class="setting-copy">
        <span class="setting-label">${q(e.label)}</span>
        <span class="setting-description">${q(e.description)}</span>
        <span class="setting-default">${q(t)}</span>
      </span>
      <span class="setting-badge">${q(n)}</span>
    </div>
  `}function pr(e){S.querySelectorAll(`input, select, textarea`).forEach(t=>{t.disabled=e}),it.disabled=e,at.disabled=e||!nt.value.trim(),Ze.disabled=e,xt.disabled=e}async function mr(){Je.hidden=!1,document.body.classList.add(`settings-open`),Ye.focus(),un?J(un):(x.textContent=`loading settings...`,x.classList.remove(`is-empty`),$e.innerHTML=``);try{await gr()}catch{x.textContent=`could not load settings.`}}function hr(){Je.hidden=!0,document.body.classList.remove(`settings-open`),qe.focus()}async function gr(){let e=await fetch(`/api/config`);if(!e.ok)throw Error(`Config request failed`);J(await e.json())}async function _r(){Ze.disabled=!0,Ze.textContent=`filling blank fields...`,x.textContent=`sending the master resume to the selected AI provider...`,x.classList.remove(`is-empty`);try{let e=await fetch(`/api/config/extract-profile`,{method:`POST`});if(!e.ok)throw Error(`Profile extraction request failed`);let t=await e.json(),n=Array.isArray(t.populated)?t.populated:[];J(t.config,n.length?`filled ${n.length} blank profile ${n.length===1?`field`:`fields`}.`:`no blank profile fields could be filled.`)}catch{x.textContent=`could not fill profile fields from the resume.`}finally{Ze.disabled=!1,Ze.textContent=`fill blank fields`}}function vr(e){let t=e?.value;return t==null?`n/a`:e?.kind===`ratio`?Number(t).toLocaleString(void 0,{maximumFractionDigits:2,minimumFractionDigits:0}):typeof t==`number`?t.toLocaleString():K(t)}function yr(e,t=`metric-card`){return`
    <article class="${t}">
      <span>${q(e?.label)}</span>
      <strong>${G(vr(e))}</strong>
    </article>
  `}function br(e,t=``){dn=e,dt.textContent=t||(e?.updated_at?`updated ${W(e.updated_at)}`:``),dt.classList.toggle(`is-empty`,!dt.textContent);let n=Array.isArray(e?.overview)?e.overview:[],r=Array.isArray(e?.sections)?e.sections:[],i=Array.isArray(e?.recent_scans)?e.recent_scans:[];ft.innerHTML=n.map(e=>yr(e)).join(``),pt.innerHTML=r.map(xr).join(``),mt.innerHTML=i.length?i.map(Sr).join(``):`<p class="empty-copy">no scan runs recorded.</p>`}function xr(e){let t=Array.isArray(e?.metrics)?e.metrics:[];return`
    <section class="metrics-section">
      <div class="metrics-section-heading">
        <h3>${q(e?.title)}</h3>
      </div>
      <div class="metrics-section-grid">
        ${t.map(e=>yr(e,`metric-card metric-card-compact`)).join(``)}
      </div>
    </section>
  `}function Sr(e){let t=e?.scan_status??`unknown`,n=e?.started_at?W(e.started_at):`not started`,r=e?.finished_at?W(e.finished_at):`not finished`,i=e?.error?`<span>${q(e.error)}</span>`:``;return`
    <article class="metrics-scan-row">
      <div>
        <strong>${q(e?.company_name??`unknown company`)}</strong>
        <span>${q(n)} -> ${q(r)}</span>
        ${i}
      </div>
      <span class="metrics-status-pill">${q(t)}</span>
    </article>
  `}async function Cr(){lt.hidden=!1,document.body.classList.add(`metrics-open`),ut.focus(),dn?br(dn):(dt.textContent=`loading metrics...`,dt.classList.remove(`is-empty`),ft.innerHTML=``,pt.innerHTML=``,mt.innerHTML=``);try{await Tr()}catch{dt.textContent=`could not load metrics.`}}function wr(){lt.hidden=!0,document.body.classList.remove(`metrics-open`),ct.focus()}async function Tr(){let e=await fetch(`/api/metrics`);if(!e.ok)throw Error(`Metrics request failed`);br(await e.json())}function Er(e,t=``){fn=e;let n=Number(e?.role_count??0),r=Array.isArray(e?.links)?e.links:[],i=Array.isArray(e?.paths)?e.paths:[];vt.textContent=t||(e?.updated_at?`${n.toLocaleString()} roles | updated ${W(e.updated_at)}`:``),vt.classList.toggle(`is-empty`,!vt.textContent),yt.innerHTML=r.length?Dr(e):`<p class="empty-copy">no role transitions recorded yet.</p>`,bt.innerHTML=i.length?i.map(jr).join(``):`<p class="empty-copy">no role paths recorded yet.</p>`}function Dr(e){let t=Array.isArray(e?.nodes)?e.nodes:[],n=Array.isArray(e?.links)?e.links:[],r=Ar(t,n),i=r.nodes,a=r.links,o=(r.flowLinks??n).map(e=>{let t=i.get(e.source),n=i.get(e.target),r=a.get(e);if(!t||!n||!r)return``;let o=r.width,s=n.x<t.x,c=Or(e.target),l=r.priority?`0.42`:s?`0.28`:`0.34`,u=r.path??kr({isBacktrack:s,sourceX:t.x+t.width,sourceY:r.sourceY,targetX:n.x,targetY:r.targetY,width:o});return`
        <path class="${[`sankey-link`,s?`sankey-link-backtrack`:``,r.priority?`sankey-link-priority`:``].filter(Boolean).join(` `)}" d="${u}" fill="${r.path?`none`:c}" fill-opacity="${l}" stroke="${c}" style="stroke-width: ${r.path?o:1}px">
          <title>${q(t.label)} to ${q(n.label)}: ${Number(e.value??0).toLocaleString()}</title>
        </path>
      `}).join(``),s=Array.from(i.values()).map(e=>{let t=Number(e.history_count??e.current_count??0),n=Number(e.value??t),i=n>0?n.toLocaleString():`0`,a=e.x>r.width-180,o=a?e.x-8:e.x+e.width+8,s=Math.max(24,e.y-e.height/2-16),c=a?`end`:`start`,l=Or(e.id);return`
        <g class="sankey-node" transform="translate(${e.x}, ${e.y-e.height/2})">
          <rect width="${e.width}" height="${e.height}" rx="7" fill="${l}" stroke="${l}"></rect>
        </g>
        <g class="sankey-node-label" transform="translate(${o}, ${s})">
          <text text-anchor="${c}">${q(e.label)}</text>
          <text class="sankey-node-count" y="16" text-anchor="${c}">${q(i)} roles</text>
        </g>
      `}).join(``);return`
    <svg class="sankey-svg" viewBox="0 0 ${r.width} ${r.height}" role="img" aria-label="role state transition sankey diagram">
      <g>${o}</g>
      <g>${s}</g>
    </svg>
  `}function Or(e){return Nt.get(String(e).toLowerCase())??`#4f6472`}function kr({isBacktrack:e,sourceX:t,sourceY:n,targetX:r,targetY:i,width:a}){let o=a/2,s=n-o,c=n+o,l=i-o,u=i+o;if(e){let e=Math.max(80,Math.abs(t-r)*.42);return[`M ${t} ${s}`,`C ${t-e} ${s}, ${r+e} ${l}, ${r} ${l}`,`L ${r} ${u}`,`C ${r+e} ${u}, ${t-e} ${c}, ${t} ${c}`,`Z`].join(` `)}let ee=Math.max(46,(r-t)*.48);return[`M ${t} ${s}`,`C ${t+ee} ${s}, ${r-ee} ${l}, ${r} ${l}`,`L ${r} ${u}`,`C ${r-ee} ${u}, ${t+ee} ${c}, ${t} ${c}`,`Z`].join(` `)}function Ar(e,r){let i=new Map([[`discovered`,0],[`interested`,1],[`disinterested`,2],[`applied`,2],[`oa`,3],[`interview`,3],[`rejected`,4],[`closed`,4],[`archived`,4]]),a=new Map,o=new Map;r.forEach(e=>{a.set(e.target,(a.get(e.target)??0)+Number(e.value??0)),o.set(e.source,(o.get(e.source)??0)+Number(e.value??0))});let s=e.filter(e=>Number(e?.history_count??e?.current_count??0)>0||a.has(e.id)||o.has(e.id)),c=new Set(s.map(e=>e.id)),l=r.filter(e=>c.has(e.source)&&c.has(e.target)&&Number(e.value??0)>0),u=e=>i.get(String(e).toLowerCase())??0,ee=l.filter(e=>u(e.target)>=u(e.source)),te=l.filter(e=>u(e.target)<u(e.source)),ne={nodes:s.map(e=>({...e,fixedValue:Math.max(0,Number(e?.history_count??e?.current_count??0))})),links:ee.map(e=>({...e}))},d=t().nodeId(e=>e.id).nodeWidth(26).nodePadding(44).nodeAlign((e,t)=>Math.min(t-1,u(e.id))).extent([[92,88],[1014,634]]).iterations(32)(ne),re=new Map;d.nodes.forEach(e=>{re.set(e.id,{...e,x:e.x0,y:e.y0+(e.y1-e.y0)/2,width:e.x1-e.x0,height:Math.max(1.5,e.y1-e.y0),value:Number(e.fixedValue??e.value??0)})});let f=new Map,p=[],m=n();d.links.forEach(e=>{let t={source:e.source.id,target:e.target.id,value:e.value};p.push(t),f.set(t,{path:m(e),width:Math.max(1.5,e.width),sourceY:e.y0,targetY:e.y1,priority:Number(e.value??0)>=20})});let ie=Math.max(.6,...d.links.map(e=>Number(e.width??0)/Math.max(1,Number(e.value??0))));return te.forEach(e=>{let t=re.get(e.source),n=re.get(e.target);if(!t||!n)return;let r=Math.max(1.5,Number(e.value??0)*ie),i={...e};p.push(i),f.set(i,{width:r,sourceY:t.y+t.height/2-r/2,targetY:n.y+n.height/2-r/2,priority:!1})}),p.sort((e,t)=>Number(e.value??0)-Number(t.value??0)),{flowLinks:p,height:720,links:f,nodes:re,width:1120}}function jr(e){let t=Array.isArray(e?.path)?e.path:[];return`
    <article class="sankey-path-row">
      <div>
        <strong>${q(e?.company_name??`unknown company`)} / ${q(e?.title??`untitled role`)}</strong>
        <span>${t.map(e=>q(e)).join(` -> `)}</span>
      </div>
      <span class="metrics-status-pill">${Number(e?.loops_collapsed??0).toLocaleString()} loops</span>
    </article>
  `}async function Mr(){Je.hidden=!0,document.body.classList.remove(`settings-open`),gt.hidden=!1,document.body.classList.add(`sankey-open`),_t.focus(),fn?Er(fn):(vt.textContent=`loading role flow...`,vt.classList.remove(`is-empty`),yt.innerHTML=``,bt.innerHTML=``);try{await Pr()}catch{vt.textContent=`could not load role flow.`}}function Nr(){gt.hidden=!0,document.body.classList.remove(`sankey-open`),qe.focus()}async function Pr(){let e=await fetch(`/api/role-sankey`);if(!e.ok)throw Error(`Role sankey request failed`);Er(await e.json())}async function Fr(e){let t=e.name;if(!t)return;let n=e.type===`checkbox`?!e.checked:un?.settings?.find(e=>e.key===t)?.value,r=e.type===`checkbox`?e.checked:e.value;pr(!0),x.textContent=`saving settings...`,x.classList.remove(`is-empty`);try{let e=await fetch(`/api/config`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({[t]:r})});if(!e.ok)throw Error(`Config update failed`);J(await e.json(),`settings saved.`)}catch{e.type===`checkbox`?e.checked=n:n!==void 0&&(e.value=n),x.textContent=`could not save settings.`,pr(!1)}}async function Ir(){st.disabled=!0,x.textContent=`clearing recommendation history...`,x.classList.remove(`is-empty`);try{let e=await fetch(`/api/recommendation-history/clear`,{method:`POST`});if(!e.ok)throw Error(`Recommendation history clear failed`);let t=await e.json();J(t.config,`cleared ${t.deleted_count} saved decisions.`)}catch{x.textContent=`could not clear recommendation history.`,st.disabled=!1}}async function Lr(){let e=nt.value.trim();if(!e){x.textContent=`central api url is required.`,x.classList.remove(`is-empty`);return}let t={central_api_url:e},n=rt.value.trim();n&&(t.central_passkey=n),pr(!0),x.textContent=`saving central settings...`,x.classList.remove(`is-empty`);try{let e=await fetch(`/api/config`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(t)});if(!e.ok)throw Error(`Central settings update failed`);J(await e.json(),`central settings saved.`)}catch{x.textContent=`could not save central settings.`,pr(!1)}}async function Rr(){at.disabled=!0,x.textContent=`syncing remote company ids...`,x.classList.remove(`is-empty`);try{let e=await fetch(`/api/central/resolve-companies`,{method:`POST`});if(!e.ok)throw Error(`Central company sync failed`);let t=await e.json(),n=t.result??{},r=t.pulled_companies,i=r?` remote: ${Number(r.created??0)} created, ${Number(r.linked??0)} linked, ${Number(r.existing??0)} existing.`:``;J(t.config,`company sync: ${Number(n.linked??0)} matched, ${Number(n.created??0)} created, ${Number(n.needs_review??0)} review, ${Number(n.failed??0)} failed.${i}`),t.companies&&(U=t.companies,Wr(t.companies.companies))}catch{x.textContent=`could not sync companies.`,at.disabled=!nt.value.trim()}}async function zr(){let e=await fetch(`/api/central/resolve-companies`,{method:`POST`});if(!e.ok)throw Error(`Central company sync failed`);let t=await e.json();t.companies&&(U=t.companies,Wr(t.companies.companies))}async function Br(){await hi().catch(()=>{i.innerHTML=`<p class="empty-copy">could not load jobs.</p>`}),Qr().catch(()=>{kt.textContent=`could not load companies.`})}function Vr(){window.setTimeout(()=>{zr().catch(()=>{})},1e4)}async function Hr(){if(window.confirm(`Update callumployed and restart the tracker?`)){pr(!0),xt.disabled=!0,x.textContent=`updating callumployed; tracker will restart shortly...`,x.classList.remove(`is-empty`);try{if(!(await fetch(`/api/app/update`,{method:`POST`})).ok)throw Error(`App update failed`);x.textContent=`update started. reconnect in a moment.`}catch{x.textContent=`could not start update.`,pr(!1)}}}function Ur(e,t=``){U=e;let n=Array.isArray(e?.companies)?e.companies:[];if(Wr(n),C.textContent=t||`${n.length} ${n.length===1?`company`:`companies`} stored`,C.classList.toggle(`is-empty`,n.length===0&&!t),n.length===0){w.innerHTML=`<p class="empty-copy">no companies yet.</p>`;return}w.innerHTML=n.map(e=>Gr(e)).join(``)}function Wr(e){pn=Array.isArray(e)?e:[],Ot.innerHTML=pn.map(e=>`<option value="${G(e.name)}"></option>`).join(``)}function Gr(e){let t=Array.isArray(e.career_pages)?e.career_pages:[],n=W(e.updated_at),r=Kr(e.prestige_tier),i=Number(e.scan_count??0),a=Number(e.discovered_role_count??0),o=i>0&&a===0?`<span class="company-discovery-status">Discovered 0 potential roles</span>`:``;return`
    <details class="company-panel ${r}" data-company-id="${e.id}">
      <summary class="company-summary">
        <span class="company-chevron">></span>
        <span class="company-summary-main">
          <span class="company-name">${q(e.name)}</span>
          <span class="company-summary-meta">${t.length} ${t.length===1?`link`:`links`}${n?` | updated ${q(n)}`:``}</span>
          ${o}
        </span>
      </summary>
      <div class="company-body">
        <div class="company-info">
          <label class="company-notes-field">
            <span>notes</span>
            <textarea data-company-notes="${e.id}" rows="3">${G(e.notes??``)}</textarea>
          </label>
          <label>
            <span>tier</span>
            <select data-company-tier="${e.id}">
              ${qr(e.prestige_tier)}
            </select>
          </label>
          <div>
            <span>browser wait</span>
            <strong>${Number(e.browser_extra_wait_ms??0)}ms</strong>
          </div>
        </div>
        <div class="company-links">
          ${t.length>0?t.map(e=>Jr(e)).join(``):`<p class="company-empty-links">no career links yet.</p>`}
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
  `}function Kr(e){let t=String(e??``);return[`0`,`1`,`2`,`3`,`4`].includes(t)?`company-tier-${t}`:`company-tier-unset`}function qr(e){let t=String(e??``);return[``,`0`,`1`,`2`,`3`,`4`].map(e=>{let n=e?`tier ${e}`:`not set`,r=e===t?` selected`:``;return`<option value="${G(e)}"${r}>${q(n)}</option>`}).join(``)}function Jr(e){let t=e.label?q(e.label):`career page`,n=G(e.url);return`
    <div class="company-link-row" data-career-page-id="${e.id}">
      <a class="company-link-url" href="${n}" target="_blank" rel="noreferrer">
        <span class="company-link-label">${t}</span>
        <span class="company-link-text">${G(e.url)}</span>
      </a>
      <button class="company-link-delete" type="button" data-delete-career-page="${e.id}" aria-label="delete ${t} link" title="delete link">
        ${Tn()}
      </button>
    </div>
  `}async function Yr(){St.hidden=!1,document.body.classList.add(`companies-open`),Ct.focus(),U?Ur(U):(C.textContent=`loading companies...`,C.classList.remove(`is-empty`),w.innerHTML=``);try{await Zr()}catch{C.textContent=`could not load companies.`}}function Xr(){St.hidden=!0,document.body.classList.remove(`companies-open`),Ie.focus()}async function Zr(e=``){let t=await fetch(`/api/companies`);if(!t.ok)throw Error(`Companies request failed`);Ur(await t.json(),e)}async function Qr(){let e=await fetch(`/api/companies`);if(!e.ok)throw Error(`Companies request failed`);Wr((await e.json()).companies)}async function $r(e){let t=new FormData(e),n={name:String(t.get(`name`)??``),career_url:String(t.get(`career_url`)??``),notes:String(t.get(`notes`)??``)};C.textContent=`adding company...`;let r=await fetch(`/api/companies`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(n)});if(!r.ok)throw Error(`Company create failed`);e.reset(),Ur(await r.json(),`company added.`),hi(hn()).catch(()=>{})}async function ei(e){let t=e.dataset.companyLinkForm;if(!t)return;let n=new FormData(e),r={label:String(n.get(`label`)??``),url:String(n.get(`url`)??``)};C.textContent=`adding link...`;let i=await fetch(`/api/companies/${encodeURIComponent(t)}/career-pages`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(r)});if(!i.ok)throw Error(`Career page create failed`);e.reset(),Ur(await i.json(),`link added.`)}async function ti(e){C.textContent=`deleting link...`;let t=await fetch(`/api/company-career-pages/${encodeURIComponent(e)}`,{method:`DELETE`});if(!t.ok)throw Error(`Career page delete failed`);Ur(await t.json(),`link deleted.`)}async function ni(e){C.textContent=`deactivating company...`;let t=await fetch(`/api/companies/${encodeURIComponent(e)}`,{method:`DELETE`});if(!t.ok)throw Error(`Company deactivate failed`);Ur(await t.json(),`company deactivated.`),hi(hn()).catch(()=>{})}function ri(){let e=Dt.value.trim().toLocaleLowerCase();return pn.find(t=>t.name.toLocaleLowerCase()===e)}async function ii(e){let t=ri();if(!t?.id){kt.textContent=`pick a saved company.`;return}let n=new FormData(e),r={company_id:t.id,role_url:String(n.get(`role_url`)??``)};kt.textContent=`adding role...`;let i=await fetch(`/api/roles`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(r)});if(!i.ok)throw Error(`Role create failed`);let a=await i.json();a.tracker?tr(a.tracker):await hi(hn()),Et.value=``;let o=a.role?.title?K(a.role.title):`role`;kt.textContent=a.scan_error?`${o} added; scan could not finish.`:`${o} added.`}function ai(e){return(Array.isArray(U?.companies)?U.companies:[]).find(t=>String(t.id)===String(e))}function oi(e){C.textContent=e,C.classList.remove(`is-empty`)}function si(e){window.clearTimeout(mn.get(e)),mn.set(e,window.setTimeout(()=>{ci(e).catch(()=>{oi(`could not save company.`)})},700))}async function ci(e){let t=w.querySelector(`[data-company-id="${CSS.escape(String(e))}"]`);if(!t)return;let n=t.querySelector(`[data-company-notes="${CSS.escape(String(e))}"]`),r=t.querySelector(`[data-company-tier="${CSS.escape(String(e))}"]`),i=ai(e),a={notes:n?.value??i?.notes??``,prestige_tier:r?.value??i?.prestige_tier??``};i&&(i.notes=a.notes,i.prestige_tier=a.prestige_tier),li(t,a.prestige_tier),oi(`saving company...`);let o=await fetch(`/api/companies/${encodeURIComponent(e)}`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(a)});if(!o.ok)throw Error(`Company update failed`);U=await o.json(),oi(`company saved.`),ui(e)}function li(e,t){e.classList.remove(`company-tier-unset`,`company-tier-0`,`company-tier-1`,`company-tier-2`,`company-tier-3`,`company-tier-4`),e.classList.add(Kr(t))}function ui(e){let t=w.querySelector(`[data-company-id="${CSS.escape(String(e))}"]`),n=ai(e);if(!t||!n)return;let r=Array.isArray(n.career_pages)?n.career_pages:[],i=W(n.updated_at),a=t.querySelector(`.company-summary-meta`);a&&(a.textContent=`${r.length} ${r.length===1?`link`:`links`}${i?` | updated ${i}`:``}`)}async function di(){let e=await fetch(`/api/scan/status`);if(e.status===404){y.disabled=!0,b.hidden=!0,b.classList.add(`scan-error`),Le.textContent=`restart server to enable scanning`;return}if(!e.ok)throw Error(`Scan status request failed`);nr(await e.json())}function fi(){sn===null&&(sn=window.setInterval(()=>{di().catch(()=>{})},3e3))}async function pi(){y.disabled=!0,y.textContent=`starting...`;try{let e=await fetch(`/api/scan/all`,{method:`POST`});if(e.status===404){y.disabled=!0,y.textContent=`scan roles`,b.hidden=!0,b.classList.add(`scan-error`),Le.textContent=`restart server to enable scanning`;return}if(!e.ok&&e.status!==409)throw Error(`Scan start failed`);nr(await e.json()),fi()}catch{y.disabled=!1,y.textContent=`scan roles`,b.hidden=!0,b.classList.add(`scan-error`),Le.textContent=`could not start scan`}}async function mi(){y.disabled=!0,y.textContent=`cancelling...`;try{let e=await fetch(`/api/scan/cancel`,{method:`POST`});if(e.status===404){y.disabled=!0,y.textContent=`scan roles`,b.hidden=!0,b.classList.add(`scan-error`),Le.textContent=`restart server to enable scanning`;return}if(!e.ok&&e.status!==409)throw Error(`Scan cancel failed`);nr(await e.json()),fi()}catch{y.disabled=!1,y.textContent=`cancel scan`,b.hidden=!1,b.classList.add(`scan-error`),Le.textContent=`could not cancel scan`}}async function hi(e=``){i.innerHTML=`<p class="empty-copy">loading jobs...</p>`;let t=new URLSearchParams;e&&t.set(`q`,e);let n=await fetch(`/api/tracker?${t.toString()}`);if(!n.ok)throw Error(`Tracker request failed`);tr(await n.json())}async function gi(e={}){let t=await fetch(`/api/application-materials`);if(!t.ok)throw Error(`Application materials request failed`);Fn(await t.json(),e)}async function _i(e){if(e){if(!e.name.toLowerCase().endsWith(`.tex`)){kn(It,`resume must be a .tex file.`);return}m.disabled=!0,kn(It,`uploading...`);try{let t=await e.text();if(!(await fetch(`/api/master-resume`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({filename:e.name,content:t})})).ok)throw Error(`Master resume upload failed`);await gi()}catch{kn(It,`could not save resume.`),Ln()}finally{p.value=``,m.disabled=!1}}}async function vi(e){let t=Array.from(e??[]);if(t.length!==0){oe.disabled=!0,Pn(E,`uploading ${t.length} ${t.length===1?`resource`:`resources`}...`);try{for(let e of t)if(!(await fetch(`/api/resume-resources`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({filename:e.name,content_base64:await xi(e)})})).ok)throw Error(`Resume resource upload failed`);await gi()}catch{Pn(E,`could not save every resource.`),Ln()}finally{ae.value=``,oe.disabled=!1}}}async function yi(e){let t=Array.from(e??[]);if(t.length!==0){ue.disabled=!0,jn(D,`uploading ${t.length} ${t.length===1?`example`:`examples`}...`);try{for(let e of t){let t={filename:e.name};if([`.pdf`,`.docx`].some(t=>e.name.toLowerCase().endsWith(t))?t.content_base64=await xi(e):t.content=await e.text(),!(await fetch(`/api/cover-letter-examples`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(t)})).ok)throw Error(`Cover letter example upload failed`)}await gi()}catch{jn(D,`could not save every example.`),Ln()}finally{le.value=``,ue.disabled=!1}}}async function bi(e){let t=Array.from(e??[]);if(t.length!==0){me.disabled=!0,Mn(O,`uploading ${t.length} ${t.length===1?`note`:`notes`}...`);try{for(let e of t){let t=e.name.toLowerCase(),n={filename:e.name};if(t.endsWith(`.pdf`)||t.endsWith(`.docx`)?n.content_base64=await xi(e):n.content=await e.text(),!(await fetch(`/api/experience-notes`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(n)})).ok)throw Error(`Experience note upload failed`)}j.clear(),await gi()}catch{Mn(O,`could not save every note.`),Ln()}finally{pe.value=``,me.disabled=!1}}}function xi(e){return new Promise((t,n)=>{let r=new FileReader;r.addEventListener(`load`,()=>{let e=String(r.result??``);t(e.includes(`,`)?e.split(`,`,2)[1]:e)}),r.addEventListener(`error`,()=>n(r.error)),r.readAsDataURL(e)})}c.addEventListener(`submit`,e=>{e.preventDefault(),hi(l.value.trim()),vn()}),a.addEventListener(`click`,()=>{if(hn()){hi();return}_n()}),l.addEventListener(`keydown`,e=>{e.key===`Escape`&&(e.stopPropagation(),vn())}),u.addEventListener(`click`,vn),s.addEventListener(`click`,vn),m.addEventListener(`click`,()=>{p.click()}),p.addEventListener(`change`,()=>{_i(p.files?.[0])}),oe.addEventListener(`click`,()=>{ae.click()}),ae.addEventListener(`change`,()=>{vi(ae.files)}),ue.addEventListener(`click`,()=>{le.click()}),le.addEventListener(`change`,()=>{yi(le.files)}),me.addEventListener(`click`,()=>{pe.click()}),pe.addEventListener(`change`,()=>{bi(pe.files)}),te.addEventListener(`click`,()=>{Rn(te.getAttribute(`aria-expanded`)===`true`)});async function Si(e){e.disabled=!0;let t=e.textContent;e.textContent=`opening...`;try{if(!(await fetch(`/api/application-materials/index/open`,{method:`POST`})).ok)throw Error(`Could not open the application material index.`)}catch(e){ge.hidden=!1,ge.textContent=e instanceof Error?e.message:`Could not open the application material index.`}finally{e.disabled=!1,e.textContent=t}}ne.addEventListener(`click`,e=>{let t=e.target.closest(`[data-open-material-index]`);if(t){Si(t);return}let n=e.target.closest(`[data-material-view]`);if(n){Vn(n);return}let r=e.target.closest(`[data-material-remove]`);r&&Hn(r)}),y.addEventListener(`click`,()=>{if(ln?.scanning){mi();return}pi()}),i.addEventListener(`click`,e=>{let t=e.target.closest(`[data-view-role-info]`);if(t){try{Fi(t.dataset.viewRoleInfo)}catch{window.alert(`Could not load role information.`)}return}let n=e.target.closest(`[data-review-role-id]`);if(n){Pi(n.dataset.reviewRoleId);return}let r=e.target.closest(`[data-prep-role-id]`);if(r){Ri(r.dataset.prepRoleId);return}let i=e.target.closest(`[data-autoprep-role-id]`);if(i){let e=Ni().find(e=>String(e.id)===String(i.dataset.autoprepRoleId));if(e?.autoprep_started){ka(e.id).catch(()=>{Ke.textContent=`could not open that prepared role. try again.`});return}Aa(i.dataset.autoprepRoleId).catch(()=>{Ke.textContent=`could not add that role to Autoprep. try again.`});return}let a=e.target.closest(`.job-action`);if(a){Ci(a);return}let o=e.target.closest(`.pane-toggle`);if(!o)return;let s=o.parentElement.querySelector(`.pane-body`),c=o.getAttribute(`aria-expanded`)===`true`;o.setAttribute(`aria-expanded`,String(!c)),o.querySelector(`.chevron`).textContent=c?`>`:`v`,s.hidden=c,fo()});async function Ci(e){let{roleId:t,status:n}=e.dataset;if(!t||!n)return;let r=e.closest(`.job-actions`),i=e.closest(`.job`);r.querySelectorAll(`button`).forEach(e=>{e.disabled=!0}),e.textContent=`updating...`;try{let e=await fetch(`/api/roles/${encodeURIComponent(t)}/status`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({status:n})});if(!e.ok)throw Error(`Status update failed`);wi((await e.json()).role,i)}catch{r.querySelectorAll(`button`).forEach(e=>{e.disabled=!1}),e.textContent=n===`disinterested`?`disinterested`:n.toLowerCase()}}function wi(e,t){if(!e||!T)return;let n=t?.closest(`.status-pane`)?.dataset.bucket??e.role_status,r=e.role_status,i=Ei(e,n,r);Di(n,r),Oi(n,r),On(),ji(T.statuses),ki(t,i,n,r),fo()}function Ti(e){if(!e||!T)return null;let t=null;return T.statuses.forEach(n=>{let r=n.jobs.findIndex(t=>String(t.id)===String(e.id));r!==-1&&(t={...n.jobs[r],...e},n.jobs[r]=t)}),ji(T.statuses),t}function Ei(e,t,n){let r=e;T.statuses.forEach(t=>{let n=t.jobs.findIndex(t=>String(t.id)===String(e.id));n!==-1&&(r={...t.jobs[n],...e},t.jobs.splice(n,1),t.count=t.jobs.length)});let i=T.statuses.find(e=>e.key===n);return i&&(i.jobs.unshift(r),i.count=i.jobs.length),r}function Di(e,t){T.statuses.forEach(e=>{let t=document.querySelector(`#status-${CSS.escape(e.key)}`);t?.classList.toggle(`empty`,e.count===0);let n=t?.querySelector(`.count`);n&&(n.textContent=e.count)}),[e,t].forEach(e=>{Ai(document.querySelector(`#status-${CSS.escape(e)}`))})}function Oi(e,t){if(!T.stats)return;let n=Mt.has(e),r=Mt.has(t);if(n===r){Dn(T.stats);return}T.stats.applications_total=Number(T.stats.applications_total??0)+(r?1:-1),Dn(T.stats)}function ki(e,t,n,r){let i=document.querySelector(`#status-${CSS.escape(r)}`),a=i?.querySelector(`.pane-body`);if(!e||!i||!a)return;e.remove(),Ai(document.querySelector(`#status-${CSS.escape(n)}`)),a.hidden=!1;let o=i.querySelector(`.pane-toggle`);o?.setAttribute(`aria-expanded`,`true`);let s=o?.querySelector(`.chevron`);s&&(s.textContent=`v`);let c=a.querySelector(`.jobs`);c||=(a.innerHTML=`<div class="jobs"></div>`,a.querySelector(`.jobs`)),c.insertAdjacentHTML(`afterbegin`,Wn(t,r)),Ai(i)}function Ai(e){if(!e)return;let t=e.querySelector(`.pane-body`);if(!t)return;let n=t.querySelector(`.jobs`),r=!!n?.querySelector(`.job`),i=t.querySelector(`.empty-copy`);if(r){i?.remove();return}n?.remove(),i||t.insertAdjacentHTML(`beforeend`,`<p class="empty-copy">no jobs in this status.</p>`)}function ji(e){ve.disabled=Mi(e).length===0,ve.setAttribute(`aria-label`,`review discovered`),ve.innerHTML=`<span class="review-discovered-label">review discovered</span>`}function Mi(e=T?.statuses??[]){return e.find(e=>e.key===`discovered`)?.jobs??[]}function Ni(e=T?.statuses??[]){return e.find(e=>e.key===`interested`)?.jobs??[]}function Pi(e=null){let t=[...Mi()],n=e==null?null:String(e);if(n){let e=t.findIndex(e=>String(e.id)===n);if(e>0){let[n]=t.splice(e,1);t.unshift(n)}}k=t,h.hidden=!1,document.body.classList.add(`review-open`),Bi()}function Fi(e){let t=String(e),n=(T?.statuses??[]).flatMap(e=>e.jobs??[]).find(e=>String(e.id)===t);if(!n)throw Error(`Role information not found`);be.innerHTML=`
    <div class="review-title-row">
      <p class="review-company">${q(n.company_name)}</p>
      <p class="review-role-title">${q(n.title)}</p>
    </div>
    <dl class="review-details review-primary-details">
      ${Y(`location`,n.location,!1,`review-location-detail`)}
      ${Y(`first`,W(n.first_seen_at))}
      ${Y(`last`,W(n.last_seen_at))}
    </dl>
    ${Hi(n.description)}
    <dl class="review-details review-technical-details">
      ${Y(`notes`,n.notes,!1,`review-wide-detail`)}
      ${Y(`company id`,n.company_id)}
      ${Y(`role id`,n.id)}
      ${Y(`status`,n.role_status)}
      ${Y(`posting id`,n.posting_id)}
      ${Y(`created`,W(n.created_at))}
      ${Y(`updated`,W(n.updated_at))}
      ${Y(`url`,n.role_url,!1,`review-wide-detail`)}
    </dl>
  `,ye.hidden=!1,document.body.classList.add(`review-open`),xe.focus()}function Ii(){ye.hidden=!0,be.innerHTML=``,document.body.classList.remove(`review-open`)}function Li(){h.hidden=!0,document.body.classList.remove(`review-open`),k=[]}function Ri(e=null){let t=[...Ni()].sort((e,t)=>Number(!!t.prep_started)-Number(!!e.prep_started)),n=e==null?null:String(e);if(n){let e=t.findIndex(e=>String(e.id)===n);if(e>0){let[n]=t.splice(e,1);t.unshift(n)}}A=t,g.hidden=!1,document.body.classList.add(`prep-open`),na()}function zi(){g.hidden=!0,document.body.classList.remove(`prep-open`),A=[]}function Bi(e=``){let t=k[0],n=k.length,r=t?Vi(t):``;if(Se.textContent=n>0?`review queue`:`review complete`,Ce.textContent=n>0?`${n} discovered ${n===1?`role`:`roles`} in queue`:``,h.querySelectorAll(`.review-action`).forEach(e=>{e.disabled=n===0}),!t){we.innerHTML=`
      <div class="review-empty">
        <h3>no discovered jobs left.</h3>
        <p>everything in this queue has been handled or moved out of discovered.</p>
      </div>
    `;return}we.innerHTML=`
    ${e?`<p class="review-message">${G(e)}</p>`:``}
    ${r?`<p class="review-message review-message-warning">${G(r)}</p>`:``}
    <div class="review-title-row">
      <p class="review-company">${q(t.company_name)}</p>
      ${En(t.title,t.role_url,`review-role-title`)}
    </div>
    <dl class="review-details review-primary-details">
      ${Y(`location`,t.location,!1,`review-location-detail`)}
      ${Y(`first`,W(t.first_seen_at))}
      ${Y(`last`,W(t.last_seen_at))}
    </dl>
    ${Hi(t.description)}
    <dl class="review-details review-technical-details">
      ${Y(`notes`,t.notes,!1,`review-wide-detail`)}
      ${Y(`company id`,t.company_id)}
      ${Y(`role id`,t.id)}
      ${Y(`status`,t.role_status)}
      ${Y(`posting id`,t.posting_id)}
      ${Y(`created`,W(t.created_at))}
      ${Y(`updated`,W(t.updated_at))}
      ${Y(`url`,t.role_url,!0,`review-wide-detail`)}
    </dl>
  `}function Vi(e){let t=Number(e.review_later_count??0);return t<=At?``:`role review has been postponed ${t} times. it is recommended to set it to disinterested.`}function Y(e,t,n=!1,r=``){if(!t)return``;let i=n?`<a href="${G(t)}" target="_blank" rel="noreferrer">${q(t)}</a>`:q(t);return`
    <div class="review-detail ${G(r)}">
      <dt>${q(e)}</dt>
      <dd>${i}</dd>
    </div>
  `}function Hi(e){return e?`
    <div class="review-detail review-description">
      <dt>description</dt>
      <dd>${Ui(e)}</dd>
    </div>
  `:``}function Ui(e){let t=Wi(String(e)).replace(/\u00a0/g,` `);if(Gi(t))return Ki(t);let n=t.split(/\r?\n/).map(e=>e.trim()).filter(Boolean),r=[],i=[],a=()=>{i.length!==0&&(r.push(`<ul>${i.map(e=>`<li>${e}</li>`).join(``)}</ul>`),i=[])};return n.forEach(e=>{let t=e.match(/^#{2,3}\s+(.+)$/);if(t){a(),r.push(`<h3>${q(t[1])}</h3>`);return}if(ea(e)){a(),r.push(`<h3>${q(e.replace(/:$/,``))}</h3>`);return}let n=e.match(/^[-*]\s+(.+)$/);if(n){i.push(q(n[1]));return}a(),r.push(`<p>${q(e)}</p>`)}),a(),r.join(``)}function Wi(e){let t=document.createElement(`textarea`);return t.innerHTML=e,t.value}function Gi(e){return/<\/?(?:a|br|div|em|h[1-6]|li|ol|p|span|strong|ul)\b/i.test(e)}function Ki(e){let t=document.createElement(`template`);t.innerHTML=e;let n=[];return qi(t.content.childNodes,n),n.join(``)}function qi(e,t){e.forEach(e=>{if(e.nodeType===Node.TEXT_NODE){let n=Qi(e.textContent);n&&t.push(`<p>${q(n)}</p>`);return}if(e.nodeType!==Node.ELEMENT_NODE)return;let n=e,r=n.tagName.toLowerCase();if(r===`script`||r===`style`||r===`br`)return;if(/^h[1-6]$/.test(r)){Yi(t,n.textContent);return}if(r===`ul`||r===`ol`){let e=Xi(n);e&&t.push(e);return}if(r===`p`){Ji(n,t);return}let i=Array.from(n.children).some(e=>[`DIV`,`H1`,`H2`,`H3`,`H4`,`H5`,`H6`,`OL`,`P`,`UL`].includes(e.tagName));if([`article`,`div`,`section`].includes(r)&&i){qi(n.childNodes,t);return}let a=Array.from(n.children).filter(e=>[`UL`,`OL`].includes(e.tagName)),o=Qi(Zi(n));if(o&&($i(o,n)?Yi(t,o):t.push(`<p>${q(o)}</p>`)),a.length>0){a.forEach(e=>{let n=Xi(e);n&&t.push(n)});return}!o&&i&&qi(n.childNodes,t)})}function Ji(e,t){if(!e.querySelector(`br`)){let n=Qi(Zi(e));if(!n)return;$i(n,e)?Yi(t,n):t.push(`<p>${q(n)}</p>`);return}let n=``,r=()=>{let r=Qi(n);n=``,r&&($i(r,e)?Yi(t,r):t.push(`<p>${q(r)}</p>`))};e.childNodes.forEach(e=>{if(e.nodeType===Node.ELEMENT_NODE&&e.tagName.toLowerCase()===`br`){r();return}n+=` ${e.textContent??``}`}),r()}function Yi(e,t){let n=Qi(t).replace(/:$/,``);n&&e.push(`<h3>${q(n)}</h3>`)}function Xi(e){let t=Array.from(e.children).filter(e=>e.tagName===`LI`).map(e=>{let t=Qi(Zi(e)),n=Array.from(e.children).filter(e=>[`UL`,`OL`].includes(e.tagName)).map(e=>Xi(e)).filter(Boolean).join(``);return t||n?`<li>${q(t)}${n}</li>`:``}).filter(Boolean);return t.length>0?`<ul>${t.join(``)}</ul>`:``}function Zi(e){let t=e.cloneNode(!0);return t.querySelectorAll(`ul, ol`).forEach(e=>{e.remove()}),t.textContent}function Qi(e){return String(e??``).replace(/\s+/g,` `).trim()}function $i(e,t){let n=e.replace(/:$/,``).trim();return!n||n.length>90?!1:ea(n)||/:$/.test(e)?!0:/[.!?]$/.test(n)||n.split(/\s+/).length>10?!1:t.querySelector(`strong, b, u`)?!0:ea(n)}function ea(e){return Pt.test(String(e).trim())}async function ta(e){let t=k[0];if(!t)return;if(e===`later`){h.querySelectorAll(`.review-action`).forEach(e=>{e.disabled=!0});try{let e=await Ea(t.id);k.shift(),Ti(e),Bi(`moved out of this review pass.`)}catch{Bi(`could not postpone that role. try again.`)}finally{h.querySelectorAll(`.review-action`).forEach(e=>{e.disabled=k.length===0})}return}if(![`interested`,`disinterested`].includes(e))return;let n=h.querySelectorAll(`.review-action`);n.forEach(e=>{e.disabled=!0});try{let n=await Da(t.id,e);k.shift(),Bi(e===`interested`?`marked interested.`:`marked disinterested.`),wi(n,document.querySelector(`.job[data-role-id="${CSS.escape(String(t.id))}"]`))}catch{n.forEach(e=>{e.disabled=!1}),Bi(`could not update that role. try again.`)}}async function na(e=``){let t=A[0],n=A.length;Ee.textContent=n>0?`prep queue`:`prep complete`,De.textContent=n>0?`${n} interested ${n===1?`role`:`roles`} in queue`:``,g.querySelectorAll(`.review-action`).forEach(e=>{e.disabled=n===0});let r=g.querySelector(`[data-prep-action="autoprep"]`);if(r&&(r.textContent=t?.autoprep_started?`view / regenerate prep`:`autoprep`),!t){_.innerHTML=`
      <div class="review-empty">
        <h3>no interested jobs left.</h3>
        <p>everything in this queue has been prepped, moved, or postponed.</p>
      </div>
    `;return}_.innerHTML=`
    ${e?`<p class="review-message">${G(e)}</p>`:``}
    <section class="prep-role-hero" aria-label="role overview">
      <div class="review-title-row">
        <div class="prep-role-eyebrow">
          <p class="review-company">${q(t.company_name)}</p>
          <span>application workspace</span>
        </div>
        ${En(t.title,t.role_url,`review-role-title`)}
      </div>
      <dl class="review-details review-primary-details">
        ${Y(`location`,t.location,!1,`review-location-detail`)}
        ${Y(`last`,W(t.last_seen_at))}
        ${Y(`updated`,W(t.updated_at))}
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
      ${ra(t)}
      ${sa(t)}
      ${ia(t.id,t.description)}
      ${aa(t)}
    </div>
  `,Sn(),ma(t.id).then(e=>{!e||A[0]?.id!==t.id||(M.set(t.id,e),_.querySelector(`.prep-resume`)?.replaceWith(X(ra(t,{resume:e}))),Sn())}).catch(()=>{}),Ta(t.id).then(e=>{!e||A[0]?.id!==t.id||(N.set(t.id,e),_.querySelector(`.prep-cover-letter`)?.replaceWith(X(sa(t,{coverLetter:e}))),Sn())}).catch(()=>{})}function ra(e,t={}){let n=M.get(e.id),r=t.resume??n,i=t.tweaks??zt.get(e.id)??``,a=`/api/roles/${encodeURIComponent(e.id)}/resume.pdf`;return t.loading?`
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
          ${r.pdf_base64?`<a class="prep-summary-action prep-cover-pdf-link" href="${G(a)}" target="_blank" rel="noreferrer">view</a>`:``}
        </div>
      </summary>
      <p class="prep-overview">${q(r.summary??`Saved resume for this role.`)}</p>
      ${ca(e)}
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
          >${G(i)}</textarea>
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
          >${G(r.latex??``)}</textarea>
        </label>
        <section class="prep-document-preview" aria-label="resume preview">
          <div class="prep-preview-heading">
            <span>document preview</span>
            <p>Updates automatically after the source is saved.</p>
          </div>
          ${r.pdf_base64?`
                <iframe class="prep-cover-pdf" title="resume PDF preview" src="${G(a)}"></iframe>
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
    `}function ia(e,t){return`
    <details class="prep-panel prep-description-panel" id="prep-description-${e}">
      <summary class="prep-analysis-header">
        <span class="prep-accordion-icon" aria-hidden="true"></span>
        <h3>description</h3>
      </summary>
      ${Hi(t)}
    </details>
  `}function aa(e,t={}){let n=t.messages??Bt.get(e.id)??[],r=!!t.loading;return`
    <details class="prep-panel prep-role-chat" id="prep-chat-${e.id}">
      <summary class="prep-analysis-header">
        <span class="prep-accordion-icon" aria-hidden="true"></span>
        <h3>chat about this role</h3>
        <span>${n.length?`${n.length} messages`:`ready`}</span>
      </summary>
      <div class="prep-role-chat-log" aria-live="polite">
        ${n.length?n.map(oa).join(``):`<p class="prep-role-chat-empty">ask about fit, risks, resume emphasis, or cover letter angle.</p>`}
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
  `}function oa(e){let t=e?.role===`assistant`?`assistant`:`user`;return`
    <article class="prep-role-chat-message prep-role-chat-message-${t}">
      <span>${t}</span>
      <p>${q(e?.content??``)}</p>
    </article>
  `}function sa(e,t={}){let n=N.get(e.id),r=t.coverLetter??n,i=t.tweaks??r?.tweaks??``,a=`/api/roles/${encodeURIComponent(e.id)}/cover-letter.pdf`;return t.loading?`
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
          ${r?.pdf_base64?`<a class="prep-summary-action prep-cover-pdf-link" href="${G(a)}" target="_blank" rel="noreferrer">view</a>`:``}
        </div>
      </summary>
      ${r?`<p class="prep-overview">${q(r.summary??`cover letter generated`)}</p>`:`<p class="prep-overview">generate a LaTeX cover letter from the resume, posting, and stored examples.</p>`}
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
                >${G(i)}</textarea>
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
                >${G(r.latex??``)}</textarea>
              </label>
              <section class="prep-document-preview" aria-label="cover letter preview">
                <div class="prep-preview-heading">
                  <span>document preview</span>
                  <p>Updates automatically after the source is saved.</p>
                </div>
                ${r.pdf_base64?`
                      <iframe class="prep-cover-pdf" title="cover letter PDF preview" src="${G(a)}"></iframe>
                    `:`<p class="prep-cover-path">PDF preview unavailable.</p>`}
              </section>
            </div>
          `:``}
    </details>
  `}function ca(e,t={}){let n=j.get(e.id);if(!t.loading&&!t.error&&!t.analysis&&n)return ca(e,{analysis:n});if(!t.loading&&!t.error&&!t.analysis)return`
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
    `;let r=t.analysis,i=Array.isArray(r?.feedback_items)?r.feedback_items:[],a=r?.verdict===`ready_to_apply`?`ready to apply`:`tweak`,o=Math.min(Rt.get(e.id)??0,Math.max(i.length-1,0)),s=i[o];return`
    <section class="prep-analysis" aria-label="ai analysis">
      <div class="prep-analysis-header">
        <h3>ai analysis</h3>
        <span>${i.length} ${i.length===1?`item`:`items`}</span>
      </div>
      <p class="prep-verdict">${q(a)}</p>
      <p class="prep-overview">${q(r?.overview??`analysis unavailable`)}</p>
      ${s?`
            <article class="prep-feedback" data-feedback-index="${o}">
              <p class="prep-feedback-label">${q(s.label)}</p>
              <h4>${q(s.title)}</h4>
              <p>${q(s.detail)}</p>
              ${la(s)}
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
  `}function la(e){return e?.tweak_prompt?`
    <div class="prep-proposed-edit">
      <p class="prep-proposed-label">tweak prompt</p>
      <p>${q(e.tweak_prompt)}</p>
    </div>
  `:`
      <div class="prep-proposed-edit">
        <p class="prep-proposed-label">feedback only</p>
        <p>not enough information to turn this into a safe resume tweak.</p>
      </div>
    `}async function ua(e,t={}){if(!t.force&&j.has(e))return j.get(e);let n=await fetch(`/api/roles/${encodeURIComponent(e)}/prep-analysis`);if(!n.ok)throw Error(`Prep analysis request failed`);let r=await n.json();return r.analysis.resources=r.resources??[],j.set(e,r.analysis),r.analysis}function X(e){let t=document.createElement(`template`);return t.innerHTML=e.trim(),t.content.firstElementChild}async function da(e){let t=A[0];if(!t)return;let n=g.querySelectorAll(`.review-action`);if(n.forEach(e=>{e.disabled=!0}),e===`later`){try{await Ea(t.id),t.review_later_count=Number(t.review_later_count??0)+1,A.length>1?(A.push(A.shift()),na(`moved to the back of the prep queue.`)):na(`only one role is in the prep queue.`)}catch{na(`could not postpone prep. try again.`)}return}if(e===`autoprep`){try{if(t.autoprep_started){await ka(t.id);return}await Aa(t.id)}catch{na(`could not add that role to Autoprep. try again.`)}return}if(e===`applied`)try{let e=await Da(t.id,`applied`);A.shift(),na(`moved to applied.`),wi(e,document.querySelector(`.job[data-role-id="${CSS.escape(String(t.id))}"]`))}catch{n.forEach(e=>{e.disabled=!1}),na(`could not move that role. try again.`)}}async function fa(e,t,n,r){let i=await fetch(`/api/roles/${encodeURIComponent(e)}/prep-feedback`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({feedback_index:t,feedback_item:n,comment:r})});if(!i.ok)throw Error(`Prep feedback update failed`);return i.json()}async function pa(e,t,n,r){let i=await fetch(`/api/roles/${encodeURIComponent(e)}/prep-feedback-ignore`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({feedback_index:t,feedback_item:n,comment:r})});if(!i.ok)throw Error(`Prep feedback ignore failed`);return i.json()}async function ma(e,{force:t=!1}={}){if(!t&&M.has(e))return M.get(e);let n=await fetch(`/api/roles/${encodeURIComponent(e)}/resume`);if(!n.ok)throw Error(`Resume request failed`);let r=await n.json();return r.resume&&M.set(e,r.resume),r.resume}async function ha(e,t){let n=await fetch(`/api/roles/${encodeURIComponent(e)}/resume/save`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({latex:t})});if(!n.ok)throw Error(`Resume save failed`);return n.json()}async function ga(e,t,n){let r=await fetch(`/api/roles/${encodeURIComponent(e)}/resume`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({tweaks:t,previous_latex:n})});if(!r.ok)throw Error(`Resume generation failed`);return r.json()}async function _a(e,t){let n=await fetch(`/api/roles/${encodeURIComponent(e)}/chat`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({messages:t})});if(!n.ok)throw Error(`Role chat failed`);return n.json()}function va(e,t,n=jt){let r=Vt.get(e)??{timer:null,saving:!1,version:0,latex:``};r.version+=1,r.latex=t,r.timer&&clearTimeout(r.timer),r.timer=setTimeout(()=>{r.timer=null,ya(e)},n),Vt.set(e,r)}async function ya(e){let t=Vt.get(e);if(!t||t.saving)return;t.saving=!0;let n=t.version,r=t.latex;try{let i=await ha(e,r);t.version===n&&(M.set(e,i.resume),ba(`resume`,e,i.resume))}catch{}finally{t.saving=!1,t.version!==n&&va(e,t.latex,0)}}function ba(e,t,n){if(!n?.pdf_base64)return;let r=e===`resume`?`[data-prep-resume-latex="${t}"]`:`[data-prep-cover-letter-latex="${t}"]`,i=_.querySelector(r)?.closest(`.prep-panel`),a=i?.querySelector(`.prep-cover-pdf`),o=i?.querySelector(`.prep-cover-pdf-link`),s=e===`resume`?`/api/roles/${encodeURIComponent(t)}/resume.pdf`:`/api/roles/${encodeURIComponent(t)}/cover-letter.pdf`;a&&(a.src=`${s}?v=${Date.now()}`),o&&(o.href=s)}async function xa(e,t=``,n=``){let r=await fetch(`/api/roles/${encodeURIComponent(e)}/cover-letter`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({tweaks:t,previous_latex:n})});if(!r.ok)throw Error(`Cover letter generation failed`);return r.json()}async function Sa(e,t){let n=await fetch(`/api/roles/${encodeURIComponent(e)}/cover-letter/save`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({latex:t})});if(!n.ok)throw Error(`Cover letter save failed`);return n.json()}function Ca(e,t,n=``,r=jt){let i=Ht.get(e)??{timer:null,saving:!1,version:0,latex:``,tweaks:``};i.version+=1,i.latex=t,i.tweaks=n,i.timer&&clearTimeout(i.timer),i.timer=setTimeout(()=>{i.timer=null,wa(e)},r),Ht.set(e,i)}async function wa(e){let t=Ht.get(e);if(!t||t.saving)return;t.saving=!0;let n=t.version,r=t.latex,i=t.tweaks;try{let a=await Sa(e,r);t.version===n&&(N.set(e,{...a.cover_letter,tweaks:i}),ba(`coverLetter`,e,a.cover_letter))}catch{}finally{t.saving=!1,t.version!==n&&Ca(e,t.latex,t.tweaks,0)}}async function Ta(e){if(N.has(e))return N.get(e);let t=await fetch(`/api/roles/${encodeURIComponent(e)}/cover-letter`);if(!t.ok)throw Error(`Cover letter request failed`);let n=await t.json();return n.cover_letter&&N.set(e,n.cover_letter),n.cover_letter}async function Ea(e){let t=await fetch(`/api/roles/${encodeURIComponent(e)}/review-later`,{method:`POST`});if(!t.ok)throw Error(`Review later update failed`);return(await t.json()).role}async function Da(e,t){let n=await fetch(`/api/roles/${encodeURIComponent(e)}/status`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({status:t})});if(!n.ok)throw Error(`Status update failed`);return(await n.json()).role}function Oa(e){return`${e}-${globalThis.crypto?.randomUUID?.()??`${Date.now()}-${Math.random()}`}`}async function ka(e){let t=Number(e);!Number.isInteger(t)||t<=0||(F=t,g.hidden||zi(),await Ma())}async function Aa(e){let t=Number(e);if(!Number.isInteger(t)||t<=0||Gt.has(t))return null;Gt.add(t);let n=document.querySelectorAll(`[data-autoprep-role-id="${CSS.escape(String(t))}"]`);n.forEach(e=>{e.disabled=!0,e.setAttribute(`aria-busy`,`true`),e.textContent=`queuing...`});try{let e=await fetch(`/api/autoprep/jobs`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({role_ids:[t],idempotency_key:Oa(`autoprep-role-${t}`)})}),n=await e.json();if(!e.ok)throw Error(n.error||`Autoprep request failed`);let r=Array.isArray(n.jobs)?n.jobs:[],i=new Map(P.map(e=>[Number(e.role_id),e]));r.forEach(e=>i.set(Number(e.role_id),e));let a=r.find(e=>Number(e.role_id)===t),o=Ni().find(e=>Number(e.id)===t);return a&&o&&T&&(o.autoprep_started=!0,o.autoprep_status=a.overall_status??`queued`,tr(T)),F=t,g.hidden||zi(),await Ma({seedJobs:[...i.values()]}),r}finally{Gt.delete(t),n.forEach(e=>{e.disabled=!1,e.removeAttribute(`aria-busy`),e.textContent=Ni().find(e=>Number(e.id)===t)?.autoprep_started?`view / regenerate prep`:`autoprep`})}}function ja(e){window.location.hash!==e&&window.history.pushState({},``,e||`${window.location.pathname}${window.location.search}`)}async function Ma({seedJobs:e=null}={}){Ae.hidden=!1,document.body.classList.add(`prepped-open`),ja(`#prepped-roles`),e?(P=e,F=F??P[0]?.role_id??null,Q()):P.length===0&&(Me.textContent=`loading prepared roles...`),await Pa(),Fa()}function Na({clearHash:e=!0}={}){Ae.hidden=!0,document.body.classList.remove(`prepped-open`),Ia(),R.clear(),Jt.clear(),H.forEach(e=>URL.revokeObjectURL(e)),H.clear(),tn.clear(),nn.clear(),e&&window.location.hash===`#prepped-roles`&&ja(``)}window.addEventListener(`pagehide`,()=>{document.querySelectorAll(`[data-preview-blob-url]`).forEach(e=>{URL.revokeObjectURL(e.dataset.previewBlobUrl)}),H.forEach(e=>URL.revokeObjectURL(e)),H.clear(),tn.clear()});async function Pa(){try{let e=await fetch(`/api/autoprep/jobs`);if(!e.ok)throw Error(`Prepped roles request failed`);let t=await e.json();P=t.jobs??[];let n=t.bulk_cover_letter_regeneration;if(n){let e=Array.isArray(n.jobs)?n.jobs:[];L={idempotencyKey:n.idempotency_key,roleIds:e.map(e=>Number(e.role_id)),jobs:e,skipped:Array.isArray(n.skipped)?n.skipped:[]}}P.some(e=>Number(e.role_id)===Number(F))||(F=P[0]?.role_id??null),Q()}catch{Me.textContent=`could not refresh preparation progress.`}}function Fa(){Ia(),P.some(La)&&(Ut=window.setInterval(Pa,2e3))}function Ia(){Ut!==null&&window.clearInterval(Ut),Ut=null}function La(e){return[`queued`,`generating_resume_tweaks`,`regenerating_resume`,`generating_cover_letter`].includes(e.overall_status)}function Ra(e){return[e.resume_status,e.cover_letter_status].some(e=>[`failed`,`interrupted`].includes(e))}function za(e){return e.cover_letter_status===`generating`||e.overall_status===`generating_cover_letter`}function Ba(e){return za(e)||e.resume_status===`generating_tweaks`||e.resume_status===`regenerating`||e.overall_status===`generating_resume_tweaks`||e.overall_status===`regenerating_resume`}function Va(e){return e.worker_state===`queued`||e.overall_status===`queued`}function Ha(e){return{queued:`Queued`,generating_resume_tweaks:`Generating resume tweaks`,regenerating_resume:`Regenerating resume`,generating_cover_letter:`Generating cover letter`,partially_complete:`Partially complete`,ready:`Ready`,failed:`Failed`,interrupted:`Interrupted`,generating_tweaks:`Generating tweaks`,regenerating:`Regenerating`,generating:`Generating`}[e]??K(e)}function Ua(e,t){let n=t===`cover-letter`?`cover_letter`:`resume`;return`${e.updated_at||``}:${e[`${n}_artifact_path`]||``}`}function Z(e,{close:t=!1}={}){let n=H.get(e);n&&URL.revokeObjectURL(n),H.delete(e),tn.delete(e),nn.delete(e),t&&R.delete(e)}function Wa(){tn.forEach((e,t)=>{let[n,r]=t.split(`:`),i=P.find(e=>Number(e.role_id)===Number(n));(!i||Ua(i,r)!==e)&&Z(t,{close:!0})})}function Ga(){if(!L)return;let e=L.jobs||P,t=new Map(e.map(e=>[Number(e.role_id),e])),n=L.roleIds.map(e=>t.get(Number(e))),r=n.filter(e=>e?.worker_state===`idle`&&e.cover_letter_status===`ready`).length,i=n.filter(e=>!e||e.worker_state===`idle`&&[`failed`,`interrupted`].includes(e.cover_letter_status)),a=n.length-r-i.length,o=L.skipped.length?` Skipped before queueing: ${L.skipped.map(e=>`${e.company_name} — ${e.title}: ${e.reason}`).join(` · `)}`:``,s=i.length?` Queued regeneration failures: ${i.map(e=>e?`${e.company_name} — ${e.title}: ${e.cover_letter_error||`generation failed`}`:`A role left the Prepped queue before regeneration completed`).join(` · `)}`:``;I=n.length?a>0?`Cover-letter regeneration in progress: ${r} of ${n.length} complete · ${a} remaining.${o}${s}`:`Cover-letter regeneration complete: ${r} succeeded, ${i.length} failed.${o}${s}`:`No cover letters were queued.${o}`}function Q(){Wa(),Ga();let e=P.filter(La).length,t=P.filter(e=>e.worker_state===`idle`&&e.cover_letter_status===`ready`).length;Me.textContent=P.length?`${P.length} prepped ${P.length===1?`role`:`roles`}${e?` · ${e} in progress`:``}`:`No queued or prepared roles.`,Ne.disabled=Wt||t===0,Ne.setAttribute(`aria-busy`,Wt?`true`:`false`),Ne.textContent=Wt?`queuing cover letters...`:`regenerate all cover letters`,Pe.textContent=I,Fe.innerHTML=P.map(e=>{let t=Ra(e),n=!t&&Ba(e),r=!t&&!n&&Va(e),i=Number(e.role_id)===Number(F)?` is-active`:``;return`
      <button type="button" class="prepped-list-item${r?` is-generation-queued`:``}${n?` is-document-generating`:``}${t?` has-generation-failure`:``}${i}" data-prepped-role="${e.role_id}">
        <strong>${q(e.company_name)}</strong><span>${q(e.title)}</span>
        <small class="status-${G(e.overall_status)}">${G(Ha(e.overall_status))}</small>
      </button>`}).join(``),$(),Fa()}function $(){let e=P.findIndex(e=>Number(e.role_id)===Number(F)),t=P[e];if(!t){v.innerHTML=`<div class="prepped-empty"><h3>nothing prepped yet.</h3><p>Queue Interested roles from Autoprep Interested.</p></div>`;return}let n=q(t.title),r=bn(t.role_url),i=r?`<a class="prepped-role-link" href="${G(r)}" target="_blank" rel="noopener noreferrer">${n}<span aria-hidden="true">↗</span></a>`:n,a=[[`Location`,t.location||`Unavailable`],[`Added`,W(t.date_added||t.created_at)||`Unavailable`],[`Last seen`,W(t.last_seen_at)||`Unavailable`],[`Posting ID`,t.posting_id||`Unavailable`]],o=Kt.has(Number(t.role_id)),s=o||La(t),c=`${t.role_id}:description`,l=`${t.role_id}:notes`;v.innerHTML=`
    <header class="prepped-detail-heading">
      <div><p class="eyebrow">${q(t.company_name)}</p><h3>${i}</h3></div>
      <span class="prepped-status status-${G(t.overall_status)}">${G(Ha(t.overall_status))}</span>
    </header>
    <dl class="prepped-role-facts">${a.map(([e,t])=>`<div><dt>${G(e)}</dt><dd>${q(t)}</dd></div>`).join(``)}</dl>
    <details class="prepped-role-description" data-prepped-detail-section="description" ${Jt.has(c)?`open`:``}>
      <summary>Job description</summary>
      <div class="prepped-description-copy">${q(t.description||`No job description was saved.`).replaceAll(`
`,`<br>`)}</div>
    </details>
    ${t.notes?`<details class="prepped-role-description" data-prepped-detail-section="notes" ${Jt.has(l)?`open`:``}><summary>Role notes</summary><div class="prepped-description-copy">${q(t.notes).replaceAll(`
`,`<br>`)}</div></details>`:``}
    <div class="prepped-document-grid">
      ${no(t,`resume`,`Resume`)}
      ${no(t,`cover-letter`,`Cover letter`)}
    </div>
    ${qa(t)}
    <div class="prepped-detail-actions">
      <button class="prepped-nav-action" type="button" data-prepped-nav="previous" ${e<=0?`disabled`:``}>Previous</button>
      <button class="prepped-nav-action" type="button" data-prepped-nav="next" ${e>=P.length-1?`disabled`:``}>Next</button>
      <button class="prepped-folder-action" type="button" data-autoprep-open-folder ${t.artifact_directory?``:`disabled`}>Open Documents Folder</button>
      <button class="prepped-disinterested" type="button" data-autoprep-disinterested aria-busy="${o?`true`:`false`}" ${s?`disabled`:``} title="${La(t)?`Wait for preparation to finish before moving this role`:`Move this role out of Prepped`}">${o?`Moving to Disinterested...`:`Move to Disinterested`}</button>
      <button class="success" type="button" data-autoprep-applied ${t.overall_status===`ready`?``:`disabled`}>Applied</button>
    </div>
    <p class="prepped-safety-note">Autoprep prepares files only. It never submits an application.</p>`,Xt.has(Number(t.role_id))||Ya(t.role_id)}function Ka(e){return Array.isArray(e)?e:Array.isArray(e?.answers)?e.answers:e?.answer&&typeof e.answer==`object`?[e.answer]:e?.record&&typeof e.record==`object`?[e.record]:e&&typeof e==`object`&&(`question`in e||`answer`in e||`status`in e||`error`in e)?[e]:[]}function qa(e){let t=Number(e.role_id),n=z.get(t)??[],r=Yt.get(t)??``,i=B.has(t),a=Zt.has(t),o=V.get(t);return`<section class="application-questions-workspace" aria-labelledby="application-questions-heading-${t}">
    <div class="application-questions-heading"><div><p class="eyebrow">Application helper</p><h4 id="application-questions-heading-${t}">Application questions</h4></div><span>${n.length} saved</span></div>
    <p class="application-questions-intro">Paste a question from an application form to generate and keep a role-specific answer.</p>
    <div class="application-answer-history" aria-live="polite">
      ${a&&!n.length?`<p class="application-answer-empty">Loading saved answers…</p>`:``}
      ${o?`<p class="prepped-error">${q(o)}</p>`:``}
      ${!a&&!o&&!n.length?`<p class="application-answer-empty">No application questions saved yet.</p>`:``}
      ${n.map((e,t)=>Ja(e,t,i)).join(``)}
    </div>
    <div class="application-question-composer">
      <label for="application-question-${t}">Question</label>
      <textarea id="application-question-${t}" data-application-question-draft rows="4" placeholder="Paste an application question…" ${i?`disabled`:``}>${G(r)}</textarea>
      <div><small>Answers are saved to this role. Asking never changes its status.</small><button class="application-question-submit" type="button" data-application-question-submit aria-busy="${i?`true`:`false`}" ${i||!r.trim()?`disabled`:``}>${i?`Generating…`:`Generate answer`}</button></div>
    </div>
  </section>`}function Ja(e,t,n){let r=e?.status??`saved`,i=e?.created_at??e?.updated_at??e?.timestamp,a=e?.backend??e?.generation_backend,o=Number(e?.id),s=Number.isFinite(o)&&r!==`pending`&&!n,c=Qt.has(o),l=$t.has(o),u=en.has(o);return`<article class="application-answer-record status-${G(r)}">
    <div class="application-answer-meta"><span>${q(r)}</span>${a?`<span>${q(a)}</span>`:``}${i?`<time datetime="${G(i)}">${q(W(i)||i)}</time>`:``}</div>
    <h5>${G(e.question??`Question unavailable`)}</h5>
    ${e.answer?`<p class="application-answer-copy">${G(e.answer).replaceAll(`
`,`<br>`)}</p>`:``}
    ${e.error?`<p class="prepped-error">${q(e.error)}</p>`:``}
    <div class="application-answer-actions">
      ${e.answer?`<button type="button" data-application-answer-copy="${t}">Copy answer</button>`:``}
      ${Number.isFinite(o)?`<button type="button" data-application-answer-regenerate="${o}" ${s?``:`disabled`}>${l||r===`pending`?`Regenerating…`:`Regenerate`}</button><button class="danger" type="button" data-application-answer-delete="${o}" ${s?``:`disabled`}>${u?`Deleting…`:c?`Confirm delete`:`Delete question`}</button>`:``}
    </div>
  </article>`}async function Ya(e){let t=Number(e);if(!Zt.has(t)){Zt.add(t),V.delete(t);try{let n=await fetch(`/api/autoprep/roles/${encodeURIComponent(e)}/application-answers`),r=await n.json();if(!n.ok)throw Error(r?.error||`Could not load saved answers.`);z.set(t,Ka(r)),Xt.add(t)}catch(e){V.set(t,e instanceof Error?e.message:`Could not load saved answers.`)}finally{Zt.delete(t),Number(F)===t&&$()}}}async function Xa(e){if(navigator.clipboard?.writeText)try{await navigator.clipboard.writeText(e);return}catch{}let t=document.createElement(`textarea`);t.value=e,t.readOnly=!0,t.style.position=`fixed`,t.style.opacity=`0`,document.body.append(t),t.select();let n=document.execCommand(`copy`);if(t.remove(),!n)throw Error(`Clipboard copy is unavailable`)}async function Za(e){let t=Number(e),n=String(Yt.get(t)??``).trim();if(!(!n||B.has(t))){B.add(t),$();try{let r=await fetch(`/api/autoprep/roles/${encodeURIComponent(e)}/application-answers`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({question:n})}),i=await r.json(),a=Ka(i),o=z.get(t)??[];if(Array.isArray(i?.answers)?z.set(t,a):a.length&&z.set(t,[...o,...a]),!r.ok)throw Error(i?.error||a[0]?.error||`Could not generate an answer.`);Yt.delete(t),Xt.add(t),V.delete(t)}catch(e){V.set(t,e instanceof Error?e.message:`Could not generate an answer.`)}finally{B.delete(t),Number(F)===t&&$()}}}function Qa(e,t){let n=Number(e),r=z.get(n)??[],i=Number(t?.id),a=r.findIndex(e=>Number(e?.id)===i);if(a<0){z.set(n,[t,...r]);return}let o=[...r];o[a]=t,z.set(n,o)}async function $a(e,t){let n=Number(e);if(!B.has(n)){B.add(n),$t.add(Number(t)),Qt.delete(Number(t)),V.delete(n),$();try{let r=await fetch(`/api/autoprep/roles/${encodeURIComponent(e)}/application-answers/${encodeURIComponent(t)}/regenerate`,{method:`POST`}),i=await r.json(),[a]=Ka(i);if(a&&Qa(n,a),!r.ok)throw Error(i?.error||a?.error||`Could not regenerate the answer.`)}catch(e){V.set(n,e instanceof Error?e.message:`Could not regenerate the answer.`)}finally{$t.delete(Number(t)),B.delete(n),Number(F)===n&&$()}}}async function eo(e,t){let n=Number(e),r=Number(t);if(!Qt.has(r)){Qt.add(r),$();return}if(!B.has(n)){B.add(n),en.add(r),Qt.delete(r),V.delete(n),$();try{let i=await fetch(`/api/autoprep/roles/${encodeURIComponent(e)}/application-answers/${encodeURIComponent(t)}`,{method:`DELETE`}),a=await i.json();if(!i.ok)throw Error(a?.error||`Could not delete the question.`);let o=z.get(n)??[];z.set(n,o.filter(e=>Number(e?.id)!==r))}catch(e){V.set(n,e instanceof Error?e.message:`Could not delete the question.`)}finally{en.delete(r),B.delete(n),Number(F)===n&&$()}}}async function to(e,t){let n=`${e.role_id}:${t}`,r=Ua(e,t);if(!(tn.get(n)===r||rn.has(n))){Z(n),rn.add(n),nn.delete(n),$();try{let i=await Bn(`/api/autoprep/roles/${encodeURIComponent(e.role_id)}/documents/${t}.pdf?v=${encodeURIComponent(e.updated_at||``)}`),a=P.find(t=>Number(t.role_id)===Number(e.role_id));if(!R.has(n)||!a||Ua(a,t)!==r){URL.revokeObjectURL(i),R.delete(n);return}H.set(n,i),tn.set(n,r)}catch(e){nn.set(n,e instanceof Error?e.message:`PDF preview unavailable`)}finally{rn.delete(n),Number(F)===Number(e.role_id)&&$()}}}function no(e,t,n){let r=t===`cover-letter`?`cover_letter`:`resume`,i=e[`${r}_status`],a=e[`${r}_artifact_path`],o=a?.split(`/`).pop()??`Not available`,s=e[`${r}_error`],c=e[`${r}_instruction`]||``,l=`${e.role_id}:${t}`,u=qt.get(l)??c,ee=t===`cover-letter`?`Optional comments for the next version`:`Comments for the next version`,te=t===`cover-letter`?`Optionally describe specific, truthful changes...`:`Describe specific, truthful changes...`,ne=[`failed`,`interrupted`].includes(i),d=e.worker_state!==`idle`||[`queued`,`generating`,`generating_tweaks`,`regenerating`].includes(i),re=!d&&(i===`ready`||ne)&&(ne||t===`cover-letter`||String(u).trim()),f=R.has(l),p=`/api/autoprep/roles/${encodeURIComponent(e.role_id)}/documents/${t}.pdf?v=${encodeURIComponent(e.updated_at||``)}`,m=H.get(l),ie=nn.get(l),ae=rn.has(l),oe=a?`<a class="prep-cover-pdf-link" data-autoprep-view="${t}" href="${G(p)}" target="_blank" rel="noreferrer" aria-label="View ${G(n.toLowerCase())} PDF in browser">View PDF</a>`:``;return`
    <section class="prepped-document${f?` has-open-preview`:``} status-${G(i)}">
      <div class="prepped-document-heading"><h4>${G(n)}</h4><span>${G(Ha(i))}</span></div>
      <p class="prepped-filename">${G(o)}</p>
      ${s?`<p class="prepped-error">${G(s)}</p>`:``}
      <div class="prepped-document-actions">
        <button type="button" data-autoprep-preview="${t}" ${a?``:`disabled`}>${f?`Hide preview`:`Preview PDF`}</button>
        ${oe}
      </div>
      <div class="prepped-pdf-preview" data-autoprep-preview-panel="${t}" ${f&&a?``:`hidden`}>
        ${f&&m?`<iframe title="${G(n)} PDF preview" src="${G(m)}"></iframe>`:``}
        ${f&&ae?`<p>Loading PDF preview...</p>`:``}
        ${f&&ie?`<p class="prepped-error">${q(ie)}</p>`:``}
      </div>
      <label class="prepped-comments-label" for="prepped-comments-${G(l)}">${ee}</label>
      <textarea id="prepped-comments-${G(l)}" data-autoprep-comments="${t}" rows="4" placeholder="${te}" ${d?`disabled`:``}>${q(u)}</textarea>
      <button class="prepped-regenerate" type="button" data-autoprep-regenerate="${t}" ${re?``:`disabled`}>${d?`Regenerating...`:`Regenerate ${G(n)}`}</button>
    </section>`}async function ro(e,t,n){if(n.disabled)return;let r=`${e.role_id}:${t}`,i=e[`${t===`cover-letter`?`cover_letter`:`resume`}_status`],a=[`failed`,`interrupted`].includes(i),o=v.querySelector(`[data-autoprep-comments="${t}"]`),s=String(o?.value||qt.get(r)||``).trim();if(!s&&t!==`cover-letter`&&!a){o?.focus();return}n.disabled=!0,n.textContent=`Queuing regeneration...`;try{let n=await fetch(`/api/autoprep/roles/${encodeURIComponent(e.role_id)}/${a?`retry`:`regenerate`}/${t}`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(a?{idempotency_key:Oa(`retry-${t}`)}:{comments:s,idempotency_key:Oa(`regenerate-${t}`)})}),i=await n.json();if(!n.ok)throw Error(i.error||`Regeneration request failed`);qt.delete(r),Z(r,{close:!0});let o=P.findIndex(t=>Number(t.role_id)===Number(e.role_id));o>=0&&(P[o]=i.job),Q()}catch(e){window.alert(e instanceof Error?e.message:`Regeneration request failed`),await Pa()}}async function io(){if(!Wt){Wt=!0,L=null,I=`Queuing eligible cover letters...`,Q();try{let e=await fetch(`/api/autoprep/cover-letters/regenerate`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({idempotency_key:Oa(`regenerate-all-cover-letters`)})}),t=await e.json();if(!e.ok)throw Error(t.error||`Bulk regeneration request failed`);let n=Number(t.queued_count||0),r=Array.isArray(t.skipped)?t.skipped:[];L={roleIds:(t.jobs||[]).map(e=>Number(e.role_id)),jobs:t.jobs||[],skipped:r},!n&&!r.length&&(L=null,I=`No prepped roles are available to regenerate.`),(t.jobs||[]).forEach(e=>{let t=P.findIndex(t=>Number(t.role_id)===Number(e.role_id));t>=0&&(P[t]=e),Z(`${e.role_id}:cover-letter`,{close:!0})}),await Pa(),Fa()}catch(e){L=null,I=e instanceof Error?e.message:`Bulk regeneration request failed`}finally{Wt=!1,Q()}}}async function ao(e,t){let n=Number(e);if(Kt.has(n))return;Kt.add(n),t.disabled=!0,t.setAttribute(`aria-busy`,`true`),t.textContent=`Moving to Disinterested...`;let r=P.findIndex(e=>Number(e.role_id)===n);try{await Da(e,`disinterested`),Z(`${e}:resume`,{close:!0}),Z(`${e}:cover-letter`,{close:!0}),r>=0&&P.splice(r,1),F=P[Math.min(r,P.length-1)]?.role_id??null,I=`Role moved to Disinterested.`,Q(),Br()}catch(e){I=e instanceof Error?e.message:`Could not move this role to Disinterested.`,await Pa()}finally{Kt.delete(n),P.some(e=>Number(e.role_id)===n)&&Q()}}async function oo(e,t){if(t.disabled)return;t.disabled=!0,t.textContent=`Moving to Applied...`;let n=P.findIndex(t=>Number(t.role_id)===Number(e));try{if(!(await fetch(`/api/autoprep/roles/${encodeURIComponent(e)}/applied`,{method:`POST`})).ok)throw Error(`Applied update failed`);Z(`${e}:resume`,{close:!0}),Z(`${e}:cover-letter`,{close:!0}),P.splice(n,1),F=P[Math.min(n,P.length-1)]?.role_id??null,Q(),Br()}catch{await Pa()}}ve.addEventListener(`click`,Pi),Te.addEventListener(`click`,Li),xe.addEventListener(`click`,Ii),ke.addEventListener(`click`,()=>Ma()),je.addEventListener(`click`,Na),Ne.addEventListener(`click`,io),Fe.addEventListener(`click`,e=>{let t=e.target.closest(`[data-prepped-role]`);t&&(F=Number(t.dataset.preppedRole),Q())}),v.addEventListener(`input`,e=>{let t=e.target.closest(`[data-application-question-draft]`);if(t){let e=Number(F);Yt.set(e,t.value);let n=v.querySelector(`[data-application-question-submit]`);n&&(n.disabled=!t.value.trim()||B.has(e));return}let n=e.target.closest(`[data-autoprep-comments]`);if(!n)return;let r=`${F}:${n.dataset.autoprepComments}`;qt.set(r,n.value);let i=v.querySelector(`[data-autoprep-regenerate="${n.dataset.autoprepComments}"]`),a=P.find(e=>Number(e.role_id)===Number(F)),o=n.dataset.autoprepComments===`cover-letter`?`cover_letter`:`resume`,s=a?.[`${o}_status`],c=[`failed`,`interrupted`].includes(s);i&&(i.disabled=a?.worker_state!==`idle`||![`ready`,`failed`,`interrupted`].includes(s)||!c&&n.dataset.autoprepComments!==`cover-letter`&&!n.value.trim())}),v.addEventListener(`toggle`,e=>{let t=e.target.closest(`[data-prepped-detail-section]`);if(!t)return;let n=`${F}:${t.dataset.preppedDetailSection}`;t.open?Jt.add(n):Jt.delete(n)},!0),v.addEventListener(`click`,async e=>{let t=P.find(e=>Number(e.role_id)===Number(F));if(!t)return;if(e.target.closest(`[data-application-question-submit]`)){Za(t.role_id);return}let n=e.target.closest(`[data-application-answer-regenerate]`);if(n){$a(t.role_id,n.dataset.applicationAnswerRegenerate);return}let r=e.target.closest(`[data-application-answer-delete]`);if(r){eo(t.role_id,r.dataset.applicationAnswerDelete);return}let i=e.target.closest(`[data-application-answer-copy]`);if(i){let e=(z.get(Number(t.role_id))??[])[Number(i.dataset.applicationAnswerCopy)]?.answer;if(!e)return;try{await Xa(String(e)),i.textContent=`Copied`}catch{i.textContent=`Copy unavailable`}return}let a=e.target.closest(`[data-prepped-nav]`);if(a){let e=P.indexOf(t),n=a.dataset.preppedNav===`next`?1:-1;F=P[e+n]?.role_id??t.role_id,Q();return}let o=e.target.closest(`[data-autoprep-preview]`);if(o){let e=o.dataset.autoprepPreview,n=`${t.role_id}:${e}`;R.has(n)?(R.delete(n),$()):(R.add(n),$(),to(t,e));return}let s=e.target.closest(`[data-autoprep-regenerate]`);if(s){ro(t,s.dataset.autoprepRegenerate,s);return}let c=e.target.closest(`[data-autoprep-open-folder]`);if(c&&!c.disabled){c.disabled=!0,c.textContent=`Opening...`;try{if(!(await fetch(`/api/autoprep/roles/${encodeURIComponent(t.role_id)}/open-folder`,{method:`POST`})).ok)throw Error(`Could not open the documents folder.`);c.textContent=`Opened in Finder`,window.setTimeout(()=>{c.isConnected&&(c.textContent=`Open Documents Folder`,c.disabled=!1)},1500)}catch(e){c.textContent=e instanceof Error?e.message:`Could not open folder`,c.disabled=!1}return}let l=e.target.closest(`[data-autoprep-disinterested]`);if(l){ao(t.role_id,l);return}let u=e.target.closest(`[data-autoprep-applied]`);u&&oo(t.role_id,u)}),Oe.addEventListener(`click`,zi),h.addEventListener(`click`,e=>{let t=e.target.closest(`[data-review-action]`);t&&ta(t.dataset.reviewAction)}),g.addEventListener(`click`,e=>{e.target.closest(`.prep-summary-action`)&&e.stopPropagation()}),g.addEventListener(`input`,e=>{let t=e.target.closest(`[data-prep-resume-tweaks]`);if(t){let e=Number(t.dataset.prepResumeTweaks);Number.isFinite(e)&&zt.set(e,t.value);return}let n=e.target.closest(`[data-prep-resume-latex]`);if(n){let e=Number(n.dataset.prepResumeLatex);if(!Number.isFinite(e))return;va(e,n.value);return}let r=e.target.closest(`[data-prep-cover-letter-latex]`);if(!r)return;let i=Number(r.dataset.prepCoverLetterLatex);if(!Number.isFinite(i))return;let a=r.closest(`.prep-cover-letter`)?.querySelector(`[data-prep-cover-letter-tweaks="${i}"]`)?.value??``;Ca(i,r.value,a)}),g.addEventListener(`scroll`,e=>{e.target.closest(`[data-prep-resume-latex], [data-prep-cover-letter-latex]`)},!0),g.addEventListener(`focusout`,e=>{let t=e.target.closest(`[data-prep-resume-latex]`);if(t){let e=Number(t.dataset.prepResumeLatex);if(!Number.isFinite(e))return;va(e,t.value,0);return}let n=e.target.closest(`[data-prep-cover-letter-latex]`);if(!n)return;let r=Number(n.dataset.prepCoverLetterLatex);if(!Number.isFinite(r))return;let i=n.closest(`.prep-cover-letter`)?.querySelector(`[data-prep-cover-letter-tweaks="${r}"]`)?.value??``;Ca(r,n.value,i,0)}),g.addEventListener(`submit`,async e=>{let t=e.target.closest(`[data-prep-role-chat-form]`);if(!t||!A[0])return;e.preventDefault();let n=Number(t.dataset.prepRoleChatForm);if(!Number.isFinite(n))return;let r=t.querySelector(`[data-prep-role-chat-input="${n}"]`),i=r?.value?.trim()??``;if(!i){r?.focus();return}let a=[...Bt.get(n)??[],{role:`user`,content:i}];Bt.set(n,a),_.querySelector(`.prep-role-chat`)?.replaceWith(X(aa(A[0],{messages:a,loading:!0})));try{let e=await _a(n,a),t=[...a,e.message];Bt.set(n,t),_.querySelector(`.prep-role-chat`)?.replaceWith(X(aa(A[0],{messages:t})))}catch{let e=[...a,{role:`assistant`,content:`could not answer right now.`}];Bt.set(n,e),_.querySelector(`.prep-role-chat`)?.replaceWith(X(aa(A[0],{messages:e})))}}),g.addEventListener(`click`,async e=>{let t=e.target.closest(`[data-prep-section-target]`);if(t){let e=t.dataset.prepSectionTarget,n=e?document.getElementById(e):null;if(n instanceof HTMLDetailsElement){n.open=!0,n.scrollIntoView({behavior:`smooth`,block:`start`});let e=n.querySelector(`summary`);e?.setAttribute(`tabindex`,`-1`),e?.focus({preventScroll:!0})}return}if(e.target.closest(`[data-prep-analysis]`)&&A[0]){let e=A[0].id;_.querySelector(`.prep-analysis`)?.replaceWith(X(ca(A[0],{loading:!0})));try{let t=await ua(e,{force:!0});if(A[0]?.id!==e)return;_.querySelector(`.prep-analysis`)?.replaceWith(X(ca(A[0],{analysis:t})))}catch{_.querySelector(`.prep-analysis`)?.replaceWith(X(ca(A[0],{error:!0})))}return}if(e.target.closest(`[data-prep-resume-regenerate]`)&&A[0]){let e=A[0].id,t=_.querySelector(`.prep-resume`),n=t?.querySelector(`[data-prep-resume-tweaks="${e}"]`)?.value??``,r=t?.querySelector(`[data-prep-resume-latex="${e}"]`)?.value??``;if(!n.trim()){t?.querySelector(`[data-prep-resume-tweaks="${e}"]`)?.focus();return}zt.set(e,n),t?.replaceWith(X(ra(A[0],{loading:!0})));try{let t=await ga(e,n,r);M.set(e,t.resume),_.querySelector(`.prep-resume`)?.replaceWith(X(ra(A[0],{resume:t.resume}))),Sn()}catch{_.querySelector(`.prep-resume`)?.replaceWith(X(ra(A[0],{resume:M.get(e),tweaks:n}))),Sn()}return}if(e.target.closest(`[data-prep-cover-letter]`)&&A[0]){let e=A[0].id,t=_.querySelector(`.prep-cover-letter`),n=t?.querySelector(`[data-prep-cover-letter-tweaks="${e}"]`)?.value??``,r=n.trim()?t?.querySelector(`[data-prep-cover-letter-latex="${e}"]`)?.value??``:``;t?.replaceWith(X(sa(A[0],{loading:!0})));try{let t=await xa(e,n,r);N.set(e,t.cover_letter),_.querySelector(`.prep-cover-letter`)?.replaceWith(X(sa(A[0],{coverLetter:t.cover_letter}))),Sn()}catch{_.querySelector(`.prep-cover-letter`)?.replaceWith(X(sa(A[0],{coverLetter:N.get(e),tweaks:n}))),Sn()}return}let n=e.target.closest(`[data-prep-action]`);if(n){da(n.dataset.prepAction);return}let r=e.target.closest(`[data-prep-feedback]`);if(!r||!A[0])return;let i=A[0].id,a=j.get(i),o=Array.isArray(a?.feedback_items)?a.feedback_items.length:0,s=Rt.get(i)??0;if(r.dataset.prepFeedback===`accept`||r.dataset.prepFeedback===`ignore`){let e=a?.feedback_items?.[s];if(!e)return;let t=_.querySelector(`[data-prep-feedback-comment]`)?.value??``,n=r.dataset.prepFeedback,o=n;r.disabled=!0,r.textContent=n===`accept`?`adding...`:`ignoring...`;try{if(n===`accept`){let n=await fa(i,s,e,t),r=document.querySelector(`.job[data-role-id="${CSS.escape(String(i))}"]`);n.role&&(A[0]=n.role,wi(n.role,r)),co(i,n.tweak_prompt??e.tweak_prompt??``),so(i,s,a)}else await pa(i,s,e,t),so(i,s,a)}catch{r.disabled=!1,r.textContent=o}return}let c=r.dataset.prepFeedback===`next`?1:-1;Rt.set(i,Math.max(0,Math.min(s+c,o-1))),_.querySelector(`.prep-analysis`)?.replaceWith(X(ca(A[0],{analysis:a})))});function so(e,t,n){let r=n.feedback_items.filter((e,n)=>n!==t),i=Math.min(t,Math.max(r.length-1,0)),a={...n,feedback_items:r,verdict:r.length===0?`ready_to_apply`:n.verdict};Rt.set(e,i),j.set(e,a),_.querySelector(`.prep-analysis`)?.replaceWith(X(ca(A[0],{analysis:a})))}function co(e,t){let n=String(t||``).trim();if(!n)return;let r=zt.get(e)?.trim()??``,i=r?`${r}\n\n${n}`:n;zt.set(e,i);let a=_.querySelector(`[data-prep-resume-tweaks="${e}"]`);a&&(a.value=i,a.focus())}document.addEventListener(`keydown`,e=>{e.key===`Escape`&&!ye.hidden&&Ii(),e.key===`Escape`&&!Be.hidden&&ir(),e.key===`Escape`&&!o.hidden&&vn(),e.key===`Escape`&&!h.hidden&&Li(),e.key===`Escape`&&!g.hidden&&zi(),e.key===`Escape`&&!Ae.hidden&&Na(),e.key===`Escape`&&!Je.hidden&&hr(),e.key===`Escape`&&!lt.hidden&&wr(),e.key===`Escape`&&!gt.hidden&&Nr(),e.key===`Escape`&&!St.hidden&&Xr()}),ze.addEventListener(`click`,rr),He.addEventListener(`click`,ir),Ve.addEventListener(`click`,ir);function lo(){return Array.from(document.querySelectorAll(`.pane-toggle`))}function uo(){return lo().some(e=>e.getAttribute(`aria-expanded`)===`true`)}function fo(){We.textContent=uo()?`collapse all`:`expand all`}function po(){document.querySelectorAll(`.pane-toggle`).forEach(e=>{e.setAttribute(`aria-expanded`,`true`),e.querySelector(`.chevron`).textContent=`v`,e.parentElement.querySelector(`.pane-body`).hidden=!1})}function mo(){document.querySelectorAll(`.job[open]`).forEach(e=>{e.open=!1}),document.querySelectorAll(`.pane-toggle`).forEach(e=>{e.setAttribute(`aria-expanded`,`false`),e.querySelector(`.chevron`).textContent=`>`,e.parentElement.querySelector(`.pane-body`).hidden=!0})}We.addEventListener(`click`,()=>{uo()?mo():po(),fo()}),Ge.addEventListener(`click`,()=>{Ft=!Ft,Ge.textContent=Ft?`show empty`:`hide empty`,T&&Un(T.statuses)}),qe.addEventListener(`click`,mr),Ze.addEventListener(`click`,_r),Ye.addEventListener(`click`,hr),ct.addEventListener(`click`,Cr),ut.addEventListener(`click`,wr),ht.addEventListener(`click`,Mr),_t.addEventListener(`click`,Nr),Ie.addEventListener(`click`,Yr),Ct.addEventListener(`click`,Xr),wt.addEventListener(`submit`,e=>{e.preventDefault(),$r(wt).catch(()=>{C.textContent=`could not add company.`})}),Tt.addEventListener(`submit`,e=>{e.preventDefault(),ii(Tt).catch(()=>{kt.textContent=`could not add role.`})}),w.addEventListener(`submit`,e=>{let t=e.target.closest(`[data-company-link-form]`);t&&(e.preventDefault(),ei(t).catch(()=>{C.textContent=`could not add link.`}))}),w.addEventListener(`input`,e=>{let t=e.target.closest(`[data-company-notes]`);t&&si(t.dataset.companyNotes)}),w.addEventListener(`change`,e=>{let t=e.target.closest(`[data-company-tier]`);if(!t)return;let n=t.closest(`.company-panel`);n&&li(n,t.value),window.clearTimeout(mn.get(t.dataset.companyTier)),ci(t.dataset.companyTier).catch(()=>{oi(`could not save company.`)})}),w.addEventListener(`click`,e=>{let t=e.target.closest(`[data-delete-company]`);if(t){let e=ai(t.dataset.deleteCompany),n=e?.name?K(e.name):`this company`;if(!window.confirm(`Deactivate ${n}? It will be hidden from company counts and skipped during scans.`))return;t.disabled=!0,ni(t.dataset.deleteCompany).catch(()=>{C.textContent=`could not deactivate company.`,t.disabled=!1});return}let n=e.target.closest(`[data-delete-career-page]`);if(!n)return;let r=n.closest(`.company-link-row`)?.querySelector(`.company-link-text`)?.textContent?.trim();window.confirm(`Delete ${r||`this career link`}?`)&&(n.disabled=!0,ti(n.dataset.deleteCareerPage).catch(()=>{C.textContent=`could not delete link.`,n.disabled=!1}))}),S.addEventListener(`change`,e=>{let t=e.target.closest(`input[type="checkbox"], select, input[data-setting-text], textarea[data-setting-textarea]`);t&&Fr(t)}),S.addEventListener(`click`,async e=>{let t=e.target.closest(`[data-application-runtime-test]`);if(!t||t.disabled)return;let n=t.dataset.applicationRuntimeTest,r=S.querySelector(`[data-application-runtime-test-status="${CSS.escape(n)}"]`);t.disabled=!0,t.textContent=`Testing…`,r&&(r.textContent=`Creating a bounded Callumployed session…`);try{let e=await fetch(`/api/application-generation/backends/${encodeURIComponent(n)}/test`,{method:`POST`}),t=await e.json();if(!e.ok||t?.ok!==!0)throw Error(t?.error||`Connection test failed.`);r&&(r.textContent=t.message||`Connection succeeded.`)}catch(e){r&&(r.textContent=e instanceof Error?e.message:`Connection test failed.`)}finally{t.disabled=!1,t.textContent=`Test connection`}}),S.addEventListener(`submit`,async e=>{e.preventDefault();let t=S.querySelector(`button[type="submit"]`),n=S.querySelectorAll(`input[type="checkbox"][name], select[name], input[data-setting-text][name], textarea[data-setting-textarea][name]`),r={};n.forEach(e=>{let t=e.name;t&&(r[t]=e.type===`checkbox`?e.checked:e.value)}),t.disabled=!0,t.textContent=`saving...`;try{x.textContent=`saving settings...`;let e=await fetch(`/api/config`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(r)});if(!e.ok)throw Error(`Config update failed`);J(await e.json(),`settings saved.`)}catch{x.textContent=`could not save settings.`,x.classList.remove(`is-empty`)}finally{t.disabled=!1,t.textContent=`save settings`}}),nt.addEventListener(`input`,()=>{at.disabled=!nt.value.trim()}),it.addEventListener(`click`,Lr),at.addEventListener(`click`,Rr),st.addEventListener(`click`,Ir),xt.addEventListener(`click`,Hr);function ho(){if(window.location.hash===`#prepped-roles`){Ma();return}Na({clearHash:!1})}window.addEventListener(`popstate`,ho),Br().finally(Vr),window.location.hash===`#prepped-roles`&&ho(),Rn(!0),gi({applyDefaultCollapsed:!0}).catch(()=>{kn(null,`could not load resume.`),jn([],`could not load cover letter examples.`),Ln()}),di().then(()=>{fi()}).catch(()=>{Le.textContent=`could not load scan status`});