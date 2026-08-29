import{t as e}from"./preload-helper-Czpn1I53.js";var{sankey:t,sankeyLinkHorizontal:n}=await e(async()=>{let{sankey:e,sankeyLinkHorizontal:t}=await import(`/assets/d3-sankey.js`);return{sankey:e,sankeyLinkHorizontal:t}},[]),r=document.querySelector(`#stats`),i=document.querySelector(`#status-list`),a=document.querySelector(`#search-toggle`),o=document.querySelector(`#search-dialog`),s=document.querySelector(`#search-backdrop`),c=document.querySelector(`#search-form`),l=document.querySelector(`#search-input`),u=document.querySelector(`#close-search`),d=document.querySelector(`#materials-panel`),ee=document.querySelector(`#materials-toggle`),te=document.querySelector(`#materials-body`),f=document.querySelector(`#materials-summary`),ne=document.querySelector(`#materials-required-warning`),p=document.querySelector(`#resume-meta`),m=document.querySelector(`#resume-upload`),re=document.querySelector(`#resume-upload-button`),ie=document.querySelector(`#resume-resource-meta`),ae=document.querySelector(`#resume-resource-upload`),oe=document.querySelector(`#resume-resource-upload-button`),se=document.querySelector(`#resume-resource-list`),ce=document.querySelector(`#cover-letter-meta`),le=document.querySelector(`#cover-letter-upload`),ue=document.querySelector(`#cover-letter-upload-button`),de=document.querySelector(`#cover-letter-list`),fe=document.querySelector(`#experience-note-meta`),pe=document.querySelector(`#experience-note-upload`),me=document.querySelector(`#experience-note-upload-button`),he=document.querySelector(`#experience-note-list`);document.querySelector(`#material-index-button`);var ge=document.querySelector(`#material-index-warning`),_e=document.querySelector(`#material-index-status`),ve=document.querySelector(`#review-discovered`),ye=document.querySelector(`#prep-interested`),h=document.querySelector(`#review-view`),be=document.querySelector(`#review-heading`),xe=document.querySelector(`#review-progress`),Se=document.querySelector(`#review-card`),Ce=document.querySelector(`#close-review`),g=document.querySelector(`#prep-view`),we=document.querySelector(`#prep-heading`),Te=document.querySelector(`#prep-progress`),_=document.querySelector(`#prep-card`),Ee=document.querySelector(`#close-prep`),De=document.querySelector(`#prepped-roles`),Oe=document.querySelector(`#prepped-view`),ke=document.querySelector(`#close-prepped`),Ae=document.querySelector(`#prepped-summary`),je=document.querySelector(`#regenerate-all-cover-letters`),Me=document.querySelector(`#prepped-bulk-status`),Ne=document.querySelector(`#prepped-list`),v=document.querySelector(`#prepped-detail`),y=document.querySelector(`#scan-all-button`),Pe=document.querySelector(`#manage-companies-button`),b=document.querySelector(`#scan-status-bar`),x=document.querySelector(`#scan-status-text`),Fe=document.querySelector(`#scan-last-time`),Ie=document.querySelector(`#scan-failures-open`),Le=document.querySelector(`#scan-failures-dialog`),Re=document.querySelector(`#scan-failures-backdrop`),ze=document.querySelector(`#scan-failures-close`),Be=document.querySelector(`#scan-failures-list`),Ve=document.querySelector(`#toggle-all`),He=document.querySelector(`#collapse-empty`),Ue=document.querySelector(`#toolbar-summary`),We=document.querySelector(`#settings-open`),Ge=document.querySelector(`#settings-view`),Ke=document.querySelector(`#settings-close`),S=document.querySelector(`#settings-status`),qe=document.querySelector(`#settings-form`),Je=document.querySelector(`#settings-profile-options`),Ye=document.querySelector(`#settings-autoprep-options`),Xe=document.querySelector(`#settings-options`),Ze=document.querySelector(`#central-store-summary`),Qe=document.querySelector(`#central-store-sync-summary`),$e=document.querySelector(`#central-api-url-input`),et=document.querySelector(`#central-passkey-input`),tt=document.querySelector(`#central-save-button`),nt=document.querySelector(`#central-sync-button`),rt=document.querySelector(`#recommendation-history-summary`),it=document.querySelector(`#clear-recommendation-history`),at=document.querySelector(`#metrics-open-button`),ot=document.querySelector(`#metrics-view`),st=document.querySelector(`#metrics-close`),ct=document.querySelector(`#metrics-status`),lt=document.querySelector(`#metrics-overview`),ut=document.querySelector(`#metrics-sections`),dt=document.querySelector(`#metrics-scan-list`),ft=document.querySelector(`#sankey-open-button`),pt=document.querySelector(`#sankey-view`),mt=document.querySelector(`#sankey-close`),ht=document.querySelector(`#sankey-status`),gt=document.querySelector(`#sankey-canvas`),_t=document.querySelector(`#sankey-path-list`),vt=document.querySelector(`#app-update-button`),yt=document.querySelector(`#companies-view`),bt=document.querySelector(`#companies-close`),C=document.querySelector(`#companies-status`),xt=document.querySelector(`#company-create-form`),w=document.querySelector(`#companies-list`),St=document.querySelector(`#role-add-form`),Ct=document.querySelector(`#role-url-input`),wt=document.querySelector(`#role-company-input`),Tt=document.querySelector(`#role-company-options`),Et=document.querySelector(`#role-add-status`),Dt=3,Ot=1200,kt=new Set([`applied`,`OA`,`interview`,`rejected`,`offer`]),At=new Map([[`discovered`,`#4f6472`],[`interested`,`#00897b`],[`disinterested`,`#626970`],[`applied`,`#2257ad`],[`oa`,`#b36b00`],[`interview`,`#5f2bd8`],[`rejected`,`#b93d2d`],[`offer`,`#137347`],[`closed`,`#53606b`],[`archived`,`#765b4a`]]),jt=/^(?:about (?:the )?(?:role|team|job)|about this role|job description|job responsibilities|minimum qualifications|preferred qualifications|qualifications|requirements|responsibilities|what to expect|what (?:you'll|you’ll|you will) (?:bring|do)|what'?s in it for you|who you are|your objectives|your skills & talents):?$/i,Mt=!0,T=null,Nt=null,E=[],D=[],O=[],Pt=null,k=[],A=[],j=new Map,Ft=new Map,M=new Map,It=new Map,N=new Map,Lt=new Map,Rt=new Map,zt=new Map,P=[],F=null,Bt=null,Vt=!1,I=``,L=null,Ht=new Set,Ut=new Map,R=new Set,Wt=new Set,z=new Map,Gt=new Map,Kt=new Map,qt=new Set,Jt=!1,Yt=0,Xt=null,Zt=!1,Qt=null,$t=null,en=null,tn=null,B=null,nn=[],rn=new Map;function V(){return T?.query?.trim()??``}function an(){let e=!!V();a.classList.toggle(`search-active`,e),a.setAttribute(`aria-label`,e?`clear search`:`search jobs`)}function on(){l.value=V(),o.hidden=!1,c.hidden=!1,l.focus(),l.select()}function sn(){o.hidden=!0,c.hidden=!0,a.focus()}function cn(e){return e?new Intl.DateTimeFormat(void 0,{month:`short`,day:`numeric`,hour:`numeric`,minute:`2-digit`}).format(new Date(e)).toLocaleLowerCase():``}function H(e){return e?new Intl.DateTimeFormat(void 0,{month:`short`,day:`numeric`,hour:`numeric`,minute:`2-digit`}).format(new Date(e)).replace(`, `,` `).toLocaleLowerCase():``}function U(e){return String(e??``).replaceAll(`&`,`&amp;`).replaceAll(`<`,`&lt;`).replaceAll(`>`,`&gt;`).replaceAll(`"`,`&quot;`).replaceAll(`'`,`&#039;`)}function W(e){return String(e??``).toLocaleLowerCase()}function G(e){return U(W(e))}function ln(e){try{let t=new URL(String(e||``));return[`http:`,`https:`].includes(t.protocol)?t.href:``}catch{return``}}function un(e){return e}function K(e=_){e.querySelectorAll(`[data-prep-resume-latex], [data-prep-cover-letter-latex]`).forEach(un)}function dn(){return`
    <svg class="role-link-icon" viewBox="0 0 24 24" aria-hidden="true">
      <path d="M7 17 17 7"></path>
      <path d="M8 7h9v9"></path>
    </svg>
  `}function fn(){return`
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M12 5v14"></path>
      <path d="M5 12h14"></path>
    </svg>
  `}function pn(){return`
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M3 6h18"></path>
      <path d="M8 6V4h8v2"></path>
      <path d="m19 6-1 14H6L5 6"></path>
      <path d="M10 11v5"></path>
      <path d="M14 11v5"></path>
    </svg>
  `}function mn(e,t,n){let r=`<span class="role-title-text">${G(e)}</span>`;return t?`<a class="${n}" href="${U(t)}" target="_blank" rel="noreferrer">${r}${dn()}</a>`:`<span class="${n}">${r}</span>`}function hn(e){r.innerHTML=[[`companies`,e.companies_total],[`jobs`,e.jobs_total],[`applications`,e.applications_total]].map(([e,t])=>`<dl class="stat"><dt>${G(e)}</dt><dd>${t}</dd></dl>`).join(``)}function gn(e=T){if(!e){Ue.innerHTML=``;return}let t=t=>e.statuses.find(e=>e.key===t)?.count??0;Ue.innerHTML=[[`discovered`,t(`discovered`)],[`interested`,t(`interested`)],[`applied`,e.stats?.applications_total??0],[`total`,e.stats?.jobs_total??0]].map(([e,t])=>`
        <dl>
          <dt>${G(e)}</dt>
          <dd>${t}</dd>
        </dl>
      `).join(``)}function _n(e,t=``){if(Nt=e,re.textContent=e?`replace`:`upload`,t){p.textContent=t;return}if(!e){p.textContent=`no resume uploaded`;return}let n=H(e.updated_at),r=En(e.content_bytes);p.textContent=[W(e.filename),r,n].filter(Boolean).join(` | `)}function vn(e,t,n,{binary:r=!1}={}){let i=r?e.filename:e.id;return`
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
    </li>`}function yn(e,t=``){D=Array.isArray(e)?e:[],ue.textContent=D.length>0?`add`:`upload`,ce.textContent=t||(D.length===0?`no examples uploaded`:`${D.length} ${D.length===1?`example`:`examples`} stored`),de.innerHTML=D.map(e=>vn(e,`cover-letter-examples`,En(e.content_bytes))).join(``)}function bn(e,t=``){O=Array.isArray(e)?e:[],me.textContent=O.length>0?`add`:`upload`,fe.textContent=t||(O.length===0?`no notes uploaded`:`${O.length} ${O.length===1?`note`:`notes`} stored`),he.innerHTML=O.map(e=>vn(e,`experience-notes`,En(e.content_bytes))).join(``)}function xn(e,t=``){Pt=e??null;let n=Pt?.status??`missing`,r=n!==`ready`;if(O.length,ge.hidden=!r,ge.textContent=t||Pt?.warning||``,t)_e.textContent=t;else if(n===`ready`){let e=Number(Pt?.document_count??0),t=Number(Pt?.skipped_source_count??0),n=H(Pt?.generated_at);_e.innerHTML=[`${e} indexed ${e===1?`page`:`pages`}`,t?`${t} unreadable upload skipped`:``,n].filter(Boolean).map(e=>`<button type="button" class="material-index-link" data-open-material-index title="Reveal the application material index in Finder">${G(e)}</button>`).join(`<span aria-hidden="true"> | </span>`)}else _e.textContent=n===`stale`?`index out of date`:`not indexed`}function Sn(e,t=``){E=Array.isArray(e)?e:[],oe.textContent=E.length>0?`add`:`upload`,ie.textContent=t||(E.length===0?`no resources uploaded`:`${E.length} ${E.length===1?`resource`:`resources`} stored`),se.innerHTML=E.map(e=>vn(e,`resume-resources`,En(e.bytes),{binary:!0})).join(``)}function Cn(e,t={}){Yt+=1,document.querySelectorAll(`[data-preview-blob-url]`).forEach(e=>{URL.revokeObjectURL(e.dataset.previewBlobUrl)}),_n(e?.master_resume??null),Sn(e?.resume_resources??[]),yn(e?.cover_letter_examples??[]),bn(e?.experience_notes??[]),xn(e?.material_index??null),wn(e?.ui),(!Jt||t.applyDefaultCollapsed)&&(Tn(!!e?.ui?.default_collapsed),Jt=!0)}function wn(e=null){let t=Nt?`resume ready`:`no resume`,n=E.length===0?`no resources`:`${E.length} ${E.length===1?`resource`:`resources`}`,r=D.length,i=r===0?`no cover letters`:`${r} cover ${r===1?`letter`:`letters`}`,a=O.length,o=a===0?`no notes`:`${a} experience ${a===1?`note`:`notes`}`;ne.hidden=!(typeof e?.has_missing_required_materials==`boolean`?e.has_missing_required_materials:!Nt||r===0||a===0),f.textContent=`${t} | ${n} | ${i} | ${o}`}function Tn(e){d.classList.toggle(`collapsed`,e),ee.setAttribute(`aria-expanded`,String(!e)),ee.querySelector(`.materials-chevron`).textContent=e?`>`:`v`,te.hidden=e}function En(e){return Number.isFinite(e)?e<1024?`${e} b`:`${Math.round(e/1024)} kb`:``}async function Dn(e){let t=await fetch(e,{cache:`no-store`});if(!t.ok)throw Error(`Preview unavailable`);let n=await t.arrayBuffer();if(new TextDecoder(`ascii`).decode(n.slice(0,5))!==`%PDF-`)throw Error(`The selected file is not a readable PDF.`);return URL.createObjectURL(new Blob([n],{type:`application/pdf`}))}async function On(e){let t=e.closest(`.material-source-item`)?.querySelector(`[data-material-preview-body]`);if(!t)return;if(t.dataset.loaded===`true`){t.hidden=!t.hidden,e.textContent=t.hidden?`preview`:`hide`;return}e.disabled=!0,e.textContent=`loading...`;let n=e.dataset.materialView,r=e.dataset.materialId,i=Yt,a=`/api/${encodeURIComponent(n)}/${encodeURIComponent(r)}`;try{if(e.dataset.materialBinary===`true`){let e=await Dn(a);if(!t.isConnected||Yt!==i){URL.revokeObjectURL(e);return}t.dataset.previewBlobUrl=e,t.innerHTML=`<iframe title="${G(r)} preview"></iframe>`,t.querySelector(`iframe`).src=e}else{let e=await fetch(a);if(!e.ok)throw Error(`Preview unavailable`);let n=await e.json(),r=document.createElement(`pre`);r.textContent=n.content||`This source is empty.`,t.replaceChildren(r)}t.dataset.loaded=`true`,t.hidden=!1,e.textContent=`hide`}catch(n){t.textContent=n instanceof Error?n.message:`Preview unavailable`,t.hidden=!1,e.textContent=`preview`}finally{e.disabled=!1}}async function kn(e){let t=e.dataset.materialRemove,n=e.dataset.materialId;if(e.dataset.confirmRemove!==`true`){e.dataset.confirmRemove=`true`,e.textContent=`confirm remove`,e.classList.add(`danger`),window.setTimeout(()=>{!e.isConnected||e.disabled||(delete e.dataset.confirmRemove,e.textContent=`remove`,e.classList.remove(`danger`))},6e3);return}e.disabled=!0,e.textContent=`removing...`;try{let e=await fetch(`/api/${encodeURIComponent(t)}/${encodeURIComponent(n)}`,{method:`DELETE`}),r=await e.json();if(!e.ok)throw Error(r.error||`Remove failed`);Cn(r)}catch(t){e.disabled=!1,delete e.dataset.confirmRemove,e.classList.remove(`danger`),e.textContent=`remove`,window.alert(t instanceof Error?t.message:`Remove failed`)}}function An(e){i.innerHTML=e.map(e=>{let t=e.jobs.map(t=>jn(t,e.key)).join(``);return`
        <section class="status-pane ${e.count===0?`empty`:``} ${Mt?`hidden-empty`:``}" id="status-${U(e.key)}" data-bucket="${U(e.key)}">
          <button class="pane-toggle" type="button" aria-expanded="false">
            <span class="chevron">></span>
            <span class="pane-title">${G(e.label)}</span>
            <span class="count">${e.count}</span>
          </button>
          <div class="pane-body" hidden>
            ${t?`<div class="jobs">${t}</div>`:`<p class="empty-copy">no jobs in this status.</p>`}
          </div>
        </section>
      `}).join(``)}function jn(e,t){return`
    <details class="job" data-role-id="${U(e.id)}">
      <summary class="job-summary">
        <span class="job-chevron">></span>
        <span class="job-identity">
          <span class="job-company">[${G(e.company_name)}]</span>
          ${mn(e.title,e.role_url,`job-title`)}
          ${t===`interested`&&e.prep_started?Pn():``}
          ${t===`closed`&&e.updated_in_latest_scan?Mn():``}
          ${[`discovered`,`interested`].includes(t)&&e.missing_from_latest_scan?Nn():``}
        </span>
      </summary>
      <div class="job-detail">
        ${t===`discovered`?Fn(e):``}
        ${t===`interested`?In(e):``}
        ${t===`disinterested`?Ln(e):``}
        ${t===`applied`?Rn(e):``}
        ${t===`OA`?zn(e):``}
        ${t===`interview`?Bn(e):``}
        ${t===`closed`?Vn(e):``}
        <dl>
          ${e.location?`<div>
                  <dt>location</dt>
                  <dd>${G(e.location)}</dd>
                </div>`:``}
          <div>
            <dt>updated</dt>
            <dd>${cn(e.updated_at)}</dd>
          </div>
        </dl>
      </div>
    </details>
  `}function Mn(){return`<span class="latest-scan-dot" title="updated in latest scan" aria-label="updated in latest scan"></span>`}function Nn(){return`<span class="missing-latest-scan-dot" title="not seen in latest scan" aria-label="not seen in latest scan"></span>`}function Pn(){return`<span class="prep-started-dot" title="application materials started" aria-label="application materials started"></span>`}function Fn(e){return`
    <div class="job-actions job-actions-nowrap" aria-label="discovered role actions">
      <button class="job-action success" type="button" data-review-role-id="${e.id}">view</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="interested">interested</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="disinterested">disinterested</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="closed">closed</button>
    </div>
  `}function In(e){return`
    <div class="job-actions" aria-label="interested role actions">
      <button class="job-action success" type="button" data-prep-role-id="${e.id}">prep</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="applied">applied</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="disinterested">disinterested</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="closed">closed</button>
    </div>
  `}function Ln(e){return`
    <div class="job-actions" aria-label="disinterested role actions">
      <button class="job-action success" type="button" data-role-id="${e.id}" data-status="interested">interested</button>
    </div>
  `}function Rn(e){return`
    <div class="job-actions job-actions-nowrap" aria-label="applied role actions">
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="OA">oa</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="interview">interview</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="rejected">rejected</button>
    </div>
  `}function zn(e){return`
    <div class="job-actions job-actions-nowrap" aria-label="oa role actions">
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="interview">interview</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="disinterested">disinterested</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="rejected">rejected</button>
    </div>
  `}function Bn(e){return`
    <div class="job-actions" aria-label="interview role actions">
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="rejected">rejected</button>
      <button class="job-action success" type="button" data-role-id="${e.id}" data-status="offer">offer</button>
    </div>
  `}function Vn(e){return`
    <div class="job-actions" aria-label="closed role actions">
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="interested">interested</button>
    </div>
  `}function Hn(e){T=e,l.value=e.query,an(),hn(e.stats),gn(e),An(e.statuses),Fa(),fi(e.statuses),mi(e.statuses)}function Un(e){Qt=e??null;let t=!!e?.scanning,n=t&&!!e?.cancel_requested,r=Number(e?.completed_companies??0),i=Number(e?.total_companies??0),a=Number(e?.failed_companies??0),o=typeof e?.error==`string`?e.error.trim():``,s=Array.isArray(e?.failures)?e.failures:[];y.disabled=n,y.textContent=t?n?`cancelling...`:`cancel scan`:`scan roles`,y.classList.toggle(`danger`,t&&!n),b.hidden=!t&&!o&&s.length===0,b.classList.toggle(`scanning`,t),b.classList.toggle(`scan-error`,!t&&!!o||s.length>0),x.textContent=n?`cancelling scan...`:t?`scanning roles${i>0?` ${r}/${i}`:``}${a>0?`, ${a} failed`:``}`:s.length>0?`${s.length} recent scan ${s.length===1?`failure`:`failures`}`:o?`last scan error: ${o}`:`scan idle`,Ie&&Be&&(Ie.hidden=s.length===0,Be.innerHTML=s.slice(0,5).map(e=>{let t=e?.company_name||`unknown company`,n=e?.error||`scan failed`;return`
          <p>
            <span>${G(t)}</span>
            <span>${U(n)}</span>
          </p>
        `}).join(``),s.length===0&&Gn());let c=e?.last_scan_at;Fe.textContent=c?`last scan: ${H(c)}`:`last scan: never`,Zt&&!t&&Y(V()).catch(()=>{}),Zt=t}function Wn(){Ie.hidden||(Le.hidden=!1,ze.focus())}function Gn(){Le.hidden=!0}function q(e,t=``){$t=e;let n=Array.isArray(e?.settings)?e.settings:[],r=n.filter(e=>e.key?.startsWith(`applicant_`)),i=n.filter(e=>e.key?.startsWith(`autoprep_`)),a=n.filter(e=>!e.key?.startsWith(`applicant_`)&&!e.key?.startsWith(`autoprep_`)),o=e?.central??{};S.textContent=t,S.classList.toggle(`is-empty`,!t);let s=Number(e?.recommendation_history_count??0);rt.textContent=s>0?`${s} saved ${s===1?`feedback decision`:`feedback decisions`}`:`no saved resume feedback decisions`,it.disabled=s===0,Kn(o),Je.innerHTML=r.map(e=>qn(e)).join(``),Ye.innerHTML=i.map(e=>qn(e)).join(``),Xe.innerHTML=a.map(e=>qn(e)).join(``),J(!1)}function Kn(e){let t=e?.api_url??``;$e.value=t,et.value=``;let n=e?.passkey_configured?`passkey saved`:`no passkey saved`;Ze.textContent=t?`${W(t)} | ${n}`:`no api url | ${n}`,Qe.textContent=`${Number(e?.companies_linked??0)} linked | ${Number(e?.companies_unlinked??0)} unlinked | ${Number(e?.companies_needs_review??0)} review | ${Number(e?.companies_failed??0)} failed`,nt.disabled=!t}function qn(e){if(e.control===`textarea`&&e.editable!==!1)return Yn(e);if(e.control===`text`&&e.editable!==!1)return Jn(e);if(e.control===`select`&&e.editable!==!1)return Xn(e);if(e.control!==`toggle`||e.editable===!1)return Zn(e);let t=e.value?`checked`:``,n=e.default?`on by default`:`off by default`;return`
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
  `}function Jn(e){let t=e.default?`default: ${W(e.default)}`:`optional`,n=e.input_type??`text`,r=e.autocomplete??`name`;return`
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
  `}function Yn(e){return`
    <label class="setting-option setting-option-prompt">
      <span class="setting-copy">
        <span class="setting-label">${G(e.label)}</span>
        <span class="setting-description">${G(e.description)}</span>
      </span>
      <textarea
        class="setting-prompt-input"
        data-setting-textarea
        name="${U(e.key)}"
        rows="7"
        maxlength="8000"
      >${G(e.value??``)}</textarea>
    </label>
  `}function Xn(e){let t=Array.isArray(e.options)?e.options:[],n=`default: ${W(e.default)}`;return`
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
  `}function Zn(e){let t=e.default?`on by default`:`off by default`,n=e.value?`automatic`:`off`;return`
    <div class="setting-option setting-option-readonly">
      <span class="setting-copy">
        <span class="setting-label">${G(e.label)}</span>
        <span class="setting-description">${G(e.description)}</span>
        <span class="setting-default">${G(t)}</span>
      </span>
      <span class="setting-badge">${G(n)}</span>
    </div>
  `}function J(e){qe.querySelectorAll(`input, select, textarea`).forEach(t=>{t.disabled=e}),tt.disabled=e,nt.disabled=e||!$e.value.trim(),vt.disabled=e}async function Qn(){Ge.hidden=!1,document.body.classList.add(`settings-open`),Ke.focus(),$t?q($t):(S.textContent=`loading settings...`,S.classList.remove(`is-empty`),Xe.innerHTML=``);try{await er()}catch{S.textContent=`could not load settings.`}}function $n(){Ge.hidden=!0,document.body.classList.remove(`settings-open`),We.focus()}async function er(){let e=await fetch(`/api/config`);if(!e.ok)throw Error(`Config request failed`);q(await e.json())}function tr(e){let t=e?.value;return t==null?`n/a`:e?.kind===`ratio`?Number(t).toLocaleString(void 0,{maximumFractionDigits:2,minimumFractionDigits:0}):typeof t==`number`?t.toLocaleString():W(t)}function nr(e,t=`metric-card`){return`
    <article class="${t}">
      <span>${G(e?.label)}</span>
      <strong>${U(tr(e))}</strong>
    </article>
  `}function rr(e,t=``){en=e,ct.textContent=t||(e?.updated_at?`updated ${H(e.updated_at)}`:``),ct.classList.toggle(`is-empty`,!ct.textContent);let n=Array.isArray(e?.overview)?e.overview:[],r=Array.isArray(e?.sections)?e.sections:[],i=Array.isArray(e?.recent_scans)?e.recent_scans:[];lt.innerHTML=n.map(e=>nr(e)).join(``),ut.innerHTML=r.map(ir).join(``),dt.innerHTML=i.length?i.map(ar).join(``):`<p class="empty-copy">no scan runs recorded.</p>`}function ir(e){let t=Array.isArray(e?.metrics)?e.metrics:[];return`
    <section class="metrics-section">
      <div class="metrics-section-heading">
        <h3>${G(e?.title)}</h3>
      </div>
      <div class="metrics-section-grid">
        ${t.map(e=>nr(e,`metric-card metric-card-compact`)).join(``)}
      </div>
    </section>
  `}function ar(e){let t=e?.scan_status??`unknown`,n=e?.started_at?H(e.started_at):`not started`,r=e?.finished_at?H(e.finished_at):`not finished`,i=e?.error?`<span>${G(e.error)}</span>`:``;return`
    <article class="metrics-scan-row">
      <div>
        <strong>${G(e?.company_name??`unknown company`)}</strong>
        <span>${G(n)} -> ${G(r)}</span>
        ${i}
      </div>
      <span class="metrics-status-pill">${G(t)}</span>
    </article>
  `}async function or(){ot.hidden=!1,document.body.classList.add(`metrics-open`),st.focus(),en?rr(en):(ct.textContent=`loading metrics...`,ct.classList.remove(`is-empty`),lt.innerHTML=``,ut.innerHTML=``,dt.innerHTML=``);try{await cr()}catch{ct.textContent=`could not load metrics.`}}function sr(){ot.hidden=!0,document.body.classList.remove(`metrics-open`),at.focus()}async function cr(){let e=await fetch(`/api/metrics`);if(!e.ok)throw Error(`Metrics request failed`);rr(await e.json())}function lr(e,t=``){tn=e;let n=Number(e?.role_count??0),r=Array.isArray(e?.links)?e.links:[],i=Array.isArray(e?.paths)?e.paths:[];ht.textContent=t||(e?.updated_at?`${n.toLocaleString()} roles | updated ${H(e.updated_at)}`:``),ht.classList.toggle(`is-empty`,!ht.textContent),gt.innerHTML=r.length?ur(e):`<p class="empty-copy">no role transitions recorded yet.</p>`,_t.innerHTML=i.length?i.map(mr).join(``):`<p class="empty-copy">no role paths recorded yet.</p>`}function ur(e){let t=Array.isArray(e?.nodes)?e.nodes:[],n=Array.isArray(e?.links)?e.links:[],r=pr(t,n),i=r.nodes,a=r.links,o=(r.flowLinks??n).map(e=>{let t=i.get(e.source),n=i.get(e.target),r=a.get(e);if(!t||!n||!r)return``;let o=r.width,s=n.x<t.x,c=dr(e.target),l=r.priority?`0.42`:s?`0.28`:`0.34`,u=r.path??fr({isBacktrack:s,sourceX:t.x+t.width,sourceY:r.sourceY,targetX:n.x,targetY:r.targetY,width:o});return`
        <path class="${[`sankey-link`,s?`sankey-link-backtrack`:``,r.priority?`sankey-link-priority`:``].filter(Boolean).join(` `)}" d="${u}" fill="${r.path?`none`:c}" fill-opacity="${l}" stroke="${c}" style="stroke-width: ${r.path?o:1}px">
          <title>${G(t.label)} to ${G(n.label)}: ${Number(e.value??0).toLocaleString()}</title>
        </path>
      `}).join(``),s=Array.from(i.values()).map(e=>{let t=Number(e.history_count??e.current_count??0),n=Number(e.value??t),i=n>0?n.toLocaleString():`0`,a=e.x>r.width-180,o=a?e.x-8:e.x+e.width+8,s=Math.max(24,e.y-e.height/2-16),c=a?`end`:`start`,l=dr(e.id);return`
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
  `}function dr(e){return At.get(String(e).toLowerCase())??`#4f6472`}function fr({isBacktrack:e,sourceX:t,sourceY:n,targetX:r,targetY:i,width:a}){let o=a/2,s=n-o,c=n+o,l=i-o,u=i+o;if(e){let e=Math.max(80,Math.abs(t-r)*.42);return[`M ${t} ${s}`,`C ${t-e} ${s}, ${r+e} ${l}, ${r} ${l}`,`L ${r} ${u}`,`C ${r+e} ${u}, ${t-e} ${c}, ${t} ${c}`,`Z`].join(` `)}let d=Math.max(46,(r-t)*.48);return[`M ${t} ${s}`,`C ${t+d} ${s}, ${r-d} ${l}, ${r} ${l}`,`L ${r} ${u}`,`C ${r-d} ${u}, ${t+d} ${c}, ${t} ${c}`,`Z`].join(` `)}function pr(e,r){let i=new Map([[`discovered`,0],[`interested`,1],[`disinterested`,2],[`applied`,2],[`oa`,3],[`interview`,3],[`rejected`,4],[`closed`,4],[`archived`,4]]),a=new Map,o=new Map;r.forEach(e=>{a.set(e.target,(a.get(e.target)??0)+Number(e.value??0)),o.set(e.source,(o.get(e.source)??0)+Number(e.value??0))});let s=e.filter(e=>Number(e?.history_count??e?.current_count??0)>0||a.has(e.id)||o.has(e.id)),c=new Set(s.map(e=>e.id)),l=r.filter(e=>c.has(e.source)&&c.has(e.target)&&Number(e.value??0)>0),u=e=>i.get(String(e).toLowerCase())??0,d=l.filter(e=>u(e.target)>=u(e.source)),ee=l.filter(e=>u(e.target)<u(e.source)),te={nodes:s.map(e=>({...e,fixedValue:Math.max(0,Number(e?.history_count??e?.current_count??0))})),links:d.map(e=>({...e}))},f=t().nodeId(e=>e.id).nodeWidth(26).nodePadding(44).nodeAlign((e,t)=>Math.min(t-1,u(e.id))).extent([[92,88],[1014,634]]).iterations(32)(te),ne=new Map;f.nodes.forEach(e=>{ne.set(e.id,{...e,x:e.x0,y:e.y0+(e.y1-e.y0)/2,width:e.x1-e.x0,height:Math.max(1.5,e.y1-e.y0),value:Number(e.fixedValue??e.value??0)})});let p=new Map,m=[],re=n();f.links.forEach(e=>{let t={source:e.source.id,target:e.target.id,value:e.value};m.push(t),p.set(t,{path:re(e),width:Math.max(1.5,e.width),sourceY:e.y0,targetY:e.y1,priority:Number(e.value??0)>=20})});let ie=Math.max(.6,...f.links.map(e=>Number(e.width??0)/Math.max(1,Number(e.value??0))));return ee.forEach(e=>{let t=ne.get(e.source),n=ne.get(e.target);if(!t||!n)return;let r=Math.max(1.5,Number(e.value??0)*ie),i={...e};m.push(i),p.set(i,{width:r,sourceY:t.y+t.height/2-r/2,targetY:n.y+n.height/2-r/2,priority:!1})}),m.sort((e,t)=>Number(e.value??0)-Number(t.value??0)),{flowLinks:m,height:720,links:p,nodes:ne,width:1120}}function mr(e){let t=Array.isArray(e?.path)?e.path:[];return`
    <article class="sankey-path-row">
      <div>
        <strong>${G(e?.company_name??`unknown company`)} / ${G(e?.title??`untitled role`)}</strong>
        <span>${t.map(e=>G(e)).join(` -> `)}</span>
      </div>
      <span class="metrics-status-pill">${Number(e?.loops_collapsed??0).toLocaleString()} loops</span>
    </article>
  `}async function hr(){Ge.hidden=!0,document.body.classList.remove(`settings-open`),pt.hidden=!1,document.body.classList.add(`sankey-open`),mt.focus(),tn?lr(tn):(ht.textContent=`loading role flow...`,ht.classList.remove(`is-empty`),gt.innerHTML=``,_t.innerHTML=``);try{await _r()}catch{ht.textContent=`could not load role flow.`}}function gr(){pt.hidden=!0,document.body.classList.remove(`sankey-open`),We.focus()}async function _r(){let e=await fetch(`/api/role-sankey`);if(!e.ok)throw Error(`Role sankey request failed`);lr(await e.json())}async function vr(e){let t=e.name;if(!t)return;let n=e.type===`checkbox`?!e.checked:$t?.settings?.find(e=>e.key===t)?.value,r=e.type===`checkbox`?e.checked:e.value;J(!0),S.textContent=`saving settings...`,S.classList.remove(`is-empty`);try{let e=await fetch(`/api/config`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({[t]:r})});if(!e.ok)throw Error(`Config update failed`);q(await e.json(),`settings saved.`)}catch{e.type===`checkbox`?e.checked=n:n!==void 0&&(e.value=n),S.textContent=`could not save settings.`,J(!1)}}async function yr(){it.disabled=!0,S.textContent=`clearing recommendation history...`,S.classList.remove(`is-empty`);try{let e=await fetch(`/api/recommendation-history/clear`,{method:`POST`});if(!e.ok)throw Error(`Recommendation history clear failed`);let t=await e.json();q(t.config,`cleared ${t.deleted_count} saved decisions.`)}catch{S.textContent=`could not clear recommendation history.`,it.disabled=!1}}async function br(){let e=$e.value.trim();if(!e){S.textContent=`central api url is required.`,S.classList.remove(`is-empty`);return}let t={central_api_url:e},n=et.value.trim();n&&(t.central_passkey=n),J(!0),S.textContent=`saving central settings...`,S.classList.remove(`is-empty`);try{let e=await fetch(`/api/config`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(t)});if(!e.ok)throw Error(`Central settings update failed`);q(await e.json(),`central settings saved.`)}catch{S.textContent=`could not save central settings.`,J(!1)}}async function xr(){nt.disabled=!0,S.textContent=`syncing remote company ids...`,S.classList.remove(`is-empty`);try{let e=await fetch(`/api/central/resolve-companies`,{method:`POST`});if(!e.ok)throw Error(`Central company sync failed`);let t=await e.json(),n=t.result??{},r=t.pulled_companies,i=r?` remote: ${Number(r.created??0)} created, ${Number(r.linked??0)} linked, ${Number(r.existing??0)} existing.`:``;q(t.config,`company sync: ${Number(n.linked??0)} matched, ${Number(n.created??0)} created, ${Number(n.needs_review??0)} review, ${Number(n.failed??0)} failed.${i}`),t.companies&&(B=t.companies,Er(t.companies.companies))}catch{S.textContent=`could not sync companies.`,nt.disabled=!$e.value.trim()}}async function Sr(){let e=await fetch(`/api/central/resolve-companies`,{method:`POST`});if(!e.ok)throw Error(`Central company sync failed`);let t=await e.json();t.companies&&(B=t.companies,Er(t.companies.companies))}async function Cr(){let e=Sr().catch(()=>{});await Promise.all([Y().catch(()=>{i.innerHTML=`<p class="empty-copy">could not load jobs.</p>`}),Pr().catch(()=>{Et.textContent=`could not load companies.`})]),await e}async function wr(){if(window.confirm(`Update callumployed and restart the tracker?`)){J(!0),vt.disabled=!0,S.textContent=`updating callumployed; tracker will restart shortly...`,S.classList.remove(`is-empty`);try{if(!(await fetch(`/api/app/update`,{method:`POST`})).ok)throw Error(`App update failed`);S.textContent=`update started. reconnect in a moment.`}catch{S.textContent=`could not start update.`,J(!1)}}}function Tr(e,t=``){B=e;let n=Array.isArray(e?.companies)?e.companies:[];if(Er(n),C.textContent=t||`${n.length} ${n.length===1?`company`:`companies`} stored`,C.classList.toggle(`is-empty`,n.length===0&&!t),n.length===0){w.innerHTML=`<p class="empty-copy">no companies yet.</p>`;return}w.innerHTML=n.map(e=>Dr(e)).join(``)}function Er(e){nn=Array.isArray(e)?e:[],Tt.innerHTML=nn.map(e=>`<option value="${U(e.name)}"></option>`).join(``)}function Dr(e){let t=Array.isArray(e.career_pages)?e.career_pages:[],n=H(e.updated_at),r=Or(e.prestige_tier),i=Number(e.scan_count??0),a=Number(e.discovered_role_count??0),o=i>0&&a===0?`<span class="company-discovery-status">Discovered 0 potential roles</span>`:``;return`
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
              ${kr(e.prestige_tier)}
            </select>
          </label>
          <div>
            <span>browser wait</span>
            <strong>${Number(e.browser_extra_wait_ms??0)}ms</strong>
          </div>
        </div>
        <div class="company-links">
          ${t.length>0?t.map(e=>Ar(e)).join(``):`<p class="company-empty-links">no career links yet.</p>`}
        </div>
        <section class="company-link-panel" aria-label="add career link">
          <form class="company-link-form" data-company-link-form="${e.id}">
            <input name="label" type="text" placeholder="label" aria-label="career link label" />
            <input name="url" type="url" placeholder="https://..." aria-label="career link url" required />
            <button class="company-link-add" type="submit" aria-label="add career link" title="add career link">
              ${fn()}
            </button>
          </form>
        </section>
        <div class="company-danger-row">
          <button class="company-delete-button" type="button" data-delete-company="${e.id}">
            ${pn()}
            <span>deactivate company</span>
          </button>
        </div>
      </div>
    </details>
  `}function Or(e){let t=String(e??``);return[`0`,`1`,`2`,`3`,`4`].includes(t)?`company-tier-${t}`:`company-tier-unset`}function kr(e){let t=String(e??``);return[``,`0`,`1`,`2`,`3`,`4`].map(e=>{let n=e?`tier ${e}`:`not set`,r=e===t?` selected`:``;return`<option value="${U(e)}"${r}>${G(n)}</option>`}).join(``)}function Ar(e){let t=e.label?G(e.label):`career page`,n=U(e.url);return`
    <div class="company-link-row" data-career-page-id="${e.id}">
      <a class="company-link-url" href="${n}" target="_blank" rel="noreferrer">
        <span class="company-link-label">${t}</span>
        <span class="company-link-text">${U(e.url)}</span>
      </a>
      <button class="company-link-delete" type="button" data-delete-career-page="${e.id}" aria-label="delete ${t} link" title="delete link">
        ${pn()}
      </button>
    </div>
  `}async function jr(){yt.hidden=!1,document.body.classList.add(`companies-open`),bt.focus(),B?Tr(B):(C.textContent=`loading companies...`,C.classList.remove(`is-empty`),w.innerHTML=``);try{await Nr()}catch{C.textContent=`could not load companies.`}}function Mr(){yt.hidden=!0,document.body.classList.remove(`companies-open`),Pe.focus()}async function Nr(e=``){let t=await fetch(`/api/companies`);if(!t.ok)throw Error(`Companies request failed`);Tr(await t.json(),e)}async function Pr(){let e=await fetch(`/api/companies`);if(!e.ok)throw Error(`Companies request failed`);Er((await e.json()).companies)}async function Fr(e){let t=new FormData(e),n={name:String(t.get(`name`)??``),career_url:String(t.get(`career_url`)??``),notes:String(t.get(`notes`)??``)};C.textContent=`adding company...`;let r=await fetch(`/api/companies`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(n)});if(!r.ok)throw Error(`Company create failed`);e.reset(),Tr(await r.json(),`company added.`),Y(V()).catch(()=>{})}async function Ir(e){let t=e.dataset.companyLinkForm;if(!t)return;let n=new FormData(e),r={label:String(n.get(`label`)??``),url:String(n.get(`url`)??``)};C.textContent=`adding link...`;let i=await fetch(`/api/companies/${encodeURIComponent(t)}/career-pages`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(r)});if(!i.ok)throw Error(`Career page create failed`);e.reset(),Tr(await i.json(),`link added.`)}async function Lr(e){C.textContent=`deleting link...`;let t=await fetch(`/api/company-career-pages/${encodeURIComponent(e)}`,{method:`DELETE`});if(!t.ok)throw Error(`Career page delete failed`);Tr(await t.json(),`link deleted.`)}async function Rr(e){C.textContent=`deactivating company...`;let t=await fetch(`/api/companies/${encodeURIComponent(e)}`,{method:`DELETE`});if(!t.ok)throw Error(`Company deactivate failed`);Tr(await t.json(),`company deactivated.`),Y(V()).catch(()=>{})}function zr(){let e=wt.value.trim().toLocaleLowerCase();return nn.find(t=>t.name.toLocaleLowerCase()===e)}async function Br(e){let t=zr();if(!t?.id){Et.textContent=`pick a saved company.`;return}let n=new FormData(e),r={company_id:t.id,role_url:String(n.get(`role_url`)??``)};Et.textContent=`adding role...`;let i=await fetch(`/api/roles`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(r)});if(!i.ok)throw Error(`Role create failed`);let a=await i.json();a.tracker?Hn(a.tracker):await Y(V()),Ct.value=``;let o=a.role?.title?W(a.role.title):`role`;Et.textContent=a.scan_error?`${o} added; scan could not finish.`:`${o} added.`}function Vr(e){return(Array.isArray(B?.companies)?B.companies:[]).find(t=>String(t.id)===String(e))}function Hr(e){C.textContent=e,C.classList.remove(`is-empty`)}function Ur(e){window.clearTimeout(rn.get(e)),rn.set(e,window.setTimeout(()=>{Wr(e).catch(()=>{Hr(`could not save company.`)})},700))}async function Wr(e){let t=w.querySelector(`[data-company-id="${CSS.escape(String(e))}"]`);if(!t)return;let n=t.querySelector(`[data-company-notes="${CSS.escape(String(e))}"]`),r=t.querySelector(`[data-company-tier="${CSS.escape(String(e))}"]`),i=Vr(e),a={notes:n?.value??i?.notes??``,prestige_tier:r?.value??i?.prestige_tier??``};i&&(i.notes=a.notes,i.prestige_tier=a.prestige_tier),Gr(t,a.prestige_tier),Hr(`saving company...`);let o=await fetch(`/api/companies/${encodeURIComponent(e)}`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(a)});if(!o.ok)throw Error(`Company update failed`);B=await o.json(),Hr(`company saved.`),Kr(e)}function Gr(e,t){e.classList.remove(`company-tier-unset`,`company-tier-0`,`company-tier-1`,`company-tier-2`,`company-tier-3`,`company-tier-4`),e.classList.add(Or(t))}function Kr(e){let t=w.querySelector(`[data-company-id="${CSS.escape(String(e))}"]`),n=Vr(e);if(!t||!n)return;let r=Array.isArray(n.career_pages)?n.career_pages:[],i=H(n.updated_at),a=t.querySelector(`.company-summary-meta`);a&&(a.textContent=`${r.length} ${r.length===1?`link`:`links`}${i?` | updated ${i}`:``}`)}async function qr(){let e=await fetch(`/api/scan/status`);if(e.status===404){y.disabled=!0,b.hidden=!0,b.classList.add(`scan-error`),x.textContent=`restart server to enable scanning`;return}if(!e.ok)throw Error(`Scan status request failed`);Un(await e.json())}function Jr(){Xt===null&&(Xt=window.setInterval(()=>{qr().catch(()=>{})},3e3))}async function Yr(){y.disabled=!0,y.textContent=`starting...`;try{let e=await fetch(`/api/scan/all`,{method:`POST`});if(e.status===404){y.disabled=!0,y.textContent=`scan roles`,b.hidden=!0,b.classList.add(`scan-error`),x.textContent=`restart server to enable scanning`;return}if(!e.ok&&e.status!==409)throw Error(`Scan start failed`);Un(await e.json()),Jr()}catch{y.disabled=!1,y.textContent=`scan roles`,b.hidden=!0,b.classList.add(`scan-error`),x.textContent=`could not start scan`}}async function Xr(){y.disabled=!0,y.textContent=`cancelling...`;try{let e=await fetch(`/api/scan/cancel`,{method:`POST`});if(e.status===404){y.disabled=!0,y.textContent=`scan roles`,b.hidden=!0,b.classList.add(`scan-error`),x.textContent=`restart server to enable scanning`;return}if(!e.ok&&e.status!==409)throw Error(`Scan cancel failed`);Un(await e.json()),Jr()}catch{y.disabled=!1,y.textContent=`cancel scan`,b.hidden=!1,b.classList.add(`scan-error`),x.textContent=`could not cancel scan`}}async function Y(e=``){i.innerHTML=`<p class="empty-copy">loading jobs...</p>`;let t=new URLSearchParams;e&&t.set(`q`,e);let n=await fetch(`/api/tracker?${t.toString()}`);if(!n.ok)throw Error(`Tracker request failed`);Hn(await n.json())}async function Zr(e={}){let t=await fetch(`/api/application-materials`);if(!t.ok)throw Error(`Application materials request failed`);Cn(await t.json(),e)}async function Qr(e){if(e){if(!e.name.toLowerCase().endsWith(`.tex`)){_n(Nt,`resume must be a .tex file.`);return}re.disabled=!0,_n(Nt,`uploading...`);try{let t=await e.text();if(!(await fetch(`/api/master-resume`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({filename:e.name,content:t})})).ok)throw Error(`Master resume upload failed`);await Zr()}catch{_n(Nt,`could not save resume.`),wn()}finally{m.value=``,re.disabled=!1}}}async function $r(e){let t=Array.from(e??[]);if(t.length!==0){oe.disabled=!0,Sn(E,`uploading ${t.length} ${t.length===1?`resource`:`resources`}...`);try{for(let e of t)if(!(await fetch(`/api/resume-resources`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({filename:e.name,content_base64:await ni(e)})})).ok)throw Error(`Resume resource upload failed`);await Zr()}catch{Sn(E,`could not save every resource.`),wn()}finally{ae.value=``,oe.disabled=!1}}}async function ei(e){let t=Array.from(e??[]);if(t.length!==0){ue.disabled=!0,yn(D,`uploading ${t.length} ${t.length===1?`example`:`examples`}...`);try{for(let e of t){let t={filename:e.name};if([`.pdf`,`.docx`].some(t=>e.name.toLowerCase().endsWith(t))?t.content_base64=await ni(e):t.content=await e.text(),!(await fetch(`/api/cover-letter-examples`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(t)})).ok)throw Error(`Cover letter example upload failed`)}await Zr()}catch{yn(D,`could not save every example.`),wn()}finally{le.value=``,ue.disabled=!1}}}async function ti(e){let t=Array.from(e??[]);if(t.length!==0){me.disabled=!0,bn(O,`uploading ${t.length} ${t.length===1?`note`:`notes`}...`);try{for(let e of t){let t=e.name.toLowerCase(),n={filename:e.name};if(t.endsWith(`.pdf`)||t.endsWith(`.docx`)?n.content_base64=await ni(e):n.content=await e.text(),!(await fetch(`/api/experience-notes`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(n)})).ok)throw Error(`Experience note upload failed`)}j.clear(),await Zr()}catch{bn(O,`could not save every note.`),wn()}finally{pe.value=``,me.disabled=!1}}}function ni(e){return new Promise((t,n)=>{let r=new FileReader;r.addEventListener(`load`,()=>{let e=String(r.result??``);t(e.includes(`,`)?e.split(`,`,2)[1]:e)}),r.addEventListener(`error`,()=>n(r.error)),r.readAsDataURL(e)})}c.addEventListener(`submit`,e=>{e.preventDefault(),Y(l.value.trim()),sn()}),a.addEventListener(`click`,()=>{if(V()){Y();return}on()}),l.addEventListener(`keydown`,e=>{e.key===`Escape`&&(e.stopPropagation(),sn())}),u.addEventListener(`click`,sn),s.addEventListener(`click`,sn),re.addEventListener(`click`,()=>{m.click()}),m.addEventListener(`change`,()=>{Qr(m.files?.[0])}),oe.addEventListener(`click`,()=>{ae.click()}),ae.addEventListener(`change`,()=>{$r(ae.files)}),ue.addEventListener(`click`,()=>{le.click()}),le.addEventListener(`change`,()=>{ei(le.files)}),me.addEventListener(`click`,()=>{pe.click()}),pe.addEventListener(`change`,()=>{ti(pe.files)}),ee.addEventListener(`click`,()=>{Tn(ee.getAttribute(`aria-expanded`)===`true`)});async function ri(e){e.disabled=!0;let t=e.textContent;e.textContent=`opening...`;try{if(!(await fetch(`/api/application-materials/index/open`,{method:`POST`})).ok)throw Error(`Could not open the application material index.`)}catch(e){ge.hidden=!1,ge.textContent=e instanceof Error?e.message:`Could not open the application material index.`}finally{e.disabled=!1,e.textContent=t}}te.addEventListener(`click`,e=>{let t=e.target.closest(`[data-open-material-index]`);if(t){ri(t);return}let n=e.target.closest(`[data-material-view]`);if(n){On(n);return}let r=e.target.closest(`[data-material-remove]`);r&&kn(r)}),y.addEventListener(`click`,()=>{if(Qt?.scanning){Xr();return}Yr()}),i.addEventListener(`click`,e=>{let t=e.target.closest(`[data-review-role-id]`);if(t){gi(t.dataset.reviewRoleId);return}let n=e.target.closest(`[data-prep-role-id]`);if(n){vi(n.dataset.prepRoleId);return}let r=e.target.closest(`.job-action`);if(r){ii(r);return}let i=e.target.closest(`.pane-toggle`);if(!i)return;let a=i.parentElement.querySelector(`.pane-body`),o=i.getAttribute(`aria-expanded`)===`true`;i.setAttribute(`aria-expanded`,String(!o)),i.querySelector(`.chevron`).textContent=o?`>`:`v`,a.hidden=o,Fa()});async function ii(e){let{roleId:t,status:n}=e.dataset;if(!t||!n)return;let r=e.closest(`.job-actions`),i=e.closest(`.job`);r.querySelectorAll(`button`).forEach(e=>{e.disabled=!0}),e.textContent=`updating...`;try{let e=await fetch(`/api/roles/${encodeURIComponent(t)}/status`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({status:n})});if(!e.ok)throw Error(`Status update failed`);ai((await e.json()).role,i)}catch{r.querySelectorAll(`button`).forEach(e=>{e.disabled=!1}),e.textContent=n===`disinterested`?`disinterested`:n.toLowerCase()}}function ai(e,t){if(!e||!T)return;let n=t?.closest(`.status-pane`)?.dataset.bucket??e.role_status,r=e.role_status,i=si(e,n,r);ci(n,r),li(n,r),gn(),fi(T.statuses),mi(T.statuses),ui(t,i,n,r),Fa()}function oi(e){if(!e||!T)return null;let t=null;return T.statuses.forEach(n=>{let r=n.jobs.findIndex(t=>String(t.id)===String(e.id));r!==-1&&(t={...n.jobs[r],...e},n.jobs[r]=t)}),fi(T.statuses),mi(T.statuses),t}function si(e,t,n){let r=e;T.statuses.forEach(t=>{let n=t.jobs.findIndex(t=>String(t.id)===String(e.id));n!==-1&&(r={...t.jobs[n],...e},t.jobs.splice(n,1),t.count=t.jobs.length)});let i=T.statuses.find(e=>e.key===n);return i&&(i.jobs.unshift(r),i.count=i.jobs.length),r}function ci(e,t){T.statuses.forEach(e=>{let t=document.querySelector(`#status-${CSS.escape(e.key)}`);t?.classList.toggle(`empty`,e.count===0);let n=t?.querySelector(`.count`);n&&(n.textContent=e.count)}),[e,t].forEach(e=>{di(document.querySelector(`#status-${CSS.escape(e)}`))})}function li(e,t){if(!T.stats)return;let n=kt.has(e),r=kt.has(t);if(n===r){hn(T.stats);return}T.stats.applications_total=Number(T.stats.applications_total??0)+(r?1:-1),hn(T.stats)}function ui(e,t,n,r){let i=document.querySelector(`#status-${CSS.escape(r)}`),a=i?.querySelector(`.pane-body`);if(!e||!i||!a)return;e.remove(),di(document.querySelector(`#status-${CSS.escape(n)}`)),a.hidden=!1;let o=i.querySelector(`.pane-toggle`);o?.setAttribute(`aria-expanded`,`true`);let s=o?.querySelector(`.chevron`);s&&(s.textContent=`v`);let c=a.querySelector(`.jobs`);c||=(a.innerHTML=`<div class="jobs"></div>`,a.querySelector(`.jobs`)),c.insertAdjacentHTML(`afterbegin`,jn(t,r)),di(i)}function di(e){if(!e)return;let t=e.querySelector(`.pane-body`);if(!t)return;let n=t.querySelector(`.jobs`),r=!!n?.querySelector(`.job`),i=t.querySelector(`.empty-copy`);if(r){i?.remove();return}n?.remove(),i||t.insertAdjacentHTML(`beforeend`,`<p class="empty-copy">no jobs in this status.</p>`)}function fi(e){ve.disabled=pi(e).length===0,ve.setAttribute(`aria-label`,`review discovered`),ve.innerHTML=`<span class="review-discovered-label">review discovered</span>`}function pi(e=T?.statuses??[]){return e.find(e=>e.key===`discovered`)?.jobs??[]}function mi(e){ye.disabled=hi(e).length===0,ye.setAttribute(`aria-label`,`prep interested`),ye.innerHTML=`<span class="review-discovered-label">prep interested</span>`}function hi(e=T?.statuses??[]){return e.find(e=>e.key===`interested`)?.jobs??[]}function gi(e=null){let t=[...pi()],n=e==null?null:String(e);if(n){let e=t.findIndex(e=>String(e.id)===n);if(e>0){let[n]=t.splice(e,1);t.unshift(n)}}k=t,h.hidden=!1,document.body.classList.add(`review-open`),bi()}function _i(){h.hidden=!0,document.body.classList.remove(`review-open`),k=[]}function vi(e=null){let t=[...hi()].sort((e,t)=>Number(!!t.prep_started)-Number(!!e.prep_started)),n=e==null?null:String(e);if(n){let e=t.findIndex(e=>String(e.id)===n);if(e>0){let[n]=t.splice(e,1);t.unshift(n)}}A=t,g.hidden=!1,document.body.classList.add(`prep-open`),Ii()}function yi(){g.hidden=!0,document.body.classList.remove(`prep-open`),A=[]}function bi(e=``){let t=k[0],n=k.length,r=t?xi(t):``;if(be.textContent=n>0?`review queue`:`review complete`,xe.textContent=n>0?`${n} discovered ${n===1?`role`:`roles`} in queue`:``,h.querySelectorAll(`.review-action`).forEach(e=>{e.disabled=n===0}),!t){Se.innerHTML=`
      <div class="review-empty">
        <h3>no discovered jobs left.</h3>
        <p>everything in this queue has been handled or moved out of discovered.</p>
      </div>
    `;return}Se.innerHTML=`
    ${e?`<p class="review-message">${U(e)}</p>`:``}
    ${r?`<p class="review-message review-message-warning">${U(r)}</p>`:``}
    <div class="review-title-row">
      <p class="review-company">${G(t.company_name)}</p>
      ${mn(t.title,t.role_url,`review-role-title`)}
    </div>
    <dl class="review-details review-primary-details">
      ${X(`location`,t.location,!1,`review-location-detail`)}
      ${X(`first`,H(t.first_seen_at))}
      ${X(`last`,H(t.last_seen_at))}
    </dl>
    ${Si(t.description)}
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
  `}function xi(e){let t=Number(e.review_later_count??0);return t<=Dt?``:`role review has been postponed ${t} times. it is recommended to set it to disinterested.`}function X(e,t,n=!1,r=``){if(!t)return``;let i=n?`<a href="${U(t)}" target="_blank" rel="noreferrer">${G(t)}</a>`:G(t);return`
    <div class="review-detail ${U(r)}">
      <dt>${G(e)}</dt>
      <dd>${i}</dd>
    </div>
  `}function Si(e){return e?`
    <div class="review-detail review-description">
      <dt>description</dt>
      <dd>${Ci(e)}</dd>
    </div>
  `:``}function Ci(e){let t=wi(String(e)).replace(/\u00a0/g,` `);if(Ti(t))return Ei(t);let n=t.split(/\r?\n/).map(e=>e.trim()).filter(Boolean),r=[],i=[],a=()=>{i.length!==0&&(r.push(`<ul>${i.map(e=>`<li>${e}</li>`).join(``)}</ul>`),i=[])};return n.forEach(e=>{let t=e.match(/^#{2,3}\s+(.+)$/);if(t){a(),r.push(`<h3>${G(t[1])}</h3>`);return}if(Pi(e)){a(),r.push(`<h3>${G(e.replace(/:$/,``))}</h3>`);return}let n=e.match(/^[-*]\s+(.+)$/);if(n){i.push(G(n[1]));return}a(),r.push(`<p>${G(e)}</p>`)}),a(),r.join(``)}function wi(e){let t=document.createElement(`textarea`);return t.innerHTML=e,t.value}function Ti(e){return/<\/?(?:a|br|div|em|h[1-6]|li|ol|p|span|strong|ul)\b/i.test(e)}function Ei(e){let t=document.createElement(`template`);t.innerHTML=e;let n=[];return Di(t.content.childNodes,n),n.join(``)}function Di(e,t){e.forEach(e=>{if(e.nodeType===Node.TEXT_NODE){let n=Mi(e.textContent);n&&t.push(`<p>${G(n)}</p>`);return}if(e.nodeType!==Node.ELEMENT_NODE)return;let n=e,r=n.tagName.toLowerCase();if(r===`script`||r===`style`||r===`br`)return;if(/^h[1-6]$/.test(r)){ki(t,n.textContent);return}if(r===`ul`||r===`ol`){let e=Ai(n);e&&t.push(e);return}if(r===`p`){Oi(n,t);return}let i=Array.from(n.children).some(e=>[`DIV`,`H1`,`H2`,`H3`,`H4`,`H5`,`H6`,`OL`,`P`,`UL`].includes(e.tagName));if([`article`,`div`,`section`].includes(r)&&i){Di(n.childNodes,t);return}let a=Array.from(n.children).filter(e=>[`UL`,`OL`].includes(e.tagName)),o=Mi(ji(n));if(o&&(Ni(o,n)?ki(t,o):t.push(`<p>${G(o)}</p>`)),a.length>0){a.forEach(e=>{let n=Ai(e);n&&t.push(n)});return}!o&&i&&Di(n.childNodes,t)})}function Oi(e,t){if(!e.querySelector(`br`)){let n=Mi(ji(e));if(!n)return;Ni(n,e)?ki(t,n):t.push(`<p>${G(n)}</p>`);return}let n=``,r=()=>{let r=Mi(n);n=``,r&&(Ni(r,e)?ki(t,r):t.push(`<p>${G(r)}</p>`))};e.childNodes.forEach(e=>{if(e.nodeType===Node.ELEMENT_NODE&&e.tagName.toLowerCase()===`br`){r();return}n+=` ${e.textContent??``}`}),r()}function ki(e,t){let n=Mi(t).replace(/:$/,``);n&&e.push(`<h3>${G(n)}</h3>`)}function Ai(e){let t=Array.from(e.children).filter(e=>e.tagName===`LI`).map(e=>{let t=Mi(ji(e)),n=Array.from(e.children).filter(e=>[`UL`,`OL`].includes(e.tagName)).map(e=>Ai(e)).filter(Boolean).join(``);return t||n?`<li>${G(t)}${n}</li>`:``}).filter(Boolean);return t.length>0?`<ul>${t.join(``)}</ul>`:``}function ji(e){let t=e.cloneNode(!0);return t.querySelectorAll(`ul, ol`).forEach(e=>{e.remove()}),t.textContent}function Mi(e){return String(e??``).replace(/\s+/g,` `).trim()}function Ni(e,t){let n=e.replace(/:$/,``).trim();return!n||n.length>90?!1:Pi(n)||/:$/.test(e)?!0:/[.!?]$/.test(n)||n.split(/\s+/).length>10?!1:t.querySelector(`strong, b, u`)?!0:Pi(n)}function Pi(e){return jt.test(String(e).trim())}async function Fi(e){let t=k[0];if(!t)return;if(e===`later`){h.querySelectorAll(`.review-action`).forEach(e=>{e.disabled=!0});try{let e=await oa(t.id);k.shift(),oi(e),bi(`moved out of this review pass.`)}catch{bi(`could not postpone that role. try again.`)}finally{h.querySelectorAll(`.review-action`).forEach(e=>{e.disabled=k.length===0})}return}if(![`interested`,`disinterested`].includes(e))return;let n=h.querySelectorAll(`.review-action`);n.forEach(e=>{e.disabled=!0});try{let n=await sa(t.id,e);k.shift(),bi(e===`interested`?`marked interested.`:`marked disinterested.`),ai(n,document.querySelector(`.job[data-role-id="${CSS.escape(String(t.id))}"]`))}catch{n.forEach(e=>{e.disabled=!1}),bi(`could not update that role. try again.`)}}async function Ii(e=``){let t=A[0],n=A.length;if(we.textContent=n>0?`prep queue`:`prep complete`,Te.textContent=n>0?`${n} interested ${n===1?`role`:`roles`} in queue`:``,g.querySelectorAll(`.review-action`).forEach(e=>{e.disabled=n===0}),!t){_.innerHTML=`
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
        ${mn(t.title,t.role_url,`review-role-title`)}
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
      ${Li(t)}
      ${Vi(t)}
      ${Ri(t.id,t.description)}
      ${zi(t)}
    </div>
  `,K(),Ji(t.id).then(e=>{!e||A[0]?.id!==t.id||(M.set(t.id,e),_.querySelector(`.prep-resume`)?.replaceWith(Z(Li(t,{resume:e}))),K())}).catch(()=>{}),aa(t.id).then(e=>{!e||A[0]?.id!==t.id||(N.set(t.id,e),_.querySelector(`.prep-cover-letter`)?.replaceWith(Z(Vi(t,{coverLetter:e}))),K())}).catch(()=>{})}function Li(e,t={}){let n=M.get(e.id),r=t.resume??n,i=t.tweaks??It.get(e.id)??``,a=`/api/roles/${encodeURIComponent(e.id)}/resume.pdf`;return t.loading?`
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
      ${Hi(e)}
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
    `}function Ri(e,t){return`
    <details class="prep-panel prep-description-panel" id="prep-description-${e}">
      <summary class="prep-analysis-header">
        <span class="prep-accordion-icon" aria-hidden="true"></span>
        <h3>description</h3>
      </summary>
      ${Si(t)}
    </details>
  `}function zi(e,t={}){let n=t.messages??Lt.get(e.id)??[],r=!!t.loading;return`
    <details class="prep-panel prep-role-chat" id="prep-chat-${e.id}">
      <summary class="prep-analysis-header">
        <span class="prep-accordion-icon" aria-hidden="true"></span>
        <h3>chat about this role</h3>
        <span>${n.length?`${n.length} messages`:`ready`}</span>
      </summary>
      <div class="prep-role-chat-log" aria-live="polite">
        ${n.length?n.map(Bi).join(``):`<p class="prep-role-chat-empty">ask about fit, risks, resume emphasis, or cover letter angle.</p>`}
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
  `}function Bi(e){let t=e?.role===`assistant`?`assistant`:`user`;return`
    <article class="prep-role-chat-message prep-role-chat-message-${t}">
      <span>${t}</span>
      <p>${G(e?.content??``)}</p>
    </article>
  `}function Vi(e,t={}){let n=N.get(e.id),r=t.coverLetter??n,i=t.tweaks??r?.tweaks??``,a=`/api/roles/${encodeURIComponent(e.id)}/cover-letter.pdf`;return t.loading?`
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
  `}function Hi(e,t={}){let n=j.get(e.id);if(!t.loading&&!t.error&&!t.analysis&&n)return Hi(e,{analysis:n});if(!t.loading&&!t.error&&!t.analysis)return`
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
      <p class="prep-verdict">${G(a)}</p>
      <p class="prep-overview">${G(r?.overview??`analysis unavailable`)}</p>
      ${s?`
            <article class="prep-feedback" data-feedback-index="${o}">
              <p class="prep-feedback-label">${G(s.label)}</p>
              <h4>${G(s.title)}</h4>
              <p>${G(s.detail)}</p>
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
      <p>${G(e.tweak_prompt)}</p>
    </div>
  `:`
      <div class="prep-proposed-edit">
        <p class="prep-proposed-label">feedback only</p>
        <p>not enough information to turn this into a safe resume tweak.</p>
      </div>
    `}async function Wi(e,t={}){if(!t.force&&j.has(e))return j.get(e);let n=await fetch(`/api/roles/${encodeURIComponent(e)}/prep-analysis`);if(!n.ok)throw Error(`Prep analysis request failed`);let r=await n.json();return r.analysis.resources=r.resources??[],j.set(e,r.analysis),r.analysis}function Z(e){let t=document.createElement(`template`);return t.innerHTML=e.trim(),t.content.firstElementChild}async function Gi(e){let t=A[0];if(!t)return;let n=g.querySelectorAll(`.review-action`);if(n.forEach(e=>{e.disabled=!0}),e===`later`){try{await oa(t.id),t.review_later_count=Number(t.review_later_count??0)+1,A.length>1?(A.push(A.shift()),Ii(`moved to the back of the prep queue.`)):Ii(`only one role is in the prep queue.`)}catch{Ii(`could not postpone prep. try again.`)}return}if(e===`applied`)try{let e=await sa(t.id,`applied`);A.shift(),Ii(`moved to applied.`),ai(e,document.querySelector(`.job[data-role-id="${CSS.escape(String(t.id))}"]`))}catch{n.forEach(e=>{e.disabled=!1}),Ii(`could not move that role. try again.`)}}async function Ki(e,t,n,r){let i=await fetch(`/api/roles/${encodeURIComponent(e)}/prep-feedback`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({feedback_index:t,feedback_item:n,comment:r})});if(!i.ok)throw Error(`Prep feedback update failed`);return i.json()}async function qi(e,t,n,r){let i=await fetch(`/api/roles/${encodeURIComponent(e)}/prep-feedback-ignore`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({feedback_index:t,feedback_item:n,comment:r})});if(!i.ok)throw Error(`Prep feedback ignore failed`);return i.json()}async function Ji(e,{force:t=!1}={}){if(!t&&M.has(e))return M.get(e);let n=await fetch(`/api/roles/${encodeURIComponent(e)}/resume`);if(!n.ok)throw Error(`Resume request failed`);let r=await n.json();return r.resume&&M.set(e,r.resume),r.resume}async function Yi(e,t){let n=await fetch(`/api/roles/${encodeURIComponent(e)}/resume/save`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({latex:t})});if(!n.ok)throw Error(`Resume save failed`);return n.json()}async function Xi(e,t,n){let r=await fetch(`/api/roles/${encodeURIComponent(e)}/resume`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({tweaks:t,previous_latex:n})});if(!r.ok)throw Error(`Resume generation failed`);return r.json()}async function Zi(e,t){let n=await fetch(`/api/roles/${encodeURIComponent(e)}/chat`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({messages:t})});if(!n.ok)throw Error(`Role chat failed`);return n.json()}function Qi(e,t,n=Ot){let r=Rt.get(e)??{timer:null,saving:!1,version:0,latex:``};r.version+=1,r.latex=t,r.timer&&clearTimeout(r.timer),r.timer=setTimeout(()=>{r.timer=null,$i(e)},n),Rt.set(e,r)}async function $i(e){let t=Rt.get(e);if(!t||t.saving)return;t.saving=!0;let n=t.version,r=t.latex;try{let i=await Yi(e,r);t.version===n&&(M.set(e,i.resume),ea(`resume`,e,i.resume))}catch{}finally{t.saving=!1,t.version!==n&&Qi(e,t.latex,0)}}function ea(e,t,n){if(!n?.pdf_base64)return;let r=e===`resume`?`[data-prep-resume-latex="${t}"]`:`[data-prep-cover-letter-latex="${t}"]`,i=_.querySelector(r)?.closest(`.prep-panel`),a=i?.querySelector(`.prep-cover-pdf`),o=i?.querySelector(`.prep-cover-pdf-link`),s=e===`resume`?`/api/roles/${encodeURIComponent(t)}/resume.pdf`:`/api/roles/${encodeURIComponent(t)}/cover-letter.pdf`;a&&(a.src=`${s}?v=${Date.now()}`),o&&(o.href=s)}async function ta(e,t=``,n=``){let r=await fetch(`/api/roles/${encodeURIComponent(e)}/cover-letter`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({tweaks:t,previous_latex:n})});if(!r.ok)throw Error(`Cover letter generation failed`);return r.json()}async function na(e,t){let n=await fetch(`/api/roles/${encodeURIComponent(e)}/cover-letter/save`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({latex:t})});if(!n.ok)throw Error(`Cover letter save failed`);return n.json()}function ra(e,t,n=``,r=Ot){let i=zt.get(e)??{timer:null,saving:!1,version:0,latex:``,tweaks:``};i.version+=1,i.latex=t,i.tweaks=n,i.timer&&clearTimeout(i.timer),i.timer=setTimeout(()=>{i.timer=null,ia(e)},r),zt.set(e,i)}async function ia(e){let t=zt.get(e);if(!t||t.saving)return;t.saving=!0;let n=t.version,r=t.latex,i=t.tweaks;try{let a=await na(e,r);t.version===n&&(N.set(e,{...a.cover_letter,tweaks:i}),ea(`coverLetter`,e,a.cover_letter))}catch{}finally{t.saving=!1,t.version!==n&&ra(e,t.latex,t.tweaks,0)}}async function aa(e){if(N.has(e))return N.get(e);let t=await fetch(`/api/roles/${encodeURIComponent(e)}/cover-letter`);if(!t.ok)throw Error(`Cover letter request failed`);let n=await t.json();return n.cover_letter&&N.set(e,n.cover_letter),n.cover_letter}async function oa(e){let t=await fetch(`/api/roles/${encodeURIComponent(e)}/review-later`,{method:`POST`});if(!t.ok)throw Error(`Review later update failed`);return(await t.json()).role}async function sa(e,t){let n=await fetch(`/api/roles/${encodeURIComponent(e)}/status`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({status:t})});if(!n.ok)throw Error(`Status update failed`);return(await n.json()).role}function ca(e){return`${e}-${globalThis.crypto?.randomUUID?.()??`${Date.now()}-${Math.random()}`}`}function la(e){window.location.hash!==e&&window.history.pushState({},``,e||`${window.location.pathname}${window.location.search}`)}async function ua({seedJobs:e=null}={}){Oe.hidden=!1,document.body.classList.add(`prepped-open`),la(`#prepped-roles`),e?(P=e,F=F??P[0]?.role_id??null,$()):P.length===0&&(Ae.textContent=`loading prepared roles...`),await fa(),pa()}function da({clearHash:e=!0}={}){Oe.hidden=!0,document.body.classList.remove(`prepped-open`),ma(),R.clear(),Wt.clear(),z.forEach(e=>URL.revokeObjectURL(e)),z.clear(),Gt.clear(),Kt.clear(),e&&window.location.hash===`#prepped-roles`&&la(``)}window.addEventListener(`pagehide`,()=>{document.querySelectorAll(`[data-preview-blob-url]`).forEach(e=>{URL.revokeObjectURL(e.dataset.previewBlobUrl)}),z.forEach(e=>URL.revokeObjectURL(e)),z.clear(),Gt.clear()});async function fa(){try{let e=await fetch(`/api/autoprep/jobs`);if(!e.ok)throw Error(`Prepped roles request failed`);let t=await e.json();P=t.jobs??[];let n=t.bulk_cover_letter_regeneration;if(n){let e=Array.isArray(n.jobs)?n.jobs:[];L={idempotencyKey:n.idempotency_key,roleIds:e.map(e=>Number(e.role_id)),jobs:e,skipped:Array.isArray(n.skipped)?n.skipped:[]}}P.some(e=>Number(e.role_id)===Number(F))||(F=P[0]?.role_id??null),$()}catch{Ae.textContent=`could not refresh preparation progress.`}}function pa(){ma(),P.some(ha)&&(Bt=window.setInterval(fa,2e3))}function ma(){Bt!==null&&window.clearInterval(Bt),Bt=null}function ha(e){return[`queued`,`generating_resume_tweaks`,`regenerating_resume`,`generating_cover_letter`].includes(e.overall_status)}function ga(e){return[e.resume_status,e.cover_letter_status].some(e=>[`failed`,`interrupted`].includes(e))}function _a(e){return e.cover_letter_status===`generating`||e.overall_status===`generating_cover_letter`}function va(e){return _a(e)||e.resume_status===`generating_tweaks`||e.resume_status===`regenerating`||e.overall_status===`generating_resume_tweaks`||e.overall_status===`regenerating_resume`}function ya(e){return e.worker_state===`queued`||e.overall_status===`queued`}function ba(e){return{queued:`Queued`,generating_resume_tweaks:`Generating resume tweaks`,regenerating_resume:`Regenerating resume`,generating_cover_letter:`Generating cover letter`,partially_complete:`Partially complete`,ready:`Ready`,failed:`Failed`,interrupted:`Interrupted`,generating_tweaks:`Generating tweaks`,regenerating:`Regenerating`,generating:`Generating`}[e]??W(e)}function xa(e,t){let n=t===`cover-letter`?`cover_letter`:`resume`;return`${e.updated_at||``}:${e[`${n}_artifact_path`]||``}`}function Q(e,{close:t=!1}={}){let n=z.get(e);n&&URL.revokeObjectURL(n),z.delete(e),Gt.delete(e),Kt.delete(e),t&&R.delete(e)}function Sa(){Gt.forEach((e,t)=>{let[n,r]=t.split(`:`),i=P.find(e=>Number(e.role_id)===Number(n));(!i||xa(i,r)!==e)&&Q(t,{close:!0})})}function Ca(){if(!L)return;let e=L.jobs||P,t=new Map(e.map(e=>[Number(e.role_id),e])),n=L.roleIds.map(e=>t.get(Number(e))),r=n.filter(e=>e?.worker_state===`idle`&&e.cover_letter_status===`ready`).length,i=n.filter(e=>!e||e.worker_state===`idle`&&[`failed`,`interrupted`].includes(e.cover_letter_status)),a=n.length-r-i.length,o=L.skipped.length?` Skipped before queueing: ${L.skipped.map(e=>`${e.company_name} — ${e.title}: ${e.reason}`).join(` · `)}`:``,s=i.length?` Queued regeneration failures: ${i.map(e=>e?`${e.company_name} — ${e.title}: ${e.cover_letter_error||`generation failed`}`:`A role left the Prepped queue before regeneration completed`).join(` · `)}`:``;I=n.length?a>0?`Cover-letter regeneration in progress: ${r} of ${n.length} complete · ${a} remaining.${o}${s}`:`Cover-letter regeneration complete: ${r} succeeded, ${i.length} failed.${o}${s}`:`No cover letters were queued.${o}`}function $(){Sa(),Ca();let e=P.filter(ha).length,t=P.filter(e=>e.worker_state===`idle`&&e.cover_letter_status===`ready`).length;Ae.textContent=P.length?`${P.length} prepped ${P.length===1?`role`:`roles`}${e?` · ${e} in progress`:``}`:`No queued or prepared roles.`,je.disabled=Vt||t===0,je.setAttribute(`aria-busy`,Vt?`true`:`false`),je.textContent=Vt?`queuing cover letters...`:`regenerate all cover letters`,Me.textContent=I,Ne.innerHTML=P.map(e=>{let t=ga(e),n=!t&&va(e),r=!t&&!n&&ya(e),i=Number(e.role_id)===Number(F)?` is-active`:``;return`
      <button type="button" class="prepped-list-item${r?` is-generation-queued`:``}${n?` is-document-generating`:``}${t?` has-generation-failure`:``}${i}" data-prepped-role="${e.role_id}">
        <strong>${G(e.company_name)}</strong><span>${G(e.title)}</span>
        <small class="status-${U(e.overall_status)}">${U(ba(e.overall_status))}</small>
      </button>`}).join(``),wa(),pa()}function wa(){let e=P.findIndex(e=>Number(e.role_id)===Number(F)),t=P[e];if(!t){v.innerHTML=`<div class="prepped-empty"><h3>nothing prepped yet.</h3><p>Queue Interested roles from Autoprep Interested.</p></div>`;return}let n=G(t.title),r=ln(t.role_url),i=r?`<a class="prepped-role-link" href="${U(r)}" target="_blank" rel="noopener noreferrer">${n}<span aria-hidden="true">↗</span></a>`:n,a=[[`Location`,t.location||`Unavailable`],[`Added`,H(t.date_added||t.created_at)||`Unavailable`],[`Last seen`,H(t.last_seen_at)||`Unavailable`],[`Posting ID`,t.posting_id||`Unavailable`]],o=Ht.has(Number(t.role_id)),s=o||ha(t),c=`${t.role_id}:description`,l=`${t.role_id}:notes`;v.innerHTML=`
    <header class="prepped-detail-heading">
      <div><p class="eyebrow">${G(t.company_name)}</p><h3>${i}</h3></div>
      <span class="prepped-status status-${U(t.overall_status)}">${U(ba(t.overall_status))}</span>
    </header>
    <dl class="prepped-role-facts">${a.map(([e,t])=>`<div><dt>${U(e)}</dt><dd>${G(t)}</dd></div>`).join(``)}</dl>
    <details class="prepped-role-description" data-prepped-detail-section="description" ${Wt.has(c)?`open`:``}>
      <summary>Job description</summary>
      <div class="prepped-description-copy">${G(t.description||`No job description was saved.`).replaceAll(`
`,`<br>`)}</div>
    </details>
    ${t.notes?`<details class="prepped-role-description" data-prepped-detail-section="notes" ${Wt.has(l)?`open`:``}><summary>Role notes</summary><div class="prepped-description-copy">${G(t.notes).replaceAll(`
`,`<br>`)}</div></details>`:``}
    <div class="prepped-document-grid">
      ${Ea(t,`resume`,`Resume`)}
      ${Ea(t,`cover-letter`,`Cover letter`)}
    </div>
    <div class="prepped-detail-actions">
      <button type="button" data-prepped-nav="previous" ${e<=0?`disabled`:``}>Previous</button>
      <button type="button" data-prepped-nav="next" ${e>=P.length-1?`disabled`:``}>Next</button>
      <button type="button" data-autoprep-open-folder ${t.artifact_directory?``:`disabled`}>Open Documents Folder</button>
      <button class="prepped-disinterested" type="button" data-autoprep-disinterested aria-busy="${o?`true`:`false`}" ${s?`disabled`:``} title="${ha(t)?`Wait for preparation to finish before moving this role`:`Move this role out of Prepped`}">${o?`Moving to Disinterested...`:`Move to Disinterested`}</button>
      <button class="success" type="button" data-autoprep-applied ${t.overall_status===`ready`?``:`disabled`}>Applied</button>
    </div>
    <p class="prepped-safety-note">Autoprep prepares files only. It never submits an application.</p>`}async function Ta(e,t){let n=`${e.role_id}:${t}`,r=xa(e,t);if(!(Gt.get(n)===r||qt.has(n))){Q(n),qt.add(n),Kt.delete(n),wa();try{let i=await Dn(`/api/autoprep/roles/${encodeURIComponent(e.role_id)}/documents/${t}.pdf?v=${encodeURIComponent(e.updated_at||``)}`),a=P.find(t=>Number(t.role_id)===Number(e.role_id));if(!R.has(n)||!a||xa(a,t)!==r){URL.revokeObjectURL(i),R.delete(n);return}z.set(n,i),Gt.set(n,r)}catch(e){Kt.set(n,e instanceof Error?e.message:`PDF preview unavailable`)}finally{qt.delete(n),Number(F)===Number(e.role_id)&&wa()}}}function Ea(e,t,n){let r=t===`cover-letter`?`cover_letter`:`resume`,i=e[`${r}_status`],a=e[`${r}_artifact_path`],o=a?.split(`/`).pop()??`Not available`,s=e[`${r}_error`],c=e[`${r}_instruction`]||``,l=`${e.role_id}:${t}`,u=Ut.get(l)??c,d=t===`cover-letter`?`Optional comments for the next version`:`Comments for the next version`,ee=t===`cover-letter`?`Optionally describe specific, truthful changes...`:`Describe specific, truthful changes...`,te=[`failed`,`interrupted`].includes(i),f=e.worker_state!==`idle`||[`queued`,`generating`,`generating_tweaks`,`regenerating`].includes(i),ne=!f&&(i===`ready`||te)&&(te||t===`cover-letter`||String(u).trim()),p=R.has(l),m=`/api/autoprep/roles/${encodeURIComponent(e.role_id)}/documents/${t}.pdf?v=${encodeURIComponent(e.updated_at||``)}`,re=z.get(l),ie=Kt.get(l),ae=qt.has(l),oe=a?`<a class="prep-cover-pdf-link" data-autoprep-view="${t}" href="${U(m)}" target="_blank" rel="noreferrer" aria-label="View ${U(n.toLowerCase())} PDF in browser">View PDF</a>`:``;return`
    <section class="prepped-document${p?` has-open-preview`:``} status-${U(i)}">
      <div class="prepped-document-heading"><h4>${U(n)}</h4><span>${U(ba(i))}</span></div>
      <p class="prepped-filename">${U(o)}</p>
      ${s?`<p class="prepped-error">${U(s)}</p>`:``}
      <div class="prepped-document-actions">
        <button type="button" data-autoprep-preview="${t}" ${a?``:`disabled`}>${p?`Hide preview`:`Preview PDF`}</button>
        ${oe}
      </div>
      <div class="prepped-pdf-preview" data-autoprep-preview-panel="${t}" ${p&&a?``:`hidden`}>
        ${p&&re?`<iframe title="${U(n)} PDF preview" src="${U(re)}"></iframe>`:``}
        ${p&&ae?`<p>Loading PDF preview...</p>`:``}
        ${p&&ie?`<p class="prepped-error">${G(ie)}</p>`:``}
      </div>
      <label class="prepped-comments-label" for="prepped-comments-${U(l)}">${d}</label>
      <textarea id="prepped-comments-${U(l)}" data-autoprep-comments="${t}" rows="4" placeholder="${ee}" ${f?`disabled`:``}>${G(u)}</textarea>
      <button class="prepped-regenerate" type="button" data-autoprep-regenerate="${t}" ${ne?``:`disabled`}>${f?`Regenerating...`:`Regenerate ${U(n)}`}</button>
    </section>`}async function Da(e,t,n){if(n.disabled)return;let r=`${e.role_id}:${t}`,i=e[`${t===`cover-letter`?`cover_letter`:`resume`}_status`],a=[`failed`,`interrupted`].includes(i),o=v.querySelector(`[data-autoprep-comments="${t}"]`),s=String(o?.value||Ut.get(r)||``).trim();if(!s&&t!==`cover-letter`&&!a){o?.focus();return}n.disabled=!0,n.textContent=`Queuing regeneration...`;try{let n=await fetch(`/api/autoprep/roles/${encodeURIComponent(e.role_id)}/${a?`retry`:`regenerate`}/${t}`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(a?{idempotency_key:ca(`retry-${t}`)}:{comments:s,idempotency_key:ca(`regenerate-${t}`)})}),i=await n.json();if(!n.ok)throw Error(i.error||`Regeneration request failed`);Ut.delete(r),Q(r,{close:!0});let o=P.findIndex(t=>Number(t.role_id)===Number(e.role_id));o>=0&&(P[o]=i.job),$()}catch(e){window.alert(e instanceof Error?e.message:`Regeneration request failed`),await fa()}}async function Oa(){if(!Vt){Vt=!0,L=null,I=`Queuing eligible cover letters...`,$();try{let e=await fetch(`/api/autoprep/cover-letters/regenerate`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({idempotency_key:ca(`regenerate-all-cover-letters`)})}),t=await e.json();if(!e.ok)throw Error(t.error||`Bulk regeneration request failed`);let n=Number(t.queued_count||0),r=Array.isArray(t.skipped)?t.skipped:[];L={roleIds:(t.jobs||[]).map(e=>Number(e.role_id)),jobs:t.jobs||[],skipped:r},!n&&!r.length&&(L=null,I=`No prepped roles are available to regenerate.`),(t.jobs||[]).forEach(e=>{let t=P.findIndex(t=>Number(t.role_id)===Number(e.role_id));t>=0&&(P[t]=e),Q(`${e.role_id}:cover-letter`,{close:!0})}),await fa(),pa()}catch(e){L=null,I=e instanceof Error?e.message:`Bulk regeneration request failed`}finally{Vt=!1,$()}}}async function ka(e,t){let n=Number(e);if(Ht.has(n))return;Ht.add(n),t.disabled=!0,t.setAttribute(`aria-busy`,`true`),t.textContent=`Moving to Disinterested...`;let r=P.findIndex(e=>Number(e.role_id)===n);try{await sa(e,`disinterested`),Q(`${e}:resume`,{close:!0}),Q(`${e}:cover-letter`,{close:!0}),r>=0&&P.splice(r,1),F=P[Math.min(r,P.length-1)]?.role_id??null,I=`Role moved to Disinterested.`,$(),Cr()}catch(e){I=e instanceof Error?e.message:`Could not move this role to Disinterested.`,await fa()}finally{Ht.delete(n),P.some(e=>Number(e.role_id)===n)&&$()}}async function Aa(e,t){if(t.disabled)return;t.disabled=!0,t.textContent=`Moving to Applied...`;let n=P.findIndex(t=>Number(t.role_id)===Number(e));try{if(!(await fetch(`/api/autoprep/roles/${encodeURIComponent(e)}/applied`,{method:`POST`})).ok)throw Error(`Applied update failed`);Q(`${e}:resume`,{close:!0}),Q(`${e}:cover-letter`,{close:!0}),P.splice(n,1),F=P[Math.min(n,P.length-1)]?.role_id??null,$(),Cr()}catch{await fa()}}ve.addEventListener(`click`,gi),Ce.addEventListener(`click`,_i),ye.addEventListener(`click`,vi),De.addEventListener(`click`,()=>ua()),ke.addEventListener(`click`,da),je.addEventListener(`click`,Oa),Ne.addEventListener(`click`,e=>{let t=e.target.closest(`[data-prepped-role]`);t&&(F=Number(t.dataset.preppedRole),$())}),v.addEventListener(`input`,e=>{let t=e.target.closest(`[data-autoprep-comments]`);if(!t)return;let n=`${F}:${t.dataset.autoprepComments}`;Ut.set(n,t.value);let r=v.querySelector(`[data-autoprep-regenerate="${t.dataset.autoprepComments}"]`),i=P.find(e=>Number(e.role_id)===Number(F)),a=t.dataset.autoprepComments===`cover-letter`?`cover_letter`:`resume`,o=i?.[`${a}_status`],s=[`failed`,`interrupted`].includes(o);r&&(r.disabled=i?.worker_state!==`idle`||![`ready`,`failed`,`interrupted`].includes(o)||!s&&t.dataset.autoprepComments!==`cover-letter`&&!t.value.trim())}),v.addEventListener(`toggle`,e=>{let t=e.target.closest(`[data-prepped-detail-section]`);if(!t)return;let n=`${F}:${t.dataset.preppedDetailSection}`;t.open?Wt.add(n):Wt.delete(n)},!0),v.addEventListener(`click`,async e=>{let t=P.find(e=>Number(e.role_id)===Number(F));if(!t)return;let n=e.target.closest(`[data-prepped-nav]`);if(n){let e=P.indexOf(t),r=n.dataset.preppedNav===`next`?1:-1;F=P[e+r]?.role_id??t.role_id,$();return}let r=e.target.closest(`[data-autoprep-preview]`);if(r){let e=r.dataset.autoprepPreview,n=`${t.role_id}:${e}`;R.has(n)?(R.delete(n),wa()):(R.add(n),wa(),Ta(t,e));return}let i=e.target.closest(`[data-autoprep-regenerate]`);if(i){Da(t,i.dataset.autoprepRegenerate,i);return}let a=e.target.closest(`[data-autoprep-open-folder]`);if(a&&!a.disabled){a.disabled=!0,a.textContent=`Opening...`;try{if(!(await fetch(`/api/autoprep/roles/${encodeURIComponent(t.role_id)}/open-folder`,{method:`POST`})).ok)throw Error(`Could not open the documents folder.`);a.textContent=`Opened in Finder`,window.setTimeout(()=>{a.isConnected&&(a.textContent=`Open Documents Folder`,a.disabled=!1)},1500)}catch(e){a.textContent=e instanceof Error?e.message:`Could not open folder`,a.disabled=!1}return}let o=e.target.closest(`[data-autoprep-disinterested]`);if(o){ka(t.role_id,o);return}let s=e.target.closest(`[data-autoprep-applied]`);s&&Aa(t.role_id,s)}),Ee.addEventListener(`click`,yi),h.addEventListener(`click`,e=>{let t=e.target.closest(`[data-review-action]`);t&&Fi(t.dataset.reviewAction)}),g.addEventListener(`click`,e=>{e.target.closest(`.prep-summary-action`)&&e.stopPropagation()}),g.addEventListener(`input`,e=>{let t=e.target.closest(`[data-prep-resume-tweaks]`);if(t){let e=Number(t.dataset.prepResumeTweaks);Number.isFinite(e)&&It.set(e,t.value);return}let n=e.target.closest(`[data-prep-resume-latex]`);if(n){let e=Number(n.dataset.prepResumeLatex);if(!Number.isFinite(e))return;Qi(e,n.value);return}let r=e.target.closest(`[data-prep-cover-letter-latex]`);if(!r)return;let i=Number(r.dataset.prepCoverLetterLatex);if(!Number.isFinite(i))return;let a=r.closest(`.prep-cover-letter`)?.querySelector(`[data-prep-cover-letter-tweaks="${i}"]`)?.value??``;ra(i,r.value,a)}),g.addEventListener(`scroll`,e=>{e.target.closest(`[data-prep-resume-latex], [data-prep-cover-letter-latex]`)},!0),g.addEventListener(`focusout`,e=>{let t=e.target.closest(`[data-prep-resume-latex]`);if(t){let e=Number(t.dataset.prepResumeLatex);if(!Number.isFinite(e))return;Qi(e,t.value,0);return}let n=e.target.closest(`[data-prep-cover-letter-latex]`);if(!n)return;let r=Number(n.dataset.prepCoverLetterLatex);if(!Number.isFinite(r))return;let i=n.closest(`.prep-cover-letter`)?.querySelector(`[data-prep-cover-letter-tweaks="${r}"]`)?.value??``;ra(r,n.value,i,0)}),g.addEventListener(`submit`,async e=>{let t=e.target.closest(`[data-prep-role-chat-form]`);if(!t||!A[0])return;e.preventDefault();let n=Number(t.dataset.prepRoleChatForm);if(!Number.isFinite(n))return;let r=t.querySelector(`[data-prep-role-chat-input="${n}"]`),i=r?.value?.trim()??``;if(!i){r?.focus();return}let a=[...Lt.get(n)??[],{role:`user`,content:i}];Lt.set(n,a),_.querySelector(`.prep-role-chat`)?.replaceWith(Z(zi(A[0],{messages:a,loading:!0})));try{let e=await Zi(n,a),t=[...a,e.message];Lt.set(n,t),_.querySelector(`.prep-role-chat`)?.replaceWith(Z(zi(A[0],{messages:t})))}catch{let e=[...a,{role:`assistant`,content:`could not answer right now.`}];Lt.set(n,e),_.querySelector(`.prep-role-chat`)?.replaceWith(Z(zi(A[0],{messages:e})))}}),g.addEventListener(`click`,async e=>{let t=e.target.closest(`[data-prep-section-target]`);if(t){let e=t.dataset.prepSectionTarget,n=e?document.getElementById(e):null;if(n instanceof HTMLDetailsElement){n.open=!0,n.scrollIntoView({behavior:`smooth`,block:`start`});let e=n.querySelector(`summary`);e?.setAttribute(`tabindex`,`-1`),e?.focus({preventScroll:!0})}return}if(e.target.closest(`[data-prep-analysis]`)&&A[0]){let e=A[0].id;_.querySelector(`.prep-analysis`)?.replaceWith(Z(Hi(A[0],{loading:!0})));try{let t=await Wi(e,{force:!0});if(A[0]?.id!==e)return;_.querySelector(`.prep-analysis`)?.replaceWith(Z(Hi(A[0],{analysis:t})))}catch{_.querySelector(`.prep-analysis`)?.replaceWith(Z(Hi(A[0],{error:!0})))}return}if(e.target.closest(`[data-prep-resume-regenerate]`)&&A[0]){let e=A[0].id,t=_.querySelector(`.prep-resume`),n=t?.querySelector(`[data-prep-resume-tweaks="${e}"]`)?.value??``,r=t?.querySelector(`[data-prep-resume-latex="${e}"]`)?.value??``;if(!n.trim()){t?.querySelector(`[data-prep-resume-tweaks="${e}"]`)?.focus();return}It.set(e,n),t?.replaceWith(Z(Li(A[0],{loading:!0})));try{let t=await Xi(e,n,r);M.set(e,t.resume),_.querySelector(`.prep-resume`)?.replaceWith(Z(Li(A[0],{resume:t.resume}))),K()}catch{_.querySelector(`.prep-resume`)?.replaceWith(Z(Li(A[0],{resume:M.get(e),tweaks:n}))),K()}return}if(e.target.closest(`[data-prep-cover-letter]`)&&A[0]){let e=A[0].id,t=_.querySelector(`.prep-cover-letter`),n=t?.querySelector(`[data-prep-cover-letter-tweaks="${e}"]`)?.value??``,r=n.trim()?t?.querySelector(`[data-prep-cover-letter-latex="${e}"]`)?.value??``:``;t?.replaceWith(Z(Vi(A[0],{loading:!0})));try{let t=await ta(e,n,r);N.set(e,t.cover_letter),_.querySelector(`.prep-cover-letter`)?.replaceWith(Z(Vi(A[0],{coverLetter:t.cover_letter}))),K()}catch{_.querySelector(`.prep-cover-letter`)?.replaceWith(Z(Vi(A[0],{coverLetter:N.get(e),tweaks:n}))),K()}return}let n=e.target.closest(`[data-prep-action]`);if(n){Gi(n.dataset.prepAction);return}let r=e.target.closest(`[data-prep-feedback]`);if(!r||!A[0])return;let i=A[0].id,a=j.get(i),o=Array.isArray(a?.feedback_items)?a.feedback_items.length:0,s=Ft.get(i)??0;if(r.dataset.prepFeedback===`accept`||r.dataset.prepFeedback===`ignore`){let e=a?.feedback_items?.[s];if(!e)return;let t=_.querySelector(`[data-prep-feedback-comment]`)?.value??``,n=r.dataset.prepFeedback,o=n;r.disabled=!0,r.textContent=n===`accept`?`adding...`:`ignoring...`;try{if(n===`accept`){let n=await Ki(i,s,e,t),r=document.querySelector(`.job[data-role-id="${CSS.escape(String(i))}"]`);n.role&&(A[0]=n.role,ai(n.role,r)),Ma(i,n.tweak_prompt??e.tweak_prompt??``),ja(i,s,a)}else await qi(i,s,e,t),ja(i,s,a)}catch{r.disabled=!1,r.textContent=o}return}let c=r.dataset.prepFeedback===`next`?1:-1;Ft.set(i,Math.max(0,Math.min(s+c,o-1))),_.querySelector(`.prep-analysis`)?.replaceWith(Z(Hi(A[0],{analysis:a})))});function ja(e,t,n){let r=n.feedback_items.filter((e,n)=>n!==t),i=Math.min(t,Math.max(r.length-1,0)),a={...n,feedback_items:r,verdict:r.length===0?`ready_to_apply`:n.verdict};Ft.set(e,i),j.set(e,a),_.querySelector(`.prep-analysis`)?.replaceWith(Z(Hi(A[0],{analysis:a})))}function Ma(e,t){let n=String(t||``).trim();if(!n)return;let r=It.get(e)?.trim()??``,i=r?`${r}\n\n${n}`:n;It.set(e,i);let a=_.querySelector(`[data-prep-resume-tweaks="${e}"]`);a&&(a.value=i,a.focus())}document.addEventListener(`keydown`,e=>{e.key===`Escape`&&!Le.hidden&&Gn(),e.key===`Escape`&&!o.hidden&&sn(),e.key===`Escape`&&!h.hidden&&_i(),e.key===`Escape`&&!g.hidden&&yi(),e.key===`Escape`&&!Oe.hidden&&da(),e.key===`Escape`&&!Ge.hidden&&$n(),e.key===`Escape`&&!ot.hidden&&sr(),e.key===`Escape`&&!pt.hidden&&gr(),e.key===`Escape`&&!yt.hidden&&Mr()}),Ie.addEventListener(`click`,Wn),ze.addEventListener(`click`,Gn),Re.addEventListener(`click`,Gn);function Na(){return Array.from(document.querySelectorAll(`.pane-toggle`))}function Pa(){return Na().some(e=>e.getAttribute(`aria-expanded`)===`true`)}function Fa(){Ve.textContent=Pa()?`collapse all`:`expand all`}function Ia(){document.querySelectorAll(`.pane-toggle`).forEach(e=>{e.setAttribute(`aria-expanded`,`true`),e.querySelector(`.chevron`).textContent=`v`,e.parentElement.querySelector(`.pane-body`).hidden=!1})}function La(){document.querySelectorAll(`.job[open]`).forEach(e=>{e.open=!1}),document.querySelectorAll(`.pane-toggle`).forEach(e=>{e.setAttribute(`aria-expanded`,`false`),e.querySelector(`.chevron`).textContent=`>`,e.parentElement.querySelector(`.pane-body`).hidden=!0})}Ve.addEventListener(`click`,()=>{Pa()?La():Ia(),Fa()}),He.addEventListener(`click`,()=>{Mt=!Mt,He.textContent=Mt?`show empty`:`hide empty`,T&&An(T.statuses)}),We.addEventListener(`click`,Qn),Ke.addEventListener(`click`,$n),at.addEventListener(`click`,or),st.addEventListener(`click`,sr),ft.addEventListener(`click`,hr),mt.addEventListener(`click`,gr),Pe.addEventListener(`click`,jr),bt.addEventListener(`click`,Mr),xt.addEventListener(`submit`,e=>{e.preventDefault(),Fr(xt).catch(()=>{C.textContent=`could not add company.`})}),St.addEventListener(`submit`,e=>{e.preventDefault(),Br(St).catch(()=>{Et.textContent=`could not add role.`})}),w.addEventListener(`submit`,e=>{let t=e.target.closest(`[data-company-link-form]`);t&&(e.preventDefault(),Ir(t).catch(()=>{C.textContent=`could not add link.`}))}),w.addEventListener(`input`,e=>{let t=e.target.closest(`[data-company-notes]`);t&&Ur(t.dataset.companyNotes)}),w.addEventListener(`change`,e=>{let t=e.target.closest(`[data-company-tier]`);if(!t)return;let n=t.closest(`.company-panel`);n&&Gr(n,t.value),window.clearTimeout(rn.get(t.dataset.companyTier)),Wr(t.dataset.companyTier).catch(()=>{Hr(`could not save company.`)})}),w.addEventListener(`click`,e=>{let t=e.target.closest(`[data-delete-company]`);if(t){let e=Vr(t.dataset.deleteCompany),n=e?.name?W(e.name):`this company`;if(!window.confirm(`Deactivate ${n}? It will be hidden from company counts and skipped during scans.`))return;t.disabled=!0,Rr(t.dataset.deleteCompany).catch(()=>{C.textContent=`could not deactivate company.`,t.disabled=!1});return}let n=e.target.closest(`[data-delete-career-page]`);if(!n)return;let r=n.closest(`.company-link-row`)?.querySelector(`.company-link-text`)?.textContent?.trim();window.confirm(`Delete ${r||`this career link`}?`)&&(n.disabled=!0,Lr(n.dataset.deleteCareerPage).catch(()=>{C.textContent=`could not delete link.`,n.disabled=!1}))}),qe.addEventListener(`change`,e=>{let t=e.target.closest(`input[type="checkbox"], select, input[data-setting-text], textarea[data-setting-textarea]`);t&&vr(t)}),qe.addEventListener(`submit`,async e=>{e.preventDefault();let t=qe.querySelector(`button[type="submit"]`),n=qe.querySelectorAll(`input[type="checkbox"][name], select[name], input[data-setting-text][name], textarea[data-setting-textarea][name]`),r={};n.forEach(e=>{let t=e.name;t&&(r[t]=e.type===`checkbox`?e.checked:e.value)}),t.disabled=!0,t.textContent=`saving...`;try{S.textContent=`saving settings...`;let e=await fetch(`/api/config`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(r)});if(!e.ok)throw Error(`Config update failed`);q(await e.json(),`settings saved.`)}catch{S.textContent=`could not save settings.`,S.classList.remove(`is-empty`)}finally{t.disabled=!1,t.textContent=`save settings`}}),$e.addEventListener(`input`,()=>{nt.disabled=!$e.value.trim()}),tt.addEventListener(`click`,br),nt.addEventListener(`click`,xr),it.addEventListener(`click`,yr),vt.addEventListener(`click`,wr);function Ra(){if(window.location.hash===`#prepped-roles`){ua();return}da({clearHash:!1})}window.addEventListener(`popstate`,Ra),Cr(),window.location.hash===`#prepped-roles`&&Ra(),Zr({applyDefaultCollapsed:!0}).catch(()=>{_n(null,`could not load resume.`),yn([],`could not load cover letter examples.`),wn()}),qr().then(()=>{Jr()}).catch(()=>{x.textContent=`could not load scan status`});