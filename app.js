const STORAGE_KEY = 'static_checklists_v1'

function load(){
  const raw = localStorage.getItem(STORAGE_KEY)
  return raw? JSON.parse(raw) : []
}
function save(data){
  localStorage.setItem(STORAGE_KEY, JSON.stringify(data))
}

function renderList(){
  const container = document.getElementById('checklists-list')
  container.innerHTML = ''
  const data = load()
  if(!data.length) container.innerHTML = '<li>(nenhum checklist salvo)</li>'
  data.forEach((c, i)=>{
    const li = document.createElement('li')
    li.innerHTML = `<strong>${c.equipamento||'(sem equipamento)'}</strong> — ${c.local||''} <button data-i='${i}'>ver</button>`
    container.appendChild(li)
  })
  container.querySelectorAll('button').forEach(b=>b.addEventListener('click', e=>viewChecklist(e.target.dataset.i)))
}

function viewChecklist(i){
  const data = load()
  const c = data[i]
  if(!c) return
  document.getElementById('view-title').textContent = `Checklist #${i+1}`
  document.getElementById('view-meta').textContent = `Equip: ${c.equipamento || ''} — Local: ${c.local || ''} — Técnico: ${c.tecnico||''}`
  const items = document.getElementById('view-items')
  items.innerHTML = ''
  (c.items||[]).forEach(it=>{
    const li = document.createElement('li'); li.textContent = it; items.appendChild(li)
  })
  document.getElementById('list').classList.add('hidden')
  document.getElementById('new-checklist').classList.add('hidden')
  document.getElementById('view').classList.remove('hidden')
  // attach delete
  document.getElementById('delete-checklist').onclick = ()=>{ if(confirm('Deletar?')){ data.splice(i,1); save(data); renderList(); backView() } }
}

function backView(){
  document.getElementById('view').classList.add('hidden')
  document.getElementById('list').classList.remove('hidden')
  document.getElementById('new-checklist').classList.remove('hidden')
}

document.addEventListener('DOMContentLoaded', ()=>{
  renderList()
  document.getElementById('checklist-form').addEventListener('submit', e=>{
    e.preventDefault()
    const equipamento = document.getElementById('equipamento').value
    const local = document.getElementById('local').value
    const tecnico = document.getElementById('tecnico').value
    const items = document.getElementById('items').value.split('\n').map(s=>s.trim()).filter(s=>s)
    const data = load()
    data.unshift({equipamento, local, tecnico, items, created: new Date().toISOString()})
    save(data); renderList();
    e.target.reset()
  })
  document.getElementById('clear-data').addEventListener('click', ()=>{ if(confirm('Limpar todos os dados?')){ localStorage.removeItem(STORAGE_KEY); renderList() } })

  document.getElementById('back').addEventListener('click', backView)
  document.getElementById('download-all').addEventListener('click', ()=>{
    const blob = new Blob([JSON.stringify(load(), null, 2)], {type:'application/json'})
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a'); a.href = url; a.download='checklists.json'; document.body.appendChild(a); a.click(); a.remove(); URL.revokeObjectURL(url)
  })
  document.getElementById('import-json').addEventListener('click', ()=>{
    try{
      const raw = document.getElementById('import-area').value
      const parsed = JSON.parse(raw)
      if(!Array.isArray(parsed)) throw new Error('JSON deve ser um array de checklists')
      save(parsed); renderList(); alert('Importado com sucesso')
    }catch(err){ alert('Erro ao importar: '+err.message) }
  })
})
