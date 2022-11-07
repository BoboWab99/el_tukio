document.querySelectorAll('.modal').forEach(modal => {
    if (modal.querySelector('.form-control')) {
        modal.addEventListener('shown.bs.modal', () => {
            modal.querySelector('.form-control').focus();
        });
    }
});