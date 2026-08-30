import{t as e}from"./preload-helper-Czpn1I53.js";var{sankey:t,sankeyLinkHorizontal:n}=await e(async()=>{let{sankey:e,sankeyLinkHorizontal:t}=await import(`/assets/d3-sankey.js`);return{sankey:e,sankeyLinkHorizontal:t}},[]),r=document.querySelector(`#stats`),i=document.querySelector(`#status-list`),a=document.querySelector(`#search-toggle`),o=document.querySelector(`#search-dialog`),s=document.querySelector(`#search-backdrop`),c=document.querySelector(`#search-form`),l=document.querySelector(`#search-input`),u=document.querySelector(`#close-search`),ee=document.querySelector(`#materials-panel`),te=document.querySelector(`#materials-toggle`),ne=document.querySelector(`#materials-body`),d=document.querySelector(`#materials-summary`),re=document.querySelector(`#materials-required-warning`),f=document.querySelector(`#resume-meta`),p=document.querySelector(`#resume-upload`),m=document.querySelector(`#resume-upload-button`),ie=document.querySelector(`#resume-resource-meta`),ae=document.querySelector(`#resume-resource-upload`),oe=document.querySelector(`#resume-resource-upload-button`),se=document.querySelector(`#resume-resource-list`),ce=document.querySelector(`#cover-letter-meta`),le=document.querySelector(`#cover-letter-upload`),ue=document.querySelector(`#cover-letter-upload-button`),de=document.querySelector(`#cover-letter-list`),fe=document.querySelector(`#experience-note-meta`),pe=document.querySelector(`#experience-note-upload`),me=document.querySelector(`#experience-note-upload-button`),he=document.querySelector(`#experience-note-list`);document.querySelector(`#material-index-button`);var ge=document.querySelector(`#material-index-warning`),_e=document.querySelector(`#material-index-status`),ve=document.querySelector(`#review-discovered`),h=document.querySelector(`#review-view`),ye=document.querySelector(`#review-heading`),be=document.querySelector(`#review-progress`),xe=document.querySelector(`#review-card`),Se=document.querySelector(`#close-review`),g=document.querySelector(`#prep-view`),Ce=document.querySelector(`#prep-heading`),we=document.querySelector(`#prep-progress`),_=document.querySelector(`#prep-card`),Te=document.querySelector(`#close-prep`),Ee=document.querySelector(`#prepped-roles`),De=document.querySelector(`#prepped-view`),Oe=document.querySelector(`#close-prepped`),ke=document.querySelector(`#prepped-summary`),Ae=document.querySelector(`#regenerate-all-cover-letters`),je=document.querySelector(`#prepped-bulk-status`),Me=document.querySelector(`#prepped-list`),v=document.querySelector(`#prepped-detail`),y=document.querySelector(`#scan-all-button`),Ne=document.querySelector(`#manage-companies-button`),b=document.querySelector(`#scan-status-bar`),Pe=document.querySelector(`#scan-status-text`),Fe=document.querySelector(`#scan-last-time`),Ie=document.querySelector(`#scan-failures-open`),Le=document.querySelector(`#scan-failures-dialog`),Re=document.querySelector(`#scan-failures-backdrop`),ze=document.querySelector(`#scan-failures-close`),Be=document.querySelector(`#scan-failures-list`),Ve=document.querySelector(`#toggle-all`),He=document.querySelector(`#collapse-empty`),Ue=document.querySelector(`#toolbar-summary`),We=document.querySelector(`#settings-open`),Ge=document.querySelector(`#settings-view`),Ke=document.querySelector(`#settings-close`),x=document.querySelector(`#settings-status`),S=document.querySelector(`#settings-form`),qe=document.querySelector(`#settings-profile-options`),Je=document.querySelector(`#settings-profile-extract`),Ye=document.querySelector(`#settings-autoprep-options`),Xe=document.querySelector(`#settings-options`),Ze=document.querySelector(`#central-store-summary`),Qe=document.querySelector(`#central-store-sync-summary`),$e=document.querySelector(`#central-api-url-input`),et=document.querySelector(`#central-passkey-input`),tt=document.querySelector(`#central-save-button`),nt=document.querySelector(`#central-sync-button`),rt=document.querySelector(`#recommendation-history-summary`),it=document.querySelector(`#clear-recommendation-history`),at=document.querySelector(`#metrics-open-button`),ot=document.querySelector(`#metrics-view`),st=document.querySelector(`#metrics-close`),ct=document.querySelector(`#metrics-status`),lt=document.querySelector(`#metrics-overview`),ut=document.querySelector(`#metrics-sections`),dt=document.querySelector(`#metrics-scan-list`),ft=document.querySelector(`#sankey-open-button`),pt=document.querySelector(`#sankey-view`),mt=document.querySelector(`#sankey-close`),ht=document.querySelector(`#sankey-status`),gt=document.querySelector(`#sankey-canvas`),_t=document.querySelector(`#sankey-path-list`),vt=document.querySelector(`#app-update-button`),yt=document.querySelector(`#companies-view`),bt=document.querySelector(`#companies-close`),C=document.querySelector(`#companies-status`),xt=document.querySelector(`#company-create-form`),w=document.querySelector(`#companies-list`),St=document.querySelector(`#role-add-form`),Ct=document.querySelector(`#role-url-input`),wt=document.querySelector(`#role-company-input`),Tt=document.querySelector(`#role-company-options`),Et=document.querySelector(`#role-add-status`),Dt=3,Ot=1200,kt=new Set([`applied`,`OA`,`interview`,`rejected`,`offer`]),At=new Map([[`discovered`,`#4f6472`],[`interested`,`#00897b`],[`disinterested`,`#626970`],[`applied`,`#2257ad`],[`oa`,`#b36b00`],[`interview`,`#5f2bd8`],[`rejected`,`#b93d2d`],[`offer`,`#137347`],[`closed`,`#53606b`],[`archived`,`#765b4a`]]),jt=/^(?:about (?:the )?(?:role|team|job)|about this role|job description|job responsibilities|minimum qualifications|preferred qualifications|qualifications|requirements|responsibilities|what to expect|what (?:you'll|you’ll|you will) (?:bring|do)|what'?s in it for you|who you are|your objectives|your skills & talents):?$/i,Mt=!0,T=null,Nt=null,E=[],D=[],O=[],Pt=null,k=[],A=[],j=new Map,Ft=new Map,M=new Map,It=new Map,N=new Map,Lt=new Map,Rt=new Map,zt=new Map,P=[],F=null,Bt=null,Vt=!1,I=``,L=null,Ht=new Set,Ut=new Set,Wt=new Map,R=new Set,Gt=new Set,z=new Map,Kt=new Map,qt=new Set,Jt=new Set,B=new Set,Yt=new Set,Xt=new Set,Zt=new Set,V=new Map,H=new Map,Qt=new Map,$t=new Map,en=new Set,tn=!1,nn=0,rn=null,an=!1,on=null,sn=null,cn=null,ln=null,U=null,un=[],dn=new Map;function fn(){return T?.query?.trim()??``}function pn(){let e=!!fn();a.classList.toggle(`search-active`,e),a.setAttribute(`aria-label`,e?`clear search`:`search jobs`)}function mn(){l.value=fn(),o.hidden=!1,c.hidden=!1,l.focus(),l.select()}function hn(){o.hidden=!0,c.hidden=!0,a.focus()}function gn(e){return e?new Intl.DateTimeFormat(void 0,{month:`short`,day:`numeric`,hour:`numeric`,minute:`2-digit`}).format(new Date(e)).toLocaleLowerCase():``}function W(e){return e?new Intl.DateTimeFormat(void 0,{month:`short`,day:`numeric`,hour:`numeric`,minute:`2-digit`}).format(new Date(e)).replace(`, `,` `).toLocaleLowerCase():``}function G(e){return String(e??``).replaceAll(`&`,`&amp;`).replaceAll(`<`,`&lt;`).replaceAll(`>`,`&gt;`).replaceAll(`"`,`&quot;`).replaceAll(`'`,`&#039;`)}function K(e){return String(e??``).toLocaleLowerCase()}function q(e){return G(K(e))}function _n(e){try{let t=new URL(String(e||``));return[`http:`,`https:`].includes(t.protocol)?t.href:``}catch{return``}}function vn(e){return e}function yn(e=_){e.querySelectorAll(`[data-prep-resume-latex], [data-prep-cover-letter-latex]`).forEach(vn)}function bn(){return`
    <svg class="role-link-icon" viewBox="0 0 24 24" aria-hidden="true">
      <path d="M7 17 17 7"></path>
      <path d="M8 7h9v9"></path>
    </svg>
  `}function xn(){return`
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M12 5v14"></path>
      <path d="M5 12h14"></path>
    </svg>
  `}function Sn(){return`
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M3 6h18"></path>
      <path d="M8 6V4h8v2"></path>
      <path d="m19 6-1 14H6L5 6"></path>
      <path d="M10 11v5"></path>
      <path d="M14 11v5"></path>
    </svg>
  `}function Cn(e,t,n){let r=`<span class="role-title-text">${q(e)}</span>`;return t?`<a class="${n}" href="${G(t)}" target="_blank" rel="noreferrer">${r}${bn()}</a>`:`<span class="${n}">${r}</span>`}function wn(e){r.innerHTML=[[`companies`,e.companies_total],[`jobs`,e.jobs_total],[`applications`,e.applications_total]].map(([e,t])=>`<dl class="stat"><dt>${q(e)}</dt><dd>${t}</dd></dl>`).join(``)}function Tn(e=T){if(!e){Ue.innerHTML=``;return}let t=t=>e.statuses.find(e=>e.key===t)?.count??0;Ue.innerHTML=[[`discovered`,t(`discovered`)],[`interested`,t(`interested`)],[`applied`,e.stats?.applications_total??0],[`total`,e.stats?.jobs_total??0]].map(([e,t])=>`
        <dl>
          <dt>${q(e)}</dt>
          <dd>${t}</dd>
        </dl>
      `).join(``)}function En(e,t=``){if(Nt=e,m.textContent=e?`replace`:`upload`,t){f.textContent=t;return}if(!e){f.textContent=`no resume uploaded`;return}let n=W(e.updated_at),r=Fn(e.content_bytes);f.textContent=[K(e.filename),r,n].filter(Boolean).join(` | `)}function Dn(e,t,n,{binary:r=!1}={}){let i=r?e.filename:e.id;return`
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
    </li>`}function On(e,t=``){D=Array.isArray(e)?e:[],ue.textContent=D.length>0?`add`:`upload`,ce.textContent=t||(D.length===0?`no examples uploaded`:`${D.length} ${D.length===1?`example`:`examples`} stored`),de.innerHTML=D.map(e=>Dn(e,`cover-letter-examples`,Fn(e.content_bytes))).join(``)}function kn(e,t=``){O=Array.isArray(e)?e:[],me.textContent=O.length>0?`add`:`upload`,fe.textContent=t||(O.length===0?`no notes uploaded`:`${O.length} ${O.length===1?`note`:`notes`} stored`),he.innerHTML=O.map(e=>Dn(e,`experience-notes`,Fn(e.content_bytes))).join(``)}function An(e,t=``){Pt=e??null;let n=Pt?.status??`missing`,r=n!==`ready`;if(O.length,ge.hidden=!r,ge.textContent=t||Pt?.warning||``,t)_e.textContent=t;else if(n===`ready`){let e=Number(Pt?.document_count??0),t=Number(Pt?.skipped_source_count??0),n=W(Pt?.generated_at);_e.innerHTML=[`${e} indexed ${e===1?`page`:`pages`}`,t?`${t} unreadable upload skipped`:``,n].filter(Boolean).map(e=>`<button type="button" class="material-index-link" data-open-material-index title="Reveal the application material index in Finder">${q(e)}</button>`).join(`<span aria-hidden="true"> | </span>`)}else _e.textContent=n===`stale`?`index out of date`:`not indexed`}function jn(e,t=``){E=Array.isArray(e)?e:[],oe.textContent=E.length>0?`add`:`upload`,ie.textContent=t||(E.length===0?`no resources uploaded`:`${E.length} ${E.length===1?`resource`:`resources`} stored`),se.innerHTML=E.map(e=>Dn(e,`resume-resources`,Fn(e.bytes),{binary:!0})).join(``)}function Mn(e,t={}){nn+=1,document.querySelectorAll(`[data-preview-blob-url]`).forEach(e=>{URL.revokeObjectURL(e.dataset.previewBlobUrl)}),En(e?.master_resume??null),jn(e?.resume_resources??[]),On(e?.cover_letter_examples??[]),kn(e?.experience_notes??[]),An(e?.material_index??null),Nn(e?.ui),(!tn||t.applyDefaultCollapsed)&&(Pn(!!e?.ui?.default_collapsed),tn=!0)}function Nn(e=null){let t=Nt?`resume ready`:`no resume`,n=E.length===0?`no resources`:`${E.length} ${E.length===1?`resource`:`resources`}`,r=D.length,i=r===0?`no cover letters`:`${r} cover ${r===1?`letter`:`letters`}`,a=O.length,o=a===0?`no notes`:`${a} experience ${a===1?`note`:`notes`}`;re.hidden=!(typeof e?.has_missing_required_materials==`boolean`?e.has_missing_required_materials:!Nt||r===0||a===0),d.textContent=`${t} | ${n} | ${i} | ${o}`}function Pn(e){ee.classList.toggle(`collapsed`,e),te.setAttribute(`aria-expanded`,String(!e)),te.querySelector(`.materials-chevron`).textContent=e?`>`:`v`,ne.hidden=e}function Fn(e){return Number.isFinite(e)?e<1024?`${e} b`:`${Math.round(e/1024)} kb`:``}async function In(e){let t=await fetch(e,{cache:`no-store`});if(!t.ok)throw Error(`Preview unavailable`);let n=await t.arrayBuffer();if(new TextDecoder(`ascii`).decode(n.slice(0,5))!==`%PDF-`)throw Error(`The selected file is not a readable PDF.`);return URL.createObjectURL(new Blob([n],{type:`application/pdf`}))}async function Ln(e){let t=e.closest(`.material-source-item`)?.querySelector(`[data-material-preview-body]`);if(!t)return;if(t.dataset.loaded===`true`){t.hidden=!t.hidden,e.textContent=t.hidden?`preview`:`hide`;return}e.disabled=!0,e.textContent=`loading...`;let n=e.dataset.materialView,r=e.dataset.materialId,i=nn,a=`/api/${encodeURIComponent(n)}/${encodeURIComponent(r)}`;try{if(e.dataset.materialBinary===`true`){let e=await In(a);if(!t.isConnected||nn!==i){URL.revokeObjectURL(e);return}t.dataset.previewBlobUrl=e,t.innerHTML=`<iframe title="${q(r)} preview"></iframe>`,t.querySelector(`iframe`).src=e}else{let e=await fetch(a);if(!e.ok)throw Error(`Preview unavailable`);let n=await e.json(),r=document.createElement(`pre`);r.textContent=n.content||`This source is empty.`,t.replaceChildren(r)}t.dataset.loaded=`true`,t.hidden=!1,e.textContent=`hide`}catch(n){t.textContent=n instanceof Error?n.message:`Preview unavailable`,t.hidden=!1,e.textContent=`preview`}finally{e.disabled=!1}}async function Rn(e){let t=e.dataset.materialRemove,n=e.dataset.materialId;if(e.dataset.confirmRemove!==`true`){e.dataset.confirmRemove=`true`,e.textContent=`confirm remove`,e.classList.add(`danger`),window.setTimeout(()=>{!e.isConnected||e.disabled||(delete e.dataset.confirmRemove,e.textContent=`remove`,e.classList.remove(`danger`))},6e3);return}e.disabled=!0,e.textContent=`removing...`;try{let e=await fetch(`/api/${encodeURIComponent(t)}/${encodeURIComponent(n)}`,{method:`DELETE`}),r=await e.json();if(!e.ok)throw Error(r.error||`Remove failed`);Mn(r)}catch(t){e.disabled=!1,delete e.dataset.confirmRemove,e.classList.remove(`danger`),e.textContent=`remove`,window.alert(t instanceof Error?t.message:`Remove failed`)}}function zn(e){i.innerHTML=e.map(e=>{let t=e.jobs.map(t=>Bn(t,e.key)).join(``);return`
        <section class="status-pane ${e.count===0?`empty`:``} ${Mt?`hidden-empty`:``}" id="status-${G(e.key)}" data-bucket="${G(e.key)}">
          <button class="pane-toggle" type="button" aria-expanded="false">
            <span class="chevron">></span>
            <span class="pane-title">${q(e.label)}</span>
            <span class="count">${e.count}</span>
          </button>
          <div class="pane-body" hidden>
            ${t?`<div class="jobs">${t}</div>`:`<p class="empty-copy">${e.key===`archived`&&e.count>0?`archived role details are hidden.`:`no jobs in this status.`}</p>`}
          </div>
        </section>
      `}).join(``)}function Bn(e,t){return`
    <details class="job" data-role-id="${G(e.id)}">
      <summary class="job-summary">
        <span class="job-chevron">></span>
        <span class="job-identity">
          <span class="job-company">[${q(e.company_name)}]</span>
          ${Cn(e.title,e.role_url,`job-title`)}
          ${t===`interested`&&e.prep_started?Un():``}
          ${t===`closed`&&e.updated_in_latest_scan?Vn():``}
          ${[`discovered`,`interested`].includes(t)&&e.missing_from_latest_scan?Hn():``}
        </span>
      </summary>
      <div class="job-detail">
        ${t===`discovered`?Wn(e):``}
        ${t===`interested`?Gn(e):``}
        ${t===`disinterested`?Kn(e):``}
        ${t===`applied`?qn(e):``}
        ${t===`OA`?Jn(e):``}
        ${t===`interview`?Yn(e):``}
        ${t===`closed`?Xn(e):``}
        <dl>
          ${e.location?`<div>
                  <dt>location</dt>
                  <dd>${q(e.location)}</dd>
                </div>`:``}
          <div>
            <dt>updated</dt>
            <dd>${gn(e.updated_at)}</dd>
          </div>
        </dl>
      </div>
    </details>
  `}function Vn(){return`<span class="latest-scan-dot" title="updated in latest scan" aria-label="updated in latest scan"></span>`}function Hn(){return`<span class="missing-latest-scan-dot" title="not seen in latest scan" aria-label="not seen in latest scan"></span>`}function Un(){return`<span class="prep-started-dot" title="application materials started" aria-label="application materials started"></span>`}function Wn(e){return`
    <div class="job-actions job-actions-nowrap" aria-label="discovered role actions">
      <button class="job-action success" type="button" data-review-role-id="${e.id}">view</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="interested">interested</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="disinterested">disinterested</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="closed">closed</button>
    </div>
  `}function Gn(e){return`
    <div class="job-actions" aria-label="interested role actions">
      <button class="job-action success" type="button" data-prep-role-id="${e.id}">prep</button>
      <button class="job-action success" type="button" data-autoprep-role-id="${e.id}">${e.autoprep_started?`view / regenerate prep`:`autoprep`}</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="applied">applied</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="disinterested">disinterested</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="closed">closed</button>
    </div>
    ${e.autoprep_started?`<p class="job-prepped-note">already prepped</p>`:``}
  `}function Kn(e){return`
    <div class="job-actions" aria-label="disinterested role actions">
      <button class="job-action success" type="button" data-role-id="${e.id}" data-status="interested">interested</button>
    </div>
  `}function qn(e){return`
    <div class="job-actions job-actions-nowrap" aria-label="applied role actions">
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="OA">oa</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="interview">interview</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="rejected">rejected</button>
    </div>
  `}function Jn(e){return`
    <div class="job-actions job-actions-nowrap" aria-label="oa role actions">
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="interview">interview</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="disinterested">disinterested</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="rejected">rejected</button>
    </div>
  `}function Yn(e){return`
    <div class="job-actions" aria-label="interview role actions">
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="rejected">rejected</button>
      <button class="job-action success" type="button" data-role-id="${e.id}" data-status="offer">offer</button>
    </div>
  `}function Xn(e){return`
    <div class="job-actions" aria-label="closed role actions">
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="interested">interested</button>
    </div>
  `}function Zn(e){T=e,l.value=e.query,pn(),wn(e.stats),Tn(e),zn(e.statuses),io(),Ei(e.statuses)}function Qn(e){on=e??null;let t=!!e?.scanning,n=t&&!!e?.cancel_requested,r=Number(e?.completed_companies??0),i=Number(e?.total_companies??0),a=Number(e?.failed_companies??0),o=typeof e?.error==`string`?e.error.trim():``,s=Array.isArray(e?.failures)?e.failures:[];y.disabled=n,y.textContent=t?n?`cancelling...`:`cancel scan`:`scan roles`,y.classList.toggle(`danger`,t&&!n),b.hidden=!t&&!o&&s.length===0,b.classList.toggle(`scanning`,t),b.classList.toggle(`scan-error`,!t&&!!o||s.length>0),Pe.textContent=n?`cancelling scan...`:t?`scanning roles${i>0?` ${r}/${i}`:``}${a>0?`, ${a} failed`:``}`:s.length>0?`${s.length} recent scan ${s.length===1?`failure`:`failures`}`:o?`last scan error: ${o}`:`scan idle`,Ie&&Be&&(Ie.hidden=s.length===0,Be.innerHTML=s.slice(0,5).map(e=>{let t=e?.company_name||`unknown company`,n=e?.error||`scan failed`;return`
          <p>
            <span>${q(t)}</span>
            <span>${G(n)}</span>
          </p>
        `}).join(``),s.length===0&&er());let c=e?.last_scan_at;Fe.textContent=c?`last scan: ${W(c)}`:`last scan: never`,an&&!t&&ui(fn()).catch(()=>{}),an=t}function $n(){Ie.hidden||(Le.hidden=!1,ze.focus())}function er(){Le.hidden=!0}function J(e,t=``){sn=e;let n=Array.isArray(e?.settings)?e.settings:[],r=n.filter(e=>e.key?.startsWith(`applicant_`)),i=n.filter(e=>e.key?.startsWith(`autoprep_`)||e.key===`application_generation_backend`),a=n.filter(e=>!e.key?.startsWith(`applicant_`)&&!e.key?.startsWith(`autoprep_`)&&e.key!==`application_generation_backend`),o=e?.central??{};x.textContent=t,x.classList.toggle(`is-empty`,!t);let s=Number(e?.recommendation_history_count??0);rt.textContent=s>0?`${s} saved ${s===1?`feedback decision`:`feedback decisions`}`:`no saved resume feedback decisions`,it.disabled=s===0,rr(o),qe.innerHTML=r.map(e=>ir(e)).join(``),Ye.innerHTML=i.map(t=>ir(tr(t,e))).join(``)+nr(e),Xe.innerHTML=a.map(e=>ir(e)).join(``),lr(!1)}function tr(e,t){if(e.key!==`application_generation_backend`||!Array.isArray(e.options))return e;let n=t?.application_generation_runtimes??{};return{...e,options:e.options.map(e=>{let t=n?.[e.value];return!t||e.available===!1||e.disabled===!0?e:{...e,available:t.available??t.detected??!0,reason:t.reason}})}}function nr(e){let t=e?.application_generation_runtimes??e?.runtime_availability??e?.runtimes??{},n=[[`hermes`,t?.hermes??t?.Hermes],[`openclaw`,t?.openclaw??t?.OpenClaw]];return n.some(([,e])=>e&&typeof e==`object`)?`<div class="application-runtime-statuses" aria-label="application generation runtime detection">
    ${n.map(([e,t])=>{let n=t?.available??t?.detected??!1,r=t?.reason??t?.message??(n?`Runtime detected`:`Runtime unavailable`);return`<div class="application-runtime-status" data-application-runtime="${G(e)}">
        <span><strong>${q(e===`openclaw`?`OpenClaw`:`Hermes`)}</strong> ${n?`available`:`unavailable`}</span>
        <small>${q(r)}</small>
        <button type="button" data-application-runtime-test="${G(e)}" ${n?``:`disabled`}>Test connection</button>
        <small data-application-runtime-test-status="${G(e)}" aria-live="polite"></small>
      </div>`}).join(``)}
  </div>`:``}function rr(e){let t=e?.api_url??``;$e.value=t,et.value=``;let n=e?.passkey_configured?`passkey saved`:`no passkey saved`;Ze.textContent=t?`${K(t)} | ${n}`:`no api url | ${n}`,Qe.textContent=`${Number(e?.companies_linked??0)} linked | ${Number(e?.companies_unlinked??0)} unlinked | ${Number(e?.companies_needs_review??0)} review | ${Number(e?.companies_failed??0)} failed`,nt.disabled=!t}function ir(e){if(e.control===`textarea`&&e.editable!==!1)return or(e);if(e.control===`text`&&e.editable!==!1)return ar(e);if(e.control===`select`&&e.editable!==!1)return sr(e);if(e.control!==`toggle`||e.editable===!1)return cr(e);let t=e.value?`checked`:``,n=e.default?`on by default`:`off by default`;return`
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
  `}function ar(e){let t=e.default?`default: ${K(e.default)}`:`optional`,n=e.input_type??`text`,r=e.autocomplete??`name`;return`
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
  `}function or(e){return`
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
  `}function sr(e){let t=Array.isArray(e.options)?e.options:[],n=`default: ${K(e.default)}`,r=e.key===`application_generation_backend`,i=r?`setting-select setting-select-application-backend`:`setting-select`;return`
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
  `}function cr(e){let t=e.default?`on by default`:`off by default`,n=e.value?`automatic`:`off`;return`
    <div class="setting-option setting-option-readonly">
      <span class="setting-copy">
        <span class="setting-label">${q(e.label)}</span>
        <span class="setting-description">${q(e.description)}</span>
        <span class="setting-default">${q(t)}</span>
      </span>
      <span class="setting-badge">${q(n)}</span>
    </div>
  `}function lr(e){S.querySelectorAll(`input, select, textarea`).forEach(t=>{t.disabled=e}),tt.disabled=e,nt.disabled=e||!$e.value.trim(),Je.disabled=e,vt.disabled=e}async function ur(){Ge.hidden=!1,document.body.classList.add(`settings-open`),Ke.focus(),sn?J(sn):(x.textContent=`loading settings...`,x.classList.remove(`is-empty`),Xe.innerHTML=``);try{await fr()}catch{x.textContent=`could not load settings.`}}function dr(){Ge.hidden=!0,document.body.classList.remove(`settings-open`),We.focus()}async function fr(){let e=await fetch(`/api/config`);if(!e.ok)throw Error(`Config request failed`);J(await e.json())}async function pr(){Je.disabled=!0,Je.textContent=`filling blank fields...`,x.textContent=`sending the master resume to the selected AI provider...`,x.classList.remove(`is-empty`);try{let e=await fetch(`/api/config/extract-profile`,{method:`POST`});if(!e.ok)throw Error(`Profile extraction request failed`);let t=await e.json(),n=Array.isArray(t.populated)?t.populated:[];J(t.config,n.length?`filled ${n.length} blank profile ${n.length===1?`field`:`fields`}.`:`no blank profile fields could be filled.`)}catch{x.textContent=`could not fill profile fields from the resume.`}finally{Je.disabled=!1,Je.textContent=`fill blank fields`}}function mr(e){let t=e?.value;return t==null?`n/a`:e?.kind===`ratio`?Number(t).toLocaleString(void 0,{maximumFractionDigits:2,minimumFractionDigits:0}):typeof t==`number`?t.toLocaleString():K(t)}function hr(e,t=`metric-card`){return`
    <article class="${t}">
      <span>${q(e?.label)}</span>
      <strong>${G(mr(e))}</strong>
    </article>
  `}function gr(e,t=``){cn=e,ct.textContent=t||(e?.updated_at?`updated ${W(e.updated_at)}`:``),ct.classList.toggle(`is-empty`,!ct.textContent);let n=Array.isArray(e?.overview)?e.overview:[],r=Array.isArray(e?.sections)?e.sections:[],i=Array.isArray(e?.recent_scans)?e.recent_scans:[];lt.innerHTML=n.map(e=>hr(e)).join(``),ut.innerHTML=r.map(_r).join(``),dt.innerHTML=i.length?i.map(vr).join(``):`<p class="empty-copy">no scan runs recorded.</p>`}function _r(e){let t=Array.isArray(e?.metrics)?e.metrics:[];return`
    <section class="metrics-section">
      <div class="metrics-section-heading">
        <h3>${q(e?.title)}</h3>
      </div>
      <div class="metrics-section-grid">
        ${t.map(e=>hr(e,`metric-card metric-card-compact`)).join(``)}
      </div>
    </section>
  `}function vr(e){let t=e?.scan_status??`unknown`,n=e?.started_at?W(e.started_at):`not started`,r=e?.finished_at?W(e.finished_at):`not finished`,i=e?.error?`<span>${q(e.error)}</span>`:``;return`
    <article class="metrics-scan-row">
      <div>
        <strong>${q(e?.company_name??`unknown company`)}</strong>
        <span>${q(n)} -> ${q(r)}</span>
        ${i}
      </div>
      <span class="metrics-status-pill">${q(t)}</span>
    </article>
  `}async function yr(){ot.hidden=!1,document.body.classList.add(`metrics-open`),st.focus(),cn?gr(cn):(ct.textContent=`loading metrics...`,ct.classList.remove(`is-empty`),lt.innerHTML=``,ut.innerHTML=``,dt.innerHTML=``);try{await xr()}catch{ct.textContent=`could not load metrics.`}}function br(){ot.hidden=!0,document.body.classList.remove(`metrics-open`),at.focus()}async function xr(){let e=await fetch(`/api/metrics`);if(!e.ok)throw Error(`Metrics request failed`);gr(await e.json())}function Sr(e,t=``){ln=e;let n=Number(e?.role_count??0),r=Array.isArray(e?.links)?e.links:[],i=Array.isArray(e?.paths)?e.paths:[];ht.textContent=t||(e?.updated_at?`${n.toLocaleString()} roles | updated ${W(e.updated_at)}`:``),ht.classList.toggle(`is-empty`,!ht.textContent),gt.innerHTML=r.length?Cr(e):`<p class="empty-copy">no role transitions recorded yet.</p>`,_t.innerHTML=i.length?i.map(Dr).join(``):`<p class="empty-copy">no role paths recorded yet.</p>`}function Cr(e){let t=Array.isArray(e?.nodes)?e.nodes:[],n=Array.isArray(e?.links)?e.links:[],r=Er(t,n),i=r.nodes,a=r.links,o=(r.flowLinks??n).map(e=>{let t=i.get(e.source),n=i.get(e.target),r=a.get(e);if(!t||!n||!r)return``;let o=r.width,s=n.x<t.x,c=wr(e.target),l=r.priority?`0.42`:s?`0.28`:`0.34`,u=r.path??Tr({isBacktrack:s,sourceX:t.x+t.width,sourceY:r.sourceY,targetX:n.x,targetY:r.targetY,width:o});return`
        <path class="${[`sankey-link`,s?`sankey-link-backtrack`:``,r.priority?`sankey-link-priority`:``].filter(Boolean).join(` `)}" d="${u}" fill="${r.path?`none`:c}" fill-opacity="${l}" stroke="${c}" style="stroke-width: ${r.path?o:1}px">
          <title>${q(t.label)} to ${q(n.label)}: ${Number(e.value??0).toLocaleString()}</title>
        </path>
      `}).join(``),s=Array.from(i.values()).map(e=>{let t=Number(e.history_count??e.current_count??0),n=Number(e.value??t),i=n>0?n.toLocaleString():`0`,a=e.x>r.width-180,o=a?e.x-8:e.x+e.width+8,s=Math.max(24,e.y-e.height/2-16),c=a?`end`:`start`,l=wr(e.id);return`
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
  `}function wr(e){return At.get(String(e).toLowerCase())??`#4f6472`}function Tr({isBacktrack:e,sourceX:t,sourceY:n,targetX:r,targetY:i,width:a}){let o=a/2,s=n-o,c=n+o,l=i-o,u=i+o;if(e){let e=Math.max(80,Math.abs(t-r)*.42);return[`M ${t} ${s}`,`C ${t-e} ${s}, ${r+e} ${l}, ${r} ${l}`,`L ${r} ${u}`,`C ${r+e} ${u}, ${t-e} ${c}, ${t} ${c}`,`Z`].join(` `)}let ee=Math.max(46,(r-t)*.48);return[`M ${t} ${s}`,`C ${t+ee} ${s}, ${r-ee} ${l}, ${r} ${l}`,`L ${r} ${u}`,`C ${r-ee} ${u}, ${t+ee} ${c}, ${t} ${c}`,`Z`].join(` `)}function Er(e,r){let i=new Map([[`discovered`,0],[`interested`,1],[`disinterested`,2],[`applied`,2],[`oa`,3],[`interview`,3],[`rejected`,4],[`closed`,4],[`archived`,4]]),a=new Map,o=new Map;r.forEach(e=>{a.set(e.target,(a.get(e.target)??0)+Number(e.value??0)),o.set(e.source,(o.get(e.source)??0)+Number(e.value??0))});let s=e.filter(e=>Number(e?.history_count??e?.current_count??0)>0||a.has(e.id)||o.has(e.id)),c=new Set(s.map(e=>e.id)),l=r.filter(e=>c.has(e.source)&&c.has(e.target)&&Number(e.value??0)>0),u=e=>i.get(String(e).toLowerCase())??0,ee=l.filter(e=>u(e.target)>=u(e.source)),te=l.filter(e=>u(e.target)<u(e.source)),ne={nodes:s.map(e=>({...e,fixedValue:Math.max(0,Number(e?.history_count??e?.current_count??0))})),links:ee.map(e=>({...e}))},d=t().nodeId(e=>e.id).nodeWidth(26).nodePadding(44).nodeAlign((e,t)=>Math.min(t-1,u(e.id))).extent([[92,88],[1014,634]]).iterations(32)(ne),re=new Map;d.nodes.forEach(e=>{re.set(e.id,{...e,x:e.x0,y:e.y0+(e.y1-e.y0)/2,width:e.x1-e.x0,height:Math.max(1.5,e.y1-e.y0),value:Number(e.fixedValue??e.value??0)})});let f=new Map,p=[],m=n();d.links.forEach(e=>{let t={source:e.source.id,target:e.target.id,value:e.value};p.push(t),f.set(t,{path:m(e),width:Math.max(1.5,e.width),sourceY:e.y0,targetY:e.y1,priority:Number(e.value??0)>=20})});let ie=Math.max(.6,...d.links.map(e=>Number(e.width??0)/Math.max(1,Number(e.value??0))));return te.forEach(e=>{let t=re.get(e.source),n=re.get(e.target);if(!t||!n)return;let r=Math.max(1.5,Number(e.value??0)*ie),i={...e};p.push(i),f.set(i,{width:r,sourceY:t.y+t.height/2-r/2,targetY:n.y+n.height/2-r/2,priority:!1})}),p.sort((e,t)=>Number(e.value??0)-Number(t.value??0)),{flowLinks:p,height:720,links:f,nodes:re,width:1120}}function Dr(e){let t=Array.isArray(e?.path)?e.path:[];return`
    <article class="sankey-path-row">
      <div>
        <strong>${q(e?.company_name??`unknown company`)} / ${q(e?.title??`untitled role`)}</strong>
        <span>${t.map(e=>q(e)).join(` -> `)}</span>
      </div>
      <span class="metrics-status-pill">${Number(e?.loops_collapsed??0).toLocaleString()} loops</span>
    </article>
  `}async function Or(){Ge.hidden=!0,document.body.classList.remove(`settings-open`),pt.hidden=!1,document.body.classList.add(`sankey-open`),mt.focus(),ln?Sr(ln):(ht.textContent=`loading role flow...`,ht.classList.remove(`is-empty`),gt.innerHTML=``,_t.innerHTML=``);try{await Ar()}catch{ht.textContent=`could not load role flow.`}}function kr(){pt.hidden=!0,document.body.classList.remove(`sankey-open`),We.focus()}async function Ar(){let e=await fetch(`/api/role-sankey`);if(!e.ok)throw Error(`Role sankey request failed`);Sr(await e.json())}async function jr(e){let t=e.name;if(!t)return;let n=e.type===`checkbox`?!e.checked:sn?.settings?.find(e=>e.key===t)?.value,r=e.type===`checkbox`?e.checked:e.value;lr(!0),x.textContent=`saving settings...`,x.classList.remove(`is-empty`);try{let e=await fetch(`/api/config`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({[t]:r})});if(!e.ok)throw Error(`Config update failed`);J(await e.json(),`settings saved.`)}catch{e.type===`checkbox`?e.checked=n:n!==void 0&&(e.value=n),x.textContent=`could not save settings.`,lr(!1)}}async function Mr(){it.disabled=!0,x.textContent=`clearing recommendation history...`,x.classList.remove(`is-empty`);try{let e=await fetch(`/api/recommendation-history/clear`,{method:`POST`});if(!e.ok)throw Error(`Recommendation history clear failed`);let t=await e.json();J(t.config,`cleared ${t.deleted_count} saved decisions.`)}catch{x.textContent=`could not clear recommendation history.`,it.disabled=!1}}async function Nr(){let e=$e.value.trim();if(!e){x.textContent=`central api url is required.`,x.classList.remove(`is-empty`);return}let t={central_api_url:e},n=et.value.trim();n&&(t.central_passkey=n),lr(!0),x.textContent=`saving central settings...`,x.classList.remove(`is-empty`);try{let e=await fetch(`/api/config`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(t)});if(!e.ok)throw Error(`Central settings update failed`);J(await e.json(),`central settings saved.`)}catch{x.textContent=`could not save central settings.`,lr(!1)}}async function Pr(){nt.disabled=!0,x.textContent=`syncing remote company ids...`,x.classList.remove(`is-empty`);try{let e=await fetch(`/api/central/resolve-companies`,{method:`POST`});if(!e.ok)throw Error(`Central company sync failed`);let t=await e.json(),n=t.result??{},r=t.pulled_companies,i=r?` remote: ${Number(r.created??0)} created, ${Number(r.linked??0)} linked, ${Number(r.existing??0)} existing.`:``;J(t.config,`company sync: ${Number(n.linked??0)} matched, ${Number(n.created??0)} created, ${Number(n.needs_review??0)} review, ${Number(n.failed??0)} failed.${i}`),t.companies&&(U=t.companies,zr(t.companies.companies))}catch{x.textContent=`could not sync companies.`,nt.disabled=!$e.value.trim()}}async function Fr(){let e=await fetch(`/api/central/resolve-companies`,{method:`POST`});if(!e.ok)throw Error(`Central company sync failed`);let t=await e.json();t.companies&&(U=t.companies,zr(t.companies.companies))}async function Ir(){let e=Fr().catch(()=>{});await Promise.all([ui().catch(()=>{i.innerHTML=`<p class="empty-copy">could not load jobs.</p>`}),qr().catch(()=>{Et.textContent=`could not load companies.`})]),await e}async function Lr(){if(window.confirm(`Update callumployed and restart the tracker?`)){lr(!0),vt.disabled=!0,x.textContent=`updating callumployed; tracker will restart shortly...`,x.classList.remove(`is-empty`);try{if(!(await fetch(`/api/app/update`,{method:`POST`})).ok)throw Error(`App update failed`);x.textContent=`update started. reconnect in a moment.`}catch{x.textContent=`could not start update.`,lr(!1)}}}function Rr(e,t=``){U=e;let n=Array.isArray(e?.companies)?e.companies:[];if(zr(n),C.textContent=t||`${n.length} ${n.length===1?`company`:`companies`} stored`,C.classList.toggle(`is-empty`,n.length===0&&!t),n.length===0){w.innerHTML=`<p class="empty-copy">no companies yet.</p>`;return}w.innerHTML=n.map(e=>Br(e)).join(``)}function zr(e){un=Array.isArray(e)?e:[],Tt.innerHTML=un.map(e=>`<option value="${G(e.name)}"></option>`).join(``)}function Br(e){let t=Array.isArray(e.career_pages)?e.career_pages:[],n=W(e.updated_at),r=Vr(e.prestige_tier),i=Number(e.scan_count??0),a=Number(e.discovered_role_count??0),o=i>0&&a===0?`<span class="company-discovery-status">Discovered 0 potential roles</span>`:``;return`
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
              ${Hr(e.prestige_tier)}
            </select>
          </label>
          <div>
            <span>browser wait</span>
            <strong>${Number(e.browser_extra_wait_ms??0)}ms</strong>
          </div>
        </div>
        <div class="company-links">
          ${t.length>0?t.map(e=>Ur(e)).join(``):`<p class="company-empty-links">no career links yet.</p>`}
        </div>
        <section class="company-link-panel" aria-label="add career link">
          <form class="company-link-form" data-company-link-form="${e.id}">
            <input name="label" type="text" placeholder="label" aria-label="career link label" />
            <input name="url" type="url" placeholder="https://..." aria-label="career link url" required />
            <button class="company-link-add" type="submit" aria-label="add career link" title="add career link">
              ${xn()}
            </button>
          </form>
        </section>
        <div class="company-danger-row">
          <button class="company-delete-button" type="button" data-delete-company="${e.id}">
            ${Sn()}
            <span>deactivate company</span>
          </button>
        </div>
      </div>
    </details>
  `}function Vr(e){let t=String(e??``);return[`0`,`1`,`2`,`3`,`4`].includes(t)?`company-tier-${t}`:`company-tier-unset`}function Hr(e){let t=String(e??``);return[``,`0`,`1`,`2`,`3`,`4`].map(e=>{let n=e?`tier ${e}`:`not set`,r=e===t?` selected`:``;return`<option value="${G(e)}"${r}>${q(n)}</option>`}).join(``)}function Ur(e){let t=e.label?q(e.label):`career page`,n=G(e.url);return`
    <div class="company-link-row" data-career-page-id="${e.id}">
      <a class="company-link-url" href="${n}" target="_blank" rel="noreferrer">
        <span class="company-link-label">${t}</span>
        <span class="company-link-text">${G(e.url)}</span>
      </a>
      <button class="company-link-delete" type="button" data-delete-career-page="${e.id}" aria-label="delete ${t} link" title="delete link">
        ${Sn()}
      </button>
    </div>
  `}async function Wr(){yt.hidden=!1,document.body.classList.add(`companies-open`),bt.focus(),U?Rr(U):(C.textContent=`loading companies...`,C.classList.remove(`is-empty`),w.innerHTML=``);try{await Kr()}catch{C.textContent=`could not load companies.`}}function Gr(){yt.hidden=!0,document.body.classList.remove(`companies-open`),Ne.focus()}async function Kr(e=``){let t=await fetch(`/api/companies`);if(!t.ok)throw Error(`Companies request failed`);Rr(await t.json(),e)}async function qr(){let e=await fetch(`/api/companies`);if(!e.ok)throw Error(`Companies request failed`);zr((await e.json()).companies)}async function Jr(e){let t=new FormData(e),n={name:String(t.get(`name`)??``),career_url:String(t.get(`career_url`)??``),notes:String(t.get(`notes`)??``)};C.textContent=`adding company...`;let r=await fetch(`/api/companies`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(n)});if(!r.ok)throw Error(`Company create failed`);e.reset(),Rr(await r.json(),`company added.`),ui(fn()).catch(()=>{})}async function Yr(e){let t=e.dataset.companyLinkForm;if(!t)return;let n=new FormData(e),r={label:String(n.get(`label`)??``),url:String(n.get(`url`)??``)};C.textContent=`adding link...`;let i=await fetch(`/api/companies/${encodeURIComponent(t)}/career-pages`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(r)});if(!i.ok)throw Error(`Career page create failed`);e.reset(),Rr(await i.json(),`link added.`)}async function Xr(e){C.textContent=`deleting link...`;let t=await fetch(`/api/company-career-pages/${encodeURIComponent(e)}`,{method:`DELETE`});if(!t.ok)throw Error(`Career page delete failed`);Rr(await t.json(),`link deleted.`)}async function Zr(e){C.textContent=`deactivating company...`;let t=await fetch(`/api/companies/${encodeURIComponent(e)}`,{method:`DELETE`});if(!t.ok)throw Error(`Company deactivate failed`);Rr(await t.json(),`company deactivated.`),ui(fn()).catch(()=>{})}function Qr(){let e=wt.value.trim().toLocaleLowerCase();return un.find(t=>t.name.toLocaleLowerCase()===e)}async function $r(e){let t=Qr();if(!t?.id){Et.textContent=`pick a saved company.`;return}let n=new FormData(e),r={company_id:t.id,role_url:String(n.get(`role_url`)??``)};Et.textContent=`adding role...`;let i=await fetch(`/api/roles`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(r)});if(!i.ok)throw Error(`Role create failed`);let a=await i.json();a.tracker?Zn(a.tracker):await ui(fn()),Ct.value=``;let o=a.role?.title?K(a.role.title):`role`;Et.textContent=a.scan_error?`${o} added; scan could not finish.`:`${o} added.`}function ei(e){return(Array.isArray(U?.companies)?U.companies:[]).find(t=>String(t.id)===String(e))}function ti(e){C.textContent=e,C.classList.remove(`is-empty`)}function ni(e){window.clearTimeout(dn.get(e)),dn.set(e,window.setTimeout(()=>{ri(e).catch(()=>{ti(`could not save company.`)})},700))}async function ri(e){let t=w.querySelector(`[data-company-id="${CSS.escape(String(e))}"]`);if(!t)return;let n=t.querySelector(`[data-company-notes="${CSS.escape(String(e))}"]`),r=t.querySelector(`[data-company-tier="${CSS.escape(String(e))}"]`),i=ei(e),a={notes:n?.value??i?.notes??``,prestige_tier:r?.value??i?.prestige_tier??``};i&&(i.notes=a.notes,i.prestige_tier=a.prestige_tier),ii(t,a.prestige_tier),ti(`saving company...`);let o=await fetch(`/api/companies/${encodeURIComponent(e)}`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(a)});if(!o.ok)throw Error(`Company update failed`);U=await o.json(),ti(`company saved.`),ai(e)}function ii(e,t){e.classList.remove(`company-tier-unset`,`company-tier-0`,`company-tier-1`,`company-tier-2`,`company-tier-3`,`company-tier-4`),e.classList.add(Vr(t))}function ai(e){let t=w.querySelector(`[data-company-id="${CSS.escape(String(e))}"]`),n=ei(e);if(!t||!n)return;let r=Array.isArray(n.career_pages)?n.career_pages:[],i=W(n.updated_at),a=t.querySelector(`.company-summary-meta`);a&&(a.textContent=`${r.length} ${r.length===1?`link`:`links`}${i?` | updated ${i}`:``}`)}async function oi(){let e=await fetch(`/api/scan/status`);if(e.status===404){y.disabled=!0,b.hidden=!0,b.classList.add(`scan-error`),Pe.textContent=`restart server to enable scanning`;return}if(!e.ok)throw Error(`Scan status request failed`);Qn(await e.json())}function si(){rn===null&&(rn=window.setInterval(()=>{oi().catch(()=>{})},3e3))}async function ci(){y.disabled=!0,y.textContent=`starting...`;try{let e=await fetch(`/api/scan/all`,{method:`POST`});if(e.status===404){y.disabled=!0,y.textContent=`scan roles`,b.hidden=!0,b.classList.add(`scan-error`),Pe.textContent=`restart server to enable scanning`;return}if(!e.ok&&e.status!==409)throw Error(`Scan start failed`);Qn(await e.json()),si()}catch{y.disabled=!1,y.textContent=`scan roles`,b.hidden=!0,b.classList.add(`scan-error`),Pe.textContent=`could not start scan`}}async function li(){y.disabled=!0,y.textContent=`cancelling...`;try{let e=await fetch(`/api/scan/cancel`,{method:`POST`});if(e.status===404){y.disabled=!0,y.textContent=`scan roles`,b.hidden=!0,b.classList.add(`scan-error`),Pe.textContent=`restart server to enable scanning`;return}if(!e.ok&&e.status!==409)throw Error(`Scan cancel failed`);Qn(await e.json()),si()}catch{y.disabled=!1,y.textContent=`cancel scan`,b.hidden=!1,b.classList.add(`scan-error`),Pe.textContent=`could not cancel scan`}}async function ui(e=``){i.innerHTML=`<p class="empty-copy">loading jobs...</p>`;let t=new URLSearchParams;e&&t.set(`q`,e);let n=await fetch(`/api/tracker?${t.toString()}`);if(!n.ok)throw Error(`Tracker request failed`);Zn(await n.json())}async function di(e={}){let t=await fetch(`/api/application-materials`);if(!t.ok)throw Error(`Application materials request failed`);Mn(await t.json(),e)}async function fi(e){if(e){if(!e.name.toLowerCase().endsWith(`.tex`)){En(Nt,`resume must be a .tex file.`);return}m.disabled=!0,En(Nt,`uploading...`);try{let t=await e.text();if(!(await fetch(`/api/master-resume`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({filename:e.name,content:t})})).ok)throw Error(`Master resume upload failed`);await di()}catch{En(Nt,`could not save resume.`),Nn()}finally{p.value=``,m.disabled=!1}}}async function pi(e){let t=Array.from(e??[]);if(t.length!==0){oe.disabled=!0,jn(E,`uploading ${t.length} ${t.length===1?`resource`:`resources`}...`);try{for(let e of t)if(!(await fetch(`/api/resume-resources`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({filename:e.name,content_base64:await gi(e)})})).ok)throw Error(`Resume resource upload failed`);await di()}catch{jn(E,`could not save every resource.`),Nn()}finally{ae.value=``,oe.disabled=!1}}}async function mi(e){let t=Array.from(e??[]);if(t.length!==0){ue.disabled=!0,On(D,`uploading ${t.length} ${t.length===1?`example`:`examples`}...`);try{for(let e of t){let t={filename:e.name};if([`.pdf`,`.docx`].some(t=>e.name.toLowerCase().endsWith(t))?t.content_base64=await gi(e):t.content=await e.text(),!(await fetch(`/api/cover-letter-examples`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(t)})).ok)throw Error(`Cover letter example upload failed`)}await di()}catch{On(D,`could not save every example.`),Nn()}finally{le.value=``,ue.disabled=!1}}}async function hi(e){let t=Array.from(e??[]);if(t.length!==0){me.disabled=!0,kn(O,`uploading ${t.length} ${t.length===1?`note`:`notes`}...`);try{for(let e of t){let t=e.name.toLowerCase(),n={filename:e.name};if(t.endsWith(`.pdf`)||t.endsWith(`.docx`)?n.content_base64=await gi(e):n.content=await e.text(),!(await fetch(`/api/experience-notes`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(n)})).ok)throw Error(`Experience note upload failed`)}j.clear(),await di()}catch{kn(O,`could not save every note.`),Nn()}finally{pe.value=``,me.disabled=!1}}}function gi(e){return new Promise((t,n)=>{let r=new FileReader;r.addEventListener(`load`,()=>{let e=String(r.result??``);t(e.includes(`,`)?e.split(`,`,2)[1]:e)}),r.addEventListener(`error`,()=>n(r.error)),r.readAsDataURL(e)})}c.addEventListener(`submit`,e=>{e.preventDefault(),ui(l.value.trim()),hn()}),a.addEventListener(`click`,()=>{if(fn()){ui();return}mn()}),l.addEventListener(`keydown`,e=>{e.key===`Escape`&&(e.stopPropagation(),hn())}),u.addEventListener(`click`,hn),s.addEventListener(`click`,hn),m.addEventListener(`click`,()=>{p.click()}),p.addEventListener(`change`,()=>{fi(p.files?.[0])}),oe.addEventListener(`click`,()=>{ae.click()}),ae.addEventListener(`change`,()=>{pi(ae.files)}),ue.addEventListener(`click`,()=>{le.click()}),le.addEventListener(`change`,()=>{mi(le.files)}),me.addEventListener(`click`,()=>{pe.click()}),pe.addEventListener(`change`,()=>{hi(pe.files)}),te.addEventListener(`click`,()=>{Pn(te.getAttribute(`aria-expanded`)===`true`)});async function _i(e){e.disabled=!0;let t=e.textContent;e.textContent=`opening...`;try{if(!(await fetch(`/api/application-materials/index/open`,{method:`POST`})).ok)throw Error(`Could not open the application material index.`)}catch(e){ge.hidden=!1,ge.textContent=e instanceof Error?e.message:`Could not open the application material index.`}finally{e.disabled=!1,e.textContent=t}}ne.addEventListener(`click`,e=>{let t=e.target.closest(`[data-open-material-index]`);if(t){_i(t);return}let n=e.target.closest(`[data-material-view]`);if(n){Ln(n);return}let r=e.target.closest(`[data-material-remove]`);r&&Rn(r)}),y.addEventListener(`click`,()=>{if(on?.scanning){li();return}ci()}),i.addEventListener(`click`,e=>{let t=e.target.closest(`[data-review-role-id]`);if(t){ki(t.dataset.reviewRoleId);return}let n=e.target.closest(`[data-prep-role-id]`);if(n){ji(n.dataset.prepRoleId);return}let r=e.target.closest(`[data-autoprep-role-id]`);if(r){let e=Oi().find(e=>String(e.id)===String(r.dataset.autoprepRoleId));if(e?.autoprep_started){Sa(e.id).catch(()=>{Ue.textContent=`could not open that prepared role. try again.`});return}Ca(r.dataset.autoprepRoleId).catch(()=>{Ue.textContent=`could not add that role to Autoprep. try again.`});return}let i=e.target.closest(`.job-action`);if(i){vi(i);return}let a=e.target.closest(`.pane-toggle`);if(!a)return;let o=a.parentElement.querySelector(`.pane-body`),s=a.getAttribute(`aria-expanded`)===`true`;a.setAttribute(`aria-expanded`,String(!s)),a.querySelector(`.chevron`).textContent=s?`>`:`v`,o.hidden=s,io()});async function vi(e){let{roleId:t,status:n}=e.dataset;if(!t||!n)return;let r=e.closest(`.job-actions`),i=e.closest(`.job`);r.querySelectorAll(`button`).forEach(e=>{e.disabled=!0}),e.textContent=`updating...`;try{let e=await fetch(`/api/roles/${encodeURIComponent(t)}/status`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({status:n})});if(!e.ok)throw Error(`Status update failed`);yi((await e.json()).role,i)}catch{r.querySelectorAll(`button`).forEach(e=>{e.disabled=!1}),e.textContent=n===`disinterested`?`disinterested`:n.toLowerCase()}}function yi(e,t){if(!e||!T)return;let n=t?.closest(`.status-pane`)?.dataset.bucket??e.role_status,r=e.role_status,i=xi(e,n,r);Si(n,r),Ci(n,r),Tn(),Ei(T.statuses),wi(t,i,n,r),io()}function bi(e){if(!e||!T)return null;let t=null;return T.statuses.forEach(n=>{let r=n.jobs.findIndex(t=>String(t.id)===String(e.id));r!==-1&&(t={...n.jobs[r],...e},n.jobs[r]=t)}),Ei(T.statuses),t}function xi(e,t,n){let r=e;T.statuses.forEach(t=>{let n=t.jobs.findIndex(t=>String(t.id)===String(e.id));n!==-1&&(r={...t.jobs[n],...e},t.jobs.splice(n,1),t.count=t.jobs.length)});let i=T.statuses.find(e=>e.key===n);return i&&(i.jobs.unshift(r),i.count=i.jobs.length),r}function Si(e,t){T.statuses.forEach(e=>{let t=document.querySelector(`#status-${CSS.escape(e.key)}`);t?.classList.toggle(`empty`,e.count===0);let n=t?.querySelector(`.count`);n&&(n.textContent=e.count)}),[e,t].forEach(e=>{Ti(document.querySelector(`#status-${CSS.escape(e)}`))})}function Ci(e,t){if(!T.stats)return;let n=kt.has(e),r=kt.has(t);if(n===r){wn(T.stats);return}T.stats.applications_total=Number(T.stats.applications_total??0)+(r?1:-1),wn(T.stats)}function wi(e,t,n,r){let i=document.querySelector(`#status-${CSS.escape(r)}`),a=i?.querySelector(`.pane-body`);if(!e||!i||!a)return;e.remove(),Ti(document.querySelector(`#status-${CSS.escape(n)}`)),a.hidden=!1;let o=i.querySelector(`.pane-toggle`);o?.setAttribute(`aria-expanded`,`true`);let s=o?.querySelector(`.chevron`);s&&(s.textContent=`v`);let c=a.querySelector(`.jobs`);c||=(a.innerHTML=`<div class="jobs"></div>`,a.querySelector(`.jobs`)),c.insertAdjacentHTML(`afterbegin`,Bn(t,r)),Ti(i)}function Ti(e){if(!e)return;let t=e.querySelector(`.pane-body`);if(!t)return;let n=t.querySelector(`.jobs`),r=!!n?.querySelector(`.job`),i=t.querySelector(`.empty-copy`);if(r){i?.remove();return}n?.remove(),i||t.insertAdjacentHTML(`beforeend`,`<p class="empty-copy">no jobs in this status.</p>`)}function Ei(e){ve.disabled=Di(e).length===0,ve.setAttribute(`aria-label`,`review discovered`),ve.innerHTML=`<span class="review-discovered-label">review discovered</span>`}function Di(e=T?.statuses??[]){return e.find(e=>e.key===`discovered`)?.jobs??[]}function Oi(e=T?.statuses??[]){return e.find(e=>e.key===`interested`)?.jobs??[]}function ki(e=null){let t=[...Di()],n=e==null?null:String(e);if(n){let e=t.findIndex(e=>String(e.id)===n);if(e>0){let[n]=t.splice(e,1);t.unshift(n)}}k=t,h.hidden=!1,document.body.classList.add(`review-open`),Ni()}function Ai(){h.hidden=!0,document.body.classList.remove(`review-open`),k=[]}function ji(e=null){let t=[...Oi()].sort((e,t)=>Number(!!t.prep_started)-Number(!!e.prep_started)),n=e==null?null:String(e);if(n){let e=t.findIndex(e=>String(e.id)===n);if(e>0){let[n]=t.splice(e,1);t.unshift(n)}}A=t,g.hidden=!1,document.body.classList.add(`prep-open`),Yi()}function Mi(){g.hidden=!0,document.body.classList.remove(`prep-open`),A=[]}function Ni(e=``){let t=k[0],n=k.length,r=t?Pi(t):``;if(ye.textContent=n>0?`review queue`:`review complete`,be.textContent=n>0?`${n} discovered ${n===1?`role`:`roles`} in queue`:``,h.querySelectorAll(`.review-action`).forEach(e=>{e.disabled=n===0}),!t){xe.innerHTML=`
      <div class="review-empty">
        <h3>no discovered jobs left.</h3>
        <p>everything in this queue has been handled or moved out of discovered.</p>
      </div>
    `;return}xe.innerHTML=`
    ${e?`<p class="review-message">${G(e)}</p>`:``}
    ${r?`<p class="review-message review-message-warning">${G(r)}</p>`:``}
    <div class="review-title-row">
      <p class="review-company">${q(t.company_name)}</p>
      ${Cn(t.title,t.role_url,`review-role-title`)}
    </div>
    <dl class="review-details review-primary-details">
      ${Y(`location`,t.location,!1,`review-location-detail`)}
      ${Y(`first`,W(t.first_seen_at))}
      ${Y(`last`,W(t.last_seen_at))}
    </dl>
    ${Fi(t.description)}
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
  `}function Pi(e){let t=Number(e.review_later_count??0);return t<=Dt?``:`role review has been postponed ${t} times. it is recommended to set it to disinterested.`}function Y(e,t,n=!1,r=``){if(!t)return``;let i=n?`<a href="${G(t)}" target="_blank" rel="noreferrer">${q(t)}</a>`:q(t);return`
    <div class="review-detail ${G(r)}">
      <dt>${q(e)}</dt>
      <dd>${i}</dd>
    </div>
  `}function Fi(e){return e?`
    <div class="review-detail review-description">
      <dt>description</dt>
      <dd>${Ii(e)}</dd>
    </div>
  `:``}function Ii(e){let t=Li(String(e)).replace(/\u00a0/g,` `);if(Ri(t))return zi(t);let n=t.split(/\r?\n/).map(e=>e.trim()).filter(Boolean),r=[],i=[],a=()=>{i.length!==0&&(r.push(`<ul>${i.map(e=>`<li>${e}</li>`).join(``)}</ul>`),i=[])};return n.forEach(e=>{let t=e.match(/^#{2,3}\s+(.+)$/);if(t){a(),r.push(`<h3>${q(t[1])}</h3>`);return}if(qi(e)){a(),r.push(`<h3>${q(e.replace(/:$/,``))}</h3>`);return}let n=e.match(/^[-*]\s+(.+)$/);if(n){i.push(q(n[1]));return}a(),r.push(`<p>${q(e)}</p>`)}),a(),r.join(``)}function Li(e){let t=document.createElement(`textarea`);return t.innerHTML=e,t.value}function Ri(e){return/<\/?(?:a|br|div|em|h[1-6]|li|ol|p|span|strong|ul)\b/i.test(e)}function zi(e){let t=document.createElement(`template`);t.innerHTML=e;let n=[];return Bi(t.content.childNodes,n),n.join(``)}function Bi(e,t){e.forEach(e=>{if(e.nodeType===Node.TEXT_NODE){let n=Gi(e.textContent);n&&t.push(`<p>${q(n)}</p>`);return}if(e.nodeType!==Node.ELEMENT_NODE)return;let n=e,r=n.tagName.toLowerCase();if(r===`script`||r===`style`||r===`br`)return;if(/^h[1-6]$/.test(r)){Hi(t,n.textContent);return}if(r===`ul`||r===`ol`){let e=Ui(n);e&&t.push(e);return}if(r===`p`){Vi(n,t);return}let i=Array.from(n.children).some(e=>[`DIV`,`H1`,`H2`,`H3`,`H4`,`H5`,`H6`,`OL`,`P`,`UL`].includes(e.tagName));if([`article`,`div`,`section`].includes(r)&&i){Bi(n.childNodes,t);return}let a=Array.from(n.children).filter(e=>[`UL`,`OL`].includes(e.tagName)),o=Gi(Wi(n));if(o&&(Ki(o,n)?Hi(t,o):t.push(`<p>${q(o)}</p>`)),a.length>0){a.forEach(e=>{let n=Ui(e);n&&t.push(n)});return}!o&&i&&Bi(n.childNodes,t)})}function Vi(e,t){if(!e.querySelector(`br`)){let n=Gi(Wi(e));if(!n)return;Ki(n,e)?Hi(t,n):t.push(`<p>${q(n)}</p>`);return}let n=``,r=()=>{let r=Gi(n);n=``,r&&(Ki(r,e)?Hi(t,r):t.push(`<p>${q(r)}</p>`))};e.childNodes.forEach(e=>{if(e.nodeType===Node.ELEMENT_NODE&&e.tagName.toLowerCase()===`br`){r();return}n+=` ${e.textContent??``}`}),r()}function Hi(e,t){let n=Gi(t).replace(/:$/,``);n&&e.push(`<h3>${q(n)}</h3>`)}function Ui(e){let t=Array.from(e.children).filter(e=>e.tagName===`LI`).map(e=>{let t=Gi(Wi(e)),n=Array.from(e.children).filter(e=>[`UL`,`OL`].includes(e.tagName)).map(e=>Ui(e)).filter(Boolean).join(``);return t||n?`<li>${q(t)}${n}</li>`:``}).filter(Boolean);return t.length>0?`<ul>${t.join(``)}</ul>`:``}function Wi(e){let t=e.cloneNode(!0);return t.querySelectorAll(`ul, ol`).forEach(e=>{e.remove()}),t.textContent}function Gi(e){return String(e??``).replace(/\s+/g,` `).trim()}function Ki(e,t){let n=e.replace(/:$/,``).trim();return!n||n.length>90?!1:qi(n)||/:$/.test(e)?!0:/[.!?]$/.test(n)||n.split(/\s+/).length>10?!1:t.querySelector(`strong, b, u`)?!0:qi(n)}function qi(e){return jt.test(String(e).trim())}async function Ji(e){let t=k[0];if(!t)return;if(e===`later`){h.querySelectorAll(`.review-action`).forEach(e=>{e.disabled=!0});try{let e=await ya(t.id);k.shift(),bi(e),Ni(`moved out of this review pass.`)}catch{Ni(`could not postpone that role. try again.`)}finally{h.querySelectorAll(`.review-action`).forEach(e=>{e.disabled=k.length===0})}return}if(![`interested`,`disinterested`].includes(e))return;let n=h.querySelectorAll(`.review-action`);n.forEach(e=>{e.disabled=!0});try{let n=await ba(t.id,e);k.shift(),Ni(e===`interested`?`marked interested.`:`marked disinterested.`),yi(n,document.querySelector(`.job[data-role-id="${CSS.escape(String(t.id))}"]`))}catch{n.forEach(e=>{e.disabled=!1}),Ni(`could not update that role. try again.`)}}async function Yi(e=``){let t=A[0],n=A.length;Ce.textContent=n>0?`prep queue`:`prep complete`,we.textContent=n>0?`${n} interested ${n===1?`role`:`roles`} in queue`:``,g.querySelectorAll(`.review-action`).forEach(e=>{e.disabled=n===0});let r=g.querySelector(`[data-prep-action="autoprep"]`);if(r&&(r.textContent=t?.autoprep_started?`view / regenerate prep`:`autoprep`),!t){_.innerHTML=`
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
        ${Cn(t.title,t.role_url,`review-role-title`)}
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
      ${Xi(t)}
      ${ea(t)}
      ${Zi(t.id,t.description)}
      ${Qi(t)}
    </div>
  `,yn(),sa(t.id).then(e=>{!e||A[0]?.id!==t.id||(M.set(t.id,e),_.querySelector(`.prep-resume`)?.replaceWith(X(Xi(t,{resume:e}))),yn())}).catch(()=>{}),va(t.id).then(e=>{!e||A[0]?.id!==t.id||(N.set(t.id,e),_.querySelector(`.prep-cover-letter`)?.replaceWith(X(ea(t,{coverLetter:e}))),yn())}).catch(()=>{})}function Xi(e,t={}){let n=M.get(e.id),r=t.resume??n,i=t.tweaks??It.get(e.id)??``,a=`/api/roles/${encodeURIComponent(e.id)}/resume.pdf`;return t.loading?`
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
    `}function Zi(e,t){return`
    <details class="prep-panel prep-description-panel" id="prep-description-${e}">
      <summary class="prep-analysis-header">
        <span class="prep-accordion-icon" aria-hidden="true"></span>
        <h3>description</h3>
      </summary>
      ${Fi(t)}
    </details>
  `}function Qi(e,t={}){let n=t.messages??Lt.get(e.id)??[],r=!!t.loading;return`
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
      <p>${q(e?.content??``)}</p>
    </article>
  `}function ea(e,t={}){let n=N.get(e.id),r=t.coverLetter??n,i=t.tweaks??r?.tweaks??``,a=`/api/roles/${encodeURIComponent(e.id)}/cover-letter.pdf`;return t.loading?`
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
  `}function ta(e,t={}){let n=j.get(e.id);if(!t.loading&&!t.error&&!t.analysis&&n)return ta(e,{analysis:n});if(!t.loading&&!t.error&&!t.analysis)return`
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
    `;let r=t.analysis,i=Array.isArray(r?.feedback_items)?r.feedback_items:[],a=r?.verdict===`ready_to_apply`?`ready to apply`:`tweak`,o=Math.min(Ft.get(e.id)??0,Math.max(i.length-1,0)),s=i[o];return`
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
      <p>${q(e.tweak_prompt)}</p>
    </div>
  `:`
      <div class="prep-proposed-edit">
        <p class="prep-proposed-label">feedback only</p>
        <p>not enough information to turn this into a safe resume tweak.</p>
      </div>
    `}async function ra(e,t={}){if(!t.force&&j.has(e))return j.get(e);let n=await fetch(`/api/roles/${encodeURIComponent(e)}/prep-analysis`);if(!n.ok)throw Error(`Prep analysis request failed`);let r=await n.json();return r.analysis.resources=r.resources??[],j.set(e,r.analysis),r.analysis}function X(e){let t=document.createElement(`template`);return t.innerHTML=e.trim(),t.content.firstElementChild}async function ia(e){let t=A[0];if(!t)return;let n=g.querySelectorAll(`.review-action`);if(n.forEach(e=>{e.disabled=!0}),e===`later`){try{await ya(t.id),t.review_later_count=Number(t.review_later_count??0)+1,A.length>1?(A.push(A.shift()),Yi(`moved to the back of the prep queue.`)):Yi(`only one role is in the prep queue.`)}catch{Yi(`could not postpone prep. try again.`)}return}if(e===`autoprep`){try{if(t.autoprep_started){await Sa(t.id);return}await Ca(t.id)}catch{Yi(`could not add that role to Autoprep. try again.`)}return}if(e===`applied`)try{let e=await ba(t.id,`applied`);A.shift(),Yi(`moved to applied.`),yi(e,document.querySelector(`.job[data-role-id="${CSS.escape(String(t.id))}"]`))}catch{n.forEach(e=>{e.disabled=!1}),Yi(`could not move that role. try again.`)}}async function aa(e,t,n,r){let i=await fetch(`/api/roles/${encodeURIComponent(e)}/prep-feedback`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({feedback_index:t,feedback_item:n,comment:r})});if(!i.ok)throw Error(`Prep feedback update failed`);return i.json()}async function oa(e,t,n,r){let i=await fetch(`/api/roles/${encodeURIComponent(e)}/prep-feedback-ignore`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({feedback_index:t,feedback_item:n,comment:r})});if(!i.ok)throw Error(`Prep feedback ignore failed`);return i.json()}async function sa(e,{force:t=!1}={}){if(!t&&M.has(e))return M.get(e);let n=await fetch(`/api/roles/${encodeURIComponent(e)}/resume`);if(!n.ok)throw Error(`Resume request failed`);let r=await n.json();return r.resume&&M.set(e,r.resume),r.resume}async function ca(e,t){let n=await fetch(`/api/roles/${encodeURIComponent(e)}/resume/save`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({latex:t})});if(!n.ok)throw Error(`Resume save failed`);return n.json()}async function la(e,t,n){let r=await fetch(`/api/roles/${encodeURIComponent(e)}/resume`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({tweaks:t,previous_latex:n})});if(!r.ok)throw Error(`Resume generation failed`);return r.json()}async function ua(e,t){let n=await fetch(`/api/roles/${encodeURIComponent(e)}/chat`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({messages:t})});if(!n.ok)throw Error(`Role chat failed`);return n.json()}function da(e,t,n=Ot){let r=Rt.get(e)??{timer:null,saving:!1,version:0,latex:``};r.version+=1,r.latex=t,r.timer&&clearTimeout(r.timer),r.timer=setTimeout(()=>{r.timer=null,fa(e)},n),Rt.set(e,r)}async function fa(e){let t=Rt.get(e);if(!t||t.saving)return;t.saving=!0;let n=t.version,r=t.latex;try{let i=await ca(e,r);t.version===n&&(M.set(e,i.resume),pa(`resume`,e,i.resume))}catch{}finally{t.saving=!1,t.version!==n&&da(e,t.latex,0)}}function pa(e,t,n){if(!n?.pdf_base64)return;let r=e===`resume`?`[data-prep-resume-latex="${t}"]`:`[data-prep-cover-letter-latex="${t}"]`,i=_.querySelector(r)?.closest(`.prep-panel`),a=i?.querySelector(`.prep-cover-pdf`),o=i?.querySelector(`.prep-cover-pdf-link`),s=e===`resume`?`/api/roles/${encodeURIComponent(t)}/resume.pdf`:`/api/roles/${encodeURIComponent(t)}/cover-letter.pdf`;a&&(a.src=`${s}?v=${Date.now()}`),o&&(o.href=s)}async function ma(e,t=``,n=``){let r=await fetch(`/api/roles/${encodeURIComponent(e)}/cover-letter`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({tweaks:t,previous_latex:n})});if(!r.ok)throw Error(`Cover letter generation failed`);return r.json()}async function ha(e,t){let n=await fetch(`/api/roles/${encodeURIComponent(e)}/cover-letter/save`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({latex:t})});if(!n.ok)throw Error(`Cover letter save failed`);return n.json()}function ga(e,t,n=``,r=Ot){let i=zt.get(e)??{timer:null,saving:!1,version:0,latex:``,tweaks:``};i.version+=1,i.latex=t,i.tweaks=n,i.timer&&clearTimeout(i.timer),i.timer=setTimeout(()=>{i.timer=null,_a(e)},r),zt.set(e,i)}async function _a(e){let t=zt.get(e);if(!t||t.saving)return;t.saving=!0;let n=t.version,r=t.latex,i=t.tweaks;try{let a=await ha(e,r);t.version===n&&(N.set(e,{...a.cover_letter,tweaks:i}),pa(`coverLetter`,e,a.cover_letter))}catch{}finally{t.saving=!1,t.version!==n&&ga(e,t.latex,t.tweaks,0)}}async function va(e){if(N.has(e))return N.get(e);let t=await fetch(`/api/roles/${encodeURIComponent(e)}/cover-letter`);if(!t.ok)throw Error(`Cover letter request failed`);let n=await t.json();return n.cover_letter&&N.set(e,n.cover_letter),n.cover_letter}async function ya(e){let t=await fetch(`/api/roles/${encodeURIComponent(e)}/review-later`,{method:`POST`});if(!t.ok)throw Error(`Review later update failed`);return(await t.json()).role}async function ba(e,t){let n=await fetch(`/api/roles/${encodeURIComponent(e)}/status`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({status:t})});if(!n.ok)throw Error(`Status update failed`);return(await n.json()).role}function xa(e){return`${e}-${globalThis.crypto?.randomUUID?.()??`${Date.now()}-${Math.random()}`}`}async function Sa(e){let t=Number(e);!Number.isInteger(t)||t<=0||(F=t,g.hidden||Mi(),await Ta())}async function Ca(e){let t=Number(e);if(!Number.isInteger(t)||t<=0||Ht.has(t))return null;Ht.add(t);let n=document.querySelectorAll(`[data-autoprep-role-id="${CSS.escape(String(t))}"]`);n.forEach(e=>{e.disabled=!0,e.setAttribute(`aria-busy`,`true`),e.textContent=`queuing...`});try{let e=await fetch(`/api/autoprep/jobs`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({role_ids:[t],idempotency_key:xa(`autoprep-role-${t}`)})}),n=await e.json();if(!e.ok)throw Error(n.error||`Autoprep request failed`);let r=Array.isArray(n.jobs)?n.jobs:[],i=new Map(P.map(e=>[Number(e.role_id),e]));r.forEach(e=>i.set(Number(e.role_id),e));let a=r.find(e=>Number(e.role_id)===t),o=Oi().find(e=>Number(e.id)===t);return a&&o&&T&&(o.autoprep_started=!0,o.autoprep_status=a.overall_status??`queued`,Zn(T)),F=t,g.hidden||Mi(),await Ta({seedJobs:[...i.values()]}),r}finally{Ht.delete(t),n.forEach(e=>{e.disabled=!1,e.removeAttribute(`aria-busy`),e.textContent=Oi().find(e=>Number(e.id)===t)?.autoprep_started?`view / regenerate prep`:`autoprep`})}}function wa(e){window.location.hash!==e&&window.history.pushState({},``,e||`${window.location.pathname}${window.location.search}`)}async function Ta({seedJobs:e=null}={}){De.hidden=!1,document.body.classList.add(`prepped-open`),wa(`#prepped-roles`),e?(P=e,F=F??P[0]?.role_id??null,Q()):P.length===0&&(ke.textContent=`loading prepared roles...`),await Da(),Oa()}function Ea({clearHash:e=!0}={}){De.hidden=!0,document.body.classList.remove(`prepped-open`),ka(),R.clear(),Gt.clear(),H.forEach(e=>URL.revokeObjectURL(e)),H.clear(),Qt.clear(),$t.clear(),e&&window.location.hash===`#prepped-roles`&&wa(``)}window.addEventListener(`pagehide`,()=>{document.querySelectorAll(`[data-preview-blob-url]`).forEach(e=>{URL.revokeObjectURL(e.dataset.previewBlobUrl)}),H.forEach(e=>URL.revokeObjectURL(e)),H.clear(),Qt.clear()});async function Da(){try{let e=await fetch(`/api/autoprep/jobs`);if(!e.ok)throw Error(`Prepped roles request failed`);let t=await e.json();P=t.jobs??[];let n=t.bulk_cover_letter_regeneration;if(n){let e=Array.isArray(n.jobs)?n.jobs:[];L={idempotencyKey:n.idempotency_key,roleIds:e.map(e=>Number(e.role_id)),jobs:e,skipped:Array.isArray(n.skipped)?n.skipped:[]}}P.some(e=>Number(e.role_id)===Number(F))||(F=P[0]?.role_id??null),Q()}catch{ke.textContent=`could not refresh preparation progress.`}}function Oa(){ka(),P.some(Aa)&&(Bt=window.setInterval(Da,2e3))}function ka(){Bt!==null&&window.clearInterval(Bt),Bt=null}function Aa(e){return[`queued`,`generating_resume_tweaks`,`regenerating_resume`,`generating_cover_letter`].includes(e.overall_status)}function ja(e){return[e.resume_status,e.cover_letter_status].some(e=>[`failed`,`interrupted`].includes(e))}function Ma(e){return e.cover_letter_status===`generating`||e.overall_status===`generating_cover_letter`}function Na(e){return Ma(e)||e.resume_status===`generating_tweaks`||e.resume_status===`regenerating`||e.overall_status===`generating_resume_tweaks`||e.overall_status===`regenerating_resume`}function Pa(e){return e.worker_state===`queued`||e.overall_status===`queued`}function Fa(e){return{queued:`Queued`,generating_resume_tweaks:`Generating resume tweaks`,regenerating_resume:`Regenerating resume`,generating_cover_letter:`Generating cover letter`,partially_complete:`Partially complete`,ready:`Ready`,failed:`Failed`,interrupted:`Interrupted`,generating_tweaks:`Generating tweaks`,regenerating:`Regenerating`,generating:`Generating`}[e]??K(e)}function Ia(e,t){let n=t===`cover-letter`?`cover_letter`:`resume`;return`${e.updated_at||``}:${e[`${n}_artifact_path`]||``}`}function Z(e,{close:t=!1}={}){let n=H.get(e);n&&URL.revokeObjectURL(n),H.delete(e),Qt.delete(e),$t.delete(e),t&&R.delete(e)}function La(){Qt.forEach((e,t)=>{let[n,r]=t.split(`:`),i=P.find(e=>Number(e.role_id)===Number(n));(!i||Ia(i,r)!==e)&&Z(t,{close:!0})})}function Ra(){if(!L)return;let e=L.jobs||P,t=new Map(e.map(e=>[Number(e.role_id),e])),n=L.roleIds.map(e=>t.get(Number(e))),r=n.filter(e=>e?.worker_state===`idle`&&e.cover_letter_status===`ready`).length,i=n.filter(e=>!e||e.worker_state===`idle`&&[`failed`,`interrupted`].includes(e.cover_letter_status)),a=n.length-r-i.length,o=L.skipped.length?` Skipped before queueing: ${L.skipped.map(e=>`${e.company_name} — ${e.title}: ${e.reason}`).join(` · `)}`:``,s=i.length?` Queued regeneration failures: ${i.map(e=>e?`${e.company_name} — ${e.title}: ${e.cover_letter_error||`generation failed`}`:`A role left the Prepped queue before regeneration completed`).join(` · `)}`:``;I=n.length?a>0?`Cover-letter regeneration in progress: ${r} of ${n.length} complete · ${a} remaining.${o}${s}`:`Cover-letter regeneration complete: ${r} succeeded, ${i.length} failed.${o}${s}`:`No cover letters were queued.${o}`}function Q(){La(),Ra();let e=P.filter(Aa).length,t=P.filter(e=>e.worker_state===`idle`&&e.cover_letter_status===`ready`).length;ke.textContent=P.length?`${P.length} prepped ${P.length===1?`role`:`roles`}${e?` · ${e} in progress`:``}`:`No queued or prepared roles.`,Ae.disabled=Vt||t===0,Ae.setAttribute(`aria-busy`,Vt?`true`:`false`),Ae.textContent=Vt?`queuing cover letters...`:`regenerate all cover letters`,je.textContent=I,Me.innerHTML=P.map(e=>{let t=ja(e),n=!t&&Na(e),r=!t&&!n&&Pa(e),i=Number(e.role_id)===Number(F)?` is-active`:``;return`
      <button type="button" class="prepped-list-item${r?` is-generation-queued`:``}${n?` is-document-generating`:``}${t?` has-generation-failure`:``}${i}" data-prepped-role="${e.role_id}">
        <strong>${q(e.company_name)}</strong><span>${q(e.title)}</span>
        <small class="status-${G(e.overall_status)}">${G(Fa(e.overall_status))}</small>
      </button>`}).join(``),$(),Oa()}function $(){let e=P.findIndex(e=>Number(e.role_id)===Number(F)),t=P[e];if(!t){v.innerHTML=`<div class="prepped-empty"><h3>nothing prepped yet.</h3><p>Queue Interested roles from Autoprep Interested.</p></div>`;return}let n=q(t.title),r=_n(t.role_url),i=r?`<a class="prepped-role-link" href="${G(r)}" target="_blank" rel="noopener noreferrer">${n}<span aria-hidden="true">↗</span></a>`:n,a=[[`Location`,t.location||`Unavailable`],[`Added`,W(t.date_added||t.created_at)||`Unavailable`],[`Last seen`,W(t.last_seen_at)||`Unavailable`],[`Posting ID`,t.posting_id||`Unavailable`]],o=Ut.has(Number(t.role_id)),s=o||Aa(t),c=`${t.role_id}:description`,l=`${t.role_id}:notes`;v.innerHTML=`
    <header class="prepped-detail-heading">
      <div><p class="eyebrow">${q(t.company_name)}</p><h3>${i}</h3></div>
      <span class="prepped-status status-${G(t.overall_status)}">${G(Fa(t.overall_status))}</span>
    </header>
    <dl class="prepped-role-facts">${a.map(([e,t])=>`<div><dt>${G(e)}</dt><dd>${q(t)}</dd></div>`).join(``)}</dl>
    <details class="prepped-role-description" data-prepped-detail-section="description" ${Gt.has(c)?`open`:``}>
      <summary>Job description</summary>
      <div class="prepped-description-copy">${q(t.description||`No job description was saved.`).replaceAll(`
`,`<br>`)}</div>
    </details>
    ${t.notes?`<details class="prepped-role-description" data-prepped-detail-section="notes" ${Gt.has(l)?`open`:``}><summary>Role notes</summary><div class="prepped-description-copy">${q(t.notes).replaceAll(`
`,`<br>`)}</div></details>`:``}
    <div class="prepped-document-grid">
      ${Ya(t,`resume`,`Resume`)}
      ${Ya(t,`cover-letter`,`Cover letter`)}
    </div>
    ${Ba(t)}
    <div class="prepped-detail-actions">
      <button class="prepped-nav-action" type="button" data-prepped-nav="previous" ${e<=0?`disabled`:``}>Previous</button>
      <button class="prepped-nav-action" type="button" data-prepped-nav="next" ${e>=P.length-1?`disabled`:``}>Next</button>
      <button class="prepped-folder-action" type="button" data-autoprep-open-folder ${t.artifact_directory?``:`disabled`}>Open Documents Folder</button>
      <button class="prepped-disinterested" type="button" data-autoprep-disinterested aria-busy="${o?`true`:`false`}" ${s?`disabled`:``} title="${Aa(t)?`Wait for preparation to finish before moving this role`:`Move this role out of Prepped`}">${o?`Moving to Disinterested...`:`Move to Disinterested`}</button>
      <button class="success" type="button" data-autoprep-applied ${t.overall_status===`ready`?``:`disabled`}>Applied</button>
    </div>
    <p class="prepped-safety-note">Autoprep prepares files only. It never submits an application.</p>`,qt.has(Number(t.role_id))||Ha(t.role_id)}function za(e){return Array.isArray(e)?e:Array.isArray(e?.answers)?e.answers:e?.answer&&typeof e.answer==`object`?[e.answer]:e?.record&&typeof e.record==`object`?[e.record]:e&&typeof e==`object`&&(`question`in e||`answer`in e||`status`in e||`error`in e)?[e]:[]}function Ba(e){let t=Number(e.role_id),n=z.get(t)??[],r=Kt.get(t)??``,i=B.has(t),a=Jt.has(t),o=V.get(t);return`<section class="application-questions-workspace" aria-labelledby="application-questions-heading-${t}">
    <div class="application-questions-heading"><div><p class="eyebrow">Application helper</p><h4 id="application-questions-heading-${t}">Application questions</h4></div><span>${n.length} saved</span></div>
    <p class="application-questions-intro">Paste a question from an application form to generate and keep a role-specific answer.</p>
    <div class="application-answer-history" aria-live="polite">
      ${a&&!n.length?`<p class="application-answer-empty">Loading saved answers…</p>`:``}
      ${o?`<p class="prepped-error">${q(o)}</p>`:``}
      ${!a&&!o&&!n.length?`<p class="application-answer-empty">No application questions saved yet.</p>`:``}
      ${n.map((e,t)=>Va(e,t,i)).join(``)}
    </div>
    <div class="application-question-composer">
      <label for="application-question-${t}">Question</label>
      <textarea id="application-question-${t}" data-application-question-draft rows="4" placeholder="Paste an application question…" ${i?`disabled`:``}>${G(r)}</textarea>
      <div><small>Answers are saved to this role. Asking never changes its status.</small><button class="application-question-submit" type="button" data-application-question-submit aria-busy="${i?`true`:`false`}" ${i||!r.trim()?`disabled`:``}>${i?`Generating…`:`Generate answer`}</button></div>
    </div>
  </section>`}function Va(e,t,n){let r=e?.status??`saved`,i=e?.created_at??e?.updated_at??e?.timestamp,a=e?.backend??e?.generation_backend,o=Number(e?.id),s=Number.isFinite(o)&&r!==`pending`&&!n,c=Yt.has(o),l=Xt.has(o),u=Zt.has(o);return`<article class="application-answer-record status-${G(r)}">
    <div class="application-answer-meta"><span>${q(r)}</span>${a?`<span>${q(a)}</span>`:``}${i?`<time datetime="${G(i)}">${q(W(i)||i)}</time>`:``}</div>
    <h5>${G(e.question??`Question unavailable`)}</h5>
    ${e.answer?`<p class="application-answer-copy">${G(e.answer).replaceAll(`
`,`<br>`)}</p>`:``}
    ${e.error?`<p class="prepped-error">${q(e.error)}</p>`:``}
    <div class="application-answer-actions">
      ${e.answer?`<button type="button" data-application-answer-copy="${t}">Copy answer</button>`:``}
      ${Number.isFinite(o)?`<button type="button" data-application-answer-regenerate="${o}" ${s?``:`disabled`}>${l||r===`pending`?`Regenerating…`:`Regenerate`}</button><button class="danger" type="button" data-application-answer-delete="${o}" ${s?``:`disabled`}>${u?`Deleting…`:c?`Confirm delete`:`Delete question`}</button>`:``}
    </div>
  </article>`}async function Ha(e){let t=Number(e);if(!Jt.has(t)){Jt.add(t),V.delete(t);try{let n=await fetch(`/api/autoprep/roles/${encodeURIComponent(e)}/application-answers`),r=await n.json();if(!n.ok)throw Error(r?.error||`Could not load saved answers.`);z.set(t,za(r)),qt.add(t)}catch(e){V.set(t,e instanceof Error?e.message:`Could not load saved answers.`)}finally{Jt.delete(t),Number(F)===t&&$()}}}async function Ua(e){if(navigator.clipboard?.writeText)try{await navigator.clipboard.writeText(e);return}catch{}let t=document.createElement(`textarea`);t.value=e,t.readOnly=!0,t.style.position=`fixed`,t.style.opacity=`0`,document.body.append(t),t.select();let n=document.execCommand(`copy`);if(t.remove(),!n)throw Error(`Clipboard copy is unavailable`)}async function Wa(e){let t=Number(e),n=String(Kt.get(t)??``).trim();if(!(!n||B.has(t))){B.add(t),$();try{let r=await fetch(`/api/autoprep/roles/${encodeURIComponent(e)}/application-answers`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({question:n})}),i=await r.json(),a=za(i),o=z.get(t)??[];if(Array.isArray(i?.answers)?z.set(t,a):a.length&&z.set(t,[...o,...a]),!r.ok)throw Error(i?.error||a[0]?.error||`Could not generate an answer.`);Kt.delete(t),qt.add(t),V.delete(t)}catch(e){V.set(t,e instanceof Error?e.message:`Could not generate an answer.`)}finally{B.delete(t),Number(F)===t&&$()}}}function Ga(e,t){let n=Number(e),r=z.get(n)??[],i=Number(t?.id),a=r.findIndex(e=>Number(e?.id)===i);if(a<0){z.set(n,[t,...r]);return}let o=[...r];o[a]=t,z.set(n,o)}async function Ka(e,t){let n=Number(e);if(!B.has(n)){B.add(n),Xt.add(Number(t)),Yt.delete(Number(t)),V.delete(n),$();try{let r=await fetch(`/api/autoprep/roles/${encodeURIComponent(e)}/application-answers/${encodeURIComponent(t)}/regenerate`,{method:`POST`}),i=await r.json(),[a]=za(i);if(a&&Ga(n,a),!r.ok)throw Error(i?.error||a?.error||`Could not regenerate the answer.`)}catch(e){V.set(n,e instanceof Error?e.message:`Could not regenerate the answer.`)}finally{Xt.delete(Number(t)),B.delete(n),Number(F)===n&&$()}}}async function qa(e,t){let n=Number(e),r=Number(t);if(!Yt.has(r)){Yt.add(r),$();return}if(!B.has(n)){B.add(n),Zt.add(r),Yt.delete(r),V.delete(n),$();try{let i=await fetch(`/api/autoprep/roles/${encodeURIComponent(e)}/application-answers/${encodeURIComponent(t)}`,{method:`DELETE`}),a=await i.json();if(!i.ok)throw Error(a?.error||`Could not delete the question.`);let o=z.get(n)??[];z.set(n,o.filter(e=>Number(e?.id)!==r))}catch(e){V.set(n,e instanceof Error?e.message:`Could not delete the question.`)}finally{Zt.delete(r),B.delete(n),Number(F)===n&&$()}}}async function Ja(e,t){let n=`${e.role_id}:${t}`,r=Ia(e,t);if(!(Qt.get(n)===r||en.has(n))){Z(n),en.add(n),$t.delete(n),$();try{let i=await In(`/api/autoprep/roles/${encodeURIComponent(e.role_id)}/documents/${t}.pdf?v=${encodeURIComponent(e.updated_at||``)}`),a=P.find(t=>Number(t.role_id)===Number(e.role_id));if(!R.has(n)||!a||Ia(a,t)!==r){URL.revokeObjectURL(i),R.delete(n);return}H.set(n,i),Qt.set(n,r)}catch(e){$t.set(n,e instanceof Error?e.message:`PDF preview unavailable`)}finally{en.delete(n),Number(F)===Number(e.role_id)&&$()}}}function Ya(e,t,n){let r=t===`cover-letter`?`cover_letter`:`resume`,i=e[`${r}_status`],a=e[`${r}_artifact_path`],o=a?.split(`/`).pop()??`Not available`,s=e[`${r}_error`],c=e[`${r}_instruction`]||``,l=`${e.role_id}:${t}`,u=Wt.get(l)??c,ee=t===`cover-letter`?`Optional comments for the next version`:`Comments for the next version`,te=t===`cover-letter`?`Optionally describe specific, truthful changes...`:`Describe specific, truthful changes...`,ne=[`failed`,`interrupted`].includes(i),d=e.worker_state!==`idle`||[`queued`,`generating`,`generating_tweaks`,`regenerating`].includes(i),re=!d&&(i===`ready`||ne)&&(ne||t===`cover-letter`||String(u).trim()),f=R.has(l),p=`/api/autoprep/roles/${encodeURIComponent(e.role_id)}/documents/${t}.pdf?v=${encodeURIComponent(e.updated_at||``)}`,m=H.get(l),ie=$t.get(l),ae=en.has(l),oe=a?`<a class="prep-cover-pdf-link" data-autoprep-view="${t}" href="${G(p)}" target="_blank" rel="noreferrer" aria-label="View ${G(n.toLowerCase())} PDF in browser">View PDF</a>`:``;return`
    <section class="prepped-document${f?` has-open-preview`:``} status-${G(i)}">
      <div class="prepped-document-heading"><h4>${G(n)}</h4><span>${G(Fa(i))}</span></div>
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
    </section>`}async function Xa(e,t,n){if(n.disabled)return;let r=`${e.role_id}:${t}`,i=e[`${t===`cover-letter`?`cover_letter`:`resume`}_status`],a=[`failed`,`interrupted`].includes(i),o=v.querySelector(`[data-autoprep-comments="${t}"]`),s=String(o?.value||Wt.get(r)||``).trim();if(!s&&t!==`cover-letter`&&!a){o?.focus();return}n.disabled=!0,n.textContent=`Queuing regeneration...`;try{let n=await fetch(`/api/autoprep/roles/${encodeURIComponent(e.role_id)}/${a?`retry`:`regenerate`}/${t}`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(a?{idempotency_key:xa(`retry-${t}`)}:{comments:s,idempotency_key:xa(`regenerate-${t}`)})}),i=await n.json();if(!n.ok)throw Error(i.error||`Regeneration request failed`);Wt.delete(r),Z(r,{close:!0});let o=P.findIndex(t=>Number(t.role_id)===Number(e.role_id));o>=0&&(P[o]=i.job),Q()}catch(e){window.alert(e instanceof Error?e.message:`Regeneration request failed`),await Da()}}async function Za(){if(!Vt){Vt=!0,L=null,I=`Queuing eligible cover letters...`,Q();try{let e=await fetch(`/api/autoprep/cover-letters/regenerate`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({idempotency_key:xa(`regenerate-all-cover-letters`)})}),t=await e.json();if(!e.ok)throw Error(t.error||`Bulk regeneration request failed`);let n=Number(t.queued_count||0),r=Array.isArray(t.skipped)?t.skipped:[];L={roleIds:(t.jobs||[]).map(e=>Number(e.role_id)),jobs:t.jobs||[],skipped:r},!n&&!r.length&&(L=null,I=`No prepped roles are available to regenerate.`),(t.jobs||[]).forEach(e=>{let t=P.findIndex(t=>Number(t.role_id)===Number(e.role_id));t>=0&&(P[t]=e),Z(`${e.role_id}:cover-letter`,{close:!0})}),await Da(),Oa()}catch(e){L=null,I=e instanceof Error?e.message:`Bulk regeneration request failed`}finally{Vt=!1,Q()}}}async function Qa(e,t){let n=Number(e);if(Ut.has(n))return;Ut.add(n),t.disabled=!0,t.setAttribute(`aria-busy`,`true`),t.textContent=`Moving to Disinterested...`;let r=P.findIndex(e=>Number(e.role_id)===n);try{await ba(e,`disinterested`),Z(`${e}:resume`,{close:!0}),Z(`${e}:cover-letter`,{close:!0}),r>=0&&P.splice(r,1),F=P[Math.min(r,P.length-1)]?.role_id??null,I=`Role moved to Disinterested.`,Q(),Ir()}catch(e){I=e instanceof Error?e.message:`Could not move this role to Disinterested.`,await Da()}finally{Ut.delete(n),P.some(e=>Number(e.role_id)===n)&&Q()}}async function $a(e,t){if(t.disabled)return;t.disabled=!0,t.textContent=`Moving to Applied...`;let n=P.findIndex(t=>Number(t.role_id)===Number(e));try{if(!(await fetch(`/api/autoprep/roles/${encodeURIComponent(e)}/applied`,{method:`POST`})).ok)throw Error(`Applied update failed`);Z(`${e}:resume`,{close:!0}),Z(`${e}:cover-letter`,{close:!0}),P.splice(n,1),F=P[Math.min(n,P.length-1)]?.role_id??null,Q(),Ir()}catch{await Da()}}ve.addEventListener(`click`,ki),Se.addEventListener(`click`,Ai),Ee.addEventListener(`click`,()=>Ta()),Oe.addEventListener(`click`,Ea),Ae.addEventListener(`click`,Za),Me.addEventListener(`click`,e=>{let t=e.target.closest(`[data-prepped-role]`);t&&(F=Number(t.dataset.preppedRole),Q())}),v.addEventListener(`input`,e=>{let t=e.target.closest(`[data-application-question-draft]`);if(t){let e=Number(F);Kt.set(e,t.value);let n=v.querySelector(`[data-application-question-submit]`);n&&(n.disabled=!t.value.trim()||B.has(e));return}let n=e.target.closest(`[data-autoprep-comments]`);if(!n)return;let r=`${F}:${n.dataset.autoprepComments}`;Wt.set(r,n.value);let i=v.querySelector(`[data-autoprep-regenerate="${n.dataset.autoprepComments}"]`),a=P.find(e=>Number(e.role_id)===Number(F)),o=n.dataset.autoprepComments===`cover-letter`?`cover_letter`:`resume`,s=a?.[`${o}_status`],c=[`failed`,`interrupted`].includes(s);i&&(i.disabled=a?.worker_state!==`idle`||![`ready`,`failed`,`interrupted`].includes(s)||!c&&n.dataset.autoprepComments!==`cover-letter`&&!n.value.trim())}),v.addEventListener(`toggle`,e=>{let t=e.target.closest(`[data-prepped-detail-section]`);if(!t)return;let n=`${F}:${t.dataset.preppedDetailSection}`;t.open?Gt.add(n):Gt.delete(n)},!0),v.addEventListener(`click`,async e=>{let t=P.find(e=>Number(e.role_id)===Number(F));if(!t)return;if(e.target.closest(`[data-application-question-submit]`)){Wa(t.role_id);return}let n=e.target.closest(`[data-application-answer-regenerate]`);if(n){Ka(t.role_id,n.dataset.applicationAnswerRegenerate);return}let r=e.target.closest(`[data-application-answer-delete]`);if(r){qa(t.role_id,r.dataset.applicationAnswerDelete);return}let i=e.target.closest(`[data-application-answer-copy]`);if(i){let e=(z.get(Number(t.role_id))??[])[Number(i.dataset.applicationAnswerCopy)]?.answer;if(!e)return;try{await Ua(String(e)),i.textContent=`Copied`}catch{i.textContent=`Copy unavailable`}return}let a=e.target.closest(`[data-prepped-nav]`);if(a){let e=P.indexOf(t),n=a.dataset.preppedNav===`next`?1:-1;F=P[e+n]?.role_id??t.role_id,Q();return}let o=e.target.closest(`[data-autoprep-preview]`);if(o){let e=o.dataset.autoprepPreview,n=`${t.role_id}:${e}`;R.has(n)?(R.delete(n),$()):(R.add(n),$(),Ja(t,e));return}let s=e.target.closest(`[data-autoprep-regenerate]`);if(s){Xa(t,s.dataset.autoprepRegenerate,s);return}let c=e.target.closest(`[data-autoprep-open-folder]`);if(c&&!c.disabled){c.disabled=!0,c.textContent=`Opening...`;try{if(!(await fetch(`/api/autoprep/roles/${encodeURIComponent(t.role_id)}/open-folder`,{method:`POST`})).ok)throw Error(`Could not open the documents folder.`);c.textContent=`Opened in Finder`,window.setTimeout(()=>{c.isConnected&&(c.textContent=`Open Documents Folder`,c.disabled=!1)},1500)}catch(e){c.textContent=e instanceof Error?e.message:`Could not open folder`,c.disabled=!1}return}let l=e.target.closest(`[data-autoprep-disinterested]`);if(l){Qa(t.role_id,l);return}let u=e.target.closest(`[data-autoprep-applied]`);u&&$a(t.role_id,u)}),Te.addEventListener(`click`,Mi),h.addEventListener(`click`,e=>{let t=e.target.closest(`[data-review-action]`);t&&Ji(t.dataset.reviewAction)}),g.addEventListener(`click`,e=>{e.target.closest(`.prep-summary-action`)&&e.stopPropagation()}),g.addEventListener(`input`,e=>{let t=e.target.closest(`[data-prep-resume-tweaks]`);if(t){let e=Number(t.dataset.prepResumeTweaks);Number.isFinite(e)&&It.set(e,t.value);return}let n=e.target.closest(`[data-prep-resume-latex]`);if(n){let e=Number(n.dataset.prepResumeLatex);if(!Number.isFinite(e))return;da(e,n.value);return}let r=e.target.closest(`[data-prep-cover-letter-latex]`);if(!r)return;let i=Number(r.dataset.prepCoverLetterLatex);if(!Number.isFinite(i))return;let a=r.closest(`.prep-cover-letter`)?.querySelector(`[data-prep-cover-letter-tweaks="${i}"]`)?.value??``;ga(i,r.value,a)}),g.addEventListener(`scroll`,e=>{e.target.closest(`[data-prep-resume-latex], [data-prep-cover-letter-latex]`)},!0),g.addEventListener(`focusout`,e=>{let t=e.target.closest(`[data-prep-resume-latex]`);if(t){let e=Number(t.dataset.prepResumeLatex);if(!Number.isFinite(e))return;da(e,t.value,0);return}let n=e.target.closest(`[data-prep-cover-letter-latex]`);if(!n)return;let r=Number(n.dataset.prepCoverLetterLatex);if(!Number.isFinite(r))return;let i=n.closest(`.prep-cover-letter`)?.querySelector(`[data-prep-cover-letter-tweaks="${r}"]`)?.value??``;ga(r,n.value,i,0)}),g.addEventListener(`submit`,async e=>{let t=e.target.closest(`[data-prep-role-chat-form]`);if(!t||!A[0])return;e.preventDefault();let n=Number(t.dataset.prepRoleChatForm);if(!Number.isFinite(n))return;let r=t.querySelector(`[data-prep-role-chat-input="${n}"]`),i=r?.value?.trim()??``;if(!i){r?.focus();return}let a=[...Lt.get(n)??[],{role:`user`,content:i}];Lt.set(n,a),_.querySelector(`.prep-role-chat`)?.replaceWith(X(Qi(A[0],{messages:a,loading:!0})));try{let e=await ua(n,a),t=[...a,e.message];Lt.set(n,t),_.querySelector(`.prep-role-chat`)?.replaceWith(X(Qi(A[0],{messages:t})))}catch{let e=[...a,{role:`assistant`,content:`could not answer right now.`}];Lt.set(n,e),_.querySelector(`.prep-role-chat`)?.replaceWith(X(Qi(A[0],{messages:e})))}}),g.addEventListener(`click`,async e=>{let t=e.target.closest(`[data-prep-section-target]`);if(t){let e=t.dataset.prepSectionTarget,n=e?document.getElementById(e):null;if(n instanceof HTMLDetailsElement){n.open=!0,n.scrollIntoView({behavior:`smooth`,block:`start`});let e=n.querySelector(`summary`);e?.setAttribute(`tabindex`,`-1`),e?.focus({preventScroll:!0})}return}if(e.target.closest(`[data-prep-analysis]`)&&A[0]){let e=A[0].id;_.querySelector(`.prep-analysis`)?.replaceWith(X(ta(A[0],{loading:!0})));try{let t=await ra(e,{force:!0});if(A[0]?.id!==e)return;_.querySelector(`.prep-analysis`)?.replaceWith(X(ta(A[0],{analysis:t})))}catch{_.querySelector(`.prep-analysis`)?.replaceWith(X(ta(A[0],{error:!0})))}return}if(e.target.closest(`[data-prep-resume-regenerate]`)&&A[0]){let e=A[0].id,t=_.querySelector(`.prep-resume`),n=t?.querySelector(`[data-prep-resume-tweaks="${e}"]`)?.value??``,r=t?.querySelector(`[data-prep-resume-latex="${e}"]`)?.value??``;if(!n.trim()){t?.querySelector(`[data-prep-resume-tweaks="${e}"]`)?.focus();return}It.set(e,n),t?.replaceWith(X(Xi(A[0],{loading:!0})));try{let t=await la(e,n,r);M.set(e,t.resume),_.querySelector(`.prep-resume`)?.replaceWith(X(Xi(A[0],{resume:t.resume}))),yn()}catch{_.querySelector(`.prep-resume`)?.replaceWith(X(Xi(A[0],{resume:M.get(e),tweaks:n}))),yn()}return}if(e.target.closest(`[data-prep-cover-letter]`)&&A[0]){let e=A[0].id,t=_.querySelector(`.prep-cover-letter`),n=t?.querySelector(`[data-prep-cover-letter-tweaks="${e}"]`)?.value??``,r=n.trim()?t?.querySelector(`[data-prep-cover-letter-latex="${e}"]`)?.value??``:``;t?.replaceWith(X(ea(A[0],{loading:!0})));try{let t=await ma(e,n,r);N.set(e,t.cover_letter),_.querySelector(`.prep-cover-letter`)?.replaceWith(X(ea(A[0],{coverLetter:t.cover_letter}))),yn()}catch{_.querySelector(`.prep-cover-letter`)?.replaceWith(X(ea(A[0],{coverLetter:N.get(e),tweaks:n}))),yn()}return}let n=e.target.closest(`[data-prep-action]`);if(n){ia(n.dataset.prepAction);return}let r=e.target.closest(`[data-prep-feedback]`);if(!r||!A[0])return;let i=A[0].id,a=j.get(i),o=Array.isArray(a?.feedback_items)?a.feedback_items.length:0,s=Ft.get(i)??0;if(r.dataset.prepFeedback===`accept`||r.dataset.prepFeedback===`ignore`){let e=a?.feedback_items?.[s];if(!e)return;let t=_.querySelector(`[data-prep-feedback-comment]`)?.value??``,n=r.dataset.prepFeedback,o=n;r.disabled=!0,r.textContent=n===`accept`?`adding...`:`ignoring...`;try{if(n===`accept`){let n=await aa(i,s,e,t),r=document.querySelector(`.job[data-role-id="${CSS.escape(String(i))}"]`);n.role&&(A[0]=n.role,yi(n.role,r)),to(i,n.tweak_prompt??e.tweak_prompt??``),eo(i,s,a)}else await oa(i,s,e,t),eo(i,s,a)}catch{r.disabled=!1,r.textContent=o}return}let c=r.dataset.prepFeedback===`next`?1:-1;Ft.set(i,Math.max(0,Math.min(s+c,o-1))),_.querySelector(`.prep-analysis`)?.replaceWith(X(ta(A[0],{analysis:a})))});function eo(e,t,n){let r=n.feedback_items.filter((e,n)=>n!==t),i=Math.min(t,Math.max(r.length-1,0)),a={...n,feedback_items:r,verdict:r.length===0?`ready_to_apply`:n.verdict};Ft.set(e,i),j.set(e,a),_.querySelector(`.prep-analysis`)?.replaceWith(X(ta(A[0],{analysis:a})))}function to(e,t){let n=String(t||``).trim();if(!n)return;let r=It.get(e)?.trim()??``,i=r?`${r}\n\n${n}`:n;It.set(e,i);let a=_.querySelector(`[data-prep-resume-tweaks="${e}"]`);a&&(a.value=i,a.focus())}document.addEventListener(`keydown`,e=>{e.key===`Escape`&&!Le.hidden&&er(),e.key===`Escape`&&!o.hidden&&hn(),e.key===`Escape`&&!h.hidden&&Ai(),e.key===`Escape`&&!g.hidden&&Mi(),e.key===`Escape`&&!De.hidden&&Ea(),e.key===`Escape`&&!Ge.hidden&&dr(),e.key===`Escape`&&!ot.hidden&&br(),e.key===`Escape`&&!pt.hidden&&kr(),e.key===`Escape`&&!yt.hidden&&Gr()}),Ie.addEventListener(`click`,$n),ze.addEventListener(`click`,er),Re.addEventListener(`click`,er);function no(){return Array.from(document.querySelectorAll(`.pane-toggle`))}function ro(){return no().some(e=>e.getAttribute(`aria-expanded`)===`true`)}function io(){Ve.textContent=ro()?`collapse all`:`expand all`}function ao(){document.querySelectorAll(`.pane-toggle`).forEach(e=>{e.setAttribute(`aria-expanded`,`true`),e.querySelector(`.chevron`).textContent=`v`,e.parentElement.querySelector(`.pane-body`).hidden=!1})}function oo(){document.querySelectorAll(`.job[open]`).forEach(e=>{e.open=!1}),document.querySelectorAll(`.pane-toggle`).forEach(e=>{e.setAttribute(`aria-expanded`,`false`),e.querySelector(`.chevron`).textContent=`>`,e.parentElement.querySelector(`.pane-body`).hidden=!0})}Ve.addEventListener(`click`,()=>{ro()?oo():ao(),io()}),He.addEventListener(`click`,()=>{Mt=!Mt,He.textContent=Mt?`show empty`:`hide empty`,T&&zn(T.statuses)}),We.addEventListener(`click`,ur),Je.addEventListener(`click`,pr),Ke.addEventListener(`click`,dr),at.addEventListener(`click`,yr),st.addEventListener(`click`,br),ft.addEventListener(`click`,Or),mt.addEventListener(`click`,kr),Ne.addEventListener(`click`,Wr),bt.addEventListener(`click`,Gr),xt.addEventListener(`submit`,e=>{e.preventDefault(),Jr(xt).catch(()=>{C.textContent=`could not add company.`})}),St.addEventListener(`submit`,e=>{e.preventDefault(),$r(St).catch(()=>{Et.textContent=`could not add role.`})}),w.addEventListener(`submit`,e=>{let t=e.target.closest(`[data-company-link-form]`);t&&(e.preventDefault(),Yr(t).catch(()=>{C.textContent=`could not add link.`}))}),w.addEventListener(`input`,e=>{let t=e.target.closest(`[data-company-notes]`);t&&ni(t.dataset.companyNotes)}),w.addEventListener(`change`,e=>{let t=e.target.closest(`[data-company-tier]`);if(!t)return;let n=t.closest(`.company-panel`);n&&ii(n,t.value),window.clearTimeout(dn.get(t.dataset.companyTier)),ri(t.dataset.companyTier).catch(()=>{ti(`could not save company.`)})}),w.addEventListener(`click`,e=>{let t=e.target.closest(`[data-delete-company]`);if(t){let e=ei(t.dataset.deleteCompany),n=e?.name?K(e.name):`this company`;if(!window.confirm(`Deactivate ${n}? It will be hidden from company counts and skipped during scans.`))return;t.disabled=!0,Zr(t.dataset.deleteCompany).catch(()=>{C.textContent=`could not deactivate company.`,t.disabled=!1});return}let n=e.target.closest(`[data-delete-career-page]`);if(!n)return;let r=n.closest(`.company-link-row`)?.querySelector(`.company-link-text`)?.textContent?.trim();window.confirm(`Delete ${r||`this career link`}?`)&&(n.disabled=!0,Xr(n.dataset.deleteCareerPage).catch(()=>{C.textContent=`could not delete link.`,n.disabled=!1}))}),S.addEventListener(`change`,e=>{let t=e.target.closest(`input[type="checkbox"], select, input[data-setting-text], textarea[data-setting-textarea]`);t&&jr(t)}),S.addEventListener(`click`,async e=>{let t=e.target.closest(`[data-application-runtime-test]`);if(!t||t.disabled)return;let n=t.dataset.applicationRuntimeTest,r=S.querySelector(`[data-application-runtime-test-status="${CSS.escape(n)}"]`);t.disabled=!0,t.textContent=`Testing…`,r&&(r.textContent=`Creating a bounded Callumployed session…`);try{let e=await fetch(`/api/application-generation/backends/${encodeURIComponent(n)}/test`,{method:`POST`}),t=await e.json();if(!e.ok||t?.ok!==!0)throw Error(t?.error||`Connection test failed.`);r&&(r.textContent=t.message||`Connection succeeded.`)}catch(e){r&&(r.textContent=e instanceof Error?e.message:`Connection test failed.`)}finally{t.disabled=!1,t.textContent=`Test connection`}}),S.addEventListener(`submit`,async e=>{e.preventDefault();let t=S.querySelector(`button[type="submit"]`),n=S.querySelectorAll(`input[type="checkbox"][name], select[name], input[data-setting-text][name], textarea[data-setting-textarea][name]`),r={};n.forEach(e=>{let t=e.name;t&&(r[t]=e.type===`checkbox`?e.checked:e.value)}),t.disabled=!0,t.textContent=`saving...`;try{x.textContent=`saving settings...`;let e=await fetch(`/api/config`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(r)});if(!e.ok)throw Error(`Config update failed`);J(await e.json(),`settings saved.`)}catch{x.textContent=`could not save settings.`,x.classList.remove(`is-empty`)}finally{t.disabled=!1,t.textContent=`save settings`}}),$e.addEventListener(`input`,()=>{nt.disabled=!$e.value.trim()}),tt.addEventListener(`click`,Nr),nt.addEventListener(`click`,Pr),it.addEventListener(`click`,Mr),vt.addEventListener(`click`,Lr);function so(){if(window.location.hash===`#prepped-roles`){Ta();return}Ea({clearHash:!1})}window.addEventListener(`popstate`,so),Ir(),window.location.hash===`#prepped-roles`&&so(),di({applyDefaultCollapsed:!0}).catch(()=>{En(null,`could not load resume.`),On([],`could not load cover letter examples.`),Nn()}),oi().then(()=>{si()}).catch(()=>{Pe.textContent=`could not load scan status`});