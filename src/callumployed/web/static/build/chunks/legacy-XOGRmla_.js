import{t as e}from"./preload-helper-Czpn1I53.js";var{sankey:t,sankeyLinkHorizontal:n}=await e(async()=>{let{sankey:e,sankeyLinkHorizontal:t}=await import(`/assets/d3-sankey.js`);return{sankey:e,sankeyLinkHorizontal:t}},[]),r=document.querySelector(`#stats`),i=document.querySelector(`#status-list`),a=document.querySelector(`#search-toggle`),o=document.querySelector(`#search-dialog`),s=document.querySelector(`#search-backdrop`),c=document.querySelector(`#search-form`),l=document.querySelector(`#search-input`),u=document.querySelector(`#close-search`),d=document.querySelector(`#materials-panel`),ee=document.querySelector(`#materials-toggle`),f=document.querySelector(`#materials-body`),te=document.querySelector(`#materials-summary`),p=document.querySelector(`#materials-required-warning`),m=document.querySelector(`#resume-meta`),h=document.querySelector(`#resume-upload`),ne=document.querySelector(`#resume-upload-button`),re=document.querySelector(`#resume-resource-meta`),ie=document.querySelector(`#resume-resource-upload`),ae=document.querySelector(`#resume-resource-upload-button`),oe=document.querySelector(`#resume-resource-list`),se=document.querySelector(`#cover-letter-meta`),ce=document.querySelector(`#cover-letter-upload`),le=document.querySelector(`#cover-letter-upload-button`),ue=document.querySelector(`#cover-letter-list`),de=document.querySelector(`#experience-note-meta`),fe=document.querySelector(`#experience-note-upload`),pe=document.querySelector(`#experience-note-upload-button`),me=document.querySelector(`#experience-note-list`);document.querySelector(`#material-index-button`);var he=document.querySelector(`#material-index-warning`),ge=document.querySelector(`#material-index-status`),_e=document.querySelector(`#review-discovered`),ve=document.querySelector(`#prep-interested`),g=document.querySelector(`#review-view`),ye=document.querySelector(`#review-heading`),be=document.querySelector(`#review-progress`),xe=document.querySelector(`#review-card`),Se=document.querySelector(`#close-review`),_=document.querySelector(`#prep-view`),Ce=document.querySelector(`#prep-heading`),we=document.querySelector(`#prep-progress`),v=document.querySelector(`#prep-card`),Te=document.querySelector(`#close-prep`),Ee=document.querySelector(`#prepped-roles`),De=document.querySelector(`#prepped-view`),Oe=document.querySelector(`#close-prepped`),ke=document.querySelector(`#prepped-summary`),Ae=document.querySelector(`#prepped-list`),je=document.querySelector(`#prepped-detail`),y=document.querySelector(`#scan-all-button`),Me=document.querySelector(`#manage-companies-button`),b=document.querySelector(`#scan-status-bar`),x=document.querySelector(`#scan-status-text`),Ne=document.querySelector(`#scan-last-time`),Pe=document.querySelector(`#scan-failures-open`),Fe=document.querySelector(`#scan-failures-dialog`),Ie=document.querySelector(`#scan-failures-backdrop`),Le=document.querySelector(`#scan-failures-close`),Re=document.querySelector(`#scan-failures-list`),ze=document.querySelector(`#toggle-all`),Be=document.querySelector(`#collapse-empty`),Ve=document.querySelector(`#toolbar-summary`),He=document.querySelector(`#settings-open`),Ue=document.querySelector(`#settings-view`),We=document.querySelector(`#settings-close`),S=document.querySelector(`#settings-status`),Ge=document.querySelector(`#settings-form`),Ke=document.querySelector(`#settings-profile-options`),qe=document.querySelector(`#settings-autoprep-options`),Je=document.querySelector(`#settings-options`),Ye=document.querySelector(`#central-store-summary`),Xe=document.querySelector(`#central-store-sync-summary`),Ze=document.querySelector(`#central-api-url-input`),Qe=document.querySelector(`#central-passkey-input`),$e=document.querySelector(`#central-save-button`),et=document.querySelector(`#central-sync-button`),tt=document.querySelector(`#recommendation-history-summary`),nt=document.querySelector(`#clear-recommendation-history`),rt=document.querySelector(`#metrics-open-button`),it=document.querySelector(`#metrics-view`),at=document.querySelector(`#metrics-close`),ot=document.querySelector(`#metrics-status`),st=document.querySelector(`#metrics-overview`),ct=document.querySelector(`#metrics-sections`),lt=document.querySelector(`#metrics-scan-list`),ut=document.querySelector(`#sankey-open-button`),dt=document.querySelector(`#sankey-view`),ft=document.querySelector(`#sankey-close`),pt=document.querySelector(`#sankey-status`),mt=document.querySelector(`#sankey-canvas`),ht=document.querySelector(`#sankey-path-list`),gt=document.querySelector(`#app-update-button`),_t=document.querySelector(`#companies-view`),vt=document.querySelector(`#companies-close`),C=document.querySelector(`#companies-status`),yt=document.querySelector(`#company-create-form`),w=document.querySelector(`#companies-list`),bt=document.querySelector(`#role-add-form`),xt=document.querySelector(`#role-url-input`),St=document.querySelector(`#role-company-input`),Ct=document.querySelector(`#role-company-options`),wt=document.querySelector(`#role-add-status`),Tt=3,Et=1200,Dt=new Set([`applied`,`OA`,`interview`,`rejected`,`offer`]),Ot=new Map([[`discovered`,`#4f6472`],[`interested`,`#00897b`],[`disinterested`,`#626970`],[`applied`,`#2257ad`],[`oa`,`#b36b00`],[`interview`,`#5f2bd8`],[`rejected`,`#b93d2d`],[`offer`,`#137347`],[`closed`,`#53606b`],[`archived`,`#765b4a`]]),kt=/^(?:about (?:the )?(?:role|team|job)|about this role|job description|job responsibilities|minimum qualifications|preferred qualifications|qualifications|requirements|responsibilities|what to expect|what (?:you'll|you’ll|you will) (?:bring|do)|what'?s in it for you|who you are|your objectives|your skills & talents):?$/i,At=!0,T=null,E=null,D=[],O=[],k=[],A=null,j=[],M=[],N=new Map,jt=new Map,P=new Map,Mt=new Map,F=new Map,Nt=new Map,Pt=new Map,Ft=new Map,I=[],L=null,It=null,Lt=new Map,R=new Set,z=new Map,Rt=new Map,zt=new Map,Bt=new Set,Vt=!1,Ht=0,Ut=null,Wt=!1,Gt=null,Kt=null,qt=null,Jt=null,B=null,Yt=[],Xt=new Map;function V(){return T?.query?.trim()??``}function Zt(){let e=!!V();a.classList.toggle(`search-active`,e),a.setAttribute(`aria-label`,e?`clear search`:`search jobs`)}function Qt(){l.value=V(),o.hidden=!1,c.hidden=!1,l.focus(),l.select()}function $t(){o.hidden=!0,c.hidden=!0,a.focus()}function en(e){return e?new Intl.DateTimeFormat(void 0,{month:`short`,day:`numeric`,hour:`numeric`,minute:`2-digit`}).format(new Date(e)).toLocaleLowerCase():``}function H(e){return e?new Intl.DateTimeFormat(void 0,{month:`short`,day:`numeric`,hour:`numeric`,minute:`2-digit`}).format(new Date(e)).replace(`, `,` `).toLocaleLowerCase():``}function U(e){return String(e??``).replaceAll(`&`,`&amp;`).replaceAll(`<`,`&lt;`).replaceAll(`>`,`&gt;`).replaceAll(`"`,`&quot;`).replaceAll(`'`,`&#039;`)}function W(e){return String(e??``).toLocaleLowerCase()}function G(e){return U(W(e))}function tn(e){try{let t=new URL(String(e||``));return[`http:`,`https:`].includes(t.protocol)?t.href:``}catch{return``}}function nn(e){return e}function K(e=v){e.querySelectorAll(`[data-prep-resume-latex], [data-prep-cover-letter-latex]`).forEach(nn)}function rn(){return`
    <svg class="role-link-icon" viewBox="0 0 24 24" aria-hidden="true">
      <path d="M7 17 17 7"></path>
      <path d="M8 7h9v9"></path>
    </svg>
  `}function an(){return`
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M12 5v14"></path>
      <path d="M5 12h14"></path>
    </svg>
  `}function on(){return`
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M3 6h18"></path>
      <path d="M8 6V4h8v2"></path>
      <path d="m19 6-1 14H6L5 6"></path>
      <path d="M10 11v5"></path>
      <path d="M14 11v5"></path>
    </svg>
  `}function sn(e,t,n){let r=`<span class="role-title-text">${G(e)}</span>`;return t?`<a class="${n}" href="${U(t)}" target="_blank" rel="noreferrer">${r}${rn()}</a>`:`<span class="${n}">${r}</span>`}function cn(e){r.innerHTML=[[`companies`,e.companies_total],[`jobs`,e.jobs_total],[`applications`,e.applications_total]].map(([e,t])=>`<dl class="stat"><dt>${G(e)}</dt><dd>${t}</dd></dl>`).join(``)}function ln(e=T){if(!e){Ve.innerHTML=``;return}let t=t=>e.statuses.find(e=>e.key===t)?.count??0;Ve.innerHTML=[[`discovered`,t(`discovered`)],[`interested`,t(`interested`)],[`applied`,e.stats?.applications_total??0],[`total`,e.stats?.jobs_total??0]].map(([e,t])=>`
        <dl>
          <dt>${G(e)}</dt>
          <dd>${t}</dd>
        </dl>
      `).join(``)}function un(e,t=``){if(E=e,ne.textContent=e?`replace`:`upload`,t){m.textContent=t;return}if(!e){m.textContent=`no resume uploaded`;return}let n=H(e.updated_at),r=yn(e.content_bytes);m.textContent=[W(e.filename),r,n].filter(Boolean).join(` | `)}function dn(e,t,n,{binary:r=!1}={}){let i=r?e.filename:e.id;return`
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
    </li>`}function fn(e,t=``){O=Array.isArray(e)?e:[],le.textContent=O.length>0?`add`:`upload`,se.textContent=t||(O.length===0?`no examples uploaded`:`${O.length} ${O.length===1?`example`:`examples`} stored`),ue.innerHTML=O.map(e=>dn(e,`cover-letter-examples`,yn(e.content_bytes))).join(``)}function pn(e,t=``){k=Array.isArray(e)?e:[],pe.textContent=k.length>0?`add`:`upload`,de.textContent=t||(k.length===0?`no notes uploaded`:`${k.length} ${k.length===1?`note`:`notes`} stored`),me.innerHTML=k.map(e=>dn(e,`experience-notes`,yn(e.content_bytes))).join(``)}function mn(e,t=``){A=e??null;let n=A?.status??`missing`,r=n!==`ready`;if(k.length,he.hidden=!r,he.textContent=t||A?.warning||``,t)ge.textContent=t;else if(n===`ready`){let e=Number(A?.document_count??0),t=Number(A?.skipped_source_count??0),n=H(A?.generated_at);ge.innerHTML=[`${e} indexed ${e===1?`page`:`pages`}`,t?`${t} unreadable upload skipped`:``,n].filter(Boolean).map(e=>`<button type="button" class="material-index-link" data-open-material-index title="Reveal the application material index in Finder">${G(e)}</button>`).join(`<span aria-hidden="true"> | </span>`)}else ge.textContent=n===`stale`?`index out of date`:`not indexed`}function hn(e,t=``){D=Array.isArray(e)?e:[],ae.textContent=D.length>0?`add`:`upload`,re.textContent=t||(D.length===0?`no resources uploaded`:`${D.length} ${D.length===1?`resource`:`resources`} stored`),oe.innerHTML=D.map(e=>dn(e,`resume-resources`,yn(e.bytes),{binary:!0})).join(``)}function gn(e,t={}){Ht+=1,document.querySelectorAll(`[data-preview-blob-url]`).forEach(e=>{URL.revokeObjectURL(e.dataset.previewBlobUrl)}),un(e?.master_resume??null),hn(e?.resume_resources??[]),fn(e?.cover_letter_examples??[]),pn(e?.experience_notes??[]),mn(e?.material_index??null),_n(e?.ui),(!Vt||t.applyDefaultCollapsed)&&(vn(!!e?.ui?.default_collapsed),Vt=!0)}function _n(e=null){let t=E?`resume ready`:`no resume`,n=D.length===0?`no resources`:`${D.length} ${D.length===1?`resource`:`resources`}`,r=O.length,i=r===0?`no cover letters`:`${r} cover ${r===1?`letter`:`letters`}`,a=k.length,o=a===0?`no notes`:`${a} experience ${a===1?`note`:`notes`}`;p.hidden=!(typeof e?.has_missing_required_materials==`boolean`?e.has_missing_required_materials:!E||r===0||a===0),te.textContent=`${t} | ${n} | ${i} | ${o}`}function vn(e){d.classList.toggle(`collapsed`,e),ee.setAttribute(`aria-expanded`,String(!e)),ee.querySelector(`.materials-chevron`).textContent=e?`>`:`v`,f.hidden=e}function yn(e){return Number.isFinite(e)?e<1024?`${e} b`:`${Math.round(e/1024)} kb`:``}async function bn(e){let t=await fetch(e,{cache:`no-store`});if(!t.ok)throw Error(`Preview unavailable`);let n=await t.arrayBuffer();if(new TextDecoder(`ascii`).decode(n.slice(0,5))!==`%PDF-`)throw Error(`The selected file is not a readable PDF.`);return URL.createObjectURL(new Blob([n],{type:`application/pdf`}))}async function xn(e){let t=e.closest(`.material-source-item`)?.querySelector(`[data-material-preview-body]`);if(!t)return;if(t.dataset.loaded===`true`){t.hidden=!t.hidden,e.textContent=t.hidden?`preview`:`hide`;return}e.disabled=!0,e.textContent=`loading...`;let n=e.dataset.materialView,r=e.dataset.materialId,i=Ht,a=`/api/${encodeURIComponent(n)}/${encodeURIComponent(r)}`;try{if(e.dataset.materialBinary===`true`){let e=await bn(a);if(!t.isConnected||Ht!==i){URL.revokeObjectURL(e);return}t.dataset.previewBlobUrl=e,t.innerHTML=`<iframe title="${G(r)} preview"></iframe>`,t.querySelector(`iframe`).src=e}else{let e=await fetch(a);if(!e.ok)throw Error(`Preview unavailable`);let n=await e.json(),r=document.createElement(`pre`);r.textContent=n.content||`This source is empty.`,t.replaceChildren(r)}t.dataset.loaded=`true`,t.hidden=!1,e.textContent=`hide`}catch(n){t.textContent=n instanceof Error?n.message:`Preview unavailable`,t.hidden=!1,e.textContent=`preview`}finally{e.disabled=!1}}async function Sn(e){let t=e.dataset.materialRemove,n=e.dataset.materialId;if(e.dataset.confirmRemove!==`true`){e.dataset.confirmRemove=`true`,e.textContent=`confirm remove`,e.classList.add(`danger`),window.setTimeout(()=>{!e.isConnected||e.disabled||(delete e.dataset.confirmRemove,e.textContent=`remove`,e.classList.remove(`danger`))},6e3);return}e.disabled=!0,e.textContent=`removing...`;try{let e=await fetch(`/api/${encodeURIComponent(t)}/${encodeURIComponent(n)}`,{method:`DELETE`}),r=await e.json();if(!e.ok)throw Error(r.error||`Remove failed`);gn(r)}catch(t){e.disabled=!1,delete e.dataset.confirmRemove,e.classList.remove(`danger`),e.textContent=`remove`,window.alert(t instanceof Error?t.message:`Remove failed`)}}function Cn(e){i.innerHTML=e.map(e=>{let t=e.jobs.map(t=>wn(t,e.key)).join(``);return`
        <section class="status-pane ${e.count===0?`empty`:``} ${At?`hidden-empty`:``}" id="status-${U(e.key)}" data-bucket="${U(e.key)}">
          <button class="pane-toggle" type="button" aria-expanded="false">
            <span class="chevron">></span>
            <span class="pane-title">${G(e.label)}</span>
            <span class="count">${e.count}</span>
          </button>
          <div class="pane-body" hidden>
            ${t?`<div class="jobs">${t}</div>`:`<p class="empty-copy">no jobs in this status.</p>`}
          </div>
        </section>
      `}).join(``)}function wn(e,t){return`
    <details class="job" data-role-id="${U(e.id)}">
      <summary class="job-summary">
        <span class="job-chevron">></span>
        <span class="job-identity">
          <span class="job-company">[${G(e.company_name)}]</span>
          ${sn(e.title,e.role_url,`job-title`)}
          ${t===`interested`&&e.prep_started?Dn():``}
          ${t===`closed`&&e.updated_in_latest_scan?Tn():``}
          ${[`discovered`,`interested`].includes(t)&&e.missing_from_latest_scan?En():``}
        </span>
      </summary>
      <div class="job-detail">
        ${t===`discovered`?On(e):``}
        ${t===`interested`?kn(e):``}
        ${t===`disinterested`?An(e):``}
        ${t===`applied`?jn(e):``}
        ${t===`OA`?Mn(e):``}
        ${t===`interview`?Nn(e):``}
        ${t===`closed`?Pn(e):``}
        <dl>
          ${e.location?`<div>
                  <dt>location</dt>
                  <dd>${G(e.location)}</dd>
                </div>`:``}
          <div>
            <dt>updated</dt>
            <dd>${en(e.updated_at)}</dd>
          </div>
        </dl>
      </div>
    </details>
  `}function Tn(){return`<span class="latest-scan-dot" title="updated in latest scan" aria-label="updated in latest scan"></span>`}function En(){return`<span class="missing-latest-scan-dot" title="not seen in latest scan" aria-label="not seen in latest scan"></span>`}function Dn(){return`<span class="prep-started-dot" title="application materials started" aria-label="application materials started"></span>`}function On(e){return`
    <div class="job-actions job-actions-nowrap" aria-label="discovered role actions">
      <button class="job-action success" type="button" data-review-role-id="${e.id}">view</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="interested">interested</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="disinterested">disinterested</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="closed">closed</button>
    </div>
  `}function kn(e){return`
    <div class="job-actions" aria-label="interested role actions">
      <button class="job-action success" type="button" data-prep-role-id="${e.id}">prep</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="applied">applied</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="disinterested">disinterested</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="closed">closed</button>
    </div>
  `}function An(e){return`
    <div class="job-actions" aria-label="disinterested role actions">
      <button class="job-action success" type="button" data-role-id="${e.id}" data-status="interested">interested</button>
    </div>
  `}function jn(e){return`
    <div class="job-actions job-actions-nowrap" aria-label="applied role actions">
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="OA">oa</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="interview">interview</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="rejected">rejected</button>
    </div>
  `}function Mn(e){return`
    <div class="job-actions job-actions-nowrap" aria-label="oa role actions">
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="interview">interview</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="disinterested">disinterested</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="rejected">rejected</button>
    </div>
  `}function Nn(e){return`
    <div class="job-actions" aria-label="interview role actions">
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="rejected">rejected</button>
      <button class="job-action success" type="button" data-role-id="${e.id}" data-status="offer">offer</button>
    </div>
  `}function Pn(e){return`
    <div class="job-actions" aria-label="closed role actions">
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="interested">interested</button>
    </div>
  `}function Fn(e){T=e,l.value=e.query,Zt(),cn(e.stats),ln(e),Cn(e.statuses),Sa(),ai(e.statuses),si(e.statuses)}function In(e){Gt=e??null;let t=!!e?.scanning,n=t&&!!e?.cancel_requested,r=Number(e?.completed_companies??0),i=Number(e?.total_companies??0),a=Number(e?.failed_companies??0),o=typeof e?.error==`string`?e.error.trim():``,s=Array.isArray(e?.failures)?e.failures:[];y.disabled=n,y.textContent=t?n?`cancelling...`:`cancel scan`:`scan roles`,y.classList.toggle(`danger`,t&&!n),b.hidden=!t&&!o&&s.length===0,b.classList.toggle(`scanning`,t),b.classList.toggle(`scan-error`,!t&&!!o||s.length>0),x.textContent=n?`cancelling scan...`:t?`scanning roles${i>0?` ${r}/${i}`:``}${a>0?`, ${a} failed`:``}`:s.length>0?`${s.length} recent scan ${s.length===1?`failure`:`failures`}`:o?`last scan error: ${o}`:`scan idle`,Pe&&Re&&(Pe.hidden=s.length===0,Re.innerHTML=s.slice(0,5).map(e=>{let t=e?.company_name||`unknown company`,n=e?.error||`scan failed`;return`
          <p>
            <span>${G(t)}</span>
            <span>${U(n)}</span>
          </p>
        `}).join(``),s.length===0&&Rn());let c=e?.last_scan_at;Ne.textContent=c?`last scan: ${H(c)}`:`last scan: never`,Wt&&!t&&Y(V()).catch(()=>{}),Wt=t}function Ln(){Pe.hidden||(Fe.hidden=!1,Le.focus())}function Rn(){Fe.hidden=!0}function q(e,t=``){Kt=e;let n=Array.isArray(e?.settings)?e.settings:[],r=n.filter(e=>e.key?.startsWith(`applicant_`)),i=n.filter(e=>e.key?.startsWith(`autoprep_`)),a=n.filter(e=>!e.key?.startsWith(`applicant_`)&&!e.key?.startsWith(`autoprep_`)),o=e?.central??{};S.textContent=t,S.classList.toggle(`is-empty`,!t);let s=Number(e?.recommendation_history_count??0);tt.textContent=s>0?`${s} saved ${s===1?`feedback decision`:`feedback decisions`}`:`no saved resume feedback decisions`,nt.disabled=s===0,zn(o),Ke.innerHTML=r.map(e=>Bn(e)).join(``),qe.innerHTML=i.map(e=>Bn(e)).join(``),Je.innerHTML=a.map(e=>Bn(e)).join(``),J(!1)}function zn(e){let t=e?.api_url??``;Ze.value=t,Qe.value=``;let n=e?.passkey_configured?`passkey saved`:`no passkey saved`;Ye.textContent=t?`${W(t)} | ${n}`:`no api url | ${n}`,Xe.textContent=`${Number(e?.companies_linked??0)} linked | ${Number(e?.companies_unlinked??0)} unlinked | ${Number(e?.companies_needs_review??0)} review | ${Number(e?.companies_failed??0)} failed`,et.disabled=!t}function Bn(e){if(e.control===`textarea`&&e.editable!==!1)return Hn(e);if(e.control===`text`&&e.editable!==!1)return Vn(e);if(e.control===`select`&&e.editable!==!1)return Un(e);if(e.control!==`toggle`||e.editable===!1)return Wn(e);let t=e.value?`checked`:``,n=e.default?`on by default`:`off by default`;return`
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
  `}function Vn(e){let t=e.default?`default: ${W(e.default)}`:`optional`,n=e.input_type??`text`,r=e.autocomplete??`name`;return`
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
  `}function Hn(e){return`
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
  `}function Un(e){let t=Array.isArray(e.options)?e.options:[],n=`default: ${W(e.default)}`;return`
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
  `}function Wn(e){let t=e.default?`on by default`:`off by default`,n=e.value?`automatic`:`off`;return`
    <div class="setting-option setting-option-readonly">
      <span class="setting-copy">
        <span class="setting-label">${G(e.label)}</span>
        <span class="setting-description">${G(e.description)}</span>
        <span class="setting-default">${G(t)}</span>
      </span>
      <span class="setting-badge">${G(n)}</span>
    </div>
  `}function J(e){Ge.querySelectorAll(`input, select, textarea`).forEach(t=>{t.disabled=e}),$e.disabled=e,et.disabled=e||!Ze.value.trim(),gt.disabled=e}async function Gn(){Ue.hidden=!1,document.body.classList.add(`settings-open`),We.focus(),Kt?q(Kt):(S.textContent=`loading settings...`,S.classList.remove(`is-empty`),Je.innerHTML=``);try{await qn()}catch{S.textContent=`could not load settings.`}}function Kn(){Ue.hidden=!0,document.body.classList.remove(`settings-open`),He.focus()}async function qn(){let e=await fetch(`/api/config`);if(!e.ok)throw Error(`Config request failed`);q(await e.json())}function Jn(e){let t=e?.value;return t==null?`n/a`:e?.kind===`ratio`?Number(t).toLocaleString(void 0,{maximumFractionDigits:2,minimumFractionDigits:0}):typeof t==`number`?t.toLocaleString():W(t)}function Yn(e,t=`metric-card`){return`
    <article class="${t}">
      <span>${G(e?.label)}</span>
      <strong>${U(Jn(e))}</strong>
    </article>
  `}function Xn(e,t=``){qt=e,ot.textContent=t||(e?.updated_at?`updated ${H(e.updated_at)}`:``),ot.classList.toggle(`is-empty`,!ot.textContent);let n=Array.isArray(e?.overview)?e.overview:[],r=Array.isArray(e?.sections)?e.sections:[],i=Array.isArray(e?.recent_scans)?e.recent_scans:[];st.innerHTML=n.map(e=>Yn(e)).join(``),ct.innerHTML=r.map(Zn).join(``),lt.innerHTML=i.length?i.map(Qn).join(``):`<p class="empty-copy">no scan runs recorded.</p>`}function Zn(e){let t=Array.isArray(e?.metrics)?e.metrics:[];return`
    <section class="metrics-section">
      <div class="metrics-section-heading">
        <h3>${G(e?.title)}</h3>
      </div>
      <div class="metrics-section-grid">
        ${t.map(e=>Yn(e,`metric-card metric-card-compact`)).join(``)}
      </div>
    </section>
  `}function Qn(e){let t=e?.scan_status??`unknown`,n=e?.started_at?H(e.started_at):`not started`,r=e?.finished_at?H(e.finished_at):`not finished`,i=e?.error?`<span>${G(e.error)}</span>`:``;return`
    <article class="metrics-scan-row">
      <div>
        <strong>${G(e?.company_name??`unknown company`)}</strong>
        <span>${G(n)} -> ${G(r)}</span>
        ${i}
      </div>
      <span class="metrics-status-pill">${G(t)}</span>
    </article>
  `}async function $n(){it.hidden=!1,document.body.classList.add(`metrics-open`),at.focus(),qt?Xn(qt):(ot.textContent=`loading metrics...`,ot.classList.remove(`is-empty`),st.innerHTML=``,ct.innerHTML=``,lt.innerHTML=``);try{await tr()}catch{ot.textContent=`could not load metrics.`}}function er(){it.hidden=!0,document.body.classList.remove(`metrics-open`),rt.focus()}async function tr(){let e=await fetch(`/api/metrics`);if(!e.ok)throw Error(`Metrics request failed`);Xn(await e.json())}function nr(e,t=``){Jt=e;let n=Number(e?.role_count??0),r=Array.isArray(e?.links)?e.links:[],i=Array.isArray(e?.paths)?e.paths:[];pt.textContent=t||(e?.updated_at?`${n.toLocaleString()} roles | updated ${H(e.updated_at)}`:``),pt.classList.toggle(`is-empty`,!pt.textContent),mt.innerHTML=r.length?rr(e):`<p class="empty-copy">no role transitions recorded yet.</p>`,ht.innerHTML=i.length?i.map(sr).join(``):`<p class="empty-copy">no role paths recorded yet.</p>`}function rr(e){let t=Array.isArray(e?.nodes)?e.nodes:[],n=Array.isArray(e?.links)?e.links:[],r=or(t,n),i=r.nodes,a=r.links,o=(r.flowLinks??n).map(e=>{let t=i.get(e.source),n=i.get(e.target),r=a.get(e);if(!t||!n||!r)return``;let o=r.width,s=n.x<t.x,c=ir(e.target),l=r.priority?`0.42`:s?`0.28`:`0.34`,u=r.path??ar({isBacktrack:s,sourceX:t.x+t.width,sourceY:r.sourceY,targetX:n.x,targetY:r.targetY,width:o});return`
        <path class="${[`sankey-link`,s?`sankey-link-backtrack`:``,r.priority?`sankey-link-priority`:``].filter(Boolean).join(` `)}" d="${u}" fill="${r.path?`none`:c}" fill-opacity="${l}" stroke="${c}" style="stroke-width: ${r.path?o:1}px">
          <title>${G(t.label)} to ${G(n.label)}: ${Number(e.value??0).toLocaleString()}</title>
        </path>
      `}).join(``),s=Array.from(i.values()).map(e=>{let t=Number(e.history_count??e.current_count??0),n=Number(e.value??t),i=n>0?n.toLocaleString():`0`,a=e.x>r.width-180,o=a?e.x-8:e.x+e.width+8,s=Math.max(24,e.y-e.height/2-16),c=a?`end`:`start`,l=ir(e.id);return`
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
  `}function ir(e){return Ot.get(String(e).toLowerCase())??`#4f6472`}function ar({isBacktrack:e,sourceX:t,sourceY:n,targetX:r,targetY:i,width:a}){let o=a/2,s=n-o,c=n+o,l=i-o,u=i+o;if(e){let e=Math.max(80,Math.abs(t-r)*.42);return[`M ${t} ${s}`,`C ${t-e} ${s}, ${r+e} ${l}, ${r} ${l}`,`L ${r} ${u}`,`C ${r+e} ${u}, ${t-e} ${c}, ${t} ${c}`,`Z`].join(` `)}let d=Math.max(46,(r-t)*.48);return[`M ${t} ${s}`,`C ${t+d} ${s}, ${r-d} ${l}, ${r} ${l}`,`L ${r} ${u}`,`C ${r-d} ${u}, ${t+d} ${c}, ${t} ${c}`,`Z`].join(` `)}function or(e,r){let i=new Map([[`discovered`,0],[`interested`,1],[`disinterested`,2],[`applied`,2],[`oa`,3],[`interview`,3],[`rejected`,4],[`closed`,4],[`archived`,4]]),a=new Map,o=new Map;r.forEach(e=>{a.set(e.target,(a.get(e.target)??0)+Number(e.value??0)),o.set(e.source,(o.get(e.source)??0)+Number(e.value??0))});let s=e.filter(e=>Number(e?.history_count??e?.current_count??0)>0||a.has(e.id)||o.has(e.id)),c=new Set(s.map(e=>e.id)),l=r.filter(e=>c.has(e.source)&&c.has(e.target)&&Number(e.value??0)>0),u=e=>i.get(String(e).toLowerCase())??0,d=l.filter(e=>u(e.target)>=u(e.source)),ee=l.filter(e=>u(e.target)<u(e.source)),f={nodes:s.map(e=>({...e,fixedValue:Math.max(0,Number(e?.history_count??e?.current_count??0))})),links:d.map(e=>({...e}))},te=t().nodeId(e=>e.id).nodeWidth(26).nodePadding(44).nodeAlign((e,t)=>Math.min(t-1,u(e.id))).extent([[92,88],[1014,634]]).iterations(32)(f),p=new Map;te.nodes.forEach(e=>{p.set(e.id,{...e,x:e.x0,y:e.y0+(e.y1-e.y0)/2,width:e.x1-e.x0,height:Math.max(1.5,e.y1-e.y0),value:Number(e.fixedValue??e.value??0)})});let m=new Map,h=[],ne=n();te.links.forEach(e=>{let t={source:e.source.id,target:e.target.id,value:e.value};h.push(t),m.set(t,{path:ne(e),width:Math.max(1.5,e.width),sourceY:e.y0,targetY:e.y1,priority:Number(e.value??0)>=20})});let re=Math.max(.6,...te.links.map(e=>Number(e.width??0)/Math.max(1,Number(e.value??0))));return ee.forEach(e=>{let t=p.get(e.source),n=p.get(e.target);if(!t||!n)return;let r=Math.max(1.5,Number(e.value??0)*re),i={...e};h.push(i),m.set(i,{width:r,sourceY:t.y+t.height/2-r/2,targetY:n.y+n.height/2-r/2,priority:!1})}),h.sort((e,t)=>Number(e.value??0)-Number(t.value??0)),{flowLinks:h,height:720,links:m,nodes:p,width:1120}}function sr(e){let t=Array.isArray(e?.path)?e.path:[];return`
    <article class="sankey-path-row">
      <div>
        <strong>${G(e?.company_name??`unknown company`)} / ${G(e?.title??`untitled role`)}</strong>
        <span>${t.map(e=>G(e)).join(` -> `)}</span>
      </div>
      <span class="metrics-status-pill">${Number(e?.loops_collapsed??0).toLocaleString()} loops</span>
    </article>
  `}async function cr(){Ue.hidden=!0,document.body.classList.remove(`settings-open`),dt.hidden=!1,document.body.classList.add(`sankey-open`),ft.focus(),Jt?nr(Jt):(pt.textContent=`loading role flow...`,pt.classList.remove(`is-empty`),mt.innerHTML=``,ht.innerHTML=``);try{await ur()}catch{pt.textContent=`could not load role flow.`}}function lr(){dt.hidden=!0,document.body.classList.remove(`sankey-open`),He.focus()}async function ur(){let e=await fetch(`/api/role-sankey`);if(!e.ok)throw Error(`Role sankey request failed`);nr(await e.json())}async function dr(e){let t=e.name;if(!t)return;let n=e.type===`checkbox`?!e.checked:Kt?.settings?.find(e=>e.key===t)?.value,r=e.type===`checkbox`?e.checked:e.value;J(!0),S.textContent=`saving settings...`,S.classList.remove(`is-empty`);try{let e=await fetch(`/api/config`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({[t]:r})});if(!e.ok)throw Error(`Config update failed`);q(await e.json(),`settings saved.`)}catch{e.type===`checkbox`?e.checked=n:n!==void 0&&(e.value=n),S.textContent=`could not save settings.`,J(!1)}}async function fr(){nt.disabled=!0,S.textContent=`clearing recommendation history...`,S.classList.remove(`is-empty`);try{let e=await fetch(`/api/recommendation-history/clear`,{method:`POST`});if(!e.ok)throw Error(`Recommendation history clear failed`);let t=await e.json();q(t.config,`cleared ${t.deleted_count} saved decisions.`)}catch{S.textContent=`could not clear recommendation history.`,nt.disabled=!1}}async function pr(){let e=Ze.value.trim();if(!e){S.textContent=`central api url is required.`,S.classList.remove(`is-empty`);return}let t={central_api_url:e},n=Qe.value.trim();n&&(t.central_passkey=n),J(!0),S.textContent=`saving central settings...`,S.classList.remove(`is-empty`);try{let e=await fetch(`/api/config`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(t)});if(!e.ok)throw Error(`Central settings update failed`);q(await e.json(),`central settings saved.`)}catch{S.textContent=`could not save central settings.`,J(!1)}}async function mr(){et.disabled=!0,S.textContent=`syncing remote company ids...`,S.classList.remove(`is-empty`);try{let e=await fetch(`/api/central/resolve-companies`,{method:`POST`});if(!e.ok)throw Error(`Central company sync failed`);let t=await e.json(),n=t.result??{},r=t.pulled_companies,i=r?` remote: ${Number(r.created??0)} created, ${Number(r.linked??0)} linked, ${Number(r.existing??0)} existing.`:``;q(t.config,`company sync: ${Number(n.linked??0)} matched, ${Number(n.created??0)} created, ${Number(n.needs_review??0)} review, ${Number(n.failed??0)} failed.${i}`),t.companies&&(B=t.companies,yr(t.companies.companies))}catch{S.textContent=`could not sync companies.`,et.disabled=!Ze.value.trim()}}async function hr(){let e=await fetch(`/api/central/resolve-companies`,{method:`POST`});if(!e.ok)throw Error(`Central company sync failed`);let t=await e.json();t.companies&&(B=t.companies,yr(t.companies.companies))}async function gr(){let e=hr().catch(()=>{});await Promise.all([Y().catch(()=>{i.innerHTML=`<p class="empty-copy">could not load jobs.</p>`}),Dr().catch(()=>{wt.textContent=`could not load companies.`})]),await e}async function _r(){if(window.confirm(`Update callumployed and restart the tracker?`)){J(!0),gt.disabled=!0,S.textContent=`updating callumployed; tracker will restart shortly...`,S.classList.remove(`is-empty`);try{if(!(await fetch(`/api/app/update`,{method:`POST`})).ok)throw Error(`App update failed`);S.textContent=`update started. reconnect in a moment.`}catch{S.textContent=`could not start update.`,J(!1)}}}function vr(e,t=``){B=e;let n=Array.isArray(e?.companies)?e.companies:[];if(yr(n),C.textContent=t||`${n.length} ${n.length===1?`company`:`companies`} stored`,C.classList.toggle(`is-empty`,n.length===0&&!t),n.length===0){w.innerHTML=`<p class="empty-copy">no companies yet.</p>`;return}w.innerHTML=n.map(e=>br(e)).join(``)}function yr(e){Yt=Array.isArray(e)?e:[],Ct.innerHTML=Yt.map(e=>`<option value="${U(e.name)}"></option>`).join(``)}function br(e){let t=Array.isArray(e.career_pages)?e.career_pages:[],n=H(e.updated_at),r=xr(e.prestige_tier),i=Number(e.scan_count??0),a=Number(e.discovered_role_count??0),o=i>0&&a===0?`<span class="company-discovery-status">Discovered 0 potential roles</span>`:``;return`
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
              ${Sr(e.prestige_tier)}
            </select>
          </label>
          <div>
            <span>browser wait</span>
            <strong>${Number(e.browser_extra_wait_ms??0)}ms</strong>
          </div>
        </div>
        <div class="company-links">
          ${t.length>0?t.map(e=>Cr(e)).join(``):`<p class="company-empty-links">no career links yet.</p>`}
        </div>
        <section class="company-link-panel" aria-label="add career link">
          <form class="company-link-form" data-company-link-form="${e.id}">
            <input name="label" type="text" placeholder="label" aria-label="career link label" />
            <input name="url" type="url" placeholder="https://..." aria-label="career link url" required />
            <button class="company-link-add" type="submit" aria-label="add career link" title="add career link">
              ${an()}
            </button>
          </form>
        </section>
        <div class="company-danger-row">
          <button class="company-delete-button" type="button" data-delete-company="${e.id}">
            ${on()}
            <span>deactivate company</span>
          </button>
        </div>
      </div>
    </details>
  `}function xr(e){let t=String(e??``);return[`0`,`1`,`2`,`3`,`4`].includes(t)?`company-tier-${t}`:`company-tier-unset`}function Sr(e){let t=String(e??``);return[``,`0`,`1`,`2`,`3`,`4`].map(e=>{let n=e?`tier ${e}`:`not set`,r=e===t?` selected`:``;return`<option value="${U(e)}"${r}>${G(n)}</option>`}).join(``)}function Cr(e){let t=e.label?G(e.label):`career page`,n=U(e.url);return`
    <div class="company-link-row" data-career-page-id="${e.id}">
      <a class="company-link-url" href="${n}" target="_blank" rel="noreferrer">
        <span class="company-link-label">${t}</span>
        <span class="company-link-text">${U(e.url)}</span>
      </a>
      <button class="company-link-delete" type="button" data-delete-career-page="${e.id}" aria-label="delete ${t} link" title="delete link">
        ${on()}
      </button>
    </div>
  `}async function wr(){_t.hidden=!1,document.body.classList.add(`companies-open`),vt.focus(),B?vr(B):(C.textContent=`loading companies...`,C.classList.remove(`is-empty`),w.innerHTML=``);try{await Er()}catch{C.textContent=`could not load companies.`}}function Tr(){_t.hidden=!0,document.body.classList.remove(`companies-open`),Me.focus()}async function Er(e=``){let t=await fetch(`/api/companies`);if(!t.ok)throw Error(`Companies request failed`);vr(await t.json(),e)}async function Dr(){let e=await fetch(`/api/companies`);if(!e.ok)throw Error(`Companies request failed`);yr((await e.json()).companies)}async function Or(e){let t=new FormData(e),n={name:String(t.get(`name`)??``),career_url:String(t.get(`career_url`)??``),notes:String(t.get(`notes`)??``)};C.textContent=`adding company...`;let r=await fetch(`/api/companies`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(n)});if(!r.ok)throw Error(`Company create failed`);e.reset(),vr(await r.json(),`company added.`),Y(V()).catch(()=>{})}async function kr(e){let t=e.dataset.companyLinkForm;if(!t)return;let n=new FormData(e),r={label:String(n.get(`label`)??``),url:String(n.get(`url`)??``)};C.textContent=`adding link...`;let i=await fetch(`/api/companies/${encodeURIComponent(t)}/career-pages`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(r)});if(!i.ok)throw Error(`Career page create failed`);e.reset(),vr(await i.json(),`link added.`)}async function Ar(e){C.textContent=`deleting link...`;let t=await fetch(`/api/company-career-pages/${encodeURIComponent(e)}`,{method:`DELETE`});if(!t.ok)throw Error(`Career page delete failed`);vr(await t.json(),`link deleted.`)}async function jr(e){C.textContent=`deactivating company...`;let t=await fetch(`/api/companies/${encodeURIComponent(e)}`,{method:`DELETE`});if(!t.ok)throw Error(`Company deactivate failed`);vr(await t.json(),`company deactivated.`),Y(V()).catch(()=>{})}function Mr(){let e=St.value.trim().toLocaleLowerCase();return Yt.find(t=>t.name.toLocaleLowerCase()===e)}async function Nr(e){let t=Mr();if(!t?.id){wt.textContent=`pick a saved company.`;return}let n=new FormData(e),r={company_id:t.id,role_url:String(n.get(`role_url`)??``)};wt.textContent=`adding role...`;let i=await fetch(`/api/roles`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(r)});if(!i.ok)throw Error(`Role create failed`);let a=await i.json();a.tracker?Fn(a.tracker):await Y(V()),xt.value=``;let o=a.role?.title?W(a.role.title):`role`;wt.textContent=a.scan_error?`${o} added; scan could not finish.`:`${o} added.`}function Pr(e){return(Array.isArray(B?.companies)?B.companies:[]).find(t=>String(t.id)===String(e))}function Fr(e){C.textContent=e,C.classList.remove(`is-empty`)}function Ir(e){window.clearTimeout(Xt.get(e)),Xt.set(e,window.setTimeout(()=>{Lr(e).catch(()=>{Fr(`could not save company.`)})},700))}async function Lr(e){let t=w.querySelector(`[data-company-id="${CSS.escape(String(e))}"]`);if(!t)return;let n=t.querySelector(`[data-company-notes="${CSS.escape(String(e))}"]`),r=t.querySelector(`[data-company-tier="${CSS.escape(String(e))}"]`),i=Pr(e),a={notes:n?.value??i?.notes??``,prestige_tier:r?.value??i?.prestige_tier??``};i&&(i.notes=a.notes,i.prestige_tier=a.prestige_tier),Rr(t,a.prestige_tier),Fr(`saving company...`);let o=await fetch(`/api/companies/${encodeURIComponent(e)}`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(a)});if(!o.ok)throw Error(`Company update failed`);B=await o.json(),Fr(`company saved.`),zr(e)}function Rr(e,t){e.classList.remove(`company-tier-unset`,`company-tier-0`,`company-tier-1`,`company-tier-2`,`company-tier-3`,`company-tier-4`),e.classList.add(xr(t))}function zr(e){let t=w.querySelector(`[data-company-id="${CSS.escape(String(e))}"]`),n=Pr(e);if(!t||!n)return;let r=Array.isArray(n.career_pages)?n.career_pages:[],i=H(n.updated_at),a=t.querySelector(`.company-summary-meta`);a&&(a.textContent=`${r.length} ${r.length===1?`link`:`links`}${i?` | updated ${i}`:``}`)}async function Br(){let e=await fetch(`/api/scan/status`);if(e.status===404){y.disabled=!0,b.hidden=!0,b.classList.add(`scan-error`),x.textContent=`restart server to enable scanning`;return}if(!e.ok)throw Error(`Scan status request failed`);In(await e.json())}function Vr(){Ut===null&&(Ut=window.setInterval(()=>{Br().catch(()=>{})},3e3))}async function Hr(){y.disabled=!0,y.textContent=`starting...`;try{let e=await fetch(`/api/scan/all`,{method:`POST`});if(e.status===404){y.disabled=!0,y.textContent=`scan roles`,b.hidden=!0,b.classList.add(`scan-error`),x.textContent=`restart server to enable scanning`;return}if(!e.ok&&e.status!==409)throw Error(`Scan start failed`);In(await e.json()),Vr()}catch{y.disabled=!1,y.textContent=`scan roles`,b.hidden=!0,b.classList.add(`scan-error`),x.textContent=`could not start scan`}}async function Ur(){y.disabled=!0,y.textContent=`cancelling...`;try{let e=await fetch(`/api/scan/cancel`,{method:`POST`});if(e.status===404){y.disabled=!0,y.textContent=`scan roles`,b.hidden=!0,b.classList.add(`scan-error`),x.textContent=`restart server to enable scanning`;return}if(!e.ok&&e.status!==409)throw Error(`Scan cancel failed`);In(await e.json()),Vr()}catch{y.disabled=!1,y.textContent=`cancel scan`,b.hidden=!1,b.classList.add(`scan-error`),x.textContent=`could not cancel scan`}}async function Y(e=``){i.innerHTML=`<p class="empty-copy">loading jobs...</p>`;let t=new URLSearchParams;e&&t.set(`q`,e);let n=await fetch(`/api/tracker?${t.toString()}`);if(!n.ok)throw Error(`Tracker request failed`);Fn(await n.json())}async function Wr(e={}){let t=await fetch(`/api/application-materials`);if(!t.ok)throw Error(`Application materials request failed`);gn(await t.json(),e)}async function Gr(e){if(e){if(!e.name.toLowerCase().endsWith(`.tex`)){un(E,`resume must be a .tex file.`);return}ne.disabled=!0,un(E,`uploading...`);try{let t=await e.text();if(!(await fetch(`/api/master-resume`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({filename:e.name,content:t})})).ok)throw Error(`Master resume upload failed`);await Wr()}catch{un(E,`could not save resume.`),_n()}finally{h.value=``,ne.disabled=!1}}}async function Kr(e){let t=Array.from(e??[]);if(t.length!==0){ae.disabled=!0,hn(D,`uploading ${t.length} ${t.length===1?`resource`:`resources`}...`);try{for(let e of t)if(!(await fetch(`/api/resume-resources`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({filename:e.name,content_base64:await Yr(e)})})).ok)throw Error(`Resume resource upload failed`);await Wr()}catch{hn(D,`could not save every resource.`),_n()}finally{ie.value=``,ae.disabled=!1}}}async function qr(e){let t=Array.from(e??[]);if(t.length!==0){le.disabled=!0,fn(O,`uploading ${t.length} ${t.length===1?`example`:`examples`}...`);try{for(let e of t){let t={filename:e.name};if([`.pdf`,`.docx`].some(t=>e.name.toLowerCase().endsWith(t))?t.content_base64=await Yr(e):t.content=await e.text(),!(await fetch(`/api/cover-letter-examples`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(t)})).ok)throw Error(`Cover letter example upload failed`)}await Wr()}catch{fn(O,`could not save every example.`),_n()}finally{ce.value=``,le.disabled=!1}}}async function Jr(e){let t=Array.from(e??[]);if(t.length!==0){pe.disabled=!0,pn(k,`uploading ${t.length} ${t.length===1?`note`:`notes`}...`);try{for(let e of t){let t=e.name.toLowerCase(),n={filename:e.name};if(t.endsWith(`.pdf`)||t.endsWith(`.docx`)?n.content_base64=await Yr(e):n.content=await e.text(),!(await fetch(`/api/experience-notes`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(n)})).ok)throw Error(`Experience note upload failed`)}N.clear(),await Wr()}catch{pn(k,`could not save every note.`),_n()}finally{fe.value=``,pe.disabled=!1}}}function Yr(e){return new Promise((t,n)=>{let r=new FileReader;r.addEventListener(`load`,()=>{let e=String(r.result??``);t(e.includes(`,`)?e.split(`,`,2)[1]:e)}),r.addEventListener(`error`,()=>n(r.error)),r.readAsDataURL(e)})}c.addEventListener(`submit`,e=>{e.preventDefault(),Y(l.value.trim()),$t()}),a.addEventListener(`click`,()=>{if(V()){Y();return}Qt()}),l.addEventListener(`keydown`,e=>{e.key===`Escape`&&(e.stopPropagation(),$t())}),u.addEventListener(`click`,$t),s.addEventListener(`click`,$t),ne.addEventListener(`click`,()=>{h.click()}),h.addEventListener(`change`,()=>{Gr(h.files?.[0])}),ae.addEventListener(`click`,()=>{ie.click()}),ie.addEventListener(`change`,()=>{Kr(ie.files)}),le.addEventListener(`click`,()=>{ce.click()}),ce.addEventListener(`change`,()=>{qr(ce.files)}),pe.addEventListener(`click`,()=>{fe.click()}),fe.addEventListener(`change`,()=>{Jr(fe.files)}),ee.addEventListener(`click`,()=>{vn(ee.getAttribute(`aria-expanded`)===`true`)});async function Xr(e){e.disabled=!0;let t=e.textContent;e.textContent=`opening...`;try{if(!(await fetch(`/api/application-materials/index/open`,{method:`POST`})).ok)throw Error(`Could not open the application material index.`)}catch(e){he.hidden=!1,he.textContent=e instanceof Error?e.message:`Could not open the application material index.`}finally{e.disabled=!1,e.textContent=t}}f.addEventListener(`click`,e=>{let t=e.target.closest(`[data-open-material-index]`);if(t){Xr(t);return}let n=e.target.closest(`[data-material-view]`);if(n){xn(n);return}let r=e.target.closest(`[data-material-remove]`);r&&Sn(r)}),y.addEventListener(`click`,()=>{if(Gt?.scanning){Ur();return}Hr()}),i.addEventListener(`click`,e=>{let t=e.target.closest(`[data-review-role-id]`);if(t){li(t.dataset.reviewRoleId);return}let n=e.target.closest(`[data-prep-role-id]`);if(n){di(n.dataset.prepRoleId);return}let r=e.target.closest(`.job-action`);if(r){Zr(r);return}let i=e.target.closest(`.pane-toggle`);if(!i)return;let a=i.parentElement.querySelector(`.pane-body`),o=i.getAttribute(`aria-expanded`)===`true`;i.setAttribute(`aria-expanded`,String(!o)),i.querySelector(`.chevron`).textContent=o?`>`:`v`,a.hidden=o,Sa()});async function Zr(e){let{roleId:t,status:n}=e.dataset;if(!t||!n)return;let r=e.closest(`.job-actions`),i=e.closest(`.job`);r.querySelectorAll(`button`).forEach(e=>{e.disabled=!0}),e.textContent=`updating...`;try{let e=await fetch(`/api/roles/${encodeURIComponent(t)}/status`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({status:n})});if(!e.ok)throw Error(`Status update failed`);Qr((await e.json()).role,i)}catch{r.querySelectorAll(`button`).forEach(e=>{e.disabled=!1}),e.textContent=n===`disinterested`?`disinterested`:n.toLowerCase()}}function Qr(e,t){if(!e||!T)return;let n=t?.closest(`.status-pane`)?.dataset.bucket??e.role_status,r=e.role_status,i=ei(e,n,r);ti(n,r),ni(n,r),ln(),ai(T.statuses),si(T.statuses),ri(t,i,n,r),Sa()}function $r(e){if(!e||!T)return null;let t=null;return T.statuses.forEach(n=>{let r=n.jobs.findIndex(t=>String(t.id)===String(e.id));r!==-1&&(t={...n.jobs[r],...e},n.jobs[r]=t)}),ai(T.statuses),si(T.statuses),t}function ei(e,t,n){let r=e;T.statuses.forEach(t=>{let n=t.jobs.findIndex(t=>String(t.id)===String(e.id));n!==-1&&(r={...t.jobs[n],...e},t.jobs.splice(n,1),t.count=t.jobs.length)});let i=T.statuses.find(e=>e.key===n);return i&&(i.jobs.unshift(r),i.count=i.jobs.length),r}function ti(e,t){T.statuses.forEach(e=>{let t=document.querySelector(`#status-${CSS.escape(e.key)}`);t?.classList.toggle(`empty`,e.count===0);let n=t?.querySelector(`.count`);n&&(n.textContent=e.count)}),[e,t].forEach(e=>{ii(document.querySelector(`#status-${CSS.escape(e)}`))})}function ni(e,t){if(!T.stats)return;let n=Dt.has(e),r=Dt.has(t);if(n===r){cn(T.stats);return}T.stats.applications_total=Number(T.stats.applications_total??0)+(r?1:-1),cn(T.stats)}function ri(e,t,n,r){let i=document.querySelector(`#status-${CSS.escape(r)}`),a=i?.querySelector(`.pane-body`);if(!e||!i||!a)return;e.remove(),ii(document.querySelector(`#status-${CSS.escape(n)}`)),a.hidden=!1;let o=i.querySelector(`.pane-toggle`);o?.setAttribute(`aria-expanded`,`true`);let s=o?.querySelector(`.chevron`);s&&(s.textContent=`v`);let c=a.querySelector(`.jobs`);c||=(a.innerHTML=`<div class="jobs"></div>`,a.querySelector(`.jobs`)),c.insertAdjacentHTML(`afterbegin`,wn(t,r)),ii(i)}function ii(e){if(!e)return;let t=e.querySelector(`.pane-body`);if(!t)return;let n=t.querySelector(`.jobs`),r=!!n?.querySelector(`.job`),i=t.querySelector(`.empty-copy`);if(r){i?.remove();return}n?.remove(),i||t.insertAdjacentHTML(`beforeend`,`<p class="empty-copy">no jobs in this status.</p>`)}function ai(e){_e.disabled=oi(e).length===0,_e.setAttribute(`aria-label`,`review discovered`),_e.innerHTML=`<span class="review-discovered-label">review discovered</span>`}function oi(e=T?.statuses??[]){return e.find(e=>e.key===`discovered`)?.jobs??[]}function si(e){ve.disabled=ci(e).length===0,ve.setAttribute(`aria-label`,`prep interested`),ve.innerHTML=`<span class="review-discovered-label">prep interested</span>`}function ci(e=T?.statuses??[]){return e.find(e=>e.key===`interested`)?.jobs??[]}function li(e=null){let t=[...oi()],n=e==null?null:String(e);if(n){let e=t.findIndex(e=>String(e.id)===n);if(e>0){let[n]=t.splice(e,1);t.unshift(n)}}j=t,g.hidden=!1,document.body.classList.add(`review-open`),pi()}function ui(){g.hidden=!0,document.body.classList.remove(`review-open`),j=[]}function di(e=null){let t=[...ci()].sort((e,t)=>Number(!!t.prep_started)-Number(!!e.prep_started)),n=e==null?null:String(e);if(n){let e=t.findIndex(e=>String(e.id)===n);if(e>0){let[n]=t.splice(e,1);t.unshift(n)}}M=t,_.hidden=!1,document.body.classList.add(`prep-open`),ki()}function fi(){_.hidden=!0,document.body.classList.remove(`prep-open`),M=[]}function pi(e=``){let t=j[0],n=j.length,r=t?mi(t):``;if(ye.textContent=n>0?`review queue`:`review complete`,be.textContent=n>0?`${n} discovered ${n===1?`role`:`roles`} in queue`:``,g.querySelectorAll(`.review-action`).forEach(e=>{e.disabled=n===0}),!t){xe.innerHTML=`
      <div class="review-empty">
        <h3>no discovered jobs left.</h3>
        <p>everything in this queue has been handled or moved out of discovered.</p>
      </div>
    `;return}xe.innerHTML=`
    ${e?`<p class="review-message">${U(e)}</p>`:``}
    ${r?`<p class="review-message review-message-warning">${U(r)}</p>`:``}
    <div class="review-title-row">
      <p class="review-company">${G(t.company_name)}</p>
      ${sn(t.title,t.role_url,`review-role-title`)}
    </div>
    <dl class="review-details review-primary-details">
      ${X(`location`,t.location,!1,`review-location-detail`)}
      ${X(`first`,H(t.first_seen_at))}
      ${X(`last`,H(t.last_seen_at))}
    </dl>
    ${hi(t.description)}
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
  `}function mi(e){let t=Number(e.review_later_count??0);return t<=Tt?``:`role review has been postponed ${t} times. it is recommended to set it to disinterested.`}function X(e,t,n=!1,r=``){if(!t)return``;let i=n?`<a href="${U(t)}" target="_blank" rel="noreferrer">${G(t)}</a>`:G(t);return`
    <div class="review-detail ${U(r)}">
      <dt>${G(e)}</dt>
      <dd>${i}</dd>
    </div>
  `}function hi(e){return e?`
    <div class="review-detail review-description">
      <dt>description</dt>
      <dd>${gi(e)}</dd>
    </div>
  `:``}function gi(e){let t=_i(String(e)).replace(/\u00a0/g,` `);if(vi(t))return yi(t);let n=t.split(/\r?\n/).map(e=>e.trim()).filter(Boolean),r=[],i=[],a=()=>{i.length!==0&&(r.push(`<ul>${i.map(e=>`<li>${e}</li>`).join(``)}</ul>`),i=[])};return n.forEach(e=>{let t=e.match(/^#{2,3}\s+(.+)$/);if(t){a(),r.push(`<h3>${G(t[1])}</h3>`);return}if(Di(e)){a(),r.push(`<h3>${G(e.replace(/:$/,``))}</h3>`);return}let n=e.match(/^[-*]\s+(.+)$/);if(n){i.push(G(n[1]));return}a(),r.push(`<p>${G(e)}</p>`)}),a(),r.join(``)}function _i(e){let t=document.createElement(`textarea`);return t.innerHTML=e,t.value}function vi(e){return/<\/?(?:a|br|div|em|h[1-6]|li|ol|p|span|strong|ul)\b/i.test(e)}function yi(e){let t=document.createElement(`template`);t.innerHTML=e;let n=[];return bi(t.content.childNodes,n),n.join(``)}function bi(e,t){e.forEach(e=>{if(e.nodeType===Node.TEXT_NODE){let n=Ti(e.textContent);n&&t.push(`<p>${G(n)}</p>`);return}if(e.nodeType!==Node.ELEMENT_NODE)return;let n=e,r=n.tagName.toLowerCase();if(r===`script`||r===`style`||r===`br`)return;if(/^h[1-6]$/.test(r)){Si(t,n.textContent);return}if(r===`ul`||r===`ol`){let e=Ci(n);e&&t.push(e);return}if(r===`p`){xi(n,t);return}let i=Array.from(n.children).some(e=>[`DIV`,`H1`,`H2`,`H3`,`H4`,`H5`,`H6`,`OL`,`P`,`UL`].includes(e.tagName));if([`article`,`div`,`section`].includes(r)&&i){bi(n.childNodes,t);return}let a=Array.from(n.children).filter(e=>[`UL`,`OL`].includes(e.tagName)),o=Ti(wi(n));if(o&&(Ei(o,n)?Si(t,o):t.push(`<p>${G(o)}</p>`)),a.length>0){a.forEach(e=>{let n=Ci(e);n&&t.push(n)});return}!o&&i&&bi(n.childNodes,t)})}function xi(e,t){if(!e.querySelector(`br`)){let n=Ti(wi(e));if(!n)return;Ei(n,e)?Si(t,n):t.push(`<p>${G(n)}</p>`);return}let n=``,r=()=>{let r=Ti(n);n=``,r&&(Ei(r,e)?Si(t,r):t.push(`<p>${G(r)}</p>`))};e.childNodes.forEach(e=>{if(e.nodeType===Node.ELEMENT_NODE&&e.tagName.toLowerCase()===`br`){r();return}n+=` ${e.textContent??``}`}),r()}function Si(e,t){let n=Ti(t).replace(/:$/,``);n&&e.push(`<h3>${G(n)}</h3>`)}function Ci(e){let t=Array.from(e.children).filter(e=>e.tagName===`LI`).map(e=>{let t=Ti(wi(e)),n=Array.from(e.children).filter(e=>[`UL`,`OL`].includes(e.tagName)).map(e=>Ci(e)).filter(Boolean).join(``);return t||n?`<li>${G(t)}${n}</li>`:``}).filter(Boolean);return t.length>0?`<ul>${t.join(``)}</ul>`:``}function wi(e){let t=e.cloneNode(!0);return t.querySelectorAll(`ul, ol`).forEach(e=>{e.remove()}),t.textContent}function Ti(e){return String(e??``).replace(/\s+/g,` `).trim()}function Ei(e,t){let n=e.replace(/:$/,``).trim();return!n||n.length>90?!1:Di(n)||/:$/.test(e)?!0:/[.!?]$/.test(n)||n.split(/\s+/).length>10?!1:t.querySelector(`strong, b, u`)?!0:Di(n)}function Di(e){return kt.test(String(e).trim())}async function Oi(e){let t=j[0];if(!t)return;if(e===`later`){g.querySelectorAll(`.review-action`).forEach(e=>{e.disabled=!0});try{let e=await Qi(t.id);j.shift(),$r(e),pi(`moved out of this review pass.`)}catch{pi(`could not postpone that role. try again.`)}finally{g.querySelectorAll(`.review-action`).forEach(e=>{e.disabled=j.length===0})}return}if(![`interested`,`disinterested`].includes(e))return;let n=g.querySelectorAll(`.review-action`);n.forEach(e=>{e.disabled=!0});try{let n=await $i(t.id,e);j.shift(),pi(e===`interested`?`marked interested.`:`marked disinterested.`),Qr(n,document.querySelector(`.job[data-role-id="${CSS.escape(String(t.id))}"]`))}catch{n.forEach(e=>{e.disabled=!1}),pi(`could not update that role. try again.`)}}async function ki(e=``){let t=M[0],n=M.length;if(Ce.textContent=n>0?`prep queue`:`prep complete`,we.textContent=n>0?`${n} interested ${n===1?`role`:`roles`} in queue`:``,_.querySelectorAll(`.review-action`).forEach(e=>{e.disabled=n===0}),!t){v.innerHTML=`
      <div class="review-empty">
        <h3>no interested jobs left.</h3>
        <p>everything in this queue has been prepped, moved, or postponed.</p>
      </div>
    `;return}v.innerHTML=`
    ${e?`<p class="review-message">${U(e)}</p>`:``}
    <section class="prep-role-hero" aria-label="role overview">
      <div class="review-title-row">
        <div class="prep-role-eyebrow">
          <p class="review-company">${G(t.company_name)}</p>
          <span>application workspace</span>
        </div>
        ${sn(t.title,t.role_url,`review-role-title`)}
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
      ${Ai(t)}
      ${Pi(t)}
      ${ji(t.id,t.description)}
      ${Mi(t)}
    </div>
  `,K(),Bi(t.id).then(e=>{!e||M[0]?.id!==t.id||(P.set(t.id,e),v.querySelector(`.prep-resume`)?.replaceWith(Q(Ai(t,{resume:e}))),K())}).catch(()=>{}),Zi(t.id).then(e=>{!e||M[0]?.id!==t.id||(F.set(t.id,e),v.querySelector(`.prep-cover-letter`)?.replaceWith(Q(Pi(t,{coverLetter:e}))),K())}).catch(()=>{})}function Ai(e,t={}){let n=P.get(e.id),r=t.resume??n,i=t.tweaks??Mt.get(e.id)??``,a=`/api/roles/${encodeURIComponent(e.id)}/resume.pdf`;return t.loading?`
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
    `}function ji(e,t){return`
    <details class="prep-panel prep-description-panel" id="prep-description-${e}">
      <summary class="prep-analysis-header">
        <span class="prep-accordion-icon" aria-hidden="true"></span>
        <h3>description</h3>
      </summary>
      ${hi(t)}
    </details>
  `}function Mi(e,t={}){let n=t.messages??Nt.get(e.id)??[],r=!!t.loading;return`
    <details class="prep-panel prep-role-chat" id="prep-chat-${e.id}">
      <summary class="prep-analysis-header">
        <span class="prep-accordion-icon" aria-hidden="true"></span>
        <h3>chat about this role</h3>
        <span>${n.length?`${n.length} messages`:`ready`}</span>
      </summary>
      <div class="prep-role-chat-log" aria-live="polite">
        ${n.length?n.map(Ni).join(``):`<p class="prep-role-chat-empty">ask about fit, risks, resume emphasis, or cover letter angle.</p>`}
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
  `}function Ni(e){let t=e?.role===`assistant`?`assistant`:`user`;return`
    <article class="prep-role-chat-message prep-role-chat-message-${t}">
      <span>${t}</span>
      <p>${G(e?.content??``)}</p>
    </article>
  `}function Pi(e,t={}){let n=F.get(e.id),r=t.coverLetter??n,i=t.tweaks??r?.tweaks??``,a=`/api/roles/${encodeURIComponent(e.id)}/cover-letter.pdf`;return t.loading?`
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
    `;let r=t.analysis,i=Array.isArray(r?.feedback_items)?r.feedback_items:[],a=r?.verdict===`ready_to_apply`?`ready to apply`:`tweak`,o=Math.min(jt.get(e.id)??0,Math.max(i.length-1,0)),s=i[o];return`
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
              ${Fi(s)}
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
  `}function Fi(e){return e?.tweak_prompt?`
    <div class="prep-proposed-edit">
      <p class="prep-proposed-label">tweak prompt</p>
      <p>${G(e.tweak_prompt)}</p>
    </div>
  `:`
      <div class="prep-proposed-edit">
        <p class="prep-proposed-label">feedback only</p>
        <p>not enough information to turn this into a safe resume tweak.</p>
      </div>
    `}async function Ii(e,t={}){if(!t.force&&N.has(e))return N.get(e);let n=await fetch(`/api/roles/${encodeURIComponent(e)}/prep-analysis`);if(!n.ok)throw Error(`Prep analysis request failed`);let r=await n.json();return r.analysis.resources=r.resources??[],N.set(e,r.analysis),r.analysis}function Q(e){let t=document.createElement(`template`);return t.innerHTML=e.trim(),t.content.firstElementChild}async function Li(e){let t=M[0];if(!t)return;let n=_.querySelectorAll(`.review-action`);if(n.forEach(e=>{e.disabled=!0}),e===`later`){try{await Qi(t.id),t.review_later_count=Number(t.review_later_count??0)+1,M.length>1?(M.push(M.shift()),ki(`moved to the back of the prep queue.`)):ki(`only one role is in the prep queue.`)}catch{ki(`could not postpone prep. try again.`)}return}if(e===`applied`)try{let e=await $i(t.id,`applied`);M.shift(),ki(`moved to applied.`),Qr(e,document.querySelector(`.job[data-role-id="${CSS.escape(String(t.id))}"]`))}catch{n.forEach(e=>{e.disabled=!1}),ki(`could not move that role. try again.`)}}async function Ri(e,t,n,r){let i=await fetch(`/api/roles/${encodeURIComponent(e)}/prep-feedback`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({feedback_index:t,feedback_item:n,comment:r})});if(!i.ok)throw Error(`Prep feedback update failed`);return i.json()}async function zi(e,t,n,r){let i=await fetch(`/api/roles/${encodeURIComponent(e)}/prep-feedback-ignore`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({feedback_index:t,feedback_item:n,comment:r})});if(!i.ok)throw Error(`Prep feedback ignore failed`);return i.json()}async function Bi(e,{force:t=!1}={}){if(!t&&P.has(e))return P.get(e);let n=await fetch(`/api/roles/${encodeURIComponent(e)}/resume`);if(!n.ok)throw Error(`Resume request failed`);let r=await n.json();return r.resume&&P.set(e,r.resume),r.resume}async function Vi(e,t){let n=await fetch(`/api/roles/${encodeURIComponent(e)}/resume/save`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({latex:t})});if(!n.ok)throw Error(`Resume save failed`);return n.json()}async function Hi(e,t,n){let r=await fetch(`/api/roles/${encodeURIComponent(e)}/resume`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({tweaks:t,previous_latex:n})});if(!r.ok)throw Error(`Resume generation failed`);return r.json()}async function Ui(e,t){let n=await fetch(`/api/roles/${encodeURIComponent(e)}/chat`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({messages:t})});if(!n.ok)throw Error(`Role chat failed`);return n.json()}function Wi(e,t,n=Et){let r=Pt.get(e)??{timer:null,saving:!1,version:0,latex:``};r.version+=1,r.latex=t,r.timer&&clearTimeout(r.timer),r.timer=setTimeout(()=>{r.timer=null,Gi(e)},n),Pt.set(e,r)}async function Gi(e){let t=Pt.get(e);if(!t||t.saving)return;t.saving=!0;let n=t.version,r=t.latex;try{let i=await Vi(e,r);t.version===n&&(P.set(e,i.resume),Ki(`resume`,e,i.resume))}catch{}finally{t.saving=!1,t.version!==n&&Wi(e,t.latex,0)}}function Ki(e,t,n){if(!n?.pdf_base64)return;let r=e===`resume`?`[data-prep-resume-latex="${t}"]`:`[data-prep-cover-letter-latex="${t}"]`,i=v.querySelector(r)?.closest(`.prep-panel`),a=i?.querySelector(`.prep-cover-pdf`),o=i?.querySelector(`.prep-cover-pdf-link`),s=e===`resume`?`/api/roles/${encodeURIComponent(t)}/resume.pdf`:`/api/roles/${encodeURIComponent(t)}/cover-letter.pdf`;a&&(a.src=`${s}?v=${Date.now()}`),o&&(o.href=s)}async function qi(e,t=``,n=``){let r=await fetch(`/api/roles/${encodeURIComponent(e)}/cover-letter`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({tweaks:t,previous_latex:n})});if(!r.ok)throw Error(`Cover letter generation failed`);return r.json()}async function Ji(e,t){let n=await fetch(`/api/roles/${encodeURIComponent(e)}/cover-letter/save`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({latex:t})});if(!n.ok)throw Error(`Cover letter save failed`);return n.json()}function Yi(e,t,n=``,r=Et){let i=Ft.get(e)??{timer:null,saving:!1,version:0,latex:``,tweaks:``};i.version+=1,i.latex=t,i.tweaks=n,i.timer&&clearTimeout(i.timer),i.timer=setTimeout(()=>{i.timer=null,Xi(e)},r),Ft.set(e,i)}async function Xi(e){let t=Ft.get(e);if(!t||t.saving)return;t.saving=!0;let n=t.version,r=t.latex,i=t.tweaks;try{let a=await Ji(e,r);t.version===n&&(F.set(e,{...a.cover_letter,tweaks:i}),Ki(`coverLetter`,e,a.cover_letter))}catch{}finally{t.saving=!1,t.version!==n&&Yi(e,t.latex,t.tweaks,0)}}async function Zi(e){if(F.has(e))return F.get(e);let t=await fetch(`/api/roles/${encodeURIComponent(e)}/cover-letter`);if(!t.ok)throw Error(`Cover letter request failed`);let n=await t.json();return n.cover_letter&&F.set(e,n.cover_letter),n.cover_letter}async function Qi(e){let t=await fetch(`/api/roles/${encodeURIComponent(e)}/review-later`,{method:`POST`});if(!t.ok)throw Error(`Review later update failed`);return(await t.json()).role}async function $i(e,t){let n=await fetch(`/api/roles/${encodeURIComponent(e)}/status`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({status:t})});if(!n.ok)throw Error(`Status update failed`);return(await n.json()).role}function ea(e){return`${e}-${globalThis.crypto?.randomUUID?.()??`${Date.now()}-${Math.random()}`}`}function ta(e){window.location.hash!==e&&window.history.pushState({},``,e||`${window.location.pathname}${window.location.search}`)}async function na({seedJobs:e=null}={}){De.hidden=!1,document.body.classList.add(`prepped-open`),ta(`#prepped-roles`),e?(I=e,L=L??I[0]?.role_id??null,$()):I.length===0&&(ke.textContent=`loading prepared roles...`),await ia(),aa()}function ra({clearHash:e=!0}={}){De.hidden=!0,document.body.classList.remove(`prepped-open`),oa(),R.clear(),z.forEach(e=>URL.revokeObjectURL(e)),z.clear(),Rt.clear(),zt.clear(),e&&window.location.hash===`#prepped-roles`&&ta(``)}window.addEventListener(`pagehide`,()=>{document.querySelectorAll(`[data-preview-blob-url]`).forEach(e=>{URL.revokeObjectURL(e.dataset.previewBlobUrl)}),z.forEach(e=>URL.revokeObjectURL(e)),z.clear(),Rt.clear()});async function ia(){try{let e=await fetch(`/api/autoprep/jobs`);if(!e.ok)throw Error(`Prepped roles request failed`);I=(await e.json()).jobs??[],I.some(e=>Number(e.role_id)===Number(L))||(L=I[0]?.role_id??null),$()}catch{ke.textContent=`could not refresh preparation progress.`}}function aa(){oa(),I.some(sa)&&(It=window.setInterval(ia,2e3))}function oa(){It!==null&&window.clearInterval(It),It=null}function sa(e){return[`queued`,`generating_resume_tweaks`,`regenerating_resume`,`generating_cover_letter`].includes(e.overall_status)}function ca(e){return{queued:`Queued`,generating_resume_tweaks:`Generating resume tweaks`,regenerating_resume:`Regenerating resume`,generating_cover_letter:`Generating cover letter`,partially_complete:`Partially complete`,ready:`Ready`,failed:`Failed`,interrupted:`Interrupted`,generating_tweaks:`Generating tweaks`,regenerating:`Regenerating`,generating:`Generating`}[e]??W(e)}function la(e,t){let n=t===`cover-letter`?`cover_letter`:`resume`;return`${e.updated_at||``}:${e[`${n}_artifact_path`]||``}`}function ua(e,{close:t=!1}={}){let n=z.get(e);n&&URL.revokeObjectURL(n),z.delete(e),Rt.delete(e),zt.delete(e),t&&R.delete(e)}function da(){Rt.forEach((e,t)=>{let[n,r]=t.split(`:`),i=I.find(e=>Number(e.role_id)===Number(n));(!i||la(i,r)!==e)&&ua(t,{close:!0})})}function $(){da();let e=I.filter(sa).length;ke.textContent=I.length?`${I.length} prepped ${I.length===1?`role`:`roles`}${e?` · ${e} in progress`:``}`:`No queued or prepared roles.`,Ae.innerHTML=I.map(e=>`
    <button type="button" class="prepped-list-item${Number(e.role_id)===Number(L)?` is-active`:``}" data-prepped-role="${e.role_id}">
      <strong>${G(e.company_name)}</strong><span>${G(e.title)}</span>
      <small class="status-${U(e.overall_status)}">${U(ca(e.overall_status))}</small>
    </button>`).join(``),fa(),aa()}function fa(){let e=I.findIndex(e=>Number(e.role_id)===Number(L)),t=I[e];if(!t){je.innerHTML=`<div class="prepped-empty"><h3>nothing prepped yet.</h3><p>Queue Interested roles from Autoprep Interested.</p></div>`;return}let n=G(t.title),r=tn(t.role_url),i=r?`<a class="prepped-role-link" href="${U(r)}" target="_blank" rel="noopener noreferrer">${n}<span aria-hidden="true">↗</span></a>`:n,a=[[`Location`,t.location||`Unavailable`],[`Added`,H(t.date_added||t.created_at)||`Unavailable`],[`Last seen`,H(t.last_seen_at)||`Unavailable`],[`Posting ID`,t.posting_id||`Unavailable`]];je.innerHTML=`
    <header class="prepped-detail-heading">
      <div><p class="eyebrow">${G(t.company_name)}</p><h3>${i}</h3></div>
      <span class="prepped-status status-${U(t.overall_status)}">${U(ca(t.overall_status))}</span>
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
      ${ma(t,`resume`,`Resume`)}
      ${ma(t,`cover-letter`,`Cover letter`)}
    </div>
    <div class="prepped-detail-actions">
      <button type="button" data-prepped-nav="previous" ${e<=0?`disabled`:``}>Previous</button>
      <button type="button" data-prepped-nav="next" ${e>=I.length-1?`disabled`:``}>Next</button>
      <button type="button" data-autoprep-open-folder ${t.artifact_directory?``:`disabled`}>Open Documents Folder</button>
      <button class="success" type="button" data-autoprep-applied ${t.overall_status===`ready`?``:`disabled`}>Applied</button>
    </div>
    <p class="prepped-safety-note">Autoprep prepares files only. It never submits an application.</p>`}async function pa(e,t){let n=`${e.role_id}:${t}`,r=la(e,t);if(!(Rt.get(n)===r||Bt.has(n))){ua(n),Bt.add(n),zt.delete(n),fa();try{let i=await bn(`/api/autoprep/roles/${encodeURIComponent(e.role_id)}/documents/${t}.pdf?v=${encodeURIComponent(e.updated_at||``)}`),a=I.find(t=>Number(t.role_id)===Number(e.role_id));if(!R.has(n)||!a||la(a,t)!==r){URL.revokeObjectURL(i),R.delete(n);return}z.set(n,i),Rt.set(n,r)}catch(e){zt.set(n,e instanceof Error?e.message:`PDF preview unavailable`)}finally{Bt.delete(n),Number(L)===Number(e.role_id)&&fa()}}}function ma(e,t,n){let r=t===`cover-letter`?`cover_letter`:`resume`,i=e[`${r}_status`],a=e[`${r}_artifact_path`],o=a?.split(`/`).pop()??`Not available`,s=e[`${r}_error`],c=e[`${r}_instruction`]||``,l=`${e.role_id}:${t}`,u=Lt.get(l)??c,d=[`queued`,`generating`,`generating_tweaks`,`regenerating`].includes(i),ee=[`failed`,`interrupted`].includes(i)?`<button type="button" data-autoprep-retry="${t}">Retry ${U(n.toLowerCase())}</button>`:``,f=R.has(l),te=`/api/autoprep/roles/${encodeURIComponent(e.role_id)}/documents/${t}.pdf?v=${encodeURIComponent(e.updated_at||``)}`,p=z.get(l),m=zt.get(l),h=Bt.has(l),ne=a?`<a class="prep-cover-pdf-link" data-autoprep-view="${t}" href="${U(te)}" target="_blank" rel="noreferrer" aria-label="View ${U(n.toLowerCase())} PDF in browser">View PDF</a>`:``;return`
    <section class="prepped-document${f?` has-open-preview`:``} status-${U(i)}">
      <div class="prepped-document-heading"><h4>${U(n)}</h4><span>${U(ca(i))}</span></div>
      <p class="prepped-filename">${U(o)}</p>
      ${s?`<p class="prepped-error">${U(s)}</p>`:``}
      <div class="prepped-document-actions">
        <button type="button" data-autoprep-preview="${t}" ${a?``:`disabled`}>${f?`Hide preview`:`Preview PDF`}</button>
        ${ne}
        ${ee}
      </div>
      <div class="prepped-pdf-preview" data-autoprep-preview-panel="${t}" ${f&&a?``:`hidden`}>
        ${f&&p?`<iframe title="${U(n)} PDF preview" src="${U(p)}"></iframe>`:``}
        ${f&&h?`<p>Loading PDF preview...</p>`:``}
        ${f&&m?`<p class="prepped-error">${G(m)}</p>`:``}
      </div>
      <label class="prepped-comments-label" for="prepped-comments-${U(l)}">Comments for the next version</label>
      <textarea id="prepped-comments-${U(l)}" data-autoprep-comments="${t}" rows="4" placeholder="Describe specific, truthful changes..." ${d?`disabled`:``}>${G(u)}</textarea>
      <button class="prepped-regenerate" type="button" data-autoprep-regenerate="${t}" ${i===`ready`&&String(u).trim()?``:`disabled`}>${d?`Regenerating...`:`Regenerate ${U(n)}`}</button>
    </section>`}async function ha(e,t,n){if(n.disabled)return;let r=`${e.role_id}:${t}`,i=je.querySelector(`[data-autoprep-comments="${t}"]`),a=String(i?.value||Lt.get(r)||``).trim();if(!a){i?.focus();return}n.disabled=!0,n.textContent=`Queuing regeneration...`;try{let n=await fetch(`/api/autoprep/roles/${encodeURIComponent(e.role_id)}/regenerate/${t}`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({comments:a,idempotency_key:ea(`regenerate-${t}`)})}),i=await n.json();if(!n.ok)throw Error(i.error||`Regeneration request failed`);Lt.delete(r),ua(r,{close:!0});let o=I.findIndex(t=>Number(t.role_id)===Number(e.role_id));o>=0&&(I[o]=i.job),$()}catch(e){window.alert(e instanceof Error?e.message:`Regeneration request failed`),await ia()}}async function ga(e,t,n){if(!n.disabled){n.disabled=!0,n.textContent=`Queuing retry...`;try{let n=await fetch(`/api/autoprep/roles/${encodeURIComponent(e)}/retry/${t}`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({idempotency_key:ea(`retry-${t}`)})}),r=await n.json();if(!n.ok)throw Error(r.error||`Retry request failed`);ua(`${e}:${t}`,{close:!0});let i=I.findIndex(t=>Number(t.role_id)===Number(e));i>=0&&(I[i]=r.job),$()}catch{await ia()}}}async function _a(e,t){if(t.disabled)return;t.disabled=!0,t.textContent=`Moving to Applied...`;let n=I.findIndex(t=>Number(t.role_id)===Number(e));try{if(!(await fetch(`/api/autoprep/roles/${encodeURIComponent(e)}/applied`,{method:`POST`})).ok)throw Error(`Applied update failed`);ua(`${e}:resume`,{close:!0}),ua(`${e}:cover-letter`,{close:!0}),I.splice(n,1),L=I[Math.min(n,I.length-1)]?.role_id??null,$(),gr()}catch{await ia()}}_e.addEventListener(`click`,li),Se.addEventListener(`click`,ui),ve.addEventListener(`click`,di),Ee.addEventListener(`click`,()=>na()),Oe.addEventListener(`click`,ra),Ae.addEventListener(`click`,e=>{let t=e.target.closest(`[data-prepped-role]`);t&&(L=Number(t.dataset.preppedRole),$())}),je.addEventListener(`input`,e=>{let t=e.target.closest(`[data-autoprep-comments]`);if(!t)return;let n=`${L}:${t.dataset.autoprepComments}`;Lt.set(n,t.value);let r=je.querySelector(`[data-autoprep-regenerate="${t.dataset.autoprepComments}"]`),i=I.find(e=>Number(e.role_id)===Number(L)),a=t.dataset.autoprepComments===`cover-letter`?`cover_letter`:`resume`;r&&(r.disabled=i?.[`${a}_status`]!==`ready`||!t.value.trim())}),je.addEventListener(`click`,async e=>{let t=I.find(e=>Number(e.role_id)===Number(L));if(!t)return;let n=e.target.closest(`[data-prepped-nav]`);if(n){let e=I.indexOf(t),r=n.dataset.preppedNav===`next`?1:-1;L=I[e+r]?.role_id??t.role_id,$();return}let r=e.target.closest(`[data-autoprep-preview]`);if(r){let e=r.dataset.autoprepPreview,n=`${t.role_id}:${e}`;R.has(n)?(R.delete(n),fa()):(R.add(n),fa(),pa(t,e));return}let i=e.target.closest(`[data-autoprep-regenerate]`);if(i){ha(t,i.dataset.autoprepRegenerate,i);return}let a=e.target.closest(`[data-autoprep-retry]`);if(a){ga(t.role_id,a.dataset.autoprepRetry,a);return}let o=e.target.closest(`[data-autoprep-open-folder]`);if(o&&!o.disabled){o.disabled=!0,o.textContent=`Opening...`;try{if(!(await fetch(`/api/autoprep/roles/${encodeURIComponent(t.role_id)}/open-folder`,{method:`POST`})).ok)throw Error(`Could not open the documents folder.`);o.textContent=`Opened in Finder`,window.setTimeout(()=>{o.isConnected&&(o.textContent=`Open Documents Folder`,o.disabled=!1)},1500)}catch(e){o.textContent=e instanceof Error?e.message:`Could not open folder`,o.disabled=!1}return}let s=e.target.closest(`[data-autoprep-applied]`);s&&_a(t.role_id,s)}),Te.addEventListener(`click`,fi),g.addEventListener(`click`,e=>{let t=e.target.closest(`[data-review-action]`);t&&Oi(t.dataset.reviewAction)}),_.addEventListener(`click`,e=>{e.target.closest(`.prep-summary-action`)&&e.stopPropagation()}),_.addEventListener(`input`,e=>{let t=e.target.closest(`[data-prep-resume-tweaks]`);if(t){let e=Number(t.dataset.prepResumeTweaks);Number.isFinite(e)&&Mt.set(e,t.value);return}let n=e.target.closest(`[data-prep-resume-latex]`);if(n){let e=Number(n.dataset.prepResumeLatex);if(!Number.isFinite(e))return;Wi(e,n.value);return}let r=e.target.closest(`[data-prep-cover-letter-latex]`);if(!r)return;let i=Number(r.dataset.prepCoverLetterLatex);if(!Number.isFinite(i))return;let a=r.closest(`.prep-cover-letter`)?.querySelector(`[data-prep-cover-letter-tweaks="${i}"]`)?.value??``;Yi(i,r.value,a)}),_.addEventListener(`scroll`,e=>{e.target.closest(`[data-prep-resume-latex], [data-prep-cover-letter-latex]`)},!0),_.addEventListener(`focusout`,e=>{let t=e.target.closest(`[data-prep-resume-latex]`);if(t){let e=Number(t.dataset.prepResumeLatex);if(!Number.isFinite(e))return;Wi(e,t.value,0);return}let n=e.target.closest(`[data-prep-cover-letter-latex]`);if(!n)return;let r=Number(n.dataset.prepCoverLetterLatex);if(!Number.isFinite(r))return;let i=n.closest(`.prep-cover-letter`)?.querySelector(`[data-prep-cover-letter-tweaks="${r}"]`)?.value??``;Yi(r,n.value,i,0)}),_.addEventListener(`submit`,async e=>{let t=e.target.closest(`[data-prep-role-chat-form]`);if(!t||!M[0])return;e.preventDefault();let n=Number(t.dataset.prepRoleChatForm);if(!Number.isFinite(n))return;let r=t.querySelector(`[data-prep-role-chat-input="${n}"]`),i=r?.value?.trim()??``;if(!i){r?.focus();return}let a=[...Nt.get(n)??[],{role:`user`,content:i}];Nt.set(n,a),v.querySelector(`.prep-role-chat`)?.replaceWith(Q(Mi(M[0],{messages:a,loading:!0})));try{let e=await Ui(n,a),t=[...a,e.message];Nt.set(n,t),v.querySelector(`.prep-role-chat`)?.replaceWith(Q(Mi(M[0],{messages:t})))}catch{let e=[...a,{role:`assistant`,content:`could not answer right now.`}];Nt.set(n,e),v.querySelector(`.prep-role-chat`)?.replaceWith(Q(Mi(M[0],{messages:e})))}}),_.addEventListener(`click`,async e=>{let t=e.target.closest(`[data-prep-section-target]`);if(t){let e=t.dataset.prepSectionTarget,n=e?document.getElementById(e):null;if(n instanceof HTMLDetailsElement){n.open=!0,n.scrollIntoView({behavior:`smooth`,block:`start`});let e=n.querySelector(`summary`);e?.setAttribute(`tabindex`,`-1`),e?.focus({preventScroll:!0})}return}if(e.target.closest(`[data-prep-analysis]`)&&M[0]){let e=M[0].id;v.querySelector(`.prep-analysis`)?.replaceWith(Q(Z(M[0],{loading:!0})));try{let t=await Ii(e,{force:!0});if(M[0]?.id!==e)return;v.querySelector(`.prep-analysis`)?.replaceWith(Q(Z(M[0],{analysis:t})))}catch{v.querySelector(`.prep-analysis`)?.replaceWith(Q(Z(M[0],{error:!0})))}return}if(e.target.closest(`[data-prep-resume-regenerate]`)&&M[0]){let e=M[0].id,t=v.querySelector(`.prep-resume`),n=t?.querySelector(`[data-prep-resume-tweaks="${e}"]`)?.value??``,r=t?.querySelector(`[data-prep-resume-latex="${e}"]`)?.value??``;if(!n.trim()){t?.querySelector(`[data-prep-resume-tweaks="${e}"]`)?.focus();return}Mt.set(e,n),t?.replaceWith(Q(Ai(M[0],{loading:!0})));try{let t=await Hi(e,n,r);P.set(e,t.resume),v.querySelector(`.prep-resume`)?.replaceWith(Q(Ai(M[0],{resume:t.resume}))),K()}catch{v.querySelector(`.prep-resume`)?.replaceWith(Q(Ai(M[0],{resume:P.get(e),tweaks:n}))),K()}return}if(e.target.closest(`[data-prep-cover-letter]`)&&M[0]){let e=M[0].id,t=v.querySelector(`.prep-cover-letter`),n=t?.querySelector(`[data-prep-cover-letter-tweaks="${e}"]`)?.value??``,r=n.trim()?t?.querySelector(`[data-prep-cover-letter-latex="${e}"]`)?.value??``:``;t?.replaceWith(Q(Pi(M[0],{loading:!0})));try{let t=await qi(e,n,r);F.set(e,t.cover_letter),v.querySelector(`.prep-cover-letter`)?.replaceWith(Q(Pi(M[0],{coverLetter:t.cover_letter}))),K()}catch{v.querySelector(`.prep-cover-letter`)?.replaceWith(Q(Pi(M[0],{coverLetter:F.get(e),tweaks:n}))),K()}return}let n=e.target.closest(`[data-prep-action]`);if(n){Li(n.dataset.prepAction);return}let r=e.target.closest(`[data-prep-feedback]`);if(!r||!M[0])return;let i=M[0].id,a=N.get(i),o=Array.isArray(a?.feedback_items)?a.feedback_items.length:0,s=jt.get(i)??0;if(r.dataset.prepFeedback===`accept`||r.dataset.prepFeedback===`ignore`){let e=a?.feedback_items?.[s];if(!e)return;let t=v.querySelector(`[data-prep-feedback-comment]`)?.value??``,n=r.dataset.prepFeedback,o=n;r.disabled=!0,r.textContent=n===`accept`?`adding...`:`ignoring...`;try{if(n===`accept`){let n=await Ri(i,s,e,t),r=document.querySelector(`.job[data-role-id="${CSS.escape(String(i))}"]`);n.role&&(M[0]=n.role,Qr(n.role,r)),ya(i,n.tweak_prompt??e.tweak_prompt??``),va(i,s,a)}else await zi(i,s,e,t),va(i,s,a)}catch{r.disabled=!1,r.textContent=o}return}let c=r.dataset.prepFeedback===`next`?1:-1;jt.set(i,Math.max(0,Math.min(s+c,o-1))),v.querySelector(`.prep-analysis`)?.replaceWith(Q(Z(M[0],{analysis:a})))});function va(e,t,n){let r=n.feedback_items.filter((e,n)=>n!==t),i=Math.min(t,Math.max(r.length-1,0)),a={...n,feedback_items:r,verdict:r.length===0?`ready_to_apply`:n.verdict};jt.set(e,i),N.set(e,a),v.querySelector(`.prep-analysis`)?.replaceWith(Q(Z(M[0],{analysis:a})))}function ya(e,t){let n=String(t||``).trim();if(!n)return;let r=Mt.get(e)?.trim()??``,i=r?`${r}\n\n${n}`:n;Mt.set(e,i);let a=v.querySelector(`[data-prep-resume-tweaks="${e}"]`);a&&(a.value=i,a.focus())}document.addEventListener(`keydown`,e=>{e.key===`Escape`&&!Fe.hidden&&Rn(),e.key===`Escape`&&!o.hidden&&$t(),e.key===`Escape`&&!g.hidden&&ui(),e.key===`Escape`&&!_.hidden&&fi(),e.key===`Escape`&&!De.hidden&&ra(),e.key===`Escape`&&!Ue.hidden&&Kn(),e.key===`Escape`&&!it.hidden&&er(),e.key===`Escape`&&!dt.hidden&&lr(),e.key===`Escape`&&!_t.hidden&&Tr()}),Pe.addEventListener(`click`,Ln),Le.addEventListener(`click`,Rn),Ie.addEventListener(`click`,Rn);function ba(){return Array.from(document.querySelectorAll(`.pane-toggle`))}function xa(){return ba().some(e=>e.getAttribute(`aria-expanded`)===`true`)}function Sa(){ze.textContent=xa()?`collapse all`:`expand all`}function Ca(){document.querySelectorAll(`.pane-toggle`).forEach(e=>{e.setAttribute(`aria-expanded`,`true`),e.querySelector(`.chevron`).textContent=`v`,e.parentElement.querySelector(`.pane-body`).hidden=!1})}function wa(){document.querySelectorAll(`.job[open]`).forEach(e=>{e.open=!1}),document.querySelectorAll(`.pane-toggle`).forEach(e=>{e.setAttribute(`aria-expanded`,`false`),e.querySelector(`.chevron`).textContent=`>`,e.parentElement.querySelector(`.pane-body`).hidden=!0})}ze.addEventListener(`click`,()=>{xa()?wa():Ca(),Sa()}),Be.addEventListener(`click`,()=>{At=!At,Be.textContent=At?`show empty`:`hide empty`,T&&Cn(T.statuses)}),He.addEventListener(`click`,Gn),We.addEventListener(`click`,Kn),rt.addEventListener(`click`,$n),at.addEventListener(`click`,er),ut.addEventListener(`click`,cr),ft.addEventListener(`click`,lr),Me.addEventListener(`click`,wr),vt.addEventListener(`click`,Tr),yt.addEventListener(`submit`,e=>{e.preventDefault(),Or(yt).catch(()=>{C.textContent=`could not add company.`})}),bt.addEventListener(`submit`,e=>{e.preventDefault(),Nr(bt).catch(()=>{wt.textContent=`could not add role.`})}),w.addEventListener(`submit`,e=>{let t=e.target.closest(`[data-company-link-form]`);t&&(e.preventDefault(),kr(t).catch(()=>{C.textContent=`could not add link.`}))}),w.addEventListener(`input`,e=>{let t=e.target.closest(`[data-company-notes]`);t&&Ir(t.dataset.companyNotes)}),w.addEventListener(`change`,e=>{let t=e.target.closest(`[data-company-tier]`);if(!t)return;let n=t.closest(`.company-panel`);n&&Rr(n,t.value),window.clearTimeout(Xt.get(t.dataset.companyTier)),Lr(t.dataset.companyTier).catch(()=>{Fr(`could not save company.`)})}),w.addEventListener(`click`,e=>{let t=e.target.closest(`[data-delete-company]`);if(t){let e=Pr(t.dataset.deleteCompany),n=e?.name?W(e.name):`this company`;if(!window.confirm(`Deactivate ${n}? It will be hidden from company counts and skipped during scans.`))return;t.disabled=!0,jr(t.dataset.deleteCompany).catch(()=>{C.textContent=`could not deactivate company.`,t.disabled=!1});return}let n=e.target.closest(`[data-delete-career-page]`);if(!n)return;let r=n.closest(`.company-link-row`)?.querySelector(`.company-link-text`)?.textContent?.trim();window.confirm(`Delete ${r||`this career link`}?`)&&(n.disabled=!0,Ar(n.dataset.deleteCareerPage).catch(()=>{C.textContent=`could not delete link.`,n.disabled=!1}))}),Ge.addEventListener(`change`,e=>{let t=e.target.closest(`input[type="checkbox"], select, input[data-setting-text], textarea[data-setting-textarea]`);t&&dr(t)}),Ge.addEventListener(`submit`,async e=>{e.preventDefault();let t=Ge.querySelector(`button[type="submit"]`),n=Ge.querySelectorAll(`input[type="checkbox"][name], select[name], input[data-setting-text][name], textarea[data-setting-textarea][name]`),r={};n.forEach(e=>{let t=e.name;t&&(r[t]=e.type===`checkbox`?e.checked:e.value)}),t.disabled=!0,t.textContent=`saving...`;try{S.textContent=`saving settings...`;let e=await fetch(`/api/config`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(r)});if(!e.ok)throw Error(`Config update failed`);q(await e.json(),`settings saved.`)}catch{S.textContent=`could not save settings.`,S.classList.remove(`is-empty`)}finally{t.disabled=!1,t.textContent=`save settings`}}),Ze.addEventListener(`input`,()=>{et.disabled=!Ze.value.trim()}),$e.addEventListener(`click`,pr),et.addEventListener(`click`,mr),nt.addEventListener(`click`,fr),gt.addEventListener(`click`,_r);function Ta(){if(window.location.hash===`#prepped-roles`){na();return}ra({clearHash:!1})}window.addEventListener(`popstate`,Ta),gr(),window.location.hash===`#prepped-roles`&&Ta(),Wr({applyDefaultCollapsed:!0}).catch(()=>{un(null,`could not load resume.`),fn([],`could not load cover letter examples.`),_n()}),Br().then(()=>{Vr()}).catch(()=>{x.textContent=`could not load scan status`});