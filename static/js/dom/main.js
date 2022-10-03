document.querySelectorAll('.modal').forEach(modal => {
    modal.addEventListener('shown.bs.modal', () => {
        modal.querySelector('.form-control').focus();
    });
});