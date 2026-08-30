import{t as e}from"./preload-helper-Czpn1I53.js";var{sankey:t,sankeyLinkHorizontal:n}=await e(async()=>{let{sankey:e,sankeyLinkHorizontal:t}=await import(`/assets/d3-sankey.js`);return{sankey:e,sankeyLinkHorizontal:t}},[]),r=document.querySelector(`#stats`),i=document.querySelector(`#status-list`),a=document.querySelector(`#search-toggle`),o=document.querySelector(`#search-dialog`),s=document.querySelector(`#search-backdrop`),c=document.querySelector(`#search-form`),l=document.querySelector(`#search-input`),u=document.querySelector(`#close-search`),d=document.querySelector(`#materials-panel`),ee=document.querySelector(`#materials-toggle`),te=document.querySelector(`#materials-body`),ne=document.querySelector(`#materials-summary`),re=document.querySelector(`#materials-required-warning`),f=document.querySelector(`#resume-meta`),p=document.querySelector(`#resume-upload`),m=document.querySelector(`#resume-upload-button`),ie=document.querySelector(`#resume-resource-meta`),ae=document.querySelector(`#resume-resource-upload`),oe=document.querySelector(`#resume-resource-upload-button`),se=document.querySelector(`#resume-resource-list`),ce=document.querySelector(`#cover-letter-meta`),le=document.querySelector(`#cover-letter-upload`),ue=document.querySelector(`#cover-letter-upload-button`),de=document.querySelector(`#cover-letter-list`),fe=document.querySelector(`#experience-note-meta`),pe=document.querySelector(`#experience-note-upload`),me=document.querySelector(`#experience-note-upload-button`),he=document.querySelector(`#experience-note-list`);document.querySelector(`#material-index-button`);var ge=document.querySelector(`#material-index-warning`),_e=document.querySelector(`#material-index-status`),ve=document.querySelector(`#review-discovered`),ye=document.querySelector(`#role-information-view`),be=document.querySelector(`#role-information-card`),xe=document.querySelector(`#close-role-information`),h=document.querySelector(`#review-view`),Se=document.querySelector(`#review-heading`),Ce=document.querySelector(`#review-progress`),we=document.querySelector(`#review-card`),Te=document.querySelector(`#close-review`),g=document.querySelector(`#prep-view`),Ee=document.querySelector(`#prep-heading`),De=document.querySelector(`#prep-progress`),_=document.querySelector(`#prep-card`),Oe=document.querySelector(`#close-prep`),ke=document.querySelector(`#prepped-roles`),Ae=document.querySelector(`#prepped-view`),je=document.querySelector(`#close-prepped`),Me=document.querySelector(`#prepped-summary`),Ne=document.querySelector(`#regenerate-all-cover-letters`),Pe=document.querySelector(`#prepped-bulk-status`),Fe=document.querySelector(`#prepped-list`),v=document.querySelector(`#prepped-detail`),y=document.querySelector(`#scan-all-button`),Ie=document.querySelector(`#manage-companies-button`),b=document.querySelector(`#scan-status-bar`),x=document.querySelector(`#scan-status-text`),Le=document.querySelector(`#scan-last-time`),Re=document.querySelector(`#scan-failures-open`),ze=document.querySelector(`#scan-failures-dialog`),Be=document.querySelector(`#scan-failures-backdrop`),Ve=document.querySelector(`#scan-failures-close`),He=document.querySelector(`#scan-failures-list`),Ue=document.querySelector(`#toggle-all`),We=document.querySelector(`#collapse-empty`),Ge=document.querySelector(`#toolbar-summary`),Ke=document.querySelector(`#settings-open`),qe=document.querySelector(`#settings-view`),Je=document.querySelector(`#settings-close`),S=document.querySelector(`#settings-status`),Ye=document.querySelector(`#settings-form`),Xe=document.querySelector(`#settings-profile-options`),Ze=document.querySelector(`#settings-autoprep-options`),Qe=document.querySelector(`#settings-options`),$e=document.querySelector(`#central-store-summary`),et=document.querySelector(`#central-store-sync-summary`),tt=document.querySelector(`#central-api-url-input`),nt=document.querySelector(`#central-passkey-input`),rt=document.querySelector(`#central-save-button`),it=document.querySelector(`#central-sync-button`),at=document.querySelector(`#recommendation-history-summary`),ot=document.querySelector(`#clear-recommendation-history`),st=document.querySelector(`#metrics-open-button`),ct=document.querySelector(`#metrics-view`),lt=document.querySelector(`#metrics-close`),ut=document.querySelector(`#metrics-status`),dt=document.querySelector(`#metrics-overview`),ft=document.querySelector(`#metrics-sections`),pt=document.querySelector(`#metrics-scan-list`),mt=document.querySelector(`#sankey-open-button`),ht=document.querySelector(`#sankey-view`),gt=document.querySelector(`#sankey-close`),_t=document.querySelector(`#sankey-status`),vt=document.querySelector(`#sankey-canvas`),yt=document.querySelector(`#sankey-path-list`),bt=document.querySelector(`#app-update-button`),xt=document.querySelector(`#companies-view`),St=document.querySelector(`#companies-close`),C=document.querySelector(`#companies-status`),Ct=document.querySelector(`#company-create-form`),w=document.querySelector(`#companies-list`),wt=document.querySelector(`#role-add-form`),Tt=document.querySelector(`#role-url-input`),Et=document.querySelector(`#role-company-input`),Dt=document.querySelector(`#role-company-options`),Ot=document.querySelector(`#role-add-status`),kt=3,At=1200,jt=new Set([`applied`,`OA`,`interview`,`rejected`,`offer`]),Mt=new Map([[`discovered`,`#4f6472`],[`interested`,`#00897b`],[`disinterested`,`#626970`],[`applied`,`#2257ad`],[`oa`,`#b36b00`],[`interview`,`#5f2bd8`],[`rejected`,`#b93d2d`],[`offer`,`#137347`],[`closed`,`#53606b`],[`archived`,`#765b4a`]]),Nt=/^(?:about (?:the )?(?:role|team|job)|about this role|job description|job responsibilities|minimum qualifications|preferred qualifications|qualifications|requirements|responsibilities|what to expect|what (?:you'll|you’ll|you will) (?:bring|do)|what'?s in it for you|who you are|your objectives|your skills & talents):?$/i,Pt=!0,T=null,Ft=null,E=[],D=[],O=[],It=null,k=[],A=[],j=new Map,Lt=new Map,M=new Map,Rt=new Map,N=new Map,zt=new Map,Bt=new Map,Vt=new Map,P=[],F=null,Ht=null,Ut=!1,Wt=``,I=null,Gt=new Set,Kt=new Map,L=new Set,qt=new Set,R=new Map,Jt=new Map,Yt=new Map,Xt=new Set,Zt=!1,Qt=0,$t=null,en=!1,tn=null,nn=null,rn=null,an=null,z=null,on=[],sn=new Map;function B(){return T?.query?.trim()??``}function cn(){let e=!!B();a.classList.toggle(`search-active`,e),a.setAttribute(`aria-label`,e?`clear search`:`search jobs`)}function ln(){l.value=B(),o.hidden=!1,c.hidden=!1,l.focus(),l.select()}function un(){o.hidden=!0,c.hidden=!0,a.focus()}function dn(e){return e?new Intl.DateTimeFormat(void 0,{month:`short`,day:`numeric`,hour:`numeric`,minute:`2-digit`}).format(new Date(e)).toLocaleLowerCase():``}function V(e){return e?new Intl.DateTimeFormat(void 0,{month:`short`,day:`numeric`,hour:`numeric`,minute:`2-digit`}).format(new Date(e)).replace(`, `,` `).toLocaleLowerCase():``}function H(e){return String(e??``).replaceAll(`&`,`&amp;`).replaceAll(`<`,`&lt;`).replaceAll(`>`,`&gt;`).replaceAll(`"`,`&quot;`).replaceAll(`'`,`&#039;`)}function U(e){return String(e??``).toLocaleLowerCase()}function W(e){return H(U(e))}function fn(e){try{let t=new URL(String(e||``));return[`http:`,`https:`].includes(t.protocol)?t.href:``}catch{return``}}function pn(e){return e}function G(e=_){e.querySelectorAll(`[data-prep-resume-latex], [data-prep-cover-letter-latex]`).forEach(pn)}function mn(){return`
    <svg class="role-link-icon" viewBox="0 0 24 24" aria-hidden="true">
      <path d="M7 17 17 7"></path>
      <path d="M8 7h9v9"></path>
    </svg>
  `}function hn(){return`
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M12 5v14"></path>
      <path d="M5 12h14"></path>
    </svg>
  `}function gn(){return`
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M3 6h18"></path>
      <path d="M8 6V4h8v2"></path>
      <path d="m19 6-1 14H6L5 6"></path>
      <path d="M10 11v5"></path>
      <path d="M14 11v5"></path>
    </svg>
  `}function _n(e,t,n){let r=`<span class="role-title-text">${W(e)}</span>`;return t?`<a class="${n}" href="${H(t)}" target="_blank" rel="noreferrer">${r}${mn()}</a>`:`<span class="${n}">${r}</span>`}function vn(e){r.innerHTML=[[`companies`,e.companies_total],[`jobs`,e.jobs_total],[`applications`,e.applications_total]].map(([e,t])=>`<dl class="stat"><dt>${W(e)}</dt><dd>${t}</dd></dl>`).join(``)}function yn(e=T){if(!e){Ge.innerHTML=``;return}let t=t=>e.statuses.find(e=>e.key===t)?.count??0;Ge.innerHTML=[[`discovered`,t(`discovered`)],[`interested`,t(`interested`)],[`applied`,e.stats?.applications_total??0],[`total`,e.stats?.jobs_total??0]].map(([e,t])=>`
        <dl>
          <dt>${W(e)}</dt>
          <dd>${t}</dd>
        </dl>
      `).join(``)}function bn(e,t=``){if(Ft=e,m.textContent=e?`replace`:`upload`,t){f.textContent=t;return}if(!e){f.textContent=`no resume uploaded`;return}let n=V(e.updated_at),r=An(e.content_bytes);f.textContent=[U(e.filename),r,n].filter(Boolean).join(` | `)}function xn(e,t,n,{binary:r=!1}={}){let i=r?e.filename:e.id;return`
    <li class="material-source-item" title="${W(e.filename)}">
      <div class="material-source-copy">
        <span>${W(e.filename)}</span>
        <small>${H(n)}</small>
      </div>
      <div class="material-source-actions">
        <button type="button" class="material-source-view" data-material-view="${H(t)}" data-material-id="${H(i)}" data-material-binary="${r}">preview</button>
        <button type="button" class="material-source-remove" data-material-remove="${H(t)}" data-material-id="${H(i)}" data-material-name="${W(e.filename)}">remove</button>
      </div>
      <div class="material-source-preview" data-material-preview-body hidden></div>
    </li>`}function Sn(e,t=``){D=Array.isArray(e)?e:[],ue.textContent=D.length>0?`add`:`upload`,ce.textContent=t||(D.length===0?`no examples uploaded`:`${D.length} ${D.length===1?`example`:`examples`} stored`),de.innerHTML=D.map(e=>xn(e,`cover-letter-examples`,An(e.content_bytes))).join(``)}function Cn(e,t=``){O=Array.isArray(e)?e:[],me.textContent=O.length>0?`add`:`upload`,fe.textContent=t||(O.length===0?`no notes uploaded`:`${O.length} ${O.length===1?`note`:`notes`} stored`),he.innerHTML=O.map(e=>xn(e,`experience-notes`,An(e.content_bytes))).join(``)}function wn(e,t=``){It=e??null;let n=It?.status??`missing`,r=n!==`ready`;if(O.length,ge.hidden=!r,ge.textContent=t||It?.warning||``,t)_e.textContent=t;else if(n===`ready`){let e=Number(It?.document_count??0),t=Number(It?.skipped_source_count??0),n=V(It?.generated_at);_e.innerHTML=[`${e} indexed ${e===1?`page`:`pages`}`,t?`${t} unreadable upload skipped`:``,n].filter(Boolean).map(e=>`<button type="button" class="material-index-link" data-open-material-index title="Reveal the application material index in Finder">${W(e)}</button>`).join(`<span aria-hidden="true"> | </span>`)}else _e.textContent=n===`stale`?`index out of date`:`not indexed`}function Tn(e,t=``){E=Array.isArray(e)?e:[],oe.textContent=E.length>0?`add`:`upload`,ie.textContent=t||(E.length===0?`no resources uploaded`:`${E.length} ${E.length===1?`resource`:`resources`} stored`),se.innerHTML=E.map(e=>xn(e,`resume-resources`,An(e.bytes),{binary:!0})).join(``)}function En(e,t={}){Qt+=1,document.querySelectorAll(`[data-preview-blob-url]`).forEach(e=>{URL.revokeObjectURL(e.dataset.previewBlobUrl)}),bn(e?.master_resume??null),Tn(e?.resume_resources??[]),Sn(e?.cover_letter_examples??[]),Cn(e?.experience_notes??[]),wn(e?.material_index??null),On(e?.ui),(!Zt||t.applyDefaultCollapsed)&&(kn(!Dn(e?.ui)),Zt=!0)}function Dn(e=null){return typeof e?.has_missing_required_materials==`boolean`?e.has_missing_required_materials:!Ft||D.length===0||O.length===0}function On(e=null){let t=Ft?`resume ready`:`no resume`,n=E.length===0?`no resources`:`${E.length} ${E.length===1?`resource`:`resources`}`,r=D.length,i=r===0?`no cover letters`:`${r} cover ${r===1?`letter`:`letters`}`,a=O.length,o=a===0?`no notes`:`${a} experience ${a===1?`note`:`notes`}`;re.hidden=!Dn(e),ne.textContent=`${t} | ${n} | ${i} | ${o}`}function kn(e){d.classList.toggle(`collapsed`,e),ee.setAttribute(`aria-expanded`,String(!e)),ee.querySelector(`.materials-chevron`).textContent=e?`>`:`v`,te.hidden=e}function An(e){return Number.isFinite(e)?e<1024?`${e} b`:`${Math.round(e/1024)} kb`:``}async function jn(e){let t=await fetch(e,{cache:`no-store`});if(!t.ok)throw Error(`Preview unavailable`);let n=await t.arrayBuffer();if(new TextDecoder(`ascii`).decode(n.slice(0,5))!==`%PDF-`)throw Error(`The selected file is not a readable PDF.`);return URL.createObjectURL(new Blob([n],{type:`application/pdf`}))}async function Mn(e){let t=e.closest(`.material-source-item`)?.querySelector(`[data-material-preview-body]`);if(!t)return;if(t.dataset.loaded===`true`){t.hidden=!t.hidden,e.textContent=t.hidden?`preview`:`hide`;return}e.disabled=!0,e.textContent=`loading...`;let n=e.dataset.materialView,r=e.dataset.materialId,i=Qt,a=`/api/${encodeURIComponent(n)}/${encodeURIComponent(r)}`;try{if(e.dataset.materialBinary===`true`){let e=await jn(a);if(!t.isConnected||Qt!==i){URL.revokeObjectURL(e);return}t.dataset.previewBlobUrl=e,t.innerHTML=`<iframe title="${W(r)} preview"></iframe>`,t.querySelector(`iframe`).src=e}else{let e=await fetch(a);if(!e.ok)throw Error(`Preview unavailable`);let n=await e.json(),r=document.createElement(`pre`);r.textContent=n.content||`This source is empty.`,t.replaceChildren(r)}t.dataset.loaded=`true`,t.hidden=!1,e.textContent=`hide`}catch(n){t.textContent=n instanceof Error?n.message:`Preview unavailable`,t.hidden=!1,e.textContent=`preview`}finally{e.disabled=!1}}async function Nn(e){let t=e.dataset.materialRemove,n=e.dataset.materialId;if(e.dataset.confirmRemove!==`true`){e.dataset.confirmRemove=`true`,e.textContent=`confirm remove`,e.classList.add(`danger`),window.setTimeout(()=>{!e.isConnected||e.disabled||(delete e.dataset.confirmRemove,e.textContent=`remove`,e.classList.remove(`danger`))},6e3);return}e.disabled=!0,e.textContent=`removing...`;try{let e=await fetch(`/api/${encodeURIComponent(t)}/${encodeURIComponent(n)}`,{method:`DELETE`}),r=await e.json();if(!e.ok)throw Error(r.error||`Remove failed`);En(r)}catch(t){e.disabled=!1,delete e.dataset.confirmRemove,e.classList.remove(`danger`),e.textContent=`remove`,window.alert(t instanceof Error?t.message:`Remove failed`)}}function Pn(e){i.innerHTML=e.map(e=>{let t=e.jobs.map(t=>Fn(t,e.key)).join(``),n=Math.max(Number(e.count)-e.jobs.length,0),r=[`disinterested`,`rejected`,`closed`].includes(e.key)&&n>0?`<p class="empty-copy status-more-copy">... and ${n} more</p>`:``;return`
        <section class="status-pane ${e.count===0?`empty`:``} ${Pt?`hidden-empty`:``}" id="status-${H(e.key)}" data-bucket="${H(e.key)}">
          <button class="pane-toggle" type="button" aria-expanded="false">
            <span class="chevron">></span>
            <span class="pane-title">${W(e.label)}</span>
            <span class="count">${e.count}</span>
          </button>
          <div class="pane-body" hidden>
            ${t||r?`<div class="jobs">${t}${r}</div>`:`<p class="empty-copy">${e.key===`archived`&&e.count>0?`archived role details are hidden.`:`no jobs in this status.`}</p>`}
          </div>
        </section>
      `}).join(``)}function Fn(e,t){return`
    <details class="job" data-role-id="${H(e.id)}">
      <summary class="job-summary">
        <span class="job-chevron">></span>
        <span class="job-identity">
          <span class="job-company">[${W(e.company_name)}]</span>
          ${_n(e.title,e.role_url,`job-title`)}
          ${t===`interested`&&e.prep_started?Rn():``}
          ${t===`closed`&&e.updated_in_latest_scan?In():``}
          ${[`discovered`,`interested`].includes(t)&&e.missing_from_latest_scan?Ln():``}
        </span>
      </summary>
      <div class="job-detail">
        ${t===`discovered`?zn(e):``}
        ${t===`interested`?Bn(e):``}
        ${t===`disinterested`?Vn(e):``}
        ${t===`applied`?Hn(e):``}
        ${t===`OA`?Un(e):``}
        ${t===`interview`?Wn(e):``}
        ${t===`closed`?Gn(e):``}
        <dl>
          ${e.location?`<div>
                  <dt>location</dt>
                  <dd>${W(e.location)}</dd>
                </div>`:``}
          <div>
            <dt>updated</dt>
            <dd>${dn(e.updated_at)}</dd>
          </div>
        </dl>
      </div>
    </details>
  `}function In(){return`<span class="latest-scan-dot" title="updated in latest scan" aria-label="updated in latest scan"></span>`}function Ln(){return`<span class="missing-latest-scan-dot" title="not seen in latest scan" aria-label="not seen in latest scan"></span>`}function Rn(){return`<span class="prep-started-dot" title="application materials started" aria-label="application materials started"></span>`}function zn(e){return`
    <div class="job-actions job-actions-nowrap" aria-label="discovered role actions">
      <button class="job-action success" type="button" data-review-role-id="${e.id}">view</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="interested">interested</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="disinterested">disinterested</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="closed">closed</button>
    </div>
  `}function Bn(e){return`
    <div class="job-actions" aria-label="interested role actions">
      <button class="job-action success" type="button" data-prep-role-id="${e.id}">prep</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="applied">applied</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="disinterested">disinterested</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="closed">closed</button>
    </div>
  `}function Vn(e){return`
    <div class="job-actions" aria-label="disinterested role actions">
      <button class="job-action success" type="button" data-role-id="${e.id}" data-status="interested">interested</button>
    </div>
  `}function Hn(e){return`
    <div class="job-actions job-actions-nowrap" aria-label="applied role actions">
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="OA">oa</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="interview">interview</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="rejected">rejected</button>
    </div>
  `}function Un(e){return`
    <div class="job-actions job-actions-nowrap" aria-label="oa role actions">
      <button class="job-action" type="button" data-view-role-info="${e.id}">view information</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="interview">interview</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="disinterested">disinterested</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="rejected">rejected</button>
    </div>
  `}function Wn(e){return`
    <div class="job-actions" aria-label="interview role actions">
      <button class="job-action" type="button" data-view-role-info="${e.id}">view information</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="rejected">rejected</button>
      <button class="job-action success" type="button" data-role-id="${e.id}" data-status="offer">offer</button>
    </div>
  `}function Gn(e){return`
    <div class="job-actions" aria-label="closed role actions">
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="interested">interested</button>
    </div>
  `}function Kn(e){T=e,l.value=e.query,cn(),vn(e.stats),yn(e),Pn(e.statuses),Ba(),_i(e.statuses)}function qn(e){tn=e??null;let t=!!e?.scanning,n=t&&!!e?.cancel_requested,r=Number(e?.completed_companies??0),i=Number(e?.total_companies??0),a=Number(e?.failed_companies??0),o=typeof e?.error==`string`?e.error.trim():``,s=Array.isArray(e?.failures)?e.failures:[];y.disabled=n,y.textContent=t?n?`cancelling...`:`cancel scan`:`scan roles`,y.classList.toggle(`danger`,t&&!n),b.hidden=!t&&!o&&s.length===0,b.classList.toggle(`scanning`,t),b.classList.toggle(`scan-error`,!t&&!!o||s.length>0),x.textContent=n?`cancelling scan...`:t?`scanning roles${i>0?` ${r}/${i}`:``}${a>0?`, ${a} failed`:``}`:s.length>0?`${s.length} recent scan ${s.length===1?`failure`:`failures`}`:o?`last scan error: ${o}`:`scan idle`,Re&&He&&(Re.hidden=s.length===0,He.innerHTML=s.slice(0,5).map(e=>{let t=e?.company_name||`unknown company`,n=e?.error||`scan failed`;return`
          <p>
            <span>${W(t)}</span>
            <span>${H(n)}</span>
          </p>
        `}).join(``),s.length===0&&Yn());let c=e?.last_scan_at;Le.textContent=c?`last scan: ${V(c)}`:`last scan: never`,en&&!t&&J(B()).catch(()=>{}),en=t}function Jn(){Re.hidden||(ze.hidden=!1,Ve.focus())}function Yn(){ze.hidden=!0}function K(e,t=``){nn=e;let n=Array.isArray(e?.settings)?e.settings:[],r=n.filter(e=>e.key?.startsWith(`applicant_`)),i=n.filter(e=>e.key?.startsWith(`autoprep_`)),a=n.filter(e=>!e.key?.startsWith(`applicant_`)&&!e.key?.startsWith(`autoprep_`)),o=e?.central??{};S.textContent=t,S.classList.toggle(`is-empty`,!t);let s=Number(e?.recommendation_history_count??0);at.textContent=s>0?`${s} saved ${s===1?`feedback decision`:`feedback decisions`}`:`no saved resume feedback decisions`,ot.disabled=s===0,Xn(o),Xe.innerHTML=r.map(e=>Zn(e)).join(``),Ze.innerHTML=i.map(e=>Zn(e)).join(``),Qe.innerHTML=a.map(e=>Zn(e)).join(``),q(!1)}function Xn(e){let t=e?.api_url??``;tt.value=t,nt.value=``;let n=e?.passkey_configured?`passkey saved`:`no passkey saved`;$e.textContent=t?`${U(t)} | ${n}`:`no api url | ${n}`,et.textContent=`${Number(e?.companies_linked??0)} linked | ${Number(e?.companies_unlinked??0)} unlinked | ${Number(e?.companies_needs_review??0)} review | ${Number(e?.companies_failed??0)} failed`,it.disabled=!t}function Zn(e){if(e.control===`textarea`&&e.editable!==!1)return $n(e);if(e.control===`text`&&e.editable!==!1)return Qn(e);if(e.control===`select`&&e.editable!==!1)return er(e);if(e.control!==`toggle`||e.editable===!1)return tr(e);let t=e.value?`checked`:``,n=e.default?`on by default`:`off by default`;return`
    <label class="setting-option">
      <span class="setting-copy">
        <span class="setting-label">${W(e.label)}</span>
        <span class="setting-description">${W(e.description)}</span>
        <span class="setting-default">${W(n)}</span>
      </span>
      <span class="setting-switch">
        <input type="checkbox" name="${H(e.key)}" ${t} />
        <span aria-hidden="true"></span>
      </span>
    </label>
  `}function Qn(e){let t=e.default?`default: ${U(e.default)}`:`optional`,n=e.input_type??`text`,r=e.autocomplete??`name`;return`
    <label class="setting-option">
      <span class="setting-copy">
        <span class="setting-label">${W(e.label)}</span>
        <span class="setting-description">${W(e.description)}</span>
        <span class="setting-default">${W(t)}</span>
      </span>
      <input
        class="setting-text-input"
        data-setting-text
        name="${H(e.key)}"
        type="${H(n)}"
        value="${H(e.value??``)}"
        autocomplete="${H(r)}"
      />
    </label>
  `}function $n(e){return`
    <label class="setting-option setting-option-prompt">
      <span class="setting-copy">
        <span class="setting-label">${W(e.label)}</span>
        <span class="setting-description">${W(e.description)}</span>
      </span>
      <textarea
        class="setting-prompt-input"
        data-setting-textarea
        name="${H(e.key)}"
        rows="7"
        maxlength="8000"
      >${W(e.value??``)}</textarea>
    </label>
  `}function er(e){let t=Array.isArray(e.options)?e.options:[],n=`default: ${U(e.default)}`;return`
    <label class="setting-option">
      <span class="setting-copy">
        <span class="setting-label">${W(e.label)}</span>
        <span class="setting-description">${W(e.description)}</span>
        <span class="setting-default">${W(n)}</span>
      </span>
      <select class="setting-select" name="${H(e.key)}">
        ${t.map(t=>{let n=t.value===e.value?`selected`:``;return`<option value="${H(t.value)}" ${n}>${W(t.label)}</option>`}).join(``)}
      </select>
    </label>
  `}function tr(e){let t=e.default?`on by default`:`off by default`,n=e.value?`automatic`:`off`;return`
    <div class="setting-option setting-option-readonly">
      <span class="setting-copy">
        <span class="setting-label">${W(e.label)}</span>
        <span class="setting-description">${W(e.description)}</span>
        <span class="setting-default">${W(t)}</span>
      </span>
      <span class="setting-badge">${W(n)}</span>
    </div>
  `}function q(e){Ye.querySelectorAll(`input, select, textarea`).forEach(t=>{t.disabled=e}),rt.disabled=e,it.disabled=e||!tt.value.trim(),bt.disabled=e}async function nr(){qe.hidden=!1,document.body.classList.add(`settings-open`),Je.focus(),nn?K(nn):(S.textContent=`loading settings...`,S.classList.remove(`is-empty`),Qe.innerHTML=``);try{await ir()}catch{S.textContent=`could not load settings.`}}function rr(){qe.hidden=!0,document.body.classList.remove(`settings-open`),Ke.focus()}async function ir(){let e=await fetch(`/api/config`);if(!e.ok)throw Error(`Config request failed`);K(await e.json())}function ar(e){let t=e?.value;return t==null?`n/a`:e?.kind===`ratio`?Number(t).toLocaleString(void 0,{maximumFractionDigits:2,minimumFractionDigits:0}):typeof t==`number`?t.toLocaleString():U(t)}function or(e,t=`metric-card`){return`
    <article class="${t}">
      <span>${W(e?.label)}</span>
      <strong>${H(ar(e))}</strong>
    </article>
  `}function sr(e,t=``){rn=e,ut.textContent=t||(e?.updated_at?`updated ${V(e.updated_at)}`:``),ut.classList.toggle(`is-empty`,!ut.textContent);let n=Array.isArray(e?.overview)?e.overview:[],r=Array.isArray(e?.sections)?e.sections:[],i=Array.isArray(e?.recent_scans)?e.recent_scans:[];dt.innerHTML=n.map(e=>or(e)).join(``),ft.innerHTML=r.map(cr).join(``),pt.innerHTML=i.length?i.map(lr).join(``):`<p class="empty-copy">no scan runs recorded.</p>`}function cr(e){let t=Array.isArray(e?.metrics)?e.metrics:[];return`
    <section class="metrics-section">
      <div class="metrics-section-heading">
        <h3>${W(e?.title)}</h3>
      </div>
      <div class="metrics-section-grid">
        ${t.map(e=>or(e,`metric-card metric-card-compact`)).join(``)}
      </div>
    </section>
  `}function lr(e){let t=e?.scan_status??`unknown`,n=e?.started_at?V(e.started_at):`not started`,r=e?.finished_at?V(e.finished_at):`not finished`,i=e?.error?`<span>${W(e.error)}</span>`:``;return`
    <article class="metrics-scan-row">
      <div>
        <strong>${W(e?.company_name??`unknown company`)}</strong>
        <span>${W(n)} -> ${W(r)}</span>
        ${i}
      </div>
      <span class="metrics-status-pill">${W(t)}</span>
    </article>
  `}async function ur(){ct.hidden=!1,document.body.classList.add(`metrics-open`),lt.focus(),rn?sr(rn):(ut.textContent=`loading metrics...`,ut.classList.remove(`is-empty`),dt.innerHTML=``,ft.innerHTML=``,pt.innerHTML=``);try{await fr()}catch{ut.textContent=`could not load metrics.`}}function dr(){ct.hidden=!0,document.body.classList.remove(`metrics-open`),st.focus()}async function fr(){let e=await fetch(`/api/metrics`);if(!e.ok)throw Error(`Metrics request failed`);sr(await e.json())}function pr(e,t=``){an=e;let n=Number(e?.role_count??0),r=Array.isArray(e?.links)?e.links:[],i=Array.isArray(e?.paths)?e.paths:[];_t.textContent=t||(e?.updated_at?`${n.toLocaleString()} roles | updated ${V(e.updated_at)}`:``),_t.classList.toggle(`is-empty`,!_t.textContent),vt.innerHTML=r.length?mr(e):`<p class="empty-copy">no role transitions recorded yet.</p>`,yt.innerHTML=i.length?i.map(vr).join(``):`<p class="empty-copy">no role paths recorded yet.</p>`}function mr(e){let t=Array.isArray(e?.nodes)?e.nodes:[],n=Array.isArray(e?.links)?e.links:[],r=_r(t,n),i=r.nodes,a=r.links,o=(r.flowLinks??n).map(e=>{let t=i.get(e.source),n=i.get(e.target),r=a.get(e);if(!t||!n||!r)return``;let o=r.width,s=n.x<t.x,c=hr(e.target),l=r.priority?`0.42`:s?`0.28`:`0.34`,u=r.path??gr({isBacktrack:s,sourceX:t.x+t.width,sourceY:r.sourceY,targetX:n.x,targetY:r.targetY,width:o});return`
        <path class="${[`sankey-link`,s?`sankey-link-backtrack`:``,r.priority?`sankey-link-priority`:``].filter(Boolean).join(` `)}" d="${u}" fill="${r.path?`none`:c}" fill-opacity="${l}" stroke="${c}" style="stroke-width: ${r.path?o:1}px">
          <title>${W(t.label)} to ${W(n.label)}: ${Number(e.value??0).toLocaleString()}</title>
        </path>
      `}).join(``),s=Array.from(i.values()).map(e=>{let t=Number(e.history_count??e.current_count??0),n=Number(e.value??t),i=n>0?n.toLocaleString():`0`,a=e.x>r.width-180,o=a?e.x-8:e.x+e.width+8,s=Math.max(24,e.y-e.height/2-16),c=a?`end`:`start`,l=hr(e.id);return`
        <g class="sankey-node" transform="translate(${e.x}, ${e.y-e.height/2})">
          <rect width="${e.width}" height="${e.height}" rx="7" fill="${l}" stroke="${l}"></rect>
        </g>
        <g class="sankey-node-label" transform="translate(${o}, ${s})">
          <text text-anchor="${c}">${W(e.label)}</text>
          <text class="sankey-node-count" y="16" text-anchor="${c}">${W(i)} roles</text>
        </g>
      `}).join(``);return`
    <svg class="sankey-svg" viewBox="0 0 ${r.width} ${r.height}" role="img" aria-label="role state transition sankey diagram">
      <g>${o}</g>
      <g>${s}</g>
    </svg>
  `}function hr(e){return Mt.get(String(e).toLowerCase())??`#4f6472`}function gr({isBacktrack:e,sourceX:t,sourceY:n,targetX:r,targetY:i,width:a}){let o=a/2,s=n-o,c=n+o,l=i-o,u=i+o;if(e){let e=Math.max(80,Math.abs(t-r)*.42);return[`M ${t} ${s}`,`C ${t-e} ${s}, ${r+e} ${l}, ${r} ${l}`,`L ${r} ${u}`,`C ${r+e} ${u}, ${t-e} ${c}, ${t} ${c}`,`Z`].join(` `)}let d=Math.max(46,(r-t)*.48);return[`M ${t} ${s}`,`C ${t+d} ${s}, ${r-d} ${l}, ${r} ${l}`,`L ${r} ${u}`,`C ${r-d} ${u}, ${t+d} ${c}, ${t} ${c}`,`Z`].join(` `)}function _r(e,r){let i=new Map([[`discovered`,0],[`interested`,1],[`disinterested`,2],[`applied`,2],[`oa`,3],[`interview`,3],[`rejected`,4],[`closed`,4],[`archived`,4]]),a=new Map,o=new Map;r.forEach(e=>{a.set(e.target,(a.get(e.target)??0)+Number(e.value??0)),o.set(e.source,(o.get(e.source)??0)+Number(e.value??0))});let s=e.filter(e=>Number(e?.history_count??e?.current_count??0)>0||a.has(e.id)||o.has(e.id)),c=new Set(s.map(e=>e.id)),l=r.filter(e=>c.has(e.source)&&c.has(e.target)&&Number(e.value??0)>0),u=e=>i.get(String(e).toLowerCase())??0,d=l.filter(e=>u(e.target)>=u(e.source)),ee=l.filter(e=>u(e.target)<u(e.source)),te={nodes:s.map(e=>({...e,fixedValue:Math.max(0,Number(e?.history_count??e?.current_count??0))})),links:d.map(e=>({...e}))},ne=t().nodeId(e=>e.id).nodeWidth(26).nodePadding(44).nodeAlign((e,t)=>Math.min(t-1,u(e.id))).extent([[92,88],[1014,634]]).iterations(32)(te),re=new Map;ne.nodes.forEach(e=>{re.set(e.id,{...e,x:e.x0,y:e.y0+(e.y1-e.y0)/2,width:e.x1-e.x0,height:Math.max(1.5,e.y1-e.y0),value:Number(e.fixedValue??e.value??0)})});let f=new Map,p=[],m=n();ne.links.forEach(e=>{let t={source:e.source.id,target:e.target.id,value:e.value};p.push(t),f.set(t,{path:m(e),width:Math.max(1.5,e.width),sourceY:e.y0,targetY:e.y1,priority:Number(e.value??0)>=20})});let ie=Math.max(.6,...ne.links.map(e=>Number(e.width??0)/Math.max(1,Number(e.value??0))));return ee.forEach(e=>{let t=re.get(e.source),n=re.get(e.target);if(!t||!n)return;let r=Math.max(1.5,Number(e.value??0)*ie),i={...e};p.push(i),f.set(i,{width:r,sourceY:t.y+t.height/2-r/2,targetY:n.y+n.height/2-r/2,priority:!1})}),p.sort((e,t)=>Number(e.value??0)-Number(t.value??0)),{flowLinks:p,height:720,links:f,nodes:re,width:1120}}function vr(e){let t=Array.isArray(e?.path)?e.path:[];return`
    <article class="sankey-path-row">
      <div>
        <strong>${W(e?.company_name??`unknown company`)} / ${W(e?.title??`untitled role`)}</strong>
        <span>${t.map(e=>W(e)).join(` -> `)}</span>
      </div>
      <span class="metrics-status-pill">${Number(e?.loops_collapsed??0).toLocaleString()} loops</span>
    </article>
  `}async function yr(){qe.hidden=!0,document.body.classList.remove(`settings-open`),ht.hidden=!1,document.body.classList.add(`sankey-open`),gt.focus(),an?pr(an):(_t.textContent=`loading role flow...`,_t.classList.remove(`is-empty`),vt.innerHTML=``,yt.innerHTML=``);try{await xr()}catch{_t.textContent=`could not load role flow.`}}function br(){ht.hidden=!0,document.body.classList.remove(`sankey-open`),Ke.focus()}async function xr(){let e=await fetch(`/api/role-sankey`);if(!e.ok)throw Error(`Role sankey request failed`);pr(await e.json())}async function Sr(e){let t=e.name;if(!t)return;let n=e.type===`checkbox`?!e.checked:nn?.settings?.find(e=>e.key===t)?.value,r=e.type===`checkbox`?e.checked:e.value;q(!0),S.textContent=`saving settings...`,S.classList.remove(`is-empty`);try{let e=await fetch(`/api/config`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({[t]:r})});if(!e.ok)throw Error(`Config update failed`);K(await e.json(),`settings saved.`)}catch{e.type===`checkbox`?e.checked=n:n!==void 0&&(e.value=n),S.textContent=`could not save settings.`,q(!1)}}async function Cr(){ot.disabled=!0,S.textContent=`clearing recommendation history...`,S.classList.remove(`is-empty`);try{let e=await fetch(`/api/recommendation-history/clear`,{method:`POST`});if(!e.ok)throw Error(`Recommendation history clear failed`);let t=await e.json();K(t.config,`cleared ${t.deleted_count} saved decisions.`)}catch{S.textContent=`could not clear recommendation history.`,ot.disabled=!1}}async function wr(){let e=tt.value.trim();if(!e){S.textContent=`central api url is required.`,S.classList.remove(`is-empty`);return}let t={central_api_url:e},n=nt.value.trim();n&&(t.central_passkey=n),q(!0),S.textContent=`saving central settings...`,S.classList.remove(`is-empty`);try{let e=await fetch(`/api/config`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(t)});if(!e.ok)throw Error(`Central settings update failed`);K(await e.json(),`central settings saved.`)}catch{S.textContent=`could not save central settings.`,q(!1)}}async function Tr(){it.disabled=!0,S.textContent=`syncing remote company ids...`,S.classList.remove(`is-empty`);try{let e=await fetch(`/api/central/resolve-companies`,{method:`POST`});if(!e.ok)throw Error(`Central company sync failed`);let t=await e.json(),n=t.result??{},r=t.pulled_companies,i=r?` remote: ${Number(r.created??0)} created, ${Number(r.linked??0)} linked, ${Number(r.existing??0)} existing.`:``;K(t.config,`company sync: ${Number(n.linked??0)} matched, ${Number(n.created??0)} created, ${Number(n.needs_review??0)} review, ${Number(n.failed??0)} failed.${i}`),t.companies&&(z=t.companies,jr(t.companies.companies))}catch{S.textContent=`could not sync companies.`,it.disabled=!tt.value.trim()}}async function Er(){let e=await fetch(`/api/central/resolve-companies`,{method:`POST`});if(!e.ok)throw Error(`Central company sync failed`);let t=await e.json();t.companies&&(z=t.companies,jr(t.companies.companies))}async function Dr(){await J().catch(()=>{i.innerHTML=`<p class="empty-copy">could not load jobs.</p>`}),zr().catch(()=>{Ot.textContent=`could not load companies.`})}function Or(){window.setTimeout(()=>{Er().catch(()=>{})},1e4)}async function kr(){if(window.confirm(`Update callumployed and restart the tracker?`)){q(!0),bt.disabled=!0,S.textContent=`updating callumployed; tracker will restart shortly...`,S.classList.remove(`is-empty`);try{if(!(await fetch(`/api/app/update`,{method:`POST`})).ok)throw Error(`App update failed`);S.textContent=`update started. reconnect in a moment.`}catch{S.textContent=`could not start update.`,q(!1)}}}function Ar(e,t=``){z=e;let n=Array.isArray(e?.companies)?e.companies:[];if(jr(n),C.textContent=t||`${n.length} ${n.length===1?`company`:`companies`} stored`,C.classList.toggle(`is-empty`,n.length===0&&!t),n.length===0){w.innerHTML=`<p class="empty-copy">no companies yet.</p>`;return}w.innerHTML=n.map(e=>Mr(e)).join(``)}function jr(e){on=Array.isArray(e)?e:[],Dt.innerHTML=on.map(e=>`<option value="${H(e.name)}"></option>`).join(``)}function Mr(e){let t=Array.isArray(e.career_pages)?e.career_pages:[],n=V(e.updated_at),r=Nr(e.prestige_tier),i=Number(e.scan_count??0),a=Number(e.discovered_role_count??0),o=i>0&&a===0?`<span class="company-discovery-status">Discovered 0 potential roles</span>`:``;return`
    <details class="company-panel ${r}" data-company-id="${e.id}">
      <summary class="company-summary">
        <span class="company-chevron">></span>
        <span class="company-summary-main">
          <span class="company-name">${W(e.name)}</span>
          <span class="company-summary-meta">${t.length} ${t.length===1?`link`:`links`}${n?` | updated ${W(n)}`:``}</span>
          ${o}
        </span>
      </summary>
      <div class="company-body">
        <div class="company-info">
          <label class="company-notes-field">
            <span>notes</span>
            <textarea data-company-notes="${e.id}" rows="3">${H(e.notes??``)}</textarea>
          </label>
          <label>
            <span>tier</span>
            <select data-company-tier="${e.id}">
              ${Pr(e.prestige_tier)}
            </select>
          </label>
          <div>
            <span>browser wait</span>
            <strong>${Number(e.browser_extra_wait_ms??0)}ms</strong>
          </div>
        </div>
        <div class="company-links">
          ${t.length>0?t.map(e=>Fr(e)).join(``):`<p class="company-empty-links">no career links yet.</p>`}
        </div>
        <section class="company-link-panel" aria-label="add career link">
          <form class="company-link-form" data-company-link-form="${e.id}">
            <input name="label" type="text" placeholder="label" aria-label="career link label" />
            <input name="url" type="url" placeholder="https://..." aria-label="career link url" required />
            <button class="company-link-add" type="submit" aria-label="add career link" title="add career link">
              ${hn()}
            </button>
          </form>
        </section>
        <div class="company-danger-row">
          <button class="company-delete-button" type="button" data-delete-company="${e.id}">
            ${gn()}
            <span>deactivate company</span>
          </button>
        </div>
      </div>
    </details>
  `}function Nr(e){let t=String(e??``);return[`0`,`1`,`2`,`3`,`4`].includes(t)?`company-tier-${t}`:`company-tier-unset`}function Pr(e){let t=String(e??``);return[``,`0`,`1`,`2`,`3`,`4`].map(e=>{let n=e?`tier ${e}`:`not set`,r=e===t?` selected`:``;return`<option value="${H(e)}"${r}>${W(n)}</option>`}).join(``)}function Fr(e){let t=e.label?W(e.label):`career page`,n=H(e.url);return`
    <div class="company-link-row" data-career-page-id="${e.id}">
      <a class="company-link-url" href="${n}" target="_blank" rel="noreferrer">
        <span class="company-link-label">${t}</span>
        <span class="company-link-text">${H(e.url)}</span>
      </a>
      <button class="company-link-delete" type="button" data-delete-career-page="${e.id}" aria-label="delete ${t} link" title="delete link">
        ${gn()}
      </button>
    </div>
  `}async function Ir(){xt.hidden=!1,document.body.classList.add(`companies-open`),St.focus(),z?Ar(z):(C.textContent=`loading companies...`,C.classList.remove(`is-empty`),w.innerHTML=``);try{await Rr()}catch{C.textContent=`could not load companies.`}}function Lr(){xt.hidden=!0,document.body.classList.remove(`companies-open`),Ie.focus()}async function Rr(e=``){let t=await fetch(`/api/companies`);if(!t.ok)throw Error(`Companies request failed`);Ar(await t.json(),e)}async function zr(){let e=await fetch(`/api/companies`);if(!e.ok)throw Error(`Companies request failed`);jr((await e.json()).companies)}async function Br(e){let t=new FormData(e),n={name:String(t.get(`name`)??``),career_url:String(t.get(`career_url`)??``),notes:String(t.get(`notes`)??``)};C.textContent=`adding company...`;let r=await fetch(`/api/companies`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(n)});if(!r.ok)throw Error(`Company create failed`);e.reset(),Ar(await r.json(),`company added.`),J(B()).catch(()=>{})}async function Vr(e){let t=e.dataset.companyLinkForm;if(!t)return;let n=new FormData(e),r={label:String(n.get(`label`)??``),url:String(n.get(`url`)??``)};C.textContent=`adding link...`;let i=await fetch(`/api/companies/${encodeURIComponent(t)}/career-pages`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(r)});if(!i.ok)throw Error(`Career page create failed`);e.reset(),Ar(await i.json(),`link added.`)}async function Hr(e){C.textContent=`deleting link...`;let t=await fetch(`/api/company-career-pages/${encodeURIComponent(e)}`,{method:`DELETE`});if(!t.ok)throw Error(`Career page delete failed`);Ar(await t.json(),`link deleted.`)}async function Ur(e){C.textContent=`deactivating company...`;let t=await fetch(`/api/companies/${encodeURIComponent(e)}`,{method:`DELETE`});if(!t.ok)throw Error(`Company deactivate failed`);Ar(await t.json(),`company deactivated.`),J(B()).catch(()=>{})}function Wr(){let e=Et.value.trim().toLocaleLowerCase();return on.find(t=>t.name.toLocaleLowerCase()===e)}async function Gr(e){let t=Wr();if(!t?.id){Ot.textContent=`pick a saved company.`;return}let n=new FormData(e),r={company_id:t.id,role_url:String(n.get(`role_url`)??``)};Ot.textContent=`adding role...`;let i=await fetch(`/api/roles`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(r)});if(!i.ok)throw Error(`Role create failed`);let a=await i.json();a.tracker?Kn(a.tracker):await J(B()),Tt.value=``;let o=a.role?.title?U(a.role.title):`role`;Ot.textContent=a.scan_error?`${o} added; scan could not finish.`:`${o} added.`}function Kr(e){return(Array.isArray(z?.companies)?z.companies:[]).find(t=>String(t.id)===String(e))}function qr(e){C.textContent=e,C.classList.remove(`is-empty`)}function Jr(e){window.clearTimeout(sn.get(e)),sn.set(e,window.setTimeout(()=>{Yr(e).catch(()=>{qr(`could not save company.`)})},700))}async function Yr(e){let t=w.querySelector(`[data-company-id="${CSS.escape(String(e))}"]`);if(!t)return;let n=t.querySelector(`[data-company-notes="${CSS.escape(String(e))}"]`),r=t.querySelector(`[data-company-tier="${CSS.escape(String(e))}"]`),i=Kr(e),a={notes:n?.value??i?.notes??``,prestige_tier:r?.value??i?.prestige_tier??``};i&&(i.notes=a.notes,i.prestige_tier=a.prestige_tier),Xr(t,a.prestige_tier),qr(`saving company...`);let o=await fetch(`/api/companies/${encodeURIComponent(e)}`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(a)});if(!o.ok)throw Error(`Company update failed`);z=await o.json(),qr(`company saved.`),Zr(e)}function Xr(e,t){e.classList.remove(`company-tier-unset`,`company-tier-0`,`company-tier-1`,`company-tier-2`,`company-tier-3`,`company-tier-4`),e.classList.add(Nr(t))}function Zr(e){let t=w.querySelector(`[data-company-id="${CSS.escape(String(e))}"]`),n=Kr(e);if(!t||!n)return;let r=Array.isArray(n.career_pages)?n.career_pages:[],i=V(n.updated_at),a=t.querySelector(`.company-summary-meta`);a&&(a.textContent=`${r.length} ${r.length===1?`link`:`links`}${i?` | updated ${i}`:``}`)}async function Qr(){let e=await fetch(`/api/scan/status`);if(e.status===404){y.disabled=!0,b.hidden=!0,b.classList.add(`scan-error`),x.textContent=`restart server to enable scanning`;return}if(!e.ok)throw Error(`Scan status request failed`);qn(await e.json())}function $r(){$t===null&&($t=window.setInterval(()=>{Qr().catch(()=>{})},3e3))}async function ei(){y.disabled=!0,y.textContent=`starting...`;try{let e=await fetch(`/api/scan/all`,{method:`POST`});if(e.status===404){y.disabled=!0,y.textContent=`scan roles`,b.hidden=!0,b.classList.add(`scan-error`),x.textContent=`restart server to enable scanning`;return}if(!e.ok&&e.status!==409)throw Error(`Scan start failed`);qn(await e.json()),$r()}catch{y.disabled=!1,y.textContent=`scan roles`,b.hidden=!0,b.classList.add(`scan-error`),x.textContent=`could not start scan`}}async function ti(){y.disabled=!0,y.textContent=`cancelling...`;try{let e=await fetch(`/api/scan/cancel`,{method:`POST`});if(e.status===404){y.disabled=!0,y.textContent=`scan roles`,b.hidden=!0,b.classList.add(`scan-error`),x.textContent=`restart server to enable scanning`;return}if(!e.ok&&e.status!==409)throw Error(`Scan cancel failed`);qn(await e.json()),$r()}catch{y.disabled=!1,y.textContent=`cancel scan`,b.hidden=!1,b.classList.add(`scan-error`),x.textContent=`could not cancel scan`}}async function J(e=``){i.innerHTML=`<p class="empty-copy">loading jobs...</p>`;let t=new URLSearchParams;e&&t.set(`q`,e);let n=await fetch(`/api/tracker?${t.toString()}`);if(!n.ok)throw Error(`Tracker request failed`);Kn(await n.json())}async function ni(e={}){let t=await fetch(`/api/application-materials`);if(!t.ok)throw Error(`Application materials request failed`);En(await t.json(),e)}async function ri(e){if(e){if(!e.name.toLowerCase().endsWith(`.tex`)){bn(Ft,`resume must be a .tex file.`);return}m.disabled=!0,bn(Ft,`uploading...`);try{let t=await e.text();if(!(await fetch(`/api/master-resume`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({filename:e.name,content:t})})).ok)throw Error(`Master resume upload failed`);await ni()}catch{bn(Ft,`could not save resume.`),On()}finally{p.value=``,m.disabled=!1}}}async function ii(e){let t=Array.from(e??[]);if(t.length!==0){oe.disabled=!0,Tn(E,`uploading ${t.length} ${t.length===1?`resource`:`resources`}...`);try{for(let e of t)if(!(await fetch(`/api/resume-resources`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({filename:e.name,content_base64:await si(e)})})).ok)throw Error(`Resume resource upload failed`);await ni()}catch{Tn(E,`could not save every resource.`),On()}finally{ae.value=``,oe.disabled=!1}}}async function ai(e){let t=Array.from(e??[]);if(t.length!==0){ue.disabled=!0,Sn(D,`uploading ${t.length} ${t.length===1?`example`:`examples`}...`);try{for(let e of t){let t={filename:e.name};if([`.pdf`,`.docx`].some(t=>e.name.toLowerCase().endsWith(t))?t.content_base64=await si(e):t.content=await e.text(),!(await fetch(`/api/cover-letter-examples`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(t)})).ok)throw Error(`Cover letter example upload failed`)}await ni()}catch{Sn(D,`could not save every example.`),On()}finally{le.value=``,ue.disabled=!1}}}async function oi(e){let t=Array.from(e??[]);if(t.length!==0){me.disabled=!0,Cn(O,`uploading ${t.length} ${t.length===1?`note`:`notes`}...`);try{for(let e of t){let t=e.name.toLowerCase(),n={filename:e.name};if(t.endsWith(`.pdf`)||t.endsWith(`.docx`)?n.content_base64=await si(e):n.content=await e.text(),!(await fetch(`/api/experience-notes`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(n)})).ok)throw Error(`Experience note upload failed`)}j.clear(),await ni()}catch{Cn(O,`could not save every note.`),On()}finally{pe.value=``,me.disabled=!1}}}function si(e){return new Promise((t,n)=>{let r=new FileReader;r.addEventListener(`load`,()=>{let e=String(r.result??``);t(e.includes(`,`)?e.split(`,`,2)[1]:e)}),r.addEventListener(`error`,()=>n(r.error)),r.readAsDataURL(e)})}c.addEventListener(`submit`,e=>{e.preventDefault(),J(l.value.trim()),un()}),a.addEventListener(`click`,()=>{if(B()){J();return}ln()}),l.addEventListener(`keydown`,e=>{e.key===`Escape`&&(e.stopPropagation(),un())}),u.addEventListener(`click`,un),s.addEventListener(`click`,un),m.addEventListener(`click`,()=>{p.click()}),p.addEventListener(`change`,()=>{ri(p.files?.[0])}),oe.addEventListener(`click`,()=>{ae.click()}),ae.addEventListener(`change`,()=>{ii(ae.files)}),ue.addEventListener(`click`,()=>{le.click()}),le.addEventListener(`change`,()=>{ai(le.files)}),me.addEventListener(`click`,()=>{pe.click()}),pe.addEventListener(`change`,()=>{oi(pe.files)}),ee.addEventListener(`click`,()=>{kn(ee.getAttribute(`aria-expanded`)===`true`)});async function ci(e){e.disabled=!0;let t=e.textContent;e.textContent=`opening...`;try{if(!(await fetch(`/api/application-materials/index/open`,{method:`POST`})).ok)throw Error(`Could not open the application material index.`)}catch(e){ge.hidden=!1,ge.textContent=e instanceof Error?e.message:`Could not open the application material index.`}finally{e.disabled=!1,e.textContent=t}}te.addEventListener(`click`,e=>{let t=e.target.closest(`[data-open-material-index]`);if(t){ci(t);return}let n=e.target.closest(`[data-material-view]`);if(n){Mn(n);return}let r=e.target.closest(`[data-material-remove]`);r&&Nn(r)}),y.addEventListener(`click`,()=>{if(tn?.scanning){ti();return}ei()}),i.addEventListener(`click`,e=>{let t=e.target.closest(`[data-view-role-info]`);if(t){try{xi(t.dataset.viewRoleInfo)}catch{window.alert(`Could not load role information.`)}return}let n=e.target.closest(`[data-review-role-id]`);if(n){bi(n.dataset.reviewRoleId);return}let r=e.target.closest(`[data-prep-role-id]`);if(r){wi(r.dataset.prepRoleId);return}let i=e.target.closest(`.job-action`);if(i){li(i);return}let a=e.target.closest(`.pane-toggle`);if(!a)return;let o=a.parentElement.querySelector(`.pane-body`),s=a.getAttribute(`aria-expanded`)===`true`;a.setAttribute(`aria-expanded`,String(!s)),a.querySelector(`.chevron`).textContent=s?`>`:`v`,o.hidden=s,Ba()});async function li(e){let{roleId:t,status:n}=e.dataset;if(!t||!n)return;let r=e.closest(`.job-actions`),i=e.closest(`.job`);r.querySelectorAll(`button`).forEach(e=>{e.disabled=!0}),e.textContent=`updating...`;try{let e=await fetch(`/api/roles/${encodeURIComponent(t)}/status`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({status:n})});if(!e.ok)throw Error(`Status update failed`);ui((await e.json()).role,i)}catch{r.querySelectorAll(`button`).forEach(e=>{e.disabled=!1}),e.textContent=n===`disinterested`?`disinterested`:n.toLowerCase()}}function ui(e,t){if(!e||!T)return;let n=t?.closest(`.status-pane`)?.dataset.bucket??e.role_status,r=e.role_status,i=fi(e,n,r);pi(n,r),mi(n,r),yn(),_i(T.statuses),hi(t,i,n,r),Ba()}function di(e){if(!e||!T)return null;let t=null;return T.statuses.forEach(n=>{let r=n.jobs.findIndex(t=>String(t.id)===String(e.id));r!==-1&&(t={...n.jobs[r],...e},n.jobs[r]=t)}),_i(T.statuses),t}function fi(e,t,n){let r=e;T.statuses.forEach(t=>{let n=t.jobs.findIndex(t=>String(t.id)===String(e.id));n!==-1&&(r={...t.jobs[n],...e},t.jobs.splice(n,1),t.count=t.jobs.length)});let i=T.statuses.find(e=>e.key===n);return i&&(i.jobs.unshift(r),i.count=i.jobs.length),r}function pi(e,t){T.statuses.forEach(e=>{let t=document.querySelector(`#status-${CSS.escape(e.key)}`);t?.classList.toggle(`empty`,e.count===0);let n=t?.querySelector(`.count`);n&&(n.textContent=e.count)}),[e,t].forEach(e=>{gi(document.querySelector(`#status-${CSS.escape(e)}`))})}function mi(e,t){if(!T.stats)return;let n=jt.has(e),r=jt.has(t);if(n===r){vn(T.stats);return}T.stats.applications_total=Number(T.stats.applications_total??0)+(r?1:-1),vn(T.stats)}function hi(e,t,n,r){let i=document.querySelector(`#status-${CSS.escape(r)}`),a=i?.querySelector(`.pane-body`);if(!e||!i||!a)return;e.remove(),gi(document.querySelector(`#status-${CSS.escape(n)}`)),a.hidden=!1;let o=i.querySelector(`.pane-toggle`);o?.setAttribute(`aria-expanded`,`true`);let s=o?.querySelector(`.chevron`);s&&(s.textContent=`v`);let c=a.querySelector(`.jobs`);c||=(a.innerHTML=`<div class="jobs"></div>`,a.querySelector(`.jobs`)),c.insertAdjacentHTML(`afterbegin`,Fn(t,r)),gi(i)}function gi(e){if(!e)return;let t=e.querySelector(`.pane-body`);if(!t)return;let n=t.querySelector(`.jobs`),r=!!n?.querySelector(`.job`),i=t.querySelector(`.empty-copy`);if(r){i?.remove();return}n?.remove(),i||t.insertAdjacentHTML(`beforeend`,`<p class="empty-copy">no jobs in this status.</p>`)}function _i(e){ve.disabled=vi(e).length===0,ve.setAttribute(`aria-label`,`review discovered`),ve.innerHTML=`<span class="review-discovered-label">review discovered</span>`}function vi(e=T?.statuses??[]){return e.find(e=>e.key===`discovered`)?.jobs??[]}function yi(e=T?.statuses??[]){return e.find(e=>e.key===`interested`)?.jobs??[]}function bi(e=null){let t=[...vi()],n=e==null?null:String(e);if(n){let e=t.findIndex(e=>String(e.id)===n);if(e>0){let[n]=t.splice(e,1);t.unshift(n)}}k=t,h.hidden=!1,document.body.classList.add(`review-open`),Ei()}function xi(e){let t=String(e),n=(T?.statuses??[]).flatMap(e=>e.jobs??[]).find(e=>String(e.id)===t);if(!n)throw Error(`Role information not found`);be.innerHTML=`
    <div class="review-title-row">
      <p class="review-company">${W(n.company_name)}</p>
      <p class="review-role-title">${W(n.title)}</p>
    </div>
    <dl class="review-details review-primary-details">
      ${Y(`location`,n.location,!1,`review-location-detail`)}
      ${Y(`first`,V(n.first_seen_at))}
      ${Y(`last`,V(n.last_seen_at))}
    </dl>
    ${Oi(n.description)}
    <dl class="review-details review-technical-details">
      ${Y(`notes`,n.notes,!1,`review-wide-detail`)}
      ${Y(`company id`,n.company_id)}
      ${Y(`role id`,n.id)}
      ${Y(`status`,n.role_status)}
      ${Y(`posting id`,n.posting_id)}
      ${Y(`created`,V(n.created_at))}
      ${Y(`updated`,V(n.updated_at))}
      ${Y(`url`,n.role_url,!1,`review-wide-detail`)}
    </dl>
  `,ye.hidden=!1,document.body.classList.add(`review-open`),xe.focus()}function Si(){ye.hidden=!0,be.innerHTML=``,document.body.classList.remove(`review-open`)}function Ci(){h.hidden=!0,document.body.classList.remove(`review-open`),k=[]}function wi(e=null){let t=[...yi()].sort((e,t)=>Number(!!t.prep_started)-Number(!!e.prep_started)),n=e==null?null:String(e);if(n){let e=t.findIndex(e=>String(e.id)===n);if(e>0){let[n]=t.splice(e,1);t.unshift(n)}}A=t,g.hidden=!1,document.body.classList.add(`prep-open`),Hi()}function Ti(){g.hidden=!0,document.body.classList.remove(`prep-open`),A=[]}function Ei(e=``){let t=k[0],n=k.length,r=t?Di(t):``;if(Se.textContent=n>0?`review queue`:`review complete`,Ce.textContent=n>0?`${n} discovered ${n===1?`role`:`roles`} in queue`:``,h.querySelectorAll(`.review-action`).forEach(e=>{e.disabled=n===0}),!t){we.innerHTML=`
      <div class="review-empty">
        <h3>no discovered jobs left.</h3>
        <p>everything in this queue has been handled or moved out of discovered.</p>
      </div>
    `;return}we.innerHTML=`
    ${e?`<p class="review-message">${H(e)}</p>`:``}
    ${r?`<p class="review-message review-message-warning">${H(r)}</p>`:``}
    <div class="review-title-row">
      <p class="review-company">${W(t.company_name)}</p>
      ${_n(t.title,t.role_url,`review-role-title`)}
    </div>
    <dl class="review-details review-primary-details">
      ${Y(`location`,t.location,!1,`review-location-detail`)}
      ${Y(`first`,V(t.first_seen_at))}
      ${Y(`last`,V(t.last_seen_at))}
    </dl>
    ${Oi(t.description)}
    <dl class="review-details review-technical-details">
      ${Y(`notes`,t.notes,!1,`review-wide-detail`)}
      ${Y(`company id`,t.company_id)}
      ${Y(`role id`,t.id)}
      ${Y(`status`,t.role_status)}
      ${Y(`posting id`,t.posting_id)}
      ${Y(`created`,V(t.created_at))}
      ${Y(`updated`,V(t.updated_at))}
      ${Y(`url`,t.role_url,!0,`review-wide-detail`)}
    </dl>
  `}function Di(e){let t=Number(e.review_later_count??0);return t<=kt?``:`role review has been postponed ${t} times. it is recommended to set it to disinterested.`}function Y(e,t,n=!1,r=``){if(!t)return``;let i=n?`<a href="${H(t)}" target="_blank" rel="noreferrer">${W(t)}</a>`:W(t);return`
    <div class="review-detail ${H(r)}">
      <dt>${W(e)}</dt>
      <dd>${i}</dd>
    </div>
  `}function Oi(e){return e?`
    <div class="review-detail review-description">
      <dt>description</dt>
      <dd>${ki(e)}</dd>
    </div>
  `:``}function ki(e){let t=Ai(String(e)).replace(/\u00a0/g,` `);if(ji(t))return Mi(t);let n=t.split(/\r?\n/).map(e=>e.trim()).filter(Boolean),r=[],i=[],a=()=>{i.length!==0&&(r.push(`<ul>${i.map(e=>`<li>${e}</li>`).join(``)}</ul>`),i=[])};return n.forEach(e=>{let t=e.match(/^#{2,3}\s+(.+)$/);if(t){a(),r.push(`<h3>${W(t[1])}</h3>`);return}if(Bi(e)){a(),r.push(`<h3>${W(e.replace(/:$/,``))}</h3>`);return}let n=e.match(/^[-*]\s+(.+)$/);if(n){i.push(W(n[1]));return}a(),r.push(`<p>${W(e)}</p>`)}),a(),r.join(``)}function Ai(e){let t=document.createElement(`textarea`);return t.innerHTML=e,t.value}function ji(e){return/<\/?(?:a|br|div|em|h[1-6]|li|ol|p|span|strong|ul)\b/i.test(e)}function Mi(e){let t=document.createElement(`template`);t.innerHTML=e;let n=[];return Ni(t.content.childNodes,n),n.join(``)}function Ni(e,t){e.forEach(e=>{if(e.nodeType===Node.TEXT_NODE){let n=Ri(e.textContent);n&&t.push(`<p>${W(n)}</p>`);return}if(e.nodeType!==Node.ELEMENT_NODE)return;let n=e,r=n.tagName.toLowerCase();if(r===`script`||r===`style`||r===`br`)return;if(/^h[1-6]$/.test(r)){Fi(t,n.textContent);return}if(r===`ul`||r===`ol`){let e=Ii(n);e&&t.push(e);return}if(r===`p`){Pi(n,t);return}let i=Array.from(n.children).some(e=>[`DIV`,`H1`,`H2`,`H3`,`H4`,`H5`,`H6`,`OL`,`P`,`UL`].includes(e.tagName));if([`article`,`div`,`section`].includes(r)&&i){Ni(n.childNodes,t);return}let a=Array.from(n.children).filter(e=>[`UL`,`OL`].includes(e.tagName)),o=Ri(Li(n));if(o&&(zi(o,n)?Fi(t,o):t.push(`<p>${W(o)}</p>`)),a.length>0){a.forEach(e=>{let n=Ii(e);n&&t.push(n)});return}!o&&i&&Ni(n.childNodes,t)})}function Pi(e,t){if(!e.querySelector(`br`)){let n=Ri(Li(e));if(!n)return;zi(n,e)?Fi(t,n):t.push(`<p>${W(n)}</p>`);return}let n=``,r=()=>{let r=Ri(n);n=``,r&&(zi(r,e)?Fi(t,r):t.push(`<p>${W(r)}</p>`))};e.childNodes.forEach(e=>{if(e.nodeType===Node.ELEMENT_NODE&&e.tagName.toLowerCase()===`br`){r();return}n+=` ${e.textContent??``}`}),r()}function Fi(e,t){let n=Ri(t).replace(/:$/,``);n&&e.push(`<h3>${W(n)}</h3>`)}function Ii(e){let t=Array.from(e.children).filter(e=>e.tagName===`LI`).map(e=>{let t=Ri(Li(e)),n=Array.from(e.children).filter(e=>[`UL`,`OL`].includes(e.tagName)).map(e=>Ii(e)).filter(Boolean).join(``);return t||n?`<li>${W(t)}${n}</li>`:``}).filter(Boolean);return t.length>0?`<ul>${t.join(``)}</ul>`:``}function Li(e){let t=e.cloneNode(!0);return t.querySelectorAll(`ul, ol`).forEach(e=>{e.remove()}),t.textContent}function Ri(e){return String(e??``).replace(/\s+/g,` `).trim()}function zi(e,t){let n=e.replace(/:$/,``).trim();return!n||n.length>90?!1:Bi(n)||/:$/.test(e)?!0:/[.!?]$/.test(n)||n.split(/\s+/).length>10?!1:t.querySelector(`strong, b, u`)?!0:Bi(n)}function Bi(e){return Nt.test(String(e).trim())}async function Vi(e){let t=k[0];if(!t)return;if(e===`later`){h.querySelectorAll(`.review-action`).forEach(e=>{e.disabled=!0});try{let e=await da(t.id);k.shift(),di(e),Ei(`moved out of this review pass.`)}catch{Ei(`could not postpone that role. try again.`)}finally{h.querySelectorAll(`.review-action`).forEach(e=>{e.disabled=k.length===0})}return}if(![`interested`,`disinterested`].includes(e))return;let n=h.querySelectorAll(`.review-action`);n.forEach(e=>{e.disabled=!0});try{let n=await fa(t.id,e);k.shift(),Ei(e===`interested`?`marked interested.`:`marked disinterested.`),ui(n,document.querySelector(`.job[data-role-id="${CSS.escape(String(t.id))}"]`))}catch{n.forEach(e=>{e.disabled=!1}),Ei(`could not update that role. try again.`)}}async function Hi(e=``){let t=A[0],n=A.length;if(Ee.textContent=n>0?`prep queue`:`prep complete`,De.textContent=n>0?`${n} interested ${n===1?`role`:`roles`} in queue`:``,g.querySelectorAll(`.review-action`).forEach(e=>{e.disabled=n===0}),!t){_.innerHTML=`
      <div class="review-empty">
        <h3>no interested jobs left.</h3>
        <p>everything in this queue has been prepped, moved, or postponed.</p>
      </div>
    `;return}_.innerHTML=`
    ${e?`<p class="review-message">${H(e)}</p>`:``}
    <section class="prep-role-hero" aria-label="role overview">
      <div class="review-title-row">
        <div class="prep-role-eyebrow">
          <p class="review-company">${W(t.company_name)}</p>
          <span>application workspace</span>
        </div>
        ${_n(t.title,t.role_url,`review-role-title`)}
      </div>
      <dl class="review-details review-primary-details">
        ${Y(`location`,t.location,!1,`review-location-detail`)}
        ${Y(`last`,V(t.last_seen_at))}
        ${Y(`updated`,V(t.updated_at))}
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
      ${Ui(t)}
      ${qi(t)}
      ${Wi(t.id,t.description)}
      ${Gi(t)}
    </div>
  `,G(),$i(t.id).then(e=>{!e||A[0]?.id!==t.id||(M.set(t.id,e),_.querySelector(`.prep-resume`)?.replaceWith(Z(Ui(t,{resume:e}))),G())}).catch(()=>{}),ua(t.id).then(e=>{!e||A[0]?.id!==t.id||(N.set(t.id,e),_.querySelector(`.prep-cover-letter`)?.replaceWith(Z(qi(t,{coverLetter:e}))),G())}).catch(()=>{})}function Ui(e,t={}){let n=M.get(e.id),r=t.resume??n,i=t.tweaks??Rt.get(e.id)??``,a=`/api/roles/${encodeURIComponent(e.id)}/resume.pdf`;return t.loading?`
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
          ${r.pdf_base64?`<a class="prep-summary-action prep-cover-pdf-link" href="${H(a)}" target="_blank" rel="noreferrer">view</a>`:``}
        </div>
      </summary>
      <p class="prep-overview">${W(r.summary??`Saved resume for this role.`)}</p>
      ${X(e)}
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
          >${H(i)}</textarea>
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
          >${H(r.latex??``)}</textarea>
        </label>
        <section class="prep-document-preview" aria-label="resume preview">
          <div class="prep-preview-heading">
            <span>document preview</span>
            <p>Updates automatically after the source is saved.</p>
          </div>
          ${r.pdf_base64?`
                <iframe class="prep-cover-pdf" title="resume PDF preview" src="${H(a)}"></iframe>
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
    `}function Wi(e,t){return`
    <details class="prep-panel prep-description-panel" id="prep-description-${e}">
      <summary class="prep-analysis-header">
        <span class="prep-accordion-icon" aria-hidden="true"></span>
        <h3>description</h3>
      </summary>
      ${Oi(t)}
    </details>
  `}function Gi(e,t={}){let n=t.messages??zt.get(e.id)??[],r=!!t.loading;return`
    <details class="prep-panel prep-role-chat" id="prep-chat-${e.id}">
      <summary class="prep-analysis-header">
        <span class="prep-accordion-icon" aria-hidden="true"></span>
        <h3>chat about this role</h3>
        <span>${n.length?`${n.length} messages`:`ready`}</span>
      </summary>
      <div class="prep-role-chat-log" aria-live="polite">
        ${n.length?n.map(Ki).join(``):`<p class="prep-role-chat-empty">ask about fit, risks, resume emphasis, or cover letter angle.</p>`}
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
  `}function Ki(e){let t=e?.role===`assistant`?`assistant`:`user`;return`
    <article class="prep-role-chat-message prep-role-chat-message-${t}">
      <span>${t}</span>
      <p>${W(e?.content??``)}</p>
    </article>
  `}function qi(e,t={}){let n=N.get(e.id),r=t.coverLetter??n,i=t.tweaks??r?.tweaks??``,a=`/api/roles/${encodeURIComponent(e.id)}/cover-letter.pdf`;return t.loading?`
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
          ${r?.pdf_base64?`<a class="prep-summary-action prep-cover-pdf-link" href="${H(a)}" target="_blank" rel="noreferrer">view</a>`:``}
        </div>
      </summary>
      ${r?`<p class="prep-overview">${W(r.summary??`cover letter generated`)}</p>`:`<p class="prep-overview">generate a LaTeX cover letter from the resume, posting, and stored examples.</p>`}
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
                >${H(i)}</textarea>
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
                >${H(r.latex??``)}</textarea>
              </label>
              <section class="prep-document-preview" aria-label="cover letter preview">
                <div class="prep-preview-heading">
                  <span>document preview</span>
                  <p>Updates automatically after the source is saved.</p>
                </div>
                ${r.pdf_base64?`
                      <iframe class="prep-cover-pdf" title="cover letter PDF preview" src="${H(a)}"></iframe>
                    `:`<p class="prep-cover-path">PDF preview unavailable.</p>`}
              </section>
            </div>
          `:``}
    </details>
  `}function X(e,t={}){let n=j.get(e.id);if(!t.loading&&!t.error&&!t.analysis&&n)return X(e,{analysis:n});if(!t.loading&&!t.error&&!t.analysis)return`
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
    `;let r=t.analysis,i=Array.isArray(r?.feedback_items)?r.feedback_items:[],a=r?.verdict===`ready_to_apply`?`ready to apply`:`tweak`,o=Math.min(Lt.get(e.id)??0,Math.max(i.length-1,0)),s=i[o];return`
    <section class="prep-analysis" aria-label="ai analysis">
      <div class="prep-analysis-header">
        <h3>ai analysis</h3>
        <span>${i.length} ${i.length===1?`item`:`items`}</span>
      </div>
      <p class="prep-verdict">${W(a)}</p>
      <p class="prep-overview">${W(r?.overview??`analysis unavailable`)}</p>
      ${s?`
            <article class="prep-feedback" data-feedback-index="${o}">
              <p class="prep-feedback-label">${W(s.label)}</p>
              <h4>${W(s.title)}</h4>
              <p>${W(s.detail)}</p>
              ${Ji(s)}
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
  `}function Ji(e){return e?.tweak_prompt?`
    <div class="prep-proposed-edit">
      <p class="prep-proposed-label">tweak prompt</p>
      <p>${W(e.tweak_prompt)}</p>
    </div>
  `:`
      <div class="prep-proposed-edit">
        <p class="prep-proposed-label">feedback only</p>
        <p>not enough information to turn this into a safe resume tweak.</p>
      </div>
    `}async function Yi(e,t={}){if(!t.force&&j.has(e))return j.get(e);let n=await fetch(`/api/roles/${encodeURIComponent(e)}/prep-analysis`);if(!n.ok)throw Error(`Prep analysis request failed`);let r=await n.json();return r.analysis.resources=r.resources??[],j.set(e,r.analysis),r.analysis}function Z(e){let t=document.createElement(`template`);return t.innerHTML=e.trim(),t.content.firstElementChild}async function Xi(e){let t=A[0];if(!t)return;let n=g.querySelectorAll(`.review-action`);if(n.forEach(e=>{e.disabled=!0}),e===`later`){try{await da(t.id),t.review_later_count=Number(t.review_later_count??0)+1,A.length>1?(A.push(A.shift()),Hi(`moved to the back of the prep queue.`)):Hi(`only one role is in the prep queue.`)}catch{Hi(`could not postpone prep. try again.`)}return}if(e===`applied`)try{let e=await fa(t.id,`applied`);A.shift(),Hi(`moved to applied.`),ui(e,document.querySelector(`.job[data-role-id="${CSS.escape(String(t.id))}"]`))}catch{n.forEach(e=>{e.disabled=!1}),Hi(`could not move that role. try again.`)}}async function Zi(e,t,n,r){let i=await fetch(`/api/roles/${encodeURIComponent(e)}/prep-feedback`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({feedback_index:t,feedback_item:n,comment:r})});if(!i.ok)throw Error(`Prep feedback update failed`);return i.json()}async function Qi(e,t,n,r){let i=await fetch(`/api/roles/${encodeURIComponent(e)}/prep-feedback-ignore`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({feedback_index:t,feedback_item:n,comment:r})});if(!i.ok)throw Error(`Prep feedback ignore failed`);return i.json()}async function $i(e,{force:t=!1}={}){if(!t&&M.has(e))return M.get(e);let n=await fetch(`/api/roles/${encodeURIComponent(e)}/resume`);if(!n.ok)throw Error(`Resume request failed`);let r=await n.json();return r.resume&&M.set(e,r.resume),r.resume}async function ea(e,t){let n=await fetch(`/api/roles/${encodeURIComponent(e)}/resume/save`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({latex:t})});if(!n.ok)throw Error(`Resume save failed`);return n.json()}async function ta(e,t,n){let r=await fetch(`/api/roles/${encodeURIComponent(e)}/resume`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({tweaks:t,previous_latex:n})});if(!r.ok)throw Error(`Resume generation failed`);return r.json()}async function na(e,t){let n=await fetch(`/api/roles/${encodeURIComponent(e)}/chat`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({messages:t})});if(!n.ok)throw Error(`Role chat failed`);return n.json()}function ra(e,t,n=At){let r=Bt.get(e)??{timer:null,saving:!1,version:0,latex:``};r.version+=1,r.latex=t,r.timer&&clearTimeout(r.timer),r.timer=setTimeout(()=>{r.timer=null,ia(e)},n),Bt.set(e,r)}async function ia(e){let t=Bt.get(e);if(!t||t.saving)return;t.saving=!0;let n=t.version,r=t.latex;try{let i=await ea(e,r);t.version===n&&(M.set(e,i.resume),aa(`resume`,e,i.resume))}catch{}finally{t.saving=!1,t.version!==n&&ra(e,t.latex,0)}}function aa(e,t,n){if(!n?.pdf_base64)return;let r=e===`resume`?`[data-prep-resume-latex="${t}"]`:`[data-prep-cover-letter-latex="${t}"]`,i=_.querySelector(r)?.closest(`.prep-panel`),a=i?.querySelector(`.prep-cover-pdf`),o=i?.querySelector(`.prep-cover-pdf-link`),s=e===`resume`?`/api/roles/${encodeURIComponent(t)}/resume.pdf`:`/api/roles/${encodeURIComponent(t)}/cover-letter.pdf`;a&&(a.src=`${s}?v=${Date.now()}`),o&&(o.href=s)}async function oa(e,t=``,n=``){let r=await fetch(`/api/roles/${encodeURIComponent(e)}/cover-letter`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({tweaks:t,previous_latex:n})});if(!r.ok)throw Error(`Cover letter generation failed`);return r.json()}async function sa(e,t){let n=await fetch(`/api/roles/${encodeURIComponent(e)}/cover-letter/save`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({latex:t})});if(!n.ok)throw Error(`Cover letter save failed`);return n.json()}function ca(e,t,n=``,r=At){let i=Vt.get(e)??{timer:null,saving:!1,version:0,latex:``,tweaks:``};i.version+=1,i.latex=t,i.tweaks=n,i.timer&&clearTimeout(i.timer),i.timer=setTimeout(()=>{i.timer=null,la(e)},r),Vt.set(e,i)}async function la(e){let t=Vt.get(e);if(!t||t.saving)return;t.saving=!0;let n=t.version,r=t.latex,i=t.tweaks;try{let a=await sa(e,r);t.version===n&&(N.set(e,{...a.cover_letter,tweaks:i}),aa(`coverLetter`,e,a.cover_letter))}catch{}finally{t.saving=!1,t.version!==n&&ca(e,t.latex,t.tweaks,0)}}async function ua(e){if(N.has(e))return N.get(e);let t=await fetch(`/api/roles/${encodeURIComponent(e)}/cover-letter`);if(!t.ok)throw Error(`Cover letter request failed`);let n=await t.json();return n.cover_letter&&N.set(e,n.cover_letter),n.cover_letter}async function da(e){let t=await fetch(`/api/roles/${encodeURIComponent(e)}/review-later`,{method:`POST`});if(!t.ok)throw Error(`Review later update failed`);return(await t.json()).role}async function fa(e,t){let n=await fetch(`/api/roles/${encodeURIComponent(e)}/status`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({status:t})});if(!n.ok)throw Error(`Status update failed`);return(await n.json()).role}function pa(e){return`${e}-${globalThis.crypto?.randomUUID?.()??`${Date.now()}-${Math.random()}`}`}function ma(e){window.location.hash!==e&&window.history.pushState({},``,e||`${window.location.pathname}${window.location.search}`)}async function ha({seedJobs:e=null}={}){Ae.hidden=!1,document.body.classList.add(`prepped-open`),ma(`#prepped-roles`),e?(P=e,F=F??P[0]?.role_id??null,$()):P.length===0&&(Me.textContent=`loading prepared roles...`),await _a(),va()}function ga({clearHash:e=!0}={}){Ae.hidden=!0,document.body.classList.remove(`prepped-open`),ya(),L.clear(),qt.clear(),R.forEach(e=>URL.revokeObjectURL(e)),R.clear(),Jt.clear(),Yt.clear(),e&&window.location.hash===`#prepped-roles`&&ma(``)}window.addEventListener(`pagehide`,()=>{document.querySelectorAll(`[data-preview-blob-url]`).forEach(e=>{URL.revokeObjectURL(e.dataset.previewBlobUrl)}),R.forEach(e=>URL.revokeObjectURL(e)),R.clear(),Jt.clear()});async function _a(){try{let e=await fetch(`/api/autoprep/jobs`);if(!e.ok)throw Error(`Prepped roles request failed`);let t=await e.json();P=t.jobs??[];let n=t.bulk_cover_letter_regeneration;if(n){let e=Array.isArray(n.jobs)?n.jobs:[];I={idempotencyKey:n.idempotency_key,roleIds:e.map(e=>Number(e.role_id)),jobs:e,skipped:Array.isArray(n.skipped)?n.skipped:[]}}P.some(e=>Number(e.role_id)===Number(F))||(F=P[0]?.role_id??null),$()}catch{Me.textContent=`could not refresh preparation progress.`}}function va(){ya(),P.some(ba)&&(Ht=window.setInterval(_a,2e3))}function ya(){Ht!==null&&window.clearInterval(Ht),Ht=null}function ba(e){return[`queued`,`generating_resume_tweaks`,`regenerating_resume`,`generating_cover_letter`].includes(e.overall_status)}function xa(e){return[e.resume_status,e.cover_letter_status].some(e=>[`failed`,`interrupted`].includes(e))}function Sa(e){return e.cover_letter_status===`generating`||e.overall_status===`generating_cover_letter`}function Ca(e){return Sa(e)||e.resume_status===`generating_tweaks`||e.resume_status===`regenerating`||e.overall_status===`generating_resume_tweaks`||e.overall_status===`regenerating_resume`}function wa(e){return e.worker_state===`queued`||e.overall_status===`queued`}function Ta(e){return{queued:`Queued`,generating_resume_tweaks:`Generating resume tweaks`,regenerating_resume:`Regenerating resume`,generating_cover_letter:`Generating cover letter`,partially_complete:`Partially complete`,ready:`Ready`,failed:`Failed`,interrupted:`Interrupted`,generating_tweaks:`Generating tweaks`,regenerating:`Regenerating`,generating:`Generating`}[e]??U(e)}function Ea(e,t){let n=t===`cover-letter`?`cover_letter`:`resume`;return`${e.updated_at||``}:${e[`${n}_artifact_path`]||``}`}function Q(e,{close:t=!1}={}){let n=R.get(e);n&&URL.revokeObjectURL(n),R.delete(e),Jt.delete(e),Yt.delete(e),t&&L.delete(e)}function Da(){Jt.forEach((e,t)=>{let[n,r]=t.split(`:`),i=P.find(e=>Number(e.role_id)===Number(n));(!i||Ea(i,r)!==e)&&Q(t,{close:!0})})}function Oa(){if(!I)return;let e=I.jobs||P,t=new Map(e.map(e=>[Number(e.role_id),e])),n=I.roleIds.map(e=>t.get(Number(e))),r=n.filter(e=>e?.worker_state===`idle`&&e.cover_letter_status===`ready`).length,i=n.filter(e=>!e||e.worker_state===`idle`&&[`failed`,`interrupted`].includes(e.cover_letter_status)),a=n.length-r-i.length,o=I.skipped.length?` Skipped before queueing: ${I.skipped.map(e=>`${e.company_name} — ${e.title}: ${e.reason}`).join(` · `)}`:``,s=i.length?` Queued regeneration failures: ${i.map(e=>e?`${e.company_name} — ${e.title}: ${e.cover_letter_error||`generation failed`}`:`A role left the Prepped queue before regeneration completed`).join(` · `)}`:``;Wt=n.length?a>0?`Cover-letter regeneration in progress: ${r} of ${n.length} complete · ${a} remaining.${o}${s}`:`Cover-letter regeneration complete: ${r} succeeded, ${i.length} failed.${o}${s}`:`No cover letters were queued.${o}`}function $(){Da(),Oa();let e=P.filter(ba).length,t=P.filter(e=>e.worker_state===`idle`&&e.cover_letter_status===`ready`).length;Me.textContent=P.length?`${P.length} prepped ${P.length===1?`role`:`roles`}${e?` · ${e} in progress`:``}`:`No queued or prepared roles.`,Ne.disabled=Ut||t===0,Ne.setAttribute(`aria-busy`,Ut?`true`:`false`),Ne.textContent=Ut?`queuing cover letters...`:`regenerate all cover letters`,Pe.textContent=Wt,Fe.innerHTML=P.map(e=>{let t=xa(e),n=!t&&Ca(e),r=!t&&!n&&wa(e),i=Number(e.role_id)===Number(F)?` is-active`:``;return`
      <button type="button" class="prepped-list-item${r?` is-generation-queued`:``}${n?` is-document-generating`:``}${t?` has-generation-failure`:``}${i}" data-prepped-role="${e.role_id}">
        <strong>${W(e.company_name)}</strong><span>${W(e.title)}</span>
        <small class="status-${H(e.overall_status)}">${H(Ta(e.overall_status))}</small>
      </button>`}).join(``),ka(),va()}function ka(){let e=P.findIndex(e=>Number(e.role_id)===Number(F)),t=P[e];if(!t){v.innerHTML=`<div class="prepped-empty"><h3>nothing prepped yet.</h3><p>Queue Interested roles from Autoprep Interested.</p></div>`;return}let n=W(t.title),r=fn(t.role_url),i=r?`<a class="prepped-role-link" href="${H(r)}" target="_blank" rel="noopener noreferrer">${n}<span aria-hidden="true">↗</span></a>`:n,a=[[`Location`,t.location||`Unavailable`],[`Added`,V(t.date_added||t.created_at)||`Unavailable`],[`Last seen`,V(t.last_seen_at)||`Unavailable`],[`Posting ID`,t.posting_id||`Unavailable`]],o=Gt.has(Number(t.role_id)),s=o||ba(t),c=`${t.role_id}:description`,l=`${t.role_id}:notes`;v.innerHTML=`
    <header class="prepped-detail-heading">
      <div><p class="eyebrow">${W(t.company_name)}</p><h3>${i}</h3></div>
      <span class="prepped-status status-${H(t.overall_status)}">${H(Ta(t.overall_status))}</span>
    </header>
    <dl class="prepped-role-facts">${a.map(([e,t])=>`<div><dt>${H(e)}</dt><dd>${W(t)}</dd></div>`).join(``)}</dl>
    <details class="prepped-role-description" data-prepped-detail-section="description" ${qt.has(c)?`open`:``}>
      <summary>Job description</summary>
      <div class="prepped-description-copy">${W(t.description||`No job description was saved.`).replaceAll(`
`,`<br>`)}</div>
    </details>
    ${t.notes?`<details class="prepped-role-description" data-prepped-detail-section="notes" ${qt.has(l)?`open`:``}><summary>Role notes</summary><div class="prepped-description-copy">${W(t.notes).replaceAll(`
`,`<br>`)}</div></details>`:``}
    <div class="prepped-document-grid">
      ${ja(t,`resume`,`Resume`)}
      ${ja(t,`cover-letter`,`Cover letter`)}
    </div>
    <div class="prepped-detail-actions">
      <button type="button" data-prepped-nav="previous" ${e<=0?`disabled`:``}>Previous</button>
      <button type="button" data-prepped-nav="next" ${e>=P.length-1?`disabled`:``}>Next</button>
      <button type="button" data-autoprep-open-folder ${t.artifact_directory?``:`disabled`}>Open Documents Folder</button>
      <button class="prepped-disinterested" type="button" data-autoprep-disinterested aria-busy="${o?`true`:`false`}" ${s?`disabled`:``} title="${ba(t)?`Wait for preparation to finish before moving this role`:`Move this role out of Prepped`}">${o?`Moving to Disinterested...`:`Move to Disinterested`}</button>
      <button class="success" type="button" data-autoprep-applied ${t.overall_status===`ready`?``:`disabled`}>Applied</button>
    </div>
    <p class="prepped-safety-note">Autoprep prepares files only. It never submits an application.</p>`}async function Aa(e,t){let n=`${e.role_id}:${t}`,r=Ea(e,t);if(!(Jt.get(n)===r||Xt.has(n))){Q(n),Xt.add(n),Yt.delete(n),ka();try{let i=await jn(`/api/autoprep/roles/${encodeURIComponent(e.role_id)}/documents/${t}.pdf?v=${encodeURIComponent(e.updated_at||``)}`),a=P.find(t=>Number(t.role_id)===Number(e.role_id));if(!L.has(n)||!a||Ea(a,t)!==r){URL.revokeObjectURL(i),L.delete(n);return}R.set(n,i),Jt.set(n,r)}catch(e){Yt.set(n,e instanceof Error?e.message:`PDF preview unavailable`)}finally{Xt.delete(n),Number(F)===Number(e.role_id)&&ka()}}}function ja(e,t,n){let r=t===`cover-letter`?`cover_letter`:`resume`,i=e[`${r}_status`],a=e[`${r}_artifact_path`],o=a?.split(`/`).pop()??`Not available`,s=e[`${r}_error`],c=e[`${r}_instruction`]||``,l=`${e.role_id}:${t}`,u=Kt.get(l)??c,d=t===`cover-letter`?`Optional comments for the next version`:`Comments for the next version`,ee=t===`cover-letter`?`Optionally describe specific, truthful changes...`:`Describe specific, truthful changes...`,te=[`failed`,`interrupted`].includes(i),ne=e.worker_state!==`idle`||[`queued`,`generating`,`generating_tweaks`,`regenerating`].includes(i),re=!ne&&(i===`ready`||te)&&(te||t===`cover-letter`||String(u).trim()),f=L.has(l),p=`/api/autoprep/roles/${encodeURIComponent(e.role_id)}/documents/${t}.pdf?v=${encodeURIComponent(e.updated_at||``)}`,m=R.get(l),ie=Yt.get(l),ae=Xt.has(l),oe=a?`<a class="prep-cover-pdf-link" data-autoprep-view="${t}" href="${H(p)}" target="_blank" rel="noreferrer" aria-label="View ${H(n.toLowerCase())} PDF in browser">View PDF</a>`:``;return`
    <section class="prepped-document${f?` has-open-preview`:``} status-${H(i)}">
      <div class="prepped-document-heading"><h4>${H(n)}</h4><span>${H(Ta(i))}</span></div>
      <p class="prepped-filename">${H(o)}</p>
      ${s?`<p class="prepped-error">${H(s)}</p>`:``}
      <div class="prepped-document-actions">
        <button type="button" data-autoprep-preview="${t}" ${a?``:`disabled`}>${f?`Hide preview`:`Preview PDF`}</button>
        ${oe}
      </div>
      <div class="prepped-pdf-preview" data-autoprep-preview-panel="${t}" ${f&&a?``:`hidden`}>
        ${f&&m?`<iframe title="${H(n)} PDF preview" src="${H(m)}"></iframe>`:``}
        ${f&&ae?`<p>Loading PDF preview...</p>`:``}
        ${f&&ie?`<p class="prepped-error">${W(ie)}</p>`:``}
      </div>
      <label class="prepped-comments-label" for="prepped-comments-${H(l)}">${d}</label>
      <textarea id="prepped-comments-${H(l)}" data-autoprep-comments="${t}" rows="4" placeholder="${ee}" ${ne?`disabled`:``}>${W(u)}</textarea>
      <button class="prepped-regenerate" type="button" data-autoprep-regenerate="${t}" ${re?``:`disabled`}>${ne?`Regenerating...`:`Regenerate ${H(n)}`}</button>
    </section>`}async function Ma(e,t,n){if(n.disabled)return;let r=`${e.role_id}:${t}`,i=e[`${t===`cover-letter`?`cover_letter`:`resume`}_status`],a=[`failed`,`interrupted`].includes(i),o=v.querySelector(`[data-autoprep-comments="${t}"]`),s=String(o?.value||Kt.get(r)||``).trim();if(!s&&t!==`cover-letter`&&!a){o?.focus();return}n.disabled=!0,n.textContent=`Queuing regeneration...`;try{let n=await fetch(`/api/autoprep/roles/${encodeURIComponent(e.role_id)}/${a?`retry`:`regenerate`}/${t}`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(a?{idempotency_key:pa(`retry-${t}`)}:{comments:s,idempotency_key:pa(`regenerate-${t}`)})}),i=await n.json();if(!n.ok)throw Error(i.error||`Regeneration request failed`);Kt.delete(r),Q(r,{close:!0});let o=P.findIndex(t=>Number(t.role_id)===Number(e.role_id));o>=0&&(P[o]=i.job),$()}catch(e){window.alert(e instanceof Error?e.message:`Regeneration request failed`),await _a()}}async function Na(){if(!Ut){Ut=!0,I=null,Wt=`Queuing eligible cover letters...`,$();try{let e=await fetch(`/api/autoprep/cover-letters/regenerate`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({idempotency_key:pa(`regenerate-all-cover-letters`)})}),t=await e.json();if(!e.ok)throw Error(t.error||`Bulk regeneration request failed`);let n=Number(t.queued_count||0),r=Array.isArray(t.skipped)?t.skipped:[];I={roleIds:(t.jobs||[]).map(e=>Number(e.role_id)),jobs:t.jobs||[],skipped:r},!n&&!r.length&&(I=null,Wt=`No prepped roles are available to regenerate.`),(t.jobs||[]).forEach(e=>{let t=P.findIndex(t=>Number(t.role_id)===Number(e.role_id));t>=0&&(P[t]=e),Q(`${e.role_id}:cover-letter`,{close:!0})}),await _a(),va()}catch(e){I=null,Wt=e instanceof Error?e.message:`Bulk regeneration request failed`}finally{Ut=!1,$()}}}async function Pa(e,t){let n=Number(e);if(Gt.has(n))return;Gt.add(n),t.disabled=!0,t.setAttribute(`aria-busy`,`true`),t.textContent=`Moving to Disinterested...`;let r=P.findIndex(e=>Number(e.role_id)===n);try{await fa(e,`disinterested`),Q(`${e}:resume`,{close:!0}),Q(`${e}:cover-letter`,{close:!0}),r>=0&&P.splice(r,1),F=P[Math.min(r,P.length-1)]?.role_id??null,Wt=`Role moved to Disinterested.`,$(),Dr()}catch(e){Wt=e instanceof Error?e.message:`Could not move this role to Disinterested.`,await _a()}finally{Gt.delete(n),P.some(e=>Number(e.role_id)===n)&&$()}}async function Fa(e,t){if(t.disabled)return;t.disabled=!0,t.textContent=`Moving to Applied...`;let n=P.findIndex(t=>Number(t.role_id)===Number(e));try{if(!(await fetch(`/api/autoprep/roles/${encodeURIComponent(e)}/applied`,{method:`POST`})).ok)throw Error(`Applied update failed`);Q(`${e}:resume`,{close:!0}),Q(`${e}:cover-letter`,{close:!0}),P.splice(n,1),F=P[Math.min(n,P.length-1)]?.role_id??null,$(),Dr()}catch{await _a()}}ve.addEventListener(`click`,bi),Te.addEventListener(`click`,Ci),xe.addEventListener(`click`,Si),ke.addEventListener(`click`,()=>ha()),je.addEventListener(`click`,ga),Ne.addEventListener(`click`,Na),Fe.addEventListener(`click`,e=>{let t=e.target.closest(`[data-prepped-role]`);t&&(F=Number(t.dataset.preppedRole),$())}),v.addEventListener(`input`,e=>{let t=e.target.closest(`[data-autoprep-comments]`);if(!t)return;let n=`${F}:${t.dataset.autoprepComments}`;Kt.set(n,t.value);let r=v.querySelector(`[data-autoprep-regenerate="${t.dataset.autoprepComments}"]`),i=P.find(e=>Number(e.role_id)===Number(F)),a=t.dataset.autoprepComments===`cover-letter`?`cover_letter`:`resume`,o=i?.[`${a}_status`],s=[`failed`,`interrupted`].includes(o);r&&(r.disabled=i?.worker_state!==`idle`||![`ready`,`failed`,`interrupted`].includes(o)||!s&&t.dataset.autoprepComments!==`cover-letter`&&!t.value.trim())}),v.addEventListener(`toggle`,e=>{let t=e.target.closest(`[data-prepped-detail-section]`);if(!t)return;let n=`${F}:${t.dataset.preppedDetailSection}`;t.open?qt.add(n):qt.delete(n)},!0),v.addEventListener(`click`,async e=>{let t=P.find(e=>Number(e.role_id)===Number(F));if(!t)return;let n=e.target.closest(`[data-prepped-nav]`);if(n){let e=P.indexOf(t),r=n.dataset.preppedNav===`next`?1:-1;F=P[e+r]?.role_id??t.role_id,$();return}let r=e.target.closest(`[data-autoprep-preview]`);if(r){let e=r.dataset.autoprepPreview,n=`${t.role_id}:${e}`;L.has(n)?(L.delete(n),ka()):(L.add(n),ka(),Aa(t,e));return}let i=e.target.closest(`[data-autoprep-regenerate]`);if(i){Ma(t,i.dataset.autoprepRegenerate,i);return}let a=e.target.closest(`[data-autoprep-open-folder]`);if(a&&!a.disabled){a.disabled=!0,a.textContent=`Opening...`;try{if(!(await fetch(`/api/autoprep/roles/${encodeURIComponent(t.role_id)}/open-folder`,{method:`POST`})).ok)throw Error(`Could not open the documents folder.`);a.textContent=`Opened in Finder`,window.setTimeout(()=>{a.isConnected&&(a.textContent=`Open Documents Folder`,a.disabled=!1)},1500)}catch(e){a.textContent=e instanceof Error?e.message:`Could not open folder`,a.disabled=!1}return}let o=e.target.closest(`[data-autoprep-disinterested]`);if(o){Pa(t.role_id,o);return}let s=e.target.closest(`[data-autoprep-applied]`);s&&Fa(t.role_id,s)}),Oe.addEventListener(`click`,Ti),h.addEventListener(`click`,e=>{let t=e.target.closest(`[data-review-action]`);t&&Vi(t.dataset.reviewAction)}),g.addEventListener(`click`,e=>{e.target.closest(`.prep-summary-action`)&&e.stopPropagation()}),g.addEventListener(`input`,e=>{let t=e.target.closest(`[data-prep-resume-tweaks]`);if(t){let e=Number(t.dataset.prepResumeTweaks);Number.isFinite(e)&&Rt.set(e,t.value);return}let n=e.target.closest(`[data-prep-resume-latex]`);if(n){let e=Number(n.dataset.prepResumeLatex);if(!Number.isFinite(e))return;ra(e,n.value);return}let r=e.target.closest(`[data-prep-cover-letter-latex]`);if(!r)return;let i=Number(r.dataset.prepCoverLetterLatex);if(!Number.isFinite(i))return;let a=r.closest(`.prep-cover-letter`)?.querySelector(`[data-prep-cover-letter-tweaks="${i}"]`)?.value??``;ca(i,r.value,a)}),g.addEventListener(`scroll`,e=>{e.target.closest(`[data-prep-resume-latex], [data-prep-cover-letter-latex]`)},!0),g.addEventListener(`focusout`,e=>{let t=e.target.closest(`[data-prep-resume-latex]`);if(t){let e=Number(t.dataset.prepResumeLatex);if(!Number.isFinite(e))return;ra(e,t.value,0);return}let n=e.target.closest(`[data-prep-cover-letter-latex]`);if(!n)return;let r=Number(n.dataset.prepCoverLetterLatex);if(!Number.isFinite(r))return;let i=n.closest(`.prep-cover-letter`)?.querySelector(`[data-prep-cover-letter-tweaks="${r}"]`)?.value??``;ca(r,n.value,i,0)}),g.addEventListener(`submit`,async e=>{let t=e.target.closest(`[data-prep-role-chat-form]`);if(!t||!A[0])return;e.preventDefault();let n=Number(t.dataset.prepRoleChatForm);if(!Number.isFinite(n))return;let r=t.querySelector(`[data-prep-role-chat-input="${n}"]`),i=r?.value?.trim()??``;if(!i){r?.focus();return}let a=[...zt.get(n)??[],{role:`user`,content:i}];zt.set(n,a),_.querySelector(`.prep-role-chat`)?.replaceWith(Z(Gi(A[0],{messages:a,loading:!0})));try{let e=await na(n,a),t=[...a,e.message];zt.set(n,t),_.querySelector(`.prep-role-chat`)?.replaceWith(Z(Gi(A[0],{messages:t})))}catch{let e=[...a,{role:`assistant`,content:`could not answer right now.`}];zt.set(n,e),_.querySelector(`.prep-role-chat`)?.replaceWith(Z(Gi(A[0],{messages:e})))}}),g.addEventListener(`click`,async e=>{let t=e.target.closest(`[data-prep-section-target]`);if(t){let e=t.dataset.prepSectionTarget,n=e?document.getElementById(e):null;if(n instanceof HTMLDetailsElement){n.open=!0,n.scrollIntoView({behavior:`smooth`,block:`start`});let e=n.querySelector(`summary`);e?.setAttribute(`tabindex`,`-1`),e?.focus({preventScroll:!0})}return}if(e.target.closest(`[data-prep-analysis]`)&&A[0]){let e=A[0].id;_.querySelector(`.prep-analysis`)?.replaceWith(Z(X(A[0],{loading:!0})));try{let t=await Yi(e,{force:!0});if(A[0]?.id!==e)return;_.querySelector(`.prep-analysis`)?.replaceWith(Z(X(A[0],{analysis:t})))}catch{_.querySelector(`.prep-analysis`)?.replaceWith(Z(X(A[0],{error:!0})))}return}if(e.target.closest(`[data-prep-resume-regenerate]`)&&A[0]){let e=A[0].id,t=_.querySelector(`.prep-resume`),n=t?.querySelector(`[data-prep-resume-tweaks="${e}"]`)?.value??``,r=t?.querySelector(`[data-prep-resume-latex="${e}"]`)?.value??``;if(!n.trim()){t?.querySelector(`[data-prep-resume-tweaks="${e}"]`)?.focus();return}Rt.set(e,n),t?.replaceWith(Z(Ui(A[0],{loading:!0})));try{let t=await ta(e,n,r);M.set(e,t.resume),_.querySelector(`.prep-resume`)?.replaceWith(Z(Ui(A[0],{resume:t.resume}))),G()}catch{_.querySelector(`.prep-resume`)?.replaceWith(Z(Ui(A[0],{resume:M.get(e),tweaks:n}))),G()}return}if(e.target.closest(`[data-prep-cover-letter]`)&&A[0]){let e=A[0].id,t=_.querySelector(`.prep-cover-letter`),n=t?.querySelector(`[data-prep-cover-letter-tweaks="${e}"]`)?.value??``,r=n.trim()?t?.querySelector(`[data-prep-cover-letter-latex="${e}"]`)?.value??``:``;t?.replaceWith(Z(qi(A[0],{loading:!0})));try{let t=await oa(e,n,r);N.set(e,t.cover_letter),_.querySelector(`.prep-cover-letter`)?.replaceWith(Z(qi(A[0],{coverLetter:t.cover_letter}))),G()}catch{_.querySelector(`.prep-cover-letter`)?.replaceWith(Z(qi(A[0],{coverLetter:N.get(e),tweaks:n}))),G()}return}let n=e.target.closest(`[data-prep-action]`);if(n){Xi(n.dataset.prepAction);return}let r=e.target.closest(`[data-prep-feedback]`);if(!r||!A[0])return;let i=A[0].id,a=j.get(i),o=Array.isArray(a?.feedback_items)?a.feedback_items.length:0,s=Lt.get(i)??0;if(r.dataset.prepFeedback===`accept`||r.dataset.prepFeedback===`ignore`){let e=a?.feedback_items?.[s];if(!e)return;let t=_.querySelector(`[data-prep-feedback-comment]`)?.value??``,n=r.dataset.prepFeedback,o=n;r.disabled=!0,r.textContent=n===`accept`?`adding...`:`ignoring...`;try{if(n===`accept`){let n=await Zi(i,s,e,t),r=document.querySelector(`.job[data-role-id="${CSS.escape(String(i))}"]`);n.role&&(A[0]=n.role,ui(n.role,r)),La(i,n.tweak_prompt??e.tweak_prompt??``),Ia(i,s,a)}else await Qi(i,s,e,t),Ia(i,s,a)}catch{r.disabled=!1,r.textContent=o}return}let c=r.dataset.prepFeedback===`next`?1:-1;Lt.set(i,Math.max(0,Math.min(s+c,o-1))),_.querySelector(`.prep-analysis`)?.replaceWith(Z(X(A[0],{analysis:a})))});function Ia(e,t,n){let r=n.feedback_items.filter((e,n)=>n!==t),i=Math.min(t,Math.max(r.length-1,0)),a={...n,feedback_items:r,verdict:r.length===0?`ready_to_apply`:n.verdict};Lt.set(e,i),j.set(e,a),_.querySelector(`.prep-analysis`)?.replaceWith(Z(X(A[0],{analysis:a})))}function La(e,t){let n=String(t||``).trim();if(!n)return;let r=Rt.get(e)?.trim()??``,i=r?`${r}\n\n${n}`:n;Rt.set(e,i);let a=_.querySelector(`[data-prep-resume-tweaks="${e}"]`);a&&(a.value=i,a.focus())}document.addEventListener(`keydown`,e=>{e.key===`Escape`&&!ye.hidden&&Si(),e.key===`Escape`&&!ze.hidden&&Yn(),e.key===`Escape`&&!o.hidden&&un(),e.key===`Escape`&&!h.hidden&&Ci(),e.key===`Escape`&&!g.hidden&&Ti(),e.key===`Escape`&&!Ae.hidden&&ga(),e.key===`Escape`&&!qe.hidden&&rr(),e.key===`Escape`&&!ct.hidden&&dr(),e.key===`Escape`&&!ht.hidden&&br(),e.key===`Escape`&&!xt.hidden&&Lr()}),Re.addEventListener(`click`,Jn),Ve.addEventListener(`click`,Yn),Be.addEventListener(`click`,Yn);function Ra(){return Array.from(document.querySelectorAll(`.pane-toggle`))}function za(){return Ra().some(e=>e.getAttribute(`aria-expanded`)===`true`)}function Ba(){Ue.textContent=za()?`collapse all`:`expand all`}function Va(){document.querySelectorAll(`.pane-toggle`).forEach(e=>{e.setAttribute(`aria-expanded`,`true`),e.querySelector(`.chevron`).textContent=`v`,e.parentElement.querySelector(`.pane-body`).hidden=!1})}function Ha(){document.querySelectorAll(`.job[open]`).forEach(e=>{e.open=!1}),document.querySelectorAll(`.pane-toggle`).forEach(e=>{e.setAttribute(`aria-expanded`,`false`),e.querySelector(`.chevron`).textContent=`>`,e.parentElement.querySelector(`.pane-body`).hidden=!0})}Ue.addEventListener(`click`,()=>{za()?Ha():Va(),Ba()}),We.addEventListener(`click`,()=>{Pt=!Pt,We.textContent=Pt?`show empty`:`hide empty`,T&&Pn(T.statuses)}),Ke.addEventListener(`click`,nr),Je.addEventListener(`click`,rr),st.addEventListener(`click`,ur),lt.addEventListener(`click`,dr),mt.addEventListener(`click`,yr),gt.addEventListener(`click`,br),Ie.addEventListener(`click`,Ir),St.addEventListener(`click`,Lr),Ct.addEventListener(`submit`,e=>{e.preventDefault(),Br(Ct).catch(()=>{C.textContent=`could not add company.`})}),wt.addEventListener(`submit`,e=>{e.preventDefault(),Gr(wt).catch(()=>{Ot.textContent=`could not add role.`})}),w.addEventListener(`submit`,e=>{let t=e.target.closest(`[data-company-link-form]`);t&&(e.preventDefault(),Vr(t).catch(()=>{C.textContent=`could not add link.`}))}),w.addEventListener(`input`,e=>{let t=e.target.closest(`[data-company-notes]`);t&&Jr(t.dataset.companyNotes)}),w.addEventListener(`change`,e=>{let t=e.target.closest(`[data-company-tier]`);if(!t)return;let n=t.closest(`.company-panel`);n&&Xr(n,t.value),window.clearTimeout(sn.get(t.dataset.companyTier)),Yr(t.dataset.companyTier).catch(()=>{qr(`could not save company.`)})}),w.addEventListener(`click`,e=>{let t=e.target.closest(`[data-delete-company]`);if(t){let e=Kr(t.dataset.deleteCompany),n=e?.name?U(e.name):`this company`;if(!window.confirm(`Deactivate ${n}? It will be hidden from company counts and skipped during scans.`))return;t.disabled=!0,Ur(t.dataset.deleteCompany).catch(()=>{C.textContent=`could not deactivate company.`,t.disabled=!1});return}let n=e.target.closest(`[data-delete-career-page]`);if(!n)return;let r=n.closest(`.company-link-row`)?.querySelector(`.company-link-text`)?.textContent?.trim();window.confirm(`Delete ${r||`this career link`}?`)&&(n.disabled=!0,Hr(n.dataset.deleteCareerPage).catch(()=>{C.textContent=`could not delete link.`,n.disabled=!1}))}),Ye.addEventListener(`change`,e=>{let t=e.target.closest(`input[type="checkbox"], select, input[data-setting-text], textarea[data-setting-textarea]`);t&&Sr(t)}),Ye.addEventListener(`submit`,async e=>{e.preventDefault();let t=Ye.querySelector(`button[type="submit"]`),n=Ye.querySelectorAll(`input[type="checkbox"][name], select[name], input[data-setting-text][name], textarea[data-setting-textarea][name]`),r={};n.forEach(e=>{let t=e.name;t&&(r[t]=e.type===`checkbox`?e.checked:e.value)}),t.disabled=!0,t.textContent=`saving...`;try{S.textContent=`saving settings...`;let e=await fetch(`/api/config`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(r)});if(!e.ok)throw Error(`Config update failed`);K(await e.json(),`settings saved.`)}catch{S.textContent=`could not save settings.`,S.classList.remove(`is-empty`)}finally{t.disabled=!1,t.textContent=`save settings`}}),tt.addEventListener(`input`,()=>{it.disabled=!tt.value.trim()}),rt.addEventListener(`click`,wr),it.addEventListener(`click`,Tr),ot.addEventListener(`click`,Cr),bt.addEventListener(`click`,kr);function Ua(){if(window.location.hash===`#prepped-roles`){ha();return}ga({clearHash:!1})}window.addEventListener(`popstate`,Ua),Dr().finally(Or),window.location.hash===`#prepped-roles`&&Ua(),kn(!0),ni({applyDefaultCollapsed:!0}).catch(()=>{bn(null,`could not load resume.`),Sn([],`could not load cover letter examples.`),On()}),Qr().then(()=>{$r()}).catch(()=>{x.textContent=`could not load scan status`});