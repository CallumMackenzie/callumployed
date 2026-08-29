import{t as e}from"./preload-helper-Czpn1I53.js";var{sankey:t,sankeyLinkHorizontal:n}=await e(async()=>{let{sankey:e,sankeyLinkHorizontal:t}=await import(`/assets/d3-sankey.js`);return{sankey:e,sankeyLinkHorizontal:t}},[]),r=document.querySelector(`#stats`),i=document.querySelector(`#status-list`),a=document.querySelector(`#search-toggle`),o=document.querySelector(`#search-dialog`),s=document.querySelector(`#search-backdrop`),c=document.querySelector(`#search-form`),l=document.querySelector(`#search-input`),u=document.querySelector(`#close-search`),d=document.querySelector(`#materials-panel`),ee=document.querySelector(`#materials-toggle`),f=document.querySelector(`#materials-body`),te=document.querySelector(`#materials-summary`),p=document.querySelector(`#materials-required-warning`),m=document.querySelector(`#resume-meta`),h=document.querySelector(`#resume-upload`),ne=document.querySelector(`#resume-upload-button`),re=document.querySelector(`#resume-resource-meta`),ie=document.querySelector(`#resume-resource-upload`),ae=document.querySelector(`#resume-resource-upload-button`),oe=document.querySelector(`#resume-resource-list`),se=document.querySelector(`#cover-letter-meta`),ce=document.querySelector(`#cover-letter-upload`),le=document.querySelector(`#cover-letter-upload-button`),ue=document.querySelector(`#cover-letter-list`),de=document.querySelector(`#experience-note-meta`),fe=document.querySelector(`#experience-note-upload`),pe=document.querySelector(`#experience-note-upload-button`),me=document.querySelector(`#experience-note-list`);document.querySelector(`#material-index-button`);var he=document.querySelector(`#material-index-warning`),ge=document.querySelector(`#material-index-status`),_e=document.querySelector(`#review-discovered`),ve=document.querySelector(`#prep-interested`),g=document.querySelector(`#review-view`),ye=document.querySelector(`#review-heading`),be=document.querySelector(`#review-progress`),xe=document.querySelector(`#review-card`),Se=document.querySelector(`#close-review`),_=document.querySelector(`#prep-view`),Ce=document.querySelector(`#prep-heading`),we=document.querySelector(`#prep-progress`),v=document.querySelector(`#prep-card`),Te=document.querySelector(`#close-prep`),Ee=document.querySelector(`#prepped-roles`),De=document.querySelector(`#prepped-view`),Oe=document.querySelector(`#close-prepped`),ke=document.querySelector(`#prepped-summary`),Ae=document.querySelector(`#regenerate-all-cover-letters`),je=document.querySelector(`#prepped-bulk-status`),Me=document.querySelector(`#prepped-list`),Ne=document.querySelector(`#prepped-detail`),y=document.querySelector(`#scan-all-button`),Pe=document.querySelector(`#manage-companies-button`),b=document.querySelector(`#scan-status-bar`),x=document.querySelector(`#scan-status-text`),Fe=document.querySelector(`#scan-last-time`),Ie=document.querySelector(`#scan-failures-open`),Le=document.querySelector(`#scan-failures-dialog`),Re=document.querySelector(`#scan-failures-backdrop`),ze=document.querySelector(`#scan-failures-close`),Be=document.querySelector(`#scan-failures-list`),Ve=document.querySelector(`#toggle-all`),He=document.querySelector(`#collapse-empty`),Ue=document.querySelector(`#toolbar-summary`),We=document.querySelector(`#settings-open`),Ge=document.querySelector(`#settings-view`),Ke=document.querySelector(`#settings-close`),S=document.querySelector(`#settings-status`),qe=document.querySelector(`#settings-form`),Je=document.querySelector(`#settings-profile-options`),Ye=document.querySelector(`#settings-autoprep-options`),Xe=document.querySelector(`#settings-options`),Ze=document.querySelector(`#central-store-summary`),Qe=document.querySelector(`#central-store-sync-summary`),$e=document.querySelector(`#central-api-url-input`),et=document.querySelector(`#central-passkey-input`),tt=document.querySelector(`#central-save-button`),nt=document.querySelector(`#central-sync-button`),rt=document.querySelector(`#recommendation-history-summary`),it=document.querySelector(`#clear-recommendation-history`),at=document.querySelector(`#metrics-open-button`),ot=document.querySelector(`#metrics-view`),st=document.querySelector(`#metrics-close`),ct=document.querySelector(`#metrics-status`),lt=document.querySelector(`#metrics-overview`),ut=document.querySelector(`#metrics-sections`),dt=document.querySelector(`#metrics-scan-list`),ft=document.querySelector(`#sankey-open-button`),pt=document.querySelector(`#sankey-view`),mt=document.querySelector(`#sankey-close`),ht=document.querySelector(`#sankey-status`),gt=document.querySelector(`#sankey-canvas`),_t=document.querySelector(`#sankey-path-list`),vt=document.querySelector(`#app-update-button`),yt=document.querySelector(`#companies-view`),bt=document.querySelector(`#companies-close`),C=document.querySelector(`#companies-status`),xt=document.querySelector(`#company-create-form`),w=document.querySelector(`#companies-list`),St=document.querySelector(`#role-add-form`),Ct=document.querySelector(`#role-url-input`),wt=document.querySelector(`#role-company-input`),Tt=document.querySelector(`#role-company-options`),Et=document.querySelector(`#role-add-status`),Dt=3,Ot=1200,kt=new Set([`applied`,`OA`,`interview`,`rejected`,`offer`]),At=new Map([[`discovered`,`#4f6472`],[`interested`,`#00897b`],[`disinterested`,`#626970`],[`applied`,`#2257ad`],[`oa`,`#b36b00`],[`interview`,`#5f2bd8`],[`rejected`,`#b93d2d`],[`offer`,`#137347`],[`closed`,`#53606b`],[`archived`,`#765b4a`]]),jt=/^(?:about (?:the )?(?:role|team|job)|about this role|job description|job responsibilities|minimum qualifications|preferred qualifications|qualifications|requirements|responsibilities|what to expect|what (?:you'll|you’ll|you will) (?:bring|do)|what'?s in it for you|who you are|your objectives|your skills & talents):?$/i,Mt=!0,T=null,Nt=null,E=[],D=[],O=[],Pt=null,k=[],A=[],Ft=new Map,It=new Map,j=new Map,Lt=new Map,M=new Map,Rt=new Map,zt=new Map,Bt=new Map,N=[],P=null,Vt=null,Ht=!1,Ut=``,F=null,Wt=new Set,Gt=new Map,I=new Set,L=new Map,Kt=new Map,qt=new Map,Jt=new Set,Yt=!1,Xt=0,Zt=null,Qt=!1,$t=null,en=null,tn=null,nn=null,R=null,rn=[],an=new Map;function z(){return T?.query?.trim()??``}function on(){let e=!!z();a.classList.toggle(`search-active`,e),a.setAttribute(`aria-label`,e?`clear search`:`search jobs`)}function sn(){l.value=z(),o.hidden=!1,c.hidden=!1,l.focus(),l.select()}function cn(){o.hidden=!0,c.hidden=!0,a.focus()}function ln(e){return e?new Intl.DateTimeFormat(void 0,{month:`short`,day:`numeric`,hour:`numeric`,minute:`2-digit`}).format(new Date(e)).toLocaleLowerCase():``}function B(e){return e?new Intl.DateTimeFormat(void 0,{month:`short`,day:`numeric`,hour:`numeric`,minute:`2-digit`}).format(new Date(e)).replace(`, `,` `).toLocaleLowerCase():``}function V(e){return String(e??``).replaceAll(`&`,`&amp;`).replaceAll(`<`,`&lt;`).replaceAll(`>`,`&gt;`).replaceAll(`"`,`&quot;`).replaceAll(`'`,`&#039;`)}function H(e){return String(e??``).toLocaleLowerCase()}function U(e){return V(H(e))}function un(e){try{let t=new URL(String(e||``));return[`http:`,`https:`].includes(t.protocol)?t.href:``}catch{return``}}function dn(e){return e}function W(e=v){e.querySelectorAll(`[data-prep-resume-latex], [data-prep-cover-letter-latex]`).forEach(dn)}function fn(){return`
    <svg class="role-link-icon" viewBox="0 0 24 24" aria-hidden="true">
      <path d="M7 17 17 7"></path>
      <path d="M8 7h9v9"></path>
    </svg>
  `}function pn(){return`
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M12 5v14"></path>
      <path d="M5 12h14"></path>
    </svg>
  `}function mn(){return`
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M3 6h18"></path>
      <path d="M8 6V4h8v2"></path>
      <path d="m19 6-1 14H6L5 6"></path>
      <path d="M10 11v5"></path>
      <path d="M14 11v5"></path>
    </svg>
  `}function hn(e,t,n){let r=`<span class="role-title-text">${U(e)}</span>`;return t?`<a class="${n}" href="${V(t)}" target="_blank" rel="noreferrer">${r}${fn()}</a>`:`<span class="${n}">${r}</span>`}function gn(e){r.innerHTML=[[`companies`,e.companies_total],[`jobs`,e.jobs_total],[`applications`,e.applications_total]].map(([e,t])=>`<dl class="stat"><dt>${U(e)}</dt><dd>${t}</dd></dl>`).join(``)}function _n(e=T){if(!e){Ue.innerHTML=``;return}let t=t=>e.statuses.find(e=>e.key===t)?.count??0;Ue.innerHTML=[[`discovered`,t(`discovered`)],[`interested`,t(`interested`)],[`applied`,e.stats?.applications_total??0],[`total`,e.stats?.jobs_total??0]].map(([e,t])=>`
        <dl>
          <dt>${U(e)}</dt>
          <dd>${t}</dd>
        </dl>
      `).join(``)}function vn(e,t=``){if(Nt=e,ne.textContent=e?`replace`:`upload`,t){m.textContent=t;return}if(!e){m.textContent=`no resume uploaded`;return}let n=B(e.updated_at),r=Dn(e.content_bytes);m.textContent=[H(e.filename),r,n].filter(Boolean).join(` | `)}function yn(e,t,n,{binary:r=!1}={}){let i=r?e.filename:e.id;return`
    <li class="material-source-item" title="${U(e.filename)}">
      <div class="material-source-copy">
        <span>${U(e.filename)}</span>
        <small>${V(n)}</small>
      </div>
      <div class="material-source-actions">
        <button type="button" class="material-source-view" data-material-view="${V(t)}" data-material-id="${V(i)}" data-material-binary="${r}">preview</button>
        <button type="button" class="material-source-remove" data-material-remove="${V(t)}" data-material-id="${V(i)}" data-material-name="${U(e.filename)}">remove</button>
      </div>
      <div class="material-source-preview" data-material-preview-body hidden></div>
    </li>`}function bn(e,t=``){D=Array.isArray(e)?e:[],le.textContent=D.length>0?`add`:`upload`,se.textContent=t||(D.length===0?`no examples uploaded`:`${D.length} ${D.length===1?`example`:`examples`} stored`),ue.innerHTML=D.map(e=>yn(e,`cover-letter-examples`,Dn(e.content_bytes))).join(``)}function xn(e,t=``){O=Array.isArray(e)?e:[],pe.textContent=O.length>0?`add`:`upload`,de.textContent=t||(O.length===0?`no notes uploaded`:`${O.length} ${O.length===1?`note`:`notes`} stored`),me.innerHTML=O.map(e=>yn(e,`experience-notes`,Dn(e.content_bytes))).join(``)}function Sn(e,t=``){Pt=e??null;let n=Pt?.status??`missing`,r=n!==`ready`;if(O.length,he.hidden=!r,he.textContent=t||Pt?.warning||``,t)ge.textContent=t;else if(n===`ready`){let e=Number(Pt?.document_count??0),t=Number(Pt?.skipped_source_count??0),n=B(Pt?.generated_at);ge.innerHTML=[`${e} indexed ${e===1?`page`:`pages`}`,t?`${t} unreadable upload skipped`:``,n].filter(Boolean).map(e=>`<button type="button" class="material-index-link" data-open-material-index title="Reveal the application material index in Finder">${U(e)}</button>`).join(`<span aria-hidden="true"> | </span>`)}else ge.textContent=n===`stale`?`index out of date`:`not indexed`}function Cn(e,t=``){E=Array.isArray(e)?e:[],ae.textContent=E.length>0?`add`:`upload`,re.textContent=t||(E.length===0?`no resources uploaded`:`${E.length} ${E.length===1?`resource`:`resources`} stored`),oe.innerHTML=E.map(e=>yn(e,`resume-resources`,Dn(e.bytes),{binary:!0})).join(``)}function wn(e,t={}){Xt+=1,document.querySelectorAll(`[data-preview-blob-url]`).forEach(e=>{URL.revokeObjectURL(e.dataset.previewBlobUrl)}),vn(e?.master_resume??null),Cn(e?.resume_resources??[]),bn(e?.cover_letter_examples??[]),xn(e?.experience_notes??[]),Sn(e?.material_index??null),Tn(e?.ui),(!Yt||t.applyDefaultCollapsed)&&(En(!!e?.ui?.default_collapsed),Yt=!0)}function Tn(e=null){let t=Nt?`resume ready`:`no resume`,n=E.length===0?`no resources`:`${E.length} ${E.length===1?`resource`:`resources`}`,r=D.length,i=r===0?`no cover letters`:`${r} cover ${r===1?`letter`:`letters`}`,a=O.length,o=a===0?`no notes`:`${a} experience ${a===1?`note`:`notes`}`;p.hidden=!(typeof e?.has_missing_required_materials==`boolean`?e.has_missing_required_materials:!Nt||r===0||a===0),te.textContent=`${t} | ${n} | ${i} | ${o}`}function En(e){d.classList.toggle(`collapsed`,e),ee.setAttribute(`aria-expanded`,String(!e)),ee.querySelector(`.materials-chevron`).textContent=e?`>`:`v`,f.hidden=e}function Dn(e){return Number.isFinite(e)?e<1024?`${e} b`:`${Math.round(e/1024)} kb`:``}async function On(e){let t=await fetch(e,{cache:`no-store`});if(!t.ok)throw Error(`Preview unavailable`);let n=await t.arrayBuffer();if(new TextDecoder(`ascii`).decode(n.slice(0,5))!==`%PDF-`)throw Error(`The selected file is not a readable PDF.`);return URL.createObjectURL(new Blob([n],{type:`application/pdf`}))}async function kn(e){let t=e.closest(`.material-source-item`)?.querySelector(`[data-material-preview-body]`);if(!t)return;if(t.dataset.loaded===`true`){t.hidden=!t.hidden,e.textContent=t.hidden?`preview`:`hide`;return}e.disabled=!0,e.textContent=`loading...`;let n=e.dataset.materialView,r=e.dataset.materialId,i=Xt,a=`/api/${encodeURIComponent(n)}/${encodeURIComponent(r)}`;try{if(e.dataset.materialBinary===`true`){let e=await On(a);if(!t.isConnected||Xt!==i){URL.revokeObjectURL(e);return}t.dataset.previewBlobUrl=e,t.innerHTML=`<iframe title="${U(r)} preview"></iframe>`,t.querySelector(`iframe`).src=e}else{let e=await fetch(a);if(!e.ok)throw Error(`Preview unavailable`);let n=await e.json(),r=document.createElement(`pre`);r.textContent=n.content||`This source is empty.`,t.replaceChildren(r)}t.dataset.loaded=`true`,t.hidden=!1,e.textContent=`hide`}catch(n){t.textContent=n instanceof Error?n.message:`Preview unavailable`,t.hidden=!1,e.textContent=`preview`}finally{e.disabled=!1}}async function An(e){let t=e.dataset.materialRemove,n=e.dataset.materialId;if(e.dataset.confirmRemove!==`true`){e.dataset.confirmRemove=`true`,e.textContent=`confirm remove`,e.classList.add(`danger`),window.setTimeout(()=>{!e.isConnected||e.disabled||(delete e.dataset.confirmRemove,e.textContent=`remove`,e.classList.remove(`danger`))},6e3);return}e.disabled=!0,e.textContent=`removing...`;try{let e=await fetch(`/api/${encodeURIComponent(t)}/${encodeURIComponent(n)}`,{method:`DELETE`}),r=await e.json();if(!e.ok)throw Error(r.error||`Remove failed`);wn(r)}catch(t){e.disabled=!1,delete e.dataset.confirmRemove,e.classList.remove(`danger`),e.textContent=`remove`,window.alert(t instanceof Error?t.message:`Remove failed`)}}function jn(e){i.innerHTML=e.map(e=>{let t=e.jobs.map(t=>Mn(t,e.key)).join(``);return`
        <section class="status-pane ${e.count===0?`empty`:``} ${Mt?`hidden-empty`:``}" id="status-${V(e.key)}" data-bucket="${V(e.key)}">
          <button class="pane-toggle" type="button" aria-expanded="false">
            <span class="chevron">></span>
            <span class="pane-title">${U(e.label)}</span>
            <span class="count">${e.count}</span>
          </button>
          <div class="pane-body" hidden>
            ${t?`<div class="jobs">${t}</div>`:`<p class="empty-copy">no jobs in this status.</p>`}
          </div>
        </section>
      `}).join(``)}function Mn(e,t){return`
    <details class="job" data-role-id="${V(e.id)}">
      <summary class="job-summary">
        <span class="job-chevron">></span>
        <span class="job-identity">
          <span class="job-company">[${U(e.company_name)}]</span>
          ${hn(e.title,e.role_url,`job-title`)}
          ${t===`interested`&&e.prep_started?Fn():``}
          ${t===`closed`&&e.updated_in_latest_scan?Nn():``}
          ${[`discovered`,`interested`].includes(t)&&e.missing_from_latest_scan?Pn():``}
        </span>
      </summary>
      <div class="job-detail">
        ${t===`discovered`?In(e):``}
        ${t===`interested`?Ln(e):``}
        ${t===`disinterested`?Rn(e):``}
        ${t===`applied`?zn(e):``}
        ${t===`OA`?Bn(e):``}
        ${t===`interview`?Vn(e):``}
        ${t===`closed`?Hn(e):``}
        <dl>
          ${e.location?`<div>
                  <dt>location</dt>
                  <dd>${U(e.location)}</dd>
                </div>`:``}
          <div>
            <dt>updated</dt>
            <dd>${ln(e.updated_at)}</dd>
          </div>
        </dl>
      </div>
    </details>
  `}function Nn(){return`<span class="latest-scan-dot" title="updated in latest scan" aria-label="updated in latest scan"></span>`}function Pn(){return`<span class="missing-latest-scan-dot" title="not seen in latest scan" aria-label="not seen in latest scan"></span>`}function Fn(){return`<span class="prep-started-dot" title="application materials started" aria-label="application materials started"></span>`}function In(e){return`
    <div class="job-actions job-actions-nowrap" aria-label="discovered role actions">
      <button class="job-action success" type="button" data-review-role-id="${e.id}">view</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="interested">interested</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="disinterested">disinterested</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="closed">closed</button>
    </div>
  `}function Ln(e){return`
    <div class="job-actions" aria-label="interested role actions">
      <button class="job-action success" type="button" data-prep-role-id="${e.id}">prep</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="applied">applied</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="disinterested">disinterested</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="closed">closed</button>
    </div>
  `}function Rn(e){return`
    <div class="job-actions" aria-label="disinterested role actions">
      <button class="job-action success" type="button" data-role-id="${e.id}" data-status="interested">interested</button>
    </div>
  `}function zn(e){return`
    <div class="job-actions job-actions-nowrap" aria-label="applied role actions">
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="OA">oa</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="interview">interview</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="rejected">rejected</button>
    </div>
  `}function Bn(e){return`
    <div class="job-actions job-actions-nowrap" aria-label="oa role actions">
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="interview">interview</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="disinterested">disinterested</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="rejected">rejected</button>
    </div>
  `}function Vn(e){return`
    <div class="job-actions" aria-label="interview role actions">
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="rejected">rejected</button>
      <button class="job-action success" type="button" data-role-id="${e.id}" data-status="offer">offer</button>
    </div>
  `}function Hn(e){return`
    <div class="job-actions" aria-label="closed role actions">
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="interested">interested</button>
    </div>
  `}function Un(e){T=e,l.value=e.query,on(),gn(e.stats),_n(e),jn(e.statuses),ja(),pi(e.statuses),hi(e.statuses)}function Wn(e){$t=e??null;let t=!!e?.scanning,n=t&&!!e?.cancel_requested,r=Number(e?.completed_companies??0),i=Number(e?.total_companies??0),a=Number(e?.failed_companies??0),o=typeof e?.error==`string`?e.error.trim():``,s=Array.isArray(e?.failures)?e.failures:[];y.disabled=n,y.textContent=t?n?`cancelling...`:`cancel scan`:`scan roles`,y.classList.toggle(`danger`,t&&!n),b.hidden=!t&&!o&&s.length===0,b.classList.toggle(`scanning`,t),b.classList.toggle(`scan-error`,!t&&!!o||s.length>0),x.textContent=n?`cancelling scan...`:t?`scanning roles${i>0?` ${r}/${i}`:``}${a>0?`, ${a} failed`:``}`:s.length>0?`${s.length} recent scan ${s.length===1?`failure`:`failures`}`:o?`last scan error: ${o}`:`scan idle`,Ie&&Be&&(Ie.hidden=s.length===0,Be.innerHTML=s.slice(0,5).map(e=>{let t=e?.company_name||`unknown company`,n=e?.error||`scan failed`;return`
          <p>
            <span>${U(t)}</span>
            <span>${V(n)}</span>
          </p>
        `}).join(``),s.length===0&&Kn());let c=e?.last_scan_at;Fe.textContent=c?`last scan: ${B(c)}`:`last scan: never`,Qt&&!t&&q(z()).catch(()=>{}),Qt=t}function Gn(){Ie.hidden||(Le.hidden=!1,ze.focus())}function Kn(){Le.hidden=!0}function G(e,t=``){en=e;let n=Array.isArray(e?.settings)?e.settings:[],r=n.filter(e=>e.key?.startsWith(`applicant_`)),i=n.filter(e=>e.key?.startsWith(`autoprep_`)),a=n.filter(e=>!e.key?.startsWith(`applicant_`)&&!e.key?.startsWith(`autoprep_`)),o=e?.central??{};S.textContent=t,S.classList.toggle(`is-empty`,!t);let s=Number(e?.recommendation_history_count??0);rt.textContent=s>0?`${s} saved ${s===1?`feedback decision`:`feedback decisions`}`:`no saved resume feedback decisions`,it.disabled=s===0,qn(o),Je.innerHTML=r.map(e=>Jn(e)).join(``),Ye.innerHTML=i.map(e=>Jn(e)).join(``),Xe.innerHTML=a.map(e=>Jn(e)).join(``),K(!1)}function qn(e){let t=e?.api_url??``;$e.value=t,et.value=``;let n=e?.passkey_configured?`passkey saved`:`no passkey saved`;Ze.textContent=t?`${H(t)} | ${n}`:`no api url | ${n}`,Qe.textContent=`${Number(e?.companies_linked??0)} linked | ${Number(e?.companies_unlinked??0)} unlinked | ${Number(e?.companies_needs_review??0)} review | ${Number(e?.companies_failed??0)} failed`,nt.disabled=!t}function Jn(e){if(e.control===`textarea`&&e.editable!==!1)return Xn(e);if(e.control===`text`&&e.editable!==!1)return Yn(e);if(e.control===`select`&&e.editable!==!1)return Zn(e);if(e.control!==`toggle`||e.editable===!1)return Qn(e);let t=e.value?`checked`:``,n=e.default?`on by default`:`off by default`;return`
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
  `}function Yn(e){let t=e.default?`default: ${H(e.default)}`:`optional`,n=e.input_type??`text`,r=e.autocomplete??`name`;return`
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
  `}function Xn(e){return`
    <label class="setting-option setting-option-prompt">
      <span class="setting-copy">
        <span class="setting-label">${U(e.label)}</span>
        <span class="setting-description">${U(e.description)}</span>
      </span>
      <textarea
        class="setting-prompt-input"
        data-setting-textarea
        name="${V(e.key)}"
        rows="7"
        maxlength="8000"
      >${U(e.value??``)}</textarea>
    </label>
  `}function Zn(e){let t=Array.isArray(e.options)?e.options:[],n=`default: ${H(e.default)}`;return`
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
  `}function Qn(e){let t=e.default?`on by default`:`off by default`,n=e.value?`automatic`:`off`;return`
    <div class="setting-option setting-option-readonly">
      <span class="setting-copy">
        <span class="setting-label">${U(e.label)}</span>
        <span class="setting-description">${U(e.description)}</span>
        <span class="setting-default">${U(t)}</span>
      </span>
      <span class="setting-badge">${U(n)}</span>
    </div>
  `}function K(e){qe.querySelectorAll(`input, select, textarea`).forEach(t=>{t.disabled=e}),tt.disabled=e,nt.disabled=e||!$e.value.trim(),vt.disabled=e}async function $n(){Ge.hidden=!1,document.body.classList.add(`settings-open`),Ke.focus(),en?G(en):(S.textContent=`loading settings...`,S.classList.remove(`is-empty`),Xe.innerHTML=``);try{await tr()}catch{S.textContent=`could not load settings.`}}function er(){Ge.hidden=!0,document.body.classList.remove(`settings-open`),We.focus()}async function tr(){let e=await fetch(`/api/config`);if(!e.ok)throw Error(`Config request failed`);G(await e.json())}function nr(e){let t=e?.value;return t==null?`n/a`:e?.kind===`ratio`?Number(t).toLocaleString(void 0,{maximumFractionDigits:2,minimumFractionDigits:0}):typeof t==`number`?t.toLocaleString():H(t)}function rr(e,t=`metric-card`){return`
    <article class="${t}">
      <span>${U(e?.label)}</span>
      <strong>${V(nr(e))}</strong>
    </article>
  `}function ir(e,t=``){tn=e,ct.textContent=t||(e?.updated_at?`updated ${B(e.updated_at)}`:``),ct.classList.toggle(`is-empty`,!ct.textContent);let n=Array.isArray(e?.overview)?e.overview:[],r=Array.isArray(e?.sections)?e.sections:[],i=Array.isArray(e?.recent_scans)?e.recent_scans:[];lt.innerHTML=n.map(e=>rr(e)).join(``),ut.innerHTML=r.map(ar).join(``),dt.innerHTML=i.length?i.map(or).join(``):`<p class="empty-copy">no scan runs recorded.</p>`}function ar(e){let t=Array.isArray(e?.metrics)?e.metrics:[];return`
    <section class="metrics-section">
      <div class="metrics-section-heading">
        <h3>${U(e?.title)}</h3>
      </div>
      <div class="metrics-section-grid">
        ${t.map(e=>rr(e,`metric-card metric-card-compact`)).join(``)}
      </div>
    </section>
  `}function or(e){let t=e?.scan_status??`unknown`,n=e?.started_at?B(e.started_at):`not started`,r=e?.finished_at?B(e.finished_at):`not finished`,i=e?.error?`<span>${U(e.error)}</span>`:``;return`
    <article class="metrics-scan-row">
      <div>
        <strong>${U(e?.company_name??`unknown company`)}</strong>
        <span>${U(n)} -> ${U(r)}</span>
        ${i}
      </div>
      <span class="metrics-status-pill">${U(t)}</span>
    </article>
  `}async function sr(){ot.hidden=!1,document.body.classList.add(`metrics-open`),st.focus(),tn?ir(tn):(ct.textContent=`loading metrics...`,ct.classList.remove(`is-empty`),lt.innerHTML=``,ut.innerHTML=``,dt.innerHTML=``);try{await lr()}catch{ct.textContent=`could not load metrics.`}}function cr(){ot.hidden=!0,document.body.classList.remove(`metrics-open`),at.focus()}async function lr(){let e=await fetch(`/api/metrics`);if(!e.ok)throw Error(`Metrics request failed`);ir(await e.json())}function ur(e,t=``){nn=e;let n=Number(e?.role_count??0),r=Array.isArray(e?.links)?e.links:[],i=Array.isArray(e?.paths)?e.paths:[];ht.textContent=t||(e?.updated_at?`${n.toLocaleString()} roles | updated ${B(e.updated_at)}`:``),ht.classList.toggle(`is-empty`,!ht.textContent),gt.innerHTML=r.length?dr(e):`<p class="empty-copy">no role transitions recorded yet.</p>`,_t.innerHTML=i.length?i.map(hr).join(``):`<p class="empty-copy">no role paths recorded yet.</p>`}function dr(e){let t=Array.isArray(e?.nodes)?e.nodes:[],n=Array.isArray(e?.links)?e.links:[],r=mr(t,n),i=r.nodes,a=r.links,o=(r.flowLinks??n).map(e=>{let t=i.get(e.source),n=i.get(e.target),r=a.get(e);if(!t||!n||!r)return``;let o=r.width,s=n.x<t.x,c=fr(e.target),l=r.priority?`0.42`:s?`0.28`:`0.34`,u=r.path??pr({isBacktrack:s,sourceX:t.x+t.width,sourceY:r.sourceY,targetX:n.x,targetY:r.targetY,width:o});return`
        <path class="${[`sankey-link`,s?`sankey-link-backtrack`:``,r.priority?`sankey-link-priority`:``].filter(Boolean).join(` `)}" d="${u}" fill="${r.path?`none`:c}" fill-opacity="${l}" stroke="${c}" style="stroke-width: ${r.path?o:1}px">
          <title>${U(t.label)} to ${U(n.label)}: ${Number(e.value??0).toLocaleString()}</title>
        </path>
      `}).join(``),s=Array.from(i.values()).map(e=>{let t=Number(e.history_count??e.current_count??0),n=Number(e.value??t),i=n>0?n.toLocaleString():`0`,a=e.x>r.width-180,o=a?e.x-8:e.x+e.width+8,s=Math.max(24,e.y-e.height/2-16),c=a?`end`:`start`,l=fr(e.id);return`
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
  `}function fr(e){return At.get(String(e).toLowerCase())??`#4f6472`}function pr({isBacktrack:e,sourceX:t,sourceY:n,targetX:r,targetY:i,width:a}){let o=a/2,s=n-o,c=n+o,l=i-o,u=i+o;if(e){let e=Math.max(80,Math.abs(t-r)*.42);return[`M ${t} ${s}`,`C ${t-e} ${s}, ${r+e} ${l}, ${r} ${l}`,`L ${r} ${u}`,`C ${r+e} ${u}, ${t-e} ${c}, ${t} ${c}`,`Z`].join(` `)}let d=Math.max(46,(r-t)*.48);return[`M ${t} ${s}`,`C ${t+d} ${s}, ${r-d} ${l}, ${r} ${l}`,`L ${r} ${u}`,`C ${r-d} ${u}, ${t+d} ${c}, ${t} ${c}`,`Z`].join(` `)}function mr(e,r){let i=new Map([[`discovered`,0],[`interested`,1],[`disinterested`,2],[`applied`,2],[`oa`,3],[`interview`,3],[`rejected`,4],[`closed`,4],[`archived`,4]]),a=new Map,o=new Map;r.forEach(e=>{a.set(e.target,(a.get(e.target)??0)+Number(e.value??0)),o.set(e.source,(o.get(e.source)??0)+Number(e.value??0))});let s=e.filter(e=>Number(e?.history_count??e?.current_count??0)>0||a.has(e.id)||o.has(e.id)),c=new Set(s.map(e=>e.id)),l=r.filter(e=>c.has(e.source)&&c.has(e.target)&&Number(e.value??0)>0),u=e=>i.get(String(e).toLowerCase())??0,d=l.filter(e=>u(e.target)>=u(e.source)),ee=l.filter(e=>u(e.target)<u(e.source)),f={nodes:s.map(e=>({...e,fixedValue:Math.max(0,Number(e?.history_count??e?.current_count??0))})),links:d.map(e=>({...e}))},te=t().nodeId(e=>e.id).nodeWidth(26).nodePadding(44).nodeAlign((e,t)=>Math.min(t-1,u(e.id))).extent([[92,88],[1014,634]]).iterations(32)(f),p=new Map;te.nodes.forEach(e=>{p.set(e.id,{...e,x:e.x0,y:e.y0+(e.y1-e.y0)/2,width:e.x1-e.x0,height:Math.max(1.5,e.y1-e.y0),value:Number(e.fixedValue??e.value??0)})});let m=new Map,h=[],ne=n();te.links.forEach(e=>{let t={source:e.source.id,target:e.target.id,value:e.value};h.push(t),m.set(t,{path:ne(e),width:Math.max(1.5,e.width),sourceY:e.y0,targetY:e.y1,priority:Number(e.value??0)>=20})});let re=Math.max(.6,...te.links.map(e=>Number(e.width??0)/Math.max(1,Number(e.value??0))));return ee.forEach(e=>{let t=p.get(e.source),n=p.get(e.target);if(!t||!n)return;let r=Math.max(1.5,Number(e.value??0)*re),i={...e};h.push(i),m.set(i,{width:r,sourceY:t.y+t.height/2-r/2,targetY:n.y+n.height/2-r/2,priority:!1})}),h.sort((e,t)=>Number(e.value??0)-Number(t.value??0)),{flowLinks:h,height:720,links:m,nodes:p,width:1120}}function hr(e){let t=Array.isArray(e?.path)?e.path:[];return`
    <article class="sankey-path-row">
      <div>
        <strong>${U(e?.company_name??`unknown company`)} / ${U(e?.title??`untitled role`)}</strong>
        <span>${t.map(e=>U(e)).join(` -> `)}</span>
      </div>
      <span class="metrics-status-pill">${Number(e?.loops_collapsed??0).toLocaleString()} loops</span>
    </article>
  `}async function gr(){Ge.hidden=!0,document.body.classList.remove(`settings-open`),pt.hidden=!1,document.body.classList.add(`sankey-open`),mt.focus(),nn?ur(nn):(ht.textContent=`loading role flow...`,ht.classList.remove(`is-empty`),gt.innerHTML=``,_t.innerHTML=``);try{await vr()}catch{ht.textContent=`could not load role flow.`}}function _r(){pt.hidden=!0,document.body.classList.remove(`sankey-open`),We.focus()}async function vr(){let e=await fetch(`/api/role-sankey`);if(!e.ok)throw Error(`Role sankey request failed`);ur(await e.json())}async function yr(e){let t=e.name;if(!t)return;let n=e.type===`checkbox`?!e.checked:en?.settings?.find(e=>e.key===t)?.value,r=e.type===`checkbox`?e.checked:e.value;K(!0),S.textContent=`saving settings...`,S.classList.remove(`is-empty`);try{let e=await fetch(`/api/config`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({[t]:r})});if(!e.ok)throw Error(`Config update failed`);G(await e.json(),`settings saved.`)}catch{e.type===`checkbox`?e.checked=n:n!==void 0&&(e.value=n),S.textContent=`could not save settings.`,K(!1)}}async function br(){it.disabled=!0,S.textContent=`clearing recommendation history...`,S.classList.remove(`is-empty`);try{let e=await fetch(`/api/recommendation-history/clear`,{method:`POST`});if(!e.ok)throw Error(`Recommendation history clear failed`);let t=await e.json();G(t.config,`cleared ${t.deleted_count} saved decisions.`)}catch{S.textContent=`could not clear recommendation history.`,it.disabled=!1}}async function xr(){let e=$e.value.trim();if(!e){S.textContent=`central api url is required.`,S.classList.remove(`is-empty`);return}let t={central_api_url:e},n=et.value.trim();n&&(t.central_passkey=n),K(!0),S.textContent=`saving central settings...`,S.classList.remove(`is-empty`);try{let e=await fetch(`/api/config`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(t)});if(!e.ok)throw Error(`Central settings update failed`);G(await e.json(),`central settings saved.`)}catch{S.textContent=`could not save central settings.`,K(!1)}}async function Sr(){nt.disabled=!0,S.textContent=`syncing remote company ids...`,S.classList.remove(`is-empty`);try{let e=await fetch(`/api/central/resolve-companies`,{method:`POST`});if(!e.ok)throw Error(`Central company sync failed`);let t=await e.json(),n=t.result??{},r=t.pulled_companies,i=r?` remote: ${Number(r.created??0)} created, ${Number(r.linked??0)} linked, ${Number(r.existing??0)} existing.`:``;G(t.config,`company sync: ${Number(n.linked??0)} matched, ${Number(n.created??0)} created, ${Number(n.needs_review??0)} review, ${Number(n.failed??0)} failed.${i}`),t.companies&&(R=t.companies,Dr(t.companies.companies))}catch{S.textContent=`could not sync companies.`,nt.disabled=!$e.value.trim()}}async function Cr(){let e=await fetch(`/api/central/resolve-companies`,{method:`POST`});if(!e.ok)throw Error(`Central company sync failed`);let t=await e.json();t.companies&&(R=t.companies,Dr(t.companies.companies))}async function wr(){let e=Cr().catch(()=>{});await Promise.all([q().catch(()=>{i.innerHTML=`<p class="empty-copy">could not load jobs.</p>`}),Fr().catch(()=>{Et.textContent=`could not load companies.`})]),await e}async function Tr(){if(window.confirm(`Update callumployed and restart the tracker?`)){K(!0),vt.disabled=!0,S.textContent=`updating callumployed; tracker will restart shortly...`,S.classList.remove(`is-empty`);try{if(!(await fetch(`/api/app/update`,{method:`POST`})).ok)throw Error(`App update failed`);S.textContent=`update started. reconnect in a moment.`}catch{S.textContent=`could not start update.`,K(!1)}}}function Er(e,t=``){R=e;let n=Array.isArray(e?.companies)?e.companies:[];if(Dr(n),C.textContent=t||`${n.length} ${n.length===1?`company`:`companies`} stored`,C.classList.toggle(`is-empty`,n.length===0&&!t),n.length===0){w.innerHTML=`<p class="empty-copy">no companies yet.</p>`;return}w.innerHTML=n.map(e=>Or(e)).join(``)}function Dr(e){rn=Array.isArray(e)?e:[],Tt.innerHTML=rn.map(e=>`<option value="${V(e.name)}"></option>`).join(``)}function Or(e){let t=Array.isArray(e.career_pages)?e.career_pages:[],n=B(e.updated_at),r=kr(e.prestige_tier),i=Number(e.scan_count??0),a=Number(e.discovered_role_count??0),o=i>0&&a===0?`<span class="company-discovery-status">Discovered 0 potential roles</span>`:``;return`
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
              ${Ar(e.prestige_tier)}
            </select>
          </label>
          <div>
            <span>browser wait</span>
            <strong>${Number(e.browser_extra_wait_ms??0)}ms</strong>
          </div>
        </div>
        <div class="company-links">
          ${t.length>0?t.map(e=>jr(e)).join(``):`<p class="company-empty-links">no career links yet.</p>`}
        </div>
        <section class="company-link-panel" aria-label="add career link">
          <form class="company-link-form" data-company-link-form="${e.id}">
            <input name="label" type="text" placeholder="label" aria-label="career link label" />
            <input name="url" type="url" placeholder="https://..." aria-label="career link url" required />
            <button class="company-link-add" type="submit" aria-label="add career link" title="add career link">
              ${pn()}
            </button>
          </form>
        </section>
        <div class="company-danger-row">
          <button class="company-delete-button" type="button" data-delete-company="${e.id}">
            ${mn()}
            <span>deactivate company</span>
          </button>
        </div>
      </div>
    </details>
  `}function kr(e){let t=String(e??``);return[`0`,`1`,`2`,`3`,`4`].includes(t)?`company-tier-${t}`:`company-tier-unset`}function Ar(e){let t=String(e??``);return[``,`0`,`1`,`2`,`3`,`4`].map(e=>{let n=e?`tier ${e}`:`not set`,r=e===t?` selected`:``;return`<option value="${V(e)}"${r}>${U(n)}</option>`}).join(``)}function jr(e){let t=e.label?U(e.label):`career page`,n=V(e.url);return`
    <div class="company-link-row" data-career-page-id="${e.id}">
      <a class="company-link-url" href="${n}" target="_blank" rel="noreferrer">
        <span class="company-link-label">${t}</span>
        <span class="company-link-text">${V(e.url)}</span>
      </a>
      <button class="company-link-delete" type="button" data-delete-career-page="${e.id}" aria-label="delete ${t} link" title="delete link">
        ${mn()}
      </button>
    </div>
  `}async function Mr(){yt.hidden=!1,document.body.classList.add(`companies-open`),bt.focus(),R?Er(R):(C.textContent=`loading companies...`,C.classList.remove(`is-empty`),w.innerHTML=``);try{await Pr()}catch{C.textContent=`could not load companies.`}}function Nr(){yt.hidden=!0,document.body.classList.remove(`companies-open`),Pe.focus()}async function Pr(e=``){let t=await fetch(`/api/companies`);if(!t.ok)throw Error(`Companies request failed`);Er(await t.json(),e)}async function Fr(){let e=await fetch(`/api/companies`);if(!e.ok)throw Error(`Companies request failed`);Dr((await e.json()).companies)}async function Ir(e){let t=new FormData(e),n={name:String(t.get(`name`)??``),career_url:String(t.get(`career_url`)??``),notes:String(t.get(`notes`)??``)};C.textContent=`adding company...`;let r=await fetch(`/api/companies`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(n)});if(!r.ok)throw Error(`Company create failed`);e.reset(),Er(await r.json(),`company added.`),q(z()).catch(()=>{})}async function Lr(e){let t=e.dataset.companyLinkForm;if(!t)return;let n=new FormData(e),r={label:String(n.get(`label`)??``),url:String(n.get(`url`)??``)};C.textContent=`adding link...`;let i=await fetch(`/api/companies/${encodeURIComponent(t)}/career-pages`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(r)});if(!i.ok)throw Error(`Career page create failed`);e.reset(),Er(await i.json(),`link added.`)}async function Rr(e){C.textContent=`deleting link...`;let t=await fetch(`/api/company-career-pages/${encodeURIComponent(e)}`,{method:`DELETE`});if(!t.ok)throw Error(`Career page delete failed`);Er(await t.json(),`link deleted.`)}async function zr(e){C.textContent=`deactivating company...`;let t=await fetch(`/api/companies/${encodeURIComponent(e)}`,{method:`DELETE`});if(!t.ok)throw Error(`Company deactivate failed`);Er(await t.json(),`company deactivated.`),q(z()).catch(()=>{})}function Br(){let e=wt.value.trim().toLocaleLowerCase();return rn.find(t=>t.name.toLocaleLowerCase()===e)}async function Vr(e){let t=Br();if(!t?.id){Et.textContent=`pick a saved company.`;return}let n=new FormData(e),r={company_id:t.id,role_url:String(n.get(`role_url`)??``)};Et.textContent=`adding role...`;let i=await fetch(`/api/roles`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(r)});if(!i.ok)throw Error(`Role create failed`);let a=await i.json();a.tracker?Un(a.tracker):await q(z()),Ct.value=``;let o=a.role?.title?H(a.role.title):`role`;Et.textContent=a.scan_error?`${o} added; scan could not finish.`:`${o} added.`}function Hr(e){return(Array.isArray(R?.companies)?R.companies:[]).find(t=>String(t.id)===String(e))}function Ur(e){C.textContent=e,C.classList.remove(`is-empty`)}function Wr(e){window.clearTimeout(an.get(e)),an.set(e,window.setTimeout(()=>{Gr(e).catch(()=>{Ur(`could not save company.`)})},700))}async function Gr(e){let t=w.querySelector(`[data-company-id="${CSS.escape(String(e))}"]`);if(!t)return;let n=t.querySelector(`[data-company-notes="${CSS.escape(String(e))}"]`),r=t.querySelector(`[data-company-tier="${CSS.escape(String(e))}"]`),i=Hr(e),a={notes:n?.value??i?.notes??``,prestige_tier:r?.value??i?.prestige_tier??``};i&&(i.notes=a.notes,i.prestige_tier=a.prestige_tier),Kr(t,a.prestige_tier),Ur(`saving company...`);let o=await fetch(`/api/companies/${encodeURIComponent(e)}`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(a)});if(!o.ok)throw Error(`Company update failed`);R=await o.json(),Ur(`company saved.`),qr(e)}function Kr(e,t){e.classList.remove(`company-tier-unset`,`company-tier-0`,`company-tier-1`,`company-tier-2`,`company-tier-3`,`company-tier-4`),e.classList.add(kr(t))}function qr(e){let t=w.querySelector(`[data-company-id="${CSS.escape(String(e))}"]`),n=Hr(e);if(!t||!n)return;let r=Array.isArray(n.career_pages)?n.career_pages:[],i=B(n.updated_at),a=t.querySelector(`.company-summary-meta`);a&&(a.textContent=`${r.length} ${r.length===1?`link`:`links`}${i?` | updated ${i}`:``}`)}async function Jr(){let e=await fetch(`/api/scan/status`);if(e.status===404){y.disabled=!0,b.hidden=!0,b.classList.add(`scan-error`),x.textContent=`restart server to enable scanning`;return}if(!e.ok)throw Error(`Scan status request failed`);Wn(await e.json())}function Yr(){Zt===null&&(Zt=window.setInterval(()=>{Jr().catch(()=>{})},3e3))}async function Xr(){y.disabled=!0,y.textContent=`starting...`;try{let e=await fetch(`/api/scan/all`,{method:`POST`});if(e.status===404){y.disabled=!0,y.textContent=`scan roles`,b.hidden=!0,b.classList.add(`scan-error`),x.textContent=`restart server to enable scanning`;return}if(!e.ok&&e.status!==409)throw Error(`Scan start failed`);Wn(await e.json()),Yr()}catch{y.disabled=!1,y.textContent=`scan roles`,b.hidden=!0,b.classList.add(`scan-error`),x.textContent=`could not start scan`}}async function Zr(){y.disabled=!0,y.textContent=`cancelling...`;try{let e=await fetch(`/api/scan/cancel`,{method:`POST`});if(e.status===404){y.disabled=!0,y.textContent=`scan roles`,b.hidden=!0,b.classList.add(`scan-error`),x.textContent=`restart server to enable scanning`;return}if(!e.ok&&e.status!==409)throw Error(`Scan cancel failed`);Wn(await e.json()),Yr()}catch{y.disabled=!1,y.textContent=`cancel scan`,b.hidden=!1,b.classList.add(`scan-error`),x.textContent=`could not cancel scan`}}async function q(e=``){i.innerHTML=`<p class="empty-copy">loading jobs...</p>`;let t=new URLSearchParams;e&&t.set(`q`,e);let n=await fetch(`/api/tracker?${t.toString()}`);if(!n.ok)throw Error(`Tracker request failed`);Un(await n.json())}async function Qr(e={}){let t=await fetch(`/api/application-materials`);if(!t.ok)throw Error(`Application materials request failed`);wn(await t.json(),e)}async function $r(e){if(e){if(!e.name.toLowerCase().endsWith(`.tex`)){vn(Nt,`resume must be a .tex file.`);return}ne.disabled=!0,vn(Nt,`uploading...`);try{let t=await e.text();if(!(await fetch(`/api/master-resume`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({filename:e.name,content:t})})).ok)throw Error(`Master resume upload failed`);await Qr()}catch{vn(Nt,`could not save resume.`),Tn()}finally{h.value=``,ne.disabled=!1}}}async function ei(e){let t=Array.from(e??[]);if(t.length!==0){ae.disabled=!0,Cn(E,`uploading ${t.length} ${t.length===1?`resource`:`resources`}...`);try{for(let e of t)if(!(await fetch(`/api/resume-resources`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({filename:e.name,content_base64:await ri(e)})})).ok)throw Error(`Resume resource upload failed`);await Qr()}catch{Cn(E,`could not save every resource.`),Tn()}finally{ie.value=``,ae.disabled=!1}}}async function ti(e){let t=Array.from(e??[]);if(t.length!==0){le.disabled=!0,bn(D,`uploading ${t.length} ${t.length===1?`example`:`examples`}...`);try{for(let e of t){let t={filename:e.name};if([`.pdf`,`.docx`].some(t=>e.name.toLowerCase().endsWith(t))?t.content_base64=await ri(e):t.content=await e.text(),!(await fetch(`/api/cover-letter-examples`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(t)})).ok)throw Error(`Cover letter example upload failed`)}await Qr()}catch{bn(D,`could not save every example.`),Tn()}finally{ce.value=``,le.disabled=!1}}}async function ni(e){let t=Array.from(e??[]);if(t.length!==0){pe.disabled=!0,xn(O,`uploading ${t.length} ${t.length===1?`note`:`notes`}...`);try{for(let e of t){let t=e.name.toLowerCase(),n={filename:e.name};if(t.endsWith(`.pdf`)||t.endsWith(`.docx`)?n.content_base64=await ri(e):n.content=await e.text(),!(await fetch(`/api/experience-notes`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(n)})).ok)throw Error(`Experience note upload failed`)}Ft.clear(),await Qr()}catch{xn(O,`could not save every note.`),Tn()}finally{fe.value=``,pe.disabled=!1}}}function ri(e){return new Promise((t,n)=>{let r=new FileReader;r.addEventListener(`load`,()=>{let e=String(r.result??``);t(e.includes(`,`)?e.split(`,`,2)[1]:e)}),r.addEventListener(`error`,()=>n(r.error)),r.readAsDataURL(e)})}c.addEventListener(`submit`,e=>{e.preventDefault(),q(l.value.trim()),cn()}),a.addEventListener(`click`,()=>{if(z()){q();return}sn()}),l.addEventListener(`keydown`,e=>{e.key===`Escape`&&(e.stopPropagation(),cn())}),u.addEventListener(`click`,cn),s.addEventListener(`click`,cn),ne.addEventListener(`click`,()=>{h.click()}),h.addEventListener(`change`,()=>{$r(h.files?.[0])}),ae.addEventListener(`click`,()=>{ie.click()}),ie.addEventListener(`change`,()=>{ei(ie.files)}),le.addEventListener(`click`,()=>{ce.click()}),ce.addEventListener(`change`,()=>{ti(ce.files)}),pe.addEventListener(`click`,()=>{fe.click()}),fe.addEventListener(`change`,()=>{ni(fe.files)}),ee.addEventListener(`click`,()=>{En(ee.getAttribute(`aria-expanded`)===`true`)});async function ii(e){e.disabled=!0;let t=e.textContent;e.textContent=`opening...`;try{if(!(await fetch(`/api/application-materials/index/open`,{method:`POST`})).ok)throw Error(`Could not open the application material index.`)}catch(e){he.hidden=!1,he.textContent=e instanceof Error?e.message:`Could not open the application material index.`}finally{e.disabled=!1,e.textContent=t}}f.addEventListener(`click`,e=>{let t=e.target.closest(`[data-open-material-index]`);if(t){ii(t);return}let n=e.target.closest(`[data-material-view]`);if(n){kn(n);return}let r=e.target.closest(`[data-material-remove]`);r&&An(r)}),y.addEventListener(`click`,()=>{if($t?.scanning){Zr();return}Xr()}),i.addEventListener(`click`,e=>{let t=e.target.closest(`[data-review-role-id]`);if(t){_i(t.dataset.reviewRoleId);return}let n=e.target.closest(`[data-prep-role-id]`);if(n){yi(n.dataset.prepRoleId);return}let r=e.target.closest(`.job-action`);if(r){ai(r);return}let i=e.target.closest(`.pane-toggle`);if(!i)return;let a=i.parentElement.querySelector(`.pane-body`),o=i.getAttribute(`aria-expanded`)===`true`;i.setAttribute(`aria-expanded`,String(!o)),i.querySelector(`.chevron`).textContent=o?`>`:`v`,a.hidden=o,ja()});async function ai(e){let{roleId:t,status:n}=e.dataset;if(!t||!n)return;let r=e.closest(`.job-actions`),i=e.closest(`.job`);r.querySelectorAll(`button`).forEach(e=>{e.disabled=!0}),e.textContent=`updating...`;try{let e=await fetch(`/api/roles/${encodeURIComponent(t)}/status`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({status:n})});if(!e.ok)throw Error(`Status update failed`);oi((await e.json()).role,i)}catch{r.querySelectorAll(`button`).forEach(e=>{e.disabled=!1}),e.textContent=n===`disinterested`?`disinterested`:n.toLowerCase()}}function oi(e,t){if(!e||!T)return;let n=t?.closest(`.status-pane`)?.dataset.bucket??e.role_status,r=e.role_status,i=ci(e,n,r);li(n,r),ui(n,r),_n(),pi(T.statuses),hi(T.statuses),di(t,i,n,r),ja()}function si(e){if(!e||!T)return null;let t=null;return T.statuses.forEach(n=>{let r=n.jobs.findIndex(t=>String(t.id)===String(e.id));r!==-1&&(t={...n.jobs[r],...e},n.jobs[r]=t)}),pi(T.statuses),hi(T.statuses),t}function ci(e,t,n){let r=e;T.statuses.forEach(t=>{let n=t.jobs.findIndex(t=>String(t.id)===String(e.id));n!==-1&&(r={...t.jobs[n],...e},t.jobs.splice(n,1),t.count=t.jobs.length)});let i=T.statuses.find(e=>e.key===n);return i&&(i.jobs.unshift(r),i.count=i.jobs.length),r}function li(e,t){T.statuses.forEach(e=>{let t=document.querySelector(`#status-${CSS.escape(e.key)}`);t?.classList.toggle(`empty`,e.count===0);let n=t?.querySelector(`.count`);n&&(n.textContent=e.count)}),[e,t].forEach(e=>{fi(document.querySelector(`#status-${CSS.escape(e)}`))})}function ui(e,t){if(!T.stats)return;let n=kt.has(e),r=kt.has(t);if(n===r){gn(T.stats);return}T.stats.applications_total=Number(T.stats.applications_total??0)+(r?1:-1),gn(T.stats)}function di(e,t,n,r){let i=document.querySelector(`#status-${CSS.escape(r)}`),a=i?.querySelector(`.pane-body`);if(!e||!i||!a)return;e.remove(),fi(document.querySelector(`#status-${CSS.escape(n)}`)),a.hidden=!1;let o=i.querySelector(`.pane-toggle`);o?.setAttribute(`aria-expanded`,`true`);let s=o?.querySelector(`.chevron`);s&&(s.textContent=`v`);let c=a.querySelector(`.jobs`);c||=(a.innerHTML=`<div class="jobs"></div>`,a.querySelector(`.jobs`)),c.insertAdjacentHTML(`afterbegin`,Mn(t,r)),fi(i)}function fi(e){if(!e)return;let t=e.querySelector(`.pane-body`);if(!t)return;let n=t.querySelector(`.jobs`),r=!!n?.querySelector(`.job`),i=t.querySelector(`.empty-copy`);if(r){i?.remove();return}n?.remove(),i||t.insertAdjacentHTML(`beforeend`,`<p class="empty-copy">no jobs in this status.</p>`)}function pi(e){_e.disabled=mi(e).length===0,_e.setAttribute(`aria-label`,`review discovered`),_e.innerHTML=`<span class="review-discovered-label">review discovered</span>`}function mi(e=T?.statuses??[]){return e.find(e=>e.key===`discovered`)?.jobs??[]}function hi(e){ve.disabled=gi(e).length===0,ve.setAttribute(`aria-label`,`prep interested`),ve.innerHTML=`<span class="review-discovered-label">prep interested</span>`}function gi(e=T?.statuses??[]){return e.find(e=>e.key===`interested`)?.jobs??[]}function _i(e=null){let t=[...mi()],n=e==null?null:String(e);if(n){let e=t.findIndex(e=>String(e.id)===n);if(e>0){let[n]=t.splice(e,1);t.unshift(n)}}k=t,g.hidden=!1,document.body.classList.add(`review-open`),xi()}function vi(){g.hidden=!0,document.body.classList.remove(`review-open`),k=[]}function yi(e=null){let t=[...gi()].sort((e,t)=>Number(!!t.prep_started)-Number(!!e.prep_started)),n=e==null?null:String(e);if(n){let e=t.findIndex(e=>String(e.id)===n);if(e>0){let[n]=t.splice(e,1);t.unshift(n)}}A=t,_.hidden=!1,document.body.classList.add(`prep-open`),Li()}function bi(){_.hidden=!0,document.body.classList.remove(`prep-open`),A=[]}function xi(e=``){let t=k[0],n=k.length,r=t?Si(t):``;if(ye.textContent=n>0?`review queue`:`review complete`,be.textContent=n>0?`${n} discovered ${n===1?`role`:`roles`} in queue`:``,g.querySelectorAll(`.review-action`).forEach(e=>{e.disabled=n===0}),!t){xe.innerHTML=`
      <div class="review-empty">
        <h3>no discovered jobs left.</h3>
        <p>everything in this queue has been handled or moved out of discovered.</p>
      </div>
    `;return}xe.innerHTML=`
    ${e?`<p class="review-message">${V(e)}</p>`:``}
    ${r?`<p class="review-message review-message-warning">${V(r)}</p>`:``}
    <div class="review-title-row">
      <p class="review-company">${U(t.company_name)}</p>
      ${hn(t.title,t.role_url,`review-role-title`)}
    </div>
    <dl class="review-details review-primary-details">
      ${J(`location`,t.location,!1,`review-location-detail`)}
      ${J(`first`,B(t.first_seen_at))}
      ${J(`last`,B(t.last_seen_at))}
    </dl>
    ${Ci(t.description)}
    <dl class="review-details review-technical-details">
      ${J(`notes`,t.notes,!1,`review-wide-detail`)}
      ${J(`company id`,t.company_id)}
      ${J(`role id`,t.id)}
      ${J(`status`,t.role_status)}
      ${J(`posting id`,t.posting_id)}
      ${J(`created`,B(t.created_at))}
      ${J(`updated`,B(t.updated_at))}
      ${J(`url`,t.role_url,!0,`review-wide-detail`)}
    </dl>
  `}function Si(e){let t=Number(e.review_later_count??0);return t<=Dt?``:`role review has been postponed ${t} times. it is recommended to set it to disinterested.`}function J(e,t,n=!1,r=``){if(!t)return``;let i=n?`<a href="${V(t)}" target="_blank" rel="noreferrer">${U(t)}</a>`:U(t);return`
    <div class="review-detail ${V(r)}">
      <dt>${U(e)}</dt>
      <dd>${i}</dd>
    </div>
  `}function Ci(e){return e?`
    <div class="review-detail review-description">
      <dt>description</dt>
      <dd>${wi(e)}</dd>
    </div>
  `:``}function wi(e){let t=Ti(String(e)).replace(/\u00a0/g,` `);if(Ei(t))return Di(t);let n=t.split(/\r?\n/).map(e=>e.trim()).filter(Boolean),r=[],i=[],a=()=>{i.length!==0&&(r.push(`<ul>${i.map(e=>`<li>${e}</li>`).join(``)}</ul>`),i=[])};return n.forEach(e=>{let t=e.match(/^#{2,3}\s+(.+)$/);if(t){a(),r.push(`<h3>${U(t[1])}</h3>`);return}if(Fi(e)){a(),r.push(`<h3>${U(e.replace(/:$/,``))}</h3>`);return}let n=e.match(/^[-*]\s+(.+)$/);if(n){i.push(U(n[1]));return}a(),r.push(`<p>${U(e)}</p>`)}),a(),r.join(``)}function Ti(e){let t=document.createElement(`textarea`);return t.innerHTML=e,t.value}function Ei(e){return/<\/?(?:a|br|div|em|h[1-6]|li|ol|p|span|strong|ul)\b/i.test(e)}function Di(e){let t=document.createElement(`template`);t.innerHTML=e;let n=[];return Oi(t.content.childNodes,n),n.join(``)}function Oi(e,t){e.forEach(e=>{if(e.nodeType===Node.TEXT_NODE){let n=Ni(e.textContent);n&&t.push(`<p>${U(n)}</p>`);return}if(e.nodeType!==Node.ELEMENT_NODE)return;let n=e,r=n.tagName.toLowerCase();if(r===`script`||r===`style`||r===`br`)return;if(/^h[1-6]$/.test(r)){Ai(t,n.textContent);return}if(r===`ul`||r===`ol`){let e=ji(n);e&&t.push(e);return}if(r===`p`){ki(n,t);return}let i=Array.from(n.children).some(e=>[`DIV`,`H1`,`H2`,`H3`,`H4`,`H5`,`H6`,`OL`,`P`,`UL`].includes(e.tagName));if([`article`,`div`,`section`].includes(r)&&i){Oi(n.childNodes,t);return}let a=Array.from(n.children).filter(e=>[`UL`,`OL`].includes(e.tagName)),o=Ni(Mi(n));if(o&&(Pi(o,n)?Ai(t,o):t.push(`<p>${U(o)}</p>`)),a.length>0){a.forEach(e=>{let n=ji(e);n&&t.push(n)});return}!o&&i&&Oi(n.childNodes,t)})}function ki(e,t){if(!e.querySelector(`br`)){let n=Ni(Mi(e));if(!n)return;Pi(n,e)?Ai(t,n):t.push(`<p>${U(n)}</p>`);return}let n=``,r=()=>{let r=Ni(n);n=``,r&&(Pi(r,e)?Ai(t,r):t.push(`<p>${U(r)}</p>`))};e.childNodes.forEach(e=>{if(e.nodeType===Node.ELEMENT_NODE&&e.tagName.toLowerCase()===`br`){r();return}n+=` ${e.textContent??``}`}),r()}function Ai(e,t){let n=Ni(t).replace(/:$/,``);n&&e.push(`<h3>${U(n)}</h3>`)}function ji(e){let t=Array.from(e.children).filter(e=>e.tagName===`LI`).map(e=>{let t=Ni(Mi(e)),n=Array.from(e.children).filter(e=>[`UL`,`OL`].includes(e.tagName)).map(e=>ji(e)).filter(Boolean).join(``);return t||n?`<li>${U(t)}${n}</li>`:``}).filter(Boolean);return t.length>0?`<ul>${t.join(``)}</ul>`:``}function Mi(e){let t=e.cloneNode(!0);return t.querySelectorAll(`ul, ol`).forEach(e=>{e.remove()}),t.textContent}function Ni(e){return String(e??``).replace(/\s+/g,` `).trim()}function Pi(e,t){let n=e.replace(/:$/,``).trim();return!n||n.length>90?!1:Fi(n)||/:$/.test(e)?!0:/[.!?]$/.test(n)||n.split(/\s+/).length>10?!1:t.querySelector(`strong, b, u`)?!0:Fi(n)}function Fi(e){return jt.test(String(e).trim())}async function Ii(e){let t=k[0];if(!t)return;if(e===`later`){g.querySelectorAll(`.review-action`).forEach(e=>{e.disabled=!0});try{let e=await oa(t.id);k.shift(),si(e),xi(`moved out of this review pass.`)}catch{xi(`could not postpone that role. try again.`)}finally{g.querySelectorAll(`.review-action`).forEach(e=>{e.disabled=k.length===0})}return}if(![`interested`,`disinterested`].includes(e))return;let n=g.querySelectorAll(`.review-action`);n.forEach(e=>{e.disabled=!0});try{let n=await sa(t.id,e);k.shift(),xi(e===`interested`?`marked interested.`:`marked disinterested.`),oi(n,document.querySelector(`.job[data-role-id="${CSS.escape(String(t.id))}"]`))}catch{n.forEach(e=>{e.disabled=!1}),xi(`could not update that role. try again.`)}}async function Li(e=``){let t=A[0],n=A.length;if(Ce.textContent=n>0?`prep queue`:`prep complete`,we.textContent=n>0?`${n} interested ${n===1?`role`:`roles`} in queue`:``,_.querySelectorAll(`.review-action`).forEach(e=>{e.disabled=n===0}),!t){v.innerHTML=`
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
        ${hn(t.title,t.role_url,`review-role-title`)}
      </div>
      <dl class="review-details review-primary-details">
        ${J(`location`,t.location,!1,`review-location-detail`)}
        ${J(`last`,B(t.last_seen_at))}
        ${J(`updated`,B(t.updated_at))}
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
      ${Ri(t)}
      ${Hi(t)}
      ${zi(t.id,t.description)}
      ${Bi(t)}
    </div>
  `,W(),Ji(t.id).then(e=>{!e||A[0]?.id!==t.id||(j.set(t.id,e),v.querySelector(`.prep-resume`)?.replaceWith(X(Ri(t,{resume:e}))),W())}).catch(()=>{}),aa(t.id).then(e=>{!e||A[0]?.id!==t.id||(M.set(t.id,e),v.querySelector(`.prep-cover-letter`)?.replaceWith(X(Hi(t,{coverLetter:e}))),W())}).catch(()=>{})}function Ri(e,t={}){let n=j.get(e.id),r=t.resume??n,i=t.tweaks??Lt.get(e.id)??``,a=`/api/roles/${encodeURIComponent(e.id)}/resume.pdf`;return t.loading?`
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
      ${Y(e)}
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
        <section class="prep-document-preview" aria-label="resume preview">
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
    `}function zi(e,t){return`
    <details class="prep-panel prep-description-panel" id="prep-description-${e}">
      <summary class="prep-analysis-header">
        <span class="prep-accordion-icon" aria-hidden="true"></span>
        <h3>description</h3>
      </summary>
      ${Ci(t)}
    </details>
  `}function Bi(e,t={}){let n=t.messages??Rt.get(e.id)??[],r=!!t.loading;return`
    <details class="prep-panel prep-role-chat" id="prep-chat-${e.id}">
      <summary class="prep-analysis-header">
        <span class="prep-accordion-icon" aria-hidden="true"></span>
        <h3>chat about this role</h3>
        <span>${n.length?`${n.length} messages`:`ready`}</span>
      </summary>
      <div class="prep-role-chat-log" aria-live="polite">
        ${n.length?n.map(Vi).join(``):`<p class="prep-role-chat-empty">ask about fit, risks, resume emphasis, or cover letter angle.</p>`}
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
  `}function Vi(e){let t=e?.role===`assistant`?`assistant`:`user`;return`
    <article class="prep-role-chat-message prep-role-chat-message-${t}">
      <span>${t}</span>
      <p>${U(e?.content??``)}</p>
    </article>
  `}function Hi(e,t={}){let n=M.get(e.id),r=t.coverLetter??n,i=t.tweaks??r?.tweaks??``,a=`/api/roles/${encodeURIComponent(e.id)}/cover-letter.pdf`;return t.loading?`
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
          <p>Use the role, resume, and saved examples to shape the letter.</p>
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
  `}function Y(e,t={}){let n=Ft.get(e.id);if(!t.loading&&!t.error&&!t.analysis&&n)return Y(e,{analysis:n});if(!t.loading&&!t.error&&!t.analysis)return`
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
    `;let r=t.analysis,i=Array.isArray(r?.feedback_items)?r.feedback_items:[],a=r?.verdict===`ready_to_apply`?`ready to apply`:`tweak`,o=Math.min(It.get(e.id)??0,Math.max(i.length-1,0)),s=i[o];return`
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
              ${Ui(s)}
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
  `}function Ui(e){return e?.tweak_prompt?`
    <div class="prep-proposed-edit">
      <p class="prep-proposed-label">tweak prompt</p>
      <p>${U(e.tweak_prompt)}</p>
    </div>
  `:`
      <div class="prep-proposed-edit">
        <p class="prep-proposed-label">feedback only</p>
        <p>not enough information to turn this into a safe resume tweak.</p>
      </div>
    `}async function Wi(e,t={}){if(!t.force&&Ft.has(e))return Ft.get(e);let n=await fetch(`/api/roles/${encodeURIComponent(e)}/prep-analysis`);if(!n.ok)throw Error(`Prep analysis request failed`);let r=await n.json();return r.analysis.resources=r.resources??[],Ft.set(e,r.analysis),r.analysis}function X(e){let t=document.createElement(`template`);return t.innerHTML=e.trim(),t.content.firstElementChild}async function Gi(e){let t=A[0];if(!t)return;let n=_.querySelectorAll(`.review-action`);if(n.forEach(e=>{e.disabled=!0}),e===`later`){try{await oa(t.id),t.review_later_count=Number(t.review_later_count??0)+1,A.length>1?(A.push(A.shift()),Li(`moved to the back of the prep queue.`)):Li(`only one role is in the prep queue.`)}catch{Li(`could not postpone prep. try again.`)}return}if(e===`applied`)try{let e=await sa(t.id,`applied`);A.shift(),Li(`moved to applied.`),oi(e,document.querySelector(`.job[data-role-id="${CSS.escape(String(t.id))}"]`))}catch{n.forEach(e=>{e.disabled=!1}),Li(`could not move that role. try again.`)}}async function Ki(e,t,n,r){let i=await fetch(`/api/roles/${encodeURIComponent(e)}/prep-feedback`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({feedback_index:t,feedback_item:n,comment:r})});if(!i.ok)throw Error(`Prep feedback update failed`);return i.json()}async function qi(e,t,n,r){let i=await fetch(`/api/roles/${encodeURIComponent(e)}/prep-feedback-ignore`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({feedback_index:t,feedback_item:n,comment:r})});if(!i.ok)throw Error(`Prep feedback ignore failed`);return i.json()}async function Ji(e,{force:t=!1}={}){if(!t&&j.has(e))return j.get(e);let n=await fetch(`/api/roles/${encodeURIComponent(e)}/resume`);if(!n.ok)throw Error(`Resume request failed`);let r=await n.json();return r.resume&&j.set(e,r.resume),r.resume}async function Yi(e,t){let n=await fetch(`/api/roles/${encodeURIComponent(e)}/resume/save`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({latex:t})});if(!n.ok)throw Error(`Resume save failed`);return n.json()}async function Xi(e,t,n){let r=await fetch(`/api/roles/${encodeURIComponent(e)}/resume`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({tweaks:t,previous_latex:n})});if(!r.ok)throw Error(`Resume generation failed`);return r.json()}async function Zi(e,t){let n=await fetch(`/api/roles/${encodeURIComponent(e)}/chat`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({messages:t})});if(!n.ok)throw Error(`Role chat failed`);return n.json()}function Qi(e,t,n=Ot){let r=zt.get(e)??{timer:null,saving:!1,version:0,latex:``};r.version+=1,r.latex=t,r.timer&&clearTimeout(r.timer),r.timer=setTimeout(()=>{r.timer=null,$i(e)},n),zt.set(e,r)}async function $i(e){let t=zt.get(e);if(!t||t.saving)return;t.saving=!0;let n=t.version,r=t.latex;try{let i=await Yi(e,r);t.version===n&&(j.set(e,i.resume),ea(`resume`,e,i.resume))}catch{}finally{t.saving=!1,t.version!==n&&Qi(e,t.latex,0)}}function ea(e,t,n){if(!n?.pdf_base64)return;let r=e===`resume`?`[data-prep-resume-latex="${t}"]`:`[data-prep-cover-letter-latex="${t}"]`,i=v.querySelector(r)?.closest(`.prep-panel`),a=i?.querySelector(`.prep-cover-pdf`),o=i?.querySelector(`.prep-cover-pdf-link`),s=e===`resume`?`/api/roles/${encodeURIComponent(t)}/resume.pdf`:`/api/roles/${encodeURIComponent(t)}/cover-letter.pdf`;a&&(a.src=`${s}?v=${Date.now()}`),o&&(o.href=s)}async function ta(e,t=``,n=``){let r=await fetch(`/api/roles/${encodeURIComponent(e)}/cover-letter`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({tweaks:t,previous_latex:n})});if(!r.ok)throw Error(`Cover letter generation failed`);return r.json()}async function na(e,t){let n=await fetch(`/api/roles/${encodeURIComponent(e)}/cover-letter/save`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({latex:t})});if(!n.ok)throw Error(`Cover letter save failed`);return n.json()}function ra(e,t,n=``,r=Ot){let i=Bt.get(e)??{timer:null,saving:!1,version:0,latex:``,tweaks:``};i.version+=1,i.latex=t,i.tweaks=n,i.timer&&clearTimeout(i.timer),i.timer=setTimeout(()=>{i.timer=null,ia(e)},r),Bt.set(e,i)}async function ia(e){let t=Bt.get(e);if(!t||t.saving)return;t.saving=!0;let n=t.version,r=t.latex,i=t.tweaks;try{let a=await na(e,r);t.version===n&&(M.set(e,{...a.cover_letter,tweaks:i}),ea(`coverLetter`,e,a.cover_letter))}catch{}finally{t.saving=!1,t.version!==n&&ra(e,t.latex,t.tweaks,0)}}async function aa(e){if(M.has(e))return M.get(e);let t=await fetch(`/api/roles/${encodeURIComponent(e)}/cover-letter`);if(!t.ok)throw Error(`Cover letter request failed`);let n=await t.json();return n.cover_letter&&M.set(e,n.cover_letter),n.cover_letter}async function oa(e){let t=await fetch(`/api/roles/${encodeURIComponent(e)}/review-later`,{method:`POST`});if(!t.ok)throw Error(`Review later update failed`);return(await t.json()).role}async function sa(e,t){let n=await fetch(`/api/roles/${encodeURIComponent(e)}/status`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({status:t})});if(!n.ok)throw Error(`Status update failed`);return(await n.json()).role}function ca(e){return`${e}-${globalThis.crypto?.randomUUID?.()??`${Date.now()}-${Math.random()}`}`}function la(e){window.location.hash!==e&&window.history.pushState({},``,e||`${window.location.pathname}${window.location.search}`)}async function ua({seedJobs:e=null}={}){De.hidden=!1,document.body.classList.add(`prepped-open`),la(`#prepped-roles`),e?(N=e,P=P??N[0]?.role_id??null,$()):N.length===0&&(ke.textContent=`loading prepared roles...`),await Z(),fa()}function da({clearHash:e=!0}={}){De.hidden=!0,document.body.classList.remove(`prepped-open`),pa(),I.clear(),L.forEach(e=>URL.revokeObjectURL(e)),L.clear(),Kt.clear(),qt.clear(),e&&window.location.hash===`#prepped-roles`&&la(``)}window.addEventListener(`pagehide`,()=>{document.querySelectorAll(`[data-preview-blob-url]`).forEach(e=>{URL.revokeObjectURL(e.dataset.previewBlobUrl)}),L.forEach(e=>URL.revokeObjectURL(e)),L.clear(),Kt.clear()});async function Z(){try{let e=await fetch(`/api/autoprep/jobs`);if(!e.ok)throw Error(`Prepped roles request failed`);let t=await e.json();N=t.jobs??[];let n=t.bulk_cover_letter_regeneration;if(n){let e=Array.isArray(n.jobs)?n.jobs:[];F={idempotencyKey:n.idempotency_key,roleIds:e.map(e=>Number(e.role_id)),jobs:e,skipped:Array.isArray(n.skipped)?n.skipped:[]}}N.some(e=>Number(e.role_id)===Number(P))||(P=N[0]?.role_id??null),$()}catch{ke.textContent=`could not refresh preparation progress.`}}function fa(){pa(),N.some(ma)&&(Vt=window.setInterval(Z,2e3))}function pa(){Vt!==null&&window.clearInterval(Vt),Vt=null}function ma(e){return[`queued`,`generating_resume_tweaks`,`regenerating_resume`,`generating_cover_letter`].includes(e.overall_status)}function ha(e){return{queued:`Queued`,generating_resume_tweaks:`Generating resume tweaks`,regenerating_resume:`Regenerating resume`,generating_cover_letter:`Generating cover letter`,partially_complete:`Partially complete`,ready:`Ready`,failed:`Failed`,interrupted:`Interrupted`,generating_tweaks:`Generating tweaks`,regenerating:`Regenerating`,generating:`Generating`}[e]??H(e)}function ga(e,t){let n=t===`cover-letter`?`cover_letter`:`resume`;return`${e.updated_at||``}:${e[`${n}_artifact_path`]||``}`}function Q(e,{close:t=!1}={}){let n=L.get(e);n&&URL.revokeObjectURL(n),L.delete(e),Kt.delete(e),qt.delete(e),t&&I.delete(e)}function _a(){Kt.forEach((e,t)=>{let[n,r]=t.split(`:`),i=N.find(e=>Number(e.role_id)===Number(n));(!i||ga(i,r)!==e)&&Q(t,{close:!0})})}function va(){if(!F)return;let e=F.jobs||N,t=new Map(e.map(e=>[Number(e.role_id),e])),n=F.roleIds.map(e=>t.get(Number(e))),r=n.filter(e=>e?.worker_state===`idle`&&e.cover_letter_status===`ready`).length,i=n.filter(e=>!e||e.worker_state===`idle`&&[`failed`,`interrupted`].includes(e.cover_letter_status)),a=n.length-r-i.length,o=F.skipped.length?` Skipped before queueing: ${F.skipped.map(e=>`${e.company_name} — ${e.title}: ${e.reason}`).join(` · `)}`:``,s=i.length?` Queued regeneration failures: ${i.map(e=>e?`${e.company_name} — ${e.title}: ${e.cover_letter_error||`generation failed`}`:`A role left the Prepped queue before regeneration completed`).join(` · `)}`:``;Ut=n.length?a>0?`Cover-letter regeneration in progress: ${r} of ${n.length} complete · ${a} remaining.${o}${s}`:`Cover-letter regeneration complete: ${r} succeeded, ${i.length} failed.${o}${s}`:`No cover letters were queued.${o}`}function $(){_a(),va();let e=N.filter(ma).length,t=N.filter(e=>e.worker_state===`idle`&&e.cover_letter_status===`ready`).length;ke.textContent=N.length?`${N.length} prepped ${N.length===1?`role`:`roles`}${e?` · ${e} in progress`:``}`:`No queued or prepared roles.`,Ae.disabled=Ht||t===0,Ae.setAttribute(`aria-busy`,Ht?`true`:`false`),Ae.textContent=Ht?`queuing cover letters...`:`regenerate all cover letters`,je.textContent=Ut,Me.innerHTML=N.map(e=>`
    <button type="button" class="prepped-list-item${Number(e.role_id)===Number(P)?` is-active`:``}" data-prepped-role="${e.role_id}">
      <strong>${U(e.company_name)}</strong><span>${U(e.title)}</span>
      <small class="status-${V(e.overall_status)}">${V(ha(e.overall_status))}</small>
    </button>`).join(``),ya(),fa()}function ya(){let e=N.findIndex(e=>Number(e.role_id)===Number(P)),t=N[e];if(!t){Ne.innerHTML=`<div class="prepped-empty"><h3>nothing prepped yet.</h3><p>Queue Interested roles from Autoprep Interested.</p></div>`;return}let n=U(t.title),r=un(t.role_url),i=r?`<a class="prepped-role-link" href="${V(r)}" target="_blank" rel="noopener noreferrer">${n}<span aria-hidden="true">↗</span></a>`:n,a=[[`Location`,t.location||`Unavailable`],[`Added`,B(t.date_added||t.created_at)||`Unavailable`],[`Last seen`,B(t.last_seen_at)||`Unavailable`],[`Posting ID`,t.posting_id||`Unavailable`]],o=Wt.has(Number(t.role_id)),s=o||ma(t);Ne.innerHTML=`
    <header class="prepped-detail-heading">
      <div><p class="eyebrow">${U(t.company_name)}</p><h3>${i}</h3></div>
      <span class="prepped-status status-${V(t.overall_status)}">${V(ha(t.overall_status))}</span>
    </header>
    <dl class="prepped-role-facts">${a.map(([e,t])=>`<div><dt>${V(e)}</dt><dd>${U(t)}</dd></div>`).join(``)}</dl>
    <details class="prepped-role-description">
      <summary>Job description</summary>
      <div class="prepped-description-copy">${U(t.description||`No job description was saved.`).replaceAll(`
`,`<br>`)}</div>
    </details>
    ${t.notes?`<details class="prepped-role-description"><summary>Role notes</summary><div class="prepped-description-copy">${U(t.notes).replaceAll(`
`,`<br>`)}</div></details>`:``}
    <div class="prepped-document-grid">
      ${xa(t,`resume`,`Resume`)}
      ${xa(t,`cover-letter`,`Cover letter`)}
    </div>
    <div class="prepped-detail-actions">
      <button type="button" data-prepped-nav="previous" ${e<=0?`disabled`:``}>Previous</button>
      <button type="button" data-prepped-nav="next" ${e>=N.length-1?`disabled`:``}>Next</button>
      <button type="button" data-autoprep-open-folder ${t.artifact_directory?``:`disabled`}>Open Documents Folder</button>
      <button class="prepped-disinterested" type="button" data-autoprep-disinterested aria-busy="${o?`true`:`false`}" ${s?`disabled`:``} title="${ma(t)?`Wait for preparation to finish before moving this role`:`Move this role out of Prepped`}">${o?`Moving to Disinterested...`:`Move to Disinterested`}</button>
      <button class="success" type="button" data-autoprep-applied ${t.overall_status===`ready`?``:`disabled`}>Applied</button>
    </div>
    <p class="prepped-safety-note">Autoprep prepares files only. It never submits an application.</p>`}async function ba(e,t){let n=`${e.role_id}:${t}`,r=ga(e,t);if(!(Kt.get(n)===r||Jt.has(n))){Q(n),Jt.add(n),qt.delete(n),ya();try{let i=await On(`/api/autoprep/roles/${encodeURIComponent(e.role_id)}/documents/${t}.pdf?v=${encodeURIComponent(e.updated_at||``)}`),a=N.find(t=>Number(t.role_id)===Number(e.role_id));if(!I.has(n)||!a||ga(a,t)!==r){URL.revokeObjectURL(i),I.delete(n);return}L.set(n,i),Kt.set(n,r)}catch(e){qt.set(n,e instanceof Error?e.message:`PDF preview unavailable`)}finally{Jt.delete(n),Number(P)===Number(e.role_id)&&ya()}}}function xa(e,t,n){let r=t===`cover-letter`?`cover_letter`:`resume`,i=e[`${r}_status`],a=e[`${r}_artifact_path`],o=a?.split(`/`).pop()??`Not available`,s=e[`${r}_error`],c=e[`${r}_instruction`]||``,l=`${e.role_id}:${t}`,u=Gt.get(l)??c,d=[`queued`,`generating`,`generating_tweaks`,`regenerating`].includes(i),ee=[`failed`,`interrupted`].includes(i)?`<button type="button" data-autoprep-retry="${t}">Retry ${V(n.toLowerCase())}</button>`:``,f=I.has(l),te=`/api/autoprep/roles/${encodeURIComponent(e.role_id)}/documents/${t}.pdf?v=${encodeURIComponent(e.updated_at||``)}`,p=L.get(l),m=qt.get(l),h=Jt.has(l),ne=a?`<a class="prep-cover-pdf-link" data-autoprep-view="${t}" href="${V(te)}" target="_blank" rel="noreferrer" aria-label="View ${V(n.toLowerCase())} PDF in browser">View PDF</a>`:``;return`
    <section class="prepped-document${f?` has-open-preview`:``} status-${V(i)}">
      <div class="prepped-document-heading"><h4>${V(n)}</h4><span>${V(ha(i))}</span></div>
      <p class="prepped-filename">${V(o)}</p>
      ${s?`<p class="prepped-error">${V(s)}</p>`:``}
      <div class="prepped-document-actions">
        <button type="button" data-autoprep-preview="${t}" ${a?``:`disabled`}>${f?`Hide preview`:`Preview PDF`}</button>
        ${ne}
        ${ee}
      </div>
      <div class="prepped-pdf-preview" data-autoprep-preview-panel="${t}" ${f&&a?``:`hidden`}>
        ${f&&p?`<iframe title="${V(n)} PDF preview" src="${V(p)}"></iframe>`:``}
        ${f&&h?`<p>Loading PDF preview...</p>`:``}
        ${f&&m?`<p class="prepped-error">${U(m)}</p>`:``}
      </div>
      <label class="prepped-comments-label" for="prepped-comments-${V(l)}">Comments for the next version</label>
      <textarea id="prepped-comments-${V(l)}" data-autoprep-comments="${t}" rows="4" placeholder="Describe specific, truthful changes..." ${d?`disabled`:``}>${U(u)}</textarea>
      <button class="prepped-regenerate" type="button" data-autoprep-regenerate="${t}" ${i===`ready`&&String(u).trim()?``:`disabled`}>${d?`Regenerating...`:`Regenerate ${V(n)}`}</button>
    </section>`}async function Sa(e,t,n){if(n.disabled)return;let r=`${e.role_id}:${t}`,i=Ne.querySelector(`[data-autoprep-comments="${t}"]`),a=String(i?.value||Gt.get(r)||``).trim();if(!a){i?.focus();return}n.disabled=!0,n.textContent=`Queuing regeneration...`;try{let n=await fetch(`/api/autoprep/roles/${encodeURIComponent(e.role_id)}/regenerate/${t}`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({comments:a,idempotency_key:ca(`regenerate-${t}`)})}),i=await n.json();if(!n.ok)throw Error(i.error||`Regeneration request failed`);Gt.delete(r),Q(r,{close:!0});let o=N.findIndex(t=>Number(t.role_id)===Number(e.role_id));o>=0&&(N[o]=i.job),$()}catch(e){window.alert(e instanceof Error?e.message:`Regeneration request failed`),await Z()}}async function Ca(){if(!Ht){Ht=!0,F=null,Ut=`Queuing eligible cover letters...`,$();try{let e=await fetch(`/api/autoprep/cover-letters/regenerate`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({idempotency_key:ca(`regenerate-all-cover-letters`)})}),t=await e.json();if(!e.ok)throw Error(t.error||`Bulk regeneration request failed`);let n=Number(t.queued_count||0),r=Array.isArray(t.skipped)?t.skipped:[];F={roleIds:(t.jobs||[]).map(e=>Number(e.role_id)),jobs:t.jobs||[],skipped:r},!n&&!r.length&&(F=null,Ut=`No prepped roles are available to regenerate.`),(t.jobs||[]).forEach(e=>{let t=N.findIndex(t=>Number(t.role_id)===Number(e.role_id));t>=0&&(N[t]=e),Q(`${e.role_id}:cover-letter`,{close:!0})}),await Z(),fa()}catch(e){F=null,Ut=e instanceof Error?e.message:`Bulk regeneration request failed`}finally{Ht=!1,$()}}}async function wa(e,t,n){if(!n.disabled){n.disabled=!0,n.textContent=`Queuing retry...`;try{let n=await fetch(`/api/autoprep/roles/${encodeURIComponent(e)}/retry/${t}`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({idempotency_key:ca(`retry-${t}`)})}),r=await n.json();if(!n.ok)throw Error(r.error||`Retry request failed`);Q(`${e}:${t}`,{close:!0});let i=N.findIndex(t=>Number(t.role_id)===Number(e));i>=0&&(N[i]=r.job),$()}catch{await Z()}}}async function Ta(e,t){let n=Number(e);if(Wt.has(n))return;Wt.add(n),t.disabled=!0,t.setAttribute(`aria-busy`,`true`),t.textContent=`Moving to Disinterested...`;let r=N.findIndex(e=>Number(e.role_id)===n);try{await sa(e,`disinterested`),Q(`${e}:resume`,{close:!0}),Q(`${e}:cover-letter`,{close:!0}),r>=0&&N.splice(r,1),P=N[Math.min(r,N.length-1)]?.role_id??null,Ut=`Role moved to Disinterested.`,$(),wr()}catch(e){Ut=e instanceof Error?e.message:`Could not move this role to Disinterested.`,await Z()}finally{Wt.delete(n),N.some(e=>Number(e.role_id)===n)&&$()}}async function Ea(e,t){if(t.disabled)return;t.disabled=!0,t.textContent=`Moving to Applied...`;let n=N.findIndex(t=>Number(t.role_id)===Number(e));try{if(!(await fetch(`/api/autoprep/roles/${encodeURIComponent(e)}/applied`,{method:`POST`})).ok)throw Error(`Applied update failed`);Q(`${e}:resume`,{close:!0}),Q(`${e}:cover-letter`,{close:!0}),N.splice(n,1),P=N[Math.min(n,N.length-1)]?.role_id??null,$(),wr()}catch{await Z()}}_e.addEventListener(`click`,_i),Se.addEventListener(`click`,vi),ve.addEventListener(`click`,yi),Ee.addEventListener(`click`,()=>ua()),Oe.addEventListener(`click`,da),Ae.addEventListener(`click`,Ca),Me.addEventListener(`click`,e=>{let t=e.target.closest(`[data-prepped-role]`);t&&(P=Number(t.dataset.preppedRole),$())}),Ne.addEventListener(`input`,e=>{let t=e.target.closest(`[data-autoprep-comments]`);if(!t)return;let n=`${P}:${t.dataset.autoprepComments}`;Gt.set(n,t.value);let r=Ne.querySelector(`[data-autoprep-regenerate="${t.dataset.autoprepComments}"]`),i=N.find(e=>Number(e.role_id)===Number(P)),a=t.dataset.autoprepComments===`cover-letter`?`cover_letter`:`resume`;r&&(r.disabled=i?.[`${a}_status`]!==`ready`||!t.value.trim())}),Ne.addEventListener(`click`,async e=>{let t=N.find(e=>Number(e.role_id)===Number(P));if(!t)return;let n=e.target.closest(`[data-prepped-nav]`);if(n){let e=N.indexOf(t),r=n.dataset.preppedNav===`next`?1:-1;P=N[e+r]?.role_id??t.role_id,$();return}let r=e.target.closest(`[data-autoprep-preview]`);if(r){let e=r.dataset.autoprepPreview,n=`${t.role_id}:${e}`;I.has(n)?(I.delete(n),ya()):(I.add(n),ya(),ba(t,e));return}let i=e.target.closest(`[data-autoprep-regenerate]`);if(i){Sa(t,i.dataset.autoprepRegenerate,i);return}let a=e.target.closest(`[data-autoprep-retry]`);if(a){wa(t.role_id,a.dataset.autoprepRetry,a);return}let o=e.target.closest(`[data-autoprep-open-folder]`);if(o&&!o.disabled){o.disabled=!0,o.textContent=`Opening...`;try{if(!(await fetch(`/api/autoprep/roles/${encodeURIComponent(t.role_id)}/open-folder`,{method:`POST`})).ok)throw Error(`Could not open the documents folder.`);o.textContent=`Opened in Finder`,window.setTimeout(()=>{o.isConnected&&(o.textContent=`Open Documents Folder`,o.disabled=!1)},1500)}catch(e){o.textContent=e instanceof Error?e.message:`Could not open folder`,o.disabled=!1}return}let s=e.target.closest(`[data-autoprep-disinterested]`);if(s){Ta(t.role_id,s);return}let c=e.target.closest(`[data-autoprep-applied]`);c&&Ea(t.role_id,c)}),Te.addEventListener(`click`,bi),g.addEventListener(`click`,e=>{let t=e.target.closest(`[data-review-action]`);t&&Ii(t.dataset.reviewAction)}),_.addEventListener(`click`,e=>{e.target.closest(`.prep-summary-action`)&&e.stopPropagation()}),_.addEventListener(`input`,e=>{let t=e.target.closest(`[data-prep-resume-tweaks]`);if(t){let e=Number(t.dataset.prepResumeTweaks);Number.isFinite(e)&&Lt.set(e,t.value);return}let n=e.target.closest(`[data-prep-resume-latex]`);if(n){let e=Number(n.dataset.prepResumeLatex);if(!Number.isFinite(e))return;Qi(e,n.value);return}let r=e.target.closest(`[data-prep-cover-letter-latex]`);if(!r)return;let i=Number(r.dataset.prepCoverLetterLatex);if(!Number.isFinite(i))return;let a=r.closest(`.prep-cover-letter`)?.querySelector(`[data-prep-cover-letter-tweaks="${i}"]`)?.value??``;ra(i,r.value,a)}),_.addEventListener(`scroll`,e=>{e.target.closest(`[data-prep-resume-latex], [data-prep-cover-letter-latex]`)},!0),_.addEventListener(`focusout`,e=>{let t=e.target.closest(`[data-prep-resume-latex]`);if(t){let e=Number(t.dataset.prepResumeLatex);if(!Number.isFinite(e))return;Qi(e,t.value,0);return}let n=e.target.closest(`[data-prep-cover-letter-latex]`);if(!n)return;let r=Number(n.dataset.prepCoverLetterLatex);if(!Number.isFinite(r))return;let i=n.closest(`.prep-cover-letter`)?.querySelector(`[data-prep-cover-letter-tweaks="${r}"]`)?.value??``;ra(r,n.value,i,0)}),_.addEventListener(`submit`,async e=>{let t=e.target.closest(`[data-prep-role-chat-form]`);if(!t||!A[0])return;e.preventDefault();let n=Number(t.dataset.prepRoleChatForm);if(!Number.isFinite(n))return;let r=t.querySelector(`[data-prep-role-chat-input="${n}"]`),i=r?.value?.trim()??``;if(!i){r?.focus();return}let a=[...Rt.get(n)??[],{role:`user`,content:i}];Rt.set(n,a),v.querySelector(`.prep-role-chat`)?.replaceWith(X(Bi(A[0],{messages:a,loading:!0})));try{let e=await Zi(n,a),t=[...a,e.message];Rt.set(n,t),v.querySelector(`.prep-role-chat`)?.replaceWith(X(Bi(A[0],{messages:t})))}catch{let e=[...a,{role:`assistant`,content:`could not answer right now.`}];Rt.set(n,e),v.querySelector(`.prep-role-chat`)?.replaceWith(X(Bi(A[0],{messages:e})))}}),_.addEventListener(`click`,async e=>{let t=e.target.closest(`[data-prep-section-target]`);if(t){let e=t.dataset.prepSectionTarget,n=e?document.getElementById(e):null;if(n instanceof HTMLDetailsElement){n.open=!0,n.scrollIntoView({behavior:`smooth`,block:`start`});let e=n.querySelector(`summary`);e?.setAttribute(`tabindex`,`-1`),e?.focus({preventScroll:!0})}return}if(e.target.closest(`[data-prep-analysis]`)&&A[0]){let e=A[0].id;v.querySelector(`.prep-analysis`)?.replaceWith(X(Y(A[0],{loading:!0})));try{let t=await Wi(e,{force:!0});if(A[0]?.id!==e)return;v.querySelector(`.prep-analysis`)?.replaceWith(X(Y(A[0],{analysis:t})))}catch{v.querySelector(`.prep-analysis`)?.replaceWith(X(Y(A[0],{error:!0})))}return}if(e.target.closest(`[data-prep-resume-regenerate]`)&&A[0]){let e=A[0].id,t=v.querySelector(`.prep-resume`),n=t?.querySelector(`[data-prep-resume-tweaks="${e}"]`)?.value??``,r=t?.querySelector(`[data-prep-resume-latex="${e}"]`)?.value??``;if(!n.trim()){t?.querySelector(`[data-prep-resume-tweaks="${e}"]`)?.focus();return}Lt.set(e,n),t?.replaceWith(X(Ri(A[0],{loading:!0})));try{let t=await Xi(e,n,r);j.set(e,t.resume),v.querySelector(`.prep-resume`)?.replaceWith(X(Ri(A[0],{resume:t.resume}))),W()}catch{v.querySelector(`.prep-resume`)?.replaceWith(X(Ri(A[0],{resume:j.get(e),tweaks:n}))),W()}return}if(e.target.closest(`[data-prep-cover-letter]`)&&A[0]){let e=A[0].id,t=v.querySelector(`.prep-cover-letter`),n=t?.querySelector(`[data-prep-cover-letter-tweaks="${e}"]`)?.value??``,r=n.trim()?t?.querySelector(`[data-prep-cover-letter-latex="${e}"]`)?.value??``:``;t?.replaceWith(X(Hi(A[0],{loading:!0})));try{let t=await ta(e,n,r);M.set(e,t.cover_letter),v.querySelector(`.prep-cover-letter`)?.replaceWith(X(Hi(A[0],{coverLetter:t.cover_letter}))),W()}catch{v.querySelector(`.prep-cover-letter`)?.replaceWith(X(Hi(A[0],{coverLetter:M.get(e),tweaks:n}))),W()}return}let n=e.target.closest(`[data-prep-action]`);if(n){Gi(n.dataset.prepAction);return}let r=e.target.closest(`[data-prep-feedback]`);if(!r||!A[0])return;let i=A[0].id,a=Ft.get(i),o=Array.isArray(a?.feedback_items)?a.feedback_items.length:0,s=It.get(i)??0;if(r.dataset.prepFeedback===`accept`||r.dataset.prepFeedback===`ignore`){let e=a?.feedback_items?.[s];if(!e)return;let t=v.querySelector(`[data-prep-feedback-comment]`)?.value??``,n=r.dataset.prepFeedback,o=n;r.disabled=!0,r.textContent=n===`accept`?`adding...`:`ignoring...`;try{if(n===`accept`){let n=await Ki(i,s,e,t),r=document.querySelector(`.job[data-role-id="${CSS.escape(String(i))}"]`);n.role&&(A[0]=n.role,oi(n.role,r)),Oa(i,n.tweak_prompt??e.tweak_prompt??``),Da(i,s,a)}else await qi(i,s,e,t),Da(i,s,a)}catch{r.disabled=!1,r.textContent=o}return}let c=r.dataset.prepFeedback===`next`?1:-1;It.set(i,Math.max(0,Math.min(s+c,o-1))),v.querySelector(`.prep-analysis`)?.replaceWith(X(Y(A[0],{analysis:a})))});function Da(e,t,n){let r=n.feedback_items.filter((e,n)=>n!==t),i=Math.min(t,Math.max(r.length-1,0)),a={...n,feedback_items:r,verdict:r.length===0?`ready_to_apply`:n.verdict};It.set(e,i),Ft.set(e,a),v.querySelector(`.prep-analysis`)?.replaceWith(X(Y(A[0],{analysis:a})))}function Oa(e,t){let n=String(t||``).trim();if(!n)return;let r=Lt.get(e)?.trim()??``,i=r?`${r}\n\n${n}`:n;Lt.set(e,i);let a=v.querySelector(`[data-prep-resume-tweaks="${e}"]`);a&&(a.value=i,a.focus())}document.addEventListener(`keydown`,e=>{e.key===`Escape`&&!Le.hidden&&Kn(),e.key===`Escape`&&!o.hidden&&cn(),e.key===`Escape`&&!g.hidden&&vi(),e.key===`Escape`&&!_.hidden&&bi(),e.key===`Escape`&&!De.hidden&&da(),e.key===`Escape`&&!Ge.hidden&&er(),e.key===`Escape`&&!ot.hidden&&cr(),e.key===`Escape`&&!pt.hidden&&_r(),e.key===`Escape`&&!yt.hidden&&Nr()}),Ie.addEventListener(`click`,Gn),ze.addEventListener(`click`,Kn),Re.addEventListener(`click`,Kn);function ka(){return Array.from(document.querySelectorAll(`.pane-toggle`))}function Aa(){return ka().some(e=>e.getAttribute(`aria-expanded`)===`true`)}function ja(){Ve.textContent=Aa()?`collapse all`:`expand all`}function Ma(){document.querySelectorAll(`.pane-toggle`).forEach(e=>{e.setAttribute(`aria-expanded`,`true`),e.querySelector(`.chevron`).textContent=`v`,e.parentElement.querySelector(`.pane-body`).hidden=!1})}function Na(){document.querySelectorAll(`.job[open]`).forEach(e=>{e.open=!1}),document.querySelectorAll(`.pane-toggle`).forEach(e=>{e.setAttribute(`aria-expanded`,`false`),e.querySelector(`.chevron`).textContent=`>`,e.parentElement.querySelector(`.pane-body`).hidden=!0})}Ve.addEventListener(`click`,()=>{Aa()?Na():Ma(),ja()}),He.addEventListener(`click`,()=>{Mt=!Mt,He.textContent=Mt?`show empty`:`hide empty`,T&&jn(T.statuses)}),We.addEventListener(`click`,$n),Ke.addEventListener(`click`,er),at.addEventListener(`click`,sr),st.addEventListener(`click`,cr),ft.addEventListener(`click`,gr),mt.addEventListener(`click`,_r),Pe.addEventListener(`click`,Mr),bt.addEventListener(`click`,Nr),xt.addEventListener(`submit`,e=>{e.preventDefault(),Ir(xt).catch(()=>{C.textContent=`could not add company.`})}),St.addEventListener(`submit`,e=>{e.preventDefault(),Vr(St).catch(()=>{Et.textContent=`could not add role.`})}),w.addEventListener(`submit`,e=>{let t=e.target.closest(`[data-company-link-form]`);t&&(e.preventDefault(),Lr(t).catch(()=>{C.textContent=`could not add link.`}))}),w.addEventListener(`input`,e=>{let t=e.target.closest(`[data-company-notes]`);t&&Wr(t.dataset.companyNotes)}),w.addEventListener(`change`,e=>{let t=e.target.closest(`[data-company-tier]`);if(!t)return;let n=t.closest(`.company-panel`);n&&Kr(n,t.value),window.clearTimeout(an.get(t.dataset.companyTier)),Gr(t.dataset.companyTier).catch(()=>{Ur(`could not save company.`)})}),w.addEventListener(`click`,e=>{let t=e.target.closest(`[data-delete-company]`);if(t){let e=Hr(t.dataset.deleteCompany),n=e?.name?H(e.name):`this company`;if(!window.confirm(`Deactivate ${n}? It will be hidden from company counts and skipped during scans.`))return;t.disabled=!0,zr(t.dataset.deleteCompany).catch(()=>{C.textContent=`could not deactivate company.`,t.disabled=!1});return}let n=e.target.closest(`[data-delete-career-page]`);if(!n)return;let r=n.closest(`.company-link-row`)?.querySelector(`.company-link-text`)?.textContent?.trim();window.confirm(`Delete ${r||`this career link`}?`)&&(n.disabled=!0,Rr(n.dataset.deleteCareerPage).catch(()=>{C.textContent=`could not delete link.`,n.disabled=!1}))}),qe.addEventListener(`change`,e=>{let t=e.target.closest(`input[type="checkbox"], select, input[data-setting-text], textarea[data-setting-textarea]`);t&&yr(t)}),qe.addEventListener(`submit`,async e=>{e.preventDefault();let t=qe.querySelector(`button[type="submit"]`),n=qe.querySelectorAll(`input[type="checkbox"][name], select[name], input[data-setting-text][name], textarea[data-setting-textarea][name]`),r={};n.forEach(e=>{let t=e.name;t&&(r[t]=e.type===`checkbox`?e.checked:e.value)}),t.disabled=!0,t.textContent=`saving...`;try{S.textContent=`saving settings...`;let e=await fetch(`/api/config`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(r)});if(!e.ok)throw Error(`Config update failed`);G(await e.json(),`settings saved.`)}catch{S.textContent=`could not save settings.`,S.classList.remove(`is-empty`)}finally{t.disabled=!1,t.textContent=`save settings`}}),$e.addEventListener(`input`,()=>{nt.disabled=!$e.value.trim()}),tt.addEventListener(`click`,xr),nt.addEventListener(`click`,Sr),it.addEventListener(`click`,br),vt.addEventListener(`click`,Tr);function Pa(){if(window.location.hash===`#prepped-roles`){ua();return}da({clearHash:!1})}window.addEventListener(`popstate`,Pa),wr(),window.location.hash===`#prepped-roles`&&Pa(),Qr({applyDefaultCollapsed:!0}).catch(()=>{vn(null,`could not load resume.`),bn([],`could not load cover letter examples.`),Tn()}),Jr().then(()=>{Yr()}).catch(()=>{x.textContent=`could not load scan status`});