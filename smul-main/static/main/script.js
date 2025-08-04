const loginMenu = document.querySelector('.menu-item[data-key="login"]');
if (loginMenu) {
    loginMenu.textContent = 'LOGIN';
    loginMenu.removeAttribute('onclick');
    loginMenu.addEventListener('click', () => {
        const redirect_uri = window.location.origin + "/handle-token/";
        window.location.href = `http://127.0.0.1:8001/login/?redirect_uri=${redirect_uri}`;
    });
}
