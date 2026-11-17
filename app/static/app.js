const $=id=>document.getElementById(id);
const statuses=["Scheduled","Checked-in","Completed","Cancelled"];
async function api(url,options={}){const r=await fetch(url,{headers:{"Content-Type":"application/json",...(options.headers||{})},...options});const d=await r.json().catch(()=>null);if(!r.ok)throw Error(d?.detail||d?.message||`Request failed (${r.status})`);return d}
function esc(v){return String(v??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]))}
function toast(msg){$("toast").textContent=msg;$("toast").style.display="block";setTimeout(()=>$("toast").style.display="none",3200)}
function options(items){return items.map(x=>`<option value="${x.id}">${esc(x.full_name)}</option>`).join("")}
async function refreshAll(){try{
 const [d,p,docs,a,v]=await Promise.all([api("/api/dashboard"),api("/api/patients"),api("/api/doctors"),api("/api/appointments"),api("/api/visits")]);
 $("patientsCount").textContent=d.total_patients;$("doctorsCount").textContent=d.active_doctors;$("todayCount").textContent=d.appointments_today;$("visitsCount").textContent=d.total_visits;
 $("patients").innerHTML=p.map(x=>`<article class="item"><strong>${esc(x.full_name)}</strong><small>${esc(x.phone)} · ${esc(x.email)}</small></article>`).join("")||'<p class="muted">No patients registered.</p>';
 $("doctors").innerHTML=docs.map(x=>`<article class="item"><strong>${esc(x.full_name)}</strong><small>${esc(x.specialty)} · ${esc(x.phone)}</small></article>`).join("")||'<p class="muted">No doctors added.</p>';
 ["appointmentPatient","visitPatient"].forEach(id=>$(id).innerHTML=options(p));
 ["appointmentDoctor","visitDoctor"].forEach(id=>$(id).innerHTML=options(docs));
 $("appointments").innerHTML=a.map(x=>`<tr><td>${esc(x.appointment_date)} ${esc(String(x.appointment_time).slice(0,5))}</td><td>${esc(x.patient_name)}</td><td>${esc(x.doctor_name)}</td><td>${esc(x.reason)}</td><td>${esc(x.status)}</td><td><select onchange="changeStatus(${x.id},this.value)">${statuses.map(s=>`<option ${s===x.status?"selected":""}>${s}</option>`).join("")}</select></td></tr>`).join("")||'<tr><td colspan="6">No appointments scheduled.</td></tr>';
 $("visits").innerHTML=v.map(x=>`<article class="item"><strong>${esc(x.patient_name)} · ${esc(x.visit_date)}</strong><small>Doctor: ${esc(x.doctor_name)} · Follow-up: ${esc(x.follow_up_date||"Not scheduled")}</small><small>Visit notes: ${esc(x.clinical_notes||"No notes entered")}</small></article>`).join("")||'<p class="muted">No visit records yet.</p>';
 }catch(e){toast(e.message)}}
function formObject(form){const obj=Object.fromEntries(new FormData(form).entries());for(const k of Object.keys(obj))if(obj[k]==="")obj[k]=null;return obj}
$("patientForm").addEventListener("submit",async e=>{e.preventDefault();try{await api("/api/patients",{method:"POST",body:JSON.stringify(formObject(e.target))});e.target.reset();toast("Patient registered.");refreshAll()}catch(x){toast(x.message)}});
$("doctorForm").addEventListener("submit",async e=>{e.preventDefault();try{await api("/api/doctors",{method:"POST",body:JSON.stringify(formObject(e.target))});e.target.reset();toast("Doctor added.");refreshAll()}catch(x){toast(x.message)}});
$("appointmentForm").addEventListener("submit",async e=>{e.preventDefault();const o=formObject(e.target);o.patient_id=Number(o.patient_id);o.doctor_id=Number(o.doctor_id);try{await api("/api/appointments",{method:"POST",body:JSON.stringify(o)});e.target.reset();toast("Appointment scheduled.");refreshAll()}catch(x){toast(x.message)}});
$("visitForm").addEventListener("submit",async e=>{e.preventDefault();const o=formObject(e.target);o.patient_id=Number(o.patient_id);o.doctor_id=Number(o.doctor_id);try{await api("/api/visits",{method:"POST",body:JSON.stringify(o)});e.target.reset();toast("Visit record saved.");refreshAll()}catch(x){toast(x.message)}});
async function changeStatus(id,status){try{await api(`/api/appointments/${id}/status`,{method:"PATCH",body:JSON.stringify({status})});toast("Appointment updated.");refreshAll()}catch(e){toast(e.message)}}
refreshAll();
