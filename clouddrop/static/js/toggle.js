document.addEventListener('DOMContentLoaded', function(){

    const close_btn = document.getElementById("close-btn")
    const menu = document.getElementById("toggle-menu")
    const toggle_trigger = document.getElementById("toggle-trigger")

    close_btn.addEventListener('click', () => close_menu(menu))
    toggle_trigger.addEventListener('click', () => show_menu(menu))

    

    console.log('toggle menu script loader')
});

function close_menu(menu){
    menu.style.display = 'none'
}

function show_menu(menu) {
    menu.style.display = 'flex'
}