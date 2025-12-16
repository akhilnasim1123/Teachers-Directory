function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden'; // Prevent scrolling
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = ''; // Restore scrolling
    }
}

// Close modal if clicking outside content
document.addEventListener('click', function (event) {
    if (event.target.classList.contains('modal-overlay')) {
        event.target.classList.remove('active');
        document.body.style.overflow = '';
    }
});

// Helper to pre-select subjects in edit modal (if simple HTML is not enough)
// For this app, since we are doing SSR rendering for modals (via Django template context), 
// we might rely on Django rendering the form with values.
// However, the "Edit" button just opens a hidden div. We need those divs to be pre-filled.
// The easiest way for Detail page is to just render the specific teacher's update form in a hidden modal div.
