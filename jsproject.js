// --------------------------
// SAMPLE MENU DATA
// --------------------------
const MENU = [
  {id:1,name:'Margherita Pizza',cat:'mains',price:12,veg:true,desc:'Classic pizza with tomato, mozzarella & basil',emoji:'🍕'},
  {id:2,name:'Garlic Bread',cat:'starters',price:6,veg:true,desc:'Toasted bread with garlic butter',emoji:'🥖'},
  {id:3,name:'Butter Chicken',cat:'mains',price:14,veg:false,desc:'Creamy spiced tomato gravy with tender chicken',emoji:'🍛'},
  {id:4,name:'Caesar Salad',cat:'starters',price:8,veg:false,desc:'Romaine, parmesan, croutons & Caesar dressing',emoji:'🥗'},
  {id:5,name:'Chocolate Lava Cake',cat:'dessert',price:7,veg:true,desc:'Warm molten cake with vanilla ice cream',emoji:'🍰'},
  {id:6,name:'Cold Brew',cat:'drinks',price:4,veg:true,desc:'Slow-brewed coffee, chilled',emoji:'🥤'},
  {id:7,name:'Paneer Tikka',cat:'starters',price:9,veg:true,desc:'Smoky grilled paneer with spices',emoji:'🧀'},
  {id:8,name:'Pepperoni Pizza',cat:'mains',price:13,veg:false,desc:'Pepperoni, cheese & tomato',emoji:'🍕'},
  {id:9,name:'Tiramisu',cat:'dessert',price:8,veg:true,desc:'Coffee-soaked ladyfingers & mascarpone',emoji:'☕'},
];

// --------------------------
// CART STATE
// --------------------------
let cart = JSON.parse(localStorage.getItem('delish_cart') || '[]');

// --------------------------
// DOM ELEMENTS
// --------------------------
const cartIcon = document.getElementById('cartIcon');
const cartCountEl  = document.getElementById('cartCount');
const cartDrawer   = document.getElementById('cartDrawer');
const cartListEl   = document.getElementById('cartItems');
const cartTotalEl  = document.getElementById('cartTotal');
const closeDrawerBtn = document.getElementById('closeCart');
const mobileMenuBtn = document.getElementById('mobile-menu');
const navLinks = document.getElementById('nav-links');
const themeBtn = document.getElementById('theme-toggle');

// --------------------------
// MENU RENDER
// --------------------------
function renderMenu(filter='all', vegOnly=false){
  const grid = document.getElementById('menu-grid');
  grid.innerHTML = '';

  const items = MENU.filter(i => 
    (filter === 'all' || i.cat === filter) &&
    (!vegOnly || i.veg)
  );

  items.forEach(it=>{
    const div = document.createElement('div');
    div.className = 'menu-item';
    div.innerHTML = `
      <div style="font-size:34px">${it.emoji}</div>
      <div class="meta">
        <h4>${it.name} <span class="muted" style="font-weight:600;font-size:13px">${it.veg?'• veg':''}</span></h4>
        <div class="muted" style="font-size:13px">${it.desc}</div>
      </div>
      <div style="text-align:right">
        <div class="price">$${it.price.toFixed(2)}</div>
        <div style="margin-top:8px">
          <button class="ghost" onclick="openDetails(${it.id})">Details</button>
          <button class="add" onclick="addToCart(${it.id})">Add</button>
        </div>
      </div>
    `;
    grid.appendChild(div);
  });
}

renderMenu();

// --------------------------
// MENU FILTERS
// --------------------------
document.querySelectorAll('.chip').forEach(ch => {
  ch.addEventListener('click', () => {
    document.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
    ch.classList.add('active');
    renderMenu(ch.dataset.type, document.getElementById('veg-only').checked);
  });
});

document.getElementById('veg-only').addEventListener('change', (e) => {
  const active = document.querySelector('.chip.active');
  renderMenu(active.dataset.type, e.target.checked);
});

// --------------------------
// CART FUNCTIONS
// --------------------------
function saveCart(){
  localStorage.setItem('delish_cart', JSON.stringify(cart));
  renderCart();
}

