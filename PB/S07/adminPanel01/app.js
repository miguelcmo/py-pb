// Datos en memoria
let tasks = [];
let editId = null;

// Elementos
const taskForm = document.getElementById('taskForm');
const employeeInput = document.getElementById('employee');
const projectInput = document.getElementById('project');
const descriptionInput = document.getElementById('description');
const durationInput = document.getElementById('duration');
const tasksList = document.getElementById('tasksList');
const filterProject = document.getElementById('filterProject');
const resetBtn = document.getElementById('resetBtn');

taskForm.addEventListener('submit', (e) => {
e.preventDefault();
const payload = {
    id: editId || Date.now().toString(),
    employee: employeeInput.value.trim(),
    project: projectInput.value.trim(),
    description: descriptionInput.value.trim(),
    duration: Number(durationInput.value),
    createdAt: new Date().toISOString()
};

if(editId){
    tasks = tasks.map(t => t.id === editId ? payload : t);
    editId = null;
    document.getElementById('saveBtn').textContent = 'Agregar tarea';
} else {
    tasks.push(payload);
}

// Lugar para integrar con backend:
// fetch('/api/tasks', { method: 'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload) })

renderTasks();
taskForm.reset();
durationInput.value = 1;
});

resetBtn.addEventListener('click', () => {
editId = null; taskForm.reset(); durationInput.value = 1; document.getElementById('saveBtn').textContent = 'Agregar tarea';
});

filterProject.addEventListener('input', renderTasks);

function renderTasks(){
const filter = filterProject.value.trim().toLowerCase();
if(tasks.length === 0){
    tasksList.innerHTML = '<div class="empty">No hay tareas registradas.</div>';
    return;
}
const filtered = filter ? tasks.filter(t => t.project.toLowerCase().includes(filter)) : tasks;
let html = '<table><thead><tr><th>Tarea</th><th>Empleado</th><th>Proyecto</th><th>Duración (hrs)</th><th>Creada</th><th></th></tr></thead><tbody>';
for(const t of filtered){
    html += `<tr>
    <td><div class="small">${escapeHtml(t.description || '-')}</div></td>
    <td>${escapeHtml(t.employee)}</td>
    <td><span class="pill">${escapeHtml(t.project)}</span></td>
    <td>${t.duration}</td>
    <td class="small">${new Date(t.createdAt).toLocaleString()}</td>
    <td class="actions">
        <button class="btn btn-ghost" onclick="editTask('${t.id}')">Editar</button>
        <button class="btn" style="background:var(--danger); color:#fff;" onclick="deleteTask('${t.id}')">Eliminar</button>
    </td>
    </tr>`;
}
html += '</tbody></table>';
tasksList.innerHTML = html;
}

function editTask(id){
const t = tasks.find(x => x.id === id);
if(!t) return alert('Registro no encontrado');
employeeInput.value = t.employee;
projectInput.value = t.project;
descriptionInput.value = t.description;
durationInput.value = t.duration;
editId = id;
document.getElementById('saveBtn').textContent = 'Guardar cambios';
window.scrollTo({top:0, behavior:'smooth'});
}

function deleteTask(id){
if(!confirm('¿Eliminar esta tarea?')) return;
tasks = tasks.filter(t => t.id !== id);
// fetch('/api/tasks/'+id, { method: 'DELETE' })
renderTasks();
}

function escapeHtml(unsafe){
    return String(unsafe).replace(/[&<>"']/g, (m) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":"&#039;"}[m]));
    }

// Demo inicial
// tasks.push({
// id: Date.now().toString(),
// employee: 'María López',
// project: 'Integración API',
// description: 'Configuración y pruebas iniciales',
// duration: 3,
// createdAt: new Date().toISOString()
// });

renderTasks();
