import{t as e}from"./preload-helper-Czpn1I53.js";var{sankey:t,sankeyLinkHorizontal:n}=await e(async()=>{let{sankey:e,sankeyLinkHorizontal:t}=await import(`/assets/d3-sankey.js`);return{sankey:e,sankeyLinkHorizontal:t}},[]),r=document.querySelector(`#stats`),i=document.querySelector(`#status-list`),a=document.querySelector(`#search-toggle`),o=document.querySelector(`#search-dialog`),s=document.querySelector(`#search-backdrop`),c=document.querySelector(`#search-form`),l=document.querySelector(`#search-input`),u=document.querySelector(`#close-search`),ee=document.querySelector(`#materials-panel`),te=document.querySelector(`#materials-toggle`),ne=document.querySelector(`#materials-body`),re=document.querySelector(`#materials-summary`),ie=document.querySelector(`#materials-required-warning`),d=document.querySelector(`#resume-meta`),f=document.querySelector(`#resume-upload`),ae=document.querySelector(`#resume-upload-button`),oe=document.querySelector(`#resume-resource-meta`),se=document.querySelector(`#resume-resource-upload`),ce=document.querySelector(`#resume-resource-upload-button`),le=document.querySelector(`#resume-resource-list`),ue=document.querySelector(`#cover-letter-meta`),de=document.querySelector(`#cover-letter-upload`),fe=document.querySelector(`#cover-letter-upload-button`),pe=document.querySelector(`#cover-letter-list`),me=document.querySelector(`#experience-note-meta`),he=document.querySelector(`#experience-note-upload`),ge=document.querySelector(`#experience-note-upload-button`),_e=document.querySelector(`#experience-note-list`),p=document.querySelector(`#material-index-button`),m=document.querySelector(`#material-index-warning`),ve=document.querySelector(`#material-index-status`),ye=document.querySelector(`#review-discovered`),be=document.querySelector(`#prep-interested`),h=document.querySelector(`#review-view`),xe=document.querySelector(`#review-heading`),Se=document.querySelector(`#review-progress`),Ce=document.querySelector(`#review-card`),we=document.querySelector(`#close-review`),g=document.querySelector(`#prep-view`),Te=document.querySelector(`#prep-heading`),Ee=document.querySelector(`#prep-progress`),_=document.querySelector(`#prep-card`),De=document.querySelector(`#close-prep`),Oe=document.querySelector(`#autoprep-interested`),ke=document.querySelector(`#prepped-roles`),Ae=document.querySelector(`#autoprep-view`),je=document.querySelector(`#close-autoprep`),Me=document.querySelector(`#autoprep-select-all`),Ne=document.querySelector(`#autoprep-deselect-all`),Pe=document.querySelector(`#autoprep-selection-count`),Fe=document.querySelector(`#autoprep-status`),Ie=document.querySelector(`#autoprep-list`),Le=document.querySelector(`#autoprep-selected`),Re=document.querySelector(`#prepped-view`),ze=document.querySelector(`#close-prepped`),Be=document.querySelector(`#prepped-summary`),Ve=document.querySelector(`#prepped-list`),He=document.querySelector(`#prepped-detail`),v=document.querySelector(`#scan-all-button`),Ue=document.querySelector(`#manage-companies-button`),y=document.querySelector(`#scan-status-bar`),b=document.querySelector(`#scan-status-text`),We=document.querySelector(`#scan-last-time`),Ge=document.querySelector(`#scan-failures-open`),Ke=document.querySelector(`#scan-failures-dialog`),qe=document.querySelector(`#scan-failures-backdrop`),Je=document.querySelector(`#scan-failures-close`),Ye=document.querySelector(`#scan-failures-list`),Xe=document.querySelector(`#toggle-all`),Ze=document.querySelector(`#collapse-empty`),Qe=document.querySelector(`#toolbar-summary`),$e=document.querySelector(`#settings-open`),et=document.querySelector(`#settings-view`),tt=document.querySelector(`#settings-close`),x=document.querySelector(`#settings-status`),nt=document.querySelector(`#settings-form`),rt=document.querySelector(`#settings-profile-options`),it=document.querySelector(`#settings-options`),at=document.querySelector(`#central-store-summary`),ot=document.querySelector(`#central-store-sync-summary`),st=document.querySelector(`#central-api-url-input`),ct=document.querySelector(`#central-passkey-input`),lt=document.querySelector(`#central-save-button`),ut=document.querySelector(`#central-sync-button`),dt=document.querySelector(`#recommendation-history-summary`),ft=document.querySelector(`#clear-recommendation-history`),pt=document.querySelector(`#metrics-open-button`),mt=document.querySelector(`#metrics-view`),ht=document.querySelector(`#metrics-close`),S=document.querySelector(`#metrics-status`),gt=document.querySelector(`#metrics-overview`),_t=document.querySelector(`#metrics-sections`),vt=document.querySelector(`#metrics-scan-list`),yt=document.querySelector(`#sankey-open-button`),bt=document.querySelector(`#sankey-view`),xt=document.querySelector(`#sankey-close`),C=document.querySelector(`#sankey-status`),St=document.querySelector(`#sankey-canvas`),Ct=document.querySelector(`#sankey-path-list`),wt=document.querySelector(`#app-update-button`),Tt=document.querySelector(`#companies-view`),Et=document.querySelector(`#companies-close`),w=document.querySelector(`#companies-status`),Dt=document.querySelector(`#company-create-form`),T=document.querySelector(`#companies-list`),Ot=document.querySelector(`#role-add-form`),kt=document.querySelector(`#role-url-input`),At=document.querySelector(`#role-company-input`),jt=document.querySelector(`#role-company-options`),Mt=document.querySelector(`#role-add-status`),Nt=3,Pt=1200,Ft=new Set([`applied`,`OA`,`interview`,`rejected`,`offer`]),It=new Map([[`discovered`,`#4f6472`],[`interested`,`#00897b`],[`disinterested`,`#626970`],[`applied`,`#2257ad`],[`oa`,`#b36b00`],[`interview`,`#5f2bd8`],[`rejected`,`#b93d2d`],[`offer`,`#137347`],[`closed`,`#53606b`],[`archived`,`#765b4a`]]),Lt=/^(?:about (?:the )?(?:role|team|job)|about this role|job description|job responsibilities|minimum qualifications|preferred qualifications|qualifications|requirements|responsibilities|what to expect|what (?:you'll|you’ll|you will) (?:bring|do)|what'?s in it for you|who you are|your objectives|your skills & talents):?$/i,Rt=!0,E=null,zt=null,D=[],O=[],k=[],A=null,j=[],M=[],N=new Map,Bt=new Map,P=new Map,Vt=new Map,F=new Map,Ht=new Map,Ut=new Map,Wt=new Map,I=[],L=new Set,R=!1,z=[],B=null,Gt=null,Kt=!1,qt=null,Jt=!1,Yt=null,Xt=null,Zt=null,Qt=null,V=null,$t=[],en=new Map;function H(){return E?.query?.trim()??``}function tn(){let e=!!H();a.classList.toggle(`search-active`,e),a.setAttribute(`aria-label`,e?`clear search`:`search jobs`)}function nn(){l.value=H(),o.hidden=!1,c.hidden=!1,l.focus(),l.select()}function rn(){o.hidden=!0,c.hidden=!0,a.focus()}function an(e){return e?new Intl.DateTimeFormat(void 0,{month:`short`,day:`numeric`,hour:`numeric`,minute:`2-digit`}).format(new Date(e)).toLocaleLowerCase():``}function U(e){return e?new Intl.DateTimeFormat(void 0,{month:`short`,day:`numeric`,hour:`numeric`,minute:`2-digit`}).format(new Date(e)).replace(`, `,` `).toLocaleLowerCase():``}function W(e){return String(e??``).replaceAll(`&`,`&amp;`).replaceAll(`<`,`&lt;`).replaceAll(`>`,`&gt;`).replaceAll(`"`,`&quot;`).replaceAll(`'`,`&#039;`)}function G(e){return String(e??``).toLocaleLowerCase()}function K(e){return W(G(e))}function on(e){return e}function q(e=_){e.querySelectorAll(`[data-prep-resume-latex], [data-prep-cover-letter-latex]`).forEach(on)}function sn(){return`
    <svg class="role-link-icon" viewBox="0 0 24 24" aria-hidden="true">
      <path d="M7 17 17 7"></path>
      <path d="M8 7h9v9"></path>
    </svg>
  `}function cn(){return`
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M12 5v14"></path>
      <path d="M5 12h14"></path>
    </svg>
  `}function ln(){return`
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M3 6h18"></path>
      <path d="M8 6V4h8v2"></path>
      <path d="m19 6-1 14H6L5 6"></path>
      <path d="M10 11v5"></path>
      <path d="M14 11v5"></path>
    </svg>
  `}function un(e,t,n){let r=`<span class="role-title-text">${K(e)}</span>`;return t?`<a class="${n}" href="${W(t)}" target="_blank" rel="noreferrer">${r}${sn()}</a>`:`<span class="${n}">${r}</span>`}function dn(e){r.innerHTML=[[`companies`,e.companies_total],[`jobs`,e.jobs_total],[`applications`,e.applications_total]].map(([e,t])=>`<dl class="stat"><dt>${K(e)}</dt><dd>${t}</dd></dl>`).join(``)}function fn(e=E){if(!e){Qe.innerHTML=``;return}let t=t=>e.statuses.find(e=>e.key===t)?.count??0;Qe.innerHTML=[[`discovered`,t(`discovered`)],[`interested`,t(`interested`)],[`applied`,e.stats?.applications_total??0],[`total`,e.stats?.jobs_total??0]].map(([e,t])=>`
        <dl>
          <dt>${K(e)}</dt>
          <dd>${t}</dd>
        </dl>
      `).join(``)}function pn(e,t=``){if(zt=e,ae.textContent=e?`replace`:`upload`,t){d.textContent=t;return}if(!e){d.textContent=`no resume uploaded`;return}let n=U(e.updated_at),r=xn(e.content_bytes);d.textContent=[G(e.filename),r,n].filter(Boolean).join(` | `)}function mn(e,t=``){O=Array.isArray(e)?e:[],fe.textContent=O.length>0?`add`:`upload`,ue.textContent=t||(O.length===0?`no examples uploaded`:`${O.length} ${O.length===1?`example`:`examples`} stored`);let n=O.slice(0,3),r=Math.max(O.length-n.length,0);pe.innerHTML=n.map(e=>{let t=xn(e.content_bytes);return`
        <li title="${K(e.filename)}">
          <span>${K(e.filename)}</span>
          <small>${W(t)}</small>
        </li>
      `}).join(``),r>0&&pe.insertAdjacentHTML(`beforeend`,`<li class="examples-more"><span>+${r} more</span></li>`)}function hn(e,t=``){k=Array.isArray(e)?e:[],ge.textContent=k.length>0?`add`:`upload`,me.textContent=t||(k.length===0?`no notes uploaded`:`${k.length} ${k.length===1?`note`:`notes`} stored`);let n=k.slice(0,3),r=Math.max(k.length-n.length,0);_e.innerHTML=n.map(e=>{let t=xn(e.content_bytes);return`
        <li title="${K(e.filename)}">
          <span>${K(e.filename)}</span>
          <small>${W(t)}</small>
        </li>
      `}).join(``),r>0&&_e.insertAdjacentHTML(`beforeend`,`<li class="examples-more"><span>+${r} more</span></li>`)}function gn(e,t=``){A=e??null;let n=A?.status??`missing`,r=n!==`ready`,i=k.length>0;if(m.hidden=!r,m.textContent=t||A?.warning||``,p.disabled=!i,p.textContent=n===`ready`?`reindex materials`:`index materials`,t)ve.textContent=t;else if(n===`ready`){let e=Number(A?.document_count??0),t=Number(A?.skipped_source_count??0),n=U(A?.generated_at);ve.textContent=[`${e} indexed ${e===1?`page`:`pages`}`,t?`${t} unreadable upload skipped`:``,n].filter(Boolean).join(` | `)}else ve.textContent=n===`stale`?`index out of date`:`not indexed`}function _n(e,t=``){D=Array.isArray(e)?e:[],ce.textContent=D.length>0?`add`:`upload`,oe.textContent=t||(D.length===0?`no resources uploaded`:`${D.length} ${D.length===1?`resource`:`resources`} stored`);let n=D.slice(0,3),r=Math.max(D.length-n.length,0);le.innerHTML=n.map(e=>{let t=xn(e.bytes);return`
        <li title="${K(e.filename)}">
          <span>${K(e.filename)}</span>
          <small>${W(t)}</small>
        </li>
      `}).join(``),r>0&&le.insertAdjacentHTML(`beforeend`,`<li class="examples-more"><span>+${r} more</span></li>`)}function vn(e,t={}){pn(e?.master_resume??null),_n(e?.resume_resources??[]),mn(e?.cover_letter_examples??[]),hn(e?.experience_notes??[]),gn(e?.material_index??null),yn(e?.ui),(!Kt||t.applyDefaultCollapsed)&&(bn(!!e?.ui?.default_collapsed),Kt=!0)}function yn(e=null){let t=zt?`resume ready`:`no resume`,n=D.length===0?`no resources`:`${D.length} ${D.length===1?`resource`:`resources`}`,r=O.length,i=r===0?`no cover letters`:`${r} cover ${r===1?`letter`:`letters`}`,a=k.length,o=a===0?`no notes`:`${a} experience ${a===1?`note`:`notes`}`;ie.hidden=!(typeof e?.has_missing_required_materials==`boolean`?e.has_missing_required_materials:!zt||r===0||a===0),re.textContent=`${t} | ${n} | ${i} | ${o}`}function bn(e){ee.classList.toggle(`collapsed`,e),te.setAttribute(`aria-expanded`,String(!e)),te.querySelector(`.materials-chevron`).textContent=e?`>`:`v`,ne.hidden=e}function xn(e){return Number.isFinite(e)?e<1024?`${e} b`:`${Math.round(e/1024)} kb`:``}function Sn(e){i.innerHTML=e.map(e=>{let t=e.jobs.map(t=>Cn(t,e.key)).join(``);return`
        <section class="status-pane ${e.count===0?`empty`:``} ${Rt?`hidden-empty`:``}" id="status-${W(e.key)}" data-bucket="${W(e.key)}">
          <button class="pane-toggle" type="button" aria-expanded="false">
            <span class="chevron">></span>
            <span class="pane-title">${K(e.label)}</span>
            <span class="count">${e.count}</span>
          </button>
          <div class="pane-body" hidden>
            ${t?`<div class="jobs">${t}</div>`:`<p class="empty-copy">no jobs in this status.</p>`}
          </div>
        </section>
      `}).join(``)}function Cn(e,t){return`
    <details class="job" data-role-id="${W(e.id)}">
      <summary class="job-summary">
        <span class="job-chevron">></span>
        <span class="job-identity">
          <span class="job-company">[${K(e.company_name)}]</span>
          ${un(e.title,e.role_url,`job-title`)}
          ${t===`interested`&&e.prep_started?En():``}
          ${t===`closed`&&e.updated_in_latest_scan?wn():``}
          ${[`discovered`,`interested`].includes(t)&&e.missing_from_latest_scan?Tn():``}
        </span>
      </summary>
      <div class="job-detail">
        ${t===`discovered`?Dn(e):``}
        ${t===`interested`?On(e):``}
        ${t===`disinterested`?kn(e):``}
        ${t===`applied`?An(e):``}
        ${t===`OA`?jn(e):``}
        ${t===`interview`?Mn(e):``}
        ${t===`closed`?Nn(e):``}
        <dl>
          ${e.location?`<div>
                  <dt>location</dt>
                  <dd>${K(e.location)}</dd>
                </div>`:``}
          <div>
            <dt>updated</dt>
            <dd>${an(e.updated_at)}</dd>
          </div>
        </dl>
      </div>
    </details>
  `}function wn(){return`<span class="latest-scan-dot" title="updated in latest scan" aria-label="updated in latest scan"></span>`}function Tn(){return`<span class="missing-latest-scan-dot" title="not seen in latest scan" aria-label="not seen in latest scan"></span>`}function En(){return`<span class="prep-started-dot" title="application materials started" aria-label="application materials started"></span>`}function Dn(e){return`
    <div class="job-actions job-actions-nowrap" aria-label="discovered role actions">
      <button class="job-action success" type="button" data-review-role-id="${e.id}">view</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="interested">interested</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="disinterested">disinterested</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="closed">closed</button>
    </div>
  `}function On(e){return`
    <div class="job-actions" aria-label="interested role actions">
      <button class="job-action success" type="button" data-prep-role-id="${e.id}">prep</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="applied">applied</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="disinterested">disinterested</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="closed">closed</button>
    </div>
  `}function kn(e){return`
    <div class="job-actions" aria-label="disinterested role actions">
      <button class="job-action success" type="button" data-role-id="${e.id}" data-status="interested">interested</button>
    </div>
  `}function An(e){return`
    <div class="job-actions job-actions-nowrap" aria-label="applied role actions">
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="OA">oa</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="interview">interview</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="rejected">rejected</button>
    </div>
  `}function jn(e){return`
    <div class="job-actions job-actions-nowrap" aria-label="oa role actions">
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="interview">interview</button>
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="disinterested">disinterested</button>
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="rejected">rejected</button>
    </div>
  `}function Mn(e){return`
    <div class="job-actions" aria-label="interview role actions">
      <button class="job-action danger" type="button" data-role-id="${e.id}" data-status="rejected">rejected</button>
      <button class="job-action success" type="button" data-role-id="${e.id}" data-status="offer">offer</button>
    </div>
  `}function Nn(e){return`
    <div class="job-actions" aria-label="closed role actions">
      <button class="job-action" type="button" data-role-id="${e.id}" data-status="interested">interested</button>
    </div>
  `}function Pn(e){E=e,l.value=e.query,tn(),dn(e.stats),fn(e),Sn(e.statuses),xa(),ri(e.statuses),ai(e.statuses)}function Fn(e){Yt=e??null;let t=!!e?.scanning,n=t&&!!e?.cancel_requested,r=Number(e?.completed_companies??0),i=Number(e?.total_companies??0),a=Number(e?.failed_companies??0),o=typeof e?.error==`string`?e.error.trim():``,s=Array.isArray(e?.failures)?e.failures:[];v.disabled=n,v.textContent=t?n?`cancelling...`:`cancel scan`:`scan roles`,v.classList.toggle(`danger`,t&&!n),y.hidden=!t&&!o&&s.length===0,y.classList.toggle(`scanning`,t),y.classList.toggle(`scan-error`,!t&&!!o||s.length>0),b.textContent=n?`cancelling scan...`:t?`scanning roles${i>0?` ${r}/${i}`:``}${a>0?`, ${a} failed`:``}`:s.length>0?`${s.length} recent scan ${s.length===1?`failure`:`failures`}`:o?`last scan error: ${o}`:`scan idle`,Ge&&Ye&&(Ge.hidden=s.length===0,Ye.innerHTML=s.slice(0,5).map(e=>{let t=e?.company_name||`unknown company`,n=e?.error||`scan failed`;return`
          <p>
            <span>${K(t)}</span>
            <span>${W(n)}</span>
          </p>
        `}).join(``),s.length===0&&Ln());let c=e?.last_scan_at;We.textContent=c?`last scan: ${U(c)}`:`last scan: never`,Jt&&!t&&X(H()).catch(()=>{}),Jt=t}function In(){Ge.hidden||(Ke.hidden=!1,Je.focus())}function Ln(){Ke.hidden=!0}function J(e,t=``){Xt=e;let n=Array.isArray(e?.settings)?e.settings:[],r=n.filter(e=>e.key?.startsWith(`applicant_`)),i=n.filter(e=>!e.key?.startsWith(`applicant_`)),a=e?.central??{};x.textContent=t,x.classList.toggle(`is-empty`,!t);let o=Number(e?.recommendation_history_count??0);dt.textContent=o>0?`${o} saved ${o===1?`feedback decision`:`feedback decisions`}`:`no saved resume feedback decisions`,ft.disabled=o===0,Rn(a),rt.innerHTML=r.map(e=>zn(e)).join(``),it.innerHTML=i.map(e=>zn(e)).join(``),Y(!1)}function Rn(e){let t=e?.api_url??``;st.value=t,ct.value=``;let n=e?.passkey_configured?`passkey saved`:`no passkey saved`;at.textContent=t?`${G(t)} | ${n}`:`no api url | ${n}`,ot.textContent=`${Number(e?.companies_linked??0)} linked | ${Number(e?.companies_unlinked??0)} unlinked | ${Number(e?.companies_needs_review??0)} review | ${Number(e?.companies_failed??0)} failed`,ut.disabled=!t}function zn(e){if(e.control===`text`&&e.editable!==!1)return Bn(e);if(e.control===`select`&&e.editable!==!1)return Vn(e);if(e.control!==`toggle`||e.editable===!1)return Hn(e);let t=e.value?`checked`:``,n=e.default?`on by default`:`off by default`;return`
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
  `}function Bn(e){let t=e.default?`default: ${G(e.default)}`:`optional`,n=e.input_type??`text`,r=e.autocomplete??`name`;return`
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
  `}function Vn(e){let t=Array.isArray(e.options)?e.options:[],n=`default: ${G(e.default)}`;return`
    <label class="setting-option">
      <span class="setting-copy">
        <span class="setting-label">${K(e.label)}</span>
        <span class="setting-description">${K(e.description)}</span>
        <span class="setting-default">${K(n)}</span>
      </span>
      <select class="setting-select" name="${W(e.key)}">
        ${t.map(t=>{let n=t.value===e.value?`selected`:``;return`<option value="${W(t.value)}" ${n}>${K(t.label)}</option>`}).join(``)}
      </select>
    </label>
  `}function Hn(e){let t=e.default?`on by default`:`off by default`,n=e.value?`automatic`:`off`;return`
    <div class="setting-option setting-option-readonly">
      <span class="setting-copy">
        <span class="setting-label">${K(e.label)}</span>
        <span class="setting-description">${K(e.description)}</span>
        <span class="setting-default">${K(t)}</span>
      </span>
      <span class="setting-badge">${K(n)}</span>
    </div>
  `}function Y(e){nt.querySelectorAll(`input, select`).forEach(t=>{t.disabled=e}),lt.disabled=e,ut.disabled=e||!st.value.trim(),wt.disabled=e}async function Un(){et.hidden=!1,document.body.classList.add(`settings-open`),tt.focus(),Xt?J(Xt):(x.textContent=`loading settings...`,x.classList.remove(`is-empty`),it.innerHTML=``);try{await Gn()}catch{x.textContent=`could not load settings.`}}function Wn(){et.hidden=!0,document.body.classList.remove(`settings-open`),$e.focus()}async function Gn(){let e=await fetch(`/api/config`);if(!e.ok)throw Error(`Config request failed`);J(await e.json())}function Kn(e){let t=e?.value;return t==null?`n/a`:e?.kind===`ratio`?Number(t).toLocaleString(void 0,{maximumFractionDigits:2,minimumFractionDigits:0}):typeof t==`number`?t.toLocaleString():G(t)}function qn(e,t=`metric-card`){return`
    <article class="${t}">
      <span>${K(e?.label)}</span>
      <strong>${W(Kn(e))}</strong>
    </article>
  `}function Jn(e,t=``){Zt=e,S.textContent=t||(e?.updated_at?`updated ${U(e.updated_at)}`:``),S.classList.toggle(`is-empty`,!S.textContent);let n=Array.isArray(e?.overview)?e.overview:[],r=Array.isArray(e?.sections)?e.sections:[],i=Array.isArray(e?.recent_scans)?e.recent_scans:[];gt.innerHTML=n.map(e=>qn(e)).join(``),_t.innerHTML=r.map(Yn).join(``),vt.innerHTML=i.length?i.map(Xn).join(``):`<p class="empty-copy">no scan runs recorded.</p>`}function Yn(e){let t=Array.isArray(e?.metrics)?e.metrics:[];return`
    <section class="metrics-section">
      <div class="metrics-section-heading">
        <h3>${K(e?.title)}</h3>
      </div>
      <div class="metrics-section-grid">
        ${t.map(e=>qn(e,`metric-card metric-card-compact`)).join(``)}
      </div>
    </section>
  `}function Xn(e){let t=e?.scan_status??`unknown`,n=e?.started_at?U(e.started_at):`not started`,r=e?.finished_at?U(e.finished_at):`not finished`,i=e?.error?`<span>${K(e.error)}</span>`:``;return`
    <article class="metrics-scan-row">
      <div>
        <strong>${K(e?.company_name??`unknown company`)}</strong>
        <span>${K(n)} -> ${K(r)}</span>
        ${i}
      </div>
      <span class="metrics-status-pill">${K(t)}</span>
    </article>
  `}async function Zn(){mt.hidden=!1,document.body.classList.add(`metrics-open`),ht.focus(),Zt?Jn(Zt):(S.textContent=`loading metrics...`,S.classList.remove(`is-empty`),gt.innerHTML=``,_t.innerHTML=``,vt.innerHTML=``);try{await $n()}catch{S.textContent=`could not load metrics.`}}function Qn(){mt.hidden=!0,document.body.classList.remove(`metrics-open`),pt.focus()}async function $n(){let e=await fetch(`/api/metrics`);if(!e.ok)throw Error(`Metrics request failed`);Jn(await e.json())}function er(e,t=``){Qt=e;let n=Number(e?.role_count??0),r=Array.isArray(e?.links)?e.links:[],i=Array.isArray(e?.paths)?e.paths:[];C.textContent=t||(e?.updated_at?`${n.toLocaleString()} roles | updated ${U(e.updated_at)}`:``),C.classList.toggle(`is-empty`,!C.textContent),St.innerHTML=r.length?tr(e):`<p class="empty-copy">no role transitions recorded yet.</p>`,Ct.innerHTML=i.length?i.map(ar).join(``):`<p class="empty-copy">no role paths recorded yet.</p>`}function tr(e){let t=Array.isArray(e?.nodes)?e.nodes:[],n=Array.isArray(e?.links)?e.links:[],r=ir(t,n),i=r.nodes,a=r.links,o=(r.flowLinks??n).map(e=>{let t=i.get(e.source),n=i.get(e.target),r=a.get(e);if(!t||!n||!r)return``;let o=r.width,s=n.x<t.x,c=nr(e.target),l=r.priority?`0.42`:s?`0.28`:`0.34`,u=r.path??rr({isBacktrack:s,sourceX:t.x+t.width,sourceY:r.sourceY,targetX:n.x,targetY:r.targetY,width:o});return`
        <path class="${[`sankey-link`,s?`sankey-link-backtrack`:``,r.priority?`sankey-link-priority`:``].filter(Boolean).join(` `)}" d="${u}" fill="${r.path?`none`:c}" fill-opacity="${l}" stroke="${c}" style="stroke-width: ${r.path?o:1}px">
          <title>${K(t.label)} to ${K(n.label)}: ${Number(e.value??0).toLocaleString()}</title>
        </path>
      `}).join(``),s=Array.from(i.values()).map(e=>{let t=Number(e.history_count??e.current_count??0),n=Number(e.value??t),i=n>0?n.toLocaleString():`0`,a=e.x>r.width-180,o=a?e.x-8:e.x+e.width+8,s=Math.max(24,e.y-e.height/2-16),c=a?`end`:`start`,l=nr(e.id);return`
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
  `}function nr(e){return It.get(String(e).toLowerCase())??`#4f6472`}function rr({isBacktrack:e,sourceX:t,sourceY:n,targetX:r,targetY:i,width:a}){let o=a/2,s=n-o,c=n+o,l=i-o,u=i+o;if(e){let e=Math.max(80,Math.abs(t-r)*.42);return[`M ${t} ${s}`,`C ${t-e} ${s}, ${r+e} ${l}, ${r} ${l}`,`L ${r} ${u}`,`C ${r+e} ${u}, ${t-e} ${c}, ${t} ${c}`,`Z`].join(` `)}let ee=Math.max(46,(r-t)*.48);return[`M ${t} ${s}`,`C ${t+ee} ${s}, ${r-ee} ${l}, ${r} ${l}`,`L ${r} ${u}`,`C ${r-ee} ${u}, ${t+ee} ${c}, ${t} ${c}`,`Z`].join(` `)}function ir(e,r){let i=new Map([[`discovered`,0],[`interested`,1],[`disinterested`,2],[`applied`,2],[`oa`,3],[`interview`,3],[`rejected`,4],[`closed`,4],[`archived`,4]]),a=new Map,o=new Map;r.forEach(e=>{a.set(e.target,(a.get(e.target)??0)+Number(e.value??0)),o.set(e.source,(o.get(e.source)??0)+Number(e.value??0))});let s=e.filter(e=>Number(e?.history_count??e?.current_count??0)>0||a.has(e.id)||o.has(e.id)),c=new Set(s.map(e=>e.id)),l=r.filter(e=>c.has(e.source)&&c.has(e.target)&&Number(e.value??0)>0),u=e=>i.get(String(e).toLowerCase())??0,ee=l.filter(e=>u(e.target)>=u(e.source)),te=l.filter(e=>u(e.target)<u(e.source)),ne={nodes:s.map(e=>({...e,fixedValue:Math.max(0,Number(e?.history_count??e?.current_count??0))})),links:ee.map(e=>({...e}))},re=t().nodeId(e=>e.id).nodeWidth(26).nodePadding(44).nodeAlign((e,t)=>Math.min(t-1,u(e.id))).extent([[92,88],[1014,634]]).iterations(32)(ne),ie=new Map;re.nodes.forEach(e=>{ie.set(e.id,{...e,x:e.x0,y:e.y0+(e.y1-e.y0)/2,width:e.x1-e.x0,height:Math.max(1.5,e.y1-e.y0),value:Number(e.fixedValue??e.value??0)})});let d=new Map,f=[],ae=n();re.links.forEach(e=>{let t={source:e.source.id,target:e.target.id,value:e.value};f.push(t),d.set(t,{path:ae(e),width:Math.max(1.5,e.width),sourceY:e.y0,targetY:e.y1,priority:Number(e.value??0)>=20})});let oe=Math.max(.6,...re.links.map(e=>Number(e.width??0)/Math.max(1,Number(e.value??0))));return te.forEach(e=>{let t=ie.get(e.source),n=ie.get(e.target);if(!t||!n)return;let r=Math.max(1.5,Number(e.value??0)*oe),i={...e};f.push(i),d.set(i,{width:r,sourceY:t.y+t.height/2-r/2,targetY:n.y+n.height/2-r/2,priority:!1})}),f.sort((e,t)=>Number(e.value??0)-Number(t.value??0)),{flowLinks:f,height:720,links:d,nodes:ie,width:1120}}function ar(e){let t=Array.isArray(e?.path)?e.path:[];return`
    <article class="sankey-path-row">
      <div>
        <strong>${K(e?.company_name??`unknown company`)} / ${K(e?.title??`untitled role`)}</strong>
        <span>${t.map(e=>K(e)).join(` -> `)}</span>
      </div>
      <span class="metrics-status-pill">${Number(e?.loops_collapsed??0).toLocaleString()} loops</span>
    </article>
  `}async function or(){et.hidden=!0,document.body.classList.remove(`settings-open`),bt.hidden=!1,document.body.classList.add(`sankey-open`),xt.focus(),Qt?er(Qt):(C.textContent=`loading role flow...`,C.classList.remove(`is-empty`),St.innerHTML=``,Ct.innerHTML=``);try{await cr()}catch{C.textContent=`could not load role flow.`}}function sr(){bt.hidden=!0,document.body.classList.remove(`sankey-open`),$e.focus()}async function cr(){let e=await fetch(`/api/role-sankey`);if(!e.ok)throw Error(`Role sankey request failed`);er(await e.json())}async function lr(e){let t=e.name;if(!t)return;let n=e.type===`checkbox`?!e.checked:Xt?.settings?.find(e=>e.key===t)?.value,r=e.type===`checkbox`?e.checked:e.value;Y(!0),x.textContent=`saving settings...`,x.classList.remove(`is-empty`);try{let e=await fetch(`/api/config`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({[t]:r})});if(!e.ok)throw Error(`Config update failed`);J(await e.json(),`settings saved.`)}catch{e.type===`checkbox`?e.checked=n:n!==void 0&&(e.value=n),x.textContent=`could not save settings.`,Y(!1)}}async function ur(){ft.disabled=!0,x.textContent=`clearing recommendation history...`,x.classList.remove(`is-empty`);try{let e=await fetch(`/api/recommendation-history/clear`,{method:`POST`});if(!e.ok)throw Error(`Recommendation history clear failed`);let t=await e.json();J(t.config,`cleared ${t.deleted_count} saved decisions.`)}catch{x.textContent=`could not clear recommendation history.`,ft.disabled=!1}}async function dr(){let e=st.value.trim();if(!e){x.textContent=`central api url is required.`,x.classList.remove(`is-empty`);return}let t={central_api_url:e},n=ct.value.trim();n&&(t.central_passkey=n),Y(!0),x.textContent=`saving central settings...`,x.classList.remove(`is-empty`);try{let e=await fetch(`/api/config`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(t)});if(!e.ok)throw Error(`Central settings update failed`);J(await e.json(),`central settings saved.`)}catch{x.textContent=`could not save central settings.`,Y(!1)}}async function fr(){ut.disabled=!0,x.textContent=`syncing remote company ids...`,x.classList.remove(`is-empty`);try{let e=await fetch(`/api/central/resolve-companies`,{method:`POST`});if(!e.ok)throw Error(`Central company sync failed`);let t=await e.json(),n=t.result??{},r=t.pulled_companies,i=r?` remote: ${Number(r.created??0)} created, ${Number(r.linked??0)} linked, ${Number(r.existing??0)} existing.`:``;J(t.config,`company sync: ${Number(n.linked??0)} matched, ${Number(n.created??0)} created, ${Number(n.needs_review??0)} review, ${Number(n.failed??0)} failed.${i}`),t.companies&&(V=t.companies,_r(t.companies.companies))}catch{x.textContent=`could not sync companies.`,ut.disabled=!st.value.trim()}}async function pr(){let e=await fetch(`/api/central/resolve-companies`,{method:`POST`});if(!e.ok)throw Error(`Central company sync failed`);let t=await e.json();t.companies&&(V=t.companies,_r(t.companies.companies))}async function mr(){let e=pr().catch(()=>{});await Promise.all([X().catch(()=>{i.innerHTML=`<p class="empty-copy">could not load jobs.</p>`}),Tr().catch(()=>{Mt.textContent=`could not load companies.`})]),await e}async function hr(){if(window.confirm(`Update callumployed and restart the tracker?`)){Y(!0),wt.disabled=!0,x.textContent=`updating callumployed; tracker will restart shortly...`,x.classList.remove(`is-empty`);try{if(!(await fetch(`/api/app/update`,{method:`POST`})).ok)throw Error(`App update failed`);x.textContent=`update started. reconnect in a moment.`}catch{x.textContent=`could not start update.`,Y(!1)}}}function gr(e,t=``){V=e;let n=Array.isArray(e?.companies)?e.companies:[];if(_r(n),w.textContent=t||`${n.length} ${n.length===1?`company`:`companies`} stored`,w.classList.toggle(`is-empty`,n.length===0&&!t),n.length===0){T.innerHTML=`<p class="empty-copy">no companies yet.</p>`;return}T.innerHTML=n.map(e=>vr(e)).join(``)}function _r(e){$t=Array.isArray(e)?e:[],jt.innerHTML=$t.map(e=>`<option value="${W(e.name)}"></option>`).join(``)}function vr(e){let t=Array.isArray(e.career_pages)?e.career_pages:[],n=U(e.updated_at),r=yr(e.prestige_tier),i=Number(e.scan_count??0),a=Number(e.discovered_role_count??0),o=i>0&&a===0?`<span class="company-discovery-status">Discovered 0 potential roles</span>`:``;return`
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
              ${br(e.prestige_tier)}
            </select>
          </label>
          <div>
            <span>browser wait</span>
            <strong>${Number(e.browser_extra_wait_ms??0)}ms</strong>
          </div>
        </div>
        <div class="company-links">
          ${t.length>0?t.map(e=>xr(e)).join(``):`<p class="company-empty-links">no career links yet.</p>`}
        </div>
        <section class="company-link-panel" aria-label="add career link">
          <form class="company-link-form" data-company-link-form="${e.id}">
            <input name="label" type="text" placeholder="label" aria-label="career link label" />
            <input name="url" type="url" placeholder="https://..." aria-label="career link url" required />
            <button class="company-link-add" type="submit" aria-label="add career link" title="add career link">
              ${cn()}
            </button>
          </form>
        </section>
        <div class="company-danger-row">
          <button class="company-delete-button" type="button" data-delete-company="${e.id}">
            ${ln()}
            <span>deactivate company</span>
          </button>
        </div>
      </div>
    </details>
  `}function yr(e){let t=String(e??``);return[`0`,`1`,`2`,`3`,`4`].includes(t)?`company-tier-${t}`:`company-tier-unset`}function br(e){let t=String(e??``);return[``,`0`,`1`,`2`,`3`,`4`].map(e=>{let n=e?`tier ${e}`:`not set`,r=e===t?` selected`:``;return`<option value="${W(e)}"${r}>${K(n)}</option>`}).join(``)}function xr(e){let t=e.label?K(e.label):`career page`,n=W(e.url);return`
    <div class="company-link-row" data-career-page-id="${e.id}">
      <a class="company-link-url" href="${n}" target="_blank" rel="noreferrer">
        <span class="company-link-label">${t}</span>
        <span class="company-link-text">${W(e.url)}</span>
      </a>
      <button class="company-link-delete" type="button" data-delete-career-page="${e.id}" aria-label="delete ${t} link" title="delete link">
        ${ln()}
      </button>
    </div>
  `}async function Sr(){Tt.hidden=!1,document.body.classList.add(`companies-open`),Et.focus(),V?gr(V):(w.textContent=`loading companies...`,w.classList.remove(`is-empty`),T.innerHTML=``);try{await wr()}catch{w.textContent=`could not load companies.`}}function Cr(){Tt.hidden=!0,document.body.classList.remove(`companies-open`),Ue.focus()}async function wr(e=``){let t=await fetch(`/api/companies`);if(!t.ok)throw Error(`Companies request failed`);gr(await t.json(),e)}async function Tr(){let e=await fetch(`/api/companies`);if(!e.ok)throw Error(`Companies request failed`);_r((await e.json()).companies)}async function Er(e){let t=new FormData(e),n={name:String(t.get(`name`)??``),career_url:String(t.get(`career_url`)??``),notes:String(t.get(`notes`)??``)};w.textContent=`adding company...`;let r=await fetch(`/api/companies`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(n)});if(!r.ok)throw Error(`Company create failed`);e.reset(),gr(await r.json(),`company added.`),X(H()).catch(()=>{})}async function Dr(e){let t=e.dataset.companyLinkForm;if(!t)return;let n=new FormData(e),r={label:String(n.get(`label`)??``),url:String(n.get(`url`)??``)};w.textContent=`adding link...`;let i=await fetch(`/api/companies/${encodeURIComponent(t)}/career-pages`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(r)});if(!i.ok)throw Error(`Career page create failed`);e.reset(),gr(await i.json(),`link added.`)}async function Or(e){w.textContent=`deleting link...`;let t=await fetch(`/api/company-career-pages/${encodeURIComponent(e)}`,{method:`DELETE`});if(!t.ok)throw Error(`Career page delete failed`);gr(await t.json(),`link deleted.`)}async function kr(e){w.textContent=`deactivating company...`;let t=await fetch(`/api/companies/${encodeURIComponent(e)}`,{method:`DELETE`});if(!t.ok)throw Error(`Company deactivate failed`);gr(await t.json(),`company deactivated.`),X(H()).catch(()=>{})}function Ar(){let e=At.value.trim().toLocaleLowerCase();return $t.find(t=>t.name.toLocaleLowerCase()===e)}async function jr(e){let t=Ar();if(!t?.id){Mt.textContent=`pick a saved company.`;return}let n=new FormData(e),r={company_id:t.id,role_url:String(n.get(`role_url`)??``)};Mt.textContent=`adding role...`;let i=await fetch(`/api/roles`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(r)});if(!i.ok)throw Error(`Role create failed`);let a=await i.json();a.tracker?Pn(a.tracker):await X(H()),kt.value=``;let o=a.role?.title?G(a.role.title):`role`;Mt.textContent=a.scan_error?`${o} added; scan could not finish.`:`${o} added.`}function Mr(e){return(Array.isArray(V?.companies)?V.companies:[]).find(t=>String(t.id)===String(e))}function Nr(e){w.textContent=e,w.classList.remove(`is-empty`)}function Pr(e){window.clearTimeout(en.get(e)),en.set(e,window.setTimeout(()=>{Fr(e).catch(()=>{Nr(`could not save company.`)})},700))}async function Fr(e){let t=T.querySelector(`[data-company-id="${CSS.escape(String(e))}"]`);if(!t)return;let n=t.querySelector(`[data-company-notes="${CSS.escape(String(e))}"]`),r=t.querySelector(`[data-company-tier="${CSS.escape(String(e))}"]`),i=Mr(e),a={notes:n?.value??i?.notes??``,prestige_tier:r?.value??i?.prestige_tier??``};i&&(i.notes=a.notes,i.prestige_tier=a.prestige_tier),Ir(t,a.prestige_tier),Nr(`saving company...`);let o=await fetch(`/api/companies/${encodeURIComponent(e)}`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(a)});if(!o.ok)throw Error(`Company update failed`);V=await o.json(),Nr(`company saved.`),Lr(e)}function Ir(e,t){e.classList.remove(`company-tier-unset`,`company-tier-0`,`company-tier-1`,`company-tier-2`,`company-tier-3`,`company-tier-4`),e.classList.add(yr(t))}function Lr(e){let t=T.querySelector(`[data-company-id="${CSS.escape(String(e))}"]`),n=Mr(e);if(!t||!n)return;let r=Array.isArray(n.career_pages)?n.career_pages:[],i=U(n.updated_at),a=t.querySelector(`.company-summary-meta`);a&&(a.textContent=`${r.length} ${r.length===1?`link`:`links`}${i?` | updated ${i}`:``}`)}async function Rr(){let e=await fetch(`/api/scan/status`);if(e.status===404){v.disabled=!0,y.hidden=!0,y.classList.add(`scan-error`),b.textContent=`restart server to enable scanning`;return}if(!e.ok)throw Error(`Scan status request failed`);Fn(await e.json())}function zr(){qt===null&&(qt=window.setInterval(()=>{Rr().catch(()=>{})},3e3))}async function Br(){v.disabled=!0,v.textContent=`starting...`;try{let e=await fetch(`/api/scan/all`,{method:`POST`});if(e.status===404){v.disabled=!0,v.textContent=`scan roles`,y.hidden=!0,y.classList.add(`scan-error`),b.textContent=`restart server to enable scanning`;return}if(!e.ok&&e.status!==409)throw Error(`Scan start failed`);Fn(await e.json()),zr()}catch{v.disabled=!1,v.textContent=`scan roles`,y.hidden=!0,y.classList.add(`scan-error`),b.textContent=`could not start scan`}}async function Vr(){v.disabled=!0,v.textContent=`cancelling...`;try{let e=await fetch(`/api/scan/cancel`,{method:`POST`});if(e.status===404){v.disabled=!0,v.textContent=`scan roles`,y.hidden=!0,y.classList.add(`scan-error`),b.textContent=`restart server to enable scanning`;return}if(!e.ok&&e.status!==409)throw Error(`Scan cancel failed`);Fn(await e.json()),zr()}catch{v.disabled=!1,v.textContent=`cancel scan`,y.hidden=!1,y.classList.add(`scan-error`),b.textContent=`could not cancel scan`}}async function X(e=``){i.innerHTML=`<p class="empty-copy">loading jobs...</p>`;let t=new URLSearchParams;e&&t.set(`q`,e);let n=await fetch(`/api/tracker?${t.toString()}`);if(!n.ok)throw Error(`Tracker request failed`);Pn(await n.json())}async function Hr(e={}){let t=await fetch(`/api/application-materials`);if(!t.ok)throw Error(`Application materials request failed`);vn(await t.json(),e)}async function Ur(e){if(e){if(!e.name.toLowerCase().endsWith(`.tex`)){pn(zt,`resume must be a .tex file.`);return}ae.disabled=!0,pn(zt,`uploading...`);try{let t=await e.text();if(!(await fetch(`/api/master-resume`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({filename:e.name,content:t})})).ok)throw Error(`Master resume upload failed`);await Hr()}catch{pn(zt,`could not save resume.`),yn()}finally{f.value=``,ae.disabled=!1}}}async function Wr(e){let t=Array.from(e??[]);if(t.length!==0){ce.disabled=!0,_n(D,`uploading ${t.length} ${t.length===1?`resource`:`resources`}...`);try{for(let e of t)if(!(await fetch(`/api/resume-resources`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({filename:e.name,content_base64:await Jr(e)})})).ok)throw Error(`Resume resource upload failed`);await Hr()}catch{_n(D,`could not save every resource.`),yn()}finally{se.value=``,ce.disabled=!1}}}async function Gr(e){let t=Array.from(e??[]);if(t.length!==0){fe.disabled=!0,mn(O,`uploading ${t.length} ${t.length===1?`example`:`examples`}...`);try{for(let e of t){let t={filename:e.name};if(e.name.toLowerCase().endsWith(`.docx`)?t.content_base64=await Jr(e):t.content=await e.text(),!(await fetch(`/api/cover-letter-examples`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(t)})).ok)throw Error(`Cover letter example upload failed`)}await Hr()}catch{mn(O,`could not save every example.`),yn()}finally{de.value=``,fe.disabled=!1}}}async function Kr(e){let t=Array.from(e??[]);if(t.length!==0){ge.disabled=!0,hn(k,`uploading ${t.length} ${t.length===1?`note`:`notes`}...`);try{for(let e of t){let t=e.name.toLowerCase(),n={filename:e.name};if(t.endsWith(`.pdf`)||t.endsWith(`.docx`)?n.content_base64=await Jr(e):n.content=await e.text(),!(await fetch(`/api/experience-notes`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(n)})).ok)throw Error(`Experience note upload failed`)}N.clear(),await Hr()}catch{hn(k,`could not save every note.`),yn()}finally{he.value=``,ge.disabled=!1}}}async function qr(){if(!(p.disabled||k.length===0)){p.disabled=!0,p.textContent=`indexing...`,m.hidden=!1,m.textContent=`Building section pages and a targeted retrieval index...`,ve.textContent=`indexing...`;try{if(!(await fetch(`/api/application-materials/index`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({})})).ok)throw Error(`Application material indexing failed`);await Hr()}catch{m.hidden=!1,m.textContent=`Could not index application materials. Try again.`,ve.textContent=`index failed`}finally{p.disabled=k.length===0,p.textContent=A?.status===`ready`?`reindex materials`:`index materials`}}}function Jr(e){return new Promise((t,n)=>{let r=new FileReader;r.addEventListener(`load`,()=>{let e=String(r.result??``);t(e.includes(`,`)?e.split(`,`,2)[1]:e)}),r.addEventListener(`error`,()=>n(r.error)),r.readAsDataURL(e)})}c.addEventListener(`submit`,e=>{e.preventDefault(),X(l.value.trim()),rn()}),a.addEventListener(`click`,()=>{if(H()){X();return}nn()}),l.addEventListener(`keydown`,e=>{e.key===`Escape`&&(e.stopPropagation(),rn())}),u.addEventListener(`click`,rn),s.addEventListener(`click`,rn),ae.addEventListener(`click`,()=>{f.click()}),f.addEventListener(`change`,()=>{Ur(f.files?.[0])}),ce.addEventListener(`click`,()=>{se.click()}),se.addEventListener(`change`,()=>{Wr(se.files)}),fe.addEventListener(`click`,()=>{de.click()}),de.addEventListener(`change`,()=>{Gr(de.files)}),ge.addEventListener(`click`,()=>{he.click()}),he.addEventListener(`change`,()=>{Kr(he.files)}),p.addEventListener(`click`,()=>{qr()}),te.addEventListener(`click`,()=>{bn(te.getAttribute(`aria-expanded`)===`true`)}),v.addEventListener(`click`,()=>{if(Yt?.scanning){Vr();return}Br()}),i.addEventListener(`click`,e=>{let t=e.target.closest(`[data-review-role-id]`);if(t){si(t.dataset.reviewRoleId);return}let n=e.target.closest(`[data-prep-role-id]`);if(n){li(n.dataset.prepRoleId);return}let r=e.target.closest(`.job-action`);if(r){Yr(r);return}let i=e.target.closest(`.pane-toggle`);if(!i)return;let a=i.parentElement.querySelector(`.pane-body`),o=i.getAttribute(`aria-expanded`)===`true`;i.setAttribute(`aria-expanded`,String(!o)),i.querySelector(`.chevron`).textContent=o?`>`:`v`,a.hidden=o,xa()});async function Yr(e){let{roleId:t,status:n}=e.dataset;if(!t||!n)return;let r=e.closest(`.job-actions`),i=e.closest(`.job`);r.querySelectorAll(`button`).forEach(e=>{e.disabled=!0}),e.textContent=`updating...`;try{let e=await fetch(`/api/roles/${encodeURIComponent(t)}/status`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({status:n})});if(!e.ok)throw Error(`Status update failed`);Xr((await e.json()).role,i)}catch{r.querySelectorAll(`button`).forEach(e=>{e.disabled=!1}),e.textContent=n===`disinterested`?`disinterested`:n.toLowerCase()}}function Xr(e,t){if(!e||!E)return;let n=t?.closest(`.status-pane`)?.dataset.bucket??e.role_status,r=e.role_status,i=Qr(e,n,r);$r(n,r),ei(n,r),fn(),ri(E.statuses),ai(E.statuses),ti(t,i,n,r),xa()}function Zr(e){if(!e||!E)return null;let t=null;return E.statuses.forEach(n=>{let r=n.jobs.findIndex(t=>String(t.id)===String(e.id));r!==-1&&(t={...n.jobs[r],...e},n.jobs[r]=t)}),ri(E.statuses),ai(E.statuses),t}function Qr(e,t,n){let r=e;E.statuses.forEach(t=>{let n=t.jobs.findIndex(t=>String(t.id)===String(e.id));n!==-1&&(r={...t.jobs[n],...e},t.jobs.splice(n,1),t.count=t.jobs.length)});let i=E.statuses.find(e=>e.key===n);return i&&(i.jobs.unshift(r),i.count=i.jobs.length),r}function $r(e,t){E.statuses.forEach(e=>{let t=document.querySelector(`#status-${CSS.escape(e.key)}`);t?.classList.toggle(`empty`,e.count===0);let n=t?.querySelector(`.count`);n&&(n.textContent=e.count)}),[e,t].forEach(e=>{ni(document.querySelector(`#status-${CSS.escape(e)}`))})}function ei(e,t){if(!E.stats)return;let n=Ft.has(e),r=Ft.has(t);if(n===r){dn(E.stats);return}E.stats.applications_total=Number(E.stats.applications_total??0)+(r?1:-1),dn(E.stats)}function ti(e,t,n,r){let i=document.querySelector(`#status-${CSS.escape(r)}`),a=i?.querySelector(`.pane-body`);if(!e||!i||!a)return;e.remove(),ni(document.querySelector(`#status-${CSS.escape(n)}`)),a.hidden=!1;let o=i.querySelector(`.pane-toggle`);o?.setAttribute(`aria-expanded`,`true`);let s=o?.querySelector(`.chevron`);s&&(s.textContent=`v`);let c=a.querySelector(`.jobs`);c||=(a.innerHTML=`<div class="jobs"></div>`,a.querySelector(`.jobs`)),c.insertAdjacentHTML(`afterbegin`,Cn(t,r)),ni(i)}function ni(e){if(!e)return;let t=e.querySelector(`.pane-body`);if(!t)return;let n=t.querySelector(`.jobs`),r=!!n?.querySelector(`.job`),i=t.querySelector(`.empty-copy`);if(r){i?.remove();return}n?.remove(),i||t.insertAdjacentHTML(`beforeend`,`<p class="empty-copy">no jobs in this status.</p>`)}function ri(e){ye.disabled=ii(e).length===0,ye.setAttribute(`aria-label`,`review discovered`),ye.innerHTML=`<span class="review-discovered-label">review discovered</span>`}function ii(e=E?.statuses??[]){return e.find(e=>e.key===`discovered`)?.jobs??[]}function ai(e){be.disabled=oi(e).length===0,be.setAttribute(`aria-label`,`prep interested`),be.innerHTML=`<span class="review-discovered-label">prep interested</span>`}function oi(e=E?.statuses??[]){return e.find(e=>e.key===`interested`)?.jobs??[]}function si(e=null){let t=[...ii()],n=e==null?null:String(e);if(n){let e=t.findIndex(e=>String(e.id)===n);if(e>0){let[n]=t.splice(e,1);t.unshift(n)}}j=t,h.hidden=!1,document.body.classList.add(`review-open`),di()}function ci(){h.hidden=!0,document.body.classList.remove(`review-open`),j=[]}function li(e=null){let t=[...oi()].sort((e,t)=>Number(!!t.prep_started)-Number(!!e.prep_started)),n=e==null?null:String(e);if(n){let e=t.findIndex(e=>String(e.id)===n);if(e>0){let[n]=t.splice(e,1);t.unshift(n)}}M=t,g.hidden=!1,document.body.classList.add(`prep-open`),Di()}function ui(){g.hidden=!0,document.body.classList.remove(`prep-open`),M=[]}function di(e=``){let t=j[0],n=j.length,r=t?fi(t):``;if(xe.textContent=n>0?`review queue`:`review complete`,Se.textContent=n>0?`${n} discovered ${n===1?`role`:`roles`} in queue`:``,h.querySelectorAll(`.review-action`).forEach(e=>{e.disabled=n===0}),!t){Ce.innerHTML=`
      <div class="review-empty">
        <h3>no discovered jobs left.</h3>
        <p>everything in this queue has been handled or moved out of discovered.</p>
      </div>
    `;return}Ce.innerHTML=`
    ${e?`<p class="review-message">${W(e)}</p>`:``}
    ${r?`<p class="review-message review-message-warning">${W(r)}</p>`:``}
    <div class="review-title-row">
      <p class="review-company">${K(t.company_name)}</p>
      ${un(t.title,t.role_url,`review-role-title`)}
    </div>
    <dl class="review-details review-primary-details">
      ${Z(`location`,t.location,!1,`review-location-detail`)}
      ${Z(`first`,U(t.first_seen_at))}
      ${Z(`last`,U(t.last_seen_at))}
    </dl>
    ${pi(t.description)}
    <dl class="review-details review-technical-details">
      ${Z(`notes`,t.notes,!1,`review-wide-detail`)}
      ${Z(`company id`,t.company_id)}
      ${Z(`role id`,t.id)}
      ${Z(`status`,t.role_status)}
      ${Z(`posting id`,t.posting_id)}
      ${Z(`created`,U(t.created_at))}
      ${Z(`updated`,U(t.updated_at))}
      ${Z(`url`,t.role_url,!0,`review-wide-detail`)}
    </dl>
  `}function fi(e){let t=Number(e.review_later_count??0);return t<=Nt?``:`role review has been postponed ${t} times. it is recommended to set it to disinterested.`}function Z(e,t,n=!1,r=``){if(!t)return``;let i=n?`<a href="${W(t)}" target="_blank" rel="noreferrer">${K(t)}</a>`:K(t);return`
    <div class="review-detail ${W(r)}">
      <dt>${K(e)}</dt>
      <dd>${i}</dd>
    </div>
  `}function pi(e){return e?`
    <div class="review-detail review-description">
      <dt>description</dt>
      <dd>${mi(e)}</dd>
    </div>
  `:``}function mi(e){let t=hi(String(e)).replace(/\u00a0/g,` `);if(gi(t))return _i(t);let n=t.split(/\r?\n/).map(e=>e.trim()).filter(Boolean),r=[],i=[],a=()=>{i.length!==0&&(r.push(`<ul>${i.map(e=>`<li>${e}</li>`).join(``)}</ul>`),i=[])};return n.forEach(e=>{let t=e.match(/^#{2,3}\s+(.+)$/);if(t){a(),r.push(`<h3>${K(t[1])}</h3>`);return}if(Ti(e)){a(),r.push(`<h3>${K(e.replace(/:$/,``))}</h3>`);return}let n=e.match(/^[-*]\s+(.+)$/);if(n){i.push(K(n[1]));return}a(),r.push(`<p>${K(e)}</p>`)}),a(),r.join(``)}function hi(e){let t=document.createElement(`textarea`);return t.innerHTML=e,t.value}function gi(e){return/<\/?(?:a|br|div|em|h[1-6]|li|ol|p|span|strong|ul)\b/i.test(e)}function _i(e){let t=document.createElement(`template`);t.innerHTML=e;let n=[];return vi(t.content.childNodes,n),n.join(``)}function vi(e,t){e.forEach(e=>{if(e.nodeType===Node.TEXT_NODE){let n=Ci(e.textContent);n&&t.push(`<p>${K(n)}</p>`);return}if(e.nodeType!==Node.ELEMENT_NODE)return;let n=e,r=n.tagName.toLowerCase();if(r===`script`||r===`style`||r===`br`)return;if(/^h[1-6]$/.test(r)){bi(t,n.textContent);return}if(r===`ul`||r===`ol`){let e=xi(n);e&&t.push(e);return}if(r===`p`){yi(n,t);return}let i=Array.from(n.children).some(e=>[`DIV`,`H1`,`H2`,`H3`,`H4`,`H5`,`H6`,`OL`,`P`,`UL`].includes(e.tagName));if([`article`,`div`,`section`].includes(r)&&i){vi(n.childNodes,t);return}let a=Array.from(n.children).filter(e=>[`UL`,`OL`].includes(e.tagName)),o=Ci(Si(n));if(o&&(wi(o,n)?bi(t,o):t.push(`<p>${K(o)}</p>`)),a.length>0){a.forEach(e=>{let n=xi(e);n&&t.push(n)});return}!o&&i&&vi(n.childNodes,t)})}function yi(e,t){if(!e.querySelector(`br`)){let n=Ci(Si(e));if(!n)return;wi(n,e)?bi(t,n):t.push(`<p>${K(n)}</p>`);return}let n=``,r=()=>{let r=Ci(n);n=``,r&&(wi(r,e)?bi(t,r):t.push(`<p>${K(r)}</p>`))};e.childNodes.forEach(e=>{if(e.nodeType===Node.ELEMENT_NODE&&e.tagName.toLowerCase()===`br`){r();return}n+=` ${e.textContent??``}`}),r()}function bi(e,t){let n=Ci(t).replace(/:$/,``);n&&e.push(`<h3>${K(n)}</h3>`)}function xi(e){let t=Array.from(e.children).filter(e=>e.tagName===`LI`).map(e=>{let t=Ci(Si(e)),n=Array.from(e.children).filter(e=>[`UL`,`OL`].includes(e.tagName)).map(e=>xi(e)).filter(Boolean).join(``);return t||n?`<li>${K(t)}${n}</li>`:``}).filter(Boolean);return t.length>0?`<ul>${t.join(``)}</ul>`:``}function Si(e){let t=e.cloneNode(!0);return t.querySelectorAll(`ul, ol`).forEach(e=>{e.remove()}),t.textContent}function Ci(e){return String(e??``).replace(/\s+/g,` `).trim()}function wi(e,t){let n=e.replace(/:$/,``).trim();return!n||n.length>90?!1:Ti(n)||/:$/.test(e)?!0:/[.!?]$/.test(n)||n.split(/\s+/).length>10?!1:t.querySelector(`strong, b, u`)?!0:Ti(n)}function Ti(e){return Lt.test(String(e).trim())}async function Ei(e){let t=j[0];if(!t)return;if(e===`later`){h.querySelectorAll(`.review-action`).forEach(e=>{e.disabled=!0});try{let e=await Xi(t.id);j.shift(),Zr(e),di(`moved out of this review pass.`)}catch{di(`could not postpone that role. try again.`)}finally{h.querySelectorAll(`.review-action`).forEach(e=>{e.disabled=j.length===0})}return}if(![`interested`,`disinterested`].includes(e))return;let n=h.querySelectorAll(`.review-action`);n.forEach(e=>{e.disabled=!0});try{let n=await Zi(t.id,e);j.shift(),di(e===`interested`?`marked interested.`:`marked disinterested.`),Xr(n,document.querySelector(`.job[data-role-id="${CSS.escape(String(t.id))}"]`))}catch{n.forEach(e=>{e.disabled=!1}),di(`could not update that role. try again.`)}}async function Di(e=``){let t=M[0],n=M.length;if(Te.textContent=n>0?`prep queue`:`prep complete`,Ee.textContent=n>0?`${n} interested ${n===1?`role`:`roles`} in queue`:``,g.querySelectorAll(`.review-action`).forEach(e=>{e.disabled=n===0}),!t){_.innerHTML=`
      <div class="review-empty">
        <h3>no interested jobs left.</h3>
        <p>everything in this queue has been prepped, moved, or postponed.</p>
      </div>
    `;return}_.innerHTML=`
    ${e?`<p class="review-message">${W(e)}</p>`:``}
    <section class="prep-role-hero" aria-label="role overview">
      <div class="review-title-row">
        <div class="prep-role-eyebrow">
          <p class="review-company">${K(t.company_name)}</p>
          <span>application workspace</span>
        </div>
        ${un(t.title,t.role_url,`review-role-title`)}
      </div>
      <dl class="review-details review-primary-details">
        ${Z(`location`,t.location,!1,`review-location-detail`)}
        ${Z(`last`,U(t.last_seen_at))}
        ${Z(`updated`,U(t.updated_at))}
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
      ${Oi(t)}
      ${Mi(t)}
      ${ki(t.id,t.description)}
      ${Ai(t)}
    </div>
  `,q(),Ri(t.id).then(e=>{!e||M[0]?.id!==t.id||(P.set(t.id,e),_.querySelector(`.prep-resume`)?.replaceWith($(Oi(t,{resume:e}))),q())}).catch(()=>{}),Yi(t.id).then(e=>{!e||M[0]?.id!==t.id||(F.set(t.id,e),_.querySelector(`.prep-cover-letter`)?.replaceWith($(Mi(t,{coverLetter:e}))),q())}).catch(()=>{})}function Oi(e,t={}){let n=P.get(e.id),r=t.resume??n,i=t.tweaks??Vt.get(e.id)??``,a=`/api/roles/${encodeURIComponent(e.id)}/resume.pdf`;return t.loading?`
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
      ${Q(e)}
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
        <section class="prep-document-preview" aria-label="résumé preview">
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
    `}function ki(e,t){return`
    <details class="prep-panel prep-description-panel" id="prep-description-${e}">
      <summary class="prep-analysis-header">
        <span class="prep-accordion-icon" aria-hidden="true"></span>
        <h3>description</h3>
      </summary>
      ${pi(t)}
    </details>
  `}function Ai(e,t={}){let n=t.messages??Ht.get(e.id)??[],r=!!t.loading;return`
    <details class="prep-panel prep-role-chat" id="prep-chat-${e.id}">
      <summary class="prep-analysis-header">
        <span class="prep-accordion-icon" aria-hidden="true"></span>
        <h3>chat about this role</h3>
        <span>${n.length?`${n.length} messages`:`ready`}</span>
      </summary>
      <div class="prep-role-chat-log" aria-live="polite">
        ${n.length?n.map(ji).join(``):`<p class="prep-role-chat-empty">ask about fit, risks, resume emphasis, or cover letter angle.</p>`}
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
  `}function ji(e){let t=e?.role===`assistant`?`assistant`:`user`;return`
    <article class="prep-role-chat-message prep-role-chat-message-${t}">
      <span>${t}</span>
      <p>${K(e?.content??``)}</p>
    </article>
  `}function Mi(e,t={}){let n=F.get(e.id),r=t.coverLetter??n,i=t.tweaks??r?.tweaks??``,a=`/api/roles/${encodeURIComponent(e.id)}/cover-letter.pdf`;return t.loading?`
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
          <p>Use the role, résumé, and saved examples to shape the letter.</p>
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
  `}function Q(e,t={}){let n=N.get(e.id);if(!t.loading&&!t.error&&!t.analysis&&n)return Q(e,{analysis:n});if(!t.loading&&!t.error&&!t.analysis)return`
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
    `;let r=t.analysis,i=Array.isArray(r?.feedback_items)?r.feedback_items:[],a=r?.verdict===`ready_to_apply`?`ready to apply`:`tweak`,o=Math.min(Bt.get(e.id)??0,Math.max(i.length-1,0)),s=i[o];return`
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
              ${Ni(s)}
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
  `}function Ni(e){return e?.tweak_prompt?`
    <div class="prep-proposed-edit">
      <p class="prep-proposed-label">tweak prompt</p>
      <p>${K(e.tweak_prompt)}</p>
    </div>
  `:`
      <div class="prep-proposed-edit">
        <p class="prep-proposed-label">feedback only</p>
        <p>not enough information to turn this into a safe resume tweak.</p>
      </div>
    `}async function Pi(e,t={}){if(!t.force&&N.has(e))return N.get(e);let n=await fetch(`/api/roles/${encodeURIComponent(e)}/prep-analysis`);if(!n.ok)throw Error(`Prep analysis request failed`);let r=await n.json();return r.analysis.resources=r.resources??[],N.set(e,r.analysis),r.analysis}function $(e){let t=document.createElement(`template`);return t.innerHTML=e.trim(),t.content.firstElementChild}async function Fi(e){let t=M[0];if(!t)return;let n=g.querySelectorAll(`.review-action`);if(n.forEach(e=>{e.disabled=!0}),e===`later`){try{await Xi(t.id),t.review_later_count=Number(t.review_later_count??0)+1,M.length>1?(M.push(M.shift()),Di(`moved to the back of the prep queue.`)):Di(`only one role is in the prep queue.`)}catch{Di(`could not postpone prep. try again.`)}return}if(e===`applied`)try{let e=await Zi(t.id,`applied`);M.shift(),Di(`moved to applied.`),Xr(e,document.querySelector(`.job[data-role-id="${CSS.escape(String(t.id))}"]`))}catch{n.forEach(e=>{e.disabled=!1}),Di(`could not move that role. try again.`)}}async function Ii(e,t,n,r){let i=await fetch(`/api/roles/${encodeURIComponent(e)}/prep-feedback`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({feedback_index:t,feedback_item:n,comment:r})});if(!i.ok)throw Error(`Prep feedback update failed`);return i.json()}async function Li(e,t,n,r){let i=await fetch(`/api/roles/${encodeURIComponent(e)}/prep-feedback-ignore`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({feedback_index:t,feedback_item:n,comment:r})});if(!i.ok)throw Error(`Prep feedback ignore failed`);return i.json()}async function Ri(e,{force:t=!1}={}){if(!t&&P.has(e))return P.get(e);let n=await fetch(`/api/roles/${encodeURIComponent(e)}/resume`);if(!n.ok)throw Error(`Resume request failed`);let r=await n.json();return r.resume&&P.set(e,r.resume),r.resume}async function zi(e,t){let n=await fetch(`/api/roles/${encodeURIComponent(e)}/resume/save`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({latex:t})});if(!n.ok)throw Error(`Resume save failed`);return n.json()}async function Bi(e,t,n){let r=await fetch(`/api/roles/${encodeURIComponent(e)}/resume`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({tweaks:t,previous_latex:n})});if(!r.ok)throw Error(`Resume generation failed`);return r.json()}async function Vi(e,t){let n=await fetch(`/api/roles/${encodeURIComponent(e)}/chat`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({messages:t})});if(!n.ok)throw Error(`Role chat failed`);return n.json()}function Hi(e,t,n=Pt){let r=Ut.get(e)??{timer:null,saving:!1,version:0,latex:``};r.version+=1,r.latex=t,r.timer&&clearTimeout(r.timer),r.timer=setTimeout(()=>{r.timer=null,Ui(e)},n),Ut.set(e,r)}async function Ui(e){let t=Ut.get(e);if(!t||t.saving)return;t.saving=!0;let n=t.version,r=t.latex;try{let i=await zi(e,r);t.version===n&&(P.set(e,i.resume),Wi(`resume`,e,i.resume))}catch{}finally{t.saving=!1,t.version!==n&&Hi(e,t.latex,0)}}function Wi(e,t,n){if(!n?.pdf_base64)return;let r=e===`resume`?`[data-prep-resume-latex="${t}"]`:`[data-prep-cover-letter-latex="${t}"]`,i=_.querySelector(r)?.closest(`.prep-panel`),a=i?.querySelector(`.prep-cover-pdf`),o=i?.querySelector(`.prep-cover-pdf-link`),s=e===`resume`?`/api/roles/${encodeURIComponent(t)}/resume.pdf`:`/api/roles/${encodeURIComponent(t)}/cover-letter.pdf`;a&&(a.src=`${s}?v=${Date.now()}`),o&&(o.href=s)}async function Gi(e,t=``,n=``){let r=await fetch(`/api/roles/${encodeURIComponent(e)}/cover-letter`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({tweaks:t,previous_latex:n})});if(!r.ok)throw Error(`Cover letter generation failed`);return r.json()}async function Ki(e,t){let n=await fetch(`/api/roles/${encodeURIComponent(e)}/cover-letter/save`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({latex:t})});if(!n.ok)throw Error(`Cover letter save failed`);return n.json()}function qi(e,t,n=``,r=Pt){let i=Wt.get(e)??{timer:null,saving:!1,version:0,latex:``,tweaks:``};i.version+=1,i.latex=t,i.tweaks=n,i.timer&&clearTimeout(i.timer),i.timer=setTimeout(()=>{i.timer=null,Ji(e)},r),Wt.set(e,i)}async function Ji(e){let t=Wt.get(e);if(!t||t.saving)return;t.saving=!0;let n=t.version,r=t.latex,i=t.tweaks;try{let a=await Ki(e,r);t.version===n&&(F.set(e,{...a.cover_letter,tweaks:i}),Wi(`coverLetter`,e,a.cover_letter))}catch{}finally{t.saving=!1,t.version!==n&&qi(e,t.latex,t.tweaks,0)}}async function Yi(e){if(F.has(e))return F.get(e);let t=await fetch(`/api/roles/${encodeURIComponent(e)}/cover-letter`);if(!t.ok)throw Error(`Cover letter request failed`);let n=await t.json();return n.cover_letter&&F.set(e,n.cover_letter),n.cover_letter}async function Xi(e){let t=await fetch(`/api/roles/${encodeURIComponent(e)}/review-later`,{method:`POST`});if(!t.ok)throw Error(`Review later update failed`);return(await t.json()).role}async function Zi(e,t){let n=await fetch(`/api/roles/${encodeURIComponent(e)}/status`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({status:t})});if(!n.ok)throw Error(`Status update failed`);return(await n.json()).role}function Qi(e){return`${e}-${globalThis.crypto?.randomUUID?.()??`${Date.now()}-${Math.random()}`}`}function $i(e){window.location.hash!==e&&window.history.pushState({},``,e||`${window.location.pathname}${window.location.search}`)}async function ea(){R=!1,Le.textContent=`Autoprep Selected`,Ae.hidden=!1,document.body.classList.add(`autoprep-open`),$i(`#autoprep-interested`),Fe.textContent=`loading Interested roles...`;try{let e=await fetch(`/api/autoprep/interested`);if(!e.ok)throw Error(`Interested roles request failed`);I=(await e.json()).roles??[];let t=new Set(I.filter(e=>e.selectable).map(e=>Number(e.id)));L=new Set([...L].filter(e=>t.has(e))),Fe.textContent=``,na()}catch{Fe.textContent=`could not load Interested roles.`,Ie.innerHTML=``}}function ta({clearHash:e=!0}={}){Ae.hidden=!0,document.body.classList.remove(`autoprep-open`),e&&window.location.hash===`#autoprep-interested`&&$i(``)}function na(){if(I.length===0){Ie.innerHTML=`<div class="autoprep-empty"><h3>no Interested roles.</h3><p>Mark roles Interested on the homepage before using Autoprep.</p></div>`,ra();return}Ie.innerHTML=I.map(e=>{let t=Number(e.id),n=e.preparation_status?da(e.preparation_status):e.manual_prep_started?`Manual preparation started`:`Not started`,r=[e.location,e.date_added?`added ${U(e.date_added)}`:``].filter(Boolean).map(K).join(` · `);return`
      <label class="autoprep-role${e.selectable?``:` is-unavailable`}">
        <input type="checkbox" data-autoprep-role="${t}" ${L.has(t)?`checked`:``} ${e.selectable?``:`disabled`} />
        <span class="autoprep-role-copy"><strong>${K(e.company_name)}</strong><span>${K(e.title)}</span><small>${r}</small></span>
        <span class="autoprep-role-status">${W(n)}</span>
      </label>`}).join(``),ra()}function ra(){let e=L.size;Pe.textContent=`${e} selected`,Le.disabled=e===0||R,Me.disabled=R||!I.some(e=>e.selectable),Ne.disabled=R||e===0}async function ia(){if(!(R||L.size===0)){R=!0,Le.disabled=!0,Le.textContent=`Queuing selected roles...`,Fe.textContent=`creating durable preparation jobs...`,Ie.querySelectorAll(`input`).forEach(e=>{e.disabled=!0});try{let e=await fetch(`/api/autoprep/jobs`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({role_ids:[...L],idempotency_key:Qi(`autoprep`)})}),t=await e.json();if(!e.ok)throw Error(t.error||`Autoprep queue request failed`);z=t.jobs??[],B=z[0]?.role_id??null,ta({clearHash:!1}),aa({seedJobs:z})}catch(e){Fe.textContent=e.message||`could not queue selected roles.`,R=!1,Le.textContent=`Autoprep Selected`,na()}}}async function aa({seedJobs:e=null}={}){Re.hidden=!1,document.body.classList.add(`prepped-open`),$i(`#prepped-roles`),e?(z=e,B=B??z[0]?.role_id??null,fa()):z.length===0&&(Be.textContent=`loading prepared roles...`),await sa(),ca()}function oa({clearHash:e=!0}={}){Re.hidden=!0,document.body.classList.remove(`prepped-open`),la(),e&&window.location.hash===`#prepped-roles`&&$i(``)}async function sa(){try{let e=await fetch(`/api/autoprep/jobs`);if(!e.ok)throw Error(`Prepped roles request failed`);z=(await e.json()).jobs??[],z.some(e=>Number(e.role_id)===Number(B))||(B=z[0]?.role_id??null),fa()}catch{Be.textContent=`could not refresh preparation progress.`}}function ca(){la(),z.some(ua)&&(Gt=window.setInterval(sa,2e3))}function la(){Gt!==null&&window.clearInterval(Gt),Gt=null}function ua(e){return[`queued`,`generating_resume_tweaks`,`regenerating_resume`,`generating_cover_letter`].includes(e.overall_status)}function da(e){return{queued:`Queued`,generating_resume_tweaks:`Generating résumé tweaks`,regenerating_resume:`Regenerating résumé`,generating_cover_letter:`Generating cover letter`,partially_complete:`Partially complete`,ready:`Ready`,failed:`Failed`,interrupted:`Interrupted`,generating_tweaks:`Generating tweaks`,regenerating:`Regenerating`,generating:`Generating`}[e]??G(e)}function fa(){let e=z.filter(ua).length;Be.textContent=z.length?`${z.length} prepped ${z.length===1?`role`:`roles`}${e?` · ${e} in progress`:``}`:`No queued or prepared roles.`,Ve.innerHTML=z.map(e=>`
    <button type="button" class="prepped-list-item${Number(e.role_id)===Number(B)?` is-active`:``}" data-prepped-role="${e.role_id}">
      <strong>${K(e.company_name)}</strong><span>${K(e.title)}</span>
      <small class="status-${W(e.overall_status)}">${W(da(e.overall_status))}</small>
    </button>`).join(``),pa(),ca()}function pa(){let e=z.findIndex(e=>Number(e.role_id)===Number(B)),t=z[e];if(!t){He.innerHTML=`<div class="prepped-empty"><h3>nothing prepped yet.</h3><p>Queue Interested roles from Autoprep Interested.</p></div>`;return}let n=t.resume_artifact_path?.split(`/`).pop()??`Not available`,r=t.cover_letter_artifact_path?.split(`/`).pop()??`Not available`,i=[`failed`,`interrupted`].includes(t.resume_status)?`<button type="button" data-autoprep-retry="resume">Retry résumé</button>`:``,a=[`failed`,`interrupted`].includes(t.cover_letter_status)?`<button type="button" data-autoprep-retry="cover-letter">Retry cover letter</button>`:``;He.innerHTML=`
    <header class="prepped-detail-heading"><div><p class="eyebrow">${K(t.company_name)}</p><h3>${K(t.title)}</h3><p>${K(t.location||`location unavailable`)}</p></div><span class="prepped-status status-${W(t.overall_status)}">${W(da(t.overall_status))}</span></header>
    <div class="prepped-document-grid">
      ${ma(`Résumé`,t.resume_status,n,t.resume_error,t.resume_session_id,i)}
      ${ma(`Cover letter`,t.cover_letter_status,r,t.cover_letter_error,t.cover_letter_session_id,a)}
    </div>
    <div class="prepped-detail-actions">
      <button type="button" data-prepped-nav="previous" ${e<=0?`disabled`:``}>Previous</button>
      <button type="button" data-prepped-nav="next" ${e>=z.length-1?`disabled`:``}>Next</button>
      <button type="button" data-autoprep-open-folder ${t.artifact_directory?``:`disabled`}>Open Documents Folder</button>
      <button class="success" type="button" data-autoprep-applied ${t.overall_status===`ready`?``:`disabled`}>Applied</button>
    </div>
    <p class="prepped-safety-note">Autoprep prepares files only. It never submits an application.</p>`}function ma(e,t,n,r,i,a){return`<section class="prepped-document status-${W(t)}"><div class="prepped-document-heading"><h4>${W(e)}</h4><span>${W(da(t))}</span></div><p class="prepped-filename">${W(n)}</p>${i?`<p class="prepped-session">Hermes session: ${W(i)}</p>`:``}${r?`<p class="prepped-error">${W(r)}</p>`:``}${a}</section>`}async function ha(e,t,n){if(!n.disabled){n.disabled=!0,n.textContent=`Queuing retry...`;try{let n=await fetch(`/api/autoprep/roles/${encodeURIComponent(e)}/retry/${t}`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify({idempotency_key:Qi(`retry-${t}`)})}),r=await n.json();if(!n.ok)throw Error(r.error||`Retry request failed`);let i=z.findIndex(t=>Number(t.role_id)===Number(e));i>=0&&(z[i]=r.job),fa()}catch{await sa()}}}async function ga(e,t){if(t.disabled)return;t.disabled=!0,t.textContent=`Moving to Applied...`;let n=z.findIndex(t=>Number(t.role_id)===Number(e));try{if(!(await fetch(`/api/autoprep/roles/${encodeURIComponent(e)}/applied`,{method:`POST`})).ok)throw Error(`Applied update failed`);z.splice(n,1),B=z[Math.min(n,z.length-1)]?.role_id??null,fa(),mr()}catch{await sa()}}ye.addEventListener(`click`,si),we.addEventListener(`click`,ci),be.addEventListener(`click`,li),Oe.addEventListener(`click`,ea),ke.addEventListener(`click`,()=>aa()),je.addEventListener(`click`,ta),ze.addEventListener(`click`,oa),Me.addEventListener(`click`,()=>{R||(L=new Set(I.filter(e=>e.selectable).map(e=>Number(e.id))),na())}),Ne.addEventListener(`click`,()=>{R||(L.clear(),na())}),Ie.addEventListener(`change`,e=>{let t=e.target.closest(`[data-autoprep-role]`);if(!t||R)return;let n=Number(t.dataset.autoprepRole);t.checked?L.add(n):L.delete(n),ra()}),Le.addEventListener(`click`,ia),Ve.addEventListener(`click`,e=>{let t=e.target.closest(`[data-prepped-role]`);t&&(B=Number(t.dataset.preppedRole),fa())}),He.addEventListener(`click`,async e=>{let t=z.find(e=>Number(e.role_id)===Number(B));if(!t)return;let n=e.target.closest(`[data-prepped-nav]`);if(n){let e=z.indexOf(t),r=n.dataset.preppedNav===`next`?1:-1;B=z[e+r]?.role_id??t.role_id,fa();return}let r=e.target.closest(`[data-autoprep-retry]`);if(r){ha(t.role_id,r.dataset.autoprepRetry,r);return}let i=e.target.closest(`[data-autoprep-open-folder]`);if(i&&!i.disabled){i.disabled=!0;try{if(!(await fetch(`/api/autoprep/roles/${encodeURIComponent(t.role_id)}/open-folder`,{method:`POST`})).ok)throw Error(`Folder open failed`)}finally{i.disabled=!1}return}let a=e.target.closest(`[data-autoprep-applied]`);a&&ga(t.role_id,a)}),De.addEventListener(`click`,ui),h.addEventListener(`click`,e=>{let t=e.target.closest(`[data-review-action]`);t&&Ei(t.dataset.reviewAction)}),g.addEventListener(`click`,e=>{e.target.closest(`.prep-summary-action`)&&e.stopPropagation()}),g.addEventListener(`input`,e=>{let t=e.target.closest(`[data-prep-resume-tweaks]`);if(t){let e=Number(t.dataset.prepResumeTweaks);Number.isFinite(e)&&Vt.set(e,t.value);return}let n=e.target.closest(`[data-prep-resume-latex]`);if(n){let e=Number(n.dataset.prepResumeLatex);if(!Number.isFinite(e))return;Hi(e,n.value);return}let r=e.target.closest(`[data-prep-cover-letter-latex]`);if(!r)return;let i=Number(r.dataset.prepCoverLetterLatex);if(!Number.isFinite(i))return;let a=r.closest(`.prep-cover-letter`)?.querySelector(`[data-prep-cover-letter-tweaks="${i}"]`)?.value??``;qi(i,r.value,a)}),g.addEventListener(`scroll`,e=>{e.target.closest(`[data-prep-resume-latex], [data-prep-cover-letter-latex]`)},!0),g.addEventListener(`focusout`,e=>{let t=e.target.closest(`[data-prep-resume-latex]`);if(t){let e=Number(t.dataset.prepResumeLatex);if(!Number.isFinite(e))return;Hi(e,t.value,0);return}let n=e.target.closest(`[data-prep-cover-letter-latex]`);if(!n)return;let r=Number(n.dataset.prepCoverLetterLatex);if(!Number.isFinite(r))return;let i=n.closest(`.prep-cover-letter`)?.querySelector(`[data-prep-cover-letter-tweaks="${r}"]`)?.value??``;qi(r,n.value,i,0)}),g.addEventListener(`submit`,async e=>{let t=e.target.closest(`[data-prep-role-chat-form]`);if(!t||!M[0])return;e.preventDefault();let n=Number(t.dataset.prepRoleChatForm);if(!Number.isFinite(n))return;let r=t.querySelector(`[data-prep-role-chat-input="${n}"]`),i=r?.value?.trim()??``;if(!i){r?.focus();return}let a=[...Ht.get(n)??[],{role:`user`,content:i}];Ht.set(n,a),_.querySelector(`.prep-role-chat`)?.replaceWith($(Ai(M[0],{messages:a,loading:!0})));try{let e=await Vi(n,a),t=[...a,e.message];Ht.set(n,t),_.querySelector(`.prep-role-chat`)?.replaceWith($(Ai(M[0],{messages:t})))}catch{let e=[...a,{role:`assistant`,content:`could not answer right now.`}];Ht.set(n,e),_.querySelector(`.prep-role-chat`)?.replaceWith($(Ai(M[0],{messages:e})))}}),g.addEventListener(`click`,async e=>{let t=e.target.closest(`[data-prep-section-target]`);if(t){let e=t.dataset.prepSectionTarget,n=e?document.getElementById(e):null;if(n instanceof HTMLDetailsElement){n.open=!0,n.scrollIntoView({behavior:`smooth`,block:`start`});let e=n.querySelector(`summary`);e?.setAttribute(`tabindex`,`-1`),e?.focus({preventScroll:!0})}return}if(e.target.closest(`[data-prep-analysis]`)&&M[0]){let e=M[0].id;_.querySelector(`.prep-analysis`)?.replaceWith($(Q(M[0],{loading:!0})));try{let t=await Pi(e,{force:!0});if(M[0]?.id!==e)return;_.querySelector(`.prep-analysis`)?.replaceWith($(Q(M[0],{analysis:t})))}catch{_.querySelector(`.prep-analysis`)?.replaceWith($(Q(M[0],{error:!0})))}return}if(e.target.closest(`[data-prep-resume-regenerate]`)&&M[0]){let e=M[0].id,t=_.querySelector(`.prep-resume`),n=t?.querySelector(`[data-prep-resume-tweaks="${e}"]`)?.value??``,r=t?.querySelector(`[data-prep-resume-latex="${e}"]`)?.value??``;if(!n.trim()){t?.querySelector(`[data-prep-resume-tweaks="${e}"]`)?.focus();return}Vt.set(e,n),t?.replaceWith($(Oi(M[0],{loading:!0})));try{let t=await Bi(e,n,r);P.set(e,t.resume),_.querySelector(`.prep-resume`)?.replaceWith($(Oi(M[0],{resume:t.resume}))),q()}catch{_.querySelector(`.prep-resume`)?.replaceWith($(Oi(M[0],{resume:P.get(e),tweaks:n}))),q()}return}if(e.target.closest(`[data-prep-cover-letter]`)&&M[0]){let e=M[0].id,t=_.querySelector(`.prep-cover-letter`),n=t?.querySelector(`[data-prep-cover-letter-tweaks="${e}"]`)?.value??``,r=n.trim()?t?.querySelector(`[data-prep-cover-letter-latex="${e}"]`)?.value??``:``;t?.replaceWith($(Mi(M[0],{loading:!0})));try{let t=await Gi(e,n,r);F.set(e,t.cover_letter),_.querySelector(`.prep-cover-letter`)?.replaceWith($(Mi(M[0],{coverLetter:t.cover_letter}))),q()}catch{_.querySelector(`.prep-cover-letter`)?.replaceWith($(Mi(M[0],{coverLetter:F.get(e),tweaks:n}))),q()}return}let n=e.target.closest(`[data-prep-action]`);if(n){Fi(n.dataset.prepAction);return}let r=e.target.closest(`[data-prep-feedback]`);if(!r||!M[0])return;let i=M[0].id,a=N.get(i),o=Array.isArray(a?.feedback_items)?a.feedback_items.length:0,s=Bt.get(i)??0;if(r.dataset.prepFeedback===`accept`||r.dataset.prepFeedback===`ignore`){let e=a?.feedback_items?.[s];if(!e)return;let t=_.querySelector(`[data-prep-feedback-comment]`)?.value??``,n=r.dataset.prepFeedback,o=n;r.disabled=!0,r.textContent=n===`accept`?`adding...`:`ignoring...`;try{if(n===`accept`){let n=await Ii(i,s,e,t),r=document.querySelector(`.job[data-role-id="${CSS.escape(String(i))}"]`);n.role&&(M[0]=n.role,Xr(n.role,r)),va(i,n.tweak_prompt??e.tweak_prompt??``),_a(i,s,a)}else await Li(i,s,e,t),_a(i,s,a)}catch{r.disabled=!1,r.textContent=o}return}let c=r.dataset.prepFeedback===`next`?1:-1;Bt.set(i,Math.max(0,Math.min(s+c,o-1))),_.querySelector(`.prep-analysis`)?.replaceWith($(Q(M[0],{analysis:a})))});function _a(e,t,n){let r=n.feedback_items.filter((e,n)=>n!==t),i=Math.min(t,Math.max(r.length-1,0)),a={...n,feedback_items:r,verdict:r.length===0?`ready_to_apply`:n.verdict};Bt.set(e,i),N.set(e,a),_.querySelector(`.prep-analysis`)?.replaceWith($(Q(M[0],{analysis:a})))}function va(e,t){let n=String(t||``).trim();if(!n)return;let r=Vt.get(e)?.trim()??``,i=r?`${r}\n\n${n}`:n;Vt.set(e,i);let a=_.querySelector(`[data-prep-resume-tweaks="${e}"]`);a&&(a.value=i,a.focus())}document.addEventListener(`keydown`,e=>{e.key===`Escape`&&!Ke.hidden&&Ln(),e.key===`Escape`&&!o.hidden&&rn(),e.key===`Escape`&&!h.hidden&&ci(),e.key===`Escape`&&!g.hidden&&ui(),e.key===`Escape`&&!Ae.hidden&&ta(),e.key===`Escape`&&!Re.hidden&&oa(),e.key===`Escape`&&!et.hidden&&Wn(),e.key===`Escape`&&!mt.hidden&&Qn(),e.key===`Escape`&&!bt.hidden&&sr(),e.key===`Escape`&&!Tt.hidden&&Cr()}),Ge.addEventListener(`click`,In),Je.addEventListener(`click`,Ln),qe.addEventListener(`click`,Ln);function ya(){return Array.from(document.querySelectorAll(`.pane-toggle`))}function ba(){return ya().some(e=>e.getAttribute(`aria-expanded`)===`true`)}function xa(){Xe.textContent=ba()?`collapse all`:`expand all`}function Sa(){document.querySelectorAll(`.pane-toggle`).forEach(e=>{e.setAttribute(`aria-expanded`,`true`),e.querySelector(`.chevron`).textContent=`v`,e.parentElement.querySelector(`.pane-body`).hidden=!1})}function Ca(){document.querySelectorAll(`.job[open]`).forEach(e=>{e.open=!1}),document.querySelectorAll(`.pane-toggle`).forEach(e=>{e.setAttribute(`aria-expanded`,`false`),e.querySelector(`.chevron`).textContent=`>`,e.parentElement.querySelector(`.pane-body`).hidden=!0})}Xe.addEventListener(`click`,()=>{ba()?Ca():Sa(),xa()}),Ze.addEventListener(`click`,()=>{Rt=!Rt,Ze.textContent=Rt?`show empty`:`hide empty`,E&&Sn(E.statuses)}),$e.addEventListener(`click`,Un),tt.addEventListener(`click`,Wn),pt.addEventListener(`click`,Zn),ht.addEventListener(`click`,Qn),yt.addEventListener(`click`,or),xt.addEventListener(`click`,sr),Ue.addEventListener(`click`,Sr),Et.addEventListener(`click`,Cr),Dt.addEventListener(`submit`,e=>{e.preventDefault(),Er(Dt).catch(()=>{w.textContent=`could not add company.`})}),Ot.addEventListener(`submit`,e=>{e.preventDefault(),jr(Ot).catch(()=>{Mt.textContent=`could not add role.`})}),T.addEventListener(`submit`,e=>{let t=e.target.closest(`[data-company-link-form]`);t&&(e.preventDefault(),Dr(t).catch(()=>{w.textContent=`could not add link.`}))}),T.addEventListener(`input`,e=>{let t=e.target.closest(`[data-company-notes]`);t&&Pr(t.dataset.companyNotes)}),T.addEventListener(`change`,e=>{let t=e.target.closest(`[data-company-tier]`);if(!t)return;let n=t.closest(`.company-panel`);n&&Ir(n,t.value),window.clearTimeout(en.get(t.dataset.companyTier)),Fr(t.dataset.companyTier).catch(()=>{Nr(`could not save company.`)})}),T.addEventListener(`click`,e=>{let t=e.target.closest(`[data-delete-company]`);if(t){let e=Mr(t.dataset.deleteCompany),n=e?.name?G(e.name):`this company`;if(!window.confirm(`Deactivate ${n}? It will be hidden from company counts and skipped during scans.`))return;t.disabled=!0,kr(t.dataset.deleteCompany).catch(()=>{w.textContent=`could not deactivate company.`,t.disabled=!1});return}let n=e.target.closest(`[data-delete-career-page]`);if(!n)return;let r=n.closest(`.company-link-row`)?.querySelector(`.company-link-text`)?.textContent?.trim();window.confirm(`Delete ${r||`this career link`}?`)&&(n.disabled=!0,Or(n.dataset.deleteCareerPage).catch(()=>{w.textContent=`could not delete link.`,n.disabled=!1}))}),nt.addEventListener(`change`,e=>{let t=e.target.closest(`input[type="checkbox"], select, input[data-setting-text]`);t&&lr(t)}),nt.addEventListener(`submit`,async e=>{e.preventDefault();let t=nt.querySelector(`button[type="submit"]`),n=nt.querySelectorAll(`input[type="checkbox"][name], select[name], input[data-setting-text][name]`),r={};n.forEach(e=>{let t=e.name;t&&(r[t]=e.type===`checkbox`?e.checked:e.value)}),t.disabled=!0,t.textContent=`saving...`;try{x.textContent=`saving settings...`;let e=await fetch(`/api/config`,{method:`POST`,headers:{"Content-Type":`application/json`},body:JSON.stringify(r)});if(!e.ok)throw Error(`Config update failed`);J(await e.json(),`settings saved.`)}catch{x.textContent=`could not save settings.`,x.classList.remove(`is-empty`)}finally{t.disabled=!1,t.textContent=`save settings`}}),st.addEventListener(`input`,()=>{ut.disabled=!st.value.trim()}),lt.addEventListener(`click`,dr),ut.addEventListener(`click`,fr),ft.addEventListener(`click`,ur),wt.addEventListener(`click`,hr);function wa(){if(window.location.hash===`#autoprep-interested`){oa({clearHash:!1}),ea();return}if(window.location.hash===`#prepped-roles`){ta({clearHash:!1}),aa();return}ta({clearHash:!1}),oa({clearHash:!1})}window.addEventListener(`popstate`,wa),mr(),[`#autoprep-interested`,`#prepped-roles`].includes(window.location.hash)&&wa(),Hr({applyDefaultCollapsed:!0}).catch(()=>{pn(null,`could not load resume.`),mn([],`could not load cover letter examples.`),yn()}),Rr().then(()=>{zr()}).catch(()=>{b.textContent=`could not load scan status`});