function addToCart(id){
  const item = MENU.find(m=>m.id===id);
  const exists = cart.find(c=>c.id===id);

  if(exists){
    exists.qty++;
  } else {
    cart.push({id:item.id,name:item.name,price:item.price,qty:1});
  }

  saveCart();
  openCart();
}

function renderCart(){
  cartListEl.innerHTML = '';
  if(cart.length === 0){
    cartListEl.innerHTML = '<div class="cart-empty">Your cart is empty</div>';
    cartCountEl.textContent = '0';
    cartTotalEl.textContent = '0.00';
    return;
  }

  let total = 0;
  cart.forEach(it=>{
    total += it.price * it.qty;
    const el = document.createElement('div');
    el.className = 'cart-item';
    el.innerHTML = `
      <div>
        <strong>${it.name}</strong>
        <div class="muted">$${it.price.toFixed(2)} each</div>
      </div>
      <div style="text-align:right">
        <div class="qty">
          <button class="icon-btn" onclick="changeQty(${it.id},-1)">-</button>
          <div style="min-width:22px;text-align:center">${it.qty}</div>
          <button class="icon-btn" onclick="changeQty(${it.id},1)">+</button>
        </div>
        <div style="margin-top:8px">$${(it.price * it.qty).toFixed(2)}</div>
        <button class="ghost" style="margin-top:8px" onclick="removeItem(${it.id})">Remove</button>
      </div>
    `;
    cartListEl.appendChild(el);
  });

  cartCountEl.textContent = cart.reduce((s,i)=>s+i.qty, 0);
  cartTotalEl.textContent = total.toFixed(2);
}

function changeQty(id, delta){
  const it = cart.find(c=>c.id===id);
  if(!it) return;
  it.qty += delta;
  if(it.qty <= 0) cart = cart.filter(c => c.id !== id);
  saveCart();
}

function removeItem(id){
  cart = cart.filter(c=>c.id!==id);
  saveCart();
}

function openCart(){
  cartDrawer.classList.add('open');
  renderCart();
}

cartIcon.addEventListener('click', openCart);
closeDrawerBtn.addEventListener('click', ()=> cartDrawer.classList.remove('open'));

// --------------------------
// MODAL (ITEM DETAILS)
// --------------------------
function openDetails(id){
  const m = MENU.find(x=>x.id===id);
  const modal = document.getElementById('modal-content');
  modal.innerHTML = `
    <div style="display:flex;gap:12px">
      <div style="font-size:46px">${m.emoji}</div>
      <div>
        <h3>${m.name}</h3>
        <p class='muted'>${m.desc}</p>
        <p style='font-weight:900'>$${m.price.toFixed(2)}</p>
        <div style='margin-top:10px'>
          <button class='add' onclick='addToCart(${m.id}); closeModal();'>Add to cart</button>
        </div>
      </div>
    </div>
  `;
  document.getElementById('modal-back').style.display = 'flex';
}

function closeModal(){
  document.getElementById('modal-back').style.display = 'none';
}

document.getElementById('modal-back').addEventListener('click', (e)=>{
  if(e.target.id==='modal-back') closeModal();
});
document.getElementById('close-modal').addEventListener('click', closeModal);

// --------------------------
// THEME TOGGLE
// --------------------------
themeBtn.addEventListener('click', ()=>{
  if(document.documentElement.getAttribute('data-theme')==='dark'){
    document.documentElement.removeAttribute('data-theme');
    localStorage.removeItem('delish_theme');
  } else {
    document.documentElement.setAttribute('data-theme','dark');
    localStorage.setItem('delish_theme','dark');
  }
});

if(localStorage.getItem('delish_theme')==='dark'){
  document.documentElement.setAttribute('data-theme','dark');
}

// --------------------------
// MOBILE MENU TOGGLE
// --------------------------
mobileMenuBtn.addEventListener('click', () => {
  navLinks.classList.toggle('open'); // toggle the 'open' class
});


// --------------------------
// EXPOSE FUNCTIONS GLOBALLY
// --------------------------
window.addToCart = addToCart;
window.openCart = openCart;
window.closeModal = closeModal;
