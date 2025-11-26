const KEY = 'koru_products_v1';
let products = JSON.parse(localStorage.getItem(KEY) || '[]');
let currentView = 'cards';

const productsContainer = document.getElementById('productsContainer');
const search = document.getElementById('search');
const btnTable = document.getElementById('btnTable');
const btnCards = document.getElementById('btnCards');

document.getElementById('productForm').addEventListener('submit', (e)=>{
  e.preventDefault();
  const id = Date.now().toString();
  const name = document.getElementById('pName').value.trim();
  const ref = document.getElementById('pRef').value.trim();
  const qty = Number(document.getElementById('pQty').value);
  const photo = document.getElementById('pPhoto').value.trim();
  products.push({id,name,ref,qty,photo});
  localStorage.setItem(KEY, JSON.stringify(products));
  const modal = bootstrap.Modal.getInstance(document.getElementById('productModal'));
  modal.hide();
  e.target.reset();
  renderProducts();
});

document.getElementById('moveForm').addEventListener('submit', (e)=>{
  e.preventDefault();
  const id = document.getElementById('mProductId').value;
  const type = document.getElementById('mType').value;
  const qty = Number(document.getElementById('mQty').value);
  const product = products.find(p=>p.id===id);
  if(!product) return alert('Producto no encontrado');
  if(type === 'out' && product.qty < qty) return alert('Cantidad insuficiente');
  product.qty += (type === 'in' ? qty : -qty);
  localStorage.setItem(KEY, JSON.stringify(products));
  bootstrap.Modal.getInstance(document.getElementById('moveModal')).hide();
  renderProducts();
});

btnTable.addEventListener('click', ()=>{ currentView='table'; renderProducts(); });
btnCards.addEventListener('click', ()=>{ currentView='cards'; renderProducts(); });
search.addEventListener('input', renderProducts);

function renderProducts(){
  const q = search.value.trim().toLowerCase();
  const list = products.filter(p => p.name.toLowerCase().includes(q) || p.ref.toLowerCase().includes(q));
  if(list.length === 0){ productsContainer.innerHTML = '<div class="alert alert-secondary">No hay productos</div>'; return; }

  if(currentView === 'table'){
    let html = '<table class="table table-striped"><thead><tr><th>Foto</th><th>Producto</th><th>Referencia</th><th>Cantidad</th><th>Acciones</th></tr></thead><tbody>';
    for(const p of list){
      const stockClass = p.qty <= 2 ? 'stock-low' : 'stock-ok';
      html += `<tr>
        <td style="width:120px"><img src="${p.photo || 'https://via.placeholder.com/120x80?text=Producto'}" style="width:120px; height:80px; object-fit:cover; border-radius:6px" /></td>
        <td>${escapeHtml(p.name)}</td>
        <td>${escapeHtml(p.ref)}</td>
        <td class="${stockClass}">${p.qty}</td>
        <td>
          <button class="btn btn-sm btn-outline-primary" onclick="openMove('${p.id}')">Movimiento</button>
          <button class="btn btn-sm btn-outline-danger" onclick="deleteProduct('${p.id}')">Eliminar</button>
        </td>
      </tr>`;
    }
    html += '</tbody></table>';
    productsContainer.innerHTML = html;
  } else {
    let html = '<div class="row">';
    for(const p of list){
      const stockClass = p.qty <= 2 ? 'stock-low' : 'stock-ok';
      html += `<div class="col-md-4 mb-3">
        <div class="card card-product">
          <img src="${p.photo || 'https://via.placeholder.com/400x250?text=Producto'}" class="card-img-top" alt="${escapeHtml(p.name)}">
          <div class="card-body">
            <h5 class="card-title">${escapeHtml(p.name)}</h5>
            <p class="card-text small">Ref: ${escapeHtml(p.ref)}</p>
            <p class="${stockClass}">Cantidad: ${p.qty}</p>
            <div class="d-flex gap-2">
              <button class="btn btn-sm btn-outline-primary" onclick="openMove('${p.id}')">Movimiento</button>
              <button class="btn btn-sm btn-outline-danger" onclick="deleteProduct('${p.id}')">Eliminar</button>
            </div>
          </div>
        </div>
      </div>`;
    }
    html += '</div>';
    productsContainer.innerHTML = html;
  }
}

function openMove(id){
  document.getElementById('mProductId').value = id;
  document.getElementById('mQty').value = 1;
  document.getElementById('mNote').value = '';
  const modal = new bootstrap.Modal(document.getElementById('moveModal'));
  modal.show();
}

function deleteProduct(id){
  if(!confirm('Eliminar producto?')) return;
  products = products.filter(p=>p.id !== id);
  localStorage.setItem(KEY, JSON.stringify(products));
  renderProducts();
}

function escapeHtml(unsafe){
  return String(unsafe).replace(/[&<>"']/g, (m) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":"&#039;"}[m]));
}

// Demo
if(products.length === 0){
  products = [
    {id:'p1', name:'Camiseta básica', ref:'CB-001', qty:10, photo:''},
    {id:'p2', name:'Taza cerámica', ref:'TZ-122', qty:2, photo:''},
    {id:'p3', name:'Libreta A5', ref:'LB-55', qty:5, photo:''}
  ];
  localStorage.setItem(KEY, JSON.stringify(products));
}
renderProducts();

// funciones globales
window.openMove = openMove;
window.deleteProduct = deleteProduct;
window.renderProducts = renderProducts;
